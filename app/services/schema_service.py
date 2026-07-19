from __future__ import annotations

from sqlalchemy import inspect

from app.database.connection import engine

# Tables managed by Alembic / internal — excluded from schema context
_EXCLUDE = {"alembic_version", "audit_logs"}


def get_schema_documents() -> list[str]:
    """Return one text document per table, describing columns and FK relationships."""
    inspector = inspect(engine)
    docs: list[str] = []

    for table_name in sorted(inspector.get_table_names(schema="public")):
        if table_name in _EXCLUDE:
            continue

        columns = inspector.get_columns(table_name)
        pk_cols: set[str] = set(
            inspector.get_pk_constraint(table_name).get("constrained_columns", [])
        )
        fks = inspector.get_foreign_keys(table_name)
        indexes = inspector.get_indexes(table_name)

        col_lines: list[str] = []
        for col in columns:
            type_str = str(col["type"])
            flags: list[str] = []
            if col["name"] in pk_cols:
                flags.append("PK")
            if not col.get("nullable", True):
                flags.append("NOT NULL")
            flag_str = f"  [{', '.join(flags)}]" if flags else ""
            col_lines.append(f"  {col['name']} {type_str}{flag_str}")

        fk_lines: list[str] = [
            f"  {', '.join(fk['constrained_columns'])} → "
            f"{fk['referred_table']}({', '.join(fk['referred_columns'])})"
            for fk in fks
        ]

        idx_lines: list[str] = [
            f"  INDEX on ({', '.join(idx['column_names'])})"
            for idx in indexes
            if not idx.get("unique")
        ]

        parts = [f"Table: {table_name}", "Columns:"] + col_lines
        if fk_lines:
            parts += ["Foreign Keys:"] + fk_lines
        if idx_lines:
            parts += ["Indexes:"] + idx_lines

        docs.append("\n".join(parts))

    return docs


def get_full_schema_context() -> str:
    """Return all schema documents as a single formatted string."""
    return "\n\n---\n\n".join(get_schema_documents())
