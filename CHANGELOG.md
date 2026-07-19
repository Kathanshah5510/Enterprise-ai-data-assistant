# Changelog

All notable changes to this project will be documented here.

## [Unreleased]

### Added — AI Layer & Conversation System (Phases 7–8)
- `app/core/config.py`: added `READONLY_DATABASE_URL`, `SQL_TIMEOUT_SECONDS`, `SQL_ROW_LIMIT`, `FAISS_INDEX_PATH`, `CONVERSATION_HISTORY_LIMIT`
- `app/database/connection.py`: added `readonly_engine`, `ReadonlySessionLocal`, `get_readonly_session()` context manager
- `app/services/schema_service.py`: introspects DB schema into per-table text documents for LLM context
- `app/services/sql_validator.py`: validates generated SQL is a safe single SELECT (rejects DDL, DML, dangerous functions)
- `app/services/sql_executor.py`: executes SELECT queries on read-only connection with configurable timeout and row limit
- `app/services/llm_service.py`: Gemini 2.5 Flash wrappers — `generate_sql()` (NL→SQL) and `suggest_chart()` (result→chart type)
- `app/rag/embeddings.py`: FAISS index over schema documents; auto-builds on first use, persists to `embeddings/schema_index`
- `app/agents/query_agent.py`: LangGraph `StateGraph` — nodes: retrieve_schema → generate_sql → validate_sql → execute_sql → suggest_chart; conditional routing on validation failure and execution error
- `app/models/conversation.py`: Conversation model (user_id FK, title, is_active, messages relationship)
- `app/models/message.py`: Message model (conversation_id FK, role, content, sql_query, result_data JSON, row_count, execution_time_ms, error, chart_suggestion)
- `app/models/audit_log.py`: AuditLog model (user_id FK, conversation_id FK, action, sql_query, status, error_message, execution_time_ms)
- `app/schemas/query.py`: `QueryRequest` (question, optional conversation_id), `QueryResponse`
- `app/schemas/conversation.py`: `ConversationCreate`, `ConversationResponse`, `MessageResponse`, `ConversationDetailResponse`
- `app/api/v1/query.py`: `POST /api/v1/query/` — runs LangGraph agent, persists messages, writes audit log
- `app/api/v1/conversations.py`: GET list, POST create, GET detail (with messages), DELETE (soft)
- `alembic/versions/e570d3e819ea_*`: migration creating `conversations`, `messages`, `audit_logs` tables
- `scripts/build_embeddings.py`: CLI to pre-build FAISS schema index
- `requirements.txt`: rewritten as UTF-8; added langchain, langchain-google-genai, langchain-community, langgraph, faiss-cpu; removed unused passlib

### Added — JWT Authentication, RBAC & CRUD APIs (Phases 4–6)
- `app/core/security.py`: `hash_password`, `verify_password` (direct `bcrypt`), `create_access_token`, `create_refresh_token`, `decode_token` (JWT via `python-jose`)
- `app/schemas/auth.py`: `LoginRequest`, `RefreshRequest`, `TokenResponse`, `RoleOut`, `UserResponse`
- `app/api/auth.py`: `POST /auth/login`, `POST /auth/refresh`, `GET /auth/me`
- `app/api/deps.py`: `get_current_user` (JWT decode + DB load with `joinedload`), `require_role(*roles)` factory (403 on role mismatch)
- `app/api/v1/departments.py`: full CRUD; GET open to all authenticated; POST/PUT/DELETE admin-only; 409 on duplicate code
- `app/api/v1/employees.py`: GET list admin/manager/hr/finance; GET single all authenticated; POST/PUT admin/hr; DELETE admin
- `app/api/v1/projects.py`: GET all authenticated; POST/PUT admin/manager; DELETE admin
- `app/api/v1/budgets.py`: GET/PUT admin/finance/manager; POST admin/finance; `is_over_budget` computed field on `BudgetResponse`
- `app/schemas/department.py`, `employee.py`, `project.py`, `budget.py`: Pydantic v2 schemas with `from_attributes=True`
- `app/main.py`: all routers registered under `/api/v1`
- `scripts/rehash_users.py`: one-time migration of seed user passwords from SHA-256 to bcrypt

### Added
- Initial Alembic migration (`512620fe3142`) creating all foundation tables: `roles`, `departments`, `employees`, `users`
- All primary key constraints (UUID), foreign key constraints, unique indexes, and non-unique indexes applied
- `alembic_version` table tracking migration state at `head`

### Added — Business Models
- `app/models/project.py`: Project model (name, status, start/end dates, department FK)
- `app/models/budget.py`: Budget model (total_amount, spent_amount, fiscal_year; one-per-project via unique FK)
- `app/models/project_assignment.py`: ProjectAssignment model (project FK, employee FK, role; composite unique constraint)
- Migration `53347362076e`: creates `projects`, `budgets`, `project_assignments` tables with all indexes and constraints
- `Department.projects` and `Employee.project_assignments` back-references added
- Seed extended: 10 projects, 10 budgets (2 over-budget), 39 cross-department assignments
- `scripts/seed.py` updated with separate idempotency guard for project data

### Added — Seed Data
- `scripts/seed.py`: idempotent seed script for NovaTech Solutions demo data
- 5 roles: admin, manager, hr, finance, employee
- 7 departments: Engineering, Finance, HR, Marketing, Sales, Operations, Customer Support
- 38 employees across all departments with realistic salaries, hire dates, and manager hierarchy
- 9 application users covering all 5 roles
- Employment type variety: FULL_TIME (36), CONTRACT (1), PART_TIME (1)
- Status variety: ACTIVE (37), INACTIVE (1) for realistic AI query results