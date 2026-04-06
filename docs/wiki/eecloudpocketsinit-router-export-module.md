# ee.cloud.pockets.__init__ — Router Export Module

> This module serves as the public API entry point for the pockets package, exporting the router object for handling pocket-related HTTP endpoints and requests. It acts as a facade that re-exports core routing functionality while maintaining clean package boundaries.

**Categories:** cloud infrastructure, API routing, package initialization  
**Concepts:** router export, package facade pattern, API entry point, re-export, public interface  
**Words:** 179 | **Version:** 1

---

## Purpose
Provides a clean public interface for the pockets package by exporting the router module, enabling callers to import routing functionality directly from the pockets package level.

## Key Classes/Functions
- **router**: FastAPI/Starlette-compatible router object imported from `ee.cloud.pockets.router` that handles all pocket-related HTTP routes and request handling

## Dependencies
- `ee.cloud.pockets.router`: Core module containing the router definition and endpoint handlers

## Related Modules
This package integrates with multiple submodules for complete pocket management functionality:
- `errors`: Exception and error handling
- `workspace`: Workspace integration
- `license`: License management
- `user`: User management and authentication
- `agent`: Agent-related operations
- `comment`, `file`, `group`, `invite`, `message`, `notification`: Domain entities
- `session`: Session management
- `event_handlers`: Event-driven functionality
- `agent_bridge`: Agent communication interface
- `core`: Core utilities and business logic
- `deps`: Dependency injection

## Usage Examples
```python
from ee.cloud.pockets import router

# Include the router in main FastAPI application
app.include_router(router)
```

## Notes
- The `# noqa: F401` comment suppresses unused import warnings, indicating the import is intentionally for re-export
- Follows Python packaging convention of centralizing imports in `__init__.py`

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
