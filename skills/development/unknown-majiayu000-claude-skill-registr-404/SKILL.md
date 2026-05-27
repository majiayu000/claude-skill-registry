---
name: Workers Development
description: This skill should be used when the user asks about "Workers API", "fetch handler", "Workers runtime", "request handling", "response handling", "Workers bindings", "environment variables in Workers", "Workers context", or discusses implementing Workers code, routing patterns, or using Cloudflare bindings like KV, D1, R2, Durable Objects in Workers.
version: 0.1.0
---

# Workers Development

## Purpose

This skill provides comprehensive guidance for developing Cloudflare Workers, including runtime APIs, fetch event handlers, request/response handling, bindings usage, and common development patterns. Use this skill when implementing Workers code, designing Workers architecture, or working with the Workers runtime environment.

## Workers Runtime Overview

Cloudflare Workers run on the V8 JavaScript engine at the edge. Workers use the Service Worker API with extensions specific to the Cloudflare platform.

### Key Characteristics

- **Isolate-based architecture**: Each request runs in an isolated V8 context, not a container
- **Fast cold starts**: Sub-millisecond startup time due to isolate architecture
- **Automatic scaling**: No configuration needed, scales to millions of requests
- **Global deployment**: Code runs at 300+ Cloudflare data centers worldwide
- **Standards-based**: Uses Web APIs (fetch, Request, Response, Headers, etc.)

### Execution Model

Workers execute on incoming requests:

1. Request arrives at Cloudflare edge
2. Worker isolate spawns (or reuses existing)
3. Fetch event handler executes
4. Response returns to client
5. Isolate may persist for subsequent requests

## Fetch Event Handler

The fetch event handler is the entry point for Workers:

```javascript
export default {
  async fetch(request, env, ctx) {
    // request: Request object
    // env: Bindings and environment variables
    // ctx: Execution context with waitUntil() and passThroughOnException()

    return new Response('Hello World');
  }
};
```

### Parameters

**request**: Incoming `Request` object (Web API standard)
- `request.url` - Full URL string
- `request.method` - HTTP method (GET, POST, etc.)
- `request.headers` - Headers object
- `request.body` - ReadableStream of request body
- `request.cf` - Cloudflare-specific properties

**env**: Environment object containing bindings
- KV namespaces: `env.MY_KV`
- D1 databases: `env.MY_DB`
- R2 buckets: `env.MY_BUCKET`
- Durable Objects: `env.MY_DO`
- Secrets: `env.MY_SECRET`
- Environment variables: `env.MY_VAR`

**ctx**: Execution context
- `ctx.waitUntil(promise)` - Extend execution lifetime for async tasks
- `ctx.passThroughOnException()` - Pass request to origin if Worker throws

### Return Value

Must return a `Response` object or a Promise that resolves to a Response:

```javascript
// Direct return
return new Response('Hello', { status: 200 });

// Async return
return await fetch('https://api.example.com');

// With headers
return new Response(JSON.stringify({ ok: true }), {
  status: 200,
  headers: {
    'Content-Type': 'application/json'
  }
});
```

## Request Handling Patterns

### Routing

Common routing patterns for multi-route Workers:

```javascript
export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);

    // Path-based routing
    if (url.pathname === '/api/users') {
      return handleUsers(request, env);
    }

    if (url.pathname.startsWith('/api/')) {
      return handleAPI(request, env);
    }

    // Method-based routing
    if (request.method === 'POST') {
      return handlePost(request, env);
    }

    // Default
    return new Response('Not Found', { status: 404 });
  }
};
```

See `examples/fetch-handler-patterns.js` for complete routing examples.

### Request Inspection

Access request properties:

```javascript
const url = new URL(request.url);
const method = request.method;
const headers = request.headers.get('Authorization');
const cookies = request.headers.get('Cookie');

// Cloudflare-specific properties
const country = request.cf?.country;
const colo = request.cf?.colo; // Data center code
```

### Request Body Parsing

Parse request bodies based on content type:

```javascript
// JSON
const data = await request.json();

// Form data
const formData = await request.formData();
const field = formData.get('fieldName');

// Text
const text = await request.text();

// Array buffer
const buffer = await request.arrayBuffer();
```

## Response Construction

### Basic Responses

```javascript
// Text response
return new Response('Hello World');

// JSON response
return new Response(JSON.stringify({ message: 'Success' }), {
  headers: { 'Content-Type': 'application/json' }
});

// HTML response
return new Response('<h1>Hello</h1>', {
  headers: { 'Content-Type': 'text/html' }
});

// Status codes
return new Response('Not Found', { status: 404 });
return new Response('Created', { status: 201 });
```

### Headers

```javascript
// Set headers
const headers = new Headers({
  'Content-Type': 'application/json',
  'Cache-Control': 'max-age=3600',
  'X-Custom-Header': 'value'
});

return new Response(body, { headers });

// CORS headers
const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type'
};
```

### Redirects

```javascript
// 301 permanent redirect
return Response.redirect('https://example.com', 301);

// 302 temporary redirect
return Response.redirect('https://example.com', 302);
```

## Bindings

Bindings provide access to Cloudflare resources and are configured in `wrangler.toml` or `wrangler.jsonc`.

### Binding Types Overview

- **KV**: Key-value storage for static content
- **D1**: SQLite database for relational data
- **R2**: Object storage for large files
- **Durable Objects**: Stateful coordination and real-time features
- **Queues**: Message queuing for async processing
- **Vectorize**: Vector database for embeddings
- **Workers AI**: AI inference and embeddings
- **Service bindings**: Call other Workers
- **Environment variables**: Configuration values
- **Secrets**: Sensitive credentials

See `references/bindings-guide.md` for complete binding configuration and usage patterns.

### Common Binding Usage

**KV (Key-Value):**
```javascript
// Read
const value = await env.MY_KV.get('key');
const json = await env.MY_KV.get('key', 'json');

// Write
await env.MY_KV.put('key', 'value');
await env.MY_KV.put('key', JSON.stringify(data), {
  expirationTtl: 3600 // Expire in 1 hour
});
```

**D1 (Database):**
```javascript
// Query
const result = await env.MY_DB.prepare(
  'SELECT * FROM users WHERE id = ?'
).bind(userId).first();

// Insert
await env.MY_DB.prepare(
  'INSERT INTO users (name, email) VALUES (?, ?)'
).bind(name, email).run();
```

**R2 (Object Storage):**
```javascript
// Read
const object = await env.MY_BUCKET.get('file.txt');
const text = await object.text();

// Write
await env.MY_BUCKET.put('file.txt', 'content');
```

## Error Handling

### Try-Catch Patterns

```javascript
export default {
  async fetch(request, env, ctx) {
    try {
      // Your logic here
      const result = await processRequest(request, env);
      return new Response(JSON.stringify(result), {
        headers: { 'Content-Type': 'application/json' }
      });
    } catch (error) {
      console.error('Error:', error);
      return new Response(JSON.stringify({
        error: error.message
      }), {
        status: 500,
        headers: { 'Content-Type': 'application/json' }
      });
    }
  }
};
```

### Error Response Helpers

```javascript
function errorResponse(message, status = 500) {
  return new Response(JSON.stringify({ error: message }), {
    status,
    headers: { 'Content-Type': 'application/json' }
  });
}

// Usage
if (!apiKey) {
  return errorResponse('API key required', 401);
}
```

See `examples/error-handling.js` for comprehensive error handling patterns.

## Async Operations with waitUntil

Use `ctx.waitUntil()` to perform background tasks that extend beyond the response:

```javascript
export default {
  async fetch(request, env, ctx) {
    // Respond immediately
    const response = new Response('Request received');

    // Continue processing in background
    ctx.waitUntil(
      logRequest(request, env)
    );

    return response;
  }
};

async function logRequest(request, env) {
  await env.MY_DB.prepare(
    'INSERT INTO logs (url, timestamp) VALUES (?, ?)'
  ).bind(request.url, Date.now()).run();
}
```

**Important**: `waitUntil` extends execution but doesn't guarantee completion. Use for non-critical tasks like logging, analytics, or cache warming.

## Best Practices

### Performance

- **Minimize CPU time**: Workers are billed by CPU time, keep processing lean
- **Use edge caching**: Cache responses at the edge when possible
- **Parallel requests**: Use `Promise.all()` for concurrent operations
- **Avoid blocking**: Don't use synchronous APIs or long computations

### Security

- **Validate inputs**: Always validate and sanitize user input
- **Use secrets**: Store sensitive data in secrets, not environment variables
- **CORS properly**: Configure CORS headers correctly for browser requests
- **Rate limiting**: Implement rate limiting for public APIs

### Debugging

- **Console logging**: Use `console.log()` for debugging (visible in `wrangler tail`)
- **Local testing**: Test with `wrangler dev` before deploying
- **Real-time logs**: Use `wrangler tail` to see production logs
- **Error handling**: Catch and log errors with context

### Code Organization

- **Separate concerns**: Split routing, business logic, and data access
- **Reusable functions**: Create helper functions for common operations
- **Type safety**: Use TypeScript for better IDE support and fewer bugs
- **Environment-aware**: Use bindings through `env`, not globals

## Runtime APIs

Workers support standard Web APIs and Cloudflare-specific extensions.

### Supported Web APIs

- **fetch()** - HTTP requests (Web API standard)
- **Request/Response** - HTTP primitives
- **Headers** - Header manipulation
- **URL** - URL parsing and construction
- **URLSearchParams** - Query string handling
- **ReadableStream/WritableStream** - Streaming data
- **crypto** - Cryptographic operations
- **TextEncoder/TextDecoder** - Text encoding
- **atob/btoa** - Base64 encoding

### Cloudflare Extensions

- **request.cf** - Cloudflare request properties (country, colo, etc.)
- **HTMLRewriter** - HTML parsing and transformation
- **Cache API** - Edge caching control
- **scheduled()** - Cron Triggers (in addition to fetch)

See `references/runtime-apis.md` for complete API documentation and examples.

## TypeScript Support

Workers fully support TypeScript with official type definitions:

```typescript
export interface Env {
  MY_KV: KVNamespace;
  MY_DB: D1Database;
  MY_BUCKET: R2Bucket;
  MY_SECRET: string;
}

export default {
  async fetch(
    request: Request,
    env: Env,
    ctx: ExecutionContext
  ): Promise<Response> {
    // Type-safe access to bindings
    const value = await env.MY_KV.get('key');
    return new Response(value);
  }
};
```

Install types: `npm install -D @cloudflare/workers-types`

## Additional Resources

### Reference Files

For detailed information, consult:
- **`references/runtime-apis.md`** - Complete Workers runtime API documentation with examples
- **`references/bindings-guide.md`** - All binding types with configuration and usage patterns

### Example Files

Working examples in `examples/`:
- **`fetch-handler-patterns.js`** - Common routing and request handling patterns
- **`error-handling.js`** - Comprehensive error handling strategies

### Documentation Links

For the latest documentation:
- Workers fundamentals: https://developers.cloudflare.com/workers/
- Runtime APIs: https://developers.cloudflare.com/workers/runtime-apis/
- Bindings: https://developers.cloudflare.com/workers/configuration/bindings/

Use the cloudflare-docs-specialist agent to search documentation and fetch the latest information.
