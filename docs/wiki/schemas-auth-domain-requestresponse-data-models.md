# schemas — Auth domain request/response data models

> Defines Pydantic request and response schemas for authentication operations in the PocketPaw cloud system. Provides type-safe contracts for profile updates, workspace management, and user data serialization across the auth domain and dependent services.

**Categories:** authentication, data models, API contracts  
**Concepts:** ProfileUpdateRequest, SetWorkspaceRequest, UserResponse, Pydantic BaseModel, optional fields, ORM compatibility, request/response schemas, type validation, Pydantic  
**Words:** 238 | **Version:** 1

---

## Purpose
This module serves as the data validation and serialization layer for authentication-related operations. It uses Pydantic BaseModel to enforce type safety and validation on incoming requests and outgoing user data.

## Key Classes

### ProfileUpdateRequest
Request model for user profile modifications.
- **Fields:**
  - `full_name: str | None` — User's display name (optional)
  - `avatar: str | None` — User avatar URL or data (optional)
  - `status: str | None` — User status message (optional)

### SetWorkspaceRequest
Request model for switching active workspace.
- **Fields:**
  - `workspace_id: str` — Target workspace identifier (required)

### UserResponse
Response model for user data serialization.
- **Fields:**
  - `id: str` — User unique identifier
  - `email: str` — User email address
  - `name: str` — User display name
  - `image: str` — User avatar/image URL
  - `email_verified: bool` — Email verification status
  - `active_workspace: str | None` — Currently active workspace ID
  - `workspaces: list[dict]` — List of accessible workspaces
- **Config:** `from_attributes = True` — Enables ORM model compatibility

## Dependencies
No internal module dependencies within the scanned codebase.

## Usage Examples
```python
# Profile update request
profile_update = ProfileUpdateRequest(
    full_name="John Doe",
    avatar="https://example.com/avatar.jpg"
)

# Workspace switching
workspace_switch = SetWorkspaceRequest(workspace_id="ws_123")

# User response from API
user = UserResponse(
    id="user_456",
    email="john@example.com",
    name="John Doe",
    image="https://example.com/avatar.jpg",
    email_verified=True,
    active_workspace="ws_123",
    workspaces=[{"id": "ws_123", "name": "Main"}]
)
```

## Integration Points
Consumed by: `router`, `service`, `group_service`, `message_service`, `ws`, `agent_bridge` modules for request validation and response formatting.

---

## Related

- [router-workspace-domain-fastapi-endpoints](router-workspace-domain-fastapi-endpoints.md)
- [workspaceservice-workspace-domain-business-logic](workspaceservice-workspace-domain-business-logic.md)
- [groupservice-group-and-channel-business-logic-crud-membership-agents-dms](groupservice-group-and-channel-business-logic-crud-membership-agents-dms.md)
- [messageservice-message-business-logic-and-crud-operations](messageservice-message-business-logic-and-crud-operations.md)
- [ws-websocket-connection-manager-for-real-time-chat](ws-websocket-connection-manager-for-real-time-chat.md)
- [agentbridge-cloud-chat-event-bridge-to-pocketpaw-agent-pool](agentbridge-cloud-chat-event-bridge-to-pocketpaw-agent-pool.md)
