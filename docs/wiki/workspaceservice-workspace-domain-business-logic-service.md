# workspace/service — Workspace domain business logic service

> Stateless service layer encapsulating all workspace business logic including CRUD operations, member management, and invite workflows. Acts as the core orchestrator between the router (API layer) and the database models, enforcing role-based access control, seat limits, and domain invariants for multi-tenant workspace operations.

**Categories:** workspace management, multi-tenancy, business logic service, member management, invite workflow, access control  
**Concepts:** WorkspaceService, WorkspaceMembership, Invite, stateless service pattern, role-based access control, soft delete, seat limit enforcement, token-based invites, event bus, check_workspace_role  
**Words:** 675 | **Version:** 1

---

## Purpose

This module implements the `WorkspaceService` class — a stateless service that centralizes all workspace-related business logic. It sits between the HTTP router layer (`router`) and the Beanie ODM models, ensuring that authorization checks, seat-limit enforcement, and domain rules are consistently applied. It is also consumed by `agent_bridge` for programmatic workspace access.

## Key Classes/Functions

### `WorkspaceService` (class)
Stateless service with all `@staticmethod` async methods organized into three logical groups:

#### Workspace CRUD
| Method | Role Required | Description |
|---|---|---|
| `create(user, body)` | any authenticated | Creates a workspace with a unique slug, adds creator as owner, sets it as active workspace |
| `get(workspace_id, user)` | member | Retrieves a workspace by ID with live member count |
| `update(workspace_id, user, body)` | admin+ | Updates workspace name and/or settings |
| `delete(workspace_id, user)` | owner | Soft-deletes a workspace by setting `deleted_at` |
| `list_for_user(user)` | member | Returns all non-deleted workspaces the user belongs to |

#### Member Management
| Method | Role Required | Description |
|---|---|---|
| `list_members(workspace_id, user)` | member | Lists all workspace members with profile info and role |
| `update_member_role(workspace_id, target_user_id, role, user)` | admin+ | Changes a member's role; protects workspace owner from demotion |
| `remove_member(workspace_id, target_user_id, user)` | admin+ | Removes a member; protects owner from removal; emits `member.removed` event; clears active workspace if needed |

#### Invite Workflow
| Method | Role Required | Description |
|---|---|---|
| `create_invite(workspace_id, user, body)` | admin+ | Creates a token-based invite; enforces seat limits and prevents duplicate pending invites per email+group |
| `validate_invite(token)` | none (public) | Looks up invite status by token — used for invite link previews |
| `accept_invite(token, user)` | any authenticated | Validates invite state (not accepted/revoked/expired), checks seat limit, adds user to workspace, emits `invite.accepted` event |
| `revoke_invite(workspace_id, invite_id, user)` | admin+ | Marks an invite as revoked |

### Private Helper Functions
| Function | Description |
|---|---|
| `_workspace_response(ws, member_count)` | Serializes a `Workspace` document to a frontend-compatible dict with camelCase keys |
| `_invite_response(invite)` | Serializes an `Invite` document to a frontend-compatible dict |
| `_get_membership(user, workspace_id)` | Finds a user's `WorkspaceMembership` or raises `NotFound` |
| `_count_members(workspace_id)` | Counts users with membership in a workspace via MongoDB query |

## Design Patterns

- **Stateless Service Pattern**: All methods are `@staticmethod` — no instance state, making the service easy to test and call from anywhere.
- **Soft Delete**: Workspaces use `deleted_at` timestamps rather than hard deletion; all queries filter for `deleted_at == None`.
- **Role-Based Access Control**: Uses `check_workspace_role(role, minimum=...)` with a role hierarchy (`member` < `admin` < `owner`) to gate operations.
- **Seat Limit Enforcement**: Both invite creation and invite acceptance check `member_count >= ws.seats` before allowing new members.
- **Event-Driven Side Effects**: Member removal and invite acceptance emit events via `event_bus` for downstream processing (notifications, cleanup, etc.).
- **Token-Based Invites**: Invites use `secrets.token_urlsafe(32)` for secure, unguessable invite links.
- **Idempotent Accept**: If a user is already a member when accepting an invite, the seat check is skipped and only the invite is marked accepted.

## Dependencies

### Internal Models
- `ee.cloud.models.workspace.Workspace`, `WorkspaceSettings` — workspace document and settings sub-document
- `ee.cloud.models.user.User`, `WorkspaceMembership` — user document and embedded membership sub-document
- `ee.cloud.models.invite.Invite` — invite document

### Internal Shared
- `ee.cloud.shared.errors` — `ConflictError`, `Forbidden`, `NotFound`, `SeatLimitError`
- `ee.cloud.shared.events.event_bus` — async event emitter for domain events
- `ee.cloud.shared.permissions.check_workspace_role` — role hierarchy enforcement

### Request Schemas
- `ee.cloud.workspace.schemas` — `CreateWorkspaceRequest`, `UpdateWorkspaceRequest`, `CreateInviteRequest`

### External Libraries
- `beanie` (MongoDB ODM with Pydantic) — `PydanticObjectId`, document queries
- `secrets` — secure token generation

## Consumed By
- `router` — HTTP API layer that delegates to this service
- `agent_bridge` — programmatic access for AI agent operations

## Usage Examples

```python
# Create a workspace
result = await WorkspaceService.create(user, CreateWorkspaceRequest(name="Acme", slug="acme"))

# List user's workspaces
workspaces = await WorkspaceService.list_for_user(user)

# Invite a new member
invite = await WorkspaceService.create_invite(
    workspace_id="abc123",
    user=admin_user,
    body=CreateInviteRequest(email="new@example.com", role="member")
)

# Accept an invite (typically from a different user)
await WorkspaceService.accept_invite(token="invite-token", user=invited_user)
```