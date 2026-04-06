# workspace.router — FastAPI REST router for workspace management

> Defines the FastAPI APIRouter that exposes all workspace-related HTTP endpoints under the /workspaces prefix. It covers full CRUD for workspaces, member role management, and a token-based invite workflow, delegating all business logic to WorkspaceService while enforcing license and authentication guards at the router level.

**Categories:** workspace, api-routing, enterprise-licensing, authentication, member-management, invite-management  
**Concepts:** APIRouter, WorkspaceService, CreateWorkspaceRequest, UpdateWorkspaceRequest, CreateInviteRequest, UpdateMemberRoleRequest, current_user, require_license, thin controller pattern, dependency injection  
**Words:** 509 | **Version:** 1

---

## Purpose

This module is the HTTP transport layer for the **Workspace** domain. It translates incoming REST requests into calls on `WorkspaceService`, validates request bodies via Pydantic schemas, and enforces two cross-cutting concerns as FastAPI dependencies:

1. **License gating** — every endpoint requires a valid enterprise license (`require_license`).
2. **Authentication** — all mutating and read endpoints (except public invite validation) inject the authenticated `User` via `current_user`.

The router is mounted by the package's `__init__` module and is tagged `"Workspace"` for OpenAPI grouping.

## Key Functions

### Workspace CRUD

| Endpoint | Function | Description |
|---|---|---|
| `POST /workspaces` | `create_workspace` | Creates a new workspace owned by the current user. Accepts `CreateWorkspaceRequest`. |
| `GET /workspaces` | `list_workspaces` | Returns all workspaces the authenticated user belongs to. |
| `GET /workspaces/{workspace_id}` | `get_workspace` | Retrieves a single workspace by ID (membership-scoped). |
| `PATCH /workspaces/{workspace_id}` | `update_workspace` | Partially updates workspace metadata via `UpdateWorkspaceRequest`. |
| `DELETE /workspaces/{workspace_id}` | `delete_workspace` | Deletes a workspace; returns HTTP 204 No Content. |

### Member Management

| Endpoint | Function | Description |
|---|---|---|
| `GET /workspaces/{workspace_id}/members` | `list_members` | Lists all members of a workspace. |
| `PATCH /workspaces/{workspace_id}/members/{user_id}` | `update_member_role` | Changes a member's role via `UpdateMemberRoleRequest`. |
| `DELETE /workspaces/{workspace_id}/members/{user_id}` | `remove_member` | Removes a member from the workspace (HTTP 204). |

### Invite Workflow

| Endpoint | Function | Description |
|---|---|---|
| `POST /workspaces/{workspace_id}/invites` | `create_invite` | Generates a new invite token for the workspace via `CreateInviteRequest`. |
| `GET /workspaces/invites/{token}` | `validate_invite` | Public endpoint — validates an invite token without requiring authentication. |
| `POST /workspaces/invites/{token}/accept` | `accept_invite` | Authenticated user accepts the invite and becomes a workspace member. |
| `DELETE /workspaces/{workspace_id}/invites/{invite_id}` | `revoke_invite` | Revokes a pending invite (HTTP 204). |

## Dependencies

| Dependency | Role |
|---|---|
| `ee.cloud.workspace.service.WorkspaceService` | Static service class containing all business logic; every endpoint delegates to it. |
| `ee.cloud.workspace.schemas` | Pydantic request models (`CreateWorkspaceRequest`, `UpdateWorkspaceRequest`, `CreateInviteRequest`, `UpdateMemberRoleRequest`). |
| `ee.cloud.shared.deps.current_user` | FastAPI dependency that extracts and validates the authenticated `User`. |
| `ee.cloud.license.require_license` | FastAPI dependency applied router-wide to enforce enterprise licensing. |
| `ee.cloud.models.user.User` | Domain model representing the authenticated user. |

## Design Patterns

- **Thin Controller / Fat Service** — The router contains zero business logic; it is purely a mapping from HTTP semantics to service calls.
- **Dependency Injection** — Uses FastAPI's `Depends()` for auth and licensing, applied both per-endpoint and router-wide.
- **Static Service Methods** — `WorkspaceService` is consumed as a collection of static/class methods (`WorkspaceService.create(...)`) rather than as an injected instance.
- **Explicit 204 Responses** — Delete and removal endpoints manually return `Response(status_code=204)` to avoid body serialization.

## Usage Examples

```python
# Mounting the router in the FastAPI application
from ee.cloud.workspace.router import router as workspace_router

app.include_router(workspace_router, prefix="/api/v1")
# All endpoints become available under /api/v1/workspaces/...
```

```python
# Typical invite flow (client-side)
# 1. Owner creates invite
POST /workspaces/{ws_id}/invites  {"email": "new@example.com", "role": "member"}
# 2. Invitee validates token (unauthenticated)
GET  /workspaces/invites/{token}
# 3. Invitee accepts (authenticated)
POST /workspaces/invites/{token}/accept
```