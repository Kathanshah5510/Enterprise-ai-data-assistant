from __future__ import annotations

import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, computed_field


class BudgetCreate(BaseModel):
    project_id: uuid.UUID
    total_amount: Decimal
    spent_amount: Decimal = Decimal("0.00")
    fiscal_year: int


class BudgetUpdate(BaseModel):
    total_amount: Decimal | None = None
    spent_amount: Decimal | None = None
    fiscal_year: int | None = None


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
