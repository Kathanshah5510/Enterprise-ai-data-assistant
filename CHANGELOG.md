# Changelog

All notable changes to this project will be documented here.

## [Unreleased]

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