# backend_adapter — LLM backend adapter for knowledge base compilation

> Provides a bridge between PocketPaw's agent registry and the knowledge_base compiler, enabling KB compilation to use any active LLM backend (Claude, OpenAI, etc.). Implements the CompilerBackend protocol by wrapping PocketPaw's backend infrastructure and streaming responses.

**Categories:** backend integration, knowledge base compilation, LLM adapters, agent infrastructure  
**Concepts:** PocketPawCompilerBackend, async/await pattern, protocol adapter, event streaming, backend registry, configuration override, resource cleanup, chunk aggregation  
**Words:** 279 | **Version:** 1

---

## Purpose
The `backend_adapter` module adapts PocketPaw's pluggable agent backends to satisfy the `knowledge_base.compiler.CompilerBackend` protocol. This decouples the standalone knowledge-base package from PocketPaw's specific agent implementations while allowing KB compilation to dynamically use whichever backend is configured.

## Key Classes

### PocketPawCompilerBackend
Async-compatible adapter that implements the CompilerBackend protocol.

**Constructor:**
- `__init__(backend_name: str = "", model: str = "")` — Optionally override the backend and model; defaults to settings if not provided

**Methods:**
- `async complete(prompt: str, system_prompt: str = "") -> str` — Sends a prompt to the active backend, streams message chunks, and returns the concatenated full response. Falls back to a knowledge-compiler system prompt if none provided.

## Architecture & Design

- **Protocol Implementation:** Conforms to `knowledge_base.compiler.CompilerBackend` async interface
- **Dynamic Backend Resolution:** Queries `pocketpaw.agents.registry.get_backend_class()` at runtime
- **Configuration Integration:** Loads settings from `pocketpaw.config.Settings` and allows per-request model override
- **Streaming Aggregation:** Iterates over async agent events, filters for `message` type, and concatenates chunks
- **Resource Management:** Ensures agent cleanup via try/finally with `agent.stop()`
- **Model Switching:** Supports runtime model selection for Claude SDK and OpenAI backends

## Dependencies
- `pocketpaw.agents.registry` — Backend factory and resolution
- `pocketpaw.config.Settings` — Configuration management
- Python 3.7+ (`from __future__ import annotations`)

## Usage Examples

```python
# Use default backend from settings
backend = PocketPawCompilerBackend()
response = await backend.complete(
    prompt="Compile these docs into JSON schema",
    system_prompt="Output valid JSON only"
)

# Override backend and model
backend = PocketPawCompilerBackend(
    backend_name="openai",
    model="gpt-4-turbo"
)
response = await backend.complete(prompt="...")  # Uses gpt-4-turbo
```

## Integration Points
- **Imported by:** `knowledge`, `router` modules
- **Used in:** KB compiler pipeline for LLM-based schema/metadata generation
- **Logging:** Warns if requested backend is unavailable; returns empty string fallback

---

## Related

- [knowledge-agent-scoped-knowledge-base-service](knowledge-agent-scoped-knowledge-base-service.md)
- [router-workspace-domain-fastapi-endpoints](router-workspace-domain-fastapi-endpoints.md)
