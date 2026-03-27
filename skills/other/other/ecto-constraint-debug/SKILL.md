---
name: ecto-constraint-debug
description: Debug Ecto constraint violations - trace triggers, check migrations, find duplicate data. Use when seeing unique_constraint, foreign_key_constraint, or check_constraint errors.
effort: medium
---

# Ecto Constraint Debugging

Systematic approach to diagnosing constraint violations. Load when you see `Ecto.ConstraintError`, `unique_constraint`, `foreign_key_constraint`, or constraint-related changeset errors.

## Iron Laws

1. **READ THE CONSTRAINT NAME** — The constraint name (e.g., `links_url_index`) tells you exactly which index/constraint failed. Parse it from the error message first
2. **CHECK MIGRATION BEFORE CODE** — Verify the constraint definition in `priv/repo/migrations/` matches what the schema expects
3. **TRACE ALL INSERT PATHS** — Find every code path that inserts into the constrained table. The bug is often in a path you didn't consider
4. **RACE CONDITION UNTIL PROVEN OTHERWISE** — If validation passes but constraint fails, assume concurrent inserts until you prove a single-request cause

## Step-by-Step Debugging

### Step 1: Parse the Error

Extract from the error message:

- **Constraint name** (e.g., `users_email_index`)
- **Table name** (e.g., `users`)
- **Operation** (insert, update, or delete)
- **Conflicting values** (if available in logs)

### Step 2: Find the Migration

```bash
grep -r "constraint_name" priv/repo/migrations/
# Also check: create unique_index, create index, add constraint
```

Verify: Does the migration constraint match the schema's `unique_constraint/3` or `foreign_key_constraint/3` call?

### Step 3: Find the Schema

```elixir
# Look for the constraint handling in changeset
grep -r "unique_constraint\|foreign_key_constraint\|check_constraint" lib/
```

### Step 4: Trace Insert Paths

Find ALL callers that insert/update this schema:

```bash
grep -r "Repo.insert\|Repo.update\|Repo.insert_all\|cast_assoc.*:schema_name" lib/
```

### Step 5: Identify the Cause

| Symptom | Likely Cause | Fix Pattern |
|---------|-------------|-------------|
| Same user triggers twice | Race condition (double-click, retry) | Upsert with `on_conflict` |
| Multiple parents share child | `cast_assoc` doesn't dedup across changesets | Dedup before building changesets |
| Concurrent API requests | Missing transaction isolation | Wrap in `Repo.transaction` or use upsert |
| Migration added constraint to existing data | Data violates new constraint | Backfill or clean data first |

### Step 6: Apply Fix

See `${CLAUDE_SKILL_DIR}/references/constraint-patterns.md` for detailed fix patterns.

## Quick Fixes by Constraint Type

**Unique violation** → Upsert: `Repo.insert(changeset, on_conflict: :replace_all, conflict_target: [:field])`

**Foreign key violation** → Check: Does the referenced record exist? Was it deleted concurrently?

**Check constraint** → Validate: Does the value satisfy the constraint condition?

## References

- `${CLAUDE_SKILL_DIR}/references/constraint-patterns.md` - Detailed patterns for each constraint type
