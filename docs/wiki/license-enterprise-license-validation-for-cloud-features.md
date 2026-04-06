# license — Enterprise license validation for cloud features

> Validates Ed25519-signed license keys for enterprise feature gating in cloud deployments. License keys are loaded from environment variables on startup, cached in memory, and checked per-request via FastAPI dependencies. Supports both Ed25519 public-key and HMAC-SHA256 secret-based verification modes.

**Categories:** Cloud Platform, Enterprise Features, Authentication & Authorization, Licensing  
**Concepts:** LicensePayload, LicenseInfo, validate_license_key, _verify_signature, load_license, get_license, require_license, require_feature, get_license_info, Ed25519 signature verification  
**Words:** 451 | **Version:** 1

---

## Purpose
Provides enterprise licensing infrastructure for PocketPaw cloud deployments. Validates license keys at startup and gates premium features behind license checks using FastAPI dependency injection. Keys are base64-encoded JSON payloads with cryptographic signatures.

## Key Classes

### LicensePayload
Pydantic model representing decoded license data:
- **Fields**: `org` (organization), `plan` (team|business|enterprise), `seats`, `exp` (ISO expiration date), `features` (optional list)
- **Properties**: `expired` (boolean check against current UTC time), `has_feature(feature)` (checks feature flag or enterprise plan)

### LicenseInfo
Pydantic model for API responses exposing license status to UI:
- **Fields**: `valid`, `org`, `plan`, `seats`, `exp`, `error`

## Key Functions

### Validation
- `validate_license_key(key: str) → LicensePayload` — Decodes base64 key, verifies signature, parses JSON payload, checks expiration. Raises `ValueError` on any failure.
- `_verify_signature(payload_bytes, signature_hex) → bool` — Verifies Ed25519 signature (or HMAC-SHA256 fallback) using embedded or env-configured public key.

### Loading & Caching
- `load_license() → LicensePayload | None` — Loads `POCKETPAW_LICENSE_KEY` env var, validates, caches in `_cached_license`, logs errors to `_license_error`.
- `get_license() → LicensePayload | None` — Returns cached license or calls `load_license()`.

### FastAPI Dependencies
- `require_license() → LicensePayload` — Async dependency that raises HTTP 403 if license missing, invalid, or expired.
- `require_feature(feature: str)` — Dependency factory returning closure that checks `license.has_feature(feature)`, raises HTTP 403 if not included.
- `get_license_info() → LicenseInfo` — Returns license status object for settings UI endpoint.

## Dependencies

**External**:
- `fastapi` (Depends, HTTPException, Request)
- `pydantic` (BaseModel, Field)
- `cryptography` (Ed25519PublicKey — optional, falls back to HMAC)
- `python-dotenv` (load_dotenv — optional)

**Internal**: None (within scanned set)

## Configuration

Environment variables:
- `POCKETPAW_LICENSE_KEY` — Base64-encoded signed license key (required for enterprise features)
- `POCKETPAW_LICENSE_PUBLIC_KEY` — Hex-encoded Ed25519 public key (optional; uses HMAC if absent)
- `POCKETPAW_LICENSE_SECRET` — Shared secret for HMAC-SHA256 verification (fallback mode)

## Key Format

```
base64(payload_json "." signature_hex)
```

**Payload example**:
```json
{"org": "acme-inc", "plan": "team", "seats": 10, "exp": "2027-01-01", "features": ["audit"]}
```

## Usage Examples

**Gate endpoint behind license**:
```python
from fastapi import Depends
from ee.cloud.license import require_license

@app.post("/api/enterprise-feature")
async def feature(lic: LicensePayload = Depends(require_license)):
    return {"org": lic.org, "plan": lic.plan}
```

**Check specific feature**:
```python
from ee.cloud.license import require_feature

@app.post("/api/audit-logs")
async def logs(lic: LicensePayload = Depends(require_feature("audit"))):
    return {"status": "ok"}
```

**Check license at startup**:
```python
from ee.cloud.license import load_license

license = load_license()  # Logs warnings if invalid; returns None if absent
if license:
    print(f"Loaded license for {license.org}")
```

## Patterns & Abstractions

- **Dual-mode crypto**: Ed25519 (production) with HMAC fallback (self-hosted)
- **Lazy loading + caching**: License validated once, cached globally
- **Dependency injection**: FastAPI integration via `Depends()` for clean middleware
- **Plan-based feature bundling**: Enterprise plan auto-enables all features; others use explicit flags
- **Graceful degradation**: Missing key logs warning but doesn't crash; gated endpoints return 403

---

## Related

- [eecloudworkspace-workspace-module-initialization](eecloudworkspace-workspace-module-initialization.md)
- [router-workspace-domain-fastapi-endpoints](router-workspace-domain-fastapi-endpoints.md)
