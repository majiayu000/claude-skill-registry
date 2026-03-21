---
name: redis-patterns
description: Data structure selection, pub/sub patterns, Lua scripting, pipelining, and cluster topology strategies.
---

# Redis Patterns

Advanced Redis usage beyond simple key-value caching.

## Data Structure Selection

```
Use Case                → Structure      → Why
Session store           → Hash           → Partial field updates without full deserialize
Rate limiter            → Sorted Set     → ZRANGEBYSCORE for sliding window
Job queue               → List + Stream  → BRPOPLPUSH for reliable queue
Leaderboard             → Sorted Set     → ZREVRANGE with scores
Unique visitors         → HyperLogLog    → O(1) cardinality, 0.81% error
Feature flags           → Hash           → HGET per flag, HGETALL for bulk
Presence (who's online) → Set            → SADD/SREM, SMEMBERS
Geolocation             → Geo            → GEOSEARCH within radius
```

## Distributed Lock (Redlock-lite)

```typescript
import Redis from 'ioredis'

const redis = new Redis(process.env.REDIS_URL!)

async function acquireLock(
  key: string,
  ttlMs: number = 10_000
): Promise<string | null> {
  const token = crypto.randomUUID()
  const acquired = await redis.set(
    `lock:${key}`, token,
    'PX', ttlMs,
    'NX'  // Only set if not exists
  )
  return acquired === 'OK' ? token : null
}

async function releaseLock(key: string, token: string): Promise<boolean> {
  // Lua script: only delete if token matches (atomic check-and-delete)
  const script = `
    if redis.call("get", KEYS[1]) == ARGV[1] then
      return redis.call("del", KEYS[1])
    else
      return 0
    end
  `
  const result = await redis.eval(script, 1, `lock:${key}`, token)
  return result === 1
}

// Usage
async function processExclusively(resourceId: string): Promise<void> {
  const token = await acquireLock(resourceId, 5000)
  if (!token) throw new Error('Could not acquire lock')

  try {
    await doWork(resourceId)
  } finally {
    await releaseLock(resourceId, token)
  }
}
```

## Sliding Window Rate Limiter

```typescript
async function isRateLimited(
  userId: string,
  maxRequests: number,
  windowMs: number
): Promise<boolean> {
  const key = `ratelimit:${userId}`
  const now = Date.now()
  const windowStart = now - windowMs

  const pipeline = redis.pipeline()
  pipeline.zremrangebyscore(key, 0, windowStart)  // Remove expired entries
  pipeline.zadd(key, now.toString(), `${now}:${crypto.randomUUID()}`)
  pipeline.zcard(key)                              // Count entries in window
  pipeline.pexpire(key, windowMs)                  // Auto-cleanup

  const results = await pipeline.exec()
  const count = results![2][1] as number
  return count > maxRequests
}
```

## Lua Scripting for Atomicity

```typescript
// Problem: check-then-act is not atomic with separate commands
// Solution: Lua script executes atomically on Redis server

// Atomic counter with ceiling
const incrementWithCeiling = `
  local current = tonumber(redis.call("GET", KEYS[1]) or "0")
  local ceiling = tonumber(ARGV[1])
  if current >= ceiling then
    return -1
  end
  return redis.call("INCR", KEYS[1])
`

async function tryIncrement(key: string, max: number): Promise<number> {
  const result = await redis.eval(incrementWithCeiling, 1, key, max.toString())
  return result as number  // -1 means ceiling reached
}

// Atomic dequeue with conditional processing
const dequeueIfReady = `
  local item = redis.call("LPOP", KEYS[1])
  if item == nil then return nil end

  local data = cjson.decode(item)
  if data.scheduledAt and tonumber(data.scheduledAt) > tonumber(ARGV[1]) then
    redis.call("LPUSH", KEYS[1], item)  -- Put back, not ready yet
    return nil
  end
  redis.call("SADD", KEYS[2], item)  -- Move to processing set
  return item
`
```

## Pipeline for Bulk Operations

```typescript
// Without pipeline: N round trips
// With pipeline: 1 round trip for N commands

async function bulkGetUsers(userIds: string[]): Promise<Map<string, User>> {
  const pipeline = redis.pipeline()
  for (const id of userIds) {
    pipeline.hgetall(`user:${id}`)
  }

  const results = await pipeline.exec()
  const userMap = new Map<string, User>()

  for (let i = 0; i < userIds.length; i++) {
    const [err, data] = results![i]
    if (!err && data && Object.keys(data as object).length > 0) {
      userMap.set(userIds[i], data as User)
    }
  }
  return userMap
}
```

## Pub/Sub with Redis Streams

```typescript
// Streams > Pub/Sub: persistence, consumer groups, acknowledgment

// Producer
async function publishEvent(stream: string, event: Record<string, string>): Promise<string> {
  // MAXLEN ~ 10000: approximate trimming for performance
  return redis.xadd(stream, 'MAXLEN', '~', '10000', '*', ...Object.entries(event).flat())
}

// Consumer group setup
await redis.xgroup('CREATE', 'events', 'worker-group', '0', 'MKSTREAM')

// Consumer
async function consumeEvents(
  stream: string,
  group: string,
  consumer: string
): Promise<void> {
  while (true) {
    const entries = await redis.xreadgroup(
      'GROUP', group, consumer,
      'COUNT', '10',
      'BLOCK', '5000',  // Block up to 5s for new messages
      'STREAMS', stream, '>'
    )

    if (!entries) continue

    for (const [, messages] of entries) {
      for (const [id, fields] of messages) {
        try {
          await processEvent(Object.fromEntries(
            fields.reduce((acc: [string, string][], v, i, arr) =>
              i % 2 === 0 ? [...acc, [v, arr[i + 1]]] : acc, []
            )
          ))
          await redis.xack(stream, group, id)
        } catch (err) {
          console.error(`Failed to process ${id}:`, err)
          // Message stays pending, will be re-delivered
        }
      }
    }
  }
}
```

## Checklist

- [ ] Use appropriate data structure for each use case (not everything is a string)
- [ ] Pipeline bulk operations (avoid N round trips)
- [ ] Lua scripts for atomic multi-step operations
- [ ] Set TTL on every key (avoid memory leaks)
- [ ] Use SCAN instead of KEYS in production (KEYS blocks)
- [ ] Configure maxmemory-policy (allkeys-lru for cache, noeviction for queue)
- [ ] Monitor slow log: `SLOWLOG GET 10`
- [ ] Streams over Pub/Sub when message persistence needed

## Anti-Patterns

- Using KEYS * in production (blocks entire Redis, use SCAN)
- Storing large values (>1MB) in a single key (fragment or compress)
- No TTL on keys: silent memory leak until OOM
- Check-then-set without Lua: race condition between GET and SET
- Using Redis as primary database without persistence config (RDB/AOF)
- Single Redis instance for both cache and queue (eviction kills queue items)
