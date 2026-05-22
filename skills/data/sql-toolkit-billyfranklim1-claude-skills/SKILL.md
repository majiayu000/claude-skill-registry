---
name: sql-toolkit
description: Query, design, migrate, and optimize SQL databases. Use when working with SQLite, PostgreSQL, or MySQL — schema design, writing queries, creating migrations, indexing, backup/restore, and debugging slow queries.
---

# SQL Toolkit

Work with relational databases directly from the command line. Covers SQLite, PostgreSQL, and MySQL with patterns for schema design, querying, migrations, indexing, and operations.

## When to Use

- Creating or modifying database schemas
- Writing complex queries (joins, aggregations, window functions, CTEs)
- Building migration scripts
- Optimizing slow queries with indexes and EXPLAIN
- Backing up and restoring databases
- Quick data exploration with SQLite (zero setup)

## MySQL

### Connection

```bash
mysql -h localhost -u root -p mydb
mysql -h localhost -u root -p -e "SELECT NOW();" mydb
```

### Key Patterns

```sql
-- Auto-increment table
CREATE TABLE users (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- JSON type (MySQL 5.7+)
CREATE TABLE orders (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT UNSIGNED NOT NULL,
    metadata JSON,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Query JSON
SELECT * FROM orders WHERE JSON_EXTRACT(metadata, '$.source') = 'web';
SELECT * FROM orders WHERE metadata->>'$.source' = 'web';
```

## Query Patterns

### Joins

```sql
-- Inner join
SELECT u.name, o.total, o.status
FROM users u
INNER JOIN orders o ON o.user_id = u.id
WHERE o.created_at > '2026-01-01';

-- Left join with count
SELECT u.name, COUNT(o.id) AS order_count, COALESCE(SUM(o.total), 0) AS total_spent
FROM users u
LEFT JOIN orders o ON o.user_id = u.id
GROUP BY u.id, u.name;
```

### Window Functions

```sql
-- Running total
SELECT date, revenue,
    SUM(revenue) OVER (ORDER BY date) AS cumulative_revenue
FROM daily_sales;

-- Rank within groups
SELECT user_id, total,
    RANK() OVER (PARTITION BY user_id ORDER BY total DESC) AS rank
FROM orders;

-- Moving average (last 7 entries)
SELECT date, revenue,
    AVG(revenue) OVER (ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS ma_7
FROM daily_sales;
```

### CTEs

```sql
-- Monthly revenue with growth %
WITH monthly_revenue AS (
    SELECT DATE_FORMAT(created_at, '%Y-%m') AS month,
           SUM(total) AS revenue
    FROM orders WHERE status = 'paid'
    GROUP BY 1
)
SELECT month, revenue,
    LAG(revenue) OVER (ORDER BY month) AS prev_revenue
FROM monthly_revenue ORDER BY month;

-- Recursive (org chart / tree)
WITH RECURSIVE org_tree AS (
    SELECT id, name, manager_id, 0 AS depth
    FROM employees WHERE manager_id IS NULL
    UNION ALL
    SELECT e.id, e.name, e.manager_id, t.depth + 1
    FROM employees e JOIN org_tree t ON e.manager_id = t.id
)
SELECT REPEAT('  ', depth), name FROM org_tree ORDER BY depth, name;
```

## Query Optimization

### EXPLAIN (MySQL)

```sql
EXPLAIN SELECT * FROM orders WHERE user_id = 1 AND status = 'paid';
EXPLAIN ANALYZE SELECT * FROM orders WHERE user_id = 1;
```

**What to look for:**
- `ALL` in type column (full table scan) → needs index
- `rows` being high → index doesn't cover the filter
- `Using filesort` → consider index on ORDER BY columns
- `Using temporary` → GROUP BY without index

### Index Strategy

```sql
-- Single column
CREATE INDEX idx_orders_user_id ON orders(user_id);

-- Composite (equality filters first, range filters last)
CREATE INDEX idx_orders_user_status ON orders(user_id, status);

-- Covering index (avoids table lookup)
CREATE INDEX idx_orders_covering ON orders(user_id, status, total, created_at);

-- Partial index via filtered query (MySQL doesn't have native partial, use generated col)
ALTER TABLE orders ADD COLUMN is_pending TINYINT GENERATED ALWAYS AS (IF(status='pending',1,NULL));
CREATE INDEX idx_orders_pending ON orders(is_pending, user_id);

-- Check unused indexes
SELECT s.table_name, s.index_name, s.rows_selected
FROM information_schema.statistics s
LEFT JOIN sys.schema_unused_indexes u
  ON s.table_schema = u.object_schema AND s.table_name = u.object_name AND s.index_name = u.index_name
WHERE s.table_schema = 'mydb'
ORDER BY s.rows_selected;
```

## Backup & Restore

```bash
# Full dump
mysqldump -h localhost -u root -p mydb > backup.sql

# Specific tables
mysqldump -h localhost -u root -p mydb users orders > partial.sql

# Compressed
mysqldump -h localhost -u root -p mydb | gzip > backup.sql.gz

# Restore
mysql -h localhost -u root -p mydb < backup.sql
gunzip -c backup.sql.gz | mysql -h localhost -u root -p mydb

# Export to CSV (from MySQL)
mysql -h localhost -u root -p mydb -e "SELECT * FROM users" | sed 's/\t/,/g' > users.csv
```

## SQLite Quick Reference

```bash
# One-liner query
sqlite3 mydb.sqlite "SELECT COUNT(*) FROM users WHERE created_at > '2026-01-01';"

# Import CSV
sqlite3 mydb.sqlite ".mode csv" ".import data.csv mytable" "SELECT COUNT(*) FROM mytable;"

# Export to CSV
sqlite3 -header -csv mydb.sqlite "SELECT * FROM orders;" > orders.csv

# Interactive mode
sqlite3 -header -column mydb.sqlite

# Backup
sqlite3 mydb.sqlite ".backup backup.sqlite"
```

## Tips

- Always use parameterized queries — never concatenate user input into SQL
- Use `EXPLAIN` before deploying any query that runs on large tables
- Run `ANALYZE tablename;` if EXPLAIN estimates are way off from reality
- For quick data exploration, import any CSV into SQLite: `sqlite3 :memory: ".mode csv" ".import file.csv t" "SELECT * FROM t LIMIT 5;"`
- In MySQL 8.0, window functions (ROW_NUMBER, RANK, LAG, LEAD) are fully supported
