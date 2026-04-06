# errors — Unified error hierarchy for the cloud module

> Defines a consistent exception hierarchy rooted in `CloudError` that replaces raw `HTTPException` usage across the cloud package. Each subclass maps to a specific HTTP status code and carries a machine-readable code and human-readable message, ensuring uniform error handling, logging, and API response formatting.

**Categories:** error-handling, cloud-infrastructure, shared-utilities  
**Concepts:** CloudError, NotFound, Forbidden, ConflictError, ValidationError, SeatLimitError, to_dict, error envelope pattern, exception hierarchy, HTTP status code mapping  
**Words:** 356 | **Version:** 1

---

## Purpose

This module establishes a single error hierarchy so that every domain package within `ee.cloud` raises structured, predictable exceptions instead of ad-hoc `HTTPException` instances. This keeps error handling, logging, and JSON API responses consistent across services, routers, and permission layers.

## Key Classes

### `CloudError(Exception)`
Base exception for all cloud errors. Every instance carries three attributes:
- **`status_code`** (`int`) — HTTP status code (e.g. 404, 403).
- **`code`** (`str`) — Machine-readable error code (e.g. `"org.not_found"`).
- **`message`** (`str`) — Human-readable description.

Provides `to_dict()` which returns a standardized JSON error envelope:
```python
{"error": {"code": "...", "message": "..."}}
```

### `NotFound(CloudError)` — 404
Raised when a resource cannot be found. Accepts `resource` and optional `resource_id` to auto-generate the code (`"{resource}.not_found"`) and message.

### `Forbidden(CloudError)` — 403
Raised when access is denied. Accepts a custom `code` and an optional `message` (defaults to `"Access denied"`).

### `ConflictError(CloudError)` — 409
Raised on resource conflicts (e.g. duplicate creation). Requires both `code` and `message`.

### `ValidationError(CloudError)` — 422
Raised when input validation fails. Requires both `code` and `message`.

### `SeatLimitError(CloudError)` — 402
Raised when a billing/seat limit is reached. Accepts `seats` count and auto-generates the code `"billing.seat_limit"`.

## Dependencies

- **Imports from**: None (leaf module with no internal or third-party dependencies).
- **Imported by**: `__init__`, `service`, `group_service`, `message_service`, `router`, `deps`, `permissions` — making it a foundational module across the cloud package.

## Usage Examples

```python
from ee.cloud.shared.errors import NotFound, Forbidden, SeatLimitError

# Raising a not-found error
raise NotFound("org", org_id)
# -> 404, code="org.not_found", message="org 'abc123' not found"

# Raising a forbidden error
raise Forbidden("org.member_required")
# -> 403, code="org.member_required", message="Access denied"

# Raising a seat limit error
raise SeatLimitError(seats=10)
# -> 402, code="billing.seat_limit", message="Seat limit of 10 reached"

# Converting to JSON response in an exception handler
except CloudError as exc:
    return JSONResponse(status_code=exc.status_code, content=exc.to_dict())
```

## Design Notes

- The `to_dict()` method on the base class means any exception handler only needs to catch `CloudError` to produce a uniform JSON envelope.
- Machine-readable `code` values follow a `"{domain}.{reason}"` convention, making them stable identifiers for client-side error handling.
- The hierarchy is intentionally flat (one level of inheritance) to keep things simple and discoverable.