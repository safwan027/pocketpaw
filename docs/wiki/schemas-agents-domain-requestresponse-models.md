# schemas — Agents domain request/response models

> Defines Pydantic request and response schemas for the agents domain. Provides validation and serialization for agent creation, updates, discovery, and API responses. Acts as the contract layer between API endpoints and internal services.

**Categories:** agents domain, API schemas, data validation, request/response models  
**Concepts:** CreateAgentRequest, UpdateAgentRequest, DiscoverRequest, AgentResponse, Pydantic validation, Request/response contract, Field constraints, Soul customization, OCEAN personality model, Agent configuration  
**Words:** 295 | **Version:** 1

---

## Purpose
This module centralizes all HTTP request/response models for the agents API, ensuring consistent validation, documentation, and type safety across agent management operations.

## Key Classes

### CreateAgentRequest
Schema for creating a new agent with comprehensive configuration options.
- **Basic fields**: name (1-100 chars), slug (1-50 chars), avatar, visibility (private|workspace|public)
- **Agent config**: backend (default: claude_agent_sdk), model, persona
- **Optional overrides**: temperature, max_tokens, tools, trust_level, system_prompt
- **Soul customization**: soul_enabled (default: True), soul_archetype, soul_values, soul_ocean (OCEAN personality mapping)

### UpdateAgentRequest
Schema for partial updates to existing agents. All fields are optional, allowing selective updates.
- Mirrors CreateAgentRequest structure with optional types
- Supports generic config dict for extensible updates
- Preserves soul customization fields for personality adjustments

### DiscoverRequest
Schema for agent discovery/search queries.
- **query**: search string (empty string allowed)
- **visibility**: optional filter by visibility level
- **pagination**: page (≥1), page_size (1-100, default 20)

### AgentResponse
Schema for agent API responses. Represents complete agent state.
- **Identity**: id, workspace, owner
- **Metadata**: name, slug, avatar, visibility, created_at, updated_at
- **Configuration**: config dict containing all agent settings

## Field Validations
- String lengths enforced with min/max constraints
- Visibility enum pattern: `^(private|workspace|public)$`
- Pagination bounds: page ≥1, page_size ∈ [1,100]
- Timestamps use datetime type for proper serialization
- Soul values and ocean metrics use typed collections

## Dependencies
- `pydantic.BaseModel`: Base validation model
- `pydantic.Field`: Field-level constraints and documentation
- `datetime.datetime`: Timestamp serialization

## Usage Examples

```python
# Creating an agent
req = CreateAgentRequest(
    name="Claude Helper",
    slug="claude-helper",
    model="claude-3-sonnet",
    visibility="workspace",
    soul_archetype="helpful_assistant"
)

# Updating an agent
update = UpdateAgentRequest(
    name="Updated Name",
    temperature=0.7,
    soul_values=["helpfulness", "honesty"]
)

# Discovering agents
discover = DiscoverRequest(
    query="coding",
    visibility="public",
    page=2,
    page_size=50
)
```

## Related Modules
Imported by: `router` (HTTP endpoints), `service` (business logic), `group_service`, `message_service`, `ws` (WebSocket), `agent_bridge`

---

## Related

- [router-workspace-domain-fastapi-endpoints](router-workspace-domain-fastapi-endpoints.md)
- [workspaceservice-workspace-domain-business-logic](workspaceservice-workspace-domain-business-logic.md)
- [groupservice-group-and-channel-business-logic-crud-membership-agents-dms](groupservice-group-and-channel-business-logic-crud-membership-agents-dms.md)
- [messageservice-message-business-logic-and-crud-operations](messageservice-message-business-logic-and-crud-operations.md)
- [ws-websocket-connection-manager-for-real-time-chat](ws-websocket-connection-manager-for-real-time-chat.md)
- [agentbridge-cloud-chat-event-bridge-to-pocketpaw-agent-pool](agentbridge-cloud-chat-event-bridge-to-pocketpaw-agent-pool.md)
