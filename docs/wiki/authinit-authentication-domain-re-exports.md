# auth.__init__ — Authentication domain re-exports

> This module serves as the public API entry point for the authentication domain, re-exporting core authentication components and routing functionality. It provides backward compatibility by centralizing imports from internal submodules (core and router), allowing consumers to import authentication utilities from a single location.

**Categories:** authentication, user management, API infrastructure  
**Concepts:** UserRead, UserCreate, UserManager, fastapi_users, cookie_backend, bearer_backend, current_active_user, current_optional_user, get_jwt_strategy, get_user_manager  
**Words:** 197 | **Version:** 1

---

## Purpose
The `__init__.py` module acts as a facade for the authentication domain, aggregating and re-exporting authentication infrastructure components. This pattern enables clean public APIs and simplifies dependency management across the application.

## Re-exported Components

### User Management
- **UserRead**: User data model for API responses
- **UserCreate**: User data model for creation requests
- **UserManager**: Core user management service

### Authentication Backends
- **fastapi_users**: FastAPI Users integration instance
- **cookie_backend**: Cookie-based authentication strategy
- **bearer_backend**: Bearer token authentication strategy
- **get_jwt_strategy()**: JWT strategy factory function

### User Context Functions
- **current_active_user**: Dependency for retrieving authenticated user
- **current_optional_user**: Dependency for optionally authenticated requests

### Utilities & Configuration
- **get_user_manager()**: User manager factory function
- **get_user_db()**: Database access layer factory
- **seed_admin()**: Administrative user initialization function
- **SECRET**: JWT signing secret constant
- **TOKEN_LIFETIME**: Token expiration duration constant

### Routing
- **router**: FastAPI router with authentication endpoints

## Dependencies
All components originate from two internal submodules:
- `ee.cloud.auth.core`: Core authentication logic and configuration
- `ee.cloud.auth.router`: API route definitions

## Usage Pattern
Consumers import directly from the auth domain:
```python
from ee.cloud.auth import current_active_user, UserRead, router
```

Rather than accessing nested submodules directly, reducing coupling and supporting refactoring.

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
