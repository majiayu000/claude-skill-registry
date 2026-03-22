---
name: cloudflare-kv
description: |
  Store key-value data globally with Cloudflare KV's edge network. Use when: caching API responses, storing configuration, managing user preferences, handling TTL expiration, or troubleshooting KV_ERROR, 429 rate limits, eventual consistency, cacheTtl errors, wrangler types issues, or remote binding configuration.
user-invocable: true
---

# Cloudflare Workers KV

**Status**: Production Ready ✅
**Last Updated**: 2026-01-20
**Dependencies**: cloudflare-worker-base (for Worker setup)
**Latest Versions**: wrangler@4.59.2, @cloudflare/workers-types@4.20260109.0

**Recent Updates (2025)**:
- **August 2025**: Architecture redesign (40x performance gain, <5ms p99 latency, hybrid storage with R2)
- **April 2025**: Bulk reads API (retrieve up to 100 keys in single request, counts as 1 operation)
- **January 2025**: Namespace limit increased (200 → 1,000 namespaces per account for Free and Paid plans)

---

## Quick Start (5 Minutes)

```bash
# Create namespace
npx wrangler kv namespace create MY_NAMESPACE
# Output: [[kv_namespaces]] binding = "MY_NAMESPACE" id = "<UUID>"
```

**wrangler.jsonc:**
```jsonc
{
  "kv_namespaces": [{
    "binding": "MY_NAMESPACE",  // Access as env.MY_NAMESPACE
    "id": "<production-uuid>",
    "preview_id": "<preview-uuid>"  // Optional: local dev
  }]
}
```

**Basic Usage:**
```typescript
type Bindings = { MY_NAMESPACE: KVNamespace };

app.post('/set/:key', async (c) => {
  await c.env.MY_NAMESPACE.put(c.req.param('key'), await c.req.text());
  return c.json({ success: true });
});

app.get('/get/:key', async (c) => {
  const value = await c.env.MY_NAMESPACE.get(c.req.param('key'));
  return value ? c.json({ value }) : c.json({ error: 'Not found' }, 404);
});
```

---

## KV API Reference

### Read Operations

```typescript
// Get single key
const value = await env.MY_KV.get('key');  // string | null
const data = await env.MY_KV.get('key', { type: 'json' });  // object | null
const buffer = await env.MY_KV.get('key', { type: 'arrayBuffer' });
const stream = await env.MY_KV.get('key', { type: 'stream' });

// Get with cache (minimum 60s)
const value = await env.MY_KV.get('key', { cacheTtl: 300 });  // 5 min edge cache

// Bulk read (counts as 1 operation)
const values = await env.MY_KV.get(['key1', 'key2']);  // Map<string, string | null>

// With metadata
const { value, metadata } = await env.MY_KV.getWithMetadata('key');
const result = await env.MY_KV.getWithMetadata(['key1', 'key2']);  // Bulk with metadata
```

### Write Operations

```typescript
// Basic write (max 1/second per key)
await env.MY_KV.put('key', 'value');
await env.MY_KV.put('user:123', JSON.stringify({ name: 'John' }));

// With expiration
await env.MY_KV.put('session', data, { expirationTtl: 3600 });  // 1 hour
await env.MY_KV.put('token', value, { expiration: Math.floor(Date.now()/1000) + 86400 });

// With metadata (max 1024 bytes)
await env.MY_KV.put('config', 'dark', {
  metadata: { updatedAt: Date.now(), version: 2 }
});
```

**Critical Limits:**
- Key: 512 bytes max
- Value: 25 MiB max
- Metadata: 1024 bytes max
- Write rate: 1/second per key (429 error if exceeded)
- Expiration: 60 seconds minimum

### List Operations

```typescript
// List with pagination
const result = await env.MY_KV.list({ prefix: 'user:', limit: 1000, cursor });
// result: { keys: [], list_complete: boolean, cursor?: string }

// CRITICAL: Always check list_complete, not keys.length === 0
let cursor: string | undefined;
do {
  const result = await env.MY_KV.list({ prefix: 'user:', cursor });
  processKeys(result.keys);
  cursor = result.list_complete ? undefined : result.cursor;
} while (cursor);
```

### Delete Operations

```typescript
// Delete single key
await env.MY_KV.delete('key');  // Always succeeds

// Bulk delete (CLI only, up to 10,000 keys)
// npx wrangler kv bulk delete --binding=MY_KV keys.json
```

---

## Advanced Patterns

### Caching Pattern with CacheTtl

```typescript
async function getCachedData(kv: KVNamespace, key: string, fetchFn: () => Promise<any>, ttl = 300) {
  const cached = await kv.get(key, { type: 'json', cacheTtl: ttl });
  if (cached) return cached;

  const data = await fetchFn();
  await kv.put(key, JSON.stringify(data), { expirationTtl: ttl * 2 });
  return data;
}
```

**Guidelines**: Minimum 60s, use for read-heavy workloads (100:1 read/write ratio)

### Metadata Optimization

```typescript
// Store small values (<1024 bytes) in metadata to avoid separate get() calls
await env.MY_KV.put('user:123', '', {
  metadata: { status: 'active', plan: 'pro', lastSeen: Date.now() }
});

// list() returns metadata automatically (no additional get() calls)
const users = await env.MY_KV.list({ prefix: 'user:' });
users.keys.forEach(({ name, metadata }) => console.log(name, metadata.status));
```

### Understanding Hot vs Cold Keys

KV performance varies based on key temperature:

| Type | Response Time | When It Happens |
|------|---------------|-----------------|
| **Hot keys** | 6-8ms | Read 2+ times/minute per datacenter |
| **Cold keys** | 100-300ms | Infrequently accessed, fetched from central storage |

**Post-August 2025 Improvements**:
- P90 for all KV Worker invocations: <12ms (was 22ms before)
- Hot reads up to 3x faster
- All operations faster by up to 20ms

**Optimization**: Use key coalescing to make cold keys benefit from hot key caching:

```typescript
// ❌ Bad: Many cold keys (300ms each)
await kv.put('user:123:name', 'John');
await kv.put('user:123:email', 'john@example.com');
await kv.put('user:123:plan', 'pro');

// Each read of a cold key: ~100-300ms
const name = await kv.get('user:123:name');    // Cold
const email = await kv.get('user:123:email');  // Cold
const plan = await kv.get('user:123:plan');    // Cold

// ✅ Good: Single hot key (6-8ms)
await kv.put('user:123', JSON.stringify({
  name: 'John',
  email: 'john@example.com',
  plan: 'pro'
}));

// Single read, cached as hot key: ~6-8ms
const user = JSON.parse(await kv.get('user:123'));
```

**CacheTtl helps cold keys**: For infrequently-read data, `cacheTtl` reduces cold read latency.

**Trade-off**: Coalescing requires read-modify-write for updates

### Pagination Helper

```typescript
async function* paginateKV(kv: KVNamespace, options: { prefix?: string } = {}) {
  let cursor: string | undefined;
  do {
    const result = await kv.list({ ...options, cursor });
    yield result.keys;
    cursor = result.list_complete ? undefined : result.cursor;
  } while (cursor);
}

// Usage
for await (const keys of paginateKV(env.MY_KV, { prefix: 'user:' })) {
  processKeys(keys);
}
```

### Rate Limit Retry with Exponential Backoff

```typescript
async function putWithRetry(kv: KVNamespace, key: string, value: string, opts?: KVPutOptions) {
  let attempts = 0, delay = 1000;
  while (attempts < 5) {
    try {
      await kv.put(key, value, opts);
      return;
    } catch (error) {
      if ((error as Error).message.includes('429')) {
        attempts++;
        if (attempts >= 5) throw new Error('Max retry attempts');
        await new Promise(r => setTimeout(r, delay));
        delay *= 2;  // Exponential backoff
      } else throw error;
    }
  }
}
```

---

## Understanding Eventual Consistency

KV is **eventually consistent** across Cloudflare's global network (Aug 2025 redesign: hybrid storage, <5ms p99 latency):

**How It Works:**
1. Writes immediately visible in same location (read-your-own-write consistency within same POP)
2. Other locations see update within ~60 seconds (or cacheTtl value)
3. Cached reads may return stale data during propagation

**Example:**
```typescript
// Tokyo: Write
await env.MY_KV.put('counter', '1');
const value = await env.MY_KV.get('counter'); // "1" ✅ (same POP, RYOW)

// London (within 60s): May be stale ⚠️
const value2 = await env.MY_KV.get('counter'); // Might be old value

// After 60+ seconds: Consistent ✅
```

**Read-Your-Own-Write (RYOW) Guarantee**: Since August 2025 redesign, requests routed through the **same Cloudflare point of presence** see their own writes immediately. Global consistency across different POPs still takes up to 60 seconds.

**Timestamp Mitigation Pattern** (for critical consistency needs):
```typescript
// Use timestamp in key structure to avoid consistency issues
const timestamp = Date.now();
await kv.put(`user:123:${timestamp}`, userData);

// Find latest using list with prefix
const result = await kv.list({ prefix: 'user:123:' });
const latestKey = result.keys.sort((a, b) =>
  parseInt(b.name.split(':')[2]) - parseInt(a.name.split(':')[2])
).at(0);
```

**Use KV for**: Read-heavy workloads (100:1 ratio), config, feature flags, caching, user preferences
**Don't use KV for**: Financial transactions, strong consistency, >1/second writes per key, critical data

**Need strong consistency?** Use [Durable Objects](https://developers.cloudflare.com/durable-objects/)

**Source**: [Redesigning Workers KV](https://blog.cloudflare.com/rearchitecting-workers-kv-for-redundancy/)

---

## Wrangler CLI Essentials

```bash
# Create namespace
npx wrangler kv namespace create MY_NAMESPACE [--preview]

# Manage keys (add --remote flag to access production data)
npx wrangler kv key put --binding=MY_KV "key" "value" [--ttl=3600] [--metadata='{}']
npx wrangler kv key get --binding=MY_KV "key" [--remote]
npx wrangler kv key list --binding=MY_KV [--prefix="user:"] [--remote]
npx wrangler kv key delete --binding=MY_KV "key"

# Bulk operations (up to 10,000 keys)
npx wrangler kv bulk put --binding=MY_KV data.json
npx wrangler kv bulk delete --binding=MY_KV keys.json
```

**IMPORTANT**: CLI commands default to **local storage**. Add `--remote` flag to access production/remote data.

---

## Development vs Production

### Remote Bindings for Local Development (Wrangler 4.37+)

Connect local Workers to production KV namespaces during development:

**wrangler.jsonc:**
```jsonc
{
  "kv_namespaces": [{
    "binding": "MY_KV",
    "id": "production-uuid",
    "remote": true  // Connect to live KV
  }]
}
```

**How It Works:**
- Local Worker code executes locally (fast iteration)
- KV operations route to production namespace through proxy
- No manual data seeding required

**Benefits:**
- Test against real production data without deploying
- Fast local code execution with production data access
- Faster feedback loop (no deploy-test cycle)

**⚠️ Warning**: Writes affect production data. Consider using a staging namespace with `remote: true` instead of production.

**Version Support:**
- Wrangler 4.37.0+
- @cloudflare/vite-plugin 1.13.0+
- @cloudflare/vitest-pool-workers 0.9.0+

**Source**: [Remote bindings architecture](https://blog.cloudflare.com/connecting-to-production-the-architecture-of-remote-bindings/)

---

## Limits & Quotas

| Feature | Free Plan | Paid Plan |
|---------|-----------|-----------|
| Reads per day | 100,000 | Unlimited |
| Writes per day (different keys) | 1,000 | Unlimited |
| **Writes per key per second** | **1** | **1** |
| Operations per Worker invocation | 1,000 | 1,000 |
| **Namespaces per account** | **1,000** | **1,000** |
| Storage per account | 1 GB | Unlimited |
| Key size | 512 bytes | 512 bytes |
| Metadata size | 1024 bytes | 1024 bytes |
| Value size | 25 MiB | 25 MiB |
| Minimum cacheTtl | 60 seconds | 60 seconds |

**Critical**: 1 write/second per key (429 if exceeded), bulk operations count as 1 operation, namespace limit increased from 200 → 1,000 (Jan 2025)

---


## Error Handling

### 1. Rate Limit (429 Too Many Requests)
**Cause**: Writing to same key >1/second
**Solution**: Use retry with exponential backoff (see Advanced Patterns)

```typescript
// ❌ Bad
await env.MY_KV.put('counter', '1');
await env.MY_KV.put('counter', '2'); // 429 error!

// ✅ Good
await putWithRetry(env.MY_KV, 'counter', '2');
```

### 2. Value Too Large
**Cause**: Value exceeds 25 MiB
**Solution**: Validate size before writing

```typescript
if (value.length > 25 * 1024 * 1024) throw new Error('Value exceeds 25 MiB');
```

### 3. Metadata Too Large
**Cause**: Metadata exceeds 1024 bytes when serialized
**Solution**: Validate serialized size

```typescript
const serialized = JSON.stringify(metadata);
if (serialized.length > 1024) throw new Error('Metadata exceeds 1024 bytes');
```

### 4. Invalid CacheTtl
**Cause**: cacheTtl <60 seconds
**Solution**: Use minimum 60

```typescript
// ❌ Error
await env.MY_KV.get('key', { cacheTtl: 30 });

// ✅ Correct
await env.MY_KV.get('key', { cacheTtl: 60 });
```

---

## Critical Rules

### Always Do ✅

1. Use bulk operations when reading multiple keys (counts as 1 operation)
2. Set cacheTtl for frequently-read, infrequently-updated data (min 60s)
3. Store small values (<1024 bytes) in metadata when using `list()` frequently
4. Check `list_complete` when paginating, not `keys.length === 0`
5. Use retry logic with exponential backoff for write operations
6. Validate sizes before writing (key 512B, value 25MiB, metadata 1KB)
7. Coalesce related keys for better caching performance
8. Use KV for read-heavy workloads (100:1 read/write ratio ideal)

### Never Do ❌

1. Never write to same key >1/second (causes 429 rate limit errors)
2. Never assume immediate global consistency (takes ~60 seconds to propagate)
3. Never use KV for atomic operations (use Durable Objects instead)
4. Never set cacheTtl <60 seconds (will fail)
5. Never commit namespace IDs to public repos (use environment variables)
6. Never exceed 1000 operations per invocation (use bulk operations)
7. Never rely on write order (eventual consistency = no guarantees)
8. Never forget to handle null values (`get()` returns `null` if key doesn't exist)

---

## Troubleshooting

### Issue 1: "429 Too Many Requests" on writes
**Cause**: Writing to same key >1/second
**Solution**: Consolidate writes or use retry with exponential backoff

```typescript
// ❌ Bad: Rate limit
for (let i = 0; i < 10; i++) await kv.put('counter', String(i));

// ✅ Good: Single write
await kv.put('counter', '9');

// ✅ Good: Retry with backoff
await putWithRetry(kv, 'counter', String(i));
```

### Issue 2: Stale reads after write
**Cause**: Eventual consistency (~60 seconds propagation)
**Solution**: Accept stale reads, use Durable Objects for strong consistency, or implement app-level cache invalidation

### Issue 3: "Operations limit exceeded"
**Cause**: >1000 KV operations in single Worker invocation
**Solution**: Use bulk operations

```typescript
// ❌ Bad: 5000 operations
for (const key of 5000keys) await kv.get(key);

// ✅ Good: 1 operation
const values = await kv.get(keys);  // Bulk read
```

### Issue 4: List returns empty but cursor exists
**Cause**: Deleted/expired keys create "tombstones" that must be iterated through
**Solution**: Always check `list_complete`, not `keys.length`

```typescript
// ✅ Correct pagination
let cursor: string | undefined;
do {
  const result = await kv.list({ cursor });
  processKeys(result.keys);  // Even if empty
  cursor = result.list_complete ? undefined : result.cursor;
} while (cursor);
```

**CRITICAL**: When using `prefix`, you **must include it in all paginated calls**:

```typescript
// ❌ WRONG - Loses prefix on subsequent pages
let result = await kv.list({ prefix: 'user:' });
result = await kv.list({ cursor: result.cursor });  // Missing prefix!

// ✅ CORRECT - Include prefix on every call
let cursor: string | undefined;
do {
  const result = await kv.list({ prefix: 'user:', cursor });
  processKeys(result.keys);
  cursor = result.list_complete ? undefined : result.cursor;
} while (cursor);
```

**Source**: [List keys documentation](https://developers.cloudflare.com/kv/api/list-keys/)

### Issue 5: `wrangler types` Does Not Generate Types for Environment-Nested KV Bindings

**Cause**: KV namespaces defined within environment configurations (e.g., `[env.feature.kv_namespaces]`) are not included in generated TypeScript types
**Impact**: Loss of TypeScript autocomplete and type checking for KV bindings
**Source**: [GitHub Issue #9709](https://github.com/cloudflare/workers-sdk/issues/9709)

**Example Configuration:**
```toml
# wrangler.toml
[env.feature]
name = "my-worker-feature"
[[env.feature.kv_namespaces]]
binding = "MY_STORAGE_FEATURE"
id = "xxxxxxxxxxxx"
```

Running `npx wrangler types` creates type definitions for environment variables but not for the KV namespace bindings.

**Workaround:**
```bash
# Generate types for specific environment
npx wrangler types -e feature
```

Or define KV namespaces at top level instead of nested in environments:
```toml
# Top-level (types generated correctly)
[[kv_namespaces]]
binding = "MY_STORAGE"
id = "xxxxxxxxxxxx"
```

**Note**: Runtime bindings still work correctly; this only affects type generation.

### Issue 6: `wrangler kv key list` Returns Empty Array for Remote Data

**Cause**: CLI commands default to **local storage**, not remote/production KV
**Impact**: Users expect to see production data but get empty array from local storage
**Source**: [GitHub Issue #10395](https://github.com/cloudflare/workers-sdk/issues/10395)

**Solution**: Use `--remote` flag to access production/remote data

```bash
# ❌ Shows local storage (likely empty)
npx wrangler kv key list --binding=MY_KV

# ✅ Shows remote/production data
npx wrangler kv key list --binding=MY_KV --remote
```

**Why This Happens**: By design, `wrangler dev` uses local KV storage to avoid interfering with production data. CLI commands follow the same default for consistency.

**Applies to**: All `wrangler kv key` commands (get, list, delete, put)

---

## Production Checklist

- [ ] Environment-specific namespaces configured (`id` vs `preview_id`)
- [ ] Namespace IDs stored in environment variables (not hardcoded)
- [ ] Rate limit retry logic implemented for writes
- [ ] Appropriate `cacheTtl` values set for reads (min 60s)
- [ ] Sizes validated (key 512B, value 25MiB, metadata 1KB)
- [ ] Bulk operations used where possible
- [ ] Pagination with `list_complete` check (not `keys.length`)
- [ ] Error handling for null values
- [ ] Monitoring/alerting for rate limits

---

## Related Documentation

- [Cloudflare KV Docs](https://developers.cloudflare.com/kv/)
- [KV API Reference](https://developers.cloudflare.com/kv/api/)
- [KV Limits](https://developers.cloudflare.com/kv/platform/limits/)
- [How KV Works](https://developers.cloudflare.com/kv/concepts/how-kv-works/)
- [Wrangler KV Commands](https://developers.cloudflare.com/workers/wrangler/commands/#kv)

---

**Last Updated**: 2026-01-20
**Package Versions**: wrangler@4.59.2, @cloudflare/workers-types@4.20260109.0
**Changes**: Added 6 research findings - hot/cold key performance patterns, remote bindings (Wrangler 4.37+), wrangler types environment issue, CLI --remote flag requirement, RYOW consistency details, prefix persistence in pagination
