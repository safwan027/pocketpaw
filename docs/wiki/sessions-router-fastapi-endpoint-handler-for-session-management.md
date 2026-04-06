# Sessions Router — FastAPI endpoint handler for session management

> This module defines the FastAPI router for the Sessions domain, exposing RESTful endpoints for creating, reading, updating, and deleting user sessions. It acts as the HTTP interface layer that delegates business logic to SessionService while enforcing authentication, workspace isolation, and license requirements.

**Categories:** Sessions Domain, API Routing, Cloud Infrastructure, REST Endpoints  
**Concepts:** FastAPI Router, Dependency Injection, Request/Response validation, RESTful CRUD, User Authentication, Workspace Isolation, License Gating, Async Handlers, HTTP Status Codes (204 No Content), Pocket-based Filtering  
**Words:** 210 | **Version:** 1

---

## Purpose
Provides a complete REST API for session lifecycle management with support for CRUD operations, session history retrieval, and activity tracking through touch operations. All endpoints require valid licensing and user authentication.

## Key Functions

### CRUD Operations
- **`create_session(body, workspace_id, user_id)`** — Creates a new session with the given parameters; POST `/sessions`
- **`list_sessions(workspace_id, user_id, pocket)`** — Lists sessions filtered by workspace or pocket parameter; GET `/sessions`
- **`get_session(session_id, user_id)`** — Retrieves a specific session by ID; GET `/sessions/{session_id}`
- **`update_session(session_id, body, user_id)`** — Updates session metadata; PATCH `/sessions/{session_id}`
- **`delete_session(session_id, user_id)`** — Deletes a session; DELETE `/sessions/{session_id}` returns 204

### History & Activity
- **`get_session_history(session_id, user_id)`** — Retrieves session history records; GET `/sessions/{session_id}/history`
- **`touch_session(session_id)`** — Updates session activity timestamp; POST `/sessions/{session_id}/touch` returns 204

## Router Configuration
- **Prefix**: `/sessions`
- **Tag**: Sessions (for OpenAPI docs)
- **Dependencies**: License validation via `require_license` applied to all routes

## Dependencies
- **SessionService**: Business logic delegation for all operations
- **Schemas**: `CreateSessionRequest`, `UpdateSessionRequest` for request validation
- **Auth**: `current_user_id`, `current_workspace_id` dependency injections
- **License**: `require_license` dependency for feature gating

## Security & Isolation
- User authentication required on all endpoints (except `touch_session`)
- Workspace-scoped operations enforce multi-tenancy
- License validation as global dependency
- User-based access control in service layer

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
