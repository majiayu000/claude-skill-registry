---
name: cloudflare-workflows
description: "Cloudflare Workflows durable execution playbook: multi-step orchestration, state persistence, retries, sleep/scheduling, waitForEvent, external events, bindings, lifecycle management, limits, pricing. Keywords: Cloudflare Workflows, durable execution, WorkflowEntrypoint, step.do, step.sleep, waitForEvent, sendEvent, retries, NonRetryableError, Workflow binding."
---

# Cloudflare Workflows

Workflows provide durable multi-step execution for Workers. Steps persist state, survive restarts, support retries, and can sleep for days.

---

## Quick Start

### Create Workflow

```typescript
// src/index.ts
import { WorkflowEntrypoint, WorkflowStep, WorkflowEvent } from "cloudflare:workers";

interface Env {
  MY_WORKFLOW: Workflow;
}

interface Params {
  userId: string;
  action: string;
}

export class MyWorkflow extends WorkflowEntrypoint<Env, Params> {
  async run(event: WorkflowEvent<Params>, step: WorkflowStep) {
    const user = await step.do("fetch user", async () => {
      const resp = await fetch(`https://api.example.com/users/${event.payload.userId}`);
      return resp.json();
    });

    await step.sleep("wait before processing", "1 hour");

    const result = await step.do("process action", async () => {
      return { processed: true, user: user.id };
    });

    return result; // Available in instance.status().output
  }
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const instance = await env.MY_WORKFLOW.create({
      params: { userId: "123", action: "activate" },
    });
    return Response.json({ instanceId: instance.id });
  },
};
```

### wrangler.jsonc

```jsonc
{
  "name": "my-workflow-worker",
  "main": "src/index.ts",
  "workflows": [
    {
      "name": "my-workflow",
      "binding": "MY_WORKFLOW",
      "class_name": "MyWorkflow"
    }
  ]
}
```

### Deploy

```bash
npx wrangler deploy
```

---

## Core Concepts

### WorkflowEntrypoint

```typescript
export class MyWorkflow extends WorkflowEntrypoint<Env, Params> {
  async run(event: WorkflowEvent<Params>, step: WorkflowStep) {
    // Workflow logic with steps
    return optionalResult;
  }
}
```

### WorkflowEvent

```typescript
interface WorkflowEvent<T> {
  payload: Readonly<T>; // Immutable input params
  timestamp: Date; // Creation time
  instanceId: string; // Unique instance ID
}
```

**Warning**: Event payload is immutable. Changes are NOT persisted across steps. Return state from steps instead.

### WorkflowStep

```typescript
interface WorkflowStep {
  do<T>(name: string, callback: () => Promise<T>): Promise<T>;
  do<T>(name: string, config: StepConfig, callback: () => Promise<T>): Promise<T>;
  sleep(name: string, duration: Duration): Promise<void>;
  sleepUntil(name: string, timestamp: Date | number): Promise<void>;
  waitForEvent<T>(name: string, options: WaitOptions): Promise<T>;
}
```

See [api.md](references/api.md) for full type definitions.

---

## Steps

### Basic Step

```typescript
const result = await step.do("step name", async () => {
  const response = await fetch("https://api.example.com/data");
  return response.json(); // State persisted
});
```

### Step with Config

```typescript
const data = await step.do(
  "call external API",
  {
    retries: {
      limit: 10,
      delay: "30 seconds",
      backoff: "exponential",
    },
    timeout: "5 minutes",
  },
  async () => {
    return await externalApiCall();
  }
);
```

### Default Step Config

```typescript
const defaultConfig = {
  retries: {
    limit: 5,
    delay: 10000, // 10 seconds
    backoff: "exponential",
  },
  timeout: "10 minutes",
};
```

| Option            | Type          | Default     | Description                                 |
| ----------------- | ------------- | ----------- | ------------------------------------------- |
| `retries.limit`   | number        | 5           | Max attempts (use `Infinity` for unlimited) |
| `retries.delay`   | string/number | 10000       | Delay between retries                       |
| `retries.backoff` | string        | exponential | `constant`, `linear`, `exponential`         |
| `timeout`         | string/number | 10 min      | Per-attempt timeout                         |

---

## Sleep & Scheduling

### Relative Sleep

```typescript
await step.sleep("wait before retry", "1 hour");
await step.sleep("short pause", 5000); // 5 seconds (ms)
```

**Duration units**: `second`, `minute`, `hour`, `day`, `week`, `month`, `year`.

### Sleep Until Date

```typescript
const targetDate = new Date("2024-12-31T00:00:00Z");
await step.sleepUntil("wait until new year", targetDate);

// Or with timestamp
await step.sleepUntil("wait until launch", Date.parse("24 Oct 2024 13:00:00 UTC"));
```

**Maximum sleep**: 365 days.

**Note**: `step.sleep` and `step.sleepUntil` do NOT count towards the 1024 steps limit.

---

## Wait for Events

### Wait in Workflow

```typescript
const approval = await step.waitForEvent<{ approved: boolean }>("wait for approval", {
  type: "user_approval",
  timeout: "7 days",
});

if (approval.approved) {
  await step.do("proceed", async () => {
    /* ... */
  });
}
```

**Default timeout**: 24 hours.

**Timeout behavior**: Throws error and fails instance. Use try-catch to continue:

```typescript
try {
  const event = await step.waitForEvent("optional event", { type: "update", timeout: "1 hour" });
} catch (e) {
  // Continue without event
}
```

### Send Event from Worker

```typescript
export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const { instanceId, approved } = await request.json();
    const instance = await env.MY_WORKFLOW.get(instanceId);

    await instance.sendEvent({
      type: "user_approval", // Must match waitForEvent type
      payload: { approved },
    });

    return new Response("Event sent");
  },
};
```

**Event buffering**: Events can be sent before Workflow reaches `waitForEvent`. They are buffered and delivered when the matching step executes.

See [events.md](references/events.md) for REST API.

---

## Error Handling

### NonRetryableError

```typescript
import { NonRetryableError } from "cloudflare:workflows";

await step.do("validate input", async () => {
  if (!event.payload.data) {
    throw new NonRetryableError("Missing required data");
  }
  return event.payload.data;
});
```

### Catch and Continue

```typescript
try {
  await step.do("risky operation", async () => {
    await riskyApiCall();
  });
} catch (error) {
  await step.do("handle failure", async () => {
    await sendAlertEmail(error.message);
  });
}
```

### Workflow States

| Status            | Description                                |
| ----------------- | ------------------------------------------ |
| `queued`          | Waiting to start                           |
| `running`         | Actively executing                         |
| `paused`          | Manually paused                            |
| `waiting`         | Sleeping or waiting for event              |
| `waitingForPause` | Pause requested, waiting to take effect    |
| `complete`        | Successfully finished                      |
| `errored`         | Failed (uncaught exception or retry limit) |
| `terminated`      | Manually terminated                        |

---

## Workflow Bindings

### Create Instance

```typescript
const instance = await env.MY_WORKFLOW.create({
  id: "order-12345", // Optional custom ID (max 100 chars)
  params: { orderId: 12345 },
});
console.log(instance.id);
```

### Create Batch

```typescript
const instances = await env.MY_WORKFLOW.createBatch([{ params: { userId: "1" } }, { params: { userId: "2" } }, { params: { userId: "3" } }]);
// Up to 100 instances per batch
```

### Get Instance

```typescript
const instance = await env.MY_WORKFLOW.get("order-12345");
```

### Instance Methods

```typescript
await instance.pause(); // Pause execution
await instance.resume(); // Resume paused
await instance.terminate(); // Stop permanently
await instance.restart(); // Restart from beginning

const status = await instance.status();
console.log(status.status); // "running", "complete", etc.
console.log(status.output); // Return value from run()
console.log(status.error); // { name, message } if errored

await instance.sendEvent({
  type: "approval",
  payload: { approved: true },
});
```

---

## Rules of Workflows

### ✅ DO

- Make steps granular and self-contained
- Return state from steps (only way to persist)
- Name steps deterministically
- `await` all step calls
- Keep step return values under 1 MiB
- Use idempotent operations in steps
- Base conditions on `event.payload` or step returns

### ❌ DON'T

- Store state outside steps (lost on restart)
- Mutate `event.payload` (changes not persisted)
- Use non-deterministic step names (`Date.now()`, `Math.random()`)
- Skip `await` on step calls
- Put entire logic in one step
- Call multiple unrelated services in one step
- Do heavy CPU work in single step

### Step State Persistence

```typescript
// ✅ Good: Return state from step
const userData = await step.do("fetch user", async () => {
  return await fetchUser(userId);
});

// ❌ Bad: State stored outside step (lost on restart)
let userData;
await step.do("fetch user", async () => {
  userData = await fetchUser(userId); // Will be lost!
});
```

---

## Wrangler Commands

```bash
# List instances
wrangler workflows instances list my-workflow

# Describe instance
wrangler workflows instances describe my-workflow --id <instance-id>

# Terminate instance
wrangler workflows instances terminate my-workflow --id <instance-id>

# Trigger new instance
wrangler workflows trigger my-workflow --params '{"key": "value"}'

# Delete Workflow
wrangler workflows delete my-workflow
```

---

## Limits

| Feature                  | Free      | Paid               |
| ------------------------ | --------- | ------------------ |
| CPU time per step        | 10 ms     | 30 sec (max 5 min) |
| Wall clock per step      | Unlimited | Unlimited          |
| State per step           | 1 MiB     | 1 MiB              |
| Event payload            | 1 MiB     | 1 MiB              |
| Total state per instance | 100 MB    | 1 GB               |
| Max sleep duration       | 365 days  | 365 days           |
| Max steps per Workflow   | 1024      | 1024               |
| Concurrent instances     | 25        | 10,000             |
| Instance creation rate   | 100/sec   | 100/sec            |
| Queued instances         | 100,000   | 1,000,000          |
| Subrequests per instance | 50/req    | 1000/req           |
| Instance ID length       | 100 chars | 100 chars          |
| Retention (completed)    | 3 days    | 30 days            |

**Note**: Instances in `waiting` state (sleeping, waiting for event) do NOT count against concurrency limits.

### Increase CPU Limit

```jsonc
{
  "limits": {
    "cpu_ms": 300000 // 5 minutes
  }
}
```

---

## Pricing

Based on Workers Standard pricing:

| Metric   | Free              | Paid                            |
| -------- | ----------------- | ------------------------------- |
| Requests | 100K/day (shared) | 10M/mo included, +$0.30/M       |
| CPU time | 10 ms/invocation  | 30M ms/mo included, +$0.02/M ms |
| Storage  | 1 GB              | 1 GB included, +$0.20/GB-mo     |

**Storage notes**:

- Calculated across all instances (running, sleeping, completed)
- Deleting instances frees storage (updates within minutes)
- Free plan: instance errors if storage limit reached

See [pricing.md](references/pricing.md) for details.

---

## Prohibitions

- ❌ Do not mutate `event.payload` (changes not persisted)
- ❌ Do not store state outside steps
- ❌ Do not use non-deterministic step names
- ❌ Do not exceed 1 MiB per step return
- ❌ Do not skip `await` on step calls
- ❌ Do not rely on in-memory state between steps

---

## References

- [api.md](references/api.md) — Full API reference
- [events.md](references/events.md) — Event handling and REST API
- [patterns.md](references/patterns.md) — Saga, approval, reminders
- [pricing.md](references/pricing.md) — Billing details

## Cross-References (Skills)

- `cloudflare-workers` — Worker development
- `cloudflare-queues` — Message queue integration
- `cloudflare-r2` — Large state storage
- `cloudflare-kv` — Key-value references
