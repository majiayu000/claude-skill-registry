---
name: sql-query-generation
description: Generate SQL queries from natural-language requirements using SELECT, JOIN, GROUP BY, window functions, CTEs, and subqueries. Use when the user needs a new query from a business question or schema; use query-optimization when an existing query or execution plan is slow.
license: MIT
metadata:
  author: awesome-ai-agent-skills
  version: 1.0.0
---

# SQL Query Generation

This skill enables an AI agent to translate natural language questions into correct, efficient SQL queries. The agent maps user intent to the appropriate query constructs — joins, aggregations, window functions, CTEs, and subqueries — while respecting the target database schema. It also analyzes query performance with EXPLAIN plans and recommends optimizations such as indexing, predicate pushdown, and query restructuring.

## Workflow

1. **Parse the natural language request.** Extract the analytical intent: what metric is being asked for, which entities are involved, what filters apply, and how results should be ordered or grouped. Distinguish between requests for aggregated summaries versus row-level detail.

2. **Map to the database schema.** Identify the relevant tables and columns from the schema. Resolve ambiguous references (e.g., "sales" could mean the `orders` table or the `revenue` column). Determine the join path between tables using foreign key relationships, avoiding unnecessary joins that inflate result sets.

3. **Select the appropriate query constructs.** Choose between simple aggregation, window functions, CTEs, or subqueries based on complexity. Use CTEs for multi-step calculations to improve readability. Use window functions for running totals, rankings, and comparisons within partitions. Prefer explicit JOINs over implicit comma-separated joins.

4. **Generate the SQL query.** Write syntactically correct SQL with consistent formatting: uppercase keywords, lowercase identifiers, aliased tables, and indented clauses. Include comments for complex logic. Always specify column aliases for computed expressions.

5. **Validate and optimize.** Run EXPLAIN (or EXPLAIN ANALYZE) on the generated query to inspect the execution plan. Look for full table scans, hash joins on large tables, and sort operations on unindexed columns. Recommend indexes or query rewrites when the estimated cost is high.

6. **Return results with explanation.** Present the query alongside a plain-language explanation of what it does, the expected output format, and any assumptions made about the schema or data.

## Supported Technologies

- **PostgreSQL** — CTEs, window functions, LATERAL joins, EXPLAIN ANALYZE
- **MySQL** — common table expressions (8.0+), window functions (8.0+), EXPLAIN FORMAT=JSON
- **SQLite** — lightweight queries, window functions (3.25+)
- **SQL Server** — T-SQL extensions, cross apply, query store analysis
- **BigQuery** — STRUCT/ARRAY types, QUALIFY clause, slot-based cost estimation

## Usage

Provide the agent with a natural language question and the database schema (as DDL, a schema diagram, or a list of tables and columns). Optionally specify the target SQL dialect, any performance constraints, and whether you want the EXPLAIN analysis included.

## Examples

### Example 1: Complex analytics query from natural language

**Request:** "Show the top 5 customers by total spending in the last 12 months, along with their most frequently ordered product category and how their spending compares to the previous 12-month period."

```sql
WITH current_period AS (
    SELECT
        c.customer_id,
        c.customer_name,
        SUM(oi.quantity * oi.unit_price) AS total_spent,
        COUNT(DISTINCT o.order_id) AS order_count
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    JOIN order_items oi ON o.order_id = oi.order_id
    WHERE o.order_date >= CURRENT_DATE - INTERVAL '12 months'
    GROUP BY c.customer_id, c.customer_name
),
previous_period AS (
    SELECT
        c.customer_id,
        SUM(oi.quantity * oi.unit_price) AS prev_total_spent
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    JOIN order_items oi ON o.order_id = oi.order_id
    WHERE o.order_date >= CURRENT_DATE - INTERVAL '24 months'
      AND o.order_date < CURRENT_DATE - INTERVAL '12 months'
    GROUP BY c.customer_id
),
top_categories AS (
    SELECT DISTINCT ON (c.customer_id)
        c.customer_id,
        pc.category_name AS favorite_category,
        COUNT(*) AS category_orders
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    JOIN order_items oi ON o.order_id = oi.order_id
    JOIN products p ON oi.product_id = p.product_id
    JOIN product_categories pc ON p.category_id = pc.category_id
    WHERE o.order_date >= CURRENT_DATE - INTERVAL '12 months'
    GROUP BY c.customer_id, pc.category_name
    ORDER BY c.customer_id, COUNT(*) DESC
)
SELECT
    cp.customer_name,
    cp.total_spent,
    cp.order_count,
    tc.favorite_category,
    pp.prev_total_spent,
    ROUND(
        (cp.total_spent - COALESCE(pp.prev_total_spent, 0))
        / NULLIF(pp.prev_total_spent, 0) * 100, 1
    ) AS spending_change_pct
FROM current_period cp
LEFT JOIN previous_period pp ON cp.customer_id = pp.customer_id
LEFT JOIN top_categories tc ON cp.customer_id = tc.customer_id
ORDER BY cp.total_spent DESC
LIMIT 5;

-- Expected output:
-- customer_name | total_spent | order_count | favorite_category | prev_total_spent | spending_change_pct
-- Acme Corp     | 284,500.00  | 47          | Electronics       | 198,200.00       | 43.5
-- GlobalTech    | 231,800.00  | 38          | Software          | 245,100.00       | -5.4
-- ...
```

### Example 2: Optimizing a slow query with EXPLAIN analysis

**Original slow query** (takes 12.4 seconds on 5M rows):

```sql
SELECT product_name, SUM(quantity * unit_price) AS revenue
FROM order_items oi, products p, orders o
WHERE oi.product_id = p.product_id
  AND oi.order_id = o.order_id
  AND o.order_date BETWEEN '2024-01-01' AND '2024-12-31'
GROUP BY product_name
ORDER BY revenue DESC;
```

**EXPLAIN ANALYZE output (problem indicators):**

```
Seq Scan on orders o  (cost=0.00..98456.00 rows=1245000)
  Filter: (order_date >= '2024-01-01' AND order_date <= '2024-12-31')
  Rows Removed by Filter: 3755000
Hash Join  (cost=98456.00..245678.00 rows=3200000)
Sort  (cost=312456.00..312460.00 rows=8500)
  Sort Method: external merge  Disk: 4096kB
```

**Issues identified:**
1. Sequential scan on `orders` — no index on `order_date`
2. Implicit join syntax hides join order from optimizer
3. Sort spilling to disk due to insufficient `work_mem`

**Optimized query:**

```sql
-- Step 1: Create index (one-time)
CREATE INDEX idx_orders_date ON orders (order_date)
    INCLUDE (order_id);

-- Step 2: Rewrite with explicit joins and date index hint
SELECT
    p.product_name,
    SUM(oi.quantity * oi.unit_price) AS revenue
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id
WHERE o.order_date BETWEEN '2024-01-01' AND '2024-12-31'
GROUP BY p.product_name
ORDER BY revenue DESC;

-- After optimization: 0.34 seconds (36x faster)
-- EXPLAIN now shows:
-- Index Scan on idx_orders_date (rows=1245000, actual=1243892)
-- Merge Join (cost reduced by 85%)
-- Sort Method: quicksort  Memory: 512kB
```

## Best Practices

- Always use explicit JOIN syntax instead of comma-separated implicit joins — it makes intent clear and prevents accidental cross joins.
- Alias every table and every computed column for readability and to avoid ambiguity in complex queries.
- Use CTEs to break complex queries into named, logical steps rather than deeply nesting subqueries.
- Filter early: place WHERE conditions on the driving table to reduce the dataset before joins amplify row counts.
- Prefer `COUNT(DISTINCT col)` over `COUNT(*)` on joined tables to avoid inflated counts from one-to-many relationships.
- Always test generated queries against the actual schema before presenting them as final — column names and types in natural language descriptions often differ from the real DDL.

## Edge Cases

- **Ambiguous column names.** When multiple tables have a column with the same name (e.g., `id`, `name`, `status`), always qualify with the table alias. Prompt the user for clarification if the natural language request is genuinely ambiguous.
- **NULL handling in aggregations.** `SUM`, `AVG`, and `COUNT(col)` silently ignore NULLs. When NULLs are meaningful (e.g., "no sale"), use `COALESCE(col, 0)` before aggregating and note the assumption.
- **Division by zero in calculated metrics.** Wrap denominators with `NULLIF(denominator, 0)` to return NULL instead of an error, then handle the NULL in the presentation layer.
- **Date/time zone mismatches.** When filtering by date on a timestamp column, be explicit about boundaries: use `>= '2024-01-01' AND < '2025-01-01'` instead of `BETWEEN`, which includes the end boundary's midnight.
- **Very large result sets.** Always include `LIMIT` in exploratory queries. For production queries, add pagination with `OFFSET`/`FETCH` or keyset pagination for better performance on deep pages.
