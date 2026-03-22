---
name: bull-mq
description: >-
  You are an expert in BullMQ, the high-performance job queue for Node.js
  built on Redis. You help developers build reliable background processing
  systems with delayed jobs, rate limiting, prioritization, repeatable cron
  jobs, job dependencies, concurrency control, and dead-letter handling —
  powering email sending, image processing, webhook delivery, report
  generation, and any async workload.
license: Apache-2.0
compatibility: ''
metadata:
  author: terminal-skills
  version: 1.0.0
  category: Backend Development
  tags:
    - queue
    - redis
    - jobs
    - background
    - worker
    - cron
    - node
---

# BullMQ — Redis-Based Job Queue for Node.js

You are an expert in BullMQ, the high-performance job queue for Node.js built on Redis. You help developers build reliable background processing systems with delayed jobs, rate limiting, prioritization, repeatable cron jobs, job dependencies, concurrency control, and dead-letter handling — powering email sending, image processing, webhook delivery, report generation, and any async workload.

## Core Capabilities

### Queue and Worker

```typescript
import { Queue, Worker, QueueScheduler, FlowProducer } from "bullmq";
import IORedis from "ioredis";

const connection = new IORedis({ host: "localhost", port: 6379, maxRetriesPerRequest: null });

// Define queue
const emailQueue = new Queue("email", { connection });

// Add jobs
await emailQueue.add("welcome", {
  to: "user@example.com",
  template: "welcome",
  data: { name: "Alice" },
}, {
  priority: 1,                            // Lower = higher priority
  attempts: 3,                            // Retry up to 3 times
  backoff: { type: "exponential", delay: 2000 },
  removeOnComplete: { count: 1000 },      // Keep last 1000 completed
  removeOnFail: { age: 7 * 24 * 3600 },   // Keep failed for 7 days
});

// Delayed job
await emailQueue.add("reminder", { userId: 42 }, {
  delay: 24 * 60 * 60 * 1000,            // 24 hours from now
});

// Repeatable (cron)
await emailQueue.add("digest", {}, {
  repeat: { pattern: "0 9 * * 1" },       // Every Monday at 9 AM
});

// Worker
const worker = new Worker("email", async (job) => {
  switch (job.name) {
    case "welcome":
      await sendEmail(job.data.to, job.data.template, job.data.data);
      break;
    case "reminder":
      await sendReminderEmail(job.data.userId);
      break;
    case "digest":
      await sendWeeklyDigest();
      break;
  }

  // Progress reporting
  await job.updateProgress(100);
  return { sent: true, timestamp: Date.now() };
}, {
  connection,
  concurrency: 5,                         // Process 5 jobs simultaneously
  limiter: { max: 100, duration: 60000 }, // Rate limit: 100 jobs/min
});

worker.on("completed", (job, result) => console.log(`Job ${job.id} completed`));
worker.on("failed", (job, err) => console.error(`Job ${job?.id} failed: ${err.message}`));
```

### Job Flows (Parent-Child Dependencies)

```typescript
const flow = new FlowProducer({ connection });

await flow.add({
  name: "generate-report",
  queueName: "reports",
  data: { reportId: "monthly-2026-03" },
  children: [
    { name: "fetch-sales", queueName: "data", data: { source: "sales" } },
    { name: "fetch-users", queueName: "data", data: { source: "users" } },
    { name: "fetch-metrics", queueName: "data", data: { source: "metrics" } },
  ],
  // Parent job runs only after ALL children complete
});
```

## Installation

```bash
npm install bullmq ioredis
```

## Best Practices

1. **Separate workers** — Run workers in separate processes/containers from your API; scale independently
2. **Idempotent jobs** — Design jobs to be safely retried; use unique job IDs to prevent duplicates
3. **Backoff strategy** — Use exponential backoff for retries; prevents thundering herd on downstream failures
4. **Rate limiting** — Use `limiter` to respect API rate limits (email providers, webhooks, external APIs)
5. **Progress tracking** — Use `job.updateProgress()` for long-running jobs; clients can poll progress
6. **Graceful shutdown** — Call `worker.close()` on SIGTERM; finishes current jobs before exiting
7. **Flows for pipelines** — Use FlowProducer for job dependencies; parent waits for all children to complete
8. **Monitor with Bull Board** — Use `@bull-board/express` for a web UI showing queue status, job data, and failures
