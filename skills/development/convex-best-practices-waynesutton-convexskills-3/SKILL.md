---
name: convex-best-practices
description: Guidelines for building production-ready Convex apps covering function organization, query patterns, validation, TypeScript usage, error handling, and the Zen of Convex design philosophy
---

# Convex Best Practices

Build production-ready Convex applications by following established patterns for function organization, query optimization, validation, TypeScript usage, and error handling.

## Code Quality

All patterns in this skill comply with `@convex-dev/eslint-plugin`. Install it for build-time validation:

```bash
npm i @convex-dev/eslint-plugin --save-dev
```

```js
// eslint.config.js
import { defineConfig } from "eslint/config";
import convexPlugin from "@convex-dev/eslint-plugin";

export default defineConfig([
  ...convexPlugin.configs.recommended,
]);
```

The plugin enforces four rules:

| Rule                                | What it enforces                  |
| ----------------------------------- | --------------------------------- |
| `no-old-registered-function-syntax` | Object syntax with `handler`      |
| `require-argument-validators`       | `args: {}` on all functions       |
| `explicit-table-ids`                | Table name in db operations       |
| `import-wrong-runtime`              | No Node imports in Convex runtime |

Docs: https://docs.convex.dev/eslint

## Documentation Sources

Before implementing, do not assume; fetch the latest documentation:

- Primary: https://docs.convex.dev/understanding/best-practices/
- Error Handling: https://docs.convex.dev/functions/error-handling
- Write Conflicts: https://docs.convex.dev/error#1
- For broader context: https://docs.convex.dev/llms.txt

## Instructions

### The Zen of Convex

1. **Convex manages the hard parts** - Let Convex handle caching, real-time sync, and consistency
2. **Functions are the API** - Design your functions as your application's interface
3. **Schema is truth** - Define your data model explicitly in schema.ts
4. **TypeScript everywhere** - Leverage end-to-end type safety
5. **Queries are reactive** - Think in terms of subscriptions, not requests

### Function Organization

Organize your Convex functions by domain:

```typescript
// convex/users.ts - User-related functions
import { query, mutation } from "./_generated/server";
import { v } from "convex/values";

export const get = query({
  args: { userId: v.id("users") },
  returns: v.union(
    v.object({
      _id: v.id("users"),
      _creationTime: v.number(),
      name: v.string(),
      email: v.string(),
    }),
    v.null(),
  ),
  handler: async (ctx, args) => {
    return await ctx.db.get("users", args.userId);
  },
});
```

### Argument and Return Validation

Always define validators for arguments AND return types:

```typescript
export const createTask = mutation({
  args: {
    title: v.string(),
    description: v.optional(v.string()),
    priority: v.union(v.literal("low"), v.literal("medium"), v.literal("high")),
  },
  returns: v.id("tasks"),
  handler: async (ctx, args) => {
    return await ctx.db.insert("tasks", {
      title: args.title,
      description: args.description,
      priority: args.priority,
      completed: false,
      createdAt: Date.now(),
    });
  },
});
```

### Query Patterns

Use indexes instead of filters for efficient queries:

```typescript
// Schema with index
export default defineSchema({
  tasks: defineTable({
    userId: v.id("users"),
    status: v.string(),
    createdAt: v.number(),
  })
    .index("by_user", ["userId"])
    .index("by_user_and_status", ["userId", "status"]),
});

// Query using index
export const getTasksByUser = query({
  args: { userId: v.id("users") },
  returns: v.array(
    v.object({
      _id: v.id("tasks"),
      _creationTime: v.number(),
      userId: v.id("users"),
      status: v.string(),
      createdAt: v.number(),
    }),
  ),
  handler: async (ctx, args) => {
    return await ctx.db
      .query("tasks")
      .withIndex("by_user", (q) => q.eq("userId", args.userId))
      .order("desc")
      .collect();
  },
});
```

### Error Handling

Use ConvexError for user-facing errors:

```typescript
import { ConvexError } from "convex/values";

export const updateTask = mutation({
  args: {
    taskId: v.id("tasks"),
    title: v.string(),
  },
  returns: v.null(),
  handler: async (ctx, args) => {
    const task = await ctx.db.get("tasks", args.taskId);

    if (!task) {
      throw new ConvexError({
        code: "NOT_FOUND",
        message: "Task not found",
      });
    }

    await ctx.db.patch("tasks", args.taskId, { title: args.title });
    return null;
  },
});
```

### Avoiding Write Conflicts (Optimistic Concurrency Control)

Convex uses OCC. Follow these patterns to minimize conflicts:

```typescript
// GOOD: Make mutations idempotent
export const completeTask = mutation({
  args: { taskId: v.id("tasks") },
  returns: v.null(),
  handler: async (ctx, args) => {
    const task = await ctx.db.get("tasks", args.taskId);

    // Early return if already complete (idempotent)
    if (!task || task.status === "completed") {
      return null;
    }

    await ctx.db.patch("tasks", args.taskId, {
      status: "completed",
      completedAt: Date.now(),
    });
    return null;
  },
});

// GOOD: Patch directly without reading first when possible
export const updateNote = mutation({
  args: { id: v.id("notes"), content: v.string() },
  returns: v.null(),
  handler: async (ctx, args) => {
    // Patch directly - ctx.db.patch throws if document doesn't exist
    await ctx.db.patch("notes", args.id, { content: args.content });
    return null;
  },
});

// GOOD: Use Promise.all for parallel independent updates
export const reorderItems = mutation({
  args: { itemIds: v.array(v.id("items")) },
  returns: v.null(),
  handler: async (ctx, args) => {
    const updates = args.itemIds.map((id, index) =>
      ctx.db.patch("items", id, { order: index }),
    );
    await Promise.all(updates);
    return null;
  },
});
```

### TypeScript Best Practices

```typescript
import { Id, Doc } from "./_generated/dataModel";

// Use Id type for document references
type UserId = Id<"users">;

// Use Doc type for full documents
type User = Doc<"users">;

// Define Record types properly
const userScores: Record<Id<"users">, number> = {};
```

### Internal vs Public Functions

```typescript
// Public function - exposed to clients
export const getUser = query({
  args: { userId: v.id("users") },
  returns: v.union(
    v.null(),
    v.object({
      /* ... */
    }),
  ),
  handler: async (ctx, args) => {
    // ...
  },
});

// Internal function - only callable from other Convex functions
export const _updateUserStats = internalMutation({
  args: { userId: v.id("users") },
  returns: v.null(),
  handler: async (ctx, args) => {
    // ...
  },
});
```

## Examples

### Complete CRUD Pattern

```typescript
// convex/tasks.ts
import { query, mutation } from "./_generated/server";
import { v } from "convex/values";
import { ConvexError } from "convex/values";

const taskValidator = v.object({
  _id: v.id("tasks"),
  _creationTime: v.number(),
  title: v.string(),
  completed: v.boolean(),
  userId: v.id("users"),
});

export const list = query({
  args: { userId: v.id("users") },
  returns: v.array(taskValidator),
  handler: async (ctx, args) => {
    return await ctx.db
      .query("tasks")
      .withIndex("by_user", (q) => q.eq("userId", args.userId))
      .collect();
  },
});

export const create = mutation({
  args: {
    title: v.string(),
    userId: v.id("users"),
  },
  returns: v.id("tasks"),
  handler: async (ctx, args) => {
    return await ctx.db.insert("tasks", {
      title: args.title,
      completed: false,
      userId: args.userId,
    });
  },
});

export const update = mutation({
  args: {
    taskId: v.id("tasks"),
    title: v.optional(v.string()),
    completed: v.optional(v.boolean()),
  },
  returns: v.null(),
  handler: async (ctx, args) => {
    const { taskId, ...updates } = args;

    // Remove undefined values
    const cleanUpdates = Object.fromEntries(
      Object.entries(updates).filter(([_, v]) => v !== undefined),
    );

    if (Object.keys(cleanUpdates).length > 0) {
      await ctx.db.patch("tasks", taskId, cleanUpdates);
    }
    return null;
  },
});

export const remove = mutation({
  args: { taskId: v.id("tasks") },
  returns: v.null(),
  handler: async (ctx, args) => {
    await ctx.db.delete("tasks", args.taskId);
    return null;
  },
});
```

## Best Practices

- Never run `npx convex deploy` unless explicitly instructed
- Never run any git commands unless explicitly instructed
- Always define return validators for functions
- Use indexes for all queries that filter data
- Make mutations idempotent to handle retries gracefully
- Use ConvexError for user-facing error messages
- Organize functions by domain (users.ts, tasks.ts, etc.)
- Use internal functions for sensitive operations
- Leverage TypeScript's Id and Doc types

## Common Pitfalls

1. **Using filter instead of withIndex** - Always define indexes and use withIndex
2. **Missing return validators** - Always specify the returns field
3. **Non-idempotent mutations** - Check current state before updating
4. **Reading before patching unnecessarily** - Patch directly when possible
5. **Not handling null returns** - Document IDs might not exist

## References

- Convex Documentation: https://docs.convex.dev/
- Convex LLMs.txt: https://docs.convex.dev/llms.txt
- Best Practices: https://docs.convex.dev/understanding/best-practices/
- Error Handling: https://docs.convex.dev/functions/error-handling
- Write Conflicts: https://docs.convex.dev/error#1
