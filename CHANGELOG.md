# Changelog

All notable changes to this project will be documented here.

## [Unreleased]

### Added
- Initial Alembic migration (`512620fe3142`) creating all foundation tables: `roles`, `departments`, `employees`, `users`
- All primary key constraints (UUID), foreign key constraints, unique indexes, and non-unique indexes applied
- `alembic_version` table tracking migration state at `head`

### Added — Seed Data
- `scripts/seed.py`: idempotent seed script for NovaTech Solutions demo data
- 5 roles: admin, manager, hr, finance, employee
- 7 departments: Engineering, Finance, HR, Marketing, Sales, Operations, Customer Support
- 38 employees across all departments with realistic salaries, hire dates, and manager hierarchy
- 9 application users covering all 5 roles
- Employment type variety: FULL_TIME (36), CONTRACT (1), PART_TIME (1)
- Status variety: ACTIVE (37), INACTIVE (1) for realistic AI query results