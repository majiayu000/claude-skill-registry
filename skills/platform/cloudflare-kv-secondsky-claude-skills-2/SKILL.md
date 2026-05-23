---
name: cloudflare-kv
description: Cloudflare Workers KV global key-value storage. Use for namespaces, caching, TTL, or encountering KV_ERROR, 429 rate limits, consistency issues.

  Keywords: kv storage, cloudflare kv, workers kv, kv namespace, kv bindings, kv cache, kv ttl, kv metadata,
  kv list, kv pagination, cache optimization, edge caching, KV_ERROR, 429 too many requests, kv rate limit,
  eventually consistent, wrangler kv, kv operations, key value storage
license: MIT
metadata:
  version: "3.0.0"
  last_verified: "2025-12-27"
  production_tested: true
  token_savings: "~60%"
  errors_prevented: 5
  templates_included: 5
  references_included: 7
---

# Cloudflare Workers KV

**Status**: Production Ready ✅ | **Last Verified**: 2025-12-27

---

## What Is Workers KV?

Global key-value storage on Cloudflare edge:
- Eventually consistent
- Low latency worldwide
- 1GB+ values supported
- TTL expiration
- Metadata support

---

## Quick Start (5 Minutes)

### 1. Create KV Namespace

```bash
bunx wrangler kv namespace create MY_NAMESPACE
bunx wrangler kv namespace create MY_NAMESPACE --preview
```

### 2. Configure Binding

```jsonc
{
  "name": "my-worker",
  "main": "src/index.ts",
  "compatibility_date": "2025-10-11",
  "kv_namespaces": [
    {
      "binding": "MY_NAMESPACE",
      "id": "<PRODUCTION_ID>",
      "preview_id": "<PREVIEW_ID>"
    }
  ]
}
```

### 3. Basic Operations

```typescript
export default {
  async fetch(request, env, ctx) {
    // Write
    await env.MY_NAMESPACE.put('key', 'value');

    // Read
    const value = await env.MY_NAMESPACE.get('key');

    // Delete
    await env.MY_NAMESPACE.delete('key');

    return new Response(value);
  }
};
```

**Load `references/setup-guide.md` for complete setup.**

---

## KV API Methods

### put() - Write

```typescript
// Basic
await env.MY_NAMESPACE.put('key', 'value');

// With TTL (1 hour)
await env.MY_NAMESPACE.put('key', 'value', {
  expirationTtl: 3600
});

// With expiration timestamp
await env.MY_NAMESPACE.put('key', 'value', {
  expiration: Math.floor(Date.now() / 1000) + 3600
});

// With metadata
await env.MY_NAMESPACE.put('key', 'value', {
  metadata: { role: 'admin', created: Date.now() }
});
```

### get() - Read

```typescript
// Simple get
const value = await env.MY_NAMESPACE.get('key');

// With type
const text = await env.MY_NAMESPACE.get('key', 'text');
const json = await env.MY_NAMESPACE.get('key', 'json');
const buffer = await env.MY_NAMESPACE.get('key', 'arrayBuffer');
const stream = await env.MY_NAMESPACE.get('key', 'stream');

// With metadata
const { value, metadata } = await env.MY_NAMESPACE.getWithMetadata('key');
```

### delete() - Remove

```typescript
await env.MY_NAMESPACE.delete('key');
```

### list() - List Keys

```typescript
// Basic list
const { keys } = await env.MY_NAMESPACE.list();

// With prefix
const { keys } = await env.MY_NAMESPACE.list({
  prefix: 'user:',
  limit: 100
});

// Pagination
const { keys, cursor } = await env.MY_NAMESPACE.list({
  cursor: previousCursor
});
```

---

## Critical Rules

### Always Do ✅

1. **Use TTL** for temporary data
2. **Handle null** (key might not exist)
3. **Use metadata** for small data
4. **Paginate lists** (max 1000 keys)
5. **Use prefixes** for organization
6. **Cache in Worker** (avoid multiple KV calls)
7. **Use waitUntil()** for async writes
8. **Handle eventual consistency**
9. **Monitor rate limits**
10. **Use JSON.stringify** for objects

### Never Do ❌

1. **Never assume instant** consistency
2. **Never exceed 25MB** per value
3. **Never list all keys** without pagination
4. **Never skip error handling**
5. **Never use for real-time** data
6. **Never exceed rate limits** (1000 writes/second)
7. **Never store secrets** unencrypted
8. **Never use as database** (no transactions)
9. **Never ignore metadata limits** (1024 bytes)
10. **Never skip TTL** for temporary data

---

## Common Use Cases

### Use Case 1: API Response Caching

```typescript
const cacheKey = `api:${url}`;
let cached = await env.MY_NAMESPACE.get(cacheKey, 'json');

if (!cached) {
  cached = await fetch(url).then(r => r.json());
  await env.MY_NAMESPACE.put(cacheKey, JSON.stringify(cached), {
    expirationTtl: 300  // 5 minutes
  });
}

return Response.json(cached);
```

### Use Case 2: User Preferences

```typescript
const userId = '123';
const preferences = {
  theme: 'dark',
  language: 'en'
};

await env.MY_NAMESPACE.put(
  `user:${userId}:preferences`,
  JSON.stringify(preferences),
  {
    metadata: { updated: Date.now() }
  }
);
```

### Use Case 3: Rate Limiting

```typescript
const key = `ratelimit:${ip}`;
const count = parseInt(await env.MY_NAMESPACE.get(key) || '0');

if (count >= 100) {
  return new Response('Rate limit exceeded', { status: 429 });
}

await env.MY_NAMESPACE.put(key, String(count + 1), {
  expirationTtl: 60  // 1 minute window
});
```

### Use Case 4: List with Prefix

```typescript
const { keys } = await env.MY_NAMESPACE.list({
  prefix: 'user:',
  limit: 100
});

const users = await Promise.all(
  keys.map(({ name }) => env.MY_NAMESPACE.get(name, 'json'))
);
```

### Use Case 5: waitUntil() Pattern

```typescript
export default {
  async fetch(request, env, ctx) {
    // Don't wait for KV write
    ctx.waitUntil(
      env.MY_NAMESPACE.put('analytics', JSON.stringify(data))
    );

    return new Response('OK');
  }
};
```

---

## Limits (Summary)

**Key Limits:**
- Key size: 512 bytes max
- Value size: 25 MB max
- Metadata: 1024 bytes max

**Rate Limits:**
- Writes: 1000/sec per key
- List: 100/sec per namespace
- Reads: Unlimited

**For detailed limits, pricing, and optimization strategies, load `references/limits-quotas.md`**

---

## Eventual Consistency

KV is **eventually consistent**:
- Writes propagate globally (~60 seconds)
- Not suitable for real-time data
- Use D1 for strong consistency

**Pattern:**

```typescript
// Write
await env.MY_NAMESPACE.put('key', 'value');

// May not be visible immediately in other regions
const value = await env.MY_NAMESPACE.get('key');  // Might be null
```

---

## When to Load References

Load specific reference files based on task context:

**For Setup & Configuration:**
- Load `references/setup-guide.md` when creating namespaces or configuring bindings

**For Performance Optimization:**
- Load `references/best-practices.md` when implementing caching or optimizing performance
- Load `references/performance-tuning.md` for advanced optimization scenarios, cacheTtl strategies, or benchmarking

**For API Usage:**
- Load `references/workers-api.md` when implementing KV operations or need method signatures

**For Troubleshooting:**
- Load `references/troubleshooting.md` when debugging errors or consistency issues

**For Limits & Quotas:**
- Load `references/limits-quotas.md` when planning capacity or encountering quota errors

**For Migration:**
- Load `references/migration-guide.md` when migrating from localStorage, Redis, D1, R2, or other storage solutions

---

## Resources

**References** (`references/`):
- `best-practices.md` - Production patterns, caching strategies, rate limit handling, error recovery
- `setup-guide.md` - Complete setup with Wrangler CLI commands, namespace creation, bindings configuration
- `workers-api.md` - Complete API reference, consistency model (eventual consistency), limits & quotas, performance optimization
- `troubleshooting.md` - Comprehensive error catalog with solutions
- `limits-quotas.md` - Detailed limits, quotas, pricing, and optimization tips
- `migration-guide.md` - Complete migration guides from localStorage, Redis, D1, R2, and other storage solutions
- `performance-tuning.md` - Advanced cacheTtl strategies, bulk operations, key design, benchmarking techniques

**Templates** (`templates/`):
- `kv-basic-operations.ts` - Basic KV operations (get, put, delete, list)
- `kv-caching-pattern.ts` - HTTP caching with KV
- `kv-list-pagination.ts` - List with cursor pagination
- `kv-metadata-pattern.ts` - Metadata usage patterns
- `wrangler-kv-config.jsonc` - KV namespace bindings

**Scripts** (`scripts/`):
- `check-versions.sh` - Validate KV API endpoints and package versions
- `test-kv-connection.sh` - Test KV namespace connection and operations
- `setup-kv-namespace.sh` - Interactive namespace setup wizard
- `validate-kv-config.sh` - Validate wrangler.jsonc configuration
- `analyze-kv-usage.sh` - Analyze code for KV usage patterns and optimizations

**Commands:**
- `/cloudflare-kv:setup` - Interactive KV namespace setup wizard
- `/cloudflare-kv:test` - Test KV operations and connection
- `/cloudflare-kv:optimize` - Analyze and optimize KV usage

**Agents:**
- `kv-optimizer` - Analyzes KV usage and suggests performance optimizations
- `kv-debugger` - Helps debug KV errors and consistency issues

**Examples** (`examples/`):
- `rate-limiting/` - Complete rate limiting implementation (fixed window, sliding window, token bucket, multi-tier)
- `session-management/` - Production session store with TTL expiration, metadata tracking, and admin controls
- `api-caching/` - HTTP response caching patterns (cache-aside, stale-while-revalidate, conditional caching, ETag)
- `config-management/` - Feature flags, A/B testing, environment configs, version tracking, hot-reload

---

## Official Documentation

- **KV Overview**: https://developers.cloudflare.com/kv/
- **KV API**: https://developers.cloudflare.com/kv/api/
- **Best Practices**: https://developers.cloudflare.com/kv/best-practices/

---

**Questions? Issues?**

1. Check `references/setup-guide.md` for complete setup
2. Verify namespace binding configured
3. Handle eventual consistency
4. Check rate limits
