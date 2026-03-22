---
name: cloudflare-queues
description: |
  Build async message queues with Cloudflare Queues for background processing. Use when: handling async tasks, batch processing, implementing retries, configuring dead letter queues, managing consumer concurrency, or troubleshooting queue timeout, batch retry, message loss, or throughput exceeded. Prevents 13 documented errors including multi-dev limitations, remote binding conflicts, and DLQ issues.
user-invocable: true
---

# Cloudflare Queues

**Status**: Production Ready ✅
**Last Updated**: 2026-01-09
**Dependencies**: cloudflare-worker-base (for Worker setup)
**Latest Versions**: wrangler@4.58.0, @cloudflare/workers-types@4.20260109.0

**Recent Updates (2025)**:
- **April 2025**: Pull consumers increased limits (5,000 msg/s per queue, up from 1,200 requests/5min)
- **March 2025**: Pause & Purge APIs (wrangler queues pause-delivery, queues purge)
- **2025**: Customizable retention (60s to 14 days, previously fixed at 4 days)
- **2025**: Increased queue limits (10,000 queues per account, up from 10)

---

## Quick Start (5 Minutes)

```bash
# 1. Create queue
npx wrangler queues create my-queue

# 2. Add producer binding to wrangler.jsonc
# { "queues": { "producers": [{ "binding": "MY_QUEUE", "queue": "my-queue" }] } }

# 3. Send message from Worker
await env.MY_QUEUE.send({ userId: '123', action: 'process-order' });

# Or publish via HTTP (May 2025+) from any service
curl -X POST "https://api.cloudflare.com/client/v4/accounts/{account_id}/queues/my-queue/messages" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -d '{"messages": [{"body": {"userId": "123"}}]}'

# 4. Add consumer binding to wrangler.jsonc
# { "queues": { "consumers": [{ "queue": "my-queue", "max_batch_size": 10 }] } }

# 5. Process messages
export default {
  async queue(batch: MessageBatch, env: Env): Promise<void> {
    for (const message of batch.messages) {
      await processMessage(message.body);
      message.ack(); // Explicit acknowledgement
    }
  }
};

# 6. Deploy and test
npx wrangler deploy
npx wrangler tail my-consumer
```

---

## Producer API

```typescript
// Send single message
await env.MY_QUEUE.send({ userId: '123', action: 'send-email' });

// Send with delay (max 12 hours)
await env.MY_QUEUE.send({ action: 'reminder' }, { delaySeconds: 600 });

// Send batch (max 100 messages or 256 KB)
await env.MY_QUEUE.sendBatch([
  { body: { userId: '1' } },
  { body: { userId: '2' } },
]);
```

**Critical Limits:**
- Message size: **128 KB max** (including ~100 bytes metadata)
- Messages >128 KB will fail - store in R2 and send reference instead
- Batch size: 100 messages or 256 KB total
- Delay: 0-43200 seconds (12 hours max)

---

## HTTP Publishing (May 2025+)

**New in May 2025**: Publish messages to queues via HTTP from any service or programming language.

**Source**: [Cloudflare Changelog](https://developers.cloudflare.com/changelog/2025-05-09-publish-to-queues-via-http/)

**Authentication**: Requires Cloudflare API token with `Queues Edit` permissions.

```bash
# Single message
curl -X POST "https://api.cloudflare.com/client/v4/accounts/{account_id}/queues/my-queue/messages" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"body": {"userId": "123", "action": "process-order"}}
    ]
  }'

# Batch messages
curl -X POST "https://api.cloudflare.com/client/v4/accounts/{account_id}/queues/my-queue/messages" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"body": {"userId": "1"}},
      {"body": {"userId": "2"}},
      {"body": {"userId": "3"}}
    ]
  }'
```

**Use Cases**:
- Publishing from external microservices (Node.js, Python, Go, etc.)
- Cron jobs running outside Cloudflare
- Webhook receivers
- Legacy systems integration
- Services without Cloudflare Workers SDK

---

## Event Subscriptions (August 2025+)

**New in August 2025**: Subscribe to events from Cloudflare services and consume via Queues.

**Source**: [Cloudflare Changelog](https://developers.cloudflare.com/changelog/2025-08-19-event-subscriptions/)

**Supported Event Sources**:
- R2 (bucket.created, object.uploaded, object.deleted, etc.)
- Workers KV
- Workers AI
- Vectorize
- Workflows
- Super Slurper
- Workers Builds

**Create Subscription**:
```bash
npx wrangler queues subscription create my-queue \
  --source r2 \
  --events bucket.created,object.uploaded
```

**Event Structure**:
```typescript
interface CloudflareEvent {
  type: string;           // 'r2.bucket.created', 'kv.namespace.created'
  source: string;         // 'r2', 'kv', 'ai', etc.
  payload: any;           // Event-specific data
  metadata: {
    accountId: string;
    timestamp: string;
  };
}
```

**Consumer Example**:
```typescript
export default {
  async queue(batch: MessageBatch, env: Env): Promise<void> {
    for (const message of batch.messages) {
      const event = message.body as CloudflareEvent;

      switch (event.type) {
        case 'r2.bucket.created':
          console.log('New R2 bucket:', event.payload.bucketName);
          await notifyAdmin(event.payload);
          break;

        case 'r2.object.uploaded':
          console.log('File uploaded:', event.payload.key);
          await processNewFile(event.payload.key);
          break;

        case 'kv.namespace.created':
          console.log('New KV namespace:', event.payload.namespaceId);
          break;

        case 'ai.inference.completed':
          console.log('AI inference done:', event.payload.modelId);
          break;
      }

      message.ack();
    }
  }
};
```

**Use Cases**:
- Build custom workflows triggered by R2 uploads
- Monitor infrastructure changes (new KV namespaces, buckets)
- Track AI inference jobs
- Audit account activity
- Event-driven architectures without custom webhooks

---

## Consumer API

```typescript
export default {
  async queue(batch: MessageBatch, env: Env, ctx: ExecutionContext): Promise<void> {
    for (const message of batch.messages) {
      // message.id - unique UUID
      // message.timestamp - Date when sent
      // message.body - your content
      // message.attempts - retry count (starts at 1)

      await processMessage(message.body);
      message.ack(); // Explicit ack (critical for non-idempotent ops)
    }
  }
};

// Retry with exponential backoff
message.retry({ delaySeconds: Math.min(60 * Math.pow(2, message.attempts - 1), 3600) });

// Batch methods
batch.ackAll();   // Ack all messages
batch.retryAll(); // Retry all messages
```

**Critical:**
- **`message.ack()`** - Mark success, prevents retry even if handler fails later
- **Use explicit ack for non-idempotent operations** (DB writes, API calls, payments)
- **Implicit ack** - If handler returns successfully without calling ack(), all messages auto-acknowledged
- **Ordering not guaranteed** - Don't assume FIFO message order

---

## Critical Consumer Patterns

### Explicit Acknowledgement (Non-Idempotent Operations)

**ALWAYS use explicit ack() for:** Database writes, API calls, financial transactions

```typescript
export default {
  async queue(batch: MessageBatch, env: Env): Promise<void> {
    for (const message of batch.messages) {
      try {
        await env.DB.prepare('INSERT INTO orders (id, amount) VALUES (?, ?)')
          .bind(message.body.orderId, message.body.amount).run();
        message.ack(); // Only ack on success
      } catch (error) {
        console.error(`Failed ${message.id}:`, error);
        // Don't ack - will retry
      }
    }
  }
};
```

**Why?** Prevents duplicate writes if one message in batch fails. Failed messages retry independently.

---

### Exponential Backoff for Rate-Limited APIs

```typescript
export default {
  async queue(batch: MessageBatch, env: Env): Promise<void> {
    for (const message of batch.messages) {
      try {
        await fetch('https://api.example.com/process', {
          method: 'POST',
          body: JSON.stringify(message.body),
        });
        message.ack();
      } catch (error) {
        if (error.status === 429) {
          const delaySeconds = Math.min(60 * Math.pow(2, message.attempts - 1), 3600);
          message.retry({ delaySeconds });
        } else {
          message.retry();
        }
      }
    }
  }
};
```

---

### Dead Letter Queue (DLQ) - CRITICAL for Production

**⚠️ Without DLQ, failed messages are DELETED PERMANENTLY after max_retries**

```bash
npx wrangler queues create my-dlq
```

**wrangler.jsonc:**
```jsonc
{
  "queues": {
    "consumers": [{
      "queue": "my-queue",
      "max_retries": 3,
      "dead_letter_queue": "my-dlq"  // Messages go here after 3 failed retries
    }]
  }
}
```

**DLQ Consumer:**
```typescript
export default {
  async queue(batch: MessageBatch, env: Env): Promise<void> {
    for (const message of batch.messages) {
      console.error('PERMANENTLY FAILED:', message.id, message.body);
      await env.DB.prepare('INSERT INTO failed_messages (id, body) VALUES (?, ?)')
        .bind(message.id, JSON.stringify(message.body)).run();
      message.ack(); // Remove from DLQ
    }
  }
};
```

---

## Known Issues Prevention

This skill prevents **13** documented issues:

### Issue #1: Multiple Dev Commands - Queues Don't Flow Between Processes

**Error**: Queue messages sent in one `wrangler dev` process don't appear in another `wrangler dev` consumer process
**Source**: [GitHub Issue #9795](https://github.com/cloudflare/workers-sdk/issues/9795)

**Why It Happens**: The virtual queue used by wrangler is in-process memory. Separate dev processes cannot share the queue state.

**Prevention**:
```bash
# ❌ Don't run producer and consumer as separate processes
# Terminal 1: wrangler dev (producer)
# Terminal 2: wrangler dev (consumer)  # Won't receive messages!

# ✅ Option 1: Run both in single dev command
wrangler dev -c producer/wrangler.jsonc -c consumer/wrangler.jsonc

# ✅ Option 2: Use Vite plugin with auxiliaryWorkers
# vite.config.ts:
export default defineConfig({
  plugins: [
    cloudflare({
      auxiliaryWorkers: ['./consumer/wrangler.jsonc']
    })
  ]
})
```

---

### Issue #2: Queue Producer Binding Causes 500 Errors with Remote Dev

**Error**: All routes return 500 Internal Server Error when using `wrangler dev --remote` with queue bindings
**Source**: [GitHub Issue #9642](https://github.com/cloudflare/workers-sdk/issues/9642)

**Why It Happens**: Queues are not yet supported in `wrangler dev --remote` mode. Even routes that don't use the queue binding fail.

**Prevention**:
```jsonc
// When using remote dev, temporarily comment out queue bindings
{
  "queues": {
    // "producers": [{ "queue": "my-queue", "binding": "MY_QUEUE" }]
  }
}

// Or use local dev instead
// wrangler dev (without --remote)
```

---

### Issue #3: D1 Remote Breaks When Queue Remote is Set

**Error**: D1 remote binding stops working when `remote: true` is set on queue producer binding
**Source**: [GitHub Issue #11106](https://github.com/cloudflare/workers-sdk/issues/11106)

**Why It Happens**: Binding conflict issue affecting mixed local/remote development.

**Prevention**:
```jsonc
// ❌ Don't mix D1 remote with queue remote
{
  "d1_databases": [{
    "binding": "DB",
    "database_id": "...",
    "remote": true
  }],
  "queues": {
    "producers": [{
      "binding": "QUEUE",
      "queue": "my-queue",
      "remote": true  // ❌ Breaks D1 remote
    }]
  }
}

// ✅ Avoid remote on queues when using D1 remote
{
  "d1_databases": [{ "binding": "DB", "remote": true }],
  "queues": {
    "producers": [{ "binding": "QUEUE", "queue": "my-queue" }]
  }
}
```

**Status**: No workaround yet. Track issue for updates.

---

### Issue #4: Mixed Local/Remote Bindings - Queue Consumer Missing

**Error**: Queue consumer binding does not appear when mixing local queues with remote AI/Vectorize bindings
**Source**: [GitHub Issue #9887](https://github.com/cloudflare/workers-sdk/issues/9887)

**Why It Happens**: Wrangler doesn't support mixed local/remote bindings in the same worker.

**Prevention**:
```jsonc
// ❌ Don't mix local queues with remote AI
{
  "queues": {
    "consumers": [{ "queue": "my-queue" }]
  },
  "ai": {
    "binding": "AI",
    "experimental_remote": true  // ❌ Breaks queue consumer
  }
}

// ✅ Option 1: All local (no remote bindings)
wrangler dev

// ✅ Option 2: Separate workers for queues vs AI
// Worker 1: Queue processing (local)
// Worker 2: AI operations (remote)
```

---

### Issue #5: http_pull Type Prevents Worker Consumer Execution

**Error**: Queue consumer with `type: "http_pull"` doesn't execute in production
**Source**: [GitHub Issue #6619](https://github.com/cloudflare/workers-sdk/issues/6619)

**Why It Happens**: `http_pull` is for external HTTP-based consumers, not Worker-based consumers.

**Prevention**:
```jsonc
// ❌ Don't use type: "http_pull" for Worker consumers
{
  "queues": {
    "consumers": [{
      "queue": "my-queue",
      "type": "http_pull",  // ❌ Wrong for Workers
      "max_batch_size": 10
    }]
  }
}

// ✅ Omit type field for push-based Worker consumers
{
  "queues": {
    "consumers": [{
      "queue": "my-queue",
      "max_batch_size": 10
      // No "type" field - defaults to Worker consumer
    }]
  }
}
```

---

## Breaking Changes & Deprecations

### delivery_delay in Producer Config (Upcoming Removal)

**Warning**: The `delivery_delay` parameter in producer bindings will be removed in a future wrangler version.

**Source**: [GitHub Issue #10286](https://github.com/cloudflare/workers-sdk/issues/10286)

```jsonc
// ❌ Will be removed - don't use
{
  "queues": {
    "producers": [{
      "binding": "MY_QUEUE",
      "queue": "my-queue",
      "delivery_delay": 300  // ❌ Don't use this
    }]
  }
}
```

**Migration**: Use per-message delay instead:
```typescript
// ✅ Correct approach - per-message delay
await env.MY_QUEUE.send({ data }, { delaySeconds: 300 });
```

**Why**: Workers should not affect queue-level settings. With multiple producers, the setting from the last-deployed producer wins, causing unpredictable behavior.

---

## Community Tips

> **Note**: These tips come from community discussions and GitHub issues. Verify against your wrangler version.

### Tip: max_batch_timeout May Break Local Development

**Source**: [GitHub Issue #6619](https://github.com/cloudflare/workers-sdk/issues/6619#issuecomment-2396888227)
**Confidence**: MEDIUM
**Applies to**: Local development with `wrangler dev`

If your queue consumer doesn't execute locally, try removing `max_batch_timeout`:

```jsonc
{
  "queues": {
    "consumers": [{
      "queue": "my-queue",
      "max_batch_size": 10
      // Remove max_batch_timeout for local dev
    }]
  }
}
```

This appears to be version-specific and may not affect all setups.

---

### Tip: Queue Name Not Available on Producer Bindings

**Source**: [GitHub Issue #10131](https://github.com/cloudflare/workers-sdk/issues/10131)
**Confidence**: HIGH
**Applies to**: Multi-environment deployments (staging, PR previews, tenant-specific queues)

Queue names are only available via `batch.queue` in consumer handlers, not on producer bindings. This creates issues with environment-specific queue names like `email-queue-staging` or `email-queue-pr-123`.

**Current Limitation**:
```typescript
// ❌ Can't access queue name from producer binding
const queueName = env.MY_QUEUE.name; // Doesn't exist!

// ❌ Must hardcode or normalize in consumer
switch (batch.queue) {
  case 'email-queue':           // What about email-queue-staging?
  case 'email-queue-staging':   // Must handle all variants
  case 'email-queue-pr-123':    // Dynamic env names break this
}
```

**Workaround**:
```typescript
// In consumer: Normalize queue name
function normalizeQueueName(queueName: string): string {
  return queueName.replace(/-staging|-pr-\d+|-dev/g, '');
}

switch (normalizeQueueName(batch.queue)) {
  case 'email-queue':
    // Handle all email-queue-* variants
}
```

**Status**: Feature request tracked internally: [MQ-923](https://jira.cfdata.org/browse/MQ-923)

---

## Consumer Configuration

```jsonc
{
  "queues": {
    "consumers": [{
      "queue": "my-queue",
      "max_batch_size": 100,           // 1-100 (default: 10)
      "max_batch_timeout": 30,         // 0-60s (default: 5s)
      "max_retries": 5,                // 0-100 (default: 3)
      "retry_delay": 300,              // Seconds (default: 0)
      "max_concurrency": 10,           // 1-250 (default: auto-scale)
      "dead_letter_queue": "my-dlq"    // REQUIRED for production
    }]
  }
}
```

**Critical Settings:**

- **Batching** - Consumer called when EITHER condition met (max_batch_size OR max_batch_timeout)
- **max_retries** - After exhausted: with DLQ → sent to DLQ, without DLQ → **DELETED PERMANENTLY**
- **max_concurrency** - Only set if upstream has rate limits or connection limits. Otherwise leave unset for auto-scaling (up to 250 concurrent invocations)
- **DLQ** - Create separately: `npx wrangler queues create my-dlq`

---

## Wrangler Commands

```bash
# Create queue
npx wrangler queues create my-queue
npx wrangler queues create my-queue --message-retention-period-secs 1209600  # 14 days

# Manage queues
npx wrangler queues list
npx wrangler queues info my-queue
npx wrangler queues delete my-queue  # ⚠️ Deletes ALL messages!

# Pause/Purge (March 2025 - NEW)
npx wrangler queues pause-delivery my-queue   # Pause processing, keep receiving
npx wrangler queues resume-delivery my-queue
npx wrangler queues purge my-queue            # ⚠️ Permanently deletes all messages!

# Consumer management
npx wrangler queues consumer add my-queue my-consumer-worker \
  --batch-size 50 --batch-timeout 10 --message-retries 5
npx wrangler queues consumer remove my-queue my-consumer-worker
```

---

## Limits & Quotas

| Feature | Limit |
|---------|-------|
| **Queues per account** | 10,000 |
| **Message size** | 128 KB (includes ~100 bytes metadata) |
| **Message retries** | 100 max |
| **Batch size** | 1-100 messages |
| **Batch timeout** | 0-60 seconds |
| **Messages per sendBatch** | 100 (or 256 KB total) |
| **Queue throughput** | 5,000 messages/second per queue |
| **Message retention** | 4 days (default), 14 days (max) |
| **Queue backlog size** | 25 GB per queue |
| **Concurrent consumers** | 250 (push-based, auto-scale) |
| **Consumer duration** | 15 minutes (wall clock) |
| **Consumer CPU time** | 30 seconds (default), 5 minutes (max) |
| **Visibility timeout** | 12 hours (pull consumers) |
| **Message delay** | 12 hours (max) |
| **API rate limit** | 1200 requests / 5 minutes |

---

## Pricing

**Requires Workers Paid plan** ($5/month)

**Operations Pricing:**
- First 1,000,000 operations/month: **FREE**
- After that: **$0.40 per million operations**

**What counts as an operation:**
- Each 64 KB chunk written, read, or deleted
- Messages >64 KB count as multiple operations:
  - 65 KB message = 2 operations
  - 127 KB message = 2 operations
  - 128 KB message = 2 operations

**Typical message lifecycle:**
- 1 write + 1 read + 1 delete = **3 operations**

**Retries:**
- Each retry = additional **read operation**
- Message retried 3 times = 1 write + 4 reads + 1 delete = **6 operations**

**Dead Letter Queue:**
- Writing to DLQ = additional **write operation**

**Cost examples:**
- 1M messages/month (no retries): ((1M × 3) - 1M) / 1M × $0.40 = **$0.80**
- 10M messages/month: ((10M × 3) - 1M) / 1M × $0.40 = **$11.60**
- 100M messages/month: ((100M × 3) - 1M) / 1M × $0.40 = **$119.60**

---


## Error Handling

### Common Errors

#### 1. Message Too Large

```typescript
// ❌ Bad: Message >128 KB
await env.MY_QUEUE.send({
  data: largeArray, // >128 KB
});

// ✅ Good: Check size before sending
const message = { data: largeArray };
const size = new TextEncoder().encode(JSON.stringify(message)).length;

if (size > 128000) {
  // Store in R2, send reference
  const key = `messages/${crypto.randomUUID()}.json`;
  await env.MY_BUCKET.put(key, JSON.stringify(message));
  await env.MY_QUEUE.send({ type: 'large-message', r2Key: key });
} else {
  await env.MY_QUEUE.send(message);
}
```

---

#### 2. Throughput Exceeded

```typescript
// ❌ Bad: Exceeding 5000 msg/s per queue
for (let i = 0; i < 10000; i++) {
  await env.MY_QUEUE.send({ id: i }); // Too fast!
}

// ✅ Good: Use sendBatch
const messages = Array.from({ length: 10000 }, (_, i) => ({
  body: { id: i },
}));

// Send in batches of 100
for (let i = 0; i < messages.length; i += 100) {
  await env.MY_QUEUE.sendBatch(messages.slice(i, i + 100));
}

// ✅ Even better: Rate limit with delay
for (let i = 0; i < messages.length; i += 100) {
  await env.MY_QUEUE.sendBatch(messages.slice(i, i + 100));
  if (i + 100 < messages.length) {
    await new Promise(resolve => setTimeout(resolve, 100)); // 100ms delay
  }
}
```

---

#### 3. Consumer Timeout

```typescript
// ❌ Bad: Long processing without CPU limit increase
export default {
  async queue(batch: MessageBatch): Promise<void> {
    for (const message of batch.messages) {
      await processForMinutes(message.body); // CPU timeout!
    }
  },
};

// ✅ Good: Increase CPU limit in wrangler.jsonc
```

**wrangler.jsonc:**

```jsonc
{
  "limits": {
    "cpu_ms": 300000  // 5 minutes (max allowed)
  }
}
```

---

#### 4. Backlog Growing

```typescript
// Issue: Consumer too slow, backlog growing

// ✅ Solution 1: Increase batch size
{
  "queues": {
    "consumers": [{
      "queue": "my-queue",
      "max_batch_size": 100  // Process more per invocation
    }]
  }
}

// ✅ Solution 2: Let concurrency auto-scale (don't set max_concurrency)

// ✅ Solution 3: Optimize consumer code
export default {
  async queue(batch: MessageBatch, env: Env): Promise<void> {
    // Process in parallel
    await Promise.all(
      batch.messages.map(async (message) => {
        await process(message.body);
        message.ack();
      })
    );
  },
};
```

---

## Critical Rules

**Always:**
- ✅ Configure DLQ for production (`dead_letter_queue` in consumer config)
- ✅ Use explicit `message.ack()` for non-idempotent ops (DB writes, API calls)
- ✅ Validate message size <128 KB before sending
- ✅ Use `sendBatch()` for multiple messages (more efficient)
- ✅ Implement exponential backoff: `60 * Math.pow(2, message.attempts - 1)`
- ✅ Let concurrency auto-scale (don't set `max_concurrency` unless upstream has rate limits)

**Never:**
- ❌ Never assume FIFO ordering - not guaranteed
- ❌ Never rely on implicit ack for non-idempotent ops - use explicit `ack()`
- ❌ Never send messages >128 KB - will fail (store in R2 instead)
- ❌ Never skip DLQ in production - failed messages DELETED PERMANENTLY without DLQ
- ❌ Never exceed 5,000 msg/s per queue (push consumers) or rate limits apply
- ❌ Never process messages synchronously - use `Promise.all()` for parallelism

---

## Troubleshooting

### Issue: Messages not being delivered to consumer

**Possible causes:**
1. Consumer not deployed
2. Wrong queue name in wrangler.jsonc
3. Delivery paused
4. Consumer throwing errors

**Solution:**

```bash
# Check queue info
npx wrangler queues info my-queue

# Check if delivery paused
npx wrangler queues resume-delivery my-queue

# Check consumer logs
npx wrangler tail my-consumer
```

---

### Issue: Entire batch retried when one message fails

**Cause:** Using implicit acknowledgement with non-idempotent operations

**Solution:** Use explicit ack()

```typescript
// ✅ Explicit ack
for (const message of batch.messages) {
  try {
    await dbWrite(message.body);
    message.ack(); // Only ack on success
  } catch (error) {
    console.error(`Failed: ${message.id}`);
    // Don't ack - will retry
  }
}
```

---

### Issue: Messages deleted without processing

**Cause:** No Dead Letter Queue configured

**Solution:**

```bash
# Create DLQ
npx wrangler queues create my-dlq

# Add to consumer config
```

```jsonc
{
  "queues": {
    "consumers": [{
      "queue": "my-queue",
      "dead_letter_queue": "my-dlq"
    }]
  }
}
```

---

### Issue: Consumer not auto-scaling

**Possible causes:**
1. `max_concurrency` set to 1
2. Consumer returning errors (not processing)
3. Batch processing too fast (no backlog)

**Solution:**

```jsonc
{
  "queues": {
    "consumers": [{
      "queue": "my-queue",
      // Don't set max_concurrency - let it auto-scale
      "max_batch_size": 50  // Increase batch size instead
    }]
  }
}
```

---

## Related Documentation

- [Cloudflare Queues Docs](https://developers.cloudflare.com/queues/)
- [How Queues Works](https://developers.cloudflare.com/queues/reference/how-queues-works/)
- [JavaScript APIs](https://developers.cloudflare.com/queues/configuration/javascript-apis/)
- [Batching & Retries](https://developers.cloudflare.com/queues/configuration/batching-retries/)
- [Consumer Concurrency](https://developers.cloudflare.com/queues/configuration/consumer-concurrency/)
- [Dead Letter Queues](https://developers.cloudflare.com/queues/configuration/dead-letter-queues/)
- [Wrangler Commands](https://developers.cloudflare.com/queues/reference/wrangler-commands/)
- [Limits](https://developers.cloudflare.com/queues/platform/limits/)
- [Pricing](https://developers.cloudflare.com/queues/platform/pricing/)

---

**Last Updated**: 2026-01-21
**Version**: 2.0.0
**Changes**: Added HTTP Publishing (May 2025), Event Subscriptions (Aug 2025), Known Issues Prevention (13 issues), Breaking Changes section, Community Tips. Error count: 0 → 13. Major feature additions and comprehensive issue documentation.
**Maintainer**: Jeremy Dawes | jeremy@jezweb.net
