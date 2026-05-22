---
name: postgresql-patterns
description: PostgreSQL-specific database patterns including advanced index types (GiST, GIN, BRIN, partial), native data types (JSONB, arrays, enums, ranges), PgBouncer pooling, and VACUUM tuning. Use when working with PostgreSQL databases, writing PostgreSQL-specific SQL, or optimizing PostgreSQL performance. Do NOT use for MySQL/Aurora -- use database-patterns and mysql-aurora-patterns instead.
durability: encoded-preference
---

# PostgreSQL Patterns

PostgreSQL-specific optimization patterns. For DB-agnostic patterns (transactions, N+1, caching principles, EXPLAIN ANALYZE, zero-downtime migrations), see database-patterns skill.

## Index Types

### When to Use Which Index

| Type | Best For | Not Suitable For |
|------|----------|-----------------|
| B-tree (default) | Equality and range queries on scalar columns | JSONB, arrays, geometric data |
| GiST | Range overlap queries, geometric/spatial data, full-text on update-heavy tables | Simple equality queries |
| GIN | JSONB (`@>`, `?`, `?|`, `?&`), arrays (`@>`, `<@`, `&&`), full-text on read-heavy tables | Update-heavy tables (rebuild cost) |
| BRIN | Large tables where indexed column correlates with physical row order (timestamps, sequences) | Randomly ordered data |

### Partial Indexes

Index only the rows that matter:

```sql
-- Only index active users (skip 90% of rows)
CREATE INDEX idx_users_active_email ON users (email) WHERE is_active = true;

-- Only index non-null values
CREATE INDEX idx_users_phone ON users (phone) WHERE phone IS NOT NULL;
```

**When to use**: Queries that consistently filter on the same condition. Significant storage savings when the filtered subset is small relative to total rows.

## Data Types

### JSONB

Binary JSON with indexing support. Prefer over JSON (which stores raw text).

**Anti-pattern**: Storing relational data in JSONB to avoid schema changes. Use JSONB for truly semi-structured data (user preferences, API responses, feature flags), not as a substitute for proper columns.

### Enums

Type-safe enumerated values. **Caveat**: Adding values is easy (`ALTER TYPE ... ADD VALUE`), but removing or renaming values requires a migration. Use enums for stable value sets.

### Range Types with Exclusion Constraints

```sql
CREATE TABLE reservations (
    id BIGSERIAL PRIMARY KEY,
    room_id INTEGER NOT NULL,
    during TSTZRANGE NOT NULL,
    EXCLUDE USING gist (room_id WITH =, during WITH &&)
);
-- No overlapping reservations for the same room (enforced at DB level)
```

## Connection Pooling with PgBouncer

### Pooling Mode Selection

| Mode | Use Case | Prepared Statements | Session Features |
|------|----------|--------------------:|-----------------|
| Session | Long-lived connections | Yes | Full |
| Transaction | Serverless, short queries | No | Per-transaction only |
| Statement | Simple read replicas | No | None |

- **Transaction mode** for web applications (connections returned after each transaction)
- **Session mode** when using prepared statements or session-level features (advisory locks, temp tables)
- Avoid `LISTEN/NOTIFY` in transaction mode (requires session mode)

## VACUUM and Autovacuum

PostgreSQL's MVCC creates dead tuples on UPDATE/DELETE. VACUUM reclaims space.

### Autovacuum Tuning for Write-Heavy Tables

```sql
ALTER TABLE high_write_table SET (
    autovacuum_vacuum_scale_factor = 0.01,    -- Default 0.2 (20%)
    autovacuum_analyze_scale_factor = 0.005   -- Default 0.1 (10%)
);
```

**Anti-pattern**: Disabling autovacuum. Even if you run manual VACUUM, autovacuum also triggers ANALYZE for query planner statistics.

## Query Optimization (PostgreSQL-Specific)

### Non-Obvious Techniques

```sql
-- DISTINCT ON for "latest per group" (no equivalent in MySQL)
SELECT DISTINCT ON (user_id) user_id, created_at, content
FROM comments ORDER BY user_id, created_at DESC;
```

### pg_stat_statements

Enable for query performance monitoring:

```sql
SELECT query, calls, total_exec_time, mean_exec_time, rows
FROM pg_stat_statements ORDER BY total_exec_time DESC LIMIT 20;
```

## Review Checklist

- [ ] Correct index type for the data pattern (B-tree vs GiST vs GIN vs BRIN)
- [ ] JSONB used instead of JSON for indexed/queried data
- [ ] Partial indexes considered for filtered queries
- [ ] Autovacuum tuned for write-heavy tables
- [ ] PgBouncer mode matches application requirements
- [ ] Replication lag accounted for in read-after-write paths

For DB-agnostic review items, see database-patterns skill.
