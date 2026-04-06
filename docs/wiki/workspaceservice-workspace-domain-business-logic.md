# WorkspaceService — Workspace domain business logic

> Core service module that implements workspace CRUD operations, member management, and invitation workflows. Provides stateless business logic for creating, retrieving, updating, and deleting workspaces, along with role-based member administration and token-based invite acceptance. Enforces permissions, seat limits, and workspace soft-deletion semantics.

**Categories:** workspace domain, business logic service, member management, access control, invitation workflow  
**Concepts:** WorkspaceService, Workspace CRUD, WorkspaceMembership, Member role management, Invite tokens, Seat limiting, Role-based authorization, Soft deletion, Domain events, Permission guards  
**Words:** 282 | **Version:** 1

---

## Purpose
Encapsulates all workspace domain business logic as a stateless service. Handles workspace lifecycle management, member role administration, and invite token workflows with built-in permission checks and seat limit validation.

## Key Classes/Functions

### WorkspaceService
Stateless service class providing:
- **Workspace CRUD**: `create()`, `get()`, `update()`, `delete()`, `list_for_user()`
- **Member Management**: `list_members()`, `update_member_role()`, `remove_member()`
- **Invite Operations**: `create_invite()`, `validate_invite()`, `accept_invite()`, `revoke_invite()`

All methods are async and require authenticated users with appropriate workspace roles.

### Helper Functions
- `_workspace_response(ws, member_count)`: Transforms Workspace model to frontend DTO
- `_invite_response(invite)`: Transforms Invite model to frontend DTO
- `_get_membership(user, workspace_id)`: Retrieves user's workspace membership or raises NotFound
- `_count_members(workspace_id)`: Counts workspace members via User collection

## Dependencies
- **Models**: Workspace, User, WorkspaceMembership, Invite, WorkspaceSettings
- **Errors**: ConflictError, Forbidden, NotFound, SeatLimitError
- **Permissions**: check_workspace_role() for role validation
- **Events**: event_bus for emitting domain events (member.removed, invite.accepted)
- **Database**: Beanie ODM with PydanticObjectId

## Key Patterns
- **Permission Guards**: Role checks on all mutation operations (minimum="admin", "owner")
- **Soft Deletion**: Workspaces use deleted_at timestamp, excluded from queries
- **Seat Limiting**: Member counts validated against workspace.seats quota
- **Invite Deduplication**: Prevents duplicate pending invites per email+group combination
- **Domain Events**: Async event emission for member removal and invite acceptance
- **Membership Validation**: _get_membership() ensures user belongs to workspace before operations

## Usage Examples

### Create Workspace
```python
request = CreateWorkspaceRequest(name="My Team", slug="my-team")
ws_dict = await WorkspaceService.create(user, request)
```

### List User's Workspaces
```python
workspaces = await WorkspaceService.list_for_user(user)
```

### Update Member Role (Admin Only)
```python
await WorkspaceService.update_member_role(
    workspace_id="507f1f77bcf86cd799439011",
    target_user_id="507f1f77bcf86cd799439012",
    role="member",
    user=admin_user
)
```

### Invite User
```python
request = CreateInviteRequest(email="user@example.com", role="member")
invite_dict = await WorkspaceService.create_invite(workspace_id, admin_user, request)
```

### Accept Invite (No Auth Required)
```python
await WorkspaceService.accept_invite(token, user)
```

---

## Related

- [schemas-workspace-domain-requestresponse-models](schemas-workspace-domain-requestresponse-models.md)
- [agent-agent-configuration-models-for-the-cloud-platform](agent-agent-configuration-models-for-the-cloud-platform.md)
- [errors-unified-error-hierarchy-for-cloud-module](errors-unified-error-hierarchy-for-cloud-module.md)
- [user-enterprise-user-and-oauth-account-models](user-enterprise-user-and-oauth-account-models.md)
- [groupservice-group-and-channel-business-logic-crud-membership-agents-dms](groupservice-group-and-channel-business-logic-crud-membership-agents-dms.md)
- [messageservice-message-business-logic-and-crud-operations](messageservice-message-business-logic-and-crud-operations.md)
- [pocket-pocket-workspace-and-widget-document-models](pocket-pocket-workspace-and-widget-document-models.md)
- [session-chat-session-document-model](session-chat-session-document-model.md)
- [ripplenormalizer-ai-generated-ripplespec-validation-and-normalization](ripplenormalizer-ai-generated-ripplespec-validation-and-normalization.md)
- [events-internal-async-event-bus-for-cross-domain-side-effects](events-internal-async-event-bus-for-cross-domain-side-effects.md)
- [message-group-chat-message-document-model](message-group-chat-message-document-model.md)
- [invite-workspace-membership-invitation-management](invite-workspace-membership-invitation-management.md)
- [workspace-workspace-document-model-for-deployments-and-organizations](workspace-workspace-document-model-for-deployments-and-organizations.md)
- [permissions-role-and-access-level-permission-checks](permissions-role-and-access-level-permission-checks.md)
- [router-workspace-domain-fastapi-endpoints](router-workspace-domain-fastapi-endpoints.md)
- [agentbridge-cloud-chat-event-bridge-to-pocketpaw-agent-pool](agentbridge-cloud-chat-event-bridge-to-pocketpaw-agent-pool.md)
