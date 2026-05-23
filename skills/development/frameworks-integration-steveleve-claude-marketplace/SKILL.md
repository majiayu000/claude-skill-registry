---
name: Frameworks Integration
description: Use when asking about "Hono", "itty-router", "routing frameworks", "middleware", "API framework", "web framework for Workers", "request routing", "Express-like", or choosing between web frameworks for Cloudflare Workers.
version: 0.1.0
---

# Web Frameworks for Workers

## Purpose

This skill provides guidance on web frameworks for Cloudflare Workers, with focus on Hono and itty-router—the two most popular choices. Use this when building API endpoints, adding middleware, or choosing between vanilla fetch handlers and framework-based routing.

## When to Use a Framework

**Use a framework when**:
- Multiple routes/endpoints (>3-4)
- Need middleware (auth, logging, CORS)
- Building a REST API
- Want type-safe routing
- Team is familiar with Express-like patterns

**Stay vanilla when**:
- Single endpoint or simple proxy
- Maximum performance critical
- Minimal dependencies desired
- Learning Workers fundamentals

## Framework Comparison

| Feature | Hono | itty-router | Vanilla |
|---------|------|-------------|---------|
| **Bundle size** | ~14KB | ~1KB | 0KB |
| **Type safety** | Excellent | Good | Manual |
| **Middleware** | Built-in system | Basic | Manual |
| **Learning curve** | Medium | Low | Low |
| **Documentation** | Extensive | Moderate | N/A |
| **Active development** | Very active | Active | N/A |
| **Best for** | Full APIs | Simple routing | Single endpoint |

## Hono

### Why Hono

- Express-like API, easy to learn
- Excellent TypeScript support
- Rich middleware ecosystem
- Built for edge runtimes
- Active community and development

### Basic Setup

```typescript
import { Hono } from 'hono';

type Bindings = {
  DATABASE: D1Database;
  AI: Ai;
  CACHE: KVNamespace;
};

const app = new Hono<{ Bindings: Bindings }>();

// Routes
app.get('/', (c) => c.text('Hello from Hono!'));

app.get('/api/users', async (c) => {
  const users = await c.env.DATABASE
    .prepare('SELECT * FROM users')
    .all();
  return c.json(users.results);
});

app.post('/api/users', async (c) => {
  const body = await c.req.json();
  // Validate and create user
  return c.json({ id: '123', ...body }, 201);
});

export default app;
```

### Middleware

```typescript
import { Hono } from 'hono';
import { cors } from 'hono/cors';
import { logger } from 'hono/logger';
import { bearerAuth } from 'hono/bearer-auth';

const app = new Hono<{ Bindings: Bindings }>();

// Global middleware
app.use('*', logger());
app.use('*', cors({
  origin: ['https://example.com'],
  allowMethods: ['GET', 'POST', 'PUT', 'DELETE'],
}));

// Route-specific middleware
app.use('/api/*', bearerAuth({ token: 'secret' }));

// Or custom middleware
app.use('/api/*', async (c, next) => {
  const start = Date.now();
  await next();
  const ms = Date.now() - start;
  c.header('X-Response-Time', `${ms}ms`);
});
```

### Route Groups

```typescript
const app = new Hono<{ Bindings: Bindings }>();

// API routes
const api = new Hono<{ Bindings: Bindings }>();
api.get('/users', usersHandler);
api.get('/users/:id', userByIdHandler);
api.post('/users', createUserHandler);

// Mount the group
app.route('/api', api);

// Or inline grouping
app.route('/api/v2', new Hono()
  .get('/health', (c) => c.json({ status: 'ok' }))
  .get('/version', (c) => c.json({ version: '2.0' }))
);
```

### Error Handling

```typescript
import { HTTPException } from 'hono/http-exception';

app.onError((err, c) => {
  if (err instanceof HTTPException) {
    return c.json({ error: err.message }, err.status);
  }
  console.error('Unhandled error:', err);
  return c.json({ error: 'Internal server error' }, 500);
});

// Throwing HTTP exceptions
app.get('/api/users/:id', async (c) => {
  const id = c.req.param('id');
  const user = await getUser(id);

  if (!user) {
    throw new HTTPException(404, { message: 'User not found' });
  }

  return c.json(user);
});
```

### With Workers AI

```typescript
app.post('/api/chat', async (c) => {
  const { message } = await c.req.json();

  const response = await c.env.AI.run('@cf/meta/llama-3.1-8b-instruct', {
    messages: [
      { role: 'system', content: 'You are a helpful assistant.' },
      { role: 'user', content: message }
    ]
  });

  return c.json({ response: response.response });
});

// Streaming response
app.post('/api/chat/stream', async (c) => {
  const { message } = await c.req.json();

  const stream = await c.env.AI.run('@cf/meta/llama-3.1-8b-instruct', {
    messages: [{ role: 'user', content: message }],
    stream: true
  });

  return new Response(stream, {
    headers: { 'Content-Type': 'text/event-stream' }
  });
});
```

### Validation with Zod

```typescript
import { zValidator } from '@hono/zod-validator';
import { z } from 'zod';

const createUserSchema = z.object({
  name: z.string().min(1),
  email: z.string().email(),
  age: z.number().positive().optional(),
});

app.post('/api/users',
  zValidator('json', createUserSchema),
  async (c) => {
    const user = c.req.valid('json');
    // user is typed and validated
    return c.json({ id: '123', ...user }, 201);
  }
);
```

## itty-router

### Why itty-router

- Extremely lightweight (~1KB)
- Dead simple API
- No build step required
- Good for simple APIs
- Easy to understand source code

### Basic Setup

```typescript
import { Router } from 'itty-router';

interface Env {
  DATABASE: D1Database;
}

const router = Router();

router.get('/', () => new Response('Hello!'));

router.get('/api/users', async (request, env: Env) => {
  const users = await env.DATABASE
    .prepare('SELECT * FROM users')
    .all();
  return Response.json(users.results);
});

router.post('/api/users', async (request, env: Env) => {
  const body = await request.json();
  // Create user
  return Response.json({ id: '123', ...body }, { status: 201 });
});

// 404 fallback
router.all('*', () => new Response('Not Found', { status: 404 }));

export default {
  fetch: (request: Request, env: Env, ctx: ExecutionContext) =>
    router.handle(request, env, ctx)
};
```

### With Middleware Pattern

```typescript
import { Router } from 'itty-router';

const router = Router();

// Simple auth middleware
const withAuth = async (request: Request, env: Env) => {
  const token = request.headers.get('Authorization')?.replace('Bearer ', '');
  if (!token || token !== env.API_KEY) {
    return new Response('Unauthorized', { status: 401 });
  }
  // Don't return anything to continue to next handler
};

// Apply middleware to routes
router.get('/api/*', withAuth);
router.get('/api/data', (request, env) => Response.json({ data: 'secret' }));
```

### Route Parameters

```typescript
router.get('/api/users/:id', async (request, env) => {
  const { id } = request.params;
  const user = await env.DATABASE
    .prepare('SELECT * FROM users WHERE id = ?')
    .bind(id)
    .first();

  if (!user) {
    return new Response('Not Found', { status: 404 });
  }

  return Response.json(user);
});

// Optional parameters
router.get('/api/posts/:id?', (request) => {
  const { id } = request.params;
  if (id) {
    return Response.json({ post: id });
  }
  return Response.json({ posts: [] });
});
```

## Choosing Between Them

### Choose Hono When

- Building a substantial API (>10 endpoints)
- Need built-in middleware (CORS, auth, validation)
- Want excellent TypeScript integration
- Team comes from Express/Fastify background
- Building something that will grow

### Choose itty-router When

- Simple API with few endpoints
- Bundle size is critical
- Want minimal abstraction
- Quick prototype or proof of concept
- Learning Workers fundamentals

### Choose Vanilla When

- Single-purpose Worker (proxy, redirect, etc.)
- Maximum control needed
- Zero dependencies required
- Edge case the frameworks don't handle well

## Vanilla Fetch Handler Pattern

For comparison, here's the vanilla approach:

```typescript
interface Env {
  DATABASE: D1Database;
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);
    const path = url.pathname;
    const method = request.method;

    // Manual routing
    if (path === '/' && method === 'GET') {
      return new Response('Hello!');
    }

    if (path === '/api/users' && method === 'GET') {
      const users = await env.DATABASE
        .prepare('SELECT * FROM users')
        .all();
      return Response.json(users.results);
    }

    if (path.match(/^\/api\/users\/[\w-]+$/) && method === 'GET') {
      const id = path.split('/').pop();
      const user = await env.DATABASE
        .prepare('SELECT * FROM users WHERE id = ?')
        .bind(id)
        .first();

      if (!user) {
        return new Response('Not Found', { status: 404 });
      }
      return Response.json(user);
    }

    return new Response('Not Found', { status: 404 });
  }
};
```

## Migration Patterns

### From Vanilla to Hono

```typescript
// Before (vanilla)
export default {
  async fetch(request: Request, env: Env) {
    if (request.method === 'GET' && new URL(request.url).pathname === '/') {
      return new Response('Hello');
    }
    return new Response('Not Found', { status: 404 });
  }
};

// After (Hono)
import { Hono } from 'hono';

const app = new Hono<{ Bindings: Env }>();
app.get('/', (c) => c.text('Hello'));
export default app;
```

### From itty-router to Hono

```typescript
// Before (itty-router)
import { Router } from 'itty-router';
const router = Router();
router.get('/api/users/:id', (req, env) => {
  const { id } = req.params;
  return Response.json({ id });
});

// After (Hono)
import { Hono } from 'hono';
const app = new Hono<{ Bindings: Env }>();
app.get('/api/users/:id', (c) => {
  const id = c.req.param('id');
  return c.json({ id });
});
```

## Best Practices

### Type Safety

Always type your bindings:
```typescript
type Bindings = {
  DATABASE: D1Database;
  CACHE: KVNamespace;
  AI: Ai;
};

const app = new Hono<{ Bindings: Bindings }>();
```

### Error Handling

Always have a global error handler:
```typescript
app.onError((err, c) => {
  console.error(err);
  return c.json({ error: 'Something went wrong' }, 500);
});
```

### CORS

Configure CORS appropriately:
```typescript
app.use('*', cors({
  origin: process.env.NODE_ENV === 'production'
    ? ['https://yourdomain.com']
    : ['http://localhost:3000'],
}));
```

### Logging

Add request logging in development:
```typescript
app.use('*', logger());  // Hono's built-in logger
```

## Additional Resources

- Hono documentation: https://hono.dev/
- itty-router: https://github.com/kwhitley/itty-router
- Use cloudflare-docs-specialist for Cloudflare-specific framework guidance
