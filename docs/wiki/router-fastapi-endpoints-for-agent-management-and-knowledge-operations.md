# router — FastAPI endpoints for agent management and knowledge operations

> This module defines the FastAPI router for the Agents domain, exposing REST API endpoints for CRUD operations on agents, backend discovery, agent discovery, and knowledge base management (ingestion, search, and clearing). It serves as the HTTP interface layer for agent-related functionality in the PocketPaw cloud platform.

**Categories:** API Router, Agents Domain, Cloud Services, Knowledge Management, FastAPI Endpoints  
**Concepts:** list_available_backends, create_agent, list_agents, get_agent, get_by_slug, update_agent, delete_agent, discover_agents, ingest_text, ingest_url  
**Words:** 375 | **Version:** 1

---

## Purpose
Provide a complete FastAPI router implementation for agent lifecycle management and knowledge base operations, with built-in license requirement checks and workspace/user isolation.

## Key Endpoints

### Backend Discovery
- `GET /agents/backends` — List available agent backends with display names and availability status

### Agent CRUD Operations
- `POST /agents` — Create a new agent
- `GET /agents` — List all agents in a workspace with optional search query
- `GET /agents/{agent_id}` — Retrieve a specific agent by ID
- `GET /agents/uname/{slug}` — Retrieve an agent by slug within workspace
- `PATCH /agents/{agent_id}` — Update agent configuration
- `DELETE /agents/{agent_id}` — Delete an agent (returns 204)

### Agent Discovery
- `POST /agents/discover` — Discover available agents based on discovery request criteria

### Knowledge Base Management
- `POST /agents/{agent_id}/knowledge/text` — Ingest plain text into knowledge base
- `POST /agents/{agent_id}/knowledge/url` — Fetch and ingest a single URL
- `POST /agents/{agent_id}/knowledge/urls` — Batch ingest multiple URLs
- `GET /agents/{agent_id}/knowledge/search` — Search knowledge base with query and limit parameters
- `POST /agents/{agent_id}/knowledge/upload` — Upload and ingest files (.pdf, .txt, .md, .csv, .json, .docx, .png, .jpg, .jpeg, .webp)
- `DELETE /agents/{agent_id}/knowledge` — Clear all knowledge for an agent (returns 204)

## Dependencies
- **Service Layer**: `AgentService`, `KnowledgeService` — Business logic delegation
- **Authentication**: `current_user_id`, `current_workspace_id` — User and workspace context injection
- **Authorization**: `require_license` — Enterprise license validation
- **Data Models**: Request/response schemas from `schemas` module
- **Framework**: FastAPI, Starlette

## Router Configuration
- **Prefix**: `/agents`
- **Tags**: `["Agents"]`
- **Global Dependencies**: License requirement check applied to all endpoints

## Design Patterns
- **Dependency Injection**: Heavy use of FastAPI `Depends()` for authentication, workspace isolation, and license checks
- **Async/Await**: All endpoints are async coroutines
- **Service Delegation**: Router delegates business logic to service layer
- **Error Handling**: Try-except blocks for knowledge operations with logging
- **File Handling**: Temporary file creation with automatic cleanup for uploaded documents
- **Status Codes**: Proper HTTP status codes (204 for deletions, implicit 200 for success)

## Usage Examples

```python
# List agent backends
GET /agents/backends

# Create an agent
POST /agents
{"name": "My Agent", "backend": "openai", ...}

# Ingest text
POST /agents/agent-123/knowledge/text
{"text": "Knowledge content", "source": "manual"}

# Upload and ingest file
POST /agents/agent-123/knowledge/upload
Content-Type: multipart/form-data
file: <binary>

# Search knowledge
GET /agents/agent-123/knowledge/search?q=query&limit=10
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
