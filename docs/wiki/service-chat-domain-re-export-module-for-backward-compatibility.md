# service — Chat domain re-export module for backward compatibility

> A thin re-export module that provides backward-compatible access to chat domain services. It consolidates and re-exports GroupService and MessageService from their specialized modules (group_service.py and message_service.py), which were refactored to improve performance and maintainability. This module serves as the public API facade for the chat domain.

**Categories:** chat domain, API facade, service layer, refactoring  
**Concepts:** GroupService, MessageService, _group_response, _message_response, re-export, backward compatibility, facade pattern, N+1 query optimization, create_agent_message  
**Words:** 211 | **Version:** 1

---

## Purpose
Provide backward-compatible re-exports of chat domain services after internal refactoring. This module allows existing code to continue importing from the original location while the actual implementations have been moved to specialized, optimized modules.

## Key Classes and Functions

### GroupService
- Re-exported from `ee.cloud.chat.group_service`
- Handles group-related operations in the chat domain
- Includes N+1 query fixes for improved performance

### _group_response
- Helper function re-exported from `ee.cloud.chat.group_service`
- Formats group data for API responses

### MessageService
- Re-exported from `ee.cloud.chat.message_service`
- Manages message operations and creation
- Includes new `create_agent_message` functionality

### _message_response
- Helper function re-exported from `ee.cloud.chat.message_service`
- Formats message data for API responses

## Dependencies
Internal domain modules:
- `group_service` — group management implementation
- `message_service` — message management implementation
- `schemas`, `agent`, `errors`, `user`, `pocket`, `session`, `ripple_normalizer`, `events`, `message`, `invite`, `workspace`, `permissions` — supporting chat domain components

## Architecture Notes
- Implements the **Facade Pattern** for backward compatibility
- Part of refactoring that separated concerns into specialized modules
- Re-exports marked with `# noqa: F401` to suppress unused import warnings
- Consumed by `router` and `agent_bridge` modules

## Usage Examples
```python
# Instead of importing from message_service directly:
from ee.cloud.chat.service import MessageService, _message_response

# Or from group_service directly:
from ee.cloud.chat.service import GroupService, _group_response
```

---

## Related

- [schemas-workspace-domain-requestresponse-models](schemas-workspace-domain-requestresponse-models.md)
- [agent-agent-configuration-models-for-the-cloud-platform](agent-agent-configuration-models-for-the-cloud-platform.md)
- [errors-unified-error-hierarchy-for-cloud-module](errors-unified-error-hierarchy-for-cloud-module.md)
- [user-enterprise-user-and-oauth-account-models](user-enterprise-user-and-oauth-account-models.md)
- [groupservice-group-and-channel-business-logic-crud-membership-agents-dms](groupservice-group-and-channel-business-logic-crud-membership-agents-dms.md)
- [messageservice-message-business-logic-and-crud-operations](messageservice-message-business-logic-and-crud-operations.md)
- [pocket-pocket-workspace-and-widget-document-models](pocket-pocket-workspace-and-widget-document-models.md)
- [session-chat-session-document-model](session-chat-session-document-model.md)
- [ripplenormalizer-ai-generated-ripplespec-validation-and-normalization](ripplenormalizer-ai-generated-ripplespec-validation-and-normalization.md)
- [events-internal-async-event-bus-for-cross-domain-side-effects](events-internal-async-event-bus-for-cross-domain-side-effects.md)
- [message-group-chat-message-document-model](message-group-chat-message-document-model.md)
- [invite-workspace-membership-invitation-management](invite-workspace-membership-invitation-management.md)
- [workspace-workspace-document-model-for-deployments-and-organizations](workspace-workspace-document-model-for-deployments-and-organizations.md)
- [permissions-role-and-access-level-permission-checks](permissions-role-and-access-level-permission-checks.md)
- [router-workspace-domain-fastapi-endpoints](router-workspace-domain-fastapi-endpoints.md)
- [agentbridge-cloud-chat-event-bridge-to-pocketpaw-agent-pool](agentbridge-cloud-chat-event-bridge-to-pocketpaw-agent-pool.md)
