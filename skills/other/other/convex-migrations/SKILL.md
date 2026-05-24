---
name: convex-migrations
displayName: Convex Migrations
description: Schema migration strategies for evolving applications including adding new fields, backfilling data, removing deprecated fields, index migrations, and zero-downtime migration patterns
version: 1.0.0
author: Convex
tags: [convex, migrations, schema, database, data-modeling]
---

# Convex Migrations

Evolve your Convex database schema safely with patterns for adding fields, backfilling data, removing deprecated fields, and maintaining zero-downtime deployments.

## Documentation Sources

Before implementing, do not assume; fetch the latest documentation:

- Primary: https://docs.convex.dev/database/schemas
- Schema Overview: https://docs.convex.dev/database
- Migration Patterns: https://stack.convex.dev/migrate-data-postgres-to-convex
- For broader context: https://docs.convex.dev/llms.txt

## Instructions

### Migration Philosophy

Convex handles schema evolution differently than traditional databases:

- No explicit migration files or commands
- Schema changes deploy instantly with `npx convex dev`
- Existing data is not automatically transformed
- Use optional fields and backfill mutations for safe migrations

### Adding New Fields

Start with optional fields, then backfill:

```typescript
// Step 1: Add optional field to schema
// convex/schema.ts
import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";

export default defineSchema({
  users: defineTable({
    name: v.string(),
    email: v.string(),
    // New field - start as optional
    avatarUrl: v.optional(v.string()),
  }),
});
```

```typescript
// Step 2: Update code to handle both cases
// convex/users.ts
import { query } from "./_generated/server";
import { v } from "convex/values";

export const getUser = query({
  args: { userId: v.id("users") },
  returns: v.union(
    v.object({
      _id: v.id("users"),
      name: v.string(),
      email: v.string(),
      avatarUrl: v.union(v.string(), v.null()),
    }),
    v.null()
  ),
  handler: async (ctx, args) => {
    const user = await ctx.db.get(args.userId);
    if (!user) return null;

    return {
      _id: user._id,
      name: user.name,
      email: user.email,
      // Handle missing field gracefully
      avatarUrl: user.avatarUrl ?? null,
    };
  },
});
```

```typescript
// Step 3: Backfill existing documents
// convex/migrations.ts
import { internalMutation } from "./_generated/server";
import { internal } from "./_generated/api";
import { v } from "convex/values";

const BATCH_SIZE = 100;

export const backfillAvatarUrl = internalMutation({
  args: {
    cursor: v.optional(v.string()),
  },
  returns: v.object({
    processed: v.number(),
    hasMore: v.boolean(),
  }),
  handler: async (ctx, args) => {
    const result = await ctx.db
      .query("users")
      .paginate({ numItems: BATCH_SIZE, cursor: args.cursor ?? null });

    let processed = 0;
    for (const user of result.page) {
      // Only update if field is missing
      if (user.avatarUrl === undefined) {
        await ctx.db.patch(user._id, {
          avatarUrl: generateDefaultAvatar(user.name),
        });
        processed++;
      }
    }

    // Schedule next batch if needed
    if (!result.isDone) {
      await ctx.scheduler.runAfter(0, internal.migrations.backfillAvatarUrl, {
        cursor: result.continueCursor,
      });
    }

    return {
      processed,
      hasMore: !result.isDone,
    };
  },
});

function generateDefaultAvatar(name: string): string {
  return `https://api.dicebear.com/7.x/initials/svg?seed=${encodeURIComponent(name)}`;
}
```

```typescript
// Step 4: After backfill completes, make field required
// convex/schema.ts
export default defineSchema({
  users: defineTable({
    name: v.string(),
    email: v.string(),
    avatarUrl: v.string(), // Now required
  }),
});
```

### Removing Fields

Remove field usage before removing from schema:

```typescript
// Step 1: Stop using the field in queries and mutations
// Mark as deprecated in code comments

// Step 2: Remove field from schema (make optional first if needed)
// convex/schema.ts
export default defineSchema({
  posts: defineTable({
    title: v.string(),
    content: v.string(),
    authorId: v.id("users"),
    // legacyField: v.optional(v.string()), // Remove this line
  }),
});

// Step 3: Optionally clean up existing data
// convex/migrations.ts
export const removeDeprecatedField = internalMutation({
  args: {
    cursor: v.optional(v.string()),
  },
  returns: v.null(),
  handler: async (ctx, args) => {
    const result = await ctx.db
      .query("posts")
      .paginate({ numItems: 100, cursor: args.cursor ?? null });

    for (const post of result.page) {
      // Use replace to remove the field entirely
      const { legacyField, ...rest } = post as typeof post & { legacyField?: string };
      if (legacyField !== undefined) {
        await ctx.db.replace(post._id, rest);
      }
    }

    if (!result.isDone) {
      await ctx.scheduler.runAfter(0, internal.migrations.removeDeprecatedField, {
        cursor: result.continueCursor,
      });
    }

    return null;
  },
});
```

### Renaming Fields

Renaming requires copying data to new field, then removing old:

```typescript
// Step 1: Add new field as optional
// convex/schema.ts
export default defineSchema({
  users: defineTable({
    userName: v.string(), // Old field
    displayName: v.optional(v.string()), // New field
  }),
});

// Step 2: Update code to read from new field with fallback
export const getUser = query({
  args: { userId: v.id("users") },
  returns: v.object({
    _id: v.id("users"),
    displayName: v.string(),
  }),
  handler: async (ctx, args) => {
    const user = await ctx.db.get(args.userId);
    if (!user) throw new Error("User not found");

    return {
      _id: user._id,
      // Read new field, fall back to old
      displayName: user.displayName ?? user.userName,
    };
  },
});

// Step 3: Backfill to copy data
export const backfillDisplayName = internalMutation({
  args: { cursor: v.optional(v.string()) },
  returns: v.null(),
  handler: async (ctx, args) => {
    const result = await ctx.db
      .query("users")
      .paginate({ numItems: 100, cursor: args.cursor ?? null });

    for (const user of result.page) {
      if (user.displayName === undefined) {
        await ctx.db.patch(user._id, {
          displayName: user.userName,
        });
      }
    }

    if (!result.isDone) {
      await ctx.scheduler.runAfter(0, internal.migrations.backfillDisplayName, {
        cursor: result.continueCursor,
      });
    }

    return null;
  },
});

// Step 4: After backfill, update schema to make new field required
// and remove old field
export default defineSchema({
  users: defineTable({
    // userName removed
    displayName: v.string(),
  }),
});
```

### Adding Indexes

Add indexes before using them in queries:

```typescript
// Step 1: Add index to schema
// convex/schema.ts
export default defineSchema({
  posts: defineTable({
    title: v.string(),
    authorId: v.id("users"),
    publishedAt: v.optional(v.number()),
    status: v.string(),
  })
    .index("by_author", ["authorId"])
    // New index
    .index("by_status_and_published", ["status", "publishedAt"]),
});

// Step 2: Deploy schema change
// Run: npx convex dev

// Step 3: Now use the index in queries
export const getPublishedPosts = query({
  args: {},
  returns: v.array(v.object({
    _id: v.id("posts"),
    title: v.string(),
    publishedAt: v.number(),
  })),
  handler: async (ctx) => {
    const posts = await ctx.db
      .query("posts")
      .withIndex("by_status_and_published", (q) =>
        q.eq("status", "published")
      )
      .order("desc")
      .take(10);

    return posts
      .filter((p) => p.publishedAt !== undefined)
      .map((p) => ({
        _id: p._id,
        title: p.title,
        publishedAt: p.publishedAt!,
      }));
  },
});
```

### Changing Field Types

Type changes require careful migration:

```typescript
// Example: Change from string to number for a "priority" field

// Step 1: Add new field with new type
// convex/schema.ts
export default defineSchema({
  tasks: defineTable({
    title: v.string(),
    priority: v.string(), // Old: "low", "medium", "high"
    priorityLevel: v.optional(v.number()), // New: 1, 2, 3
  }),
});

// Step 2: Backfill with type conversion
export const migratePriorityToNumber = internalMutation({
  args: { cursor: v.optional(v.string()) },
  returns: v.null(),
  handler: async (ctx, args) => {
    const result = await ctx.db
      .query("tasks")
      .paginate({ numItems: 100, cursor: args.cursor ?? null });

    const priorityMap: Record<string, number> = {
      low: 1,
      medium: 2,
      high: 3,
    };

    for (const task of result.page) {
      if (task.priorityLevel === undefined) {
        await ctx.db.patch(task._id, {
          priorityLevel: priorityMap[task.priority] ?? 1,
        });
      }
    }

    if (!result.isDone) {
      await ctx.scheduler.runAfter(0, internal.migrations.migratePriorityToNumber, {
        cursor: result.continueCursor,
      });
    }

    return null;
  },
});

// Step 3: Update code to use new field
export const getTask = query({
  args: { taskId: v.id("tasks") },
  returns: v.object({
    _id: v.id("tasks"),
    title: v.string(),
    priorityLevel: v.number(),
  }),
  handler: async (ctx, args) => {
    const task = await ctx.db.get(args.taskId);
    if (!task) throw new Error("Task not found");

    const priorityMap: Record<string, number> = {
      low: 1,
      medium: 2,
      high: 3,
    };

    return {
      _id: task._id,
      title: task.title,
      priorityLevel: task.priorityLevel ?? priorityMap[task.priority] ?? 1,
    };
  },
});

// Step 4: After backfill, update schema
export default defineSchema({
  tasks: defineTable({
    title: v.string(),
    // priority field removed
    priorityLevel: v.number(),
  }),
});
```

### Migration Runner Pattern

Create a reusable migration system:

```typescript
// convex/schema.ts
import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";

export default defineSchema({
  migrations: defineTable({
    name: v.string(),
    startedAt: v.number(),
    completedAt: v.optional(v.number()),
    status: v.union(
      v.literal("running"),
      v.literal("completed"),
      v.literal("failed")
    ),
    error: v.optional(v.string()),
    processed: v.number(),
  }).index("by_name", ["name"]),

  // Your other tables...
});
```

```typescript
// convex/migrations.ts
import { internalMutation, internalQuery } from "./_generated/server";
import { internal } from "./_generated/api";
import { v } from "convex/values";

// Check if migration has run
export const hasMigrationRun = internalQuery({
  args: { name: v.string() },
  returns: v.boolean(),
  handler: async (ctx, args) => {
    const migration = await ctx.db
      .query("migrations")
      .withIndex("by_name", (q) => q.eq("name", args.name))
      .first();
    return migration?.status === "completed";
  },
});

// Start a migration
export const startMigration = internalMutation({
  args: { name: v.string() },
  returns: v.id("migrations"),
  handler: async (ctx, args) => {
    // Check if already exists
    const existing = await ctx.db
      .query("migrations")
      .withIndex("by_name", (q) => q.eq("name", args.name))
      .first();

    if (existing) {
      if (existing.status === "completed") {
        throw new Error(`Migration ${args.name} already completed`);
      }
      if (existing.status === "running") {
        throw new Error(`Migration ${args.name} already running`);
      }
      // Reset failed migration
      await ctx.db.patch(existing._id, {
        status: "running",
        startedAt: Date.now(),
        error: undefined,
        processed: 0,
      });
      return existing._id;
    }

    return await ctx.db.insert("migrations", {
      name: args.name,
      startedAt: Date.now(),
      status: "running",
      processed: 0,
    });
  },
});

// Update migration progress
export const updateMigrationProgress = internalMutation({
  args: {
    migrationId: v.id("migrations"),
    processed: v.number(),
  },
  returns: v.null(),
  handler: async (ctx, args) => {
    const migration = await ctx.db.get(args.migrationId);
    if (!migration) return null;

    await ctx.db.patch(args.migrationId, {
      processed: migration.processed + args.processed,
    });

    return null;
  },
});

// Complete a migration
export const completeMigration = internalMutation({
  args: { migrationId: v.id("migrations") },
  returns: v.null(),
  handler: async (ctx, args) => {
    await ctx.db.patch(args.migrationId, {
      status: "completed",
      completedAt: Date.now(),
    });
    return null;
  },
});

// Fail a migration
export const failMigration = internalMutation({
  args: {
    migrationId: v.id("migrations"),
    error: v.string(),
  },
  returns: v.null(),
  handler: async (ctx, args) => {
    await ctx.db.patch(args.migrationId, {
      status: "failed",
      error: args.error,
    });
    return null;
  },
});
```

```typescript
// convex/migrations/addUserTimestamps.ts
import { internalMutation } from "../_generated/server";
import { internal } from "../_generated/api";
import { v } from "convex/values";

const MIGRATION_NAME = "add_user_timestamps_v1";
const BATCH_SIZE = 100;

export const run = internalMutation({
  args: {
    migrationId: v.optional(v.id("migrations")),
    cursor: v.optional(v.string()),
  },
  returns: v.null(),
  handler: async (ctx, args) => {
    // Initialize migration on first run
    let migrationId = args.migrationId;
    if (!migrationId) {
      const hasRun = await ctx.runQuery(internal.migrations.hasMigrationRun, {
        name: MIGRATION_NAME,
      });
      if (hasRun) {
        console.log(`Migration ${MIGRATION_NAME} already completed`);
        return null;
      }
      migrationId = await ctx.runMutation(internal.migrations.startMigration, {
        name: MIGRATION_NAME,
      });
    }

    try {
      const result = await ctx.db
        .query("users")
        .paginate({ numItems: BATCH_SIZE, cursor: args.cursor ?? null });

      let processed = 0;
      for (const user of result.page) {
        if (user.createdAt === undefined) {
          await ctx.db.patch(user._id, {
            createdAt: user._creationTime,
            updatedAt: user._creationTime,
          });
          processed++;
        }
      }

      // Update progress
      await ctx.runMutation(internal.migrations.updateMigrationProgress, {
        migrationId,
        processed,
      });

      // Continue or complete
      if (!result.isDone) {
        await ctx.scheduler.runAfter(0, internal.migrations.addUserTimestamps.run, {
          migrationId,
          cursor: result.continueCursor,
        });
      } else {
        await ctx.runMutation(internal.migrations.completeMigration, {
          migrationId,
        });
        console.log(`Migration ${MIGRATION_NAME} completed`);
      }
    } catch (error) {
      await ctx.runMutation(internal.migrations.failMigration, {
        migrationId,
        error: String(error),
      });
      throw error;
    }

    return null;
  },
});
```

## Examples

### Schema with Migration Support

```typescript
// convex/schema.ts
import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";

export default defineSchema({
  // Migration tracking
  migrations: defineTable({
    name: v.string(),
    startedAt: v.number(),
    completedAt: v.optional(v.number()),
    status: v.union(
      v.literal("running"),
      v.literal("completed"),
      v.literal("failed")
    ),
    error: v.optional(v.string()),
    processed: v.number(),
  }).index("by_name", ["name"]),

  // Users table with evolved schema
  users: defineTable({
    // Original fields
    name: v.string(),
    email: v.string(),
    
    // Added in migration v1
    createdAt: v.optional(v.number()),
    updatedAt: v.optional(v.number()),
    
    // Added in migration v2
    avatarUrl: v.optional(v.string()),
    
    // Added in migration v3
    settings: v.optional(v.object({
      theme: v.string(),
      notifications: v.boolean(),
    })),
  })
    .index("by_email", ["email"])
    .index("by_createdAt", ["createdAt"]),

  // Posts table with indexes for common queries
  posts: defineTable({
    title: v.string(),
    content: v.string(),
    authorId: v.id("users"),
    status: v.union(
      v.literal("draft"),
      v.literal("published"),
      v.literal("archived")
    ),
    publishedAt: v.optional(v.number()),
    createdAt: v.number(),
    updatedAt: v.number(),
  })
    .index("by_author", ["authorId"])
    .index("by_status", ["status"])
    .index("by_author_and_status", ["authorId", "status"])
    .index("by_publishedAt", ["publishedAt"]),
});
```

## Best Practices

- Never run `npx convex deploy` unless explicitly instructed
- Never run any git commands unless explicitly instructed
- Always start with optional fields when adding new data
- Backfill data in batches to avoid timeouts
- Test migrations on development before production
- Keep track of completed migrations to avoid re-running
- Update code to handle both old and new data during transition
- Remove deprecated fields only after all code stops using them
- Use pagination for large datasets
- Add appropriate indexes before running queries on new fields

## Common Pitfalls

1. **Making new fields required immediately** - Breaks existing documents
2. **Not handling undefined values** - Causes runtime errors
3. **Large batch sizes** - Causes function timeouts
4. **Forgetting to update indexes** - Queries fail or perform poorly
5. **Running migrations without tracking** - May run multiple times
6. **Removing fields before code update** - Breaks existing functionality
7. **Not testing on development** - Production data issues

## References

- Convex Documentation: https://docs.convex.dev/
- Convex LLMs.txt: https://docs.convex.dev/llms.txt
- Schemas: https://docs.convex.dev/database/schemas
- Database Overview: https://docs.convex.dev/database
- Migration Patterns: https://stack.convex.dev/migrate-data-postgres-to-convex
