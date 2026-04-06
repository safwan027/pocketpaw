# knowledge — Agent-scoped knowledge base service

> Thin wrapper over the standalone knowledge_base package that provides agent-scoped knowledge operations. Delegates all knowledge management (ingestion, search, clearing) to KnowledgeEngine instances configured with PocketPawCompilerBackend for LLM-powered compilation and retrieval.

**Categories:** knowledge management, agent services, information retrieval, cloud backend  
**Concepts:** KnowledgeService, agent-scoped operations, multi-tenant isolation, ingest_text, ingest_url, ingest_file, search, search_context, semantic search, prompt injection context  
**Words:** 260 | **Version:** 1

---

## Purpose

Provides a stateless service layer for knowledge management operations bound to individual agents. Abstracts the standalone `knowledge_base` package behind a simple async API, handling ingestion from multiple sources (text, URLs, files) and semantic search with LLM-powered context compilation.

## Key Classes

### KnowledgeService
Static-method-based service class providing agent-scoped knowledge operations:

- **Ingestion**: `ingest_text()`, `ingest_url()`, `ingest_file()` — accepts knowledge from various sources, returns article metadata
- **Retrieval**: `search()` — semantic search returning summaries/snippets; `search_context()` — formatted context for prompt injection
- **Maintenance**: `clear()` — wipe agent's knowledge base; `stats()` — retrieve storage metrics; `lint()` — validate knowledge integrity
- **Internal**: `_engine()` — factory method creating scoped KnowledgeEngine instances

## Architecture

**Scoping Pattern**: Each operation receives `agent_id` and creates a new `KnowledgeEngine(scope=f"agent:{agent_id}")` — supports multi-tenant isolation without persistent state.

**Backend**: Uses `PocketPawCompilerBackend` from `ee.cloud.kb.backend_adapter` to enable LLM-powered knowledge compilation and semantic ranking.

**Error Handling**: URL and file ingestion catch exceptions and return error dictionaries; text ingestion and search assume success.

## Dependencies

- `knowledge_base.KnowledgeEngine` — standalone knowledge engine (switched from pocketpaw.knowledge in Apr 2026)
- `ee.cloud.kb.backend_adapter.PocketPawCompilerBackend` — LLM backend for compilation
- Standard library: `logging`

## Usage Examples

```python
# Ingest knowledge
await KnowledgeService.ingest_text(
    agent_id="agent-123",
    text="Python is a programming language...",
    source="training_doc"
)

# Search with context for prompt injection
context = await KnowledgeService.search_context(
    agent_id="agent-123",
    query="Python best practices",
    limit=3
)

# Get knowledge statistics
stats = KnowledgeService.stats(agent_id="agent-123")

# Clear agent's knowledge
await KnowledgeService.clear(agent_id="agent-123")
```

## Integration Points

- **Imported by**: `router` (HTTP endpoints), `agent_bridge` (agent orchestration)
- **Depends on**: `backend_adapter` (LLM compilation)
- **Updated**: 2026-04-06 — migrated to standalone `knowledge_base` package

---

## Related

- [backendadapter-llm-backend-adapter-for-knowledge-base-compilation](backendadapter-llm-backend-adapter-for-knowledge-base-compilation.md)
- [router-workspace-domain-fastapi-endpoints](router-workspace-domain-fastapi-endpoints.md)
- [agentbridge-cloud-chat-event-bridge-to-pocketpaw-agent-pool](agentbridge-cloud-chat-event-bridge-to-pocketpaw-agent-pool.md)
