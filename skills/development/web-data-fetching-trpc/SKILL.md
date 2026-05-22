---
name: web-data-fetching-trpc
description: tRPC type-safe API patterns, procedures, middleware, React Query integration
---

# tRPC Type-Safe API Patterns

> **Quick Guide:** tRPC provides end-to-end type safety by sharing TypeScript types directly from server to client -- no code generation, no schema files. Export `AppRouter` type from your router (this is the key bridge). Use Zod for input validation, `TRPCError` with proper codes for errors, and middleware for auth. v11 is the current stable version: transformer goes inside `httpBatchLink()`, subscriptions use async generators (not `observable()`), and `@trpc/tanstack-react-query` is the recommended React integration.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

**(You MUST export `AppRouter` type from your tRPC router for client-side type inference)**

**(You MUST use `TRPCError` with appropriate error codes -- never throw raw Error objects)**

**(You MUST use Zod for input validation on ALL procedures accepting user input)**

**(You MUST place transformer inside `httpBatchLink()` in v11 -- NOT at client level)**

</critical_requirements>

---

**Auto-detection:** tRPC router, initTRPC, createTRPCClient, createTRPCContext, @trpc/server, @trpc/client, @trpc/react-query, @trpc/tanstack-react-query, TRPCError, procedure, publicProcedure, protectedProcedure, query, mutation, subscription, httpBatchLink, queryOptions, mutationOptions, useTRPC

**When to use:**

- Building APIs in TypeScript monorepos with shared types
- End-to-end type safety without code generation
- Full-stack TypeScript applications where both client and server are TypeScript
- Projects where types should flow automatically from backend to frontend

**When NOT to use:**

- Public APIs consumed by third parties (use OpenAPI/REST)
- Non-TypeScript clients (mobile apps, other languages)
- Need HTTP caching at CDN level (tRPC uses POST by default)
- GraphQL requirements with partial queries

**Key patterns covered:**

- Router and procedure definition (initTRPC, router, procedure)
- Input validation with Zod schemas
- Context and middleware for authentication
- Error handling with TRPCError codes
- React integration via `@trpc/tanstack-react-query` (recommended) or `@trpc/react-query` (classic)
- Optimistic updates, infinite queries, subscriptions

**Detailed Resources:**

- [examples/core.md](examples/core.md) - Router setup, CRUD, provider, type inference, queryOptions
- [examples/middleware.md](examples/middleware.md) - Logging, rate limiting, org-scoped access
- [examples/infinite-queries.md](examples/infinite-queries.md) - Cursor pagination, infinite scroll
- [examples/optimistic-updates.md](examples/optimistic-updates.md) - Optimistic updates with rollback
- [examples/subscriptions.md](examples/subscriptions.md) - Async generator subscriptions, SSE
- [examples/file-uploads.md](examples/file-uploads.md) - FormData file uploads (v11+)
- [reference.md](reference.md) - Decision frameworks, error codes, anti-patterns, v11 migration

---

<philosophy>

## Philosophy

tRPC eliminates API layer friction by sharing types directly between server and client. No schemas to write, no code to generate -- export your router type and import it client-side for full autocompletion and type safety.

**Core principles:**

- **Zero schema duplication**: Types flow from backend to frontend automatically
- **TypeScript-native**: Leverages TypeScript's type inference, not code generation
- **Procedure-based**: Queries read data, mutations write data -- clear separation
- **Composable middleware**: Build reusable authentication and validation layers
- **Built on TanStack Query**: Full caching, invalidation, and optimistic updates via React Query

**Trade-offs:**

- Requires TypeScript on both ends (no polyglot support)
- Best in monorepos where types can be shared directly
- Not suitable for public APIs needing OpenAPI documentation
- Uses POST by default -- no HTTP caching without configuration

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: tRPC Initialization and Router Setup

Initialize tRPC once per application. Export the router and procedure factories.

```typescript
import { initTRPC, TRPCError } from "@trpc/server";
import { ZodError } from "zod";
import type { Context } from "./context";

const t = initTRPC.context<Context>().create({
  errorFormatter({ shape, error }) {
    return {
      ...shape,
      data: {
        ...shape.data,
        zodError:
          error.cause instanceof ZodError ? error.cause.flatten() : null,
      },
    };
  },
});

export const router = t.router;
export const publicProcedure = t.procedure;
export const middleware = t.middleware;
```

**Why good:** Single initialization point, error formatter provides structured Zod errors to client, exported factories enable composition across router files

See [examples/core.md](examples/core.md) Pattern 1 for complete router and context factory.

---

### Pattern 2: Procedures with Zod Input Validation

Zod schemas provide runtime validation AND TypeScript inference from a single source.

```typescript
const createUserSchema = z.object({
  email: z.string().email(),
  name: z.string().min(1).max(100),
});

export const userRouter = router({
  create: protectedProcedure
    .input(createUserSchema)
    .mutation(async ({ input, ctx }) => {
      // input is typed: { email: string; name: string }
      return ctx.db.user.create({ data: input });
    }),
});
```

```typescript
// BAD: No input validation -- input is 'unknown'
publicProcedure.mutation(async ({ input }) => {
  return ctx.db.user.create({ data: input as any }); // Dangerous!
});
```

**Why bad:** Without Zod validation, input is unknown type, no runtime validation, injection risks, `as any` defeats TypeScript

See [examples/core.md](examples/core.md) Pattern 2 for complete CRUD router.

---

### Pattern 3: Authentication Middleware

Middleware narrows context types -- `ctx.user` becomes non-nullable after auth middleware.

```typescript
const isAuthenticated = middleware(async ({ ctx, next }) => {
  if (!ctx.session || !ctx.user) {
    throw new TRPCError({ code: "UNAUTHORIZED" });
  }
  return next({ ctx: { ...ctx, session: ctx.session, user: ctx.user } });
});

export const protectedProcedure = publicProcedure.use(isAuthenticated);
```

**Why good:** Auth enforced at procedure definition, TypeScript narrows `ctx.user` to non-nullable, eliminates duplicated if-checks in every handler

See [examples/middleware.md](examples/middleware.md) for logging, rate limiting, and org-scoped access patterns.

---

### Pattern 4: AppRouter Type Export

This is the KEY to tRPC's type safety. Export the router type for client-side inference.

```typescript
export const appRouter = router({
  user: userRouter,
  post: postRouter,
});

// THIS IS ESSENTIAL -- without it, clients have no type inference
export type AppRouter = typeof appRouter;
```

Use `inferRouterInputs`/`inferRouterOutputs` for extracting procedure types:

```typescript
import type { inferRouterInputs, inferRouterOutputs } from "@trpc/server";
type RouterInputs = inferRouterInputs<AppRouter>;
type RouterOutputs = inferRouterOutputs<AppRouter>;

// Extract specific type
type User = RouterOutputs["user"]["getById"];
```

See [examples/core.md](examples/core.md) Pattern 4 for complete type inference utilities.

---

### Pattern 5: React Integration (v11 Recommended)

v11 introduces `@trpc/tanstack-react-query` with `queryOptions`/`mutationOptions` factories that work directly with TanStack Query hooks.

```typescript
// Setup: createTRPCContext provides typed hooks
import { createTRPCContext } from "@trpc/tanstack-react-query";
export const { TRPCProvider, useTRPC } = createTRPCContext<AppRouter>();

// Usage: standard TanStack Query hooks with tRPC type safety
const trpc = useTRPC();
const { data } = useQuery(trpc.user.getById.queryOptions({ id: userId }));
```

**v11 CRITICAL:** Transformer must be inside `httpBatchLink()`, NOT at `createTRPCClient()` level.

```typescript
// BAD: v11 error
createTRPCClient({ transformer: superjson, links: [...] });

// GOOD: transformer inside the link
httpBatchLink({ url: "/api/trpc", transformer: superjson });
```

See [examples/core.md](examples/core.md) Patterns 3 and 5 for complete provider and component setup.

---

### Pattern 6: Error Handling with TRPCError

Use standardized error codes that map to HTTP status codes.

```typescript
// Server: throw TRPCError with appropriate code
throw new TRPCError({
  code: "NOT_FOUND",
  message: "User not found",
});

throw new TRPCError({
  code: "INTERNAL_SERVER_ERROR",
  message: "Failed to delete",
  cause: error, // Preserves original stack trace
});
```

```typescript
// Client: typed error handling
const trpc = useTRPC();
const deletePost = useMutation({
  ...trpc.post.delete.mutationOptions(),
  onError: (error) => {
    switch (error.data?.code) {
      case "NOT_FOUND":
        toast.error("Not found");
        break;
      case "FORBIDDEN":
        toast.error("Not allowed");
        break;
    }
  },
});
```

See [reference.md](reference.md) for complete error code table with HTTP status mappings.

---

### Pattern 7: Optimistic Updates

Cancel queries, snapshot state, optimistically update, rollback on error, invalidate on settle.

```typescript
const trpc = useTRPC();
const queryClient = useQueryClient();

const toggleTodo = useMutation({
  ...trpc.todo.toggle.mutationOptions(),
  onMutate: async ({ id }) => {
    await queryClient.cancelQueries({ queryKey: trpc.todo.list.queryKey() });
    const previousTodos = queryClient.getQueryData(trpc.todo.list.queryKey());
    queryClient.setQueryData(trpc.todo.list.queryKey(), (old: any) =>
      old?.map((t: any) =>
        t.id === id ? { ...t, completed: !t.completed } : t,
      ),
    );
    return { previousTodos };
  },
  onError: (err, vars, context) => {
    if (context?.previousTodos)
      queryClient.setQueryData(
        trpc.todo.list.queryKey(),
        context.previousTodos,
      );
  },
  onSettled: () =>
    queryClient.invalidateQueries({ queryKey: trpc.todo.list.queryKey() }),
});
```

**Why good:** Immediate UI feedback, automatic rollback on failure, eventual consistency via invalidation

See [examples/optimistic-updates.md](examples/optimistic-updates.md) for complete pattern with like button example.

</patterns>

---

<red_flags>

## RED FLAGS

**High Priority Issues:**

- **Missing `export type AppRouter`** -- clients have no type inference, defeats purpose of tRPC
- **Raw `throw new Error()`** -- should use `TRPCError` with appropriate code for HTTP mapping
- **Procedures without `.input()` validation** -- no runtime validation, type is `unknown`
- **Auth checks in procedure body** -- should use middleware for protected procedures
- **Transformer at client level in v11** -- must be inside `httpBatchLink()`, not at `createTRPCClient()` level

**Medium Priority Issues:**

- **Missing SuperJSON transformer** -- Date/Map/Set won't serialize correctly
- **No error formatter** -- Zod errors should be formatted for better client DX
- **Optimistic updates without rollback** -- must include `onError` handler to restore previous state
- **Using `observable()` for subscriptions** -- v11 uses async generators; `observable()` is the v10 pattern
- **Using `rawInput` in middleware** -- v11 changed to `getRawInput()` function

**Gotchas & Edge Cases:**

- `httpBatchLink` combines requests -- all batched requests share the same HTTP status code
- SuperJSON transformer must be configured on BOTH client and server
- Context is created per-request -- don't store mutable state in context
- Middleware runs in order -- auth middleware should come before rate limiting
- Query keys are auto-generated -- use `queryKey()` method (v11) or `getQueryKey()` for manual access
- Subscription reconnection with `tracked()` requires `lastEventId` in input schema
- Don't retry mutations (`retry: false`) -- retrying writes can cause duplicates

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

**(You MUST export `AppRouter` type from your tRPC router for client-side type inference)**

**(You MUST use `TRPCError` with appropriate error codes -- never throw raw Error objects)**

**(You MUST use Zod for input validation on ALL procedures accepting user input)**

**(You MUST place transformer inside `httpBatchLink()` in v11 -- NOT at client level)**

**Failure to follow these rules will break type safety, cause runtime errors, and defeat the purpose of using tRPC.**

</critical_reminders>
