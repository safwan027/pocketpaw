# schemas — Pockets domain request/response schemas

> This module defines Pydantic models for request and response validation in the Pockets domain. It standardizes data contracts between the frontend and backend for pocket management operations, including creation, updates, widget management, sharing, and collaboration. The schema definitions support a flexible pocket specification system where agents, ripple configurations, and widgets can be initialized at creation time.

**Categories:** domain-schemas, pockets-domain, request-validation, api-contracts  
**Concepts:** CreatePocketRequest, UpdatePocketRequest, AddWidgetRequest, UpdateWidgetRequest, ReorderWidgetsRequest, ShareLinkRequest, AddCollaboratorRequest, PocketResponse, Pydantic validation, Field aliases  
**Words:** 354 | **Version:** 1

---

## Purpose

Provides typed request/response schemas for the Pockets domain using Pydantic BaseModel. Enables validation and serialization of data exchanged between client and server for pocket lifecycle operations.

## Key Classes

### Request Models

**CreatePocketRequest**
- Creates a new pocket with initial configuration
- Fields: name, description, type, icon, color, visibility (private/workspace/public)
- Supports agents (agent IDs), ripple_spec (configuration), and widgets (initial definitions)
- Uses aliases for camelCase (sessionId → session_id, rippleSpec → ripple_spec)

**UpdatePocketRequest**
- Partially updates existing pocket properties
- All fields are optional for selective updates
- Supports ripple_spec modifications via alias

**AddWidgetRequest**
- Adds a new widget to a pocket
- Fields: name, type, icon, color, span (CSS grid), data_source_type, config, props, assigned_agent
- Defaults provided for most optional fields

**UpdateWidgetRequest**
- Updates widget properties and data
- All fields optional; supports config, props, and assigned_agent modifications
- Generic data field accepts Any type

**ReorderWidgetsRequest**
- Reorders widgets via ordered list of widget IDs

**ShareLinkRequest**
- Creates share links with access levels (view/comment/edit)

**AddCollaboratorRequest**
- Adds collaborators with specified access levels
- Requires user_id and optional access level

### Response Model

**PocketResponse**
- Complete pocket representation returned from server
- Includes metadata: id, workspace, owner, created_at, updated_at
- Contains relationships: team, agents, widgets, shared_with
- Includes sharing state: share_link_token, share_link_access
- Supports optional ripple_spec for advanced configuration

## Design Patterns

- **Alias support**: Uses Pydantic aliases to accept camelCase from frontend while maintaining snake_case internally
- **populate_by_name**: Allows both snake_case and camelCase in requests
- **Field constraints**: Validates name length (1-100), visibility/access patterns via regex
- **Factory defaults**: Uses Field(default_factory=list/dict) for mutable defaults
- **Optional fields**: Supports partial updates via optional typing (Type | None)

## Dependencies

- pydantic: BaseModel, Field for validation and serialization
- datetime: For created_at/updated_at timestamps
- typing: For type hints (Any, list, dict unions)

## Usage Examples

```python
# Creating a pocket with full spec
request = CreatePocketRequest(
    name="My Pocket",
    description="Test pocket",
    visibility="workspace",
    agents=["agent-1", "agent-2"],
    rippleSpec={"enabled": True},
    widgets=[{"name": "Widget1", "type": "chart"}]
)

# Updating specific fields
update = UpdatePocketRequest(
    name="Updated Name",
    visibility="public"
)

# Adding widget
widget = AddWidgetRequest(
    name="Dashboard",
    type="dashboard",
    data_source_type="api",
    assigned_agent="agent-1"
)
```

---

## Related

- [router-workspace-domain-fastapi-endpoints](router-workspace-domain-fastapi-endpoints.md)
- [workspaceservice-workspace-domain-business-logic](workspaceservice-workspace-domain-business-logic.md)
- [groupservice-group-and-channel-business-logic-crud-membership-agents-dms](groupservice-group-and-channel-business-logic-crud-membership-agents-dms.md)
- [messageservice-message-business-logic-and-crud-operations](messageservice-message-business-logic-and-crud-operations.md)
- [ws-websocket-connection-manager-for-real-time-chat](ws-websocket-connection-manager-for-real-time-chat.md)
- [agentbridge-cloud-chat-event-bridge-to-pocketpaw-agent-pool](agentbridge-cloud-chat-event-bridge-to-pocketpaw-agent-pool.md)
