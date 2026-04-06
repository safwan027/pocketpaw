# router — Workspace domain FastAPI endpoints

> Provides REST API endpoints for workspace management in the PocketPaw cloud application. Handles workspace CRUD operations, member management, and workspace invite workflows. All endpoints require authentication and an active license.

**Categories:** workspace management, multi-tenant infrastructure, user access control  
**Concepts:** FastAPI Router, dependency injection (Depends), async endpoints, license validation, authentication/authorization, workspace lifecycle, member role management, invite token-based onboarding, RESTful API patterns, FastAPI  
**Words:** 245 | **Version:** 1

---

## Purpose
This module implements the FastAPI router for the workspace domain, exposing HTTP endpoints for creating, reading, updating, and deleting workspaces, managing workspace members, and handling workspace invitations.

## Key Functions

### Workspace CRUD
- `create_workspace(body, user)` - POST `/workspaces` - Create a new workspace
- `list_workspaces(user)` - GET `/workspaces` - List all workspaces for current user
- `get_workspace(workspace_id, user)` - GET `/workspaces/{workspace_id}` - Retrieve workspace details
- `update_workspace(workspace_id, body, user)` - PATCH `/workspaces/{workspace_id}` - Update workspace properties
- `delete_workspace(workspace_id, user)` - DELETE `/workspaces/{workspace_id}` - Delete a workspace

### Member Management
- `list_members(workspace_id, user)` - GET `/workspaces/{workspace_id}/members` - List workspace members
- `update_member_role(workspace_id, user_id, body, user)` - PATCH `/workspaces/{workspace_id}/members/{user_id}` - Change member role
- `remove_member(workspace_id, user_id, user)` - DELETE `/workspaces/{workspace_id}/members/{user_id}` - Remove member from workspace

### Invite Management
- `create_invite(workspace_id, body, user)` - POST `/workspaces/{workspace_id}/invites` - Generate workspace invite
- `validate_invite(token)` - GET `/workspaces/invites/{token}` - Validate invite token
- `accept_invite(token, user)` - POST `/workspaces/invites/{token}/accept` - Accept workspace invitation
- `revoke_invite(workspace_id, invite_id, user)` - DELETE `/workspaces/{workspace_id}/invites/{invite_id}` - Revoke invite

## Dependencies
- FastAPI router and dependency injection
- `WorkspaceService` - business logic layer
- `current_user` - authentication dependency
- `require_license` - license validation decorator
- Request/response schemas: `CreateWorkspaceRequest`, `UpdateWorkspaceRequest`, `CreateInviteRequest`, `UpdateMemberRoleRequest`

## Usage Examples

All endpoints are prefixed with `/workspaces` and require an active license and authenticated user. Examples:

```
POST /workspaces
GET /workspaces
GET /workspaces/{workspace_id}
PATCH /workspaces/{workspace_id}
DELETE /workspaces/{workspace_id}
GET /workspaces/{workspace_id}/members
PATCH /workspaces/{workspace_id}/members/{user_id}
DELETE /workspaces/{workspace_id}/members/{user_id}
POST /workspaces/{workspace_id}/invites
GET /workspaces/invites/{token}
POST /workspaces/invites/{token}/accept
DELETE /workspaces/{workspace_id}/invites/{invite_id}
```

---

## Related

- [schemas-workspace-domain-requestresponse-models](schemas-workspace-domain-requestresponse-models.md)
- [workspaceservice-workspace-domain-business-logic](workspaceservice-workspace-domain-business-logic.md)
- [license-enterprise-license-validation-for-cloud-features](license-enterprise-license-validation-for-cloud-features.md)
- [deps-fastapi-dependency-injection-for-cloud-authentication-and-authorization](deps-fastapi-dependency-injection-for-cloud-authentication-and-authorization.md)
- [knowledge-agent-scoped-knowledge-base-service](knowledge-agent-scoped-knowledge-base-service.md)
- [core-enterprise-authentication-with-fastapi-users-jwt-and-multi-transport](core-enterprise-authentication-with-fastapi-users-jwt-and-multi-transport.md)
- [user-enterprise-user-and-oauth-account-models](user-enterprise-user-and-oauth-account-models.md)
- [ws-websocket-connection-manager-for-real-time-chat](ws-websocket-connection-manager-for-real-time-chat.md)
- [group-multi-user-chat-channels-with-ai-agent-participants](group-multi-user-chat-channels-with-ai-agent-participants.md)
- [message-group-chat-message-document-model](message-group-chat-message-document-model.md)
- [errors-unified-error-hierarchy-for-cloud-module](errors-unified-error-hierarchy-for-cloud-module.md)
- [backendadapter-llm-backend-adapter-for-knowledge-base-compilation](backendadapter-llm-backend-adapter-for-knowledge-base-compilation.md)
- [workspace-workspace-document-model-for-deployments-and-organizations](workspace-workspace-document-model-for-deployments-and-organizations.md)
- [eecloudworkspace-workspace-module-initialization](eecloudworkspace-workspace-module-initialization.md)
