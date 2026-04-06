# comment — Threaded comments on pockets and widgets

> Defines data models for managing threaded comments in the Pocketpaw system. Enables users to leave comments on pockets and widgets with support for comment threads, mentions, and resolution tracking. Integrates with the Beanie ODM for MongoDB persistence.

**Categories:** data models, collaboration features, comments and feedback, document persistence  
**Concepts:** CommentTarget, CommentAuthor, Comment, TimestampedDocument, Beanie ODM, Indexed fields, Threading/hierarchical comments, User mentions, Comment resolution, MongoDB indexing  
**Words:** 308 | **Version:** 1

---

## Purpose
Provides Pydantic and Beanie models for storing and querying threaded comments attached to pockets and widgets. Supports comment hierarchies through parent comment references, user mentions, and comment resolution workflow.

## Key Classes

### CommentTarget
- **Purpose**: Identifies what entity a comment is attached to
- **Fields**:
  - `type` (str): One of "pocket", "widget", or "agent"
  - `pocket_id` (str): Reference to the parent pocket
  - `widget_id` (str | None): Optional reference to a widget within the pocket

### CommentAuthor
- **Purpose**: Represents the user who created a comment
- **Fields**:
  - `id` (str): Unique user identifier
  - `name` (str): Display name of the author
  - `avatar` (str): URL or path to user avatar image

### Comment
- **Purpose**: Main document model for threaded comments (extends TimestampedDocument)
- **Fields**:
  - `workspace` (Indexed[str]): Workspace scope for the comment
  - `target` (CommentTarget): What this comment is attached to
  - `thread` (str | None): Parent comment ID for reply threading
  - `author` (CommentAuthor): Who wrote the comment
  - `body` (str): Comment text content
  - `mentions` (list[str]): List of mentioned user IDs
  - `resolved` (bool): Whether comment has been resolved
  - `resolved_by` (str | None): ID of user who resolved the comment
- **Indexes**: Compound index on (target.pocket_id, created_at) for efficient queries
- **Collection**: Stored in "comments" MongoDB collection

## Dependencies
- `beanie`: ODM library for MongoDB, provides Indexed field and document persistence
- `pydantic`: Data validation and serialization (BaseModel, Field)
- `ee.cloud.models.base`: TimestampedDocument base class with created_at/updated_at

## Usage Examples

```python
# Create a comment on a pocket
comment = Comment(
    workspace="workspace_123",
    target=CommentTarget(
        type="pocket",
        pocket_id="pocket_456",
        widget_id=None
    ),
    author=CommentAuthor(
        id="user_789",
        name="John Doe",
        avatar="https://example.com/avatar.jpg"
    ),
    body="Great idea! This could improve workflow.",
    mentions=["user_101"],
    resolved=False
)

# Create a reply to a comment (thread)
reply = Comment(
    workspace="workspace_123",
    target=comment.target,
    thread=comment.id,  # Reference to parent comment
    author=CommentAuthor(
        id="user_202",
        name="Jane Smith"
    ),
    body="@user_101 agreed!",
    mentions=["user_101"]
)
```

---

## Related

- [base-timestamped-document-base-class](base-timestamped-document-base-class.md)
- [eecloudworkspace-workspace-module-initialization](eecloudworkspace-workspace-module-initialization.md)
