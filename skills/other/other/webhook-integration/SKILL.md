---
name: webhook-integration
description: Implement secure webhook systems for event-driven integrations, including signature verification, retry logic, and delivery guarantees. Use when building third-party integrations, event notifications, or real-time data synchronization.
---

# Webhook Integration

## Overview

Implement robust webhook systems for event-driven architectures, enabling real-time communication between services and third-party integrations.

## When to Use

- Third-party service integrations (Stripe, GitHub, Shopify)
- Event notification systems
- Real-time data synchronization
- Automated workflow triggers
- Payment processing callbacks
- CI/CD pipeline notifications
- User activity tracking
- Microservices communication

## Webhook Architecture

```
┌──────────┐         ┌──────────┐         ┌──────────┐
│  Event   │────────▶│ Webhook  │────────▶│ Consumer │
│  Source  │         │  Sender  │         │ Endpoint │
└──────────┘         └──────────┘         └──────────┘
                           │
                           ▼
                    ┌──────────────┐
                    │ Retry Queue  │
                    │ (Failed)     │
                    └──────────────┘
```

## Implementation Examples

### 1. **Webhook Sender (TypeScript)**

```typescript
import crypto from 'crypto';
import axios from 'axios';

interface WebhookEvent {
  id: string;
  type: string;
  timestamp: number;
  data: any;
}

interface WebhookEndpoint {
  url: string;
  secret: string;
  events: string[];
  active: boolean;
}

interface DeliveryAttempt {
  attemptNumber: number;
  timestamp: number;
  statusCode?: number;
  error?: string;
  duration: number;
}

class WebhookSender {
  private maxRetries = 3;
  private retryDelays = [1000, 5000, 30000]; // Exponential backoff
  private timeout = 10000; // 10 seconds

  /**
   * Generate HMAC signature for webhook payload
   */
  private generateSignature(
    payload: string,
    secret: string
  ): string {
    return crypto
      .createHmac('sha256', secret)
      .update(payload)
      .digest('hex');
  }

  /**
   * Send webhook to endpoint
   */
  async send(
    endpoint: WebhookEndpoint,
    event: WebhookEvent
  ): Promise<DeliveryAttempt[]> {
    if (!endpoint.active) {
      throw new Error('Endpoint is not active');
    }

    if (!endpoint.events.includes(event.type)) {
      throw new Error(`Event type ${event.type} not subscribed`);
    }

    const payload = JSON.stringify(event);
    const signature = this.generateSignature(payload, endpoint.secret);

    const attempts: DeliveryAttempt[] = [];

    for (let attempt = 0; attempt < this.maxRetries; attempt++) {
      const startTime = Date.now();

      try {
        const response = await axios.post(endpoint.url, payload, {
          headers: {
            'Content-Type': 'application/json',
            'X-Webhook-Signature': signature,
            'X-Webhook-ID': event.id,
            'X-Webhook-Timestamp': event.timestamp.toString(),
            'User-Agent': 'WebhookService/1.0'
          },
          timeout: this.timeout,
          validateStatus: (status) => status >= 200 && status < 300
        });

        const duration = Date.now() - startTime;

        attempts.push({
          attemptNumber: attempt + 1,
          timestamp: Date.now(),
          statusCode: response.status,
          duration
        });

        console.log(
          `Webhook delivered successfully to ${endpoint.url} (attempt ${attempt + 1})`
        );

        return attempts;
      } catch (error: any) {
        const duration = Date.now() - startTime;

        attempts.push({
          attemptNumber: attempt + 1,
          timestamp: Date.now(),
          statusCode: error.response?.status,
          error: error.message,
          duration
        });

        console.error(
          `Webhook delivery failed to ${endpoint.url} (attempt ${attempt + 1}):`,
          error.message
        );

        // Wait before retry (except on last attempt)
        if (attempt < this.maxRetries - 1) {
          await this.delay(this.retryDelays[attempt]);
        }
      }
    }

    throw new Error(
      `Webhook delivery failed after ${this.maxRetries} attempts`
    );
  }

  /**
   * Batch send webhooks
   */
  async sendBatch(
    endpoints: WebhookEndpoint[],
    event: WebhookEvent
  ): Promise<Map<string, DeliveryAttempt[]>> {
    const results = new Map<string, DeliveryAttempt[]>();

    await Promise.allSettled(
      endpoints.map(async (endpoint) => {
        try {
          const attempts = await this.send(endpoint, event);
          results.set(endpoint.url, attempts);
        } catch (error) {
          console.error(`Failed to deliver to ${endpoint.url}:`, error);
        }
      })
    );

    return results;
  }

  private delay(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}

// Usage
const sender = new WebhookSender();

const endpoint: WebhookEndpoint = {
  url: 'https://api.example.com/webhooks',
  secret: 'your-webhook-secret',
  events: ['user.created', 'user.updated'],
  active: true
};

const event: WebhookEvent = {
  id: crypto.randomUUID(),
  type: 'user.created',
  timestamp: Date.now(),
  data: {
    userId: '123',
    email: 'user@example.com'
  }
};

await sender.send(endpoint, event);
```

### 2. **Webhook Receiver (Express)**

```typescript
import express from 'express';
import crypto from 'crypto';
import { body, validationResult } from 'express-validator';

interface WebhookConfig {
  secret: string;
  signatureHeader: string;
  timestampTolerance: number; // seconds
}

class WebhookReceiver {
  constructor(private config: WebhookConfig) {}

  /**
   * Verify webhook signature
   */
  verifySignature(
    payload: string,
    signature: string
  ): boolean {
    const expectedSignature = crypto
      .createHmac('sha256', this.config.secret)
      .update(payload)
      .digest('hex');

    return crypto.timingSafeEqual(
      Buffer.from(signature),
      Buffer.from(expectedSignature)
    );
  }

  /**
   * Verify timestamp to prevent replay attacks
   */
  verifyTimestamp(timestamp: number): boolean {
    const now = Date.now();
    const diff = Math.abs(now - timestamp) / 1000;

    return diff <= this.config.timestampTolerance;
  }

  /**
   * Middleware for webhook verification
   */
  createMiddleware() {
    return async (
      req: express.Request,
      res: express.Response,
      next: express.NextFunction
    ) => {
      try {
        const signature = req.headers[this.config.signatureHeader] as string;
        const timestamp = parseInt(
          req.headers['x-webhook-timestamp'] as string
        );

        if (!signature) {
          return res.status(401).json({
            error: 'Missing signature'
          });
        }

        // Verify timestamp
        if (!this.verifyTimestamp(timestamp)) {
          return res.status(401).json({
            error: 'Invalid timestamp'
          });
        }

        // Get raw body for signature verification
        const payload = JSON.stringify(req.body);

        // Verify signature
        if (!this.verifySignature(payload, signature)) {
          return res.status(401).json({
            error: 'Invalid signature'
          });
        }

        next();
      } catch (error) {
        console.error('Webhook verification error:', error);
        res.status(500).json({
          error: 'Verification failed'
        });
      }
    };
  }
}

// Setup Express app
const app = express();

// Use raw body parser for signature verification
app.use(express.json({
  verify: (req: any, res, buf) => {
    req.rawBody = buf.toString();
  }
}));

const receiver = new WebhookReceiver({
  secret: process.env.WEBHOOK_SECRET!,
  signatureHeader: 'x-webhook-signature',
  timestampTolerance: 300 // 5 minutes
});

// Webhook endpoint
app.post('/webhooks',
  receiver.createMiddleware(),
  [
    body('id').isString(),
    body('type').isString(),
    body('data').isObject()
  ],
  async (req, res) => {
    // Validate request
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }

    const { id, type, data } = req.body;

    try {
      // Process webhook event
      await processWebhookEvent(type, data);

      // Respond immediately
      res.status(200).json({
        received: true,
        eventId: id
      });

      // Process asynchronously if needed
      processEventAsync(type, data).catch(console.error);
    } catch (error) {
      console.error('Webhook processing error:', error);
      res.status(500).json({
        error: 'Processing failed'
      });
    }
  }
);

async function processWebhookEvent(type: string, data: any): Promise<void> {
  switch (type) {
    case 'user.created':
      await handleUserCreated(data);
      break;
    case 'payment.success':
      await handlePaymentSuccess(data);
      break;
    default:
      console.log(`Unknown event type: ${type}`);
  }
}

async function processEventAsync(type: string, data: any): Promise<void> {
  // Heavy processing that doesn't need to block the response
}

async function handleUserCreated(data: any): Promise<void> {
  console.log('User created:', data);
}

async function handlePaymentSuccess(data: any): Promise<void> {
  console.log('Payment successful:', data);
}

app.listen(3000, () => {
  console.log('Webhook receiver listening on port 3000');
});
```

### 3. **Webhook Queue with Bull**

```typescript
import Queue from 'bull';
import axios from 'axios';

interface WebhookJob {
  endpoint: WebhookEndpoint;
  event: WebhookEvent;
}

class WebhookQueue {
  private queue: Queue.Queue<WebhookJob>;

  constructor(redisUrl: string) {
    this.queue = new Queue('webhooks', redisUrl, {
      defaultJobOptions: {
        attempts: 3,
        backoff: {
          type: 'exponential',
          delay: 2000
        },
        removeOnComplete: 100,
        removeOnFail: 1000
      }
    });

    this.setupProcessors();
    this.setupEventHandlers();
  }

  private setupProcessors(): void {
    // Process webhook deliveries
    this.queue.process('delivery', 5, async (job) => {
      const { endpoint, event } = job.data;

      job.log(`Delivering webhook to ${endpoint.url}`);

      const sender = new WebhookSender();
      const attempts = await sender.send(endpoint, event);

      return {
        endpoint: endpoint.url,
        attempts,
        success: true
      };
    });
  }

  private setupEventHandlers(): void {
    this.queue.on('completed', (job, result) => {
      console.log(`Webhook delivered: ${job.id}`, result);
    });

    this.queue.on('failed', (job, err) => {
      console.error(`Webhook delivery failed: ${job?.id}`, err);
    });

    this.queue.on('stalled', (job) => {
      console.warn(`Webhook delivery stalled: ${job.id}`);
    });
  }

  async enqueue(
    endpoint: WebhookEndpoint,
    event: WebhookEvent,
    options?: Queue.JobOptions
  ): Promise<Queue.Job<WebhookJob>> {
    return this.queue.add(
      'delivery',
      { endpoint, event },
      {
        jobId: `${event.id}-${endpoint.url}`,
        ...options
      }
    );
  }

  async enqueueBatch(
    endpoints: WebhookEndpoint[],
    event: WebhookEvent
  ): Promise<Queue.Job<WebhookJob>[]> {
    const jobs = endpoints.map(endpoint => ({
      name: 'delivery',
      data: { endpoint, event },
      opts: {
        jobId: `${event.id}-${endpoint.url}`
      }
    }));

    return this.queue.addBulk(jobs);
  }

  async getJobStatus(jobId: string): Promise<any> {
    const job = await this.queue.getJob(jobId);
    if (!job) return null;

    return {
      id: job.id,
      state: await job.getState(),
      progress: job.progress(),
      attempts: job.attemptsMade,
      failedReason: job.failedReason,
      finishedOn: job.finishedOn,
      processedOn: job.processedOn
    };
  }

  async retryFailed(jobId: string): Promise<void> {
    const job = await this.queue.getJob(jobId);
    if (!job) {
      throw new Error('Job not found');
    }

    await job.retry();
  }

  async pause(): Promise<void> {
    await this.queue.pause();
  }

  async resume(): Promise<void> {
    await this.queue.resume();
  }

  async close(): Promise<void> {
    await this.queue.close();
  }
}

// Usage
const webhookQueue = new WebhookQueue('redis://localhost:6379');

// Enqueue single webhook
await webhookQueue.enqueue(endpoint, event, {
  delay: 1000, // Delay 1 second
  priority: 1
});

// Enqueue to multiple endpoints
await webhookQueue.enqueueBatch(endpoints, event);

// Check job status
const status = await webhookQueue.getJobStatus('job-id');
console.log('Job status:', status);
```

### 4. **Webhook Testing Utilities**

```typescript
import express from 'express';
import crypto from 'crypto';

class WebhookTester {
  private app: express.Application;
  private receivedEvents: WebhookEvent[] = [];

  constructor() {
    this.app = express();
    this.setupTestEndpoint();
  }

  private setupTestEndpoint(): void {
    this.app.use(express.json());

    this.app.post('/test-webhook', (req, res) => {
      const event = req.body;

      // Validate signature if provided
      const signature = req.headers['x-webhook-signature'] as string;
      if (signature) {
        // Verify signature here
      }

      // Store received event
      this.receivedEvents.push(event);

      console.log('Received webhook:', event);

      // Respond based on test scenario
      res.status(200).json({
        received: true,
        eventId: event.id
      });
    });

    // Endpoint that simulates failures
    this.app.post('/test-webhook/fail', (req, res) => {
      const failureType = req.query.type;

      switch (failureType) {
        case 'timeout':
          // Don't respond (simulates timeout)
          break;
        case 'server-error':
          res.status(500).json({ error: 'Internal server error' });
          break;
        case 'unauthorized':
          res.status(401).json({ error: 'Unauthorized' });
          break;
        default:
          res.status(400).json({ error: 'Bad request' });
      }
    });
  }

  start(port: number): void {
    this.app.listen(port, () => {
      console.log(`Webhook test server running on port ${port}`);
    });
  }

  getReceivedEvents(): WebhookEvent[] {
    return this.receivedEvents;
  }

  clearEvents(): void {
    this.receivedEvents = [];
  }

  /**
   * Create mock webhook event
   */
  static createMockEvent(type: string, data: any): WebhookEvent {
    return {
      id: crypto.randomUUID(),
      type,
      timestamp: Date.now(),
      data
    };
  }
}

// Testing
const tester = new WebhookTester();
tester.start(3001);

// Send test webhook
const mockEvent = WebhookTester.createMockEvent('user.created', {
  userId: '123',
  email: 'test@example.com'
});

const sender = new WebhookSender();
await sender.send(
  {
    url: 'http://localhost:3001/test-webhook',
    secret: 'test-secret',
    events: ['user.created'],
    active: true
  },
  mockEvent
);

// Verify received
const received = tester.getReceivedEvents();
console.log('Received events:', received);
```

## Best Practices

### ✅ DO
- Use HMAC signatures for verification
- Implement idempotency with event IDs
- Return 200 OK quickly, process asynchronously
- Implement exponential backoff for retries
- Include timestamp to prevent replay attacks
- Use queue systems for reliable delivery
- Log all delivery attempts
- Provide webhook testing tools
- Document webhook payload schemas
- Implement webhook management UI
- Allow filtering by event types
- Support webhook versioning

### ❌ DON'T
- Send sensitive data in webhooks
- Skip signature verification
- Block responses with heavy processing
- Retry indefinitely
- Expose internal error details
- Send webhooks to localhost (in production)
- Forget timeout handling
- Skip rate limiting

## Security Checklist

- [ ] Verify signatures using HMAC
- [ ] Check timestamp to prevent replay attacks
- [ ] Validate SSL certificates
- [ ] Use HTTPS only
- [ ] Implement rate limiting
- [ ] Validate webhook URLs
- [ ] Rotate secrets periodically
- [ ] Log security events
- [ ] Implement IP whitelisting (optional)
- [ ] Sanitize error messages

## Resources

- [Stripe Webhooks Guide](https://stripe.com/docs/webhooks)
- [GitHub Webhooks](https://docs.github.com/en/developers/webhooks-and-events/webhooks)
- [Webhook Best Practices](https://webhooks.fyi/)
