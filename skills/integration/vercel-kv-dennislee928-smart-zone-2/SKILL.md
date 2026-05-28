---
name: vercel-kv
description: |
  Integrate Redis-compatible Vercel KV for caching, session management, and rate limiting in Next.js. Powered by Upstash with strong consistency and TTL support.

  Use when implementing cache strategies, rate limiters, or troubleshooting environment variables, serialization errors, rate limit issues, scanIterator hangs, or Next.js cache stale reads.
user-invocable: true
---

# Vercel KV

**Last Updated**: 2026-01-21
**Version**: @vercel/kv@3.0.0 (Redis-compatible, powered by Upstash)

---

## Quick Start

```bash
# Create KV: Vercel Dashboard → Storage → KV
vercel env pull .env.local  # Creates KV_REST_API_URL and KV_REST_API_TOKEN
npm install @vercel/kv
```

**Basic Usage**:
```typescript
import { kv } from '@vercel/kv';

// Set with TTL (expires in 1 hour)
await kv.setex('session:abc', 3600, { userId: 123 });

// Get
const session = await kv.get('session:abc');

// Increment counter (atomic)
const views = await kv.incr('views:post:123');
```

**CRITICAL**: Always use namespaced keys (`user:123` not `123`) and set TTL for temporary data.

---

## Common Patterns

**Caching** (cache-aside):
```typescript
const cached = await kv.get(`post:${slug}`);
if (cached) return cached;

const post = await db.query.posts.findFirst({ where: eq(posts.slug, slug) });
await kv.setex(`post:${slug}`, 3600, post); // Cache 1 hour
return post;
```

**Rate Limiting**:
```typescript
async function checkRateLimit(ip: string): Promise<boolean> {
  const key = `ratelimit:${ip}`;
  const current = await kv.incr(key);
  if (current === 1) await kv.expire(key, 60); // 60s window
  return current <= 10; // 10 requests per window
}
```

**Session Management**:
```typescript
const sessionId = crypto.randomUUID();
await kv.setex(`session:${sessionId}`, 7 * 24 * 3600, { userId });
```

**Pipeline** (batch operations):
```typescript
const pipeline = kv.pipeline();
pipeline.set('user:1', data);
pipeline.incr('counter');
const results = await pipeline.exec(); // Single round-trip
```

**Key Naming**: Use namespaces like `user:123`, `post:abc:views`, `ratelimit:ip:endpoint`

---

## Critical Rules

**Always**:
- ✅ Set TTL for temporary data (`setex` not `set`)
- ✅ Use namespaced keys (`user:123` not `123`)
- ✅ Handle null returns (non-existent keys)
- ✅ Use pipeline for batch operations

**Never**:
- ❌ Forget to set TTL (memory leak)
- ❌ Store large values >1MB (use Vercel Blob)
- ❌ Use KV as primary database (it's a cache)
- ❌ Store non-JSON-serializable data (functions, BigInt, circular refs)

---

## Known Issues Prevention

This skill prevents **15 documented issues**:

### Issue #1: Missing Environment Variables
**Error**: `Error: KV_REST_API_URL is not defined` or `KV_REST_API_TOKEN is not defined`
**Source**: https://vercel.com/docs/storage/vercel-kv/quickstart | [GitHub Issue #759](https://github.com/vercel/storage/issues/759)
**Why It Happens**: Environment variables not set locally or in deployment. In monorepos (Turborepo/pnpm workspaces), abstracting `@vercel/kv` into a shared package can cause Vercel builds to fail even though local builds work.
**Prevention**: Run `vercel env pull .env.local` and ensure `.env.local` is in `.gitignore`. For monorepos, either (1) create client in consuming app not shared package, (2) use Vercel Environment Variables UI to set at project level, or (3) add env vars to `turbo.json` pipeline config: `{ "pipeline": { "build": { "env": ["KV_REST_API_URL", "KV_REST_API_TOKEN"] } } }`.

### Issue #2: JSON Serialization Error
**Error**: `TypeError: Do not know how to serialize a BigInt` or circular reference errors. Also, `hset()` coerces numeric strings to numbers.
**Source**: https://github.com/vercel/storage/issues/89 | [GitHub Issue #727](https://github.com/vercel/storage/issues/727)
**Why It Happens**: Trying to store non-JSON-serializable data (functions, BigInt, circular refs). Additionally, when using `hset()` to store string values that look numeric (e.g., `'123456'`), `hgetall()` returns them as numbers, breaking type consistency.
**Prevention**: Only store plain objects, arrays, strings, numbers, booleans, null. Convert BigInt to string. For hash fields with numeric strings, either (1) use non-numeric prefix like `'code_123456'`, (2) store as JSON string and parse after retrieval, or (3) validate and recast types: `String(value.field)` after `hgetall()`.

### Issue #3: Key Naming Collisions
**Error**: Unexpected data returned, data overwritten by different feature
**Source**: Production debugging, best practices
**Why It Happens**: Using generic key names like `cache`, `data`, `temp` across different features
**Prevention**: Always use namespaced keys: `feature:id:type` pattern.

### Issue #4: TTL Not Set
**Error**: Memory usage grows indefinitely, old data never expires
**Source**: Vercel KV best practices
**Why It Happens**: Using `set()` without `setex()` for temporary data
**Prevention**: Use `setex(key, ttl, value)` for all temporary data. Set appropriate TTL (seconds).

### Issue #5: Rate Limit Exceeded (Free Tier)
**Error**: `Error: Rate limit exceeded` or commands failing
**Source**: https://vercel.com/docs/storage/vercel-kv/limits
**Why It Happens**: Exceeding 30,000 commands/month on free tier
**Prevention**: Monitor usage in Vercel dashboard, upgrade plan if needed, use caching to reduce KV calls.

### Issue #6: Storing Large Values
**Error**: `Error: Value too large` or performance degradation
**Source**: https://vercel.com/docs/storage/vercel-kv/limits
**Why It Happens**: Trying to store values >1MB in KV
**Prevention**: Use Vercel Blob for files/images. Keep KV values small (<100KB recommended).

### Issue #7: Type Mismatch on Get
**Error**: TypeScript errors, runtime type errors. Generic `kv.get<T>()` sometimes returns `null` even when data exists.
**Source**: Common TypeScript issue | [GitHub Issue #510](https://github.com/vercel/storage/issues/510)
**Why It Happens**: `kv.get()` returns `unknown` type, need to cast or validate. Additionally, there's a type inference bug where using generics like `kv.get<T>()` can cause the function to return `null` even when CLI shows data exists, due to serialization/deserialization issues.
**Prevention**: Don't use generics with `get()`. Instead, retrieve without type parameter and cast after retrieval: `const rawData = await kv.get('key'); const data = rawData as MyType | null;`. Validate with Zod or type guards before using.

### Issue #8: Pipeline Errors Not Handled
**Error**: Silent failures, partial execution
**Source**: https://github.com/vercel/storage/issues/120
**Why It Happens**: Pipeline execution can have individual command failures
**Prevention**: Check results array from `pipeline.exec()` and handle errors.

### Issue #9: Scan Operation Inefficiency
**Error**: Slow queries, timeout errors. In v3.0.0+, cursor type changed from `number` to `string`.
**Source**: Redis best practices | [Release Notes v3.0.0](https://github.com/vercel/storage/releases/tag/@vercel/kv@3.0.0)
**Why It Happens**: Using `scan()` with large datasets or wrong cursor handling. Version 3.0.0 introduced a breaking change where scan cursor is now `string` instead of `number`.
**Prevention**: Limit `count` parameter, iterate properly with cursor, avoid full scans in production. In v3.0.0+, use `let cursor: string = "0"` and compare with `cursor !== "0"` (not `!== 0`).

### Issue #10: Missing TTL Refresh
**Error**: Session expires too early, cache invalidates prematurely
**Source**: Production debugging
**Why It Happens**: Not refreshing TTL on access (sliding expiration)
**Prevention**: Use `expire(key, newTTL)` on access to implement sliding windows.

### Issue #11: scanIterator() Infinite Loop (v2.0.0+)
**Error**: `for await` loop never terminates when using `kv.scanIterator()`
**Source**: [GitHub Issue #706](https://github.com/vercel/storage/issues/706)
**Why It Happens**: Bug in v2.0.0+ where iterator doesn't properly signal completion. The iterator processes keys correctly but never exits, preventing the function from returning. Also affects `sscanIterator()`.
**Prevention**: Use manual `scan()` with cursor instead of `scanIterator()`.

```typescript
// Don't use scanIterator() - it hangs in v2.0.0+
for await (const key of kv.scanIterator()) {
  // This loop never terminates
}

// Use manual scan with cursor instead
let cursor: string = "0"; // v3.x uses string
do {
  const [newCursor, keys] = await kv.scan(cursor);
  cursor = newCursor;
  for (const key of keys) {
    const value = await kv.get(key);
    // process key/value
  }
} while (cursor !== "0");
```

### Issue #12: zrange() with rev: true Returns Empty Array
**Error**: `kv.zrange(key, 0, -1, { rev: true })` returns empty array even though data exists
**Source**: [GitHub Issue #742](https://github.com/vercel/storage/issues/742)
**Why It Happens**: SDK bug in reverse flag handling for certain key patterns. CLI always returns correct values. Removing the `rev` flag returns data correctly.
**Prevention**: Omit `rev` flag and reverse in-memory, or use `zrevrange()` instead.

```typescript
// This sometimes returns empty array (BUG)
const chats = await kv.zrange(`user:chat:${userId}`, 0, -1, { rev: true });
// [] - but CLI shows 12 items

// Workaround 1: Omit rev flag and reverse in-memory
const chats = await kv.zrange(`user:chat:${userId}`, 0, -1);
const reversedChats = chats.reverse();

// Workaround 2: Use zrevrange instead
const chats = await kv.zrevrange(`user:chat:${userId}`, 0, -1);
```

### Issue #13: Next.js Dev Server Returns Null on First Call
**Error**: `kv.get()` returns `null` on first call after starting dev server, correct data on subsequent calls
**Source**: [GitHub Issue #781](https://github.com/vercel/storage/issues/781)
**Why It Happens**: Next.js static rendering caches the first response. Happens on each compilation restart in Next.js dev server.
**Prevention**: Force dynamic rendering with `unstable_noStore()`, use `cache: 'no-store'` in fetch calls, or add retry logic.

```typescript
import { unstable_noStore as noStore } from 'next/cache';

export async function getData() {
  noStore(); // Force dynamic rendering
  const data = await kv.get('mykey');
  return data; // Now returns correct value on first call
}

// Or add retry logic
async function getWithRetry(key: string, retries = 2) {
  let data = await kv.get(key);
  let attempt = 0;
  while (!data && attempt < retries) {
    await new Promise(r => setTimeout(r, 100));
    data = await kv.get(key);
    attempt++;
  }
  return data;
}
```

### Issue #14: Vite "process is not defined" Error
**Error**: `Uncaught ReferenceError: process is not defined` when importing `@vercel/kv` in Vite
**Source**: [GitHub Issue #743](https://github.com/vercel/storage/issues/743)
**Why It Happens**: Vite doesn't polyfill Node.js `process.env` by default. `@vercel/kv` expects `process.env` to exist.
**Prevention**: Use Vite's `define` to polyfill, use `createClient` with `import.meta.env`, or install `vite-plugin-node-polyfills`.

```typescript
// Option 1: Vite config with define
// vite.config.ts
import { defineConfig, loadEnv } from 'vite';

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '');
  return {
    define: {
      'process.env.KV_REST_API_URL': JSON.stringify(env.KV_REST_API_URL),
      'process.env.KV_REST_API_TOKEN': JSON.stringify(env.KV_REST_API_TOKEN),
    },
  };
});

// Option 2: Use createClient with import.meta.env
import { createClient } from '@vercel/kv';

const kv = createClient({
  url: import.meta.env.VITE_KV_REST_API_URL,
  token: import.meta.env.VITE_KV_REST_API_TOKEN,
});
```

### Issue #15: Next.js Server Actions Return Stale Data
**Error**: `kv.get()` in Server Actions returns stale/cached data even after KV values are updated
**Source**: [GitHub Issue #510](https://github.com/vercel/storage/issues/510)
**Why It Happens**: Next.js static rendering caches Server Action responses. Console output appears yellow (cache hit indicator).
**Prevention**: Use `unstable_noStore()` to force dynamic rendering, or use route handlers instead of Server Actions.

```typescript
// In Server Actions
'use server'
import { unstable_noStore as noStore } from 'next/cache';

export async function logChat(text: string) {
  noStore(); // Force dynamic rendering
  let n_usage = await kv.get('n_usage');
  // Now returns fresh value, not cached
}

// Or use route handlers (automatically dynamic)
// app/api/chat/route.ts
export async function GET() {
  let n_usage = await kv.get('n_usage'); // Fresh data
  return Response.json({ n_usage });
}
```

---

## Version Migration Guide

### v3.0.0 Breaking Changes

**Cursor Type Changed** ([Release Notes](https://github.com/vercel/storage/releases/tag/@vercel/kv@3.0.0)):
- Scan cursor now returns `string` instead of `number`
- Update comparisons from `cursor !== 0` to `cursor !== "0"`

```typescript
// v2.x
let cursor: number = 0;
do {
  const [newCursor, keys] = await kv.scan(cursor);
  cursor = newCursor;
} while (cursor !== 0);

// v3.x
let cursor: string = "0";
do {
  const [newCursor, keys] = await kv.scan(cursor);
  cursor = newCursor;
} while (cursor !== "0");
```

### v2.0.0 Breaking Changes

**Auto-Pipelining Enabled by Default** ([Release Notes](https://github.com/vercel/storage/releases/tag/@vercel/kv@2.0.0)):
- Commands now automatically batched for performance
- May cause timing issues in edge cases
- Disable with `enableAutoPipelining: false` if needed

```typescript
// If auto-pipelining causes issues, disable it:
import { createClient } from '@vercel/kv';

const kv = createClient({
  url: process.env.KV_REST_API_URL,
  token: process.env.KV_REST_API_TOKEN,
  enableAutoPipelining: false // Disable auto-pipelining
});
```

**scanIterator() Bug Introduced**: v2.0.0+ has infinite loop bug with `scanIterator()`. See Issue #11 for workaround.

---

## Known Limitations

### Redis Streams Not Supported

**Source**: [Vercel KV Redis Compatibility](https://vercel.com/docs/storage/vercel-kv/redis-compatibility) | [GitHub Issue #278](https://github.com/vercel/storage/issues/278)

`@vercel/kv` does not support Redis Streams (XREAD, XADD, XGROUP, etc.) even though underlying Upstash Redis supports them. The package lacks stream methods.

**Workaround**: Use `@upstash/redis` directly for streams:

```typescript
// @vercel/kv doesn't have stream methods
// await kv.xAdd(...) // TypeError: kv.xAdd is not a function

// Use Upstash Redis client directly
import { Redis } from '@upstash/redis';

const redis = new Redis({
  url: process.env.KV_REST_API_URL!,
  token: process.env.KV_REST_API_TOKEN!,
});

await redis.xadd('stream:events', '*', { event: 'user.login' });
const messages = await redis.xread('stream:events', '0');
```

### Hash Operations Return Objects Not Strings

**Source**: [GitHub Issue #674](https://github.com/vercel/storage/issues/674)

`kv.hgetall()` returns a JavaScript object, not a JSON string. This confuses developers expecting string serialization.

```typescript
await kv.hset('foobar', { '1834': 'https://example.com' });

const data = await kv.hgetall('foobar');
console.log(typeof data); // "object" not "string"

// It's already an object - use directly
console.log(data['1834']); // 'https://example.com'

// If you need JSON string
const jsonString = JSON.stringify(data);
```

---

## Advanced Patterns

**Distributed Lock** (prevents race conditions):
```typescript
const lockKey = `lock:${resource}`;
const lockValue = crypto.randomUUID();

const acquired = await kv.setnx(lockKey, lockValue);
if (acquired) {
  await kv.expire(lockKey, 10); // TTL prevents deadlock
  try {
    await processOrders();
  } finally {
    const current = await kv.get(lockKey);
    if (current === lockValue) await kv.del(lockKey);
  }
}
```

**Leaderboard** (sorted sets):
```typescript
await kv.zadd('leaderboard', { score, member: userId.toString() });

// Note: zrange with { rev: true } has a known bug (Issue #12)
// Use zrevrange instead for reliability
const top = await kv.zrevrange('leaderboard', 0, 9, { withScores: true });
const rank = await kv.zrevrank('leaderboard', userId.toString());
```

---

**Last verified**: 2026-01-21 | **Skill version**: 2.0.0 | **Changes**: Added 5 new issues (scanIterator hang, zrange rev bug, Next.js dev server null, Vite process error, Server Actions stale cache), expanded Issues #1, #2, #7, #9 with TIER 1-2 research findings, added Version Migration Guide and Known Limitations sections
