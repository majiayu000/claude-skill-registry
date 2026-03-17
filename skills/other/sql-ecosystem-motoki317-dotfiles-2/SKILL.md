---
name: SQL Ecosystem
description: This skill should be used when working with SQL databases, "SELECT", "INSERT", "UPDATE", "DELETE", "CREATE TABLE", "JOIN", "INDEX", "EXPLAIN", transactions, or database migrations. Provides comprehensive SQL patterns across PostgreSQL, MySQL, and SQLite.
---

# Critical Rules

- **ALWAYS use parameterized queries** for user input - NEVER use string concatenation
- Create indexes on foreign key columns
- Use explicit transaction boundaries for multi-statement operations
- Escape wildcards in LIKE patterns when using user input

# Data Types

**ANSI Standard** (portable): `INTEGER`, `BIGINT`, `DECIMAL(p,s)`, `CHAR(n)`, `VARCHAR(n)`, `TEXT`, `DATE`, `TIMESTAMP`, `BOOLEAN`

**PostgreSQL specific**: `UUID`, `JSONB`, `ARRAY`, `INET`, `SERIAL`/`BIGSERIAL`, range types

**MySQL specific**: `TINYINT`, `ENUM`, `SET`, `JSON`

**SQLite**: Type affinity (`TEXT`, `INTEGER`, `REAL`, `BLOB`, `NULL`)

# DDL Patterns

**Create table with constraints**:
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT email_format CHECK (email ~* '^[A-Za-z0-9._%+-]+@')
);
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

**Indexes**:
```sql
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_orders_user_status ON orders(user_id, status);  -- Composite
CREATE INDEX idx_active_users ON users(email) WHERE active = true;  -- Partial (PostgreSQL)
CREATE INDEX idx_users_lower_email ON users(LOWER(email));  -- Expression
```

# DML Patterns

**Parameterized queries** (CRITICAL - prevents SQL injection):
```python
# PostgreSQL (psycopg2)
cursor.execute("SELECT * FROM users WHERE email = %s", (user_email,))
# MySQL (mysql-connector)
cursor.execute("SELECT * FROM users WHERE email = %s", (user_email,))
# SQLite
cursor.execute("SELECT * FROM users WHERE email = ?", (user_email,))
```

**Safe LIKE patterns** (escape wildcards in user input):
```python
escaped = user_input.replace('%', '\\%').replace('_', '\\_')
cursor.execute("SELECT * FROM products WHERE name LIKE %s", ('%' + escaped + '%',))
```

**Upsert**:
```sql
-- PostgreSQL
INSERT INTO users (email, name) VALUES ('user@example.com', 'Name')
ON CONFLICT (email) DO UPDATE SET name = EXCLUDED.name;
-- MySQL
INSERT INTO users (email, name) VALUES ('user@example.com', 'Name')
ON DUPLICATE KEY UPDATE name = VALUES(name);
```

**Soft delete**: `UPDATE users SET deleted_at = NOW() WHERE id = 1;`

# Joins

- **INNER JOIN**: Return only matching rows from both tables
- **LEFT JOIN**: Return all rows from left table, matching rows from right
- **RIGHT JOIN**: Return all rows from right table (often rewritten as LEFT JOIN)
- **FULL OUTER JOIN**: Return all rows from both tables (not in MySQL)
- **CROSS JOIN**: Cartesian product (M*N rows - use carefully)
- **Self join**: Join table with itself (e.g., employees and managers)

# Subqueries and CTEs

**EXISTS** (more efficient than IN for existence checks):
```sql
SELECT * FROM users u WHERE EXISTS (
    SELECT 1 FROM orders o WHERE o.user_id = u.id AND o.total > 1000
);
```

**CTE** (Common Table Expression):
```sql
WITH active_users AS (SELECT id, name FROM users WHERE active = true)
SELECT au.name, COUNT(o.id) FROM active_users au
LEFT JOIN orders o ON au.id = o.user_id GROUP BY au.id, au.name;
```

**Recursive CTE** (hierarchical data):
```sql
WITH RECURSIVE org_tree AS (
    SELECT id, name, manager_id, 1 as level FROM employees WHERE manager_id IS NULL
    UNION ALL
    SELECT e.id, e.name, e.manager_id, ot.level + 1
    FROM employees e INNER JOIN org_tree ot ON e.manager_id = ot.id
) SELECT * FROM org_tree;
```

# Window Functions

```sql
ROW_NUMBER() OVER (ORDER BY total DESC) as rank
ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY created_at DESC) as order_num
RANK() OVER (ORDER BY score DESC)        -- gaps after ties
DENSE_RANK() OVER (ORDER BY score DESC)  -- no gaps
LAG(revenue, 1) OVER (ORDER BY date)     -- previous row
LEAD(revenue, 1) OVER (ORDER BY date)    -- next row
SUM(revenue) OVER (ORDER BY date)        -- cumulative
AVG(revenue) OVER (ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)  -- moving avg
NTILE(4) OVER (ORDER BY score DESC)      -- quartiles
```

# Schema Design

**Normalization**:
- 1NF: Atomic values, no repeating groups
- 2NF: No partial dependencies on composite key
- 3NF: No transitive dependencies

**Patterns**:
- Surrogate key: Auto-generated ID as primary key
- Soft delete: `deleted_at TIMESTAMP NULL` with partial unique constraint
- Audit columns: `created_at`, `updated_at`, `created_by`, `updated_by`
- Junction table: Many-to-many relationship with composite primary key

# Query Optimization

**EXPLAIN**: Understand query execution plans.
```sql
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'test@example.com';
```

Key indicators: `Seq Scan` (bad for large tables), `Index Scan` (good), `Index Only Scan` (best).

**Index strategies**:
- Covering index: Include all columns needed by query
- Composite index order: Put high-cardinality columns first
- Leftmost prefix rule: Index `(a, b)` supports `WHERE a=?` but not `WHERE b=?`

**Optimizations**:
- Select only needed columns (avoid `SELECT *`)
- Use `EXISTS` over `COUNT(*)` for existence checks
- Batch inserts/updates
- Keyset pagination over offset for large datasets:
  ```sql
  SELECT * FROM orders WHERE id > 1000 ORDER BY id LIMIT 20;
  ```

# Transactions

**Isolation levels**:
- READ UNCOMMITTED: Can read uncommitted changes
- READ COMMITTED: Default in PostgreSQL
- REPEATABLE READ: Default in MySQL
- SERIALIZABLE: Highest isolation, potential deadlocks

**Locking**:
```sql
SELECT * FROM accounts WHERE id = 1 FOR UPDATE;           -- Row lock
SELECT * FROM jobs WHERE status = 'pending' FOR UPDATE SKIP LOCKED LIMIT 1;  -- Queue processing
```

**Optimistic locking**: Version column with check on update.

**Deadlock prevention**: Always acquire locks in consistent order, use lock timeouts.

# Migrations

**Zero-downtime patterns**:
- Add nullable column first, backfill, then add NOT NULL
- PostgreSQL 11+: `ADD COLUMN ... DEFAULT` is instant
- Create index concurrently: `CREATE INDEX CONCURRENTLY ...`
- Rename column: Add new, copy data, deploy code reading both, drop old

**Batch updates**:
```sql
UPDATE users SET email_normalized = LOWER(email)
WHERE id IN (SELECT id FROM users WHERE email_normalized IS NULL LIMIT 1000);
```

# Anti-patterns
- `SELECT *` in production
- Missing indexes on filter/join columns
- N+1 queries in loops - Use JOIN or IN clause
- String concatenation for SQL - Always use parameterized queries
- Implicit type conversion preventing index usage
- Cartesian joins from missing ON clause
- Over-normalization causing too many joins

# Context7 Integration
- PostgreSQL: `/websites/postgresql`
- MySQL: `/websites/dev_mysql_doc_refman_9_4_en`
- SQLite: `/sqlite/sqlite`

# Best Practices
- Use parameterized queries to prevent SQL injection
- Create indexes on foreign keys and frequently filtered columns
- Use transactions for multi-statement operations
- Analyze query plans with EXPLAIN before optimizing
- Use appropriate isolation levels for transaction requirements
- Implement soft deletes for audit trails
- Name constraints explicitly for easier migration management
- Prefer keyset pagination over offset for large datasets
- Use CTEs for complex query readability
- Test migrations on production-like data before deployment
