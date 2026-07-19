#!/bin/bash
set -e

echo "Running database migrations..."
alembic upgrade head

echo "Building FAISS schema index..."
python scripts/build_embeddings.py

echo "Starting server..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
