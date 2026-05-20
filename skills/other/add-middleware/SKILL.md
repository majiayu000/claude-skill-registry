---
name: add-middleware
description: Create Hono middleware with test file for the API server
---

# Add Middleware Skill

Create a new Hono middleware for the x4-mono API server.

## Arguments

The user describes the middleware. If unclear, ask for:

- Middleware name (camelCase, e.g., `requestSizeLimit`)
- What it should do
- Where in the chain it belongs (before/after auth, rate limiting, etc.)
- Which routes it applies to (`'*'`, `/trpc/*`, `/api/auth/*`, etc.)

## File Locations

- **Middleware**: `apps/api/src/middleware/{name}.ts`
- **Registration**: `apps/api/src/app.ts`
- **Tests**: `apps/api/src/__tests__/{name}.test.ts`

## Middleware Template

Reference: `apps/api/src/middleware/rateLimit.ts`

```typescript
import type { MiddlewareHandler } from 'hono';
import { apiLogger } from '../lib/logger';

export interface MyMiddlewareOptions {
  // Configuration options
}

export function myMiddleware(options: MyMiddlewareOptions): MiddlewareHandler {
  return async (c, next) => {
    try {
      // Pre-processing logic
      // Access request: c.req.raw, c.req.header('X-Custom')
      // Access context: c.get('requestId')
      // Set headers: c.header('X-Custom', 'value')

      await next();

      // Post-processing logic (after route handler)
    } catch (error) {
      apiLogger.warn({ error }, 'middleware-name: error description');
      // Fail-open for non-security middleware:
      await next();
      // OR fail-closed for security middleware:
      // return c.json({ error: 'Forbidden' }, 403);
    }
  };
}
```

## Middleware Chain Order

New middleware must be inserted at the correct position:

```
1. requestLogger  → generates requestId, logs all requests
2. CORS           → per route group (/trpc/*, /api/auth/*)
3. rate limiting  → per route group, different tiers
4. auth           → Better Auth handler for /api/auth/**
5. route-specific → custom middleware for specific paths
```

## Registration in app.ts

```typescript
import { myMiddleware } from './middleware/myMiddleware';

// Insert at correct position in the chain
app.use(
  '/trpc/*',
  myMiddleware({
    /* options */
  }),
);
```

## Test Template

```typescript
import { describe, test, expect } from 'bun:test';
import app from '../app';

describe('myMiddleware', () => {
  test('allows valid requests', async () => {
    const res = await app.request('/trpc/health', {
      method: 'GET',
    });
    expect(res.status).toBe(200);
  });

  test('blocks invalid requests', async () => {
    const res = await app.request('/trpc/something', {
      method: 'POST',
      headers: {
        /* trigger rejection */
      },
    });
    expect(res.status).toBe(403);
  });
});
```

## Patterns

- **Fail-open**: Non-critical middleware (metrics, analytics) should `await next()` on error
- **Fail-closed**: Security middleware should return an error response on failure
- **Lazy init**: Cache expensive resources at module scope, initialize on first call
- **Structured logging**: Use `apiLogger.warn({ ... }, 'message')` — never `console.log`

## Workflow

1. Read `apps/api/src/app.ts` to understand current middleware chain
2. Create middleware file at `apps/api/src/middleware/{name}.ts`
3. Register in `apps/api/src/app.ts` at the correct position
4. Create test file at `apps/api/src/__tests__/{name}.test.ts`
5. Run `bun test --cwd apps/api` to verify
6. Run `bun turbo type-check` to verify
