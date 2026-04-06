# agent_bridge — Cloud chat event bridge to PocketPaw agent pool

> Orchestrates the bridge between cloud chat events and the PocketPaw agent pool, determining when agents should respond to messages based on their respond modes (silent, auto, mention_only, smart). Streams agent responses back to chat groups via WebSocket, handles ripple spec parsing for UI generation, and delegates pocket creation to PocketService.

**Categories:** cloud-agents, event-orchestration, real-time-communication, agent-framework  
**Concepts:** on_message_for_agents, _should_agent_respond, _smart_relevance_check, _run_agent_response, register_agent_bridge, respond_mode, ripple_spec, session_key, knowledge_context, event-driven orchestration  
**Words:** 492 | **Version:** 1

---

## Purpose
The agent_bridge module acts as a focused orchestrator that connects real-time chat events in the cloud platform to intelligent agent responses. When a message is sent to a group, it evaluates each agent's configuration to decide if they should respond, executes the agent with conversation context and knowledge, streams the response in real-time, and handles downstream artifacts like pocket creation.

## Key Functions

### on_message_for_agents(data: dict)
Main event handler that listens to `message.sent` events. Loads the group, checks if it has agents configured, and conditionally spawns response tasks for qualifying agents.

### _should_agent_respond(group_agent, content, mentions)
Determines whether an agent should respond based on its respond_mode:
- **silent**: Never respond
- **auto**: Always respond
- **mention_only**: Respond only if explicitly mentioned
- **smart**: Use LLM to evaluate relevance (cheap Haiku model)

### _smart_relevance_check(agent_id, content)
Performs a lightweight Claude Haiku LLM inference to determine if a message is contextually relevant to an agent's persona. Falls back gracefully on errors.

### _run_agent_response(agent_id, group_id, workspace_id, user_message, group_members)
Core execution function that:
1. Fetches recent conversation history (20 messages) from MongoDB
2. Injects knowledge context from the agent's knowledge engine
3. Broadcasts `agent.stream_start` notification
4. Streams response chunks via WebSocket (`agent.stream_chunk`)
5. Parses ripple specs from JSON blocks in response
6. Delegates pocket creation to PocketService
7. Persists agent message with attachments
8. Broadcasts final `agent.stream_end` message
9. Observes response with agent soul for learning

### register_agent_bridge()
Registers the event handler with the event bus on module initialization.

## Architecture Patterns

**Event-Driven**: Subscribes to `message.sent` events via centralized event_bus

**Async Task Spawning**: Uses `asyncio.create_task()` to handle agent responses non-blocking

**Real-Time Streaming**: WebSocket broadcasts enable progressive message revelation

**Ripple Spec Parsing**: Extracts JSON UI specifications from agent markdown responses using regex

**Service Delegation**: Pocket creation delegated to PocketService to reduce coupling

**Context Injection**: Combines conversation history + knowledge context before agent execution

**Loop Prevention**: Ignores messages from agents themselves to prevent infinite cycles

## Dependencies

- **Beanie/MongoDB**: Group, Agent, Message, Attachment models
- **PocketPaw**: Agent pool, backend registry (Claude Haiku SDK)
- **WebSocket Manager**: Real-time broadcast to group members
- **Event Bus**: Pub/sub event handling
- **KnowledgeService**: Context injection for agent responses
- **PocketService**: Ripple spec-to-pocket creation
- **Ripple Normalizer**: Validates and normalizes UI specifications

## Key Concepts

- **Respond Mode**: Configuration determining when an agent participates (silent/auto/mention_only/smart)
- **Ripple Spec**: JSON UI widget specification embedded in agent responses
- **Session Key**: Unique identifier for agent conversation state: `cloud:{group_id}:{agent_id}`
- **Knowledge Context**: Retrieved relevant information injected into agent prompt
- **Streaming**: Progressive message delivery for responsive UX
- **Soul Observation**: Learning mechanism for agent adaptation

## Usage Example

```python
from ee.cloud.shared.agent_bridge import register_agent_bridge

# On module initialization
register_agent_bridge()

# When message.sent event fires:
# 1. Event data contains group_id, sender_id, content, mentions
# 2. on_message_for_agents() checks each agent's respond_mode
# 3. Matching agents spawn async _run_agent_response() tasks
# 4. WebSocket clients receive streaming updates in real-time
# 5. Final message with pocket_id and ripple_spec persisted
```

---

## Related

- [schemas-workspace-domain-requestresponse-models](schemas-workspace-domain-requestresponse-models.md)
- [ws-websocket-connection-manager-for-real-time-chat](ws-websocket-connection-manager-for-real-time-chat.md)
- [events-internal-async-event-bus-for-cross-domain-side-effects](events-internal-async-event-bus-for-cross-domain-side-effects.md)
- [group-multi-user-chat-channels-with-ai-agent-participants](group-multi-user-chat-channels-with-ai-agent-participants.md)
- [agent-agent-configuration-models-for-the-cloud-platform](agent-agent-configuration-models-for-the-cloud-platform.md)
- [message-group-chat-message-document-model](message-group-chat-message-document-model.md)
- [knowledge-agent-scoped-knowledge-base-service](knowledge-agent-scoped-knowledge-base-service.md)
- [workspaceservice-workspace-domain-business-logic](workspaceservice-workspace-domain-business-logic.md)
- [ripplenormalizer-ai-generated-ripplespec-validation-and-normalization](ripplenormalizer-ai-generated-ripplespec-validation-and-normalization.md)
- [eecloudworkspace-workspace-module-initialization](eecloudworkspace-workspace-module-initialization.md)
