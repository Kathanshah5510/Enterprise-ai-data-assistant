from __future__ import annotations

import uuid
from decimal import Decimal
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, Integer, Numeric, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseModel

if TYPE_CHECKING:
    from app.models.project import Project


class Budget(BaseModel):
    """Database model representing a project budget."""

    __tablename__ = "budgets"

    project_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        ForeignKey("projects.id"),
        nullable=False,
        unique=True,
        index=True,
    )
    total_amount: Mapped[Decimal] = mapped_column(
        Numeric(14, 2),
        nullable=False,
    )
    spent_amount: Mapped[Decimal] = mapped_column(
        Numeric(14, 2),
        nullable=False,
        default=Decimal("0.00"),
    )
    fiscal_year: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        index=True,
    )

    # Relationships
    project: Mapped[Project] = relationship(
        back_populates="budget",
    )
