---
name: supabase-postgres
model: standard
description: Postgres performance optimization and best practices from Supabase — covering indexing, connection management, RLS security, schema design, locking, data access patterns, and monitoring. Use when writing SQL, designing schemas, optimizing queries, or configuring Postgres.
license: MIT
metadata:
  author: supabase
  version: "1.1.0"
---

# Supabase Postgres Best Practices

Comprehensive Postgres performance guide organized by impact priority. Each rule includes incorrect vs. correct SQL examples with explanations.

## When to Use

- Writing SQL queries or designing schemas
- Implementing or reviewing indexes
- Debugging slow queries or connection issues
- Configuring connection pooling
- Implementing Row-Level Security (RLS)
- Reviewing database performance

## Rule Categories by Priority

| Priority | Category | Impact | Reference Prefix |
|----------|----------|--------|-----------------|
| 1 | Query Performance | CRITICAL | `query-` |
| 2 | Connection Management | CRITICAL | `conn-` |
| 3 | Security & RLS | CRITICAL | `security-` |
| 4 | Schema Design | HIGH | `schema-` |
| 5 | Concurrency & Locking | MEDIUM-HIGH | `lock-` |
| 6 | Data Access Patterns | MEDIUM | `data-` |
| 7 | Monitoring & Diagnostics | LOW-MEDIUM | `monitor-` |
| 8 | Advanced Features | LOW | `advanced-` |

See `references/` for detailed rule files with full SQL examples.


## Installation

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install supabase-postgres
```


---

## Critical Rules Summary

### Query Performance

**Always index WHERE and JOIN columns.** Unindexed columns cause full table scans that get exponentially slower as tables grow. Create indexes on every column used in WHERE, JOIN, or ORDER BY on large tables.

```sql
-- Create index on frequently filtered column
create index orders_customer_id_idx on orders (customer_id);
```

**Choose the right index type.** B-tree (default) handles `=, <, >, BETWEEN`. Use GIN for JSONB/arrays/full-text, BRIN for large time-series tables, Hash for equality-only lookups.

```sql
create index products_attrs_idx on products using gin (attributes);  -- JSONB
create index events_time_idx on events using brin (created_at);      -- Time-series
```

**Use partial indexes** for queries that always filter on the same condition. They're smaller, faster, and cheaper to maintain.

```sql
create index orders_pending_idx on orders (created_at)
  where status = 'pending';
```

### Connection Management

**Always use connection pooling.** Each Postgres connection uses 1-3MB RAM. Without pooling, 500 concurrent users = 500 connections = crashed database.

- Use PgBouncer or Supabase's built-in pooler
- **Transaction mode** for most apps (connection returned after each transaction)
- **Session mode** only when using prepared statements or temp tables
- Formula: pool_size = `(CPU cores * 2) + disk_count`

**Set appropriate connection limits.** Monitor with:

```sql
select count(*), state from pg_stat_activity group by state;
```

### Security & RLS

**Enable RLS for multi-tenant data.** Application-level filtering alone is one bug away from exposing all data.

```sql
alter table orders enable row level security;
create policy orders_policy on orders
  for all to authenticated
  using ((select auth.uid()) = user_id);  -- Wrap in SELECT for performance
```

**Optimize RLS policies.** Wrap function calls in `(select ...)` so they execute once, not per-row. On a 1M-row table, this is 100x+ faster.

```sql
-- BAD: auth.uid() called per row
using (auth.uid() = user_id);

-- GOOD: auth.uid() called once, cached
using ((select auth.uid()) = user_id);
```

---

## High-Impact Rules Summary

### Schema Design

**Choose appropriate data types:**

```sql
create table users (
  id bigint generated always as identity primary key,  -- Not serial
  email text,                      -- Not varchar(n)
  created_at timestamptz,          -- Not timestamp
  is_active boolean default true,  -- Not varchar
  price numeric(10,2)              -- Not float
);
```

Key guidelines: `bigint` over `int`, `text` over `varchar(n)`, `timestamptz` over `timestamp`, `numeric` over `float` for money.

**Select optimal primary keys:** `bigint identity` for single-database, UUIDv7 for distributed systems. Avoid random UUIDv4 as PK on large tables (causes index fragmentation).

**Always index foreign key columns.** Postgres does NOT auto-index FKs. Missing FK indexes cause slow JOINs and CASCADE operations.

```sql
-- Find missing FK indexes
select conrelid::regclass as table_name, a.attname as fk_column
from pg_constraint c
join pg_attribute a on a.attrelid = c.conrelid and a.attnum = any(c.conkey)
where c.contype = 'f'
  and not exists (
    select 1 from pg_index i
    where i.indrelid = c.conrelid and a.attnum = any(i.indkey)
  );
```

### Concurrency & Locking

**Prevent deadlocks with consistent lock ordering.** Always acquire locks in a deterministic order (e.g., by ID).

```sql
-- Lock rows in ID order before updating
begin;
select * from accounts where id in (1, 2) order by id for update;
update accounts set balance = balance - 100 where id = 1;
update accounts set balance = balance + 100 where id = 2;
commit;
```

### Data Access Patterns

**Eliminate N+1 queries.** Batch with `ANY(array[...])` or use JOINs instead of per-row queries.

```sql
-- BAD: 101 round trips
select id from users where active = true;  -- 100 IDs
select * from orders where user_id = 1;    -- repeated 100 times

-- GOOD: 1 round trip
select * from orders where user_id = any($1::bigint[]);
```

**Use cursor-based pagination.** OFFSET scans all skipped rows. Keyset pagination is O(1) regardless of page depth.

```sql
-- BAD: page 1000 scans 20,000 rows
select * from products order by id limit 20 offset 19980;

-- GOOD: page 1000, same speed as page 1
select * from products where id > $last_id order by id limit 20;
```

---

## Monitoring & Diagnostics

**Use EXPLAIN ANALYZE** to diagnose slow queries:

```sql
explain (analyze, buffers, format text)
select * from orders where customer_id = 123 and status = 'pending';
```

What to look for:
- `Seq Scan` on large tables → missing index
- `Rows Removed by Filter` → poor selectivity
- `Buffers: read >> hit` → data not cached
- `Sort Method: external merge` → increase `work_mem`

**Monitor with pg_stat_statements** for aggregate query performance across the system.

---

## Quick Reference

| Problem | Solution |
|---------|----------|
| Slow filtered queries | Add index on WHERE columns |
| Slow JOINs | Index foreign key columns |
| JSONB/array queries slow | Use GIN index |
| Time-series table huge | Use BRIN index |
| Too many connections | Use connection pooling |
| Data leaks | Enable RLS with policies |
| RLS is slow | Wrap functions in `(select ...)` |
| N+1 queries | Batch with `ANY(array[...])` |
| Deep pagination slow | Cursor/keyset pagination |
| Deadlocks | Consistent lock ordering |
| Schema bloat | Use correct data types |
| Index fragmentation | Use `bigint identity` or UUIDv7 PKs |

## NEVER Do

- **NEVER skip connection pooling** — Direct connections don't scale
- **NEVER use `float` for money** — Use `numeric` for exact arithmetic
- **NEVER rely on app-only filtering for security** — Use RLS
- **NEVER use `OFFSET` for deep pagination** — Use keyset/cursor pagination
- **NEVER use random UUIDv4 as PK on large tables** — Causes index fragmentation
- **NEVER create foreign keys without indexes** — Postgres doesn't auto-index them

## References

Detailed rule files in `references/`:

**Query Performance (Critical):**
- `query-missing-indexes.md` — Index WHERE and JOIN columns
- `query-index-types.md` — B-tree vs GIN vs BRIN vs Hash
- `query-partial-indexes.md` — Partial indexes for filtered queries
- `query-composite-indexes.md` — Multi-column index design
- `query-covering-indexes.md` — Index-only scans

**Connection Management (Critical):**
- `conn-pooling.md` — Connection pooling with PgBouncer
- `conn-limits.md` — Setting connection limits
- `conn-idle-timeout.md` — Idle connection management
- `conn-prepared-statements.md` — Prepared statement pooling

**Security (Critical):**
- `security-rls-basics.md` — Row-Level Security fundamentals
- `security-rls-performance.md` — Optimizing RLS policies
- `security-privileges.md` — Role and privilege management

**Schema Design (High):**
- `schema-data-types.md` — Choosing data types
- `schema-primary-keys.md` — Primary key strategies
- `schema-foreign-key-indexes.md` — FK index requirements
- `schema-lowercase-identifiers.md` — Naming conventions
- `schema-partitioning.md` — Table partitioning strategies

**Concurrency & Locking (Medium-High):**
- `lock-deadlock-prevention.md` — Avoiding deadlocks
- `lock-short-transactions.md` — Keeping transactions short
- `lock-skip-locked.md` — Queue processing pattern
- `lock-advisory.md` — Advisory locks

**Data Access (Medium):**
- `data-n-plus-one.md` — Eliminating N+1 queries
- `data-pagination.md` — Cursor vs offset pagination
- `data-batch-inserts.md` — Bulk insert patterns
- `data-upsert.md` — Upsert patterns

**Monitoring (Low-Medium):**
- `monitor-explain-analyze.md` — Query plan analysis
- `monitor-pg-stat-statements.md` — Aggregate query stats
- `monitor-vacuum-analyze.md` — Table maintenance

**Advanced Features (Low):**
- `advanced-jsonb-indexing.md` — JSONB query optimization
- `advanced-full-text-search.md` — Full-text search setup

External:
- https://www.postgresql.org/docs/current/
- https://supabase.com/docs/guides/database/overview
- https://supabase.com/docs/guides/auth/row-level-security
