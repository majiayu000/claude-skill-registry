---
name: postgresql-best-practices
description: PostgreSQL development best practices for schema design, query optimization, and database administration
---

# PostgreSQL Best Practices

## Core Principles

- Leverage PostgreSQL's advanced features for robust data modeling
- Optimize queries using EXPLAIN ANALYZE and proper indexing strategies
- Use native PostgreSQL data types appropriately
- Implement proper connection pooling and resource management
- Follow PostgreSQL-specific security best practices

## Schema Design

### Data Types

- Use appropriate native types: `UUID`, `JSONB`, `ARRAY`, `INET`, `CIDR`
- Prefer `TIMESTAMPTZ` over `TIMESTAMP` for timezone-aware applications
- Use `TEXT` instead of `VARCHAR` when no length limit is needed
- Consider `NUMERIC` for precise decimal calculations (financial data)
- Use `SERIAL` or `BIGSERIAL` for auto-incrementing IDs, or `UUID` for distributed systems

```sql
CREATE TABLE orders (
    order_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    customer_id UUID NOT NULL REFERENCES customers(customer_id),
    order_data JSONB NOT NULL DEFAULT '{}',
    tags TEXT[] DEFAULT '{}',
    total_amount NUMERIC(12, 2) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

### Table Design

- Always define primary keys
- Use foreign keys with appropriate ON DELETE/UPDATE actions
- Add NOT NULL constraints where appropriate
- Use CHECK constraints for data validation
- Consider partitioning for large tables

```sql
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    sku VARCHAR(50) NOT NULL UNIQUE,
    name TEXT NOT NULL,
    price NUMERIC(10, 2) NOT NULL CHECK (price >= 0),
    status VARCHAR(20) NOT NULL DEFAULT 'active'
        CHECK (status IN ('active', 'inactive', 'discontinued')),
    metadata JSONB DEFAULT '{}'
);
```

### Partitioning

- Use declarative partitioning for large tables (millions of rows)
- Choose appropriate partition strategy: RANGE, LIST, or HASH
- Create indexes on partitioned tables after partitioning

```sql
CREATE TABLE events (
    event_id BIGSERIAL,
    event_type VARCHAR(50) NOT NULL,
    payload JSONB,
    created_at TIMESTAMPTZ NOT NULL
) PARTITION BY RANGE (created_at);

CREATE TABLE events_2024_q1 PARTITION OF events
    FOR VALUES FROM ('2024-01-01') TO ('2024-04-01');
```

## Indexing Strategies

### Index Types

- Use B-tree indexes (default) for equality and range queries
- Use GIN indexes for JSONB, arrays, and full-text search
- Use GiST indexes for geometric data and range types
- Use BRIN indexes for large, naturally ordered data
- Consider partial indexes for filtered queries

```sql
-- B-tree index for common lookups
CREATE INDEX idx_orders_customer ON orders(customer_id);

-- GIN index for JSONB queries
CREATE INDEX idx_orders_data ON orders USING GIN (order_data);

-- Partial index for active records only
CREATE INDEX idx_active_products ON products(name) WHERE status = 'active';

-- Covering index to avoid table lookup
CREATE INDEX idx_orders_covering ON orders(customer_id)
    INCLUDE (order_date, total_amount);
```

### Index Maintenance

- Regularly run ANALYZE to update statistics
- Use REINDEX for bloated indexes
- Monitor index usage with `pg_stat_user_indexes`
- Remove unused indexes to reduce write overhead

```sql
-- Check index usage
SELECT schemaname, relname, indexrelname, idx_scan, idx_tup_read
FROM pg_stat_user_indexes
ORDER BY idx_scan ASC;
```

## Query Optimization

### EXPLAIN ANALYZE

- Always analyze query plans for slow queries
- Look for sequential scans on large tables
- Identify missing indexes from query plans
- Watch for high row estimates vs actual rows

```sql
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT c.name, COUNT(o.order_id)
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE c.created_at > '2024-01-01'
GROUP BY c.customer_id, c.name;
```

### Common Table Expressions (CTEs)

- Use CTEs for complex query organization
- Note: CTEs are optimization fences in older PostgreSQL versions
- Use `MATERIALIZED`/`NOT MATERIALIZED` hints in PostgreSQL 12+

```sql
WITH recent_orders AS MATERIALIZED (
    SELECT customer_id, COUNT(*) AS order_count, SUM(total) AS total_spent
    FROM orders
    WHERE order_date > CURRENT_DATE - INTERVAL '30 days'
    GROUP BY customer_id
)
SELECT c.name, ro.order_count, ro.total_spent
FROM customers c
JOIN recent_orders ro ON c.customer_id = ro.customer_id
WHERE ro.total_spent > 1000;
```

### Window Functions

- Use window functions for analytics queries
- Leverage PARTITION BY and ORDER BY for complex calculations

```sql
SELECT
    order_id,
    customer_id,
    total_amount,
    SUM(total_amount) OVER (PARTITION BY customer_id ORDER BY order_date) AS running_total,
    ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date DESC) AS order_rank
FROM orders;
```

## JSONB Best Practices

- Use JSONB over JSON for better performance and indexing
- Create GIN indexes for JSONB columns you query
- Use containment operators (@>, <@) for efficient queries
- Extract frequently queried fields to regular columns

```sql
-- Efficient JSONB query with GIN index
SELECT * FROM products
WHERE metadata @> '{"category": "electronics"}';

-- Extract specific fields
SELECT
    product_id,
    metadata->>'brand' AS brand,
    (metadata->>'rating')::numeric AS rating
FROM products
WHERE metadata ? 'rating';
```

## Connection Management

### Connection Pooling

- Use PgBouncer or pgpool-II for connection pooling
- Set appropriate pool sizes based on workload
- Use transaction pooling mode for short-lived connections

### Connection Settings

```sql
-- Recommended session settings
SET statement_timeout = '30s';
SET lock_timeout = '10s';
SET idle_in_transaction_session_timeout = '60s';
```

## Transactions and Locking

- Use appropriate transaction isolation levels
- Keep transactions short to reduce lock contention
- Use advisory locks for application-level locking
- Monitor and resolve lock conflicts

```sql
-- Use advisory locks for application coordination
SELECT pg_advisory_lock(hashtext('resource_name'));
-- Do work
SELECT pg_advisory_unlock(hashtext('resource_name'));

-- Check for blocking queries
SELECT blocked_locks.pid AS blocked_pid,
       blocking_locks.pid AS blocking_pid,
       blocked_activity.query AS blocked_query
FROM pg_catalog.pg_locks blocked_locks
JOIN pg_catalog.pg_locks blocking_locks
    ON blocking_locks.locktype = blocked_locks.locktype
    AND blocking_locks.relation = blocked_locks.relation
    AND blocking_locks.pid != blocked_locks.pid
JOIN pg_catalog.pg_stat_activity blocked_activity
    ON blocked_activity.pid = blocked_locks.pid;
```

## Maintenance

### Vacuum and Analyze

- Enable autovacuum and tune for your workload
- Run manual VACUUM ANALYZE after bulk operations
- Monitor table bloat

```sql
-- Check table bloat
SELECT schemaname, relname,
       n_live_tup, n_dead_tup,
       round(n_dead_tup * 100.0 / nullif(n_live_tup + n_dead_tup, 0), 2) AS dead_pct
FROM pg_stat_user_tables
WHERE n_dead_tup > 1000
ORDER BY n_dead_tup DESC;
```

### Backup Strategies

- Use pg_dump for logical backups
- Use pg_basebackup for physical backups
- Implement point-in-time recovery (PITR) with WAL archiving
- Test backup restoration regularly

## Security

- Use SSL/TLS for connections
- Implement row-level security (RLS) for multi-tenant applications
- Use roles and GRANT/REVOKE for access control
- Audit sensitive operations with pgAudit extension

```sql
-- Enable row-level security
ALTER TABLE documents ENABLE ROW LEVEL SECURITY;

CREATE POLICY documents_tenant_policy ON documents
    FOR ALL
    USING (tenant_id = current_setting('app.tenant_id')::uuid);

-- Grant minimal privileges
GRANT SELECT, INSERT, UPDATE ON orders TO app_user;
GRANT USAGE ON SEQUENCE orders_order_id_seq TO app_user;
```

## Monitoring

- Monitor with pg_stat_statements extension
- Track slow queries and optimize regularly
- Set up alerts for replication lag, connection count, and disk usage
- Use pg_stat_activity to monitor active queries

```sql
-- Enable pg_stat_statements
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

-- Find slow queries
SELECT query, calls, mean_exec_time, total_exec_time
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 10;
```
