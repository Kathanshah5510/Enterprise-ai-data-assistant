from __future__ import annotations

from langchain_google_genai import ChatGoogleGenerativeAI

from app.core.config import settings

_llm: ChatGoogleGenerativeAI | None = None

_SQL_PROMPT = """\
You are an expert PostgreSQL query writer for an enterprise HR and project management system called NovaTech Solutions.

Relevant database schema:
{schema_context}

Conversation history (most recent last):
{history}

User question: {question}

Rules:
- Write a single valid PostgreSQL SELECT statement only
- Use only the tables and columns listed in the schema above
- Never use INSERT, UPDATE, DELETE, DROP, CREATE, ALTER, or TRUNCATE
- Use table aliases for readability
- Use explicit JOIN syntax (not implicit comma joins)
- Handle NULL values appropriately with COALESCE or IS NULL checks
- Output ONLY the raw SQL — no explanation, no markdown, no ```sql fences

SQL:"""

_CHART_PROMPT = """\
Given this SQL query and result metadata, choose the best chart type for visualization.

SQL: {sql}
Result columns: {columns}
Row count: {row_count}

Choose exactly one:
- bar   → comparisons between named categories (e.g. avg salary per department)
- line  → values over time (e.g. monthly hires)
- pie   → proportions of a whole, max 8 categories
- table → multiple columns or complex/mixed data
- none  → single scalar value

Respond with ONLY one word (bar, line, pie, table, or none).

Chart type:"""


def _get_llm() -> ChatGoogleGenerativeAI:
    global _llm
    if _llm is None:
        if not settings.GEMINI_API_KEY:
            raise RuntimeError(
                "GEMINI_API_KEY is not configured. "
                "Set it in your .env file to enable AI features."
            )
        _llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=settings.GEMINI_API_KEY,
            temperature=0,
        )
    return _llm


def generate_sql(question: str, schema_context: str, history: str = "") -> str:
    """Call Gemini to generate a SQL query for the given question."""
    llm = _get_llm()
    prompt = _SQL_PROMPT.format(
        schema_context=schema_context,
        history=history or "No prior conversation.",
        question=question,
    )
    response = llm.invoke(prompt)
    sql: str = response.content.strip()

    # Strip accidental markdown code fences
    if sql.startswith("```"):
        lines = sql.splitlines()
        sql = "\n".join(
            line for line in lines if not line.startswith("```")
        ).strip()

    return sql


def suggest_chart(sql: str, columns: list[str], row_count: int) -> str:
    """Ask Gemini to suggest the best chart type for the query result."""
    llm = _get_llm()
    prompt = _CHART_PROMPT.format(
        sql=sql, columns=", ".join(columns), row_count=row_count
    )
    response = llm.invoke(prompt)
    raw = response.content.strip().lower().split()[0]
    valid = {"bar", "line", "pie", "table", "none"}
    return raw if raw in valid else "table"
