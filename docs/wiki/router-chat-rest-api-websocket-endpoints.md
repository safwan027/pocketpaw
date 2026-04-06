# router — Chat REST API & WebSocket endpoints

> Provides FastAPI routes and WebSocket handler for enterprise chat functionality. Implements group management, messaging, reactions, typing indicators, and read receipts. All REST endpoints require enterprise license; WebSocket authenticates via JWT query parameter.

**Categories:** Chat Domain, REST API, WebSocket, Real-time Communication, Enterprise Features  
**Concepts:** REST API routes, WebSocket endpoint, JWT authentication, License requirement enforcement, Dependency injection, Async request handlers, Message dispatcher pattern, Broadcast to group, Cursor-based pagination, Pydantic schema validation  
**Words:** 712 | **Version:** 1

---

## Purpose

This module defines the complete Chat domain API surface, bridging HTTP REST endpoints and real-time WebSocket communication. It enforces license requirements, validates requests through Pydantic schemas, delegates business logic to service classes, and broadcasts events to connected clients via the WebSocket manager.

## Architecture

### Endpoint Organization

- **Groups**: Create, list, retrieve, update, archive, join, leave
- **Group Members**: Add/remove members and agents
- **Messages**: Send, edit, delete, react, thread retrieval
- **Pins**: Pin/unpin messages in groups
- **Search**: Full-text message search
- **DMs**: Get or create direct message groups
- **WebSocket**: Real-time bidirectional communication at `/ws/cloud`

### Route Structure

```
REST Routes (prefix: /chat, requires license)
├── /groups                          [POST, GET]
├── /groups/{group_id}               [GET, PATCH, POST archive/join/leave]
├── /groups/{group_id}/members       [POST add, DELETE remove]
├── /groups/{group_id}/agents        [POST add, PATCH update, DELETE remove]
├── /groups/{group_id}/messages      [GET, POST]
├── /groups/{group_id}/pin/{msg_id}  [POST, DELETE]
├── /groups/{group_id}/search        [GET]
├── /messages/{message_id}           [PATCH edit, DELETE, POST react]
├── /messages/{message_id}/thread    [GET]
└── /dm/{target_user_id}             [POST]

WebSocket
└── /ws/cloud                        [authenticate via JWT token query param]
```

## Key Functions

### REST Endpoints (Async)

**Groups**
- `create_group()` - POST /chat/groups - Create new group
- `list_groups()` - GET /chat/groups - List user's groups
- `get_group()` - GET /chat/groups/{group_id} - Retrieve group details
- `update_group()` - PATCH /chat/groups/{group_id} - Modify group metadata
- `archive_group()` - POST /chat/groups/{group_id}/archive
- `join_group()` - POST /chat/groups/{group_id}/join
- `leave_group()` - POST /chat/groups/{group_id}/leave
- `add_members()` - POST /chat/groups/{group_id}/members
- `remove_member()` - DELETE /chat/groups/{group_id}/members/{user_id}
- `add_group_agent()` - POST /chat/groups/{group_id}/agents
- `update_group_agent()` - PATCH /chat/groups/{group_id}/agents/{agent_id}
- `remove_group_agent()` - DELETE /chat/groups/{group_id}/agents/{agent_id}

**Messages**
- `get_messages()` - GET /chat/groups/{group_id}/messages - Paginated retrieval with cursor
- `send_message()` - POST /chat/groups/{group_id}/messages
- `edit_message()` - PATCH /chat/messages/{message_id}
- `delete_message()` - DELETE /chat/messages/{message_id}
- `react_to_message()` - POST /chat/messages/{message_id}/react - Toggle emoji reaction
- `get_thread()` - GET /chat/messages/{message_id}/thread - Fetch replies

**Pins**
- `pin_message()` - POST /chat/groups/{group_id}/pin/{message_id}
- `unpin_message()` - DELETE /chat/groups/{group_id}/pin/{message_id}

**Search & DMs**
- `search_messages()` - GET /chat/groups/{group_id}/search?q=... - Full-text search
- `get_or_create_dm()` - POST /chat/dm/{target_user_id}

### WebSocket Handler

- `websocket_endpoint()` - Authenticates JWT token, manages connection lifecycle, dispatches typed JSON messages
- `_handle_ws_message()` - Routes inbound WsInbound messages by type

### WebSocket Message Handlers

- `_ws_message_send()` - Broadcast new message to group members
- `_ws_message_edit()` - Broadcast message edit with timestamp
- `_ws_message_delete()` - Broadcast message deletion
- `_ws_message_react()` - Broadcast emoji reaction with user attribution
- `_ws_typing()` - Track typing state and broadcast indicator
- `_ws_read_ack()` - Broadcast read receipt with last-read message ID

## Dependencies

**External Frameworks**
- `fastapi`: APIRouter, Depends, Query, WebSocket, WebSocketDisconnect
- `pydantic`: Schema validation (models from schemas module)
- `pyjwt`: JWT token decoding for WebSocket auth

**Internal Modules**
- `ee.cloud.chat.schemas`: Request/response Pydantic models (WsInbound, WsOutbound, etc.)
- `ee.cloud.chat.service`: GroupService, MessageService business logic
- `ee.cloud.chat.ws`: WebSocket manager for connection tracking and broadcasting
- `ee.cloud.license`: `require_license` dependency for REST route protection
- `ee.cloud.shared.deps`: `current_user_id`, `current_workspace_id` dependency injectors
- `ee.cloud.models.group`: Group ORM model
- `ee.cloud.models.message`: Message ORM model

## Security

1. **REST Routes**: Protected by `require_license` dependency - checks enterprise license on every request
2. **WebSocket**: Authenticates JWT token from query parameter using HS256 algorithm with `AUTH_SECRET` environment variable; validates `audience` claim and extracts `sub` (user_id)
3. **User Context**: All endpoints receive `user_id` via dependency injection to enforce authorization

## Design Patterns

- **Dependency Injection**: FastAPI Depends() for auth and workspace context
- **Layered Architecture**: Router → Service → Model layers
- **Async/Await**: All I/O operations non-blocking
- **Message Dispatcher**: Type-based routing in `_handle_ws_message()`
- **Broadcast Pattern**: `manager.broadcast_to_group()` for multi-client updates
- **Lazy Imports**: Model imports inside handlers to avoid circular dependencies

## Error Handling

- **WebSocket Auth Failure**: Close with code 4001 (custom close code)
- **Invalid WsInbound**: Send error type message
- **Unhandled Exceptions**: Log and gracefully disconnect; cleanup via finally block
- **Missing Required Fields**: Handler methods guard with null checks before processing

## Pagination & Limits

- `get_messages()`: cursor-based pagination, limit 1-100 (default 50)
- `search_messages()`: query string min_length=1

## Data Flow Examples

**Send Message via WebSocket:**
1. Client sends `{type: 'message.send', group_id, content, ...}`
2. `_handle_ws_message()` routes to `_ws_message_send()`
3. `MessageService.send_message()` persists to DB
4. `manager.broadcast_to_group()` sends `message.new` to all members (except sender)
5. Sender receives `message.sent` confirmation

**Typing Indicator:**
1. Client sends `{type: 'typing.start', group_id}`
2. `_ws_typing()` activates typing state in manager
3. Broadcasts `typing` event with user_id and active=true
4. Client sends `{type: 'typing.stop'}` to deactivate

---

## Related

- [schemas-workspace-domain-requestresponse-models](schemas-workspace-domain-requestresponse-models.md)
- [workspaceservice-workspace-domain-business-logic](workspaceservice-workspace-domain-business-logic.md)
- [license-enterprise-license-validation-for-cloud-features](license-enterprise-license-validation-for-cloud-features.md)
- [deps-fastapi-dependency-injection-for-cloud-authentication-and-authorization](deps-fastapi-dependency-injection-for-cloud-authentication-and-authorization.md)
- [knowledge-agent-scoped-knowledge-base-service](knowledge-agent-scoped-knowledge-base-service.md)
- [core-enterprise-authentication-with-fastapi-users-jwt-and-multi-transport](core-enterprise-authentication-with-fastapi-users-jwt-and-multi-transport.md)
- [user-enterprise-user-and-oauth-account-models](user-enterprise-user-and-oauth-account-models.md)
- [ws-websocket-connection-manager-for-real-time-chat](ws-websocket-connection-manager-for-real-time-chat.md)
- [group-multi-user-chat-channels-with-ai-agent-participants](group-multi-user-chat-channels-with-ai-agent-participants.md)
- [message-group-chat-message-document-model](message-group-chat-message-document-model.md)
- [errors-unified-error-hierarchy-for-cloud-module](errors-unified-error-hierarchy-for-cloud-module.md)
- [backendadapter-llm-backend-adapter-for-knowledge-base-compilation](backendadapter-llm-backend-adapter-for-knowledge-base-compilation.md)
- [workspace-workspace-document-model-for-deployments-and-organizations](workspace-workspace-document-model-for-deployments-and-organizations.md)
- [eecloudworkspace-workspace-module-initialization](eecloudworkspace-workspace-module-initialization.md)
