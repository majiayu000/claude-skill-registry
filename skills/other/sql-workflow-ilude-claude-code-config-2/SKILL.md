---
name: sql-workflow
description: SQL workflow guidelines. Activate when working with SQL files (.sql), database queries, migrations, or SQLFluff.
location: user
---

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in RFC 2119.

# SQL Workflow

## Tool Grid

| Task | Tool | Command |
|------|------|---------|
| Lint | SQLFluff | `sqlfluff lint` |
| Format | SQLFluff | `sqlfluff fix` |
| Analyze | Database | `EXPLAIN ANALYZE` |

## Naming Conventions

### Tables and Columns
- All identifiers MUST use `snake_case`
- Table names SHOULD be plural nouns (e.g., `users`, `order_items`)
- Column names MUST be descriptive and unambiguous
- Primary keys SHOULD be named `id` or `{table_singular}_id`
- Foreign keys MUST follow `{referenced_table_singular}_id` pattern
- Boolean columns SHOULD use `is_`, `has_`, or `can_` prefix

### Examples
```sql
-- Good
CREATE TABLE orders (
    id BIGINT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    is_completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE
);

-- Bad
CREATE TABLE Order (
    OrderID INT,
    userId INT,
    completed BOOLEAN
);
```

## Data Types

### Preferred Types
- Text: MUST use `TEXT` over `VARCHAR` unless length constraint is business requirement
- Timestamps: MUST use `TIMESTAMP WITH TIME ZONE` for all temporal data
- Integers: SHOULD use `BIGINT` for IDs to prevent overflow
- Decimals: MUST use `NUMERIC(precision, scale)` for money/financial data
- UUIDs: SHOULD use native `UUID` type when available
- JSON: SHOULD use `JSONB` over `JSON` for PostgreSQL

### Avoid
- `CHAR(n)` - wastes space with padding
- `FLOAT`/`DOUBLE` for financial calculations
- `TIMESTAMP` without time zone

## Migrations

### File Naming
Migrations MUST follow: `YYYYMMDD_HHMMSS_description.sql`

```
20241215_143022_create_users_table.sql
20241215_150000_add_email_index_to_users.sql
20241216_090000_create_orders_table.sql
```

### Migration Structure
```sql
-- Migration: 20241215_143022_create_users_table.sql
-- Description: Creates the users table with core fields

BEGIN;

CREATE TABLE users (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    email TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

COMMIT;
```

### Rules
- Each migration MUST be wrapped in a transaction (BEGIN/COMMIT)
- Migrations MUST be idempotent when possible (use IF NOT EXISTS)
- Down migrations SHOULD be provided for reversible changes
- Data migrations MUST be separate from schema migrations

## Query Style

### Formatting
- Keywords MUST be uppercase: `SELECT`, `FROM`, `WHERE`, `JOIN`
- Identifiers MUST be lowercase: `users`, `created_at`
- Each major clause SHOULD start on a new line
- Indentation SHOULD be 4 spaces
- Commas SHOULD be at the end of lines (trailing commas)

### Example
```sql
SELECT
    u.id,
    u.email,
    COUNT(o.id) AS order_count
FROM users AS u
LEFT JOIN orders AS o
    ON u.id = o.user_id
WHERE u.is_active = TRUE
    AND u.created_at >= '2024-01-01'
GROUP BY u.id, u.email
HAVING COUNT(o.id) > 0
ORDER BY order_count DESC
LIMIT 100;
```

### Aliases
- Table aliases MUST be meaningful (not single letters for complex queries)
- Column aliases MUST use `AS` keyword explicitly
- Aliases SHOULD be lowercase

## Indexes

### When to Create
- Primary keys automatically create indexes
- Foreign key columns SHOULD have indexes
- Columns frequently used in WHERE clauses SHOULD be indexed
- Columns used in ORDER BY with LIMIT SHOULD be considered
- Composite indexes for multi-column queries

### Naming Convention
```
idx_{table}_{column(s)}
idx_{table}_{column1}_{column2}
```

### Examples
```sql
-- Single column index
CREATE INDEX idx_users_email ON users (email);

-- Composite index
CREATE INDEX idx_orders_user_id_created_at ON orders (user_id, created_at);

-- Partial index
CREATE INDEX idx_orders_pending ON orders (id)
WHERE status = 'pending';

-- Unique index
CREATE UNIQUE INDEX idx_users_email_unique ON users (email);
```

### Anti-patterns
- Indexes on low-cardinality columns (boolean, status with few values)
- Too many indexes on write-heavy tables
- Unused indexes consuming storage

## Constraints

### Foreign Keys
```sql
ALTER TABLE orders
ADD CONSTRAINT fk_orders_user_id
FOREIGN KEY (user_id) REFERENCES users (id)
ON DELETE CASCADE
ON UPDATE CASCADE;
```

### Check Constraints
```sql
ALTER TABLE products
ADD CONSTRAINT chk_products_price_positive
CHECK (price > 0);

ALTER TABLE users
ADD CONSTRAINT chk_users_email_format
CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$');
```

### Naming
- Foreign keys: `fk_{table}_{column}`
- Check constraints: `chk_{table}_{description}`
- Unique constraints: `uq_{table}_{column(s)}`

## NULL Handling

### Rules
- MUST use `IS NULL` / `IS NOT NULL` for NULL comparisons
- MUST NOT use `= NULL` or `!= NULL`
- SHOULD use `COALESCE()` for default values
- SHOULD use `NULLIF()` to convert values to NULL

### Examples
```sql
-- Correct NULL handling
SELECT * FROM users WHERE deleted_at IS NULL;

-- Using COALESCE for defaults
SELECT COALESCE(nickname, email) AS display_name FROM users;

-- Using NULLIF to handle empty strings
SELECT NULLIF(phone, '') AS phone FROM users;
```

## Performance

### Query Analysis
- MUST use `EXPLAIN ANALYZE` before optimizing
- SHOULD check for sequential scans on large tables
- SHOULD monitor query execution time

```sql
EXPLAIN ANALYZE
SELECT * FROM orders WHERE user_id = 123;
```

### Best Practices
- MUST NOT use `SELECT *` in production code
- SHOULD specify only required columns
- SHOULD use `EXISTS` instead of `COUNT(*)` for existence checks
- SHOULD use `LIMIT` with `ORDER BY` for pagination
- MUST avoid N+1 queries - use JOINs or batch fetching

### Examples
```sql
-- Bad: SELECT *
SELECT * FROM users WHERE id = 1;

-- Good: Explicit columns
SELECT id, email, created_at FROM users WHERE id = 1;

-- Bad: COUNT for existence
SELECT COUNT(*) > 0 FROM orders WHERE user_id = 1;

-- Good: EXISTS
SELECT EXISTS (SELECT 1 FROM orders WHERE user_id = 1);
```

## Transactions

### Rules
- Write operations SHOULD use explicit transactions
- Transactions MUST be as short as possible
- SHOULD set appropriate isolation level when needed

### Example
```sql
BEGIN;

UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;

COMMIT;
```

### Isolation Levels
```sql
-- For critical financial operations
BEGIN ISOLATION LEVEL SERIALIZABLE;
-- ... operations ...
COMMIT;
```

## SQLFluff Configuration

### Recommended .sqlfluff
```ini
[sqlfluff]
dialect = postgres
templater = raw
max_line_length = 120

[sqlfluff:rules:capitalisation.keywords]
capitalisation_policy = upper

[sqlfluff:rules:capitalisation.identifiers]
capitalisation_policy = lower

[sqlfluff:rules:layout.long_lines]
ignore_comment_lines = True
```

## Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| `= NULL` comparison | Use `IS NULL` |
| `SELECT *` in production | Explicit column list |
| Missing indexes on FKs | Always index foreign keys |
| VARCHAR for text | Use TEXT |
| TIMESTAMP without TZ | Use TIMESTAMP WITH TIME ZONE |
| No transaction for writes | Wrap in BEGIN/COMMIT |
| Guessing query performance | Use EXPLAIN ANALYZE |
