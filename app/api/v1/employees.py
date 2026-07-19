from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_role
from app.database.connection import get_db
from app.models import Employee, User
from app.schemas.employee import EmployeeCreate, EmployeeResponse, EmployeeUpdate

router = APIRouter(prefix="/employees", tags=["Employees"])


@router.get("/", response_model=list[EmployeeResponse])
def list_employees(
    skip: int = 0,
    limit: int = Query(default=20, le=100),
    _: User = Depends(require_role("admin", "manager", "hr", "finance")),
    db: Session = Depends(get_db),
) -> list[Employee]:
    return db.query(Employee).offset(skip).limit(limit).all()


@router.get("/{employee_id}", response_model=EmployeeResponse)
def get_employee(
    employee_id: str,
    _: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Employee:
    emp = db.query(Employee).filter(Employee.id == employee_id).first()
    if not emp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    return emp


@router.post("/", response_model=EmployeeResponse, status_code=status.HTTP_201_CREATED)
def create_employee(
    body: EmployeeCreate,
    _: User = Depends(require_role("admin", "hr")),
    db: Session = Depends(get_db),
) -> Employee:
    emp = Employee(**body.model_dump())
    db.add(emp)
    try:
        db.commit()
        db.refresh(emp)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Employee number or email already exists")
    return emp


@router.put("/{employee_id}", response_model=EmployeeResponse)
def update_employee(
    employee_id: str,
    body: EmployeeUpdate,
    _: User = Depends(require_role("admin", "hr")),
    db: Session = Depends(get_db),
) -> Employee:
    emp = db.query(Employee).filter(Employee.id == employee_id).first()
    if not emp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    for field, value in body.model_dump(exclude_none=True).items():
        setattr(emp, field, value)
    try:
        db.commit()
        db.refresh(emp)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")
    return emp


@router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(
    employee_id: str,
    _: User = Depends(require_role("admin")),
    db: Session = Depends(get_db),
) -> None:
    emp = db.query(Employee).filter(Employee.id == employee_id).first()
    if not emp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    db.delete(emp)
    db.commit()
