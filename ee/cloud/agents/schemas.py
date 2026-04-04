"""Agents domain — Pydantic request/response schemas."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Requests
# ---------------------------------------------------------------------------


class CreateAgentRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    slug: str = Field(min_length=1, max_length=50)
    avatar: str = ""
    visibility: str = Field(default="private", pattern="^(private|workspace|public)$")
    config: dict | None = None  # AgentConfig fields


class UpdateAgentRequest(BaseModel):
    name: str | None = None
    avatar: str | None = None
    visibility: str | None = Field(default=None, pattern="^(private|workspace|public)$")
    config: dict | None = None


class DiscoverRequest(BaseModel):
    query: str = ""
    visibility: str | None = None  # filter
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)


# ---------------------------------------------------------------------------
# Responses
# ---------------------------------------------------------------------------


class AgentResponse(BaseModel):
    id: str
    workspace: str
    name: str
    slug: str
    avatar: str
    visibility: str
    config: dict
    owner: str
    created_at: datetime
    updated_at: datetime
