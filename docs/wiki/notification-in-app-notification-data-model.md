# notification — In-app notification data model

> Defines the data models for in-app notifications in the pocketPaw system. Provides a Notification document class for storing user notifications with metadata about the source, read status, and expiration. Integrates with Beanie ODM for MongoDB persistence with indexed queries for efficient retrieval.

**Categories:** notification system, data models, cloud infrastructure, MongoDB/Beanie  
**Concepts:** NotificationSource, Notification, TimestampedDocument, Beanie ODM, MongoDB indexing, data validation, multi-tenancy (workspace), notification types (mention, comment, reply, invite, agent_complete, pocket_shared), read status tracking, notification expiration  
**Words:** 295 | **Version:** 1

---

## Purpose
This module defines the data structure for in-app notifications that are delivered to users within the pocketPaw application. It handles notification persistence, indexing, and metadata management.

## Key Classes

### NotificationSource
A Pydantic BaseModel representing the origin of a notification:
- **type** (str): The category of the notification source
- **id** (str): Unique identifier of the source entity
- **pocket_id** (str | None): Optional reference to an associated pocket

### Notification
A Beanie TimestampedDocument (MongoDB document) representing a user notification with the following fields:
- **workspace** (Indexed[str]): Workspace identifier for multi-tenancy
- **recipient** (Indexed[str]): User ID of the notification recipient
- **type** (str): Notification category (mention, comment, reply, invite, agent_complete, pocket_shared)
- **title** (str): Notification headline
- **body** (str): Notification message content (optional, defaults to empty)
- **source** (NotificationSource | None): Optional metadata about the notification source
- **read** (bool): Flag indicating whether the user has read the notification
- **expires_at** (datetime | None): Optional expiration timestamp for the notification
- **created_at** (datetime): Auto-managed timestamp from TimestampedDocument parent class
- **updated_at** (datetime): Auto-managed timestamp from TimestampedDocument parent class

**Database Settings:**
- Collection name: "notifications"
- Composite index: (recipient, read, created_at descending) for efficient queries of unread notifications

## Dependencies
- **beanie**: MongoDB ODM for document persistence and indexing
- **pydantic**: Data validation and serialization
- **ee.cloud.models.base.TimestampedDocument**: Base class providing timestamp management

## Usage Examples
```python
# Create a notification instance
notification = Notification(
    workspace="workspace_123",
    recipient="user_456",
    type="mention",
    title="You were mentioned",
    body="John mentioned you in a comment",
    source=NotificationSource(
        type="comment",
        id="comment_789",
        pocket_id="pocket_abc"
    ),
    read=False,
    expires_at=datetime.now() + timedelta(days=30)
)

# Query unread notifications for a user
unread = await Notification.find(
    {"recipient": "user_456", "read": False}
).sort([("created_at", -1)]).to_list()
```

## Related Modules
- **Imported by**: __init__ (module exports), event_handlers (notification triggering logic)
- **Depends on**: base (TimestampedDocument parent class)

---

## Related

- [base-timestamped-document-base-class](base-timestamped-document-base-class.md)
- [eecloudworkspace-workspace-module-initialization](eecloudworkspace-workspace-module-initialization.md)
- [eventhandlers-cross-domain-event-processing-and-notifications](eventhandlers-cross-domain-event-processing-and-notifications.md)
