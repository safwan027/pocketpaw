# group_service — Group and channel business logic (CRUD, membership, agents, DMs)

> Provides stateless service layer for group/channel operations including creation, membership management, agent assignment, and direct message handling. Implements authorization checks (owner/member validation), batch-optimized data loading to prevent N+1 queries, and slug generation for group identifiers. Core component of the chat domain business logic.

**Categories:** chat domain, business logic, service layer, group management, CRUD operations, membership management, authorization, backend  
**Concepts:** GroupService, create_group, list_groups, get_group, update_group, archive_group, join_group, leave_group, add_members, remove_member  
**Words:** 627 | **Version:** 1

---

## Purpose

The `group_service` module encapsulates all group and channel business logic for the chat domain. It handles:
- **Group CRUD**: create, retrieve, update, archive
- **Membership**: join, leave, add/remove members with ownership constraints
- **Agent Management**: add, update, remove agents within groups
- **Direct Messages**: get or create DM groups between users

## Key Classes and Functions

### GroupService (Main Class)

Stateless service class providing static methods for group operations:

- **`create_group(workspace_id, user_id, body)`** — Creates a group with creator as owner and member. Special handling for DM type: validates exactly 1 target member, auto-names as "DM", sorts members.

- **`list_groups(workspace_id, user_id)`** — Returns public groups in workspace plus private/DM groups where user is a member.

- **`get_group(group_id, user_id)`** — Retrieves single group with membership check for private/DM types.

- **`update_group(group_id, user_id, body)`** — Updates name, slug, description, icon, color. Owner-only. Prevents DM updates.

- **`archive_group(group_id, user_id)`** — Sets archived flag. Owner-only.

- **`join_group(group_id, user_id)`** — Adds user to public group members. Validates group is public and not archived.

- **`leave_group(group_id, user_id)`** — Removes user from members. Prevents owner from leaving without transferring ownership.

- **`add_members(group_id, user_id, member_ids)`** — Bulk add members. Owner-only. Idempotent.

- **`remove_member(group_id, user_id, target_user_id)`** — Removes specific member. Owner-only. Prevents owner removal.

- **`add_agent(group_id, user_id, body)`** — Adds agent with role and respond_mode. Owner-only. Prevents duplicates.

- **`update_agent(group_id, user_id, agent_id, body)`** — Updates agent's respond_mode. Owner-only.

- **`remove_agent(group_id, user_id, agent_id)`** — Removes agent from group. Owner-only.

- **`get_or_create_dm(workspace_id, user_id, target_user_id)`** — Finds existing DM or creates new one with sorted members.

### Helper Functions

- **`_generate_slug(name)`** — Converts group name to URL-safe slug: lowercase, replaces spaces/underscores with hyphens, strips non-alphanumeric, collapses multiple hyphens.

- **`_group_response(group)`** — Converts Group document to frontend-compatible dict. **Key optimization**: batch-loads members (User) and agents (AgentModel) to avoid N+1 queries. Populates member details (name, email, avatar) and agent details (name, slug, role, respond_mode).

- **`_require_group_member(group, user_id)`** — Validates user membership. Raises Forbidden if not member.

- **`_require_group_admin(group, user_id)`** — Validates user ownership. Raises Forbidden if not owner (note: groups have single owner, no per-member roles).

- **`_get_group_or_404(group_id)`** — Loads group by ID or raises NotFound.

## Design Patterns

- **Stateless Service**: All methods are static, no instance state
- **Authorization Guards**: Consistent use of `_require_group_member()` and `_require_group_admin()` for access control
- **Batch Loading Optimization**: `_group_response()` uses single batch queries instead of per-member/per-agent queries
- **Domain Objects**: Works with Beanie ODM models (Group, GroupAgent, User, Agent)
- **Custom Exceptions**: Uses domain-specific error classes (Forbidden, NotFound, ValidationError) with error codes and messages

## Dependencies

- `ee.cloud.chat.schemas`: Request DTOs (CreateGroupRequest, UpdateGroupRequest, AddGroupAgentRequest, UpdateGroupAgentRequest)
- `ee.cloud.models.group`: Group and GroupAgent domain models
- `ee.cloud.models.agent`: Agent domain model
- `ee.cloud.models.user`: User domain model
- `ee.cloud.shared.errors`: Error classes (Forbidden, NotFound, ValidationError)
- `beanie`: PydanticObjectId for MongoDB ObjectId handling
- `re`: Regex for slug generation

## Usage Examples

```python
# Create a public group
group_dict = await GroupService.create_group(
    workspace_id="workspace_123",
    user_id="user_456",
    body=CreateGroupRequest(
        type="public",
        name="Engineering Team",
        description="Chat for engineers",
        member_ids=["user_789"]
    )
)

# List user's visible groups
groups = await GroupService.list_groups(
    workspace_id="workspace_123",
    user_id="user_456"
)

# Add agent to group
await GroupService.add_agent(
    group_id="group_123",
    user_id="user_456",  # must be owner
    body=AddGroupAgentRequest(
        agent_id="agent_789",
        role="assistant",
        respond_mode="always"
    )
)

# Get or create DM
dm_group = await GroupService.get_or_create_dm(
    workspace_id="workspace_123",
    user_id="user_456",
    target_user_id="user_789"
)
```

## Key Authorization Rules

- **Owner-only operations**: update_group, archive_group, add/remove members, add/update/remove agents
- **Member-only operations**: get_group (for private/DM), leave_group
- **Public join**: join_group (any user for public groups)
- **Owner constraints**: Cannot leave group or be removed without transfer; cannot update DMs

## Data Model Notes

- Groups belong to workspaces
- Members stored as list of user_ids
- Single owner (no hierarchical roles)
- Agents stored as list of GroupAgent objects (contains agent_id, role, respond_mode)
- DM type has special constraints: exactly 2 sorted members, auto-named "DM", not updatable

---

## Related

- [schemas-workspace-domain-requestresponse-models](schemas-workspace-domain-requestresponse-models.md)
- [group-multi-user-chat-channels-with-ai-agent-participants](group-multi-user-chat-channels-with-ai-agent-participants.md)
- [errors-unified-error-hierarchy-for-cloud-module](errors-unified-error-hierarchy-for-cloud-module.md)
- [agent-agent-configuration-models-for-the-cloud-platform](agent-agent-configuration-models-for-the-cloud-platform.md)
- [user-enterprise-user-and-oauth-account-models](user-enterprise-user-and-oauth-account-models.md)
- [messageservice-message-business-logic-and-crud-operations](messageservice-message-business-logic-and-crud-operations.md)
- [workspaceservice-workspace-domain-business-logic](workspaceservice-workspace-domain-business-logic.md)
