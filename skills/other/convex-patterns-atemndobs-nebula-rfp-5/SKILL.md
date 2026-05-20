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

### Authenticated Action (Client-Callable)

Actions called from the client **MUST** verify authentication before processing:

```typescript
// ✅ Good: Auth check for client-callable action
export const uploadData = action({
  args: { data: v.string() },
  handler: async (ctx, args) => {
    // CRITICAL: Always verify auth for client-callable actions
    const identity = await ctx.auth.getUserIdentity();
    if (!identity) {
      throw new Error("Not authenticated");
    }

    // Delegate to internal action for processing
    return await ctx.runAction(internal.ingestion.processData, args);
  },
});

// ✅ Good: Use internalAction for background processing
export const processData = internalAction({
  args: { data: v.string() },
  handler: async (ctx, args) => {
    // Internal actions are only callable from other Convex functions
    // No auth check needed here - the calling action handles it
    // ... process data
  },
});
```

**Why separate action vs internalAction?**
- `action` - Callable from client, needs auth check
- `internalAction` - Only callable from server, can skip auth check
- Pattern: Client calls `action` (with auth) → `action` calls `internalAction` (for processing)

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

## Bandwidth Optimization Patterns

### Stats Aggregation Table

Pre-compute counts to avoid querying thousands of documents. This is **critical** for free tier limits (1GB/month).

```typescript
// ❌ Bad: Reads entire table to count
const all = await ctx.db.query("evaluations").collect();
return { total: all.length, eligible: all.filter(e => e.status === "ELIGIBLE").length };

// ✅ Good: Read single aggregation document
const cached = await ctx.db
  .query("statsAggregation")
  .withIndex("by_key", (q) => q.eq("key", "eligibility"))
  .first();

return {
  total: cached?.counts.total ?? 0,
  eligible: cached?.counts.eligible ?? 0,
};
```

**Schema for aggregation table:**
```typescript
statsAggregation: defineTable({
  key: v.string(), // e.g., "eligibility", "opportunities"
  counts: v.object({
    total: v.number(),
    eligible: v.optional(v.number()),
    // ... other counts
  }),
  lastUpdatedAt: v.number(),
}).index("by_key", ["key"]),
```

**Update stats incrementally** when records change:
```typescript
// In your create/update/delete mutations:
async function updateStatsOnIncrement(ctx: MutationCtx, status: string) {
  const existing = await ctx.db.query("statsAggregation")
    .withIndex("by_key", (q) => q.eq("key", "eligibility")).first();

  if (!existing) {
    await ctx.db.insert("statsAggregation", {
      key: "eligibility",
      counts: { total: 1, eligible: status === "ELIGIBLE" ? 1 : 0 },
      lastUpdatedAt: Date.now(),
    });
    return;
  }

  const counts = { ...existing.counts };
  counts.total = (counts.total ?? 0) + 1;
  if (status === "ELIGIBLE") counts.eligible = (counts.eligible ?? 0) + 1;
  await ctx.db.patch(existing._id, { counts, lastUpdatedAt: Date.now() });
}
```

### Conditional Query Loading (Skip Pattern)

Only load data when user actually needs it:

```tsx
// ✅ Good: Data won't load until user clicks export
const [wantsExport, setWantsExport] = useState(false);
const exportData = useQuery(
  api.eligibilityRules.exportRules,
  wantsExport ? {} : "skip"  // "skip" prevents the query from running
);

// User clicks button → query runs → data loads
<button onClick={() => setWantsExport(true)}>Export Rules</button>

// ❌ Bad: Loads all data on component mount even if rarely used
const exportData = useQuery(api.eligibilityRules.exportRules, {});
```

### Batch Operations with hasMore Pattern

For deleting or processing large datasets:

```typescript
// ✅ Good: Process in batches, return hasMore flag
export const resetAllEvaluations = mutation({
  args: { batchSize: v.optional(v.number()) },
  handler: async (ctx, args) => {
    const batchSize = args.batchSize ?? 100;
    const evaluations = await ctx.db.query("evaluations").take(batchSize);

    for (const evaluation of evaluations) {
      await ctx.db.delete(evaluation._id);
    }

    return {
      deleted: evaluations.length,
      hasMore: evaluations.length === batchSize  // True if there might be more
    };
  },
});
```

**Client-side loop:**
```typescript
const handleReset = async () => {
  let hasMore = true;
  let totalDeleted = 0;

  while (hasMore) {
    const result = await resetEvaluations({ batchSize: 100 });
    totalDeleted += result.deleted;
    hasMore = result.hasMore;
  }

  console.log(`Deleted ${totalDeleted} evaluations`);
};
```

### Indexed Lookups for Joins

When joining tables, use indexed lookups per-record instead of loading entire tables:

```typescript
// ❌ Bad: Loads ALL evaluations, then filters in JS
const allEvaluations = await ctx.db.query("evaluations").take(1000);
const evaluationMap = new Map(allEvaluations.map(e => [e.opportunityId, e]));
return opportunities.map(opp => ({
  ...opp,
  evaluation: evaluationMap.get(opp._id),
}));

// ✅ Good: Use indexed lookup per opportunity (N queries, but each is tiny)
const evaluationPromises = opportunities.map(opp =>
  ctx.db.query("evaluations")
    .withIndex("by_opportunity", (q) => q.eq("opportunityId", opp._id))
    .first()
  );
const evaluations = await Promise.all(evaluationPromises);
return opportunities.map((opp, i) => ({
  ...opp,
  evaluation: evaluations[i],
}));
```

### Deduplication with Sets

For upsert operations, use Set-based lookups instead of array includes:

```typescript
// ❌ Bad: O(n) lookup for each check
const recentIds = recentOpportunities.map(o => o.externalIds[0]?.externalId);
if (recentIds.includes(record.externalId)) continue;

// ✅ Good: O(1) lookup with Set
const existingIds = new Set(
  recentOpportunities.flatMap(o => o.externalIds.map(e => e.externalId))
);
if (existingIds.has(record.externalId)) continue;
```

## Anti-Patterns to Avoid

| ❌ Avoid                                   | ✅ Do Instead                            |
| ----------------------------------------- | --------------------------------------- |
| `.collect()` without limit                | `.take(limit)`                          |
| Large `.take(1000)` on heavyweight tables | Smaller limits (50-200) with pagination |
| Loading full table to count records       | Stats aggregation table                 |
| Filtering in JS after fetch               | Use indexes                             |
| Storing derived data                      | Compute in queries (unless for stats)   |
| `any` types in args                       | Proper `v.*` validators                 |
| Multiple awaits in loops                  | `Promise.all` for batches               |
| Env vars in queries                       | Only in actions                         |
| Loading unused data on mount              | Conditional queries with `"skip"`       |
| Full table scan for joins                 | Indexed lookups per record              |
