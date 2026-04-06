# Pockets Router — FastAPI endpoint definitions for pocket management

> FastAPI router module that exposes RESTful API endpoints for the Pockets domain, handling CRUD operations on pockets, widgets, team members, agents, sharing mechanisms, collaborators, and sessions. All endpoints require license validation and user authentication.

**Categories:** api routing, pockets domain, fastapi, collaboration features, access control  
**Concepts:** create_pocket, list_pockets, get_pocket, update_pocket, delete_pocket, add_widget, update_widget, remove_widget, reorder_widgets, add_team_member  
**Words:** 358 | **Version:** 1

---

## Purpose
Provides a complete API surface for pocket management in the OCEAN workspace platform, supporting collaborative features like sharing, team membership, agent integration, and session creation.

## Key Endpoints

### CRUD Operations
- `POST /pockets` — Create a new pocket
- `GET /pockets` — List all pockets in workspace
- `GET /pockets/{pocket_id}` — Retrieve single pocket
- `PATCH /pockets/{pocket_id}` — Update pocket metadata
- `DELETE /pockets/{pocket_id}` — Delete pocket (204 No Content)

### Widgets Management
- `POST /pockets/{pocket_id}/widgets` — Add widget to pocket
- `PATCH /pockets/{pocket_id}/widgets/{widget_id}` — Update widget
- `DELETE /pockets/{pocket_id}/widgets/{widget_id}` — Remove widget (204)
- `POST /pockets/{pocket_id}/widgets/reorder` — Reorder widgets by ID

### Team Management
- `POST /pockets/{pocket_id}/team` — Add team member
- `DELETE /pockets/{pocket_id}/team/{member_id}` — Remove team member (204)

### Agents Integration
- `POST /pockets/{pocket_id}/agents` — Add agent to pocket
- `DELETE /pockets/{pocket_id}/agents/{agent_id}` — Remove agent (204)

### Sharing & Access Control
- `POST /pockets/{pocket_id}/share` — Generate share link with access level
- `PATCH /pockets/{pocket_id}/share` — Update share link access
- `DELETE /pockets/{pocket_id}/share` — Revoke share link (204)
- `GET /pockets/shared/{token}` — Access pocket via share token (public)

### Collaborators
- `POST /pockets/{pocket_id}/collaborators` — Add collaborator (204)
- `DELETE /pockets/{pocket_id}/collaborators/{target_user_id}` — Remove collaborator (204)

### Sessions
- `POST /pockets/{pocket_id}/sessions` — Create session for pocket
- `GET /pockets/{pocket_id}/sessions` — List pocket sessions

## Dependencies
- **FastAPI**: `APIRouter`, `Depends` for routing and dependency injection
- **Authentication**: `current_user_id`, `current_workspace_id` (dependency providers)
- **Authorization**: `require_license` (universal dependency for all endpoints)
- **Service Layer**: `PocketService`, `SessionService` for business logic
- **Schemas**: Request/response validation models (`CreatePocketRequest`, `UpdatePocketRequest`, `AddCollaboratorRequest`, etc.)

## Architecture Patterns
- **Router Dependencies**: All endpoints require license validation via `require_license`
- **User Context**: User and workspace extracted via dependency injection
- **Service Delegation**: Business logic delegated to `PocketService` and `SessionService`
- **Status Code Convention**: Successful deletions return 204 No Content
- **Token-based Sharing**: Public endpoint for share link access (no auth required)
- **Flexible Request Parsing**: Agent ID supports both `agentId` and `agent_id` keys for compatibility

## Usage Context
This router is mounted at the `/pockets` prefix and integrated into the application's main FastAPI app. All endpoints operate within workspace and user context, ensuring multi-tenancy and access control.

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
