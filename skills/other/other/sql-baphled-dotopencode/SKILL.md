---
id: skill-sql
tier: T2
category: Database-Persistence
---

# Skill: sql

## What I do
- **Query Optimisation**: Analyse and tune slow-running queries using `EXPLAIN`.
- **Index Design**: Create and manage indices to support efficient query patterns.
- **Advanced SQL**: Implement Common Table Expressions (CTEs), Window Functions, and Recursive CTEs.
- **Data Analysis**: Perform complex aggregations, filtering, and analytical queries.
- **Bulk Operations**: Optimise large-scale inserts, updates, and deletes.

## When to use me
- Writing complex queries involving multiple joins or subqueries.
- Identifying and fixing performance bottlenecks in database access.
- Designing database schemas and efficient indexing strategies.
- Migrating ORM-generated queries to optimised raw SQL.

## Core principles
- **Efficiency First**: Design queries to leverage indices and minimise data transfer.
- **Readability**: Break complex logic into readable CTEs and document business rules.
- **Performance Awareness**: Use `EXPLAIN` regularly; avoid N+1 queries.
- **Security**: Always use parameterised queries to prevent SQL injection.

## Patterns & examples

### CTE for Readability (PostgreSQL/MySQL)
```sql
WITH active_users AS (
    SELECT id, name FROM users WHERE status = 'active'
),
user_orders AS (
    SELECT user_id, COUNT(*) as order_count, SUM(total) as total_spent
    FROM orders GROUP BY user_id
)
SELECT u.name, uo.order_count, uo.total_spent
FROM active_users u
JOIN user_orders uo ON u.id = uo.user_id;
```

## Anti-patterns to avoid
❌ **SELECT ***: Returning unnecessary data and risking breakage on schema changes.
❌ **Leading Wildcards**: `LIKE '%text'` prevents index usage.
❌ **Implicit Conversions**: Comparing different data types.
❌ **Application-Level Joins**: Fetching data in a loop instead of using a SQL join.

## KB Reference

`~/vaults/baphled/3. Resources/Knowledge Base/AI Development System/Skills/Database-Persistence/SQL.md`

