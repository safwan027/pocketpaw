# AgentService — Agent domain business logic

> Stateless service module encapsulating agent CRUD operations and discovery logic. Handles agent creation with slug uniqueness validation, retrieval by ID or slug, updates with owner authorization checks, deletion, and paginated discovery with visibility-based filtering across workspaces.

**Categories:** domain service, business logic, agent management, CRUD operations  
**Concepts:** AgentService, create, list_agents, get, get_by_slug, update, delete, discover, _agent_response, Agent model  
**Words:** 383 | **Version:** 1

---

## Purpose
Provides the core business logic layer for agent management in the pocketPaw system. Acts as a mediator between HTTP routes and the Agent data model, enforcing validation rules, ownership constraints, and visibility policies.

## Key Classes/Functions

### AgentService
Stateless async service class with static methods for agent operations:

- **create(workspace_id, user_id, body)** — Creates a new agent with slug uniqueness validation within workspace. Constructs AgentConfig from request parameters, supporting optional fields like temperature, max_tokens, tools, and soul-specific settings.

- **list_agents(workspace_id, query)** — Lists all agents in a workspace with optional case-insensitive name search via regex.

- **get(agent_id)** — Retrieves single agent by MongoDB ObjectId, raises NotFound if missing.

- **get_by_slug(workspace_id, slug)** — Looks up agent by slug within a specific workspace.

- **update(agent_id, user_id, body)** — Updates agent metadata (name, avatar, visibility) and config fields. Enforces owner-only access. Handles both bulk config replacement and granular field updates.

- **delete(agent_id, user_id)** — Hard-deletes agent document. Requires owner authorization.

- **discover(workspace_id, user_id, body)** — Paginated discovery endpoint with visibility filtering: private (user's own agents), workspace (all in workspace), public (cross-workspace), or default (combination of all three). Supports name search and pagination via page/page_size.

### _agent_response(agent)
Helper function that transforms Agent MongoDB documents into frontend-compatible dictionaries, mapping internal fields to API schema (e.g., `_id` as string, `uname` for slug, ISO timestamps).

## Dependencies
- **schemas**: CreateAgentRequest, DiscoverRequest, UpdateAgentRequest
- **agent**: Agent model, AgentConfig
- **errors**: ConflictError, Forbidden, NotFound exceptions
- **beanie**: PydanticObjectId for MongoDB operations

## Usage Examples

```python
# Create agent
agent_dict = await AgentService.create(
    workspace_id="ws123",
    user_id="user456",
    body=CreateAgentRequest(
        name="Assistant Bot",
        slug="assistant-bot",
        avatar="url",
        backend="openai",
        model="gpt-4",
        system_prompt="You are helpful...",
        soul_enabled=True
    )
)

# Discover agents with visibility filtering
agents = await AgentService.discover(
    workspace_id="ws123",
    user_id="user456",
    body=DiscoverRequest(visibility="workspace", query="bot", page=1, page_size=10)
)

# Update agent config
updated = await AgentService.update(
    agent_id="agent789",
    user_id="user456",
    body=UpdateAgentRequest(name="New Name", temperature=0.7)
)
```

## Key Patterns
- **Owner authorization**: Checks `agent.owner == user_id` before mutations
- **Slug uniqueness**: Database-level lookup prevents duplicates within workspace scope
- **Flexible config updates**: Supports both full config replacement and selective field updates
- **Visibility filtering**: MongoDB `$or` operators for multi-criteria discovery
- **Response normalization**: Consistent dict transformation for all return values

## Database Model Notes
Operates on `Agent` documents with fields: workspace, name, slug, avatar, visibility, config (AgentConfig), owner, createdAt, updatedAt. Uses Beanie ODM for async MongoDB operations.

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
