---
name: api-database-redis
description: Redis in-memory data store patterns with ioredis and node-redis -- caching, sessions, rate limiting, pub/sub, streams, queues, transactions, cluster
---

# Redis Patterns

> **Quick Guide:** Use Redis as an in-memory data store for caching, session management, rate limiting, pub/sub messaging, and job queues. Use **ioredis** (v5.x) as the primary client for its superior TypeScript support, Cluster/Sentinel integration, auto-pipelining, and Lua scripting. Use **node-redis** (v5.x) only when you need Redis Stack modules (JSON, Search, TimeSeries). Always set `maxRetriesPerRequest: null` for BullMQ workers, use separate connections for Pub/Sub subscribers, and define Lua scripts via `defineCommand` for atomic multi-step operations.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST use a SEPARATE Redis connection for Pub/Sub subscribers -- a subscribed connection enters a special mode and cannot execute other commands)**

**(You MUST set `maxRetriesPerRequest: null` on any ioredis connection passed to BullMQ -- BullMQ requires infinite retries and will throw if this is not set)**

**(You MUST use Lua scripts (`defineCommand` or `eval`) for any operation requiring atomicity across multiple Redis commands -- separate commands are NOT atomic even in a pipeline)**

**(You MUST handle the `error` event on every Redis client instance -- unhandled errors crash the Node.js process)**

</critical_requirements>

---

## Examples

- [Core Patterns](examples/core.md) -- ioredis/node-redis connection, error handling, reconnection, cluster, sentinel, pipelining, transactions
- [Caching Patterns](examples/caching.md) -- Cache-aside, write-through, invalidation, stampede prevention, multi-key pipeline
- [Data Structures](examples/data-structures.md) -- Strings, hashes, lists, sets, sorted sets with typed helpers
- [Sessions](examples/sessions.md) -- Express connect-redis (node-redis required for v9+), Hono manual middleware
- [Pub/Sub](examples/pub-sub.md) -- Publish/subscribe, event broadcasting, pattern subscriptions
- [Rate Limiting](examples/rate-limiting.md) -- Sliding window (Lua), token bucket (Lua), middleware integration
- [Queues & Locks](examples/queues.md) -- BullMQ job queues, Redis Streams with consumer groups, distributed locks

**Additional resources:**

- [reference.md](reference.md) -- Command cheat sheet, connection options, anti-patterns, production checklist

---

**Auto-detection:** Redis, ioredis, node-redis, createClient, RedisStore, BullMQ, Queue, Worker, pub/sub, MULTI, EXEC, pipeline, Lua script, defineCommand, xadd, xread, cache-aside, rate limit, session store, connect-redis, Redis.Cluster, Sentinel

**When to use:**

- Caching database queries or API responses (cache-aside, write-through)
- Session storage for Express/Hono/Fastify applications
- Distributed rate limiting (sliding window, token bucket)
- Real-time messaging with Pub/Sub
- Background job processing with BullMQ queues
- Leaderboards, counters, and real-time analytics with sorted sets
- Distributed locks and atomic operations with Lua scripts

**Key patterns covered:**

- ioredis connection setup, configuration, and error handling
- Data structures (strings, hashes, lists, sets, sorted sets, streams)
- Cache-aside and write-through caching with TTL management
- Session storage with connect-redis
- Rate limiting with Lua scripts (sliding window, token bucket)
- Pub/Sub messaging with separate connections
- Redis Streams for persistent message queues
- BullMQ for job queues with retries and scheduling
- Pipelining and transactions (MULTI/EXEC)
- Lua scripting for atomic operations
- Cluster mode and Sentinel for high availability

**When NOT to use:**

- Primary database for relational data (use your relational database)
- Document storage with complex queries (use a document database)
- Large binary file storage (use S3/object storage)
- Data that must survive total memory loss without persistence configured

---

<philosophy>

## Philosophy

Redis is an **in-memory data store** used as a cache, message broker, and streaming engine. The core principle: **use Redis for fast, ephemeral, or real-time data -- not as a primary database.**

**Core principles:**

1. **Cache, don't store** -- Redis complements your primary database. Cache frequently accessed data, but always have a source of truth elsewhere.
2. **Atomic operations** -- Use Lua scripts or MULTI/EXEC for operations spanning multiple keys. Individual Redis commands are atomic, but sequences are not.
3. **Separate concerns** -- Use different Redis databases (or key prefixes) for caching, sessions, and queues. Use separate connections for Pub/Sub.
4. **Set TTLs on everything** -- Memory is finite. Every cached key should expire. Use `EX` (seconds) or `PX` (milliseconds) on SET commands.
5. **Fail gracefully** -- Redis is a cache, not a database. If Redis is down, the application should degrade gracefully (bypass cache, use database directly).

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: ioredis Connection Setup

Configure ioredis with proper error handling and reconnection strategy. See [examples/core.md](examples/core.md) for full examples including node-redis and cluster configuration.

```typescript
// ✅ Good Example - Proper ioredis setup with error handling
import Redis from "ioredis";

const RETRY_DELAY_BASE_MS = 50;
const RETRY_DELAY_MAX_MS = 2000;

function createRedisClient(): Redis {
  const url = process.env.REDIS_URL;
  if (!url) {
    throw new Error("REDIS_URL environment variable is required");
  }

  const client = new Redis(url, {
    maxRetriesPerRequest: 3,
    retryStrategy(times) {
      return Math.min(times * RETRY_DELAY_BASE_MS, RETRY_DELAY_MAX_MS);
    },
    lazyConnect: true,
  });

  client.on("error", (err) => {
    console.error("Redis connection error:", err.message);
  });

  return client;
}

export { createRedisClient };
```

**Why good:** Environment variable validation, named constants for retry delays, `lazyConnect` prevents connection before ready, error event handler prevents process crash

```typescript
// ❌ Bad Example - No error handling, hardcoded config
import Redis from "ioredis";
const redis = new Redis("redis://localhost:6379");
// No error handler, no retry strategy, hardcoded URL
```

**Why bad:** Missing error event handler crashes Node.js process on connection failure, hardcoded URL prevents environment-specific configuration

---

### Pattern 2: Cache-Aside

Check cache first, fall back to database on miss, populate cache. See [examples/caching.md](examples/caching.md) for write-through, invalidation, stampede prevention, and multi-key cache patterns.

```typescript
// ✅ Good Example - Generic cache-aside helper
const CACHE_TTL_SECONDS = 300;

async function cacheAside<T>(
  redis: Redis,
  key: string,
  fetcher: () => Promise<T>,
  ttlSeconds: number = CACHE_TTL_SECONDS,
): Promise<T> {
  const cached = await redis.get(key);
  if (cached !== null) {
    return JSON.parse(cached) as T;
  }

  const data = await fetcher();

  // Fire-and-forget cache write
  redis.set(key, JSON.stringify(data), "EX", ttlSeconds).catch((err) => {
    console.error(`Cache write failed for ${key}:`, err.message);
  });

  return data;
}
```

**Why good:** Generic `cacheAside<T>` works with any data type, fire-and-forget cache write prevents cache failure from blocking response, configurable TTL

---

### Pattern 3: Pipelining and Transactions

Batch commands for network efficiency (pipeline) or atomicity (MULTI/EXEC). See [examples/core.md](examples/core.md) for full examples.

```typescript
// ✅ Pipeline - batch for network efficiency (NOT atomic)
const pipeline = redis.pipeline();
pipeline.hset(key, { name: user.name, email: user.email });
pipeline.expire(key, TTL_SECONDS);
await pipeline.exec();

// ✅ Transaction - atomic execution with optimistic locking
await redis.watch(fromKey);
const results = await redis
  .multi()
  .decrby(fromKey, amount)
  .incrby(toKey, amount)
  .exec();
if (!results) {
  /* WATCH detected change, retry */
}
```

**Why good:** Pipeline reduces round-trips, MULTI/EXEC provides atomicity, WATCH enables optimistic locking

```typescript
// ❌ Bad Example - Non-atomic balance transfer
await redis.decrby("balance:user1", 100);
await redis.incrby("balance:user2", 100);
// Crash between commands causes data loss
```

**Why bad:** Two separate commands are not atomic, crash between them causes data inconsistency

---

### Pattern 4: Lua Scripting for Atomicity

Lua scripts execute atomically on the Redis server. See [examples/rate-limiting.md](examples/rate-limiting.md) for complete Lua-based rate limiters.

```typescript
// ✅ Define custom atomic command
redis.defineCommand("rateLimit", {
  numberOfKeys: 1,
  lua: `
    local key = KEYS[1]
    local limit = tonumber(ARGV[1])
    local window = tonumber(ARGV[2])
    local now = tonumber(ARGV[3])
    redis.call('ZREMRANGEBYSCORE', key, 0, now - window)
    local count = redis.call('ZCARD', key)
    if count < limit then
      redis.call('ZADD', key, now, now .. '-' .. math.random(1000000))
      redis.call('EXPIRE', key, window)
      return 1
    end
    return 0
  `,
});
```

**Why good:** `defineCommand` uses EVALSHA internally for performance, Lua script is atomic -- no race conditions

---

### Pattern 5: Pub/Sub Messaging

Requires **separate connections** for subscribing and publishing. See [examples/pub-sub.md](examples/pub-sub.md) for event broadcasting system.

```typescript
// ✅ Good Example - Separate connections
const publisher = new Redis(url);
const subscriber = new Redis(url); // MUST be separate

await subscriber.subscribe("notifications");
subscriber.on("message", (channel, message) => {
  handleNotification(JSON.parse(message));
});

await publisher.publish("notifications", JSON.stringify(data));
```

**Why good:** Separate connections for pub and sub (required by Redis protocol), error handlers on both

```typescript
// ❌ Bad Example - Same connection
const redis = new Redis();
await redis.subscribe("channel");
await redis.set("key", "value"); // THROWS: connection is in subscriber mode
```

**Why bad:** A subscribed connection cannot execute non-pub/sub commands

---

### Pattern 6: BullMQ Job Queues

Robust job queuing with retries, scheduling, and priorities. See [examples/queues.md](examples/queues.md) for complete examples with workers, events, and graceful shutdown.

```typescript
// ✅ Good Example - BullMQ connection factory
function createBullMQConnection(): Redis {
  return new Redis(process.env.REDIS_URL!, {
    maxRetriesPerRequest: null, // REQUIRED for BullMQ
  });
}

const emailQueue = new Queue<EmailJobData>(QUEUE_NAME, {
  connection: createBullMQConnection(),
  defaultJobOptions: {
    attempts: MAX_RETRY_ATTEMPTS,
    backoff: { type: "exponential", delay: BACKOFF_DELAY_MS },
  },
});
```

**Why good:** `maxRetriesPerRequest: null` is required for BullMQ, separate connection per Queue/Worker

```typescript
// ❌ Bad Example - Missing required config
const connection = new Redis(); // Missing maxRetriesPerRequest: null
const queue = new Queue("emails", { connection });
// BullMQ will throw: "maxRetriesPerRequest must be null"
```

**Why bad:** BullMQ requires infinite retries -- without `null`, ioredis gives up after a set number of attempts

---

### Pattern 7: Redis Streams

Persistent, ordered message logs with consumer groups. See [examples/queues.md](examples/queues.md) for full producer/consumer implementation with pending message recovery.

```typescript
// Producer
const entryId = await redis.xadd(
  STREAM_KEY,
  "*",
  "orderId",
  id,
  "action",
  action,
);

// Consumer group setup (idempotent)
try {
  await redis.xgroup("CREATE", STREAM_KEY, GROUP_NAME, "0", "MKSTREAM");
} catch (err) {
  if (!(err instanceof Error) || !err.message.includes("BUSYGROUP")) throw err;
}

// Consumer read + acknowledge
const results = await redis.xreadgroup(
  "GROUP",
  GROUP_NAME,
  consumerName,
  "COUNT",
  "10",
  "BLOCK",
  "5000",
  "STREAMS",
  STREAM_KEY,
  ">",
);
await redis.xack(STREAM_KEY, GROUP_NAME, messageId);
```

**Why good:** MKSTREAM creates stream if absent, BUSYGROUP handling for idempotent setup, XACK confirms processing

</patterns>

---

<performance>

## Performance Optimization

- **Auto-pipelining** -- Enable `enableAutoPipelining: true` to batch commands issued during the same event loop tick. Does NOT work with WATCH/MULTI or blocking commands. See [examples/core.md](examples/core.md) for setup.
- **Manual pipelining** -- Use `redis.pipeline()` for explicit command batching. See [examples/core.md](examples/core.md).
- **Key expiration** -- Set TTLs on all cache keys. Use named constants (`TTL_SHORT_SECONDS = 60`, `TTL_MEDIUM_SECONDS = 300`, etc.). See [examples/core.md](examples/core.md).
- **SCAN over KEYS** -- Never use `KEYS` in production (blocks Redis). Use `redis.scanStream({ match: "pattern", count: 100 })`. See [examples/core.md](examples/core.md).
- **UNLINK over DEL** -- Use `unlink` for large keys (non-blocking deletion).

</performance>

---

<decision_framework>

## Decision Framework

### Which Redis Client?

```
Which Redis client should I use?
├─ Need Redis Stack modules (JSON, Search, TimeSeries)? -> node-redis (v5.x)
├─ Using BullMQ for job queues? -> ioredis (BullMQ requires it)
├─ Need Cluster or Sentinel support? -> ioredis (built-in, battle-tested)
├─ Need auto-pipelining? -> ioredis (enableAutoPipelining option)
└─ General caching/sessions/pub-sub? -> ioredis (recommended default)
```

### Which Caching Strategy?

```
How should I cache this data?
├─ Read-heavy, tolerates brief staleness? -> Cache-aside with TTL
├─ Needs strong consistency after writes? -> Write-through (update DB + invalidate cache)
├─ Write-heavy, can tolerate brief data loss? -> Write-behind (async cache update)
└─ Data changes rarely? -> Cache-aside with long TTL + manual invalidation
```

### Which Data Structure?

```
What Redis data structure should I use?
├─ Simple key-value (cache, sessions)? -> Strings (GET/SET)
├─ Object with multiple fields? -> Hashes (HSET/HGET)
├─ Ordered ranking/leaderboard? -> Sorted Sets (ZADD/ZRANGE)
├─ Queue (FIFO/LIFO)? -> Lists (LPUSH/RPOP)
├─ Unique collection (tags, categories)? -> Sets (SADD/SMEMBERS)
├─ Persistent message log with consumers? -> Streams (XADD/XREAD)
└─ Rate limiting (sliding window)? -> Sorted Sets + Lua script
```

### Which Messaging Pattern?

```
How should I implement real-time messaging?
├─ Fire-and-forget broadcast? -> Pub/Sub (no persistence)
├─ Need message persistence and replay? -> Streams with consumer groups
├─ Need reliable job processing with retries? -> BullMQ (built on Redis)
└─ Need request-reply pattern? -> Pub/Sub with correlation IDs
```

### Atomicity Decision

```
Do I need atomicity across multiple commands?
├─ YES -> Are the commands on the same key?
│   ├─ YES -> Use a single atomic command (INCR, SETNX, etc.)
│   └─ NO -> Use Lua script (defineCommand)
├─ NO, but I want batching -> Use pipeline (non-atomic, single round-trip)
└─ Need optimistic locking? -> Use WATCH + MULTI/EXEC
```

</decision_framework>

---

<integration>

## Integration Guide

**Common integration patterns:**

- **Database caching** -- Cache query results using cache-aside pattern; invalidate cache on writes
- **HTTP framework sessions** -- Session storage middleware, rate limiting middleware
- **BullMQ job queues** -- Built on Redis (requires ioredis with `maxRetriesPerRequest: null`)
- **WebSocket scaling** -- Redis adapter for distributing WebSocket connections across servers

**Replaces / Conflicts with:**

- **In-memory caches** -- Redis provides distributed caching across multiple app instances
- **Database-backed sessions** -- Redis sessions are faster and reduce database load
- **Simple message queues** -- Redis Streams and BullMQ cover most queue use cases; use dedicated message brokers for complex routing or massive throughput

</integration>

---

<red_flags>

## RED FLAGS

**High Priority Issues:**

- Using the same connection for Pub/Sub subscribe and regular commands -- subscribed connections cannot execute non-pub/sub commands
- Missing `maxRetriesPerRequest: null` on BullMQ connections -- BullMQ throws immediately without this setting
- Using `KEYS` command in production -- blocks the entire Redis server while scanning all keys
- No `error` event handler on Redis client -- unhandled errors crash the Node.js process
- Storing large objects (> 1 MB) in Redis -- degrades performance and wastes memory; store a reference and fetch from object storage

**Medium Priority Issues:**

- Missing TTL on cached keys -- causes unbounded memory growth until Redis runs out of memory
- Using `del` with many keys instead of `unlink` -- `del` blocks Redis; `unlink` frees memory asynchronously
- Not using pipelining for batch operations -- each command is a separate network round-trip
- Serializing/deserializing complex objects without error handling -- malformed JSON in cache crashes on parse
- Sharing a single Redis connection across BullMQ Queue and Worker -- each needs its own connection

**Common Mistakes:**

- Assuming pipeline commands are atomic -- pipelines batch for network efficiency but do not provide atomicity (use MULTI/EXEC or Lua)
- Forgetting that `hgetall` returns an empty object `{}` for non-existent keys (not `null`) -- check `Object.keys(result).length === 0`
- Using `MULTI/EXEC` without `WATCH` for conditional updates -- transactions execute unconditionally unless you WATCH keys first
- Not handling `null` returns from `GET` -- cache misses return `null`, not `undefined`
- Connecting to Redis without TLS in production -- credentials sent in plaintext over the network

**Gotchas & Edge Cases:**

- Redis `HGETALL` returns all values as strings -- numbers stored with `HSET` come back as strings, requiring explicit parsing
- `EXPIRE` resets when a key is overwritten with `SET` -- if you `SET` a key that already has a TTL, the TTL is removed unless you include `EX`/`PX` in the `SET` command
- Pub/Sub messages are fire-and-forget -- if no subscriber is listening when a message is published, it is lost forever (use Streams for persistence)
- Redis Cluster does not support multi-key operations across different hash slots -- use `{hash-tag}` prefix to force related keys to the same slot
- `WATCH` is connection-scoped -- concurrent requests sharing a connection will interfere with each other's WATCH state
- ioredis auto-pipelining does not work with `WATCH`/`MULTI` or blocking commands (`BRPOP`, `BLPOP`, `XREAD BLOCK`)

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST use a SEPARATE Redis connection for Pub/Sub subscribers -- a subscribed connection enters a special mode and cannot execute other commands)**

**(You MUST set `maxRetriesPerRequest: null` on any ioredis connection passed to BullMQ -- BullMQ requires infinite retries and will throw if this is not set)**

**(You MUST use Lua scripts (`defineCommand` or `eval`) for any operation requiring atomicity across multiple Redis commands -- separate commands are NOT atomic even in a pipeline)**

**(You MUST handle the `error` event on every Redis client instance -- unhandled errors crash the Node.js process)**

**Failure to follow these rules will cause pub/sub failures, BullMQ connection errors, race conditions, and application crashes.**

</critical_reminders>
