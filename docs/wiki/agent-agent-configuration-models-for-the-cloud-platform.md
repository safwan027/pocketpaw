# agent — Agent configuration models for the cloud platform

> This module defines data models for agent configuration in the PocketPaw cloud system. It provides two main classes: `AgentConfig` for agent behavior parameters and `Agent` for storing agent metadata with configuration in a MongoDB-backed document store. The module supports OCEAN personality trait integration and soul-based personalization.

**Categories:** cloud models, agent management, configuration, personality systems, data persistence  
**Concepts:** AgentConfig, Agent, TimestampedDocument, Indexed, BaseModel, Field, trust_level, soul_ocean, OCEAN trait model, personality configuration  
**Words:** 174 | **Version:** 1

---

## Purpose
Defines the data structure and validation for AI agent configuration, including backend selection, model parameters, tool availability, and personality/soul integration settings.

## Key Classes

### AgentConfig
Pydantic BaseModel containing agent execution parameters:
- **Backend & Model**: `backend` (default: "claude_agent_sdk"), `model` (empty for default)
- **Behavior**: `system_prompt`, `temperature` (0-2, default 0.7), `max_tokens` (default 4096)
- **Trust & Safety**: `trust_level` (1-5, default 3), `tools` list
- **Soul Integration**: `soul_enabled`, `soul_persona`, `soul_archetype`, `soul_values`, `soul_ocean` (OCEAN trait scores)

### Agent
TimestampedDocument subclass representing an agent record in MongoDB:
- **Metadata**: `workspace`, `name`, `slug`, `avatar`, `owner` (User ID)
- **Configuration**: `config` (AgentConfig instance)
- **Access Control**: `visibility` (private/workspace/public)
- **Indexes**: Composite index on (workspace, slug) for efficient querying

## Dependencies
- `beanie`: MongoDB ODM for document indexing
- `pydantic`: Data validation and BaseModel
- `ee.cloud.models.base`: TimestampedDocument base class

## Key Patterns
- Nested configuration objects (AgentConfig within Agent)
- Field constraints using Pydantic validators (ge, le, pattern)
- Factory defaults for mutable fields
- MongoDB document naming and indexing via Settings class
- OCEAN personality model integration

---

## Related

- [base-timestamped-document-base-class](base-timestamped-document-base-class.md)
- [workspaceservice-workspace-domain-business-logic](workspaceservice-workspace-domain-business-logic.md)
- [groupservice-group-and-channel-business-logic-crud-membership-agents-dms](groupservice-group-and-channel-business-logic-crud-membership-agents-dms.md)
- [eecloudworkspace-workspace-module-initialization](eecloudworkspace-workspace-module-initialization.md)
- [agentbridge-cloud-chat-event-bridge-to-pocketpaw-agent-pool](agentbridge-cloud-chat-event-bridge-to-pocketpaw-agent-pool.md)
