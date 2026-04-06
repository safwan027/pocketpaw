# base — Timestamped Document Base Class

> Provides a base document class that automatically manages createdAt and updatedAt timestamps for MongoDB documents. All domain models in the system inherit from TimestampedDocument to ensure consistent timestamp tracking across insert, update, and replace operations.

**Categories:** data models, database layer, mongodb, core infrastructure  
**Concepts:** TimestampedDocument, _set_created, _set_updated, before_event, Insert, Update, Replace, Save, Document, Beanie ODM  
**Words:** 249 | **Version:** 1

---

## Purpose
This module defines the foundational document class for the pocketPaw application, enabling automatic timestamp management at the database level. It leverages Beanie's event hooks to intercept database operations and maintain accurate creation and modification timestamps.

## Key Classes

### TimestampedDocument
Base class extending Beanie's `Document` for all data models.

**Fields:**
- `createdAt` (datetime): Set once at document creation, defaults to current UTC time
- `updatedAt` (datetime): Set at creation and updated on every modification, defaults to current UTC time

**Methods:**
- `_set_created()`: Executed before Insert events; sets both createdAt and updatedAt to current UTC time
- `_set_updated()`: Executed before Replace, Save, and Update events; updates only the updatedAt field

**Configuration:**
- `use_state_management = True`: Enables Beanie's state tracking for change detection

## Dependencies
- `beanie`: ODM (Object Document Mapper) for MongoDB providing Document base class and event decorators
- `pydantic`: Field validation and schema management
- `datetime`: UTC timezone and datetime handling

## Usage Examples

```python
# Inherit from TimestampedDocument in domain models
from ee.cloud.models.base import TimestampedDocument

class User(TimestampedDocument):
    name: str
    email: str
    # createdAt and updatedAt inherited automatically

# Timestamps managed automatically
user = User(name='John', email='john@example.com')
await user.insert()  # createdAt and updatedAt set

# updatedAt changes on modification
user.name = 'Jane'
await user.save()  # updatedAt refreshed
```

## Event Flow
1. **Insert**: Both timestamps set to current time
2. **Save/Update/Replace**: Only updatedAt refreshed
3. **Query**: Timestamps available on all retrieved documents

## Design Pattern
Base class pattern with Beanie lifecycle hooks (before_event) for cross-cutting timestamp concerns.

---

## Related

- [agent-agent-configuration-models-for-the-cloud-platform](agent-agent-configuration-models-for-the-cloud-platform.md)
- [comment-threaded-comments-on-pockets-and-widgets](comment-threaded-comments-on-pockets-and-widgets.md)
- [group-multi-user-chat-channels-with-ai-agent-participants](group-multi-user-chat-channels-with-ai-agent-participants.md)
- [message-group-chat-message-document-model](message-group-chat-message-document-model.md)
- [notification-in-app-notification-data-model](notification-in-app-notification-data-model.md)
- [pocket-pocket-workspace-and-widget-document-models](pocket-pocket-workspace-and-widget-document-models.md)
- [session-chat-session-document-model](session-chat-session-document-model.md)
- [workspace-workspace-document-model-for-deployments-and-organizations](workspace-workspace-document-model-for-deployments-and-organizations.md)
