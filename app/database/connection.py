from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.core.config import settings

if not settings.DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is missing.")

engine = create_engine(
    settings.DATABASE_URL,
    echo=False,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db() -> Generator[Session, None, None]:
    """Yield database session."""
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()