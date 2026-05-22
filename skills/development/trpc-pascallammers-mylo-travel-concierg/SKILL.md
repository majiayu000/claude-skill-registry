---
name: trpc
description: Auto-activates when user mentions tRPC, type-safe APIs, procedures, or tRPC routers. Expert in tRPC including router setup, procedures, middleware, and React Query integration.
category: api
---

# tRPC - End-to-End Type-Safe APIs

**tRPC** enables you to build fully type-safe APIs without code generation or schema files. It provides automatic type inference from server to client, making TypeScript work seamlessly across your full stack.

**Official Documentation**: https://trpc.io

---

## 🎯 Core Concepts

### What is tRPC?

tRPC is a TypeScript-first framework for building type-safe APIs using Remote Procedure Calls (RPC). Unlike REST or GraphQL, tRPC eliminates the need for:

- ❌ Manual type definitions
- ❌ Code generation
- ❌ Schema synchronization
- ❌ API contracts

Instead, you get:

- ✅ **End-to-end type safety**: Types flow automatically from server to client
- ✅ **Autocomplete everywhere**: Full IntelliSense for all your API calls
- ✅ **Instant feedback**: TypeScript errors when your API changes
- ✅ **Zero runtime overhead**: Type information is stripped at build time

---

## 🏗️ Router Setup (Complete Guide)

### Server Initialization

Initialize tRPC **exactly once** per application to avoid conflicts:

```typescript
// server/trpc.ts
import { initTRPC } from '@trpc/server';

// Initialize tRPC
const t = initTRPC.create();

// Export router and procedure builders
export const router = t.router;
export const publicProcedure = t.procedure;
```

✅ **Good**: Single initialization per app
```typescript
// server/trpc.ts
const t = initTRPC.create();
export const router = t.router;
export const publicProcedure = t.procedure;
```

❌ **Bad**: Multiple tRPC instances
```typescript
// ❌ Don't do this!
const t1 = initTRPC.create();
const t2 = initTRPC.create(); // Causes conflicts
```

### Creating Your First Router

Define routers with procedures (API endpoints):

```typescript
// server/routers/_app.ts
import { router, publicProcedure } from '../trpc';
import { z } from 'zod';

export const appRouter = router({
  // Query: fetch data
  greeting: publicProcedure
    .input(z.object({ name: z.string() }))
    .query(({ input }) => {
      return { message: `Hello ${input.name}!` };
    }),

  // Mutation: modify data
  createUser: publicProcedure
    .input(z.object({
      email: z.string().email(),
      name: z.string(),
    }))
    .mutation(async ({ input }) => {
      // Create user in database
      return { id: '1', ...input };
    }),
});

// Export type for client
export type AppRouter = typeof appRouter;
```

### Nested Routers (Modular Organization)

Organize your API into logical modules using nested routers:

```typescript
// server/routers/user.ts
import { router, publicProcedure } from '../trpc';
import { z } from 'zod';

export const userRouter = router({
  getById: publicProcedure
    .input(z.string())
    .query(async ({ input }) => {
      return await db.user.findUnique({ where: { id: input } });
    }),

  list: publicProcedure
    .input(z.object({
      limit: z.number().min(1).max(100).default(10),
      cursor: z.string().optional(),
    }))
    .query(async ({ input }) => {
      const users = await db.user.findMany({
        take: input.limit + 1,
        cursor: input.cursor ? { id: input.cursor } : undefined,
      });
      
      let nextCursor: string | undefined;
      if (users.length > input.limit) {
        const nextItem = users.pop();
        nextCursor = nextItem!.id;
      }

      return { users, nextCursor };
    }),

  create: publicProcedure
    .input(z.object({
      email: z.string().email(),
      name: z.string().min(1),
    }))
    .mutation(async ({ input }) => {
      return await db.user.create({ data: input });
    }),

  update: publicProcedure
    .input(z.object({
      id: z.string(),
      email: z.string().email().optional(),
      name: z.string().min(1).optional(),
    }))
    .mutation(async ({ input }) => {
      const { id, ...data } = input;
      return await db.user.update({
        where: { id },
        data,
      });
    }),

  delete: publicProcedure
    .input(z.string())
    .mutation(async ({ input }) => {
      return await db.user.delete({ where: { id: input } });
    }),
});
```

```typescript
// server/routers/post.ts
import { router, publicProcedure } from '../trpc';
import { z } from 'zod';

export const postRouter = router({
  getById: publicProcedure
    .input(z.string())
    .query(async ({ input }) => {
      return await db.post.findUnique({
        where: { id: input },
        include: { author: true },
      });
    }),

  list: publicProcedure
    .input(z.object({
      userId: z.string().optional(),
      published: z.boolean().optional(),
    }))
    .query(async ({ input }) => {
      return await db.post.findMany({
        where: {
          authorId: input.userId,
          published: input.published,
        },
        include: { author: true },
      });
    }),

  create: publicProcedure
    .input(z.object({
      title: z.string().min(1),
      content: z.string(),
      authorId: z.string(),
    }))
    .mutation(async ({ input }) => {
      return await db.post.create({ data: input });
    }),
});
```

```typescript
// server/routers/_app.ts - Merging routers
import { router } from '../trpc';
import { userRouter } from './user';
import { postRouter } from './post';

export const appRouter = router({
  user: userRouter,
  post: postRouter,
});

export type AppRouter = typeof appRouter;
```

✅ **Good**: Modular router organization
```typescript
// ✅ Clean, organized structure
const appRouter = router({
  user: userRouter,
  post: postRouter,
  comment: commentRouter,
  auth: authRouter,
});
```

❌ **Bad**: Monolithic router
```typescript
// ❌ Hard to maintain
const appRouter = router({
  getUserById: procedure.query(/* ... */),
  listUsers: procedure.query(/* ... */),
  createUser: procedure.mutation(/* ... */),
  getPostById: procedure.query(/* ... */),
  listPosts: procedure.query(/* ... */),
  // ... 50 more procedures
});
```

### Next.js App Router Setup

Complete setup for Next.js 13+ App Router:

```typescript
// server/context.ts
import { type CreateNextContextOptions } from '@trpc/server/adapters/next';
import { getServerSession } from 'next-auth';
import { authOptions } from './auth';

export async function createContext(opts: CreateNextContextOptions) {
  const session = await getServerSession(authOptions);

  return {
    session,
    req: opts.req,
    res: opts.res,
  };
}

export type Context = Awaited<ReturnType<typeof createContext>>;
```

```typescript
// server/trpc.ts
import { initTRPC, TRPCError } from '@trpc/server';
import { type Context } from './context';

const t = initTRPC.context<Context>().create();

export const router = t.router;
export const publicProcedure = t.procedure;

// Protected procedure (requires auth)
export const protectedProcedure = t.procedure.use(({ ctx, next }) => {
  if (!ctx.session?.user) {
    throw new TRPCError({ code: 'UNAUTHORIZED' });
  }
  return next({
    ctx: {
      // Session is now non-nullable
      session: ctx.session,
    },
  });
});
```

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

### Advanced Router Configuration

Customize tRPC with runtime configuration:

```typescript
// server/trpc.ts
import { initTRPC } from '@trpc/server';
import superjson from 'superjson';

const t = initTRPC
  .context<Context>()
  .meta<Meta>()
  .create({
    // Data transformer (serialize Date, Map, Set, etc.)
    transformer: superjson,

    // Custom error formatting
    errorFormatter({ shape, error }) {
      return {
        ...shape,
        data: {
          ...shape.data,
          zodError:
            error.cause instanceof ZodError
              ? error.cause.flatten()
              : null,
        },
      };
    },

    // Development mode (shows stack traces)
    isDev: process.env.NODE_ENV !== 'production',

    // Allow non-server environments (for testing)
    allowOutsideOfServer: process.env.NODE_ENV === 'test',
  });
```

✅ **Good**: Proper configuration
```typescript
// ✅ Data transformer for complex types
const t = initTRPC.create({
  transformer: superjson,
  errorFormatter: customFormatter,
});
```

❌ **Bad**: No data transformer with complex types
```typescript
// ❌ Date objects won't serialize correctly
const t = initTRPC.create();

// This will fail!
return {
  createdAt: new Date(), // ❌ Won't work without transformer
};
```

---

## 🔧 Procedures (Queries & Mutations)

### Query Procedures

Queries are for fetching data without side effects:

```typescript
import { publicProcedure, router } from '../trpc';
import { z } from 'zod';

export const blogRouter = router({
  // Simple query (no input)
  listAll: publicProcedure.query(async () => {
    return await db.post.findMany();
  }),

  // Query with input validation
  getById: publicProcedure
    .input(z.string().uuid())
    .query(async ({ input }) => {
      const post = await db.post.findUnique({
        where: { id: input },
      });

      if (!post) {
        throw new TRPCError({
          code: 'NOT_FOUND',
          message: 'Post not found',
        });
      }

      return post;
    }),

  // Query with complex input
  search: publicProcedure
    .input(z.object({
      query: z.string().min(1),
      tags: z.array(z.string()).optional(),
      authorId: z.string().optional(),
      limit: z.number().min(1).max(100).default(10),
      offset: z.number().min(0).default(0),
    }))
    .query(async ({ input }) => {
      return await db.post.findMany({
        where: {
          OR: [
            { title: { contains: input.query, mode: 'insensitive' } },
            { content: { contains: input.query, mode: 'insensitive' } },
          ],
          tags: input.tags ? { hasSome: input.tags } : undefined,
          authorId: input.authorId,
        },
        take: input.limit,
        skip: input.offset,
      });
    }),

  // Infinite query pattern
  listInfinite: publicProcedure
    .input(z.object({
      limit: z.number().min(1).max(100).default(10),
      cursor: z.string().optional(),
    }))
    .query(async ({ input }) => {
      const items = await db.post.findMany({
        take: input.limit + 1,
        cursor: input.cursor ? { id: input.cursor } : undefined,
        orderBy: { createdAt: 'desc' },
      });

      let nextCursor: string | undefined;
      if (items.length > input.limit) {
        const nextItem = items.pop();
        nextCursor = nextItem!.id;
      }

      return {
        items,
        nextCursor,
      };
    }),
});
```

✅ **Good**: Proper query design
```typescript
// ✅ Query has no side effects
getUser: publicProcedure
  .input(z.string())
  .query(async ({ input }) => {
    return await db.user.findUnique({ where: { id: input } });
  }),
```

❌ **Bad**: Query with side effects
```typescript
// ❌ Don't modify data in queries!
getUser: publicProcedure
  .input(z.string())
  .query(async ({ input }) => {
    // ❌ Incrementing view count in a query
    await db.user.update({
      where: { id: input },
      data: { views: { increment: 1 } },
    });
    return await db.user.findUnique({ where: { id: input } });
  }),
```

### Mutation Procedures

Mutations are for creating, updating, or deleting data:

```typescript
export const userRouter = router({
  // Create mutation
  create: publicProcedure
    .input(z.object({
      email: z.string().email(),
      name: z.string().min(1),
      password: z.string().min(8),
    }))
    .mutation(async ({ input }) => {
      const hashedPassword = await hash(input.password);

      const user = await db.user.create({
        data: {
          email: input.email,
          name: input.name,
          password: hashedPassword,
        },
      });

      return {
        id: user.id,
        email: user.email,
        name: user.name,
      };
    }),

  // Update mutation
  update: publicProcedure
    .input(z.object({
      id: z.string(),
      name: z.string().min(1).optional(),
      bio: z.string().optional(),
    }))
    .mutation(async ({ input, ctx }) => {
      if (!ctx.session?.user) {
        throw new TRPCError({ code: 'UNAUTHORIZED' });
      }

      const { id, ...data } = input;

      return await db.user.update({
        where: { id },
        data,
      });
    }),

  // Delete mutation
  delete: publicProcedure
    .input(z.string())
    .mutation(async ({ input, ctx }) => {
      if (!ctx.session?.user) {
        throw new TRPCError({ code: 'UNAUTHORIZED' });
      }

      await db.user.delete({ where: { id: input } });

      return { success: true };
    }),

  // Complex mutation with transaction
  transferOwnership: publicProcedure
    .input(z.object({
      postId: z.string(),
      newOwnerId: z.string(),
    }))
    .mutation(async ({ input, ctx }) => {
      return await db.$transaction(async (tx) => {
        // Update post ownership
        const post = await tx.post.update({
          where: { id: input.postId },
          data: { authorId: input.newOwnerId },
        });

        // Create activity log
        await tx.activity.create({
          data: {
            type: 'OWNERSHIP_TRANSFER',
            postId: input.postId,
            fromUserId: ctx.session!.user.id,
            toUserId: input.newOwnerId,
          },
        });

        return post;
      });
    }),
});
```

### Input Validation with Zod

tRPC uses Zod for runtime validation:

```typescript
import { z } from 'zod';

export const formRouter = router({
  // Basic types
  submitBasic: publicProcedure
    .input(z.object({
      string: z.string(),
      number: z.number(),
      boolean: z.boolean(),
      date: z.date(),
    }))
    .mutation(({ input }) => input),

  // Advanced validation
  submitAdvanced: publicProcedure
    .input(z.object({
      email: z.string().email(),
      url: z.string().url(),
      uuid: z.string().uuid(),
      age: z.number().min(18).max(120),
      password: z.string().min(8).regex(/[A-Z]/).regex(/[0-9]/),
      enum: z.enum(['ADMIN', 'USER', 'GUEST']),
    }))
    .mutation(({ input }) => input),

  // Optional and nullable
  submitOptional: publicProcedure
    .input(z.object({
      required: z.string(),
      optional: z.string().optional(),
      nullable: z.string().nullable(),
      withDefault: z.string().default('default value'),
    }))
    .mutation(({ input }) => input),

  // Arrays and objects
  submitComplex: publicProcedure
    .input(z.object({
      tags: z.array(z.string()),
      metadata: z.record(z.string()),
      nested: z.object({
        deep: z.object({
          value: z.number(),
        }),
      }),
    }))
    .mutation(({ input }) => input),

  // Discriminated unions
  submitUnion: publicProcedure
    .input(z.discriminatedUnion('type', [
      z.object({
        type: z.literal('email'),
        email: z.string().email(),
      }),
      z.object({
        type: z.literal('phone'),
        phone: z.string().regex(/^\+?[1-9]\d{1,14}$/),
      }),
    ]))
    .mutation(({ input }) => {
      if (input.type === 'email') {
        // input.email is available
        return { method: 'email', value: input.email };
      } else {
        // input.phone is available
        return { method: 'phone', value: input.phone };
      }
    }),
});
```

✅ **Good**: Strong input validation
```typescript
// ✅ Validates email format, length, etc.
createUser: publicProcedure
  .input(z.object({
    email: z.string().email(),
    name: z.string().min(1).max(100),
    age: z.number().min(0).max(150),
  }))
  .mutation(({ input }) => {
    // input is fully validated
  }),
```

❌ **Bad**: No input validation
```typescript
// ❌ No validation, accepts anything
createUser: publicProcedure
  .mutation(({ input }: any) => {
    // input could be anything!
    db.user.create({ data: input });
  }),
```

### Output Validation

Validate procedure output to ensure consistency:

```typescript
export const apiRouter = router({
  // Output validation with Zod
  getUser: publicProcedure
    .input(z.string())
    .output(z.object({
      id: z.string(),
      email: z.string().email(),
      name: z.string(),
      createdAt: z.date(),
    }))
    .query(async ({ input }) => {
      const user = await db.user.findUnique({
        where: { id: input },
      });

      if (!user) {
        throw new TRPCError({ code: 'NOT_FOUND' });
      }

      // Output must match schema
      return {
        id: user.id,
        email: user.email,
        name: user.name,
        createdAt: user.createdAt,
      };
    }),
});
```

---

## 🛡️ Middleware (Authorization & Logging)

### Authentication Middleware

Create protected procedures that require authentication:

```typescript
// server/trpc.ts
import { initTRPC, TRPCError } from '@trpc/server';
import type { Context } from './context';

const t = initTRPC.context<Context>().create();

// Public procedure (no auth)
export const publicProcedure = t.procedure;

// Protected procedure (requires auth)
export const protectedProcedure = t.procedure.use(async ({ ctx, next }) => {
  if (!ctx.session?.user) {
    throw new TRPCError({
      code: 'UNAUTHORIZED',
      message: 'You must be logged in',
    });
  }

  return next({
    ctx: {
      // User is now non-nullable
      session: {
        ...ctx.session,
        user: ctx.session.user,
      },
    },
  });
});

// Admin procedure (requires admin role)
export const adminProcedure = protectedProcedure.use(async ({ ctx, next }) => {
  if (ctx.session.user.role !== 'ADMIN') {
    throw new TRPCError({
      code: 'FORBIDDEN',
      message: 'You must be an admin',
    });
  }

  return next({
    ctx: {
      session: ctx.session,
    },
  });
});
```

### Authorization Middleware

Check permissions for specific resources:

```typescript
// Check if user owns a resource
export const ownershipProcedure = protectedProcedure
  .input(z.object({ postId: z.string() }))
  .use(async ({ ctx, input, next }) => {
    const post = await db.post.findUnique({
      where: { id: input.postId },
    });

    if (!post) {
      throw new TRPCError({
        code: 'NOT_FOUND',
        message: 'Post not found',
      });
    }

    if (post.authorId !== ctx.session.user.id) {
      throw new TRPCError({
        code: 'FORBIDDEN',
        message: 'You do not own this post',
      });
    }

    return next({
      ctx: {
        post, // Add post to context
      },
    });
  });

// Usage
export const postRouter = router({
  update: ownershipProcedure
    .input(z.object({
      postId: z.string(),
      title: z.string().optional(),
      content: z.string().optional(),
    }))
    .mutation(async ({ ctx, input }) => {
      // ctx.post is available and ownership is verified
      return await db.post.update({
        where: { id: input.postId },
        data: {
          title: input.title,
          content: input.content,
        },
      });
    }),
});
```

### Organization Membership Middleware

Verify user belongs to an organization:

```typescript
export const organizationProcedure = protectedProcedure
  .input(z.object({ organizationId: z.string() }))
  .use(async ({ ctx, input, next }) => {
    const membership = await db.membership.findFirst({
      where: {
        organizationId: input.organizationId,
        userId: ctx.session.user.id,
      },
      include: {
        organization: true,
      },
    });

    if (!membership) {
      throw new TRPCError({
        code: 'FORBIDDEN',
        message: 'You are not a member of this organization',
      });
    }

    return next({
      ctx: {
        organization: membership.organization,
        membership,
      },
    });
  });

// Usage
export const orgRouter = router({
  createProject: organizationProcedure
    .input(z.object({
      organizationId: z.string(),
      name: z.string(),
    }))
    .mutation(async ({ ctx, input }) => {
      // Organization membership verified
      return await db.project.create({
        data: {
          name: input.name,
          organizationId: ctx.organization.id,
        },
      });
    }),
});
```

### Logging Middleware

Track request timing and errors:

```typescript
// server/trpc.ts
export const loggedProcedure = publicProcedure.use(async ({ path, type, next }) => {
  const start = Date.now();

  console.log(`📥 ${type.toUpperCase()} ${path} - Started`);

  const result = await next();

  const duration = Date.now() - start;

  if (result.ok) {
    console.log(`✅ ${type.toUpperCase()} ${path} - ${duration}ms`);
  } else {
    console.error(`❌ ${type.toUpperCase()} ${path} - ${duration}ms - Error: ${result.error.message}`);
  }

  return result;
});
```

### Rate Limiting Middleware

Prevent abuse with rate limiting:

```typescript
import { Ratelimit } from '@upstash/ratelimit';
import { Redis } from '@upstash/redis';

const ratelimit = new Ratelimit({
  redis: Redis.fromEnv(),
  limiter: Ratelimit.slidingWindow(10, '10 s'),
});

export const rateLimitedProcedure = publicProcedure.use(async ({ ctx, next }) => {
  if (!ctx.req) {
    throw new TRPCError({ code: 'INTERNAL_SERVER_ERROR' });
  }

  const ip = ctx.req.headers.get('x-forwarded-for') ?? 'unknown';
  const { success, remaining } = await ratelimit.limit(ip);

  if (!success) {
    throw new TRPCError({
      code: 'TOO_MANY_REQUESTS',
      message: 'Rate limit exceeded',
    });
  }

  return next({
    ctx: {
      rateLimit: { remaining },
    },
  });
});
```

### Context Extension

Add data to context through middleware:

```typescript
// Add database to context
export const dbProcedure = publicProcedure.use(({ next }) => {
  return next({
    ctx: {
      db: prisma,
    },
  });
});

// Add request metadata
export const metaProcedure = publicProcedure.use(({ ctx, next }) => {
  return next({
    ctx: {
      requestTime: new Date(),
      userAgent: ctx.req?.headers.get('user-agent'),
    },
  });
});
```

### Chaining Middleware

Combine multiple middleware:

```typescript
// Combine logging + auth + rate limiting
export const protectedApiProcedure = publicProcedure
  .use(loggerMiddleware)
  .use(rateLimitMiddleware)
  .use(authMiddleware);

// Usage
export const apiRouter = router({
  sensitiveAction: protectedApiProcedure
    .input(z.string())
    .mutation(async ({ input, ctx }) => {
      // All middleware have run:
      // - Request is logged
      // - Rate limit checked
      // - User authenticated
    }),
});
```

✅ **Good**: Reusable middleware
```typescript
// ✅ Create reusable base procedures
export const authedProcedure = publicProcedure.use(authMiddleware);
export const adminProcedure = authedProcedure.use(adminMiddleware);
```

❌ **Bad**: Repeated middleware logic
```typescript
// ❌ Don't repeat auth checks everywhere
getUserData: publicProcedure.query(({ ctx }) => {
  if (!ctx.session) throw new TRPCError({ code: 'UNAUTHORIZED' });
  // ...
}),

updateUser: publicProcedure.mutation(({ ctx }) => {
  if (!ctx.session) throw new TRPCError({ code: 'UNAUTHORIZED' });
  // ...
}),
```

---

## 🎯 Context (Request-Scoped Data)

### Creating Context

Context is created per-request and available in all procedures:

```typescript
// server/context.ts
import type { CreateNextContextOptions } from '@trpc/server/adapters/next';
import { getServerSession } from 'next-auth';
import { prisma } from './db';

export async function createContext(opts: CreateNextContextOptions) {
  // Get session from Next-Auth
  const session = await getServerSession(authOptions);

  return {
    session,
    prisma,
    req: opts.req,
    res: opts.res,
  };
}

export type Context = Awaited<ReturnType<typeof createContext>>;
```

### Using Context in Procedures

Access context data in any procedure:

```typescript
export const userRouter = router({
  getCurrentUser: publicProcedure.query(async ({ ctx }) => {
    if (!ctx.session?.user) {
      throw new TRPCError({ code: 'UNAUTHORIZED' });
    }

    return await ctx.prisma.user.findUnique({
      where: { id: ctx.session.user.id },
    });
  }),

  updateProfile: publicProcedure
    .input(z.object({
      name: z.string(),
      bio: z.string(),
    }))
    .mutation(async ({ ctx, input }) => {
      if (!ctx.session?.user) {
        throw new TRPCError({ code: 'UNAUTHORIZED' });
      }

      return await ctx.prisma.user.update({
        where: { id: ctx.session.user.id },
        data: input,
      });
    }),
});
```

### Inner and Outer Context

Separate request-independent and request-dependent context:

```typescript
// server/context.ts

// Inner context: request-independent (for testing/SSR)
export async function createContextInner(opts?: { session: Session | null }) {
  return {
    session: opts?.session ?? null,
    prisma,
  };
}

// Outer context: request-dependent
export async function createContext(opts: CreateNextContextOptions) {
  const session = await getServerSession(authOptions);

  const innerCtx = await createContextInner({ session });

  return {
    ...innerCtx,
    req: opts.req,
    res: opts.res,
  };
}

// Type from inner context (always available)
export type Context = Awaited<ReturnType<typeof createContextInner>>;
```

### Database in Context

Provide database access to all procedures:

```typescript
// server/context.ts
import { PrismaClient } from '@prisma/client';

const globalForPrisma = global as unknown as {
  prisma: PrismaClient | undefined;
};

export const prisma =
  globalForPrisma.prisma ??
  new PrismaClient({
    log: process.env.NODE_ENV === 'development' ? ['query', 'error', 'warn'] : ['error'],
  });

if (process.env.NODE_ENV !== 'production') {
  globalForPrisma.prisma = prisma;
}

export async function createContext() {
  return {
    prisma,
  };
}
```

### Request/Response Access

Access raw request/response objects:

```typescript
export async function createContext(opts: CreateNextContextOptions) {
  return {
    req: opts.req,
    res: opts.res,
  };
}

// Use in procedures
export const cookieRouter = router({
  setCookie: publicProcedure
    .input(z.object({
      name: z.string(),
      value: z.string(),
    }))
    .mutation(({ ctx, input }) => {
      ctx.res.setHeader('Set-Cookie', `${input.name}=${input.value}; Path=/`);
      return { success: true };
    }),

  getCookie: publicProcedure
    .input(z.string())
    .query(({ ctx, input }) => {
      const cookies = ctx.req.headers.cookie ?? '';
      const value = cookies
        .split('; ')
        .find(row => row.startsWith(`${input}=`))
        ?.split('=')[1];
      return value;
    }),
});
```

✅ **Good**: Shared resources in context
```typescript
// ✅ Database, session in context
export async function createContext() {
  return {
    prisma,
    session: await getSession(),
  };
}
```

❌ **Bad**: Creating DB connection per procedure
```typescript
// ❌ Don't create connections in procedures
getUserById: publicProcedure.query(async () => {
  const prisma = new PrismaClient(); // ❌ Wasteful!
  return await prisma.user.findFirst();
});
```

---

## 🎨 Client Setup (React Query Integration)

### Installing Dependencies

```bash
npm install @trpc/client @trpc/server @trpc/react-query @tanstack/react-query
```

### Next.js App Router Client Setup

```typescript
// app/providers.tsx
'use client';

import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { httpBatchLink } from '@trpc/client';
import { createTRPCReact } from '@trpc/react-query';
import { useState } from 'react';
import { type AppRouter } from '@/server/routers/_app';

export const trpc = createTRPCReact<AppRouter>();

export function TRPCProvider({ children }: { children: React.ReactNode }) {
  const [queryClient] = useState(() => new QueryClient({
    defaultOptions: {
      queries: {
        staleTime: 5 * 1000,
        refetchOnWindowFocus: false,
      },
    },
  }));

  const [trpcClient] = useState(() =>
    trpc.createClient({
      links: [
        httpBatchLink({
          url: `${process.env.NEXT_PUBLIC_APP_URL}/api/trpc`,
          headers() {
            return {
              'x-trpc-source': 'client',
            };
          },
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

```typescript
// app/layout.tsx
import { TRPCProvider } from './providers';

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <TRPCProvider>{children}</TRPCProvider>
      </body>
    </html>
  );
}
```

### Using Queries

```typescript
'use client';

import { trpc } from '@/app/providers';

export function UserProfile() {
  // Simple query
  const { data, isLoading, error } = trpc.user.getCurrentUser.useQuery();

  // Query with input
  const { data: user } = trpc.user.getById.useQuery('user-id-123');

  // Query with complex input
  const { data: posts } = trpc.post.list.useQuery({
    userId: 'user-id',
    published: true,
  });

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;

  return <div>Hello {data?.name}!</div>;
}
```

### Using Mutations

```typescript
'use client';

import { trpc } from '@/app/providers';

export function CreateUserForm() {
  const utils = trpc.useUtils();

  const createUser = trpc.user.create.useMutation({
    onSuccess(data) {
      // Invalidate and refetch
      utils.user.list.invalidate();
      
      // Or update cache directly
      utils.user.getById.setData(data.id, data);
    },
    onError(error) {
      console.error('Failed to create user:', error);
    },
  });

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);

    createUser.mutate({
      email: formData.get('email') as string,
      name: formData.get('name') as string,
    });
  };

  return (
    <form onSubmit={handleSubmit}>
      <input name="email" type="email" required />
      <input name="name" type="text" required />
      <button type="submit" disabled={createUser.isPending}>
        {createUser.isPending ? 'Creating...' : 'Create User'}
      </button>
      {createUser.error && <p>Error: {createUser.error.message}</p>}
    </form>
  );
}
```

### Optimistic Updates

Update UI immediately before server responds:

```typescript
export function TodoList() {
  const utils = trpc.useUtils();

  const toggleTodo = trpc.todo.toggle.useMutation({
    onMutate: async (id) => {
      // Cancel outgoing fetches
      await utils.todo.list.cancel();

      // Snapshot previous value
      const prevData = utils.todo.list.getData();

      // Optimistically update
      utils.todo.list.setData(undefined, (old) =>
        old?.map((todo) =>
          todo.id === id ? { ...todo, completed: !todo.completed } : todo
        )
      );

      return { prevData };
    },
    onError: (err, id, context) => {
      // Rollback on error
      utils.todo.list.setData(undefined, context?.prevData);
    },
    onSettled: () => {
      // Refetch after error or success
      utils.todo.list.invalidate();
    },
  });

  const { data: todos } = trpc.todo.list.useQuery();

  return (
    <ul>
      {todos?.map((todo) => (
        <li key={todo.id}>
          <input
            type="checkbox"
            checked={todo.completed}
            onChange={() => toggleTodo.mutate(todo.id)}
          />
          {todo.title}
        </li>
      ))}
    </ul>
  );
}
```

### Infinite Queries

Load data with pagination:

```typescript
export function InfinitePostList() {
  const {
    data,
    fetchNextPage,
    hasNextPage,
    isFetchingNextPage,
  } = trpc.post.listInfinite.useInfiniteQuery(
    { limit: 10 },
    {
      getNextPageParam: (lastPage) => lastPage.nextCursor,
    }
  );

  return (
    <div>
      {data?.pages.map((page) =>
        page.items.map((post) => (
          <article key={post.id}>
            <h2>{post.title}</h2>
            <p>{post.content}</p>
          </article>
        ))
      )}

      {hasNextPage && (
        <button onClick={() => fetchNextPage()} disabled={isFetchingNextPage}>
          {isFetchingNextPage ? 'Loading more...' : 'Load More'}
        </button>
      )}
    </div>
  );
}
```

✅ **Good**: Proper client setup
```typescript
// ✅ Batching requests
links: [
  httpBatchLink({
    url: '/api/trpc',
  }),
],
```

❌ **Bad**: No batching
```typescript
// ❌ Each request is separate (slower)
links: [
  httpLink({
    url: '/api/trpc',
  }),
],
```

---

## ⚠️ Error Handling

### TRPCError Types

tRPC provides standard error codes:

```typescript
import { TRPCError } from '@trpc/server';

// UNAUTHORIZED - User not authenticated
throw new TRPCError({
  code: 'UNAUTHORIZED',
  message: 'You must be logged in',
});

// FORBIDDEN - User not authorized
throw new TRPCError({
  code: 'FORBIDDEN',
  message: 'You do not have permission',
});

// NOT_FOUND - Resource not found
throw new TRPCError({
  code: 'NOT_FOUND',
  message: 'User not found',
});

// BAD_REQUEST - Invalid input
throw new TRPCError({
  code: 'BAD_REQUEST',
  message: 'Invalid email format',
});

// CONFLICT - Resource conflict
throw new TRPCError({
  code: 'CONFLICT',
  message: 'Email already exists',
});

// INTERNAL_SERVER_ERROR - Server error
throw new TRPCError({
  code: 'INTERNAL_SERVER_ERROR',
  message: 'Something went wrong',
});

// TOO_MANY_REQUESTS - Rate limit exceeded
throw new TRPCError({
  code: 'TOO_MANY_REQUESTS',
  message: 'Rate limit exceeded',
});

// TIMEOUT - Request timeout
throw new TRPCError({
  code: 'TIMEOUT',
  message: 'Request took too long',
});
```

### Custom Error Data

Add custom data to errors:

```typescript
export const userRouter = router({
  create: publicProcedure
    .input(z.object({
      email: z.string().email(),
      name: z.string(),
    }))
    .mutation(async ({ input }) => {
      const existing = await db.user.findUnique({
        where: { email: input.email },
      });

      if (existing) {
        throw new TRPCError({
          code: 'CONFLICT',
          message: 'User already exists',
          cause: {
            field: 'email',
            value: input.email,
          },
        });
      }

      return await db.user.create({ data: input });
    }),
});
```

### Error Formatting

Format errors for client consumption:

```typescript
// server/trpc.ts
import { initTRPC } from '@trpc/server';
import { ZodError } from 'zod';

const t = initTRPC.create({
  errorFormatter({ shape, error }) {
    return {
      ...shape,
      data: {
        ...shape.data,
        zodError:
          error.cause instanceof ZodError
            ? error.cause.flatten()
            : null,
        customField: 'custom data',
      },
    };
  },
});
```

### Client-Side Error Handling

Handle errors in React components:

```typescript
export function UserForm() {
  const createUser = trpc.user.create.useMutation({
    onError(error) {
      // Check error code
      if (error.data?.code === 'CONFLICT') {
        toast.error('Email already exists');
      } else if (error.data?.code === 'UNAUTHORIZED') {
        toast.error('Please log in');
      } else {
        toast.error('Something went wrong');
      }

      // Access Zod errors
      if (error.data?.zodError) {
        const fieldErrors = error.data.zodError.fieldErrors;
        console.log('Validation errors:', fieldErrors);
      }
    },
  });

  return (
    <form onSubmit={(e) => {
      e.preventDefault();
      createUser.mutate({ email: '...', name: '...' });
    }}>
      {/* Form fields */}
      {createUser.error && (
        <div className="error">
          {createUser.error.message}
        </div>
      )}
    </form>
  );
}
```

✅ **Good**: Specific error codes
```typescript
// ✅ Clear error codes
if (!user) {
  throw new TRPCError({
    code: 'NOT_FOUND',
    message: 'User not found',
  });
}
```

❌ **Bad**: Generic errors
```typescript
// ❌ Unclear error
if (!user) {
  throw new Error('Not found');
}
```

---

## 🔒 Type Safety (End-to-End)

### Automatic Type Inference

tRPC infers types automatically:

```typescript
// server/routers/user.ts
export const userRouter = router({
  getById: publicProcedure
    .input(z.string())
    .query(async ({ input }) => {
      return await db.user.findUnique({
        where: { id: input },
        select: {
          id: true,
          name: true,
          email: true,
          createdAt: true,
        },
      });
    }),
});
```

```typescript
// client/components/User.tsx
import { trpc } from '@/app/providers';

export function UserProfile({ userId }: { userId: string }) {
  const { data } = trpc.user.getById.useQuery(userId);
  
  // TypeScript knows exact shape:
  // data: { id: string; name: string; email: string; createdAt: Date } | undefined
  
  return <div>{data?.name}</div>; // ✅ Autocomplete works!
}
```

### AppRouter Type Export

Share types between server and client:

```typescript
// server/routers/_app.ts
import { router } from '../trpc';
import { userRouter } from './user';
import { postRouter } from './post';

export const appRouter = router({
  user: userRouter,
  post: postRouter,
});

// ⚠️ CRITICAL: Export only the TYPE, not the implementation
export type AppRouter = typeof appRouter;
```

```typescript
// app/providers.tsx
import { type AppRouter } from '@/server/routers/_app';
import { createTRPCReact } from '@trpc/react-query';

// Client gets full type safety
export const trpc = createTRPCReact<AppRouter>();
```

### Sharing Zod Schemas

Reuse validation schemas between server and client:

```typescript
// shared/schemas/user.ts
import { z } from 'zod';

export const createUserSchema = z.object({
  email: z.string().email('Invalid email'),
  name: z.string().min(1, 'Name required'),
  password: z.string().min(8, 'Password must be 8+ characters'),
});

export type CreateUserInput = z.infer<typeof createUserSchema>;
```

```typescript
// server/routers/user.ts
import { createUserSchema } from '@/shared/schemas/user';

export const userRouter = router({
  create: publicProcedure
    .input(createUserSchema)
    .mutation(async ({ input }) => {
      // input is typed as CreateUserInput
      return await db.user.create({ data: input });
    }),
});
```

```typescript
// app/components/UserForm.tsx
import { createUserSchema, type CreateUserInput } from '@/shared/schemas/user';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';

export function UserForm() {
  const form = useForm<CreateUserInput>({
    resolver: zodResolver(createUserSchema),
  });

  const createUser = trpc.user.create.useMutation();

  return (
    <form onSubmit={form.handleSubmit((data) => createUser.mutate(data))}>
      {/* Form fields with validation */}
    </form>
  );
}
```

### Type Inference Helpers

Extract types from procedures:

```typescript
import type { inferProcedureInput, inferProcedureOutput } from '@trpc/server';
import type { AppRouter } from '@/server/routers/_app';

// Infer input type
type CreateUserInput = inferProcedureInput<AppRouter['user']['create']>;

// Infer output type
type User = inferProcedureOutput<AppRouter['user']['getById']>;

// Use in your code
const user: User = {
  id: '1',
  name: 'John',
  email: 'john@example.com',
  createdAt: new Date(),
};
```

✅ **Good**: Full type safety
```typescript
// ✅ Types flow automatically
const { data } = trpc.user.getById.useQuery(userId);
data?.name; // TypeScript knows this exists
```

❌ **Bad**: Type assertions
```typescript
// ❌ Don't use 'any' or assertions
const { data } = trpc.user.getById.useQuery(userId) as any;
data.name; // No type safety!
```

---

## 📚 Additional Resources

- **Official Documentation**: https://trpc.io/docs
- **GitHub Repository**: https://github.com/trpc/trpc
- **Examples**: https://github.com/trpc/examples-next-app-dir
- **Discord Community**: https://trpc.io/discord

---

## 🎯 Best Practices Summary

### ✅ Do This

- ✅ Use `publicProcedure` for public endpoints
- ✅ Create reusable base procedures (`authedProcedure`, `adminProcedure`)
- ✅ Validate all inputs with Zod
- ✅ Organize routers by feature/domain
- ✅ Use middleware for cross-cutting concerns
- ✅ Leverage context for shared resources
- ✅ Enable request batching on client
- ✅ Handle errors with specific codes
- ✅ Export only router types, not implementations

### ❌ Avoid This

- ❌ Multiple tRPC instances
- ❌ Monolithic routers with 50+ procedures
- ❌ Side effects in query procedures
- ❌ Skipping input validation
- ❌ Repeated auth checks in every procedure
- ❌ Creating database connections per procedure
- ❌ Using `any` types
- ❌ Generic error messages
- ❌ Importing server code on client

---

**End of tRPC Skill** • Last Updated: 2025-11-16
