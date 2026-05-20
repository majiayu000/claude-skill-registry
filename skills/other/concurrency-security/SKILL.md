---
name: concurrency-security
description: TOCTOU prevention, distributed locking, idempotency keys, race condition detection for Node.js and serverless environments.
---

# Concurrency Security

Patterns for preventing race conditions, double-execution, and state corruption in concurrent systems.

## TOCTOU Prevention

Time-of-Check to Time-of-Use: the gap between reading state and acting on it.

```typescript
// WRONG: check then act - another process can change state between lines
const balance = await db.accounts.findUnique({ where: { id } })
if (balance.amount >= amount) {
  await db.accounts.update({ where: { id }, data: { amount: balance.amount - amount } })
}

// CORRECT: atomic check-and-update in a single statement
const updated = await db.$executeRaw`
  UPDATE accounts
  SET amount = amount - ${amount}
  WHERE id = ${id} AND amount >= ${amount}
  RETURNING *
`
if (updated.count === 0) throw new Error('Insufficient funds or concurrent update')
```

```typescript
// File system TOCTOU (Node.js)
// WRONG
if (fs.existsSync(filePath)) {
  fs.writeFileSync(filePath, data)  // another process may have deleted it
}

// CORRECT: use O_EXCL flag for exclusive creation
import { open } from 'fs/promises'
try {
  const fh = await open(filePath, 'wx')  // fail if file exists
  await fh.writeFile(data)
  await fh.close()
} catch (err: any) {
  if (err.code === 'EEXIST') { /* already exists, handle */ }
  throw err
}
```

## Distributed Locking with Redis

```typescript
import Redis from 'ioredis'

const redis = new Redis(process.env.REDIS_URL!)

// Simple SETNX + TTL lock
async function acquireLock(key: string, ttlMs: number): Promise<string | null> {
  const token = crypto.randomUUID()
  // SET key token NX PX ttlMs — atomic, returns OK or null
  const result = await redis.set(`lock:${key}`, token, 'NX', 'PX', ttlMs)
  return result === 'OK' ? token : null
}

async function releaseLock(key: string, token: string): Promise<void> {
  // Lua script: only delete if we own the lock (atomic compare-and-delete)
  const script = `
    if redis.call("GET", KEYS[1]) == ARGV[1] then
      return redis.call("DEL", KEYS[1])
    else
      return 0
    end
  `
  await redis.eval(script, 1, `lock:${key}`, token)
}

// Usage
async function processPayment(paymentId: string) {
  const token = await acquireLock(paymentId, 30_000)  // 30s TTL
  if (!token) throw new Error('Payment already being processed')

  try {
    await doPaymentWork(paymentId)
  } finally {
    await releaseLock(paymentId, token)
  }
}
```

### Redlock Algorithm (multi-node)

```typescript
import Redlock from 'redlock'
import Redis from 'ioredis'

// Connect to 3+ independent Redis nodes for Redlock quorum
const clients = [
  new Redis('redis://redis1:6379'),
  new Redis('redis://redis2:6379'),
  new Redis('redis://redis3:6379'),
]

const redlock = new Redlock(clients, {
  retryCount: 3,
  retryDelay: 200,
  retryJitter: 100,
})

async function criticalSection(resourceId: string) {
  await redlock.using([`resource:${resourceId}`], 10_000, async (signal) => {
    if (signal.aborted) throw signal.error

    await performAtomicOperation(resourceId)

    if (signal.aborted) throw signal.error  // check after long operations
  })
}
```

## PostgreSQL Advisory Locks

```typescript
import { Pool } from 'pg'
const pool = new Pool()

// Session-level advisory lock (held until released or connection closes)
async function withAdvisoryLock<T>(lockId: number, fn: () => Promise<T>): Promise<T> {
  const client = await pool.connect()
  try {
    await client.query('SELECT pg_advisory_lock($1)', [lockId])
    return await fn()
  } finally {
    await client.query('SELECT pg_advisory_unlock($1)', [lockId])
    client.release()
  }
}

// Non-blocking try variant — returns false if lock is already held
async function tryAdvisoryLock(lockId: number): Promise<boolean> {
  const client = await pool.connect()
  try {
    const { rows } = await client.query('SELECT pg_try_advisory_lock($1) AS acquired', [lockId])
    return rows[0].acquired
  } finally {
    client.release()
  }
}

// Usage
const PAYMENT_PROCESSOR_LOCK = 12345  // stable integer per operation type
await withAdvisoryLock(PAYMENT_PROCESSOR_LOCK, async () => {
  await processQueue()
})
```

## Idempotency Key Implementation

```typescript
// Middleware: extract idempotency key from header and dedup in DB
import { Request, Response, NextFunction } from 'express'
import { db } from './db'

export async function idempotencyMiddleware(req: Request, res: Response, next: NextFunction) {
  const idempotencyKey = req.headers['idempotency-key'] as string | undefined

  if (!idempotencyKey || req.method === 'GET') return next()

  // Look up existing result
  const existing = await db.idempotencyKeys.findUnique({
    where: { key: idempotencyKey },
  })

  if (existing) {
    // Return cached response — same status and body
    return res.status(existing.statusCode).json(existing.responseBody)
  }

  // Capture response to store it
  const originalJson = res.json.bind(res)
  res.json = (body: unknown) => {
    // Store before sending
    db.idempotencyKeys.create({
      data: {
        key: idempotencyKey,
        statusCode: res.statusCode,
        responseBody: body,
        expiresAt: new Date(Date.now() + 24 * 60 * 60 * 1000),  // 24h TTL
      },
    }).catch(console.error)

    return originalJson(body)
  }

  next()
}
```

```sql
-- DB schema for idempotency keys
CREATE TABLE idempotency_keys (
  key         TEXT PRIMARY KEY,
  status_code INT NOT NULL,
  response_body JSONB NOT NULL,
  created_at  TIMESTAMPTZ DEFAULT NOW(),
  expires_at  TIMESTAMPTZ NOT NULL
);

CREATE INDEX ON idempotency_keys (expires_at);
-- Clean up expired keys via pg_cron or a scheduled job
```

## Atomic Database Operations

```typescript
// SELECT FOR UPDATE: pessimistic lock on row
async function debitAccount(accountId: string, amount: number) {
  await db.$transaction(async (tx) => {
    const account = await tx.$queryRaw<Account[]>`
      SELECT * FROM accounts WHERE id = ${accountId} FOR UPDATE
    `
    if (!account[0] || account[0].balance < amount) {
      throw new Error('Insufficient funds')
    }
    await tx.$executeRaw`
      UPDATE accounts SET balance = balance - ${amount} WHERE id = ${accountId}
    `
  })
}

// UPSERT: atomic insert-or-update (no read-then-write gap)
await db.$executeRaw`
  INSERT INTO user_stats (user_id, login_count, last_login)
  VALUES (${userId}, 1, NOW())
  ON CONFLICT (user_id)
  DO UPDATE SET
    login_count = user_stats.login_count + 1,
    last_login  = NOW()
`
```

## Double-Submit Prevention

```typescript
// Form submit: disable button + server-side idempotency key
// Client side
async function submitForm(data: FormData) {
  const key = crypto.randomUUID()  // generate once per form render
  const response = await fetch('/api/checkout', {
    method: 'POST',
    headers: { 'Idempotency-Key': key },
    body: JSON.stringify(data),
  })
  return response.json()
}

// Payment webhook: verify signature + mark event processed
async function handleStripeWebhook(req: Request, res: Response) {
  const event = stripe.webhooks.constructEvent(
    req.body, req.headers['stripe-signature']!, process.env.STRIPE_WEBHOOK_SECRET!
  )

  // Atomic insert — unique constraint prevents double-processing
  try {
    await db.$executeRaw`
      INSERT INTO processed_webhook_events (event_id, processed_at)
      VALUES (${event.id}, NOW())
    `
  } catch (err: any) {
    if (err.code === '23505') {  // unique_violation
      return res.status(200).json({ received: true })  // already handled
    }
    throw err
  }

  await fulfillOrder(event)
  res.status(200).json({ received: true })
}
```

## Optimistic vs Pessimistic Concurrency Control

```typescript
// Optimistic: version field — no lock held, conflict detected on save
interface Document {
  id: string
  content: string
  version: number
}

async function updateDocument(id: string, content: string, expectedVersion: number) {
  const result = await db.$executeRaw`
    UPDATE documents
    SET content = ${content}, version = version + 1
    WHERE id = ${id} AND version = ${expectedVersion}
  `
  if (result === 0) throw new Error('Conflict: document was modified by another process')
}

// Pessimistic: FOR UPDATE — lock row for duration of transaction
// Use when conflicts are frequent or the cost of retry is high
async function updateDocumentPessimistic(id: string, content: string) {
  await db.$transaction(async (tx) => {
    await tx.$queryRaw`SELECT 1 FROM documents WHERE id = ${id} FOR UPDATE`
    await tx.$executeRaw`UPDATE documents SET content = ${content} WHERE id = ${id}`
  })
}
```

## Serverless Cold Start Race Conditions

```typescript
// Problem: two cold starts may both try to initialize shared state
// Solution: use atomic cloud primitives, not in-process flags

// DynamoDB conditional write for distributed init lock
import { DynamoDB } from '@aws-sdk/client-dynamodb'
const ddb = new DynamoDB({})

async function initializeOnce(jobId: string): Promise<boolean> {
  try {
    await ddb.putItem({
      TableName: 'distributed-locks',
      Item: { pk: { S: `init:${jobId}` } },
      ConditionExpression: 'attribute_not_exists(pk)',
    })
    return true  // this instance won the race
  } catch (err: any) {
    if (err.name === 'ConditionalCheckFailedException') return false  // another won
    throw err
  }
}
```

## Testing for Race Conditions

```typescript
// Run the same operation N times in parallel and assert idempotency
async function testConcurrentDebit() {
  const accountId = await createTestAccount({ balance: 100 })
  const debitAmount = 100

  // Fire 10 concurrent debit requests
  const results = await Promise.allSettled(
    Array.from({ length: 10 }, () => debitAccount(accountId, debitAmount))
  )

  const successes = results.filter(r => r.status === 'fulfilled')
  const failures  = results.filter(r => r.status === 'rejected')

  // Exactly one should succeed
  console.assert(successes.length === 1, `Expected 1 success, got ${successes.length}`)
  console.assert(failures.length === 9,  `Expected 9 failures, got ${failures.length}`)

  const account = await getAccount(accountId)
  console.assert(account.balance === 0, `Balance should be 0, got ${account.balance}`)
}
```

**Core rule**: Every shared mutable resource needs either an atomic operation, a lock, or an idempotency guard. "It works in testing" is not enough — test with parallel load.
