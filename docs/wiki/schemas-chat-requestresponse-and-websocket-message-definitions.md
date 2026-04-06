# schemas — Chat request/response and WebSocket message definitions

> This module defines Pydantic-based request, response, and WebSocket message schemas for the chat subsystem. It provides type-safe contracts for REST API endpoints and real-time WebSocket communication, including group management, messaging, and presence features.

**Categories:** chat, schemas, api-contracts, websocket, messaging  
**Concepts:** CreateGroupRequest, UpdateGroupRequest, AddGroupMembersRequest, AddGroupAgentRequest, UpdateGroupAgentRequest, SendMessageRequest, EditMessageRequest, ReactRequest, MessageResponse, GroupResponse  
**Words:** 280 | **Version:** 1

---

## Purpose
Provide centralized schema definitions for chat operations across REST and WebSocket protocols, enabling request validation, response serialization, and type safety throughout the chat service layer.

## Key Classes/Functions

### REST Request Schemas
- **CreateGroupRequest**: Group creation with name, description, type (public/private/dm), members, icon, and color
- **UpdateGroupRequest**: Partial group updates (name, description, icon, color)
- **AddGroupMembersRequest**: Add users to existing group
- **AddGroupAgentRequest**: Add AI agent with role and respond_mode
- **UpdateGroupAgentRequest**: Update agent respond_mode
- **SendMessageRequest**: Message with content (1-10k chars), reply threading, mentions, attachments
- **EditMessageRequest**: Edit existing message content
- **ReactRequest**: Emoji reaction (1-50 chars)

### REST Response Schemas
- **MessageResponse**: Complete message object with sender, timestamps, reactions, edit/delete status
- **GroupResponse**: Group metadata including members, agents, pinned messages, archives status
- **CursorPage**: Pagination wrapper with items, next_cursor, and has_more flag

### WebSocket Schemas
- **WsInbound**: Validated client→server messages with 8 operation types (message.send, message.edit, message.delete, message.react, typing.start, typing.stop, presence.update, read.ack)
- **WsOutbound**: Generic server→client envelope with type and data payload

## Dependencies
- `pydantic.BaseModel`: Model base class
- `pydantic.Field`: Field constraints (min/max length, defaults)
- `datetime`: Timestamp fields
- `typing`: Type hints (Literal, Any)

## Usage Examples
```python
# Request validation
req = CreateGroupRequest(name="engineering", type="private", member_ids=["user1", "user2"])

# Response serialization
msg_resp = MessageResponse(
    id="msg123",
    group="group456",
    sender="user1",
    sender_type="user",
    content="Hello",
    mentions=[],
    reply_to=None,
    attachments=[],
    reactions=[],
    edited=False,
    edited_at=None,
    deleted=False,
    created_at=datetime.now()
)

# WebSocket handling
ws_msg = WsInbound(type="message.send", group_id="g1", content="Hi")
response = WsOutbound(type="message.created", data={"id": "m123"})
```

## Patterns
- Field constraints for security (length limits on content)
- Optional fields for partial updates
- Type unions for nullable fields
- Literal types for enumerations (group types, WebSocket operation types)
- Default factories for list fields
- Cursor-based pagination abstraction

---

## Related

- [router-workspace-domain-fastapi-endpoints](router-workspace-domain-fastapi-endpoints.md)
- [workspaceservice-workspace-domain-business-logic](workspaceservice-workspace-domain-business-logic.md)
- [groupservice-group-and-channel-business-logic-crud-membership-agents-dms](groupservice-group-and-channel-business-logic-crud-membership-agents-dms.md)
- [messageservice-message-business-logic-and-crud-operations](messageservice-message-business-logic-and-crud-operations.md)
- [ws-websocket-connection-manager-for-real-time-chat](ws-websocket-connection-manager-for-real-time-chat.md)
- [agentbridge-cloud-chat-event-bridge-to-pocketpaw-agent-pool](agentbridge-cloud-chat-event-bridge-to-pocketpaw-agent-pool.md)
