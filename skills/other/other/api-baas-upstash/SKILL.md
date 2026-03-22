---
name: api-baas-upstash
description: Upstash serverless Redis -- REST-based client, auto-serialization, pipelines, rate limiting, QStash, edge compatibility, global replication
---

# Upstash Patterns

> **Quick Guide:** Upstash provides a **REST/HTTP-based Redis client** (`@upstash/redis`) designed for serverless and edge runtimes where TCP connections are unavailable. Unlike ioredis/node-redis, every command is an HTTP request -- no persistent connections, no connection pools, no teardown. The client **automatically serializes/deserializes JSON** (objects stored via `set` come back as objects from `get`), which is convenient but has gotchas with large numbers and cross-client compatibility. Use `redis.pipeline()` to batch commands into a single HTTP request, `redis.multi()` for atomic transactions, and `@upstash/ratelimit` for pre-built rate limiting algorithms. For background jobs, use `@upstash/qstash` which pushes messages to your API via HTTP webhooks.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST use `Redis.fromEnv()` for initialization in production code -- never hardcode `UPSTASH_REDIS_REST_URL` or `UPSTASH_REDIS_REST_TOKEN` values)**

**(You MUST handle the `pending` promise from `@upstash/ratelimit` responses in edge runtimes -- use `context.waitUntil(pending)` on Vercel Edge/Cloudflare Workers or analytics data is lost)**

**(You MUST use `redis.pipeline()` when issuing 3+ independent commands in a single handler -- each command is a separate HTTP round-trip without pipelining)**

**(You MUST NOT use Upstash for Pub/Sub, blocking commands (BRPOP, BLPOP, XREAD BLOCK), or Lua scripting -- REST API does not support these; use ioredis with a TCP connection instead)**

</critical_requirements>

---

## Examples

- [Core Patterns](examples/core.md) -- Client setup, commands, auto-serialization, pipeline, transactions
- [Rate Limiting](examples/rate-limiting.md) -- @upstash/ratelimit algorithms, middleware, analytics
- [QStash](examples/qstash.md) -- Background jobs, scheduling, message publishing

**Additional resources:**

- [reference.md](reference.md) -- Command cheat sheet, constructor options, environment variables, eviction policies

---

**Auto-detection:** Upstash, @upstash/redis, @upstash/ratelimit, @upstash/qstash, Redis.fromEnv, UPSTASH_REDIS_REST_URL, UPSTASH_REDIS_REST_TOKEN, Ratelimit.slidingWindow, Ratelimit.fixedWindow, Ratelimit.tokenBucket, serverless Redis, edge Redis, REST Redis

**When to use:**

- Serverless functions (AWS Lambda, Vercel, Netlify) that cannot maintain TCP connections
- Edge runtimes (Cloudflare Workers, Vercel Edge, Fastly Compute) that only support HTTP
- Rate limiting API routes with pre-built algorithms (sliding window, fixed window, token bucket)
- Caching in serverless/edge where ioredis connection pooling is impractical
- Background job scheduling with QStash (push-based, no long-running consumers needed)
- Global read latency optimization via Upstash Global Database with read replicas

**Key patterns covered:**

- `@upstash/redis` client setup with `Redis.fromEnv()` and constructor options
- Automatic JSON serialization/deserialization behavior and gotchas
- Pipeline batching (`redis.pipeline()`) and atomic transactions (`redis.multi()`)
- `@upstash/ratelimit` algorithms: sliding window, fixed window, token bucket
- `@upstash/qstash` for serverless background jobs and scheduling
- Global Database architecture (primary + read regions, eventual consistency)
- Edge runtime compatibility and `context.waitUntil()` patterns

**When NOT to use:**

- Long-running servers with persistent connections (use ioredis -- lower latency per command via TCP)
- Pub/Sub, blocking commands, or Lua scripting (REST API does not support these)
- Write-heavy workloads on Global Database (writes always go to primary region)
- Latency-critical paths where per-command HTTP overhead (~5-15ms) is unacceptable (use ioredis with TCP for <1ms per command)
- Large payloads (>1 MB) -- REST API has payload size limits

---

<philosophy>

## Philosophy

Upstash exists because **serverless and edge runtimes cannot maintain TCP connections**. Traditional Redis clients (ioredis, node-redis) rely on persistent TCP sockets -- they fail in Cloudflare Workers, break in short-lived Lambda functions, and cannot run in browser/WebAssembly environments. Upstash replaces TCP with REST/HTTP, trading per-command latency (~5-15ms vs <1ms) for universal compatibility.

**Core principles:**

1. **Connectionless by design** -- Every command is a stateless HTTP request. No connection pools, no teardown, no connection limits. This is a feature, not a limitation.
2. **Auto-serialization is default** -- Objects go in, objects come out. No manual `JSON.stringify`/`JSON.parse`. This simplifies 90% of use cases but surprises developers who expect raw string behavior.
3. **Pipeline for performance** -- Without pipelining, N commands = N HTTP requests. Always batch independent commands with `redis.pipeline()` to reduce round-trips.
4. **Rate limiting as a first-class citizen** -- `@upstash/ratelimit` provides production-ready algorithms without writing Lua scripts. The library handles all the Redis plumbing internally.
5. **Push-based messaging** -- QStash delivers messages TO your API via HTTP webhooks. No long-running consumer processes needed -- perfect for serverless.

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Client Setup with Redis.fromEnv()

Initialize using environment variables for zero-config deployment. See [examples/core.md](examples/core.md) for full examples including constructor options and timeout configuration.

```typescript
// Good Example
import { Redis } from "@upstash/redis";

const redis = Redis.fromEnv();
// Reads UPSTASH_REDIS_REST_URL and UPSTASH_REDIS_REST_TOKEN automatically

export { redis };
```

**Why good:** Zero-config, environment variables injected by platform (Vercel, Fly.io), no secrets in code

```typescript
// Bad Example
import { Redis } from "@upstash/redis";

const redis = new Redis({
  url: "https://us1-merry-cat-12345.upstash.io",
  token: "AXXXAAIgcDE...",
});
```

**Why bad:** Hardcoded credentials leak in version control, non-portable across environments

---

### Pattern 2: Automatic JSON Serialization

Upstash auto-serializes objects with `JSON.stringify` on write and `JSON.parse` on read. See [examples/core.md](examples/core.md) for type-safe patterns and disabling auto-serialization.

```typescript
// Good Example -- objects round-trip automatically
interface UserProfile {
  name: string;
  email: string;
  loginCount: number;
}

const CACHE_TTL_SECONDS = 3600;

await redis.set<UserProfile>(
  "user:123",
  {
    name: "Alice",
    email: "alice@example.com",
    loginCount: 42,
  },
  { ex: CACHE_TTL_SECONDS },
);

// Returns typed object -- no JSON.parse needed
const user = await redis.get<UserProfile>("user:123");
// user is UserProfile | null
```

**Why good:** TypeScript generics provide type safety, no manual serialization, TTL set via options object

```typescript
// Bad Example -- unnecessary manual serialization
await redis.set("user:123", JSON.stringify({ name: "Alice" }));
const raw = await redis.get("user:123");
const user = JSON.parse(raw as string); // Double-serialized: "{\"name\":\"Alice\"}"
```

**Why bad:** Auto-serialization already calls `JSON.stringify` -- doing it manually results in double-encoded strings that return as escaped JSON

---

### Pattern 3: Pipeline Batching

Batch multiple commands into a single HTTP request. Without pipelining, each command is a separate round-trip (~5-15ms each). See [examples/core.md](examples/core.md) for typed pipeline results.

```typescript
// Good Example -- single HTTP request for all commands
const USER_TTL_SECONDS = 3600;

const pipe = redis.pipeline();
pipe.set("user:123:name", "Alice", { ex: USER_TTL_SECONDS });
pipe.set("user:123:email", "alice@example.com", { ex: USER_TTL_SECONDS });
pipe.incr("stats:signups");

const results = await pipe.exec<["OK", "OK", number]>();
// results[0] => "OK"
// results[1] => "OK"
// results[2] => 1 (incremented value)
```

**Why good:** Single HTTP round-trip for 3 commands, typed results with generics, named TTL constant

```typescript
// Bad Example -- 3 separate HTTP requests
await redis.set("user:123:name", "Alice");
await redis.set("user:123:email", "alice@example.com");
await redis.incr("stats:signups");
// 3 round-trips = ~15-45ms total vs ~5-15ms with pipeline
```

**Why bad:** Each `await` is a separate HTTP request, tripling latency in serverless where every millisecond of cold start matters

---

### Pattern 4: Atomic Transactions

Use `redis.multi()` when commands must execute atomically. See [examples/core.md](examples/core.md) for examples.

```typescript
// Good Example -- atomic counter + flag update
const tx = redis.multi();
tx.incr("order:count");
tx.set("order:last-updated", Date.now());
const [count, status] = await tx.exec<[number, "OK"]>();
```

**Why good:** All commands execute atomically (no interleaving from other clients), typed results

**When to use pipeline vs transaction:**

- **Pipeline** (`redis.pipeline()`) -- Commands are independent, you want batching for speed, atomicity not required
- **Transaction** (`redis.multi()`) -- Commands must all succeed together, no interleaving allowed

---

### Pattern 5: Rate Limiting with @upstash/ratelimit

Pre-built rate limiting that handles all Redis internals. See [examples/rate-limiting.md](examples/rate-limiting.md) for all algorithms, middleware integration, and analytics.

```typescript
// Good Example
import { Ratelimit } from "@upstash/ratelimit";
import { Redis } from "@upstash/redis";

const MAX_REQUESTS = 10;
const WINDOW_DURATION = "10 s";

const ratelimit = new Ratelimit({
  redis: Redis.fromEnv(),
  limiter: Ratelimit.slidingWindow(MAX_REQUESTS, WINDOW_DURATION),
  analytics: true,
});

const { success, limit, remaining, reset, pending } =
  await ratelimit.limit("user:123");

// CRITICAL: In edge runtimes, handle the pending promise
// context.waitUntil(pending);

if (!success) {
  return new Response("Too Many Requests", {
    status: 429,
    headers: {
      "X-RateLimit-Limit": String(limit),
      "X-RateLimit-Remaining": String(remaining),
      "X-RateLimit-Reset": String(reset),
    },
  });
}
```

**Why good:** No Lua scripts needed, named constants for limits, analytics for monitoring, proper 429 response with standard headers

---

### Pattern 6: QStash Background Jobs

Push-based messaging for serverless. See [examples/qstash.md](examples/qstash.md) for scheduling, retries, and receiver verification.

```typescript
// Good Example -- publish a background job
import { Client } from "@upstash/qstash";

const qstash = new Client({
  token: process.env.QSTASH_TOKEN!,
});

await qstash.publishJSON({
  url: "https://your-app.com/api/process-order",
  body: { orderId: "order-456", action: "fulfill" },
  retries: 3,
  delay: "10s",
});
```

**Why good:** Fire-and-forget from handler, automatic retries on failure, configurable delay, at-least-once delivery guaranteed

</patterns>

---

<decision_framework>

## Decision Framework

### Upstash vs ioredis/node-redis

```
Which Redis client should I use?
|-- Running in edge runtime (Cloudflare Workers, Vercel Edge)?
|   --> @upstash/redis (only option -- no TCP available)
|-- Running in serverless (Lambda, Vercel Serverless)?
|   |-- Short-lived functions with no connection reuse?
|   |   --> @upstash/redis (no connection management overhead)
|   |-- Long-lived functions with connection pooling?
|       --> ioredis (lower per-command latency)
|-- Running on a persistent server (Docker, EC2, K8s)?
|   --> ioredis (persistent TCP = <1ms latency vs ~5-15ms HTTP)
|-- Need Pub/Sub, blocking commands, or Lua scripts?
|   --> ioredis (REST API cannot support these)
|-- Need to run in browser or WebAssembly?
    --> @upstash/redis (HTTP works everywhere)
```

### Which Rate Limiting Algorithm?

```
Which @upstash/ratelimit algorithm should I use?
|-- Need strict, evenly distributed limiting?
|   --> slidingWindow -- smoothest, no burst-at-boundary issues
|-- Need simple, low-overhead limiting?
|   --> fixedWindow -- cheapest computationally, allows boundary bursts
|-- Need to allow burst traffic up to a capacity?
|   --> tokenBucket -- smooths bursts, allows initial spike up to maxTokens
|-- Need multi-region rate limiting?
    --> fixedWindow (slidingWindow has high Redis command overhead in multi-region)
```

### Pipeline vs Transaction vs Sequential

```
How should I batch these Redis commands?
|-- Commands are independent (no ordering dependency)?
|   --> Pipeline (redis.pipeline()) -- non-atomic but single HTTP request
|-- Commands must execute atomically (all-or-nothing)?
|   --> Transaction (redis.multi()) -- atomic, single HTTP request
|-- Only 1-2 commands?
    --> Sequential is fine -- pipeline overhead not worth it
```

### Global Database vs Regional

```
Should I use Upstash Global Database?
|-- Read-heavy workload with users worldwide?
|   --> Global Database -- reads from nearest replica
|-- Write-heavy workload?
|   --> Regional Database -- writes always go to primary, replication doubles write cost
|-- Need strong consistency?
|   --> Regional Database -- Global is eventually consistent
|-- Latency-sensitive reads from multiple continents?
    --> Global Database -- sub-1ms reads from nearest region
```

</decision_framework>

---

<red_flags>

## RED FLAGS

**High Priority Issues:**

- Using `JSON.stringify()` before passing objects to `redis.set()` -- auto-serialization already handles this, resulting in double-encoded strings like `"{\"name\":\"Alice\"}"` that break on read
- Ignoring the `pending` promise from `ratelimit.limit()` in edge runtimes -- analytics data and multi-region sync are lost silently; use `context.waitUntil(pending)`
- Issuing 5+ sequential `await redis.get/set()` calls without pipelining -- each is a separate HTTP request, adding 25-75ms of unnecessary latency
- Attempting Pub/Sub (`redis.subscribe`), blocking commands (`BRPOP`, `BLPOP`), or Lua scripting (`eval`) -- Upstash REST API does not support these; use ioredis with TCP

**Medium Priority Issues:**

- Missing TTL on cached keys -- same as any Redis: unbounded memory growth until eviction kicks in
- Using Global Database for write-heavy workloads -- writes always route to primary region and replication doubles command costs
- Not setting `automaticDeserialization: false` when interoperating with non-Upstash clients -- other clients store raw strings, Upstash will fail to parse them as JSON
- Creating a new `Redis` instance per request instead of reusing a module-level singleton -- while connectionless, the client still benefits from HTTP keep-alive and warm connections

**Common Mistakes:**

- Expecting `redis.get()` to return a string when an object was stored -- auto-deserialization returns the original object type, not a JSON string
- Assuming pipeline execution is atomic -- pipelines batch for network efficiency but other clients can interleave; use `redis.multi()` for atomicity
- Using `Ratelimit.slidingWindow` with `MultiRegionRatelimit` -- sliding window has high Redis command overhead in multi-region setups; use `fixedWindow` instead
- Storing values larger than 1 MB -- REST API has payload size limits; store references and fetch large data from object storage

**Gotchas & Edge Cases:**

- **Large numbers become strings**: JavaScript cannot safely handle numbers > `2^53 - 1` (Number.MAX_SAFE_INTEGER). Upstash returns these as strings even when the TypeScript type says `number`. Always validate large numeric values.
- **Base64 encoding by default**: The SDK requests base64-encoded responses to handle edge cases. If you see garbled output like `dmFsdWU=`, the response encoding is interfering -- check `responseEncoding` option.
- **`redis.get()` returns `null` for missing keys, not `undefined`**: This matters for TypeScript narrowing -- check `result !== null`, not truthiness.
- **SET options use an object, not positional args**: Upstash uses `redis.set("key", "value", { ex: 300 })` not `redis.set("key", "value", "EX", 300)` -- the ioredis positional argument style does not work.
- **Global Database is eventually consistent**: A write followed immediately by a read from a different region may return stale data. Design for eventual consistency or use regional database for strong consistency.
- **`hgetall` returns an empty object `{}` for non-existent keys**: Check `Object.keys(result).length === 0`, not `result === null`.
- **`blockUntilReady()` does not work on Cloudflare Workers**: Cloudflare's `Date.now()` behaves differently; use `limit()` with manual retry logic instead.
- **No WATCH command**: Upstash REST API does not support `WATCH` for optimistic locking. Use `redis.multi()` for atomic operations or implement application-level optimistic concurrency.
- **Auto-pipelining is available**: The SDK can automatically batch commands issued during the same event loop tick via `enableAutoPipelining: true` in the constructor.

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST use `Redis.fromEnv()` for initialization in production code -- never hardcode `UPSTASH_REDIS_REST_URL` or `UPSTASH_REDIS_REST_TOKEN` values)**

**(You MUST handle the `pending` promise from `@upstash/ratelimit` responses in edge runtimes -- use `context.waitUntil(pending)` on Vercel Edge/Cloudflare Workers or analytics data is lost)**

**(You MUST use `redis.pipeline()` when issuing 3+ independent commands in a single handler -- each command is a separate HTTP round-trip without pipelining)**

**(You MUST NOT use Upstash for Pub/Sub, blocking commands (BRPOP, BLPOP, XREAD BLOCK), or Lua scripting -- REST API does not support these; use ioredis with a TCP connection instead)**

**Failure to follow these rules will cause credential leaks, silent data loss in edge runtimes, unnecessary latency from sequential HTTP requests, and runtime errors from unsupported commands.**

</critical_reminders>
