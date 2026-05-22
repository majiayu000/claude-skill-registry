---
name: innozverse-api-style
description: Follow API development conventions including RESTful design, Fastify patterns, Zod validation, error handling, and versioning. Use when building API endpoints, adding routes, or working with API code.
---

# innozverse API Development Style

When developing API endpoints for innozverse, follow these patterns and conventions.

## Fastify Basics

### Route Registration
```typescript
// apps/api/src/routes/v1/users.ts
import { FastifyInstance } from 'fastify';

export async function usersRoutes(fastify: FastifyInstance) {
  fastify.get('/users', async (request, reply) => {
    return { users: [] };
  });

  fastify.get('/users/:id', async (request, reply) => {
    const { id } = request.params as { id: string };
    return { user: { id } };
  });

  fastify.post('/users', async (request, reply) => {
    const body = request.body;
    return reply.code(201).send({ user: body });
  });
}
```

### Register in Index
```typescript
// apps/api/src/index.ts
import { usersRoutes } from './routes/v1/users';

fastify.register(usersRoutes, { prefix: '/v1' });
```

## Response Patterns

### Success Response
```typescript
return reply.code(200).send({
  status: 'ok',
  data: { /* ... */ }
});
```

### Created Response
```typescript
return reply.code(201).send({
  status: 'created',
  data: { id: newId }
});
```

### Error Response
```typescript
return reply.code(400).send({
  error: 'ValidationError',
  message: 'Invalid input',
  statusCode: 400
});
```

## Type Safety

### Define Types in @innozverse/shared
```typescript
// packages/shared/src/types.ts
export interface User {
  id: string;
  name: string;
  email: string;
}

export interface UserResponse {
  status: 'ok';
  data: User;
}
```

### Use in API
```typescript
import { User, UserResponse } from '@innozverse/shared';

fastify.get<{ Reply: UserResponse }>('/users/:id', async (request, reply) => {
  const user: User = { /* ... */ };
  return reply.send({
    status: 'ok',
    data: user
  });
});
```

## Validation with Zod

### Define Schema in @innozverse/shared
```typescript
// packages/shared/src/schemas.ts
import { z } from 'zod';

export const userSchema = z.object({
  name: z.string().min(1),
  email: z.string().email()
});
```

### Use in API
```typescript
import { userSchema } from '@innozverse/shared';

fastify.post('/users', async (request, reply) => {
  try {
    const validated = userSchema.parse(request.body);
    // Use validated data
    return reply.code(201).send({ data: validated });
  } catch (error) {
    return reply.code(400).send({
      error: 'ValidationError',
      message: error.message
    });
  }
});
```

## Error Handling

### Global Error Handler
```typescript
// apps/api/src/index.ts
fastify.setErrorHandler((error, request, reply) => {
  fastify.log.error(error);

  reply.status(error.statusCode || 500).send({
    error: error.name || 'InternalServerError',
    message: error.message || 'Something went wrong',
    statusCode: error.statusCode || 500
  });
});
```

### Throwing Errors
```typescript
fastify.get('/users/:id', async (request, reply) => {
  const user = await findUser(id);

  if (!user) {
    return reply.code(404).send({
      error: 'NotFound',
      message: 'User not found',
      statusCode: 404
    });
  }

  return { data: user };
});
```

## Async/Await

Always use async/await, never callbacks:
```typescript
// ✅ Good
fastify.get('/users', async (request, reply) => {
  const users = await getUsers();
  return { users };
});

// ❌ Bad
fastify.get('/users', (request, reply) => {
  getUsers((err, users) => {
    reply.send({ users });
  });
});
```

## RESTful Conventions

### Resource Naming
- Plural nouns: `/users`, `/posts`
- Nested resources: `/users/:userId/posts`

### HTTP Methods
- `GET /resource` - List all
- `GET /resource/:id` - Get one
- `POST /resource` - Create
- `PUT /resource/:id` - Replace
- `PATCH /resource/:id` - Update
- `DELETE /resource/:id` - Delete

### Status Codes
- `200` - Success (GET, PUT, PATCH, DELETE)
- `201` - Created (POST)
- `204` - No Content (DELETE)
- `400` - Bad Request (validation error)
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `409` - Conflict (duplicate)
- `500` - Internal Server Error

## Versioning

Always version API routes:
```typescript
// ✅ Good
fastify.register(v1Routes, { prefix: '/v1' });
fastify.register(v2Routes, { prefix: '/v2' });

// ❌ Bad
fastify.register(routes); // No version
```

## CORS Configuration

```typescript
import cors from '@fastify/cors';

await fastify.register(cors, {
  origin: process.env.CORS_ORIGIN || '*',
  credentials: true
});
```

## Environment Variables

```typescript
const PORT = parseInt(process.env.PORT || '8080', 10);
const NODE_ENV = process.env.NODE_ENV || 'development';

// Never hardcode secrets
const DB_URL = process.env.DATABASE_URL; // ✅
const API_KEY = process.env.API_KEY; // ✅
```

## Logging

```typescript
// Use Fastify's built-in logger
fastify.log.info('Server starting');
fastify.log.error({ err: error }, 'Error occurred');
fastify.log.debug({ data }, 'Debug info');
```

## Health Check

Always maintain a health check endpoint:
```typescript
fastify.get('/health', async () => ({
  status: 'ok',
  timestamp: new Date().toISOString(),
  version: process.env.API_VERSION || '1.0.0'
}));
```

## Testing (Future)

```typescript
// apps/api/src/routes/__tests__/users.test.ts
import { buildServer } from '../../index';

describe('Users API', () => {
  let fastify;

  beforeAll(async () => {
    fastify = await buildServer();
  });

  afterAll(async () => {
    await fastify.close();
  });

  test('GET /v1/users returns users list', async () => {
    const response = await fastify.inject({
      method: 'GET',
      url: '/v1/users'
    });

    expect(response.statusCode).toBe(200);
    expect(response.json()).toHaveProperty('users');
  });
});
```

## Database Patterns (Future)

When adding database:
```typescript
// Use a connection pool
import { Pool } from 'pg';

const pool = new Pool({
  connectionString: process.env.DATABASE_URL
});

// Close connections gracefully
fastify.addHook('onClose', async () => {
  await pool.end();
});

// Use in routes
fastify.get('/users/:id', async (request, reply) => {
  const { rows } = await pool.query(
    'SELECT * FROM users WHERE id = $1',
    [request.params.id]
  );

  if (rows.length === 0) {
    return reply.code(404).send({ error: 'Not found' });
  }

  return { data: rows[0] };
});
```

## Best Practices

### Single Responsibility
Each route file handles one resource:
```
routes/v1/
├── users.ts      # User management
├── posts.ts      # Post management
└── comments.ts   # Comment management
```

### DRY Principles
Extract common logic:
```typescript
// utils/auth.ts
export async function requireAuth(request, reply) {
  const token = request.headers.authorization;
  if (!token) {
    return reply.code(401).send({ error: 'Unauthorized' });
  }
  // Verify token
}

// routes/v1/users.ts
fastify.get('/users/me', {
  preHandler: requireAuth
}, async (request, reply) => {
  return { user: request.user };
});
```

### Graceful Shutdown
```typescript
process.on('SIGTERM', async () => {
  await fastify.close();
  process.exit(0);
});
```

## Anti-Patterns to Avoid

❌ Don't use `any` types:
```typescript
// Bad
fastify.get('/users', async (request: any, reply: any) => {
```

❌ Don't block the event loop:
```typescript
// Bad
fastify.get('/heavy', async () => {
  let result = 0;
  for (let i = 0; i < 1000000000; i++) {
    result += i;
  }
  return { result };
});
```

❌ Don't ignore errors:
```typescript
// Bad
fastify.get('/users', async () => {
  const users = await getUsers().catch(() => []);
  return { users };
});
```

❌ Don't expose internal errors to clients:
```typescript
// Bad
return reply.code(500).send({ error: error.stack });

// Good
fastify.log.error(error);
return reply.code(500).send({ error: 'Internal Server Error' });
```

## References

- [Fastify Documentation](https://www.fastify.io/)
- [Zod Documentation](https://zod.dev/)
- [RESTful API Design](https://restfulapi.net/)
