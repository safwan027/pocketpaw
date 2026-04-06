# agent_bridge — Bridge between cloud chat events and the PocketPaw agent pool

> Orchestrates agent responses in group chats by listening to message events, evaluating each agent's respond mode (silent, auto, mention_only, smart), and streaming AI-generated replies back through WebSocket. It also parses ripple specs from agent output, delegates pocket creation to PocketService, and persists agent messages to MongoDB.

**Categories:** agent orchestration, real-time chat, event-driven architecture, cloud infrastructure  
**Concepts:** on_message_for_agents, _should_agent_respond, _smart_relevance_check, _run_agent_response, register_agent_bridge, respond_mode (silent, auto, mention_only, smart), event-driven orchestration, WebSocket streaming (stream_start, stream_chunk, stream_end), ripple spec extraction, agent pool pattern  
**Words:** 607 | **Version:** 1

---

## Purpose

`agent_bridge` is a focused orchestrator that connects the cloud chat system's real-time message events to PocketPaw's agent pool. When a user sends a message in a group that contains agents, this module determines which agents should respond, runs them concurrently, streams their output token-by-token over WebSocket, and handles any structured artifacts (ripple specs) embedded in the response.

## Key Functions

### `on_message_for_agents(data: dict) -> None`
The primary event handler, subscribed to `message.sent` on the event bus. It loads the group, iterates over its agents, checks each agent's respond mode, and spawns concurrent `_run_agent_response` tasks for those that should reply. Guards against infinite loops by ignoring messages from other agents.

### `_should_agent_respond(group_agent, content, mentions) -> bool`
Evaluates the agent's `respond_mode` setting:
- **silent** — never responds
- **auto** — always responds
- **mention_only** — responds only when explicitly @-mentioned
- **smart** — delegates to `_smart_relevance_check` for LLM-based triage

### `_smart_relevance_check(agent_id, content) -> bool`
Performs a lightweight LLM call (Claude Haiku) to determine if a message is relevant to the agent's persona. Constructs a yes/no prompt using the agent's `soul_persona` or `system_prompt`, runs it through the `claude_agent_sdk` backend, and parses the binary answer. Falls back to `False` on any failure.

### `_run_agent_response(agent_id, group_id, workspace_id, user_message, group_members) -> None`
The core response pipeline:
1. **History retrieval** — Fetches the last 20 messages from MongoDB for conversational context
2. **Knowledge injection** — Queries `KnowledgeService.search_context` for RAG-style context augmentation
3. **Stream start** — Broadcasts `agent.stream_start` WebSocket event
4. **Token streaming** — Iterates over the agent pool's async generator, broadcasting `agent.stream_chunk` events with the accumulated text
5. **Ripple spec extraction** — Regex-parses JSON code blocks for objects containing `lifecycle` or `widgets` keys, normalizes them via `normalize_ripple_spec`
6. **Pocket creation** — Delegates to `PocketService.create_from_ripple_spec()` if a ripple spec is found
7. **Persistence** — Inserts the final `Message` document (with optional ripple attachment) into MongoDB
8. **Stream end** — Broadcasts `agent.stream_end` with the final content, ripple spec, and pocket ID
9. **Soul observation** — Calls `pool.observe()` for the agent's memory/learning loop

### `register_agent_bridge() -> None`
Wires up the module by subscribing `on_message_for_agents` to the `message.sent` event on the shared event bus. Called during application startup.

## Dependencies

| Dependency | Role |
|---|---|
| `ee.cloud.chat.schemas.WsOutbound` | WebSocket outbound message envelope |
| `ee.cloud.chat.ws.manager` | WebSocket broadcast to group members |
| `ee.cloud.shared.events.event_bus` | Pub/sub event bus for `message.sent` |
| `ee.cloud.models.group.Group` | Beanie ODM model for chat groups |
| `ee.cloud.models.agent.Agent` | Beanie ODM model for agent config |
| `ee.cloud.models.message.Message` | Beanie ODM model for persisted messages |
| `ee.cloud.agents.knowledge.KnowledgeService` | RAG knowledge retrieval |
| `ee.cloud.ripple_normalizer` | Normalizes raw ripple spec JSON |
| `ee.cloud.pockets.service.PocketService` | Creates pockets from ripple specs |
| `pocketpaw.agents.pool` | Agent instance pool (get, run, observe) |
| `pocketpaw.agents.registry` | Backend class lookup for LLM calls |
| `pocketpaw.config.Settings` | Runtime settings for agent backends |

## Architecture Notes

- **Lazy imports**: Heavy dependencies (`beanie`, model classes, `pocketpaw`) are imported inside functions to avoid circular imports and reduce startup cost.
- **Concurrency model**: Each agent response runs as an independent `asyncio.create_task`, allowing multiple agents in the same group to respond in parallel.
- **Loop prevention**: Messages with `sender_type == "agent"` are immediately discarded to prevent recursive agent-to-agent conversations.
- **Decoupled pocket creation**: Pocket creation was refactored out of this module into `PocketService.create_from_ripple_spec()` to reduce coupling with the pockets domain.

## Usage Examples

```python
# At application startup
from ee.cloud.shared.agent_bridge import register_agent_bridge
register_agent_bridge()

# The event bus then automatically routes message.sent events:
await event_bus.emit("message.sent", {
    "group_id": "abc123",
    "sender_id": "user456",
    "sender_type": "user",
    "content": "Hey @agent, build me a dashboard",
    "mentions": [{"type": "agent", "id": "agent789"}],
    "workspace_id": "ws001",
})
```