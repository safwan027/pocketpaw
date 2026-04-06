# schemas — Pydantic request/response schemas for the Workspace domain

> Defines the data validation and serialization layer for workspace-related API operations. This module provides Pydantic models for creating/updating workspaces, managing invitations and member roles, and standardized response shapes. It is a foundational dependency imported by the router, service, group_service, message_service, WebSocket, and agent_bridge modules.

**Categories:** workspace, schemas, API contracts, validation  
**Concepts:** CreateWorkspaceRequest, UpdateWorkspaceRequest, CreateInviteRequest, UpdateMemberRoleRequest, WorkspaceResponse, MemberResponse, InviteResponse, validate_slug, Pydantic BaseModel, field_validator  
**Words:** 320 | **Version:** 1

---

## Purpose

This module serves as the single source of truth for all request and response data shapes in the Workspace domain. By centralizing validation rules (slug format, role enums, field length constraints) in Pydantic models, it ensures consistent input validation at the API boundary and uniform serialization for outbound responses.

## Key Classes

### Request Models

- **`CreateWorkspaceRequest`** — Validates `name` (1–100 chars) and `slug` (1–50 chars, lowercase alphanumeric with hyphens). Includes a `field_validator` that enforces the slug regex pattern `^[a-z0-9][a-z0-9-]*[a-z0-9]$|^[a-z0-9]$`.
- **`UpdateWorkspaceRequest`** — Partial-update model with optional `name` and `settings` fields.
- **`CreateInviteRequest`** — Accepts `email`, a `role` constrained to `admin` or `member` (default `member`), and an optional `group_id`.
- **`UpdateMemberRoleRequest`** — Accepts a `role` constrained to `owner`, `admin`, or `member`.

### Response Models

- **`WorkspaceResponse`** — Returns workspace metadata: `id`, `name`, `slug`, `owner`, `plan`, `seats`, `created_at`, and a computed `member_count`.
- **`MemberResponse`** — Returns member profile data: `id`, `email`, `name`, `avatar`, `role`, and `joined_at`.
- **`InviteResponse`** — Returns full invite state: `id`, `email`, `role`, `invited_by`, `token`, and boolean flags `accepted`, `revoked`, `expired`, plus `expires_at`.

## Dependencies

- **External**: `pydantic` (BaseModel, Field, field_validator), `re`, `datetime`
- **Internal**: None — this is a leaf module with no inward dependencies.
- **Depended on by**: `router`, `service`, `group_service`, `message_service`, `ws`, `agent_bridge`

## Usage Examples

```python
# Validating a workspace creation payload
from ee.cloud.workspace.schemas import CreateWorkspaceRequest

req = CreateWorkspaceRequest(name="Acme Corp", slug="acme-corp")
```

```python
# Serializing a workspace response
from ee.cloud.workspace.schemas import WorkspaceResponse

response = WorkspaceResponse(
    id="ws_123", name="Acme Corp", slug="acme-corp",
    owner="user_1", plan="pro", seats=10,
    created_at=datetime.now(), member_count=5
)
return response.model_dump()
```

## Design Notes

- The slug validator uses a regex that permits single-character slugs (`^[a-z0-9]$`) as well as multi-character slugs with internal hyphens, but disallows leading/trailing hyphens.
- Role fields use Pydantic `pattern` constraints rather than Python `Enum` types, keeping the schema lightweight and JSON-serializable.
- Request and response models are cleanly separated, following a CQRS-lite convention where input shapes differ from output shapes.