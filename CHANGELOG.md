# Changelog

All notable changes to this project will be documented here.

## [Unreleased]

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