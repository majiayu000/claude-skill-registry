---
name: postgres-optimization
description: Unconventional PostgreSQL optimization techniques
license: MIT
tier: 2
allowed-tools:
  - read_file
  - write_file
  - run_terminal_cmd
  - grep
related: [debugging, plan-then-execute, robust-first]
tags: [moollm, database, postgresql, performance, optimization, indexing]
inputs:
  query:
    type: string
    required: false
    description: "Query to optimize"
  table:
    type: string
    required: false
    description: "Table to analyze"
outputs:
  - OPTIMIZATION.md
  - EXPLAIN-ANALYSIS.txt
credits:
  source:
    title: "Unconventional PostgreSQL Optimizations"
    author: "Haki Benita"
    url: "https://hakibenita.com/postgresql-unconventional-optimizations"
---

# 🐘 PostgreSQL Optimization

> **"Beyond 'just add an index' — creative solutions for real performance problems."**

Unconventional optimization techniques for PostgreSQL that go beyond standard DBA playbooks.

## Purpose

When conventional approaches fall short — query rewrites, adding indexes, VACUUM, ANALYZE — these techniques offer creative solutions:

- Eliminate impossible query scans with constraint exclusion
- Reduce index size with function-based indexes
- Enforce uniqueness with hash indexes instead of B-Trees

## When to Use

- Ad-hoc query environments where users make mistakes
- Large indexes approaching table size
- Uniqueness constraints on large text values (URLs, documents)
- Timestamp columns queried at coarser granularity

---

## Technique 1: Constraint Exclusion

### The Problem

Check constraints prevent invalid data, but PostgreSQL doesn't use them to optimize queries by default.

```sql
CREATE TABLE users (
    id INT PRIMARY KEY,
    username TEXT NOT NULL,
    plan TEXT NOT NULL,
    CONSTRAINT plan_check CHECK (plan IN ('free', 'pro'))
);
```

An analyst writes:

```sql
SELECT * FROM users WHERE plan = 'Pro';  -- Note: capital P
```

Despite the check constraint making this condition impossible, PostgreSQL scans the entire table.

### The Solution

```sql
SET constraint_exclusion TO 'on';
```

With constraint exclusion enabled:

```sql
EXPLAIN ANALYZE SELECT * FROM users WHERE plan = 'Pro';
```

```
Result  (cost=0.00..0.00 rows=0 width=0)
  One-Time Filter: false
Execution Time: 0.008 ms
```

PostgreSQL recognizes the condition contradicts the constraint and skips the scan entirely.

### When to Enable

| Environment | Recommendation |
|-------------|----------------|
| OLTP production | Leave as 'partition' (default) |
| BI / Data Warehouse | Set to 'on' |
| Ad-hoc query tools | Set to 'on' |
| Reporting databases | Set to 'on' |

### Tradeoffs

- **Benefit**: Eliminates impossible query scans
- **Cost**: Extra planning overhead evaluating constraints against conditions
- **Default**: 'partition' — only used for partition pruning

---

## Technique 2: Function-Based Indexes for Lower Cardinality

### The Problem

You have a sales table with timestamps:

```sql
CREATE TABLE sale (
    id INT PRIMARY KEY,
    sold_at TIMESTAMPTZ NOT NULL,
    charged INT NOT NULL
);
```

Analysts query by day:

```sql
SELECT date_trunc('day', sold_at AT TIME ZONE 'UTC'), SUM(charged)
FROM sale
WHERE sold_at BETWEEN '2025-01-01 UTC' AND '2025-02-01 UTC'
GROUP BY 1;
```

You add a B-Tree index on `sold_at` — 214 MB for a 160 MB table. The index is almost half the table size!

### The Solution

Index only what queries need:

```sql
CREATE INDEX sale_sold_at_date_ix 
ON sale((date_trunc('day', sold_at AT TIME ZONE 'UTC'))::date);
```

| Index | Size |
|-------|------|
| `sale_sold_at_ix` (full timestamp) | 214 MB |
| `sale_sold_at_date_ix` (date only) | 66 MB |

The function-based index is **3x smaller** because:
- Dates are 4 bytes vs 8 bytes for timestamptz
- Fewer distinct values enable deduplication

### The Discipline Problem

Function-based indexes require exact expression match:

```sql
-- Uses the index ✓
WHERE date_trunc('day', sold_at AT TIME ZONE 'UTC')::date 
      BETWEEN '2025-01-01' AND '2025-01-31'

-- Does NOT use the index ✗
WHERE (sold_at AT TIME ZONE 'UTC')::date 
      BETWEEN '2025-01-01' AND '2025-01-31'
```

### Solution: Virtual Generated Columns (PostgreSQL 18+)

```sql
ALTER TABLE sale ADD sold_at_date DATE
GENERATED ALWAYS AS (date_trunc('day', sold_at AT TIME ZONE 'UTC'));
```

Now queries use the virtual column:

```sql
SELECT sold_at_date, SUM(charged)
FROM sale
WHERE sold_at_date BETWEEN '2025-01-01' AND '2025-01-31'
GROUP BY 1;
```

**Benefits:**
- Smaller index
- Faster queries
- No discipline required — column guarantees correct expression
- No ambiguity about timezones

**Limitation:** PostgreSQL 18 doesn't support indexes directly on virtual columns (yet).

---

## Technique 3: Hash Index for Uniqueness

### The Problem

You have a table with large URLs:

```sql
CREATE TABLE urls (
    id INT PRIMARY KEY,
    url TEXT NOT NULL,
    data JSON
);
```

You add a unique B-Tree index:

```sql
CREATE UNIQUE INDEX urls_url_unique_ix ON urls(url);
```

| Size |
|------|
| Table: 160 MB |
| B-Tree index: 154 MB |

The index is almost as large as the table because B-Tree stores actual values in leaf blocks.

### The Solution

Use an exclusion constraint with a hash index:

```sql
ALTER TABLE urls 
ADD CONSTRAINT urls_url_unique_hash 
EXCLUDE USING HASH (url WITH =);
```

| Index | Size |
|-------|------|
| B-Tree | 154 MB |
| Hash | 32 MB |

The hash index is **5x smaller** because it stores hash values, not the actual URLs.

### Uniqueness Is Enforced

```sql
INSERT INTO urls (id, url) VALUES (1000002, 'https://example.com');
-- ERROR: conflicting key value violates exclusion constraint
```

### Queries Still Fast

```sql
EXPLAIN ANALYZE SELECT * FROM urls WHERE url = 'https://example.com';
```

```
Index Scan using urls_url_unique_hash on urls
Execution Time: 0.022 ms  -- Faster than B-Tree's 0.046 ms!
```

### Limitations

| Feature | B-Tree Unique | Hash Exclusion |
|---------|--------------|----------------|
| Foreign key reference | ✓ | ✗ |
| `ON CONFLICT (column)` | ✓ | ✗ |
| `ON CONFLICT ON CONSTRAINT` | ✓ | ✓ (DO NOTHING only) |
| `ON CONFLICT DO UPDATE` | ✓ | ✗ |
| `MERGE` | ✓ | ✓ |

### Workaround: Use MERGE

Instead of `INSERT ... ON CONFLICT DO UPDATE`:

```sql
MERGE INTO urls t
USING (VALUES (1000004, 'https://example.com')) AS s(id, url)
ON t.url = s.url
WHEN MATCHED THEN UPDATE SET id = s.id
WHEN NOT MATCHED THEN INSERT (id, url) VALUES (s.id, s.url);
```

---

## Quick Reference

### Diagnostic Queries

**Check index sizes:**
```sql
\di+ table_*
```

**Compare index to table size:**
```sql
SELECT 
    relname AS name,
    pg_size_pretty(pg_relation_size(oid)) AS size
FROM pg_class 
WHERE relname LIKE 'your_table%'
ORDER BY pg_relation_size(oid) DESC;
```

**Check constraint_exclusion setting:**
```sql
SHOW constraint_exclusion;
```

### Decision Tree

```
Is the query scanning impossibly?
├── Yes → Enable constraint_exclusion
└── No
    ↓
Is index nearly as large as table?
├── Yes, timestamp column → Function-based index on date
├── Yes, large text column → Hash exclusion constraint
└── No → Standard B-Tree is fine
```

---

## Commands

| Command | Action |
|---------|--------|
| `ANALYZE [table]` | Analyze query performance |
| `CHECK-CONSTRAINTS` | Evaluate constraint exclusion opportunity |
| `LOWER-CARDINALITY` | Find function-based index opportunities |
| `HASH-UNIQUE` | Evaluate hash index for large values |
| `COMPARE-INDEXES` | Compare index sizes and performance |

---

## Integration

| Direction | Skill | Relationship |
|-----------|-------|--------------|
| ← | [debugging](../debugging/) | Query debugging leads here |
| → | [plan-then-execute](../plan-then-execute/) | Systematic optimization |
