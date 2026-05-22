---
name: clerk-hono
description: Use Clerk auth in Hono apps via @hono/clerk-auth. Use when adding or changing Clerk authentication, protecting routes, or reading userId/orgId in Hono.
---

Source: [honojs/middleware - packages/clerk-auth](https://github.com/honojs/middleware/tree/main/packages/clerk-auth)

## Setup

- **Install**: `pnpm add @hono/clerk-auth` (or npm). No custom auth middleware - use the package directly.
- **Env**: `CLERK_SECRET_KEY`, `CLERK_PUBLISHABLE_KEY` (e.g. in wrangler or `.dev.vars`).

## Usage

Apply middleware to the routes that need auth, then use `getAuth(c)` in handlers:

```ts
import { clerkMiddleware, getAuth } from '@hono/clerk-auth';
import { Hono } from 'hono';

const app = new Hono();
app.use('/push/*', clerkMiddleware());
app.use('/orgs/*', clerkMiddleware());
app.route('/', sessionRouter);
```

In route handlers:

```ts
app.get('/', (c) => {
  const { userId, orgId } = getAuth(c);
  if (!userId) {
    return c.json({ message: 'You are not logged in.' }, 401);
  }
  if (!orgId) {
    return c.json({ message: 'No active organization selected.' }, 400);
  }
  return c.json({ userId, orgId });
});
```

- **Backend API**: `const clerkClient = c.get('clerk')` then e.g. `clerkClient.users.getUser(...)`.

## API keys

Use when the route is a resource server or machine-to-machine and should accept Clerk-issued API keys instead of (or in addition to) session tokens.

### Using API keys in requests

Once you have an API key, use it to authenticate requests to your application's API. Send the API key as a Bearer token in the `Authorization` header:

```ts
await fetch('https://your-api.com/users', {
  method: 'GET',
  headers: {
    'Content-Type': 'application/json',
    Authorization: `Bearer ${apiKey}`,
  },
});
```

On your backend, verify the API key using Clerk's SDK (e.g. @hono/clerk-auth with `getAuth(c, { acceptsToken: 'api_key' })`). See the [verifying API keys guide](https://clerk.com/docs/guides/development/verifying-api-keys) for framework-specific examples.

### Verifying API keys on the backend

By default `getAuth(c)` only accepts session tokens; API keys are rejected unless you pass `acceptsToken`.

- **Single token type** (API keys only):

```ts
const { userId } = getAuth(c, { acceptsToken: 'api_key' });
if (!userId) {
  return c.json({ error: 'Unauthorized' }, 401);
}
```

- **Multiple token types** (sessions + API keys):

```ts
const { userId, tokenType, scopes } = getAuth(c, {
  acceptsToken: ['session_token', 'oauth_token', 'api_key'],
});
if (!userId) {
  return c.json({ error: 'Unauthorized' }, 401);
}
// Optional: enforce scopes for api_key
if (tokenType === 'api_key' && !scopes?.includes('write:users')) {
  return c.json({ error: 'API key missing required scope' }, 403);
}
```

Clerk API keys are in beta; behavior may change. Full details: [Verify API keys (Clerk)](https://clerk.com/docs/guides/development/verifying-api-keys).

---

Do not add a custom `clerkAuthMiddleware` or re-export from a local `auth.ts`; import `clerkMiddleware` and `getAuth` from `@hono/clerk-auth` in app and routers.
