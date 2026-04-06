# SessionService — Session business logic and CRUD operations

> Encapsulates stateless business logic for managing user sessions in the cloud workspace. Handles session creation, retrieval, updates, deletion, and activity tracking. Integrates with pockets, groups, and message history to provide a complete session management layer.

**Categories:** domain/sessions, business logic, cloud services, CRUD operations  
**Concepts:** SessionService, _session_response, create, list_sessions, get, update, delete, list_for_pocket, create_for_pocket, get_history  
**Words:** 447 | **Version:** 1

---

## Purpose

The `SessionService` module implements the core business logic for session management in the OCEAN cloud platform. Sessions represent persistent chat contexts that users create within workspaces, optionally linked to pockets (document containers) and groups (shared collections). The service enforces ownership/permission checks and coordinates with related domain services.

## Key Classes and Functions

### SessionService (Main Service Class)

Stateless service providing session domain operations:

**CRUD Operations:**
- `create(workspace_id, user_id, body)` — Creates a new session with optional pocket/group/agent links; emits `session.created` event
- `get(session_id, user_id)` — Retrieves a single session by ObjectId or sessionId UUID; verifies ownership
- `list_sessions(workspace_id, user_id)` — Lists all non-deleted sessions for user, sorted by lastActivity descending
- `update(session_id, user_id, body)` — Updates title and pocket_id fields; owner-only
- `delete(session_id, user_id)` — Soft-deletes via `deleted_at` timestamp; owner-only

**Pocket-Scoped Helpers:**
- `list_for_pocket(pocket_id, user_id)` — Lists sessions filtered by pocket
- `create_for_pocket(workspace_id, user_id, pocket_id, body)` — Creates session pre-bound to a pocket

**Runtime & Activity:**
- `get_history(session_id, user_id)` — Retrieves chat message history from MongoDB group messages; graceful error handling returns empty messages
- `touch(session_id)` — Updates lastActivity timestamp and increments messageCount for activity tracking

**Internal:**
- `_get_session(session_id, user_id)` — Internal lookup by ObjectId or sessionId; enforces ownership verification and deletion check; raises `NotFound` or `Forbidden`

### _session_response(session)

Helper function converting MongoDB Session documents to frontend-compatible dictionaries. Normalizes datetime fields to ISO format and maps internal fields to API contract (e.g., `deleted_at` → `deletedAt`).

## Dependencies

- **Models**: `Session` (Beanie ODM document)
- **Schemas**: `CreateSessionRequest`, `UpdateSessionRequest` for validation
- **Error Handling**: `Forbidden`, `NotFound` exceptions from `ee.cloud.shared.errors`
- **Events**: `event_bus` for async event publishing (session lifecycle events)
- **External Domains**: Implicitly used by router and agent_bridge; coordinates with message, pocket, group, and user services

## Usage Examples

**Creating a session:**
```python
request = CreateSessionRequest(title="Chat with Agent", pocket_id="abc123", agent_id="agent1")
session = await SessionService.create(workspace_id="ws1", user_id="user1", body=request)
# Returns: {"_id": "...", "sessionId": "uuid", "title": "Chat with Agent", ...}
```

**Listing user sessions:**
```python
sessions = await SessionService.list_sessions(workspace_id="ws1", user_id="user1")
# Returns sorted list of active sessions by recent activity
```

**Retrieving chat history:**
```python
history = await SessionService.get_history(session_id="session_uuid", user_id="user1")
# Returns: {"messages": [{"role": "user|assistant", "content": "...", "createdAt": "..."}]}
```

**Recording activity:**
```python
await SessionService.touch(session_id="session_uuid")
# Updates lastActivity and messageCount for sorting/pagination
```

## Architecture Patterns

- **Stateless Service**: All methods are static; no instance state
- **Soft Deletes**: Uses `deleted_at` timestamp instead of hard deletion for data retention
- **Ownership Verification**: All user-scoped operations check `session.owner == user_id`
- **Event Publishing**: Emits domain events for session creation via event bus
- **Graceful Error Handling**: History retrieval logs warnings rather than propagating exceptions
- **ObjectId + UUID Duality**: Sessions have both MongoDB `_id` and a UUID `sessionId` for cross-system references

---

## Related

- [schemas-workspace-domain-requestresponse-models](schemas-workspace-domain-requestresponse-models.md)
- [agent-agent-configuration-models-for-the-cloud-platform](agent-agent-configuration-models-for-the-cloud-platform.md)
- [errors-unified-error-hierarchy-for-cloud-module](errors-unified-error-hierarchy-for-cloud-module.md)
- [user-enterprise-user-and-oauth-account-models](user-enterprise-user-and-oauth-account-models.md)
- [groupservice-group-and-channel-business-logic-crud-membership-agents-dms](groupservice-group-and-channel-business-logic-crud-membership-agents-dms.md)
- [messageservice-message-business-logic-and-crud-operations](messageservice-message-business-logic-and-crud-operations.md)
- [pocket-pocket-workspace-and-widget-document-models](pocket-pocket-workspace-and-widget-document-models.md)
- [session-chat-session-document-model](session-chat-session-document-model.md)
- [ripplenormalizer-ai-generated-ripplespec-validation-and-normalization](ripplenormalizer-ai-generated-ripplespec-validation-and-normalization.md)
- [events-internal-async-event-bus-for-cross-domain-side-effects](events-internal-async-event-bus-for-cross-domain-side-effects.md)
- [message-group-chat-message-document-model](message-group-chat-message-document-model.md)
- [invite-workspace-membership-invitation-management](invite-workspace-membership-invitation-management.md)
- [workspace-workspace-document-model-for-deployments-and-organizations](workspace-workspace-document-model-for-deployments-and-organizations.md)
- [permissions-role-and-access-level-permission-checks](permissions-role-and-access-level-permission-checks.md)
- [router-workspace-domain-fastapi-endpoints](router-workspace-domain-fastapi-endpoints.md)
- [agentbridge-cloud-chat-event-bridge-to-pocketpaw-agent-pool](agentbridge-cloud-chat-event-bridge-to-pocketpaw-agent-pool.md)
