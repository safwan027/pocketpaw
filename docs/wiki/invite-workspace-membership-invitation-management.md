# invite — Workspace membership invitation management

> This module defines the Invite document model for managing workspace membership invitations. It handles invitation creation, expiration tracking, and role assignment for users invited to join workspaces via email tokens.

**Categories:** Access Control, Workspace Management, Data Models, Cloud Infrastructure  
**Concepts:** Invite (document model), workspace (indexed field), email (indexed field), token (unique indexed field), role (validation pattern), expiration management, timezone-aware datetime, _default_expiry (factory function), expired (computed property), Beanie Document  
**Words:** 259 | **Version:** 1

---

## Purpose
Provides a MongoDB document model (via Beanie ODM) for storing and managing workspace invitations. Invitations are time-limited tokens sent to email addresses, allowing users to accept membership in a workspace with a specified role.

## Key Classes

### Invite(Document)
A Beanie ODM document representing a workspace invitation.

**Fields:**
- `workspace` (Indexed[str]): Target workspace identifier
- `email` (Indexed[str]): Recipient email address
- `role` (str): User role upon acceptance — must be one of `admin`, `member`, or `viewer` (default: `member`)
- `invited_by` (str): User ID of the inviter
- `token` (Indexed[str], unique): Unique invitation token for acceptance
- `group` (str | None): Optional group ID for auto-adding user to a group on acceptance
- `accepted` (bool): Whether the invitation has been accepted (default: False)
- `revoked` (bool): Whether the invitation has been revoked (default: False)
- `expires_at` (datetime): Expiration timestamp (default: 7 days from creation)

**Properties:**
- `expired`: Read-only boolean indicating whether the invitation has expired, with timezone-aware comparison

**MongoDB Collection:** `invites`

## Key Functions

### _default_expiry() → datetime
Factory function providing default expiration timestamp (current UTC time + 7 days). Used as the default factory for `expires_at` field.

## Dependencies
- `beanie`: ODM for MongoDB document management (Document, Indexed)
- `pydantic`: Data validation and field constraints (Field)
- `datetime`: Timezone-aware datetime handling (UTC, datetime, timedelta)

## Usage Examples

```python
# Create an invitation
invite = Invite(
    workspace="ws_123",
    email="user@example.com",
    role="member",
    invited_by="admin_user_id",
    token="unique_invite_token_xyz"
)

# Check if invitation has expired
if invite.expired:
    print("Invitation has expired")

# Check invitation status
if invite.accepted:
    print("User already accepted")
elif invite.revoked:
    print("Invitation was revoked")
```

---

## Related

- [eecloudworkspace-workspace-module-initialization](eecloudworkspace-workspace-module-initialization.md)
- [workspaceservice-workspace-domain-business-logic](workspaceservice-workspace-domain-business-logic.md)
