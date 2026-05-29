---
name: sqlalchemy-code-review
description: Reviews SQLAlchemy code for session management, relationships, N+1 queries, and migration patterns. Use when reviewing SQLAlchemy 2.0 code, checking session lifecycle, relationship() usage, or Alembic migrations.
---

# SQLAlchemy Code Review

## Quick Reference

| Issue Type | Reference |
|------------|-----------|
| Session lifecycle, context managers, async sessions | [references/sessions.md](references/sessions.md) |
| relationship(), lazy loading, N+1, joinedload | [references/relationships.md](references/relationships.md) |
| select() vs query(), ORM overhead, bulk ops | [references/queries.md](references/queries.md) |
| Alembic patterns, reversible migrations, data migrations | [references/migrations.md](references/migrations.md) |

## Review Checklist

- [ ] Sessions use context managers (`with`, `async with`)
- [ ] No session sharing across requests or threads
- [ ] Sessions closed/cleaned up properly
- [ ] `relationship()` uses appropriate `lazy` strategy
- [ ] Explicit `joinedload`/`selectinload` to avoid N+1
- [ ] No lazy loading in loops (N+1 queries)
- [ ] Using SQLAlchemy 2.0 `select()` syntax, not legacy `query()`
- [ ] Bulk operations use bulk_insert/bulk_update, not ORM loops
- [ ] Async sessions use proper async context managers
- [ ] Migrations are reversible with `downgrade()`
- [ ] Data migrations use `op.execute()` not ORM models
- [ ] Migration dependencies properly ordered

## Gates (SQLAlchemy-specific)

Run **once per SQLAlchemy-related finding**, after you can anchor **`file:line`** (see [review-verification-protocol](../review-verification-protocol/SKILL.md)) and **before** the finding ships. If a step’s pass condition is not met, **do not** assert the finding as written—gather evidence, withdraw, downgrade severity, or rephrase as a question.

### Gate 1 — Session scope and lifecycle

| Step | Action | **Pass condition** |
|------|--------|---------------------|
| 1a | Open the module where the session is created or injected (not from memory). | **`file:line`** for `Session`, `sessionmaker`, `async_session`, or the factory/`Depends()` that yields a session. |
| 1b | If claiming leak, cross-request sharing, or missing cleanup: trace the session’s scope (context manager, `try`/`finally`, middleware). | **Scoped region** cited with a **`file:line` range**, or withdraw if scope is correct after the read. |

### Gate 2 — N+1, lazy loading, eager loads

| Step | Action | **Pass condition** |
|------|--------|---------------------|
| 2a | Identify the loop or repeated call site (ORM attribute access, `execute` in a loop). | **`file:line`** for the loop or hot path. |
| 2b | If claiming N+1: name the relationship or query pattern emitted per iteration. | **Relationship or per-iteration SQL pattern** with **`file:line`**, or rephrase as a question if unclear. |

### Gate 3 — Migrations (Alembic)

| Step | Action | **Pass condition** |
|------|--------|---------------------|
| 3a | Open the revision file (e.g. under `versions/`, or the project’s Alembic layout). | **Repo-relative path** + **`file:line`** for `revision` / `upgrade` / `downgrade`. |
| 3b | If claiming broken `downgrade()` or risky data migration: point at the `op.*` / `op.execute()` involved. | **Snippet or line range** in that file for each claimed op, or withdraw. |

## When to Load References

- Reviewing session creation/cleanup → sessions.md
- Reviewing model relationships → relationships.md
- Reviewing database queries → queries.md
- Reviewing Alembic migration files → migrations.md

## Review Questions

1. Are all sessions properly managed with context managers?
2. Are relationships configured to avoid N+1 queries?
3. Are queries using SQLAlchemy 2.0 `select()` syntax?
4. Are all migrations reversible and properly tested?
