---
name: trpc
description: Builds type-safe APIs with tRPC including routers, procedures, context, and client integration. Use when creating end-to-end type-safe APIs, building full-stack TypeScript applications, or replacing REST/GraphQL with simpler patterns.
---

# tRPC

End-to-end typesafe APIs without code generation or runtime overhead.

## Quick Start

**Install:**
```bash
npm install @trpc/server @trpc/client @trpc/react-query @tanstack/react-query zod
```

**Project structure:**
```
src/
  server/
    trpc.ts           # tRPC instance
    routers/
      _app.ts         # Root router
      posts.ts        # Posts router
  app/
    api/trpc/[trpc]/
      route.ts        # API handler (Next.js)
  trpc/
    client.ts         # Client setup
    Provider.tsx      # React provider
```

## Server Setup

### Initialize tRPC

```typescript
// server/trpc.ts
import { initTRPC, TRPCError } from '@trpc/server';
import superjson from 'superjson';
import { ZodError } from 'zod';
import type { Context } from './context';

const t = initTRPC.context<Context>().create({
  transformer: superjson,
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

### Context

```typescript
// server/context.ts
import type { inferAsyncReturnType } from '@trpc/server';
import type { FetchCreateContextFnOptions } from '@trpc/server/adapters/fetch';
import { prisma } from '@/lib/prisma';
import { getSession } from '@/lib/auth';

export async function createContext(opts: FetchCreateContextFnOptions) {
  const session = await getSession(opts.req);

  return {
    prisma,
    session,
    user: session?.user ?? null,
  };
}

export type Context = inferAsyncReturnType<typeof createContext>;
```

### Protected Procedure

```typescript
// server/trpc.ts
const isAuthed = middleware(({ ctx, next }) => {
  if (!ctx.user) {
    throw new TRPCError({ code: 'UNAUTHORIZED' });
  }
  return next({
    ctx: {
      user: ctx.user, // Now non-nullable
    },
  });
});

export const protectedProcedure = t.procedure.use(isAuthed);
```

## Routers

### Basic Router

```typescript
// server/routers/posts.ts
import { z } from 'zod';
import { router, publicProcedure, protectedProcedure } from '../trpc';

export const postsRouter = router({
  // Query - GET operations
  list: publicProcedure.query(async ({ ctx }) => {
    return ctx.prisma.post.findMany({
      orderBy: { createdAt: 'desc' },
    });
  }),

  // Query with input
  byId: publicProcedure
    .input(z.object({ id: z.string() }))
    .query(async ({ ctx, input }) => {
      return ctx.prisma.post.findUnique({
        where: { id: input.id },
      });
    }),

  // Mutation - POST/PUT/DELETE operations
  create: protectedProcedure
    .input(
      z.object({
        title: z.string().min(1).max(100),
        content: z.string().min(1),
      })
    )
    .mutation(async ({ ctx, input }) => {
      return ctx.prisma.post.create({
        data: {
          ...input,
          authorId: ctx.user.id,
        },
      });
    }),

  // Mutation with validation
  update: protectedProcedure
    .input(
      z.object({
        id: z.string(),
        title: z.string().min(1).max(100).optional(),
        content: z.string().min(1).optional(),
      })
    )
    .mutation(async ({ ctx, input }) => {
      const { id, ...data } = input;
      return ctx.prisma.post.update({
        where: { id },
        data,
      });
    }),

  delete: protectedProcedure
    .input(z.object({ id: z.string() }))
    .mutation(async ({ ctx, input }) => {
      return ctx.prisma.post.delete({
        where: { id: input.id },
      });
    }),
});
```

### Root Router

```typescript
// server/routers/_app.ts
import { router } from '../trpc';
import { postsRouter } from './posts';
import { usersRouter } from './users';

export const appRouter = router({
  posts: postsRouter,
  users: usersRouter,
});

export type AppRouter = typeof appRouter;
```

### API Handler (Next.js)

```typescript
// app/api/trpc/[trpc]/route.ts
import { fetchRequestHandler } from '@trpc/server/adapters/fetch';
import { appRouter } from '@/server/routers/_app';
import { createContext } from '@/server/context';

const handler = (req: Request) =>
  fetchRequestHandler({
    endpoint: '/api/trpc',
    req,
    router: appRouter,
    createContext,
  });

export { handler as GET, handler as POST };
```

## Client Setup

### React Query Client

```typescript
// trpc/client.ts
import { createTRPCReact } from '@trpc/react-query';
import type { AppRouter } from '@/server/routers/_app';

export const trpc = createTRPCReact<AppRouter>();
```

### Provider

```tsx
// trpc/Provider.tsx
'use client';

import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { httpBatchLink } from '@trpc/client';
import { useState } from 'react';
import superjson from 'superjson';
import { trpc } from './client';

function getBaseUrl() {
  if (typeof window !== 'undefined') return '';
  if (process.env.VERCEL_URL) return `https://${process.env.VERCEL_URL}`;
  return 'http://localhost:3000';
}

export function TRPCProvider({ children }: { children: React.ReactNode }) {
  const [queryClient] = useState(() => new QueryClient());
  const [trpcClient] = useState(() =>
    trpc.createClient({
      links: [
        httpBatchLink({
          url: `${getBaseUrl()}/api/trpc`,
          transformer: superjson,
        }),
      ],
    })
  );

  return (
    <trpc.Provider client={trpcClient} queryClient={queryClient}>
      <QueryClientProvider client={queryClient}>
        {children}
      </QueryClientProvider>
    </trpc.Provider>
  );
}
```

## Using tRPC in Components

### Queries

```tsx
'use client';

import { trpc } from '@/trpc/client';

function PostList() {
  const { data: posts, isLoading, error } = trpc.posts.list.useQuery();

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;

  return (
    <ul>
      {posts?.map((post) => (
        <li key={post.id}>{post.title}</li>
      ))}
    </ul>
  );
}

// With input
function Post({ id }: { id: string }) {
  const { data: post } = trpc.posts.byId.useQuery({ id });
  return <h1>{post?.title}</h1>;
}

// With options
function RecentPosts() {
  const { data } = trpc.posts.list.useQuery(undefined, {
    staleTime: 5 * 60 * 1000,
    refetchOnWindowFocus: false,
  });
  // ...
}
```

### Mutations

```tsx
'use client';

import { trpc } from '@/trpc/client';

function CreatePostForm() {
  const utils = trpc.useUtils();

  const mutation = trpc.posts.create.useMutation({
    onSuccess: () => {
      utils.posts.list.invalidate();
    },
  });

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);

    mutation.mutate({
      title: formData.get('title') as string,
      content: formData.get('content') as string,
    });
  };

  return (
    <form onSubmit={handleSubmit}>
      <input name="title" required />
      <textarea name="content" required />
      <button disabled={mutation.isPending}>
        {mutation.isPending ? 'Creating...' : 'Create'}
      </button>
      {mutation.error && <p>{mutation.error.message}</p>}
    </form>
  );
}
```

### Optimistic Updates

```tsx
function TodoItem({ todo }: { todo: Todo }) {
  const utils = trpc.useUtils();

  const toggleMutation = trpc.todos.toggle.useMutation({
    onMutate: async ({ id, completed }) => {
      await utils.todos.list.cancel();

      const previousTodos = utils.todos.list.getData();

      utils.todos.list.setData(undefined, (old) =>
        old?.map((t) => (t.id === id ? { ...t, completed } : t))
      );

      return { previousTodos };
    },
    onError: (err, variables, context) => {
      utils.todos.list.setData(undefined, context?.previousTodos);
    },
    onSettled: () => {
      utils.todos.list.invalidate();
    },
  });

  return (
    <input
      type="checkbox"
      checked={todo.completed}
      onChange={(e) =>
        toggleMutation.mutate({ id: todo.id, completed: e.target.checked })
      }
    />
  );
}
```

### Infinite Queries

```tsx
function InfinitePosts() {
  const { data, fetchNextPage, hasNextPage, isFetchingNextPage } =
    trpc.posts.infinite.useInfiniteQuery(
      { limit: 10 },
      {
        getNextPageParam: (lastPage) => lastPage.nextCursor,
      }
    );

  return (
    <div>
      {data?.pages.map((page) =>
        page.posts.map((post) => <PostCard key={post.id} post={post} />)
      )}

      <button
        onClick={() => fetchNextPage()}
        disabled={!hasNextPage || isFetchingNextPage}
      >
        {isFetchingNextPage ? 'Loading...' : 'Load More'}
      </button>
    </div>
  );
}

// Router procedure
infinitePosts: publicProcedure
  .input(
    z.object({
      limit: z.number().min(1).max(100).default(10),
      cursor: z.string().optional(),
    })
  )
  .query(async ({ ctx, input }) => {
    const posts = await ctx.prisma.post.findMany({
      take: input.limit + 1,
      cursor: input.cursor ? { id: input.cursor } : undefined,
      orderBy: { createdAt: 'desc' },
    });

    let nextCursor: string | undefined;
    if (posts.length > input.limit) {
      const nextItem = posts.pop();
      nextCursor = nextItem?.id;
    }

    return { posts, nextCursor };
  }),
```

## Server-Side Calls

### Server Components (Next.js)

```typescript
// lib/trpc-server.ts
import { appRouter } from '@/server/routers/_app';
import { createContext } from '@/server/context';

export const serverClient = appRouter.createCaller(await createContext());

// Usage in Server Component
async function PostsPage() {
  const posts = await serverClient.posts.list();

  return (
    <ul>
      {posts.map((post) => (
        <li key={post.id}>{post.title}</li>
      ))}
    </ul>
  );
}
```

### Server Actions

```typescript
// app/actions.ts
'use server';

import { serverClient } from '@/lib/trpc-server';

export async function createPost(formData: FormData) {
  const result = await serverClient.posts.create({
    title: formData.get('title') as string,
    content: formData.get('content') as string,
  });

  return result;
}
```

## Error Handling

### Throwing Errors

```typescript
import { TRPCError } from '@trpc/server';

delete: protectedProcedure
  .input(z.object({ id: z.string() }))
  .mutation(async ({ ctx, input }) => {
    const post = await ctx.prisma.post.findUnique({
      where: { id: input.id },
    });

    if (!post) {
      throw new TRPCError({
        code: 'NOT_FOUND',
        message: 'Post not found',
      });
    }

    if (post.authorId !== ctx.user.id) {
      throw new TRPCError({
        code: 'FORBIDDEN',
        message: 'You can only delete your own posts',
      });
    }

    return ctx.prisma.post.delete({ where: { id: input.id } });
  }),
```

### Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| PARSE_ERROR | 400 | Invalid JSON |
| BAD_REQUEST | 400 | Invalid input |
| UNAUTHORIZED | 401 | Not authenticated |
| FORBIDDEN | 403 | Not authorized |
| NOT_FOUND | 404 | Resource not found |
| CONFLICT | 409 | Resource conflict |
| TOO_MANY_REQUESTS | 429 | Rate limit exceeded |
| INTERNAL_SERVER_ERROR | 500 | Server error |

## Middleware

### Logging Middleware

```typescript
const loggerMiddleware = middleware(async ({ path, type, next }) => {
  const start = Date.now();
  const result = await next();
  const duration = Date.now() - start;

  console.log(`[${type}] ${path} - ${duration}ms`);

  return result;
});

export const loggedProcedure = t.procedure.use(loggerMiddleware);
```

### Rate Limiting

```typescript
import { Ratelimit } from '@upstash/ratelimit';
import { Redis } from '@upstash/redis';

const ratelimit = new Ratelimit({
  redis: Redis.fromEnv(),
  limiter: Ratelimit.slidingWindow(10, '10 s'),
});

const rateLimitMiddleware = middleware(async ({ ctx, next }) => {
  const identifier = ctx.user?.id ?? 'anonymous';
  const { success } = await ratelimit.limit(identifier);

  if (!success) {
    throw new TRPCError({ code: 'TOO_MANY_REQUESTS' });
  }

  return next();
});

export const rateLimitedProcedure = t.procedure.use(rateLimitMiddleware);
```

## Best Practices

1. **Organize routers by feature** - One router per domain
2. **Use input validation** - Always validate with Zod
3. **Create procedure variants** - publicProcedure, protectedProcedure
4. **Leverage useUtils** - For cache manipulation
5. **Handle errors properly** - Use TRPCError with codes

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Not typing context | Create typed context properly |
| Missing transformer | Add superjson for Date, Map, Set |
| Inline mutations | Use useMutation for all mutations |
| Not invalidating cache | Call utils.x.invalidate() |
| Over-fetching | Use select in queries |

## Reference Files

- [references/patterns.md](references/patterns.md) - Advanced patterns
- [references/testing.md](references/testing.md) - Testing tRPC
- [references/deployment.md](references/deployment.md) - Production setup
