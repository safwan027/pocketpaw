# core — Enterprise authentication with FastAPI-Users, JWT, and multi-transport

> Implements enterprise-grade authentication for PocketPaw using fastapi-users with JWT strategy and dual transport layers (cookies for browsers, bearer tokens for API/Tauri clients). Provides user registration, login, logout, profile management, and admin seeding functionality.

**Categories:** authentication, security, enterprise, fastapi, user-management  
**Concepts:** UserManager, UserRead, UserCreate, ObjectIDIDMixin, BaseUserManager, JWTStrategy, AuthenticationBackend, CookieTransport, BearerTransport, BeanieUserDatabase  
**Words:** 401 | **Version:** 1

---

## Purpose
This module sets up a complete authentication system compliant with enterprise standards, supporting both stateless bearer token authentication and stateful cookie-based sessions. It integrates with Beanie ODM for MongoDB user persistence and provides automatic admin user initialization.

## Key Classes

### UserManager
Extends `ObjectIDIDMixin` and `BaseUserManager[User, PydanticObjectId]`. Handles user lifecycle events:
- `on_after_register()` — Logs new user registrations
- `on_after_login()` — Logs successful login attempts
- Manages password hashing and token generation via inherited base class

### UserRead
Pydantic schema for user profile responses. Extends `fastapi_users_schemas.BaseUser[PydanticObjectId]` with:
- `full_name` — User display name
- `avatar` — User avatar URL

### UserCreate
Pydantic schema for registration payloads. Extends `fastapi_users_schemas.BaseUserCreate` with:
- `full_name` — Optional user display name (default: empty string)

## Key Functions

### Authentication Setup
- `get_user_db()` — Dependency yielding Beanie-backed user database adapter
- `get_user_manager()` — Dependency yielding configured UserManager instance
- `get_jwt_strategy()` — Creates JWT strategy with shared secret and 7-day lifetime

### Admin Initialization
- `seed_admin(email, password, full_name)` — Creates default admin user if not exists. Reads environment variables (ADMIN_EMAIL, ADMIN_PASSWORD, ADMIN_NAME) and skips creation if user already exists. Returns created User or None on failure.

## Authentication Architecture

**Transports:**
- **Cookie Transport** (`paw_auth`) — Browser-based sessions with 7-day expiration, SameSite=lax
- **Bearer Transport** — API/Tauri client requests via Authorization header

**Backends:**
- Both use shared `JWTStrategy` with configurable SECRET and TOKEN_LIFETIME (7 days default)
- `cookie_backend` — Stateless JWT in httpOnly cookie
- `bearer_backend` — Stateless JWT in Authorization header

**FastAPIUsers Instance:**
- Manages dual-backend authentication pipeline
- Provides dependency injection: `current_active_user`, `current_optional_user`

## Environment Variables
- `AUTH_SECRET` — JWT signing secret (default: "change-me-in-production-please")
- `ADMIN_EMAIL` — Default admin email (default: admin@pocketpaw.ai)
- `ADMIN_PASSWORD` — Default admin password (default: admin123)
- `ADMIN_NAME` — Default admin display name (default: Admin)

## API Endpoints (via fastapi_users)
- `POST /auth/register` — Sign up with email and password
- `POST /auth/login` — Sign in, returns JWT cookie + bearer token
- `POST /auth/logout` — Clear authentication cookie
- `GET /auth/me` — Retrieve current authenticated user profile
- `PATCH /auth/me` — Update current user profile

## Dependencies
- **Internal:** `ee.cloud.models.user` (User, OAuthAccount, WorkspaceMembership models)
- **External:** fastapi-users, fastapi-users-db-beanie, Beanie, FastAPI, Pydantic

## Usage Example
```python
# On application startup
from ee.cloud.auth.core import seed_admin
await seed_admin()  # Creates admin if missing

# In route handlers
from ee.cloud.auth.core import current_active_user

@app.get("/protected")
async def protected(user: User = Depends(current_active_user)):
    return {"message": f"Hello {user.full_name}"}
```

---

## Related

- [user-enterprise-user-and-oauth-account-models](user-enterprise-user-and-oauth-account-models.md)
- [eecloudworkspace-workspace-module-initialization](eecloudworkspace-workspace-module-initialization.md)
- [router-workspace-domain-fastapi-endpoints](router-workspace-domain-fastapi-endpoints.md)
