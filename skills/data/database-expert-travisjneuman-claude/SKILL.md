---
name: database-expert
description: Advanced database design and administration for PostgreSQL, MongoDB, and Redis. Use when designing schemas, optimizing queries, managing database performance, or implementing data patterns.
---

# Database Expert

Comprehensive guide for database design, optimization, and administration.

## Database Selection

| Database       | Type       | Best For                            |
| -------------- | ---------- | ----------------------------------- |
| **PostgreSQL** | Relational | Complex queries, ACID, JSON support |
| **MongoDB**    | Document   | Flexible schemas, rapid iteration   |
| **Redis**      | Key-Value  | Caching, sessions, real-time        |
| **SQLite**     | Embedded   | Mobile, desktop, testing            |

---

## PostgreSQL

### Schema Design

```sql
-- Users table with proper constraints
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'active'
        CHECK (status IN ('active', 'inactive', 'suspended')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Index for common queries
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_status ON users(status) WHERE status = 'active';

-- Automatic updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Posts with full-text search
CREATE TABLE posts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    author_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    tags TEXT[] DEFAULT '{}',
    search_vector TSVECTOR,
    published_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Full-text search index
CREATE INDEX idx_posts_search ON posts USING GIN(search_vector);
```

### Query Optimization

```sql
-- EXPLAIN ANALYZE for query analysis
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT u.full_name, COUNT(p.id) as post_count
FROM users u
LEFT JOIN posts p ON p.author_id = u.id
WHERE u.status = 'active'
GROUP BY u.id
ORDER BY post_count DESC
LIMIT 10;

-- Partial index for filtered queries
CREATE INDEX idx_posts_published
ON posts(published_at)
WHERE published_at IS NOT NULL;

-- Covering index (index-only scan)
CREATE INDEX idx_posts_author_title
ON posts(author_id)
INCLUDE (title, published_at);

-- Expression index
CREATE INDEX idx_users_email_lower
ON users(LOWER(email));
```

### Advanced Features

```sql
-- Common Table Expression (CTE)
WITH active_authors AS (
    SELECT DISTINCT author_id
    FROM posts
    WHERE published_at > NOW() - INTERVAL '30 days'
),
author_stats AS (
    SELECT
        u.id,
        u.full_name,
        COUNT(p.id) as total_posts
    FROM users u
    JOIN active_authors aa ON aa.author_id = u.id
    LEFT JOIN posts p ON p.author_id = u.id
    GROUP BY u.id
)
SELECT * FROM author_stats
ORDER BY total_posts DESC;

-- Window functions
SELECT
    id,
    title,
    author_id,
    published_at,
    ROW_NUMBER() OVER (PARTITION BY author_id ORDER BY published_at DESC) as author_rank,
    LAG(published_at) OVER (PARTITION BY author_id ORDER BY published_at) as prev_post_date
FROM posts
WHERE published_at IS NOT NULL;

-- JSON operations
SELECT
    id,
    metadata->>'source' as source,
    metadata->'stats'->>'views' as views
FROM posts
WHERE metadata @> '{"featured": true}';

-- Recursive CTE (for hierarchies)
WITH RECURSIVE category_tree AS (
    SELECT id, name, parent_id, 0 as depth
    FROM categories
    WHERE parent_id IS NULL
    UNION ALL
    SELECT c.id, c.name, c.parent_id, ct.depth + 1
    FROM categories c
    JOIN category_tree ct ON c.parent_id = ct.id
    WHERE ct.depth < 10
)
SELECT * FROM category_tree ORDER BY depth;
```

---

## MongoDB

### Schema Design Patterns

```javascript
// Embedding (for 1:few relationships)
const userSchema = {
  _id: ObjectId,
  email: String,
  profile: {
    firstName: String,
    lastName: String,
    avatar: String,
  },
  addresses: [
    {
      type: String,
      street: String,
      city: String,
    },
  ],
};

// Referencing (for 1:many relationships)
const postSchema = {
  _id: ObjectId,
  authorId: ObjectId,
  title: String,
  content: String,
  tags: [String],
};
```

### Aggregation Pipeline

```javascript
// Complex aggregation
db.orders.aggregate([
  {
    $match: {
      status: "completed",
      createdAt: { $gte: ISODate("2024-01-01") },
    },
  },
  {
    $lookup: {
      from: "users",
      localField: "userId",
      foreignField: "_id",
      as: "user",
    },
  },
  { $unwind: "$user" },
  {
    $group: {
      _id: { month: { $month: "$createdAt" } },
      totalRevenue: { $sum: "$total" },
      orderCount: { $sum: 1 },
    },
  },
  { $sort: { totalRevenue: -1 } },
]);
```

### Indexes

```javascript
// Compound index
db.posts.createIndex({ authorId: 1, createdAt: -1 });

// Text index
db.posts.createIndex(
  { title: "text", content: "text" },
  { weights: { title: 10, content: 1 } },
);

// Partial index
db.orders.createIndex(
  { createdAt: 1 },
  { partialFilterExpression: { status: "pending" } },
);

// TTL index (auto-expire)
db.sessions.createIndex({ createdAt: 1 }, { expireAfterSeconds: 3600 });
```

---

## Redis

### Data Structures

```redis
# Strings
SET user:1:name "John Doe"
GET user:1:name
SETEX session:abc123 3600 "user_data"
INCR page:home:views

# Hashes
HSET user:1 name "John" email "john@example.com"
HGETALL user:1

# Lists (queues)
LPUSH queue:jobs '{"type":"email"}'
RPOP queue:jobs

# Sets
SADD user:1:roles admin editor
SISMEMBER user:1:roles admin

# Sorted Sets (leaderboards)
ZADD leaderboard 1000 "player1" 1500 "player2"
ZREVRANGE leaderboard 0 9 WITHSCORES

# Streams (event log)
XADD events * type "user_login" user_id "123"
XREAD COUNT 10 STREAMS events 0
```

### Caching Patterns

```typescript
// Cache-aside pattern
async function getUser(userId: string): Promise<User> {
  const cacheKey = `user:${userId}`;
  const cached = await redis.get(cacheKey);

  if (cached) {
    return JSON.parse(cached);
  }

  const user = await db.users.findById(userId);
  await redis.setex(cacheKey, 3600, JSON.stringify(user));
  return user;
}

// Rate limiting
async function checkRateLimit(
  userId: string,
  limit: number,
  window: number,
): Promise<boolean> {
  const key = `ratelimit:${userId}`;
  const current = await redis.incr(key);

  if (current === 1) {
    await redis.expire(key, window);
  }

  return current <= limit;
}

// Distributed lock
async function acquireLock(
  resource: string,
  ttl: number,
): Promise<string | null> {
  const lockId = crypto.randomUUID();
  const acquired = await redis.set(`lock:${resource}`, lockId, "NX", "EX", ttl);
  return acquired ? lockId : null;
}

// Release lock with Lua script (atomic operation)
// Use EVALSHA with pre-loaded script for production
const releaseLockScript = `
  if redis.call("get", KEYS[1]) == ARGV[1] then
    return redis.call("del", KEYS[1])
  else
    return 0
  end
`;
```

### Pub/Sub

```typescript
// Publisher
async function publishEvent(channel: string, event: object): Promise<void> {
  await redis.publish(channel, JSON.stringify(event));
}

// Subscriber
const subscriber = redis.duplicate();
subscriber.subscribe("events");
subscriber.on("message", (channel, message) => {
  const event = JSON.parse(message);
  handleEvent(event);
});
```

---

## Query Optimization Checklist

### PostgreSQL

- [ ] Use EXPLAIN ANALYZE for slow queries
- [ ] Create indexes for WHERE, JOIN, ORDER BY columns
- [ ] Use partial indexes for filtered queries
- [ ] Use connection pooling (pgbouncer)
- [ ] Regular VACUUM and ANALYZE

### MongoDB

- [ ] Create compound indexes matching query patterns
- [ ] Use covered queries when possible
- [ ] Avoid large array fields in documents
- [ ] Monitor with explain()

### Redis

- [ ] Use appropriate data structures
- [ ] Set TTL on cache keys
- [ ] Use pipelining for bulk operations
- [ ] Monitor memory usage
