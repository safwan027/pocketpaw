# router — Auth domain FastAPI endpoint definitions

> Defines FastAPI routes for authentication operations including login, logout, registration, and user profile management. Acts as the HTTP interface layer for the auth domain, delegating business logic to AuthService while handling dependency injection of authenticated users.

**Categories:** authentication, API routing, user management, workspace management  
**Concepts:** get_me, update_me, set_active_workspace, APIRouter, Depends, current_active_user, fastapi_users, cookie_backend, bearer_backend, ProfileUpdateRequest  
**Words:** 220 | **Version:** 1

---

## Purpose
Provides REST API endpoints for authentication and user profile operations in the PocketPaw cloud application. Integrates fastapi-users library for standard auth flows while exposing custom endpoints for profile updates and workspace management.

## Key Functions

### get_me
**GET /auth/me**
- Returns current authenticated user's profile data
- Requires active user authentication via `current_active_user` dependency
- Delegates to `AuthService.get_profile()`

### update_me
**PATCH /auth/me**
- Updates authenticated user's profile information
- Accepts `ProfileUpdateRequest` body
- Requires active user authentication
- Delegates to `AuthService.update_profile()`

### set_active_workspace
**POST /auth/set-active-workspace**
- Sets the active workspace for the authenticated user
- Accepts `SetWorkspaceRequest` containing workspace_id
- Returns confirmation with selected workspace ID
- Delegates to `AuthService.set_active_workspace()`

## Integrated Routes

**Login/Logout** (`/auth/*`):
- Cookie-based authentication via `cookie_backend`
- Bearer token authentication via `bearer_backend`
- Provided by `fastapi_users.get_auth_router()`

**Registration** (`/auth/register`):
- User registration endpoint
- Uses `UserRead` and `UserCreate` schemas
- Provided by `fastapi_users.get_register_router()`

## Dependencies
- **fastapi-users**: Authentication framework providing pre-built routers
- **AuthService**: Business logic for profile and workspace operations
- **current_active_user**: Dependency for validating authenticated sessions
- **Schemas**: ProfileUpdateRequest, SetWorkspaceRequest
- **Core auth**: cookie_backend, bearer_backend, UserRead, UserCreate

## Architecture Pattern
- **Router Layer**: FastAPI APIRouter handles HTTP request/response
- **Service Layer**: AuthService handles business logic
- **Dependency Injection**: Uses FastAPI Depends() for user authentication validation
- **Schema Validation**: Pydantic models for request bodies

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
