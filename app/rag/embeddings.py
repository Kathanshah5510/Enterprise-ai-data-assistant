from __future__ import annotations

import threading
from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from app.core.config import settings
from app.services.schema_service import get_schema_documents

_INDEX_PATH = Path(settings.FAISS_INDEX_PATH)
_store: FAISS | None = None
_store_lock = threading.Lock()


def _make_embeddings() -> GoogleGenerativeAIEmbeddings:
    if not settings.GEMINI_API_KEY:
        raise RuntimeError(
            "GEMINI_API_KEY is not configured. "
            "Set it in your .env file to enable AI features."
        )
    return GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=settings.GEMINI_API_KEY,
    )


def build_index() -> None:
    """Build FAISS index from current DB schema and persist to disk."""
    docs = get_schema_documents()
    if not docs:
        raise RuntimeError("No schema documents found. Is the database migrated?")
    embeddings = _make_embeddings()
    store = FAISS.from_texts(docs, embeddings)
    _INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
    store.save_local(str(_INDEX_PATH))
    print(f"FAISS index built: {len(docs)} table(s) → {_INDEX_PATH}")


def _load_store() -> FAISS:
    global _store
    if _store is not None:
        return _store

    with _store_lock:
        if _store is not None:
            return _store

        embeddings = _make_embeddings()
        if _INDEX_PATH.exists():
            _store = FAISS.load_local(
                str(_INDEX_PATH),
                embeddings,
                allow_dangerous_deserialization=True,
            )
        else:
            # Auto-build on first use if index is missing
            docs = get_schema_documents()
            _store = FAISS.from_texts(docs, embeddings)
            _INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
            _store.save_local(str(_INDEX_PATH))
            print(f"FAISS index auto-built: {len(docs)} table(s) → {_INDEX_PATH}")

    return _store


def search_schema(query: str, k: int = 5) -> str:
    """Return the top-k schema chunks most semantically relevant to the query."""
    store = _load_store()
    results = store.similarity_search(query, k=k)
    return "\n\n---\n\n".join(doc.page_content for doc in results)
