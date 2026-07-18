# Enterprise AI Data Assistant

## Project Goal

Build a production-grade Enterprise AI Data Assistant that allows enterprise users to ask natural language questions about company data.

Example:

- Which department has the highest average salary?
- Show employees hired after 2024.
- Which projects are over budget?
- Compare Engineering and Finance expenses.

The assistant should translate natural language into SQL using an LLM, execute the SQL safely, and present the results through a React frontend.

---

# Tech Stack

## Backend

- Python 3.11
- FastAPI
- SQLAlchemy 2.0
- PostgreSQL
- Alembic
- Pydantic
- JWT Authentication

## AI

- Google Gemini
- LangChain
- LangGraph
- RAG
- FAISS (schema/document embeddings)

## Frontend

- React
- TypeScript
- TailwindCSS
- Recharts

## Infrastructure

- Docker
- Docker Compose
- Kubernetes

---

# Current Project Structure

```
Enterprise-ai-data-assistant/

app/
    api/
    core/
    database/
    models/
    services/
    agents/
    rag/
    utils/
    main.py

database/
docker/
docs/
embeddings/
frontend/
kubernetes/
langgraph/
scripts/
tests/

.env
.env.example
README.md
CHANGELOG.md
requirements.txt
```

---

# Architecture Rules

Never change the folder structure.

Never rename existing files.

Never introduce new libraries unless explicitly requested.

Never remove existing functionality.

Never rewrite working code.

Only modify the files necessary for the requested task.

---

# Coding Standards

- Python 3.11
- SQLAlchemy 2.0 style
- Mapped typing
- mapped_column()
- relationship()
- TYPE_CHECKING for circular imports
- PEP8
- Type hints everywhere
- Concise docstrings
- Minimal comments
- Modular code
- One responsibility per file

---

# Database Rules

Use Alembic for every schema change.

Never use Base.metadata.create_all().

Never hardcode database credentials.

Use settings.DATABASE_URL.

UUID primary keys.

Timezone-aware timestamps.

---

# AI Rules

Use LangGraph for orchestration.

Use LangChain integrations where appropriate.

Conversation memory must be persistent.

Schema embeddings must be cached.

Never execute unsafe SQL.

Always validate generated SQL.

---

# Frontend Rules

React + TypeScript only.

TailwindCSS.

Charts via Recharts.

No Streamlit.

---

# Features

Authentication

- JWT
- RBAC

Enterprise Data

- Departments
- Employees
- Projects
- Budgets

AI

- Natural language to SQL
- SQL explanation
- Query history
- Conversation memory
- Audit logging
- Charts
- Execution time metrics

Deployment

- Docker
- Kubernetes

---

# Current Status

Completed:

✅ FastAPI
✅ PostgreSQL
✅ SQLAlchemy
✅ Alembic configuration
✅ Configuration management
✅ Health endpoint
✅ Base ORM model
✅ User model
✅ Role model
✅ Department model
✅ Employee model

In Progress:

- Initial Alembic migration

Upcoming:

- Seed data
- Authentication
- LangChain
- LangGraph
- React frontend

---

# Important Rules

Never expose secrets.

Never expose database exceptions.

Prefer dependency injection.

Prefer composition.

Avoid unnecessary abstraction.

Fail fast.

Follow production best practices.

---

# Working Style

When given a task:

1. Analyze existing code.
2. Minimize changes.
3. Explain assumptions.
4. Explain modified files.
5. Generate production-quality code.
6. Do not modify unrelated code.
7. If the task is ambiguous, ask before implementing.



Review your own implementation.

Check:

- Did you satisfy every requirement?
- Did you modify unnecessary files?
- Did you introduce bugs?
- Did you follow docs/CLAUDE.md?
- Can anything be simplified?

Produce a self-review.

Only then show the code.
