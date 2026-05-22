---
name: trpc
description: Expert guidance for tRPC v11 type-safe APIs, procedures, middleware, error handling, and TanStack Query integration. Use when user says "trpc", "/trpc", "create procedure", "add endpoint", "api route", "mutation", "query", "middleware", or asks about type-safe APIs, routers, or server/client setup.
---

# tRPC Skill

Expert guidance for tRPC v11 with type-safe APIs, procedures, middleware patterns, and TanStack React Query integration.

## Quick Reference

### Project Structure

```
src/
├── trpc/
│   ├── trpc.ts          # tRPC initialization (t.router, t.procedure)
│   ├── context.ts       # Request context type
│   ├── router.ts        # Root router (merges all sub-routers)
│   ├── users.ts         # User procedures
│   └── posts.ts         # Post procedures
├── lib/
│   └── trpc-client.ts   # React client setup
└── server.ts            # tRPC adapter integration
```

## Server Setup

### Initialize tRPC (Once Per App)

```typescript
// src/trpc/trpc.ts
import { initTRPC, TRPCError } from "@trpc/server"
import type { Context } from "./context"

const t = initTRPC.context<Context>().create()

export const router = t.router
export const procedure = t.procedure
export const publicProcedure = t.procedure
```

### Define Context

```typescript
// src/trpc/context.ts
export interface Context {
  user?: { id: string; role: "user" | "admin" }
  db: DatabaseClient
}

export function createContext({ req }: { req: Request }): Context {
  const token = req.headers.get("authorization")
  return {
    user: token ? verifyToken(token) : undefined,
    db: getDbClient(),
  }
}
```

### Root Router

```typescript
// src/trpc/router.ts
import { router } from "./trpc"
import { usersRouter } from "./users"
import { postsRouter } from "./posts"

export const appRouter = router({
  users: usersRouter,
  posts: postsRouter,
})

export type AppRouter = typeof appRouter
```

## Procedures

### Query (Read Data)

```typescript
import { z } from "zod"
import { router, publicProcedure } from "./trpc"

export const usersRouter = router({
  // Simple query
  list: publicProcedure.query(async ({ ctx }) => {
    return ctx.db.users.findMany()
  }),

  // Query with input
  getById: publicProcedure
    .input(z.object({ id: z.string() }))
    .query(async ({ ctx, input }) => {
      const user = await ctx.db.users.findUnique({ where: { id: input.id } })
      if (!user) {
        throw new TRPCError({ code: "NOT_FOUND", message: "User not found" })
      }
      return user
    }),
})
```

### Mutation (Write Data)

```typescript
export const postsRouter = router({
  create: publicProcedure
    .input(z.object({
      title: z.string().min(1).max(100),
      content: z.string(),
      published: z.boolean().default(false),
    }))
    .mutation(async ({ ctx, input }) => {
      return ctx.db.posts.create({ data: input })
    }),

  update: publicProcedure
    .input(z.object({
      id: z.string(),
      title: z.string().optional(),
      content: z.string().optional(),
    }))
    .mutation(async ({ ctx, input }) => {
      const { id, ...data } = input
      return ctx.db.posts.update({ where: { id }, data })
    }),

  delete: publicProcedure
    .input(z.object({ id: z.string() }))
    .mutation(async ({ ctx, input }) => {
      await ctx.db.posts.delete({ where: { id: input.id } })
      return { success: true }
    }),
})
```

### Subscription (Real-time with SSE)

```typescript
import { observable } from "@trpc/server/observable"

export const eventsRouter = router({
  onUpdate: publicProcedure
    .input(z.object({ channelId: z.string() }))
    .subscription(({ input }) => {
      return observable<{ message: string }>((emit) => {
        const handler = (data: { message: string }) => {
          emit.next(data)
        }

        eventEmitter.on(input.channelId, handler)

        return () => {
          eventEmitter.off(input.channelId, handler)
        }
      })
    }),
})
```

## Middleware

### Base Procedure Pattern (Recommended)

```typescript
// src/trpc/trpc.ts
import { initTRPC, TRPCError } from "@trpc/server"

const t = initTRPC.context<Context>().create()

// 1. Public procedure with logging
const loggedProcedure = t.procedure.use(async ({ path, type, next }) => {
  const start = Date.now()
  const result = await next()
  console.log(`${type} ${path} - ${Date.now() - start}ms`)
  return result
})

// 2. Authenticated procedure (extends logged)
export const authedProcedure = loggedProcedure.use(async ({ ctx, next }) => {
  if (!ctx.user) {
    throw new TRPCError({ code: "UNAUTHORIZED" })
  }
  return next({
    ctx: { ...ctx, user: ctx.user }, // user is now non-null
  })
})

// 3. Admin procedure (extends authed)
export const adminProcedure = authedProcedure.use(async ({ ctx, next }) => {
  if (ctx.user.role !== "admin") {
    throw new TRPCError({ code: "FORBIDDEN", message: "Admin access required" })
  }
  return next({ ctx })
})

export const router = t.router
export const publicProcedure = loggedProcedure
```

### Using Protected Procedures

```typescript
import { router, authedProcedure, adminProcedure } from "./trpc"

export const adminRouter = router({
  // Requires authentication
  getProfile: authedProcedure.query(({ ctx }) => {
    return ctx.db.users.findUnique({ where: { id: ctx.user.id } })
  }),

  // Requires admin role
  deleteUser: adminProcedure
    .input(z.object({ userId: z.string() }))
    .mutation(({ ctx, input }) => {
      return ctx.db.users.delete({ where: { id: input.userId } })
    }),
})
```

### Context Extension with Middleware

```typescript
// Add organization context
const withOrganization = t.middleware(async ({ ctx, input, next }) => {
  const orgId = (input as { organizationId?: string })?.organizationId
  if (!orgId) {
    throw new TRPCError({ code: "BAD_REQUEST", message: "organizationId required" })
  }

  const org = await ctx.db.organizations.findUnique({ where: { id: orgId } })
  if (!org) {
    throw new TRPCError({ code: "NOT_FOUND", message: "Organization not found" })
  }

  return next({
    ctx: { ...ctx, organization: org },
  })
})

export const orgProcedure = authedProcedure.use(withOrganization)
```

## Error Handling

### TRPCError Codes

| Code | HTTP Status | Use Case |
|------|-------------|----------|
| `BAD_REQUEST` | 400 | Invalid input |
| `UNAUTHORIZED` | 401 | Not logged in |
| `FORBIDDEN` | 403 | Insufficient permissions |
| `NOT_FOUND` | 404 | Resource doesn't exist |
| `CONFLICT` | 409 | Resource conflict |
| `PRECONDITION_FAILED` | 412 | Condition not met |
| `TOO_MANY_REQUESTS` | 429 | Rate limited |
| `INTERNAL_SERVER_ERROR` | 500 | Server error |

### Throwing Errors

```typescript
import { TRPCError } from "@trpc/server"

// Basic error
throw new TRPCError({
  code: "NOT_FOUND",
  message: "Post not found",
})

// With cause (preserves stack trace)
try {
  await riskyOperation()
} catch (err) {
  throw new TRPCError({
    code: "INTERNAL_SERVER_ERROR",
    message: "Operation failed",
    cause: err,
  })
}
```

### Global Error Handler

```typescript
// In server setup
const handler = createHTTPHandler({
  router: appRouter,
  createContext,
  onError: ({ error, type, path, input, ctx }) => {
    console.error(`tRPC Error: ${type} ${path}`, {
      code: error.code,
      message: error.message,
      input,
      userId: ctx?.user?.id,
    })

    // Report to error tracking
    if (error.code === "INTERNAL_SERVER_ERROR") {
      reportError(error)
    }
  },
})
```

## React Client Setup

### v11 New Pattern (Recommended)

```typescript
// src/lib/trpc-client.ts
import { createTRPCContext } from "@trpc/tanstack-react-query"
import { httpBatchLink } from "@trpc/client"
import type { AppRouter } from "@/trpc/router"

export const { TRPCProvider, useTRPC, useTRPCClient } = createTRPCContext<AppRouter>()

export function createTRPCClient() {
  return {
    links: [
      httpBatchLink({
        url: "/api/trpc",
        headers: () => ({
          authorization: getAuthToken(),
        }),
      }),
    ],
  }
}
```

### Provider Setup

```tsx
// src/main.tsx
import { QueryClient, QueryClientProvider } from "@tanstack/react-query"
import { TRPCProvider, createTRPCClient } from "@/lib/trpc-client"

const queryClient = new QueryClient()
const trpcClient = createTRPCClient()

function App() {
  return (
    <TRPCProvider client={trpcClient} queryClient={queryClient}>
      <QueryClientProvider client={queryClient}>
        <Router />
      </QueryClientProvider>
    </TRPCProvider>
  )
}
```

### Classic Pattern (Still Supported)

```typescript
// src/lib/trpc-client.ts
import { createTRPCReact } from "@trpc/react-query"
import { httpBatchLink } from "@trpc/client"
import type { AppRouter } from "@/trpc/router"

export const trpc = createTRPCReact<AppRouter>()

export function createTRPCClient() {
  return trpc.createClient({
    links: [
      httpBatchLink({
        url: "/api/trpc",
      }),
    ],
  })
}
```

## React Usage

### v11 New Pattern

```tsx
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query"
import { useTRPC } from "@/lib/trpc-client"

function UserProfile({ userId }: { userId: string }) {
  const trpc = useTRPC()
  const queryClient = useQueryClient()

  // Query
  const { data: user, isLoading } = useQuery(
    trpc.users.getById.queryOptions({ id: userId })
  )

  // Mutation with cache invalidation
  const updateUser = useMutation({
    ...trpc.users.update.mutationOptions(),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: trpc.users.getById.queryKey({ id: userId }) })
    },
  })

  if (isLoading) return <div>Loading...</div>

  return (
    <div>
      <h1>{user?.name}</h1>
      <button onClick={() => updateUser.mutate({ id: userId, name: "New Name" })}>
        Update
      </button>
    </div>
  )
}
```

### Classic Pattern

```tsx
import { trpc } from "@/lib/trpc-client"

function UserProfile({ userId }: { userId: string }) {
  const utils = trpc.useUtils()

  // Query
  const { data: user, isLoading } = trpc.users.getById.useQuery({ id: userId })

  // Mutation
  const updateUser = trpc.users.update.useMutation({
    onSuccess: () => {
      utils.users.getById.invalidate({ id: userId })
    },
  })

  if (isLoading) return <div>Loading...</div>

  return (
    <div>
      <h1>{user?.name}</h1>
      <button onClick={() => updateUser.mutate({ id: userId, name: "New Name" })}>
        Update
      </button>
    </div>
  )
}
```

### Optimistic Updates

```tsx
const updatePost = useMutation({
  ...trpc.posts.update.mutationOptions(),
  onMutate: async (newData) => {
    await queryClient.cancelQueries({ queryKey: trpc.posts.getById.queryKey({ id: newData.id }) })

    const previous = queryClient.getQueryData(trpc.posts.getById.queryKey({ id: newData.id }))

    queryClient.setQueryData(
      trpc.posts.getById.queryKey({ id: newData.id }),
      (old) => ({ ...old, ...newData })
    )

    return { previous }
  },
  onError: (err, newData, context) => {
    queryClient.setQueryData(
      trpc.posts.getById.queryKey({ id: newData.id }),
      context?.previous
    )
  },
})
```

## Input Validation with Zod

### Common Patterns

```typescript
import { z } from "zod"

// Pagination
const paginationInput = z.object({
  page: z.number().int().min(1).default(1),
  limit: z.number().int().min(1).max(100).default(20),
})

// Filters
const filterInput = z.object({
  search: z.string().optional(),
  status: z.enum(["active", "inactive", "all"]).default("all"),
  sortBy: z.enum(["createdAt", "name", "updatedAt"]).default("createdAt"),
  sortOrder: z.enum(["asc", "desc"]).default("desc"),
})

// Combined
export const listUsersInput = paginationInput.merge(filterInput)

// Usage
list: publicProcedure
  .input(listUsersInput)
  .query(async ({ ctx, input }) => {
    const { page, limit, search, status, sortBy, sortOrder } = input
    // ...
  }),
```

### Complex Validation

```typescript
const createUserInput = z.object({
  email: z.string().email(),
  password: z.string().min(8).regex(/[A-Z]/, "Must contain uppercase"),
  profile: z.object({
    name: z.string().min(1).max(100),
    bio: z.string().max(500).optional(),
    avatar: z.string().url().optional(),
  }),
  preferences: z.record(z.string(), z.unknown()).optional(),
})
```

## Advanced Patterns

### Batch Requests

```typescript
// Client automatically batches requests made in same tick
const [users, posts, settings] = await Promise.all([
  trpc.users.list.query(),
  trpc.posts.list.query(),
  trpc.settings.get.query(),
])
// → Single HTTP request with all 3 procedures
```

### File Uploads (v11)

```typescript
// Server
upload: publicProcedure
  .input(z.object({
    file: z.instanceof(File),
    metadata: z.object({ name: z.string() }),
  }))
  .mutation(async ({ input }) => {
    const buffer = await input.file.arrayBuffer()
    // Process file...
  }),

// Client - use FormData link
import { unstable_formDataLink } from "@trpc/client"
```

### Type Inference

```typescript
import type { inferRouterInputs, inferRouterOutputs } from "@trpc/server"
import type { AppRouter } from "@/trpc/router"

type RouterInputs = inferRouterInputs<AppRouter>
type RouterOutputs = inferRouterOutputs<AppRouter>

// Usage
type CreateUserInput = RouterInputs["users"]["create"]
type User = RouterOutputs["users"]["getById"]
```

## Gotchas and Tips

1. **Export type only**: Use `export type { AppRouter }` to prevent server code in client bundles
2. **Initialize once**: Call `initTRPC` once per app, not per router file
3. **Base procedures**: Create 2-3 reusable base procedures (public, authed, admin)
4. **Context flows through**: Middleware can narrow context types for downstream procedures
5. **Zod schemas**: Define input schemas at the top of files for reusability
6. **Error codes matter**: Use appropriate codes for proper HTTP status mapping
7. **Batch by default**: `httpBatchLink` batches requests automatically
8. **TypeScript 5.7+**: Required for v11, enable strict mode

## Migration from v10 to v11

| v10 | v11 |
|-----|-----|
| `trpc.users.getById.useQuery()` | `useQuery(trpc.users.getById.queryOptions())` |
| `trpc.users.create.useMutation()` | `useMutation(trpc.users.create.mutationOptions())` |
| `utils.users.invalidate()` | `queryClient.invalidateQueries({ queryKey: trpc.users.queryKey() })` |
| WebSocket subscriptions | SSE subscriptions (recommended) |
