# Cloud Models __init__ — Beanie document model re-exports

> Central re-export module that aggregates all cloud document models for Beanie ODM initialization. Provides a single import point for all document classes used in the cloud persistence layer and defines the complete set of documents to be registered with the database.

**Categories:** Cloud Infrastructure, Data Models, Database Layer, ODM/ORM  
**Concepts:** Beanie ODM, Document model aggregation, Re-export pattern, Model registration, User, Agent, Workspace, Message, Pocket, Notification, Comment, Session, Embedded documents and nested models  
**Words:** 219 | **Version:** 1

---

## Purpose
This module serves as the public API for cloud document models, consolidating imports from specialized model submodules and providing `ALL_DOCUMENTS` constant for Beanie ODM initialization.

## Key Classes/Functions

### Exported Classes
- **User**: User account model with OAuth integration
- **Agent**: AI agent entity with configuration
- **Pocket**: Primary user content container
- **Session**: User session management
- **Comment**: Threaded comments with author and target tracking
- **Notification**: User notifications with source tracking
- **FileObj**: File storage and metadata
- **Workspace**: Collaborative workspace container
- **Group**: User grouping mechanism
- **Message**: Chat/messaging entities
- **Invite**: Workspace invitation model
- **Supporting Classes**: CommentAuthor, CommentTarget, GroupAgent, Message (Mention, Attachment, Reaction), NotificationSource, OAuthAccount, Widget, WidgetPosition, WorkspaceMembership, WorkspaceSettings

### Constants
- **ALL_DOCUMENTS**: List of 11 primary document classes for Beanie collection registration

## Dependencies
Imports from 12 sibling modules within `ee.cloud.models.*`:
- agent, comment, file, group, invite, message, notification, pocket, session, user, workspace

## Usage Examples
```python
# In Beanie initialization:
from ee.cloud.models import ALL_DOCUMENTS
await init_beanie(database=db, models=ALL_DOCUMENTS)

# Direct imports:
from ee.cloud.models import User, Agent, Workspace, Message
```

## Architecture Notes
- Uses `from __future__ import annotations` for forward compatibility
- Implements star-export pattern for clean public API
- Separates collection registration (ALL_DOCUMENTS) from full model catalog
- Not all imported classes included in ALL_DOCUMENTS (e.g., CommentAuthor, Reaction are omitted)

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
