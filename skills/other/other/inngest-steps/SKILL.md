---
name: inngest-steps
description: Use Inngest step methods to build durable workflows. Covers step.run, step.sleep, step.waitForEvent, step.waitForSignal, step.sendEvent, step.invoke, step.ai, and patterns for loops and parallel execution.
---

# Inngest Steps

Build robust, durable workflows with Inngest's step methods. Each step is a separate HTTP request that can be independently retried and monitored.

> **These skills are focused on TypeScript.** For Python or Go, refer to the [Inngest documentation](https://www.inngest.com/llms.txt) for language-specific guidance. Core concepts apply across all languages.

## Core Concept

**🔄 Critical: Each step re-runs your function from the beginning.** Put ALL non-deterministic code (API calls, DB queries, randomness) inside steps, never outside.

**📊 Step Limits:** Every function has a maximum of 1,000 steps and 4MB total step data.

```typescript
// ❌ WRONG - will run 4 times
export default inngest.createFunction(
  { id: "bad-example" },
  { event: "test" },
  async ({ step }) => {
    console.log("This logs 4 times!"); // Outside step = bad
    await step.run("a", () => console.log("a"));
    await step.run("b", () => console.log("b"));
    await step.run("c", () => console.log("c"));
  }
);

// ✅ CORRECT - logs once each
export default inngest.createFunction(
  { id: "good-example" },
  { event: "test" },
  async ({ step }) => {
    await step.run("log-hello", () => console.log("hello"));
    await step.run("a", () => console.log("a"));
    await step.run("b", () => console.log("b"));
    await step.run("c", () => console.log("c"));
  }
);
```

## step.run()

Execute retriable code as a step. **Each step ID can be reused** - Inngest automatically handles counters.

```typescript
// Basic usage
const result = await step.run("fetch-user", async () => {
  const user = await db.user.findById(userId);
  return user; // Always return useful data
});

// Synchronous code works too
const transformed = await step.run("transform-data", () => {
  return processData(result);
});

// Side effects (no return needed)
await step.run("send-notification", async () => {
  await sendEmail(user.email, "Welcome!");
});
```

**✅ DO:**

- Put ALL non-deterministic logic inside steps
- Return useful data for subsequent steps
- Reuse step IDs in loops (counters handled automatically)

**❌ DON'T:**

- Put deterministic logic in steps unnecessarily
- Forget that each step = separate HTTP request

## step.sleep()

Pause execution without using compute time.

```typescript
// Duration strings
await step.sleep("wait-24h", "24h");
await step.sleep("short-delay", "30s");
await step.sleep("weekly-pause", "7d");

// Use in workflows
await step.run("send-welcome", () => sendEmail(email));
await step.sleep("wait-for-engagement", "3d");
await step.run("send-followup", () => sendFollowupEmail(email));
```

## step.sleepUntil()

Sleep until a specific datetime.

```typescript
const reminderDate = new Date("2024-12-25T09:00:00Z");
await step.sleepUntil("wait-for-christmas", reminderDate);

// From event data
const scheduledTime = new Date(event.data.remind_at);
await step.sleepUntil("wait-for-scheduled-time", scheduledTime);
```

## step.waitForEvent()

**🚨 CRITICAL: waitForEvent ONLY catches events sent AFTER this step executes.**

- ❌ Event sent before waitForEvent runs → will NOT be caught
- ✅ Event sent after waitForEvent runs → will be caught
- Always check for `null` return (means timeout, event never arrived)

```typescript
// Basic event waiting with timeout
const approval = await step.waitForEvent("wait-for-approval", {
  event: "app/invoice.approved",
  timeout: "7d",
  match: "data.invoiceId" // Simple matching
});

// Expression-based matching (CEL syntax)
const subscription = await step.waitForEvent("wait-for-subscription", {
  event: "app/subscription.created",
  timeout: "30d",
  if: "event.data.userId == async.data.userId && async.data.plan == 'pro'"
});

// Handle timeout
if (!approval) {
  await step.run("handle-timeout", () => {
    // Approval never came
    return notifyAccountingTeam();
  });
}
```

**✅ DO:**

- Use unique IDs for matching (userId, sessionId, requestId)
- Always set reasonable timeouts
- Handle null return (timeout case)
- Use with Realtime for human-in-the-loop flows

**❌ DON'T:**

- Expect events sent before this step to be handled
- Use without timeouts in production

### Expression Syntax

In expressions, `event` = the **original** triggering event, `async` = the **new** event being matched. See [Expression Syntax Reference](../references/expressions.md) for full syntax, operators, and patterns.

## step.waitForSignal()

Wait for unique signals (not events). Better for 1:1 matching.

```typescript
const taskId = "task-" + crypto.randomUUID();

const signal = await step.waitForSignal("wait-for-task-completion", {
  signal: taskId,
  timeout: "1h",
  onConflict: "replace" // Required: "replace" overwrites pending signal, "fail" throws an error
});

// Send signal elsewhere via Inngest API or SDK
// POST /v1/events with signal matching taskId
```

**When to use:**

- **waitForEvent**: Multiple functions might handle the same event
- **waitForSignal**: Exact 1:1 signal to specific function run

## step.sendEvent()

Fan out to other functions without waiting for results.

```typescript
// Trigger other functions
await step.sendEvent("notify-systems", {
  name: "user/profile.updated",
  data: { userId: user.id, changes: profileChanges }
});

// Multiple events at once
await step.sendEvent("batch-notifications", [
  { name: "billing/invoice.created", data: { invoiceId } },
  { name: "email/invoice.send", data: { email: user.email, invoiceId } }
]);
```

**Use when:** You want to trigger other functions but don't need their results in the current function.

## step.invoke()

Call other functions and handle their results. Perfect for composition.

```typescript
const computeSquare = inngest.createFunction(
  { id: "compute-square" },
  { event: "calculate/square" },
  async ({ event }) => {
    return { result: event.data.number * event.data.number };
  }
);

// Invoke and use result
const square = await step.invoke("get-square", {
  function: computeSquare,
  data: { number: 4 }
});

console.log(square.result); // 16, fully typed!
```

**Great for:**

- Breaking complex workflows into composable functions
- Reusing logic across multiple workflows
- Map-reduce patterns

## Patterns

### Loops with Steps

Reuse step IDs - Inngest handles counters automatically.

```typescript
const allProducts = [];
let cursor = null;
let hasMore = true;

while (hasMore) {
  // Same ID "fetch-page" reused - counters handled automatically
  const page = await step.run("fetch-page", async () => {
    return shopify.products.list({ cursor, limit: 50 });
  });

  allProducts.push(...page.products);

  if (page.products.length < 50) {
    hasMore = false;
  } else {
    cursor = page.products[49].id;
  }
}

await step.run("process-products", () => {
  return processAllProducts(allProducts);
});
```

### Parallel Execution

Use Promise.all for parallel steps.

```typescript
// Create steps without awaiting
const sendEmail = step.run("send-email", async () => {
  return await sendWelcomeEmail(user.email);
});

const updateCRM = step.run("update-crm", async () => {
  return await crmService.addUser(user);
});

const createSubscription = step.run("create-subscription", async () => {
  return await subscriptionService.create(user.id);
});

// Run all in parallel
const [emailId, crmRecord, subscription] = await Promise.all([
  sendEmail,
  updateCRM,
  createSubscription
]);

// Optimization: Enable optimizeParallelism for many parallel steps
export default inngest.createFunction(
  {
    id: "parallel-heavy-function",
    optimizeParallelism: true // Reduces HTTP requests by ~50%
  },
  { event: "process/batch" },
  async ({ event, step }) => {
    const results = await Promise.all(
      event.data.items.map((item, i) =>
        step.run(`process-item-${i}`, () => processItem(item))
      )
    );
  }
);
```

See **inngest-flow-control** for concurrency and throttling options.

### Chunking Jobs

Perfect for batch processing with parallel steps.

```typescript
export default inngest.createFunction(
  { id: "process-large-dataset" },
  { event: "data/process.large" },
  async ({ event, step }) => {
    const chunks = chunkArray(event.data.items, 10);

    // Process chunks in parallel
    const results = await Promise.all(
      chunks.map((chunk, index) =>
        step.run(`process-chunk-${index}`, () => processChunk(chunk))
      )
    );

    // Combine results
    await step.run("combine-results", () => {
      return aggregateResults(results);
    });
  }
);
```

## Key Gotchas

**🔄 Function Re-execution:** Code outside steps runs on every step execution
**⏰ Event Timing:** waitForEvent only catches events sent AFTER the step runs
**🔢 Step Limits:** Max 1,000 steps per function, 4MB per step output, 32MB per function run in total
**📨 HTTP Requests:** With `serve`, use `checkpointing` to reduce HTTP requests
**🔁 Step IDs:** Can be reused in loops - Inngest handles counters
**⚡ Parallelism:** Use Promise.all, consider optimizeParallelism for many steps

## Common Use Cases

- **Human-in-the-loop:** waitForEvent + Realtime UI
- **Multi-step onboarding:** sleep between steps, waitForEvent for user actions
- **Data processing:** Parallel steps for chunked work
- **External integrations:** step.run for reliable API calls
- **AI workflows:** step.ai for durable LLM orchestration
- **Function composition:** step.invoke to build complex workflows

Remember: Steps make your functions durable, observable, and debuggable. Embrace them!
