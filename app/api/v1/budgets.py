from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.deps import require_role
from app.database.connection import get_db
from app.models import Budget, User
from app.schemas.budget import BudgetCreate, BudgetResponse, BudgetUpdate

router = APIRouter(prefix="/budgets", tags=["Budgets"])

_BUDGET_READ_ROLES = ("admin", "finance", "manager")
_BUDGET_WRITE_ROLES = ("admin", "finance")


@router.get("/", response_model=list[BudgetResponse])
def list_budgets(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, le=100),
    _: User = Depends(require_role(*_BUDGET_READ_ROLES)),
    db: Session = Depends(get_db),
) -> list[Budget]:
    return db.query(Budget).offset(skip).limit(limit).all()


@router.get("/{budget_id}", response_model=BudgetResponse)
def get_budget(
    budget_id: str,
    _: User = Depends(require_role(*_BUDGET_READ_ROLES)),
    db: Session = Depends(get_db),
) -> Budget:
    budget = db.query(Budget).filter(Budget.id == budget_id).first()
    if not budget:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Budget not found")
    return budget


@router.post("/", response_model=BudgetResponse, status_code=status.HTTP_201_CREATED)
def create_budget(
    body: BudgetCreate,
    _: User = Depends(require_role(*_BUDGET_WRITE_ROLES)),
    db: Session = Depends(get_db),
) -> Budget:
    budget = Budget(**body.model_dump())
    db.add(budget)
    try:
        db.commit()
        db.refresh(budget)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="A budget for this project already exists")
    return budget


@router.put("/{budget_id}", response_model=BudgetResponse)
def update_budget(
    budget_id: str,
    body: BudgetUpdate,
    _: User = Depends(require_role(*_BUDGET_WRITE_ROLES)),
    db: Session = Depends(get_db),
) -> Budget:
    budget = db.query(Budget).filter(Budget.id == budget_id).first()
    if not budget:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Budget not found")
    for field, value in body.model_dump(exclude_none=True).items():
        setattr(budget, field, value)
    try:
        db.commit()
        db.refresh(budget)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Budget update conflict")
    return budget
