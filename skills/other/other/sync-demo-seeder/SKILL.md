---
name: sync-demo-seeder
description: Synchronizes scripts/seed-demo.sql with the current Drizzle schema and migrations. Use this skill whenever a new migration is added or src/lib/db/schema.ts changes, to keep the demo dataset consistent with the database structure.
---

Synchronize `scripts/seed-demo.sql` with the current database schema after a Drizzle migration or schema change.

## Your Task

When invoked, perform the following steps in order:

### Step 1 — Understand the current state

Read all of the following files completely before making any changes:

1. `src/lib/db/schema.ts` — source of truth for all tables, columns, and enum values
2. Every SQL file in `drizzle/` (sorted by filename, i.e. migration order)
3. `scripts/seed-demo.sql` — the current demo seed that needs updating

### Step 2 — Diff the schema against the seed

Compare the schema to what the seed currently does. Identify every discrepancy:

**Tables:**
- Is every table that holds user data present in the `TRUNCATE` statement?
  - Excluded tables (never seed): `conversations`, `messages`, `documents`
  - The TRUNCATE must list all remaining user-data tables
- Is there a new table that needs demo rows?
- Is a table removed? Remove its TRUNCATE entry and INSERT block.

**Columns:**
- Are the column names in each `INSERT` statement still correct?
  - Column names come from the second argument of each Drizzle column definition, e.g. `uuid('account_id')` → SQL column is `account_id`
  - Never guess — read the schema directly
- Are there new NOT NULL columns without a DEFAULT that are missing from the INSERTs? They must be added with a sensible demo value.
- Are there removed or renamed columns still referenced in the seed? Remove or rename them.

**Enum values:**
- Are any enum values used in the seed that no longer exist in the schema?
- Are there new enum variants that existing demo rows should use?

### Step 3 — Plan the changes

Before editing, write out a concise list of every change you are about to make, grouped by table. For example:
```
accounts       — no changes
expenses       — add new column `budget_id` (nullable, use NULL in all rows)
categories     — enum 'shopping' renamed to 'retail', update 3 rows
budget_groups  — NEW TABLE: add TRUNCATE entry + INSERT block with 2 demo rows
```

If no changes are required, say so explicitly and stop.

### Step 4 — Edit scripts/seed-demo.sql

Apply every planned change to `scripts/seed-demo.sql`. Follow these rules:

**UUID format:** All hardcoded UUIDs must use valid hex characters only (`0-9`, `a-f`).
Use the existing naming convention:
- `a0000000-0000-0000-0000-00000000000N` for accounts
- `b0000000-0000-0000-0000-00000000000N` for incomes
- `c0000000-0000-0000-0000-00000000000N` for categories
- `d0000000-0000-0000-0000-00000000000N` for transfers
- `e0000000-0000-0000-0000-00000000000N` for expenses
- For new tables, pick the next unused letter (`f`, then `0a`, etc.)
- For tables seeded with `gen_random_uuid()` (daily_expenses), keep using it

**Demo data quality:** New demo rows must be realistic and consistent with the existing dataset (German locale, EUR currency, plausible financial amounts and descriptions). Never insert placeholder values like "Test" or "TODO".

**Transaction:** The entire file must remain wrapped in `BEGIN; ... COMMIT;`.

**TRUNCATE:** Keep all truncated tables in a single `TRUNCATE TABLE ... CASCADE;` statement at the top.

**Column order:** Match the column order in each INSERT to what's defined in the schema for readability.

**Comments:** Keep existing section comments (`-- === ACCOUNTS ===` etc.). Add a matching comment for any new table section.

### Step 5 — Verify

After editing, re-read the updated `scripts/seed-demo.sql` and confirm:

- [ ] Every table referenced in INSERTs exists in the current schema
- [ ] Every column in every INSERT matches the schema's SQL column name exactly
- [ ] All hardcoded UUIDs contain only valid hex characters
- [ ] No enum value is used that isn't declared in the schema
- [ ] The file starts with `BEGIN;` and ends with `COMMIT;`
- [ ] The TRUNCATE covers all user-data tables

Report the final checklist result to the user.

## Context

- **ORM:** Drizzle ORM — the TypeScript property name and the SQL column name often differ.
  Always use the SQL column name (second argument of the column function).
  Example: `accountId: uuid('account_id')` → INSERT uses `account_id`, not `accountId`.
- **Migrations live in** `drizzle/` — each `.sql` file represents one schema version.
- **The seed resets all user data daily** via `scripts/demo-reset.sh` in the demo Docker stack.
- **Do not touch** `conversations`, `messages`, `documents` — these are excluded from seeding by design (AI chat history is ephemeral, documents are large binary blobs).
- **Do not change** the reset logic in `scripts/demo-reset.sh` unless explicitly asked.
