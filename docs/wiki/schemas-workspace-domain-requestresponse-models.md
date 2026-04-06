# schemas — Workspace Domain Request/Response Models

> Defines Pydantic-based request and response schemas for workspace management operations. Provides validation and serialization for workspace CRUD, member management, and invite handling across the workspace domain.

**Categories:** workspace domain, schemas & validation, API contracts, data models  
**Concepts:** CreateWorkspaceRequest, UpdateWorkspaceRequest, CreateInviteRequest, UpdateMemberRoleRequest, WorkspaceResponse, MemberResponse, InviteResponse, validate_slug, field_validator, Pydantic BaseModel  
**Words:** 248 | **Version:** 1

---

## Purpose
This module centralizes all request/response data models for the workspace domain using Pydantic BaseModel. It ensures type safety, validation, and consistent API contracts across workspace-related endpoints and services.

## Key Classes/Functions

### Request Schemas
- **CreateWorkspaceRequest**: Validates workspace creation with name (1-100 chars) and slug (alphanumeric with hyphens, validated via regex)
  - `validate_slug()`: Custom validator ensuring lowercase alphanumeric format with optional hyphens
- **UpdateWorkspaceRequest**: Partial update model with optional name and settings dict
- **CreateInviteRequest**: Invite creation with email, role (admin/member default), and optional group_id
- **UpdateMemberRoleRequest**: Role updates with enum-like pattern validation (owner/admin/member)

### Response Schemas
- **WorkspaceResponse**: Workspace details including id, name, slug, owner, plan, seats, creation time, and member count
- **MemberResponse**: Member profile with id, email, name, avatar, role, and join timestamp
- **InviteResponse**: Invite status tracking with email, role, token, acceptance/revocation/expiry flags, and expiration datetime

## Dependencies
- `pydantic`: BaseModel, Field, field_validator for validation and serialization
- `re`: Regex pattern matching for slug validation
- `datetime`: Timestamp fields for audit trails

## Usage Examples
```python
# Creating a workspace
req = CreateWorkspaceRequest(name="My Team", slug="my-team")
# Validates slug matches: ^[a-z0-9][a-z0-9-]*[a-z0-9]$|^[a-z0-9]$

# Workspace response with metadata
response = WorkspaceResponse(
    id="ws_123",
    name="My Team",
    slug="my-team",
    owner="user_456",
    plan="professional",
    seats=10,
    created_at=datetime.now(),
    member_count=5
)

# Inviting a member
invite = CreateInviteRequest(
    email="user@example.com",
    role="member",
    group_id="grp_789"
)
```

## Validation Rules
- Slug: lowercase alphanumeric, single char or multi-char with hyphens at start/end
- Name: 1-100 characters
- Role fields: Enum-constrained via regex patterns
- Email: Standard email field type

---

## Related

- [router-workspace-domain-fastapi-endpoints](router-workspace-domain-fastapi-endpoints.md)
- [workspaceservice-workspace-domain-business-logic](workspaceservice-workspace-domain-business-logic.md)
- [groupservice-group-and-channel-business-logic-crud-membership-agents-dms](groupservice-group-and-channel-business-logic-crud-membership-agents-dms.md)
- [messageservice-message-business-logic-and-crud-operations](messageservice-message-business-logic-and-crud-operations.md)
- [ws-websocket-connection-manager-for-real-time-chat](ws-websocket-connection-manager-for-real-time-chat.md)
- [agentbridge-cloud-chat-event-bridge-to-pocketpaw-agent-pool](agentbridge-cloud-chat-event-bridge-to-pocketpaw-agent-pool.md)
