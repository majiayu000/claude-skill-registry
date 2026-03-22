---
name: mysql-aurora-patterns
description: "MySQL and Aurora-specific database patterns including InnoDB conventions, utf8mb4 charset, Aurora read replicas, RDS Proxy, and failover retry logic. Use when working with MySQL or Aurora databases. Do NOT use for PostgreSQL -- use postgresql-patterns instead. Do NOT use for generic database principles -- use database-patterns instead."
durability: encoded-preference
---

# MySQL/Aurora Patterns

MySQL and Aurora-specific optimization patterns. For DB-agnostic patterns (transactions, N+1, caching principles, EXPLAIN ANALYZE, zero-downtime migrations), see database-patterns skill.

## MySQL Schema Conventions

### Data Type and Engine Defaults

```sql
CREATE TABLE users (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  email VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  is_active TINYINT(1) DEFAULT 1,
  balance DECIMAL(10,2)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

**Key Points:**
- **InnoDB** engine required (transactions, foreign keys, row-level locking)
- **utf8mb4** charset required (full Unicode including emoji)
- **AUTO_INCREMENT** for sequential primary keys
- **TINYINT(1)** for boolean columns (MySQL has no native BOOLEAN type)

## Aurora Specific

### Read Replicas

- Use reader endpoint for read-heavy queries
- Use writer endpoint for writes only
- Design application to tolerate replication lag on read replicas

### Connection Management

- Use connection pooling (RDS Proxy recommended for Aurora)
- Keep transactions short for failover resilience
- Implement retry logic for failover scenarios

### Failover Retry Pattern

Aurora failover typically completes within 30 seconds. Applications should:
1. Detect connection errors during failover
2. Retry with exponential backoff
3. Re-resolve DNS for the cluster endpoint (Aurora updates DNS on failover)
4. Avoid caching resolved IP addresses

## MySQL Security

### Least Privilege User Creation

```sql
-- Read-only application user
CREATE USER 'app_readonly'@'%' IDENTIFIED BY 'password';
GRANT SELECT ON mydb.products TO 'app_readonly'@'%';

-- Read-write application user
CREATE USER 'app_writer'@'%' IDENTIFIED BY 'password';
GRANT SELECT, INSERT, UPDATE ON mydb.orders TO 'app_writer'@'%';
-- No DELETE permission unless explicitly needed
```

## MySQL Non-Blocking DDL

### Index Creation

```sql
-- Non-blocking index creation on MySQL/Aurora
ALTER TABLE orders ADD INDEX idx_customer_id (customer_id), ALGORITHM=INPLACE, LOCK=NONE;
```

### Column Operations

```sql
-- Non-blocking column addition
ALTER TABLE orders ADD COLUMN tracking_number VARCHAR(100), ALGORITHM=INPLACE, LOCK=NONE;
```

**Caveat**: Not all DDL operations support `ALGORITHM=INPLACE`. Check MySQL documentation for the specific operation. Operations that require table rebuild (e.g., changing column type) may need `ALGORITHM=COPY`.

## Anti-Patterns

### MySQL-Specific Anti-Patterns
- Missing `utf8mb4` charset (causes data loss for emoji and some CJK characters)
- Using MyISAM or other engines instead of InnoDB
- Not using `ALGORITHM=INPLACE, LOCK=NONE` for online DDL when available
- Caching Aurora cluster endpoint DNS resolution (breaks failover)

## Review Checklist

- [ ] utf8mb4 charset used
- [ ] InnoDB engine used
- [ ] Non-blocking DDL uses ALGORITHM=INPLACE, LOCK=NONE
- [ ] Aurora read replicas used for read-heavy queries
- [ ] RDS Proxy or connection pooling configured for Aurora

For DB-agnostic review items, see database-patterns skill.
