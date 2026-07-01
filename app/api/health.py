from fastapi import APIRouter
from sqlalchemy import text

from app.database.connection import engine

router = APIRouter(
    prefix="/health",
    tags=["Health"],
)


@router.get("/db")
def database_health():
    with engine.connect() as connection:
        version = connection.execute(
            text("SELECT version();")
        ).scalar()

    return {
        "status": "connected",
        "database": "enterprise_ai_db",
        "postgres_version": version,
    }