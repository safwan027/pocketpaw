# ripple_normalizer — AI-generated rippleSpec validation and normalization

> Normalizes AI-generated rippleSpec objects before persistence by ensuring envelope fields (version, lifecycle ID, metadata), generating missing widget IDs, and handling multiple spec formats (multi-pane, UISpec v1.0, flat widgets). Acts as a validation layer that standardizes inconsistent AI output into a uniform internal format.

**Categories:** AI specification processing, data normalization, pocket/dashboard framework, cloud service utilities  
**Concepts:** _short_id, normalize_ripple_spec, envelope standardization, pocket ID generation, multi-pane specs, UISpec v1.0, flat widget specs, widget ID generation, metadata normalization, fallback chaining  
**Words:** 436 | **Version:** 1

---

## Purpose

Provides minimal normalization for rippleSpec objects produced by AI agents. Ensures all specs have required envelope metadata and widget identifiers before being persisted to the system, without modifying the core structure of well-formed specs.

## Key Functions

### `_short_id() → str`
Generates a cryptographically secure 8-character hex token using `secrets.token_hex(4)`. Used to create unique pocket IDs when not provided.

### `normalize_ripple_spec(spec: dict | None) → dict | None`
Main normalization entry point. Accepts a spec dictionary and returns a normalized version or None if invalid.

**Envelope Standardization:**
- Extracts or generates pocket ID from: `spec.id` → `lifecycle.id` → `pocket-{random}`
- Extracts title/name from `title` or `name` fields
- Resolves color from `color` or `metadata.color` (default: `#0A84FF`)
- Ensures metadata contains category (default: `custom`)

**Format-Specific Handling:**
1. **Multi-pane specs** (`panes` field exists): Passes through with envelope and version 1.0
2. **UISpec v1.0** (`ui` field with type): Passes through with envelope and version 1.0
3. **Flat widget specs** (`widgets` list): Generates missing widget IDs as `{pocket_id}-w{index}`, ensures titles, adds display/dashboard_layout defaults, sets intent to `dashboard`, uses version 2.0
4. **Empty specs**: Returns envelope only

**Widget Processing:**
- Skips non-dict widgets
- Generates ID as `{pocket_id}-w{index}` if missing
- Populates title from `name` field or defaults to `Widget {n}`

## Dependencies

- `secrets` (stdlib) — cryptographic token generation
- `typing` (stdlib) — type hints for Python 3.9+

## Input/Output

**Input:** AI-generated rippleSpec dict with inconsistent envelope fields and optional widget specs

**Output:** Normalized spec dict with guaranteed:
- `lifecycle.id` (unique pocket identifier)
- `title` and `name`
- `color` and `metadata.color`
- `metadata.category`
- `version` (1.0 or 2.0 depending on format)
- Widget IDs (for flat widget specs)

## Usage Examples

```python
# AI-generated spec with missing envelope fields
raw_spec = {
  "title": "Sales Dashboard",
  "widgets": [
    {"name": "Revenue", "data_source": "sales_db"},
    {"name": "Growth", "data_source": "analytics"}
  ]
}

normalized = normalize_ripple_spec(raw_spec)
# Returns:
# {
#   "title": "Sales Dashboard",
#   "name": "Sales Dashboard",
#   "lifecycle": {"type": "persistent", "id": "pocket-a1b2c3d4"},
#   "color": "#0A84FF",
#   "metadata": {"category": "custom", "color": "#0A84FF"},
#   "version": "2.0",
#   "intent": "dashboard",
#   "widgets": [
#     {"id": "pocket-a1b2c3d4-w0", "title": "Revenue", ...},
#     {"id": "pocket-a1b2c3d4-w1", "title": "Growth", ...}
#   ],
#   "display": {"columns": 3},
#   "dashboard_layout": {"type": "grid", "columns": 3, "gap": 10}
# }
```

## Design Patterns

- **Fallback chaining** — sequential field checks for ID, color, category
- **Format detection** — type-based routing (panes → multi-pane, ui.type → UISpec, widgets → flat)
- **Minimal mutation** — preserves original spec fields while layering envelope
- **Defensive copying** — shallow copies widgets to avoid modifying input
- **Null safety** — returns None for invalid inputs, supports None input

---

## Related

- [workspaceservice-workspace-domain-business-logic](workspaceservice-workspace-domain-business-logic.md)
- [agentbridge-cloud-chat-event-bridge-to-pocketpaw-agent-pool](agentbridge-cloud-chat-event-bridge-to-pocketpaw-agent-pool.md)
