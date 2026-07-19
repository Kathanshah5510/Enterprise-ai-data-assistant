from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.agents.query_agent import query_agent, AgentState
from app.api.deps import get_current_user
from app.database.connection import get_db
from app.models import User
from app.models.audit_log import AuditLog
from app.models.conversation import Conversation
from app.models.message import Message
from app.schemas.query import QueryRequest, QueryResponse

router = APIRouter(prefix="/query", tags=["AI Query"])


def _build_history(messages: list[Message]) -> str:
    """Format recent conversation messages as context for the LLM."""
    if not messages:
        return ""
    lines: list[str] = []
    for msg in messages:
        if msg.role == "user":
            lines.append(f"User: {msg.content}")
        else:
            lines.append(f"Assistant SQL: {msg.sql_query or '(error)'}")
    return "\n".join(lines)


def _get_or_create_conversation(
    db: Session,
    user: User,
    conversation_id: uuid.UUID | None,
    question: str,
) -> Conversation:
    if conversation_id:
        conv = (
            db.query(Conversation)
            .filter(
                Conversation.id == conversation_id,
                Conversation.user_id == user.id,
                Conversation.is_active == True,
            )
            .first()
        )
        if not conv:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found",
            )
        return conv

    # Auto-create: title is first 80 chars of question
    title = question[:80] + ("…" if len(question) > 80 else "")
    conv = Conversation(user_id=user.id, title=title)
    db.add(conv)
    db.flush()  # get conv.id before we need it in messages
    return conv


@router.post("/", response_model=QueryResponse, status_code=status.HTTP_200_OK)
def run_query(
    body: QueryRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> QueryResponse:
    """
    Convert a natural language question into SQL, execute it, and return results.
    Persists the exchange to the conversation and writes an audit log entry.
    """
    conv = _get_or_create_conversation(
        db, current_user, body.conversation_id, body.question
    )

    # Load conversation history for multi-turn context
    from app.core.config import settings as cfg
    recent = (
        db.query(Message)
        .filter(Message.conversation_id == conv.id)
        .order_by(Message.created_at.desc())
        .limit(cfg.CONVERSATION_HISTORY_LIMIT)
        .all()
    )
    history = _build_history(list(reversed(recent)))

    # ── Run LangGraph agent ───────────────────────────────────────────────────
    initial_state: AgentState = {
        "question": body.question,
        "history": history,
        "schema_context": "",
        "sql_query": "",
        "sql_valid": False,
        "validation_error": "",
        "results": [],
        "row_count": 0,
        "execution_time_ms": 0,
        "error": "",
        "chart_suggestion": "none",
    }

    try:
        final_state: AgentState = query_agent.invoke(initial_state)
    except Exception as exc:
        # Catch LLM / embedding failures (e.g. missing API key)
        final_state = {**initial_state, "error": str(exc)}

    # ── Persist user message ──────────────────────────────────────────────────
    user_msg = Message(
        conversation_id=conv.id,
        role="user",
        content=body.question,
    )
    db.add(user_msg)

    # ── Persist assistant message ─────────────────────────────────────────────
    result_payload: dict | None = (
        {"rows": final_state["results"]} if final_state["results"] else None
    )
    assistant_msg = Message(
        conversation_id=conv.id,
        role="assistant",
        content=body.question,  # echoed — frontend uses sql_query + result_data
        sql_query=final_state.get("sql_query") or None,
        result_data=result_payload,
        row_count=final_state.get("row_count") or 0,
        execution_time_ms=final_state.get("execution_time_ms") or 0,
        error=final_state.get("error") or None,
        chart_suggestion=final_state.get("chart_suggestion") or "none",
    )
    db.add(assistant_msg)

    # ── Audit log ─────────────────────────────────────────────────────────────
    has_error = bool(final_state.get("error"))
    action = "query_blocked" if final_state.get("validation_error") else (
        "query_failed" if has_error else "query_executed"
    )
    audit = AuditLog(
        user_id=current_user.id,
        conversation_id=conv.id,
        action=action,
        sql_query=final_state.get("sql_query") or None,
        status="error" if has_error else "success",
        error_message=final_state.get("error") or None,
        execution_time_ms=final_state.get("execution_time_ms") or None,
    )
    db.add(audit)
    db.commit()

    return QueryResponse(
        question=body.question,
        sql_query=final_state.get("sql_query") or "",
        results=final_state.get("results") or [],
        row_count=final_state.get("row_count") or 0,
        execution_time_ms=final_state.get("execution_time_ms") or 0,
        chart_suggestion=final_state.get("chart_suggestion") or "none",
        conversation_id=conv.id,
        message_id=assistant_msg.id,
        error=final_state.get("error") or None,
    )
