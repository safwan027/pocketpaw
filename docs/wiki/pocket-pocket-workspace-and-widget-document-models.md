# pocket — Pocket workspace and widget document models

> Defines MongoDB document models for Pocket workspaces and embedded Widget subdocuments. Pockets are collaborative workspaces containing configurable widgets, team members, agents, and ripple specifications. Integrates with Beanie ODM and provides camelCase field aliases for frontend compatibility.

**Categories:** data models, MongoDB schemas, workspace management, document database  
**Concepts:** Pocket, Widget, WidgetPosition, TimestampedDocument, Beanie ODM, embedded subdocuments, field aliases, camelCase serialization, ObjectId, indexed fields  
**Words:** 412 | **Version:** 1

---

## Purpose
This module provides Pydantic/Beanie models for representing Pocket workspaces and their contained widgets in the OCEAN platform. It establishes the data schema for collaborative workspace containers with rich metadata, permissions, and widget configurations.

## Key Classes

### WidgetPosition
Simple positional model for widget grid placement.
- `row` (int): Grid row coordinate (default: 0)
- `col` (int): Grid column coordinate (default: 0)

### Widget
Embedded subdocument model for individual widgets within a Pocket.
- **Purpose**: Self-contained widget configuration with unique ID addressing
- **Key Fields**:
  - `id` / `_id`: Unique identifier for frontend addressing (auto-generated ObjectId)
  - `name`: Display name
  - `type`: Widget type (default: "custom")
  - `icon`, `color`: Visual styling
  - `span`: CSS grid class (e.g., "col-span-1")
  - `dataSourceType`: Data binding type (default: "static")
  - `config`: Arbitrary configuration dictionary
  - `props`: Component properties dictionary
  - `data`: Widget data payload
  - `assignedAgent`: Optional agent reference
  - `position`: WidgetPosition subdocument
- **Features**: camelCase field aliases via `populate_by_name` config

### Pocket
Main timestamped document model for workspace containers.
- **Extends**: TimestampedDocument (provides created_at, updated_at)
- **Key Fields**:
  - `workspace`: Indexed string reference to parent workspace
  - `name`, `description`: Metadata
  - `type`: Pocket type (e.g., "custom", "deep-work")
  - `icon`, `color`: Visual styling
  - `owner`: Owner user ID
  - `team`: List of team member IDs or populated user objects
  - `agents`: List of assigned agent IDs or populated objects
  - `widgets`: List of embedded Widget subdocuments
  - `rippleSpec`: Optional ripple effect configuration
  - `visibility`: Access level (private|workspace|public, pattern-validated)
  - `share_link_token`: Optional share token for public access
  - `share_link_access`: Permission level (view|comment|edit, pattern-validated)
  - `shared_with`: List of user IDs with explicit access grants
- **Collection Name**: "pockets"
- **Features**: camelCase alias support, indexed workspace field for queries

## Dependencies
- **beanie**: MongoDB ODM integration (Indexed)
- **bson**: ObjectId generation
- **pydantic**: BaseModel and Field validation
- **ee.cloud.models.base**: TimestampedDocument base class

## Usage Pattern
```python
# Creating a pocket with widgets
from pocket import Pocket, Widget, WidgetPosition

widget = Widget(
    name="Chart",
    type="chart",
    config={"chartType": "line"},
    position=WidgetPosition(row=0, col=1)
)

pocket = Pocket(
    workspace="workspace_id",
    name="Analysis Dashboard",
    owner="user_id",
    visibility="workspace",
    widgets=[widget]
)
```

## Key Design Patterns
- **Embedded Documents**: Widgets are nested within Pocket, enabling atomic updates
- **Field Aliasing**: camelCase convention for frontend API/serialization
- **Auto-ID Generation**: Widgets get ObjectId-based identifiers for granular frontend addressing
- **Flexible References**: team/agents fields accept both IDs and populated objects (denormalization flexibility)
- **Pattern Validation**: visibility and share_link_access use regex patterns for constraint enforcement
- **Indexed Queries**: workspace field indexed for efficient Pocket lookups

---

## Related

- [base-timestamped-document-base-class](base-timestamped-document-base-class.md)
- [eecloudworkspace-workspace-module-initialization](eecloudworkspace-workspace-module-initialization.md)
- [workspaceservice-workspace-domain-business-logic](workspaceservice-workspace-domain-business-logic.md)
- [eventhandlers-cross-domain-event-processing-and-notifications](eventhandlers-cross-domain-event-processing-and-notifications.md)
