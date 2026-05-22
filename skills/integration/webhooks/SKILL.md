---
name: webhooks
description: Webhook implementation and consumption patterns. Use when implementing webhook endpoints, webhook receivers, webhook senders, HTTP callbacks, event notifications, push notifications, or real-time integrations. Covers signature verification (HMAC, crypto), retry strategies (exponential backoff), idempotency keys, delivery guarantees, webhook security, payload design, and monitoring. Keywords: webhook, webhooks, callback, callbacks, HTTP callback, event notification, push notification, signature verification, HMAC, hmac, crypto signature, retry, exponential backoff, idempotency, idempotent, delivery guarantee, at-least-once delivery, webhook receiver, webhook sender, webhook security, webhook authentication, replay attack, dead letter queue, webhook monitoring.
---

# Webhooks

## Overview

Webhooks are HTTP callbacks that notify external systems when events occur. They enable real-time communication between services without polling. This skill covers webhook design patterns, security, reliability, and implementation best practices.

## Key Concepts

### Webhook Design Patterns

**Event-Driven Architecture:**

```typescript
interface WebhookEvent {
  id: string; // Unique event ID
  type: string; // Event type (e.g., 'order.created')
  created: number; // Unix timestamp
  apiVersion: string; // API version for payload format
  data: {
    object: Record<string, any>; // The resource that triggered the event
    previousAttributes?: Record<string, any>; // For update events
  };
}

// Example events
const orderCreatedEvent: WebhookEvent = {
  id: "evt_1234567890",
  type: "order.created",
  created: 1702987200,
  apiVersion: "2024-01-01",
  data: {
    object: {
      id: "ord_abc123",
      status: "pending",
      total: 9999,
      currency: "usd",
      customer: "cus_xyz789",
    },
  },
};

const orderUpdatedEvent: WebhookEvent = {
  id: "evt_1234567891",
  type: "order.updated",
  created: 1702987260,
  apiVersion: "2024-01-01",
  data: {
    object: {
      id: "ord_abc123",
      status: "shipped",
      total: 9999,
      currency: "usd",
    },
    previousAttributes: {
      status: "pending",
    },
  },
};
```

**Webhook Subscription Model:**

```typescript
interface WebhookEndpoint {
  id: string;
  url: string;
  secret: string;
  events: string[]; // Event types to receive
  status: "active" | "disabled";
  metadata?: Record<string, string>;
  createdAt: Date;
  updatedAt: Date;
}

interface WebhookDelivery {
  id: string;
  endpointId: string;
  eventId: string;
  url: string;
  requestHeaders: Record<string, string>;
  requestBody: string;
  responseStatus?: number;
  responseHeaders?: Record<string, string>;
  responseBody?: string;
  duration?: number;
  attempts: number;
  nextRetryAt?: Date;
  status: "pending" | "success" | "failed" | "retrying";
  createdAt: Date;
  completedAt?: Date;
}
```

### Signature Verification (HMAC)

**Generating Signatures:**

```typescript
import crypto from "crypto";

class WebhookSigner {
  constructor(private secret: string) {}

  sign(payload: string, timestamp: number): string {
    const signedPayload = `${timestamp}.${payload}`;
    return crypto
      .createHmac("sha256", this.secret)
      .update(signedPayload)
      .digest("hex");
  }

  generateHeaders(payload: string): Record<string, string> {
    const timestamp = Math.floor(Date.now() / 1000);
    const signature = this.sign(payload, timestamp);

    return {
      "X-Webhook-Timestamp": timestamp.toString(),
      "X-Webhook-Signature": `v1=${signature}`,
      "Content-Type": "application/json",
    };
  }
}
```

**Verifying Signatures:**

```typescript
class WebhookVerifier {
  constructor(
    private secret: string,
    private tolerance: number = 300 // 5 minutes
  ) {}

  verify(payload: string, signature: string, timestamp: string): boolean {
    // Check timestamp to prevent replay attacks
    const ts = parseInt(timestamp, 10);
    const now = Math.floor(Date.now() / 1000);

    if (Math.abs(now - ts) > this.tolerance) {
      throw new WebhookError(
        "Timestamp outside tolerance",
        "TIMESTAMP_EXPIRED"
      );
    }

    // Extract signature value
    const sigParts = signature.split(",");
    const v1Sig = sigParts
      .find((part) => part.startsWith("v1="))
      ?.replace("v1=", "");

    if (!v1Sig) {
      throw new WebhookError("No valid signature found", "INVALID_SIGNATURE");
    }

    // Compute expected signature
    const signedPayload = `${timestamp}.${payload}`;
    const expectedSig = crypto
      .createHmac("sha256", this.secret)
      .update(signedPayload)
      .digest("hex");

    // Constant-time comparison
    const isValid = crypto.timingSafeEqual(
      Buffer.from(v1Sig),
      Buffer.from(expectedSig)
    );

    if (!isValid) {
      throw new WebhookError("Signature mismatch", "INVALID_SIGNATURE");
    }

    return true;
  }
}

class WebhookError extends Error {
  constructor(message: string, public code: string) {
    super(message);
    this.name = "WebhookError";
  }
}
```

**Express Middleware for Verification:**

```typescript
import express from "express";

function webhookVerificationMiddleware(secret: string) {
  const verifier = new WebhookVerifier(secret);

  return (
    req: express.Request,
    res: express.Response,
    next: express.NextFunction
  ) => {
    const signature = req.headers["x-webhook-signature"] as string;
    const timestamp = req.headers["x-webhook-timestamp"] as string;

    if (!signature || !timestamp) {
      return res.status(401).json({ error: "Missing signature headers" });
    }

    // Need raw body for signature verification
    let rawBody = "";
    req.setEncoding("utf8");

    req.on("data", (chunk) => {
      rawBody += chunk;
    });

    req.on("end", () => {
      try {
        verifier.verify(rawBody, signature, timestamp);
        req.body = JSON.parse(rawBody);
        next();
      } catch (error) {
        if (error instanceof WebhookError) {
          return res
            .status(401)
            .json({ error: error.message, code: error.code });
        }
        return res.status(400).json({ error: "Invalid request" });
      }
    });
  };
}

// Usage with raw body parser
app.post(
  "/webhooks",
  express.raw({ type: "application/json" }),
  (req, res, next) => {
    const verifier = new WebhookVerifier(process.env.WEBHOOK_SECRET!);
    try {
      verifier.verify(
        req.body.toString(),
        req.headers["x-webhook-signature"] as string,
        req.headers["x-webhook-timestamp"] as string
      );
      req.body = JSON.parse(req.body.toString());
      next();
    } catch (error) {
      res.status(401).json({ error: "Invalid signature" });
    }
  }
);
```

### Retry Logic with Exponential Backoff

**Retry Configuration:**

```typescript
interface RetryConfig {
  maxAttempts: number;
  initialDelay: number; // milliseconds
  maxDelay: number; // milliseconds
  backoffMultiplier: number;
  retryableStatuses: number[];
}

const defaultRetryConfig: RetryConfig = {
  maxAttempts: 5,
  initialDelay: 1000, // 1 second
  maxDelay: 3600000, // 1 hour
  backoffMultiplier: 2,
  retryableStatuses: [408, 429, 500, 502, 503, 504],
};

function calculateNextRetry(attempt: number, config: RetryConfig): number {
  // Exponential backoff with jitter
  const delay = Math.min(
    config.initialDelay * Math.pow(config.backoffMultiplier, attempt),
    config.maxDelay
  );

  // Add random jitter (0-25% of delay)
  const jitter = delay * Math.random() * 0.25;

  return delay + jitter;
}
```

**Webhook Delivery Service:**

```typescript
import fetch from "node-fetch";

class WebhookDeliveryService {
  constructor(
    private db: Database,
    private retryConfig: RetryConfig = defaultRetryConfig
  ) {}

  async deliver(endpoint: WebhookEndpoint, event: WebhookEvent): Promise<void> {
    const delivery = await this.createDelivery(endpoint, event);
    await this.attemptDelivery(delivery);
  }

  private async createDelivery(
    endpoint: WebhookEndpoint,
    event: WebhookEvent
  ): Promise<WebhookDelivery> {
    const payload = JSON.stringify(event);
    const signer = new WebhookSigner(endpoint.secret);
    const headers = signer.generateHeaders(payload);

    return this.db.deliveries.create({
      id: generateId(),
      endpointId: endpoint.id,
      eventId: event.id,
      url: endpoint.url,
      requestHeaders: headers,
      requestBody: payload,
      attempts: 0,
      status: "pending",
      createdAt: new Date(),
    });
  }

  async attemptDelivery(delivery: WebhookDelivery): Promise<void> {
    delivery.attempts++;

    const startTime = Date.now();

    try {
      const response = await fetch(delivery.url, {
        method: "POST",
        headers: delivery.requestHeaders,
        body: delivery.requestBody,
        timeout: 30000, // 30 second timeout
      });

      delivery.responseStatus = response.status;
      delivery.responseHeaders = Object.fromEntries(response.headers);
      delivery.responseBody = await response.text();
      delivery.duration = Date.now() - startTime;

      if (response.ok) {
        delivery.status = "success";
        delivery.completedAt = new Date();
      } else if (this.shouldRetry(delivery)) {
        await this.scheduleRetry(delivery);
      } else {
        delivery.status = "failed";
        delivery.completedAt = new Date();
      }
    } catch (error) {
      delivery.duration = Date.now() - startTime;

      if (this.shouldRetry(delivery)) {
        await this.scheduleRetry(delivery);
      } else {
        delivery.status = "failed";
        delivery.completedAt = new Date();
      }
    }

    await this.db.deliveries.update(delivery);
  }

  private shouldRetry(delivery: WebhookDelivery): boolean {
    if (delivery.attempts >= this.retryConfig.maxAttempts) {
      return false;
    }

    // Retry on network errors or retryable status codes
    if (!delivery.responseStatus) {
      return true;
    }

    return this.retryConfig.retryableStatuses.includes(delivery.responseStatus);
  }

  private async scheduleRetry(delivery: WebhookDelivery): Promise<void> {
    const delay = calculateNextRetry(delivery.attempts, this.retryConfig);
    delivery.nextRetryAt = new Date(Date.now() + delay);
    delivery.status = "retrying";

    // Queue for later processing
    await this.queue.add(
      "webhook-retry",
      {
        deliveryId: delivery.id,
      },
      {
        delay,
      }
    );
  }
}
```

### Idempotency Keys

**Idempotency Implementation:**

```typescript
class IdempotencyManager {
  constructor(private redis: Redis) {}

  async checkAndStore(
    key: string,
    ttl: number = 86400 // 24 hours
  ): Promise<{ isNew: boolean; existingResult?: any }> {
    const existing = await this.redis.get(`idempotency:${key}`);

    if (existing) {
      return {
        isNew: false,
        existingResult: JSON.parse(existing),
      };
    }

    // Mark as processing
    const acquired = await this.redis.set(
      `idempotency:${key}`,
      JSON.stringify({ status: "processing" }),
      "EX",
      ttl,
      "NX"
    );

    return { isNew: acquired === "OK" };
  }

  async storeResult(
    key: string,
    result: any,
    ttl: number = 86400
  ): Promise<void> {
    await this.redis.set(
      `idempotency:${key}`,
      JSON.stringify({ status: "completed", result }),
      "EX",
      ttl
    );
  }

  async markFailed(key: string): Promise<void> {
    await this.redis.del(`idempotency:${key}`);
  }
}
```

**Webhook Handler with Idempotency:**

```typescript
class WebhookHandler {
  constructor(
    private idempotency: IdempotencyManager,
    private handlers: Map<string, (data: any) => Promise<any>>
  ) {}

  async handleEvent(event: WebhookEvent): Promise<any> {
    // Use event ID as idempotency key
    const check = await this.idempotency.checkAndStore(event.id);

    if (!check.isNew) {
      console.log(`Event ${event.id} already processed`);
      return check.existingResult?.result;
    }

    try {
      const handler = this.handlers.get(event.type);

      if (!handler) {
        console.log(`No handler for event type: ${event.type}`);
        return null;
      }

      const result = await handler(event.data);
      await this.idempotency.storeResult(event.id, result);

      return result;
    } catch (error) {
      await this.idempotency.markFailed(event.id);
      throw error;
    }
  }
}
```

### Webhook Payload Design

**Payload Structure Best Practices:**

```typescript
// Good: Self-contained payload with all needed data
interface GoodWebhookPayload {
  id: string;
  type: "invoice.paid";
  apiVersion: string;
  created: number;
  data: {
    object: {
      id: string;
      customerId: string;
      customerEmail: string;
      amount: number;
      currency: string;
      status: string;
      lineItems: Array<{
        description: string;
        amount: number;
        quantity: number;
      }>;
      paidAt: string;
    };
  };
  // Include related data to avoid extra API calls
  relatedObjects?: {
    customer: {
      id: string;
      name: string;
      email: string;
    };
  };
}

// Bad: Requires additional API calls
interface BadWebhookPayload {
  type: "invoice.paid";
  invoiceId: string; // Only ID, no data - receiver must fetch
}
```

**Versioning Strategy:**

```typescript
class WebhookPayloadTransformer {
  private transformers: Map<string, (data: any) => any> = new Map();

  constructor() {
    // Register version transformers
    this.transformers.set("2023-01-01", this.transformV20230101);
    this.transformers.set("2024-01-01", this.transformV20240101);
  }

  transform(event: WebhookEvent, targetVersion: string): WebhookEvent {
    const transformer = this.transformers.get(targetVersion);

    if (!transformer) {
      throw new Error(`Unknown API version: ${targetVersion}`);
    }

    return {
      ...event,
      apiVersion: targetVersion,
      data: {
        ...event.data,
        object: transformer(event.data.object),
      },
    };
  }

  private transformV20230101(data: any): any {
    // Legacy format
    return {
      ...data,
      amount_cents: data.amount, // Old field name
    };
  }

  private transformV20240101(data: any): any {
    // Current format
    return data;
  }
}
```

### Delivery Guarantees

**At-Least-Once Delivery:**

```typescript
class WebhookDispatcher {
  private queue: Queue;
  private deliveryService: WebhookDeliveryService;

  async dispatch(
    event: WebhookEvent,
    endpoints: WebhookEndpoint[]
  ): Promise<void> {
    // Persist event first
    await this.db.events.create(event);

    // Queue deliveries for each endpoint
    for (const endpoint of endpoints) {
      if (endpoint.status !== "active") continue;
      if (!this.matchesEventFilter(event.type, endpoint.events)) continue;

      await this.queue.add(
        "webhook-delivery",
        {
          eventId: event.id,
          endpointId: endpoint.id,
        },
        {
          attempts: 5,
          backoff: {
            type: "exponential",
            delay: 1000,
          },
          removeOnComplete: true,
          removeOnFail: false, // Keep failed jobs for inspection
        }
      );
    }
  }

  private matchesEventFilter(eventType: string, filters: string[]): boolean {
    return filters.some((filter) => {
      if (filter === "*") return true;
      if (filter.endsWith(".*")) {
        const prefix = filter.slice(0, -2);
        return eventType.startsWith(prefix);
      }
      return eventType === filter;
    });
  }
}
```

**Dead Letter Queue:**

```typescript
class DeadLetterHandler {
  constructor(private db: Database, private alertService: AlertService) {}

  async handleFailedDelivery(delivery: WebhookDelivery): Promise<void> {
    // Move to dead letter queue
    await this.db.deadLetterQueue.create({
      id: generateId(),
      deliveryId: delivery.id,
      eventId: delivery.eventId,
      endpointId: delivery.endpointId,
      lastAttempt: new Date(),
      totalAttempts: delivery.attempts,
      lastError: delivery.responseBody,
      lastStatus: delivery.responseStatus,
      createdAt: new Date(),
    });

    // Alert on repeated failures
    const recentFailures = await this.db.deadLetterQueue.count({
      endpointId: delivery.endpointId,
      createdAt: { $gte: new Date(Date.now() - 3600000) }, // Last hour
    });

    if (recentFailures >= 10) {
      await this.alertService.send({
        severity: "warning",
        title: "Webhook Endpoint Failing",
        message: `Endpoint ${delivery.endpointId} has ${recentFailures} failures in the last hour`,
        metadata: {
          endpointId: delivery.endpointId,
          url: delivery.url,
        },
      });

      // Optionally disable the endpoint
      await this.disableEndpointIfNeeded(delivery.endpointId);
    }
  }

  private async disableEndpointIfNeeded(endpointId: string): Promise<void> {
    const failures24h = await this.db.deadLetterQueue.count({
      endpointId,
      createdAt: { $gte: new Date(Date.now() - 86400000) },
    });

    if (failures24h >= 100) {
      await this.db.webhookEndpoints.update(endpointId, {
        status: "disabled",
        disabledReason: "Too many consecutive failures",
      });
    }
  }
}
```

### Webhook Monitoring and Debugging

**Delivery Dashboard Data:**

```typescript
interface WebhookMetrics {
  endpointId: string;
  period: "hour" | "day" | "week";
  totalDeliveries: number;
  successfulDeliveries: number;
  failedDeliveries: number;
  avgResponseTime: number;
  p95ResponseTime: number;
  successRate: number;
  errorBreakdown: Record<number, number>; // status code -> count
}

class WebhookMetricsService {
  constructor(private db: Database) {}

  async getMetrics(
    endpointId: string,
    period: "hour" | "day" | "week"
  ): Promise<WebhookMetrics> {
    const since = this.getPeriodStart(period);

    const deliveries = await this.db.deliveries.aggregate([
      {
        $match: {
          endpointId,
          createdAt: { $gte: since },
        },
      },
      {
        $group: {
          _id: null,
          total: { $sum: 1 },
          successful: {
            $sum: { $cond: [{ $eq: ["$status", "success"] }, 1, 0] },
          },
          failed: {
            $sum: { $cond: [{ $eq: ["$status", "failed"] }, 1, 0] },
          },
          avgDuration: { $avg: "$duration" },
          durations: { $push: "$duration" },
        },
      },
    ]);

    const errorBreakdown = await this.db.deliveries.aggregate([
      {
        $match: {
          endpointId,
          createdAt: { $gte: since },
          status: "failed",
        },
      },
      {
        $group: {
          _id: "$responseStatus",
          count: { $sum: 1 },
        },
      },
    ]);

    const data = deliveries[0] || { total: 0, successful: 0, failed: 0 };

    return {
      endpointId,
      period,
      totalDeliveries: data.total,
      successfulDeliveries: data.successful,
      failedDeliveries: data.failed,
      avgResponseTime: data.avgDuration || 0,
      p95ResponseTime: this.calculateP95(data.durations || []),
      successRate: data.total > 0 ? data.successful / data.total : 0,
      errorBreakdown: Object.fromEntries(
        errorBreakdown.map((e) => [e._id, e.count])
      ),
    };
  }

  private getPeriodStart(period: string): Date {
    const now = new Date();
    switch (period) {
      case "hour":
        return new Date(now.getTime() - 3600000);
      case "day":
        return new Date(now.getTime() - 86400000);
      case "week":
        return new Date(now.getTime() - 604800000);
      default:
        return now;
    }
  }

  private calculateP95(values: number[]): number {
    if (values.length === 0) return 0;
    const sorted = values.sort((a, b) => a - b);
    const index = Math.ceil(sorted.length * 0.95) - 1;
    return sorted[index];
  }
}
```

**Event Replay:**

```typescript
class WebhookReplayService {
  constructor(
    private db: Database,
    private deliveryService: WebhookDeliveryService
  ) {}

  async replayEvent(eventId: string, endpointId?: string): Promise<void> {
    const event = await this.db.events.findById(eventId);
    if (!event) {
      throw new Error(`Event not found: ${eventId}`);
    }

    let endpoints: WebhookEndpoint[];

    if (endpointId) {
      const endpoint = await this.db.webhookEndpoints.findById(endpointId);
      if (!endpoint) {
        throw new Error(`Endpoint not found: ${endpointId}`);
      }
      endpoints = [endpoint];
    } else {
      endpoints = await this.db.webhookEndpoints.findByEventType(event.type);
    }

    for (const endpoint of endpoints) {
      await this.deliveryService.deliver(endpoint, event);
    }
  }

  async replayFailedDeliveries(
    endpointId: string,
    since: Date
  ): Promise<number> {
    const failedDeliveries = await this.db.deliveries.find({
      endpointId,
      status: "failed",
      createdAt: { $gte: since },
    });

    for (const delivery of failedDeliveries) {
      const event = await this.db.events.findById(delivery.eventId);
      const endpoint = await this.db.webhookEndpoints.findById(endpointId);

      if (event && endpoint) {
        await this.deliveryService.deliver(endpoint, event);
      }
    }

    return failedDeliveries.length;
  }
}
```

## Best Practices

### Security (Signature Verification, Authentication)

**Core Principles:**

- Always use HTTPS for webhook URLs
- Implement HMAC signature verification for authentication
- Include timestamp in signatures to prevent replay attacks
- Use constant-time comparison for signatures (timing-safe)
- Rotate webhook secrets periodically
- Validate payload structure before processing
- Rate limit webhook endpoints to prevent abuse

**When to Use:**

- Any webhook receiver that handles sensitive data
- Systems requiring proof of origin
- Preventing man-in-the-middle attacks
- Ensuring message integrity

### Reliability (Retry Strategies, Delivery Guarantees)

**Core Principles:**

- Implement exponential backoff with jitter for retries
- Use idempotency keys to handle duplicates safely
- Provide at-least-once delivery guarantees
- Queue webhook deliveries asynchronously
- Implement dead letter queues for persistent failures
- Set reasonable timeout limits (30s recommended)
- Track delivery attempts and final status

**Retry Configuration:**

- Max attempts: 5 (configurable)
- Initial delay: 1 second
- Max delay: 1 hour
- Retryable status codes: 408, 429, 500, 502, 503, 504
- Add 0-25% random jitter to prevent thundering herd

**When to Use:**

- Systems requiring guaranteed event delivery
- Distributed architectures with network unreliability
- Customer-facing webhook integrations
- Any async event notification system

### Idempotency (Duplicate Prevention)

**Core Principles:**

- Use event ID as idempotency key
- Store processing status in Redis/cache (24h TTL)
- Return cached result for duplicate requests
- Mark as processing to prevent race conditions
- Clean up failed processing attempts

**When to Use:**

- Payment processing webhooks
- Order creation/updates
- Any state-changing operation
- Systems with retry logic (prevents double-processing)

### Payload Design (Event Structure)

**Core Principles:**

- Include all necessary data in the payload (avoid extra API calls)
- Version your webhook payloads (`apiVersion` field)
- Keep payloads reasonably sized (< 256KB)
- Use consistent event naming conventions (`resource.action`)
- Include event IDs for deduplication
- Provide `previousAttributes` for update events
- Add timestamps (Unix epoch) for event timing

**Event Naming Patterns:**

- `order.created`, `order.updated`, `order.cancelled`
- `payment.completed`, `payment.failed`
- `user.registered`, `user.deleted`
- Support wildcard subscriptions: `order.*`, `*`

**When to Use:**

- Designing new webhook systems
- Improving webhook consumer experience
- Version migrations for breaking changes

### Receiver Implementation (Webhook Endpoints)

**Core Principles:**

- Respond quickly (< 5 seconds, ideally < 1 second)
- Process webhooks asynchronously (acknowledge first, process later)
- Store raw payloads before processing (for replay/debugging)
- Implement proper error handling
- Return appropriate status codes (200 for success, 4xx for permanent errors, 5xx for retries)
- Use request ID for tracing

**Status Code Guidelines:**

- 200: Successfully received and queued
- 400: Bad request (malformed payload, will not retry)
- 401: Invalid signature (authentication failure, will not retry)
- 500: Internal error (sender will retry)
- 503: Service temporarily unavailable (sender will retry)

**When to Use:**

- Building webhook receiver endpoints
- Integrating with third-party webhooks (Stripe, GitHub, etc.)
- Ensuring webhook endpoint reliability

### Monitoring (Observability, Debugging)

**Core Principles:**

- Track delivery success rates per endpoint
- Alert on endpoint failures (disable after threshold)
- Log all delivery attempts with full context
- Provide webhook event logs to customers
- Implement replay functionality for failed events
- Monitor response times (avg, p95, p99)
- Dashboard showing delivery metrics

**Key Metrics:**

- Total deliveries (hour/day/week)
- Success rate percentage
- Average response time
- P95 response time
- Error breakdown by status code
- Dead letter queue size

**When to Use:**

- Operating production webhook systems
- Debugging customer integration issues
- SLA monitoring and alerting
- Capacity planning

## Examples

### Complete Webhook System

```typescript
// Webhook sender service
import express from "express";
import { Queue, Worker } from "bullmq";
import Redis from "ioredis";

const redis = new Redis(process.env.REDIS_URL);
const webhookQueue = new Queue("webhooks", { connection: redis });

// Event emitter
async function emitEvent(type: string, data: any): Promise<void> {
  const event: WebhookEvent = {
    id: `evt_${generateId()}`,
    type,
    created: Math.floor(Date.now() / 1000),
    apiVersion: "2024-01-01",
    data: { object: data },
  };

  // Persist event
  await db.events.create(event);

  // Find subscribed endpoints
  const endpoints = await db.webhookEndpoints.find({
    status: "active",
    events: { $in: [type, "*", `${type.split(".")[0]}.*`] },
  });

  // Queue deliveries
  for (const endpoint of endpoints) {
    await webhookQueue.add("deliver", {
      eventId: event.id,
      endpointId: endpoint.id,
    });
  }
}

// Delivery worker
const worker = new Worker(
  "webhooks",
  async (job) => {
    const { eventId, endpointId } = job.data;

    const event = await db.events.findById(eventId);
    const endpoint = await db.webhookEndpoints.findById(endpointId);

    if (!event || !endpoint) return;

    const payload = JSON.stringify(event);
    const signer = new WebhookSigner(endpoint.secret);
    const headers = signer.generateHeaders(payload);

    const response = await fetch(endpoint.url, {
      method: "POST",
      headers,
      body: payload,
      timeout: 30000,
    });

    if (!response.ok) {
      throw new Error(`Webhook delivery failed: ${response.status}`);
    }
  },
  {
    connection: redis,
    limiter: { max: 100, duration: 1000 },
  }
);

// Webhook receiver
const app = express();

app.post("/webhooks", express.raw({ type: "application/json" }), (req, res) => {
  const verifier = new WebhookVerifier(process.env.WEBHOOK_SECRET!);

  try {
    verifier.verify(
      req.body.toString(),
      req.headers["x-webhook-signature"] as string,
      req.headers["x-webhook-timestamp"] as string
    );
  } catch (error) {
    return res.status(401).json({ error: "Invalid signature" });
  }

  const event = JSON.parse(req.body.toString()) as WebhookEvent;

  // Acknowledge quickly
  res.status(200).json({ received: true });

  // Process asynchronously
  processEventAsync(event).catch(console.error);
});

async function processEventAsync(event: WebhookEvent): Promise<void> {
  // Check idempotency
  const processed = await redis.get(`processed:${event.id}`);
  if (processed) return;

  // Handle event by type
  switch (event.type) {
    case "order.created":
      await handleOrderCreated(event.data.object);
      break;
    case "payment.completed":
      await handlePaymentCompleted(event.data.object);
      break;
  }

  // Mark as processed
  await redis.set(`processed:${event.id}`, "1", "EX", 86400);
}
```
