---
name: convex-tanstack
description: Comprehensive guide for building full-stack applications with Convex and TanStack Start. This skill should be used when working on projects that use Convex as the backend database with TanStack Start (React meta-framework). Covers schema design, queries, mutations, actions, authentication with Better Auth, routing, data fetching patterns, SSR, file storage, scheduling, AI agents, and frontend patterns. Use this when implementing features, debugging issues, or needing guidance on Convex + TanStack Start best practices.
---

# Convex + TanStack Start

## Overview

This skill provides guidance for building reactive, real-time full-stack applications using Convex (reactive backend-as-a-service) with TanStack Start (full-stack React meta-framework). The stack provides live-updating queries, type-safe end-to-end development, SSR support, and automatic cache invalidation.

## When to Use This Skill

- Implementing Convex queries, mutations, or actions
- Setting up or troubleshooting Better Auth authentication
- Configuring TanStack Router routes and loaders
- Writing schema definitions and indexes
- Implementing data fetching patterns (useQuery, useSuspenseQuery)
- Working with file storage, scheduling, or cron jobs
- Building AI agents with @convex-dev/agent
- Debugging SSR or hydration issues

## Quick Reference

### Essential Imports

```typescript
// Data fetching (always use cached version)
import { useQuery } from 'convex-helpers/react/cache'
import { useMutation, useAction } from 'convex/react'

// SSR with React Query
import { useSuspenseQuery } from '@tanstack/react-query'
import { convexQuery } from '@convex-dev/react-query'

// API and types
import { api } from '~/convex/_generated/api'
import type { Id, Doc } from '~/convex/_generated/dataModel'

// Backend functions
import { query, mutation, action } from "./_generated/server"
import { v } from "convex/values"
```

### The Skip Pattern

Never call hooks conditionally. Use `"skip"` instead:

```typescript
const user = useQuery(api.users.get, userId ? { userId } : "skip")
const org = useQuery(api.orgs.get, user?.orgId ? { orgId: user.orgId } : "skip")
```

### Three-State Query Handling

```typescript
if (data === undefined) return <Skeleton />  // Loading
if (data === null) return <NotFound />       // Not found
return <Content data={data} />               // Success
```

### Function Syntax (Always Include Returns Validator)

```typescript
export const getUser = query({
  args: { userId: v.id("users") },
  returns: v.union(
    v.object({ _id: v.id("users"), name: v.string() }),
    v.null()
  ),
  handler: async (ctx, args) => {
    return await ctx.db.get(args.userId)
  },
})
```

### Index Best Practices

```typescript
// Schema - name includes all fields
.index("by_organizationId_status", ["organizationId", "status"])

// Query - fields in same order as index
.withIndex("by_organizationId_status", (q) =>
  q.eq("organizationId", orgId).eq("status", "published")
)
```

### Auth Check (Backend)

```typescript
import { authComponent } from "./auth"

const user = await authComponent.getAuthUser(ctx)
if (!user) throw new Error("Not authenticated")
```

## Core Principles

1. **Use queries for reads** - Queries are reactive, cacheable, and consistent
2. **Keep functions fast** - Finish in < 100ms, work with < a few hundred records
3. **Prefer queries/mutations over actions** - Actions are for external API calls only
4. **Always use indexes** - Never do table scans with `.filter()`
5. **Minimize client state** - Rely on Convex's real-time sync

## Common Anti-Patterns

| Wrong | Correct |
|-------|---------|
| `import { useQuery } from 'convex/react'` | `import { useQuery } from 'convex-helpers/react/cache'` |
| `if (id) useQuery(...)` | `useQuery(..., id ? {...} : "skip")` |
| `.filter(x => x.field === val)` | `.withIndex("by_field", q => q.eq("field", val))` |
| Action with `ctx.db` | Use `ctx.runQuery/runMutation` |
| `count || 0` | `count ?? 0` (0 is falsy) |

## Reference Files

Load the appropriate reference file based on the task:

| File | Use When |
|------|----------|
| `references/01-setup.md` | Project setup, config files, environment variables |
| `references/02-router.md` | Router setup, root route, file-based routing, layouts |
| `references/03-auth.md` | Better Auth setup, sign up/in/out, protected routes, SSR auth |
| `references/04-data-fetching.md` | useQuery, useSuspenseQuery, mutations, loaders, prefetching |
| `references/05-backend.md` | Schema, queries, mutations, actions, internal functions, HTTP endpoints |
| `references/06-types.md` | TypeScript patterns, validators, type mapping |
| `references/07-storage.md` | File upload, download, metadata, deletion |
| `references/08-scheduling.md` | scheduler.runAfter, cron jobs |
| `references/09-agents.md` | AI agents, tools, RAG setup |
| `references/10-frontend.md` | Component patterns, loading states, Tailwind/shadcn |
| `references/11-permissions.md` | Role hierarchy, feature access patterns |
| `references/12-deployment.md` | Dev commands, Convex CLI, Vercel deployment |
| `references/13-quick-reference.md` | Import cheatsheet, common patterns summary |

### When to Load References

- **Starting a new project**: Load `01-setup.md`
- **Adding authentication**: Load `03-auth.md`
- **Writing backend functions**: Load `05-backend.md`
- **Implementing data fetching**: Load `04-data-fetching.md`
- **Building UI components**: Load `10-frontend.md`
- **Need quick syntax**: Load `13-quick-reference.md`
