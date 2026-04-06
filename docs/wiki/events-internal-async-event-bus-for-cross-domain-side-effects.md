# events — Internal async event bus for cross-domain side effects

> Provides a simple in-process pub/sub event bus that enables decoupled communication between domains without direct imports. Allows domains to subscribe to and emit events, enabling cross-cutting concerns like notifications and group management to react to domain events without tight coupling.

**Categories:** messaging, event-driven architecture, async patterns, cloud infrastructure  
**Concepts:** EventBus, pub/sub, async handlers, event subscription, event emission, error handling, decoupling, cross-domain communication  
**Words:** 278 | **Version:** 2

---

## Purpose
The `events` module implements a lightweight, in-process pub/sub system for asynchronous event-driven architecture. It prevents tight coupling between domains by allowing them to communicate through events rather than direct imports.

## Key Classes

### EventBus
Simple in-process async pub/sub event bus.

**Attributes:**
- `_handlers`: `defaultdict[str, list[Handler]]` — Maps event names to lists of async handler functions

**Methods:**
- `__init__() -> None` — Initializes the handlers dictionary
- `subscribe(event: str, handler: Handler) -> None` — Registers an async handler for a specific event
- `unsubscribe(event: str, handler: Handler) -> None` — Removes a handler from an event (no-op if not subscribed)
- `async emit(event: str, data: dict[str, Any]) -> None` — Emits an event to all registered handlers in subscription order; logs exceptions without stopping other handlers

## Key Types

**Handler:** `Callable[[dict[str, Any]], Coroutine[Any, Any, None]]` — Async function signature for event handlers

## Module-Level Instance

- `event_bus: EventBus` — Singleton instance used throughout the cloud module

## Usage Examples

```python
from ee.cloud.shared.events import event_bus

# Define an async event handler
async def on_invite_accepted(data: dict[str, Any]) -> None:
    user_id = data["user_id"]
    await create_notification(user_id, "Invite accepted")
    await add_user_to_group(user_id, data["group_id"])

# Subscribe to an event
event_bus.subscribe("invite.accepted", on_invite_accepted)

# Emit an event
await event_bus.emit("invite.accepted", {"user_id": 123, "group_id": 456})

# Unsubscribe from an event
event_bus.unsubscribe("invite.accepted", on_invite_accepted)
```

## Dependencies

- **Standard Library:** `logging`, `collections.defaultdict`, `collections.abc.Coroutine`, `typing`
- **Internal:** None within scanned set
- **Imported By:** `message_service`, `service`, `agent_bridge`, `event_handlers`

## Design Patterns

- **Pub/Sub Pattern:** Decoupled event publishing and subscription
- **Async-First Design:** All handlers are coroutines, enabling non-blocking event processing
- **Error Isolation:** Handler exceptions are logged without stopping subsequent handlers
- **Singleton Pattern:** Module-level `event_bus` instance provides global access

---

## Related

- [messageservice-message-business-logic-and-crud-operations](messageservice-message-business-logic-and-crud-operations.md)
- [workspaceservice-workspace-domain-business-logic](workspaceservice-workspace-domain-business-logic.md)
- [agentbridge-cloud-chat-event-bridge-to-pocketpaw-agent-pool](agentbridge-cloud-chat-event-bridge-to-pocketpaw-agent-pool.md)
- [eventhandlers-cross-domain-event-processing-and-notifications](eventhandlers-cross-domain-event-processing-and-notifications.md)
