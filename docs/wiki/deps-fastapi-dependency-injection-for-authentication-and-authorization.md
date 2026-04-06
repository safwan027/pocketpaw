# deps — FastAPI dependency injection for authentication and authorization

> Provides reusable FastAPI dependencies that extract authenticated user information from JWT tokens and enforce workspace-level access control. These dependencies form the security backbone for all cloud API routers, handling user resolution, workspace context extraction, and role-based permission checks.

**Categories:** authentication, authorization, fastapi-dependencies, cloud-infrastructure  
**Concepts:** current_user, current_user_id, current_workspace_id, optional_workspace_id, require_role, FastAPI Depends, dependency injection, dependency factory, closure pattern, role-based access control  
**Words:** 405 | **Version:** 1

---

## Purpose

The `deps` module centralizes all FastAPI dependency-injection functions used by cloud routers to authenticate requests and authorize actions. Rather than each router implementing its own auth logic, routers declare these dependencies via `Depends()` and receive pre-validated user objects, IDs, and workspace contexts.

## Key Functions

### `current_user(user) -> User`
Simple pass-through dependency that resolves the authenticated `User` object from the JWT token via `current_active_user`. Serves as the canonical way to obtain the full user model in route handlers.

### `current_user_id(user) -> str`
Extracts and returns just the user ID as a string. Useful for routes that only need the identifier without the full user model.

### `current_workspace_id(user) -> str`
Extracts the `active_workspace` from the authenticated user. Raises an `HTTPException(400)` if no workspace is set, enforcing that workspace-scoped endpoints always have a valid context.

### `optional_workspace_id(user) -> str | None`
Same as `current_workspace_id` but permits `None` — used by endpoints that can operate with or without a workspace context.

### `require_role(minimum: str) -> Depends`
A **dependency factory** (closure pattern) that returns a FastAPI-compatible dependency function. The inner function:
1. Resolves the user and active workspace ID
2. Finds the user's membership record for that workspace
3. Raises `Forbidden` if the user is not a member
4. Delegates to `check_workspace_role()` to verify the user meets the minimum role threshold
5. Returns the validated `User` on success

Usage: `Depends(require_role("admin"))` in a route signature.

## Dependencies

| Import | Purpose |
|---|---|
| `ee.cloud.auth.current_active_user` | JWT token resolution and user lookup |
| `ee.cloud.models.user.User` | User model with workspace memberships |
| `ee.cloud.shared.errors.Forbidden` | Structured authorization error |
| `ee.cloud.shared.permissions.check_workspace_role` | Role hierarchy validation |

Imported by `__init__` (re-exported) and `router` modules across the cloud package.

## Usage Examples

```python
from fastapi import APIRouter, Depends
from ee.cloud.shared.deps import current_user, current_workspace_id, require_role
from ee.cloud.models.user import User

router = APIRouter()

# Basic authenticated route
@router.get("/me")
async def get_profile(user: User = Depends(current_user)):
    return user

# Workspace-scoped route
@router.get("/workspace/data")
async def get_data(workspace_id: str = Depends(current_workspace_id)):
    return fetch_data(workspace_id)

# Role-gated route using the dependency factory
@router.delete("/workspace/settings")
async def delete_settings(user: User = Depends(require_role("admin"))):
    ...
```

## Design Patterns

- **Dependency Injection Chain**: All dependencies ultimately resolve through `current_active_user`, creating a single authentication entry point.
- **Factory Pattern**: `require_role` is a closure-based factory that produces parameterized dependencies, enabling declarative role checks in route signatures.
- **Layered Authorization**: Authentication (JWT → User) is separated from authorization (role checks), following the principle of separation of concerns.