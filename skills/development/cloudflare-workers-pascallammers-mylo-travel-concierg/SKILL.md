---
name: cloudflare-workers
description: Auto-activates when user mentions Cloudflare Workers, edge functions, or serverless deployment. Expert in Cloudflare Workers including deployment, KV storage, and Durable Objects.
category: serverless
---

# Cloudflare Workers Skill

Expert knowledge in Cloudflare Workers, edge computing, KV storage, Durable Objects, R2, and serverless deployment patterns.

---

## 1. Worker Basics

### 1.1 Worker Syntax & Structure

Workers use the **fetch event handler** pattern to intercept and handle HTTP requests at the edge.

#### ✅ Good: Standard fetch event handler
```typescript
export default {
  async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
    return new Response('Hello from the edge!', {
      status: 200,
      headers: { 'Content-Type': 'text/plain' },
    });
  },
};
```

#### ✅ Good: Module worker with typed environment
```typescript
interface Env {
  MY_KV: KVNamespace;
  MY_SECRET: string;
  MY_DURABLE_OBJECT: DurableObjectNamespace;
}

export default {
  async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
    const url = new URL(request.url);
    
    if (url.pathname === '/api/data') {
      const data = await env.MY_KV.get('key');
      return new Response(data, { status: 200 });
    }
    
    return new Response('Not found', { status: 404 });
  },
};
```

#### ❌ Bad: Using global state (resets between requests)
```typescript
// Global state is NOT persistent across requests!
let requestCount = 0; // ❌ This resets unpredictably

export default {
  async fetch(request: Request): Promise<Response> {
    requestCount++; // ❌ Unreliable counter
    return new Response(`Count: ${requestCount}`);
  },
};
```

#### ❌ Bad: Blocking synchronous operations
```typescript
export default {
  async fetch(request: Request): Promise<Response> {
    // ❌ Don't use synchronous blocking operations
    const data = someHeavyComputationSync(); // Wastes CPU time
    return new Response(data);
  },
};
```

### 1.2 Request & Response Objects

Workers use standard **Web APIs** (Request/Response) for HTTP handling.

#### ✅ Good: Parsing request data
```typescript
export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);
    const method = request.method;
    
    if (method === 'POST') {
      const contentType = request.headers.get('Content-Type');
      
      if (contentType?.includes('application/json')) {
        const body = await request.json();
        return Response.json({ received: body }, { status: 200 });
      }
      
      if (contentType?.includes('application/x-www-form-urlencoded')) {
        const formData = await request.formData();
        return Response.json({ fields: Object.fromEntries(formData) });
      }
    }
    
    return new Response('Method not allowed', { status: 405 });
  },
};
```

#### ✅ Good: Setting response headers and status
```typescript
export default {
  async fetch(request: Request): Promise<Response> {
    const data = { message: 'Success', timestamp: Date.now() };
    
    return new Response(JSON.stringify(data), {
      status: 200,
      headers: {
        'Content-Type': 'application/json',
        'Cache-Control': 'public, max-age=300',
        'X-Custom-Header': 'edge-response',
      },
    });
  },
};
```

### 1.3 Routing Patterns

#### ✅ Good: Path-based routing
```typescript
export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);
    const path = url.pathname;
    
    if (path === '/') {
      return new Response('Home page');
    }
    
    if (path.startsWith('/api/')) {
      return handleAPI(request, env);
    }
    
    if (path.startsWith('/static/')) {
      return handleStatic(request, env);
    }
    
    return new Response('Not found', { status: 404 });
  },
};

async function handleAPI(request: Request, env: Env): Promise<Response> {
  return Response.json({ api: 'v1', status: 'ok' });
}

async function handleStatic(request: Request, env: Env): Promise<Response> {
  // Serve static assets from R2 or KV
  return new Response('Static content', { status: 200 });
}
```

#### ✅ Good: Using URL patterns with regex
```typescript
const routes = [
  { pattern: /^\/api\/users\/(\d+)$/, handler: getUserById },
  { pattern: /^\/api\/posts\/([a-z0-9-]+)$/, handler: getPostBySlug },
  { pattern: /^\/health$/, handler: healthCheck },
];

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);
    
    for (const route of routes) {
      const match = url.pathname.match(route.pattern);
      if (match) {
        return route.handler(request, env, match);
      }
    }
    
    return new Response('Not found', { status: 404 });
  },
};

async function getUserById(
  request: Request,
  env: Env,
  match: RegExpMatchArray
): Promise<Response> {
  const userId = match[1];
  return Response.json({ userId, name: 'John Doe' });
}

async function getPostBySlug(
  request: Request,
  env: Env,
  match: RegExpMatchArray
): Promise<Response> {
  const slug = match[1];
  const post = await env.POSTS_KV.get(slug);
  return new Response(post || 'Not found', { status: post ? 200 : 404 });
}

async function healthCheck(): Promise<Response> {
  return Response.json({ status: 'healthy', timestamp: Date.now() });
}
```

### 1.4 Local Development

Use **Wrangler** for local development with hot reloading.

#### ✅ Good: Local development workflow
```bash
# Install Wrangler globally
npm install -g wrangler

# Create new Worker project
wrangler init my-worker

# Start local development server (port 8787 by default)
wrangler dev

# Start with remote resources (KV, Durable Objects)
wrangler dev --remote

# Start on custom port
wrangler dev --port 3000

# Start with live reload
wrangler dev --live-reload
```

#### ✅ Good: Testing locally with curl
```bash
# Test GET request
curl http://localhost:8787/

# Test POST with JSON
curl -X POST http://localhost:8787/api/data \
  -H "Content-Type: application/json" \
  -d '{"key":"value"}'

# Test with headers
curl http://localhost:8787/api/users/123 \
  -H "Authorization: Bearer token"
```

### 1.5 Deployment

#### ✅ Good: Deploy to production
```bash
# Deploy Worker
wrangler deploy

# Deploy to specific environment
wrangler deploy --env production

# Deploy with verbose logging
wrangler deploy --verbose

# Tail logs after deployment
wrangler tail
```

#### ✅ Good: wrangler.toml configuration
```toml
name = "my-worker"
main = "src/index.ts"
compatibility_date = "2024-11-01"

# Routes (alternative to dashboard configuration)
routes = [
  { pattern = "example.com/*", zone_name = "example.com" }
]

# Environment variables
[vars]
ENVIRONMENT = "production"
API_VERSION = "v1"

# KV bindings
[[kv_namespaces]]
binding = "MY_KV"
id = "abc123"

# Durable Object bindings
[[durable_objects.bindings]]
name = "MY_DO"
class_name = "MyDurableObject"
script_name = "my-worker"

# R2 bindings
[[r2_buckets]]
binding = "MY_BUCKET"
bucket_name = "my-bucket"
```

---

## 2. KV Storage (Key-Value)

Workers KV is a **global, low-latency key-value store** optimized for high read volumes and infrequent writes.

### 2.1 KV Operations

#### ✅ Good: Basic KV operations
```typescript
interface Env {
  MY_KV: KVNamespace;
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);
    const key = url.searchParams.get('key');
    
    if (!key) {
      return new Response('Key required', { status: 400 });
    }
    
    // GET: Read value
    const value = await env.MY_KV.get(key);
    
    if (value === null) {
      return new Response('Not found', { status: 404 });
    }
    
    return new Response(value, { status: 200 });
  },
};
```

#### ✅ Good: PUT with metadata and TTL
```typescript
export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const { key, value, ttl } = await request.json();
    
    // Put with metadata and expiration
    await env.MY_KV.put(key, value, {
      expirationTtl: ttl || 3600, // 1 hour default
      metadata: {
        createdAt: Date.now(),
        version: '1.0',
        author: 'worker',
      },
    });
    
    return Response.json({ success: true, key });
  },
};
```

#### ✅ Good: GET with metadata
```typescript
export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const key = 'user:123';
    
    // Get value with metadata
    const { value, metadata } = await env.MY_KV.getWithMetadata(key);
    
    if (value === null) {
      return new Response('Not found', { status: 404 });
    }
    
    return Response.json({
      value,
      metadata, // Custom metadata attached to the key
    });
  },
};
```

#### ✅ Good: DELETE operation
```typescript
export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const key = 'session:abc123';
    
    // Delete key
    await env.MY_KV.delete(key);
    
    return Response.json({ deleted: true, key });
  },
};
```

### 2.2 KV Namespaces

KV data is organized into **namespaces** (isolated storage buckets).

#### ✅ Good: Multiple namespaces for different data types
```toml
# wrangler.toml
[[kv_namespaces]]
binding = "USERS"
id = "abc123"

[[kv_namespaces]]
binding = "SESSIONS"
id = "def456"

[[kv_namespaces]]
binding = "CACHE"
id = "ghi789"
```

```typescript
interface Env {
  USERS: KVNamespace;
  SESSIONS: KVNamespace;
  CACHE: KVNamespace;
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    // Different namespaces for different purposes
    const user = await env.USERS.get('user:123');
    const session = await env.SESSIONS.get('session:abc');
    const cachedData = await env.CACHE.get('api:response:xyz');
    
    return Response.json({ user, session, cachedData });
  },
};
```

### 2.3 TTL and Expiration

#### ✅ Good: Using TTL for automatic expiration
```typescript
export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const sessionId = 'session:abc123';
    const sessionData = JSON.stringify({ userId: 123, loggedIn: true });
    
    // Expire after 1 hour (3600 seconds)
    await env.SESSIONS.put(sessionId, sessionData, {
      expirationTtl: 3600,
    });
    
    return Response.json({ message: 'Session created with 1-hour TTL' });
  },
};
```

#### ✅ Good: Using absolute expiration timestamp
```typescript
export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const cacheKey = 'cache:data';
    const data = JSON.stringify({ result: 'cached' });
    
    // Expire at specific Unix timestamp (24 hours from now)
    const expirationTime = Math.floor(Date.now() / 1000) + 86400;
    
    await env.CACHE.put(cacheKey, data, {
      expiration: expirationTime,
    });
    
    return Response.json({ message: 'Cached until tomorrow' });
  },
};
```

#### ❌ Bad: Not using TTL for temporary data
```typescript
// ❌ Storing temporary data without expiration
await env.SESSIONS.put('session:temp', 'data'); // Never expires, wastes storage
```

### 2.4 Bulk Operations

#### ✅ Good: Listing keys with pagination
```typescript
export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const allKeys: string[] = [];
    let cursor: string | undefined;
    
    // Paginate through all keys
    do {
      const result = await env.MY_KV.list({ cursor, limit: 1000 });
      allKeys.push(...result.keys.map((k) => k.name));
      cursor = result.cursor;
    } while (cursor);
    
    return Response.json({ keys: allKeys, total: allKeys.length });
  },
};
```

#### ✅ Good: Listing keys with prefix filter
```typescript
export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    // List all user keys (e.g., "user:123", "user:456")
    const result = await env.USERS.list({ prefix: 'user:' });
    
    const userKeys = result.keys.map((k) => k.name);
    
    return Response.json({ users: userKeys });
  },
};
```

#### ❌ Bad: Fetching all keys at once without pagination
```typescript
// ❌ Doesn't handle pagination, limited to 1000 keys
const result = await env.MY_KV.list();
const keys = result.keys.map((k) => k.name); // Only gets first 1000 keys
```

### 2.5 Caching Patterns

#### ✅ Good: Cache-aside pattern
```typescript
export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const userId = 'user:123';
    
    // Try to get from cache first
    let user = await env.CACHE.get(userId);
    
    if (!user) {
      // Cache miss - fetch from origin/database
      user = await fetchUserFromDatabase(userId);
      
      // Store in cache for 5 minutes
      await env.CACHE.put(userId, user, { expirationTtl: 300 });
    }
    
    return new Response(user, { status: 200 });
  },
};

async function fetchUserFromDatabase(userId: string): Promise<string> {
  // Simulate database fetch
  return JSON.stringify({ id: userId, name: 'John Doe' });
}
```

#### ✅ Good: Cache invalidation on updates
```typescript
export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);
    const userId = url.searchParams.get('userId');
    
    if (request.method === 'PUT') {
      const newData = await request.json();
      
      // Update database
      await updateDatabase(userId!, newData);
      
      // Invalidate cache
      await env.CACHE.delete(`user:${userId}`);
      
      return Response.json({ message: 'User updated, cache invalidated' });
    }
    
    return new Response('Method not allowed', { status: 405 });
  },
};

async function updateDatabase(userId: string, data: any): Promise<void> {
  // Update database logic
}
```

#### ❌ Bad: Storing large values in KV
```typescript
// ❌ KV has a 25 MB limit per key
const largeFile = await fetch('https://example.com/large-file.zip').then(r => r.arrayBuffer());
await env.MY_KV.put('file', largeFile); // ❌ May fail if > 25 MB
```

#### ❌ Bad: Using KV for high-write workloads
```typescript
// ❌ KV is optimized for reads, not writes
for (let i = 0; i < 10000; i++) {
  await env.MY_KV.put(`counter:${i}`, String(i)); // ❌ Slow, use Durable Objects instead
}
```

### 2.6 KV Limits

| Limit | Free | Paid |
|-------|------|------|
| Reads/day | 100,000 | Unlimited |
| Writes/day | 1,000 | Unlimited |
| Deletes/day | 1,000 | Unlimited |
| Lists/day | 1,000 | Unlimited |
| Key size | 512 bytes | 512 bytes |
| Value size | 25 MB | 25 MB |
| Metadata size | 1024 bytes | 1024 bytes |

---

## 3. Durable Objects

Durable Objects provide **strongly consistent, stateful storage** at the edge with built-in coordination.

### 3.1 Creating Durable Object Classes

#### ✅ Good: Basic Durable Object structure
```typescript
export class Counter {
  private state: DurableObjectState;
  private count: number = 0;
  
  constructor(state: DurableObjectState, env: Env) {
    this.state = state;
    
    // Load persisted count from storage
    this.state.blockConcurrencyWhile(async () => {
      const stored = await this.state.storage.get<number>('count');
      this.count = stored || 0;
    });
  }
  
  async fetch(request: Request): Promise<Response> {
    const url = new URL(request.url);
    
    if (url.pathname === '/increment') {
      this.count++;
      await this.state.storage.put('count', this.count);
      return Response.json({ count: this.count });
    }
    
    if (url.pathname === '/get') {
      return Response.json({ count: this.count });
    }
    
    return new Response('Not found', { status: 404 });
  }
}
```

#### ✅ Good: Durable Object with alarm
```typescript
export class Scheduler {
  private state: DurableObjectState;
  
  constructor(state: DurableObjectState, env: Env) {
    this.state = state;
  }
  
  async fetch(request: Request): Promise<Response> {
    const { taskId, delay } = await request.json();
    
    // Schedule alarm for future execution
    const alarmTime = Date.now() + delay;
    await this.state.storage.setAlarm(alarmTime);
    await this.state.storage.put('taskId', taskId);
    
    return Response.json({ scheduled: true, alarmTime });
  }
  
  async alarm(): Promise<void> {
    // Called when alarm triggers
    const taskId = await this.state.storage.get<string>('taskId');
    console.log(`Executing task: ${taskId}`);
    
    // Perform scheduled work
    await this.executeTask(taskId);
  }
  
  private async executeTask(taskId: string | undefined): Promise<void> {
    // Task execution logic
  }
}
```

### 3.2 Instance Coordination

#### ✅ Good: Using Durable Objects for coordination
```typescript
export class RateLimiter {
  private state: DurableObjectState;
  
  constructor(state: DurableObjectState, env: Env) {
    this.state = state;
  }
  
  async fetch(request: Request): Promise<Response> {
    const { userId, limit, window } = await request.json();
    
    const key = `requests:${userId}`;
    const now = Date.now();
    
    // Get request timestamps
    let timestamps = await this.state.storage.get<number[]>(key) || [];
    
    // Filter out old timestamps outside the window
    timestamps = timestamps.filter(ts => now - ts < window);
    
    if (timestamps.length >= limit) {
      return Response.json({ allowed: false, remaining: 0 }, { status: 429 });
    }
    
    // Add current timestamp
    timestamps.push(now);
    await this.state.storage.put(key, timestamps);
    
    return Response.json({
      allowed: true,
      remaining: limit - timestamps.length,
    });
  }
}
```

#### ✅ Good: Accessing Durable Objects from Workers
```typescript
interface Env {
  COUNTER: DurableObjectNamespace;
  RATE_LIMITER: DurableObjectNamespace;
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    // Get Durable Object instance by unique ID
    const id = env.COUNTER.idFromName('global-counter');
    const stub = env.COUNTER.get(id);
    
    // Forward request to Durable Object
    return stub.fetch(request);
  },
};
```

#### ✅ Good: Using unique IDs for isolation
```typescript
export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const userId = 'user:123';
    
    // Each user gets their own Durable Object instance
    const id = env.RATE_LIMITER.idFromName(userId);
    const stub = env.RATE_LIMITER.get(id);
    
    const response = await stub.fetch('http://fake-host/check', {
      method: 'POST',
      body: JSON.stringify({ userId, limit: 100, window: 60000 }),
    });
    
    return response;
  },
};
```

### 3.3 WebSocket Connections

#### ✅ Good: WebSocket server in Durable Object
```typescript
export class ChatRoom {
  private state: DurableObjectState;
  private sessions: Set<WebSocket> = new Set();
  
  constructor(state: DurableObjectState, env: Env) {
    this.state = state;
  }
  
  async fetch(request: Request): Promise<Response> {
    // Upgrade to WebSocket
    const upgradeHeader = request.headers.get('Upgrade');
    if (upgradeHeader !== 'websocket') {
      return new Response('Expected WebSocket', { status: 400 });
    }
    
    const pair = new WebSocketPair();
    const [client, server] = Object.values(pair);
    
    // Accept WebSocket connection
    this.state.acceptWebSocket(server);
    this.sessions.add(server);
    
    server.addEventListener('message', (event) => {
      // Broadcast message to all connected clients
      this.broadcast(event.data as string);
    });
    
    server.addEventListener('close', () => {
      this.sessions.delete(server);
    });
    
    return new Response(null, { status: 101, webSocket: client });
  }
  
  private broadcast(message: string): void {
    for (const session of this.sessions) {
      try {
        session.send(message);
      } catch (err) {
        this.sessions.delete(session);
      }
    }
  }
  
  async webSocketMessage(ws: WebSocket, message: string | ArrayBuffer): Promise<void> {
    // Handle incoming WebSocket messages
    this.broadcast(typeof message === 'string' ? message : 'Binary message');
  }
  
  async webSocketClose(ws: WebSocket, code: number, reason: string): Promise<void> {
    this.sessions.delete(ws);
  }
}
```

#### ✅ Good: WebSocket hibernation for scalability
```typescript
export class ScalableChatRoom {
  private state: DurableObjectState;
  
  constructor(state: DurableObjectState, env: Env) {
    this.state = state;
    
    // Enable WebSocket hibernation to reduce memory usage
    this.state.setWebSocketAutoResponse(
      new WebSocketRequestResponsePair(
        JSON.stringify({ type: 'ping' }),
        JSON.stringify({ type: 'pong' })
      )
    );
  }
  
  async fetch(request: Request): Promise<Response> {
    const pair = new WebSocketPair();
    const [client, server] = Object.values(pair);
    
    // Accept with hibernation enabled
    this.state.acceptWebSocket(server);
    
    return new Response(null, { status: 101, webSocket: client });
  }
  
  async webSocketMessage(ws: WebSocket, message: string | ArrayBuffer): Promise<void> {
    // Only called when message is received (not during hibernation)
    const msg = typeof message === 'string' ? message : new TextDecoder().decode(message);
    const data = JSON.parse(msg);
    
    // Broadcast to all active WebSockets
    this.state.getWebSockets().forEach((socket) => {
      socket.send(JSON.stringify({ from: 'server', data }));
    });
  }
}
```

### 3.4 Use Cases

#### ✅ Good: Collaborative editing
```typescript
export class Document {
  private state: DurableObjectState;
  private content: string = '';
  
  constructor(state: DurableObjectState, env: Env) {
    this.state = state;
    
    this.state.blockConcurrencyWhile(async () => {
      this.content = await this.state.storage.get<string>('content') || '';
    });
  }
  
  async fetch(request: Request): Promise<Response> {
    const url = new URL(request.url);
    
    if (url.pathname === '/edit') {
      const { operation, position, text } = await request.json();
      
      // Apply edit operation
      if (operation === 'insert') {
        this.content = this.content.slice(0, position) + text + this.content.slice(position);
      } else if (operation === 'delete') {
        this.content = this.content.slice(0, position) + this.content.slice(position + text.length);
      }
      
      // Persist changes
      await this.state.storage.put('content', this.content);
      
      return Response.json({ success: true, content: this.content });
    }
    
    if (url.pathname === '/get') {
      return Response.json({ content: this.content });
    }
    
    return new Response('Not found', { status: 404 });
  }
}
```

#### ✅ Good: Global counters
```typescript
export class PageViewCounter {
  private state: DurableObjectState;
  private views: Map<string, number> = new Map();
  
  constructor(state: DurableObjectState, env: Env) {
    this.state = state;
  }
  
  async fetch(request: Request): Promise<Response> {
    const { page } = await request.json();
    
    const currentViews = this.views.get(page) || 0;
    const newViews = currentViews + 1;
    
    this.views.set(page, newViews);
    
    // Persist to storage
    await this.state.storage.put(`views:${page}`, newViews);
    
    return Response.json({ page, views: newViews });
  }
}
```

#### ❌ Bad: Using Durable Objects for stateless operations
```typescript
// ❌ Don't use Durable Objects for simple stateless operations
export class SimpleAPI {
  async fetch(request: Request): Promise<Response> {
    // ❌ No state needed, use regular Worker instead
    return Response.json({ message: 'Hello' });
  }
}
```

#### ❌ Bad: Not persisting state to storage
```typescript
export class BadCounter {
  private count: number = 0; // ❌ Only in memory, lost on restart
  
  async fetch(request: Request): Promise<Response> {
    this.count++; // ❌ Not persisted to storage
    return Response.json({ count: this.count });
  }
}
```

---

## 4. R2 Storage

R2 is Cloudflare's **object storage** for large files (images, videos, backups, etc.) with S3-compatible API.

### 4.1 Upload & Download

#### ✅ Good: Upload file to R2
```typescript
interface Env {
  MY_BUCKET: R2Bucket;
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    if (request.method === 'POST') {
      const formData = await request.formData();
      const file = formData.get('file') as File;
      
      if (!file) {
        return new Response('No file provided', { status: 400 });
      }
      
      // Upload to R2
      await env.MY_BUCKET.put(file.name, file.stream(), {
        httpMetadata: {
          contentType: file.type,
        },
        customMetadata: {
          uploadedBy: 'worker',
          uploadedAt: new Date().toISOString(),
        },
      });
      
      return Response.json({ success: true, filename: file.name });
    }
    
    return new Response('Method not allowed', { status: 405 });
  },
};
```

#### ✅ Good: Download file from R2
```typescript
export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);
    const key = url.pathname.slice(1); // Remove leading slash
    
    // Get object from R2
    const object = await env.MY_BUCKET.get(key);
    
    if (!object) {
      return new Response('Object not found', { status: 404 });
    }
    
    // Return object with proper headers
    return new Response(object.body, {
      headers: {
        'Content-Type': object.httpMetadata?.contentType || 'application/octet-stream',
        'Content-Length': String(object.size),
        'ETag': object.etag,
        'Cache-Control': 'public, max-age=3600',
      },
    });
  },
};
```

#### ✅ Good: Upload with custom metadata
```typescript
export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const { key, content, metadata } = await request.json();
    
    await env.MY_BUCKET.put(key, content, {
      httpMetadata: {
        contentType: 'application/json',
        contentEncoding: 'gzip',
        cacheControl: 'public, max-age=31536000',
      },
      customMetadata: {
        version: metadata.version,
        author: metadata.author,
        tags: JSON.stringify(metadata.tags),
      },
    });
    
    return Response.json({ success: true });
  },
};
```

### 4.2 List & Delete

#### ✅ Good: List objects with pagination
```typescript
export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);
    const prefix = url.searchParams.get('prefix') || '';
    const limit = parseInt(url.searchParams.get('limit') || '1000');
    
    const listed = await env.MY_BUCKET.list({
      prefix,
      limit,
    });
    
    const objects = listed.objects.map(obj => ({
      key: obj.key,
      size: obj.size,
      uploaded: obj.uploaded,
      etag: obj.etag,
    }));
    
    return Response.json({
      objects,
      truncated: listed.truncated,
      cursor: listed.cursor,
    });
  },
};
```

#### ✅ Good: Delete object
```typescript
export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    if (request.method === 'DELETE') {
      const url = new URL(request.url);
      const key = url.pathname.slice(1);
      
      await env.MY_BUCKET.delete(key);
      
      return Response.json({ deleted: true, key });
    }
    
    return new Response('Method not allowed', { status: 405 });
  },
};
```

### 4.3 Multipart Uploads

#### ✅ Good: Multipart upload for large files
```typescript
export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const key = 'large-file.zip';
    
    // Start multipart upload
    const multipart = await env.MY_BUCKET.createMultipartUpload(key);
    
    const parts: R2UploadedPart[] = [];
    const chunkSize = 5 * 1024 * 1024; // 5 MB chunks
    
    // Upload parts (simulated)
    for (let i = 0; i < 10; i++) {
      const chunk = new Uint8Array(chunkSize); // Simulate chunk data
      
      const uploadedPart = await multipart.uploadPart(i + 1, chunk);
      parts.push(uploadedPart);
    }
    
    // Complete multipart upload
    const object = await multipart.complete(parts);
    
    return Response.json({ success: true, etag: object.etag });
  },
};
```

#### ❌ Bad: Uploading large files without multipart
```typescript
// ❌ Don't upload files > 100 MB in single request
const largeFile = new Uint8Array(200 * 1024 * 1024); // 200 MB
await env.MY_BUCKET.put('large.bin', largeFile); // ❌ May timeout or fail
```

### 4.4 Public Buckets & Presigned URLs

#### ✅ Good: Serve public files from R2
```typescript
export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);
    const key = url.pathname.slice(1);
    
    const object = await env.MY_BUCKET.get(key);
    
    if (!object) {
      return new Response('Not found', { status: 404 });
    }
    
    // Serve with caching headers
    return new Response(object.body, {
      headers: {
        'Content-Type': object.httpMetadata?.contentType || 'application/octet-stream',
        'Cache-Control': 'public, max-age=86400',
        'ETag': object.etag,
      },
    });
  },
};
```

#### ✅ Good: Generate presigned URL (alternative pattern)
```typescript
// R2 doesn't have native presigned URLs, but you can create signed tokens
export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const key = 'private/document.pdf';
    const token = await generateToken(key, env.SECRET_KEY);
    
    const signedUrl = `https://my-worker.example.com/download/${key}?token=${token}`;
    
    return Response.json({ url: signedUrl });
  },
};

async function generateToken(key: string, secret: string): Promise<string> {
  const data = `${key}:${Date.now() + 3600000}`; // Expires in 1 hour
  const encoder = new TextEncoder();
  const keyData = encoder.encode(secret);
  const algorithm = { name: 'HMAC', hash: 'SHA-256' };
  const cryptoKey = await crypto.subtle.importKey('raw', keyData, algorithm, false, ['sign']);
  const signature = await crypto.subtle.sign(algorithm.name, cryptoKey, encoder.encode(data));
  return btoa(String.fromCharCode(...new Uint8Array(signature)));
}
```

#### ❌ Bad: Exposing sensitive files without authentication
```typescript
// ❌ Serving private files without access control
export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const key = 'private/secret.pdf';
    const object = await env.MY_BUCKET.get(key);
    return new Response(object?.body); // ❌ No authentication!
  },
};
```

---

## 5. Bindings

Bindings connect Workers to Cloudflare resources (KV, Durable Objects, R2, etc.).

### 5.1 KV Bindings

#### ✅ Good: KV binding in wrangler.toml
```toml
[[kv_namespaces]]
binding = "MY_KV"
id = "abc123def456"

[[kv_namespaces]]
binding = "CACHE"
id = "xyz789"
preview_id = "preview123" # For local dev
```

#### ✅ Good: Using KV bindings in TypeScript
```typescript
interface Env {
  MY_KV: KVNamespace;
  CACHE: KVNamespace;
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const data = await env.MY_KV.get('key');
    return new Response(data);
  },
};
```

### 5.2 Durable Object Bindings

#### ✅ Good: Durable Object binding
```toml
[[durable_objects.bindings]]
name = "COUNTER"
class_name = "Counter"
script_name = "my-worker" # Optional if in same script

[[migrations]]
tag = "v1"
new_classes = ["Counter"]
```

```typescript
interface Env {
  COUNTER: DurableObjectNamespace;
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const id = env.COUNTER.idFromName('global');
    const stub = env.COUNTER.get(id);
    return stub.fetch(request);
  },
};

export class Counter {
  private state: DurableObjectState;
  
  constructor(state: DurableObjectState, env: Env) {
    this.state = state;
  }
  
  async fetch(request: Request): Promise<Response> {
    return Response.json({ count: 123 });
  }
}
```

### 5.3 R2 Bindings

#### ✅ Good: R2 bucket binding
```toml
[[r2_buckets]]
binding = "MY_BUCKET"
bucket_name = "my-bucket-name"

[[r2_buckets]]
binding = "ASSETS"
bucket_name = "static-assets"
```

```typescript
interface Env {
  MY_BUCKET: R2Bucket;
  ASSETS: R2Bucket;
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const file = await env.ASSETS.get('logo.png');
    return new Response(file?.body);
  },
};
```

### 5.4 Service Bindings

Service bindings allow Workers to call other Workers directly (RPC-style).

#### ✅ Good: Service binding configuration
```toml
# worker-a/wrangler.toml
name = "worker-a"

[[services]]
binding = "WORKER_B"
service = "worker-b"
```

```typescript
// worker-a/index.ts
interface Env {
  WORKER_B: Fetcher;
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    // Call worker-b directly (no HTTP overhead)
    const response = await env.WORKER_B.fetch('http://fake-host/api/data');
    const data = await response.json();
    
    return Response.json({ fromWorkerB: data });
  },
};
```

```typescript
// worker-b/index.ts
export default {
  async fetch(request: Request): Promise<Response> {
    return Response.json({ message: 'Hello from Worker B' });
  },
};
```

### 5.5 Environment Variables & Secrets

#### ✅ Good: Environment variables
```toml
[vars]
ENVIRONMENT = "production"
API_VERSION = "v1"
MAX_RETRIES = "3"
```

```typescript
interface Env {
  ENVIRONMENT: string;
  API_VERSION: string;
  MAX_RETRIES: string;
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    return Response.json({
      env: env.ENVIRONMENT,
      version: env.API_VERSION,
    });
  },
};
```

#### ✅ Good: Managing secrets with Wrangler
```bash
# Set secret (not stored in wrangler.toml)
wrangler secret put API_KEY
# Enter secret value when prompted

# Delete secret
wrangler secret delete API_KEY

# List secrets
wrangler secret list
```

```typescript
interface Env {
  API_KEY: string; // Secret from Wrangler
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const response = await fetch('https://api.example.com/data', {
      headers: { 'Authorization': `Bearer ${env.API_KEY}` },
    });
    
    return response;
  },
};
```

#### ❌ Bad: Hardcoding secrets in code
```typescript
// ❌ Never hardcode secrets!
const API_KEY = 'sk-1234567890abcdef'; // ❌ Exposed in source code

export default {
  async fetch(request: Request): Promise<Response> {
    const response = await fetch('https://api.example.com', {
      headers: { 'Authorization': `Bearer ${API_KEY}` },
    });
    return response;
  },
};
```

---

## 6. Performance & Limits

### 6.1 CPU Time Limits

| Plan | CPU Time (HTTP) | CPU Time (Cron) |
|------|-----------------|-----------------|
| Free | 10 ms | 10 ms |
| Paid | 30 seconds | 15 minutes |

#### ✅ Good: Efficient CPU usage
```typescript
export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    // Offload heavy computation to external API or Durable Object
    const result = await fetch('https://compute-service.example.com/heavy-task');
    return result;
  },
};
```

#### ❌ Bad: CPU-intensive operations
```typescript
// ❌ Heavy computation exceeds CPU limits
export default {
  async fetch(request: Request): Promise<Response> {
    let result = 0;
    for (let i = 0; i < 1_000_000_000; i++) {
      result += Math.sqrt(i); // ❌ Exceeds 10ms CPU limit
    }
    return Response.json({ result });
  },
};
```

### 6.2 Memory Limits

Workers have a **128 MB memory limit**.

#### ✅ Good: Streaming large responses
```typescript
export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const object = await env.MY_BUCKET.get('large-file.mp4');
    
    // Stream directly (doesn't load into memory)
    return new Response(object?.body, {
      headers: { 'Content-Type': 'video/mp4' },
    });
  },
};
```

#### ❌ Bad: Loading large files into memory
```typescript
// ❌ Loading entire file into memory
export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const object = await env.MY_BUCKET.get('large-file.mp4');
    const arrayBuffer = await object?.arrayBuffer(); // ❌ May exceed 128 MB
    return new Response(arrayBuffer);
  },
};
```

### 6.3 Request & Response Limits

| Limit | Value |
|-------|-------|
| Request URL | 16 KB |
| Request headers | 128 KB |
| Request body (Free/Pro) | 100 MB |
| Request body (Business) | 200 MB |
| Request body (Enterprise) | 500 MB |
| Response headers | 128 KB |
| Subrequests | 50 (Free), 1000 (Paid) |

#### ✅ Good: Handling subrequest limits
```typescript
export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    // Batch requests to stay under subrequest limit
    const urls = ['url1', 'url2', 'url3']; // Only 3 subrequests
    
    const responses = await Promise.all(
      urls.map(url => fetch(`https://api.example.com/${url}`))
    );
    
    const data = await Promise.all(responses.map(r => r.json()));
    
    return Response.json(data);
  },
};
```

#### ❌ Bad: Exceeding subrequest limits
```typescript
// ❌ Too many subrequests on free plan
export default {
  async fetch(request: Request): Promise<Response> {
    const promises = [];
    for (let i = 0; i < 100; i++) {
      promises.push(fetch(`https://api.example.com/item/${i}`)); // ❌ Exceeds 50 subrequests
    }
    await Promise.all(promises);
    return new Response('Done');
  },
};
```

### 6.4 KV Limits (Repeated for Reference)

| Limit | Free | Paid |
|-------|------|------|
| Reads/day | 100,000 | Unlimited |
| Writes/day | 1,000 | Unlimited |
| Key size | 512 bytes | 512 bytes |
| Value size | 25 MB | 25 MB |

### 6.5 Optimization Strategies

#### ✅ Good: Caching responses
```typescript
export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const cache = caches.default;
    const cacheKey = new Request(request.url, request);
    
    // Try cache first
    let response = await cache.match(cacheKey);
    
    if (!response) {
      // Cache miss - fetch from origin
      response = await fetch(request);
      
      // Cache for 1 hour
      response = new Response(response.body, response);
      response.headers.set('Cache-Control', 'public, max-age=3600');
      
      await cache.put(cacheKey, response.clone());
    }
    
    return response;
  },
};
```

#### ✅ Good: Lazy loading and code splitting
```typescript
// Use dynamic imports to reduce initial bundle size
export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);
    
    if (url.pathname.startsWith('/admin')) {
      // Only load admin module when needed
      const { handleAdmin } = await import('./admin');
      return handleAdmin(request, env);
    }
    
    return new Response('Home page');
  },
};
```

---

## 7. Wrangler CLI

Wrangler is the official CLI tool for managing Cloudflare Workers.

### 7.1 Project Initialization

#### ✅ Good: Create new Worker project
```bash
# Create new project with interactive prompts
wrangler init my-worker

# Create with TypeScript
wrangler init my-worker --type typescript

# Create from template
wrangler init my-worker --from-dash
```

#### ✅ Good: Project structure
```
my-worker/
├── src/
│   └── index.ts
├── wrangler.toml
├── package.json
└── tsconfig.json
```

### 7.2 Configuration (wrangler.toml)

#### ✅ Good: Complete wrangler.toml example
```toml
name = "my-worker"
main = "src/index.ts"
compatibility_date = "2024-11-01"
compatibility_flags = ["nodejs_compat"]

# Workers Paid plan
workers_dev = true
account_id = "your-account-id"

# Routes
routes = [
  { pattern = "example.com/api/*", zone_name = "example.com" }
]

# Environment variables
[vars]
ENVIRONMENT = "production"
LOG_LEVEL = "info"

# KV namespaces
[[kv_namespaces]]
binding = "MY_KV"
id = "abc123"

# Durable Objects
[[durable_objects.bindings]]
name = "COUNTER"
class_name = "Counter"
script_name = "my-worker"

# R2 buckets
[[r2_buckets]]
binding = "MY_BUCKET"
bucket_name = "my-bucket"

# Service bindings
[[services]]
binding = "AUTH_SERVICE"
service = "auth-worker"

# Build configuration
[build]
command = "npm run build"

[build.upload]
format = "modules"
main = "./dist/index.js"

# Environments
[env.staging]
vars = { ENVIRONMENT = "staging" }
routes = [{ pattern = "staging.example.com/*", zone_name = "example.com" }]

[env.production]
vars = { ENVIRONMENT = "production" }
routes = [{ pattern = "example.com/*", zone_name = "example.com" }]
```

### 7.3 Local Development

#### ✅ Good: Local dev workflows
```bash
# Start local dev server
wrangler dev

# Dev with remote resources (KV, Durable Objects)
wrangler dev --remote

# Dev with specific port
wrangler dev --port 3000

# Dev with live reload
wrangler dev --live-reload

# Dev with specific environment
wrangler dev --env staging

# Test locally
curl http://localhost:8787/api/test
```

### 7.4 Deployment

#### ✅ Good: Deployment commands
```bash
# Deploy to production
wrangler deploy

# Deploy to specific environment
wrangler deploy --env staging

# Dry run (validate without deploying)
wrangler deploy --dry-run

# Deploy with verbose output
wrangler deploy --verbose

# Rollback to previous version
wrangler rollback
```

### 7.5 Secrets Management

#### ✅ Good: Managing secrets securely
```bash
# Add secret
wrangler secret put API_KEY
# Prompt: Enter a secret value: ********

# Add secret for specific environment
wrangler secret put API_KEY --env production

# List secrets
wrangler secret list

# Delete secret
wrangler secret delete API_KEY

# Bulk secret management
echo "SECRET_VALUE" | wrangler secret put SECRET_KEY
```

### 7.6 Tailing Logs

#### ✅ Good: Real-time log monitoring
```bash
# Tail logs in real-time
wrangler tail

# Tail with filtering
wrangler tail --status error

# Tail specific environment
wrangler tail --env production

# Tail with JSON output
wrangler tail --format json

# Sample logs
wrangler tail --sampling-rate 0.1  # 10% of requests
```

```typescript
// Logging in Worker
export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    console.log('Request received:', request.url);
    console.error('Error occurred:', new Error('Sample error'));
    console.warn('Warning: High memory usage');
    
    return new Response('OK');
  },
};
```

#### ✅ Good: KV management via CLI
```bash
# Create KV namespace
wrangler kv:namespace create "MY_KV"

# List namespaces
wrangler kv:namespace list

# Put key-value
wrangler kv:key put --binding=MY_KV "key" "value"

# Get value
wrangler kv:key get --binding=MY_KV "key"

# Delete key
wrangler kv:key delete --binding=MY_KV "key"

# List keys
wrangler kv:key list --binding=MY_KV --prefix="user:"

# Bulk upload from JSON
wrangler kv:bulk put --binding=MY_KV data.json
```

---

## 8. Use Cases & Patterns

### 8.1 API Proxying

#### ✅ Good: Proxy with caching
```typescript
export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);
    
    // Proxy to backend API
    const backendUrl = `https://api.backend.com${url.pathname}`;
    
    // Check cache first
    const cacheKey = new Request(backendUrl);
    const cachedResponse = await caches.default.match(cacheKey);
    
    if (cachedResponse) {
      return cachedResponse;
    }
    
    // Fetch from backend
    const response = await fetch(backendUrl, {
      headers: {
        'Authorization': `Bearer ${env.API_KEY}`,
      },
    });
    
    // Cache successful responses
    if (response.ok) {
      const responseToCache = response.clone();
      await caches.default.put(cacheKey, responseToCache);
    }
    
    return response;
  },
};
```

### 8.2 A/B Testing

#### ✅ Good: Edge-based A/B testing
```typescript
export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);
    
    // Determine variant based on cookie or random assignment
    const variant = getVariant(request);
    
    if (variant === 'A') {
      return fetch(`https://variant-a.example.com${url.pathname}`);
    } else {
      return fetch(`https://variant-b.example.com${url.pathname}`);
    }
  },
};

function getVariant(request: Request): 'A' | 'B' {
  const cookie = request.headers.get('Cookie');
  
  if (cookie?.includes('variant=A')) {
    return 'A';
  }
  
  if (cookie?.includes('variant=B')) {
    return 'B';
  }
  
  // Random assignment (50/50)
  return Math.random() < 0.5 ? 'A' : 'B';
}
```

### 8.3 Geo-Routing

#### ✅ Good: Route based on location
```typescript
export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const country = request.cf?.country as string;
    
    // Route to regional backend
    if (country === 'US' || country === 'CA') {
      return fetch('https://us-backend.example.com', request);
    } else if (country === 'GB' || country === 'DE' || country === 'FR') {
      return fetch('https://eu-backend.example.com', request);
    } else {
      return fetch('https://global-backend.example.com', request);
    }
  },
};
```

### 8.4 Authentication at the Edge

#### ✅ Good: JWT validation at the edge
```typescript
export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const authHeader = request.headers.get('Authorization');
    
    if (!authHeader?.startsWith('Bearer ')) {
      return new Response('Unauthorized', { status: 401 });
    }
    
    const token = authHeader.slice(7);
    
    // Validate JWT (simplified)
    const isValid = await validateJWT(token, env.JWT_SECRET);
    
    if (!isValid) {
      return new Response('Invalid token', { status: 403 });
    }
    
    // Forward to backend
    return fetch('https://backend.example.com', request);
  },
};

async function validateJWT(token: string, secret: string): Promise<boolean> {
  // JWT validation logic (use library like jose)
  return true; // Simplified
}
```

#### ❌ Bad: Insecure authentication
```typescript
// ❌ Never expose secrets in responses
export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    return Response.json({ secret: env.API_KEY }); // ❌ Exposed!
  },
};
```

---

## Summary

This comprehensive Cloudflare Workers skill covers:

1. **Worker Basics**: Fetch handlers, routing, local dev, deployment
2. **KV Storage**: Key-value operations, TTL, caching patterns, limits
3. **Durable Objects**: Stateful computing, WebSockets, coordination, alarms
4. **R2 Storage**: Object storage, uploads, downloads, multipart uploads
5. **Bindings**: KV, Durable Objects, R2, service bindings, secrets
6. **Performance & Limits**: CPU, memory, request limits, optimization
7. **Wrangler CLI**: Init, config, dev, deploy, secrets, logs
8. **Use Cases**: API proxying, A/B testing, geo-routing, edge auth

Use Cloudflare Workers for **edge computing**, **low-latency APIs**, **global state management**, and **serverless applications** at scale.
