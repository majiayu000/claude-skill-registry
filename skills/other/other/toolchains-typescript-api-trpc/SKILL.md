# tRPC - End-to-End Type Safety

---
progressive_disclosure:
  entry_point: summary
  sections:
    - id: summary
      title: "tRPC Overview"
      tokens: 70
      next: [when_to_use, quick_start]
    - id: when_to_use
      title: "When to Use tRPC"
      tokens: 150
      next: [quick_start, core_concepts]
    - id: quick_start
      title: "Quick Start"
      tokens: 300
      next: [core_concepts, router_definition]
    - id: core_concepts
      title: "Core Concepts"
      tokens: 400
      next: [router_definition, procedures]
    - id: router_definition
      title: "Router Definition"
      tokens: 350
      next: [procedures, context]
    - id: procedures
      title: "Procedures (Query & Mutation)"
      tokens: 400
      next: [input_validation, context]
    - id: input_validation
      title: "Input Validation with Zod"
      tokens: 350
      next: [context, middleware]
    - id: context
      title: "Context Management"
      tokens: 400
      next: [middleware, error_handling]
    - id: middleware
      title: "Middleware"
      tokens: 400
      next: [error_handling, client_setup]
    - id: error_handling
      title: "Error Handling"
      tokens: 350
      next: [client_setup, react_integration]
    - id: client_setup
      title: "Client Setup"
      tokens: 400
      next: [react_integration, nextjs_integration]
    - id: react_integration
      title: "React Query Integration"
      tokens: 450
      next: [nextjs_integration, subscriptions]
    - id: nextjs_integration
      title: "Next.js App Router Integration"
      tokens: 500
      next: [subscriptions, file_uploads]
    - id: subscriptions
      title: "Real-time Subscriptions"
      tokens: 400
      next: [file_uploads, batching]
    - id: file_uploads
      title: "File Uploads"
      tokens: 300
      next: [batching, typescript_inference]
    - id: batching
      title: "Batch Requests & Data Loaders"
      tokens: 350
      next: [typescript_inference, testing]
    - id: typescript_inference
      title: "TypeScript Inference Patterns"
      tokens: 300
      next: [testing, production_patterns]
    - id: testing
      title: "Testing Strategies"
      tokens: 400
      next: [production_patterns, comparison]
    - id: production_patterns
      title: "Production Patterns"
      tokens: 450
      next: [comparison, migration]
    - id: comparison
      title: "Comparison with REST & GraphQL"
      tokens: 250
      next: [migration, best_practices]
    - id: migration
      title: "Migration from REST"
      tokens: 300
      next: [best_practices]
    - id: best_practices
      title: "Best Practices & Performance"
      tokens: 400
---

## Summary

**tRPC** enables end-to-end type safety between TypeScript clients and servers without code generation. Define your API once, get automatic type inference everywhere.

**Key Benefits**: Zero codegen, TypeScript inference, React Query integration, minimal boilerplate.

---

## When to Use tRPC

**✅ Perfect For**:
- Full-stack TypeScript applications (Next.js, T3 stack)
- Projects where client and server share TypeScript codebase
- Teams wanting REST-like simplicity with GraphQL-like type safety
- Apps using React Query for data fetching
- Internal APIs where you control both client and server

**❌ Avoid When**:
- Public APIs consumed by non-TypeScript clients
- Microservices in different languages
- Mobile apps using Swift/Kotlin (use REST/GraphQL instead)
- Need API documentation for external developers (OpenAPI better)

**When to Choose**:
- **tRPC**: Full-stack TypeScript, monorepo, internal tools
- **REST**: Public APIs, language-agnostic, broad compatibility
- **GraphQL**: Complex data graphs, multiple clients, flexible queries

---

## Quick Start

### Installation

```bash
# Server dependencies
npm install @trpc/server zod

# React/Next.js client dependencies
npm install @trpc/client @trpc/react-query @tanstack/react-query
```

### Define Router (Server)

```typescript
// server/trpc.ts
import { initTRPC } from '@trpc/server';
import { z } from 'zod';

const t = initTRPC.create();

export const appRouter = t.router({
  hello: t.procedure
    .input(z.object({ name: z.string() }))
    .query(({ input }) => {
      return { greeting: `Hello ${input.name}` };
    }),

  createPost: t.procedure
    .input(z.object({ title: z.string(), content: z.string() }))
    .mutation(async ({ input }) => {
      // Save to database
      return { id: 1, ...input };
    }),
});

export type AppRouter = typeof appRouter;
```

### Use in Client (React)

```typescript
// client/trpc.ts
import { createTRPCReact } from '@trpc/react-query';
import type { AppRouter } from '../server/trpc';

export const trpc = createTRPCReact<AppRouter>();

// Component
function MyComponent() {
  const { data } = trpc.hello.useQuery({ name: 'World' });
  const createPost = trpc.createPost.useMutation();

  return <div>{data?.greeting}</div>; // Fully typed!
}
```

**Next**: Learn core concepts or dive into router definition.

---

## Core Concepts

### The tRPC Philosophy

tRPC provides **type-safe remote procedure calls** by sharing TypeScript types between client and server. No code generation—just TypeScript's inference.

### Key Components

1. **Router**: Collection of procedures (API endpoints)
2. **Procedure**: Single API operation (query or mutation)
3. **Context**: Request-scoped data (user, database, etc.)
4. **Middleware**: Intercept/modify requests (auth, logging)
5. **Input/Output**: Validated with Zod schemas

### Type Flow

```typescript
// Server defines types
const router = t.router({
  getUser: t.procedure
    .input(z.string())
    .query(({ input }) => ({ id: input, name: 'Alice' })),
});

// Client gets automatic types
const user = await trpc.getUser.query('123');
// user is typed as { id: string, name: string }
```

### Architecture Pattern

```
┌─────────────┐     Type-safe     ┌──────────────┐
│   Client    │ ←────────────────→ │    Server    │
│ (React)     │   No codegen!      │   (Node.js)  │
└─────────────┘                    └──────────────┘
      ↓                                    ↓
 React Query                          tRPC Router
 (caching)                            (procedures)
```

**Advantages**:
- Changes propagate instantly (no build step)
- Rename refactoring works across client/server
- Impossible to call wrong types
- Auto-complete for all API methods

---

## Router Definition

### Basic Router Structure

```typescript
import { initTRPC } from '@trpc/server';

const t = initTRPC.create();

export const appRouter = t.router({
  // Procedures go here
});

export type AppRouter = typeof appRouter;
```

### Nested Routers (Namespacing)

```typescript
const userRouter = t.router({
  getById: t.procedure
    .input(z.string())
    .query(({ input }) => getUser(input)),

  create: t.procedure
    .input(z.object({ name: z.string(), email: z.string() }))
    .mutation(({ input }) => createUser(input)),
});

const postRouter = t.router({
  list: t.procedure.query(() => getPosts()),
  create: t.procedure
    .input(z.object({ title: z.string() }))
    .mutation(({ input }) => createPost(input)),
});

export const appRouter = t.router({
  user: userRouter,
  post: postRouter,
});

// Client usage:
// trpc.user.getById.useQuery('123')
// trpc.post.list.useQuery()
```

### Router Merging

```typescript
import { adminRouter } from './admin';
import { publicRouter } from './public';

export const appRouter = t.mergeRouters(publicRouter, adminRouter);
```

### Router Organization Best Practices

```
server/
├── trpc.ts           # tRPC instance, context, middleware
├── routers/
│   ├── user.ts       # User-related procedures
│   ├── post.ts       # Post-related procedures
│   └── index.ts      # Combine all routers
└── index.ts          # Export AppRouter type
```

---

## Procedures (Query & Mutation)

### Query Procedures (Read Operations)

```typescript
const router = t.router({
  // Simple query
  getUser: t.procedure
    .input(z.string())
    .query(({ input }) => {
      return db.user.findUnique({ where: { id: input } });
    }),

  // Query with multiple inputs
  searchUsers: t.procedure
    .input(z.object({
      query: z.string(),
      limit: z.number().default(10),
    }))
    .query(({ input }) => {
      return db.user.findMany({
        where: { name: { contains: input.query } },
        take: input.limit,
      });
    }),
});
```

### Mutation Procedures (Write Operations)

```typescript
const router = t.router({
  createUser: t.procedure
    .input(z.object({
      name: z.string().min(3),
      email: z.string().email(),
    }))
    .mutation(async ({ input }) => {
      return await db.user.create({ data: input });
    }),

  updateUser: t.procedure
    .input(z.object({
      id: z.string(),
      data: z.object({
        name: z.string().optional(),
        email: z.string().email().optional(),
      }),
    }))
    .mutation(async ({ input }) => {
      return await db.user.update({
        where: { id: input.id },
        data: input.data,
      });
    }),
});
```

### Query vs Mutation

| Aspect | Query | Mutation |
|--------|-------|----------|
| **Purpose** | Read data | Modify data |
| **HTTP Method** | GET | POST |
| **Caching** | Cached by React Query | Not cached |
| **Idempotent** | Yes | No |
| **Side Effects** | None | Database writes, emails, etc. |

### Output Typing

```typescript
const router = t.router({
  getUser: t.procedure
    .input(z.string())
    .output(z.object({ id: z.string(), name: z.string() })) // Optional
    .query(({ input }) => {
      return { id: input, name: 'Alice' };
    }),
});
```

**Note**: Output validation adds runtime overhead—use for critical data only.

---

## Input Validation with Zod

### Why Zod?

tRPC uses **Zod** for runtime type validation and TypeScript inference. Zod schemas provide:
- Runtime validation (prevent invalid data)
- TypeScript types (auto-inferred from schema)
- Transformation (parse, coerce, default values)

### Basic Validation

```typescript
import { z } from 'zod';

const router = t.router({
  createPost: t.procedure
    .input(z.object({
      title: z.string().min(5).max(100),
      content: z.string(),
      published: z.boolean().default(false),
      tags: z.array(z.string()).optional(),
    }))
    .mutation(({ input }) => {
      // input is fully typed and validated
      return createPost(input);
    }),
});
```

### Advanced Validation

```typescript
const createUserInput = z.object({
  email: z.string().email(),
  password: z.string().min(8),
  age: z.number().int().min(18),
  role: z.enum(['user', 'admin']),
  metadata: z.record(z.string(), z.unknown()).optional(),
});

const router = t.router({
  createUser: t.procedure
    .input(createUserInput)
    .mutation(({ input }) => {
      // All validation passed
      return saveUser(input);
    }),
});
```

### Transformations

```typescript
const router = t.router({
  getUser: t.procedure
    .input(
      z.object({
        id: z.string().transform((id) => parseInt(id, 10)),
      })
    )
    .query(({ input }) => {
      // input.id is now a number
      return db.user.findUnique({ where: { id: input.id } });
    }),
});
```

### Reusable Schemas

```typescript
// schemas/user.ts
export const CreateUserSchema = z.object({
  name: z.string(),
  email: z.string().email(),
});

export const UpdateUserSchema = CreateUserSchema.partial().extend({
  id: z.string(),
});

// routers/user.ts
const router = t.router({
  create: t.procedure.input(CreateUserSchema).mutation(/*...*/),
  update: t.procedure.input(UpdateUserSchema).mutation(/*...*/),
});
```

---

## Context Management

### What is Context?

**Context** provides request-scoped data to all procedures—authentication, database connections, logging, etc.

### Creating Context

```typescript
import { inferAsyncReturnType } from '@trpc/server';
import { CreateNextContextOptions } from '@trpc/server/adapters/next';

export async function createContext(opts: CreateNextContextOptions) {
  const session = await getSession(opts.req);

  return {
    session,
    db: prisma,
    req: opts.req,
    res: opts.res,
  };
}

export type Context = inferAsyncReturnType<typeof createContext>;

const t = initTRPC.context<Context>().create();
```

### Using Context in Procedures

```typescript
const router = t.router({
  getMe: t.procedure.query(({ ctx }) => {
    if (!ctx.session?.user) {
      throw new TRPCError({ code: 'UNAUTHORIZED' });
    }

    return ctx.db.user.findUnique({
      where: { id: ctx.session.user.id },
    });
  }),

  createPost: t.procedure
    .input(z.object({ title: z.string() }))
    .mutation(async ({ ctx, input }) => {
      return ctx.db.post.create({
        data: {
          title: input.title,
          authorId: ctx.session.user.id,
        },
      });
    }),
});
```

### Context Best Practices

```typescript
// ✅ Good: Lazy database connection
export async function createContext(opts: CreateNextContextOptions) {
  return {
    getDB: () => prisma, // Lazy
    session: await getSession(opts.req),
  };
}

// ❌ Bad: Heavy computation in context
export async function createContext(opts: CreateNextContextOptions) {
  const allUsers = await prisma.user.findMany(); // Too expensive!
  return { allUsers };
}
```

---

## Middleware

### What is Middleware?

Middleware intercepts procedure calls to add cross-cutting concerns: logging, timing, authentication, rate limiting.

### Basic Middleware

```typescript
const loggerMiddleware = t.middleware(async ({ path, type, next }) => {
  const start = Date.now();
  console.log(`→ ${type} ${path}`);

  const result = await next();

  const duration = Date.now() - start;
  console.log(`✓ ${type} ${path} - ${duration}ms`);

  return result;
});

const loggedProcedure = t.procedure.use(loggerMiddleware);
```

### Authentication Middleware

```typescript
const isAuthed = t.middleware(({ ctx, next }) => {
  if (!ctx.session?.user) {
    throw new TRPCError({ code: 'UNAUTHORIZED' });
  }

  return next({
    ctx: {
      ...ctx,
      user: ctx.session.user, // Narrow type
    },
  });
});

// Protected procedure builder
const protectedProcedure = t.procedure.use(isAuthed);

const router = t.router({
  // Public
  getPublicPosts: t.procedure.query(() => getPosts()),

  // Protected - requires authentication
  getMyPosts: protectedProcedure.query(({ ctx }) => {
    // ctx.user is guaranteed to exist
    return getPostsByUser(ctx.user.id);
  }),
});
```

### Chaining Middleware

```typescript
const timingMiddleware = t.middleware(async ({ next }) => {
  const start = performance.now();
  const result = await next();
  console.log(`Execution time: ${performance.now() - start}ms`);
  return result;
});

const rateLimitMiddleware = t.middleware(async ({ ctx, next }) => {
  await checkRateLimit(ctx.session?.user?.id);
  return next();
});

const protectedProcedure = t.procedure
  .use(timingMiddleware)
  .use(rateLimitMiddleware)
  .use(isAuthed);
```

### Context Transformation

```typescript
const enrichContextMiddleware = t.middleware(async ({ ctx, next }) => {
  const user = ctx.session?.user
    ? await ctx.db.user.findUnique({ where: { id: ctx.session.user.id } })
    : null;

  return next({
    ctx: {
      ...ctx,
      user, // Full user object
    },
  });
});
```

---

## Error Handling

### TRPCError

```typescript
import { TRPCError } from '@trpc/server';

const router = t.router({
  getUser: t.procedure
    .input(z.string())
    .query(async ({ input }) => {
      const user = await db.user.findUnique({ where: { id: input } });

      if (!user) {
        throw new TRPCError({
          code: 'NOT_FOUND',
          message: `User ${input} not found`,
        });
      }

      return user;
    }),
});
```

### Error Codes

| Code | HTTP Status | Use Case |
|------|-------------|----------|
| `BAD_REQUEST` | 400 | Invalid input |
| `UNAUTHORIZED` | 401 | Not authenticated |
| `FORBIDDEN` | 403 | Not authorized |
| `NOT_FOUND` | 404 | Resource not found |
| `TIMEOUT` | 408 | Request timeout |
| `CONFLICT` | 409 | Resource conflict |
| `PRECONDITION_FAILED` | 412 | Precondition failed |
| `PAYLOAD_TOO_LARGE` | 413 | Request too large |
| `TOO_MANY_REQUESTS` | 429 | Rate limit exceeded |
| `CLIENT_CLOSED_REQUEST` | 499 | Client closed connection |
| `INTERNAL_SERVER_ERROR` | 500 | Server error |

### Custom Error Handling

```typescript
const router = t.router({
  deleteUser: t.procedure
    .input(z.string())
    .mutation(async ({ input, ctx }) => {
      try {
        return await ctx.db.user.delete({ where: { id: input } });
      } catch (error) {
        if (error.code === 'P2025') { // Prisma not found
          throw new TRPCError({
            code: 'NOT_FOUND',
            message: 'User not found',
            cause: error,
          });
        }
        throw new TRPCError({
          code: 'INTERNAL_SERVER_ERROR',
          message: 'Failed to delete user',
          cause: error,
        });
      }
    }),
});
```

### Error Formatting

```typescript
const t = initTRPC.context<Context>().create({
  errorFormatter({ shape, error }) {
    return {
      ...shape,
      data: {
        ...shape.data,
        zodError:
          error.code === 'BAD_REQUEST' && error.cause instanceof ZodError
            ? error.cause.flatten()
            : null,
      },
    };
  },
});
```

### Client-Side Error Handling

```typescript
function MyComponent() {
  const mutation = trpc.createUser.useMutation({
    onError: (error) => {
      if (error.data?.code === 'UNAUTHORIZED') {
        router.push('/login');
      } else {
        toast.error(error.message);
      }
    },
  });
}
```

---

## Client Setup

### Vanilla Client

```typescript
import { createTRPCProxyClient, httpBatchLink } from '@trpc/client';
import type { AppRouter } from './server';

const client = createTRPCProxyClient<AppRouter>({
  links: [
    httpBatchLink({
      url: 'http://localhost:3000/api/trpc',
    }),
  ],
});

// Usage
const user = await client.user.getById.query('123');
const newPost = await client.post.create.mutate({ title: 'Hello' });
```

### React Client Setup

```typescript
// utils/trpc.ts
import { createTRPCReact } from '@trpc/react-query';
import type { AppRouter } from '../server/routers';

export const trpc = createTRPCReact<AppRouter>();

// _app.tsx
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { httpBatchLink } from '@trpc/client';
import { useState } from 'react';
import { trpc } from '../utils/trpc';

export default function App({ Component, pageProps }: AppProps) {
  const [queryClient] = useState(() => new QueryClient());
  const [trpcClient] = useState(() =>
    trpc.createClient({
      links: [
        httpBatchLink({
          url: 'http://localhost:3000/api/trpc',
        }),
      ],
    })
  );

  return (
    <trpc.Provider client={trpcClient} queryClient={queryClient}>
      <QueryClientProvider client={queryClient}>
        <Component {...pageProps} />
      </QueryClientProvider>
    </trpc.Provider>
  );
}
```

### Next.js API Route

```typescript
// pages/api/trpc/[trpc].ts
import { createNextApiHandler } from '@trpc/server/adapters/next';
import { appRouter } from '../../../server/routers';
import { createContext } from '../../../server/context';

export default createNextApiHandler({
  router: appRouter,
  createContext,
});
```

### Headers & Authentication

```typescript
const trpcClient = trpc.createClient({
  links: [
    httpBatchLink({
      url: 'http://localhost:3000/api/trpc',
      headers: async () => {
        const token = await getAuthToken();
        return {
          authorization: token ? `Bearer ${token}` : undefined,
        };
      },
    }),
  ],
});
```

---

## React Query Integration

### useQuery Hook

```typescript
function UserProfile({ userId }: { userId: string }) {
  const { data, isLoading, error } = trpc.user.getById.useQuery(userId);

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;

  return <div>{data.name}</div>;
}
```

### Query Options

```typescript
const { data } = trpc.posts.list.useQuery(undefined, {
  refetchOnWindowFocus: false,
  staleTime: 5 * 60 * 1000, // 5 minutes
  cacheTime: 10 * 60 * 1000, // 10 minutes
  retry: 3,
  onSuccess: (data) => console.log('Fetched', data.length, 'posts'),
});
```

### useMutation Hook

```typescript
function CreatePostForm() {
  const utils = trpc.useContext();

  const createPost = trpc.post.create.useMutation({
    onSuccess: () => {
      // Invalidate and refetch
      utils.post.list.invalidate();
    },
  });

  const handleSubmit = (data: { title: string }) => {
    createPost.mutate(data);
  };

  return (
    <form onSubmit={handleSubmit}>
      <input name="title" />
      <button disabled={createPost.isLoading}>
        {createPost.isLoading ? 'Creating...' : 'Create'}
      </button>
      {createPost.error && <p>{createPost.error.message}</p>}
    </form>
  );
}
```

### Optimistic Updates

```typescript
const createPost = trpc.post.create.useMutation({
  onMutate: async (newPost) => {
    // Cancel outgoing refetches
    await utils.post.list.cancel();

    // Snapshot previous value
    const previousPosts = utils.post.list.getData();

    // Optimistically update
    utils.post.list.setData(undefined, (old) => [
      ...(old ?? []),
      { id: 'temp', ...newPost },
    ]);

    return { previousPosts };
  },
  onError: (err, newPost, context) => {
    // Rollback on error
    utils.post.list.setData(undefined, context?.previousPosts);
  },
  onSettled: () => {
    // Refetch after success or error
    utils.post.list.invalidate();
  },
});
```

### Infinite Queries

```typescript
// Server
const router = t.router({
  posts: t.procedure
    .input(z.object({
      cursor: z.number().optional(),
      limit: z.number().default(10),
    }))
    .query(({ input }) => {
      const posts = getPosts(input.cursor, input.limit);
      return {
        posts,
        nextCursor: posts.length === input.limit ? input.cursor + input.limit : undefined,
      };
    }),
});

// Client
function PostList() {
  const {
    data,
    fetchNextPage,
    hasNextPage,
    isFetchingNextPage,
  } = trpc.posts.useInfiniteQuery(
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
      {hasNextPage && (
        <button onClick={() => fetchNextPage()} disabled={isFetchingNextPage}>
          Load More
        </button>
      )}
    </div>
  );
}
```

---

## Next.js App Router Integration

### Server Components

```typescript
// app/users/page.tsx (Server Component)
import { createCaller } from '../server/routers';
import { createContext } from '../server/context';

export default async function UsersPage() {
  const ctx = await createContext({ req: null, res: null });
  const caller = createCaller(ctx);

  const users = await caller.user.list();

  return (
    <div>
      {users.map((user) => (
        <div key={user.id}>{user.name}</div>
      ))}
    </div>
  );
}
```

### Server Actions

```typescript
// app/actions.ts
'use server';

import { createCaller } from '../server/routers';
import { createContext } from '../server/context';

export async function createPost(formData: FormData) {
  const ctx = await createContext({ req: null, res: null });
  const caller = createCaller(ctx);

  return caller.post.create({
    title: formData.get('title') as string,
    content: formData.get('content') as string,
  });
}
```

### App Router Provider

```typescript
// app/providers.tsx
'use client';

import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { httpBatchLink } from '@trpc/client';
import { useState } from 'react';
import { trpc } from './trpc';

export function Providers({ children }: { children: React.ReactNode }) {
  const [queryClient] = useState(() => new QueryClient());
  const [trpcClient] = useState(() =>
    trpc.createClient({
      links: [
        httpBatchLink({
          url: '/api/trpc',
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

// app/layout.tsx
import { Providers } from './providers';

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
```

### Client Components in App Router

```typescript
// app/posts/create-button.tsx
'use client';

import { trpc } from '../trpc';

export function CreatePostButton() {
  const createPost = trpc.post.create.useMutation();

  return (
    <button onClick={() => createPost.mutate({ title: 'New Post' })}>
      Create Post
    </button>
  );
}
```

### API Route Handler (App Router)

```typescript
// app/api/trpc/[trpc]/route.ts
import { fetchRequestHandler } from '@trpc/server/adapters/fetch';
import { appRouter } from '../../../../server/routers';
import { createContext } from '../../../../server/context';

const handler = (req: Request) =>
  fetchRequestHandler({
    endpoint: '/api/trpc',
    req,
    router: appRouter,
    createContext,
  });

export { handler as GET, handler as POST };
```

---

## Real-time Subscriptions

### WebSocket Setup (Server)

```typescript
import { applyWSSHandler } from '@trpc/server/adapters/ws';
import ws from 'ws';

const wss = new ws.Server({ port: 3001 });

applyWSSHandler({
  wss,
  router: appRouter,
  createContext,
});

console.log('WebSocket server listening on port 3001');
```

### Subscription Procedure

```typescript
import { observable } from '@trpc/server/observable';
import { EventEmitter } from 'events';

const ee = new EventEmitter();

const router = t.router({
  onPostAdd: t.procedure.subscription(() => {
    return observable<Post>((emit) => {
      const onAdd = (data: Post) => emit.next(data);

      ee.on('add', onAdd);

      return () => {
        ee.off('add', onAdd);
      };
    });
  }),

  createPost: t.procedure
    .input(z.object({ title: z.string() }))
    .mutation(({ input }) => {
      const post = { id: Date.now().toString(), ...input };
      ee.emit('add', post); // Emit to subscribers
      return post;
    }),
});
```

### Client WebSocket Setup

```typescript
import { createWSClient, wsLink } from '@trpc/client';

const wsClient = createWSClient({
  url: 'ws://localhost:3001',
});

const trpcClient = trpc.createClient({
  links: [
    wsLink({
      client: wsClient,
    }),
  ],
});
```

### useSubscription Hook

```typescript
function PostFeed() {
  const [posts, setPosts] = useState<Post[]>([]);

  trpc.onPostAdd.useSubscription(undefined, {
    onData: (post) => {
      setPosts((prev) => [post, ...prev]);
    },
    onError: (err) => {
      console.error('Subscription error:', err);
    },
  });

  return (
    <div>
      {posts.map((post) => (
        <PostCard key={post.id} post={post} />
      ))}
    </div>
  );
}
```

### Subscription with Input

```typescript
// Server
const router = t.router({
  onUserStatusChange: t.procedure
    .input(z.string())
    .subscription(({ input }) => {
      return observable<UserStatus>((emit) => {
        const onChange = (userId: string, status: UserStatus) => {
          if (userId === input) {
            emit.next(status);
          }
        };

        ee.on('statusChange', onChange);
        return () => ee.off('statusChange', onChange);
      });
    }),
});

// Client
trpc.onUserStatusChange.useSubscription('user-123', {
  onData: (status) => console.log('Status:', status),
});
```

---

## File Uploads

### Multipart Form Data (Server)

```typescript
// Next.js API route with file upload
import { NextApiRequest, NextApiResponse } from 'next';
import formidable from 'formidable';
import fs from 'fs';

export const config = {
  api: { bodyParser: false },
};

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  const form = formidable({ multiples: false });

  form.parse(req, async (err, fields, files) => {
    if (err) return res.status(500).json({ error: 'Upload failed' });

    const file = files.file as formidable.File;
    const buffer = fs.readFileSync(file.filepath);

    // Upload to S3, etc.
    const url = await uploadToS3(buffer, file.originalFilename);

    res.json({ url });
  });
}
```

### Base64 Upload (tRPC)

```typescript
// For small files only (<1MB)
const router = t.router({
  uploadAvatar: t.procedure
    .input(z.object({
      fileName: z.string(),
      fileData: z.string(), // Base64
    }))
    .mutation(async ({ input }) => {
      const buffer = Buffer.from(input.fileData, 'base64');
      const url = await uploadToS3(buffer, input.fileName);
      return { url };
    }),
});

// Client
const uploadAvatar = trpc.uploadAvatar.useMutation();

const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
  const file = e.target.files?.[0];
  if (!file) return;

  const reader = new FileReader();
  reader.onload = () => {
    const base64 = reader.result as string;
    uploadAvatar.mutate({
      fileName: file.name,
      fileData: base64.split(',')[1], // Remove data:image/...;base64,
    });
  };
  reader.readAsDataURL(file);
};
```

### Signed URL Pattern (Recommended)

```typescript
// Step 1: Get signed upload URL from tRPC
const router = t.router({
  getUploadUrl: t.procedure
    .input(z.object({
      fileName: z.string(),
      fileType: z.string(),
    }))
    .mutation(async ({ input }) => {
      const signedUrl = await s3.getSignedUrl('putObject', {
        Bucket: 'my-bucket',
        Key: input.fileName,
        ContentType: input.fileType,
        Expires: 60, // 1 minute
      });

      return { uploadUrl: signedUrl, fileUrl: `https://cdn.example.com/${input.fileName}` };
    }),
});

// Step 2: Client uploads directly to S3
async function uploadFile(file: File) {
  // Get signed URL
  const { uploadUrl, fileUrl } = await trpc.getUploadUrl.mutate({
    fileName: file.name,
    fileType: file.type,
  });

  // Upload directly to S3
  await fetch(uploadUrl, {
    method: 'PUT',
    body: file,
    headers: { 'Content-Type': file.type },
  });

  // Save file URL to database via tRPC
  await trpc.user.updateAvatar.mutate({ url: fileUrl });
}
```

---

## Batch Requests & Data Loaders

### Automatic Batching

```typescript
// Client configuration
const trpcClient = trpc.createClient({
  links: [
    httpBatchLink({
      url: 'http://localhost:3000/api/trpc',
      maxBatchSize: 10, // Batch up to 10 requests
    }),
  ],
});

// Multiple calls made close together are batched into one HTTP request
const user1 = trpc.user.getById.useQuery('1');
const user2 = trpc.user.getById.useQuery('2');
const user3 = trpc.user.getById.useQuery('3');
// → Single HTTP request with 3 procedure calls
```

### DataLoader Pattern

```typescript
import DataLoader from 'dataloader';

// Create DataLoader in context
export async function createContext() {
  const userLoader = new DataLoader(async (ids: readonly string[]) => {
    const users = await db.user.findMany({
      where: { id: { in: [...ids] } },
    });

    // Return in same order as input
    return ids.map((id) => users.find((u) => u.id === id));
  });

  return { userLoader };
}

// Use in procedures
const router = t.router({
  getUser: t.procedure
    .input(z.string())
    .query(({ ctx, input }) => {
      return ctx.userLoader.load(input); // Batched!
    }),

  getPosts: t.procedure.query(async ({ ctx }) => {
    const posts = await db.post.findMany({ take: 10 });

    // N+1 problem solved—all authors fetched in one query
    const postsWithAuthors = await Promise.all(
      posts.map(async (post) => ({
        ...post,
        author: await ctx.userLoader.load(post.authorId),
      }))
    );

    return postsWithAuthors;
  }),
});
```

### Conditional Batching

```typescript
import { httpBatchLink, httpLink, splitLink } from '@trpc/client';

const trpcClient = trpc.createClient({
  links: [
    splitLink({
      // Batch queries, don't batch mutations
      condition: (op) => op.type === 'query',
      true: httpBatchLink({ url: '/api/trpc' }),
      false: httpLink({ url: '/api/trpc' }),
    }),
  ],
});
```

---

## TypeScript Inference Patterns

### Inferring Types from Router

```typescript
import type { inferRouterInputs, inferRouterOutputs } from '@trpc/server';
import type { AppRouter } from './server';

// Input types
type RouterInputs = inferRouterInputs<AppRouter>;
type CreateUserInput = RouterInputs['user']['create'];

// Output types
type RouterOutputs = inferRouterOutputs<AppRouter>;
type User = RouterOutputs['user']['getById'];

// Use in components
function UserCard({ user }: { user: User }) {
  return <div>{user.name}</div>;
}
```

### Procedure Helpers

```typescript
import type { inferProcedureInput, inferProcedureOutput } from '@trpc/server';

type CreatePostInput = inferProcedureInput<AppRouter['post']['create']>;
type Post = inferProcedureOutput<AppRouter['post']['getById']>;
```

### Context Type Inference

```typescript
import { inferAsyncReturnType } from '@trpc/server';

export async function createContext() {
  return {
    db: prisma,
    user: null as User | null,
  };
}

export type Context = inferAsyncReturnType<typeof createContext>;

const t = initTRPC.context<Context>().create();
```

### Generic Procedures

```typescript
// Reusable pagination
function createPaginatedProcedure<T>(
  getData: (cursor: number, limit: number) => Promise<T[]>
) {
  return t.procedure
    .input(z.object({
      cursor: z.number().optional(),
      limit: z.number().default(10),
    }))
    .query(async ({ input }) => {
      const items = await getData(input.cursor ?? 0, input.limit);
      return {
        items,
        nextCursor: items.length === input.limit
          ? (input.cursor ?? 0) + input.limit
          : undefined,
      };
    });
}

const router = t.router({
  posts: createPaginatedProcedure((cursor, limit) =>
    db.post.findMany({ skip: cursor, take: limit })
  ),
  users: createPaginatedProcedure((cursor, limit) =>
    db.user.findMany({ skip: cursor, take: limit })
  ),
});
```

---

## Testing Strategies

### Unit Testing Procedures

```typescript
import { createCaller } from '../routers';

describe('User Router', () => {
  it('should create user', async () => {
    const ctx = {
      db: mockDb,
      session: null,
    };

    const caller = createCaller(ctx);

    const result = await caller.user.create({
      name: 'Alice',
      email: 'alice@example.com',
    });

    expect(result).toMatchObject({
      name: 'Alice',
      email: 'alice@example.com',
    });
  });
});
```

### Integration Testing

```typescript
import { httpBatchLink } from '@trpc/client';
import { createTRPCProxyClient } from '@trpc/client';
import type { AppRouter } from '../server';

describe('tRPC Integration', () => {
  const client = createTRPCProxyClient<AppRouter>({
    links: [
      httpBatchLink({
        url: 'http://localhost:3000/api/trpc',
      }),
    ],
  });

  it('should fetch user', async () => {
    const user = await client.user.getById.query('123');
    expect(user.id).toBe('123');
  });
});
```

### Mocking Context

```typescript
import { createCaller } from '../routers';

const mockContext = {
  db: {
    user: {
      findUnique: vi.fn().mockResolvedValue({ id: '1', name: 'Alice' }),
      create: vi.fn(),
    },
  },
  session: {
    user: { id: '1', email: 'alice@example.com' },
  },
};

it('should get current user', async () => {
  const caller = createCaller(mockContext);
  const user = await caller.user.getMe();

  expect(mockContext.db.user.findUnique).toHaveBeenCalledWith({
    where: { id: '1' },
  });
  expect(user.name).toBe('Alice');
});
```

### Testing React Hooks

```typescript
import { renderHook, waitFor } from '@testing-library/react';
import { createWrapper } from './test-utils';

it('should fetch posts', async () => {
  const { result } = renderHook(() => trpc.post.list.useQuery(), {
    wrapper: createWrapper(),
  });

  await waitFor(() => expect(result.current.isSuccess).toBe(true));

  expect(result.current.data).toHaveLength(10);
});

// test-utils.ts
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { httpBatchLink } from '@trpc/client';
import { trpc } from '../utils/trpc';

export function createWrapper() {
  const queryClient = new QueryClient();
  const trpcClient = trpc.createClient({
    links: [httpBatchLink({ url: 'http://localhost:3000/api/trpc' })],
  });

  return ({ children }) => (
    <trpc.Provider client={trpcClient} queryClient={queryClient}>
      <QueryClientProvider client={queryClient}>
        {children}
      </QueryClientProvider>
    </trpc.Provider>
  );
}
```

---

## Production Patterns

### Error Monitoring

```typescript
import * as Sentry from '@sentry/node';

const t = initTRPC.context<Context>().create({
  errorFormatter({ shape, error }) {
    // Log to Sentry
    if (error.code === 'INTERNAL_SERVER_ERROR') {
      Sentry.captureException(error);
    }

    return {
      ...shape,
      data: {
        ...shape.data,
        // Don't expose internal errors in production
        message: process.env.NODE_ENV === 'production' && error.code === 'INTERNAL_SERVER_ERROR'
          ? 'Internal server error'
          : shape.message,
      },
    };
  },
});
```

### Rate Limiting

```typescript
import { Ratelimit } from '@upstash/ratelimit';
import { Redis } from '@upstash/redis';

const ratelimit = new Ratelimit({
  redis: Redis.fromEnv(),
  limiter: Ratelimit.slidingWindow(10, '10 s'),
});

const rateLimitMiddleware = t.middleware(async ({ ctx, next }) => {
  const identifier = ctx.session?.user?.id ?? ctx.req.ip;
  const { success } = await ratelimit.limit(identifier);

  if (!success) {
    throw new TRPCError({
      code: 'TOO_MANY_REQUESTS',
      message: 'Rate limit exceeded',
    });
  }

  return next();
});
```

### Caching

```typescript
import { Redis } from 'ioredis';

const redis = new Redis(process.env.REDIS_URL);

const router = t.router({
  getUser: t.procedure
    .input(z.string())
    .query(async ({ input }) => {
      // Check cache
      const cached = await redis.get(`user:${input}`);
      if (cached) return JSON.parse(cached);

      // Fetch from database
      const user = await db.user.findUnique({ where: { id: input } });

      // Cache for 5 minutes
      await redis.setex(`user:${input}`, 300, JSON.stringify(user));

      return user;
    }),
});
```

### Request Logging

```typescript
const loggingMiddleware = t.middleware(async ({ path, type, next, input }) => {
  const start = Date.now();

  console.log(`→ ${type} ${path}`, { input });

  try {
    const result = await next();
    const duration = Date.now() - start;
    console.log(`✓ ${type} ${path} - ${duration}ms`);
    return result;
  } catch (error) {
    const duration = Date.now() - start;
    console.error(`✗ ${type} ${path} - ${duration}ms`, { error });
    throw error;
  }
});
```

### OpenTelemetry Integration

```typescript
import { trace } from '@opentelemetry/api';

const tracingMiddleware = t.middleware(async ({ path, type, next }) => {
  const tracer = trace.getTracer('trpc');

  return tracer.startActiveSpan(`trpc.${type}.${path}`, async (span) => {
    try {
      const result = await next();
      span.setStatus({ code: 0 }); // OK
      return result;
    } catch (error) {
      span.setStatus({ code: 2, message: error.message }); // ERROR
      span.recordException(error);
      throw error;
    } finally {
      span.end();
    }
  });
});
```

---

## Comparison with REST & GraphQL

### Feature Comparison

| Feature | tRPC | REST | GraphQL |
|---------|------|------|---------|
| **Type Safety** | Full (TypeScript) | Manual/codegen | Manual/codegen |
| **Code Generation** | None | Optional (OpenAPI) | Required |
| **Learning Curve** | Low | Low | Medium/High |
| **Client Libraries** | TypeScript only | Any language | Any language |
| **API Documentation** | TypeScript types | OpenAPI/Swagger | Schema/introspection |
| **Public APIs** | ❌ No | ✅ Yes | ✅ Yes |
| **Flexible Queries** | ❌ Fixed | ❌ Fixed | ✅ Yes |
| **Overfetching** | Minimal | Common | None |
| **Caching** | React Query | HTTP caching | Complex |
| **Real-time** | WebSocket | SSE/WebSocket | Subscriptions |
| **File Uploads** | Workarounds | Native | Complex |

### When to Choose Each

**tRPC**:
- ✅ Full-stack TypeScript monorepo
- ✅ Internal tools and dashboards
- ✅ Next.js applications
- ✅ Rapid development with small teams
- ❌ Public APIs for external consumers
- ❌ Multi-language clients

**REST**:
- ✅ Public APIs with broad compatibility
- ✅ Multi-language services
- ✅ HTTP caching requirements
- ✅ File uploads and downloads
- ❌ Complex nested data structures
- ❌ Need for type safety without codegen

**GraphQL**:
- ✅ Complex data graphs
- ✅ Multiple client types (web, mobile, etc.)
- ✅ Need for flexible queries
- ✅ Avoiding overfetching
- ❌ Simple CRUD operations
- ❌ Small teams (complexity overhead)

### Migration Path

tRPC can **coexist** with REST/GraphQL:
```typescript
// Use tRPC for internal, REST for public
const router = t.router({
  internal: internalRouter, // tRPC only
});

// Expose REST endpoints separately
app.get('/api/public/users', publicRestHandler);
```

---

## Migration from REST

### Gradual Migration Strategy

1. **Add tRPC alongside REST**: Don't rewrite everything at once
2. **New features in tRPC**: Start with new endpoints
3. **Migrate high-value endpoints**: Focus on complex or frequently used APIs
4. **Keep public APIs in REST**: Only migrate internal consumption

### Converting REST to tRPC

**Before (REST)**:
```typescript
// pages/api/users/[id].ts
export default async function handler(req, res) {
  if (req.method === 'GET') {
    const user = await db.user.findUnique({ where: { id: req.query.id } });
    res.json(user);
  } else if (req.method === 'PATCH') {
    const user = await db.user.update({
      where: { id: req.query.id },
      data: req.body,
    });
    res.json(user);
  }
}

// Client
const response = await fetch(`/api/users/${id}`);
const user = await response.json(); // No types!
```

**After (tRPC)**:
```typescript
// server/routers/user.ts
export const userRouter = t.router({
  getById: t.procedure
    .input(z.string())
    .query(({ input }) => db.user.findUnique({ where: { id: input } })),

  update: t.procedure
    .input(z.object({
      id: z.string(),
      data: z.object({ name: z.string().optional() }),
    }))
    .mutation(({ input }) => db.user.update({
      where: { id: input.id },
      data: input.data,
    })),
});

// Client
const user = await trpc.user.getById.query(id); // Fully typed!
```

### Shared Validation

```typescript
// Reuse Zod schemas across REST and tRPC during migration
import { createUserSchema } from '../schemas/user';

// tRPC
const router = t.router({
  createUser: t.procedure
    .input(createUserSchema)
    .mutation(({ input }) => createUser(input)),
});

// REST (validate with same schema)
export default async function handler(req, res) {
  const parsed = createUserSchema.safeParse(req.body);
  if (!parsed.success) {
    return res.status(400).json({ errors: parsed.error });
  }
  const user = await createUser(parsed.data);
  res.json(user);
}
```

---

## Best Practices & Performance

### Code Organization

```
server/
├── trpc.ts              # tRPC instance, base procedures
├── context.ts           # Context creation
├── middleware/
│   ├── auth.ts          # Authentication middleware
│   ├── logging.ts       # Logging middleware
│   └── rateLimit.ts     # Rate limiting
├── routers/
│   ├── _app.ts          # Root router
│   ├── user.ts          # User procedures
│   ├── post.ts          # Post procedures
│   └── admin/
│       └── index.ts     # Admin-only procedures
└── schemas/
    ├── user.ts          # User Zod schemas
    └── post.ts          # Post Zod schemas
```

### Performance Tips

1. **Use batching for multiple queries**:
   ```typescript
   httpBatchLink({ url: '/api/trpc', maxBatchSize: 10 })
   ```

2. **Implement DataLoader for N+1 queries**:
   ```typescript
   const userLoader = new DataLoader(batchLoadUsers);
   ```

3. **Cache expensive queries**:
   ```typescript
   trpc.posts.list.useQuery(undefined, { staleTime: 5 * 60 * 1000 });
   ```

4. **Optimize database queries**:
   ```typescript
   // ❌ Bad: N+1 query
   const posts = await db.post.findMany();
   const postsWithAuthors = await Promise.all(
     posts.map((p) => db.user.findUnique({ where: { id: p.authorId } }))
   );

   // ✅ Good: Single query with include
   const posts = await db.post.findMany({
     include: { author: true },
   });
   ```

5. **Use React Query's deduplication**:
   ```typescript
   // Multiple components can call same query—React Query deduplicates
   const { data } = trpc.user.getMe.useQuery();
   ```

### Security Best Practices

1. **Always validate input with Zod**
2. **Use middleware for authentication**:
   ```typescript
   const protectedProcedure = t.procedure.use(isAuthed);
   ```
3. **Sanitize error messages in production**
4. **Implement rate limiting**
5. **Use HTTPS in production**
6. **Set CORS properly**:
   ```typescript
   createNextApiHandler({
     router: appRouter,
     createContext,
     onError: ({ error }) => {
       if (error.code === 'INTERNAL_SERVER_ERROR') {
         console.error('Internal error:', error);
       }
     },
   });
   ```

### Type Safety Tips

1. **Export router type, not implementation**:
   ```typescript
   export type AppRouter = typeof appRouter; // ✅
   // Don't export `appRouter` itself to client
   ```

2. **Use `satisfies` for better inference**:
   ```typescript
   const input = {
     name: 'Alice',
     age: 30,
   } satisfies CreateUserInput;
   ```

3. **Avoid `any` in context**:
   ```typescript
   // ❌ Bad
   ctx: { user: any }

   // ✅ Good
   ctx: { user: User | null }
   ```

### Development Workflow

1. **Define schema first**: Write Zod schemas before procedures
2. **Test procedures in isolation**: Use `createCaller` for unit tests
3. **Use TypeScript strict mode**: Catch type errors early
4. **Enable React Query DevTools**:
   ```typescript
   import { ReactQueryDevtools } from '@tanstack/react-query-devtools';

   <ReactQueryDevtools initialIsOpen={false} />
   ```

### Common Pitfalls

❌ **Don't return sensitive data**:
```typescript
// Bad: Exposes password hash
.query(() => db.user.findMany())

// Good: Select specific fields
.query(() => db.user.findMany({ select: { id: true, name: true } }))
```

❌ **Don't use mutations for reads**:
```typescript
// Bad: Side-effect-free operation as mutation
getMostRecentPost: t.procedure.mutation(() => getPost())

// Good: Use query for reads
getMostRecentPost: t.procedure.query(() => getPost())
```

❌ **Don't skip input validation**:
```typescript
// Bad: No validation
.input(z.any())

// Good: Strict validation
.input(z.object({ id: z.string().uuid() }))
```

### Monitoring & Observability

```typescript
const t = initTRPC.context<Context>().create({
  errorFormatter({ shape, error }) {
    // Log metrics
    metrics.increment('trpc.error', { code: error.code });

    // Send to error tracking
    if (error.code === 'INTERNAL_SERVER_ERROR') {
      Sentry.captureException(error);
    }

    return shape;
  },
});

const loggingMiddleware = t.middleware(async ({ path, type, next }) => {
  const start = Date.now();
  const result = await next();

  // Log performance metrics
  metrics.timing('trpc.duration', Date.now() - start, { path, type });

  return result;
});
```

---

## Summary

**tRPC** enables type-safe APIs with minimal boilerplate:
- ✅ **No code generation**: Types inferred from TypeScript
- ✅ **React Query integration**: Built-in caching and optimistic updates
- ✅ **Next.js first-class support**: App Router, Server Components
- ✅ **Developer experience**: Auto-complete, refactoring, type errors

**Best for**: Full-stack TypeScript apps, Next.js projects, internal tools
**Avoid for**: Public APIs, multi-language services

**Get Started**: Install → Define router → Use in client → Enjoy type safety!

**Related Skills**: Zod (validation), React Query (caching), Next.js (integration)