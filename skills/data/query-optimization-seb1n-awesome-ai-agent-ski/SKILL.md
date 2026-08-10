---
name: query-optimization
description: Diagnose and optimize existing slow SQL queries using execution plans, indexing strategies, query rewriting, and ORM tuning. Use when the user provides a query, performance symptom, or EXPLAIN plan; use sql-query-generation when creating a new query from requirements.
license: MIT
metadata:
  author: AI Agent Skills Community
  version: 1.0.0
---

# Query Optimization

This skill enables an AI agent to diagnose and fix slow database queries. The agent uses EXPLAIN/EXPLAIN ANALYZE to interpret query execution plans, identifies missing indexes and inefficient scan patterns, rewrites queries to eliminate performance bottlenecks, detects and resolves N+1 query problems in ORMs, and recommends monitoring tools to track query performance over time. The focus is on practical, measurable improvements with before-and-after evidence.

## Workflow

1. **Identify the slow query:** Collect the problematic query from slow query logs, application performance monitoring (APM) tools, or user reports. Note the current execution time, the table sizes involved, and how frequently the query runs. High-frequency slow queries should be prioritized over rare ones.

2. **Analyze the execution plan:** Run `EXPLAIN ANALYZE` (PostgreSQL) or `EXPLAIN FORMAT=JSON` (MySQL) on the query to obtain the actual execution plan. Look for sequential scans on large tables, nested loop joins with high row estimates, sort operations on unindexed columns, and large gaps between estimated and actual row counts.

3. **Identify optimization opportunities:** Based on the plan, identify concrete fixes: add indexes for columns in WHERE, JOIN, and ORDER BY clauses; rewrite subqueries as JOINs; replace `SELECT *` with specific columns; add LIMIT clauses where appropriate; use covering indexes to avoid table lookups; eliminate redundant or duplicate conditions.

4. **Apply optimizations:** Create the necessary indexes, rewrite the query, or adjust ORM usage. For N+1 problems, switch from lazy loading to eager loading (e.g., `select_related`/`prefetch_related` in Django, `include` in Prisma, `joinedload` in SQLAlchemy). Apply one change at a time to measure each improvement independently.

5. **Measure and validate:** Re-run `EXPLAIN ANALYZE` on the optimized query and compare execution time, rows scanned, and plan structure against the original. Verify that the query returns identical results. Check that new indexes do not degrade write performance beyond acceptable thresholds.

6. **Set up ongoing monitoring:** Configure slow query logging with appropriate thresholds (e.g., 100ms for PostgreSQL via `log_min_duration_statement`). Integrate with monitoring tools like pg_stat_statements, Datadog, or Grafana to track query performance trends and catch regressions early.

## Supported Technologies

- **PostgreSQL:** EXPLAIN ANALYZE, pg_stat_statements, pg_stat_user_indexes, auto_explain
- **MySQL:** EXPLAIN FORMAT=JSON, Performance Schema, slow query log, pt-query-digest
- **ORMs:** SQLAlchemy, Django ORM, Prisma, ActiveRecord, Sequelize, TypeORM
- **Monitoring:** pganalyze, Datadog APM, New Relic, Grafana + Prometheus

## Usage

Provide the slow SQL query (or describe the ORM operation) along with the database type and approximate table sizes. If possible, include the current EXPLAIN output. The agent will analyze the plan, recommend specific optimizations, and provide the rewritten query with index creation statements. The agent can also review ORM code for N+1 patterns and suggest eager loading fixes.

## Examples

### Example 1: Optimizing a Slow JOIN Query

**Problem:** A report query joining orders with users and products takes 4.2 seconds on a table with 500K orders.

**Original query and EXPLAIN:**

```sql
EXPLAIN ANALYZE
SELECT *
FROM orders o
JOIN users u ON o.user_id = u.id
JOIN order_items oi ON oi.order_id = o.id
JOIN products p ON oi.product_id = p.id
WHERE o.status = 'shipped'
  AND o.ordered_at >= '2025-01-01';
```

```
Nested Loop  (cost=0.00..98452.30 rows=12340 width=892) (actual time=0.08..4201.33 rows=11842 loops=1)
  -> Seq Scan on orders o  (cost=0.00..15420.00 rows=24500 width=64) (actual time=0.04..1823.12 rows=24312 loops=1)
       Filter: ((status = 'shipped') AND (ordered_at >= '2025-01-01'))
       Rows Removed by Filter: 475688
  -> Index Scan using order_items_order_id_idx on order_items oi  (...)
Planning Time: 0.45 ms
Execution Time: 4201.88 ms
```

**Diagnosis:** Sequential scan on `orders` (500K rows) filtering by `status` and `ordered_at`. No composite index exists for these filter columns. Also selecting all columns when only a subset is needed.

**Fix — add a composite index and rewrite the query:**

```sql
-- Create composite index matching the WHERE clause
CREATE INDEX idx_orders_status_ordered_at ON orders(status, ordered_at);

-- Rewrite query with specific columns
EXPLAIN ANALYZE
SELECT o.id AS order_id, u.full_name, u.email,
       p.name AS product_name, oi.quantity, oi.unit_price,
       o.ordered_at
FROM orders o
JOIN users u ON o.user_id = u.id
JOIN order_items oi ON oi.order_id = o.id
JOIN products p ON oi.product_id = p.id
WHERE o.status = 'shipped'
  AND o.ordered_at >= '2025-01-01';
```

**Optimized EXPLAIN:**

```
Nested Loop  (cost=1.12..3842.56 rows=12340 width=198) (actual time=0.06..87.42 rows=11842 loops=1)
  -> Index Scan using idx_orders_status_ordered_at on orders o  (cost=0.42..892.15 rows=24500 width=24) (actual time=0.03..12.68 rows=24312 loops=1)
       Index Cond: ((status = 'shipped') AND (ordered_at >= '2025-01-01'))
  -> Index Scan using order_items_order_id_idx on order_items oi  (...)
Planning Time: 0.52 ms
Execution Time: 88.04 ms
```

**Result:** Execution time dropped from 4,201ms to 88ms (48x improvement) by replacing a sequential scan with an index scan and reducing the data transferred with specific column selection.

### Example 2: Fixing N+1 Queries in a Django ORM Application

**Problem:** A view listing 100 orders with their user names and product details generates 201 SQL queries (1 for orders + 100 for users + 100 for products) and takes 1.8 seconds.

**Before — N+1 pattern:**

```python
# views.py — Triggers N+1 queries
def order_list(request):
    orders = Order.objects.filter(status="shipped").order_by("-ordered_at")[:100]
    results = []
    for order in orders:
        results.append({
            "id": order.id,
            "customer": order.user.full_name,       # Lazy load: 1 query per order
            "items": [
                {"product": item.product.name, "qty": item.quantity}
                for item in order.items.all()        # Lazy load: 1 query per order
            ],
        })
    return JsonResponse(results, safe=False)
```

**Django Debug Toolbar output:** 201 queries in 1,823ms.

**After — eager loading with select_related and prefetch_related:**

```python
# views.py — Fixed with eager loading
def order_list(request):
    orders = (
        Order.objects
        .filter(status="shipped")
        .select_related("user")                      # JOIN for user (1:1/FK)
        .prefetch_related("items__product")           # Prefetch items + products (1:N)
        .order_by("-ordered_at")[:100]
    )
    results = []
    for order in orders:
        results.append({
            "id": order.id,
            "customer": order.user.full_name,         # No extra query
            "items": [
                {"product": item.product.name, "qty": item.quantity}
                for item in order.items.all()          # No extra query
            ],
        })
    return JsonResponse(results, safe=False)
```

**Django Debug Toolbar output:** 3 queries in 42ms.

**Result:** Query count dropped from 201 to 3, and response time dropped from 1,823ms to 42ms (43x improvement). `select_related` uses a SQL JOIN for the user FK, while `prefetch_related` issues a single IN query for all order items and their products.

## Best Practices

- **Always use EXPLAIN ANALYZE, not just EXPLAIN** — the `ANALYZE` variant runs the query and shows actual row counts and timings, which often differ significantly from estimates and reveal the real bottleneck.
- **Create composite indexes matching your WHERE + ORDER BY pattern** — a composite index on `(status, ordered_at)` is far more effective than separate indexes on each column, because the database can use a single index range scan.
- **Avoid SELECT * in production queries** — selecting all columns forces the database to read wider rows, increases I/O, and prevents the use of covering indexes. Always specify only the columns you need.
- **Fix N+1 problems at the ORM level** — use `select_related` (Django), `joinedload` (SQLAlchemy), `include` (Prisma), or `includes` (ActiveRecord) to batch related-object loading into one or two queries instead of hundreds.
- **Monitor query performance continuously** — enable `pg_stat_statements` in PostgreSQL or Performance Schema in MySQL to track the most time-consuming queries by total execution time, not just individual query duration.
- **Test index impact on writes** — every index speeds up reads but slows down writes (INSERT, UPDATE, DELETE). Benchmark write-heavy operations after adding indexes to ensure the trade-off is acceptable.

## Edge Cases

- **Statistics drift causing bad plans:** When table data changes significantly (e.g., after a large data import), the query planner may use outdated statistics. Run `ANALYZE` (PostgreSQL) or `ANALYZE TABLE` (MySQL) to refresh statistics and get accurate plans.
- **Index bloat on high-churn tables:** Tables with frequent updates and deletes can develop bloated indexes that degrade performance. Schedule periodic `REINDEX` (PostgreSQL) or `OPTIMIZE TABLE` (MySQL) to reclaim space.
- **Correlated subqueries hiding in views:** A query that looks simple may reference a view containing a correlated subquery that executes once per row. Always expand views in your EXPLAIN analysis to see the full execution plan.
- **Parameter sniffing / plan caching:** A query plan cached for one parameter value may perform poorly for another. In PostgreSQL, use `PREPARE`/`EXECUTE` or set `plan_cache_mode = force_custom_plan` for queries with highly variable parameter selectivity.
- **ORM-generated queries with unnecessary JOINs:** ORMs sometimes generate LEFT JOINs when INNER JOINs would suffice, or add unnecessary subqueries. Use `QuerySet.query` (Django) or `.toSQL()` (Knex) to inspect the actual SQL and override with raw queries when the ORM's output is suboptimal.
