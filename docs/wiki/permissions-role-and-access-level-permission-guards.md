# permissions — Role and access-level permission guards

> Defines hierarchical enums for workspace roles and pocket access levels, each with an associated privilege level. Provides guard functions that compare a user's current role or access against a required minimum and raise `Forbidden` when insufficient. Used by the `deps` and `service` modules to enforce authorization checks throughout the cloud layer.

**Categories:** authorization, access control, cloud infrastructure  
**Concepts:** WorkspaceRole, PocketAccess, check_workspace_role, check_pocket_access, ordered enum hierarchy, privilege level comparison, guard function pattern, keyword-only arguments, Forbidden exception  
**Words:** 338 | **Version:** 1

---

## Purpose

The `permissions` module centralizes all authorization logic for the cloud subsystem. It models two distinct permission hierarchies—workspace-wide roles and per-pocket access levels—as ordered enums, then exposes simple guard functions that raise `Forbidden` on insufficient privilege. This keeps authorization rules declarative and consistent across the codebase.

## Key Classes/Functions

### `WorkspaceRole(Enum)`

Represents workspace membership tiers ordered by privilege:

| Member | Value | Level |
|--------|---------|-------|
| `MEMBER` | `"member"` | 1 |
| `ADMIN` | `"admin"` | 2 |
| `OWNER` | `"owner"` | 3 |

Each member stores a string value and an integer `level` used for comparison. The `from_str(role)` class method resolves a raw string to the corresponding enum member or raises `ValueError`.

### `PocketAccess(Enum)`

Represents per-pocket access tiers ordered by privilege:

| Member | Value | Level |
|--------|---------|-------|
| `VIEW` | `"view"` | 1 |
| `COMMENT` | `"comment"` | 2 |
| `EDIT` | `"edit"` | 3 |
| `OWNER` | `"owner"` | 4 |

Follows the same pattern as `WorkspaceRole` with a `from_str(access)` class method.

### `check_workspace_role(role, *, minimum)`

Accepts the user's current role and a required minimum as strings. Resolves both to `WorkspaceRole` members and raises `Forbidden` with code `"workspace.insufficient_role"` if the user's level is below the minimum.

### `check_pocket_access(access, *, minimum)`

Accepts the user's current access and a required minimum as strings. Resolves both to `PocketAccess` members and raises `Forbidden` with code `"pocket.insufficient_access"` if the user's level is below the minimum.

## Dependencies

- **Imports from:** `ee.cloud.shared.errors.Forbidden` — the exception raised on authorization failure.
- **Imported by:** `deps` (dependency injection / request context), `service` (business logic layer).

## Usage Examples

```python
from ee.cloud.shared.permissions import check_workspace_role, check_pocket_access

# Ensure the user is at least an admin before allowing workspace settings changes
check_workspace_role(user.role, minimum="admin")

# Ensure the user has edit access before modifying pocket contents
check_pocket_access(user.pocket_access, minimum="edit")
```

Both functions are designed to be called as guards at the top of service methods or within dependency injection, short-circuiting request handling with a `Forbidden` error when the caller lacks sufficient privilege.