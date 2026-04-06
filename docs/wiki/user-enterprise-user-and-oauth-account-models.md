# user — Enterprise user and OAuth account models

> Defines the core user domain model for the PocketPaw system, integrating fastapi-users and Beanie for MongoDB-backed authentication and authorization. Provides user profiles with OAuth support, workspace memberships, and presence tracking for enterprise collaboration.

**Categories:** authentication, user management, data models, multi-tenancy  
**Concepts:** OAuthAccount, WorkspaceMembership, User, BeanieBaseUser, BaseOAuthAccount, Document, multi-workspace membership, OAuth integration, user presence tracking, enterprise user model  
**Words:** 325 | **Version:** 1

---

## Purpose

This module establishes the data models for user authentication, authorization, and workspace membership within the PocketPaw enterprise platform. It extends fastapi-users' authentication framework with custom fields for multi-workspace support, user presence, and OAuth provider integration.

## Key Classes

### OAuthAccount
- **Purpose**: Represents linked OAuth credentials (Google, GitHub, etc.)
- **Inheritance**: Extends `BaseOAuthAccount` from fastapi-users
- **Role**: Enables passwordless and multi-provider authentication

### WorkspaceMembership
- **Purpose**: Models a user's association with a workspace and their role within it
- **Fields**:
  - `workspace`: Workspace identifier (string)
  - `role`: Permission level (owner, admin, member, viewer) - defaults to "member"
  - `joined_at`: Timestamp of workspace membership (auto-set to current UTC time)
- **Pattern**: Embedded document for many-to-many workspace relationships

### User
- **Purpose**: Core user entity with enterprise features
- **Inheritance**: Combines `BeanieBaseUser` (from fastapi-users-db-beanie) and Beanie's `Document` for MongoDB persistence
- **Fields**:
  - `full_name`: Display name (string, optional)
  - `avatar`: Profile image URL (string, optional)
  - `active_workspace`: Currently selected workspace ID (nullable)
  - `workspaces`: List of `WorkspaceMembership` objects (multi-workspace support)
  - `status`: Presence indicator (online, offline, away, dnd) with validation
  - `last_seen`: Timestamp of last activity (auto-set to current UTC time)
  - `oauth_accounts`: List of linked OAuth providers
- **Database**: Stored in "users" collection with case-insensitive email handling disabled

## Dependencies

- **fastapi-users**: Authentication framework (`BeanieBaseUser`, `BaseOAuthAccount`)
- **beanie**: MongoDB ODM for Python (`Document`)
- **pydantic**: Data validation (`BaseModel`, `Field`)
- **Python stdlib**: `datetime` module for timestamps with UTC timezone

## Usage Examples

```python
# Creating a user with workspace membership
user = User(
    email="alice@company.com",
    full_name="Alice Johnson",
    avatar="https://example.com/alice.jpg",
    active_workspace="workspace_001",
    workspaces=[
        WorkspaceMembership(
            workspace="workspace_001",
            role="admin"
        ),
        WorkspaceMembership(
            workspace="workspace_002",
            role="member"
        )
    ],
    status="online"
)

# Linking OAuth account
user.oauth_accounts.append(
    OAuthAccount(provider="google", account_id="...")
)
```

## Architecture Notes

- **Multi-tenancy**: `active_workspace` and `workspaces` list enable users across multiple workspaces
- **Presence Tracking**: Status and `last_seen` fields support real-time collaboration features
- **Extensible Auth**: OAuth integration allows integration with external identity providers
- **Document-oriented**: MongoDB as backend enables flexible schema evolution

---

## Related

- [eecloudworkspace-workspace-module-initialization](eecloudworkspace-workspace-module-initialization.md)
- [core-enterprise-authentication-with-fastapi-users-jwt-and-multi-transport](core-enterprise-authentication-with-fastapi-users-jwt-and-multi-transport.md)
- [router-workspace-domain-fastapi-endpoints](router-workspace-domain-fastapi-endpoints.md)
- [workspaceservice-workspace-domain-business-logic](workspaceservice-workspace-domain-business-logic.md)
- [groupservice-group-and-channel-business-logic-crud-membership-agents-dms](groupservice-group-and-channel-business-logic-crud-membership-agents-dms.md)
- [deps-fastapi-dependency-injection-for-cloud-authentication-and-authorization](deps-fastapi-dependency-injection-for-cloud-authentication-and-authorization.md)
