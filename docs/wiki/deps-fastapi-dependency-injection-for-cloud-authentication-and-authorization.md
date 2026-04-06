# deps — FastAPI dependency injection for cloud authentication and authorization

> Provides reusable FastAPI dependency functions for extracting and validating user authentication, workspace context, and role-based access control. This module serves as the central dependency injection layer for cloud routers, ensuring consistent authentication and authorization across endpoints.

**Categories:** authentication, authorization, dependency injection, cloud infrastructure  
**Concepts:** dependency injection, JWT authentication, role-based access control (RBAC), workspace isolation, closure pattern, async dependencies, FastAPI Depends, HTTPException, user context extraction, FastAPI  
**Words:** 331 | **Version:** 1

---

## Purpose

The `deps` module implements FastAPI dependency injection functions that extract authenticated user information from JWT tokens and enforce role-based access control at the route level. It acts as a middleware abstraction layer between authentication logic and route handlers.

## Key Functions

### User Extraction

- **`current_user(user)`** — Async dependency that returns the authenticated user object from JWT token validation. Wraps the core `current_active_user` dependency.

- **`current_user_id(user)`** — Async dependency that extracts and returns the user ID as a string from the authenticated user.

### Workspace Context

- **`current_workspace_id(user)`** — Async dependency that retrieves the active workspace ID from the authenticated user. Raises `HTTPException(400)` if no active workspace is set, enforcing workspace context requirement.

- **`optional_workspace_id(user)`** — Async dependency that returns the active workspace ID if available, or `None` if not set. Used for optional workspace context scenarios.

### Authorization

- **`require_role(minimum)`** — Dependency factory function that creates a closure-based dependency checker. Validates that the user has a specified minimum role in the current workspace. Raises `Forbidden` exception if user is not a workspace member or lacks sufficient permissions.

## Dependencies

- **`ee.cloud.auth`** — Provides `current_active_user` for JWT token validation
- **`ee.cloud.models.user`** — Defines `User` data model
- **`ee.cloud.shared.errors`** — Provides `Forbidden` custom exception
- **`ee.cloud.shared.permissions`** — Implements `check_workspace_role` role validation logic

## Usage Examples

```python
# Basic user injection
@router.get('/me')
async def get_current_user(user: User = Depends(current_user)):
    return user

# Extract user ID for audit logging
@router.post('/resource')
async def create_resource(user_id: str = Depends(current_user_id)):
    # Use user_id for tracking resource ownership
    pass

# Require workspace context
@router.get('/workspace/data')
async def get_workspace_data(workspace_id: str = Depends(current_workspace_id)):
    # This endpoint requires an active workspace
    pass

# Role-based access control
@router.post('/workspace/admin')
async def admin_action(user: User = Depends(require_role('admin'))):
    # Only users with 'admin' role in active workspace can access
    pass
```

## Error Handling

- Raises `HTTPException(400)` when `current_workspace_id` is called but user has no active workspace
- Raises `Forbidden('workspace.not_member')` when `require_role` detects user is not a workspace member
- Delegates to `check_workspace_role` for role insufficiency validation

---

## Related

- [user-enterprise-user-and-oauth-account-models](user-enterprise-user-and-oauth-account-models.md)
- [errors-unified-error-hierarchy-for-cloud-module](errors-unified-error-hierarchy-for-cloud-module.md)
- [permissions-role-and-access-level-permission-checks](permissions-role-and-access-level-permission-checks.md)
- [eecloudworkspace-workspace-module-initialization](eecloudworkspace-workspace-module-initialization.md)
- [router-workspace-domain-fastapi-endpoints](router-workspace-domain-fastapi-endpoints.md)
