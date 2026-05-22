---
name: event-driven-patterns
description: Message queue patterns with BullMQ, Kafka, RabbitMQ - saga, outbox, dead letter queue, exactly-once semantics.
---

# Event-Driven Patterns

Message queue and event bus patterns for decoupled, reliable async processing.

## BullMQ Setup (Producer + Consumer)

```typescript
import { Queue, Worker, QueueEvents } from 'bullmq'
import Redis from 'ioredis'

const connection = new Redis(process.env.REDIS_URL!, { maxRetriesPerRequest: null })

// Producer: define queue
const emailQueue = new Queue('email', { connection })
const marketQueue = new Queue('market-resolution', { connection })

// Add job with options
await emailQueue.add(
  'send-welcome',
  { userId: 'abc', email: 'user@example.com' },
  {
    attempts: 3,
    backoff: { type: 'exponential', delay: 1000 },
    removeOnComplete: { count: 1000 },
    removeOnFail: { count: 5000 }
  }
)

// Delayed job (send after 1 hour)
await emailQueue.add('send-reminder', { userId: 'abc' }, { delay: 3_600_000 })

// Consumer: named processor
const emailWorker = new Worker(
  'email',
  async (job) => {
    if (job.name === 'send-welcome') {
      await sendWelcomeEmail(job.data.email)
    } else if (job.name === 'send-reminder') {
      await sendReminderEmail(job.data.userId)
    }
    // Return value stored in job.returnvalue
    return { sent: true, at: new Date().toISOString() }
  },
  {
    connection,
    concurrency: 10
  }
)

emailWorker.on('completed', (job, result) => {
  console.log(`Job ${job.id} completed:`, result)
})

emailWorker.on('failed', (job, err) => {
  console.error(`Job ${job?.id} failed after ${job?.attemptsMade} attempts:`, err.message)
})
```

## Retry Policies and Dead Letter Queue

```typescript
import { Queue, Worker, QueueEvents } from 'bullmq'

const dlqQueue = new Queue('dead-letter', { connection })

const processingWorker = new Worker(
  'orders',
  async (job) => {
    // Attempt processing
    await processOrder(job.data)
  },
  {
    connection,
    concurrency: 5
  }
)

// Move failed jobs to DLQ after all retries exhausted
processingWorker.on('failed', async (job, err) => {
  if (!job) return
  const isExhausted = job.attemptsMade >= (job.opts.attempts || 1)

  if (isExhausted) {
    await dlqQueue.add('order-failed', {
      originalJob: job.name,
      data: job.data,
      error: err.message,
      failedAt: new Date().toISOString(),
      attempts: job.attemptsMade
    })
    console.error(`Job moved to DLQ: ${job.id}`)
  }
})

// DLQ consumer: alert + manual review
const dlqWorker = new Worker('dead-letter', async (job) => {
  await alertOpsTeam({
    message: `Job failed permanently: ${job.data.originalJob}`,
    data: job.data
  })
}, { connection })
```

## Transactional Outbox Pattern

```typescript
// Problem: write to DB and publish event atomically (no lost messages)
// Solution: write event to outbox table in same transaction, relay worker reads and publishes

// DB schema
// CREATE TABLE outbox (
//   id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
//   aggregate_type TEXT NOT NULL,
//   aggregate_id TEXT NOT NULL,
//   event_type TEXT NOT NULL,
//   payload JSONB NOT NULL,
//   published_at TIMESTAMPTZ,
//   created_at TIMESTAMPTZ DEFAULT now()
// );

async function createMarketWithOutbox(data: CreateMarketDto): Promise<Market> {
  return db.$transaction(async (tx) => {
    // 1. Write domain entity
    const market = await tx.market.create({ data })

    // 2. Write outbox event in SAME transaction
    await tx.outbox.create({
      data: {
        aggregateType: 'Market',
        aggregateId: market.id,
        eventType: 'MarketCreated',
        payload: { marketId: market.id, name: market.name, createdAt: market.createdAt }
      }
    })

    return market
  })
}

// Relay worker: poll outbox and publish (runs separately)
async function outboxRelay(): Promise<void> {
  const unpublished = await db.outbox.findMany({
    where: { publishedAt: null },
    orderBy: { createdAt: 'asc' },
    take: 100
  })

  for (const event of unpublished) {
    try {
      await publishToQueue(event.eventType, event.payload)
      await db.outbox.update({
        where: { id: event.id },
        data: { publishedAt: new Date() }
      })
    } catch (err) {
      console.error(`Outbox relay failed for ${event.id}:`, err)
    }
  }
}

// Poll every second
setInterval(outboxRelay, 1000)
```

## Saga Pattern (Orchestration)

```typescript
// Orchestrator drives the saga steps and handles compensation

interface SagaStep<T> {
  name: string
  execute: (ctx: T) => Promise<Partial<T>>
  compensate: (ctx: T) => Promise<void>
}

class SagaOrchestrator<T extends Record<string, unknown>> {
  constructor(private steps: SagaStep<T>[]) {}

  async run(initialContext: T): Promise<T> {
    const ctx = { ...initialContext }
    const completed: SagaStep<T>[] = []

    for (const step of this.steps) {
      try {
        const result = await step.execute(ctx)
        Object.assign(ctx, result)
        completed.push(step)
        console.log(`Saga step '${step.name}' succeeded`)
      } catch (err) {
        console.error(`Saga step '${step.name}' failed, compensating...`)

        // Compensate in reverse order
        for (const done of completed.reverse()) {
          try {
            await done.compensate(ctx)
            console.log(`Compensated '${done.name}'`)
          } catch (compensateErr) {
            console.error(`Compensation '${done.name}' failed:`, compensateErr)
            // Log to manual intervention queue
          }
        }
        throw err
      }
    }

    return ctx
  }
}

// Order fulfillment saga
interface OrderContext {
  orderId: string
  userId: string
  amount: number
  paymentId?: string
  reservationId?: string
}

const orderSaga = new SagaOrchestrator<OrderContext>([
  {
    name: 'reserve-inventory',
    execute: async (ctx) => {
      const reservationId = await inventory.reserve(ctx.orderId)
      return { reservationId }
    },
    compensate: async (ctx) => {
      if (ctx.reservationId) await inventory.release(ctx.reservationId)
    }
  },
  {
    name: 'charge-payment',
    execute: async (ctx) => {
      const paymentId = await payments.charge(ctx.userId, ctx.amount)
      return { paymentId }
    },
    compensate: async (ctx) => {
      if (ctx.paymentId) await payments.refund(ctx.paymentId)
    }
  },
  {
    name: 'confirm-order',
    execute: async (ctx) => {
      await orders.confirm(ctx.orderId)
      return {}
    },
    compensate: async (ctx) => {
      await orders.cancel(ctx.orderId)
    }
  }
])
```

## Idempotent Consumers (Exactly-Once Semantics)

```typescript
// Even if a message is delivered twice, process it only once
async function processEventIdempotent(
  eventId: string,
  handler: () => Promise<void>
): Promise<void> {
  const key = `processed:${eventId}`

  // SET NX: only set if not exists (atomic)
  const isNew = await redis.set(key, '1', 'EX', 86_400, 'NX')
  if (!isNew) {
    console.log(`Event ${eventId} already processed, skipping`)
    return
  }

  try {
    await handler()
  } catch (err) {
    // Release lock so it can be retried
    await redis.del(key)
    throw err
  }
}

// In BullMQ worker
const worker = new Worker('payments', async (job) => {
  await processEventIdempotent(job.id!, async () => {
    await processPayment(job.data)
  })
}, { connection })
```

## Fan-Out Pattern

```typescript
// One event → multiple consumers in parallel
const eventBus = new Queue('events', { connection })

async function publishMarketResolved(marketId: string, outcome: string): Promise<void> {
  const event = { marketId, outcome, resolvedAt: new Date().toISOString() }

  // Fan-out to multiple downstream queues
  await Promise.all([
    notificationQueue.add('market-resolved', event),
    payoutQueue.add('process-payouts', event),
    analyticsQueue.add('track-resolution', event),
    feedQueue.add('update-feed', event)
  ])
}

// Each queue has its own worker with appropriate concurrency and retry config
```

## Priority Queue

```typescript
// Higher priority number = processed first in BullMQ
await criticalQueue.add('urgent-payout', data, { priority: 1 })   // highest
await normalQueue.add('regular-email', data, { priority: 10 })
await batchQueue.add('report-generation', data, { priority: 100 }) // lowest

// Worker respects priority automatically when picking next job
```

## Queue Monitoring

```typescript
import { QueueEvents } from 'bullmq'

const queueEvents = new QueueEvents('email', { connection })

// Track job lifecycle
queueEvents.on('waiting', ({ jobId }) => metrics.increment('jobs.waiting'))
queueEvents.on('active', ({ jobId }) => metrics.increment('jobs.active'))
queueEvents.on('completed', ({ jobId }) => metrics.increment('jobs.completed'))
queueEvents.on('failed', ({ jobId, failedReason }) => {
  metrics.increment('jobs.failed')
  console.error(`Job ${jobId} failed: ${failedReason}`)
})
queueEvents.on('stalled', ({ jobId }) => {
  metrics.increment('jobs.stalled')
  console.warn(`Job ${jobId} stalled — worker may have crashed`)
})

// Health check: alert if queue depth grows too large
async function checkQueueHealth(queue: Queue): Promise<void> {
  const counts = await queue.getJobCounts('waiting', 'active', 'failed', 'delayed')

  if (counts.waiting > 1000) {
    await alertOpsTeam({ queue: queue.name, backlog: counts.waiting })
  }
  if (counts.failed > 100) {
    await alertOpsTeam({ queue: queue.name, failures: counts.failed })
  }
}

setInterval(() => checkQueueHealth(emailQueue), 30_000)
```

**Remember**: Use the outbox pattern whenever a DB write and an event publish must be atomic. Never publish directly inside a transaction — the broker call can fail after the DB commits, causing lost events.
