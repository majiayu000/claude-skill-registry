---
name: background-job-orchestrator
description: Expert in background job processing with Bull/BullMQ (Redis), Celery, and cloud queues. Implements retries, scheduling, priority queues, and worker management. Use for async task processing, email campaigns, report generation, batch operations. Activate on "background job", "async task", "queue", "worker", "BullMQ", "Celery". NOT for real-time WebSocket communication, synchronous API calls, or simple setTimeout operations.
allowed-tools: Read,Write,Edit,Bash(npm:*,pip:*)
---

# Background Job Orchestrator

Expert in designing and implementing production-grade background job systems that handle long-running tasks without blocking API responses.

## When to Use

✅ **Use for**:
- Long-running tasks (email sends, report generation, image processing)
- Batch operations (bulk imports, exports, data migrations)
- Scheduled tasks (daily digests, cleanup jobs, recurring reports)
- Tasks requiring retry logic (external API calls, flaky operations)
- Priority-based processing (premium users first, critical alerts)
- Rate-limited operations (API quotas, third-party service limits)

❌ **NOT for**:
- Real-time bidirectional communication (use WebSockets)
- Sub-second latency requirements (use in-memory caching)
- Simple delays (setTimeout is fine for &lt;5 seconds)
- Synchronous API responses (keep logic in request handler)

## Quick Decision Tree

```
Does this task:
├── Take &gt;5 seconds? → Background job
├── Need to retry on failure? → Background job
├── Run on a schedule? → Background job (cron pattern)
├── Block user interaction? → Background job
├── Process in batches? → Background job
└── Return immediately? → Keep synchronous
```

---

## Technology Selection

### Node.js: BullMQ (Recommended 2024+)

**When to use**:
- TypeScript project
- Redis already in stack
- Need advanced features (rate limiting, priorities, repeatable jobs)

**Why BullMQ over Bull**:
- Bull (v3) → BullMQ (v4+): Complete rewrite in TypeScript
- Better Redis connection handling
- Improved concurrency and performance
- Active maintenance (Bull is in maintenance mode)

### Python: Celery

**When to use**:
- Python/Django project
- Need distributed task execution
- Complex workflows (chains, groups, chords)

**Alternatives**:
- **RQ** (Redis Queue): Simpler, fewer features
- **Dramatiq**: Modern, less ecosystem
- **Huey**: Lightweight, good for small projects

### Cloud-Native: AWS SQS, Google Cloud Tasks

**When to use**:
- Serverless architecture
- Don't want to manage Redis/RabbitMQ
- Need guaranteed delivery and dead-letter queues

---

## Common Anti-Patterns

### Anti-Pattern 1: No Dead Letter Queue

**Novice thinking**: "Retry 3 times, then fail silently"

**Problem**: Failed jobs disappear with no visibility or recovery path.

**Correct approach**:
```typescript
// BullMQ with dead letter queue
const queue = new Queue('email-queue', {
  connection: redis,
  defaultJobOptions: {
    attempts: 3,
    backoff: {
      type: 'exponential',
      delay: 2000
    },
    removeOnComplete: 100, // Keep last 100 successful
    removeOnFail: false     // Keep all failed for inspection
  }
});

// Monitor failed jobs
const failedJobs = await queue.getFailed();
```

**Timeline**:
- Pre-2020: Retry and forget
- 2020+: Dead letter queues standard
- 2024+: Observability for job failures required

---

### Anti-Pattern 2: Synchronous Job Processing

**Symptom**: API endpoint waits for job completion

**Problem**:
```typescript
// ❌ WRONG - Blocks API response
app.post('/send-email', async (req, res) => {
  await sendEmail(req.body.to, req.body.subject);
  res.json({ success: true });
});
```

**Why wrong**: Timeout, poor UX, wastes server resources

**Correct approach**:
```typescript
// ✅ RIGHT - Queue and return immediately
app.post('/send-email', async (req, res) => {
  const job = await emailQueue.add('send', {
    to: req.body.to,
    subject: req.body.subject
  });

  res.json({
    success: true,
    jobId: job.id,
    status: 'queued'
  });
});

// Separate worker processes the job
worker.process('send', async (job) => {
  await sendEmail(job.data.to, job.data.subject);
});
```

---

### Anti-Pattern 3: No Idempotency

**Problem**: Job runs twice → duplicate charges, double emails

**Why it happens**:
- Redis connection drops mid-processing
- Worker crashes before job completion
- Job timeout triggers retry while still running

**Correct approach**:
```typescript
// ✅ Idempotent job with deduplication key
await queue.add('charge-payment', {
  userId: 123,
  amount: 50.00
}, {
  jobId: `payment-${orderId}`, // Prevents duplicates
  attempts: 3
});

// In worker: Check if already processed
worker.process('charge-payment', async (job) => {
  const { userId, amount } = job.data;

  // Check idempotency
  const existing = await db.payments.findOne({
    jobId: job.id
  });
  if (existing) {
    return existing; // Already processed
  }

  // Process payment
  const result = await stripe.charges.create({...});

  // Store idempotency record
  await db.payments.create({
    jobId: job.id,
    result
  });

  return result;
});
```

---

### Anti-Pattern 4: No Rate Limiting

**Problem**: Overwhelm third-party APIs or exhaust quotas

**Symptom**: "Rate limit exceeded" errors from Sendgrid, Stripe, etc.

**Correct approach**:
```typescript
// BullMQ rate limiting
const queue = new Queue('api-calls', {
  limiter: {
    max: 100,        // Max 100 jobs
    duration: 60000  // Per 60 seconds
  }
});

// Or: Priority-based rate limits
await queue.add('send-email', data, {
  priority: user.isPremium ? 1 : 10,
  rateLimiter: {
    max: user.isPremium ? 1000 : 100,
    duration: 3600000 // Per hour
  }
});
```

---

### Anti-Pattern 5: Forgetting Worker Scaling

**Problem**: Single worker can't keep up with queue depth

**Symptom**: Queue backs up, jobs delayed hours/days

**Correct approach**:
```typescript
// Horizontal scaling with multiple workers
const worker = new Worker('email-queue', async (job) => {
  await processEmail(job.data);
}, {
  connection: redis,
  concurrency: 5  // Process 5 jobs concurrently per worker
});

// Run multiple worker processes (PM2, Kubernetes, etc.)
// Each worker processes concurrency * num_workers jobs
```

**Monitoring**:
```typescript
// Set up alerts for queue depth
setInterval(async () => {
  const waiting = await queue.getWaitingCount();
  if (waiting > 1000) {
    alert('Queue depth exceeds 1000, scale workers!');
  }
}, 60000);
```

---

## Implementation Patterns

### Pattern 1: Email Campaigns

```typescript
// Queue setup
const emailQueue = new Queue('email-campaign', { connection: redis });

// Enqueue batch
async function sendCampaign(userIds: number[], template: string) {
  const jobs = userIds.map(userId => ({
    name: 'send',
    data: { userId, template },
    opts: {
      attempts: 3,
      backoff: { type: 'exponential', delay: 5000 }
    }
  }));

  await emailQueue.addBulk(jobs);
}

// Worker with retry logic
const worker = new Worker('email-campaign', async (job) => {
  const { userId, template } = job.data;

  const user = await db.users.findById(userId);
  const email = renderTemplate(template, user);

  try {
    await sendgrid.send({
      to: user.email,
      subject: email.subject,
      html: email.body
    });
  } catch (error) {
    if (error.code === 'ECONNREFUSED') {
      throw error; // Retry
    }
    // Invalid email, don't retry
    console.error(`Invalid email for user ${userId}`);
  }
}, {
  connection: redis,
  concurrency: 10
});
```

### Pattern 2: Scheduled Reports

```typescript
// Daily report at 9 AM
await queue.add('daily-report', {
  type: 'sales',
  recipients: ['admin@company.com']
}, {
  repeat: {
    pattern: '0 9 * * *', // Cron syntax
    tz: 'America/New_York'
  }
});

// Worker generates and emails report
worker.process('daily-report', async (job) => {
  const { type, recipients } = job.data;

  const data = await generateReport(type);
  const pdf = await createPDF(data);

  await emailQueue.add('send', {
    to: recipients,
    subject: `Daily ${type} Report`,
    attachments: [{ filename: 'report.pdf', content: pdf }]
  });
});
```

### Pattern 3: Video Transcoding Pipeline

```typescript
// Multi-stage job with progress tracking
await videoQueue.add('transcode', {
  videoId: 123,
  formats: ['720p', '1080p', '4k']
}, {
  attempts: 2,
  timeout: 3600000 // 1 hour timeout
});

worker.process('transcode', async (job) => {
  const { videoId, formats } = job.data;

  for (let i = 0; i < formats.length; i++) {
    const format = formats[i];

    // Update progress
    await job.updateProgress((i / formats.length) * 100);

    // Transcode
    await ffmpeg.transcode(videoId, format);
  }

  await job.updateProgress(100);
});

// Client polls for progress
app.get('/videos/:id/status', async (req, res) => {
  const job = await queue.getJob(req.params.jobId);
  res.json({
    state: await job.getState(),
    progress: job.progress
  });
});
```

---

## Monitoring & Observability

### Essential Metrics

```typescript
// Queue health dashboard
async function getQueueMetrics() {
  const [waiting, active, completed, failed, delayed] = await Promise.all([
    queue.getWaitingCount(),
    queue.getActiveCount(),
    queue.getCompletedCount(),
    queue.getFailedCount(),
    queue.getDelayedCount()
  ]);

  return {
    waiting,    // Jobs waiting to be processed
    active,     // Jobs currently processing
    completed,  // Successfully completed
    failed,     // Failed after retries
    delayed,    // Scheduled for future
    health: waiting < 1000 && failed < 100 ? 'healthy' : 'degraded'
  };
}
```

### BullMQ Board (UI)

```typescript
// Development: Monitor jobs visually
import { createBullBoard } from '@bull-board/api';
import { BullMQAdapter } from '@bull-board/api/bullMQAdapter';
import { ExpressAdapter } from '@bull-board/express';

const serverAdapter = new ExpressAdapter();

createBullBoard({
  queues: [
    new BullMQAdapter(emailQueue),
    new BullMQAdapter(videoQueue)
  ],
  serverAdapter
});

app.use('/admin/queues', serverAdapter.getRouter());
// Visit http://localhost:3000/admin/queues
```

---

## Production Checklist

```
□ Dead letter queue configured
□ Retry strategy with exponential backoff
□ Job timeout limits set
□ Rate limiting for third-party APIs
□ Idempotency keys for critical operations
□ Worker concurrency tuned (CPU cores * 2)
□ Horizontal scaling configured (multiple workers)
□ Queue depth monitoring with alerts
□ Failed job inspection workflow
□ Job data doesn't contain PII in logs
□ Redis persistence enabled (AOF or RDB)
□ Graceful shutdown handling (SIGTERM)
```

---

## When to Use vs Avoid

| Scenario | Use Background Jobs? |
|----------|---------------------|
| Send welcome email on signup | ✅ Yes - can take 2-5 seconds |
| Charge credit card | ⚠️ Maybe - depends on payment provider latency |
| Generate PDF report (30 seconds) | ✅ Yes - definitely background |
| Fetch user profile from DB | ❌ No - milliseconds, keep synchronous |
| Process video upload (5 minutes) | ✅ Yes - always background |
| Validate form input | ❌ No - synchronous validation |
| Daily cron job | ✅ Yes - use repeatable jobs |
| Real-time chat message | ❌ No - use WebSockets |

---

## Technology Comparison

| Feature | BullMQ | Celery | AWS SQS |
|---------|--------|--------|---------|
| Language | Node.js | Python | Any (HTTP API) |
| Backend | Redis | Redis/RabbitMQ/SQS | Managed |
| Priorities | ✅ | ✅ | ✅ |
| Rate Limiting | ✅ | ❌ | ✅ (via attributes) |
| Repeat/Cron | ✅ | ✅ (celery-beat) | ❌ (use EventBridge) |
| UI Dashboard | Bull Board | Flower | CloudWatch |
| Workflows | ❌ | ✅ (chains, groups) | ❌ |
| Learning Curve | Medium | Medium | Low |
| Cost | Redis hosting | Redis hosting | $0.40/million requests |

---

## References

- `/references/bullmq-patterns.md` - Advanced BullMQ patterns and examples
- `/references/celery-workflows.md` - Celery chains, groups, and chords
- `/references/job-observability.md` - Monitoring, alerting, and debugging

## Scripts

- `scripts/setup_bullmq.sh` - Initialize BullMQ with Redis
- `scripts/queue_health_check.ts` - Queue metrics dashboard
- `scripts/retry_failed_jobs.ts` - Bulk retry failed jobs

---

**This skill guides**: Background job implementation | Queue architecture | Retry strategies | Worker scaling | Job observability
