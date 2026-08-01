---
name: api-queue-bullmq
description: Job queues, background processing, and task scheduling with BullMQ v5
---

# BullMQ Patterns

> **Quick Guide:** Use BullMQ (v5.x) for background job processing, task scheduling, and workflow orchestration on top of Redis. Core classes: `Queue` (adds jobs), `Worker` (processes jobs), `QueueEvents` (global event listener), `FlowProducer` (parent-child job trees). Always pass a `connection` object to every constructor (required in v5). Set `maxRetriesPerRequest: null` on ioredis connections for Workers. Use `upsertJobScheduler` for repeatable/cron jobs (replaces deprecated repeatable API). QueueScheduler was removed in v4 -- its responsibilities are now handled by Workers automatically.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST pass a `connection` object to every Queue, Worker, QueueEvents, and FlowProducer constructor -- BullMQ v5 throws if connection is missing)**

**(You MUST set `maxRetriesPerRequest: null` on ioredis connections used by Workers -- BullMQ requires infinite retries and throws without this setting)**

**(You MUST call `await worker.close()` on SIGTERM/SIGINT for graceful shutdown -- without it, in-progress jobs become stalled)**

**(You MUST use `upsertJobScheduler` for repeatable/cron jobs -- the old `repeat` option on `queue.add` is deprecated since v5.16.0)**

</critical_requirements>

---

## Examples

- [Core Patterns](examples/core.md) -- Queue setup, Worker processing, job options, connection factory, graceful shutdown, typed jobs
- [Advanced Patterns](examples/advanced.md) -- FlowProducer, rate limiting, job scheduling, QueueEvents, concurrency, sandboxed processors

**Additional resources:**

- [reference.md](reference.md) -- Decision frameworks, job option reference, anti-patterns, production checklist

---

**Auto-detection:** BullMQ, bullmq, Queue, Worker, QueueEvents, FlowProducer, job queue, background job, worker process, job scheduler, upsertJobScheduler, rate limiter, job priority, job delay, sandboxed processor, repeatable job, cron job, flow producer, parent child jobs

**When to use:**

- Background processing (email sending, image processing, PDF generation)
- Scheduled/cron jobs (nightly reports, periodic cleanup)
- Workflow orchestration with parent-child job dependencies (FlowProducer)
- Rate-limited API consumption (throttling outbound requests)
- Priority-based job processing (urgent jobs before bulk operations)
- Distributing CPU-intensive work across multiple workers or machines

**Key patterns covered:**

- Queue and Worker setup with typed job data and return values
- Connection factory with `maxRetriesPerRequest: null` for Workers
- Job options: delay, priority, attempts, backoff, removeOnComplete/Fail
- Graceful shutdown with `worker.close()` on process signals
- FlowProducer for parent-child job trees with dependency tracking
- Job Schedulers for repeatable/cron jobs (`upsertJobScheduler`)
- Rate limiting (global limiter and manual `Worker.RateLimitError`)
- Concurrency control (local per-worker and global)
- QueueEvents for global event monitoring across all workers
- Sandboxed processors for CPU-intensive work

**When NOT to use:**

- Simple in-process timers or `setTimeout` (no persistence needed)
- Real-time pub/sub messaging without persistence (use your pub/sub solution)
- Data that must be processed synchronously within a request-response cycle
- Queues that don't need persistence, retries, or scheduling

---

<philosophy>

## Philosophy

BullMQ is a **Redis-backed job queue** for Node.js that provides reliable background processing with at-least-once delivery guarantees. The core principle: **separate job production from job consumption** so your application stays responsive while work happens asynchronously.

**Core principles:**

1. **Producers and consumers are decoupled** -- Any process can add jobs to a queue; any Worker can process them. This enables horizontal scaling by adding more Workers.
2. **Jobs are persistent** -- Jobs survive process restarts because they live in Redis. A crashed Worker's jobs are picked up by other Workers (or the same Worker after restart).
3. **At-least-once delivery** -- BullMQ guarantees every job is processed at least once. Use idempotent processors to handle the (rare) case of duplicate processing after a stall.
4. **Fail gracefully with retries** -- Configure `attempts` and `backoff` strategies so transient failures resolve automatically. Permanently failed jobs move to the failed set for inspection.
5. **Each Queue/Worker/QueueEvents needs its own connection** -- BullMQ manages connection state internally. Never share a single ioredis instance across multiple BullMQ classes (except Queues acting only as producers).

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Connection Factory

BullMQ v5 requires an explicit Redis connection on every constructor. Workers need `maxRetriesPerRequest: null` so ioredis retries indefinitely instead of giving up.

```typescript
import Redis from "ioredis";

function createBullMQConnection(): Redis {
  const url = process.env.REDIS_URL;
  if (!url) throw new Error("REDIS_URL is required");
  return new Redis(url, { maxRetriesPerRequest: null });
}
export { createBullMQConnection };
```

**Why good:** `maxRetriesPerRequest: null` satisfies BullMQ's requirement, factory ensures consistent config, environment variable keeps credentials out of code

```typescript
// Bad -- missing maxRetriesPerRequest
const redis = new Redis("redis://localhost:6379");
const worker = new Worker("emails", processor, { connection: redis });
// BullMQ throws: "maxRetriesPerRequest must be null"
```

**Why bad:** BullMQ requires infinite retries on Worker connections and will throw at startup without `null`

See [examples/core.md](examples/core.md) for the full connection factory with producer vs consumer separation.

---

### Pattern 2: Queue and Worker Setup

Queue adds jobs; Worker processes them. Both accept TypeScript generics for type-safe job data and return values.

```typescript
import { Queue, Worker, type Job } from "bullmq";

interface EmailJobData {
  to: string;
  subject: string;
  body: string;
}

const QUEUE_NAME = "emails";

const emailQueue = new Queue<EmailJobData>(QUEUE_NAME, {
  connection: createBullMQConnection(),
});

const emailWorker = new Worker<EmailJobData>(
  QUEUE_NAME,
  async (job: Job<EmailJobData>) => {
    await sendEmail(job.data.to, job.data.subject, job.data.body);
  },
  { connection: createBullMQConnection() },
);
```

**Why good:** Generics enforce type safety on `job.data`, separate connections for Queue and Worker, named constant for queue name

See [examples/core.md](examples/core.md) for full setup with events, error handling, and typed return values.

---

### Pattern 3: Job Options

Control job behavior with options: delay, priority, retries, backoff, and auto-removal.

```typescript
const MAX_ATTEMPTS = 5;
const BACKOFF_DELAY_MS = 1000;
const DELAY_MS = 60_000;
const KEEP_COMPLETED_COUNT = 100;

await emailQueue.add(
  "send-welcome",
  { to: "user@example.com", subject: "Welcome", body: "..." },
  {
    delay: DELAY_MS,
    priority: 1, // 1 = highest, higher numbers = lower priority
    attempts: MAX_ATTEMPTS,
    backoff: { type: "exponential", delay: BACKOFF_DELAY_MS },
    removeOnComplete: { count: KEEP_COMPLETED_COUNT },
    removeOnFail: false,
  },
);
```

**Why good:** Named constants for all numeric values, exponential backoff for transient failures, `removeOnComplete` with count prevents unbounded Redis memory, `removeOnFail: false` preserves failed jobs for debugging

See [examples/core.md](examples/core.md) for `defaultJobOptions`, `addBulk`, and LIFO patterns.

---

### Pattern 4: Graceful Shutdown

Call `worker.close()` on process signals to finish in-progress jobs before exiting. Without this, jobs become stalled and are re-processed by other Workers.

```typescript
async function shutdown(workers: Worker[]): Promise<void> {
  await Promise.all(workers.map((w) => w.close()));
  process.exit(0);
}

process.on("SIGTERM", () => shutdown([emailWorker]));
process.on("SIGINT", () => shutdown([emailWorker]));
```

**Why good:** `close()` stops accepting new jobs and waits for in-progress jobs to finish, `Promise.all` handles multiple workers, signal handlers cover both SIGTERM and SIGINT

**Gotcha:** `worker.close()` has no built-in timeout. If a processor hangs, the shutdown hangs. Wrap with your own timeout if needed.

See [examples/core.md](examples/core.md) for shutdown with timeout pattern.

---

### Pattern 5: FlowProducer (Parent-Child Jobs)

FlowProducer creates job trees where parent jobs wait for all children to complete. The entire tree is added atomically.

```typescript
import { FlowProducer } from "bullmq";

const flowProducer = new FlowProducer({ connection: createBullMQConnection() });

await flowProducer.add({
  name: "publish-video",
  queueName: "videos",
  children: [
    { name: "extract-audio", queueName: "media", data: { videoId: "abc" } },
    {
      name: "generate-thumbnail",
      queueName: "media",
      data: { videoId: "abc" },
    },
    {
      name: "transcode",
      queueName: "media",
      data: { videoId: "abc", format: "mp4" },
    },
  ],
});
```

**Why good:** Parent waits until all children complete, atomic addition (all or nothing), children can be in different queues, parent processor can access children results via `job.getChildrenValues()`

See [examples/advanced.md](examples/advanced.md) for accessing children values and nested flows.

---

### Pattern 6: Job Schedulers (Repeatable/Cron Jobs)

Use `upsertJobScheduler` (v5.16.0+) for repeatable jobs. Replaces the deprecated `repeat` option.

```typescript
const REPORT_INTERVAL_MS = 3_600_000; // 1 hour

// Fixed interval
await emailQueue.upsertJobScheduler(
  "hourly-digest",
  { every: REPORT_INTERVAL_MS },
  {
    name: "send-digest",
    data: { type: "hourly" },
  },
);

// Cron expression -- daily at 3:15 AM
await emailQueue.upsertJobScheduler(
  "nightly-cleanup",
  { pattern: "0 15 3 * * *" },
  {
    name: "cleanup",
    data: { type: "nightly" },
    opts: { removeOnComplete: true },
  },
);
```

**Why good:** `upsertJobScheduler` is idempotent (safe to call on every startup), template defines job name/data/opts inherited by each produced job, cron syntax via `pattern`

**Gotcha:** `every` intervals align to the clock, not to when you called `upsertJobScheduler`. A 2000ms interval fires at 0s, 2s, 4s, etc.

See [examples/advanced.md](examples/advanced.md) for removing schedulers and listing active schedulers.

---

### Pattern 7: Rate Limiting

Limit how many jobs a Worker processes per time window. The limiter is global across all Workers on the same queue.

```typescript
const RATE_LIMIT_MAX = 10;
const RATE_LIMIT_DURATION_MS = 1000;

const worker = new Worker("api-calls", processor, {
  connection: createBullMQConnection(),
  limiter: { max: RATE_LIMIT_MAX, duration: RATE_LIMIT_DURATION_MS },
});
```

**Why good:** Global rate limit (10 workers with this config still process max 10 jobs/second total), named constants for limits

For dynamic rate limiting based on external API responses, use `worker.rateLimit(duration)` + `throw Worker.RateLimitError()`. See [examples/advanced.md](examples/advanced.md).

---

### Pattern 8: QueueEvents for Global Monitoring

QueueEvents uses Redis Streams (not Pub/Sub) so events are reliable even across reconnections. Requires its own dedicated connection.

```typescript
import { QueueEvents } from "bullmq";

const queueEvents = new QueueEvents(QUEUE_NAME, {
  connection: createBullMQConnection(),
});

queueEvents.on("completed", ({ jobId, returnvalue }) => {
  console.log(`Job ${jobId} completed with: ${returnvalue}`);
});

queueEvents.on("failed", ({ jobId, failedReason }) => {
  console.error(`Job ${jobId} failed: ${failedReason}`);
});
```

**Why good:** Monitors all Workers on a queue from a single listener, reliable delivery via Redis Streams, separate connection as required

See [examples/advanced.md](examples/advanced.md) for progress tracking and waiting for specific job completion.

</patterns>

---

<performance>

## Performance Optimization

- **Concurrency** -- Set `concurrency` on Worker options to process multiple jobs in parallel within a single Worker instance: `{ concurrency: 10 }`. Only effective for I/O-bound work. CPU-bound work blocks the event loop and causes stalled jobs -- use sandboxed processors instead.
- **Sandboxed processors** -- Pass a file path instead of a function to the Worker constructor to run processors in a separate process (or worker thread with `useWorkerThreads: true`). Prevents CPU-intensive work from blocking lock renewal.
- **addBulk** -- Use `queue.addBulk([...])` to add many jobs in a single Redis round-trip instead of calling `queue.add()` in a loop.
- **removeOnComplete/Fail** -- Configure auto-removal to prevent unbounded Redis memory growth. Use `{ count: N }` to keep the last N jobs for debugging.
- **Separate connections** -- Producers (Queue) can share a connection. Workers and QueueEvents each need their own connection due to blocking Redis commands.

</performance>

---

<decision_framework>

## Decision Framework

### When to Use BullMQ

```
Do you need background job processing?
|-- NO -> Don't use BullMQ
+-- YES -> Do you need persistence, retries, or scheduling?
    |-- NO -> Simple in-process queue or setTimeout may suffice
    +-- YES -> Do you need parent-child job dependencies?
        |-- YES -> BullMQ with FlowProducer
        +-- NO -> Do you need rate limiting or priority?
            |-- YES -> BullMQ with limiter/priority options
            +-- NO -> BullMQ with basic Queue + Worker
```

### Which Job Pattern?

```
What kind of job scheduling do you need?
|-- One-time delayed job -> queue.add() with delay option
|-- Recurring on fixed interval -> upsertJobScheduler with every
|-- Recurring on cron schedule -> upsertJobScheduler with pattern
|-- Job that depends on other jobs -> FlowProducer with children
|-- Bulk of independent jobs -> queue.addBulk([...])
```

### Concurrency Strategy

```
Is the processor CPU-intensive?
|-- YES -> Use sandboxed processor (file path or useWorkerThreads)
+-- NO -> Is it I/O-bound (network calls, DB queries)?
    |-- YES -> Set concurrency option (e.g., 10-50)
    +-- NO -> Default concurrency (1) is fine
```

</decision_framework>

---

<red_flags>

## RED FLAGS

**High Priority Issues:**

- Missing `connection` on Queue/Worker/QueueEvents constructor -- BullMQ v5 throws at startup without it
- Missing `maxRetriesPerRequest: null` on Worker connections -- BullMQ throws immediately
- No graceful shutdown handler -- in-progress jobs become stalled on process exit and are re-processed by other Workers
- Using deprecated `repeat` option on `queue.add()` instead of `upsertJobScheduler` -- deprecated since v5.16.0
- Using integer job IDs -- BullMQ v5 throws; IDs must be strings

**Medium Priority Issues:**

- No `removeOnComplete`/`removeOnFail` configured -- completed/failed jobs accumulate in Redis indefinitely
- Sharing a single ioredis connection between Worker and QueueEvents -- both use blocking commands and will interfere
- CPU-intensive processor without sandboxed mode -- blocks event loop, causes stalled jobs, prevents lock renewal
- Missing error event handler on Worker -- `worker.on("error", ...)` prevents unhandled errors from crashing the process

**Common Mistakes:**

- Assuming `worker.close()` has a timeout -- it waits indefinitely for processors to finish; wrap with your own timeout
- Using QueueScheduler class -- removed in BullMQ v4; its responsibilities are handled by Workers automatically
- Expecting `limiter` to be per-Worker -- the rate limit is global across all Workers on the same queue
- Not making processors idempotent -- BullMQ guarantees at-least-once delivery; a stalled job may be processed twice

**Gotchas & Edge Cases:**

- `upsertJobScheduler` `every` intervals align to the clock (0s, 2s, 4s), not to when you called the method
- `worker.close()` does not cancel running processors -- it waits for them to finish naturally
- Job priority has a performance cost -- BullMQ uses a different data structure for priority queues; skip if not needed
- `QueueEvents` uses Redis Streams internally -- ensure your Redis instance has sufficient memory for stream data
- FlowProducer adds the entire tree atomically -- if any child fails validation, none are added
- `job.getChildrenValues()` returns an object keyed by `"queueName:jobId"` -- not an array
- Redis must have `maxmemory-policy` set to `noeviction` -- BullMQ relies on keys not being evicted

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST pass a `connection` object to every Queue, Worker, QueueEvents, and FlowProducer constructor -- BullMQ v5 throws if connection is missing)**

**(You MUST set `maxRetriesPerRequest: null` on ioredis connections used by Workers -- BullMQ requires infinite retries and throws without this setting)**

**(You MUST call `await worker.close()` on SIGTERM/SIGINT for graceful shutdown -- without it, in-progress jobs become stalled)**

**(You MUST use `upsertJobScheduler` for repeatable/cron jobs -- the old `repeat` option on `queue.add` is deprecated since v5.16.0)**

**Failure to follow these rules will cause startup crashes, stalled jobs, and unreliable job processing.**

</critical_reminders>
