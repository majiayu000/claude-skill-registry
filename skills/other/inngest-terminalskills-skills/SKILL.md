---
name: inngest
description: >-
  You are an expert in Inngest, the event-driven durable workflow engine for
  TypeScript. You help developers build reliable multi-step workflows,
  scheduled jobs, and event-driven functions with automatic retries,
  step-level caching, fan-out/fan-in patterns, rate limiting, and debouncing —
  running on any serverless platform (Vercel, Netlify, AWS Lambda, Cloudflare)
  with zero infrastructure to manage.
license: Apache-2.0
compatibility: ''
metadata:
  author: terminal-skills
  version: 1.0.0
  category: Backend Development
  tags:
    - workflow
    - event-driven
    - durable
    - serverless
    - typescript
    - step-functions
---

# Inngest — Durable Workflow Engine for TypeScript

You are an expert in Inngest, the event-driven durable workflow engine for TypeScript. You help developers build reliable multi-step workflows, scheduled jobs, and event-driven functions with automatic retries, step-level caching, fan-out/fan-in patterns, rate limiting, and debouncing — running on any serverless platform (Vercel, Netlify, AWS Lambda, Cloudflare) with zero infrastructure to manage.

## Core Capabilities

### Functions and Steps

```typescript
// inngest/functions/onboarding.ts
import { inngest } from "./client";

export const onboardUser = inngest.createFunction(
  {
    id: "onboard-user",
    retries: 3,
    concurrency: [{ limit: 10 }],         // Max 10 concurrent executions
  },
  { event: "user/signed-up" },
  async ({ event, step }) => {
    // Step 1: Create account (cached — won't re-run on retry)
    const user = await step.run("create-account", async () => {
      return await db.users.create({
        email: event.data.email,
        name: event.data.name,
      });
    });

    // Step 2: Send welcome email
    await step.run("send-welcome", async () => {
      await resend.emails.send({
        to: user.email,
        subject: "Welcome!",
        react: WelcomeEmail({ name: user.name }),
      });
    });

    // Step 3: Wait 24 hours (durable — survives deployments)
    await step.sleep("wait-for-activation", "24 hours");

    // Step 4: Check if user activated
    const activated = await step.run("check-activation", async () => {
      const u = await db.users.findById(user.id);
      return u.activatedAt !== null;
    });

    if (!activated) {
      // Step 5: Send reminder
      await step.run("send-reminder", async () => {
        await resend.emails.send({
          to: user.email,
          subject: "Complete your setup",
          react: ReminderEmail({ name: user.name }),
        });
      });
    }

    return { userId: user.id, activated };
  },
);

// Fan-out: process items in parallel
export const processBatch = inngest.createFunction(
  { id: "process-batch" },
  { event: "batch/uploaded" },
  async ({ event, step }) => {
    const items = event.data.items;

    // Fan-out — run up to 10 items in parallel
    const results = await Promise.all(
      items.map((item, i) =>
        step.run(`process-item-${i}`, () => processItem(item))
      ),
    );

    // Fan-in — aggregate results
    const summary = await step.run("summarize", () => ({
      total: results.length,
      success: results.filter(r => r.status === "ok").length,
      failed: results.filter(r => r.status === "error").length,
    }));

    return summary;
  },
);

// Scheduled (cron)
export const dailyCleanup = inngest.createFunction(
  { id: "daily-cleanup" },
  { cron: "0 3 * * *" },                 // 3 AM daily
  async ({ step }) => {
    const deleted = await step.run("cleanup-expired", async () => {
      return await db.sessions.deleteWhere({ expiresAt: { lt: new Date() } });
    });
    return { deletedSessions: deleted };
  },
);
```

### Event-Driven

```typescript
// Send events from anywhere
import { inngest } from "./client";

// From API route
app.post("/api/signup", async (req, res) => {
  const user = await createUser(req.body);

  await inngest.send({
    name: "user/signed-up",
    data: { email: user.email, name: user.name, userId: user.id },
  });

  res.json(user);
});

// Batch events
await inngest.send([
  { name: "order/created", data: { orderId: "1" } },
  { name: "order/created", data: { orderId: "2" } },
]);
```

### Debounce and Rate Limit

```typescript
export const syncCRM = inngest.createFunction(
  {
    id: "sync-crm",
    debounce: { period: "5m", key: "event.data.userId" },  // Wait 5min, take latest
    rateLimit: { limit: 100, period: "1h" },                // Max 100/hour
  },
  { event: "user/updated" },
  async ({ event, step }) => {
    await step.run("sync", () => crm.upsertContact(event.data));
  },
);
```

## Installation

```bash
npx inngest-cli@latest init
npx inngest-cli@latest dev                 # Local dev server with UI
```

## Best Practices

1. **Steps are checkpoints** — Each `step.run()` is cached; if the function retries, completed steps are skipped
2. **step.sleep for delays** — Durable sleep survives deployments and restarts; use for drip campaigns, reminders
3. **Fan-out with step.run** — Use `Promise.all` with indexed step names for parallel processing
4. **Debounce for noisy events** — Use debounce for events that fire rapidly (user edits, webhook storms)
5. **Rate limiting** — Protect downstream APIs with built-in rate limits; no external tools needed
6. **Event-first architecture** — Send events from your app; Inngest triggers functions automatically
7. **Local dev UI** — Run `inngest dev` for a visual dashboard showing function runs, events, and step details
8. **Zero infrastructure** — Works on any serverless platform; Inngest handles queuing, retries, scheduling
