"""Auth domain — business logic service."""

from __future__ import annotations

from fastapi import HTTPException

from ee.cloud.models.user import User
from ee.cloud.auth.schemas import ProfileUpdateRequest, UserResponse


class AuthService:
    """Stateless service encapsulating auth-related business logic."""

    @staticmethod
    async def get_profile(user: User) -> UserResponse:
        """Return the current user's profile as a UserResponse."""
        return UserResponse(
            id=str(user.id),
            email=user.email,
            name=user.full_name,
            image=user.avatar,
            email_verified=user.is_verified,
            active_workspace=user.active_workspace,
            workspaces=[
                {"workspace": w.workspace, "role": w.role}
                for w in user.workspaces
            ],
        )

    @staticmethod
    async def update_profile(user: User, body: ProfileUpdateRequest) -> UserResponse:
        """Update mutable profile fields and return the updated profile."""
        if body.full_name is not None:
            user.full_name = body.full_name
        if body.avatar is not None:
            user.avatar = body.avatar
        if body.status is not None:
            user.status = body.status
        await user.save()
        return await AuthService.get_profile(user)

    @staticmethod
    async def set_active_workspace(user: User, workspace_id: str) -> None:
        """Set the user's active workspace."""
        if not workspace_id:
            raise HTTPException(400, "workspace_id required")
        user.active_workspace = workspace_id
        await user.save()
