---
name: cloudflare-queues
description: "Cloudflare Queues message queue playbook: producers, consumers, Workers integration, message batching, retries, dead letter queues, delivery delay, concurrency, pull consumers, HTTP API. Keywords: Cloudflare Queues, message queue, producer, consumer, Workers binding, batch, retry, DLQ, dead letter queue, pull consumer, at-least-once delivery."
---

# Cloudflare Queues

Queues is a message queue for Workers. Supports push (Worker consumer) and pull (HTTP API) patterns. At-least-once delivery.

---

## Quick Start

### Create queue

```bash
npx wrangler queues create my-queue
```

### Producer binding

```jsonc
// wrangler.jsonc
{
  "queues": {
    "producers": [
      {
        "queue": "my-queue",
        "binding": "MY_QUEUE"
      }
    ]
  }
}
```

### Consumer binding

```jsonc
// wrangler.jsonc
{
  "queues": {
    "consumers": [
      {
        "queue": "my-queue",
        "max_batch_size": 10,
        "max_batch_timeout": 5
      }
    ]
  }
}
```

### Producer Worker

```typescript
export interface Env {
  MY_QUEUE: Queue;
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    await env.MY_QUEUE.send({ url: request.url, method: request.method });
    return new Response("Message sent");
  },
};
```

### Consumer Worker

```typescript
export interface Env {}

export default {
  async queue(batch: MessageBatch, env: Env): Promise<void> {
    for (const msg of batch.messages) {
      console.log(msg.body);
      msg.ack();
    }
  },
};
```

---

## Producer API

### send(body, options?)

```typescript
await env.MY_QUEUE.send({ action: "process", id: 123 });

// With delay
await env.MY_QUEUE.send(message, { delaySeconds: 600 }); // 10 min delay

// With content type
await env.MY_QUEUE.send(message, { contentType: "json" });
```

### sendBatch(messages, options?)

```typescript
await env.MY_QUEUE.sendBatch([{ body: { id: 1 } }, { body: { id: 2 }, options: { delaySeconds: 300 } }, { body: { id: 3 } }]);

// Global delay for batch
await env.MY_QUEUE.sendBatch(messages, { delaySeconds: 600 });
```

**Limits**:

- Max 100 messages per batch
- Max 128 KB per message
- Total batch ≤ 256 KB

### Content Types

| Type    | Description                     |
| ------- | ------------------------------- |
| `json`  | JSON serialized (default)       |
| `text`  | Plain text                      |
| `bytes` | Raw binary                      |
| `v8`    | V8 serialization (Workers only) |

**Note**: Pull consumers cannot decode `v8` content type.

See [api.md](references/api.md) for type definitions.

---

## Consumer API

### MessageBatch

```typescript
interface MessageBatch<Body = unknown> {
  readonly queue: string;
  readonly messages: Message<Body>[];
  ackAll(): void;
  retryAll(options?: { delaySeconds?: number }): void;
}
```

### Message

```typescript
interface Message<Body = unknown> {
  readonly id: string;
  readonly timestamp: Date;
  readonly body: Body;
  readonly attempts: number;
  ack(): void;
  retry(options?: { delaySeconds?: number }): void;
}
```

### Acknowledgment Patterns

```typescript
export default {
  async queue(batch: MessageBatch, env: Env): Promise<void> {
    for (const msg of batch.messages) {
      try {
        await processMessage(msg.body);
        msg.ack(); // Explicit success
      } catch (error) {
        msg.retry({ delaySeconds: 60 }); // Retry with delay
      }
    }
  },
};
```

### Batch-level operations

```typescript
export default {
  async queue(batch: MessageBatch, env: Env): Promise<void> {
    try {
      await processAll(batch.messages);
      batch.ackAll(); // All succeeded
    } catch (error) {
      batch.retryAll({ delaySeconds: 300 }); // Retry all
    }
  },
};
```

**Precedence**: Per-message calls override batch-level.

---

## Consumer Configuration

```jsonc
{
  "queues": {
    "consumers": [
      {
        "queue": "my-queue",
        "max_batch_size": 10, // 1-100, default 10
        "max_batch_timeout": 5, // 0-60 seconds, default 5
        "max_retries": 3, // default 3
        "max_concurrency": 10, // default: auto-scale
        "dead_letter_queue": "dlq", // optional DLQ
        "retry_delay": 60 // default retry delay (seconds)
      }
    ]
  }
}
```

| Setting             | Default | Max   | Description               |
| ------------------- | ------- | ----- | ------------------------- |
| `max_batch_size`    | 10      | 100   | Messages per batch        |
| `max_batch_timeout` | 5       | 60    | Seconds to wait for batch |
| `max_retries`       | 3       | 100   | Retries before DLQ/delete |
| `max_concurrency`   | auto    | 250   | Concurrent invocations    |
| `retry_delay`       | 0       | 43200 | Default retry delay (12h) |

See [consumer.md](references/consumer.md) for details.

---

## Dead Letter Queues

Messages that fail after `max_retries` go to DLQ.

```jsonc
{
  "queues": {
    "consumers": [
      {
        "queue": "my-queue",
        "max_retries": 5,
        "dead_letter_queue": "my-dlq"
      }
    ]
  }
}
```

**Create DLQ**:

```bash
npx wrangler queues create my-dlq
```

**DLQ retention**: 4 days without consumer.

**Process DLQ**:

```jsonc
{
  "queues": {
    "consumers": [
      {
        "queue": "my-dlq",
        "max_batch_size": 1
      }
    ]
  }
}
```

---

## Delivery Delay

### On send

```typescript
await env.MY_QUEUE.send(message, { delaySeconds: 600 }); // 10 min
```

### On retry

```typescript
msg.retry({ delaySeconds: 3600 }); // 1 hour
```

### Queue-level default

```bash
npx wrangler queues create my-queue --delivery-delay-secs=300
```

### Exponential backoff

```typescript
const backoff = (attempts: number, base = 10) => base ** attempts;

msg.retry({ delaySeconds: Math.min(backoff(msg.attempts), 43200) });
```

**Maximum delay**: 12 hours (43200 seconds).

---

## Concurrency

Consumers auto-scale based on backlog. Set max:

```jsonc
{
  "queues": {
    "consumers": [
      {
        "queue": "my-queue",
        "max_concurrency": 5
      }
    ]
  }
}
```

**max_concurrency: 1** = sequential processing.

**Scaling factors**:

- Backlog size and growth
- Success/failure ratio
- max_concurrency limit

**Note**: `retry()` calls don't count as failures for scaling.

---

## Pull Consumers (HTTP API)

For consuming outside Workers.

### Enable pull consumer

```jsonc
{
  "queues": {
    "consumers": [
      {
        "queue": "my-queue",
        "type": "http_pull",
        "visibility_timeout_ms": 5000,
        "max_retries": 5
      }
    ]
  }
}
```

### Pull messages

```bash
curl -X POST "https://api.cloudflare.com/client/v4/accounts/$ACCOUNT_ID/queues/$QUEUE_ID/messages/pull" \
  -H "Authorization: Bearer $API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"batch_size": 10, "visibility_timeout_ms": 30000}'
```

### Acknowledge messages

```bash
curl -X POST "https://api.cloudflare.com/client/v4/accounts/$ACCOUNT_ID/queues/$QUEUE_ID/messages/ack" \
  -H "Authorization: Bearer $API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "acks": [{"lease_id": "..."}],
    "retries": [{"lease_id": "...", "delay_seconds": 60}]
  }'
```

See [pull-consumer.md](references/pull-consumer.md) for details.

---

## Wrangler Commands

```bash
# Queue management
wrangler queues create <name> [--delivery-delay-secs=N]
wrangler queues delete <name>
wrangler queues list
wrangler queues info <name>

# Pause/resume
wrangler queues pause-delivery <name>
wrangler queues resume-delivery <name>

# Purge all messages
wrangler queues purge <name>

# Consumer management
wrangler queues consumer add <queue> <script> [options]
wrangler queues consumer remove <queue> <script>
wrangler queues consumer http add <queue> [options]
wrangler queues consumer http remove <queue>
```

---

## Limits

| Parameter              | Limit              |
| ---------------------- | ------------------ |
| Queues per account     | 10,000             |
| Message size           | 128 KB             |
| Messages per sendBatch | 100                |
| Batch size (consumer)  | 100                |
| Per-queue throughput   | 5,000 msg/sec      |
| Per-queue backlog      | 25 GB              |
| Message retention      | 4 days (max 14)    |
| Concurrent consumers   | 250                |
| Consumer duration      | 15 min wall clock  |
| Consumer CPU           | 30 sec (max 5 min) |
| Delay (send/retry)     | 12 hours           |
| Max retries            | 100                |

### Increase CPU limit

```jsonc
{
  "limits": {
    "cpu_ms": 300000 // 5 minutes
  }
}
```

---

## Pricing

**Workers Paid**: 1M operations/month included, then $0.40/million.

**Operation** = 64 KB chunk written, read, or deleted.

| Action            | Operations        |
| ----------------- | ----------------- |
| Send 1 message    | 1 write           |
| Consume 1 message | 1 read            |
| Delete 1 message  | 1 delete (on ack) |
| Retry             | 1 additional read |
| DLQ write         | 1 write           |

**Formula**: `(Messages × 3 - 1M) / 1M × $0.40`

**No egress fees**.

See [pricing.md](references/pricing.md) for examples.

---

## Delivery Guarantees

**At-least-once delivery**: Messages delivered at least once, possibly duplicated.

**Handle duplicates**:

```typescript
export default {
  async queue(batch: MessageBatch, env: Env): Promise<void> {
    for (const msg of batch.messages) {
      const key = `processed:${msg.id}`;
      if (await env.KV.get(key)) {
        msg.ack(); // Already processed
        continue;
      }
      await processMessage(msg.body);
      await env.KV.put(key, "1", { expirationTtl: 86400 });
      msg.ack();
    }
  },
};
```

---

## Event Notifications

R2 and other services can send events to Queues.

```bash
# R2 → Queue
wrangler r2 bucket notification create my-bucket \
  --event-type object-create \
  --queue my-queue
```

See `cloudflare-r2` skill for event notification setup.

---

## Prohibitions

- ❌ Do not use `v8` content type with pull consumers
- ❌ Do not exceed 128 KB per message
- ❌ Do not rely on exactly-once delivery (use idempotency)
- ❌ Do not ignore DLQ — process failed messages
- ❌ Do not set excessive concurrency without testing

---

## References

- [api.md](references/api.md) — Producer/Consumer API reference
- [consumer.md](references/consumer.md) — Consumer configuration
- [pull-consumer.md](references/pull-consumer.md) — HTTP pull API
- [pricing.md](references/pricing.md) — Billing details

## Related Skills

- `cloudflare-workers` — Worker development
- `cloudflare-r2` — R2 event notifications
- `cloudflare-durable-objects` — Queue producer from DO
- `cloudflare-kv` — Idempotency tracking
