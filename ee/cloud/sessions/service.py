"""Sessions domain — business logic service."""

from __future__ import annotations

import logging
import uuid
from datetime import UTC, datetime

from beanie import PydanticObjectId

from ee.cloud.models.session import Session
from ee.cloud.sessions.schemas import (
    CreateSessionRequest,
    UpdateSessionRequest,
)
from ee.cloud.shared.errors import Forbidden, NotFound
from ee.cloud.shared.events import event_bus

logger = logging.getLogger(__name__)


def _session_response(session: Session) -> dict:
    """Build a frontend-compatible dict from a Session document."""
    return {
        "_id": str(session.id),
        "sessionId": session.sessionId,
        "workspace": session.workspace,
        "owner": session.owner,
        "title": session.title,
        "pocket": session.pocket,
        "group": session.group,
        "agent": session.agent,
        "messageCount": session.messageCount,
        "lastActivity": session.lastActivity.isoformat() if session.lastActivity else None,
        "createdAt": session.createdAt.isoformat() if session.createdAt else None,
        "deletedAt": session.deleted_at.isoformat() if session.deleted_at else None,
    }


class SessionService:
    """Stateless service encapsulating session business logic."""

    # -----------------------------------------------------------------
    # CRUD
    # -----------------------------------------------------------------

    @staticmethod
    async def create(
        workspace_id: str, user_id: str, body: CreateSessionRequest
    ) -> dict:
        """Create a session. Optionally link to a pocket on creation."""
        session = Session(
            sessionId=str(uuid.uuid4()),
            workspace=workspace_id,
            owner=user_id,
            title=body.title,
            pocket=body.pocket_id,
            group=body.group_id,
            agent=body.agent_id,
        )
        await session.insert()

        await event_bus.emit(
            "session.created",
            {
                "session_id": str(session.id),
                "session_uuid": session.sessionId,
                "workspace_id": workspace_id,
                "owner_id": user_id,
                "pocket_id": body.pocket_id,
            },
        )

        return _session_response(session)

    @staticmethod
    async def list_sessions(
        workspace_id: str, user_id: str
    ) -> list[dict]:
        """List sessions for user in workspace, exclude deleted, sort by lastActivity desc.

        Also syncs any runtime sessions that exist in file memory but
        not yet in MongoDB (e.g. sessions created before cloud persistence).
        """
        # Sync runtime sessions to cloud
        await SessionService._sync_runtime_sessions(workspace_id, user_id)

        sessions = (
            await Session.find(
                Session.workspace == workspace_id,
                Session.owner == user_id,
                Session.deleted_at == None,  # noqa: E711
            )
            .sort(-Session.lastActivity)
            .to_list()
        )
        return [_session_response(s) for s in sessions]

    @staticmethod
    async def get(session_id: str, user_id: str) -> dict:
        """Get a session by _id or sessionId. Verify owner."""
        session = await SessionService._get_session(session_id, user_id)
        return _session_response(session)

    @staticmethod
    async def update(
        session_id: str, user_id: str, body: UpdateSessionRequest
    ) -> dict:
        """Update session fields. Owner only."""
        session = await SessionService._get_session(session_id, user_id)

        if body.title is not None:
            session.title = body.title
        if body.pocket_id is not None:
            session.pocket = body.pocket_id

        await session.save()
        return _session_response(session)

    @staticmethod
    async def delete(session_id: str, user_id: str) -> None:
        """Soft-delete a session via deleted_at. Owner only."""
        session = await SessionService._get_session(session_id, user_id)
        session.deleted_at = datetime.now(UTC)
        await session.save()

    # -----------------------------------------------------------------
    # Pocket-scoped helpers
    # -----------------------------------------------------------------

    @staticmethod
    async def list_for_pocket(
        pocket_id: str, user_id: str
    ) -> list[dict]:
        """Find sessions where pocket == pocket_id."""
        sessions = (
            await Session.find(
                Session.pocket == pocket_id,
                Session.owner == user_id,
                Session.deleted_at == None,  # noqa: E711
            )
            .sort(-Session.lastActivity)
            .to_list()
        )
        return [_session_response(s) for s in sessions]

    @staticmethod
    async def create_for_pocket(
        workspace_id: str,
        user_id: str,
        pocket_id: str,
        body: CreateSessionRequest,
    ) -> dict:
        """Create a session with pocket already set."""
        body_with_pocket = CreateSessionRequest(
            title=body.title,
            pocket_id=pocket_id,
            group_id=body.group_id,
            agent_id=body.agent_id,
        )
        return await SessionService.create(workspace_id, user_id, body_with_pocket)

    # -----------------------------------------------------------------
    # Runtime proxy
    # -----------------------------------------------------------------

    @staticmethod
    async def get_history(session_id: str, user_id: str) -> dict:
        """Get session chat history.

        Checks two sources:
        1. MongoDB Messages collection (cloud group chat)
        2. Runtime file-based memory (dashboard WebSocket chat)

        Returns whichever has messages.
        """
        session = await SessionService._get_session(session_id, user_id)

        # 1. Try cloud Messages (group chat)
        if session.group:
            try:
                from ee.cloud.models.message import Message

                messages = (
                    await Message.find(
                        Message.group == session.group,
                        Message.deleted == False,  # noqa: E711
                    )
                    .sort("createdAt")
                    .limit(100)
                    .to_list()
                )
                if messages:
                    return {
                        "messages": [
                            {
                                "_id": str(m.id),
                                "role": "assistant" if m.sender_type == "agent" else "user",
                                "content": m.content,
                                "sender": m.sender,
                                "senderType": m.sender_type,
                                "createdAt": m.createdAt.isoformat() if m.createdAt else None,
                            }
                            for m in messages
                        ]
                    }
            except Exception:
                logger.debug("Cloud message lookup failed for session %s", session.sessionId)

        # 2. Try runtime file-based memory
        try:
            from pocketpaw.memory.manager import MemoryManager

            manager = MemoryManager()
            # Try multiple key formats: the sessionId, with colon, with underscore
            sid = session.sessionId
            keys_to_try = [
                sid,                              # as-is
                sid.replace("_", ":", 1),          # websocket_abc → websocket:abc
                f"websocket:{sid}",               # prefix with websocket:
            ]
            for key in keys_to_try:
                try:
                    entries = await manager.get_session_history(key)
                    if entries:
                        return {"messages": entries}
                except Exception:
                    continue
        except Exception:
            logger.debug("Runtime memory lookup failed for session %s", session.sessionId)

        return {"messages": []}

    # -----------------------------------------------------------------
    # Touch (activity tracking)
    # -----------------------------------------------------------------

    @staticmethod
    async def touch(session_id: str) -> None:
        """Update lastActivity and increment messageCount."""
        session = await Session.find_one(Session.sessionId == session_id)
        if session:
            session.lastActivity = datetime.now(UTC)
            session.messageCount += 1
            await session.save()

    # -----------------------------------------------------------------
    # Internal helpers
    # -----------------------------------------------------------------

    @staticmethod
    @staticmethod
    async def _sync_runtime_sessions(workspace_id: str, user_id: str) -> None:
        """Import runtime file-memory sessions that don't exist in MongoDB yet.

        Reads ~/.pocketpaw/memory/sessions/_index.json for the runtime's
        session index and creates cloud Session documents for any missing.
        """
        try:
            import json
            from pocketpaw.config import get_config_dir

            index_path = get_config_dir() / "memory" / "sessions" / "_index.json"
            if not index_path.exists():
                return

            index = json.loads(index_path.read_text(encoding="utf-8"))

            # Get existing cloud session IDs
            existing = await Session.find(
                Session.workspace == workspace_id,
                Session.owner == user_id,
            ).to_list()
            existing_ids = {s.sessionId for s in existing}

            for session_key, meta in index.items():
                if session_key.startswith("_"):
                    continue
                # Normalize key: "websocket:abc" → "websocket_abc"
                session_id = session_key.replace(":", "_")
                if session_id in existing_ids or session_key in existing_ids:
                    continue

                title = meta.get("user_title") or meta.get("title") or session_key
                last_activity = meta.get("last_activity")

                session = Session(
                    sessionId=session_id,
                    workspace=workspace_id,
                    owner=user_id,
                    title=title[:100],
                    messageCount=meta.get("message_count", 0),
                )
                # Set lastActivity from index
                if last_activity:
                    try:
                        session.lastActivity = datetime.fromisoformat(last_activity)
                    except Exception:
                        pass

                await session.insert()
                logger.debug("Synced runtime session: %s → %s", session_id, title[:40])
        except Exception:
            # Non-fatal
            logger.debug("Runtime session sync failed", exc_info=True)

    @staticmethod
    async def _get_session(session_id: str, user_id: str) -> Session:
        """Fetch by ObjectId first, then by sessionId. Verify owner."""
        session = None
        try:
            session = await Session.get(PydanticObjectId(session_id))
        except Exception:
            session = await Session.find_one(Session.sessionId == session_id)

        if not session or session.deleted_at:
            raise NotFound("session", session_id)
        if session.owner != user_id:
            raise Forbidden("session.not_owner", "Not the session owner")
        return session
