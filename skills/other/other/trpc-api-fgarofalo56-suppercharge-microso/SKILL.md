---
name: trpc-api
description: Build end-to-end typesafe APIs with tRPC. Covers routers, procedures, Zod validation, React Query integration, and Next.js setup. Use when building full-stack TypeScript applications with type-safe API calls.
---

# tRPC API Development

Build end-to-end typesafe APIs without schemas or code generation. tRPC provides full type inference from backend to frontend.

## Installation

```bash
# Core packages
npm install @trpc/server @trpc/client @trpc/react-query @tanstack/react-query zod

# For Next.js
npm install @trpc/next

# For subscriptions
npm install @trpc/server ws
```

## Project Structure

```
src/
├── server/
│   ├── trpc.ts           # tRPC initialization
│   ├── context.ts        # Request context
│   ├── routers/
│   │   ├── _app.ts       # Root router
│   │   ├── user.ts       # User procedures
│   │   └── post.ts       # Post procedures
│   └── middleware/
│       └── auth.ts       # Auth middleware
├── utils/
│   └── trpc.ts           # Client configuration
└── app/
    └── api/trpc/[trpc]/route.ts  # Next.js handler
```

## Server Setup

### Initialize tRPC

```typescript
// src/server/trpc.ts
import { initTRPC, TRPCError } from "@trpc/server";
import superjson from "superjson";
import { ZodError } from "zod";
import type { Context } from "./context";

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
export const mergeRouters = t.mergeRouters;
```

### Context Creation

```typescript
// src/server/context.ts
import { type inferAsyncReturnType } from "@trpc/server";
import { type CreateNextContextOptions } from "@trpc/server/adapters/next";
import { getServerSession } from "next-auth";
import { prisma } from "@/lib/prisma";

export async function createContext(opts: CreateNextContextOptions) {
  const session = await getServerSession(opts.req, opts.res);

  return {
    session,
    prisma,
    req: opts.req,
    res: opts.res,
  };
}

export type Context = inferAsyncReturnType<typeof createContext>;
```

## Routers and Procedures

### Basic Router

```typescript
// src/server/routers/user.ts
import { z } from "zod";
import { router, publicProcedure, protectedProcedure } from "../trpc";
import { TRPCError } from "@trpc/server";

export const userRouter = router({
  // Query - fetch data
  getById: publicProcedure
    .input(z.object({ id: z.string().uuid() }))
    .query(async ({ ctx, input }) => {
      const user = await ctx.prisma.user.findUnique({
        where: { id: input.id },
        select: { id: true, name: true, email: true, createdAt: true },
      });

      if (!user) {
        throw new TRPCError({
          code: "NOT_FOUND",
          message: "User not found",
        });
      }

      return user;
    }),

  // Query with pagination
  list: publicProcedure
    .input(
      z.object({
        limit: z.number().min(1).max(100).default(10),
        cursor: z.string().nullish(),
      }),
    )
    .query(async ({ ctx, input }) => {
      const items = await ctx.prisma.user.findMany({
        take: input.limit + 1,
        cursor: input.cursor ? { id: input.cursor } : undefined,
        orderBy: { createdAt: "desc" },
      });

      let nextCursor: string | undefined;
      if (items.length > input.limit) {
        const nextItem = items.pop();
        nextCursor = nextItem?.id;
      }

      return { items, nextCursor };
    }),

  // Mutation - modify data
  create: protectedProcedure
    .input(
      z.object({
        name: z.string().min(2).max(100),
        email: z.string().email(),
      }),
    )
    .mutation(async ({ ctx, input }) => {
      return ctx.prisma.user.create({
        data: {
          ...input,
          createdById: ctx.session.user.id,
        },
      });
    }),

  // Update mutation
  update: protectedProcedure
    .input(
      z.object({
        id: z.string().uuid(),
        name: z.string().min(2).max(100).optional(),
        email: z.string().email().optional(),
      }),
    )
    .mutation(async ({ ctx, input }) => {
      const { id, ...data } = input;
      return ctx.prisma.user.update({
        where: { id },
        data,
      });
    }),

  // Delete mutation
  delete: protectedProcedure
    .input(z.object({ id: z.string().uuid() }))
    .mutation(async ({ ctx, input }) => {
      await ctx.prisma.user.delete({ where: { id: input.id } });
      return { success: true };
    }),
});
```

### Root Router

```typescript
// src/server/routers/_app.ts
import { router } from "../trpc";
import { userRouter } from "./user";
import { postRouter } from "./post";

export const appRouter = router({
  user: userRouter,
  post: postRouter,
});

export type AppRouter = typeof appRouter;
```

## Input Validation with Zod

### Complex Schemas

```typescript
// src/server/schemas/post.ts
import { z } from "zod";

export const postStatusSchema = z.enum(["draft", "published", "archived"]);

export const createPostSchema = z.object({
  title: z
    .string()
    .min(3, "Title must be at least 3 characters")
    .max(200, "Title must be less than 200 characters"),
  content: z.string().min(10),
  status: postStatusSchema.default("draft"),
  tags: z.array(z.string()).max(10).optional(),
  publishAt: z.date().optional(),
  metadata: z.record(z.string(), z.unknown()).optional(),
});

export const updatePostSchema = createPostSchema.partial().extend({
  id: z.string().uuid(),
});

export const postFilterSchema = z.object({
  status: postStatusSchema.optional(),
  authorId: z.string().uuid().optional(),
  search: z.string().optional(),
  tags: z.array(z.string()).optional(),
  dateRange: z
    .object({
      from: z.date(),
      to: z.date(),
    })
    .optional(),
});

// Infer types from schemas
export type CreatePostInput = z.infer<typeof createPostSchema>;
export type UpdatePostInput = z.infer<typeof updatePostSchema>;
export type PostFilter = z.infer<typeof postFilterSchema>;
```

### Using Schemas in Procedures

```typescript
// src/server/routers/post.ts
import { router, protectedProcedure } from "../trpc";
import {
  createPostSchema,
  updatePostSchema,
  postFilterSchema,
} from "../schemas/post";

export const postRouter = router({
  create: protectedProcedure
    .input(createPostSchema)
    .mutation(async ({ ctx, input }) => {
      return ctx.prisma.post.create({
        data: {
          ...input,
          authorId: ctx.session.user.id,
        },
      });
    }),

  list: protectedProcedure
    .input(postFilterSchema)
    .query(async ({ ctx, input }) => {
      return ctx.prisma.post.findMany({
        where: {
          status: input.status,
          authorId: input.authorId,
          ...(input.search && {
            OR: [
              { title: { contains: input.search, mode: "insensitive" } },
              { content: { contains: input.search, mode: "insensitive" } },
            ],
          }),
          ...(input.tags?.length && {
            tags: { hasSome: input.tags },
          }),
        },
      });
    }),
});
```

## Middleware

### Authentication Middleware

```typescript
// src/server/middleware/auth.ts
import { TRPCError } from "@trpc/server";
import { middleware, publicProcedure } from "../trpc";

const isAuthenticated = middleware(async ({ ctx, next }) => {
  if (!ctx.session?.user) {
    throw new TRPCError({
      code: "UNAUTHORIZED",
      message: "You must be logged in",
    });
  }

  return next({
    ctx: {
      ...ctx,
      session: ctx.session, // Narrowed type
    },
  });
});

export const protectedProcedure = publicProcedure.use(isAuthenticated);

// Role-based middleware
const hasRole = (allowedRoles: string[]) =>
  middleware(async ({ ctx, next }) => {
    if (!ctx.session?.user) {
      throw new TRPCError({ code: "UNAUTHORIZED" });
    }

    if (!allowedRoles.includes(ctx.session.user.role)) {
      throw new TRPCError({
        code: "FORBIDDEN",
        message: "Insufficient permissions",
      });
    }

    return next({ ctx });
  });

export const adminProcedure = protectedProcedure.use(hasRole(["admin"]));
export const moderatorProcedure = protectedProcedure.use(
  hasRole(["admin", "moderator"]),
);
```

### Logging Middleware

```typescript
// src/server/middleware/logging.ts
import { middleware } from "../trpc";

export const loggerMiddleware = middleware(async ({ path, type, next }) => {
  const start = Date.now();
  const result = await next();
  const duration = Date.now() - start;

  console.log(`[${type.toUpperCase()}] ${path} - ${duration}ms`);

  return result;
});

// Rate limiting middleware
const rateLimits = new Map<string, { count: number; resetAt: number }>();

export const rateLimitMiddleware = (maxRequests: number, windowMs: number) =>
  middleware(async ({ ctx, next }) => {
    const key =
      ctx.session?.user?.id ??
      ctx.req.headers["x-forwarded-for"] ??
      "anonymous";
    const now = Date.now();
    const record = rateLimits.get(key);

    if (record && record.resetAt > now) {
      if (record.count >= maxRequests) {
        throw new TRPCError({
          code: "TOO_MANY_REQUESTS",
          message: "Rate limit exceeded",
        });
      }
      record.count++;
    } else {
      rateLimits.set(key, { count: 1, resetAt: now + windowMs });
    }

    return next();
  });
```

## WebSocket Subscriptions

### Server Setup

```typescript
// src/server/routers/notifications.ts
import { z } from "zod";
import { observable } from "@trpc/server/observable";
import { router, protectedProcedure } from "../trpc";
import { EventEmitter } from "events";

const ee = new EventEmitter();

interface Notification {
  id: string;
  userId: string;
  message: string;
  createdAt: Date;
}

export const notificationRouter = router({
  onNew: protectedProcedure
    .input(z.object({ userId: z.string() }).optional())
    .subscription(({ ctx, input }) => {
      return observable<Notification>((emit) => {
        const handler = (notification: Notification) => {
          if (!input?.userId || notification.userId === input.userId) {
            emit.next(notification);
          }
        };

        ee.on("notification", handler);

        return () => {
          ee.off("notification", handler);
        };
      });
    }),

  // Trigger notification (called from mutations)
  send: protectedProcedure
    .input(
      z.object({
        userId: z.string(),
        message: z.string(),
      }),
    )
    .mutation(async ({ input }) => {
      const notification: Notification = {
        id: crypto.randomUUID(),
        userId: input.userId,
        message: input.message,
        createdAt: new Date(),
      };

      ee.emit("notification", notification);
      return notification;
    }),
});
```

### WebSocket Handler (Next.js)

```typescript
// src/pages/api/trpc/[trpc].ts (Pages Router for WS)
import { createNextApiHandler } from "@trpc/server/adapters/next";
import { appRouter } from "@/server/routers/_app";
import { createContext } from "@/server/context";

export default createNextApiHandler({
  router: appRouter,
  createContext,
  onError: ({ error, path }) => {
    console.error(`tRPC error on ${path}:`, error);
  },
});

// For WebSocket support with ws
import { applyWSSHandler } from "@trpc/server/adapters/ws";
import { WebSocketServer } from "ws";

const wss = new WebSocketServer({ port: 3001 });
applyWSSHandler({
  wss,
  router: appRouter,
  createContext,
});
```

## React Query Integration

### Client Setup

```typescript
// src/utils/trpc.ts
import { createTRPCReact } from "@trpc/react-query";
import { httpBatchLink, wsLink, splitLink } from "@trpc/client";
import superjson from "superjson";
import type { AppRouter } from "@/server/routers/_app";

export const trpc = createTRPCReact<AppRouter>();

function getBaseUrl() {
  if (typeof window !== "undefined") return "";
  if (process.env.VERCEL_URL) return `https://${process.env.VERCEL_URL}`;
  return `http://localhost:${process.env.PORT ?? 3000}`;
}

export function createTRPCClient() {
  return trpc.createClient({
    transformer: superjson,
    links: [
      splitLink({
        condition: (op) => op.type === "subscription",
        true: wsLink({
          url: `ws://localhost:3001`,
        }),
        false: httpBatchLink({
          url: `${getBaseUrl()}/api/trpc`,
          headers() {
            return {
              // Add auth headers if needed
            };
          },
        }),
      }),
    ],
  });
}
```

### Provider Setup

```typescript
// src/app/providers.tsx
'use client';

import { useState } from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { trpc, createTRPCClient } from '@/utils/trpc';

export function TRPCProvider({ children }: { children: React.ReactNode }) {
  const [queryClient] = useState(
    () =>
      new QueryClient({
        defaultOptions: {
          queries: {
            staleTime: 5 * 60 * 1000,
            refetchOnWindowFocus: false,
          },
        },
      })
  );

  const [trpcClient] = useState(() => createTRPCClient());

  return (
    <trpc.Provider client={trpcClient} queryClient={queryClient}>
      <QueryClientProvider client={queryClient}>
        {children}
      </QueryClientProvider>
    </trpc.Provider>
  );
}
```

### Using Queries and Mutations

```typescript
// src/components/UserList.tsx
'use client';

import { trpc } from '@/utils/trpc';

export function UserList() {
  // Basic query
  const { data: users, isLoading, error } = trpc.user.list.useQuery({
    limit: 20,
  });

  // Query with options
  const userQuery = trpc.user.getById.useQuery(
    { id: 'user-123' },
    {
      enabled: !!userId,
      staleTime: 60 * 1000,
      retry: 3,
    }
  );

  // Infinite query for pagination
  const infiniteQuery = trpc.user.list.useInfiniteQuery(
    { limit: 10 },
    {
      getNextPageParam: (lastPage) => lastPage.nextCursor,
    }
  );

  // Mutation with cache invalidation
  const utils = trpc.useUtils();

  const createUser = trpc.user.create.useMutation({
    onSuccess: () => {
      utils.user.list.invalidate();
    },
    onError: (error) => {
      console.error('Failed to create user:', error.message);
    },
  });

  // Optimistic update
  const updateUser = trpc.user.update.useMutation({
    onMutate: async (newData) => {
      await utils.user.getById.cancel({ id: newData.id });
      const previousData = utils.user.getById.getData({ id: newData.id });

      utils.user.getById.setData({ id: newData.id }, (old) =>
        old ? { ...old, ...newData } : old
      );

      return { previousData };
    },
    onError: (err, newData, context) => {
      if (context?.previousData) {
        utils.user.getById.setData({ id: newData.id }, context.previousData);
      }
    },
    onSettled: (_, __, { id }) => {
      utils.user.getById.invalidate({ id });
    },
  });

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;

  return (
    <ul>
      {users?.items.map((user) => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  );
}
```

## Next.js App Router Setup

### API Route Handler

```typescript
// src/app/api/trpc/[trpc]/route.ts
import { fetchRequestHandler } from "@trpc/server/adapters/fetch";
import { appRouter } from "@/server/routers/_app";
import { createContext } from "@/server/context";

const handler = (req: Request) =>
  fetchRequestHandler({
    endpoint: "/api/trpc",
    req,
    router: appRouter,
    createContext: () => createContext({ req }),
    onError: ({ error, path }) => {
      console.error(`tRPC error on ${path}:`, error);
    },
  });

export { handler as GET, handler as POST };
```

### Server-Side Calls

```typescript
// src/server/api.ts
import { appRouter } from './routers/_app';
import { createContext } from './context';

export async function createServerCaller() {
  const context = await createContext();
  return appRouter.createCaller(context);
}

// Usage in Server Components
// src/app/users/page.tsx
import { createServerCaller } from '@/server/api';

export default async function UsersPage() {
  const api = await createServerCaller();
  const users = await api.user.list({ limit: 50 });

  return (
    <ul>
      {users.items.map((user) => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  );
}
```

## Error Handling

### Custom Error Classes

```typescript
// src/server/errors.ts
import { TRPCError } from "@trpc/server";

export class ValidationError extends TRPCError {
  constructor(
    message: string,
    public fields: Record<string, string[]>,
  ) {
    super({ code: "BAD_REQUEST", message });
  }
}

export class ResourceNotFoundError extends TRPCError {
  constructor(resource: string, id: string) {
    super({
      code: "NOT_FOUND",
      message: `${resource} with id ${id} not found`,
    });
  }
}

// Error handling in procedures
export const postRouter = router({
  getById: publicProcedure
    .input(z.object({ id: z.string() }))
    .query(async ({ ctx, input }) => {
      const post = await ctx.prisma.post.findUnique({
        where: { id: input.id },
      });

      if (!post) {
        throw new ResourceNotFoundError("Post", input.id);
      }

      return post;
    }),
});
```

### Client Error Handling

```typescript
// Error boundary for tRPC
export function TRPCErrorBoundary({ children }: { children: React.ReactNode }) {
  return (
    <ErrorBoundary
      fallbackRender={({ error }) => {
        if (error instanceof TRPCClientError) {
          const code = error.data?.code;

          if (code === 'UNAUTHORIZED') {
            return <RedirectToLogin />;
          }

          if (code === 'NOT_FOUND') {
            return <NotFound message={error.message} />;
          }
        }

        return <GenericError error={error} />;
      }}
    >
      {children}
    </ErrorBoundary>
  );
}
```

## Testing

### Unit Testing Procedures

```typescript
// tests/routers/user.test.ts
import { describe, it, expect, beforeEach, vi } from "vitest";
import { appRouter } from "@/server/routers/_app";
import { createInnerContext } from "@/server/context";

describe("userRouter", () => {
  const mockPrisma = {
    user: {
      findUnique: vi.fn(),
      create: vi.fn(),
      update: vi.fn(),
    },
  };

  const createCaller = (session = null) => {
    const ctx = createInnerContext({ session, prisma: mockPrisma as any });
    return appRouter.createCaller(ctx);
  };

  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("should get user by id", async () => {
    const mockUser = { id: "1", name: "John", email: "john@example.com" };
    mockPrisma.user.findUnique.mockResolvedValue(mockUser);

    const caller = createCaller();
    const result = await caller.user.getById({ id: "1" });

    expect(result).toEqual(mockUser);
    expect(mockPrisma.user.findUnique).toHaveBeenCalledWith({
      where: { id: "1" },
      select: expect.any(Object),
    });
  });

  it("should throw NOT_FOUND for missing user", async () => {
    mockPrisma.user.findUnique.mockResolvedValue(null);

    const caller = createCaller();

    await expect(caller.user.getById({ id: "invalid" })).rejects.toThrow(
      "User not found",
    );
  });

  it("should require auth for create", async () => {
    const caller = createCaller(); // No session

    await expect(
      caller.user.create({ name: "John", email: "john@test.com" }),
    ).rejects.toThrow("UNAUTHORIZED");
  });
});
```

### Integration Testing

```typescript
// tests/integration/api.test.ts
import { describe, it, expect } from "vitest";
import { createTRPCProxyClient, httpBatchLink } from "@trpc/client";
import type { AppRouter } from "@/server/routers/_app";
import superjson from "superjson";

const client = createTRPCProxyClient<AppRouter>({
  transformer: superjson,
  links: [
    httpBatchLink({
      url: "http://localhost:3000/api/trpc",
    }),
  ],
});

describe("API Integration", () => {
  it("should list users", async () => {
    const result = await client.user.list.query({ limit: 10 });
    expect(result.items).toBeDefined();
    expect(Array.isArray(result.items)).toBe(true);
  });
});
```

## Best Practices

### Procedure Organization

```typescript
// Group related procedures logically
export const postRouter = router({
  // Queries first
  getById: publicProcedure.input(...).query(...),
  list: publicProcedure.input(...).query(...),
  search: publicProcedure.input(...).query(...),

  // Then mutations
  create: protectedProcedure.input(...).mutation(...),
  update: protectedProcedure.input(...).mutation(...),
  delete: protectedProcedure.input(...).mutation(...),

  // Subscriptions last
  onUpdate: protectedProcedure.subscription(...),
});
```

### Type Exports

```typescript
// src/server/routers/_app.ts
import type { inferRouterInputs, inferRouterOutputs } from "@trpc/server";

export type AppRouter = typeof appRouter;
export type RouterInputs = inferRouterInputs<AppRouter>;
export type RouterOutputs = inferRouterOutputs<AppRouter>;

// Usage in components
type UserListOutput = RouterOutputs["user"]["list"];
type CreateUserInput = RouterInputs["user"]["create"];
```

### Performance Tips

```typescript
// 1. Use select to limit returned fields
const user = await ctx.prisma.user.findUnique({
  where: { id: input.id },
  select: { id: true, name: true }, // Only fetch needed fields
});

// 2. Batch requests on client
const utils = trpc.useUtils();
await Promise.all([
  utils.user.getById.prefetch({ id: "1" }),
  utils.user.getById.prefetch({ id: "2" }),
]);

// 3. Use suspense for better loading states
const [user] = trpc.user.getById.useSuspenseQuery({ id });
```

## Quick Reference

| Pattern     | Usage                                                 |
| ----------- | ----------------------------------------------------- |
| Query       | `trpc.router.procedure.useQuery(input)`               |
| Mutation    | `trpc.router.procedure.useMutation()`                 |
| Infinite    | `trpc.router.procedure.useInfiniteQuery(input, opts)` |
| Prefetch    | `utils.router.procedure.prefetch(input)`              |
| Invalidate  | `utils.router.procedure.invalidate(input?)`           |
| Set Data    | `utils.router.procedure.setData(input, updater)`      |
| Server Call | `api.router.procedure(input)`                         |
