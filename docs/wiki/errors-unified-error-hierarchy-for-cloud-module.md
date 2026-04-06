# errors — Unified error hierarchy for cloud module

> Defines a consistent exception hierarchy for the cloud module that replaces raw HTTPExceptions with domain-specific errors. Every domain package raises these standardized errors to ensure uniform error handling, logging, and API responses across the system.

**Categories:** error handling, cloud module, exceptions, API response formatting  
**Concepts:** CloudError, NotFound, Forbidden, ConflictError, ValidationError, SeatLimitError, status_code, error_code, to_dict, exception_hierarchy  
**Words:** 328 | **Version:** 1

---

## Purpose

Provide a centralized, standardized error hierarchy for the cloud module that enables:
- Consistent HTTP status code mapping
- Machine-readable error codes for programmatic handling
- Human-readable messages for API responses
- JSON-serializable error envelopes

## Key Classes

### CloudError
Base exception class for all cloud errors.
- **Attributes**: `status_code` (int), `code` (str), `message` (str)
- **Methods**: `to_dict()` returns JSON-serializable error envelope
- **Usage**: Parent class for all domain-specific errors

### NotFound
Raised when a resource cannot be found (HTTP 404).
- **Constructor**: `NotFound(resource, resource_id="")`
- **Auto-generates**: Code as `{resource}.not_found`, message with optional resource ID
- **Example**: `NotFound("user", "12345")` → `user '12345' not found`

### Forbidden
Raised when access is denied (HTTP 403).
- **Constructor**: `Forbidden(code, message="Access denied")`
- **Customizable**: Both code and message parameters

### ConflictError
Raised when a resource conflict occurs (HTTP 409).
- **Constructor**: `ConflictError(code, message)`
- **Use case**: Duplicate resources, state conflicts

### ValidationError
Raised when input validation fails (HTTP 422).
- **Constructor**: `ValidationError(code, message)`
- **Use case**: Invalid request data, schema violations

### SeatLimitError
Raised when billing or seat limits are exceeded (HTTP 402).
- **Constructor**: `SeatLimitError(seats)`
- **Auto-generates**: Code as `billing.seat_limit`, message with seat count

## Error Response Format

All errors serialize to:
```json
{
  "error": {
    "code": "resource.error_type",
    "message": "Human-readable description"
  }
}
```

## Dependencies

**Internal dependencies**: None within scanned set

**Used by**: `__init__`, `service`, `group_service`, `message_service`, `router`, `deps`, `permissions`

## Usage Examples

```python
# Raise NotFound
raise NotFound("user", "user_123")

# Raise Forbidden
raise Forbidden("permission.insufficient", "Admin role required")

# Raise ValidationError
raise ValidationError("email.invalid", "Email format is invalid")

# Serialize to JSON
error = NotFound("group", "grp_456")
error.to_dict()  # {"error": {"code": "group.not_found", "message": "..."}}
```

## Architecture Notes

- **Consistency**: All errors follow a unified pattern with status code, machine-readable code, and human-readable message
- **Extensibility**: New error types inherit from `CloudError` and follow the established pattern
- **API-friendly**: Direct mapping to HTTP status codes and JSON serialization for REST responses
- **Logging-friendly**: Machine-readable codes enable structured logging and monitoring

---

## Related

- [eecloudworkspace-workspace-module-initialization](eecloudworkspace-workspace-module-initialization.md)
- [workspaceservice-workspace-domain-business-logic](workspaceservice-workspace-domain-business-logic.md)
- [groupservice-group-and-channel-business-logic-crud-membership-agents-dms](groupservice-group-and-channel-business-logic-crud-membership-agents-dms.md)
- [messageservice-message-business-logic-and-crud-operations](messageservice-message-business-logic-and-crud-operations.md)
- [router-workspace-domain-fastapi-endpoints](router-workspace-domain-fastapi-endpoints.md)
- [deps-fastapi-dependency-injection-for-cloud-authentication-and-authorization](deps-fastapi-dependency-injection-for-cloud-authentication-and-authorization.md)
- [permissions-role-and-access-level-permission-checks](permissions-role-and-access-level-permission-checks.md)
