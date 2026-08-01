---
name: api-messaging-webhooks
description: Webhook patterns — receiving, sending, signature verification, and retry logic
---

# Webhook Patterns

> **Quick Guide:** Verify signatures with HMAC-SHA256 using `crypto.createHmac` + `crypto.timingSafeEqual` on the **raw body bytes** -- never parsed JSON. Enforce idempotency by storing processed webhook IDs. Protect against replay attacks with timestamp validation. Return 200 immediately, process asynchronously. When sending, use exponential backoff with jitter and move exhausted retries to a dead letter queue.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST verify signatures against the RAW request body -- never parsed/re-serialized JSON)**

**(You MUST use `crypto.timingSafeEqual` for signature comparison -- never `===` which leaks timing information)**

**(You MUST return 2xx immediately and process webhooks asynchronously -- synchronous processing causes timeouts and duplicate deliveries)**

**(You MUST enforce idempotency by checking a stored webhook ID before processing -- retries WILL send the same event multiple times)**

</critical_requirements>

---

**Auto-detection:** webhook, webhooks, HMAC, signature verification, createHmac, timingSafeEqual, webhook-signature, webhook-id, webhook-timestamp, idempotency key, replay attack, exponential backoff, dead letter queue, event routing, webhook handler, webhook endpoint, webhook delivery, webhook retry

**When to use:**

- Receiving webhooks from external providers (payment processors, version control, messaging platforms)
- Building a webhook-sending system to notify external consumers of events
- Implementing signature verification for incoming webhook payloads
- Adding retry logic with exponential backoff for outbound webhook delivery
- Routing webhook events to type-safe handlers by event type

**When NOT to use:**

- Real-time bidirectional communication (use WebSockets or Server-Sent Events)
- Internal service-to-service communication where both sides are trusted and co-deployed
- Simple polling scenarios where the consumer controls the fetch timing

**Key patterns covered:**

- HMAC-SHA256 signature verification with timing-safe comparison
- Replay attack protection with timestamp validation
- Idempotency via stored webhook IDs with TTL
- Type-safe event routing with discriminated unions
- Outbound webhook delivery with exponential backoff and jitter
- Dead letter queues for exhausted retries
- Raw body handling to preserve signature integrity

**Detailed Resources:**

- [examples/core.md](examples/core.md) - Receiving, signature verification, idempotency, event routing
- [examples/sending.md](examples/sending.md) - Sending webhooks, retry logic, delivery tracking
- [reference.md](reference.md) - Decision frameworks, header conventions, status code handling

---

<philosophy>

## Philosophy

Webhooks are HTTP callbacks -- a producer POSTs a payload to a consumer's URL when an event occurs. The fundamental challenge is **trust and reliability**: the consumer must verify the payload is authentic (signature verification), not replayed (timestamp validation), and not processed twice (idempotency). The producer must handle delivery failures gracefully (retries with backoff) and not lose events permanently (dead letter queues).

**Core security principle:** The signature is computed over the exact bytes transmitted. Any transformation -- JSON parsing, re-serialization, whitespace normalization -- invalidates the signature. Always verify against the raw body.

**Core reliability principle:** Networks are unreliable. The consumer should acknowledge receipt immediately (return 2xx) and process asynchronously. The producer should retry with exponential backoff and eventually move to a dead letter queue.

**When to implement webhooks:**

- Notifying external systems of events in near-real-time
- Replacing polling for event-driven integrations
- Building platform APIs that external developers consume

**When NOT to implement webhooks:**

- When polling is simpler and latency requirements are relaxed (minutes, not seconds)
- For internal pub/sub where a message broker is more appropriate
- When the consumer cannot expose a public HTTP endpoint

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: HMAC-SHA256 Signature Verification

The foundation of webhook security. The producer signs the payload with a shared secret; the consumer recomputes the signature and compares using timing-safe equality.

```typescript
import { createHmac, timingSafeEqual } from "node:crypto";

const SIGNATURE_ALGORITHM = "sha256";
const SIGNATURE_ENCODING = "hex";

function verifySignature(
  rawBody: string,
  signature: string,
  secret: string,
): boolean {
  const expected = createHmac(SIGNATURE_ALGORITHM, secret)
    .update(rawBody)
    .digest(SIGNATURE_ENCODING);

  const expectedBuffer = Buffer.from(expected, "utf8");
  const receivedBuffer = Buffer.from(signature, "utf8");

  if (expectedBuffer.length !== receivedBuffer.length) return false;

  return timingSafeEqual(expectedBuffer, receivedBuffer);
}
```

**Why good:** uses `timingSafeEqual` to prevent timing attacks, operates on raw body bytes, length check before comparison prevents `timingSafeEqual` throwing on mismatched lengths

See [examples/core.md](examples/core.md) for the full handler with raw body extraction and error responses.

---

### Pattern 2: Replay Attack Protection

Timestamp validation prevents attackers from re-sending captured webhook payloads. Reject payloads older than a tolerance window.

```typescript
const MAX_TIMESTAMP_AGE_SECONDS = 300; // 5 minutes
const MS_PER_SECOND = 1000;

function isTimestampValid(timestampHeader: string): boolean {
  const webhookTime = parseInt(timestampHeader, 10);
  if (Number.isNaN(webhookTime)) return false;

  const currentTime = Math.floor(Date.now() / MS_PER_SECOND);
  return Math.abs(currentTime - webhookTime) <= MAX_TIMESTAMP_AGE_SECONDS;
}
```

**Why good:** uses absolute difference to handle minor clock skew in both directions, rejects `NaN` timestamps, named constants for tolerance window

**When to use:** When the webhook producer includes a timestamp header (most major providers do). Combine with signature verification -- sign the `timestamp.payload` concatenation so the timestamp itself is authenticated.

See [examples/core.md](examples/core.md) for timestamp-inclusive signature verification.

---

### Pattern 3: Idempotency

Webhook producers retry on failure, sending the same event multiple times. Store processed webhook IDs and skip duplicates.

```typescript
const IDEMPOTENCY_TTL_DAYS = 7;

async function processWebhookIdempotently(
  webhookId: string,
  handler: () => Promise<void>,
): Promise<{ status: "processed" | "duplicate" }> {
  const alreadyProcessed = await hasBeenProcessed(webhookId);
  if (alreadyProcessed) return { status: "duplicate" };

  await handler();
  await markAsProcessed(webhookId, IDEMPOTENCY_TTL_DAYS);
  return { status: "processed" };
}
```

**Why good:** checks before processing, stores with TTL to prevent unbounded storage growth, returns status for logging/monitoring

**Storage options:** Any key-value store with TTL support works -- in-memory cache, database table, or dedicated cache service.

See [examples/core.md](examples/core.md) for the complete idempotent webhook handler.

---

### Pattern 4: Type-Safe Event Routing

Route webhook events to handlers using a discriminated union on the event type. The type system enforces exhaustive handling.

```typescript
type WebhookEvent =
  | { type: "order.created"; data: { orderId: string; total: number } }
  | { type: "order.cancelled"; data: { orderId: string; reason: string } }
  | { type: "payment.completed"; data: { paymentId: string; amount: number } };

type EventHandlerMap = {
  [E in WebhookEvent as E["type"]]: (data: E["data"]) => Promise<void>;
};

const handlers: EventHandlerMap = {
  "order.created": async (data) => {
    /* handle */
  },
  "order.cancelled": async (data) => {
    /* handle */
  },
  "payment.completed": async (data) => {
    /* handle */
  },
};

async function routeEvent(event: WebhookEvent): Promise<void> {
  const handler = handlers[event.type] as (
    data: WebhookEvent["data"],
  ) => Promise<void>;
  await handler(event.data);
}
```

**Why good:** adding a new event type to the union causes a compile error until a handler is added, each handler receives correctly typed `data`

See [examples/core.md](examples/core.md) for full event routing with Zod validation and unknown event handling.

---

### Pattern 5: Outbound Webhook Delivery with Retry

When sending webhooks, sign the payload and deliver with exponential backoff. Classify failures by HTTP status to decide whether to retry.

```typescript
const MAX_RETRIES = 5;
const BASE_DELAY_MS = 1000;
const MAX_DELAY_MS = 3600000; // 1 hour

function calculateDelay(attempt: number): number {
  const exponential = BASE_DELAY_MS * Math.pow(2, attempt);
  const capped = Math.min(exponential, MAX_DELAY_MS);
  const jitter = Math.random() * BASE_DELAY_MS;
  return capped + jitter;
}
```

**Why good:** exponential backoff gives failing endpoints recovery time, cap prevents absurd delays, jitter prevents thundering herd when many deliveries retry simultaneously

See [examples/sending.md](examples/sending.md) for complete delivery with signing, status classification, and dead letter queues.

---

### Pattern 6: Dead Letter Queue

After all retry attempts are exhausted, preserve the event for manual investigation rather than dropping it silently.

```typescript
interface DeadLetterEntry {
  webhookId: string;
  targetUrl: string;
  payload: string;
  lastAttempt: Date;
  attempts: number;
  lastError: string;
}
```

**Why good:** preserves full context for debugging, enables manual replay after the target recovers

**When to move to DLQ immediately (no retry):** 400 Bad Request, 401 Unauthorized, 404 Not Found, 422 Unprocessable Entity -- these indicate a configuration or payload problem that retrying won't fix. Exception: 429 Too Many Requests should be retried with the `Retry-After` header value.

See [examples/sending.md](examples/sending.md) for dead letter queue implementation and status code classification.

</patterns>

---

<decision_framework>

## Decision Framework

### Receiving Webhooks

```
Incoming webhook request:
|
+-> Is the raw body available (not parsed)?
|   +-> NO -> Fix your middleware to preserve raw body FIRST
|   +-> YES -> Continue
|
+-> Does the provider send a signature header?
|   +-> YES -> Verify HMAC signature with timing-safe comparison
|   +-> NO -> Use IP allowlisting or mutual TLS instead
|
+-> Does the provider send a timestamp?
|   +-> YES -> Validate timestamp within tolerance (e.g., 5 min)
|   +-> NO -> Skip replay protection (rely on idempotency)
|
+-> Does the provider send a unique event ID?
|   +-> YES -> Check idempotency store, skip if duplicate
|   +-> NO -> Generate a hash of the payload as a dedup key
|
+-> Process asynchronously, return 200 immediately
```

### Sending Webhooks

```
Need to notify external consumers of events?
|
+-> Sign every payload with HMAC-SHA256
+-> Include: webhook-id, webhook-timestamp, webhook-signature headers
+-> Deliver with retry on failure:
    |
    +-> Is it a 2xx response?
    |   +-> YES -> Delivery succeeded, done
    |
    +-> Is it 429, 503, or a network error?
    |   +-> YES -> Retry with exponential backoff + jitter
    |
    +-> Is it 400, 401, 404, 422?
    |   +-> YES -> Move to dead letter queue immediately (not retriable)
    |
    +-> Max retries exhausted?
        +-> YES -> Move to dead letter queue
```

### Status Code Quick Reference

| Status             | Meaning          | Action                   |
| ------------------ | ---------------- | ------------------------ |
| 200-299            | Success          | Mark delivered           |
| 400                | Bad request      | DLQ immediately          |
| 401                | Unauthorized     | DLQ immediately          |
| 404                | Not found        | DLQ immediately          |
| 410                | Gone             | Disable endpoint         |
| 422                | Validation error | DLQ immediately          |
| 429                | Rate limited     | Retry with `Retry-After` |
| 500                | Server error     | Retry with backoff       |
| 502/503            | Unavailable      | Retry with backoff       |
| Timeout            | No response      | Retry with backoff       |
| Connection refused | Unreachable      | Retry with backoff       |

</decision_framework>

---

<red_flags>

## RED FLAGS

**High Priority Issues:**

- Verifying signature against parsed/re-serialized JSON instead of raw body -- JSON serialization is not deterministic (key order, whitespace), so the signature will fail
- Using `===` for signature comparison instead of `crypto.timingSafeEqual` -- leaks timing information that allows attackers to incrementally guess signatures byte by byte
- Processing webhooks synchronously before responding -- causes timeouts which trigger retries which cause duplicate processing
- No idempotency check -- retries from the producer will process the same event multiple times, causing duplicate orders, payments, etc.
- Retrying on 400/401/404 status codes -- these are permanent failures that retrying will never fix, wastes resources and delays DLQ investigation

**Medium Priority Issues:**

- No timestamp validation when the provider sends one -- enables replay attacks with captured payloads
- No maximum retry limit -- infinite retries on a dead endpoint waste resources permanently
- Retrying without jitter -- all failed deliveries retry at the same time (thundering herd)
- Using in-memory idempotency store in a multi-instance deployment -- each instance has a separate store, duplicates still occur
- Wildcard CORS on webhook endpoints -- webhook endpoints should not serve browser requests at all

**Gotchas & Edge Cases:**

- `crypto.timingSafeEqual` throws if buffers have different lengths -- always check `.length` equality first or convert both to the same encoding before comparison
- Webhook middleware order matters -- raw body capture middleware must run BEFORE any JSON parsing middleware, or the raw bytes are lost
- Some providers prefix signatures (e.g., `sha256=abc123`) -- strip the prefix before comparison
- Clock skew between producer and consumer can cause valid webhooks to fail timestamp validation -- use `Math.abs()` for the time difference and allow 5 minutes tolerance
- 410 Gone from a consumer means the endpoint is permanently removed -- disable the subscription instead of retrying
- Exponential backoff without a cap grows to astronomical delays -- always cap at a reasonable maximum (e.g., 1 hour)
- Webhook IDs should have a TTL in the idempotency store -- without TTL, storage grows unbounded

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md**

**(You MUST verify signatures against the RAW request body -- never parsed/re-serialized JSON)**

**(You MUST use `crypto.timingSafeEqual` for signature comparison -- never `===` which leaks timing information)**

**(You MUST return 2xx immediately and process webhooks asynchronously -- synchronous processing causes timeouts and duplicate deliveries)**

**(You MUST enforce idempotency by checking a stored webhook ID before processing -- retries WILL send the same event multiple times)**

**Failure to follow these rules will cause signature verification failures, timing attack vulnerabilities, duplicate event processing, and lost webhook events.**

</critical_reminders>
