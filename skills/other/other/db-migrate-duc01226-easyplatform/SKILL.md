---
name: db-migrate
version: 1.0.0
description: '[DevOps] Run or create database migrations'
activation: user-invoked
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI may ask user whether to skip.

**Prerequisites:** **MUST READ** before executing:

- `.claude/skills/shared/understand-code-first-protocol.md`
- `.claude/skills/shared/evidence-based-reasoning-protocol.md`

## Quick Summary

**Goal:** Create or run database migrations (EF Core migrations, MongoDB data migrations) following platform patterns.

**Workflow:**
1. **Identify** — Determine migration type (EF schema vs data migration)
2. **Create** — Generate migration using `dotnet ef` or `PlatformDataMigrationExecutor`
3. **Verify** — Run migration and confirm schema/data changes

**Key Rules:**
- Follow platform migration patterns from CLAUDE.md
- Always backup data before destructive migrations
- Use `PlatformDataMigrationExecutor` for MongoDB data migrations

Database migration: $ARGUMENTS

## Instructions

1. **Parse arguments**:
    - `add <name>` → Create new EF Core migration
    - `update` → Apply pending migrations
    - `list` → List all migrations and status
    - `rollback` → Revert last migration
    - No argument → Show migration status

2. **Identify database provider** from project:
    - SQL Server: Search for `*.Persistence` projects
    - PostgreSQL: Search for `*.Persistence.PostgreSql` projects
    - MongoDB: Uses `PlatformMongoMigrationExecutor` (code-based)

3. **For EF Core (SQL Server/PostgreSQL)**:

    Add migration:

    ```bash
    cd src/PlatformExampleApp/PlatformExampleApp.TextSnippet.Persistence
    dotnet ef migrations add <MigrationName> --startup-project ../PlatformExampleApp.TextSnippet.Api
    ```

    Update database:

    ```bash
    dotnet ef database update --startup-project ../PlatformExampleApp.TextSnippet.Api
    ```

    List migrations:

    ```bash
    dotnet ef migrations list --startup-project ../PlatformExampleApp.TextSnippet.Api
    ```

4. **For MongoDB migrations**:
    - MongoDB uses code-based migrations via `PlatformMongoMigrationExecutor`
    - Location: `*.Persistence.Mongo/Migrations/`
    - Migrations run automatically on application startup
    - To create: Generate new migration class following existing patterns

5. **Safety checks**:
    - Warn before applying migrations to production
    - Show what changes will be applied
    - Recommend backup before destructive operations

---

**IMPORTANT Task Planning Notes (MUST FOLLOW)**

- Always plan and break work into many small todo tasks
- Always add a final review todo task to verify work quality and identify fixes/enhancements
