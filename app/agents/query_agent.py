from __future__ import annotations

from typing import Any, TypedDict

from langgraph.graph import END, StateGraph

from app.rag.embeddings import search_schema
from app.services.llm_service import generate_sql, suggest_chart
from app.services.sql_executor import execute_query
from app.services.sql_validator import validate_sql


class AgentState(TypedDict):
    question: str
    history: str          # formatted prior conversation turns
    schema_context: str
    sql_query: str
    sql_valid: bool
    validation_error: str
    results: list[dict[str, Any]]
    row_count: int
    execution_time_ms: int
    error: str
    chart_suggestion: str


# ── Nodes ────────────────────────────────────────────────────────────────────

def _retrieve_schema(state: AgentState) -> AgentState:
    context = search_schema(state["question"])
    return {**state, "schema_context": context}


def _generate_sql(state: AgentState) -> AgentState:
    sql = generate_sql(
        question=state["question"],
        schema_context=state["schema_context"],
        history=state.get("history", ""),
    )
    return {**state, "sql_query": sql}


def _validate_sql(state: AgentState) -> AgentState:
    valid, error = validate_sql(state["sql_query"])
    return {**state, "sql_valid": valid, "validation_error": error or ""}


def _execute_sql(state: AgentState) -> AgentState:
    try:
        rows, elapsed = execute_query(state["sql_query"])
        return {
            **state,
            "results": rows,
            "row_count": len(rows),
            "execution_time_ms": elapsed,
            "error": "",
        }
    except RuntimeError as exc:
        return {
            **state,
            "results": [],
            "row_count": 0,
            "execution_time_ms": 0,
            "error": str(exc),
        }


def _suggest_chart(state: AgentState) -> AgentState:
    if state.get("error") or not state.get("results"):
        return {**state, "chart_suggestion": "none"}
    columns = list(state["results"][0].keys())
    chart = suggest_chart(state["sql_query"], columns, state["row_count"])
    return {**state, "chart_suggestion": chart}


# ── Routing ───────────────────────────────────────────────────────────────────

def _route_after_validation(state: AgentState) -> str:
    return "execute_sql" if state["sql_valid"] else END


def _route_after_execution(state: AgentState) -> str:
    return "suggest_chart" if not state.get("error") else END


# ── Graph ─────────────────────────────────────────────────────────────────────

def _build_agent() -> Any:
    graph: StateGraph = StateGraph(AgentState)

    graph.add_node("retrieve_schema", _retrieve_schema)
    graph.add_node("generate_sql", _generate_sql)
    graph.add_node("validate_sql", _validate_sql)
    graph.add_node("execute_sql", _execute_sql)
    graph.add_node("suggest_chart", _suggest_chart)

    graph.set_entry_point("retrieve_schema")
    graph.add_edge("retrieve_schema", "generate_sql")
    graph.add_edge("generate_sql", "validate_sql")
    graph.add_conditional_edges("validate_sql", _route_after_validation)
    graph.add_conditional_edges("execute_sql", _route_after_execution)
    graph.add_edge("suggest_chart", END)

    return graph.compile()


query_agent = _build_agent()
