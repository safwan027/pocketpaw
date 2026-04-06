# event_handlers — Cross-domain event processing and notifications

> Handles asynchronous side effects that span multiple domains (groups, pockets, notifications, invites) by subscribing to application events. Processes domain events on startup and executes cross-cutting concerns like auto-membership, notification creation, and cleanup operations.

**Categories:** event-driven architecture, cross-domain coordination, notification system, group management, pocket sharing, workspace membership  
**Concepts:** _on_invite_accepted, _on_message_sent, _on_pocket_shared, _on_member_removed, _create_notification, register_event_handlers, event_bus, Event Handler pattern, Event Bus pattern, Cross-domain side effects  
**Words:** 465 | **Version:** 1

---

## Purpose

This module implements the event-driven architecture for the application by acting as a mediator between different business domains. It centralizes all cross-domain side effects—operations that affect multiple entities across domain boundaries—and registers them to the event bus at application startup.

## Architecture Pattern

The module follows the **Event Handler** and **Event Bus** patterns:
- Async event handlers subscribe to domain events
- Each handler performs side effects relevant to multiple domains
- Centralized registration via `register_event_handlers()` wires up subscriptions

## Key Functions

### Event Handlers

**`_on_invite_accepted(data: dict)`**
- Auto-adds users to groups when they accept an invite containing `group_id`
- Creates a notification confirming the group membership
- Handles validation and error logging

**`_on_message_sent(data: dict)`**
- Updates group statistics (`last_message_at`, `message_count`)
- Creates mention notifications for referenced users
- Filters out self-mentions
- Truncates message body to 100 characters

**`_on_pocket_shared(data: dict)`**
- Creates notifications when a pocket is shared with a user
- Attaches pocket metadata to notification source

**`_on_member_removed(data: dict)`**
- Cleans up group memberships when a user is removed from workspace
- Revokes pocket access for the removed user
- Cascading delete across related entities

### Utility Functions

**`_create_notification(...)`**
- Factory method for creating notification documents
- Accepts optional source references (type, id, pocket_id)
- Handles insertion failures gracefully

**`register_event_handlers()`**
- Subscribes all handlers to their respective events:
  - `invite.accepted` → `_on_invite_accepted`
  - `message.sent` → `_on_message_sent`
  - `pocket.shared` → `_on_pocket_shared`
  - `member.removed` → `_on_member_removed`
- Called during application startup

## Dependencies

- **events**: `event_bus` for pub/sub mechanism
- **group**: `Group` model for membership operations
- **pocket**: `Pocket` model for access revocation
- **notification**: `Notification` and `NotificationSource` models
- **beanie**: `PydanticObjectId` for MongoDB object ID handling
- **logging**: Standard library logging

## Data Flow

```
Domain Event → Event Bus → Handler Subscription → Side Effects
                                                   ├─ Model updates (Group, Pocket)
                                                   └─ Notification creation
```

## Error Handling

All handlers implement defensive error handling:
- Validation of required fields (`group_id`, `user_id`, etc.)
- Try-catch blocks with exception logging
- Graceful degradation on failures
- No raising of exceptions to event bus

## Usage Example

```python
# In application initialization
from ee.cloud.shared.event_handlers import register_event_handlers

register_event_handlers()  # Wire up subscriptions

# Events are now automatically processed
# Example: When a message is sent
event_bus.emit('message.sent', {
    'group_id': 'grp_123',
    'sender_id': 'user_456',
    'mentions': [{'type': 'user', 'id': 'user_789'}],
    'content': '@user_789 check this out',
    'workspace_id': 'ws_001'
})
# Handler automatically:
# - Updates group.last_message_at and message_count
# - Creates notification for mentioned user
```

## Key Design Decisions

1. **Async-first**: All handlers are async to support concurrent operations
2. **Lazy imports**: Domain models imported inside handlers to avoid circular dependencies
3. **Defensive nullability**: All data access checked before use
4. **Centralized registration**: Single source of truth for event subscriptions
5. **Separation of concerns**: Handlers isolated per domain event type

---

## Related

- [events-internal-async-event-bus-for-cross-domain-side-effects](events-internal-async-event-bus-for-cross-domain-side-effects.md)
- [group-multi-user-chat-channels-with-ai-agent-participants](group-multi-user-chat-channels-with-ai-agent-participants.md)
- [pocket-pocket-workspace-and-widget-document-models](pocket-pocket-workspace-and-widget-document-models.md)
- [notification-in-app-notification-data-model](notification-in-app-notification-data-model.md)
- [eecloudworkspace-workspace-module-initialization](eecloudworkspace-workspace-module-initialization.md)
