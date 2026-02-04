---
name: cloudflare-workflows
description: Cloudflare Workflows for durable long-running execution. Use for multi-step workflows, retries, state persistence, or encountering NonRetryableError, execution failed errors.

  Keywords: cloudflare workflows, workflows workers, durable execution, workflow step,
  WorkflowEntrypoint, step.do, step.sleep, workflow retries, NonRetryableError,
  workflow state, wrangler workflows, workflow events, long-running tasks, step.sleepUntil,
  step.waitForEvent, workflow bindings
license: MIT
metadata:
  version: "3.0.0"
  wrangler_version: "4.50.0"
  workers_types_version: "4.20251126.0"
  last_verified: "2025-12-27"
  errors_prevented: 5
  templates_included: 8
  references_included: 8
  agents_included: 3
  commands_included: 4
  scripts_included: 5
---

# Cloudflare Workflows

**Status**: Production Ready ✅ | **Last Verified**: 2025-12-27 | **Version**: 3.0.0

**Dependencies**: cloudflare-worker-base (for Worker setup)

**Contents**: [Quick Start](#quick-start-10-minutes) • [Commands](#commands) • [Agents](#agents) • [Core Concepts](#core-concepts) • [Critical Rules](#critical-rules) • [Top Errors](#top-5-errors-critical) • [Common Patterns](#common-patterns) • [When to Load References](#when-to-load-references) • [Limits](#limits--pricing)

---

## Quick Start (10 Minutes)

### 1. Create a Workflow

Use the Cloudflare Workflows starter template:

```bash
npm create cloudflare@latest my-workflow -- --template cloudflare/workflows-starter --git --deploy false
cd my-workflow
```

**What you get:**
- WorkflowEntrypoint class template
- Worker to trigger workflows
- Complete wrangler.jsonc configuration

### 2. Basic Workflow Structure

**src/index.ts:**

```typescript
import { WorkflowEntrypoint, WorkflowStep, WorkflowEvent } from 'cloudflare:workers';

type Env = {
  MY_WORKFLOW: Workflow;
};

type Params = {
  userId: string;
  email: string;
};

export class MyWorkflow extends WorkflowEntrypoint<Env, Params> {
  async run(event: WorkflowEvent<Params>, step: WorkflowStep) {
    const { userId, email } = event.payload;

    // Step 1: Do work with automatic retries
    const result = await step.do('process user', async () => {
      return { processed: true, userId };
    });

    // Step 2: Wait before next step
    await step.sleep('wait 1 hour', '1 hour');

    // Step 3: Continue workflow
    await step.do('send email', async () => {
      return { sent: true, email };
    });

    return { completed: true, userId };
  }
}

// Worker to trigger workflow
export default {
  async fetch(req: Request, env: Env): Promise<Response> {
    const instance = await env.MY_WORKFLOW.create({
      params: { userId: '123', email: 'user@example.com' }
    });

    return Response.json({
      id: instance.id,
      status: await instance.status()
    });
  }
};
```

**Template**: See `templates/basic-workflow.ts` for complete example

### 3. Configure wrangler.jsonc

```jsonc
{
  "name": "my-workflow",
  "main": "src/index.ts",
  "compatibility_date": "2025-10-22",
  "workflows": [
    {
      "binding": "MY_WORKFLOW",
      "name": "my-workflow",
      "class_name": "MyWorkflow"
    }
  ]
}
```

**Template**: See `templates/wrangler-workflows-config.jsonc`

### 4. Deploy

```bash
npm run deploy
```

---

## Commands

Interactive slash commands for workflow development:

| Command | Description | Use When |
|---------|-------------|----------|
| `/workflow-setup` | Complete wizard for new workflow projects | Starting new project, need full setup |
| `/workflow-create` | Quick scaffolding for workflow classes | Adding workflow to existing project |
| `/workflow-debug` | Interactive debugging with error patterns | Troubleshooting workflow issues |
| `/workflow-test` | Test workflows locally and remotely | Validating workflow behavior |

**Example Usage**:
```
/workflow-setup   # Full guided setup wizard
/workflow-create  # Quick workflow scaffolding
/workflow-debug   # Debug workflow issues
/workflow-test    # Test workflow execution
```

---

## Agents

Autonomous agents for complex workflow tasks:

| Agent | Description | Triggers |
|-------|-------------|----------|
| `workflow-debugger` | Auto-detects and fixes configuration/runtime errors | "debug workflow", "fix workflow errors" |
| `workflow-optimizer` | Analyzes performance, cost, and reliability | "optimize workflow", "improve performance" |
| `workflow-setup-assistant` | Autonomous project scaffolding | "setup workflow", "create first workflow" |

**Key Capabilities**:
- **Debugger**: 6-phase analysis, auto-fix for I/O context, serialization, export issues
- **Optimizer**: Cost analysis, reliability scoring, actionable recommendations
- **Setup Assistant**: Project detection, automatic scaffolding, validation

---

## Scripts

Automation scripts in `scripts/` directory:

| Script | Purpose |
|--------|---------|
| `validate-workflow-config.sh` | Validate wrangler.jsonc configuration |
| `test-workflow.sh` | Create and test workflow instances |
| `benchmark-workflow.sh` | Measure performance and cost |
| `generate-workflow.sh` | Scaffold new workflows from templates |
| `check-workflow-limits.sh` | Validate against Cloudflare limits |

**Usage**:
```bash
./scripts/validate-workflow-config.sh           # Check config
./scripts/test-workflow.sh my-workflow          # Test workflow
./scripts/benchmark-workflow.sh my-workflow 10  # Benchmark 10 runs
./scripts/generate-workflow.sh MyWorkflow       # Generate scaffold
./scripts/check-workflow-limits.sh src/workflows/my-workflow.ts
```

---

## Core Concepts

### WorkflowEntrypoint

Every workflow must extend `WorkflowEntrypoint`:

```typescript
export class MyWorkflow extends WorkflowEntrypoint<Env, Params> {
  async run(event: WorkflowEvent<Params>, step: WorkflowStep) {
    // Workflow logic here
  }
}
```

**Key Points**:
- `Env`: Environment bindings (KV, D1, etc.)
- `Params`: Typed payload passed when creating workflow instance
- `event`: Contains `id`, `payload`, `timestamp`
- `step`: Methods for durable execution

### Step Methods

All workflow work MUST be done in steps for durability:

```typescript
// step.do - Execute work with automatic retries
await step.do('step name', async () => {
  return { result: 'data' };
});

// step.sleep - Wait for duration
await step.sleep('wait', '1 hour');

// step.sleepUntil - Wait until timestamp
await step.sleepUntil('wait until', Date.now() + 3600000);

// step.waitForEvent - Wait for external event
const event = await step.waitForEvent('payment received', 'payment.completed', {
  timeout: '30 minutes'
});
```

**CRITICAL**: All I/O (fetch, KV, D1, R2) must happen **inside** `step.do()` callbacks!

**Reference**: See `references/workflow-patterns.md` for all patterns

---

## Critical Rules

### Always Do ✅

✅ **Perform all I/O inside step.do()** - Required for durability
✅ **Use named steps** - Makes debugging easier
✅ **Return JSON-serializable data from steps** - Required for state persistence
✅ **Use step.sleep() for delays** - Don't use setTimeout()
✅ **Handle errors explicitly** - Use try/catch in step callbacks
✅ **Use NonRetryableError for permanent failures** - Stops retries

**Workflow Patterns**: See `references/workflow-patterns.md` for:
- Sequential workflows
- Parallel execution
- Event-driven workflows
- Scheduled workflows
- Human-in-the-loop workflows

### Never Do ❌

❌ **Never do I/O outside step.do()** - Will fail with "I/O context" error
❌ **Never use setTimeout() or setInterval()** - Use step.sleep() instead
❌ **Never return non-serializable data** - Functions, Promises, etc. will fail
❌ **Never hardcode timeouts** - Use workflow config
❌ **Never ignore NonRetryableError** - Indicates permanent failure

---

## Top 5 Critical Errors

### Error #1: I/O Context Error ⚠️

**Error:**
```
Cannot perform I/O on behalf of a different request
```

**Cause:** Performing I/O outside `step.do()` callback

**Solution:**
```typescript
// ❌ WRONG
const data = await fetch('https://api.example.com');
await step.do('use data', async () => {
  return data; // Error!
});

// ✅ CORRECT
const data = await step.do('fetch data', async () => {
  const response = await fetch('https://api.example.com');
  return await response.json();
});
```

### Error #2: Serialization Error

**Error:**
```
Cannot serialize workflow state
```

**Cause:** Returning non-JSON-serializable data from step

**Solution:**
```typescript
// ❌ WRONG
await step.do('process', async () => {
  return { fn: () => {} }; // Functions not serializable
});

// ✅ CORRECT
await step.do('process', async () => {
  return { result: 'data' }; // JSON-serializable
});
```

### Error #3: NonRetryableError Not Thrown

**Error:** Workflow retries forever on permanent failures

**Solution:**
```typescript
import { NonRetryableError } from 'cloudflare:workers';

await step.do('validate', async () => {
  if (!isValid) {
    throw new NonRetryableError('Invalid input'); // Stop retries
  }
  return { valid: true };
});
```

### Error #4: WorkflowEvent Not Found

**Error:**
```
WorkflowEvent 'payment.completed' not found
```

**Cause:** Event name mismatch between `waitForEvent` and trigger

**Solution:**
```typescript
// Workflow waits for event
const event = await step.waitForEvent('wait payment', 'payment.completed', {
  timeout: '30 minutes'
});

// Trigger event with EXACT same name
await instance.trigger('payment.completed', { amount: 100 });
```

### Error #5: Workflow Execution Failed

**Error:**
```
Workflow execution failed: Step timeout exceeded
```

**Cause:** Step exceeds maximum CPU time (30 seconds)

**Solution:**
```typescript
// ❌ WRONG
await step.do('long task', async () => {
  for (let i = 0; i < 1000000; i++) {
    // Long computation
  }
});

// ✅ CORRECT - Break into smaller steps
for (let i = 0; i < 100; i++) {
  await step.do(`batch ${i}`, async () => {
    // Process batch
  });
}
```

---

**All Issues**: See `references/common-issues.md` for complete documentation

---

## Common Patterns

### Sequential Workflow

Basic workflow with steps executing in order. Each step completes before the next begins.

**Use cases**: Order processing, user onboarding, data pipelines

**Load `templates/basic-workflow.ts` for complete example**

### Scheduled Workflow

Workflow with time delays between steps using `step.sleep()` or `step.sleepUntil()`.

**Use cases**: Reminder sequences, scheduled tasks, delayed notifications

**Load `templates/scheduled-workflow.ts` for complete example**

### Event-Driven Workflow

Wait for external events with `step.waitForEvent()`. Always set timeout and handle with `NonRetryableError`:

```typescript
const payment = await step.waitForEvent('wait payment', 'payment.completed', {
  timeout: '30 minutes'
});
if (!payment) throw new NonRetryableError('Payment timeout');
```

**Load `templates/workflow-with-events.ts` for complete example**

### Workflow with Retries

Use `NonRetryableError` for permanent failures (404), regular `Error` for transient failures (5xx):

```typescript
const data = await step.do('fetch', async () => {
  const response = await fetch(url);
  if (!response.ok) {
    if (response.status === 404) throw new NonRetryableError('Not found');
    throw new Error('Temporary failure'); // Will retry
  }
  return await response.json();
});
```

**Load `templates/workflow-with-retries.ts` for complete example with retry configuration**

---

## Triggering Workflows

**From Worker**: Create instances via `env.MY_WORKFLOW.create()`, get status with `instance.status()`, trigger events with `instance.trigger()`.

**From Cron**: Use `scheduled()` handler to create workflow instances on schedule.

**Load `templates/worker-trigger.ts` for complete Worker trigger example**
**Load `templates/scheduled-workflow.ts` for complete Cron trigger example**

---

## When to Load References

**`references/common-issues.md`**: Encountering I/O context, serialization, NonRetryableError, event naming, or timeout errors; troubleshooting workflow failures.

**`references/workflow-patterns.md`**: Building complex orchestration, approval workflows, idempotency patterns, or circuit breaker patterns.

**`references/wrangler-commands.md`**: Need CLI commands for managing workflow instances, debugging stuck workflows, or monitoring production.

**`references/production-checklist.md`**: Preparing for deployment, need pre-deployment verification, setting up monitoring/error handling.

**`references/limits-quotas.md`**: Hitting instance/step/payload limits, optimizing for cost, designing high-volume workflows.

**`references/2025-features.md`**: Using events system, enhanced retries, instance lifecycle control, or latest Workflows features.

**`references/metrics-analytics.md`**: Setting up monitoring, custom metrics, external logging integration, or workflow dashboards.

**`references/troubleshooting.md`**: Complex debugging scenarios, stuck instances, systematic diagnosis, performance issues.

**`templates/`**: **basic-workflow.ts** (sequential), **scheduled-workflow.ts** (delays/sleep), **workflow-with-events.ts** (waitForEvent), **workflow-with-retries.ts** (custom retry), **worker-trigger.ts** (Worker triggers), **wrangler-workflows-config.jsonc** (Wrangler config), **parallel-execution-workflow.ts** (batched parallel processing), **circuit-breaker-workflow.ts** (resilient external calls)

---

## Wrangler Commands

**Key Commands**: `wrangler workflows create`, `wrangler workflows instances list/describe/terminate`, `wrangler deploy`

**Load `references/wrangler-commands.md` for complete CLI reference with all workflow management commands, monitoring workflows, and debugging stuck instances.**

---

## State Persistence

Workflows automatically persist state between steps. No manual state management needed:

```typescript
export class StatefulWorkflow extends WorkflowEntrypoint {
  async run(event, step) {
    // Step 1 result is automatically persisted
    const result1 = await step.do('step 1', async () => {
      return { data: 'value' };
    });

    // Even if workflow crashes here, step 1 won't re-run
    await step.sleep('wait', '1 hour');

    // Step 2 can use step 1's result (still available after sleep)
    await step.do('step 2', async () => {
      console.log(result1.data); // 'value' - persisted!
    });
  }
}
```

**Key Points**:
- Step results automatically persisted
- Completed steps never re-run (even after crash/restart)
- State available throughout workflow lifetime

---

## Limits

| Resource | Limit |
|----------|-------|
| **Step CPU Time** | 30 seconds |
| **Workflow Duration** | 30 days |
| **Step Payload Size** | 128 KB |
| **Workflow Payload Size** | 128 KB |
| **Steps per Workflow** | 1,000 |
| **Concurrent Instances** | 1,000 per workflow |
| **Event Payload Size** | 128 KB |

**Workarounds**:
- Large data: Store in KV/R2, pass key in step
- Long CPU: Break into smaller steps
- Many steps: Consider sub-workflows

## Pricing

- **Duration**: $0.02 per million GB-s (same as Workers)
- **Requests**: $0.15 per million (workflow creation + step execution)
- **State Storage**: Included (no additional cost)
- **Sleep**: Free (no CPU usage during sleep)

**Example Cost** (1M workflow runs):
- 5 steps each = 5M requests = $0.75
- 10ms per step = 50GB-s = $0.001
- **Total**: ~$0.75 per million workflows

---

## Troubleshooting

### "I/O context" error
**Solution**: Move all I/O into `step.do()` callbacks → See `references/common-issues.md` #1

### "Serialization error"
**Solution**: Return only JSON-serializable data from steps → See `references/common-issues.md` #2

### Workflow retries forever
**Solution**: Throw `NonRetryableError` for permanent failures → See `references/common-issues.md` #3

### "WorkflowEvent not found"
**Solution**: Ensure event names match exactly → See `references/common-issues.md` #4

### "Step timeout exceeded"
**Solution**: Break long computations into smaller steps → See `references/common-issues.md` #5

---

## Production Checklist

**10-Point Pre-Deployment Checklist**: I/O context isolation, JSON serialization, NonRetryableError usage, event name consistency, step duration limits, error handling, retry configuration, timeouts, workflow naming, and monitoring.

**Load `references/production-checklist.md` for complete checklist with detailed explanations, code examples, verification steps, and deployment workflow.**

---

## Official Documentation

**Workflows**: https://developers.cloudflare.com/workflows/ • **API Reference**: https://developers.cloudflare.com/workflows/reference/ • **Examples**: https://developers.cloudflare.com/workflows/examples/ • **Blog**: https://blog.cloudflare.com/cloudflare-workflows/
