# schemas — Sessions domain request/response models

> Defines Pydantic models for session management operations in the pocketPaw system. Provides request schemas for creating and updating sessions, and a comprehensive response schema for session data retrieval. Serves as the contract between API endpoints and internal service logic.

**Categories:** sessions domain, schemas & validation, API contracts  
**Concepts:** CreateSessionRequest, UpdateSessionRequest, SessionResponse, Pydantic validation, request/response contracts, optional associations, soft-delete pattern, timestamp tracking, Pydantic  
**Words:** 234 | **Version:** 1

---

## Purpose
This module centralizes Pydantic BaseModel definitions for the sessions domain, enabling type-safe request validation and response serialization across the application. It acts as the data contract layer between HTTP handlers and business logic.

## Key Classes

### CreateSessionRequest
Schema for session creation requests.
- **title** (str): Session display name, defaults to "New Chat"
- **pocket_id** (str | None): Optional reference to a linked pocket
- **group_id** (str | None): Optional group association
- **agent_id** (str | None): Optional agent association

### UpdateSessionRequest
Schema for session modification requests.
- **title** (str | None): Update session name (optional)
- **pocket_id** (str | None): Link or unlink a pocket (optional)

### SessionResponse
Comprehensive schema for session data representation.
- **id, session_id** (str): Primary and unique session identifiers
- **workspace, owner** (str): Organizational context
- **title** (str): Session name
- **pocket, group, agent** (str | None): Optional resource associations
- **message_count** (int): Message tally
- **last_activity** (datetime): Most recent interaction timestamp
- **created_at** (datetime): Creation timestamp
- **deleted_at** (datetime | None): Soft-delete marker

## Dependencies
Dependencies: pydantic (BaseModel, Field), datetime

Used by: router, service, group_service, message_service, ws, agent_bridge

## Design Patterns
- **Optional fields with None defaults**: Enable partial updates and flexible resource associations
- **Dual ID fields**: `id` and `session_id` accommodate different internal/external identifier schemes
- **Soft-delete pattern**: `deleted_at` field supports logical deletion
- **Timestamp tracking**: Creation and activity timestamps enable temporal queries and analytics

---

## Related

- [router-workspace-domain-fastapi-endpoints](router-workspace-domain-fastapi-endpoints.md)
- [workspaceservice-workspace-domain-business-logic](workspaceservice-workspace-domain-business-logic.md)
- [groupservice-group-and-channel-business-logic-crud-membership-agents-dms](groupservice-group-and-channel-business-logic-crud-membership-agents-dms.md)
- [messageservice-message-business-logic-and-crud-operations](messageservice-message-business-logic-and-crud-operations.md)
- [ws-websocket-connection-manager-for-real-time-chat](ws-websocket-connection-manager-for-real-time-chat.md)
- [agentbridge-cloud-chat-event-bridge-to-pocketpaw-agent-pool](agentbridge-cloud-chat-event-bridge-to-pocketpaw-agent-pool.md)
