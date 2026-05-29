---
name: inngest-handler
description: Create and manage Inngest functions for reliable background jobs, workflows, and scheduled tasks.
---

# Inngest Function Handler Skill

This skill defines the standards for building durable, multi-step workflows using Inngest.

## 🚨 HARD RULES (Strictly Follow)

1.  **NO `setTimeout` / `setInterval`**:
    -   ❌ **Bad**: `await new Promise(r => setTimeout(r, 1000))`
    -   ✅ **Good**: `await step.sleep("wait-1s", "1s")`
    -   *Reason*: Serverless functions time out; Inngest sleeps persist for up to a year.

2.  **NO Side Effects Outside Steps**:
    -   Any database write, API call, or non-deterministic logic (random, date) **MUST** be wrapped in `step.run()`.
    -   *Reason*: Inngest functions execute multiple times (memoization). Code outside steps runs every time.

3.  **Deterministic Steps**:
    -   Steps are memoized by their ID (1st arg). IDs must be unique and stable.
    -   Do not dynamically generate step IDs unless you know what you are doing (e.g., inside loops with index).

4.  **Return Data from Steps**:
    -   If you need a value later, return it from the step.
    -   ❌ **Bad**: `let userId; await step.run(..., () => { userId = ... })`
    -   ✅ **Good**: `const userId = await step.run(..., () => { return ... })`

## Core Patterns

### 1. Multi-Step Execution
Wrap all logic in steps to ensure retriability and resumability.

```typescript
export const processOrder = inngest.createFunction(
  { id: "process-order" },
  { event: "shop/order.created" },
  async ({ event, step }) => {
    // 1. Step: Validate (Retriable)
    const user = await step.run("get-user", async () => {
      return await db.users.findById(event.data.userId);
    });

    // 2. Step: Sleep (Durable pause)
    await step.sleep("wait-for-payment", "1h");

    // 3. Step: Wait for Event (Human/System interaction)
    const payment = await step.waitForEvent("wait-payment", {
      event: "shop/payment.success",
      match: "data.orderId",
      timeout: "24h"
    });

    // 4. Step: Conditional Logic
    if (!payment) {
        await step.run("cancel-order", async () => { ... });
    }
  }
);
```

### 2. Parallelism
Run steps concurrently to speed up execution.

```typescript
const [user, subscription] = await Promise.all([
  step.run("fetch-user", () => db.users.find(...)),
  step.run("fetch-sub", () => stripe.subscriptions.retrieve(...))
]);
```

### 3. Working with Loops
Inside loops, ensure step IDs are unique.

```typescript
const items = event.data.items;
for (const item of items) {
  // Use dynamic ID to ensure uniqueness per item
  await step.run(`process-item-${item.id}`, async () => {
    await processItem(item);
    });
}
```

## Configuration & Flow Control

### Rate Limiting & Throttling
Prevent overwhelming 3rd party APIs.

```typescript
inngest.createFunction({
    id: "sync-crm",
    // Max 10 requests per minute per user
    rateLimit: { limit: 10, period: "1m", key: "event.data.userId" },
    // Drop events if queue is full
    throttle: { limit: 5, period: "1s" } 
}, ...);
```

### Debounce
Process only the latest event in a window (e.g., search indexing).

```typescript
inngest.createFunction({
    id: "index-product",
    // Wait 10s for more events; only run with the latest data
    debounce: { period: "10s", key: "event.data.productId" }
}, ...);
```

### Priority
Prioritize specific events (e.g., Paid users).

```typescript
inngest.createFunction({
    id: "generate-report",
    // High number = High priority
    priority: { run: "event.data.plan === 'enterprise' ? 100 : 0" }
}, ...);
```

## Error Handling

### Automatic Retries
Inngest retries steps automatically on error (default ~4-5 times with backoff).
-   **Customize**: `{ retries: 10 }` in config.

### Non-Retriable Errors
Stop execution immediately if the error is fatal (e.g., 400 Bad Request).

```typescript
import { NonRetriableError } from "inngest";

await step.run("validate", async () => {
  if (!isValid) throw new NonRetriableError("Invalid payload");
});
```

### Failure Handlers (Rollbacks)
Execute cleanup logic if the function fails after all retries.

```typescript
export const riskyFunc = inngest.createFunction(
  { 
    id: "risky-transfer",
    // Runs if main handler fails
    onFailure: async ({ error, event, step }) => {
      await step.run("rollback-funds", async () => {
        await reverseTransfer(event.data.transferId);
      });
      await step.run("notify-admin", async () => {
        await sendAlert(`Transfer failed: ${error.message}`);
      });
    }
  },
  { event: "bank/transfer.init" },
  async ({ step }) => { /* ... */ }
);
```

## Registration
**MANDATORY**: All functions must be imported and exported in `src/lib/inngest/functions/index.ts`.
