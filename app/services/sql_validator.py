from __future__ import annotations

import re

_FORBIDDEN = re.compile(
    r"\b(INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|TRUNCATE|REPLACE|MERGE"
    r"|EXEC|EXECUTE|GRANT|REVOKE|COPY|VACUUM|ANALYZE|LOCK|COMMENT)\b",
    re.IGNORECASE,
)

_DANGEROUS_FUNCS = re.compile(
    r"\b(pg_read_file|pg_ls_dir|pg_stat_file|lo_import|lo_export"
    r"|pg_sleep|dblink|pg_cancel_backend|pg_terminate_backend)\b",
    re.IGNORECASE,
)


def validate_sql(sql: str) -> tuple[bool, str]:
    """
    Validate that sql is a safe, single SELECT statement.
    Returns (is_valid, error_message). error_message is empty string when valid.
    """
    stripped = sql.strip().rstrip(";")

    if not stripped:
        return False, "Empty SQL query."

    first_word = stripped.split()[0].upper()
    if first_word not in ("SELECT", "WITH"):
        return False, f"Only SELECT queries are allowed. Got: {first_word}"

    match = _FORBIDDEN.search(stripped)
    if match:
        return False, f"Forbidden keyword detected: {match.group().upper()}"

    match = _DANGEROUS_FUNCS.search(stripped)
    if match:
        return False, f"Dangerous function detected: {match.group()}"

    # Reject multiple statements (semicolon mid-query)
    if ";" in stripped:
        return False, "Multiple SQL statements are not allowed."

    return True, ""
