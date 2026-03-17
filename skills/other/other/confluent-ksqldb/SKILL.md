---
description: ksqlDB stream processing expert. Covers SQL-like queries on Kafka topics, stream and table concepts, joins, aggregations, windowing, materialized views, and real-time data transformations. Activates for ksqldb, ksql, stream processing, kafka sql, real-time analytics, windowing, stream joins, table joins, materialized views.
---

# Confluent ksqlDB Skill

Expert knowledge of ksqlDB - Confluent's event streaming database for building real-time applications with SQL-like queries on Kafka topics.

## What I Know

### Core Concepts

**Streams** (Unbounded, Append-Only):
- Represents immutable event sequences
- Every row is a new event
- Cannot be updated or deleted
- Example: Click events, sensor readings, transactions

**Tables** (Mutable, Latest State):
- Represents current state
- Updates override previous values (by key)
- Compacted topic under the hood
- Example: User profiles, product inventory, account balances

**Key Difference**:
```sql
-- STREAM: Every event is independent
INSERT INTO clicks_stream (user_id, page, timestamp)
VALUES (1, 'homepage', CURRENT_TIMESTAMP());
-- Creates NEW row

-- TABLE: Latest value wins (by key)
INSERT INTO users_table (user_id, name, email)
VALUES (1, 'John', 'john@example.com');
-- UPDATES existing row with user_id=1
```

### Query Types

**1. Streaming Queries** (Continuous, Real-Time):
```sql
-- Filter events in real-time
SELECT user_id, page, timestamp
FROM clicks_stream
WHERE page = 'checkout'
EMIT CHANGES;

-- Transform on the fly
SELECT
  user_id,
  UPPER(page) AS page_upper,
  TIMESTAMPTOSTRING(timestamp, 'yyyy-MM-dd') AS date
FROM clicks_stream
EMIT CHANGES;
```

**2. Materialized Views** (Pre-Computed Tables):
```sql
-- Aggregate clicks per user (updates continuously)
CREATE TABLE user_click_counts AS
SELECT
  user_id,
  COUNT(*) AS click_count
FROM clicks_stream
GROUP BY user_id
EMIT CHANGES;

-- Query the table (instant results!)
SELECT * FROM user_click_counts WHERE user_id = 123;
```

**3. Pull Queries** (Point-in-Time Reads):
```sql
-- Query current state (like traditional SQL)
SELECT * FROM users_table WHERE user_id = 123;

-- No EMIT CHANGES = pull query (returns once)
```

## When to Use This Skill

Activate me when you need help with:
- ksqlDB syntax ("How to create ksqlDB stream?")
- Stream vs table concepts ("When to use stream vs table?")
- Joins ("Join stream with table")
- Aggregations ("Count events per user")
- Windowing ("Tumbling window aggregation")
- Real-time transformations ("Filter and enrich events")
- Materialized views ("Create pre-computed aggregates")

## Common Patterns

### Pattern 1: Filter Events

**Use Case**: Drop irrelevant events early

```sql
-- Create filtered stream
CREATE STREAM important_clicks AS
SELECT *
FROM clicks_stream
WHERE page IN ('checkout', 'payment', 'confirmation')
EMIT CHANGES;
```

### Pattern 2: Enrich Events (Stream-Table Join)

**Use Case**: Add user details to click events

```sql
-- Users table (current state)
CREATE TABLE users (
  user_id BIGINT PRIMARY KEY,
  name VARCHAR,
  email VARCHAR
) WITH (
  kafka_topic='users',
  value_format='AVRO'
);

-- Enrich clicks with user data
CREATE STREAM enriched_clicks AS
SELECT
  c.user_id,
  c.page,
  c.timestamp,
  u.name,
  u.email
FROM clicks_stream c
LEFT JOIN users u ON c.user_id = u.user_id
EMIT CHANGES;
```

### Pattern 3: Real-Time Aggregation

**Use Case**: Count events per user, per 5-minute window

```sql
CREATE TABLE user_clicks_per_5min AS
SELECT
  user_id,
  WINDOWSTART AS window_start,
  WINDOWEND AS window_end,
  COUNT(*) AS click_count
FROM clicks_stream
WINDOW TUMBLING (SIZE 5 MINUTES)
GROUP BY user_id
EMIT CHANGES;

-- Query current window
SELECT * FROM user_clicks_per_5min
WHERE user_id = 123
AND window_start >= NOW() - INTERVAL 5 MINUTES;
```

### Pattern 4: Detect Anomalies

**Use Case**: Alert when user clicks >100 times in 1 minute

```sql
CREATE STREAM high_click_alerts AS
SELECT
  user_id,
  COUNT(*) AS click_count
FROM clicks_stream
WINDOW TUMBLING (SIZE 1 MINUTE)
GROUP BY user_id
HAVING COUNT(*) > 100
EMIT CHANGES;
```

### Pattern 5: Change Data Capture (CDC)

**Use Case**: Track changes to user table

```sql
-- Create table from CDC topic (Debezium)
CREATE TABLE users_cdc (
  user_id BIGINT PRIMARY KEY,
  name VARCHAR,
  email VARCHAR,
  op VARCHAR  -- INSERT, UPDATE, DELETE
) WITH (
  kafka_topic='mysql.users.cdc',
  value_format='AVRO'
);

-- Stream of changes only
CREATE STREAM user_changes AS
SELECT * FROM users_cdc
WHERE op IN ('UPDATE', 'DELETE')
EMIT CHANGES;
```

## Join Types

### 1. Stream-Stream Join

**Use Case**: Correlate related events within time window

```sql
-- Join page views with clicks within 10 minutes
CREATE STREAM page_view_with_clicks AS
SELECT
  v.user_id,
  v.page AS viewed_page,
  c.page AS clicked_page
FROM page_views v
INNER JOIN clicks c WITHIN 10 MINUTES
ON v.user_id = c.user_id
EMIT CHANGES;
```

**Window Types**:
- `WITHIN 10 MINUTES` - Events must be within 10 minutes of each other
- `GRACE PERIOD 5 MINUTES` - Late-arriving events accepted for 5 more minutes

### 2. Stream-Table Join

**Use Case**: Enrich events with current state

```sql
-- Add product details to order events
CREATE STREAM enriched_orders AS
SELECT
  o.order_id,
  o.product_id,
  p.product_name,
  p.price
FROM orders_stream o
LEFT JOIN products_table p ON o.product_id = p.product_id
EMIT CHANGES;
```

### 3. Table-Table Join

**Use Case**: Combine two tables (latest state)

```sql
-- Join users with their current cart
CREATE TABLE user_with_cart AS
SELECT
  u.user_id,
  u.name,
  c.cart_total
FROM users u
LEFT JOIN shopping_carts c ON u.user_id = c.user_id
EMIT CHANGES;
```

## Windowing Types

### Tumbling Window (Non-Overlapping)

**Use Case**: Aggregate per fixed time period

```sql
-- Count events every 5 minutes
SELECT
  user_id,
  COUNT(*) AS event_count
FROM events
WINDOW TUMBLING (SIZE 5 MINUTES)
GROUP BY user_id;

-- Windows: [0:00-0:05), [0:05-0:10), [0:10-0:15)
```

### Hopping Window (Overlapping)

**Use Case**: Moving average over time

```sql
-- Count events in 10-minute windows, advancing every 5 minutes
SELECT
  user_id,
  COUNT(*) AS event_count
FROM events
WINDOW HOPPING (SIZE 10 MINUTES, ADVANCE BY 5 MINUTES)
GROUP BY user_id;

-- Windows: [0:00-0:10), [0:05-0:15), [0:10-0:20)
```

### Session Window (Event-Based)

**Use Case**: Group events by user session (gap-based)

```sql
-- Session ends after 30 minutes of inactivity
SELECT
  user_id,
  COUNT(*) AS session_events
FROM events
WINDOW SESSION (30 MINUTES)
GROUP BY user_id;
```

## Best Practices

### 1. Use Appropriate Data Types

✅ **DO**:
```sql
CREATE STREAM orders (
  order_id BIGINT,
  user_id BIGINT,
  total DECIMAL(10, 2),  -- Precise currency
  timestamp TIMESTAMP
);
```

❌ **DON'T**:
```sql
-- WRONG: Using DOUBLE for currency (precision loss!)
total DOUBLE
```

### 2. Always Specify Keys

✅ **DO**:
```sql
CREATE TABLE users (
  user_id BIGINT PRIMARY KEY,  -- Explicit key
  name VARCHAR
) WITH (kafka_topic='users');
```

❌ **DON'T**:
```sql
-- WRONG: No key specified (can't join!)
CREATE TABLE users (
  user_id BIGINT,
  name VARCHAR
);
```

### 3. Use Windowing for Aggregations

✅ **DO**:
```sql
-- Windowed aggregation (bounded memory)
SELECT COUNT(*) FROM events
WINDOW TUMBLING (SIZE 1 HOUR)
GROUP BY user_id;
```

❌ **DON'T**:
```sql
-- WRONG: Non-windowed aggregation (unbounded memory!)
SELECT COUNT(*) FROM events GROUP BY user_id;
```

### 4. Set Retention Policies

```sql
-- Limit table size (keep last 7 days)
CREATE TABLE user_stats (
  user_id BIGINT PRIMARY KEY,
  click_count BIGINT
) WITH (
  kafka_topic='user_stats',
  retention_ms=604800000  -- 7 days
);
```

## Performance Optimization

### 1. Partition Alignment

**Ensure joined streams/tables have same partition key**:

```sql
-- GOOD: Both keyed by user_id (co-partitioned)
CREATE STREAM clicks (user_id BIGINT KEY, ...)
CREATE TABLE users (user_id BIGINT PRIMARY KEY, ...)

-- Join works efficiently (no repartitioning)
SELECT * FROM clicks c
JOIN users u ON c.user_id = u.user_id;
```

### 2. Use Materialized Views

**Pre-compute expensive queries**:

```sql
-- BAD: Compute on every request
SELECT COUNT(*) FROM orders WHERE user_id = 123;

-- GOOD: Materialized table (instant lookup)
CREATE TABLE user_order_counts AS
SELECT user_id, COUNT(*) AS order_count
FROM orders GROUP BY user_id;

-- Query is now instant
SELECT order_count FROM user_order_counts WHERE user_id = 123;
```

### 3. Filter Early

```sql
-- GOOD: Filter before join
CREATE STREAM important_events AS
SELECT * FROM events WHERE event_type = 'purchase';

SELECT * FROM important_events e
JOIN users u ON e.user_id = u.user_id;

-- BAD: Join first, filter later (processes all events!)
SELECT * FROM events e
JOIN users u ON e.user_id = u.user_id
WHERE e.event_type = 'purchase';
```

## Common Issues & Solutions

### Issue 1: Query Timing Out

**Error**: Query timed out

**Root Cause**: Non-windowed aggregation on large stream

**Solution**: Add time window:
```sql
-- WRONG
SELECT COUNT(*) FROM events GROUP BY user_id;

-- RIGHT
SELECT COUNT(*) FROM events
WINDOW TUMBLING (SIZE 1 HOUR)
GROUP BY user_id;
```

### Issue 2: Partition Mismatch

**Error**: Cannot join streams (different partition keys)

**Solution**: Repartition stream:
```sql
-- Repartition stream by user_id
CREATE STREAM clicks_by_user AS
SELECT * FROM clicks PARTITION BY user_id;

-- Now join works
SELECT * FROM clicks_by_user c
JOIN users u ON c.user_id = u.user_id;
```

### Issue 3: Late-Arriving Events

**Solution**: Use grace period:
```sql
SELECT COUNT(*) FROM events
WINDOW TUMBLING (SIZE 5 MINUTES, GRACE PERIOD 1 MINUTE)
GROUP BY user_id;
-- Accepts events up to 1 minute late
```

## References

- ksqlDB Documentation: https://docs.ksqldb.io/
- ksqlDB Tutorials: https://kafka-tutorials.confluent.io/
- Windowing Guide: https://docs.ksqldb.io/en/latest/concepts/time-and-windows-in-ksqldb-queries/
- Join Types: https://docs.ksqldb.io/en/latest/developer-guide/joins/

---

**Invoke me when you need stream processing, real-time analytics, or SQL-like queries on Kafka!**
