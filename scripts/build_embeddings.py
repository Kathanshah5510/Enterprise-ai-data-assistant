"""
Build (or rebuild) the FAISS schema embedding index.

Run whenever the database schema changes:
    python scripts/build_embeddings.py

Requires GEMINI_API_KEY to be set in .env.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.rag.embeddings import build_index
from app.services.schema_service import get_schema_documents


def main() -> None:
    docs = get_schema_documents()
    print(f"Found {len(docs)} table(s) in schema:")
    for doc in docs:
        first_line = doc.splitlines()[0]
        print(f"  {first_line}")
    print()
    build_index()
    print("Done. Index is ready for queries.")


if __name__ == "__main__":
    main()
