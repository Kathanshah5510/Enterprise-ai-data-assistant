from __future__ import annotations

import uuid
from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class EmployeeCreate(BaseModel):
    employee_number: str
    first_name: str
    last_name: str
    email: str
    phone_number: str | None = None
    job_title: str
    salary: Decimal
    hire_date: date
    employment_type: str
    status: str = "ACTIVE"
    office_location: str
    department_id: uuid.UUID
    manager_id: uuid.UUID | None = None


class EmployeeUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    phone_number: str | None = None
    job_title: str | None = None
    salary: Decimal | None = None
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
