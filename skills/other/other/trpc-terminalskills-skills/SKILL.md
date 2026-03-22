---
name: trpc
description: >-
  You are an expert in tRPC, the framework for building type-safe APIs
  without schemas or code generation. You help developers create full-stack
  TypeScript applications where the server defines procedures and the client
  calls them with full type inference — no REST routes, no GraphQL schemas, no
  OpenAPI specs, just TypeScript functions that are type-safe from database to
  UI.
license: Apache-2.0
compatibility: ''
metadata:
  author: terminal-skills
  version: 1.0.0
  category: Backend Development
  tags:
    - api
    - typescript
    - rpc
    - type-safe
    - react
    - nextjs
    - end-to-end
---

# tRPC — End-to-End Type-Safe APIs

You are an expert in tRPC, the framework for building type-safe APIs without schemas or code generation. You help developers create full-stack TypeScript applications where the server defines procedures and the client calls them with full type inference — no REST routes, no GraphQL schemas, no OpenAPI specs, just TypeScript functions that are type-safe from database to UI.

## Core Capabilities

### Server

```typescript
// server/trpc.ts — tRPC setup
import { initTRPC, TRPCError } from "@trpc/server";
import { z } from "zod";

const t = initTRPC.context<Context>().create();

export const router = t.router;
export const publicProcedure = t.procedure;
export const protectedProcedure = t.procedure.use(async ({ ctx, next }) => {
  if (!ctx.session?.user) throw new TRPCError({ code: "UNAUTHORIZED" });
  return next({ ctx: { user: ctx.session.user } });
});

// server/routers/users.ts
export const usersRouter = router({
  getById: publicProcedure
    .input(z.object({ id: z.string() }))
    .query(async ({ input, ctx }) => {
      const user = await ctx.db.users.findUnique({ where: { id: input.id } });
      if (!user) throw new TRPCError({ code: "NOT_FOUND", message: "User not found" });
      return user;
    }),

  list: publicProcedure
    .input(z.object({
      cursor: z.string().optional(),
      limit: z.number().min(1).max(100).default(20),
    }))
    .query(async ({ input, ctx }) => {
      const items = await ctx.db.users.findMany({
        take: input.limit + 1,
        cursor: input.cursor ? { id: input.cursor } : undefined,
        orderBy: { createdAt: "desc" },
      });
      const hasMore = items.length > input.limit;
      return { items: items.slice(0, input.limit), nextCursor: hasMore ? items[input.limit].id : undefined };
    }),

  update: protectedProcedure
    .input(z.object({ name: z.string().min(1), bio: z.string().max(500).optional() }))
    .mutation(async ({ input, ctx }) => {
      return ctx.db.users.update({ where: { id: ctx.user.id }, data: input });
    }),
});

// server/routers/_app.ts
export const appRouter = router({
  users: usersRouter,
  posts: postsRouter,
});
export type AppRouter = typeof appRouter;
```

### React Client

```tsx
import { trpc } from "@/utils/trpc";

function UserProfile({ userId }: { userId: string }) {
  // Full type inference — hover shows return type from server
  const { data: user, isLoading } = trpc.users.getById.useQuery({ id: userId });
  const updateUser = trpc.users.update.useMutation({
    onSuccess: () => utils.users.getById.invalidate({ id: userId }),
  });
  const utils = trpc.useUtils();

  if (isLoading) return <Spinner />;

  return (
    <div>
      <h1>{user?.name}</h1>   {/* user is typed as User | undefined */}
      <button onClick={() => updateUser.mutate({ name: "New Name" })}>
        {updateUser.isPending ? "Saving..." : "Update"}
      </button>
    </div>
  );
}

// Infinite scroll
function UserList() {
  const { data, fetchNextPage, hasNextPage } = trpc.users.list.useInfiniteQuery(
    { limit: 20 },
    { getNextPageParam: (lastPage) => lastPage.nextCursor },
  );

  return (
    <>
      {data?.pages.flatMap(p => p.items).map(user => <UserCard key={user.id} user={user} />)}
      {hasNextPage && <button onClick={() => fetchNextPage()}>Load More</button>}
    </>
  );
}
```

## Installation

```bash
npm install @trpc/server @trpc/client @trpc/react-query @tanstack/react-query zod
```

## Best Practices

1. **Zero code generation** — Types flow from server to client via TypeScript inference; no build step needed
2. **Zod validation** — Use `.input(z.object(...))` for runtime validation; type-safe at compile AND runtime
3. **React Query under the hood** — `useQuery`, `useMutation`, `useInfiniteQuery` all work; full caching
4. **Procedure types** — `query` for reads, `mutation` for writes, `subscription` for WebSocket streams
5. **Middleware** — Chain middleware for auth, logging, rate limiting; `protectedProcedure` pattern
6. **Error handling** — Use `TRPCError` with standard codes; client receives typed error responses
7. **Batching** — tRPC batches multiple queries into one HTTP request by default; reduces roundtrips
8. **Next.js integration** — Use `@trpc/next` for seamless App Router / Pages Router integration
