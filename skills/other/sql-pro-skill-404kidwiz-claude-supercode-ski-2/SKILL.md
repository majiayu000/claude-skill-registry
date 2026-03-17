---
name: sql-pro
description: Use when user needs SQL development, database design, query optimization, performance tuning, or database administration across PostgreSQL, MySQL, SQL Server, and Oracle platforms.
---

# SQL Pro

## Purpose

Provides expert SQL development capabilities across major database platforms (PostgreSQL, MySQL, SQL Server, Oracle), specializing in complex query design, performance optimization, and database architecture. Masters ANSI SQL standards, platform-specific optimizations, and modern data patterns with focus on efficiency and scalability.

## When to Use

- Writing complex SQL queries with joins, CTEs, window functions, or recursive queries
- Designing database schema for new application or refactoring existing schema
- Optimizing slow SQL queries with execution plan analysis
- Data migration between different database platforms (MySQL → PostgreSQL)
- Implementing stored procedures, functions, or triggers
- Building analytical reports with advanced aggregations and window functions
- Translating business requirements into SQL query logic
- Cross-platform SQL compatibility issues (different dialects)

## Quick Start

**Invoke this skill when:**
- Writing complex queries with CTEs, window functions, or recursive patterns
- Designing or refactoring database schemas
- Optimizing slow queries with execution plan analysis
- Migrating data between different database platforms
- Implementing stored procedures, functions, or triggers
- Building analytical reports with advanced aggregations

**Do NOT invoke when:**
- PostgreSQL-specific features needed → Use postgres-pro
- MySQL-specific administration → Use database-administrator
- Simple CRUD operations → Use backend-developer
- ORM query patterns → Use appropriate language skill

## Decision Framework

### CTE vs Subquery vs JOIN Decision Tree

```
Query Requirement Analysis
│
├─ Need to reference result multiple times?
│  └─ YES → Use CTE (avoids duplicate subquery evaluation)
│     WITH user_totals AS (SELECT ...)
│     SELECT * FROM user_totals WHERE ...
│     UNION ALL
│     SELECT * FROM user_totals WHERE ...
│
├─ Recursive data traversal (hierarchy, graph)?
│  └─ YES → Use Recursive CTE (ONLY option for recursion)
│     WITH RECURSIVE tree AS (
│       SELECT ... -- anchor
│       UNION ALL
│       SELECT ... FROM tree ... -- recursive
│     )
│
├─ Simple lookup or filter?
│  └─ Use JOIN (most optimizable by query planner)
│     SELECT u.*, o.total
│     FROM users u
│     JOIN orders o ON u.id = o.user_id
│
├─ Correlated subquery in WHERE clause?
│  ├─ Checking existence → Use EXISTS (stops at first match)
│  │  WHERE EXISTS (SELECT 1 FROM orders WHERE user_id = u.id)
│  │
│  └─ Value comparison → Use JOIN instead
│     -- BAD: WHERE (SELECT COUNT(*) FROM orders WHERE user_id = users.id) > 5
│     -- GOOD: JOIN (SELECT user_id, COUNT(*) as cnt FROM orders GROUP BY user_id)
│
└─ Readability vs Performance trade-off?
   ├─ Complex logic, readability critical → CTE
   │  (Easier to understand, debug, maintain)
   │
   └─ Performance critical, simple logic → Subquery or JOIN
      (Query planner can inline and optimize)
```

### Window Function vs GROUP BY Decision Matrix

| Requirement | Solution | Example |
|------------|----------|---------|
| Need aggregation + row-level detail | Window function | `SELECT name, salary, AVG(salary) OVER () as avg_salary FROM employees` |
| Only aggregated results needed | GROUP BY | `SELECT dept, AVG(salary) FROM employees GROUP BY dept` |
| Ranking/row numbering | Window function (ROW_NUMBER, RANK, DENSE_RANK) | `ROW_NUMBER() OVER (ORDER BY sales DESC)` |
| Running totals / moving averages | Window function with frame | `SUM(amount) OVER (ORDER BY date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)` |
| LAG/LEAD (access previous/next rows) | Window function | `LAG(price, 1) OVER (ORDER BY date) as prev_price` |
| Percentile / NTILE | Window function | `NTILE(4) OVER (ORDER BY score) as quartile` |
| Simple count/sum/avg by group | GROUP BY (more efficient) | `SELECT category, COUNT(*) FROM products GROUP BY category` |

### Red Flags → Escalate to Oracle

| Observation | Why Escalate | Example |
|------------|--------------|---------|
| Cartesian product in execution plan | Unintended cross join causing exponential rows | "Query returning millions of rows" |
| Complex multi-level recursive CTE performance | Advanced optimization needed | "Recursive CTE traversing 10+ levels with 100K nodes" |
| Cross-platform migration with incompatible features | Platform-specific feature mapping | "Migrating Oracle CONNECT BY to PostgreSQL recursive CTE" |
| Query with 10+ joins and complex logic | Architecture smell, potential redesign | "Single query joining 15 tables" |
| Temporal query with complex time-series logic | Advanced analytical pattern | "SCD Type 2 with historical snapshots" |

## Core Capabilities

### Advanced Query Patterns
- Common Table Expressions (CTEs) and recursive queries
- Window functions: ROW_NUMBER, RANK, LEAD, LAG, aggregate windows
- PIVOT/UNPIVOT operations for data transformation
- Hierarchical queries for tree/graph structures
- Temporal queries for time-based analysis

### Query Optimization
- Execution plan analysis and interpretation
- Index selection strategies and covering indexes
- Statistics management and maintenance
- Query hints and plan guides (when necessary)
- Parallel query execution tuning

### Index Design Patterns
- Clustered vs. non-clustered indexes
- Covering indexes for query optimization
- Filtered/partial indexes for selective queries
- Function-based/indexes on expressions
- Composite index column ordering

## Quality Checklist

**Query Performance:**
- [ ] Execution time meets requirements (OLTP: <100ms, Analytics: <5s)
- [ ] EXPLAIN ANALYZE reviewed for all complex queries
- [ ] No sequential scans on large tables (unless intended)
- [ ] Indexes utilized effectively (check execution plan)
- [ ] No N+1 query patterns (correlated subqueries eliminated)

**SQL Quality:**
- [ ] Only necessary columns in SELECT (no SELECT *)
- [ ] Explicit table aliases used in multi-table queries
- [ ] Proper NULL handling (COALESCE, IS NULL vs = NULL)
- [ ] Data types match in comparisons (no implicit conversions)
- [ ] Parameterized queries used (SQL injection prevention)

**Optimization:**
- [ ] Window functions used instead of self-joins where applicable
- [ ] EXISTS used instead of NOT IN for better NULL handling
- [ ] Covering indexes suggested for frequent queries
- [ ] Query rewritten to eliminate correlated subqueries

**Documentation:**
- [ ] Complex query logic explained in comments
- [ ] CTE names descriptive and self-documenting
- [ ] Expected output format documented
- [ ] Performance characteristics documented

## Additional Resources

- **Detailed Technical Reference**: See [REFERENCE.md](REFERENCE.md)
- **Code Examples & Patterns**: See [EXAMPLES.md](EXAMPLES.md)
