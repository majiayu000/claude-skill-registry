---
name: bear-migrate
description: Move mountains of data with patient strength. Wake from hibernation, gather the data, move it carefully, hibernate to verify, and wake again to confirm. Use when migrating data, transforming schemas, or moving between systems.
---

# Bear Migrate

The bear moves slowly but with unstoppable strength. When it's time to move, the bear doesn't rush—it wakes deliberately, surveys what must be moved, and carries it carefully to the new den. Some journeys take seasons. The bear is patient. Data arrives intact, or it doesn't arrive at all.

## When to Activate

- User asks to "migrate data" or "move this data"
- User says "transform the schema" or "update the database"
- User calls `/bear-migrate` or mentions bear/migration
- Database schema changes requiring data migration
- Moving data between systems or formats
- Upgrading to new data structures
- Splitting or merging tables
- Importing/exporting large datasets

**Pair with:** `bloodhound-scout` to understand data relationships first

---

## The Migration

```
WAKE --> GATHER --> MOVE --> HIBERNATE --> VERIFY
  |          |         |           |           |
Prepare   Collect   Execute    Review      Confirm
 Tools      Data    Safely     Results     Success
```

### Phase 1: WAKE

*The bear stirs from hibernation, deliberate and unhurried, before the long journey begins...*

Set up the migration environment. Document the plan, take the backup, and build the Kysely migration script before moving a single row.

- Document the migration plan: source schema, destination schema, transformation mappings, calculated fields, data cleanup needed
- Back up the database — SQLite: `sqlite3 production.db ".backup backup-$(date +%Y%m%d).db"` — PostgreSQL: `pg_dump -Fc` — D1: `wrangler d1 export`
- Create the dated migration script (e.g., `migrations/20260130_name.ts`) with `up()` and `down()` functions
- Identify SQLite/D1 ALTER TABLE constraints: DROP COLUMN and MODIFY COLUMN require a full table rebuild

**Reference:** Load `references/migration-patterns.md` for the MigrationPlan interface and Kysely migration script structure. Load `references/schema-changes.md` for SQLite/D1 ALTER TABLE limitations and the table rebuild pattern. Load `references/backup-rollback.md` for backup commands and verification.

---

### Phase 2: GATHER

*The bear knows exactly what it carries before lifting a single stone...*

Understand the data thoroughly before writing transformation logic. Count rows, find orphans, check for quality issues, and map relationships. Surprises during MOVE are costly; surprises during GATHER are free.

- Count rows per table; estimate total migration time at expected batch size
- Check for orphaned records (comments without posts, preferences without users)
- Run data quality checks: nulls in required fields, duplicate unique values, malformed data (emails without `@`, invalid dates)
- Map parent-to-child relationships and establish migration order (always migrate parent tables first)

**Reference:** Load `references/migration-patterns.md` for data inventory queries, quality check code, relationship mapping patterns, and how to fail fast when quality issues are found

---

### Phase 3: MOVE

*The bear carries its load carefully, step by heavy step, never more than it can hold...*

Execute the migration safely. Use batch processing for large datasets (1000 records per batch). Wrap in a transaction so a failure leaves the database clean. Log progress so long migrations are observable.

- For small datasets (<10k rows): wrap all operations in a single transaction with validation before dropping old structure
- For large datasets (>100k rows): batch process in groups of 1000 with progress logging; pause every 10,000 records to prevent memory pressure
- Apply transformation logic: normalize emails, split names, calculate derived fields, convert status enums
- Track progress: total rows counted before batching, percent complete logged after each batch

**Reference:** Load `references/migration-patterns.md` for the complete `migrateInBatches()` implementation, transaction safety pattern, `transformRecord()` examples, and progress tracking code. Load `references/schema-changes.md` for D1-specific constraints and the table rebuild pattern for unsupported ALTER operations.

---

### Phase 4: HIBERNATE

*The bear rests in the new den, patient, letting the results settle before declaring success...*

Verify the migration before removing old data. Row counts must match. Data integrity checks must pass. Spot-check real records. Do not drop old tables until verification is complete.

- Verify row counts match between old and new structures
- Run data integrity checks: required fields, format validation (email patterns), foreign key integrity
- Spot-check 10 sample records to verify transformation logic ran correctly
- If any check fails: stop, investigate, do NOT drop old tables — the backup is your safety net

**Reference:** Load `references/backup-rollback.md` for the row count validation query, integrity check code, and spot check pattern

---

### Phase 5: VERIFY

*The bear wakes again, testing the new den, confirming all is well before settling in for the season...*

Final confirmation: run the full application test suite, check query performance on the new schema, archive the backup, and generate the migration report.

- Run full application test suite (`npm test`); test critical paths manually in dev server
- Check query performance with `EXPLAIN QUERY PLAN` on queries that touch migrated tables; add indexes if full table scans appear where they didn't before
- Archive the pre-migration backup (keep 30 days minimum in production)
- Generate the migration completion report: records migrated, duration, transformations applied, validation results, rollback location

**Reference:** Load `references/backup-rollback.md` for performance check queries, cleanup procedures, and the migration completion report template

---

## Reference Routing Table

| Phase | Reference | Load When |
|-------|-----------|-----------|
| WAKE | `references/migration-patterns.md` | Always (plan structure, Kysely script scaffold) |
| WAKE | `references/schema-changes.md` | Any schema change (ALTER TABLE, column types) |
| WAKE | `references/backup-rollback.md` | Always (backup commands before touching data) |
| GATHER | `references/migration-patterns.md` | Data inventory queries, quality checks |
| MOVE | `references/migration-patterns.md` | Batch processing, transactions, transformations |
| MOVE | `references/schema-changes.md` | D1 constraints, table rebuild, zero-downtime |
| HIBERNATE | `references/backup-rollback.md` | Row count validation, integrity checks |
| VERIFY | `references/backup-rollback.md` | Performance checks, cleanup, completion report |

---

## Bear Rules

### Patience
Large migrations take time. Don't rush. Process in batches to avoid memory issues and timeout limits. A migration that takes 20 minutes safely beats one that takes 2 minutes and corrupts data.

### Safety
Always backup. Always test rollbacks. Never migrate production without a way back. If the `down()` migration is lossy, document the backup location explicitly in the code.

### Thoroughness
Verify everything. Row counts, data integrity, application functionality. A migration that looks complete but has 3 orphaned records with null foreign keys will surface as a bug in production at the worst possible time.

### Communication
Use migration metaphors:
- "Waking from hibernation..." (preparation)
- "Gathering the harvest..." (data inventory)
- "Carrying the load..." (migration execution)
- "Resting in the new den..." (verification)
- "The den is ready." (migration complete)

---

## Anti-Patterns

**The bear does NOT:**
- Migrate without backups
- Skip validation steps (count checks, integrity checks, spot checks)
- Migrate production without testing on staging first
- Delete old data before verifying new data is complete and correct
- Rush large migrations (memory issues, timeouts, silent truncation)
- Write lossy `down()` migrations without documenting the rollback path

---

## Example Migration

**User:** "We need to split the user's full name into first and last name fields"

**Bear flow:**

1. **WAKE** — "Create migration script, backup database, plan transformation logic: split `full_name` on first space, handle null names, preserve id/email/created_at"

2. **GATHER** — "15,423 users. Found 234 emails with mixed case. 12 users with null names (will default to null first_name/last_name)."

3. **MOVE** — "Batch migration (1000 records/batch). Transform: lowercase emails, split names, calculate account_age_days. Progress logged per batch."

4. **HIBERNATE** — "Verify: row counts match (15,423/15,423), no null created_at, FK integrity intact. Spot check 10 users — transformation looks correct."

5. **VERIFY** — "App tests pass, EXPLAIN QUERY PLAN shows index use on users.email, backup archived. Migration complete."

---

## Quick Decision Guide

| Scenario | Approach |
|----------|----------|
| Schema change only (add column) | Standard migration — no batch processing needed |
| Small dataset (<10k rows) | Single transaction |
| Large dataset (>100k rows) | Batch processing with progress tracking (load `references/migration-patterns.md`) |
| Zero downtime required | Expand-Migrate-Contract pattern (load `references/schema-changes.md`) |
| Drop column in SQLite/D1 | Table rebuild pattern required (load `references/schema-changes.md`) |
| Complex transformations | ETL pipeline with validation checkpoints at each step |
| Cross-database migration | Export/import with explicit type mapping |

---

## Integration with Other Skills

**Before Migrating:**
- `bloodhound-scout` — Understand data relationships before migrating them

**After Migrating:**
- `beaver-build` — Write migration regression tests
- `fox-optimize` — If new schema has performance implications

---

*The bear moves slowly, but nothing is left behind.*
