from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.database.connection import get_db

router = APIRouter(
    prefix="/health",
    tags=["Health"],
)


@router.get("/db")
def database_health(db: Session = Depends(get_db)) -> dict[str, str | None]:
    """Check database connection health."""
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