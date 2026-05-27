---
name: Bun Redis
description: Use when working with Redis in Bun (ioredis, Upstash), caching, pub/sub, session storage, or key-value operations.
---

# Bun Redis

Redis integration with Bun using popular Redis clients.

## Client Options

| Client | Best For | Install |
|--------|----------|---------|
| `ioredis` | Self-hosted Redis | `bun add ioredis` |
| `@upstash/redis` | Serverless/Edge | `bun add @upstash/redis` |
| `redis` | Official Node client | `bun add redis` |

## ioredis Setup

```typescript
import Redis from "ioredis";

// Default connection
const redis = new Redis();

// With options
const redis = new Redis({
  host: "localhost",
  port: 6379,
  password: "secret",
  db: 0,
});

// Connection string
const redis = new Redis("redis://:password@localhost:6379/0");

// TLS connection
const redis = new Redis({
  host: "redis.example.com",
  port: 6380,
  tls: {},
});
```

## Basic Operations

```typescript
import Redis from "ioredis";

const redis = new Redis();

// Strings
await redis.set("name", "Alice");
await redis.set("count", "100");
await redis.setex("temp", 60, "expires in 60s"); // With TTL

const name = await redis.get("name"); // "Alice"
const count = await redis.incr("count"); // 101
await redis.del("name");

// Check existence
const exists = await redis.exists("name"); // 0 or 1

// TTL
await redis.expire("key", 3600); // Set 1 hour TTL
const ttl = await redis.ttl("key"); // Get remaining TTL
```

## Data Structures

### Hashes

```typescript
// Set hash fields
await redis.hset("user:1", {
  name: "Alice",
  email: "alice@example.com",
  age: "30",
});

// Get single field
const name = await redis.hget("user:1", "name");

// Get all fields
const user = await redis.hgetall("user:1");
// { name: "Alice", email: "...", age: "30" }

// Increment field
await redis.hincrby("user:1", "visits", 1);
```

### Lists

```typescript
// Add to list
await redis.rpush("queue", "task1", "task2");
await redis.lpush("queue", "urgent");

// Pop from list
const task = await redis.lpop("queue"); // "urgent"
const blocking = await redis.blpop("queue", 5); // Wait 5s

// Range
const items = await redis.lrange("queue", 0, -1);
```

### Sets

```typescript
// Add members
await redis.sadd("tags", "javascript", "typescript", "bun");

// Check membership
const isMember = await redis.sismember("tags", "bun"); // 1

// Get all members
const tags = await redis.smembers("tags");

// Set operations
await redis.sinter("tags1", "tags2"); // Intersection
await redis.sunion("tags1", "tags2"); // Union
```

### Sorted Sets

```typescript
// Add with scores
await redis.zadd("leaderboard", 100, "alice", 200, "bob", 150, "charlie");

// Get by rank
const top3 = await redis.zrevrange("leaderboard", 0, 2, "WITHSCORES");

// Get by score range
const highScores = await redis.zrangebyscore("leaderboard", 100, 200);

// Increment score
await redis.zincrby("leaderboard", 50, "alice");
```

## JSON (RedisJSON)

```typescript
// Requires RedisJSON module
await redis.call("JSON.SET", "user:1", "$", JSON.stringify({
  name: "Alice",
  settings: { theme: "dark" },
}));

const user = await redis.call("JSON.GET", "user:1");
const settings = await redis.call("JSON.GET", "user:1", "$.settings");
```

## Pub/Sub

```typescript
import Redis from "ioredis";

// Publisher
const pub = new Redis();

// Subscriber
const sub = new Redis();

// Subscribe to channel
sub.subscribe("notifications", (err, count) => {
  console.log(`Subscribed to ${count} channels`);
});

// Handle messages
sub.on("message", (channel, message) => {
  console.log(`${channel}: ${message}`);
});

// Publish
await pub.publish("notifications", JSON.stringify({
  type: "alert",
  message: "Hello!",
}));

// Pattern subscribe
sub.psubscribe("user:*");
sub.on("pmessage", (pattern, channel, message) => {
  console.log(`${pattern} -> ${channel}: ${message}`);
});
```

## Transactions

```typescript
// Multi/Exec
const results = await redis
  .multi()
  .set("key1", "value1")
  .set("key2", "value2")
  .incr("counter")
  .exec();

// Pipeline (no atomicity, better performance)
const pipeline = redis.pipeline();
pipeline.set("key1", "value1");
pipeline.set("key2", "value2");
pipeline.incr("counter");
const results = await pipeline.exec();
```

## Upstash Redis (Serverless)

```typescript
import { Redis } from "@upstash/redis";

const redis = new Redis({
  url: process.env.UPSTASH_REDIS_REST_URL,
  token: process.env.UPSTASH_REDIS_REST_TOKEN,
});

// Same API as ioredis
await redis.set("key", "value");
const value = await redis.get("key");

// With automatic JSON serialization
await redis.set("user", { name: "Alice", age: 30 });
const user = await redis.get<{ name: string; age: number }>("user");
```

## Caching Patterns

### Cache-Aside

```typescript
async function getUser(id: string) {
  // Check cache
  const cached = await redis.get(`user:${id}`);
  if (cached) {
    return JSON.parse(cached);
  }

  // Fetch from database
  const user = await db.query.users.findFirst({
    where: eq(users.id, id),
  });

  // Cache for 1 hour
  if (user) {
    await redis.setex(`user:${id}`, 3600, JSON.stringify(user));
  }

  return user;
}
```

### Write-Through

```typescript
async function updateUser(id: string, data: UserUpdate) {
  // Update database
  await db.update(users).set(data).where(eq(users.id, id));

  // Update cache
  const user = await db.query.users.findFirst({
    where: eq(users.id, id),
  });
  await redis.setex(`user:${id}`, 3600, JSON.stringify(user));

  return user;
}
```

### Rate Limiting

```typescript
async function rateLimit(key: string, limit: number, window: number) {
  const current = await redis.incr(key);

  if (current === 1) {
    await redis.expire(key, window);
  }

  return current <= limit;
}

// Usage
const allowed = await rateLimit(`rate:${userId}`, 100, 60);
if (!allowed) {
  throw new Error("Rate limit exceeded");
}
```

## Session Storage

```typescript
import { Hono } from "hono";
import Redis from "ioredis";
import { v4 as uuid } from "uuid";

const redis = new Redis();
const app = new Hono();

app.use("*", async (c, next) => {
  const sessionId = c.req.header("X-Session-Id") || uuid();
  const session = await redis.hgetall(`session:${sessionId}`);

  c.set("session", session);
  c.set("sessionId", sessionId);

  await next();

  // Save session
  const updatedSession = c.get("session");
  if (Object.keys(updatedSession).length > 0) {
    await redis.hset(`session:${sessionId}`, updatedSession);
    await redis.expire(`session:${sessionId}`, 86400); // 24h
  }
});
```

## Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `ECONNREFUSED` | Redis not running | Start Redis server |
| `NOAUTH` | Authentication required | Provide password |
| `WRONGTYPE` | Wrong data type | Check key type |
| `OOM` | Out of memory | Configure maxmemory |

## When to Load References

Load `references/clustering.md` when:
- Redis Cluster setup
- Sentinel configuration
- High availability patterns

Load `references/lua-scripts.md` when:
- Custom Lua scripts
- Atomic operations
- Complex transactions
