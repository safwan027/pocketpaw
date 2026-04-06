# event_handlers — Cross-domain event handlers for workspace side effects

> Provides async event handlers that react to domain events (invites, messages, pocket sharing, member removal) and execute side effects that span multiple domain boundaries. Registered on app startup via register_event_handlers(), these handlers bridge the gap between independent domain models by coordinating group membership, notifications, and cleanup logic through a central event bus.

**Categories:** event handling, notifications, group management, workspace lifecycle, cloud infrastructure  
**Concepts:** event_bus, register_event_handlers, _on_invite_accepted, _on_message_sent, _on_pocket_shared, _on_member_removed, _create_notification, publish-subscribe pattern, cross-domain side effects, deferred imports  
**Words:** 602 | **Version:** 1

---

## Purpose

The `event_handlers` module implements the subscriber side of PocketPaw's publish-subscribe event system. Domain actions such as accepting an invite, sending a message, sharing a pocket, or removing a workspace member each trigger cross-cutting side effects — group membership updates, notification creation, statistics tracking, and access revocation. By isolating these reactions into dedicated handlers wired through `event_bus`, the module keeps individual domain models decoupled while ensuring consistent orchestration of secondary effects.

## Key Functions

### `register_event_handlers()`
Synchronous setup function called at app startup. Subscribes all handler functions to their respective event topics on the shared `event_bus`:
- `"invite.accepted"` → `_on_invite_accepted`
- `"message.sent"` → `_on_message_sent`
- `"pocket.shared"` → `_on_pocket_shared`
- `"member.removed"` → `_on_member_removed`

### `_on_invite_accepted(data)`
Handles the `invite.accepted` event. If the invite includes a `group_id`, auto-adds the accepting user to that group's member list. Also creates an `"invite"` notification confirming workspace join.

### `_on_message_sent(data)`
Handles the `message.sent` event. Performs two tasks:
1. **Group stats update** — increments `message_count` and sets `last_message_at` on the target group.
2. **Mention notifications** — iterates over `mentions` in the message data and creates `"mention"` notifications for each referenced user (excluding the sender). Notification body is truncated to 100 characters.

### `_on_pocket_shared(data)`
Handles the `pocket.shared` event. Creates a `"pocket_shared"` notification for the target user, including a `NotificationSource` linking back to the shared pocket.

### `_on_member_removed(data)`
Handles the `member.removed` event. Performs full workspace cleanup for the removed user:
1. **Group membership** — queries all groups in the workspace containing the user and removes them from each group's member list.
2. **Pocket access revocation** — queries all pockets shared with the user in that workspace and removes the user from each pocket's `shared_with` list.

### `_create_notification(workspace_id, recipient, type, title, body, source_type, source_id, pocket_id)`
Shared helper that constructs and inserts a `Notification` document via Beanie ODM. Optionally attaches a `NotificationSource` when `source_type` and `source_id` are provided. All exceptions are caught and logged to prevent notification failures from disrupting upstream event processing.

## Dependencies

| Dependency | Role |
|---|---|
| `ee.cloud.shared.events.event_bus` | Central pub-sub bus for subscribing to domain events |
| `ee.cloud.models.group.Group` | Beanie document model for groups (lazy-imported) |
| `ee.cloud.models.pocket.Pocket` | Beanie document model for pockets (lazy-imported) |
| `ee.cloud.models.notification.Notification` | Beanie document model for notifications (lazy-imported) |
| `ee.cloud.models.notification.NotificationSource` | Embedded model for notification source metadata |
| `beanie.PydanticObjectId` | MongoDB ObjectId casting for document lookups |

All domain model imports are deferred (inside function bodies) to avoid circular import issues, since `event_handlers` sits at the boundary between multiple domain modules.

## Design Patterns

- **Event-driven architecture** — handlers are decoupled from event publishers; new side effects can be added without modifying emitting code.
- **Deferred imports** — model imports inside handler functions prevent circular dependency chains across the `group`, `pocket`, and `notification` domains.
- **Defensive error handling** — each handler wraps database operations in try/except blocks with `logger.exception()`, ensuring one failing side effect does not prevent others from executing.
- **Single registration entry point** — `register_event_handlers()` provides a clear, auditable list of all subscriptions, typically called from the app's `__init__` or startup hook.

## Usage Examples

```python
# At application startup (typically in __init__.py)
from ee.cloud.shared.event_handlers import register_event_handlers

register_event_handlers()
```

```python
# Publishing an event that triggers the handlers (from another module)
from ee.cloud.shared.events import event_bus

await event_bus.emit("invite.accepted", {
    "group_id": "663a1f...",
    "user_id": "user_abc",
    "workspace_id": "ws_123",
})
```

## Event Contract Reference

| Event | Required Fields | Optional Fields |
|---|---|---|
| `invite.accepted` | `user_id` | `group_id`, `workspace_id` |
| `message.sent` | `group_id` | `sender_id`, `mentions`, `workspace_id`, `content` |
| `pocket.shared` | `target_user_id`, `pocket_id` | `workspace_id`, `pocket_name` |
| `member.removed` | `workspace_id`, `user_id` | — |