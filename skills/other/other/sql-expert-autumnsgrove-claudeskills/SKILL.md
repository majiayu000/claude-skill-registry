---
name: sql-expert
description: "Expert SQL query writing, optimization, and database schema design with support for PostgreSQL, MySQL, SQLite, and SQL Server. Use when working with databases for: (1) Writing complex SQL queries with joins, subqueries, and window functions, (2) Optimizing slow queries and analyzing execution plans, (3) Designing database schemas with proper normalization, (4) Creating indexes and improving query performance, (5) Writing migrations and handling schema changes, (6) Debugging SQL errors and query issues"
---

# SQL Expert Skill

Expert guidance for writing, optimizing, and managing SQL databases across PostgreSQL, MySQL, SQLite, and SQL Server.

## Core Capabilities

This skill enables you to:

- **Write complex SQL queries** with JOINs, subqueries, CTEs, and window functions
- **Optimize slow queries** using EXPLAIN plans and index recommendations
- **Design database schemas** with proper normalization (1NF, 2NF, 3NF, BCNF)
- **Create effective indexes** for query performance
- **Write database migrations** safely with rollback support
- **Debug SQL errors** and understand error messages
- **Handle transactions** with proper isolation levels
- **Work with JSON/JSONB** data types
- **Generate sample data** for testing
- **Convert between database dialects** (PostgreSQL ↔ MySQL ↔ SQLite)

---

## Supported Database Systems

### PostgreSQL
**Best for**: Complex queries, JSON data, advanced features, ACID compliance

```bash
pip install psycopg2-binary sqlalchemy
```

### MySQL/MariaDB
**Best for**: Web applications, WordPress, high-read workloads

```bash
pip install mysql-connector-python sqlalchemy
```

### SQLite
**Best for**: Local development, embedded databases, testing

```bash
pip install sqlite3  # Built into Python
```

### SQL Server
**Best for**: Enterprise applications, Windows environments

```bash
pip install pyodbc sqlalchemy
```

---

## Query Writing

### Basic SELECT with JOINs

```sql
-- Simple SELECT with filtering
SELECT
    column1,
    column2,
    column3
FROM
    table_name
WHERE
    condition = 'value'
    AND another_condition > 100
ORDER BY
    column1 DESC
LIMIT 10;

-- INNER JOIN
SELECT
    users.name,
    orders.order_date,
    orders.total_amount
FROM
    users
INNER JOIN
    orders ON users.id = orders.user_id
WHERE
    orders.status = 'completed';

-- LEFT JOIN (include all users, even without orders)
SELECT
    users.name,
    COUNT(orders.id) as order_count,
    COALESCE(SUM(orders.total_amount), 0) as total_spent
FROM
    users
LEFT JOIN
    orders ON users.id = orders.user_id
GROUP BY
    users.id, users.name;
```

### Subqueries and CTEs

```sql
-- Subquery in WHERE clause
SELECT name, salary
FROM employees
WHERE salary > (SELECT AVG(salary) FROM employees);

-- Common Table Expression (CTE)
WITH high_value_customers AS (
    SELECT
        user_id,
        SUM(total_amount) as lifetime_value
    FROM orders
    GROUP BY user_id
    HAVING SUM(total_amount) > 1000
)
SELECT
    users.name,
    users.email,
    hvc.lifetime_value
FROM users
INNER JOIN high_value_customers hvc ON users.id = hvc.user_id;
```

### Window Functions

```sql
-- Ranking within groups
SELECT
    name,
    department,
    salary,
    ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) as salary_rank
FROM
    employees;

-- Running totals
SELECT
    order_date,
    total_amount,
    SUM(total_amount) OVER (ORDER BY order_date) as running_total
FROM
    orders;

-- Moving averages
SELECT
    order_date,
    total_amount,
    AVG(total_amount) OVER (
        ORDER BY order_date
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) as moving_avg_7days
FROM
    daily_sales;
```

See `examples/complex_queries.sql` for more advanced query patterns.

---

## Query Optimization

### Using EXPLAIN

```sql
-- Analyze query performance
EXPLAIN ANALYZE
SELECT
    users.name,
    COUNT(orders.id) as order_count
FROM users
LEFT JOIN orders ON users.id = orders.user_id
GROUP BY users.id, users.name;

-- Look for:
-- - Seq Scan (bad) vs Index Scan (good)
-- - High cost numbers
-- - Large row counts being processed
```

### Quick Optimization Tips

```sql
-- BAD: Function on indexed column
SELECT * FROM users WHERE LOWER(email) = 'user@example.com';

-- GOOD: Keep indexed column clean
SELECT * FROM users WHERE email = LOWER('user@example.com');

-- BAD: SELECT *
SELECT * FROM large_table WHERE id = 123;

-- GOOD: Select only needed columns
SELECT id, name, email FROM large_table WHERE id = 123;
```

For comprehensive optimization techniques, see `references/query-optimization.md`.

---

## Schema Design

### Normalization Principles

**First Normal Form (1NF)**: Eliminate repeating groups, use atomic values

```sql
-- GOOD: Separate table for order items
CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_name VARCHAR(100)
);

CREATE TABLE order_items (
    order_item_id INT PRIMARY KEY,
    order_id INT REFERENCES orders(order_id),
    product_name VARCHAR(100)
);
```

**Second Normal Form (2NF)**: All non-key attributes depend on entire primary key

```sql
-- GOOD: Separate product information
CREATE TABLE products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(100),
    product_price DECIMAL(10, 2)
);

CREATE TABLE order_items (
    order_id INT,
    product_id INT,
    quantity INT,
    PRIMARY KEY (order_id, product_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);
```

**Third Normal Form (3NF)**: No transitive dependencies

### Common Schema Patterns

**One-to-Many:**

```sql
CREATE TABLE authors (
    author_id INT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE
);

CREATE TABLE books (
    book_id INT PRIMARY KEY,
    title VARCHAR(200),
    author_id INT NOT NULL,
    published_date DATE,
    FOREIGN KEY (author_id) REFERENCES authors(author_id)
);
```

**Many-to-Many:**

```sql
CREATE TABLE students (
    student_id INT PRIMARY KEY,
    name VARCHAR(100)
);

CREATE TABLE courses (
    course_id INT PRIMARY KEY,
    course_name VARCHAR(100)
);

-- Junction table
CREATE TABLE enrollments (
    enrollment_id INT PRIMARY KEY,
    student_id INT NOT NULL,
    course_id INT NOT NULL,
    enrollment_date DATE,
    grade CHAR(2),
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id),
    UNIQUE (student_id, course_id)
);
```

See `examples/schema_examples.sql` for more schema patterns.

---

## Indexes and Performance

### Creating Indexes

```sql
-- Single column index
CREATE INDEX idx_users_email ON users(email);

-- Composite index (order matters!)
CREATE INDEX idx_orders_user_date ON orders(user_id, order_date);

-- Unique index
CREATE UNIQUE INDEX idx_users_username ON users(username);

-- Partial index (PostgreSQL)
CREATE INDEX idx_active_users ON users(email) WHERE status = 'active';
```

### Index Guidelines

**When to create indexes:**
- ✅ Columns used in WHERE clauses
- ✅ Columns used in JOIN conditions
- ✅ Columns used in ORDER BY
- ✅ Foreign key columns

**When NOT to create indexes:**
- ❌ Small tables (< 1000 rows)
- ❌ Columns with low selectivity (boolean fields)
- ❌ Columns frequently updated

For detailed index strategies, see `references/indexes-performance.md`.

---

## Migrations

### Safe Migration Pattern

```sql
-- Step 1: Add column as nullable
ALTER TABLE users ADD COLUMN status VARCHAR(20);

-- Step 2: Populate existing rows
UPDATE users SET status = 'active' WHERE status IS NULL;

-- Step 3: Make it NOT NULL
ALTER TABLE users ALTER COLUMN status SET NOT NULL;

-- Step 4: Add default for new rows
ALTER TABLE users ALTER COLUMN status SET DEFAULT 'active';

-- Rollback plan
ALTER TABLE users DROP COLUMN status;
```

### Zero-Downtime Migrations

```sql
-- GOOD: Add column as nullable first, then backfill
ALTER TABLE large_table ADD COLUMN new_column VARCHAR(100);

-- Backfill in batches
UPDATE large_table SET new_column = 'value' WHERE new_column IS NULL LIMIT 1000;
-- Repeat until complete

-- Then make it NOT NULL
ALTER TABLE large_table ALTER COLUMN new_column SET NOT NULL;
```

See `examples/migrations.sql` for more migration patterns.

---

## Advanced Patterns

### UPSERT (Insert or Update)

```sql
-- PostgreSQL
INSERT INTO users (user_id, name, email, updated_at)
VALUES (1, 'John Doe', 'john@example.com', NOW())
ON CONFLICT (user_id)
DO UPDATE SET
    name = EXCLUDED.name,
    email = EXCLUDED.email,
    updated_at = NOW();

-- MySQL
INSERT INTO users (user_id, name, email, updated_at)
VALUES (1, 'John Doe', 'john@example.com', NOW())
ON DUPLICATE KEY UPDATE
    name = VALUES(name),
    email = VALUES(email),
    updated_at = NOW();
```

### Recursive CTEs

```sql
-- Hierarchical data traversal
WITH RECURSIVE employee_hierarchy AS (
    -- Anchor: top-level employees
    SELECT id, name, manager_id, 1 as level
    FROM employees
    WHERE manager_id IS NULL

    UNION ALL

    -- Recursive: employees reporting to previous level
    SELECT e.id, e.name, e.manager_id, eh.level + 1
    FROM employees e
    INNER JOIN employee_hierarchy eh ON e.manager_id = eh.id
)
SELECT * FROM employee_hierarchy ORDER BY level, name;
```

For more advanced patterns including pivot tables, JSON operations, and bulk operations, see `references/advanced-patterns.md`.

---

## Best Practices

### Critical Guidelines

1. **Always use parameterized queries** to prevent SQL injection
2. **Use transactions for related operations** to ensure atomicity
3. **Add appropriate constraints** (PRIMARY KEY, FOREIGN KEY, NOT NULL, CHECK)
4. **Include timestamps** (created_at, updated_at) on tables
5. **Use meaningful names** for tables and columns
6. **Avoid SELECT *** - specify only needed columns
7. **Index foreign keys** for join performance
8. **Use VARCHAR instead of CHAR** for variable-length strings
9. **Handle NULL values properly** with IS NULL / IS NOT NULL
10. **Use appropriate data types** (DECIMAL for money, not FLOAT)

Example with multiple best practices:

```sql
CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    user_id INT NOT NULL,
    order_date DATE NOT NULL DEFAULT CURRENT_DATE,
    total_amount DECIMAL(10, 2) CHECK (total_amount >= 0),
    status VARCHAR(20) CHECK (status IN ('pending', 'completed', 'cancelled')),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE INDEX idx_orders_status ON orders(status);
```

For comprehensive best practices, see `references/best-practices.md`.

---

## Common Pitfalls

Watch out for these frequent issues:

1. **N+1 Query Problem** - Use JOINs instead of loops with queries
2. **Not using LIMIT** for exploratory queries on large tables
3. **Implicit type conversions** preventing index usage
4. **Using COUNT(*) when EXISTS is sufficient**
5. **Not handling NULLs properly** (NULL = NULL is always NULL, not TRUE)
6. **Using SELECT DISTINCT** as a band-aid instead of fixing the query
7. **Forgetting transactions** for related operations
8. **Using functions on indexed columns** preventing index usage

Example - Avoiding N+1:

```python
# BAD: N+1 queries
users = db.query("SELECT * FROM users")
for user in users:
    orders = db.query("SELECT * FROM orders WHERE user_id = ?", user.id)

# GOOD: Single query with JOIN
result = db.query("""
    SELECT users.*, orders.*
    FROM users
    LEFT JOIN orders ON users.id = orders.user_id
""")
```

For a complete list of pitfalls and solutions, see `references/common-pitfalls.md`.

---

## Helper Scripts and Examples

### Available Resources

**Helper Scripts** (`scripts/`):
- `sql_helper.py` - Utility functions for query building, schema introspection, index analysis, and migration helpers

**Examples** (`examples/`):
- `complex_queries.sql` - Advanced query patterns with CTEs, window functions, and subqueries
- `schema_examples.sql` - Complete schema design examples for various use cases
- `migrations.sql` - Safe migration patterns and zero-downtime techniques

**References** (`references/`):
- `query-optimization.md` - Comprehensive query optimization techniques and EXPLAIN analysis
- `indexes-performance.md` - Detailed index strategies, maintenance, and monitoring
- `advanced-patterns.md` - UPSERT, bulk operations, pivot tables, JSON operations, recursive queries
- `best-practices.md` - Complete SQL best practices guide
- `common-pitfalls.md` - Common mistakes and how to avoid them

### Quick Start

1. For basic queries, use the patterns shown above
2. For optimization, start with EXPLAIN and check `references/query-optimization.md`
3. For schema design, review normalization patterns and see `examples/schema_examples.sql`
4. For complex scenarios, check `references/advanced-patterns.md`
5. For utilities, use `scripts/sql_helper.py`

---

## Workflow

When working with SQL databases:

1. **Understand requirements** - What data needs to be queried or stored?
2. **Design schema** - Apply normalization, choose appropriate data types
3. **Create indexes** - Index foreign keys and frequently queried columns
4. **Write queries** - Start simple, add complexity as needed
5. **Optimize** - Use EXPLAIN to identify bottlenecks
6. **Test** - Verify with sample data and edge cases
7. **Document** - Add comments for complex queries

For migrations:
1. **Plan changes** - Identify affected tables and dependencies
2. **Write migration** - Create both up and down migrations
3. **Test on copy** - Test on development database first
4. **Backup** - Always backup before running migrations
5. **Execute** - Run migrations during low-traffic periods
6. **Verify** - Check data integrity after migration
