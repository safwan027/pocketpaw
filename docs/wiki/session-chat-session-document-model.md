# session — Chat session document model

> Defines the Session document model for tracking pocket-scoped chat sessions in the cloud layer. Sessions store metadata about conversations including ownership, context (pocket/group/agent), and activity timestamps, with messages managed separately in Python. Uses Beanie ODM for MongoDB persistence with indexed queries optimized for workspace and organizational filtering.

**Categories:** cloud-models, document-models, data-persistence, mongodb, chat-domain  
**Concepts:** Session, TimestampedDocument, Indexed fields, Compound indexes, Beanie ODM, Pydantic aliases, soft deletion, multi-tenant isolation, camelCase/snake_case mapping, pocket-scoped contexts  
**Words:** 386 | **Version:** 1

---

## Purpose
Provides a MongoDB document model for chat sessions via Beanie ODM, enabling cloud-side tracking of conversation metadata while keeping message content in Python memory. Sessions are scoped to pockets and linked to workspaces, owners, and optional organizational contexts (groups/agents).

## Key Classes

### Session
Extends `TimestampedDocument` to represent a chat session with the following characteristics:
- **Identification**: Unique `sessionId` (indexed) and workspace reference
- **Scope**: Optional pocket, group, and agent associations
- **Metadata**: Owner, title ('New Chat' default), message count, last activity timestamp
- **Soft Deletion**: `deleted_at` field for logical deletion
- **Frontend Contract**: Uses camelCase aliases (`sessionId`, `lastActivity`, `messageCount`) to match frontend expectations via Pydantic's `populate_by_name` config

## Field Specifications

| Field | Type | Key Features |
|-------|------|---------------|
| `sessionId` | str | Unique, indexed for fast lookups |
| `workspace` | str | Indexed, required for multi-tenant isolation |
| `owner` | str | Required, identifies session creator |
| `pocket` | str \| None | Optional scope qualifier |
| `group` | str \| None | Optional organizational context |
| `agent` | str \| None | Optional agent context |
| `title` | str | User-friendly name |
| `lastActivity` | datetime | UTC-based, auto-set to current time |
| `messageCount` | int | Tracks conversation size |
| `deleted_at` | datetime \| None | Soft-delete marker |

## Indexing Strategy

Two compound indexes optimize common queries:
1. `(workspace, pocket, lastActivity)` — Retrieve sessions by workspace/pocket sorted by recency
2. `(workspace, group, agent)` — Retrieve sessions by organizational context

## Dependencies
- **beanie**: MongoDB async ODM for document persistence and indexing
- **pydantic**: Data validation and serialization with alias support
- **ee.cloud.models.base**: `TimestampedDocument` base class providing `created_at`/`updated_at`

## Usage Examples

```python
from ee.cloud.models.session import Session
from datetime import datetime, UTC

# Create a new session
session = Session(
    sessionId="sess_abc123",
    workspace="ws_default",
    owner="user_john",
    pocket="pocket_1",
    title="Project Discussion"
)
await session.create()

# Query sessions by workspace and pocket (uses first index)
sessions = await Session.find(
    Session.workspace == "ws_default",
    Session.pocket == "pocket_1"
).sort([("lastActivity", -1)]).to_list()

# Update activity on message addition
session.lastActivity = datetime.now(UTC)
session.messageCount += 1
await session.save()

# Soft delete
session.deleted_at = datetime.now(UTC)
await session.save()
```

## Inheritance Chain
`Session` → `TimestampedDocument` → Beanie `Document`

## Configuration
- **Collection Name**: "sessions"
- **Name Population**: Accepts both camelCase (frontend) and snake_case (Python) field names

---

## Related

- [base-timestamped-document-base-class](base-timestamped-document-base-class.md)
- [eecloudworkspace-workspace-module-initialization](eecloudworkspace-workspace-module-initialization.md)
- [workspaceservice-workspace-domain-business-logic](workspaceservice-workspace-domain-business-logic.md)
