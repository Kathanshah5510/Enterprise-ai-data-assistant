from __future__ import annotations

import time
import uuid
from datetime import date, datetime
from decimal import Decimal
from typing import Any

from sqlalchemy import text
from sqlalchemy.exc import OperationalError, ProgrammingError

from app.core.config import settings
from app.database.connection import get_readonly_session


def _to_json_safe(value: Any) -> Any:
    if isinstance(value, Decimal):
        return float(value)
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    if isinstance(value, uuid.UUID):
        return str(value)
    return value


def execute_query(sql: str) -> tuple[list[dict[str, Any]], int]:
    """
    Execute a validated SELECT query on the read-only connection.

    Returns (rows, execution_time_ms).
    Raises RuntimeError for DB-level errors (timeout, syntax, missing column).
    """
    with get_readonly_session() as db:
        try:
            timeout_ms = settings.SQL_TIMEOUT_SECONDS * 1000
            db.execute(text(f"SET LOCAL statement_timeout = {int(timeout_ms)}"))

            start = time.perf_counter()
            result = db.execute(text(sql))
            rows = result.fetchmany(settings.SQL_ROW_LIMIT)
            elapsed_ms = int((time.perf_counter() - start) * 1000)

            keys = list(result.keys())
            serialized = [
                {k: _to_json_safe(v) for k, v in zip(keys, row)} for row in rows
            ]
            return serialized, elapsed_ms

        except OperationalError as exc:
            raise RuntimeError(
                f"Query failed (timeout or connection error): {exc.orig}"
            ) from exc
        except ProgrammingError as exc:
            raise RuntimeError(f"Query error: {exc.orig}") from exc
        except Exception as exc:
            raise RuntimeError(f"Unexpected execution error: {exc}") from exc
