# AuthService — Auth domain business logic

> Stateless service that encapsulates authentication and user profile management business logic. Provides methods to retrieve user profiles, update profile information, and manage active workspace selection. Acts as the core domain service layer for auth-related operations in the cloud authentication domain.

**Categories:** authentication, user management, business logic, domain service, cloud platform  
**Concepts:** AuthService, get_profile, update_profile, set_active_workspace, ProfileUpdateRequest, User model, stateless service pattern, async/await, profile response transformation, workspace management  
**Words:** 289 | **Version:** 1

---

## Purpose
The AuthService module implements the business logic layer for authentication and user profile management. It operates as a stateless service that handles profile retrieval, updates, and workspace management without maintaining any service state.

## Key Classes and Functions

### AuthService
Stateless service class providing three core async methods:

- **get_profile(user: User) -> dict**
  - Retrieves the current user's complete profile information
  - Returns a dictionary containing user ID, email, name, avatar, verification status, active workspace, and list of associated workspaces with roles
  - Transforms the User object into a API-ready response format

- **update_profile(user: User, body: ProfileUpdateRequest) -> dict**
  - Updates mutable user profile fields (full_name, avatar, status)
  - Only updates fields that are explicitly provided (non-None values)
  - Persists changes to database via user.save()
  - Returns the updated profile by calling get_profile()

- **set_active_workspace(user: User, workspace_id: str) -> None**
  - Sets the user's currently active workspace
  - Validates that workspace_id is provided, raises HTTPException(400) if empty
  - Persists the change to database

## Dependencies
- **User model**: User object representing authenticated user entity
- **ProfileUpdateRequest schema**: Defines structure for profile update requests
- **FastAPI**: HTTPException for error handling
- Related services: group_service, message_service (imported but not directly used in this module)
- Session and workspace modules for context

## Usage Examples

```python
# Get user profile
profile = await AuthService.get_profile(current_user)

# Update user profile
update_body = ProfileUpdateRequest(full_name="John Doe", avatar="url")
updated = await AuthService.update_profile(current_user, update_body)

# Switch active workspace
await AuthService.set_active_workspace(current_user, workspace_id="abc123")
```

## Architecture Notes
- All methods are static, enforcing stateless design
- Methods are async-compatible for integration with async request handlers
- Profile response includes workspace associations with user roles for authorization context
- Validation is minimal at service layer (HTTPException in set_active_workspace only)

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
