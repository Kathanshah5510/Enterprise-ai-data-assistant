# Enterprise AI Data Assistant

An enterprise-grade AI-powered data assistant that enables employees to query organisational databases using natural language, while enforcing strict Role-Based Access Control (RBAC).

## Features

- **Natural Language to SQL** — Gemini 2.5 Flash converts plain English questions into safe PostgreSQL queries
- **LangGraph Agent Workflow** — multi-step pipeline: schema retrieval → SQL generation → validation → execution → chart suggestion
- **Schema RAG** — FAISS vector index over the live DB schema keeps the LLM grounded in the actual tables and columns
- **SQL Safety Guardrails** — SELECT-only enforcement; DDL, DML, and dangerous functions are blocked
- **JWT Authentication** — access + refresh token flow
- **Role-Based Access Control** — five roles (admin, manager, hr, finance, employee) with per-endpoint enforcement
- **Conversation Memory** — multi-turn context persisted in PostgreSQL
- **Query History & Audit Logging** — every query, result, and outcome is recorded
- **Automatic Data Visualisation** — bar, line, pie charts or table auto-selected by the LLM
- **React Frontend** — Chat, Dashboard, History pages with Recharts visualisations
- **Docker & Kubernetes** — ready-to-deploy container stack and K8s manifests

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.11, FastAPI, SQLAlchemy 2.0, Alembic |
| Database | PostgreSQL 16 |
| AI / LLM | Google Gemini 2.5 Flash, LangChain, LangGraph |
| Embeddings | FAISS, `langchain-google-genai` |
| Auth | JWT (`python-jose`), bcrypt |
| Frontend | React 18, TypeScript, Vite, TailwindCSS, Recharts |
| Deployment | Docker, Docker Compose, Kubernetes |

## Project Structure

```
app/
├── agents/          # LangGraph query agent
├── api/             # FastAPI routers (auth, health, v1/*)
├── core/            # Config, security helpers
├── database/        # SQLAlchemy engine and session factory
├── models/          # ORM models
├── rag/             # FAISS index build and search
├── schemas/         # Pydantic request/response schemas
└── services/        # LLM, SQL validator, SQL executor, schema introspection

frontend/            # React + TypeScript + Vite SPA
k8s/                 # Kubernetes manifests
scripts/             # Seed data, build embeddings, rehash passwords
alembic/             # Database migrations
docs/                # Architecture, blueprint, status
```

## Quick Start (Local)

### Prerequisites
- Python 3.11
- Node.js 20
- PostgreSQL 16 running locally
- Google Gemini API key (from [aistudio.google.com](https://aistudio.google.com))

### Backend

```bash
# Create and activate virtual environment
python -m venv eaida_venv
source eaida_venv/bin/activate        # macOS/Linux
.\eaida_venv\Scripts\activate         # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your DATABASE_URL, SECRET_KEY, and GEMINI_API_KEY

# Run migrations
alembic upgrade head

# Seed demo data
python scripts/seed.py

# Build FAISS schema index
python scripts/build_embeddings.py

# Start server
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
# Open http://localhost:5173
```

### Demo Credentials

| Username | Password | Role |
|---|---|---|
| `admin` | `NovaTech@2024` | Admin — full access |
| `alice.johnson` | `NovaTech@2024` | Manager |
| `james.anderson` | `NovaTech@2024` | Finance |
| `olivia.lewis` | `NovaTech@2024` | HR |
| `bob.smith` | `NovaTech@2024` | Employee |

## Quick Start (Docker)

```bash
# Copy and fill in secrets
cp .env.example .env.docker
# Edit .env.docker with POSTGRES_PASSWORD, SECRET_KEY, GEMINI_API_KEY

docker compose --env-file .env.docker up --build
# Open http://localhost
```

## API Documentation

Interactive Swagger UI available at `http://localhost:8000/docs` when the server is running.

## Project Status

✅ Complete — all 10 phases implemented and production-ready.
