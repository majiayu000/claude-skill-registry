---
name: pg-doc-schema-review
description: Review and fix PRD/BP/tech design Markdown that includes PostgreSQL table DDL and API examples. Use to enforce these conventions: no auto-increment primary keys, no foreign keys, avoid join-based designs, unique constraints written with UNIQUE (not CREATE UNIQUE INDEX), detailed COMMENTs for tables/columns, and entity/aggregate-root tables include create_time and update_time.
---

# pg-doc-schema-review

Follow this workflow when reviewing or editing PRD/BP Markdown that contains database schema / SQL examples.

## Rules to enforce

### IDs / primary keys

- Prefer **domain-scoped globally unique string IDs** as primary keys (PostgreSQL `TEXT`), with prefix = entity name or abbreviation (e.g., `plan_...`, `sup_...`), unique within the domain.
- Do **not** use auto-increment / identity as the **primary key** (avoid `SERIAL`, `GENERATED ... AS IDENTITY`, `AUTO_INCREMENT`).
- If an auto-increment numeric ID is explicitly required (rare), use `BIGINT` and **do not expose it as the entity’s external identifier**; keep the external identifier as the prefixed string ID.

### Schema design

- Do **not** define foreign keys (`FOREIGN KEY`, `REFERENCES`).
- Avoid designs that require join queries for core read paths (“不要连表查询”): prefer denormalized fields, JSONB snapshots, or read-optimized tables.

### Indexing

- Add indexes for the intended query paths.
- Unique requirements should be expressed using `UNIQUE` (e.g., `email TEXT NOT NULL UNIQUE`, or `CONSTRAINT ux_xxx UNIQUE (...)`), **not** `CREATE UNIQUE INDEX`.

### Comments

- Every table must have `COMMENT ON TABLE ...`.
- Every column must have `COMMENT ON COLUMN ...`.

### Timestamps

- Entity tables / aggregate root tables must include:
  - `create_time TIMESTAMPTZ NOT NULL DEFAULT NOW()`
  - `update_time TIMESTAMPTZ NOT NULL DEFAULT NOW()`
- If the doc claims DB triggers, state it explicitly; otherwise, assume **application-level update of `update_time`**.

## Review checklist (what to look for)

- ID type mismatches between API examples and schema (`*_id` as string vs int).
- Use of `CREATE UNIQUE INDEX` (should be `UNIQUE`).
- Any `FOREIGN KEY` / `REFERENCES` / join-table patterns.
- Missing `create_time`/`update_time` on core tables.
- Missing `COMMENT ON TABLE` / `COMMENT ON COLUMN`.
- SQL dialect mismatch with PostgreSQL (e.g., MySQL-only syntax).

## Tooling (optional)

Run the bundled linter to quickly flag common violations:

- `python .project/ai/dev/DBA/skills/pg-doc-schema-review/scripts/lint_md_schema.py docs/path/or/file.md`

It scans Markdown ` ```sql ` blocks and reports violations and missing comment/index sections.
