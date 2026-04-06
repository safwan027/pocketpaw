# workspace — Workspace document model for deployments and organizations

> Defines the data model for organization workspaces in enterprise deployments. Each workspace represents a single deployment/org and contains configuration settings, ownership details, plan information, and seat management. Serves as a core document type in the cloud models layer.

**Categories:** data models, enterprise features, cloud platform, organizational management  
**Concepts:** TimestampedDocument, BaseModel, Indexed, workspace configuration, multi-tenancy, soft-delete pattern, unique slug constraint, license tiers, data retention policy, Beanie ODM  
**Words:** 200 | **Version:** 1

---

## Purpose
Provides Pydantic/Beanie models for workspace entities, enabling persistent storage and validation of workspace configurations across enterprise deployments.

## Key Classes

### WorkspaceSettings
Configuration options for a workspace:
- `default_agent` (str | None): Default agent ID for the workspace
- `allow_invites` (bool): Controls whether user invitations are enabled (default: True)
- `retention_days` (int | None): Data retention policy; None means indefinite retention

### Workspace
Core workspace document extending TimestampedDocument:
- `name` (str): Human-readable workspace name
- `slug` (str, unique indexed): URL-friendly identifier for the workspace
- `owner` (str): User ID of the administrator who created the workspace
- `plan` (str): License tier—"team", "business", or "enterprise" (default: "team")
- `seats` (int): Number of user seats allocated (default: 5)
- `settings` (WorkspaceSettings): Nested workspace configuration object
- `deleted_at` (datetime | None): Soft-delete timestamp; None indicates active workspace
- Inherits `created_at` and `updated_at` from TimestampedDocument
- Beanie collection name: "workspaces"

## Dependencies
- `beanie`: ODM for MongoDB document indexing
- `pydantic`: Data validation and BaseModel
- `ee.cloud.models.base`: TimestampedDocument base class
- `datetime`: Timestamp support

## Usage Context
Imported by router (API endpoints), service (business logic), and package __init__. Used throughout the enterprise cloud platform for workspace lifecycle management, multi-tenancy, and plan enforcement.

---

## Related

- [base-timestamped-document-base-class](base-timestamped-document-base-class.md)
- [eecloudworkspace-workspace-module-initialization](eecloudworkspace-workspace-module-initialization.md)
- [router-workspace-domain-fastapi-endpoints](router-workspace-domain-fastapi-endpoints.md)
- [workspaceservice-workspace-domain-business-logic](workspaceservice-workspace-domain-business-logic.md)
