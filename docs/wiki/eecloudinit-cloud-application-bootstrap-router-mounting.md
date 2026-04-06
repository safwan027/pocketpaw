# ee.cloud.__init__ — Cloud Application Bootstrap & Router Mounting

> This module initializes the PocketPaw Enterprise Cloud FastAPI application by mounting all domain-driven routers, registering global error handlers, and configuring cross-domain event systems. It serves as the single entry point for assembling the cloud API, WebSocket endpoints, and agent pool lifecycle management.

**Categories:** cloud infrastructure, api initialization, domain-driven design, fastapi configuration  
**Concepts:** mount_cloud, CloudError, cloud_error_handler, domain-driven architecture, router mounting, FastAPI lifecycle hooks, dependency injection, agent pool, event handlers, agent bridge  
**Words:** 394 | **Version:** 1

---

## Purpose
The `__init__` module implements the cloud layer initialization using domain-driven design (DDD). It orchestrates the mounting of 7 domain routers (auth, workspace, agents, chat, pockets, sessions, kb) and wires up shared infrastructure including error handling, event dispatch, agent bridging, and user search functionality.

## Key Functions

### `mount_cloud(app: FastAPI) → None`
Main initialization function that:
- **Registers global error handler** for `CloudError` exceptions with JSON serialization
- **Mounts 7 domain routers** at `/api/v1` prefix:
  - `auth_router` — authentication & authorization
  - `workspace_router` — workspace management
  - `agents_router` — agent operations
  - `chat_router` — messaging & chat
  - `pockets_router` — pocket/document management
  - `sessions_router` — session handling
  - `kb_router` — knowledge base operations
- **Registers utility endpoints**:
  - `GET /api/v1/users` — user search with regex patterns (email, full_name)
  - `GET /api/v1/license` — license info (unauthenticated)
  - `WebSocket /ws/cloud` — real-time chat endpoint
- **Initializes cross-domain infrastructure**:
  - Event handler registration for inter-domain communication
  - Agent bridge for agent pool integration
- **Manages app lifecycle**:
  - `startup` hook: starts agent pool
  - `shutdown` hook: stops agent pool

## Architecture

### Domain-Driven Structure
Each domain follows the pattern:
- `router.py` — thin HTTP layer
- `service.py` — business logic
- `schemas.py` — request/response validation

### Error Handling
Centralized via `CloudError` exception class with status codes and `to_dict()` serialization for JSON responses.

### Dependencies & Injection
Uses FastAPI `Depends()` for:
- `current_user` — authenticated user context
- `current_workspace_id` — workspace isolation

## Usage Example
```python
from fastapi import FastAPI
from ee.cloud import mount_cloud

app = FastAPI()
mount_cloud(app)  # All routers, handlers, and lifecycle hooks configured

# Now app is ready to run with uvicorn
# uvicorn main:app --reload
```

## Endpoint Summary

| Method | Path | Purpose | Auth |
|--------|------|---------|------|
| GET | `/api/v1/users` | Search users by email/name | Required |
| GET | `/api/v1/license` | License information | None |
| WS | `/ws/cloud` | Real-time chat WebSocket | Token |
| * | `/api/v1/auth/*` | Auth domain | Varies |
| * | `/api/v1/workspace/*` | Workspace domain | Required |
| * | `/api/v1/agents/*` | Agent domain | Required |
| * | `/api/v1/chat/*` | Chat domain | Required |
| * | `/api/v1/pockets/*` | Pockets domain | Required |
| * | `/api/v1/sessions/*` | Sessions domain | Required |
| * | `/api/v1/kb/*` | Knowledge base domain | Required |

---

## Related

- [errors-unified-error-hierarchy-for-cloud-module](errors-unified-error-hierarchy-for-cloud-module.md)
- [router-workspace-domain-fastapi-endpoints](router-workspace-domain-fastapi-endpoints.md)
- [workspace-workspace-document-model-for-deployments-and-organizations](workspace-workspace-document-model-for-deployments-and-organizations.md)
- [license-enterprise-license-validation-for-cloud-features](license-enterprise-license-validation-for-cloud-features.md)
- [user-enterprise-user-and-oauth-account-models](user-enterprise-user-and-oauth-account-models.md)
- [deps-fastapi-dependency-injection-for-cloud-authentication-and-authorization](deps-fastapi-dependency-injection-for-cloud-authentication-and-authorization.md)
- [eventhandlers-cross-domain-event-processing-and-notifications](eventhandlers-cross-domain-event-processing-and-notifications.md)
- [agentbridge-cloud-chat-event-bridge-to-pocketpaw-agent-pool](agentbridge-cloud-chat-event-bridge-to-pocketpaw-agent-pool.md)
- [core-enterprise-authentication-with-fastapi-users-jwt-and-multi-transport](core-enterprise-authentication-with-fastapi-users-jwt-and-multi-transport.md)
- [agent-agent-configuration-models-for-the-cloud-platform](agent-agent-configuration-models-for-the-cloud-platform.md)
- [comment-threaded-comments-on-pockets-and-widgets](comment-threaded-comments-on-pockets-and-widgets.md)
- [file-file-metadata-document-storage](file-file-metadata-document-storage.md)
- [group-multi-user-chat-channels-with-ai-agent-participants](group-multi-user-chat-channels-with-ai-agent-participants.md)
- [invite-workspace-membership-invitation-management](invite-workspace-membership-invitation-management.md)
- [message-group-chat-message-document-model](message-group-chat-message-document-model.md)
- [notification-in-app-notification-data-model](notification-in-app-notification-data-model.md)
- [pocket-pocket-workspace-and-widget-document-models](pocket-pocket-workspace-and-widget-document-models.md)
- [session-chat-session-document-model](session-chat-session-document-model.md)
