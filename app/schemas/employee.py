from __future__ import annotations

import uuid
from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class EmployeeCreate(BaseModel):
    employee_number: str = Field(..., min_length=1)
    first_name: str = Field(..., min_length=1)
    last_name: str = Field(..., min_length=1)
    email: str = Field(..., min_length=1)
    phone_number: str | None = None
    job_title: str = Field(..., min_length=1)
    salary: Decimal = Field(..., gt=Decimal("0"))
    hire_date: date
    employment_type: str = Field(..., min_length=1)
    status: str = "ACTIVE"
    office_location: str = Field(..., min_length=1)
    department_id: uuid.UUID
    manager_id: uuid.UUID | None = None


class EmployeeUpdate(BaseModel):
    first_name: str | None = Field(default=None, min_length=1)
    last_name: str | None = Field(default=None, min_length=1)
    email: str | None = Field(default=None, min_length=1)
    phone_number: str | None = None
    job_title: str | None = Field(default=None, min_length=1)
    salary: Decimal | None = Field(default=None, gt=Decimal("0"))
    employment_type: str | None = None
    status: str | None = None
    office_location: str | None = None
    department_id: uuid.UUID | None = None
    manager_id: uuid.UUID | None = None


class EmployeeResponse(BaseModel):
    id: uuid.UUID
    employee_number: str
    first_name: str
    last_name: str
    email: str
    phone_number: str | None
    job_title: str
    salary: Decimal
    hire_date: date
    employment_type: str
    status: str
    office_location: str
    department_id: uuid.UUID
    manager_id: uuid.UUID | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
