---
name: hono
description: Hono 4.x web framework patterns. Use when building APIs, middleware, routing, or server-side applications. Covers multi-runtime support (Node, Bun, Cloudflare Workers), validation, CORS, and error handling.
---

# Hono

## Overview

Lightweight, fast web framework for building APIs and server-side applications. Hono 4.x works across Node.js, Bun, Deno, Cloudflare Workers, and other runtimes with a consistent API.

**Version**: 4.x
**Install**: `pnpm add hono`

## Workflows

**Creating a basic API:**
1. [ ] Create Hono app instance: `const app = new Hono()`
2. [ ] Define routes with HTTP methods
3. [ ] Add middleware (CORS, logger, error handling)
4. [ ] Export app for runtime adapter
5. [ ] Test endpoints with curl or Postman

**Adding validation:**
1. [ ] Install Zod: `pnpm add zod @hono/zod-validator`
2. [ ] Define schemas with Zod
3. [ ] Apply validator middleware to routes
4. [ ] Handle validation errors
5. [ ] Type-safe request access

## Basic Setup

### Minimal Server (Node.js)

```typescript
import { Hono } from 'hono';
import { serve } from '@hono/node-server';

const app = new Hono();

app.get('/', (c) => {
  return c.text('Hello Hono!');
});

const port = 3000;
console.log(`Server is running on http://localhost:${port}`);

serve({
  fetch: app.fetch,
  port,
});
```

### Bun Runtime

```typescript
import { Hono } from 'hono';

const app = new Hono();

app.get('/', (c) => c.text('Hello from Bun!'));

export default {
  port: 3000,
  fetch: app.fetch,
};
```

### Cloudflare Workers

```typescript
import { Hono } from 'hono';

const app = new Hono();

app.get('/', (c) => c.text('Hello from Cloudflare!'));

export default app;
```

## Routing

### HTTP Methods

```typescript
import { Hono } from 'hono';

const app = new Hono();

// Basic routes
app.get('/users', (c) => c.json({ users: [] }));
app.post('/users', (c) => c.json({ created: true }));
app.put('/users/:id', (c) => c.json({ updated: true }));
app.delete('/users/:id', (c) => c.json({ deleted: true }));
app.patch('/users/:id', (c) => c.json({ patched: true }));

// Multiple methods on same path
app.on(['GET', 'POST'], '/multi', (c) => {
  return c.text(`Method: ${c.req.method}`);
});

// All methods
app.all('/catch-all', (c) => c.text('Any method'));
```

### Route Parameters

```typescript
// Path parameters
app.get('/users/:id', (c) => {
  const id = c.req.param('id');
  return c.json({ userId: id });
});

// Multiple parameters
app.get('/posts/:postId/comments/:commentId', (c) => {
  const { postId, commentId } = c.req.param();
  return c.json({ postId, commentId });
});

// Optional parameters
app.get('/users/:id?', (c) => {
  const id = c.req.param('id');
  return c.json({ userId: id ?? 'all' });
});
```

### Wildcards and Regex

```typescript
// Wildcard (matches anything after)
app.get('/files/*', (c) => {
  return c.text('File handler');
});

// Regex patterns
app.get('/posts/:id{[0-9]+}', (c) => {
  // Only matches numeric IDs
  const id = c.req.param('id');
  return c.json({ postId: Number.parseInt(id) });
});
```

### Route Groups

```typescript
import { Hono } from 'hono';

const app = new Hono();

// API v1 routes
const v1 = new Hono();
v1.get('/users', (c) => c.json({ version: 1, users: [] }));
v1.get('/posts', (c) => c.json({ version: 1, posts: [] }));

// API v2 routes
const v2 = new Hono();
v2.get('/users', (c) => c.json({ version: 2, users: [] }));
v2.get('/posts', (c) => c.json({ version: 2, posts: [] }));

// Mount route groups
app.route('/api/v1', v1);
app.route('/api/v2', v2);
```

## Request Handling

### Query Parameters

```typescript
app.get('/search', (c) => {
  // Single query param
  const query = c.req.query('q');

  // With default value
  const page = c.req.query('page') ?? '1';

  // All query params
  const params = c.req.queries();
  // { q: ['search'], page: ['1'], tags: ['a', 'b'] }

  return c.json({ query, page, params });
});
```

### Request Body

```typescript
// JSON body
app.post('/users', async (c) => {
  const body = await c.req.json();
  return c.json({ received: body });
});

// Form data
app.post('/upload', async (c) => {
  const formData = await c.req.formData();
  const name = formData.get('name');
  return c.text(`Received: ${name}`);
});

// Text body
app.post('/webhook', async (c) => {
  const text = await c.req.text();
  return c.text('OK');
});

// Parse once pattern
app.post('/data', async (c) => {
  const body = await c.req.parseBody();
  // Automatically detects JSON, form data, or multipart
  return c.json(body);
});
```

### Headers

```typescript
app.get('/headers', (c) => {
  // Get single header
  const auth = c.req.header('Authorization');

  // Get all headers
  const headers = c.req.raw.headers;

  // Set response headers
  c.header('X-Custom-Header', 'value');
  c.header('Cache-Control', 'no-cache');

  return c.json({ auth });
});
```

## Response Types

### JSON Response

```typescript
app.get('/users', (c) => {
  return c.json({
    users: [
      { id: 1, name: 'Alice' },
      { id: 2, name: 'Bob' },
    ],
  });
});

// With status code
app.post('/users', (c) => {
  return c.json({ created: true }, 201);
});

// Pretty print in development
app.get('/debug', (c) => {
  return c.json({ data: 'value' }, 200, {
    'Content-Type': 'application/json; charset=utf-8',
  });
});
```

### Other Responses

```typescript
// Text
app.get('/health', (c) => c.text('OK'));

// HTML
app.get('/home', (c) => {
  return c.html('<h1>Welcome</h1>');
});

// Redirect
app.get('/old', (c) => c.redirect('/new'));
app.get('/external', (c) => c.redirect('https://example.com', 301));

// Stream
app.get('/stream', (c) => {
  return c.stream(async (stream) => {
    for (let i = 0; i < 10; i++) {
      await stream.writeln(`Line ${i}`);
      await new Promise((resolve) => setTimeout(resolve, 100));
    }
  });
});

// Not Found
app.get('/missing', (c) => c.notFound());
```

## Middleware

### Built-in Middleware

```typescript
import { Hono } from 'hono';
import { logger } from 'hono/logger';
import { cors } from 'hono/cors';
import { prettyJSON } from 'hono/pretty-json';
import { secureHeaders } from 'hono/secure-headers';

const app = new Hono();

// Logger
app.use('*', logger());

// CORS
app.use('*', cors({
  origin: ['http://localhost:3000', 'https://example.com'],
  allowMethods: ['GET', 'POST', 'PUT', 'DELETE'],
  allowHeaders: ['Content-Type', 'Authorization'],
  credentials: true,
}));

// Pretty JSON in development
if (process.env.NODE_ENV === 'development') {
  app.use('*', prettyJSON());
}

// Security headers
app.use('*', secureHeaders());
```

### Custom Middleware

```typescript
// Simple middleware
app.use('*', async (c, next) => {
  console.log(`[${c.req.method}] ${c.req.url}`);
  await next();
});

// Auth middleware
const authMiddleware = async (c, next) => {
  const token = c.req.header('Authorization');

  if (!token) {
    return c.json({ error: 'Unauthorized' }, 401);
  }

  // Verify token (example)
  if (token !== 'Bearer valid-token') {
    return c.json({ error: 'Invalid token' }, 403);
  }

  // Store user in context
  c.set('user', { id: 1, name: 'Alice' });

  await next();
};

// Apply to specific routes
app.use('/api/*', authMiddleware);

app.get('/api/profile', (c) => {
  const user = c.get('user');
  return c.json({ user });
});
```

### Timing Middleware

```typescript
const timingMiddleware = async (c, next) => {
  const start = Date.now();
  await next();
  const ms = Date.now() - start;
  c.header('X-Response-Time', `${ms}ms`);
};

app.use('*', timingMiddleware);
```

## Validation with Zod

### Setup

```bash
pnpm add zod @hono/zod-validator
```

### Request Validation

```typescript
import { z } from 'zod';
import { zValidator } from '@hono/zod-validator';

// Define schemas
const userSchema = z.object({
  name: z.string().min(1).max(100),
  email: z.string().email(),
  age: z.number().int().min(0).max(120).optional(),
});

const idSchema = z.object({
  id: z.string().regex(/^\d+$/),
});

const querySchema = z.object({
  page: z.string().regex(/^\d+$/).default('1'),
  limit: z.string().regex(/^\d+$/).default('10'),
});

// Validate request body
app.post('/users', zValidator('json', userSchema), async (c) => {
  const user = c.req.valid('json');
  // user is fully typed: { name: string; email: string; age?: number }

  return c.json({ created: true, user }, 201);
});

// Validate path params
app.get('/users/:id', zValidator('param', idSchema), (c) => {
  const { id } = c.req.valid('param');
  return c.json({ userId: id });
});

// Validate query params
app.get('/users', zValidator('query', querySchema), (c) => {
  const { page, limit } = c.req.valid('query');
  return c.json({
    page: Number.parseInt(page),
    limit: Number.parseInt(limit),
    users: [],
  });
});
```

### Custom Validation Error Handling

```typescript
import { zValidator } from '@hono/zod-validator';

app.post(
  '/users',
  zValidator('json', userSchema, (result, c) => {
    if (!result.success) {
      return c.json({
        error: 'Validation failed',
        details: result.error.flatten(),
      }, 400);
    }
  }),
  async (c) => {
    const user = c.req.valid('json');
    return c.json({ created: true, user }, 201);
  }
);
```

## Error Handling

### Try-Catch Pattern

```typescript
app.get('/users/:id', async (c) => {
  try {
    const id = c.req.param('id');
    const user = await db.users.findById(id);

    if (!user) {
      return c.json({ error: 'User not found' }, 404);
    }

    return c.json({ user });
  } catch (error) {
    console.error('Error fetching user:', error);
    return c.json({ error: 'Internal server error' }, 500);
  }
});
```

### Global Error Handler

```typescript
import { HTTPException } from 'hono/http-exception';

app.onError((err, c) => {
  console.error(`Error: ${err.message}`);

  if (err instanceof HTTPException) {
    return c.json({
      error: err.message,
      status: err.status,
    }, err.status);
  }

  return c.json({
    error: 'Internal Server Error',
    message: process.env.NODE_ENV === 'development' ? err.message : undefined,
  }, 500);
});

// Throw HTTP exceptions
app.get('/protected', (c) => {
  throw new HTTPException(403, { message: 'Forbidden' });
});
```

### 404 Handler

```typescript
app.notFound((c) => {
  return c.json({
    error: 'Not Found',
    path: c.req.path,
  }, 404);
});
```

## Type Safety

### Typed Context

```typescript
import type { Context } from 'hono';

type Variables = {
  user: { id: number; name: string };
};

type Env = {
  Variables: Variables;
};

const app = new Hono<Env>();

app.use('/api/*', async (c, next) => {
  c.set('user', { id: 1, name: 'Alice' });
  await next();
});

app.get('/api/profile', (c) => {
  const user = c.get('user'); // Fully typed
  return c.json({ user });
});
```

### RPC Type Safety (Hono Client)

```typescript
// server.ts
const app = new Hono()
  .get('/posts', (c) => c.json({ posts: [] }))
  .post('/posts', async (c) => {
    const body = await c.req.json();
    return c.json({ created: true, post: body }, 201);
  });

export type AppType = typeof app;

// client.ts
import { hc } from 'hono/client';
import type { AppType } from './server';

const client = hc<AppType>('http://localhost:3000');

// Fully typed API calls
const res = await client.posts.$get();
const data = await res.json(); // { posts: [] }

await client.posts.$post({ json: { title: 'Hello' } });
```

## Static Files

```typescript
import { serveStatic } from '@hono/node-server/serve-static';

// Serve from public directory
app.use('/static/*', serveStatic({ root: './' }));

// Serve index.html for SPA
app.get('*', serveStatic({ path: './dist/index.html' }));

// With custom 404
app.use('/assets/*', serveStatic({
  root: './',
  onNotFound: (path, c) => {
    console.log(`${path} is not found`);
  },
}));
```

## CORS Configuration

```typescript
import { cors } from 'hono/cors';

// Permissive (development)
app.use('*', cors());

// Production config
app.use('/api/*', cors({
  origin: (origin) => {
    // Dynamic origin validation
    return origin.endsWith('.example.com') ? origin : 'https://example.com';
  },
  allowMethods: ['GET', 'POST', 'PUT', 'DELETE', 'PATCH'],
  allowHeaders: ['Content-Type', 'Authorization'],
  exposeHeaders: ['X-Total-Count'],
  credentials: true,
  maxAge: 600,
}));
```

## Environment Variables

```typescript
import { Hono } from 'hono';

type Bindings = {
  DATABASE_URL: string;
  API_KEY: string;
};

const app = new Hono<{ Bindings: Bindings }>();

app.get('/config', (c) => {
  // Access environment variables
  const dbUrl = c.env.DATABASE_URL;
  const apiKey = c.env.API_KEY;

  return c.json({ configured: !!dbUrl && !!apiKey });
});

// Node.js
import { serve } from '@hono/node-server';

serve({
  fetch: app.fetch,
  port: 3000,
});

// Access via process.env in Node.js
const dbUrl = process.env.DATABASE_URL;
```

## Testing

```typescript
import { describe, it, expect } from 'vitest';
import { Hono } from 'hono';

describe('API Tests', () => {
  const app = new Hono();

  app.get('/hello', (c) => c.json({ message: 'Hello' }));

  it('should return hello message', async () => {
    const res = await app.request('/hello');

    expect(res.status).toBe(200);
    expect(await res.json()).toEqual({ message: 'Hello' });
  });

  it('should handle POST requests', async () => {
    app.post('/users', async (c) => {
      const body = await c.req.json();
      return c.json({ created: true, user: body }, 201);
    });

    const res = await app.request('/users', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name: 'Alice' }),
    });

    expect(res.status).toBe(201);
    const data = await res.json();
    expect(data.created).toBe(true);
    expect(data.user.name).toBe('Alice');
  });
});
```

## Best Practices

- **Use route groups** to organize related endpoints into modular routers
- **Validate all inputs** with Zod for type safety and runtime validation
- **Apply middleware sparingly** - only use what you need per route
- **Set explicit CORS policies** for production - never use permissive CORS in prod
- **Use typed contexts** for variables set in middleware (user, db, etc.)
- **Handle errors globally** with app.onError() for consistent error responses
- **Return appropriate status codes** - 201 for created, 204 for no content, etc.
- **Use HTTP exceptions** instead of manually creating error responses
- **Test with app.request()** - Hono's built-in testing utility
- **Leverage RPC types** for type-safe client-server communication
- **Keep middleware async** - always await next() in custom middleware
- **Use environment variables** for configuration, never hardcode secrets

## Anti-Patterns

- ❌ Applying logger middleware after routes (won't log those routes)
- ❌ Forgetting to await next() in middleware (breaks middleware chain)
- ❌ Using cors() only on specific routes (preflight requests need global CORS)
- ❌ Parsing request body multiple times (cache result after first parse)
- ❌ Not validating path parameters (always validate user input)
- ❌ Returning without status code for errors (explicit is better)
- ❌ Using any type instead of proper Hono generics
- ❌ Hardcoding origins in CORS config (use environment variables)
- ❌ Missing error handlers (leads to unhandled promise rejections)
- ❌ Not using HTTPException for known errors (inconsistent error format)
- ❌ Setting headers after returning response (headers already sent)
- ❌ Forgetting to export app for runtime adapters

## Feedback Loops

**Testing endpoints:**
```bash
# Test with curl
curl -X GET http://localhost:3000/api/users
curl -X POST http://localhost:3000/api/users \
  -H "Content-Type: application/json" \
  -d '{"name":"Alice","email":"alice@example.com"}'

# Test with httpie (better formatting)
http GET localhost:3000/api/users
http POST localhost:3000/api/users name=Alice email=alice@example.com
```

**Performance testing:**
```bash
# Use autocannon for load testing
pnpm add -D autocannon
npx autocannon -c 100 -d 10 http://localhost:3000/api/users

# Check response times and throughput
# Target: <10ms p99 latency for simple endpoints
```

**Validation testing:**
```bash
# Test invalid data returns 400
curl -X POST http://localhost:3000/api/users \
  -H "Content-Type: application/json" \
  -d '{"name":"","email":"invalid"}'

# Should return validation error with details
```
