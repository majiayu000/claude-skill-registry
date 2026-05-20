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
