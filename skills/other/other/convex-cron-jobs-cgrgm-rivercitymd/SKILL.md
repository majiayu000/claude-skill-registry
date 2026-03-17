---
name: convex-cron-jobs
displayName: Convex Cron Jobs
description: Scheduled function patterns for background tasks including interval scheduling, cron expressions, job monitoring, retry strategies, and best practices for long-running tasks
version: 1.0.0
author: Convex
tags: [convex, cron, scheduling, background-jobs, automation]
---

# Convex Cron Jobs

Schedule recurring functions for background tasks, cleanup jobs, data syncing, and automated workflows in Convex applications.

## Documentation Sources

Before implementing, do not assume; fetch the latest documentation:

- Primary: https://docs.convex.dev/scheduling/cron-jobs
- Scheduling Overview: https://docs.convex.dev/scheduling
- Scheduled Functions: https://docs.convex.dev/scheduling/scheduled-functions
- For broader context: https://docs.convex.dev/llms.txt

## Instructions

### Cron Jobs Overview

Convex cron jobs allow you to schedule functions to run at regular intervals or specific times. Key features:

- Run functions on a fixed schedule
- Support for interval-based and cron expression scheduling
- Automatic retries on failure
- Monitoring via the Convex dashboard

### Basic Cron Setup

```typescript
// convex/crons.ts
import { cronJobs } from "convex/server";
import { internal } from "./_generated/api";

const crons = cronJobs();

// Run every hour
crons.interval(
  "cleanup expired sessions",
  { hours: 1 },
  internal.tasks.cleanupExpiredSessions,
  {}
);

// Run every day at midnight UTC
crons.cron(
  "daily report",
  "0 0 * * *",
  internal.reports.generateDailyReport,
  {}
);

export default crons;
```

### Interval-Based Scheduling

Use `crons.interval` for simple recurring tasks:

```typescript
// convex/crons.ts
import { cronJobs } from "convex/server";
import { internal } from "./_generated/api";

const crons = cronJobs();

// Every 5 minutes
crons.interval(
  "sync external data",
  { minutes: 5 },
  internal.sync.fetchExternalData,
  {}
);

// Every 2 hours
crons.interval(
  "cleanup temp files",
  { hours: 2 },
  internal.files.cleanupTempFiles,
  {}
);

// Every 30 seconds (minimum interval)
crons.interval(
  "health check",
  { seconds: 30 },
  internal.monitoring.healthCheck,
  {}
);

export default crons;
```

### Cron Expression Scheduling

Use `crons.cron` for precise scheduling with cron expressions:

```typescript
// convex/crons.ts
import { cronJobs } from "convex/server";
import { internal } from "./_generated/api";

const crons = cronJobs();

// Every day at 9 AM UTC
crons.cron(
  "morning notifications",
  "0 9 * * *",
  internal.notifications.sendMorningDigest,
  {}
);

// Every Monday at 8 AM UTC
crons.cron(
  "weekly summary",
  "0 8 * * 1",
  internal.reports.generateWeeklySummary,
  {}
);

// First day of every month at midnight
crons.cron(
  "monthly billing",
  "0 0 1 * *",
  internal.billing.processMonthlyBilling,
  {}
);

// Every 15 minutes
crons.cron(
  "frequent sync",
  "*/15 * * * *",
  internal.sync.syncData,
  {}
);

export default crons;
```

### Cron Expression Reference

```
┌───────────── minute (0-59)
│ ┌───────────── hour (0-23)
│ │ ┌───────────── day of month (1-31)
│ │ │ ┌───────────── month (1-12)
│ │ │ │ ┌───────────── day of week (0-6, Sunday=0)
│ │ │ │ │
* * * * *
```

Common patterns:
- `* * * * *` - Every minute
- `0 * * * *` - Every hour
- `0 0 * * *` - Every day at midnight
- `0 0 * * 0` - Every Sunday at midnight
- `0 0 1 * *` - First day of every month
- `*/5 * * * *` - Every 5 minutes
- `0 9-17 * * 1-5` - Every hour from 9 AM to 5 PM, Monday through Friday

### Internal Functions for Crons

Cron jobs should call internal functions for security:

```typescript
// convex/tasks.ts
import { internalMutation, internalQuery } from "./_generated/server";
import { v } from "convex/values";

// Cleanup expired sessions
export const cleanupExpiredSessions = internalMutation({
  args: {},
  returns: v.number(),
  handler: async (ctx) => {
    const oneHourAgo = Date.now() - 60 * 60 * 1000;
    
    const expiredSessions = await ctx.db
      .query("sessions")
      .withIndex("by_lastActive")
      .filter((q) => q.lt(q.field("lastActive"), oneHourAgo))
      .collect();

    for (const session of expiredSessions) {
      await ctx.db.delete(session._id);
    }

    return expiredSessions.length;
  },
});

// Process pending tasks
export const processPendingTasks = internalMutation({
  args: {},
  returns: v.null(),
  handler: async (ctx) => {
    const pendingTasks = await ctx.db
      .query("tasks")
      .withIndex("by_status", (q) => q.eq("status", "pending"))
      .take(100);

    for (const task of pendingTasks) {
      await ctx.db.patch(task._id, {
        status: "processing",
        startedAt: Date.now(),
      });
      
      // Schedule the actual processing
      await ctx.scheduler.runAfter(0, internal.tasks.processTask, {
        taskId: task._id,
      });
    }

    return null;
  },
});
```

### Cron Jobs with Arguments

Pass static arguments to cron jobs:

```typescript
// convex/crons.ts
import { cronJobs } from "convex/server";
import { internal } from "./_generated/api";

const crons = cronJobs();

// Different cleanup intervals for different types
crons.interval(
  "cleanup temp files",
  { hours: 1 },
  internal.cleanup.cleanupByType,
  { fileType: "temp", maxAge: 3600000 }
);

crons.interval(
  "cleanup cache files",
  { hours: 24 },
  internal.cleanup.cleanupByType,
  { fileType: "cache", maxAge: 86400000 }
);

export default crons;
```

```typescript
// convex/cleanup.ts
import { internalMutation } from "./_generated/server";
import { v } from "convex/values";

export const cleanupByType = internalMutation({
  args: {
    fileType: v.string(),
    maxAge: v.number(),
  },
  returns: v.number(),
  handler: async (ctx, args) => {
    const cutoff = Date.now() - args.maxAge;
    
    const oldFiles = await ctx.db
      .query("files")
      .withIndex("by_type_and_created", (q) => 
        q.eq("type", args.fileType).lt("createdAt", cutoff)
      )
      .collect();

    for (const file of oldFiles) {
      await ctx.storage.delete(file.storageId);
      await ctx.db.delete(file._id);
    }

    return oldFiles.length;
  },
});
```

### Monitoring and Logging

Add logging to track cron job execution:

```typescript
// convex/tasks.ts
import { internalMutation } from "./_generated/server";
import { v } from "convex/values";

export const cleanupWithLogging = internalMutation({
  args: {},
  returns: v.null(),
  handler: async (ctx) => {
    const startTime = Date.now();
    let processedCount = 0;
    let errorCount = 0;

    try {
      const expiredItems = await ctx.db
        .query("items")
        .withIndex("by_expiresAt")
        .filter((q) => q.lt(q.field("expiresAt"), Date.now()))
        .collect();

      for (const item of expiredItems) {
        try {
          await ctx.db.delete(item._id);
          processedCount++;
        } catch (error) {
          errorCount++;
          console.error(`Failed to delete item ${item._id}:`, error);
        }
      }

      // Log job completion
      await ctx.db.insert("cronLogs", {
        jobName: "cleanup",
        startTime,
        endTime: Date.now(),
        duration: Date.now() - startTime,
        processedCount,
        errorCount,
        status: errorCount === 0 ? "success" : "partial",
      });
    } catch (error) {
      // Log job failure
      await ctx.db.insert("cronLogs", {
        jobName: "cleanup",
        startTime,
        endTime: Date.now(),
        duration: Date.now() - startTime,
        processedCount,
        errorCount,
        status: "failed",
        error: String(error),
      });
      throw error;
    }

    return null;
  },
});
```

### Batching for Large Datasets

Handle large datasets in batches to avoid timeouts:

```typescript
// convex/tasks.ts
import { internalMutation } from "./_generated/server";
import { internal } from "./_generated/api";
import { v } from "convex/values";

const BATCH_SIZE = 100;

export const processBatch = internalMutation({
  args: {
    cursor: v.optional(v.string()),
  },
  returns: v.null(),
  handler: async (ctx, args) => {
    const result = await ctx.db
      .query("items")
      .withIndex("by_status", (q) => q.eq("status", "pending"))
      .paginate({ numItems: BATCH_SIZE, cursor: args.cursor ?? null });

    for (const item of result.page) {
      await ctx.db.patch(item._id, {
        status: "processed",
        processedAt: Date.now(),
      });
    }

    // Schedule next batch if there are more items
    if (!result.isDone) {
      await ctx.scheduler.runAfter(0, internal.tasks.processBatch, {
        cursor: result.continueCursor,
      });
    }

    return null;
  },
});
```

### External API Calls in Crons

Use actions for external API calls:

```typescript
// convex/sync.ts
"use node";

import { internalAction } from "./_generated/server";
import { internal } from "./_generated/api";
import { v } from "convex/values";

export const syncExternalData = internalAction({
  args: {},
  returns: v.null(),
  handler: async (ctx) => {
    // Fetch from external API
    const response = await fetch("https://api.example.com/data", {
      headers: {
        Authorization: `Bearer ${process.env.API_KEY}`,
      },
    });

    if (!response.ok) {
      throw new Error(`API request failed: ${response.status}`);
    }

    const data = await response.json();

    // Store the data using a mutation
    await ctx.runMutation(internal.sync.storeExternalData, {
      data,
      syncedAt: Date.now(),
    });

    return null;
  },
});

export const storeExternalData = internalMutation({
  args: {
    data: v.any(),
    syncedAt: v.number(),
  },
  returns: v.null(),
  handler: async (ctx, args) => {
    await ctx.db.insert("externalData", {
      data: args.data,
      syncedAt: args.syncedAt,
    });
    return null;
  },
});
```

```typescript
// convex/crons.ts
import { cronJobs } from "convex/server";
import { internal } from "./_generated/api";

const crons = cronJobs();

crons.interval(
  "sync external data",
  { minutes: 15 },
  internal.sync.syncExternalData,
  {}
);

export default crons;
```

## Examples

### Schema for Cron Job Logging

```typescript
// convex/schema.ts
import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";

export default defineSchema({
  cronLogs: defineTable({
    jobName: v.string(),
    startTime: v.number(),
    endTime: v.number(),
    duration: v.number(),
    processedCount: v.number(),
    errorCount: v.number(),
    status: v.union(
      v.literal("success"),
      v.literal("partial"),
      v.literal("failed")
    ),
    error: v.optional(v.string()),
  })
    .index("by_job", ["jobName"])
    .index("by_status", ["status"])
    .index("by_startTime", ["startTime"]),

  sessions: defineTable({
    userId: v.id("users"),
    token: v.string(),
    lastActive: v.number(),
    expiresAt: v.number(),
  })
    .index("by_user", ["userId"])
    .index("by_lastActive", ["lastActive"])
    .index("by_expiresAt", ["expiresAt"]),

  tasks: defineTable({
    type: v.string(),
    status: v.union(
      v.literal("pending"),
      v.literal("processing"),
      v.literal("completed"),
      v.literal("failed")
    ),
    data: v.any(),
    createdAt: v.number(),
    startedAt: v.optional(v.number()),
    completedAt: v.optional(v.number()),
  })
    .index("by_status", ["status"])
    .index("by_type_and_status", ["type", "status"]),
});
```

### Complete Cron Configuration Example

```typescript
// convex/crons.ts
import { cronJobs } from "convex/server";
import { internal } from "./_generated/api";

const crons = cronJobs();

// Cleanup jobs
crons.interval(
  "cleanup expired sessions",
  { hours: 1 },
  internal.cleanup.expiredSessions,
  {}
);

crons.interval(
  "cleanup old logs",
  { hours: 24 },
  internal.cleanup.oldLogs,
  { maxAgeDays: 30 }
);

// Sync jobs
crons.interval(
  "sync user data",
  { minutes: 15 },
  internal.sync.userData,
  {}
);

// Report jobs
crons.cron(
  "daily analytics",
  "0 1 * * *",
  internal.reports.dailyAnalytics,
  {}
);

crons.cron(
  "weekly summary",
  "0 9 * * 1",
  internal.reports.weeklySummary,
  {}
);

// Health checks
crons.interval(
  "service health check",
  { minutes: 5 },
  internal.monitoring.healthCheck,
  {}
);

export default crons;
```

## Best Practices

- Never run `npx convex deploy` unless explicitly instructed
- Never run any git commands unless explicitly instructed
- Only use `crons.interval` or `crons.cron` methods, not deprecated helpers
- Always call internal functions from cron jobs for security
- Import `internal` from `_generated/api` even for functions in the same file
- Add logging and monitoring for production cron jobs
- Use batching for operations that process large datasets
- Handle errors gracefully to prevent job failures
- Use meaningful job names for dashboard visibility
- Consider timezone when using cron expressions (Convex uses UTC)

## Common Pitfalls

1. **Using public functions** - Cron jobs should call internal functions only
2. **Long-running mutations** - Break large operations into batches
3. **Missing error handling** - Unhandled errors will fail the entire job
4. **Forgetting timezone** - All cron expressions use UTC
5. **Using deprecated helpers** - Avoid `crons.hourly`, `crons.daily`, etc.
6. **Not logging execution** - Makes debugging production issues difficult

## References

- Convex Documentation: https://docs.convex.dev/
- Convex LLMs.txt: https://docs.convex.dev/llms.txt
- Cron Jobs: https://docs.convex.dev/scheduling/cron-jobs
- Scheduling Overview: https://docs.convex.dev/scheduling
- Scheduled Functions: https://docs.convex.dev/scheduling/scheduled-functions
