---
name: "Convex Agents Usage Tracking"
description: "Tracks LLM token consumption and usage metrics for billing, monitoring, and optimization. Use this to log token usage, calculate costs, generate invoices, and understand which agents or users consume the most resources."
---

## Purpose

Usage tracking records how many tokens each agent uses, enabling accurate billing, cost monitoring, and performance optimization. Essential for understanding LLM costs and user impact.

## When to Use This Skill

- Billing users based on token consumption
- Monitoring API costs
- Optimizing agent efficiency
- Tracking usage by user, agent, or team
- Generating invoices and cost reports
- Alerting on high usage
- Analyzing cost trends

## How to Use It

### 1. Configure Usage Handler

Create a handler to log usage:

```typescript
// convex/agents/myAgent.ts
import { Agent } from "@convex-dev/agent";
import { components } from "../_generated/api";
import { openai } from "@ai-sdk/openai";
import { internal } from "../_generated/api";

const myAgent = new Agent(components.agent, {
  name: "My Agent",
  languageModel: openai.chat("gpt-4o-mini"),
  usageHandler: async (ctx, args) => {
    const {
      userId,
      threadId,
      agentName,
      model,
      provider,
      usage, // { inputTokens, outputTokens, totalTokens }
      providerMetadata,
    } = args;

    // Save usage to database
    await ctx.runMutation(internal.usage.recordUsage, {
      userId,
      threadId,
      agentName,
      model,
      provider,
      inputTokens: usage.inputTokens,
      outputTokens: usage.outputTokens,
      totalTokens: usage.totalTokens,
      timestamp: Date.now(),
    });
  },
});
```

### 2. Store Usage Records

Save usage data for later analysis:

```typescript
// convex/usage.ts
import { internalMutation } from "./_generated/server";
import { v } from "convex/values";
import { defineTable, defineSchema } from "convex/server";

export const schema = defineSchema({
  usage: defineTable({
    userId: v.string(),
    threadId: v.optional(v.string()),
    agentName: v.optional(v.string()),
    model: v.string(),
    provider: v.string(),
    inputTokens: v.number(),
    outputTokens: v.number(),
    totalTokens: v.number(),
    cost: v.number(), // Cost in dollars
    date: v.string(), // ISO date for daily rollups
    billingPeriod: v.string(), // YYYY-MM for monthly
  })
    .index("billingPeriod_userId", ["billingPeriod", "userId"])
    .index("date_userId", ["date", "userId"])
    .index("userId", ["userId"]),

  invoices: defineTable({
    userId: v.string(),
    billingPeriod: v.string(),
    amount: v.number(),
    status: v.union(
      v.literal("pending"),
      v.literal("paid"),
      v.literal("failed")
    ),
    generatedAt: v.number(),
  })
    .index("billingPeriod_userId", ["billingPeriod", "userId"])
    .index("userId", ["userId"]),
});

export const recordUsage = internalMutation({
  args: {
    userId: v.string(),
    threadId: v.optional(v.string()),
    agentName: v.optional(v.string()),
    model: v.string(),
    provider: v.string(),
    inputTokens: v.number(),
    outputTokens: v.number(),
    totalTokens: v.number(),
  },
  handler: async (
    ctx,
    {
      userId,
      threadId,
      agentName,
      model,
      provider,
      inputTokens,
      outputTokens,
      totalTokens,
    }
  ) => {
    const today = new Date().toISOString().split("T")[0];
    const billingPeriod = today.substring(0, 7); // YYYY-MM

    // Calculate cost (example: $0.015 per 1M input tokens, $0.060 per 1M output)
    const cost =
      (inputTokens / 1_000_000) * 0.015 + (outputTokens / 1_000_000) * 0.06;

    await ctx.db.insert("usage", {
      userId,
      threadId,
      agentName,
      model,
      provider,
      inputTokens,
      outputTokens,
      totalTokens,
      cost,
      date: today,
      billingPeriod,
    });
  },
});
```

### 3. Query Usage by User

Get total usage for a specific user:

```typescript
// convex/usage.ts
import { query } from "./_generated/server";
import { v } from "convex/values";

export const getUserUsage = query({
  args: { userId: v.string() },
  handler: async (ctx, { userId }) => {
    const records = await ctx.db
      .query("usage")
      .withIndex("userId", (q) => q.eq("userId", userId))
      .collect();

    const totals = records.reduce(
      (acc, record) => ({
        inputTokens: acc.inputTokens + record.inputTokens,
        outputTokens: acc.outputTokens + record.outputTokens,
        totalTokens: acc.totalTokens + record.totalTokens,
        cost: acc.cost + record.cost,
      }),
      { inputTokens: 0, outputTokens: 0, totalTokens: 0, cost: 0 }
    );

    return totals;
  },
});

export const getMonthlyUsageByUser = query({
  args: { billingPeriod: v.string() },
  handler: async (ctx, { billingPeriod }) => {
    const records = await ctx.db
      .query("usage")
      .withIndex("billingPeriod_userId", (q) =>
        q.eq("billingPeriod", billingPeriod)
      )
      .collect();

    // Group by userId
    const byUser: Record<string, any> = {};
    for (const record of records) {
      if (!byUser[record.userId]) {
        byUser[record.userId] = {
          userId: record.userId,
          totalTokens: 0,
          cost: 0,
          records: 0,
        };
      }
      byUser[record.userId].totalTokens += record.totalTokens;
      byUser[record.userId].cost += record.cost;
      byUser[record.userId].records += 1;
    }

    return Object.values(byUser);
  },
});
```

### 4. Generate Monthly Invoices

Create invoices from usage data:

```typescript
// convex/usage.ts
import { action } from "./_generated/server";
import { v } from "convex/values";

export const generateInvoices = action({
  args: { billingPeriod: v.string() },
  handler: async (ctx, { billingPeriod }) => {
    // Get all usage for the period
    const records = await ctx.db
      .query("usage")
      .withIndex("billingPeriod_userId", (q) =>
        q.eq("billingPeriod", billingPeriod)
      )
      .collect();

    // Group by user
    const byUser: Record<string, number> = {};
    for (const record of records) {
      byUser[record.userId] = (byUser[record.userId] || 0) + record.cost;
    }

    // Create invoices
    for (const [userId, amount] of Object.entries(byUser)) {
      const existingInvoice = await ctx.db
        .query("invoices")
        .filter(
          (inv) =>
            inv.billingPeriod === billingPeriod && inv.userId === userId
        )
        .first();

      if (!existingInvoice) {
        await ctx.db.insert("invoices", {
          userId,
          billingPeriod,
          amount,
          status: "pending",
          generatedAt: Date.now(),
        });
      }
    }

    return { invoicesCreated: Object.keys(byUser).length };
  },
});
```

### 5. Track Usage by Agent

Compare efficiency across agents:

```typescript
// convex/usage.ts
import { query } from "./_generated/server";
import { v } from "convex/values";

export const getUsageByAgent = query({
  args: { userId: v.string(), billingPeriod: v.string() },
  handler: async (ctx, { userId, billingPeriod }) => {
    const records = await ctx.db
      .query("usage")
      .withIndex("billingPeriod_userId", (q) =>
        q.eq("billingPeriod", billingPeriod)
      )
      .filter((r) => r.userId === userId)
      .collect();

    // Group by agent
    const byAgent: Record<string, any> = {};
    for (const record of records) {
      const agent = record.agentName || "unknown";
      if (!byAgent[agent]) {
        byAgent[agent] = {
          agent,
          totalTokens: 0,
          inputTokens: 0,
          outputTokens: 0,
          cost: 0,
          calls: 0,
        };
      }
      byAgent[agent].totalTokens += record.totalTokens;
      byAgent[agent].inputTokens += record.inputTokens;
      byAgent[agent].outputTokens += record.outputTokens;
      byAgent[agent].cost += record.cost;
      byAgent[agent].calls += 1;
    }

    return Object.values(byAgent).sort((a, b) => b.cost - a.cost);
  },
});
```

### 6. Set Up Scheduled Invoice Generation

Generate invoices automatically monthly:

```typescript
// convex/crons.ts
import { cronJobs } from "convex/server";
import { internal } from "./_generated/api";

const crons = cronJobs();

// Generate invoices on the 2nd day of each month at midnight UTC
crons.monthly(
  "generateMonthlyInvoices",
  { day: 2, hourUTC: 0, minuteUTC: 0 },
  internal.usage.generateInvoices,
  { billingPeriod: calculatePreviousMonth() }
);

export default crons;

function calculatePreviousMonth(): string {
  const now = new Date();
  const month = now.getMonth() === 0 ? 11 : now.getMonth() - 1;
  const year = now.getMonth() === 0 ? now.getFullYear() - 1 : now.getFullYear();
  return `${year}-${String(month + 1).padStart(2, "0")}`;
}
```

### 7. Monitor Usage Alerts

Alert on high usage:

```typescript
// convex/usage.ts
import { action } from "./_generated/server";
import { v } from "convex/values";

export const checkUsageAlerts = action({
  args: {},
  handler: async (ctx, {}) => {
    const today = new Date().toISOString().split("T")[0];

    // Get today's usage by user
    const records = await ctx.db
      .query("usage")
      .filter((r) => r.date === today)
      .collect();

    const byUser: Record<string, number> = {};
    for (const record of records) {
      byUser[record.userId] = (byUser[record.userId] || 0) + record.cost;
    }

    // Alert on users exceeding $100/day
    const alerts = [];
    for (const [userId, cost] of Object.entries(byUser)) {
      if (cost > 100) {
        alerts.push({ userId, cost, reason: "Daily spend exceeded $100" });
      }
    }

    // Send alerts (email, Slack, etc.)
    for (const alert of alerts) {
      await ctx.runMutation(internal.notifications.sendAlert, alert);
    }

    return alerts;
  },
});
```

### 8. Usage Analytics Dashboard

Query usage for display:

```typescript
// convex/usage.ts
import { query } from "./_generated/server";

export const getDashboardStats = query({
  args: { userId: v.string() },
  handler: async (ctx, { userId }) => {
    // This month's usage
    const today = new Date();
    const billingPeriod = `${today.getFullYear()}-${String(
      today.getMonth() + 1
    ).padStart(2, "0")}`;

    const monthlyRecords = await ctx.db
      .query("usage")
      .withIndex("billingPeriod_userId", (q) =>
        q.eq("billingPeriod", billingPeriod)
      )
      .filter((r) => r.userId === userId)
      .collect();

    const monthlyStats = monthlyRecords.reduce(
      (acc, r) => ({
        totalTokens: acc.totalTokens + r.totalTokens,
        cost: acc.cost + r.cost,
      }),
      { totalTokens: 0, cost: 0 }
    );

    // All time
    const allRecords = await ctx.db
      .query("usage")
      .withIndex("userId", (q) => q.eq("userId", userId))
      .collect();

    const allTimeStats = allRecords.reduce(
      (acc, r) => ({
        totalTokens: acc.totalTokens + r.totalTokens,
        cost: acc.cost + r.cost,
      }),
      { totalTokens: 0, cost: 0 }
    );

    return {
      monthly: monthlyStats,
      allTime: allTimeStats,
      averageDailyCost: monthlyStats.cost / Math.min(today.getDate(), 30),
    };
  },
});
```

## Key Principles

- **Record at generation time**: Capture usage in usageHandler
- **Calculate costs accurately**: Use provider-specific pricing
- **Monthly periods**: Align invoices with calendar months
- **User attribution**: Always track which user generated usage
- **Agent tracking**: Know which agents are most expensive
- **Archival**: Archive old usage data for compliance

## Example: Complete Billing System

```typescript
// convex/billing/complete.ts
import { Agent } from "@convex-dev/agent";
import { components } from "../_generated/api";
import { openai } from "@ai-sdk/openai";
import { internal } from "../_generated/api";

// Cost per million tokens
const PRICING = {
  "gpt-4o-mini": {
    input: 0.015,
    output: 0.06,
  },
};

export const billingAgent = new Agent(components.agent, {
  name: "Billing Agent",
  languageModel: openai.chat("gpt-4o-mini"),
  usageHandler: async (ctx, { usage, userId, model }) => {
    if (!userId) return;

    const pricing = PRICING[model as keyof typeof PRICING] || {
      input: 0.001,
      output: 0.002,
    };

    const cost =
      (usage.inputTokens / 1_000_000) * pricing.input +
      (usage.outputTokens / 1_000_000) * pricing.output;

    await ctx.runMutation(internal.billing.recordUsage, {
      userId,
      model,
      inputTokens: usage.inputTokens,
      outputTokens: usage.outputTokens,
      totalTokens: usage.totalTokens,
      cost,
    });
  },
});
```

## Common Patterns

- **Per-user billing**: Each user gets an invoice
- **Team billing**: Aggregate across team members
- **Pay-as-you-go**: Immediate billing per message
- **Monthly invoicing**: Collect charges at month end
- **Usage tiers**: Discounts for high-volume users
- **Prepaid credits**: Users buy credit packages

## Next Steps

- **Implement rate limiting**: See **Convex Agents Rate Limiting** to control costs
- **Add alerts**: Send notifications for high usage
- **Build dashboards**: Display usage analytics to users
- **Optimize costs**: Analyze which agents are most expensive

## Troubleshooting

- **Missing usage records**: Check usageHandler is configured
- **Pricing mismatches**: Verify cost calculations match your provider
- **Large invoices**: Check for runaway token generation
- **Monthly timing**: Verify billing period calculation aligns with your fiscal year
