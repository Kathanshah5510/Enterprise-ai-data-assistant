from __future__ import annotations

import uuid
from datetime import date
from typing import TYPE_CHECKING
from sqlalchemy import Date, ForeignKey, String, UniqueConstraint, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseModel

if TYPE_CHECKING:
    from app.models.employee import Employee
    from app.models.project import Project


class ProjectAssignment(BaseModel):
    """Database model linking employees to projects with a specific role."""

    __tablename__ = "project_assignments"

    __table_args__ = (
        UniqueConstraint("project_id", "employee_id", name="uq_project_employee"),
    )

    project_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        ForeignKey("projects.id"),
        nullable=False,
        index=True,
    )
    employee_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        ForeignKey("employees.id"),
        nullable=False,
        index=True,
    )
    role: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
    assigned_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )
    end_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    # Relationships
    project: Mapped[Project] = relationship(
        back_populates="assignments",
    )
    employee: Mapped[Employee] = relationship(
        back_populates="project_assignments",
    )
