---
name: sqlite-review
description: Review and tune SQLite schemas, queries, indexes, and pragmas. Connects to the actual database to gather concrete evidence (EXPLAIN QUERY PLAN, page counts, table stats) before recommending changes.
---

# SQLite Review & Tuning

Audit and optimize SQLite usage in this project. Every recommendation must be
backed by concrete evidence gathered from the live database — never guess when
you can measure.

## When to Use

- After adding or modifying tables, columns, or indexes
- After writing new queries or changing existing ones
- When investigating slow operations or large DB file sizes
- Before merging any PR that touches `src/store/db/` or `src/store/triage/`
- Periodically as the dataset grows to catch regression

## Databases in This Project

| Database | Path pattern | Purpose |
|----------|-------------|---------|
| `findings.db` | `<store_root>/findings.db` | Star-schema store for scan results (runs, occurrences, secrets, rules, paths, roots) |
| `triage.sqlite` | `<store_root>/triage/triage.sqlite` | User triage decisions (occurrence_triage, secret_triage) |

Key source files:

| File | Role |
|------|------|
| `src/store/db/schema.rs` | DDL, pragmas, migrations |
| `src/store/db/writer.rs` | Write path, batching, transactions |
| `src/store/db/query.rs` | Read path, filtering, joins |
| `src/store/triage/schema.rs` | Triage DDL, pragmas |
| `src/store/triage/ops.rs` | Triage CRUD, upserts |

## Workflow

### Phase 0 — Locate a Database

Find or create a database to work with. Prefer a real database from a test run
over an empty one, since stats on empty tables are meaningless.

```bash
# Find existing databases.
find . -name 'findings.db' -o -name 'triage.sqlite' 2>/dev/null

# If none exist, run the integration tests to generate one.
cargo test --test integration sqlite_persistence -- --nocapture 2>&1 | head -40

# Or create one by running the scanner briefly against a test fixture.
```

If no database is available, create a temporary in-memory one by executing the
schema DDL and populating it with synthetic data so that EXPLAIN QUERY PLAN and
page-count queries return meaningful results. Use the `sqlite3` CLI:

```bash
sqlite3 /tmp/scanner_review.db < <(cat <<'SQL'
-- Paste DDL from src/store/db/schema.rs, then INSERT synthetic rows.
SQL
)
```

### Phase 1 — Collect Baseline Metrics

Connect to the database with `sqlite3` and gather facts. Capture **all** of
these before proposing any changes.

```bash
sqlite3 <db_path> <<'SQL'
-- 1. Integrity check.
PRAGMA integrity_check;

-- 2. Confirm pragmas.
PRAGMA journal_mode;
PRAGMA synchronous;
PRAGMA foreign_keys;
PRAGMA cache_size;
PRAGMA page_size;
PRAGMA wal_checkpoint(PASSIVE);

-- 3. Schema version.
PRAGMA user_version;

-- 4. Table and index page counts (proxy for size).
SELECT name, type FROM sqlite_master WHERE type IN ('table','index') ORDER BY type, name;

-- 5. Per-table row counts and page estimates.
SELECT 'roots' AS tbl, COUNT(*) FROM roots
UNION ALL SELECT 'paths', COUNT(*) FROM paths
UNION ALL SELECT 'rules', COUNT(*) FROM rules
UNION ALL SELECT 'secrets', COUNT(*) FROM secrets
UNION ALL SELECT 'runs', COUNT(*) FROM runs
UNION ALL SELECT 'occurrences', COUNT(*) FROM occurrences
UNION ALL SELECT 'observations', COUNT(*) FROM observations
UNION ALL SELECT 'run_rules', COUNT(*) FROM run_rules;

-- 6. Database file size (page_count * page_size).
SELECT page_count * page_size AS db_bytes,
       page_count,
       page_size
FROM pragma_page_count(), pragma_page_size();

-- 7. Freelist pages (fragmentation indicator).
PRAGMA freelist_count;

-- 8. Index usage stats (if sqlite_stat1 exists).
SELECT * FROM sqlite_stat1;
SQL
```

Record the output — it is the baseline for comparison.

### Phase 2 — Schema Review

Read the DDL source and the live schema, then check each item:

#### Checklist

- [ ] **Column types**: Are affinity types appropriate? BLOB for hashes, INTEGER
      for PKs, TEXT only where truly variable-length.
- [ ] **NOT NULL constraints**: Every column that must never be NULL has the
      constraint. Missing NOT NULL on a FK column is a bug.
- [ ] **UNIQUE constraints vs indexes**: Prefer UNIQUE constraint on the column
      definition over a separate unique index when semantically it's a key.
- [ ] **WITHOUT ROWID**: Junction/mapping tables with composite PKs and no
      large TEXT/BLOB columns should use WITHOUT ROWID.
- [ ] **DEFAULT values**: Sensible defaults for status/count columns. Avoid
      DEFAULT on columns that should always be explicitly set.
- [ ] **Foreign keys**: All FK references exist and point to the correct PK.
      Verify with `PRAGMA foreign_key_check;`.
- [ ] **Data type sizes**: BLOB columns storing fixed-size hashes — verify
      callers enforce length. No unbounded TEXT without application-level limits.
- [ ] **Schema version**: `user_version` matches the latest migration number.

```bash
sqlite3 <db_path> <<'SQL'
-- Dump live schema for comparison with source code.
.schema

-- Check FK integrity.
PRAGMA foreign_key_check;
SQL
```

### Phase 3 — Index Analysis

For every query in `src/store/db/query.rs` and `src/store/triage/ops.rs`, run
EXPLAIN QUERY PLAN and verify the planner uses the expected index.

#### Process

1. **List all SQL strings** in the query and writer modules.
2. **For each query**, run EXPLAIN QUERY PLAN with representative bind values.
3. **Flag** any full table scan (`SCAN`) on a table with >1000 rows.
4. **Flag** any temp B-tree sort (`USE TEMP B-TREE FOR ORDER BY`) that could be
   eliminated by a covering index.
5. **Flag** any index that is never used across all queries (dead index).

```bash
sqlite3 <db_path> <<'SQL'
-- Example: check the list_findings query plan.
EXPLAIN QUERY PLAN
SELECT o.occurrence_id, o.object_path, o.start_byte, o.end_byte,
       r.rule_name, s.secret_hash
FROM observations obs
JOIN occurrences o ON o.occ_pk = obs.occ_pk
JOIN rules r ON r.rule_pk = o.rule_pk
JOIN secrets s ON s.secret_pk = o.secret_pk
WHERE obs.run_pk = 1
ORDER BY o.object_path, o.start_byte;

-- Example: check the diff_runs NOT EXISTS subquery.
EXPLAIN QUERY PLAN
SELECT o.occurrence_id
FROM observations obs1
JOIN occurrences o ON o.occ_pk = obs1.occ_pk
WHERE obs1.run_pk = 1
  AND NOT EXISTS (
      SELECT 1 FROM observations obs2
      WHERE obs2.run_pk = 2 AND obs2.occ_pk = obs1.occ_pk
  );

-- Check if any indexes are unused (requires ANALYZE first).
ANALYZE;
-- Then inspect sqlite_stat1 for indexes with NULL stat values.
SELECT * FROM sqlite_stat1 ORDER BY tbl, idx;
SQL
```

#### Covering Index Opportunities

A covering index lets SQLite satisfy a query entirely from the index without
touching the main table. Look for queries that:
- SELECT only a subset of columns
- Filter on indexed columns
- ORDER BY indexed columns

```bash
sqlite3 <db_path> <<'SQL'
-- Does the observations PK cover the diff query? (It should — WITHOUT ROWID.)
EXPLAIN QUERY PLAN
SELECT 1 FROM observations WHERE run_pk = 2 AND occ_pk = 42;
SQL
```

### Phase 4 — Query Tuning

For each query identified in Phase 3 as suboptimal:

1. **Rewrite** the query or **add/modify** an index.
2. **Re-run** EXPLAIN QUERY PLAN to confirm improvement.
3. **Benchmark** with `.timer on` on a representative dataset.

```bash
sqlite3 <db_path> <<'SQL'
.timer on

-- Before: measure baseline.
SELECT COUNT(*) FROM occurrences WHERE path_pk = 42;

-- After: with proposed composite index.
CREATE INDEX IF NOT EXISTS idx_occ_path_rule ON occurrences(path_pk, rule_pk);
SELECT COUNT(*) FROM occurrences WHERE path_pk = 42;

-- Compare times, then drop the test index if not keeping.
DROP INDEX IF EXISTS idx_occ_path_rule;
SQL
```

#### Common Patterns to Check

| Pattern | What to verify |
|---------|---------------|
| `INSERT OR IGNORE` + `SELECT` (surrogate key lookup) | The UNIQUE index on the lookup column is hit, not a scan |
| `BEGIN IMMEDIATE` batching | Batch sizes are reasonable (100–1000 rows); not one-row-at-a-time inside a loop |
| `ON CONFLICT DO UPDATE` (triage upserts) | PRIMARY KEY covers the conflict target; no redundant index |
| `hex(run_id) LIKE 'PREFIX%'` (prefix match) | Cannot use index on BLOB column — flag if table grows large |
| `JOIN` chains (observations → occurrences → rules/secrets) | Join order matches index availability; no Cartesian products |
| `NOT EXISTS` subqueries (diff_runs) | Subquery uses index seek, not a scan per outer row |
| `ORDER BY` clauses | Satisfied by index or, if not, the sort cost is acceptable for expected row counts |

### Phase 5 — PRAGMA & Connection Tuning

Review the pragma settings in `schema.rs` and `triage/schema.rs` against the
workload characteristics.

| Pragma | Current | Check |
|--------|---------|-------|
| `journal_mode` | WAL | Correct for concurrent readers + single writer |
| `synchronous` | NORMAL | Acceptable for WAL; verify durability requirements |
| `foreign_keys` | ON | Must stay ON; verify not accidentally toggled |
| `busy_timeout` | 5000 ms | Adequate? Check if any SQLITE_BUSY errors in logs |
| `cache_size` | -64000 (64 MB) | Proportional to working set? Check with `PRAGMA cache_spill` |
| `page_size` | (default 4096) | Match filesystem block size; 4096 is usually correct |
| `mmap_size` | (not set) | Consider setting for read-heavy workloads; measure with `.timer on` |
| `temp_store` | (not set) | MEMORY can help if temp tables/sorts are frequent |
| `wal_autocheckpoint` | (default 1000) | May need tuning for write-heavy bursts; check WAL file size |

```bash
sqlite3 <db_path> <<'SQL'
-- Check WAL file size (indicator of checkpoint pressure).
PRAGMA wal_checkpoint(PASSIVE);
-- Returns: busy, log_pages, checkpointed_pages

-- Check if mmap would help (read-heavy).
PRAGMA mmap_size = 268435456;  -- 256 MB; measure query times before/after.

-- Check page fragmentation.
PRAGMA freelist_count;
-- If freelist is >10% of page_count, consider VACUUM.
SQL
```

### Phase 6 — Write Path Review

Examine the writer module for correctness and performance:

- [ ] **Transaction scope**: Batches are wrapped in `BEGIN IMMEDIATE ... COMMIT`.
      No implicit autocommit for multi-row inserts.
- [ ] **Prepared statements**: SQL is prepared once and reused, not re-parsed per
      row. Check for `conn.prepare_cached()` usage.
- [ ] **Batch size**: Reasonable upper bound. SQLite performance degrades with
      very large transactions (>100K rows) due to WAL growth.
- [ ] **Error handling**: Failed transactions are rolled back. Partial batches
      don't leave the DB in an inconsistent state.
- [ ] **Mutex contention**: Writer mutex held only during DB operations, not
      during computation or I/O.

### Phase 7 — Stress & Concurrency Check

If the database is expected to handle concurrent access:

```bash
# Run the concurrent writer stress test.
cargo test --lib writer -- concurrent --nocapture

# Run the integration suite to verify no SQLITE_BUSY failures.
cargo test --test integration sqlite_persistence -- --nocapture
```

Check for:
- SQLITE_BUSY errors under load
- WAL file growing unboundedly (checkpoint not keeping up)
- Deadlocks between writer and reader connections

## Output Format

```markdown
## SQLite Review: [database name]

### Baseline Metrics

| Metric | Value |
|--------|-------|
| DB size | X MB |
| Page count | N |
| Freelist pages | N (X%) |
| WAL size | N pages |
| Row counts | roots: N, paths: N, ... |

### Schema Findings

| Severity | Table.Column | Issue | Recommendation |
|----------|-------------|-------|----------------|
| WARN | secrets.status | Missing CHECK constraint | Add CHECK (status IN (0,1,2,3)) |
| INFO | run_rules | Already WITHOUT ROWID | No action |

### Query Plan Analysis

| Query | Location | Plan | Issue | Fix |
|-------|----------|------|-------|-----|
| list_findings | query.rs:133 | SCAN occurrences | Missing composite index | Add idx_occ_root_path(root_pk, path_pk) |
| diff_runs | query.rs:215 | SEARCH observations USING PK | Optimal | None |

### Index Recommendations

| Action | Index | Rationale | Evidence |
|--------|-------|-----------|----------|
| ADD | idx_occ_root_path ON occurrences(root_pk, path_pk) | Covers list_findings filter+join | EXPLAIN shows SCAN → SEARCH |
| DROP | idx_foo | Never used in any query | sqlite_stat1 shows 0 lookups |

### PRAGMA Recommendations

| Pragma | Current | Proposed | Rationale | Evidence |
|--------|---------|----------|-----------|----------|
| mmap_size | 0 | 268435456 | Read queries 15% faster | .timer on before/after |

### Write Path Findings

| Severity | Location | Issue | Recommendation |
|----------|----------|-------|----------------|
| WARN | writer.rs:361 | Prepare per-call, not cached | Use prepare_cached() |

### Summary

- **Critical**: N issues requiring immediate action
- **Warnings**: N issues to address before next release
- **Info**: N observations, no action needed
- **Estimated size impact**: ±X MB from index changes
```

## Anti-Patterns to Flag

1. **Guessing without measuring**: Never recommend an index without showing the
   EXPLAIN QUERY PLAN that proves it's needed.
2. **Over-indexing**: Each index costs write performance and disk space. Only add
   indexes that serve actual queries.
3. **VACUUM without cause**: VACUUM rewrites the entire DB and holds an exclusive
   lock. Only recommend if freelist is >10% of total pages.
4. **Changing page_size on existing DBs**: Requires VACUUM. Only worth it for
   new databases.
5. **Disabling foreign_keys for performance**: Never. Correctness first.
6. **synchronous = OFF**: Data corruption risk. NORMAL is the floor for WAL mode.
7. **Unbounded LIKE on BLOB columns**: `hex(col) LIKE 'PREFIX%'` cannot use
   indexes. Flag and suggest alternatives (prefix table, stored hex column).

## Related Skills

- `/performance-analyzer` — Profile Rust code around DB operations
- `/test-strategy` — Choose between unit, property, and fuzz tests for DB layer
- `/security-reviewer` — Audit SQL injection risks in dynamic query construction
