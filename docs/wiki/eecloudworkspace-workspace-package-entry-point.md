# ee.cloud.workspace — Workspace Package Entry Point

> This is the package initializer for the Enterprise Edition (EE) cloud workspace module. It serves as the public API surface for the workspace package by re-exporting the FastAPI router, making it available to upstream modules that import from this package.

**Categories:** workspace, enterprise edition, API routing, package initialization  
**Concepts:** router re-export, FastAPI APIRouter, package entry point, enterprise edition module, workspace domain, noqa suppression  
**Words:** 265 | **Version:** 1

---

## Purpose

The `__init__.py` file for `ee.cloud.workspace` acts as the package entry point and public interface. Its sole responsibility is to re-export the `router` object from `ee.cloud.workspace.router`, exposing the workspace API routes to the rest of the application. This follows a common FastAPI pattern where each feature domain defines its own router, and the package init makes it easily importable.

## Key Classes/Functions

This module defines no classes or functions directly. It re-exports:

- **`router`** — The FastAPI `APIRouter` instance from `ee.cloud.workspace.router` that aggregates all workspace-related HTTP endpoints.

## Dependencies

The module directly imports from:

- `ee.cloud.workspace.router` — Contains the assembled API router for workspace operations.

The broader `ee.cloud.workspace` package has an extensive internal dependency graph spanning:

- **Core domain**: `workspace`, `core`, `deps` — Workspace models, core logic, and dependency injection
- **Auth & licensing**: `license`, `user`, `session`, `invite` — Enterprise licensing, user management, sessions, and invitations
- **Collaboration**: `agent`, `agent_bridge`, `comment`, `message`, `notification`, `group` — Agent integration, messaging, comments, notifications, and group management
- **Data & events**: `file`, `pocket`, `event_handlers` — File handling, pocket (item) management, and event-driven side effects
- **Error handling**: `errors` — Custom exception types for the workspace domain

## Usage Examples

```python
# Typical usage in a FastAPI application assembly
from ee.cloud.workspace import router as workspace_router

app.include_router(workspace_router, prefix="/workspace")
```

## Architecture Notes

This package follows the Enterprise Edition (EE) convention, residing under `ee/cloud/` to separate premium workspace features from the open-source core. The single re-export pattern keeps the public API minimal while the internal submodules handle the full complexity of workspace operations including agent orchestration, real-time collaboration, and access control.