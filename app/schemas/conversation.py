from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field


class ConversationCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)


class ConversationResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: UUID
    user_id: UUID
    title: str
    is_active: bool
    created_at: datetime
    updated_at: datetime


class MessageResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: UUID
    conversation_id: UUID
    role: str
    content: str
    sql_query: str | None
    result_data: dict[str, Any] | None
    row_count: int | None
    execution_time_ms: int | None
    error: str | None
    chart_suggestion: str | None
    created_at: datetime


class ConversationDetailResponse(ConversationResponse):
    messages: list[MessageResponse] = []
