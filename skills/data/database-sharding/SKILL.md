---
name: database-sharding
description: Implement database sharding for horizontal scalability. Use when scaling large databases, distributing data across multiple servers, or designing sharded architectures.
---

# Database Sharding

## Overview

Implement horizontal data partitioning across multiple database servers. Covers sharding strategies, consistent hashing, shard key selection, and cross-shard querying patterns.

## When to Use

- Database size exceeds single server capacity
- Read/write throughput needs horizontal scaling
- Geographic data distribution requirements
- Multi-tenant data isolation
- Cost optimization through distributed architecture
- Load balancing across database instances

## Sharding Strategies

### 1. Range-Based Sharding

**PostgreSQL - Range Sharding Implementation:**

```sql
-- Define shard ranges
-- Shard 0: user_id 0-999999
-- Shard 1: user_id 1000000-1999999
-- Shard 2: user_id 2000000-2999999

CREATE TABLE users_shard_0 (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id BIGINT NOT NULL,
  email VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT NOW(),
  CONSTRAINT shard_0_range CHECK (user_id BETWEEN 0 AND 999999)
);

CREATE TABLE users_shard_1 (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id BIGINT NOT NULL,
  email VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT NOW(),
  CONSTRAINT shard_1_range CHECK (user_id BETWEEN 1000000 AND 1999999)
);

-- Function to determine shard
CREATE OR REPLACE FUNCTION get_shard_id(p_user_id BIGINT)
RETURNS INT AS $$
BEGIN
  RETURN (p_user_id / 1000000)::INT;
END;
$$ LANGUAGE plpgsql IMMUTABLE;
```

### 2. Hash-Based Sharding

**PostgreSQL - Consistent Hash Sharding:**

```sql
-- Hash-based distribution across 4 shards
CREATE OR REPLACE FUNCTION get_hash_shard(
  p_key VARCHAR,
  p_shard_count INT DEFAULT 4
)
RETURNS INT AS $$
DECLARE
  hash_val BIGINT;
BEGIN
  -- Use PostgreSQL's hashtext function
  hash_val := abs(hashtext(p_key)::BIGINT);
  RETURN (hash_val % p_shard_count)::INT;
END;
$$ LANGUAGE plpgsql IMMUTABLE;

-- Create sharded tables
CREATE TABLE users_shard_0 (
  id UUID PRIMARY KEY,
  user_key VARCHAR(255) NOT NULL,
  email VARCHAR(255),
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE users_shard_1 AS TABLE users_shard_0;
CREATE TABLE users_shard_2 AS TABLE users_shard_0;
CREATE TABLE users_shard_3 AS TABLE users_shard_0;

-- Insert with shard routing
INSERT INTO users_shard_0
SELECT * FROM users WHERE get_hash_shard(user_key, 4) = 0;

INSERT INTO users_shard_1
SELECT * FROM users WHERE get_hash_shard(user_key, 4) = 1;
```

**Consistent Hashing for Resilience:**

```sql
-- Virtual nodes for better load distribution
CREATE TABLE shard_mapping (
  virtual_node_id INT PRIMARY KEY,
  actual_shard_id INT NOT NULL,
  shard_host VARCHAR(255),
  shard_port INT
);

INSERT INTO shard_mapping VALUES
(0, 0, 'shard0.example.com', 5432),
(1, 1, 'shard1.example.com', 5432),
(2, 2, 'shard2.example.com', 5432),
(3, 3, 'shard3.example.com', 5432),
(4, 1, 'shard1.example.com', 5432),  -- Virtual node
(5, 2, 'shard2.example.com', 5432);

-- Find shard for key
CREATE OR REPLACE FUNCTION find_shard_host(p_key VARCHAR)
RETURNS TABLE (shard_id INT, host VARCHAR, port INT) AS $$
BEGIN
  RETURN QUERY
  SELECT sm.actual_shard_id, sm.shard_host, sm.shard_port
  FROM shard_mapping sm
  WHERE sm.virtual_node_id = (
    abs(hashtext(p_key)::BIGINT) %
    (SELECT COUNT(*) FROM shard_mapping)
  )::INT
  LIMIT 1;
END;
$$ LANGUAGE plpgsql;
```

### 3. Directory-Based Sharding

**PostgreSQL - Lookup Table Approach:**

```sql
-- Create shard directory
CREATE TABLE shard_directory (
  shard_key VARCHAR(255) PRIMARY KEY,
  shard_id INT NOT NULL,
  shard_host VARCHAR(255) NOT NULL,
  shard_port INT DEFAULT 5432,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_shard_id ON shard_directory(shard_id);

-- Insert shard configuration
INSERT INTO shard_directory (shard_key, shard_id, shard_host) VALUES
('user_1', 0, 'shard0.example.com'),
('user_2', 1, 'shard1.example.com'),
('tenant_a', 2, 'shard2.example.com'),
('tenant_b', 3, 'shard3.example.com');

-- Function to get shard from directory
CREATE OR REPLACE FUNCTION get_shard_info(p_key VARCHAR)
RETURNS TABLE (shard_id INT, host VARCHAR, port INT) AS $$
BEGIN
  RETURN QUERY
  SELECT sd.shard_id, sd.shard_host, sd.shard_port
  FROM shard_directory sd
  WHERE sd.shard_key = p_key;
END;
$$ LANGUAGE plpgsql;
```

## Shard Key Selection

**Good Shard Key Characteristics:**

```sql
-- Example: User-based sharding
-- Shard Key: user_id
-- Good because: frequently used in queries, stable value

-- All queries include shard key
SELECT * FROM users WHERE user_id = 123;
SELECT * FROM orders WHERE user_id = 123 AND order_id = 456;

-- Composite shard key for multi-tenant systems
-- Shard Key: (tenant_id, user_id)
SELECT * FROM users
WHERE tenant_id = 'tenant_a' AND user_id = 123;

-- Index on shard key for performance
CREATE INDEX idx_users_shard_key ON users_shard_0(user_id);
CREATE INDEX idx_orders_shard_key ON orders_shard_0(user_id, order_id);
```

## Cross-Shard Operations

**PostgreSQL - Distributed Query Pattern:**

```sql
-- Create foreign server connections for each shard
CREATE EXTENSION postgres_fdw;

CREATE SERVER shard_0
FOREIGN DATA WRAPPER postgres_fdw
OPTIONS (host 'shard0.example.com', dbname 'mydb');

CREATE SERVER shard_1
FOREIGN DATA WRAPPER postgres_fdw
OPTIONS (host 'shard1.example.com', dbname 'mydb');

-- Create foreign tables
CREATE FOREIGN TABLE users_remote_0 (
  id UUID, user_id BIGINT, email VARCHAR, created_at TIMESTAMP
) SERVER shard_0 OPTIONS (table_name 'users');

CREATE FOREIGN TABLE users_remote_1 (
  id UUID, user_id BIGINT, email VARCHAR, created_at TIMESTAMP
) SERVER shard_1 OPTIONS (table_name 'users');

-- Distributed query across shards
SELECT * FROM users_remote_0
UNION ALL
SELECT * FROM users_remote_1
WHERE created_at > NOW() - INTERVAL '7 days'
ORDER BY created_at DESC
LIMIT 100;
```

**Cross-Shard Aggregation:**

```sql
-- Aggregate data from all shards
CREATE OR REPLACE FUNCTION aggregate_user_orders()
RETURNS TABLE (user_id BIGINT, total_orders BIGINT, total_spent DECIMAL) AS $$
BEGIN
  RETURN QUERY
  SELECT
    so.user_id,
    COUNT(so.id)::BIGINT,
    SUM(so.total)::DECIMAL
  FROM (
    SELECT user_id, id, total FROM orders_shard_0
    UNION ALL
    SELECT user_id, id, total FROM orders_shard_1
    UNION ALL
    SELECT user_id, id, total FROM orders_shard_2
    UNION ALL
    SELECT user_id, id, total FROM orders_shard_3
  ) so
  GROUP BY so.user_id;
END;
$$ LANGUAGE plpgsql;
```

## Shard Rebalancing

**PostgreSQL - Add New Shard:**

```sql
-- 1. Create new shard tables
CREATE TABLE users_shard_4 (
  id UUID PRIMARY KEY,
  user_id BIGINT NOT NULL,
  email VARCHAR(255),
  created_at TIMESTAMP
);

-- 2. Migrate data using hash function
INSERT INTO users_shard_4
SELECT * FROM (
  SELECT * FROM users_shard_0 UNION ALL
  SELECT * FROM users_shard_1 UNION ALL
  SELECT * FROM users_shard_2 UNION ALL
  SELECT * FROM users_shard_3
) all_users
WHERE get_hash_shard(user_id::VARCHAR, 5) = 4;

-- 3. Remove migrated data from old shards
DELETE FROM users_shard_0 WHERE get_hash_shard(user_id::VARCHAR, 5) = 4;
DELETE FROM users_shard_1 WHERE get_hash_shard(user_id::VARCHAR, 5) = 4;
DELETE FROM users_shard_2 WHERE get_hash_shard(user_id::VARCHAR, 5) = 4;
DELETE FROM users_shard_3 WHERE get_hash_shard(user_id::VARCHAR, 5) = 4;

-- 4. Update shard count in configuration
-- Update application configuration: shard_count = 5
```

## Shard Monitoring

**PostgreSQL - Monitor Shard Balance:**

```sql
-- Check shard distribution
CREATE OR REPLACE FUNCTION monitor_shard_distribution()
RETURNS TABLE (shard_id INT, record_count BIGINT, avg_records BIGINT) AS $$
DECLARE
  total_records BIGINT;
BEGIN
  SELECT COUNT(*) INTO total_records FROM (
    SELECT 0 as shard_id, COUNT(*) FROM users_shard_0
    UNION ALL
    SELECT 1, COUNT(*) FROM users_shard_1
    UNION ALL
    SELECT 2, COUNT(*) FROM users_shard_2
    UNION ALL
    SELECT 3, COUNT(*) FROM users_shard_3
  ) counts;

  RETURN QUERY
  SELECT * FROM (
    SELECT 0::INT, COUNT(*)::BIGINT, (total_records / 4)::BIGINT FROM users_shard_0
    UNION ALL
    SELECT 1, COUNT(*), (total_records / 4) FROM users_shard_1
    UNION ALL
    SELECT 2, COUNT(*), (total_records / 4) FROM users_shard_2
    UNION ALL
    SELECT 3, COUNT(*), (total_records / 4) FROM users_shard_3
  );
END;
$$ LANGUAGE plpgsql;

SELECT * FROM monitor_shard_distribution();
```

**Monitor Shard Access:**

```sql
-- Track which shard is accessed
CREATE TABLE shard_access_log (
  shard_id INT,
  operation VARCHAR(10),
  record_count INT,
  duration_ms INT,
  accessed_at TIMESTAMP DEFAULT NOW()
);

-- Log shard access patterns
SELECT shard_id, operation, COUNT(*) as access_count
FROM shard_access_log
WHERE accessed_at > NOW() - INTERVAL '1 hour'
GROUP BY shard_id, operation
ORDER BY shard_id;
```

## Common Sharding Mistakes

❌ Don't use non-stable values as shard keys
❌ Don't forget to include shard key in all queries
❌ Don't overlook cross-shard query complexity
❌ Don't ignore uneven shard distribution
❌ Don't miss distributed transaction challenges

✅ DO validate shard key at insertion
✅ DO monitor shard balance regularly
✅ DO plan for shard rebalancing
✅ DO test cross-shard operations thoroughly
✅ DO document shard mapping clearly

## Sharding Strategies Comparison

| Strategy | Pros | Cons |
|----------|------|------|
| Range-based | Simple to implement | Hotspots in ranges |
| Hash-based | Even distribution | Complex rebalancing |
| Directory-based | Flexible, dynamic | Extra lookup overhead |

## Resources

- [PostgreSQL Partitioning](https://www.postgresql.org/docs/current/ddl-partitioning.html)
- [Citus - PostgreSQL Sharding](https://www.citusdata.com/)
- [Vitess - MySQL Middleware](https://vitess.io/)
- [ShardingSphere - Sharding Framework](https://shardingsphere.apache.org/)
