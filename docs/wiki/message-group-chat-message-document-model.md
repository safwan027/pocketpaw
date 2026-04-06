# message — Group chat message document model

> Defines the data model for chat messages in group conversations, including support for mentions, reactions, attachments, and message threading. Messages can be sent by users or agents, support editing/deletion, and are indexed by group and creation time for efficient querying.

**Categories:** data-models, messaging, group-chat, cloud-infrastructure  
**Concepts:** Message, Mention, Attachment, Reaction, TimestampedDocument, Group chat, Message threading, Soft delete, Beanie ODM, Indexed fields  
**Words:** 356 | **Version:** 1

---

## Purpose
Provides a complete message document schema for storing and managing group chat messages in a MongoDB-backed system using Beanie ODM. Supports rich messaging features including mentions, reactions, attachments, and threaded conversations.

## Key Classes

### Message
The primary document class representing a chat message.
- **Fields:**
  - `group` (Indexed[str]): Group identifier for efficient querying
  - `sender` (str | None): User ID of message author, null for system messages
  - `sender_type` (str): Type of sender - "user" or "agent"
  - `agent` (str | None): Agent ID when sender_type is "agent"
  - `content` (str): Message text body
  - `mentions` (list[Mention]): @mentions of users/agents/everyone
  - `reply_to` (str | None): Parent message ID for threading support
  - `attachments` (list[Attachment]): Files, images, or widgets
  - `reactions` (list[Reaction]): Emoji reactions with user lists
  - `edited` (bool): Flag indicating message was modified
  - `edited_at` (datetime | None): Timestamp of last edit
  - `deleted` (bool): Soft delete flag
- **Indexes:** Composite index on (group, createdAt) for efficient group message retrieval
- **Parent:** Extends `TimestampedDocument` for automatic timestamp tracking

### Mention
Represents an @mention within a message.
- `type` (str): "user", "agent", or "everyone"
- `id` (str): User or Agent ID
- `display_name` (str): Display text like "@rohit"

### Attachment
Represents attached files or media.
- `type` (str): "file", "image", "pocket", or "widget"
- `url` (str): Resource URL
- `name` (str): Display name
- `meta` (dict): Additional metadata

### Reaction
Represents emoji reactions on messages.
- `emoji` (str): Emoji character
- `users` (list[str]): IDs of users who reacted

## Dependencies
- `beanie`: MongoDB ODM for document indexing
- `pydantic`: Data validation and serialization
- `ee.cloud.models.base`: Base model with timestamp functionality

## Usage Examples
```python
# Create a user message
message = Message(
    group="group_123",
    sender="user_456",
    content="Hey team!",
    mentions=[Mention(type="everyone", display_name="@everyone")]
)

# Create a threaded reply
reply = Message(
    group="group_123",
    sender="user_789",
    content="Thanks!",
    reply_to="original_message_id"
)

# Add attachment
message_with_file = Message(
    group="group_123",
    sender="user_456",
    content="Check this out",
    attachments=[Attachment(type="image", url="https://...", name="screenshot.png")]
)

# Add reaction
reaction = Reaction(emoji="👍", users=["user_1", "user_2"])
```

## Database Queries
The composite index enables efficient queries:
```python
# Get recent messages in a group
messages = await Message.find(
    {"group": "group_123"},
    sort=[("createdAt", -1)]
).to_list()
```

---

## Related

- [base-timestamped-document-base-class](base-timestamped-document-base-class.md)
- [messageservice-message-business-logic-and-crud-operations](messageservice-message-business-logic-and-crud-operations.md)
- [router-workspace-domain-fastapi-endpoints](router-workspace-domain-fastapi-endpoints.md)
- [eecloudworkspace-workspace-module-initialization](eecloudworkspace-workspace-module-initialization.md)
- [workspaceservice-workspace-domain-business-logic](workspaceservice-workspace-domain-business-logic.md)
- [agentbridge-cloud-chat-event-bridge-to-pocketpaw-agent-pool](agentbridge-cloud-chat-event-bridge-to-pocketpaw-agent-pool.md)
