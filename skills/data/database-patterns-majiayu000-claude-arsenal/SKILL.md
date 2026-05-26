---
name: database-patterns
description: PostgreSQL + Redis database design patterns. Use for data modeling, indexing, caching strategies. Covers JSONB, tiered storage, cache consistency.
---
# Database Patterns

## Core Principles

- **PostgreSQL Primary** — Relational data, transactions, complex queries
- **Redis Secondary** — Caching, sessions, real-time data
- **Index-First Design** — Design queries before indexes
- **JSONB Sparingly** — Structured data prefers columns
- **Cache-Aside Default** — Read-through, write-around
- **Tiered Storage** — Hot/Warm/Cold data separation
- **No backwards compatibility** — Migrate data, don't keep legacy schemas

---

## PostgreSQL

### Data Type Selection

| Use Case | Type | Avoid |
|----------|------|-------|
| Primary Key | `UUID` / `BIGSERIAL` | `INT` (range limits) |
| Timestamps | `TIMESTAMPTZ` | `TIMESTAMP` (no timezone) |
| Money | `NUMERIC(19,4)` | `FLOAT` (precision loss) |
| Status | `TEXT` + CHECK | `INT` (unreadable) |
| Semi-structured | `JSONB` | `JSON` (no indexing) |
| Full-text | `TSVECTOR` | `LIKE '%..%'` |

### Schema Design

```sql
-- Use UUID for distributed-friendly IDs
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  email TEXT UNIQUE NOT NULL,
  name TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'active'
    CHECK (status IN ('active', 'inactive', 'suspended')),
  metadata JSONB DEFAULT '{}',
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Updated timestamp trigger
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER users_updated_at
  BEFORE UPDATE ON users
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at();
```

### Indexing Strategy

```sql
-- B-Tree: Equality, range, sorting (default)
CREATE INDEX idx_users_email ON users(email);

-- Composite: Leftmost prefix rule
-- Supports: (user_id), (user_id, created_at)
-- Does NOT support: (created_at) alone
CREATE INDEX idx_orders_user_date ON orders(user_id, created_at DESC);

-- Partial: Reduce index size
CREATE INDEX idx_active_users ON users(email)
  WHERE status = 'active';

-- GIN for JSONB: Containment queries
CREATE INDEX idx_metadata ON users USING GIN (metadata jsonb_path_ops);

-- Expression: Specific JSONB field
CREATE INDEX idx_user_role ON users ((metadata->>'role'));

-- Full-text search
CREATE INDEX idx_search ON products USING GIN (to_tsvector('english', name || ' ' || description));
```

### JSONB Usage

```sql
-- Good: Dynamic attributes, rarely queried fields
CREATE TABLE products (
  id UUID PRIMARY KEY,
  name TEXT NOT NULL,
  price NUMERIC(19,4) NOT NULL,
  category TEXT NOT NULL,           -- Extracted: frequently queried
  attributes JSONB DEFAULT '{}'     -- Dynamic: color, size, specs
);

-- Query with containment
SELECT * FROM products
WHERE category = 'electronics'              -- B-Tree index
  AND attributes @> '{"brand": "Apple"}';   -- GIN index

-- Query specific field
SELECT * FROM products
WHERE attributes->>'color' = 'black';       -- Expression index

-- Update JSONB field
UPDATE products
SET attributes = attributes || '{"featured": true}'
WHERE id = '...';
```

### Query Optimization

```sql
-- Always use EXPLAIN ANALYZE
EXPLAIN ANALYZE
SELECT u.*, COUNT(o.id) as order_count
FROM users u
LEFT JOIN orders o ON o.user_id = u.id
WHERE u.status = 'active'
GROUP BY u.id
ORDER BY u.created_at DESC
LIMIT 20;

-- Watch for:
-- ❌ Seq Scan on large tables → Add index
-- ❌ Sort → Use index for ordering
-- ❌ Nested Loop with many rows → Consider JOIN order
-- ❌ Hash Join on huge tables → Add indexes
```

### Connection Pooling

```typescript
// PgBouncer or built-in pool
import { Pool } from 'pg';

const pool = new Pool({
  max: 20,                      // Max connections
  idleTimeoutMillis: 30000,     // Close idle connections
  connectionTimeoutMillis: 2000, // Fail fast
});

// Connection count formula:
// connections = (cores * 2) + effective_spindle_count
// Usually 10-30 is enough
```

---

## Redis

### Data Structure Selection

| Use Case | Structure | Example |
|----------|-----------|---------|
| Cache objects | String | `user:123` → JSON |
| Counters | String + INCR | `views:article:456` |
| Sessions | Hash | `session:abc` → {userId, ...} |
| Leaderboards | Sorted Set | `scores` → {userId: score} |
| Queues | List/Stream | `tasks` → LPUSH/RPOP |
| Unique sets | Set | `online_users` |
| Real-time | Pub/Sub/Stream | Notifications |

### Key Naming

```
# Format: <entity>:<id>:<attribute>
user:123:profile
user:123:settings
order:456:items
session:abc123

# Use colons for hierarchy
# Enables pattern matching with SCAN
SCAN 0 MATCH "user:*:profile" COUNT 100
```

### TTL Strategy

```typescript
const TTL = {
  SESSION: 24 * 60 * 60,      // 24 hours
  CACHE: 15 * 60,             // 15 minutes
  RATE_LIMIT: 60,             // 1 minute
  LOCK: 30,                   // 30 seconds
};

// Set with TTL
await redis.set(`cache:user:${id}`, JSON.stringify(user), 'EX', TTL.CACHE);

// Check TTL
const remaining = await redis.ttl(`cache:user:${id}`);
```

---

## Caching Patterns

### Cache-Aside (Lazy Loading)

```typescript
async function getUser(id: string): Promise<User> {
  const cacheKey = `user:${id}`;

  // 1. Check cache
  const cached = await redis.get(cacheKey);
  if (cached) {
    return JSON.parse(cached);
  }

  // 2. Cache miss → Query database
  const user = await db.user.findUnique({ where: { id } });
  if (!user) {
    throw new NotFoundError('User not found');
  }

  // 3. Populate cache
  await redis.set(cacheKey, JSON.stringify(user), 'EX', 900);

  return user;
}
```

### Write-Through

```typescript
async function updateUser(id: string, data: UpdateInput): Promise<User> {
  // 1. Update database
  const user = await db.user.update({
    where: { id },
    data,
  });

  // 2. Update cache immediately
  await redis.set(`user:${id}`, JSON.stringify(user), 'EX', 900);

  return user;
}
```

### Cache Invalidation

```typescript
async function deleteUser(id: string): Promise<void> {
  // 1. Delete from database
  await db.user.delete({ where: { id } });

  // 2. Invalidate cache
  await redis.del(`user:${id}`);

  // 3. Invalidate related caches
  const keys = await redis.keys(`user:${id}:*`);
  if (keys.length > 0) {
    await redis.del(...keys);
  }
}
```

### Cache Stampede Prevention

```typescript
async function getUserWithLock(id: string): Promise<User> {
  const cacheKey = `user:${id}`;
  const lockKey = `lock:user:${id}`;

  // Check cache
  const cached = await redis.get(cacheKey);
  if (cached) {
    return JSON.parse(cached);
  }

  // Try to acquire lock
  const acquired = await redis.set(lockKey, '1', 'EX', 10, 'NX');

  if (!acquired) {
    // Another process is loading, wait and retry
    await sleep(100);
    return getUserWithLock(id);
  }

  try {
    // Double-check cache (another process might have populated it)
    const rechecked = await redis.get(cacheKey);
    if (rechecked) {
      return JSON.parse(rechecked);
    }

    // Load from database
    const user = await db.user.findUnique({ where: { id } });
    await redis.set(cacheKey, JSON.stringify(user), 'EX', 900);
    return user;
  } finally {
    await redis.del(lockKey);
  }
}
```

### Cache Penetration Prevention

```typescript
async function getUserSafe(id: string): Promise<User | null> {
  const cacheKey = `user:${id}`;

  const cached = await redis.get(cacheKey);

  // Check for cached null
  if (cached === 'NULL') {
    return null;
  }

  if (cached) {
    return JSON.parse(cached);
  }

  const user = await db.user.findUnique({ where: { id } });

  if (!user) {
    // Cache null with short TTL
    await redis.set(cacheKey, 'NULL', 'EX', 60);
    return null;
  }

  await redis.set(cacheKey, JSON.stringify(user), 'EX', 900);
  return user;
}
```

---

## Tiered Storage

```
┌─────────────────────────────────────────────────┐
│                   Application                    │
└─────────────────────────────────────────────────┘
                        │
        ┌───────────────┼───────────────┐
        ▼               ▼               ▼
   ┌─────────┐    ┌─────────┐    ┌─────────┐
   │  Redis  │    │ Postgres │    │ Archive │
   │  (Hot)  │    │  (Warm)  │    │  (Cold) │
   └─────────┘    └─────────┘    └─────────┘

   < 1ms          ~10ms           ~100ms+
   Active data    Recent data     Historical
   Memory         SSD             Object storage
```

### Partitioning for Cold Data

```sql
-- Partition by date range
CREATE TABLE orders (
  id UUID NOT NULL,
  user_id UUID NOT NULL,
  total NUMERIC(19,4) NOT NULL,
  created_at TIMESTAMPTZ NOT NULL
) PARTITION BY RANGE (created_at);

-- Create partitions
CREATE TABLE orders_2025_q1 PARTITION OF orders
  FOR VALUES FROM ('2025-01-01') TO ('2025-04-01');

CREATE TABLE orders_2025_q2 PARTITION OF orders
  FOR VALUES FROM ('2025-04-01') TO ('2025-07-01');

-- Archive old data
CREATE TABLE orders_archive (LIKE orders INCLUDING ALL);

-- Move old data to archive
WITH moved AS (
  DELETE FROM orders
  WHERE created_at < NOW() - INTERVAL '1 year'
  RETURNING *
)
INSERT INTO orders_archive SELECT * FROM moved;
```

---

## Transactions

### ACID Compliance

```typescript
// Use transactions for multi-table operations
async function transferFunds(fromId: string, toId: string, amount: number) {
  await db.$transaction(async (tx) => {
    // Deduct from source
    const from = await tx.account.update({
      where: { id: fromId },
      data: { balance: { decrement: amount } },
    });

    if (from.balance < 0) {
      throw new Error('Insufficient funds');
    }

    // Add to destination
    await tx.account.update({
      where: { id: toId },
      data: { balance: { increment: amount } },
    });
  });
}
```

### Optimistic Locking

```sql
-- Add version column
ALTER TABLE products ADD COLUMN version INT DEFAULT 1;

-- Update with version check
UPDATE products
SET
  stock = stock - 1,
  version = version + 1
WHERE id = $1 AND version = $2
RETURNING *;

-- If no rows returned, concurrent modification occurred
```

---

## Checklist

```markdown
## Schema
- [ ] UUID or BIGSERIAL for primary keys
- [ ] TIMESTAMPTZ for all timestamps
- [ ] NUMERIC for money, not FLOAT
- [ ] CHECK constraints for enums
- [ ] Foreign keys with ON DELETE

## Indexing
- [ ] Index for each WHERE clause pattern
- [ ] Composite indexes match query order
- [ ] GIN index for JSONB containment
- [ ] EXPLAIN ANALYZE for slow queries

## Caching
- [ ] Cache-aside as default pattern
- [ ] TTL on all cached data
- [ ] Cache invalidation on writes
- [ ] Stampede/penetration protection

## Operations
- [ ] Connection pooling configured
- [ ] Slow query logging enabled
- [ ] Backup and recovery tested
- [ ] Partition strategy for growth
```

---

## See Also

- [reference/postgresql.md](reference/postgresql.md) — PostgreSQL deep dive
- [reference/redis.md](reference/redis.md) — Redis patterns
- [reference/caching.md](reference/caching.md) — Caching strategies
