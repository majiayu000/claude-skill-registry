---
name: cloudflare-worker-dev
description: Cloudflare Workers, KV, Durable Objects, and edge computing development. Use for serverless APIs, caching, rate limiting, real-time features. Activate on "Workers", "KV", "Durable Objects", "wrangler", "edge function", "Cloudflare". NOT for Cloudflare Pages configuration (use deployment docs), DNS management, or general CDN settings.
allowed-tools: Read,Write,Edit,Bash,Grep,Glob
category: DevOps & Site Reliability
tags:
  - cloudflare
  - workers
  - edge-computing
  - serverless
  - kv
  - caching
  - rate-limiting
---

# Cloudflare Workers Development

Build high-performance edge APIs with Workers, KV for caching, and Durable Objects for real-time coordination.

## Core Architecture

### When to Use What

| Service | Use Case | Characteristics |
|---------|----------|-----------------|
| **Workers** | Request handling, API logic | Stateless, 50ms CPU (free), 30s (paid) |
| **KV** | Caching, config, sessions | Eventually consistent, fast reads |
| **Durable Objects** | Real-time, coordination | Strongly consistent, single-threaded |
| **R2** | File storage | S3-compatible, no egress fees |
| **D1** | SQLite at edge | Serverless SQL, good for reads |

## Worker Fundamentals

### Basic Worker Structure

```typescript
// src/index.ts
export interface Env {
  MEETING_CACHE: KVNamespace;
  RATE_LIMIT: KVNamespace;
  API_KEY: string;
}

export default {
  async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
    const url = new URL(request.url);

    // CORS handling
    if (request.method === 'OPTIONS') {
      return handleCORS();
    }

    try {
      // Route handling
      if (url.pathname === '/health') {
        return json({ status: 'ok' });
      }

      if (url.pathname.startsWith('/api/')) {
        return handleAPI(request, env, ctx);
      }

      return new Response('Not Found', { status: 404 });
    } catch (error) {
      console.error('Worker error:', error);
      return json({ error: 'Internal error' }, 500);
    }
  },

  // Cron trigger
  async scheduled(event: ScheduledEvent, env: Env, ctx: ExecutionContext) {
    ctx.waitUntil(runScheduledTask(env));
  }
};
```

### CORS Headers (Essential)

```typescript
const CORS_HEADERS = {
  'Access-Control-Allow-Origin': '*', // Or specific origin
  'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type, Authorization',
  'Access-Control-Max-Age': '86400',
};

function handleCORS(): Response {
  return new Response(null, { status: 204, headers: CORS_HEADERS });
}

function json(data: unknown, status = 200): Response {
  return new Response(JSON.stringify(data), {
    status,
    headers: {
      ...CORS_HEADERS,
      'Content-Type': 'application/json',
    },
  });
}
```

### wrangler.toml Configuration

```toml
name = "my-worker"
main = "src/index.ts"
compatibility_date = "2024-01-01"

# KV Namespaces
[[kv_namespaces]]
binding = "MEETING_CACHE"
id = "abc123..."  # Production
preview_id = "def456..."  # Dev

[[kv_namespaces]]
binding = "RATE_LIMIT"
id = "ghi789..."

# Environment variables
[vars]
CACHE_TTL = "86400"
RATE_LIMIT_REQUESTS = "100"
RATE_LIMIT_WINDOW = "3600"

# Secrets (set via `wrangler secret put`)
# API_KEY, DATABASE_URL, etc.

# Cron triggers
[triggers]
crons = ["0 */6 * * *"]  # Every 6 hours

# Custom routes
# routes = [{ pattern = "api.example.com/*", zone_name = "example.com" }]
```

## KV Storage Patterns

### Basic KV Operations

```typescript
// Write with TTL
await env.CACHE.put('key', JSON.stringify(data), {
  expirationTtl: 86400, // 24 hours in seconds
});

// Write with metadata
await env.CACHE.put('key', value, {
  expirationTtl: 3600,
  metadata: { createdAt: Date.now(), source: 'api' },
});

// Read
const value = await env.CACHE.get('key');
const parsed = await env.CACHE.get('key', 'json');

// Read with metadata
const { value, metadata } = await env.CACHE.getWithMetadata('key', 'json');

// Delete
await env.CACHE.delete('key');

// List keys
const { keys, cursor } = await env.CACHE.list({ prefix: 'meetings:' });
```

### Geohash-Based Caching

```typescript
import Geohash from 'latlon-geohash';

function getCacheKey(lat: number, lng: number, radius: number): string {
  // 3-char geohash = ~150km cells, good for metro areas
  const geohash = Geohash.encode(lat, lng, 3);
  return `meetings:${geohash}:${radius}`;
}

async function getMeetingsWithCache(
  lat: number,
  lng: number,
  radius: number,
  env: Env
): Promise<{ data: Meeting[]; cached: boolean; geohash: string }> {
  const geohash = Geohash.encode(lat, lng, 3);
  const cacheKey = `meetings:${geohash}:${radius}`;

  // Try cache first
  const cached = await env.MEETING_CACHE.get(cacheKey, 'json');
  if (cached) {
    return { data: cached, cached: true, geohash };
  }

  // Fetch fresh data
  const data = await fetchMeetings(lat, lng, radius);

  // Cache in background (don't await)
  env.ctx.waitUntil(
    env.MEETING_CACHE.put(cacheKey, JSON.stringify(data), {
      expirationTtl: 86400,
      metadata: { cachedAt: Date.now(), geohash },
    })
  );

  return { data, cached: false, geohash };
}
```

### Response Headers for Cache Debugging

```typescript
function meetingsResponse(data: Meeting[], cached: boolean, geohash: string): Response {
  return new Response(JSON.stringify(data), {
    headers: {
      ...CORS_HEADERS,
      'Content-Type': 'application/json',
      'X-Cache': cached ? 'HIT' : 'MISS',
      'X-Geohash': geohash,
      'Cache-Control': 'public, max-age=3600',
    },
  });
}
```

## Rate Limiting

### IP-Based Rate Limiting

```typescript
interface RateLimitConfig {
  maxRequests: number;
  windowSeconds: number;
}

async function checkRateLimit(
  ip: string,
  env: Env,
  config: RateLimitConfig
): Promise<{ allowed: boolean; remaining: number; resetAt: number }> {
  const key = `rate:${ip}`;
  const now = Math.floor(Date.now() / 1000);
  const windowStart = now - config.windowSeconds;

  // Get current state
  const stored = await env.RATE_LIMIT.get(key, 'json') as {
    count: number;
    windowStart: number;
  } | null;

  // New window or expired
  if (!stored || stored.windowStart < windowStart) {
    await env.RATE_LIMIT.put(key, JSON.stringify({
      count: 1,
      windowStart: now,
    }), { expirationTtl: config.windowSeconds });

    return {
      allowed: true,
      remaining: config.maxRequests - 1,
      resetAt: now + config.windowSeconds,
    };
  }

  // Within window
  if (stored.count >= config.maxRequests) {
    return {
      allowed: false,
      remaining: 0,
      resetAt: stored.windowStart + config.windowSeconds,
    };
  }

  // Increment
  await env.RATE_LIMIT.put(key, JSON.stringify({
    count: stored.count + 1,
    windowStart: stored.windowStart,
  }), { expirationTtl: config.windowSeconds });

  return {
    allowed: true,
    remaining: config.maxRequests - stored.count - 1,
    resetAt: stored.windowStart + config.windowSeconds,
  };
}

// Usage in handler
async function handleAPI(request: Request, env: Env): Promise<Response> {
  const ip = request.headers.get('CF-Connecting-IP') || 'unknown';
  const rateLimit = await checkRateLimit(ip, env, {
    maxRequests: parseInt(env.RATE_LIMIT_REQUESTS || '100'),
    windowSeconds: parseInt(env.RATE_LIMIT_WINDOW || '3600'),
  });

  if (!rateLimit.allowed) {
    return json({ error: 'Rate limit exceeded' }, 429, {
      'X-RateLimit-Remaining': '0',
      'X-RateLimit-Reset': rateLimit.resetAt.toString(),
    });
  }

  // ... handle request
}
```

## Durable Objects (Real-Time)

### Chat Room Example

```typescript
// wrangler.toml
// [[durable_objects.bindings]]
// name = "CHAT_ROOMS"
// class_name = "ChatRoom"
// [[migrations]]
// tag = "v1"
// new_classes = ["ChatRoom"]

export class ChatRoom {
  state: DurableObjectState;
  sessions: WebSocket[] = [];

  constructor(state: DurableObjectState) {
    this.state = state;
  }

  async fetch(request: Request): Promise<Response> {
    const url = new URL(request.url);

    if (url.pathname === '/websocket') {
      if (request.headers.get('Upgrade') !== 'websocket') {
        return new Response('Expected WebSocket', { status: 400 });
      }

      const [client, server] = Object.values(new WebSocketPair());

      server.accept();
      this.sessions.push(server);

      server.addEventListener('message', (event) => {
        this.broadcast(event.data as string, server);
      });

      server.addEventListener('close', () => {
        this.sessions = this.sessions.filter(s => s !== server);
      });

      return new Response(null, { status: 101, webSocket: client });
    }

    return new Response('Not found', { status: 404 });
  }

  broadcast(message: string, exclude?: WebSocket) {
    this.sessions.forEach(session => {
      if (session !== exclude && session.readyState === WebSocket.OPEN) {
        session.send(message);
      }
    });
  }
}

// In main worker
export default {
  async fetch(request: Request, env: Env) {
    const url = new URL(request.url);

    if (url.pathname.startsWith('/room/')) {
      const roomId = url.pathname.split('/')[2];
      const id = env.CHAT_ROOMS.idFromName(roomId);
      const room = env.CHAT_ROOMS.get(id);
      return room.fetch(request);
    }
  }
};
```

## Deployment & Debugging

### Commands

```bash
# Development
npx wrangler dev                    # Local dev server
npx wrangler dev --remote           # Dev against real KV/DO

# Deployment
npx wrangler deploy                 # Deploy to production
npx wrangler deploy --env staging   # Deploy to staging

# Secrets
npx wrangler secret put API_KEY     # Set secret
npx wrangler secret list            # List secrets

# KV Management
npx wrangler kv:key list --namespace-id=xxx
npx wrangler kv:key get --namespace-id=xxx "key"
npx wrangler kv:key delete --namespace-id=xxx "key"

# Logs
npx wrangler tail                   # Real-time logs
npx wrangler tail --format=pretty   # Formatted output
```

### Error Codes

| Code | Meaning |
|------|---------|
| 1101 | Worker threw exception |
| 1102 | CPU time limit exceeded |
| 1015 | Rate limited by Cloudflare |
| 524 | Origin timeout (&gt;100s) |

## Quick Reference

```typescript
// Get client IP
const ip = request.headers.get('CF-Connecting-IP');

// Get country
const country = request.cf?.country;

// Background task (won't block response)
ctx.waitUntil(doBackgroundWork());

// Streaming response
return new Response(readableStream, {
  headers: { 'Content-Type': 'text/event-stream' }
});

// Proxy request
const response = await fetch(upstreamUrl, request);
return new Response(response.body, response);
```

## Anti-Patterns

### ❌ Awaiting KV writes in hot path

```typescript
// ❌ ANTI-PATTERN: Blocks response on cache write
async function handler(request: Request, env: Env) {
  const data = await fetchData();
  await env.CACHE.put('key', data);  // Unnecessary wait!
  return json(data);
}

// ✅ CORRECT: Background write with waitUntil
async function handler(request: Request, env: Env, ctx: ExecutionContext) {
  const data = await fetchData();
  ctx.waitUntil(env.CACHE.put('key', data));  // Non-blocking
  return json(data);
}
```

### ❌ Missing CORS handling

```typescript
// ❌ ANTI-PATTERN: No preflight handling = broken browser requests
export default {
  async fetch(request: Request) {
    return json({ data: 'hello' });  // OPTIONS requests fail!
  }
}

// ✅ CORRECT: Handle OPTIONS preflight
export default {
  async fetch(request: Request) {
    if (request.method === 'OPTIONS') {
      return new Response(null, { status: 204, headers: CORS_HEADERS });
    }
    return json({ data: 'hello' });
  }
}
```

### ❌ Secrets in wrangler.toml

```toml
# ❌ ANTI-PATTERN: Secrets in config (committed to git!)
[vars]
API_KEY = "sk-live-xxxxx"

# ✅ CORRECT: Use wrangler secret
# Run: npx wrangler secret put API_KEY
# Access: env.API_KEY
```

### ❌ Ignoring KV eventual consistency

```typescript
// ❌ ANTI-PATTERN: Read immediately after write
await env.KV.put('count', String(newCount));
const verify = await env.KV.get('count');  // May return old value!

// ✅ CORRECT: Trust write succeeded, or use Durable Objects for consistency
await env.KV.put('count', String(newCount));
return json({ count: newCount });  // Return what you wrote
```

### ❌ Blocking on external APIs without timeout

```typescript
// ❌ ANTI-PATTERN: External API can hang your worker
const data = await fetch('https://slow-api.com/data');

// ✅ CORRECT: Add timeout with AbortController
const controller = new AbortController();
const timeout = setTimeout(() => controller.abort(), 5000);
try {
  const data = await fetch('https://slow-api.com/data', {
    signal: controller.signal
  });
} finally {
  clearTimeout(timeout);
}
```

## References

See `/references/` for detailed guides:
- `kv-patterns.md` - Advanced KV usage patterns
- `durable-objects.md` - Real-time features with DO
- `debugging.md` - Troubleshooting common issues
