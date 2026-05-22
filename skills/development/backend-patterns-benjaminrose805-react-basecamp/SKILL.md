---
name: backend-patterns
description: Backend architecture patterns, API design, database optimization, and server-side best practices for Next.js API routes and tRPC.
---

# Backend Development Patterns

Backend architecture patterns and best practices for Next.js and tRPC applications.

## When Used

| Agent      | Phase     |
| ---------- | --------- |
| code-agent | IMPLEMENT |

## API Design Patterns

### tRPC Router Structure

```typescript
// src/server/routers/workItem.ts
import { z } from "zod";
import { router, publicProcedure, protectedProcedure } from "../trpc";
import { TRPCError } from "@trpc/server";

export const workItemRouter = router({
  list: publicProcedure
    .input(
      z.object({
        status: z.enum(["open", "in_progress", "done", "blocked"]).optional(),
        limit: z.number().min(1).max(100).default(20),
        cursor: z.string().optional(),
      })
    )
    .query(async ({ input, ctx }) => {
      const items = await ctx.db.workItem.findMany({
        where: input.status ? { status: input.status } : undefined,
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

  create: protectedProcedure
    .input(
      z.object({
        title: z.string().min(1).max(200),
        description: z.string().optional(),
      })
    )
    .mutation(async ({ input, ctx }) => {
      return ctx.db.workItem.create({
        data: {
          ...input,
          userId: ctx.session.user.id,
        },
      });
    }),

  getById: publicProcedure
    .input(z.object({ id: z.string() }))
    .query(async ({ input, ctx }) => {
      const item = await ctx.db.workItem.findUnique({
        where: { id: input.id },
      });

      if (!item) {
        throw new TRPCError({
          code: "NOT_FOUND",
          message: "Work item not found",
        });
      }

      return item;
    }),
});
```

### Repository Pattern

```typescript
// src/lib/repositories/workItem.ts
import { db } from "@/lib/db";
import type { WorkItem, Prisma } from "@prisma/client";

export const workItemRepository = {
  findById: (id: string) => db.workItem.findUnique({ where: { id } }),

  findMany: (filters?: Prisma.WorkItemWhereInput) =>
    db.workItem.findMany({
      where: filters,
      orderBy: { createdAt: "desc" },
    }),

  create: (data: Prisma.WorkItemCreateInput) => db.workItem.create({ data }),

  update: (id: string, data: Prisma.WorkItemUpdateInput) =>
    db.workItem.update({ where: { id }, data }),

  delete: (id: string) => db.workItem.delete({ where: { id } }),
};
```

### Service Layer Pattern

```typescript
// src/lib/services/workItemService.ts
import { workItemRepository } from "../repositories/workItem";
import type { CreateWorkItemDto, UpdateWorkItemDto } from "../types";

export const workItemService = {
  async createWithValidation(data: CreateWorkItemDto, userId: string) {
    // Business logic validation
    if (data.dueDate && data.dueDate < new Date()) {
      throw new Error("Due date cannot be in the past");
    }

    return workItemRepository.create({
      ...data,
      userId,
      status: "open",
    });
  },

  async updateStatus(id: string, status: string, userId: string) {
    const item = await workItemRepository.findById(id);

    if (!item) {
      throw new Error("Work item not found");
    }

    if (item.userId !== userId) {
      throw new Error("Not authorized");
    }

    return workItemRepository.update(id, { status });
  },
};
```

## Database Patterns (Prisma)

### Query Optimization

```typescript
// Select only needed fields
const items = await db.workItem.findMany({
  select: {
    id: true,
    title: true,
    status: true,
    createdAt: true,
  },
  where: { status: "open" },
  orderBy: { createdAt: "desc" },
  take: 20,
});

// Include relations efficiently
const itemsWithTasks = await db.workItem.findMany({
  include: {
    tasks: {
      select: { id: true, title: true, completed: true },
    },
    user: {
      select: { id: true, name: true },
    },
  },
});
```

### N+1 Query Prevention

```typescript
// BAD: N+1 query problem
const items = await db.workItem.findMany();
for (const item of items) {
  item.user = await db.user.findUnique({ where: { id: item.userId } });
}

// GOOD: Include relation
const items = await db.workItem.findMany({
  include: { user: true },
});

// GOOD: Batch fetch with findMany
const items = await db.workItem.findMany();
const userIds = [...new Set(items.map((i) => i.userId))];
const users = await db.user.findMany({
  where: { id: { in: userIds } },
});
const userMap = new Map(users.map((u) => [u.id, u]));
items.forEach((item) => {
  item.user = userMap.get(item.userId);
});
```

### Transactions

```typescript
// Prisma transaction for atomicity
const result = await db.$transaction(async (tx) => {
  const workItem = await tx.workItem.create({
    data: { title: "New Item", userId },
  });

  await tx.task.createMany({
    data: tasks.map((task) => ({
      ...task,
      workItemId: workItem.id,
    })),
  });

  return workItem;
});
```

## Error Handling Patterns

### Centralized Error Handler

```typescript
import { TRPCError } from "@trpc/server";
import { ZodError } from "zod";

export function handleError(error: unknown): TRPCError {
  if (error instanceof TRPCError) {
    return error;
  }

  if (error instanceof ZodError) {
    return new TRPCError({
      code: "BAD_REQUEST",
      message: "Validation failed",
      cause: error,
    });
  }

  // Log unexpected errors
  console.error("Unexpected error:", error);

  return new TRPCError({
    code: "INTERNAL_SERVER_ERROR",
    message: "An unexpected error occurred",
  });
}
```

### Retry with Exponential Backoff

```typescript
async function fetchWithRetry<T>(
  fn: () => Promise<T>,
  maxRetries = 3
): Promise<T> {
  let lastError: Error;

  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (error) {
      lastError = error as Error;

      if (i < maxRetries - 1) {
        const delay = Math.pow(2, i) * 1000;
        await new Promise((resolve) => setTimeout(resolve, delay));
      }
    }
  }

  throw lastError!;
}
```

## Middleware Patterns

### tRPC Middleware

```typescript
// Authentication middleware
const isAuthed = t.middleware(({ ctx, next }) => {
  if (!ctx.session || !ctx.session.user) {
    throw new TRPCError({ code: "UNAUTHORIZED" });
  }
  return next({
    ctx: {
      session: { ...ctx.session, user: ctx.session.user },
    },
  });
});

export const protectedProcedure = t.procedure.use(isAuthed);

// Logging middleware
const logger = t.middleware(async ({ path, type, next }) => {
  const start = Date.now();
  const result = await next();
  const duration = Date.now() - start;
  console.log(`${type} ${path} - ${duration}ms`);
  return result;
});
```

## Rate Limiting

```typescript
import { Ratelimit } from "@upstash/ratelimit";
import { Redis } from "@upstash/redis";

const ratelimit = new Ratelimit({
  redis: Redis.fromEnv(),
  limiter: Ratelimit.slidingWindow(10, "10 s"),
  analytics: true,
});

// In tRPC middleware
const rateLimitMiddleware = t.middleware(async ({ ctx, next }) => {
  const ip = ctx.req?.headers["x-forwarded-for"] || "anonymous";
  const { success } = await ratelimit.limit(ip as string);

  if (!success) {
    throw new TRPCError({
      code: "TOO_MANY_REQUESTS",
      message: "Rate limit exceeded",
    });
  }

  return next();
});
```

## Background Jobs

### Simple Queue Pattern

```typescript
interface Job<T> {
  id: string;
  data: T;
  createdAt: Date;
}

class JobQueue<T> {
  private queue: Job<T>[] = [];
  private processing = false;

  async add(data: T): Promise<string> {
    const job: Job<T> = {
      id: crypto.randomUUID(),
      data,
      createdAt: new Date(),
    };
    this.queue.push(job);

    if (!this.processing) {
      this.process();
    }

    return job.id;
  }

  private async process(): Promise<void> {
    this.processing = true;

    while (this.queue.length > 0) {
      const job = this.queue.shift()!;
      try {
        await this.execute(job);
      } catch (error) {
        console.error(`Job ${job.id} failed:`, error);
      }
    }

    this.processing = false;
  }

  protected async execute(job: Job<T>): Promise<void> {
    // Override in subclass
  }
}
```

## Logging

### Structured Logging

```typescript
interface LogContext {
  userId?: string;
  requestId?: string;
  method?: string;
  path?: string;
  [key: string]: unknown;
}

function log(
  level: "info" | "warn" | "error",
  message: string,
  context?: LogContext
) {
  const entry = {
    timestamp: new Date().toISOString(),
    level,
    message,
    ...context,
  };

  if (level === "error") {
    console.error(JSON.stringify(entry));
  } else {
    console.log(JSON.stringify(entry));
  }
}

// Usage
log("info", "Work item created", {
  userId: ctx.session.user.id,
  workItemId: item.id,
});
```

## Best Practices

1. **Use tRPC for type-safe APIs** - End-to-end type safety
2. **Repository pattern** - Abstract data access
3. **Service layer** - Business logic separation
4. **Transactions** - Atomic operations
5. **Proper error handling** - TRPCError with appropriate codes
6. **Rate limiting** - Protect endpoints
7. **Structured logging** - JSON format for parsing
8. **N+1 prevention** - Include/batch queries
