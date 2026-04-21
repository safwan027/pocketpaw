# Trace API router — list and inspect request traces.
# Created: 2026-04-20

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query

from pocketpaw.api.deps import require_scope
from pocketpaw.traces import get_trace_store

router = APIRouter(tags=["Traces"])


@router.get("/traces", dependencies=[Depends(require_scope("metrics", "admin"))])
async def list_traces(
    since: str = Query("", description="ISO timestamp filter"),
    limit: int = Query(100, ge=1, le=1000),
    session_id: str = Query("", description="session key or session id"),
    min_cost: float = Query(0.0, ge=0.0),
):
    """Return recent traces with optional filters."""
    store = get_trace_store()
    return await store.list_traces(
        since=since or None,
        limit=limit,
        session_id=session_id,
        min_cost=min_cost,
    )


@router.get("/traces/{trace_id}", dependencies=[Depends(require_scope("metrics", "admin"))])
async def get_trace(trace_id: str):
    """Return full trace payload by trace ID."""
    store = get_trace_store()
    trace = await store.get_trace(trace_id)
    if trace is None:
        raise HTTPException(status_code=404, detail="Trace not found")
    return trace
