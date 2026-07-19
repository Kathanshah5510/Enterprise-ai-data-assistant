from __future__ import annotations

import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, computed_field

_CURRENT_YEAR = 2026
_MIN_YEAR = 2000
_MAX_YEAR = _CURRENT_YEAR + 10


class BudgetCreate(BaseModel):
    project_id: uuid.UUID
    total_amount: Decimal = Field(..., ge=Decimal("0"))
    spent_amount: Decimal = Field(default=Decimal("0.00"), ge=Decimal("0"))
    fiscal_year: int = Field(..., ge=_MIN_YEAR, le=_MAX_YEAR)


class BudgetUpdate(BaseModel):
    total_amount: Decimal | None = Field(default=None, ge=Decimal("0"))
    spent_amount: Decimal | None = Field(default=None, ge=Decimal("0"))
    fiscal_year: int | None = Field(default=None, ge=_MIN_YEAR, le=_MAX_YEAR)


class BudgetResponse(BaseModel):
    id: uuid.UUID
    project_id: uuid.UUID
    total_amount: Decimal
    spent_amount: Decimal
    fiscal_year: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

    @computed_field
    @property
    def is_over_budget(self) -> bool:
        return self.spent_amount > self.total_amount
