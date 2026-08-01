---
name: api-database-vercel-kv
description: Serverless Redis-compatible key-value store via Upstash REST API -- edge-compatible, automatic JSON serialization, TTL-based caching
---

# Vercel KV / Upstash Redis Patterns

> **Quick Guide:** Use `@upstash/redis` (the successor to `@vercel/kv`) for serverless, edge-compatible Redis via REST API. Key gotchas: REST adds ~5-15ms latency per call vs TCP Redis, all values are auto-serialized as JSON (objects round-trip transparently but `Date` objects become strings), pipeline/multi execute as single HTTP requests but pipeline is NOT atomic. Use `Redis.fromEnv()` for automatic connection. Always set TTLs -- serverless Redis is billed per command.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST use `@upstash/redis` for new projects -- `@vercel/kv` was deprecated in December 2024 and all stores were migrated to Upstash Redis)**

**(You MUST set TTLs on all cached data -- serverless Redis is billed per command and has storage limits per plan)**

**(You MUST understand that this is a REST/HTTP client, NOT a TCP Redis client -- each command is an HTTP request with ~5-15ms overhead, so batch with pipelines when possible)**

</critical_requirements>

---

## Examples

- [Core Patterns](examples/core.md) -- Client setup, CRUD operations, TTL, hashes, pipelines, transactions, rate limiting, sessions

**Additional resources:**

- [reference.md](reference.md) -- Command quick reference, environment variables, plan limits

---

**Auto-detection:** Vercel KV, @vercel/kv, @upstash/redis, Upstash Redis, KV_REST_API_URL, KV_REST_API_TOKEN, UPSTASH_REDIS_REST_URL, UPSTASH_REDIS_REST_TOKEN, Redis.fromEnv, kv.set, kv.get, kv.hset, kv.hget, kv.incr, kv.expire, kv.del, createClient, automaticDeserialization, edge Redis, serverless Redis

**When to use:**

- Caching API responses or database queries in Vercel serverless/edge functions
- Rate limiting at the edge (sliding window counters)
- Session storage for serverless applications
- Feature flags, A/B test assignments, or short-lived counters
- Any Redis use case on Vercel where TCP connections are unavailable (edge runtime)

**Key patterns covered:**

- Client initialization (`Redis.fromEnv()`, `new Redis()`)
- Basic CRUD with automatic JSON serialization
- TTL and expiration strategies
- Hash operations for structured data
- Pipelines (batched HTTP) and transactions (atomic MULTI/EXEC)
- Rate limiting with sorted sets
- Session storage patterns

**When NOT to use:**

- High-throughput, low-latency Redis workloads (use ioredis with TCP -- REST adds per-request overhead)
- Pub/Sub subscribers (REST is request-response, not persistent connections)
- Redis Streams consumers (requires TCP client like ioredis)
- Large value storage (>1 MB per record on free tier, billed by command count)
- Primary database (Redis is a cache/ephemeral store, not a source of truth)

---

<philosophy>

## Philosophy

Upstash Redis (formerly Vercel KV) is a **serverless, REST-based Redis** designed for edge and serverless runtimes where TCP connections are unavailable or impractical. The core trade-off: **HTTP compatibility everywhere, at the cost of per-request latency overhead.**

**Core principles:**

1. **REST-first** -- Every Redis command is an HTTP request. This works everywhere (edge, serverless, browsers) but adds ~5-15ms per call. Batch with pipelines.
2. **Auto-serialization** -- Objects are JSON-serialized on write and deserialized on read. This is convenient but means `Date` objects, `Map`, `Set`, and functions are not preserved faithfully.
3. **Ephemeral by design** -- Set TTLs on everything. Serverless Redis is billed per command and has storage caps. Treat it as a cache, not a database.
4. **Zero connection management** -- No connection pools, no reconnection logic, no `error` event handlers. Each request is stateless HTTP.

</philosophy>

---

<patterns>

## Core Patterns

> Full implementations with good/bad pairs: [examples/core.md](examples/core.md)

### Pattern 1: Client Initialization

Two approaches: `Redis.fromEnv()` (preferred on Vercel -- reads `UPSTASH_REDIS_REST_URL` and `UPSTASH_REDIS_REST_TOKEN` automatically) or `new Redis({ url, token })` for explicit configuration. Never hardcode credentials.

```typescript
import { Redis } from "@upstash/redis";
const redis = Redis.fromEnv();
export { redis };
```

---

### Pattern 2: Automatic JSON Serialization

The SDK auto-serializes objects to JSON on write and deserializes on read. Never call `JSON.stringify` manually -- it causes double-serialization. Use `get<T>()` for typed returns, `satisfies` for type-safe writes. `Date` objects become ISO strings on round-trip -- store timestamps as numbers instead.

```typescript
await redis.set("user:123", data satisfies UserProfile, { ex: TTL_SECONDS });
const user = await redis.get<UserProfile>("user:123"); // UserProfile | null
```

---

### Pattern 3: TTL and Expiration

Always set TTLs -- serverless Redis is billed per command. Use `{ ex: seconds }` or `{ px: milliseconds }` on `set()`. Use `{ nx: true }` for distributed locks (returns `"OK"` or `null`). Keys without TTLs cause unbounded storage growth.

```typescript
await redis.set("cache:key", data, { ex: CACHE_TTL_SECONDS });
```

---

### Pattern 4: Hash Operations

Hashes enable partial field reads/writes without serializing entire objects. Use `hset` for multi-field writes, `hget`/`hgetall` for reads, `hincrby` for atomic counters. Note: `hset` does not accept TTL directly -- call `expire()` separately. `hgetall` returns `null` for missing keys (not `{}`).

---

### Pattern 5: Pipelines and Transactions

**Pipelines** (`redis.pipeline()`) batch commands into a single HTTP request but are NOT atomic. **Transactions** (`redis.multi()`) provide atomic MULTI/EXEC, also as a single HTTP request. Avoid sequential calls when multiple commands can be batched -- each call is a separate HTTP round-trip.

```typescript
const pipe = redis.pipeline();
pipe.set("k1", "v1", { ex: TTL });
pipe.incr("counter");
const results = await pipe.exec<[string, number]>();
```

**Important:** Upstash REST transactions do NOT support `WATCH` for optimistic locking.

---

### Pattern 6: Rate Limiting (Sliding Window)

Sliding window via sorted set scores -- `zadd` with timestamp as score, `zremrangebyscore` to prune expired entries, `zcard` to count, all batched in a pipeline. For production rate limiting, consider `@upstash/ratelimit` which provides built-in algorithms.

---

### Pattern 7: Cache-Aside Helper

Generic `cacheAside<T>(key, fetcher, ttl)` pattern: check cache first, fetch on miss, fire-and-forget cache write to avoid blocking responses on cache failures.

</patterns>

---

<decision_framework>

## Decision Framework

### Upstash Redis vs ioredis/node-redis?

```
Which Redis client should I use?
+-- Running in Vercel Edge Runtime? -> @upstash/redis (only option -- no TCP)
+-- Running in Vercel Serverless Functions? -> @upstash/redis (simpler) or ioredis (if you need TCP features)
+-- Need Pub/Sub subscribers? -> ioredis (REST cannot maintain subscriptions)
+-- Need Redis Streams consumers? -> ioredis (requires persistent TCP connection)
+-- Need lowest possible latency (<1ms)? -> ioredis with TCP (REST adds HTTP overhead)
+-- Simple caching/sessions/counters? -> @upstash/redis (zero connection management)
```

### Pipeline vs Transaction vs Sequential?

```
How should I batch commands?
+-- Need atomicity (all-or-nothing)? -> redis.multi() (transaction)
+-- Just reducing HTTP round-trips? -> redis.pipeline() (non-atomic batch)
+-- Single independent command? -> Direct call (redis.set, redis.get, etc.)
```

</decision_framework>

---

<red_flags>

## RED FLAGS

**High Priority Issues:**

- Using `@vercel/kv` in new projects -- deprecated December 2024, use `@upstash/redis` instead
- Missing TTLs on cached keys -- causes unbounded storage growth and unexpected billing
- Manual `JSON.stringify`/`JSON.parse` with Upstash Redis -- causes double-serialization because the SDK auto-serializes all values
- Assuming pipeline commands are atomic -- pipelines batch for HTTP efficiency but do NOT guarantee atomicity (use `multi()` for atomic execution)

**Medium Priority Issues:**

- Making sequential Redis calls where a pipeline would work -- each call is a separate HTTP round-trip (~5-15ms each)
- Storing values >1 MB -- REST requests have size limits per plan (100 MB max on free/pay-as-you-go, but large values degrade performance)
- Using Upstash Redis as a primary database -- it's a cache/ephemeral store, always have a source of truth elsewhere

**Common Mistakes:**

- Expecting `hgetall` to return an empty object `{}` for missing keys -- Upstash returns `null` (unlike ioredis which returns `{}`)
- Forgetting that `get()` returns `null` (not `undefined`) for missing keys
- Passing `Date` objects and expecting them to survive round-trip -- they serialize to ISO strings and come back as strings, not `Date` instances

**Gotchas & Edge Cases:**

- `automaticDeserialization: false` breaks many TypeScript types -- only disable if you need raw string responses and are prepared to handle typing manually
- `set` with `ex` option resets TTL on overwrite (standard Redis behavior) -- if you `set` a key that already has a TTL, the new `ex` value replaces it
- REST latency is per-request, not per-command -- a pipeline with 10 commands has the same HTTP overhead as a single command (one round-trip)
- Free tier is limited to 500K commands/month and 256 MB storage -- monitor usage in production
- `nx` (set-if-not-exists) returns `null` on failure, `"OK"` on success -- check the return value explicitly

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST use `@upstash/redis` for new projects -- `@vercel/kv` was deprecated in December 2024 and all stores were migrated to Upstash Redis)**

**(You MUST set TTLs on all cached data -- serverless Redis is billed per command and has storage limits per plan)**

**(You MUST understand that this is a REST/HTTP client, NOT a TCP Redis client -- each command is an HTTP request with ~5-15ms overhead, so batch with pipelines when possible)**

**Failure to follow these rules will cause deprecated package usage, unbounded storage costs, and unnecessary latency in serverless functions.**

</critical_reminders>
