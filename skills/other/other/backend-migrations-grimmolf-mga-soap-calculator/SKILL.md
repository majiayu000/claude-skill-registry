---
name: Backend Migrations
description: Create and manage database schema changes through versioned migration files with proper rollback support, zero-downtime deployment considerations, and backwards compatibility. Use this skill when creating migration files, modifying database schemas, adding/removing tables or columns, creating indexes, or working in migration directories. Applies to files like migrations/, alembic/, db/migrate/, schema changes, or any database evolution task requiring versioned, reversible changes that maintain data integrity during deployments.
---

# Backend Migrations

## When to use this skill

- When creating migration files in directories like `migrations/`, `alembic/versions/`, `db/migrate/`, or `prisma/migrations/`
- When modifying database schemas by adding, removing, or altering tables, columns, or constraints
- When creating or dropping database indexes, especially on large tables requiring concurrent operations
- When writing migration scripts with both upgrade (`up`) and rollback (`down`) methods
- When planning zero-downtime deployments that require backwards-compatible schema changes
- When separating schema migrations from data migrations for safer rollback capabilities
- When implementing multi-step migrations for high-availability systems (add column, backfill, add constraint)
- When naming migration files with descriptive timestamps like `20240115_add_user_email_index.py`
- When working on database version control and ensuring migrations are committed to source control
- When troubleshooting migration conflicts or planning migration strategies for production deployments

# Backend Migrations

This Skill provides Claude Code with specific guidance on how to adhere to coding standards as they relate to how it should handle backend migrations.

## Instructions

For details, refer to the information provided in this file:
[backend migrations](../../../agent-os/standards/backend/migrations.md)
