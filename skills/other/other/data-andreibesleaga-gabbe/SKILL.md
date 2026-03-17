---
name: sql-optimization
description: Query tuning, indexing strategies, and EXPLAIN plan analysis.
role: eng-database
triggers:
  - slow query
  - optimize sql
  - index
  - explain analyze
  - n+1
---

# sql-optimization Skill

This skill focuses on ensuring database interactions are performant and scalable.

## 1. The Golden Rule: Indexing
- **Primary Keys**: Always indexed by default (B-Tree).
- **Foreign Keys**: MUST be indexed manually in most DBs (Postgres/MySQL) to avoid full table scans on joins.
- **Where Clauses**: Columns used in `WHERE`, `ORDER BY`, `GROUP BY` need indexes.
- **Composite Indexes**: Order matters! `(last_name, first_name)` supports lookup by `last_name` OR `last_name + first_name`, but NOT by `first_name` alone.

## 2. Analyzing Queries (`EXPLAIN ANALYZE`)

Always run `EXPLAIN ANALYZE` on suspect queries.

| Output Term | Meaning | Action |
|---|---|---|
| **Seq Scan / Full Table Scan** | Reading every row. | **Bad** (unless table is tiny). Add an index. |
| **Index Scan** | Reading index + looking up heap. | **Good**. |
| **Index Only Scan** | Reading only index. | **Best**. (Covering Index). |
| **Nested Loop** | Looping for joins. | Fine for small datasets. Bad for large. |
| **Hash Join** | Building hash table for join. | Good for large datasets. |

## 3. Implementation Patterns

### 1. Select Only What You Need
- **Bad**: `SELECT * FROM users`
- **Good**: `SELECT id, name FROM users`
- Reason: Reduces IO, network payload, and memory usage.

### 2. Solve the N+1 Problem
- **Problem**: Fetching 100 posts, then running 100 queries to get authors.
- **Fix**: Use `JOIN` or eager loading (ORM specific: `include`, `with`).
- **Detection**: Use logs or APM query counts.

### 3. Pagination
- **Offset/Limit**: `OFFSET 1000000` is slow (DB scans 1M rows then discards).
- **Cursor/Keyset**: `WHERE id > last_seen_id LIMIT 10`. O(1) performance.

### 4. Transactions
- Keep them **short**.
- Don't make external API calls inside a DB transaction (holds locks).

## 4. Schema Optimization
- **Normalization (3NF)**: Reduces redundancy, ensures integrity. Good for write-heavy.
- **Denormalization**: Adds redundancy for read speed (e.g., storing `author_name` on `posts` table).
- **Data Types**: Use the smallest needed type.
  - `VARCHAR(255)` vs `TEXT` (Postgres treats similar, MySQL differs).
  - `INT` vs `BIGINT`.
  - `JSONB` (Postgres) for unstructured data, but don't overuse it.

## 5. Maintenance
- Run `VACUUM ANALYZE` (Postgres) regularly to update planner statistics.
- Monitor index usage. Remove unused indexes (they slow down writes).
