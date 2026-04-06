# schemas — Knowledge Base Request/Response Models

> Defines Pydantic request/response schemas for the knowledge base REST API. Provides validated data models for search, text ingestion, URL ingestion, and linting operations with built-in field constraints and optional scope overrides.

**Categories:** knowledge-base, api-schemas, data-validation, rest-api  
**Concepts:** SearchRequest, IngestTextRequest, IngestUrlRequest, LintRequest, Pydantic BaseModel, Field validation, Request schema, Scope override, Input constraints, Pydantic  
**Words:** 197 | **Version:** 1

---

## Purpose
Provides strongly-typed request schemas for the knowledge base domain, ensuring API input validation and consistent data handling across the REST endpoints and internal services.

## Key Classes/Functions

### SearchRequest
- **query** (str): Search query string, minimum length 1
- **scope** (str | None): Optional workspace scope override
- **limit** (int): Result limit, default 10, range 1-100

### IngestTextRequest
- **text** (str): Text content to ingest, minimum length 1
- **source** (str): Content source identifier, defaults to "manual"
- **scope** (str | None): Optional workspace scope override

### IngestUrlRequest
- **url** (str): URL to ingest, minimum length 1
- **scope** (str | None): Optional workspace scope override

### LintRequest
- **scope** (str | None): Optional workspace scope override

## Dependencies
- **pydantic**: BaseModel and Field for schema validation and constraints

## Usage Examples
```python
# Search knowledge base
search = SearchRequest(query="authentication flow", limit=20)

# Ingest text content
ingest_text = IngestTextRequest(text="Important documentation", source="docs")

# Ingest from URL
ingest_url = IngestUrlRequest(url="https://example.com/page")

# Lint knowledge base
lint = LintRequest(scope="custom_workspace")
```

## Design Patterns
- **Pydantic BaseModel**: Runtime validation with type hints
- **Field Constraints**: min_length, default values, range validation (ge/le)
- **Optional Scope**: Allows workspace-level override for multi-tenant operations

---

## Related

- [router-workspace-domain-fastapi-endpoints](router-workspace-domain-fastapi-endpoints.md)
- [workspaceservice-workspace-domain-business-logic](workspaceservice-workspace-domain-business-logic.md)
- [groupservice-group-and-channel-business-logic-crud-membership-agents-dms](groupservice-group-and-channel-business-logic-crud-membership-agents-dms.md)
- [messageservice-message-business-logic-and-crud-operations](messageservice-message-business-logic-and-crud-operations.md)
- [ws-websocket-connection-manager-for-real-time-chat](ws-websocket-connection-manager-for-real-time-chat.md)
- [agentbridge-cloud-chat-event-bridge-to-pocketpaw-agent-pool](agentbridge-cloud-chat-event-bridge-to-pocketpaw-agent-pool.md)
