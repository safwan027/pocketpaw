# group — Multi-user chat channels with AI agent participants

> Defines data models for group/channel entities that support multi-user collaboration with AI agent integration. Groups function like Slack channels, supporting multiple members, assigned agents with specific roles and response modes, message tracking, and workspace organization.

**Categories:** data models, collaboration, messaging, agent management  
**Concepts:** GroupAgent, Group, TimestampedDocument, respond_mode, agent role, workspace partitioning, message pinning, MongoDB indexing, multi-user channels, AI agent integration  
**Words:** 185 | **Version:** 1

---

## Purpose
Provides MongoDB document models for managing chat groups/channels within a workspace. Enables organizing conversations with multiple users and AI agents, each with configurable participation roles and response behaviors.

## Key Classes

### GroupAgent
Represents an AI agent assigned to a group with configurable participation:
- **agent**: Agent ID reference
- **role**: Participation level (`assistant`, `listener`, `moderator`)
- **respond_mode**: Behavior pattern (`mention_only`, `auto`, `silent`, `smart`)

### Group
Document model for chat groups/channels extending `TimestampedDocument`:
- **Identity**: `name`, `slug`, `description`, `icon`, `color`
- **Organization**: `workspace`, `type` (public/private/dm), `owner`
- **Participants**: `members` (user IDs), `agents` (GroupAgent list)
- **Content**: `pinned_messages`, `message_count`, `last_message_at`
- **State**: `archived` flag
- **Database Index**: Composite index on (workspace, slug) for efficient lookups

## Dependencies
- `beanie`: MongoDB ODM framework (Indexed)
- `pydantic`: Data validation (BaseModel, Field)
- `ee.cloud.models.base`: TimestampedDocument base class
- Standard library: `datetime`

## Data Model Patterns
- **Indexed fields**: `workspace` for partition isolation
- **Enum-like validation**: Pattern constraints on `type` field
- **Foreign key references**: String IDs for agents, members, and owner
- **Timestamps**: Inherited created_at/updated_at from TimestampedDocument
- **Batch data**: Lists for members, agents, and pinned messages

---

## Related

- [base-timestamped-document-base-class](base-timestamped-document-base-class.md)
- [groupservice-group-and-channel-business-logic-crud-membership-agents-dms](groupservice-group-and-channel-business-logic-crud-membership-agents-dms.md)
- [router-workspace-domain-fastapi-endpoints](router-workspace-domain-fastapi-endpoints.md)
- [eecloudworkspace-workspace-module-initialization](eecloudworkspace-workspace-module-initialization.md)
- [agentbridge-cloud-chat-event-bridge-to-pocketpaw-agent-pool](agentbridge-cloud-chat-event-bridge-to-pocketpaw-agent-pool.md)
- [eventhandlers-cross-domain-event-processing-and-notifications](eventhandlers-cross-domain-event-processing-and-notifications.md)
