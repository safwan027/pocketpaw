# message_service — Message business logic and CRUD operations

> Stateless service providing comprehensive message operations including sending, editing, deleting, reacting, threading, pinning, and searching within chat groups. Handles authorization checks, group membership validation, soft-deletion semantics, and event emission for message lifecycle events.

**Categories:** chat domain, message management, business logic, CRUD operations, authorization, event emission  
**Concepts:** MessageService, send_message, create_agent_message, edit_message, delete_message, toggle_reaction, get_messages, get_thread, pin_message, unpin_message  
**Words:** 527 | **Version:** 1

---

## Purpose

The `message_service` module encapsulates all message-related business logic for the chat domain. It serves as the single entry point for message operations, enforcing authorization rules, managing group metadata updates, and emitting domain events.

## Key Classes and Functions

### MessageService

Stateless service class with static methods for all message operations:

- **send_message()** — Create and persist a user message, verify group membership and archived status, update group stats, emit `message.sent` event
- **create_agent_message()** — Create a message from an agent (used by agent_bridge), persist to database, update group metadata
- **edit_message()** — Modify message content, set edited flag and timestamp, author-only authorization
- **delete_message()** — Soft-delete a message (author or group owner), maintains audit trail
- **toggle_reaction()** — Add/remove emoji reactions, manage reaction user lists, clean up empty reactions
- **get_messages()** — Cursor-based pagination (newest-first), membership verification, excludes deleted messages
- **get_thread()** — Retrieve all replies to a message sorted chronologically, verify group access
- **pin_message()** — Pin a message in group, admin-only, verify message belongs to group
- **unpin_message()** — Remove pinned message, admin-only, raise NotFound if not pinned
- **search_messages()** — Full-text regex search with safe escaping, limit 50 results, membership check

### Helper Functions

- **_message_response()** — Convert Message document to frontend-compatible dict with ISO timestamp formatting
- **_get_message_or_404()** — Load message by ID, raise NotFound if missing or soft-deleted

## Dependencies

- **group_service** — Group lookup and authorization helpers (`_get_group_or_404`, `_require_group_member`, `_require_group_admin`)
- **schemas** — Request DTOs (`SendMessageRequest`, `EditMessageRequest`)
- **message** — Message model and related types (`Message`, `Attachment`, `Mention`, `Reaction`)
- **errors** — Exception types (`Forbidden`, `NotFound`)
- **events** — Event bus for async event emission

## Design Patterns

### Authorization Layering

Multi-level authorization checks:
1. Group existence and accessibility (public vs. private/DM membership)
2. Group state validation (archived, active)
3. Resource ownership (author for edit/delete, owner for pin/unpin, admin for moderation)

### Soft-Deletion

Messages are marked `deleted=True` rather than removed, preserving referential integrity for threads and reactions. Helper functions filter deleted messages transparently.

### Cursor-Based Pagination

Implements compound cursor `"{iso_timestamp}|{object_id}"` to handle duplicate timestamps correctly, queries with compound sort and comparison operators, fetches `limit+1` to determine `has_more` flag.

### Event-Driven Architecture

Message operations emit domain events (`message.sent`) with relevant context (group_id, sender_id, workspace_id) for downstream processing by notifications, search indexing, etc.

## Usage Examples

```python
# Send a user message
response = await MessageService.send_message(
    group_id="group123",
    user_id="user456",
    body=SendMessageRequest(
        content="Hello!",
        mentions=[{"userId": "user789", "name": "Alice"}],
        attachments=[],
        reply_to=None
    )
)

# Create agent message
msg = await MessageService.create_agent_message(
    group_id="group123",
    agent_id="agent_bot",
    content="I found the answer...",
    attachments=[]
)

# Get paginated messages
page = await MessageService.get_messages(
    group_id="group123",
    user_id="user456",
    cursor=None,
    limit=50
)

# Toggle reaction
await MessageService.toggle_reaction(
    message_id="msg789",
    user_id="user456",
    emoji="👍"
)

# Search messages
results = await MessageService.search_messages(
    group_id="group123",
    user_id="user456",
    query="important keyword"
)
```

## Key Abstractions

- **Message Document** — Persistent entity with creation timestamp, soft-delete flag, edit tracking, reaction aggregation
- **Reaction** — Emoji with user list, supports toggle semantics
- **Cursor Token** — Opaque pagination marker enabling stable iteration over sorted message streams
- **Access Control** — Role-based (owner/admin/member) and resource-based (author) authorization

## Async-First Design

All methods are async, enabling non-blocking database I/O, event bus operations, and integration with concurrent chat operations.

---

## Related

- [groupservice-group-and-channel-business-logic-crud-membership-agents-dms](groupservice-group-and-channel-business-logic-crud-membership-agents-dms.md)
- [schemas-workspace-domain-requestresponse-models](schemas-workspace-domain-requestresponse-models.md)
- [message-group-chat-message-document-model](message-group-chat-message-document-model.md)
- [errors-unified-error-hierarchy-for-cloud-module](errors-unified-error-hierarchy-for-cloud-module.md)
- [events-internal-async-event-bus-for-cross-domain-side-effects](events-internal-async-event-bus-for-cross-domain-side-effects.md)
- [workspaceservice-workspace-domain-business-logic](workspaceservice-workspace-domain-business-logic.md)
