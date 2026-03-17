---
name: convex-patterns
description: Convex database patterns and best practices for RFP Discovery. Use when writing Convex queries, mutations, actions, or schema definitions. Also helpful for real-time subscriptions and auth integration.
allowed-tools: Read, Grep, Glob
---

# Convex Patterns Skill

## Overview

This skill provides patterns and best practices for implementing Convex backend functions in the RFP Discovery platform.

## Schema Design

### Complete Schema

```typescript
// convex/schema.ts
import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";

export default defineSchema({
  // Users (synced from Clerk)
  users: defineTable({
    clerkId: v.string(),
    name: v.string(),
    email: v.string(),
    imageUrl: v.optional(v.string()),
    role: v.string(), // "admin" | "user" | "viewer"
    createdAt: v.number(),
    updatedAt: v.number(),
  })
    .index("by_clerk_id", ["clerkId"])
    .index("by_email", ["email"]),

  // RFP Opportunities
  rfps: defineTable({
    externalId: v.string(),
    source: v.string(),
    title: v.string(),
    description: v.string(),
    summary: v.optional(v.string()),
    location: v.string(),
    category: v.string(),
    naicsCode: v.optional(v.string()),
    setAside: v.optional(v.string()),
    postedDate: v.number(),
    expiryDate: v.number(),
    url: v.string(),
    eligibilityFlags: v.optional(v.array(v.string())),
    rawData: v.optional(v.any()),
    ingestedAt: v.number(),
    updatedAt: v.number(),
  })
    .index("by_external_id", ["externalId", "source"])
    .index("by_source", ["source"])
    .index("by_expiry", ["expiryDate"])
    .searchIndex("search_title", {
      searchField: "title",
      filterFields: ["source", "category"],
    }),

  // Evaluations
  evaluations: defineTable({
    rfpId: v.id("rfps"),
    userId: v.string(),
    evaluationType: v.string(),
    score: v.number(),
    isFit: v.boolean(),
    criteriaResults: v.array(
      v.object({
        criterionId: v.string(),
        criterionName: v.string(),
        weight: v.number(),
        met: v.boolean(),
        score: v.number(),
        matchedKeywords: v.array(v.string()),
        details: v.string(),
      })
    ),
    eligibility: v.object({
      eligible: v.boolean(),
      status: v.string(),
      disqualifiers: v.array(v.string()),
    }),
    reasoning: v.optional(v.string()),
    evaluatedAt: v.number(),
  })
    .index("by_rfp", ["rfpId"])
    .index("by_user", ["userId"])
    .index("by_score", ["score"]),

  // Pursuits
  pursuits: defineTable({
    rfpId: v.id("rfps"),
    userId: v.string(),
    status: v.string(),
    decision: v.optional(v.string()),
    decisionBy: v.optional(v.string()),
    decisionAt: v.optional(v.number()),
    brief: v.optional(v.string()),
    complianceMatrix: v.optional(v.string()),
    notes: v.optional(v.string()),
    teamMembers: v.optional(v.array(v.string())),
    createdAt: v.number(),
    updatedAt: v.number(),
  })
    .index("by_rfp", ["rfpId"])
    .index("by_user", ["userId"])
    .index("by_status", ["status"]),

  // Criteria Configuration
  criteria: defineTable({
    name: v.string(),
    displayName: v.string(),
    weight: v.number(),
    enabled: v.boolean(),
    keywords: v.array(
      v.object({
        value: v.string(),
        enabled: v.boolean(),
      })
    ),
    minMatches: v.number(),
    systemInstruction: v.optional(v.string()),
    order: v.number(),
  }).index("by_order", ["order"]),

  // Ingestion Logs
  ingestionLogs: defineTable({
    source: v.string(),
    status: v.string(),
    recordsProcessed: v.number(),
    recordsInserted: v.number(),
    recordsUpdated: v.number(),
    errors: v.optional(v.array(v.string())),
    startedAt: v.number(),
    completedAt: v.optional(v.number()),
  }).index("by_source", ["source"]),
});
```

## Query Patterns

### Basic Query with Pagination

```typescript
// ✅ Good: Uses limit and proper typing
export const list = query({
  args: {
    limit: v.optional(v.number()),
    cursor: v.optional(v.id("rfps")),
  },
  handler: async (ctx, args) => {
    const limit = args.limit ?? 50;

    let q = ctx.db.query("rfps").order("desc");

    if (args.cursor) {
      const cursorDoc = await ctx.db.get(args.cursor);
      if (cursorDoc) {
        q = q.filter((q) =>
          q.lt(q.field("_creationTime"), cursorDoc._creationTime)
        );
      }
    }

    const items = await q.take(limit + 1);
    const hasMore = items.length > limit;

    return {
      items: items.slice(0, limit),
      nextCursor: hasMore ? items[limit - 1]._id : null,
    };
  },
});

// ❌ Bad: Collects all without limit
export const listAll = query({
  handler: async (ctx) => {
    return await ctx.db.query("rfps").collect(); // Don't do this!
  },
});
```

### Query with Index

```typescript
// ✅ Good: Uses index for efficient filtering
export const listBySource = query({
  args: { source: v.string() },
  handler: async (ctx, args) => {
    return await ctx.db
      .query("rfps")
      .withIndex("by_source", (q) => q.eq("source", args.source))
      .order("desc")
      .take(50);
  },
});

// ❌ Bad: Full table scan with filter
export const listBySourceBad = query({
  args: { source: v.string() },
  handler: async (ctx, args) => {
    return await ctx.db
      .query("rfps")
      .filter((q) => q.eq(q.field("source"), args.source))
      .collect();
  },
});
```

### Full-Text Search

```typescript
export const search = query({
  args: {
    searchTerm: v.string(),
    source: v.optional(v.string()),
  },
  handler: async (ctx, args) => {
    let q = ctx.db
      .query("rfps")
      .withSearchIndex("search_title", (q) => {
        let sq = q.search("title", args.searchTerm);
        if (args.source) {
          sq = sq.eq("source", args.source);
        }
        return sq;
      });

    return await q.take(20);
  },
});
```

## Mutation Patterns

### Authenticated Mutation

```typescript
// ✅ Good: Checks auth before any operation
export const create = mutation({
  args: {
    rfpId: v.id("rfps"),
    status: v.string(),
  },
  handler: async (ctx, args) => {
    const identity = await ctx.auth.getUserIdentity();
    if (!identity) {
      throw new Error("Not authenticated");
    }

    return await ctx.db.insert("pursuits", {
      rfpId: args.rfpId,
      userId: identity.subject,
      status: args.status,
      createdAt: Date.now(),
      updatedAt: Date.now(),
    });
  },
});
```

### Upsert Pattern

```typescript
export const upsert = mutation({
  args: {
    externalId: v.string(),
    source: v.string(),
    title: v.string(),
    // ... other fields
  },
  handler: async (ctx, args) => {
    const existing = await ctx.db
      .query("rfps")
      .withIndex("by_external_id", (q) =>
        q.eq("externalId", args.externalId).eq("source", args.source)
      )
      .first();

    const now = Date.now();

    if (existing) {
      await ctx.db.patch(existing._id, {
        ...args,
        updatedAt: now,
      });
      return { id: existing._id, action: "updated" as const };
    }

    const id = await ctx.db.insert("rfps", {
      ...args,
      ingestedAt: now,
      updatedAt: now,
    });
    return { id, action: "inserted" as const };
  },
});
```

### Transactional Updates

```typescript
export const updatePursuitWithHistory = mutation({
  args: {
    pursuitId: v.id("pursuits"),
    status: v.string(),
    notes: v.optional(v.string()),
  },
  handler: async (ctx, args) => {
    const identity = await ctx.auth.getUserIdentity();
    if (!identity) throw new Error("Not authenticated");

    const pursuit = await ctx.db.get(args.pursuitId);
    if (!pursuit) throw new Error("Pursuit not found");

    // Update pursuit
    await ctx.db.patch(args.pursuitId, {
      status: args.status,
      notes: args.notes,
      updatedAt: Date.now(),
    });

    // Log activity (both happen in same transaction)
    await ctx.db.insert("activityLog", {
      userId: identity.subject,
      action: "status_change",
      entityType: "pursuit",
      entityId: args.pursuitId,
      details: {
        from: pursuit.status,
        to: args.status,
      },
      timestamp: Date.now(),
    });

    return { success: true };
  },
});
```

## Action Patterns

### External API Call

```typescript
// convex/actions/samGov.ts
import { action } from "../_generated/server";
import { v } from "convex/values";
import { internal } from "../_generated/api";

export const fetchOpportunities = action({
  args: { daysBack: v.number() },
  handler: async (ctx, args) => {
    const apiKey = process.env.SAM_GOV_API_KEY;
    if (!apiKey) {
      throw new Error("SAM_GOV_API_KEY not configured");
    }

    const fromDate = new Date();
    fromDate.setDate(fromDate.getDate() - args.daysBack);

    const response = await fetch(
      `https://api.sam.gov/opportunities/v2/search?` +
        `api_key=${apiKey}&postedFrom=${fromDate.toISOString().split("T")[0]}`,
      {
        headers: { Accept: "application/json" },
      }
    );

    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }

    const data = await response.json();

    // Process in batches to avoid timeout
    const BATCH_SIZE = 10;
    const opportunities = data.opportunitiesData ?? [];

    for (let i = 0; i < opportunities.length; i += BATCH_SIZE) {
      const batch = opportunities.slice(i, i + BATCH_SIZE);

      await Promise.all(
        batch.map((opp: any) =>
          ctx.runMutation(internal.rfps.upsert, {
            externalId: opp.noticeId,
            source: "sam.gov",
            title: opp.title,
            // ... map other fields
          })
        )
      );
    }

    return { processed: opportunities.length };
  },
});
```

## React Integration

### useQuery with Loading State

```tsx
import { useQuery } from "convex/react";
import { api } from "../convex/_generated/api";

function RfpList() {
  const rfps = useQuery(api.rfps.list, { limit: 50 });

  if (rfps === undefined) {
    return <LoadingSpinner />;
  }

  if (rfps.items.length === 0) {
    return <EmptyState message="No RFPs found" />;
  }

  return (
    <div className="grid gap-4">
      {rfps.items.map((rfp) => (
        <RfpCard key={rfp._id} rfp={rfp} />
      ))}
    </div>
  );
}
```

### useMutation with Optimistic Updates

```tsx
import { useMutation, useQuery } from "convex/react";
import { api } from "../convex/_generated/api";

function PursuitActions({ pursuitId }: { pursuitId: Id<"pursuits"> }) {
  const updateStatus = useMutation(api.pursuits.updateStatus);
  const [isPending, setIsPending] = useState(false);

  const handleStatusChange = async (newStatus: string) => {
    setIsPending(true);
    try {
      await updateStatus({ pursuitId, status: newStatus });
    } finally {
      setIsPending(false);
    }
  };

  return (
    <select
      disabled={isPending}
      onChange={(e) => handleStatusChange(e.target.value)}
    >
      <option value="new">New</option>
      <option value="triage">Triage</option>
      <option value="bid">Bid</option>
      <option value="no-bid">No Bid</option>
    </select>
  );
}
```

## Common Patterns

### Auth Helper

```typescript
// convex/lib/auth.ts
import { QueryCtx, MutationCtx } from "./_generated/server";

export async function requireAuth(ctx: QueryCtx | MutationCtx) {
  const identity = await ctx.auth.getUserIdentity();
  if (!identity) {
    throw new Error("Not authenticated");
  }
  return identity;
}

export async function requireAdmin(ctx: QueryCtx | MutationCtx) {
  const identity = await requireAuth(ctx);

  const user = await ctx.db
    .query("users")
    .withIndex("by_clerk_id", (q) => q.eq("clerkId", identity.subject))
    .first();

  if (!user || user.role !== "admin") {
    throw new Error("Admin access required");
  }

  return { identity, user };
}
```

### Scheduled Jobs

```typescript
// convex/crons.ts
import { cronJobs } from "convex/server";
import { internal } from "./_generated/api";

const crons = cronJobs();

// Run every 6 hours
crons.interval(
  "ingest-sam-gov",
  { hours: 6 },
  internal.ingestion.runSamGovIngestion
);

// Run daily at 6 AM UTC
crons.daily(
  "cleanup-expired",
  { hourUTC: 6, minuteUTC: 0 },
  internal.maintenance.archiveExpiredRfps
);

export default crons;
```

## Anti-Patterns to Avoid

| ❌ Avoid | ✅ Do Instead |
|----------|---------------|
| `.collect()` without limit | `.take(limit)` |
| Filtering in JS after fetch | Use indexes |
| Storing derived data | Compute in queries |
| `any` types in args | Proper `v.*` validators |
| Multiple awaits in loops | `Promise.all` for batches |
| Env vars in queries | Only in actions |
