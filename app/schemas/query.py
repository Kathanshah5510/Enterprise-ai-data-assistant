from __future__ import annotations

from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    question: str = Field(..., min_length=3, max_length=1000)
    conversation_id: UUID | None = None


class QueryResponse(BaseModel):
    question: str
    sql_query: str
    results: list[dict[str, Any]]
    row_count: int
    execution_time_ms: int
    chart_suggestion: str
    conversation_id: UUID
    message_id: UUID
    error: str | None = None
