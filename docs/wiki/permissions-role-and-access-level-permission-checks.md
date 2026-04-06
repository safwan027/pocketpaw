# permissions — Role and access-level permission checks

> Provides enum hierarchies for workspace roles and pocket access levels with corresponding privilege levels. Includes guard functions that validate user permissions and raise `Forbidden` exceptions when access is insufficient. Central to authorization in the cloud module.

**Categories:** authorization, access control, cloud infrastructure, permissions system  
**Concepts:** WorkspaceRole, PocketAccess, check_workspace_role, check_pocket_access, Enum hierarchy, privilege levels, permission guards, Forbidden exception, role-based access control, from_str factory pattern  
**Words:** 266 | **Version:** 1

---

## Purpose
This module implements a hierarchical permission system for the cloud workspace and pocket management features. It defines role and access levels as ordered enums and provides validation functions that enforce minimum privilege requirements.

## Key Classes

### WorkspaceRole
Enumeration of workspace membership roles ordered by privilege:
- `MEMBER` (level 1): Basic workspace member
- `ADMIN` (level 2): Administrative privileges
- `OWNER` (level 3): Full ownership control

Each role has a string value and numeric level for comparison. Includes `from_str(role)` class method to resolve string identifiers to enum members.

### PocketAccess
Enumeration of per-pocket access levels ordered by privilege:
- `VIEW` (level 1): Read-only access
- `COMMENT` (level 2): View and comment
- `EDIT` (level 3): View, comment, and edit content
- `OWNER` (level 4): Full pocket ownership

Each access level has a string value and numeric level. Includes `from_str(access)` class method for string resolution.

## Key Functions

### check_workspace_role(role, *, minimum)
Validates that a user's workspace role meets the minimum required level. Raises `Forbidden` with error code `"workspace.insufficient_role"` if the check fails.

### check_pocket_access(access, *, minimum)
Validates that a user's pocket access level meets the minimum required level. Raises `Forbidden` with error code `"pocket.insufficient_access"` if the check fails.

## Dependencies
- `enum.Enum`: Standard library enum support
- `ee.cloud.shared.errors.Forbidden`: Custom exception for permission denials

## Design Patterns
- **Enum with metadata**: Enums store both string identifiers and numeric privilege levels
- **Guard functions**: Functions that validate preconditions and raise exceptions on failure
- **Hierarchical privileges**: Numeric levels enable comparison and ordering of permissions
- **String resolution**: Factory methods (`from_str`) map configuration strings to enum members

---

## Related

- [errors-unified-error-hierarchy-for-cloud-module](errors-unified-error-hierarchy-for-cloud-module.md)
- [deps-fastapi-dependency-injection-for-cloud-authentication-and-authorization](deps-fastapi-dependency-injection-for-cloud-authentication-and-authorization.md)
- [workspaceservice-workspace-domain-business-logic](workspaceservice-workspace-domain-business-logic.md)
