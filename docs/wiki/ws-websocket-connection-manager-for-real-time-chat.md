# ws — WebSocket connection manager for real-time chat

> Manages WebSocket lifecycle, user presence tracking, and message routing for real-time chat. Handles multi-device/tab connections per user, typing indicators with auto-expiry, and group broadcast messaging with optional user exclusion.

**Categories:** real-time communication, WebSocket, chat infrastructure, connection management  
**Concepts:** ConnectionManager, WebSocket lifecycle, User-to-connections mapping, Group message broadcasting, Typing indicators, Presence tracking, Grace period, Multi-device support, Dead connection cleanup, Singleton pattern  
**Words:** 468 | **Version:** 1

---

## Purpose

This module provides a centralized connection manager for WebSocket-based real-time chat in a cloud environment. It acts as the state container for all active WebSocket connections, enabling efficient message routing, presence detection, and typing indicators across multiple concurrent connections per user.

## Architecture

**Single WebSocket Endpoint:** `ws://host/ws/cloud?token=<JWT>`

**Connection Lifecycle:**
- Authenticate via JWT token
- Register connection in `ConnectionManager`
- Route messages bidirectionally
- Clean up on disconnect with grace period for offline detection

## Key Classes

### ConnectionManager

Singleton that manages all active WebSocket connections and derived state.

**State:**
- `active_connections: dict[str, set[WebSocket]]` — user_id to set of concurrent connections (multi-tab/device support)
- `_ws_to_user: dict[WebSocket, str]` — reverse lookup for connection ownership
- `_offline_tasks: dict[str, asyncio.Task]` — grace-period timers before marking users offline
- `_typing_timers: dict[tuple[str, str], asyncio.Task]` — auto-expiring typing indicators

**Connection Lifecycle Methods:**
- `connect(websocket, user_id)` — Register authenticated connection; cancel any pending offline task
- `disconnect(websocket)` — Remove connection; return user_id if last connection (caller starts grace period)
- `get_user_connections(user_id)` — Retrieve all active WebSocket connections for a user
- `is_online(user_id)` — Boolean check for active connection presence

**Message Routing:**
- `send_to_user(user_id, message)` — Send message to all connections of a user; auto-cleanup dead connections
- `broadcast_to_group(group_id, member_ids, message, exclude_user)` — Send message to online group members with optional sender exclusion

**Typing Indicators:**
- `start_typing(group_id, user_id)` — Begin typing tracking with 5-second auto-expiry
- `stop_typing(group_id, user_id)` — Explicitly end typing indicator
- `is_typing(group_id, user_id)` — Check active typing status
- `_typing_timeout(key)` — Internal coroutine for auto-expiry after TYPING_TIMEOUT_SECONDS

## Constants

- `TYPING_TIMEOUT_SECONDS = 5` — Auto-expire typing indicators
- `PRESENCE_GRACE_SECONDS = 30` — Grace period before marking user offline (allows quick reconnect on network flap)

## Dependencies

**Internal:**
- `ee.cloud.chat.schemas.WsOutbound` — outbound message schema (Pydantic model)

**External:**
- `fastapi.WebSocket` — FastAPI WebSocket connection object
- `asyncio` — async task and event loop management
- `logging` — activity logging

## Usage Examples

```python
from ee.cloud.chat.ws import manager

# Register connection
await manager.connect(websocket, user_id="user123")

# Send message to user across all devices
from ee.cloud.chat.schemas import WsOutbound
message = WsOutbound(type="chat", data={...})
await manager.send_to_user("user123", message)

# Broadcast to group (excluding sender)
await manager.broadcast_to_group(
    group_id="group456",
    member_ids=["user1", "user2", "user3"],
    message=message,
    exclude_user="user1"
)

# Track typing
manager.start_typing("group456", "user1")
if manager.is_typing("group456", "user1"):
    print("User is typing...")

# Disconnect with grace period
user_id = await manager.disconnect(websocket)
if user_id:  # Last connection removed
    # Start grace period timer in calling router
    pass
```

## Integration Points

**Used by:**
- `router` — WebSocket route handlers
- `agent_bridge` — Agent message forwarding

**Imports:**
- `schemas` — Message type definitions

## Design Patterns

- **Singleton Pattern** — Module-level `manager` instance for global state
- **Grace Period Pattern** — Deferred offline detection allows mobile reconnection scenarios
- **Auto-Expiry** — Typing timers use asyncio.Task cancellation for cleanup
- **Dead Connection Cleanup** — Failed sends trigger immediate connection removal

---

## Related

- [schemas-workspace-domain-requestresponse-models](schemas-workspace-domain-requestresponse-models.md)
- [router-workspace-domain-fastapi-endpoints](router-workspace-domain-fastapi-endpoints.md)
- [agentbridge-cloud-chat-event-bridge-to-pocketpaw-agent-pool](agentbridge-cloud-chat-event-bridge-to-pocketpaw-agent-pool.md)
