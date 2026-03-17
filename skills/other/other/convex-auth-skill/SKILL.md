---
name: convex-auth
description: 'Core authentication patterns for Convex backends. Use when implementing auth checks in functions, storing users in database, creating auth helpers, or debugging auth issues. Works with any auth provider (Clerk, WorkOS, Auth0, etc.).'
---

# Convex Authentication - Core Patterns

This skill covers universal auth patterns that work with ANY authentication provider.

## Auth in Functions

Access the authenticated user via `ctx.auth.getUserIdentity()`:

```typescript
import { query, mutation, action } from './_generated/server';

export const myQuery = query({
  args: {},
  handler: async (ctx) => {
    const identity = await ctx.auth.getUserIdentity();
    if (identity === null) {
      throw new Error('Not authenticated');
    }
    // identity.tokenIdentifier - unique across providers
    // identity.subject - user ID from provider
    // identity.email, identity.name, etc. (if configured)
  }
});
```

### UserIdentity Fields

| Field             | Guaranteed         | Description                           |
| ----------------- | ------------------ | ------------------------------------- |
| `tokenIdentifier` | ✅                 | Unique ID (subject + issuer combined) |
| `subject`         | ✅                 | User ID from auth provider            |
| `issuer`          | ✅                 | Auth provider domain                  |
| `email`           | Provider-dependent | User's email                          |
| `name`            | Provider-dependent | Display name                          |
| `pictureUrl`      | Provider-dependent | Avatar URL                            |

## Critical: Race Condition Prevention

**Problem:** Queries can execute before auth is validated on page load.

**Client-side:** Always use `useConvexAuth()` from `convex/react`, NOT your provider's hook:

```typescript
// ✅ Correct - waits for Convex to validate token
import { useConvexAuth } from 'convex/react';
const { isLoading, isAuthenticated } = useConvexAuth();

// ❌ Wrong - only checks provider, not Convex validation
const { isSignedIn } = useAuth(); // from @clerk/clerk-react
```

**Skip queries until authenticated:**

```typescript
const user = useQuery(api.users.current, isAuthenticated ? {} : 'skip');
```

**Use Convex auth components:**

```typescript
import { Authenticated, Unauthenticated, AuthLoading } from "convex/react";

<Authenticated>
  <Content /> {/* Queries here are safe */}
</Authenticated>
<Unauthenticated>
  <SignInButton />
</Unauthenticated>
```

## Storing Users in Database

See [USERS.md](references/USERS.md) for complete patterns including:

- Schema design with indexes
- Storing users via client mutation
- Storing users via webhooks (recommended for production)
- Helper functions for user lookup

## Custom Auth Wrappers

Create authenticated function wrappers using `convex-helpers`:

```typescript
// convex/lib/auth.ts
import {
  query,
  mutation,
  action,
  QueryCtx,
  MutationCtx,
  ActionCtx
} from './_generated/server';
import {
  customQuery,
  customMutation,
  customAction,
  customCtx
} from 'convex-helpers/server/customFunctions';
import { ConvexError } from 'convex/values';

async function requireAuth(ctx: QueryCtx | MutationCtx | ActionCtx) {
  const identity = await ctx.auth.getUserIdentity();
  if (!identity) {
    throw new ConvexError('Not authenticated');
  }
  return identity;
}

export const authQuery = customQuery(
  query,
  customCtx(async (ctx) => {
    const identity = await requireAuth(ctx);
    return { identity };
  })
);

export const authMutation = customMutation(
  mutation,
  customCtx(async (ctx) => {
    const identity = await requireAuth(ctx);
    return { identity };
  })
);

export const authAction = customAction(
  action,
  customCtx(async (ctx) => {
    const identity = await requireAuth(ctx);
    return { identity };
  })
);
```

**Usage:**

```typescript
import { authQuery } from './lib/auth';

export const myProtectedQuery = authQuery({
  args: {},
  handler: async (ctx) => {
    // ctx.identity is guaranteed to exist
    const userId = ctx.identity.subject;
  }
});
```

## HTTP Actions with Auth

Pass JWT in Authorization header:

```typescript
// Client
fetch('https://your-deployment.convex.site/api/endpoint', {
  headers: { Authorization: `Bearer ${jwtToken}` }
});

// convex/http.ts
import { httpAction } from './_generated/server';

export const myEndpoint = httpAction(async (ctx, request) => {
  const identity = await ctx.auth.getUserIdentity();
  if (!identity) {
    return new Response('Unauthorized', { status: 401 });
  }
  // ...
});
```

## Debugging Checklist

See [DEBUG.md](references/DEBUG.md) for detailed troubleshooting steps.

**Quick checks:**

1. `ctx.auth.getUserIdentity()` returns `null`?
   - Check if query runs before auth completes (use `"skip"` pattern)
   - Check auth.config.ts is deployed (`npx convex dev`)
2. Check Settings > Authentication in Convex Dashboard
3. Verify JWT token at https://jwt.io - check `iss` and `aud` fields
4. Ensure `domain` in auth.config.ts matches JWT `iss`
5. Ensure `applicationID` matches JWT `aud`

## DO ✅

- Always check `ctx.auth.getUserIdentity()` in public functions
- Use `useConvexAuth()` hook, not provider's auth hook
- Skip queries with `"skip"` until authenticated
- Use `<Authenticated>` component to gate protected content
- Store users in DB for cross-user queries
- Use `tokenIdentifier` or `subject` as unique user key

## DON'T ❌

- Trust client-side auth alone (Convex is a public API)
- Run queries before checking `isAuthenticated`
- Use `.filter()` to find users by token (use index)
- Assume identity fields exist (check provider config)
- Forget to redeploy after changing auth.config.ts
