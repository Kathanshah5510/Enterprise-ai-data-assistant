# Changelog

All notable changes to this project will be documented here.

## [Unreleased]

### Added
- Initial Alembic migration (`512620fe3142`) creating all foundation tables: `roles`, `departments`, `employees`, `users`
- All primary key constraints (UUID), foreign key constraints, unique indexes, and non-unique indexes applied
- `alembic_version` table tracking migration state at `head`