---
name: hono
description: Builds APIs with Hono including routing, middleware, validation, and edge deployment. Use when creating fast APIs, building edge functions, or developing serverless applications.
---

# Hono

Ultrafast web framework for the edge, built on Web Standards.

## Quick Start

**Install:**
```bash
npm install hono
```

**Create project:**
```bash
npm create hono@latest my-app
```

## Basic Server

```typescript
// src/index.ts
import { Hono } from 'hono';

const app = new Hono();

app.get('/', (c) => {
  return c.text('Hello Hono!');
});

app.get('/json', (c) => {
  return c.json({ message: 'Hello' });
});

export default app;
```

## Routing

### Basic Routes

```typescript
import { Hono } from 'hono';

const app = new Hono();

// HTTP methods
app.get('/users', (c) => c.json({ users: [] }));
app.post('/users', (c) => c.json({ created: true }));
app.put('/users/:id', (c) => c.json({ updated: true }));
app.delete('/users/:id', (c) => c.json({ deleted: true }));
app.patch('/users/:id', (c) => c.json({ patched: true }));

// All methods
app.all('/any', (c) => c.text('Any method'));
```

### Path Parameters

```typescript
app.get('/users/:id', (c) => {
  const id = c.req.param('id');
  return c.json({ id });
});

// Multiple params
app.get('/posts/:postId/comments/:commentId', (c) => {
  const { postId, commentId } = c.req.param();
  return c.json({ postId, commentId });
});

// Optional params
app.get('/posts/:id?', (c) => {
  const id = c.req.param('id');
  return c.json({ id: id || 'all' });
});

// Wildcard
app.get('/files/*', (c) => {
  const path = c.req.path;
  return c.text(`File: ${path}`);
});
```

### Query Parameters

```typescript
app.get('/search', (c) => {
  const query = c.req.query('q');
  const page = c.req.query('page') || '1';

  // Multiple values
  const tags = c.req.queries('tags');

  return c.json({ query, page, tags });
});
```

### Route Groups

```typescript
const app = new Hono();

// Group routes
const api = new Hono();
api.get('/users', (c) => c.json({ users: [] }));
api.get('/posts', (c) => c.json({ posts: [] }));

app.route('/api/v1', api);

// Chaining
app.basePath('/api').get('/users', (c) => c.json([]));
```

## Request Handling

### Request Body

```typescript
// JSON body
app.post('/users', async (c) => {
  const body = await c.req.json();
  return c.json(body);
});

// Form data
app.post('/upload', async (c) => {
  const formData = await c.req.formData();
  const name = formData.get('name');
  return c.text(`Name: ${name}`);
});

// Text body
app.post('/text', async (c) => {
  const text = await c.req.text();
  return c.text(text);
});

// Array buffer
app.post('/binary', async (c) => {
  const buffer = await c.req.arrayBuffer();
  return c.text(`Size: ${buffer.byteLength}`);
});
```

### Headers

```typescript
app.get('/headers', (c) => {
  const auth = c.req.header('Authorization');
  const contentType = c.req.header('Content-Type');

  return c.json({ auth, contentType });
});
```

## Response

### Response Types

```typescript
// Text
app.get('/text', (c) => c.text('Hello'));

// JSON
app.get('/json', (c) => c.json({ message: 'Hello' }));

// HTML
app.get('/html', (c) => c.html('<h1>Hello</h1>'));

// Redirect
app.get('/redirect', (c) => c.redirect('/new-path'));

// Custom status
app.get('/error', (c) => {
  return c.json({ error: 'Not found' }, 404);
});

// With headers
app.get('/custom', (c) => {
  return c.json(
    { data: 'value' },
    200,
    { 'X-Custom-Header': 'value' }
  );
});
```

### Streaming

```typescript
import { streamText } from 'hono/streaming';

app.get('/stream', (c) => {
  return streamText(c, async (stream) => {
    for (let i = 0; i < 5; i++) {
      await stream.write(`data: ${i}\n`);
      await stream.sleep(1000);
    }
  });
});
```

## Middleware

### Built-in Middleware

```typescript
import { Hono } from 'hono';
import { cors } from 'hono/cors';
import { logger } from 'hono/logger';
import { prettyJSON } from 'hono/pretty-json';
import { secureHeaders } from 'hono/secure-headers';
import { compress } from 'hono/compress';
import { etag } from 'hono/etag';

const app = new Hono();

app.use('*', logger());
app.use('*', cors());
app.use('*', prettyJSON());
app.use('*', secureHeaders());
app.use('*', compress());
app.use('*', etag());
```

### Custom Middleware

```typescript
import { Hono, Context, Next } from 'hono';

// Simple middleware
const timing = async (c: Context, next: Next) => {
  const start = Date.now();
  await next();
  const ms = Date.now() - start;
  c.header('X-Response-Time', `${ms}ms`);
};

app.use('*', timing);

// Middleware with options
const auth = (secret: string) => {
  return async (c: Context, next: Next) => {
    const token = c.req.header('Authorization');

    if (token !== `Bearer ${secret}`) {
      return c.json({ error: 'Unauthorized' }, 401);
    }

    await next();
  };
};

app.use('/api/*', auth('my-secret'));
```

### Route-specific Middleware

```typescript
app.get('/protected', auth('secret'), (c) => {
  return c.json({ protected: true });
});

// Multiple middleware
app.post('/data', logger(), auth('secret'), validate(), (c) => {
  return c.json({ success: true });
});
```

## Validation

### Zod Validator

```bash
npm install @hono/zod-validator
```

```typescript
import { Hono } from 'hono';
import { zValidator } from '@hono/zod-validator';
import { z } from 'zod';

const app = new Hono();

const userSchema = z.object({
  name: z.string().min(1),
  email: z.string().email(),
  age: z.number().min(0).optional(),
});

app.post(
  '/users',
  zValidator('json', userSchema),
  (c) => {
    const user = c.req.valid('json');
    return c.json({ user });
  }
);

// Query validation
const querySchema = z.object({
  page: z.string().transform(Number).default('1'),
  limit: z.string().transform(Number).default('10'),
});

app.get(
  '/users',
  zValidator('query', querySchema),
  (c) => {
    const { page, limit } = c.req.valid('query');
    return c.json({ page, limit });
  }
);

// Param validation
const paramSchema = z.object({
  id: z.string().uuid(),
});

app.get(
  '/users/:id',
  zValidator('param', paramSchema),
  (c) => {
    const { id } = c.req.valid('param');
    return c.json({ id });
  }
);
```

## Context Variables

```typescript
import { Hono } from 'hono';

type Variables = {
  user: { id: string; name: string };
};

const app = new Hono<{ Variables: Variables }>();

// Set variable in middleware
app.use('*', async (c, next) => {
  c.set('user', { id: '123', name: 'John' });
  await next();
});

// Access in handler
app.get('/me', (c) => {
  const user = c.get('user');
  return c.json(user);
});
```

## Error Handling

```typescript
import { Hono, HTTPException } from 'hono';

const app = new Hono();

// Throw HTTP exception
app.get('/error', (c) => {
  throw new HTTPException(404, { message: 'Not found' });
});

// Global error handler
app.onError((err, c) => {
  if (err instanceof HTTPException) {
    return c.json({ error: err.message }, err.status);
  }

  console.error(err);
  return c.json({ error: 'Internal Server Error' }, 500);
});

// Not found handler
app.notFound((c) => {
  return c.json({ error: 'Not Found' }, 404);
});
```

## RPC Mode

```typescript
// server.ts
import { Hono } from 'hono';
import { zValidator } from '@hono/zod-validator';
import { z } from 'zod';

const app = new Hono()
  .get('/users', (c) => {
    return c.json([{ id: 1, name: 'John' }]);
  })
  .post(
    '/users',
    zValidator('json', z.object({ name: z.string() })),
    (c) => {
      const { name } = c.req.valid('json');
      return c.json({ id: 2, name });
    }
  );

export type AppType = typeof app;
export default app;

// client.ts
import { hc } from 'hono/client';
import type { AppType } from './server';

const client = hc<AppType>('http://localhost:3000');

// Type-safe client calls
const users = await client.users.$get();
const data = await users.json();

const newUser = await client.users.$post({
  json: { name: 'Jane' },
});
```

## Deployment

### Cloudflare Workers

```typescript
// src/index.ts
import { Hono } from 'hono';

type Bindings = {
  KV: KVNamespace;
  DB: D1Database;
};

const app = new Hono<{ Bindings: Bindings }>();

app.get('/kv/:key', async (c) => {
  const key = c.req.param('key');
  const value = await c.env.KV.get(key);
  return c.json({ value });
});

export default app;
```

### Vercel

```typescript
// api/index.ts
import { Hono } from 'hono';
import { handle } from 'hono/vercel';

const app = new Hono().basePath('/api');

app.get('/hello', (c) => c.json({ message: 'Hello from Vercel' }));

export const GET = handle(app);
export const POST = handle(app);
```

### Node.js

```typescript
import { serve } from '@hono/node-server';
import { Hono } from 'hono';

const app = new Hono();

app.get('/', (c) => c.text('Hello Node.js!'));

serve({
  fetch: app.fetch,
  port: 3000,
});
```

### Bun

```typescript
import { Hono } from 'hono';

const app = new Hono();

app.get('/', (c) => c.text('Hello Bun!'));

export default {
  port: 3000,
  fetch: app.fetch,
};
```

## JSX

```tsx
import { Hono } from 'hono';
import { html } from 'hono/html';

const app = new Hono();

const Layout = ({ children }: { children: any }) => html`
  <!DOCTYPE html>
  <html>
    <head>
      <title>My App</title>
    </head>
    <body>
      ${children}
    </body>
  </html>
`;

app.get('/', (c) => {
  return c.html(
    <Layout>
      <h1>Hello, World!</h1>
    </Layout>
  );
});
```

## Best Practices

1. **Use validators** - Validate all inputs
2. **Type your bindings** - For edge environments
3. **Handle errors globally** - Use onError
4. **Use middleware** - Reusable logic
5. **Export types for RPC** - Type-safe clients

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Forgetting async | Use async/await for body |
| Wrong content type | Use c.json(), c.text() etc. |
| Missing error handling | Add onError handler |
| Not validating | Use zValidator |
| Blocking event loop | Keep handlers fast |

## Reference Files

- [references/middleware.md](references/middleware.md) - Middleware patterns
- [references/deployment.md](references/deployment.md) - Platform guides
- [references/rpc.md](references/rpc.md) - RPC client setup
