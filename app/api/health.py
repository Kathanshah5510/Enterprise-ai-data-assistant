from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.api.deps import get_current_user
from app.database.connection import get_db
from app.models import User

router = APIRouter(
    prefix="/health",
    tags=["Health"],
)


@router.get("")
def liveness() -> dict[str, str]:
    """Lightweight liveness probe — no external dependencies."""
    return {"status": "ok"}


@router.get("/db")
def database_health(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> dict[str, str | None]:
    """Check database connection health (requires authentication)."""
    try:
        version = db.execute(text("SELECT version();")).scalar()
        return {
            "status": "connected",
            "database": "enterprise_ai_db",
            "postgres_version": version,
        }
    except SQLAlchemyError:
        raise HTTPException(
            status_code=500,
            detail="Database connection failed",
        )
