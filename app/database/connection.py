from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings

if not settings.DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is missing.")

engine = create_engine(settings.DATABASE_URL, echo=False)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Read-only engine: uses a dedicated DB user if READONLY_DATABASE_URL is set,
# otherwise falls back to the main URL (SQL validation still enforces SELECT-only).
_readonly_url = settings.READONLY_DATABASE_URL or settings.DATABASE_URL
readonly_engine = create_engine(
    _readonly_url,
    echo=False,
    execution_options={"no_parameters_on_text_clause": True},
)
ReadonlySessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=readonly_engine
)


def get_db() -> Generator[Session, None, None]:
    """Yield a read-write database session with explicit rollback on error."""
    db: Session = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


@contextmanager
def get_readonly_session() -> Generator[Session, None, None]:
    """Context manager yielding a read-only database session."""
    db: Session = ReadonlySessionLocal()
    try:
        yield db
    finally:
        db.close()
