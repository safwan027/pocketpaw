"""Agents domain — FastAPI router."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from starlette.responses import Response

from ee.cloud.agents.schemas import (
    AgentResponse,
    CreateAgentRequest,
    DiscoverRequest,
    UpdateAgentRequest,
)
from ee.cloud.agents.service import AgentService
from ee.cloud.license import require_license
from ee.cloud.shared.deps import current_user_id, current_workspace_id

router = APIRouter(
    prefix="/agents", tags=["Agents"], dependencies=[Depends(require_license)]
)

# ---------------------------------------------------------------------------
# CRUD
# ---------------------------------------------------------------------------


@router.post("", response_model=AgentResponse)
async def create_agent(
    body: CreateAgentRequest,
    workspace_id: str = Depends(current_workspace_id),
    user_id: str = Depends(current_user_id),
) -> AgentResponse:
    return await AgentService.create(workspace_id, user_id, body)


@router.get("", response_model=list[AgentResponse])
async def list_agents(
    workspace_id: str = Depends(current_workspace_id),
    query: str | None = Query(default=None),
) -> list[AgentResponse]:
    return await AgentService.list_agents(workspace_id, query)


@router.get("/{agent_id}", response_model=AgentResponse)
async def get_agent(agent_id: str) -> AgentResponse:
    return await AgentService.get(agent_id)


@router.get("/uname/{slug}", response_model=AgentResponse)
async def get_by_slug(
    slug: str,
    workspace_id: str = Depends(current_workspace_id),
) -> AgentResponse:
    return await AgentService.get_by_slug(workspace_id, slug)


@router.patch("/{agent_id}", response_model=AgentResponse)
async def update_agent(
    agent_id: str,
    body: UpdateAgentRequest,
    user_id: str = Depends(current_user_id),
) -> AgentResponse:
    return await AgentService.update(agent_id, user_id, body)


@router.delete("/{agent_id}", status_code=204)
async def delete_agent(
    agent_id: str,
    user_id: str = Depends(current_user_id),
) -> Response:
    await AgentService.delete(agent_id, user_id)
    return Response(status_code=204)


# ---------------------------------------------------------------------------
# Discovery
# ---------------------------------------------------------------------------


@router.post("/discover", response_model=list[AgentResponse])
async def discover_agents(
    body: DiscoverRequest,
    workspace_id: str = Depends(current_workspace_id),
    user_id: str = Depends(current_user_id),
) -> list[AgentResponse]:
    return await AgentService.discover(workspace_id, user_id, body)
