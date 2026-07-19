from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class LoginRequest(BaseModel):
    username: str = Field(..., min_length=1, max_length=150)
    password: str = Field(..., min_length=1)


class RefreshRequest(BaseModel):
    refresh_token: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RoleOut(BaseModel):
    id: uuid.UUID
    name: str
    description: str | None

    model_config = ConfigDict(from_attributes=True)


class UserResponse(BaseModel):
    id: uuid.UUID
    username: str
    email: str
    display_name: str
    is_active: bool
    role: RoleOut
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
