---
name: portable-schema-generator
description: "Emit Postgres.sql and SQLite.sql from a single schema spec so tools work across both drivers without duplicating DDL by hand. Use when designing a schema that needs to support both shared Postgres deployments and zero-config SQLite. Reduces two-file sync burden to a single source edit."
format: 2025-10-02
version: 1.0.0
status: active
updated: 2026-04-17
---

# Portable Schema Generator

Two-driver schemas mean two migration files. Hand-keeping them in sync
drifts fast. This skill captures the translation rules and the minimal
tooling that keeps them aligned.

## When to Use

- Your tool needs to work on **both** Postgres and SQLite
- You want fresh-project onboarding to be zero-config (SQLite default)
  while shared-infra deployments keep Postgres
- A single schema change should land in both driver files with no manual
  diff-copying

## Core Differences

| Concern | Postgres | SQLite |
|---------|----------|--------|
| Schemas | `CREATE SCHEMA foo; SET search_path TO foo` | Namespace-flat — prefix names instead |
| Autoincrement | `BIGSERIAL PRIMARY KEY` | `INTEGER PRIMARY KEY AUTOINCREMENT` |
| Timestamps | `TIMESTAMPTZ DEFAULT now()` | `TEXT DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now'))` |
| Booleans | `BOOLEAN` | `INTEGER` (0/1) |
| Enums via CHECK | `CHECK (col IN ('a','b'))` | Same — both support inline CHECK |
| Foreign keys | On by default | `PRAGMA foreign_keys = ON` required at connect |
| Updated-at trigger | `CREATE TRIGGER ... EXECUTE FUNCTION touch_updated_at()` | `CREATE TRIGGER ... BEGIN UPDATE ... END` |
| Cascading drops | `ON DELETE CASCADE` | Same, but only enforced with `foreign_keys = ON` |
| Reserved-word casing | Case-insensitive | Case-insensitive, but be consistent |

## Translation Rules

When authoring the Postgres version first:

1. **Strip schema prefix** for SQLite — `CREATE SCHEMA IF NOT EXISTS foo;`
   and `SET search_path` are removed. Keep bare table names.
2. **Replace `BIGSERIAL`** with `INTEGER PRIMARY KEY AUTOINCREMENT`.
3. **Replace `TIMESTAMPTZ`** with `TEXT`; default becomes
   `(strftime('%Y-%m-%dT%H:%M:%fZ','now'))`.
4. **Replace `BOOLEAN`** with `INTEGER` (values 0/1 at insert time — use an
   adapter coercion).
5. **Drop `RESTART IDENTITY`** on truncates (SQLite uses
   `DELETE FROM sqlite_sequence WHERE name = 'table'` instead).
6. **Rewrite function-style triggers** to inline `BEGIN ... END` trigger
   bodies.

## File Layout

```
migrations/<feature>/
  001-init.postgres.sql
  001-init.sqlite.sql
  002-next.postgres.sql
  002-next.sqlite.sql
```

Numbered pairs. The adapter picks the right one based on `cfg.db.driver`.

## Adapter Runtime Responsibilities

The query adapter at runtime should:

- Rewrite `$N` placeholders → `?` for SQLite
- Strip `release_history.` schema prefix for SQLite
- Translate `now()` → `strftime(...)`, `::type` casts → drop
- Coerce JS booleans → 0/1 on param bindings
- Provide a portable `truncate(table)` helper

Reference implementation: `tools/release-history/db.mjs` in this repo.

## Workflow

1. Author the Postgres version first (richer type system reduces ambiguity).
2. Translate row-by-row using the rules above into the SQLite version.
3. Test both: apply each migration to a disposable DB, run schema-check
   script against the adapter.
4. Commit both files together; never commit one without the other.

## Anti-patterns to avoid

- Single mixed-syntax file — both drivers will try to parse it and one or
  both will fail.
- Runtime translation of whole migration files — too many edge cases.
- Letting the Postgres file diverge "just for now" — alignment rots quickly.

## Example (from this repo)

See `migrations/release-history/001-init.postgres.sql` and
`migrations/release-history/001-init.sqlite.sql`. Six tables (release,
feature, metric, retrospective, lesson, publish_target). Same semantics,
driver-idiomatic DDL.

## Related

- `env-setup` — database credentials and `.env` conventions
- `file-operation-patterns` — migration file naming discipline
