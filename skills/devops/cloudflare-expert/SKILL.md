---
name: cloudflare-expert
version: 1.0.0
description: Expert-level Cloudflare Workers, CDN, edge computing, and security services
category: cloud
tags: [cloudflare, edge-computing, cdn, workers, waf]
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash(wrangler:*)
---

# Cloudflare Expert

Expert guidance for Cloudflare Workers, edge computing, CDN optimization, and Cloudflare security services.

## Core Concepts

### Cloudflare Services
- Cloudflare Workers (serverless edge computing)
- CDN and caching
- DDoS protection
- Web Application Firewall (WAF)
- DNS management
- Load balancing
- Workers KV (key-value storage)
- Durable Objects

### Edge Computing
- Deploy code globally
- Reduce latency
- Process at the edge
- Distributed state
- Real-time applications

### Developer Tools
- Wrangler CLI
- Workers Playground
- Edge APIs
- Analytics and logs

## Cloudflare Workers

```javascript
// Basic Worker
export default {
  async fetch(request, env, ctx) {
    return new Response('Hello from Cloudflare Workers!', {
      headers: { 'Content-Type': 'text/plain' }
    });
  }
};

// Advanced routing
export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);

    // Route based on path
    switch (url.pathname) {
      case '/api/users':
        return handleUsers(request, env);
      case '/api/posts':
        return handlePosts(request, env);
      default:
        return new Response('Not Found', { status: 404 });
    }
  }
};

// API endpoint with JSON
async function handleUsers(request, env) {
  if (request.method === 'GET') {
    const users = await env.USERS_KV.get('users', { type: 'json' });
    return new Response(JSON.stringify(users), {
      headers: { 'Content-Type': 'application/json' }
    });
  }

  if (request.method === 'POST') {
    const body = await request.json();
    await env.USERS_KV.put('users', JSON.stringify(body));
    return new Response('Created', { status: 201 });
  }

  return new Response('Method Not Allowed', { status: 405 });
}
```

## Workers KV Storage

```javascript
// Workers KV operations
export default {
  async fetch(request, env, ctx) {
    // Write
    await env.MY_KV.put('key', 'value');

    // Write with metadata and expiration
    await env.MY_KV.put('key', 'value', {
      metadata: { userId: '123' },
      expirationTtl: 3600 // 1 hour
    });

    // Read
    const value = await env.MY_KV.get('key');

    // Read as JSON
    const jsonValue = await env.MY_KV.get('key', { type: 'json' });

    // Read with metadata
    const { value, metadata } = await env.MY_KV.getWithMetadata('key');

    // Delete
    await env.MY_KV.delete('key');

    // List keys
    const keys = await env.MY_KV.list({ prefix: 'user:' });

    return new Response(JSON.stringify({ value, keys }));
  }
};

// Caching pattern
class CachedAPI {
  constructor(kv) {
    this.kv = kv;
  }

  async get(key, fetcher, ttl = 3600) {
    // Try cache first
    const cached = await this.kv.get(key, { type: 'json' });
    if (cached) return cached;

    // Fetch and cache
    const data = await fetcher();
    await this.kv.put(key, JSON.stringify(data), {
      expirationTtl: ttl
    });

    return data;
  }
}

export default {
  async fetch(request, env, ctx) {
    const cache = new CachedAPI(env.MY_KV);

    const data = await cache.get('api:users', async () => {
      const response = await fetch('https://api.example.com/users');
      return response.json();
    }, 3600);

    return new Response(JSON.stringify(data));
  }
};
```

## Durable Objects

```javascript
// Durable Object for stateful logic
export class Counter {
  constructor(state, env) {
    this.state = state;
    this.value = 0;
  }

  async initialize() {
    this.value = await this.state.storage.get('value') || 0;
  }

  async fetch(request) {
    await this.initialize();

    const url = new URL(request.url);

    if (url.pathname === '/increment') {
      this.value++;
      await this.state.storage.put('value', this.value);
      return new Response(String(this.value));
    }

    if (url.pathname === '/decrement') {
      this.value--;
      await this.state.storage.put('value', this.value);
      return new Response(String(this.value));
    }

    return new Response(String(this.value));
  }
}

// WebSocket chat room with Durable Objects
export class ChatRoom {
  constructor(state, env) {
    this.state = state;
    this.sessions = [];
  }

  async fetch(request) {
    if (request.headers.get('Upgrade') !== 'websocket') {
      return new Response('Expected WebSocket', { status: 426 });
    }

    const pair = new WebSocketPair();
    const [client, server] = Object.values(pair);

    await this.handleSession(server);

    return new Response(null, {
      status: 101,
      webSocket: client
    });
  }

  async handleSession(websocket) {
    websocket.accept();
    this.sessions.push(websocket);

    websocket.addEventListener('message', async (msg) => {
      // Broadcast to all sessions
      for (const session of this.sessions) {
        try {
          session.send(msg.data);
        } catch (err) {
          // Remove closed sessions
          this.sessions = this.sessions.filter(s => s !== session);
        }
      }
    });
  }
}

// Worker that uses Durable Object
export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const roomId = url.pathname.slice(1);

    // Get or create Durable Object
    const id = env.CHAT_ROOM.idFromName(roomId);
    const stub = env.CHAT_ROOM.get(id);

    return stub.fetch(request);
  }
};
```

## Request/Response Handling

```javascript
// CORS handling
function handleCORS(request) {
  const corsHeaders = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization'
  };

  // Handle preflight
  if (request.method === 'OPTIONS') {
    return new Response(null, { headers: corsHeaders });
  }

  return corsHeaders;
}

// Authentication middleware
async function authenticate(request, env) {
  const token = request.headers.get('Authorization')?.replace('Bearer ', '');

  if (!token) {
    return new Response('Unauthorized', { status: 401 });
  }

  // Verify token (example using JWT)
  try {
    const payload = await verifyJWT(token, env.JWT_SECRET);
    return payload;
  } catch (err) {
    return new Response('Invalid token', { status: 401 });
  }
}

// Rate limiting
class RateLimiter {
  constructor(kv) {
    this.kv = kv;
  }

  async checkLimit(identifier, maxRequests, windowSeconds) {
    const key = `rate_limit:${identifier}`;
    const now = Date.now();
    const windowMs = windowSeconds * 1000;

    // Get current count
    const data = await this.kv.get(key, { type: 'json' });

    if (!data || now - data.timestamp > windowMs) {
      // New window
      await this.kv.put(key, JSON.stringify({
        count: 1,
        timestamp: now
      }), { expirationTtl: windowSeconds });
      return true;
    }

    if (data.count >= maxRequests) {
      return false; // Rate limit exceeded
    }

    // Increment count
    data.count++;
    await this.kv.put(key, JSON.stringify(data), {
      expirationTtl: windowSeconds
    });

    return true;
  }
}

export default {
  async fetch(request, env, ctx) {
    const corsHeaders = handleCORS(request);
    if (request.method === 'OPTIONS') return corsHeaders;

    // Rate limiting
    const rateLimiter = new RateLimiter(env.RATE_LIMIT_KV);
    const clientIP = request.headers.get('CF-Connecting-IP');
    const allowed = await rateLimiter.checkLimit(clientIP, 100, 60);

    if (!allowed) {
      return new Response('Rate limit exceeded', {
        status: 429,
        headers: corsHeaders
      });
    }

    // Authentication
    const user = await authenticate(request, env);
    if (user instanceof Response) {
      return user; // Error response
    }

    // Process request
    const response = await handleRequest(request, env, user);

    // Add CORS headers to response
    Object.entries(corsHeaders).forEach(([key, value]) => {
      response.headers.set(key, value);
    });

    return response;
  }
};
```

## Caching Strategies

```javascript
// Cache API
async function cacheFirst(request) {
  const cache = caches.default;
  let response = await cache.match(request);

  if (!response) {
    response = await fetch(request);
    // Cache for 1 hour
    response = new Response(response.body, response);
    response.headers.set('Cache-Control', 'max-age=3600');
    await cache.put(request, response.clone());
  }

  return response;
}

// Stale-while-revalidate
async function staleWhileRevalidate(request, ctx) {
  const cache = caches.default;
  let response = await cache.match(request);

  // Background refresh
  ctx.waitUntil(
    fetch(request).then(freshResponse => {
      const clonedResponse = freshResponse.clone();
      cache.put(request, clonedResponse);
    })
  );

  if (response) {
    return response;
  }

  return fetch(request);
}

// Custom cache keys
function customCacheKey(request) {
  const url = new URL(request.url);

  // Ignore query parameters for caching
  url.search = '';

  // Add custom cache key based on headers
  const userAgent = request.headers.get('User-Agent');
  const isMobile = /mobile/i.test(userAgent);
  url.searchParams.set('device', isMobile ? 'mobile' : 'desktop');

  return new Request(url.toString(), request);
}

export default {
  async fetch(request, env, ctx) {
    const cacheKey = customCacheKey(request);

    if (request.url.includes('/api/')) {
      // API routes: stale-while-revalidate
      return staleWhileRevalidate(cacheKey, ctx);
    }

    // Static assets: cache first
    return cacheFirst(cacheKey);
  }
};
```

## Edge Functions

```javascript
// HTML rewriting
export default {
  async fetch(request, env, ctx) {
    const response = await fetch(request);

    // Inject analytics script
    return new HTMLRewriter()
      .on('head', new HeadInjector())
      .transform(response);
  }
};

class HeadInjector {
  element(element) {
    element.append(
      '<script>console.log("Injected at edge!");</script>',
      { html: true }
    );
  }
}

// Geolocation-based routing
export default {
  async fetch(request, env, ctx) {
    const country = request.cf.country;

    // Route based on country
    const apiEndpoint = {
      'US': 'https://us-api.example.com',
      'EU': 'https://eu-api.example.com',
      'default': 'https://global-api.example.com'
    }[country] || 'https://global-api.example.com';

    const url = new URL(request.url);
    const apiUrl = new URL(url.pathname, apiEndpoint);

    return fetch(apiUrl, request);
  }
};

// A/B testing
export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);

    // Determine variant
    let variant = request.headers.get('Cookie')?.match(/variant=(\w+)/)?.[1];

    if (!variant) {
      variant = Math.random() < 0.5 ? 'A' : 'B';
    }

    // Fetch appropriate version
    const response = await fetch(`${url.origin}/variant-${variant}${url.pathname}`);

    // Set cookie
    const newResponse = new Response(response.body, response);
    newResponse.headers.set('Set-Cookie', `variant=${variant}; Path=/; Max-Age=86400`);

    return newResponse;
  }
};
```

## Wrangler CLI

```bash
# Initialize project
wrangler init my-worker

# Development server
wrangler dev

# Deploy to production
wrangler publish

# Deploy to specific environment
wrangler publish --env production

# Tail logs
wrangler tail

# KV operations
wrangler kv:namespace create "MY_KV"
wrangler kv:key put --namespace-id=<id> "key" "value"
wrangler kv:key get --namespace-id=<id> "key"

# Durable Objects
wrangler publish --new-class Counter

# Secrets
wrangler secret put SECRET_NAME
```

## wrangler.toml Configuration

```toml
name = "my-worker"
main = "src/index.js"
compatibility_date = "2024-01-01"

# KV bindings
kv_namespaces = [
  { binding = "MY_KV", id = "xxxxxxxx" },
  { binding = "CACHE_KV", id = "yyyyyyyy" }
]

# Durable Objects
[durable_objects]
bindings = [
  { name = "COUNTER", class_name = "Counter" },
  { name = "CHAT_ROOM", class_name = "ChatRoom" }
]

[[migrations]]
tag = "v1"
new_classes = ["Counter", "ChatRoom"]

# Environment variables
[vars]
ENVIRONMENT = "production"

# Routes
routes = [
  { pattern = "example.com/*", zone_name = "example.com" }
]

# Cron triggers
[triggers]
crons = ["0 */6 * * *"]
```

## Best Practices

### Performance
- Cache aggressively at the edge
- Minimize worker execution time
- Use Workers KV for global data
- Implement connection pooling
- Optimize cache keys
- Use stale-while-revalidate
- Minimize external requests

### Security
- Validate all inputs
- Implement rate limiting
- Use secrets for sensitive data
- Set security headers
- Implement CORS properly
- Use HTTPS everywhere
- Log security events

### Development
- Use TypeScript for type safety
- Test locally with wrangler dev
- Implement proper error handling
- Monitor worker metrics
- Use environment variables
- Version your workers
- Document API endpoints

## Anti-Patterns

❌ Storing large data in KV frequently
❌ Long-running computations in workers
❌ Not implementing caching
❌ Hardcoding secrets
❌ Ignoring rate limits
❌ No error handling
❌ Excessive external API calls

## Resources

- Cloudflare Workers: https://workers.cloudflare.com/
- Wrangler CLI: https://developers.cloudflare.com/workers/wrangler/
- Workers Examples: https://developers.cloudflare.com/workers/examples/
- Durable Objects: https://developers.cloudflare.com/workers/learning/using-durable-objects/
- Workers KV: https://developers.cloudflare.com/workers/runtime-apis/kv/
