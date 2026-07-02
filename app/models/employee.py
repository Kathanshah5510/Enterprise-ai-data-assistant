from __future__ import annotations

import uuid
from datetime import date
from decimal import Decimal
from typing import TYPE_CHECKING
from sqlalchemy import Boolean, Date, ForeignKey, Numeric, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseModel

if TYPE_CHECKING:
    from app.models.department import Department


class Employee(BaseModel):
    """Database model representing an employee."""

    __tablename__ = "employees"

    employee_number: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        index=True,
        nullable=False,
    )
    first_name: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
    last_name: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
    )
    phone_number: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )
    job_title: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    salary: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
        index=True,
    )
    hire_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        index=True,
    )
    employment_type: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )
    status: Mapped[str] = mapped_column(
        String(20),
        default="ACTIVE",
        nullable=False,
    )
    office_location: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    department_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        ForeignKey("departments.id"),
        nullable=False,
    )
    manager_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid,
        ForeignKey("employees.id"),
        nullable=True,
    )

    # Relationships
    department: Mapped[Department] = relationship(
        back_populates="employees",
    )
    manager: Mapped[Employee | None] = relationship(
        back_populates="direct_reports",
        remote_side="Employee.id",
    )
    direct_reports: Mapped[list[Employee]] = relationship(
        back_populates="manager",
    )
