---
name: Convex Integration
description: Guidelines for integrating Convex real-time database into the RFP Discovery application
---

# Convex Integration Skill

This skill provides guidance for integrating Convex as the real-time database backend for the RFP Discovery application.

## Installation

```bash
npm install convex
npx convex dev
```

## Schema Design

Create `convex/schema.ts` with the following tables:

### RFP Table
```typescript
import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";

export default defineSchema({
  rfps: defineTable({
    // Core fields
    externalId: v.string(), // ID from source platform
    source: v.string(),     // "sam.gov", "rfpmart", "emma", etc.
    title: v.string(),
    summary: v.string(),
    url: v.string(),
    
    // Dates
    postedDate: v.optional(v.string()),
    deadline: v.optional(v.string()),
    questionDeadline: v.optional(v.string()),
    
    // Location/Category
    location: v.optional(v.string()),
    category: v.optional(v.string()),
    state: v.optional(v.string()),
    country: v.optional(v.string()),
    
    // Budget
    budget: v.optional(v.string()),
    
    // Eligibility
    eligibility: v.optional(v.string()),
    isUsaOnly: v.optional(v.boolean()),
    requiresOnshore: v.optional(v.boolean()),
    setAsideType: v.optional(v.string()),
    
    // Metadata
    fetchedAt: v.number(),
    rawData: v.optional(v.string()),
  }).index("by_external_id", ["externalId", "source"])
    .index("by_source", ["source"])
    .index("by_deadline", ["deadline"]),

  evaluations: defineTable({
    rfpId: v.id("rfps"),
    userId: v.optional(v.string()), // Clerk user ID
    
    // Overall result
    isFit: v.boolean(),
    score: v.number(),
    maxScore: v.number(),
    
    // Per-criterion results
    technicalRelevance: v.object({
      met: v.boolean(),
      details: v.optional(v.string()),
    }),
    scopeFit: v.object({
      met: v.boolean(),
      details: v.optional(v.string()),
    }),
    categoryFocus: v.object({
      met: v.boolean(),
      details: v.optional(v.string()),
    }),
    clientProfile: v.object({
      met: v.boolean(),
      details: v.optional(v.string()),
    }),
    logistics: v.object({
      met: v.boolean(),
      details: v.optional(v.string()),
    }),
    skillSetAlignment: v.object({
      met: v.boolean(),
      details: v.optional(v.string()),
    }),
    
    // AI analysis
    aiProvider: v.optional(v.string()),
    aiAnalysis: v.optional(v.string()), // JSON string
    reasoning: v.optional(v.string()),
    
    // Timestamps
    evaluatedAt: v.number(),
  }).index("by_rfp", ["rfpId"])
    .index("by_user", ["userId"]),

  pursuits: defineTable({
    rfpId: v.id("rfps"),
    userId: v.string(), // Clerk user ID
    
    // Pipeline stage
    stage: v.union(
      v.literal("new"),
      v.literal("triage"),
      v.literal("bid"),
      v.literal("no_bid"),
      v.literal("capture"),
      v.literal("submitted"),
      v.literal("won"),
      v.literal("lost")
    ),
    
    // Decision tracking
    decision: v.optional(v.union(
      v.literal("pursue"),
      v.literal("partner_needed"),
      v.literal("reject")
    )),
    decisionReason: v.optional(v.string()),
    
    // Notes
    notes: v.optional(v.string()),
    
    // Timestamps
    createdAt: v.number(),
    updatedAt: v.number(),
  }).index("by_user", ["userId"])
    .index("by_stage", ["stage"]),

  userSettings: defineTable({
    userId: v.string(), // Clerk user ID
    
    // AI Settings
    selectedAiProvider: v.string(),
    aiProviderConfigs: v.optional(v.string()), // JSON
    corePromptTemplate: v.optional(v.string()),
    useAiForEvaluation: v.boolean(),
    
    // Criteria Config
    criteriaConfig: v.optional(v.string()), // JSON
    
    // Refresh Settings
    autoRefreshIntervalHours: v.number(),
    
    // UI Preferences
    theme: v.union(v.literal("light"), v.literal("dark")),
  }).index("by_user", ["userId"]),
});
```

## Query Patterns

### Fetching RFPs with Evaluations
```typescript
// convex/rfps.ts
import { query } from "./_generated/server";
import { v } from "convex/values";

export const listWithEvaluations = query({
  args: { 
    source: v.optional(v.string()),
    limit: v.optional(v.number()) 
  },
  handler: async (ctx, args) => {
    let rfpsQuery = ctx.db.query("rfps");
    
    if (args.source) {
      rfpsQuery = rfpsQuery.withIndex("by_source", (q) => 
        q.eq("source", args.source)
      );
    }
    
    const rfps = await rfpsQuery
      .order("desc")
      .take(args.limit ?? 50);
    
    // Fetch evaluations for each RFP
    const rfpsWithEvals = await Promise.all(
      rfps.map(async (rfp) => {
        const evaluation = await ctx.db
          .query("evaluations")
          .withIndex("by_rfp", (q) => q.eq("rfpId", rfp._id))
          .first();
        return { ...rfp, evaluation };
      })
    );
    
    return rfpsWithEvals;
  },
});
```

## Mutation Patterns

### Saving an Evaluation
```typescript
// convex/evaluations.ts
import { mutation } from "./_generated/server";
import { v } from "convex/values";

export const saveEvaluation = mutation({
  args: {
    rfpId: v.id("rfps"),
    isFit: v.boolean(),
    score: v.number(),
    maxScore: v.number(),
    criteriaResults: v.object({
      technicalRelevance: v.object({ met: v.boolean(), details: v.optional(v.string()) }),
      scopeFit: v.object({ met: v.boolean(), details: v.optional(v.string()) }),
      categoryFocus: v.object({ met: v.boolean(), details: v.optional(v.string()) }),
      clientProfile: v.object({ met: v.boolean(), details: v.optional(v.string()) }),
      logistics: v.object({ met: v.boolean(), details: v.optional(v.string()) }),
      skillSetAlignment: v.object({ met: v.boolean(), details: v.optional(v.string()) }),
    }),
    aiProvider: v.optional(v.string()),
  },
  handler: async (ctx, args) => {
    const identity = await ctx.auth.getUserIdentity();
    
    return await ctx.db.insert("evaluations", {
      rfpId: args.rfpId,
      userId: identity?.subject,
      isFit: args.isFit,
      score: args.score,
      maxScore: args.maxScore,
      ...args.criteriaResults,
      aiProvider: args.aiProvider,
      evaluatedAt: Date.now(),
    });
  },
});
```

## Integration with Clerk

When using Convex with Clerk, configure authentication in `convex/auth.config.js`:

```javascript
export default {
  providers: [
    {
      domain: "https://your-clerk-domain.clerk.accounts.dev",
      applicationID: "convex",
    },
  ],
};
```

## React Hooks Usage

```tsx
import { useQuery, useMutation } from "convex/react";
import { api } from "../convex/_generated/api";

function RfpList() {
  const rfps = useQuery(api.rfps.listWithEvaluations, { limit: 50 });
  const saveEvaluation = useMutation(api.evaluations.saveEvaluation);
  
  // Component implementation
}
```

## Migration Strategy

1. **Phase 1**: Add Convex alongside existing localStorage
   - Create Convex schema
   - Add mutations to sync localStorage to Convex
   - Keep localStorage as fallback

2. **Phase 2**: Migrate reads to Convex
   - Replace localStorage reads with Convex queries
   - Add real-time subscriptions

3. **Phase 3**: Remove localStorage
   - Remove localStorage sync code
   - Use Convex as single source of truth
