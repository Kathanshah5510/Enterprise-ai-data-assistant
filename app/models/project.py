from __future__ import annotations

import uuid
from datetime import date
from typing import TYPE_CHECKING
from sqlalchemy import Date, ForeignKey, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseModel

if TYPE_CHECKING:
    from app.models.budget import Budget
    from app.models.department import Department
    from app.models.project_assignment import ProjectAssignment


class Project(BaseModel):
    """Database model representing a company project."""

    __tablename__ = "projects"

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
        index=True,
    )
    description: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )
    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="PLANNING",
        index=True,
    )
    start_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )
    end_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )
    department_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        ForeignKey("departments.id"),
        nullable=False,
        index=True,
    )

    # Relationships
    department: Mapped[Department] = relationship(
        back_populates="projects",
    )
    budget: Mapped[Budget | None] = relationship(
        back_populates="project",
        uselist=False,
    )
    assignments: Mapped[list[ProjectAssignment]] = relationship(
        back_populates="project",
    )
