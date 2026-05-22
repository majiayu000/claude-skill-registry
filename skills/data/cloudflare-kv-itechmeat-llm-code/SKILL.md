---
name: cloudflare-kv
description: "Cloudflare Workers KV key-value storage playbook: namespaces, bindings, Workers API (get/put/delete/list), metadata, expiration TTL, bulk operations, REST API, consistency model, caching. Keywords: Cloudflare KV, Workers KV, key-value, KVNamespace, binding, metadata, expiration, TTL, cacheTtl, bulk operations, eventually consistent."
---

# Cloudflare Workers KV

KV is a global, low-latency, eventually-consistent key-value store. Optimized for high-read, low-write workloads.

---

## Quick Start

### Create namespace

```bash
npx wrangler kv namespace create MY_KV
```

### Add binding

```jsonc
// wrangler.jsonc
{
  "kv_namespaces": [
    {
      "binding": "MY_KV",
      "id": "06779da6940b431db6e566b4846d64db"
    }
  ]
}
```

### Basic Worker

```typescript
export interface Env {
  MY_KV: KVNamespace;
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    await env.MY_KV.put("user:123", JSON.stringify({ name: "Alice" }));
    const user = await env.MY_KV.get("user:123", "json");
    const keys = await env.MY_KV.list({ prefix: "user:" });
    await env.MY_KV.delete("user:123");
    return Response.json({ user, keys: keys.keys });
  },
};
```

---

## Binding Configuration

```jsonc
// wrangler.jsonc
{
  "kv_namespaces": [
    {
      "binding": "MY_KV", // Variable name in env
      "id": "namespace-uuid", // Namespace ID
      "preview_id": "preview-uuid" // Optional: for local dev
    }
  ]
}
```

```toml
# wrangler.toml
[[kv_namespaces]]
binding = "MY_KV"
id = "namespace-uuid"
preview_id = "preview-uuid"
```

### Remote binding (use production in dev)

```jsonc
{
  "kv_namespaces": [
    {
      "binding": "MY_KV",
      "id": "namespace-uuid",
      "remote": true
    }
  ]
}
```

See [binding.md](references/binding.md) for details.

---

## Workers API

### put(key, value, options?)

```typescript
await env.MY_KV.put("key", "value");

// With options
await env.MY_KV.put("key", "value", {
  expirationTtl: 3600, // Expires in 1 hour
  metadata: { version: 1 },
});

// With absolute expiration
await env.MY_KV.put("key", "value", {
  expiration: Math.floor(Date.now() / 1000) + 86400, // Unix timestamp
});
```

**Value types**: `string | ReadableStream | ArrayBuffer`

**Options**:
| Option | Type | Description |
|--------|------|-------------|
| `expirationTtl` | number | Seconds from now (min 60) |
| `expiration` | number | Unix timestamp (seconds) |
| `metadata` | object | JSON-serializable (max 1024 bytes) |

### get(key, type?)

```typescript
// Text (default)
const text = await env.MY_KV.get("key");

// JSON
const obj = await env.MY_KV.get("key", "json");

// ArrayBuffer
const buffer = await env.MY_KV.get("key", "arrayBuffer");

// Stream
const stream = await env.MY_KV.get("key", "stream");

// With cache TTL
const cached = await env.MY_KV.get("key", { type: "json", cacheTtl: 300 });
```

Returns `null` if key doesn't exist.

### get(keys[]) — Multi-key read

```typescript
const results = await env.MY_KV.get(["key1", "key2", "key3"], "json");
// Returns Map<string, T | null>

for (const [key, value] of results) {
  console.log(key, value);
}
```

Maximum 100 keys per call.

### getWithMetadata(key, type?)

```typescript
const { value, metadata } = await env.MY_KV.getWithMetadata("key", "json");
// value: T | null
// metadata: object | null
```

### list(options?)

```typescript
const result = await env.MY_KV.list();
// { keys: [...], list_complete: boolean, cursor?: string }

// With prefix
const users = await env.MY_KV.list({ prefix: "user:" });

// Pagination
let cursor: string | undefined;
do {
  const result = await env.MY_KV.list({ cursor, limit: 100 });
  for (const key of result.keys) {
    console.log(key.name, key.expiration, key.metadata);
  }
  cursor = result.list_complete ? undefined : result.cursor;
} while (cursor);
```

**Options**:
| Option | Type | Description |
|--------|------|-------------|
| `prefix` | string | Filter keys by prefix |
| `limit` | number | Max keys (default/max: 1000) |
| `cursor` | string | Pagination cursor |

### delete(key)

```typescript
await env.MY_KV.delete("key");
// Resolves even if key doesn't exist
```

See [api.md](references/api.md) for complete reference.

---

## Expiration

### Relative (TTL)

```typescript
await env.MY_KV.put("session:abc", token, {
  expirationTtl: 3600, // 1 hour from now
});
```

### Absolute

```typescript
const expires = new Date("2025-01-01").getTime() / 1000;
await env.MY_KV.put("promo:holiday", data, {
  expiration: expires,
});
```

**Minimum TTL**: 60 seconds.

Expired keys are automatically deleted and not billed.

---

## Metadata

Store up to 1024 bytes of JSON metadata per key.

```typescript
// Write with metadata
await env.MY_KV.put("file:123", fileContent, {
  metadata: {
    filename: "document.pdf",
    contentType: "application/pdf",
    uploadedBy: "user-456",
  },
});

// Read with metadata
const { value, metadata } = await env.MY_KV.getWithMetadata("file:123", "stream");

// Metadata in list results
const { keys } = await env.MY_KV.list({ prefix: "file:" });
for (const key of keys) {
  console.log(key.name, key.metadata);
}
```

**Pattern**: Store small values directly in metadata:

```typescript
await env.MY_KV.put("config:theme", "", {
  metadata: { value: "dark", version: 2 },
});

// Read via list without get()
const { keys } = await env.MY_KV.list({ prefix: "config:" });
const theme = keys.find((k) => k.name === "config:theme")?.metadata?.value;
```

---

## Cache TTL

Control how long reads are cached at edge locations.

```typescript
const data = await env.MY_KV.get("static-config", {
  type: "json",
  cacheTtl: 3600, // Cache for 1 hour
});
```

**Minimum**: 60 seconds. Default: 60 seconds.

**Use cases**:

- Increase for write-rarely data (static configs)
- Keep low or default for frequently-updated data

---

## Bulk Operations

Bulk operations via Wrangler or REST API only (not Workers binding).

### Wrangler bulk write

```bash
# Create JSON file
cat > data.json << 'EOF'
[
  { "key": "user:1", "value": "{\"name\":\"Alice\"}" },
  { "key": "user:2", "value": "{\"name\":\"Bob\"}", "expiration_ttl": 3600 }
]
EOF

npx wrangler kv bulk put data.json --binding MY_KV
```

### Wrangler bulk delete

```bash
cat > keys.json << 'EOF'
["user:1", "user:2", "user:3"]
EOF

npx wrangler kv bulk delete keys.json --binding MY_KV
```

**Limits**: 10,000 keys per request, 100 MB total.

See [bulk.md](references/bulk.md) for REST API examples.

---

## Wrangler Commands

```bash
# Namespace
wrangler kv namespace create <NAME>
wrangler kv namespace list
wrangler kv namespace delete --namespace-id <ID>

# Key operations
wrangler kv key put <KEY> <VALUE> --binding <BINDING>
wrangler kv key get <KEY> --binding <BINDING>
wrangler kv key delete <KEY> --binding <BINDING>
wrangler kv key list --binding <BINDING> [--prefix <PREFIX>]

# With options
wrangler kv key put <KEY> <VALUE> --binding <BINDING> --ttl 3600
wrangler kv key put <KEY> --binding <BINDING> --path ./file.txt

# Bulk
wrangler kv bulk put <FILE.json> --binding <BINDING>
wrangler kv bulk delete <FILE.json> --binding <BINDING>
```

---

## Consistency Model

KV is **eventually consistent**:

- Writes propagate globally in ~60 seconds (or `cacheTtl`)
- Writes are immediately visible at the origin location
- Concurrent writes to same key: **last write wins**
- Negative lookups (key not found) are cached

### Write rate limit

**1 write per second per key**. Exceeding causes 429 errors.

```typescript
// Implement retry with backoff
async function putWithRetry(key: string, value: string, retries = 3) {
  for (let i = 0; i < retries; i++) {
    try {
      await env.MY_KV.put(key, value);
      return;
    } catch (e) {
      if (i < retries - 1) await sleep(1000 * Math.pow(2, i));
      else throw e;
    }
  }
}
```

### When to use Durable Objects instead

- Need strong consistency
- Need atomic operations
- Need > 1 write/sec to same key
- Need transactions

---

## Limits

| Parameter             | Free    | Paid      |
| --------------------- | ------- | --------- |
| Reads/day             | 100,000 | Unlimited |
| Writes/day            | 1,000   | Unlimited |
| Storage               | 1 GB    | Unlimited |
| Namespaces            | 1,000   | 1,000     |
| Ops/Worker invocation | 1,000   | 1,000     |

| Parameter             | Limit       |
| --------------------- | ----------- |
| Key size              | 512 bytes   |
| Value size            | 25 MiB      |
| Metadata size         | 1,024 bytes |
| Keys per list()       | 1,000       |
| Keys per multi-get    | 100         |
| Write rate (same key) | 1/sec       |
| Minimum TTL           | 60 sec      |

---

## Pricing

**Free plan** (per day):

- 100,000 reads
- 1,000 writes/deletes/lists
- 1 GB storage

**Paid plan** (per month):
| Metric | Included | Overage |
|--------|----------|---------|
| Reads | 10 million | $0.50/million |
| Writes | 1 million | $5.00/million |
| Deletes | 1 million | $5.00/million |
| Lists | 1 million | $5.00/million |
| Storage | 1 GB | $0.50/GB |

No egress fees. Dashboard/Wrangler queries are billable.

See [pricing.md](references/pricing.md) for optimization tips.

---

## Best Practices

### Use prefixes for organization

```typescript
// Good: prefixed keys
await env.MY_KV.put("user:123:profile", data);
await env.MY_KV.put("user:123:settings", data);
await env.MY_KV.list({ prefix: "user:123:" });

// Bad: flat keys
await env.MY_KV.put("user_123_profile", data);
```

### Store small values in metadata

```typescript
// Avoid list() + get() for each key
await env.MY_KV.put(key, "", { metadata: { value: smallValue } });
```

### Coalesce related data

```typescript
// Instead of many small keys
await env.MY_KV.put(
  "user:123:settings",
  JSON.stringify({
    theme: "dark",
    language: "en",
    notifications: true,
  })
);
```

### Handle missing keys

```typescript
const value = await env.MY_KV.get("key", "json");
if (value === null) {
  // Key doesn't exist or expired
}
```

---

## Local Development

```bash
# Uses local KV by default
wrangler dev

# Use remote/production KV
wrangler dev --remote
```

Or set `"remote": true` in binding config.

---

## Prohibitions

- ❌ Do not write to same key more than 1/sec
- ❌ Do not rely on immediate consistency after writes
- ❌ Do not use KV for atomic counters (use Durable Objects)
- ❌ Do not exceed 25 MiB value size
- ❌ Do not use bulk write via Workers binding (use REST API)

---

## References

- [binding.md](references/binding.md) — Binding configuration
- [api.md](references/api.md) — Workers API reference
- [bulk.md](references/bulk.md) — Bulk operations
- [pricing.md](references/pricing.md) — Billing and optimization

## Related Skills

- `cloudflare-workers` — Worker development
- `cloudflare-pages` - Pages Functions with KV
- `cloudflare-durable-objects` - Strong consistency alternative
- `cloudflare-d1` — D1 SQL database operations
