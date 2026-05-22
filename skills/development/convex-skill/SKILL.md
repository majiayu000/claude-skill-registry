---
name: convex
description: 'Expert guidance for Convex backend development including queries, mutations, actions, schemas, authentication, scheduling, file storage, search, and Next.js integration. Use when working with Convex functions, database operations, convex/ directory code, or Next.js App Router with Convex. Triggers: convex functions, ctx.db, useQuery, useMutation, usePreloadedQuery, preloadQuery, fetchQuery, convex schema, convex auth, convex cron, convex actions, convex scheduling, ctx.storage, generateUploadUrl, file upload, storage.store, storage.getUrl, Id<"_storage">, ConvexProvider, ConvexClientProvider, db.system, _scheduled_functions, _storage system table, OCC, optimistic concurrency, transaction atomicity, schema evolution, searchIndex, vectorIndex, withSearchIndex, ctx.vectorSearch, full-text search, vector search, embeddings, RAG, semantic search, typeahead search, ConvexError, httpAction, httpRouter, CORS, webhook.'
---

# Convex Backend Development

## Core Architecture

Convex is a reactive database where queries are TypeScript functions. The sync engine (queries + mutations + database) is the heart of Convex — center your app around it.

### Function Types

| Type         | DB Access     | Deterministic | Cached/Reactive | Use For                    |
| ------------ | ------------- | ------------- | --------------- | -------------------------- |
| `query`      | Read only     | Yes           | Yes             | All reads, subscriptions   |
| `mutation`   | Read/Write    | Yes           | No              | All writes (transactions)  |
| `action`     | Via ctx.run\* | No            | No              | External APIs, LLMs, email |
| `httpAction` | Via ctx.run\* | No            | No              | Webhooks, custom HTTP      |

**Key rule**: Queries and mutations cannot make network requests. Actions cannot directly access the database.

## Project Structure (Best Practice)

```
convex/
├── _generated/         # Auto-generated types (commit this)
├── schema.ts           # Database schema
├── model/              # Helper functions (most logic lives here)
│   ├── users.ts
│   └── messages.ts
├── users.ts            # Thin wrappers exposing public API
├── messages.ts
├── crons.ts            # Cron job definitions
└── http.ts             # HTTP action routes
```

## Essential Patterns

### 1. Function Structure

```typescript
// convex/messages.ts
import { query, mutation, internalMutation } from './_generated/server';
import { internal } from './_generated/api';
import { v } from 'convex/values';

// PUBLIC query with validators (always validate public functions)
export const list = query({
  args: { channelId: v.id('channels') },
  handler: async (ctx, { channelId }) => {
    return await ctx.db
      .query('messages')
      .withIndex('by_channel', (q) => q.eq('channelId', channelId))
      .order('desc')
      .take(50);
  }
});

// PUBLIC mutation with validators and auth check
export const send = mutation({
  args: { channelId: v.id('channels'), body: v.string() },
  handler: async (ctx, { channelId, body }) => {
    const user = await ctx.auth.getUserIdentity();
    if (!user) throw new Error('Unauthorized');

    await ctx.db.insert('messages', {
      channelId,
      body,
      authorId: user.subject
    });
  }
});

// INTERNAL mutation (for scheduling, crons, actions)
export const deleteOld = internalMutation({
  args: { before: v.number() },
  handler: async (ctx, { before }) => {
    const old = await ctx.db
      .query('messages')
      .withIndex('by_createdAt', (q) => q.lt('_creationTime', before))
      .take(100);
    for (const msg of old) {
      await ctx.db.delete(msg._id);
    }
  }
});
```

### 2. Helper Functions Pattern

Most logic should live in helper functions, NOT in query/mutation handlers:

```typescript
// convex/model/users.ts
import { QueryCtx, MutationCtx } from '../_generated/server';
import { Doc } from '../_generated/dataModel';

export async function getCurrentUser(
  ctx: QueryCtx
): Promise<Doc<'users'> | null> {
  const identity = await ctx.auth.getUserIdentity();
  if (!identity) return null;

  return await ctx.db
    .query('users')
    .withIndex('by_tokenIdentifier', (q) =>
      q.eq('tokenIdentifier', identity.tokenIdentifier)
    )
    .unique();
}

export async function requireUser(ctx: QueryCtx): Promise<Doc<'users'>> {
  const user = await getCurrentUser(ctx);
  if (!user) throw new Error('Unauthorized');
  return user;
}
```

### 3. Actions with Scheduling

```typescript
// convex/ai.ts
import { action, internalMutation } from './_generated/server';
import { internal } from './_generated/api';
import { v } from 'convex/values';

export const summarize = action({
  args: { documentId: v.id('documents') },
  handler: async (ctx, { documentId }) => {
    // Read data via internal query
    const doc = await ctx.runQuery(internal.documents.get, { documentId });

    // Call external API
    const response = await fetch('https://api.openai.com/v1/...', {...});
    const summary = await response.json();

    // Write result via internal mutation
    await ctx.runMutation(internal.documents.setSummary, {
      documentId,
      summary: summary.text
    });
  }
});

// Trigger action from mutation (not directly from client)
export const requestSummary = mutation({
  args: { documentId: v.id('documents') },
  handler: async (ctx, { documentId }) => {
    const user = await ctx.auth.getUserIdentity();
    if (!user) throw new Error('Unauthorized');

    await ctx.db.patch(documentId, { status: 'processing' });

    // Schedule action (runs after mutation commits)
    await ctx.scheduler.runAfter(0, internal.ai.summarizeInternal, {
      documentId
    });
  }
});
```

### 4. Application Errors

```typescript
import { ConvexError } from 'convex/values';

export const assignRole = mutation({
  args: { roleId: v.id('roles'), userId: v.id('users') },
  handler: async (ctx, { roleId, userId }) => {
    const existing = await ctx.db
      .query('assignments')
      .withIndex('by_role', (q) => q.eq('roleId', roleId))
      .first();

    if (existing) {
      throw new ConvexError({
        code: 'ROLE_TAKEN',
        message: 'Role is already assigned'
      });
    }

    await ctx.db.insert('assignments', { roleId, userId });
  }
});
```

## Critical Rules

### DO ✅

- Use `internal.` functions for all `ctx.run*`, `ctx.scheduler`, and crons
- Always validate args for public functions with `v.*` validators
- Always check auth in public functions: `ctx.auth.getUserIdentity()`
- Use indexes with `.withIndex()` instead of `.filter()`
- Await all promises (enable `no-floating-promises` ESLint rule)
- Keep actions small — put logic in queries/mutations
- Batch database operations in single mutations
- Use `ConvexError` for user-facing errors

### DON'T ❌

- Don't use `api.` functions for scheduling (use `internal.`)
- Don't use `.filter()` on queries — use indexes or TypeScript filter
- Don't use `.collect()` on unbounded queries (use `.take()` or pagination)
- Don't use `Date.now()` in queries (breaks caching)
- Don't call actions directly from client (trigger via mutation + scheduler)
- Don't make sequential `ctx.runQuery/runMutation` calls in actions (batch them)
- Don't use `ctx.runAction` unless switching runtimes (use helper functions)

## Reference Guides

For detailed patterns, see:

- [FUNCTIONS.md](references/FUNCTIONS.md) — Queries, mutations, actions, internal functions
- [VALIDATION.md](references/VALIDATION.md) — Argument validation, extended validators
- [ERROR_HANDLING.md](references/ERROR_HANDLING.md) — ConvexError, application errors
- [HTTP_ACTIONS.md](references/HTTP_ACTIONS.md) — HTTP actions, CORS, webhooks
- [RUNTIMES.md](references/RUNTIMES.md) — Default vs Node.js runtime, bundling, debugging
- [DATABASE.md](references/DATABASE.md) — Schema, indexes, reading/writing data
- [SEARCH.md](references/SEARCH.md) — Full-text search, vector search, RAG patterns
- [ADVANCED.md](references/ADVANCED.md) — System tables, schema philosophy, OCC
- [AUTH.md](references/AUTH.md) — Row-level security, Convex Auth (first-party)
- [SCHEDULING.md](references/SCHEDULING.md) — Crons, scheduled functions, workflows
- [FILE_STORAGE.md](references/FILE_STORAGE.md) — Upload, store, serve, delete files
- [NEXTJS.md](references/NEXTJS.md) — Next.js App Router, SSR, Server Actions

**Auth Provider Skills** (add to project as needed):

- `convex-auth` — Universal auth patterns, storing users, debugging
- `convex-clerk` — Clerk setup, webhooks, JWT configuration
- `convex-workos` — WorkOS AuthKit setup, auto-provisioning
