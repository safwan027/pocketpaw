# router — Knowledge Base FastAPI Endpoints

> Provides workspace-scoped REST API endpoints for knowledge base operations including search, ingestion, linting, and browsing. Integrates with the KnowledgeEngine and PocketPawCompilerBackend to enable wiki pocket templates and KB-aware UI components.

**Categories:** knowledge-base, fastapi-router, workspace-api, ee-cloud  
**Concepts:** KnowledgeEngine, PocketPawCompilerBackend, workspace scoping, multi-tenant isolation, search, ingest_text, ingest_url, lint, article retrieval, concept tagging  
**Words:** 408 | **Version:** 1

---

## Purpose

This module exposes a FastAPI router (`/kb` prefix) that implements the complete knowledge base API surface for workspace-scoped operations. It serves as the primary interface between frontend KB consumers (wiki pocket templates, UI components) and the underlying knowledge engine infrastructure.

## Key Functions

### Core Engine Builder
- **`_engine(workspace_id, scope_override)`** — Factory function that constructs a KnowledgeEngine instance with PocketPawCompilerBackend, supporting scope overrides for multi-tenant KB isolation.

### Search Operations
- **`search_kb(body, workspace_id, user_id)`** — Full-text search across KB articles, returning metadata and snippets (truncated content, not full articles) with configurable scope and result limits.

### Ingestion Operations
- **`ingest_text(body, workspace_id, user_id)`** — Ingest plain text content into the workspace KB with source attribution.
- **`ingest_url(body, workspace_id, user_id)`** — Fetch and ingest web content from URLs, automatically handling retrieval and processing.

### Maintenance & Health
- **`lint_kb(body, workspace_id, user_id)`** — Run LLM-powered health checks on the knowledge base, returning structured issue reports.

### Browse & Retrieve
- **`get_article(article_id, workspace_id, user_id)`** — Fetch a complete article by ID including full content.
- **`get_concept_articles(name, workspace_id, user_id)`** — Retrieve all articles tagged with a specific concept.

### Metadata & Bulk Retrieval
- **`kb_stats(workspace_id, user_id)`** — Get KB statistics (article counts, concept coverage, etc.).
- **`list_articles(workspace_id, user_id)`** — List all articles in the workspace (metadata only, no content).
- **`list_concepts(workspace_id, user_id)`** — List all concepts with their article associations.

## Dependencies

**Internal modules:**
- `ee.cloud.kb.schemas` — Request/response models (SearchRequest, IngestTextRequest, IngestUrlRequest, LintRequest)
- `ee.cloud.kb.backend_adapter` — PocketPawCompilerBackend adapter for knowledge engine
- `ee.cloud.license` — License enforcement via `require_license` dependency
- `ee.cloud.shared.deps` — Dependency injection (current_user_id, current_workspace_id)
- `ee.cloud.shared.errors` — CloudError, NotFound exception types

**External packages:**
- `knowledge_base` — Standalone KnowledgeEngine (migrated from pocketpaw.knowledge as of 2026-04-06)
- `fastapi` — APIRouter, Depends

## Architecture Patterns

**License Enforcement:** All endpoints require valid license via `require_license` dependency.

**Workspace Isolation:** All operations scoped to `workspace:{workspace_id}` or override scope, enabling multi-tenant KB separation.

**Error Handling:** Ingest operations wrap exceptions in CloudError(500, "kb.ingest_failed") with logging.

**Response Consistency:** Operations return dicts with results/metadata keys and total counts for pagination awareness.

## Usage Example

```python
# Search the knowledge base
POST /kb/search
{"query": "authentication", "limit": 10, "scope": null}

# Ingest text content
POST /kb/ingest/text
{"text": "OAuth 2.0 is...", "source": "team-wiki", "scope": null}

# Retrieve full article
GET /kb/article/{article_id}

# List all concepts
GET /kb/concepts

# Run KB health checks
POST /kb/lint
{"scope": null}
```

## Version History

**Updated 2026-04-06:** Migrated from `pocketpaw.knowledge` to standalone `knowledge_base` package with PocketPawCompilerBackend adapter.

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
