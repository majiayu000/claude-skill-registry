---
name: database-migrations
model: standard
description: Safe, zero-downtime database migration strategies — schema evolution, rollback planning, data migration, tooling, and anti-pattern avoidance for production systems. Use when planning schema changes, writing migrations, or reviewing migration safety.
---

# Database Migration Patterns

## Schema Evolution Strategies

| Strategy | Risk | Downtime | Best For |
|----------|------|----------|----------|
| **Additive-Only** | Very Low | None | APIs with backward-compatibility guarantees |
| **Expand-Contract** | Low | None | Renaming, restructuring, type changes |
| **Parallel Change** | Low | None | High-risk changes on critical tables |
| **Lazy Migration** | Medium | None | Large tables where bulk migration is too slow |
| **Big Bang** | High | Yes | Dev/staging or small datasets only |

**Default to Additive-Only.** Escalate to Expand-Contract only when you must modify or remove existing structures.


## Installation

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install database-migrations
```


---

## Zero-Downtime Patterns

Every production migration must avoid locking tables or breaking running application code.

| Operation | Pattern | Key Constraint |
|-----------|---------|----------------|
| **Add column** | Nullable first | Never add `NOT NULL` without default on large tables |
| **Rename column** | Expand-contract | Add new → dual-write → backfill → switch reads → drop old |
| **Drop column** | Deprecate first | Stop reading → stop writing → deploy → drop |
| **Change type** | Parallel column | Add new type → dual-write + cast → switch → drop old |
| **Add index** | Concurrent | `CREATE INDEX CONCURRENTLY` — don't wrap in transaction |
| **Split table** | Extract + FK | Create new → backfill → add FK → update queries → drop old columns |
| **Change constraint** | Two-phase | Add `NOT VALID` → `VALIDATE CONSTRAINT` separately |
| **Add enum value** | Append only | Never remove or rename existing values |

---

## Migration Tools

| Tool | Ecosystem | Style | Key Strength |
|------|-----------|-------|-------------|
| **Prisma Migrate** | TypeScript/Node | Declarative (schema diff) | ORM integration, shadow DB |
| **Knex** | JavaScript/Node | Imperative (up/down) | Lightweight, flexible |
| **Drizzle Kit** | TypeScript/Node | Declarative (schema diff) | Type-safe, SQL-like |
| **Alembic** | Python | Imperative (upgrade/downgrade) | Granular control, autogenerate |
| **Django Migrations** | Python/Django | Declarative (model diff) | Auto-detection |
| **Flyway** | JVM / CLI | SQL file versioning | Simple, wide DB support |
| **golang-migrate** | Go / CLI | SQL (up/down files) | Minimal, embeddable |
| **Atlas** | Go / CLI | Declarative (HCL/SQL diff) | Schema-as-code, linting, CI |

Match the tool to your ORM and deployment pipeline. Prefer declarative for simple schemas, imperative for fine-grained data manipulation.

---

## Rollback Strategies

| Approach | When to Use |
|----------|-------------|
| **Reversible (up + down)** | Schema-only changes, early-stage products |
| **Forward-only (corrective migration)** | Data-destructive changes, production at scale |
| **Hybrid** | Reversible for schema, forward-only for data |

### Data Preservation

1. **Soft-delete columns** — rename with `_deprecated` suffix instead of dropping
2. **Snapshot tables** — `CREATE TABLE _backup_<table>_<date> AS SELECT * FROM <table>`
3. **Point-in-time recovery** — ensure WAL archiving covers migration windows
4. **Logical backups** — `pg_dump` of affected tables before migration

### Blue-Green Database

```
1. Replicate primary → secondary (green)
2. Apply migration to green
3. Run validation suite against green
4. Switch traffic to green
5. Keep blue as rollback target (N hours)
6. Decommission blue after confidence window
```

---

## Data Migration Patterns

### Backfill Strategies

| Strategy | Best For |
|----------|----------|
| **Inline backfill** | Small tables (< 100K rows) |
| **Batched backfill** | Medium tables (100K–10M rows) |
| **Background job** | Large tables (10M+ rows) |
| **Lazy backfill** | When immediate consistency not required |

### Batch Processing

```sql
DO $$
DECLARE
  batch_size INT := 1000;
  rows_updated INT;
BEGIN
  LOOP
    UPDATE my_table
    SET new_col = compute_value(old_col)
    WHERE id IN (
      SELECT id FROM my_table
      WHERE new_col IS NULL
      LIMIT batch_size
      FOR UPDATE SKIP LOCKED
    );
    GET DIAGNOSTICS rows_updated = ROW_COUNT;
    EXIT WHEN rows_updated = 0;
    PERFORM pg_sleep(0.1);  -- throttle to reduce lock pressure
    COMMIT;
  END LOOP;
END $$;
```

### Dual-Write Period

For expand-contract and parallel change:

1. **Dual-write** — application writes to both old and new columns/tables
2. **Backfill** — fill new structure with historical data
3. **Verify** — assert consistency (row counts, checksums)
4. **Cut over** — switch reads to new, stop writing to old
5. **Cleanup** — drop old structure after cool-down period

---

## Testing Migrations

### Test Against Production-Like Data

- Never test against empty or synthetic data only
- Use anonymized production snapshots
- Match data volume — a migration working on 1K rows may lock on 10M
- Reproduce edge cases: NULLs, empty strings, max-length, unicode

### Migration CI Pipeline

```yaml
- name: Test migrations
  steps:
    - run: docker compose up -d db
    - run: npm run migrate:up        # apply all
    - run: npm run migrate:down      # rollback all
    - run: npm run migrate:up        # re-apply (idempotency)
    - run: npm run test:integration  # validate app
    - run: npm run migrate:status    # no pending
```

Every migration PR must pass: up → down → up → tests.

---

## Migration Checklist

### Pre-Migration

- [ ] Tested against production-like data volume
- [ ] Rollback written and tested
- [ ] Backup of affected tables created
- [ ] App code compatible with both old and new schema
- [ ] Execution time benchmarked on staging
- [ ] Lock impact analyzed
- [ ] Replication lag monitoring in place

### During Migration

- [ ] Monitor lock waits and active queries
- [ ] Monitor replication lag
- [ ] Watch for error rate spikes
- [ ] Keep rollback command ready

### Post-Migration

- [ ] Schema matches expected state
- [ ] Integration tests pass against migrated DB
- [ ] Data integrity validated (row counts, checksums)
- [ ] ORM schema / type definitions updated
- [ ] Deprecated structures cleaned up after cool-down
- [ ] Migration documented in team runbook

---

## NEVER Do

1. **NEVER** run untested migrations directly in production
2. **NEVER** drop a column without first removing all application references and deploying
3. **NEVER** add `NOT NULL` to a large table without a default value in a single statement
4. **NEVER** mix schema DDL and data mutations in the same migration file
5. **NEVER** skip the dual-write phase when renaming columns in a live system
6. **NEVER** assume migrations are instantaneous — always benchmark on production-scale data
7. **NEVER** disable foreign key checks to "speed up" migrations in production
8. **NEVER** deploy application code that depends on a schema change before the migration has completed
