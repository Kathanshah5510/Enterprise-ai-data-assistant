from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_role
from app.database.connection import get_db
from app.models import Department, User
from app.schemas.department import DepartmentCreate, DepartmentResponse, DepartmentUpdate

router = APIRouter(prefix="/departments", tags=["Departments"])


@router.get("/", response_model=list[DepartmentResponse])
def list_departments(
    skip: int = 0,
    limit: int = Query(default=20, le=100),
    _: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[Department]:
    return db.query(Department).offset(skip).limit(limit).all()


@router.get("/{department_id}", response_model=DepartmentResponse)
def get_department(
    department_id: str,
    _: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Department:
    dept = db.query(Department).filter(Department.id == department_id).first()
    if not dept:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Department not found")
    return dept


@router.post("/", response_model=DepartmentResponse, status_code=status.HTTP_201_CREATED)
def create_department(
    body: DepartmentCreate,
    _: User = Depends(require_role("admin")),
    db: Session = Depends(get_db),
) -> Department:
    dept = Department(**body.model_dump())
    db.add(dept)
    try:
        db.commit()
        db.refresh(dept)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Department name or code already exists")
    return dept


@router.put("/{department_id}", response_model=DepartmentResponse)
def update_department(
    department_id: str,
    body: DepartmentUpdate,
    _: User = Depends(require_role("admin")),
    db: Session = Depends(get_db),
) -> Department:
    dept = db.query(Department).filter(Department.id == department_id).first()
    if not dept:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Department not found")
    for field, value in body.model_dump(exclude_none=True).items():
        setattr(dept, field, value)
    try:
        db.commit()
        db.refresh(dept)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Department name or code already exists")
    return dept


@router.delete("/{department_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_department(
    department_id: str,
    _: User = Depends(require_role("admin")),
    db: Session = Depends(get_db),
) -> None:
    dept = db.query(Department).filter(Department.id == department_id).first()
    if not dept:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Department not found")
    db.delete(dept)
    db.commit()
