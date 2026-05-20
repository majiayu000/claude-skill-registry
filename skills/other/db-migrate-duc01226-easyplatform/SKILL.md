---
name: db-migrate
version: 1.0.0
description: '[DevOps] Run or create database migrations'
disable-model-invocation: false
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI MUST ask user whether to skip.

**Prerequisites:** **MUST READ** before executing:

- `.claude/skills/shared/understand-code-first-protocol.md`
- `.claude/skills/shared/evidence-based-reasoning-protocol.md`
- `docs/project-reference/domain-entities-reference.md` — Domain entity catalog, relationships, cross-service sync (read when task involves business entities/models)

## Quick Summary

**Goal:** Create or run database migrations (EF Core migrations, MongoDB data migrations) following platform patterns.

**Workflow:**

1. **Identify** — Determine migration type (EF schema vs data migration)
2. **Create** — Generate migration using `dotnet ef` or project data migration executor (see docs/project-reference/backend-patterns-reference.md)
3. **Verify** — Run migration and confirm schema/data changes

**Key Rules:**

- Follow platform migration patterns from CLAUDE.md
- Always backup data before destructive migrations
- Use project data migration executor for MongoDB data migrations (see docs/project-reference/backend-patterns-reference.md)

**Be skeptical. Apply critical thinking, sequential thinking. Every claim needs traced proof, confidence percentages (Idea should be more than 80%).**

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
    - MongoDB: Uses project Mongo migration executor (code-based, see docs/project-reference/backend-patterns-reference.md)

3. **For EF Core (SQL Server/PostgreSQL)**:

    Add migration:

    ```bash
    cd src/{ExampleApp}/{ExampleApp}.TextSnippet.Persistence
    dotnet ef migrations add <MigrationName> --startup-project ../{ExampleApp}.TextSnippet.Api
    ```

    Update database:

    ```bash
    dotnet ef database update --startup-project ../{ExampleApp}.TextSnippet.Api
    ```

    List migrations:

    ```bash
    dotnet ef migrations list --startup-project ../{ExampleApp}.TextSnippet.Api
    ```

4. **For MongoDB migrations**:
    - MongoDB uses code-based migrations via project Mongo migration executor (see docs/project-reference/backend-patterns-reference.md)
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
