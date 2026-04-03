"""Socket.IO server for real-time group chat, presence, and typing indicators.

Mounted on the FastAPI app as an ASGI sub-application at /ws/chat.
Uses python-socketio with async mode.

Events:
  Client → Server:
    - authenticate { token }       → validate JWT, join user rooms
    - join_group { group_id }      → join Socket.IO room for a group
    - leave_group { group_id }     → leave group room
    - send_message { group_id, content, mentions?, reply_to?, attachments? }
    - typing { group_id }          → broadcast typing indicator
    - stop_typing { group_id }

  Server → Client:
    - authenticated { user_id, email, name }
    - auth_error { detail }
    - new_message { message }      → broadcast to group room
    - message_edited { message }
    - message_deleted { message_id, group_id }
    - typing { group_id, user_id, name }
    - user_joined { group_id, user_id }
    - user_left { group_id, user_id }
    - presence { user_id, status }
"""

from __future__ import annotations

import logging
from typing import Any

import socketio

logger = logging.getLogger(__name__)

# Create async Socket.IO server
sio = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins="*",
    logger=False,
    engineio_logger=False,
)

# Track authenticated users: sid → { user_id, email, name }
_sessions: dict[str, dict[str, str]] = {}


def _get_room_sids(room: str) -> list[str]:
    """Get all SIDs in a Socket.IO room."""
    try:
        return list(sio.manager.rooms.get("/", {}).get(room, set()))
    except Exception:
        return []


async def _get_user_from_token(token: str):
    """Validate JWT and return User or None."""
    try:
        from ee.cloud.auth import get_jwt_strategy, get_user_manager, get_user_db
        from fastapi_users_db_beanie import BeanieUserDatabase
        from ee.cloud.models.user import User, OAuthAccount
        from ee.cloud.auth import UserManager

        strategy = get_jwt_strategy()
        # Decode the token manually
        import jwt as pyjwt
        import os
        secret = os.environ.get("AUTH_SECRET", "change-me-in-production-please")
        payload = pyjwt.decode(token, secret, algorithms=["HS256"], audience=["fastapi-users:auth"])
        user_id = payload.get("sub")
        if not user_id:
            return None
        from beanie import PydanticObjectId
        user = await User.get(PydanticObjectId(user_id))
        return user
    except Exception as exc:
        logger.debug("Socket.IO auth failed: %s", exc)
        return None


# ---------------------------------------------------------------------------
# Connection lifecycle
# ---------------------------------------------------------------------------

@sio.event
async def connect(sid, environ, auth):
    """Client connected — not authenticated yet."""
    logger.debug("Socket.IO connect: %s", sid)


@sio.event
async def disconnect(sid):
    """Client disconnected — clean up."""
    session = _sessions.pop(sid, None)
    if session:
        # Broadcast offline status
        await sio.emit("presence", {
            "user_id": session["user_id"],
            "status": "offline",
        })
    logger.debug("Socket.IO disconnect: %s (user=%s)", sid, session.get("user_id") if session else "?")


# ---------------------------------------------------------------------------
# Authentication
# ---------------------------------------------------------------------------

@sio.event
async def authenticate(sid, data):
    """Authenticate with JWT token after connecting."""
    token = data.get("token", "") if isinstance(data, dict) else ""
    if not token:
        await sio.emit("auth_error", {"detail": "Token required"}, to=sid)
        return

    user = await _get_user_from_token(token)
    if not user:
        await sio.emit("auth_error", {"detail": "Invalid token"}, to=sid)
        return

    _sessions[sid] = {
        "user_id": str(user.id),
        "email": user.email,
        "name": user.full_name or user.email,
    }

    await sio.emit("authenticated", {
        "user_id": str(user.id),
        "email": user.email,
        "name": user.full_name or user.email,
    }, to=sid)

    # Broadcast online status
    await sio.emit("presence", {
        "user_id": str(user.id),
        "status": "online",
    })

    logger.info("Socket.IO authenticated: %s (%s)", user.email, sid)


def _require_auth(sid: str) -> dict[str, str] | None:
    """Get session for authenticated user, or None."""
    return _sessions.get(sid)


# ---------------------------------------------------------------------------
# Group rooms
# ---------------------------------------------------------------------------

@sio.event
async def join_group(sid, data):
    """Join a group's Socket.IO room."""
    session = _require_auth(sid)
    if not session:
        await sio.emit("auth_error", {"detail": "Not authenticated"}, to=sid)
        return

    group_id = data.get("group_id", "") if isinstance(data, dict) else ""
    if not group_id:
        return

    room = f"group:{group_id}"
    sio.enter_room(sid, room)

    # Log who's in the room now
    participants = sio.manager.get_participants("/", room)
    logger.info("ROOM %s — %s joined (sid=%s). Participants: %s",
        room, session["email"], sid,
        [(s, _sessions.get(s, {}).get("email", "?")) for s in _get_room_sids(room)])

    await sio.emit("user_joined", {
        "group_id": group_id,
        "user_id": session["user_id"],
        "name": session["name"],
    }, room=room, skip_sid=sid)


@sio.event
async def leave_group(sid, data):
    """Leave a group's Socket.IO room."""
    session = _require_auth(sid)
    if not session:
        return

    group_id = data.get("group_id", "") if isinstance(data, dict) else ""
    if not group_id:
        return

    room = f"group:{group_id}"
    sio.leave_room(sid, room)

    await sio.emit("user_left", {
        "group_id": group_id,
        "user_id": session["user_id"],
    }, room=room)


# ---------------------------------------------------------------------------
# Messaging
# ---------------------------------------------------------------------------

@sio.event
async def send_message(sid, data):
    """Send a message to a group — persists to DB and broadcasts."""
    session = _require_auth(sid)
    if not session:
        await sio.emit("auth_error", {"detail": "Not authenticated"}, to=sid)
        return

    if not isinstance(data, dict):
        return

    group_id = data.get("group_id", "")
    content = data.get("content", "").strip()
    if not group_id or not content:
        return
    if len(content) > 10_000:
        await sio.emit("error", {"detail": "Message too long"}, to=sid)
        return

    # Verify membership + not archived
    from ee.cloud.models.group import Group
    from beanie import PydanticObjectId
    try:
        group = await Group.get(PydanticObjectId(group_id))
    except Exception:
        group = None
    if not group or group.archived:
        await sio.emit("error", {"detail": "Group not found or archived"}, to=sid)
        return
    if session["user_id"] not in group.members:
        await sio.emit("error", {"detail": "Not a member of this group"}, to=sid)
        return

    # Persist to MongoDB
    from ee.cloud.models.message import Message, Mention, Attachment

    mentions = [Mention(**m) for m in data.get("mentions", []) if isinstance(m, dict)]
    attachments = [Attachment(**a) for a in data.get("attachments", []) if isinstance(a, dict)]

    msg = Message(
        group=group_id,
        sender=session["user_id"],
        sender_type="user",
        content=content,
        mentions=mentions,
        reply_to=data.get("reply_to"),
        attachments=attachments,
    )
    await msg.insert()

    # Broadcast to room (skip sender — they add it locally)
    msg_data = msg.model_dump(mode="json")
    msg_data["_id"] = str(msg.id)
    msg_data["sender_name"] = session["name"]

    room = f"group:{group_id}"
    room_sids = _get_room_sids(room)
    room_users = [(s, _sessions.get(s, {}).get("email", "?")) for s in room_sids]
    logger.info("BROADCAST to %s (skip sender %s). Room has %d members: %s",
        room, sid, len(room_sids), room_users)

    await sio.emit("new_message", msg_data, room=room, skip_sid=sid)

    # Confirm to sender with the persisted message (so they get the real _id)
    await sio.emit("message_sent", msg_data, to=sid)


# ---------------------------------------------------------------------------
# Typing indicators
# ---------------------------------------------------------------------------

@sio.event
async def typing(sid, data):
    """Broadcast typing indicator to group."""
    session = _require_auth(sid)
    if not session:
        return

    group_id = data.get("group_id", "") if isinstance(data, dict) else ""
    if not group_id:
        return

    await sio.emit("typing", {
        "group_id": group_id,
        "user_id": session["user_id"],
        "name": session["name"],
    }, room=f"group:{group_id}", skip_sid=sid)


@sio.event
async def stop_typing(sid, data):
    """Broadcast stop typing to group."""
    session = _require_auth(sid)
    if not session:
        return

    group_id = data.get("group_id", "") if isinstance(data, dict) else ""
    if not group_id:
        return

    await sio.emit("stop_typing", {
        "group_id": group_id,
        "user_id": session["user_id"],
    }, room=f"group:{group_id}", skip_sid=sid)


# ---------------------------------------------------------------------------
# ASGI app — mount on FastAPI
# ---------------------------------------------------------------------------

# Create the ASGI app that wraps the Socket.IO server
def wrap_asgi_app(fastapi_app):
    """Wrap a FastAPI app with Socket.IO ASGI middleware.

    This is the correct pattern per python-socketio docs:
    Socket.IO wraps FastAPI (not the other way around).
    Socket.IO handles /socket.io/ requests, everything else goes to FastAPI.
    """
    return socketio.ASGIApp(sio, other_app=fastapi_app)
