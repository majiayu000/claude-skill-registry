---
name: database-architecture
description: MANDATORY when designing schemas, writing migrations, creating indexes, or making architectural database decisions - enforces PostgreSQL 18 best practices including AIO, UUIDv7, temporal constraints, and modern indexing strategies
---

# PostgreSQL 18 Database Architecture

## Overview

PostgreSQL 18 introduces transformational changes: the AIO subsystem delivers 3x I/O performance, native UUIDv7 replaces UUID libraries, and temporal constraints enable bi-temporal data modeling. This skill ensures you leverage these capabilities correctly.

**Core principle:** Design for PostgreSQL 18's strengths. Don't port patterns from older versions or other databases.

**Announce at start:** "I'm applying database-architecture to ensure PostgreSQL 18 best practices."

## When This Skill Applies

This skill is MANDATORY when ANY of these patterns are touched:

| Pattern | Examples |
|---------|----------|
| `**/migrations/**` | migrations/001_create_tables.sql |
| `**/*schema*.sql` | db/schema.sql |
| `**/db/**/*.sql` | db/functions/calculate.sql |
| `**/*index*.sql` | db/indexes.sql |
| `**/models/**` | src/models/user.ts |
| `**/*entity*.ts` | src/entities/order.entity.ts |
| `**/*model*.py` | app/models/product.py |

## PostgreSQL 18 Features to Leverage

### 1. Asynchronous I/O (AIO) Subsystem

PostgreSQL 18's AIO subsystem delivers up to 3x I/O performance improvement. Design schemas to benefit:

```sql
-- Enable read_stream for sequential scans
-- PG18 automatically uses AIO for:
-- - Sequential scans
-- - COPY operations
-- - Vacuum operations
-- - Index builds

-- Design for larger, sequential access patterns
-- AIO benefits sequential operations more than random access
```

**Checklist:**
- [ ] Prefer sequential access patterns in hot paths
- [ ] Design tables to minimize random I/O
- [ ] Use partitioning to enable parallel sequential scans

### 2. Native UUIDv7 Support

PostgreSQL 18 includes native `uuidv7()` function. Use it instead of extensions:

```sql
-- DEPRECATED: Don't use extensions for UUIDs
-- CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
-- SELECT uuid_generate_v4();

-- DEPRECATED: Don't use gen_random_uuid() for new tables
-- SELECT gen_random_uuid();

-- CORRECT: Use native UUIDv7 for new primary keys
CREATE TABLE orders (
  id uuid PRIMARY KEY DEFAULT uuidv7(),
  created_at timestamptz DEFAULT now()
);

-- UUIDv7 benefits:
-- 1. Time-ordered: natural chronological sorting
-- 2. Index-friendly: sequential inserts, no page splits
-- 3. Distributed-safe: no coordination needed
-- 4. Sortable: first 48 bits are millisecond timestamp
```

**Migration pattern for existing tables:**

```sql
-- Add new UUIDv7 column alongside existing
ALTER TABLE legacy_table ADD COLUMN id_v7 uuid DEFAULT uuidv7();

-- Backfill with time-ordered UUIDs (preserves order)
UPDATE legacy_table SET id_v7 = uuidv7() WHERE id_v7 IS NULL;

-- For historical data, generate UUIDs that preserve timestamp order
-- Use application code to generate UUIDv7 from original created_at
```

**Checklist:**
- [ ] All new tables use `uuidv7()` for primary keys
- [ ] No new usage of `uuid-ossp` extension
- [ ] Migration plan for existing `uuid_generate_v4()` columns

### 3. Virtual Generated Columns

PostgreSQL 18 supports virtual (computed-on-read) generated columns:

```sql
-- STORED: Computed on write, stored on disk (PG12+)
ALTER TABLE products ADD COLUMN search_vector tsvector
  GENERATED ALWAYS AS (to_tsvector('english', name || ' ' || description)) STORED;

-- VIRTUAL: Computed on read, no storage (PG18+)
ALTER TABLE orders ADD COLUMN total_with_tax numeric
  GENERATED ALWAYS AS (subtotal * (1 + tax_rate)) VIRTUAL;

-- When to use VIRTUAL:
-- - Simple calculations
-- - Values that would bloat storage
-- - Infrequently accessed computed values
-- - Values dependent on runtime context

-- When to use STORED:
-- - Expensive computations
-- - Indexed columns (virtual columns cannot be indexed directly)
-- - Frequently accessed values
```

**Checklist:**
- [ ] Use VIRTUAL for simple, infrequently indexed calculations
- [ ] Use STORED for indexed computed columns
- [ ] Document why each generated column uses its storage type

### 4. Temporal Constraints (SQL:2011)

PostgreSQL 18 introduces temporal primary keys and foreign keys:

```sql
-- Temporal table with validity period
CREATE TABLE product_prices (
  product_id uuid REFERENCES products(id),
  price numeric NOT NULL,
  valid_from timestamptz NOT NULL,
  valid_to timestamptz NOT NULL,

  -- Temporal primary key: unique product per time period
  PRIMARY KEY (product_id, valid_from, valid_to WITHOUT OVERLAPS)
);

-- Temporal foreign key: reference must be valid at point in time
CREATE TABLE order_items (
  id uuid PRIMARY KEY DEFAULT uuidv7(),
  order_id uuid REFERENCES orders(id),
  product_id uuid,
  ordered_at timestamptz NOT NULL,

  -- Ensures product_id references a valid price at ordered_at time
  FOREIGN KEY (product_id, PERIOD(ordered_at, ordered_at))
    REFERENCES product_prices (product_id, PERIOD(valid_from, valid_to))
);
```

**Bi-temporal pattern:**

```sql
-- Track both validity time AND transaction time
CREATE TABLE contracts (
  id uuid PRIMARY KEY DEFAULT uuidv7(),
  customer_id uuid REFERENCES customers(id),
  terms jsonb NOT NULL,

  -- Validity time: when the contract is effective
  valid_from timestamptz NOT NULL,
  valid_to timestamptz NOT NULL DEFAULT 'infinity',

  -- Transaction time: when we recorded this version
  recorded_at timestamptz NOT NULL DEFAULT now(),
  superseded_at timestamptz NOT NULL DEFAULT 'infinity',

  -- Ensure no overlapping validity periods per customer
  EXCLUDE USING gist (
    customer_id WITH =,
    tstzrange(valid_from, valid_to) WITH &&
  ) WHERE (superseded_at = 'infinity')
);
```

**Checklist:**
- [ ] Use temporal constraints for time-varying data
- [ ] Consider bi-temporal design for audit requirements
- [ ] Use WITHOUT OVERLAPS for validity periods

### 5. Skip Scan on B-tree Indexes

PostgreSQL 18 can skip-scan B-tree indexes, making composite indexes more versatile:

```sql
-- This index now supports queries on BOTH columns
CREATE INDEX idx_orders_status_date ON orders(status, created_at);

-- PG17 and earlier: Only efficient for status queries
SELECT * FROM orders WHERE status = 'pending';

-- PG18: Also efficient for date-only queries (skip scan)
SELECT * FROM orders WHERE created_at > '2026-01-01';
-- Skip scan jumps between status values, checking dates in each
```

**Index design implications:**

```sql
-- Multi-column indexes are now more valuable
-- Put high-cardinality column second for skip scan benefit
CREATE INDEX idx_events_type_user ON events(event_type, user_id);

-- Both of these are now efficient:
SELECT * FROM events WHERE event_type = 'login';
SELECT * FROM events WHERE user_id = 'abc-123';
```

**Checklist:**
- [ ] Review existing indexes for skip-scan opportunities
- [ ] Consider composite indexes that benefit multiple query patterns
- [ ] Put low-cardinality columns first for skip-scan benefit

## Schema Design Principles

### Table Design

```sql
-- Standard table template for PG18
CREATE TABLE entity_name (
  -- Primary key: Always UUIDv7
  id uuid PRIMARY KEY DEFAULT uuidv7(),

  -- Foreign keys: Reference with ON DELETE behavior
  parent_id uuid REFERENCES parent_table(id) ON DELETE CASCADE,

  -- Required fields: NOT NULL with sensible defaults
  status text NOT NULL DEFAULT 'pending',

  -- Timestamps: Always timestamptz, never timestamp
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),

  -- Soft delete: Use validity period, not boolean
  deleted_at timestamptz,  -- NULL = not deleted

  -- JSON data: Use jsonb, never json
  metadata jsonb NOT NULL DEFAULT '{}',

  -- Constraints: Named for clarity
  CONSTRAINT entity_name_status_check CHECK (status IN ('pending', 'active', 'completed'))
);

-- Standard indexes
CREATE INDEX idx_entity_name_parent_id ON entity_name(parent_id);
CREATE INDEX idx_entity_name_created_at ON entity_name(created_at);
CREATE INDEX idx_entity_name_status ON entity_name(status) WHERE deleted_at IS NULL;
```

### Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Tables | snake_case, plural | `order_items` |
| Columns | snake_case | `created_at` |
| Primary keys | `id` | `id uuid` |
| Foreign keys | `{table_singular}_id` | `order_id` |
| Indexes | `idx_{table}_{columns}` | `idx_orders_status` |
| Constraints | `{table}_{purpose}_check` | `orders_amount_check` |
| Functions | snake_case, verb first | `calculate_total()` |

### Partitioning Strategy

```sql
-- Time-based partitioning for large tables
CREATE TABLE events (
  id uuid DEFAULT uuidv7(),
  event_type text NOT NULL,
  payload jsonb NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now()
) PARTITION BY RANGE (created_at);

-- Monthly partitions
CREATE TABLE events_2026_01 PARTITION OF events
  FOR VALUES FROM ('2026-01-01') TO ('2026-02-01');

-- Automated partition creation (use pg_partman or similar)
-- Or create future partitions in migration

-- UUIDv7 benefit: Partition pruning works because UUIDs are time-ordered
-- Queries on id range can prune partitions
```

## Migration Best Practices

### Migration Template

```sql
-- migrations/YYYYMMDDHHMMSS_description.sql

-- Wrap in transaction
BEGIN;

-- Version check
DO $$
BEGIN
  IF current_setting('server_version_num')::int < 180000 THEN
    RAISE EXCEPTION 'Requires PostgreSQL 18 or higher';
  END IF;
END $$;

-- Migration logic here
CREATE TABLE ...;

-- Verify migration
DO $$
BEGIN
  -- Add assertions about expected state
  IF NOT EXISTS (SELECT 1 FROM pg_tables WHERE tablename = 'new_table') THEN
    RAISE EXCEPTION 'Migration verification failed';
  END IF;
END $$;

COMMIT;
```

### Safe Schema Changes

```sql
-- SAFE: Adding nullable column
ALTER TABLE orders ADD COLUMN notes text;

-- SAFE: Adding column with default (PG11+ doesn't rewrite table)
ALTER TABLE orders ADD COLUMN priority int NOT NULL DEFAULT 0;

-- DANGEROUS: Adding NOT NULL to existing column (locks table)
-- Instead, do in steps:
ALTER TABLE orders ADD COLUMN notes_new text;
UPDATE orders SET notes_new = COALESCE(notes, 'none') WHERE notes_new IS NULL;
ALTER TABLE orders ALTER COLUMN notes_new SET NOT NULL;
ALTER TABLE orders DROP COLUMN notes;
ALTER TABLE orders RENAME COLUMN notes_new TO notes;

-- DANGEROUS: Changing column type (rewrites table)
-- Consider: Add new column, migrate data, drop old column

-- SAFE: Creating index concurrently
CREATE INDEX CONCURRENTLY idx_orders_notes ON orders(notes);
-- Note: Cannot be in transaction, requires separate migration step
```

### Zero-Downtime Migration Pattern

```sql
-- Step 1: Add new column (no lock)
ALTER TABLE orders ADD COLUMN new_status text;

-- Step 2: Backfill in batches (application or background job)
UPDATE orders SET new_status = status WHERE new_status IS NULL LIMIT 10000;
-- Repeat until complete

-- Step 3: Add constraints once backfilled
ALTER TABLE orders ALTER COLUMN new_status SET NOT NULL;

-- Step 4: Add new index concurrently
CREATE INDEX CONCURRENTLY idx_orders_new_status ON orders(new_status);

-- Step 5: Update application to use new column
-- Step 6: Drop old column in future migration
```

## Indexing Strategy

### Index Types and Usage

| Index Type | Use Case | Example |
|------------|----------|---------|
| B-tree | Equality, range, sorting | `CREATE INDEX ... ON orders(created_at)` |
| Hash | Equality only (rarely better) | `CREATE INDEX ... USING hash ON lookups(key)` |
| GiST | Ranges, geometric, full-text | `CREATE INDEX ... USING gist ON events(tstzrange(...))` |
| GIN | Arrays, JSONB, full-text | `CREATE INDEX ... USING gin ON docs(metadata)` |
| BRIN | Very large, naturally ordered | `CREATE INDEX ... USING brin ON logs(created_at)` |

### JSONB Indexing

```sql
-- Index specific paths for frequent queries
CREATE INDEX idx_metadata_type ON documents((metadata->>'type'));

-- GIN for flexible key/value queries
CREATE INDEX idx_metadata_gin ON documents USING gin(metadata);

-- GIN with specific operator class for containment queries
CREATE INDEX idx_metadata_path ON documents USING gin(metadata jsonb_path_ops);
-- Supports: metadata @> '{"type": "invoice"}'
-- Smaller index, faster for containment queries
```

### Partial Indexes

```sql
-- Index only active records
CREATE INDEX idx_orders_pending ON orders(created_at)
  WHERE status = 'pending' AND deleted_at IS NULL;

-- Index only non-null values
CREATE INDEX idx_users_email_verified ON users(email)
  WHERE email_verified_at IS NOT NULL;

-- Unique partial index for soft deletes
CREATE UNIQUE INDEX idx_users_email_unique ON users(email)
  WHERE deleted_at IS NULL;
```

### Expression Indexes

```sql
-- Index on function result
CREATE INDEX idx_users_email_lower ON users(lower(email));

-- Index on JSONB expression
CREATE INDEX idx_orders_customer_email ON orders((data->>'customer_email'));

-- Index on date part
CREATE INDEX idx_events_date ON events(date(created_at));
```

## Query Optimization

### Explain Analyze

```sql
-- Always use ANALYZE for accurate timing
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT * FROM orders WHERE status = 'pending';

-- Look for:
-- - Seq Scan on large tables (needs index?)
-- - High actual rows vs estimated rows (stale statistics?)
-- - Buffers: shared hit vs read ratio (memory pressure?)
-- - Loops with high count (N+1 query?)
```

### Statistics Targets

```sql
-- Increase statistics for columns with skewed distributions
ALTER TABLE orders ALTER COLUMN status SET STATISTICS 1000;

-- Force statistics update
ANALYZE orders;

-- Check current statistics
SELECT attname, n_distinct, most_common_vals, most_common_freqs
FROM pg_stats
WHERE tablename = 'orders';
```

### Common Query Patterns

```sql
-- Pagination: Use keyset, not offset
-- BAD:
SELECT * FROM orders ORDER BY created_at LIMIT 20 OFFSET 10000;
-- GOOD:
SELECT * FROM orders
WHERE created_at < $last_created_at
ORDER BY created_at DESC
LIMIT 20;

-- Counting: Use estimates for UI when exact not needed
-- BAD:
SELECT count(*) FROM large_table WHERE status = 'active';
-- GOOD (for UI display):
SELECT reltuples::bigint AS estimate
FROM pg_class WHERE relname = 'large_table';

-- Existence check: Use EXISTS, not COUNT
-- BAD:
SELECT count(*) > 0 FROM orders WHERE user_id = $1;
-- GOOD:
SELECT EXISTS(SELECT 1 FROM orders WHERE user_id = $1);
```

## Database Architecture Artifact

When designing or modifying schema, post this artifact:

```markdown
<!-- DATABASE_ARCHITECTURE:START -->
## Database Architecture Summary

### Tables Modified/Created

| Table | Change | Rationale |
|-------|--------|-----------|
| orders | Created | New e-commerce functionality |
| order_items | Created | Line items for orders |

### PostgreSQL 18 Features Used

- [ ] UUIDv7 primary keys
- [ ] Virtual generated columns
- [ ] Temporal constraints
- [ ] Skip-scan indexes

### Indexes Added

| Table | Index | Type | Purpose |
|-------|-------|------|---------|
| orders | idx_orders_status_date | B-tree | Skip-scan for status and date queries |
| orders | idx_orders_metadata | GIN | JSONB containment queries |

### Migration Safety

- [ ] All migrations are idempotent
- [ ] No table rewrites on production data
- [ ] Indexes created CONCURRENTLY
- [ ] Backward compatible with current application

### Performance Considerations

- [ ] Query patterns documented
- [ ] Index usage verified with EXPLAIN ANALYZE
- [ ] Partition strategy appropriate for data volume
- [ ] Statistics targets adjusted for skewed columns

**Verified At:** [timestamp]
<!-- DATABASE_ARCHITECTURE:END -->
```

## Checklist

Before completing database architecture work:

- [ ] All new tables use UUIDv7 primary keys
- [ ] All timestamps use timestamptz, not timestamp
- [ ] Foreign keys have appropriate ON DELETE behavior
- [ ] Indexes created for all foreign keys
- [ ] Partial indexes used where appropriate
- [ ] Migrations are safe for zero-downtime deployment
- [ ] Query patterns documented and tested with EXPLAIN ANALYZE
- [ ] PostgreSQL 18 features leveraged where beneficial
- [ ] Architecture artifact posted to issue

## Integration

This skill integrates with:
- `postgres-rls` - RLS is layered on top of schema design
- `postgis` - Spatial data types and indexes
- `timescaledb` - Time-series extensions and hypertables
- `local-service-testing` - Test migrations against real PostgreSQL

## References

- [PostgreSQL 18 Release Notes](https://www.postgresql.org/docs/18/release-18.html)
- [PostgreSQL 18 New Features Overview](https://www.percona.com/blog/postgresql-18-highlights/)
- [UUIDv7 RFC 9562](https://www.rfc-editor.org/rfc/rfc9562.html)
- [Temporal Tables SQL:2011](https://en.wikipedia.org/wiki/Temporal_database)
