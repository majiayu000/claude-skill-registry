---
name: lang-sql-dev
description: Foundational SQL patterns for query writing, schema design, and dialect differences. Use when writing SQL queries, designing database schemas, understanding SQL syntax across PostgreSQL/MySQL/SQLite, or preparing SQL for conversion to other query languages. This is a meta-skill for SQL derivatives.
---

# SQL Fundamentals

Foundational SQL patterns covering query writing, schema design, and dialect differences across PostgreSQL, MySQL, and SQLite. This skill serves as a base for specialized SQL skills and SQL-to-X conversions.

## Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        SQL Skill Hierarchy                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│                      ┌──────────────┐                           │
│                      │   lang-sql   │ ◄── You are here          │
│                      │ (foundation) │                           │
│                      └──────┬───────┘                           │
│                             │                                   │
│         ┌───────────────────┼───────────────────┐               │
│         │                   │                   │               │
│         ▼                   ▼                   ▼               │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐         │
│  │ sql-to-     │    │    sql-     │    │   data-     │         │
│  │  polars     │    │optimization │    │  postgres   │         │
│  └─────────────┘    └─────────────┘    └─────────────┘         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**This skill covers:**
- Query writing (SELECT, JOIN, CTEs, window functions)
- Schema design (tables, constraints, normalization)
- Dialect differences (PostgreSQL, MySQL, SQLite)
- Performance basics (EXPLAIN, indexing fundamentals)
- SQL syntax patterns useful for conversion

**This skill does NOT cover:**
- Deep optimization strategies - see `sql-optimization-patterns`
- ORM usage (SQLAlchemy, Prisma, etc.)
- Database administration (backups, replication, users)
- Platform-specific features (stored procedures, triggers)

---

## Quick Reference

| Task | PostgreSQL | MySQL | SQLite |
|------|------------|-------|--------|
| Show tables | `\dt` | `SHOW TABLES` | `.tables` |
| Describe table | `\d table` | `DESCRIBE table` | `.schema table` |
| Current database | `SELECT current_database()` | `SELECT DATABASE()` | N/A (file-based) |
| List indexes | `\di` | `SHOW INDEX FROM table` | `.indexes table` |
| Explain query | `EXPLAIN ANALYZE` | `EXPLAIN` | `EXPLAIN QUERY PLAN` |

---

## Query Patterns

### SELECT Fundamentals

```sql
-- Basic SELECT with filtering
SELECT column1, column2
FROM table_name
WHERE condition
ORDER BY column1 DESC
LIMIT 10;

-- Column aliases
SELECT
    first_name AS "First Name",
    last_name AS "Last Name",
    salary * 12 AS annual_salary
FROM employees;
```

### JOIN Types

```sql
-- INNER JOIN (matching rows only)
SELECT o.id, c.name
FROM orders o
INNER JOIN customers c ON o.customer_id = c.id;

-- LEFT JOIN (all from left, matching from right)
SELECT c.name, COUNT(o.id) as order_count
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id
GROUP BY c.name;

-- Multiple JOINs
SELECT
    o.id,
    c.name as customer,
    p.name as product
FROM orders o
JOIN customers c ON o.customer_id = c.id
JOIN order_items oi ON o.id = oi.order_id
JOIN products p ON oi.product_id = p.id;
```

### Common Table Expressions (CTEs)

```sql
-- Basic CTE
WITH active_users AS (
    SELECT id, name, email
    FROM users
    WHERE status = 'active'
)
SELECT * FROM active_users WHERE email LIKE '%@company.com';

-- Multiple CTEs
WITH
    recent_orders AS (
        SELECT * FROM orders WHERE created_at > NOW() - INTERVAL '30 days'
    ),
    order_totals AS (
        SELECT customer_id, SUM(amount) as total
        FROM recent_orders
        GROUP BY customer_id
    )
SELECT c.name, ot.total
FROM order_totals ot
JOIN customers c ON ot.customer_id = c.id;

-- Recursive CTE (hierarchical data)
WITH RECURSIVE org_chart AS (
    -- Base case: top-level managers
    SELECT id, name, manager_id, 1 as level
    FROM employees
    WHERE manager_id IS NULL

    UNION ALL

    -- Recursive case: employees under managers
    SELECT e.id, e.name, e.manager_id, oc.level + 1
    FROM employees e
    JOIN org_chart oc ON e.manager_id = oc.id
)
SELECT * FROM org_chart ORDER BY level, name;
```

### Window Functions

```sql
-- ROW_NUMBER: Sequential numbering within partition
SELECT
    department,
    name,
    salary,
    ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) as rank
FROM employees;

-- Running totals
SELECT
    date,
    amount,
    SUM(amount) OVER (ORDER BY date) as running_total
FROM transactions;

-- Compare to previous row
SELECT
    date,
    revenue,
    LAG(revenue) OVER (ORDER BY date) as prev_revenue,
    revenue - LAG(revenue) OVER (ORDER BY date) as change
FROM daily_sales;

-- Percentile ranking
SELECT
    name,
    score,
    PERCENT_RANK() OVER (ORDER BY score) as percentile
FROM test_results;
```

### Subqueries

```sql
-- Scalar subquery (returns single value)
SELECT name, salary,
    (SELECT AVG(salary) FROM employees) as avg_salary
FROM employees;

-- IN subquery
SELECT * FROM products
WHERE category_id IN (
    SELECT id FROM categories WHERE name LIKE '%Electronics%'
);

-- EXISTS subquery (often more efficient)
SELECT * FROM customers c
WHERE EXISTS (
    SELECT 1 FROM orders o
    WHERE o.customer_id = c.id
    AND o.created_at > NOW() - INTERVAL '30 days'
);

-- Correlated subquery (references outer query)
SELECT e.name, e.salary
FROM employees e
WHERE e.salary > (
    SELECT AVG(salary)
    FROM employees
    WHERE department_id = e.department_id
);
```

---

## Aggregation Patterns

### GROUP BY

```sql
-- Basic aggregation
SELECT
    department,
    COUNT(*) as employee_count,
    AVG(salary) as avg_salary,
    MIN(salary) as min_salary,
    MAX(salary) as max_salary
FROM employees
GROUP BY department;

-- HAVING (filter groups)
SELECT department, COUNT(*) as count
FROM employees
GROUP BY department
HAVING COUNT(*) > 5;

-- Multiple grouping columns
SELECT
    department,
    job_title,
    COUNT(*) as count
FROM employees
GROUP BY department, job_title
ORDER BY department, count DESC;
```

### CASE Expressions

```sql
-- Conditional aggregation
SELECT
    COUNT(CASE WHEN status = 'active' THEN 1 END) as active_count,
    COUNT(CASE WHEN status = 'inactive' THEN 1 END) as inactive_count,
    COUNT(*) as total
FROM users;

-- Bucketing data
SELECT
    CASE
        WHEN age < 18 THEN 'minor'
        WHEN age < 65 THEN 'adult'
        ELSE 'senior'
    END as age_group,
    COUNT(*) as count
FROM users
GROUP BY 1;  -- Group by first select column
```

---

## Schema Design

### Table Creation

```sql
-- Basic table with constraints
CREATE TABLE users (
    id SERIAL PRIMARY KEY,           -- PostgreSQL
    -- id INT AUTO_INCREMENT PRIMARY KEY,  -- MySQL
    -- id INTEGER PRIMARY KEY AUTOINCREMENT,  -- SQLite

    email VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table with foreign key
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    status VARCHAR(20) DEFAULT 'pending',
    total DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Many-to-many junction table
CREATE TABLE user_roles (
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    role_id INT REFERENCES roles(id) ON DELETE CASCADE,
    granted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, role_id)
);
```

### Normalization Quick Guide

| Form | Rule | Example |
|------|------|---------|
| 1NF | No repeating groups | Split `phone1, phone2` into separate rows |
| 2NF | No partial dependencies | Move `dept_name` to `departments` table if key is `(emp_id, dept_id)` |
| 3NF | No transitive dependencies | Move `city, state` to `addresses` if they depend on `zip_code` |

### Common Constraints

```sql
-- CHECK constraint
ALTER TABLE products
ADD CONSTRAINT positive_price CHECK (price > 0);

-- UNIQUE constraint on multiple columns
ALTER TABLE subscriptions
ADD CONSTRAINT unique_user_plan UNIQUE (user_id, plan_id);

-- NOT NULL with default
ALTER TABLE users
ALTER COLUMN status SET DEFAULT 'active',
ALTER COLUMN status SET NOT NULL;
```

---

## Index Basics

### When to Index

| Index | Use Case |
|-------|----------|
| Primary key | Automatic, unique identifier |
| Foreign key | Speed up JOINs |
| Frequently filtered columns | WHERE clauses |
| Frequently sorted columns | ORDER BY clauses |
| Composite | Multi-column WHERE/ORDER |

### Index Creation

```sql
-- Single column index
CREATE INDEX idx_users_email ON users(email);

-- Composite index (order matters!)
-- Good for: WHERE status = 'active' AND created_at > '2024-01-01'
CREATE INDEX idx_orders_status_created ON orders(status, created_at);

-- Partial index (PostgreSQL)
CREATE INDEX idx_active_users ON users(email) WHERE status = 'active';

-- Expression index
CREATE INDEX idx_users_lower_email ON users(LOWER(email));
```

### Reading EXPLAIN

```sql
-- PostgreSQL: Full analysis with timing
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'test@example.com';

-- Key things to look for:
-- ✓ Index Scan / Index Only Scan - good
-- ✗ Seq Scan on large tables - investigate
-- ✗ High "actual rows" vs "estimated rows" - stale statistics
```

---

## Dialect Differences

### String Concatenation

```sql
-- PostgreSQL
SELECT first_name || ' ' || last_name AS full_name FROM users;

-- MySQL
SELECT CONCAT(first_name, ' ', last_name) AS full_name FROM users;

-- SQLite (both work)
SELECT first_name || ' ' || last_name AS full_name FROM users;
```

### Date/Time Operations

```sql
-- Current timestamp
-- PostgreSQL: NOW(), CURRENT_TIMESTAMP
-- MySQL: NOW(), CURRENT_TIMESTAMP
-- SQLite: datetime('now')

-- Date arithmetic
-- PostgreSQL
SELECT created_at + INTERVAL '7 days' FROM orders;

-- MySQL
SELECT DATE_ADD(created_at, INTERVAL 7 DAY) FROM orders;

-- SQLite
SELECT datetime(created_at, '+7 days') FROM orders;

-- Extract parts
-- PostgreSQL
SELECT EXTRACT(YEAR FROM created_at) FROM orders;

-- MySQL
SELECT YEAR(created_at) FROM orders;

-- SQLite
SELECT strftime('%Y', created_at) FROM orders;
```

### UPSERT (Insert or Update)

```sql
-- PostgreSQL
INSERT INTO users (email, name)
VALUES ('test@example.com', 'Test User')
ON CONFLICT (email) DO UPDATE SET name = EXCLUDED.name;

-- MySQL
INSERT INTO users (email, name)
VALUES ('test@example.com', 'Test User')
ON DUPLICATE KEY UPDATE name = VALUES(name);

-- SQLite (3.24+)
INSERT INTO users (email, name)
VALUES ('test@example.com', 'Test User')
ON CONFLICT (email) DO UPDATE SET name = excluded.name;
```

### Pagination

```sql
-- Standard (PostgreSQL, MySQL, SQLite)
SELECT * FROM products ORDER BY id LIMIT 10 OFFSET 20;

-- Keyset pagination (more efficient for large offsets)
SELECT * FROM products
WHERE id > 1000  -- Last seen ID
ORDER BY id
LIMIT 10;
```

### Boolean Handling

```sql
-- PostgreSQL: Native BOOLEAN
SELECT * FROM users WHERE is_active = true;

-- MySQL: TINYINT(1) or BOOLEAN (alias)
SELECT * FROM users WHERE is_active = 1;

-- SQLite: INTEGER (0/1)
SELECT * FROM users WHERE is_active = 1;
```

---

## SQL for Conversion

When converting SQL to DataFrame operations (Pandas, Polars), map these patterns:

| SQL | DataFrame Equivalent |
|-----|---------------------|
| `SELECT col1, col2` | `.select(["col1", "col2"])` |
| `WHERE condition` | `.filter(condition)` |
| `ORDER BY col DESC` | `.sort("col", descending=True)` |
| `LIMIT n` | `.head(n)` or `.limit(n)` |
| `GROUP BY` | `.group_by()` |
| `JOIN` | `.join()` |
| `DISTINCT` | `.unique()` or `.distinct()` |

See derivative skills for specific conversion patterns:
- `sql-to-polars` - SQL to Polars DataFrame
- `sql-to-pandas` - SQL to Pandas DataFrame

---

## Anti-Patterns to Avoid

### 1. SELECT *

```sql
-- Bad: Fetches unnecessary data
SELECT * FROM users;

-- Good: Only fetch needed columns
SELECT id, name, email FROM users;
```

### 2. N+1 Queries

```sql
-- Bad: Query per user (in application loop)
SELECT * FROM orders WHERE user_id = 1;
SELECT * FROM orders WHERE user_id = 2;
-- ... repeated N times

-- Good: Single query with JOIN or IN
SELECT * FROM orders WHERE user_id IN (1, 2, 3, ...);
```

### 3. Functions on Indexed Columns

```sql
-- Bad: Prevents index usage
SELECT * FROM users WHERE LOWER(email) = 'test@example.com';

-- Good: Store normalized, or use expression index
SELECT * FROM users WHERE email = 'test@example.com';
```

### 4. Implicit Type Conversion

```sql
-- Bad: String compared to integer
SELECT * FROM users WHERE id = '123';

-- Good: Matching types
SELECT * FROM users WHERE id = 123;
```

### 5. Missing WHERE on UPDATE/DELETE

```sql
-- DANGEROUS: Affects all rows!
UPDATE users SET status = 'inactive';

-- Safe: Always include WHERE
UPDATE users SET status = 'inactive' WHERE last_login < '2024-01-01';
```

---

## Troubleshooting

### Query Returns No Results

1. **Check WHERE conditions**: Test each condition separately
2. **Verify JOIN keys**: Ensure matching data types and values
3. **NULL handling**: Use `IS NULL` not `= NULL`
4. **Case sensitivity**: Check collation settings

### Query Too Slow

1. **Run EXPLAIN**: Look for Seq Scans on large tables
2. **Check indexes**: Are filtered/joined columns indexed?
3. **Reduce data early**: Filter before JOINing
4. **Avoid SELECT ***: Fetch only needed columns

### Unexpected Duplicates

1. **Missing DISTINCT**: Add if needed
2. **Many-to-many JOINs**: Each match creates a row
3. **GROUP BY missing columns**: All non-aggregated columns must be grouped

### NULL Surprises

```sql
-- NULL comparisons always return NULL (unknown)
SELECT * FROM users WHERE department = NULL;  -- Returns nothing!
SELECT * FROM users WHERE department IS NULL; -- Correct

-- NULL in aggregations
SELECT AVG(salary) FROM employees;  -- NULLs ignored
SELECT COUNT(*) vs COUNT(column);   -- COUNT(*) includes NULL rows
```

---

## References

- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [MySQL Reference Manual](https://dev.mysql.com/doc/refman/8.0/en/)
- [SQLite Documentation](https://www.sqlite.org/docs.html)
- `sql-optimization-patterns` - Deep performance optimization
- `sql-expert` - Advanced query patterns
