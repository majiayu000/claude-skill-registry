---
name: bknd-webhooks
description: Use when configuring webhook integrations in Bknd. Covers receiving incoming webhooks via HTTP triggers, sending outgoing webhooks with FetchTask, event-triggered webhooks on data changes, signature verification, retry patterns, and async processing.
---

# Webhooks

Configure webhook integrations for receiving external events and sending notifications on data changes.

## Prerequisites

- Running Bknd instance
- Understanding of HTTP and webhooks concept
- Familiarity with Bknd Flows (see `bknd-custom-endpoint`)

## When to Use UI Mode

Webhook configuration requires code. No UI approach available.

## When to Use Code Mode

- Receiving webhooks from external services (Stripe, GitHub, etc.)
- Sending notifications when data changes
- Integrating with third-party services
- Building event-driven architectures

## Webhook Types

| Type | Description | Approach |
|------|-------------|----------|
| **Incoming** | Receive webhooks from external services | HTTP Trigger + Flow |
| **Outgoing** | Send webhooks when events occur | EventTrigger + FetchTask |

---

## Receiving Incoming Webhooks

### Step 1: Basic Webhook Receiver

```typescript
import { App, Flow, HttpTrigger, Task } from "bknd";
import { s } from "bknd/utils";

class WebhookReceiverTask extends Task<typeof WebhookReceiverTask.schema> {
  override type = "webhook-receiver";
  static override schema = s.strictObject({});

  override async execute(input: Request) {
    const body = await input.json();
    const eventType = input.headers.get("x-event-type");

    console.log(`Received webhook: ${eventType}`, body);

    return { received: true, event: eventType };
  }
}

const receiverTask = new WebhookReceiverTask("receive", {});

const webhookFlow = new Flow("incoming-webhook", [receiverTask]);
webhookFlow.setRespondingTask(receiverTask);

webhookFlow.setTrigger(
  new HttpTrigger({
    path: "/webhooks/external",
    method: "POST",
    mode: "async",  // Return 200 immediately
  })
);

const app = new App({
  flows: { flows: [webhookFlow] },
});
```

### Step 2: Webhook with Signature Verification

```typescript
import { createHmac, timingSafeEqual } from "crypto";

class SecureWebhookTask extends Task<typeof SecureWebhookTask.schema> {
  override type = "secure-webhook";

  static override schema = s.strictObject({
    secret: s.string(),
  });

  override async execute(input: Request) {
    const signature = input.headers.get("x-webhook-signature");
    const body = await input.text();

    // Verify signature
    if (!this.verifySignature(body, signature)) {
      throw this.error("Invalid signature", { signature });
    }

    const data = JSON.parse(body);
    return { verified: true, data };
  }

  private verifySignature(payload: string, signature: string | null): boolean {
    if (!signature) return false;

    const expected = createHmac("sha256", this.params.secret)
      .update(payload)
      .digest("hex");

    const sig = Buffer.from(signature);
    const exp = Buffer.from(`sha256=${expected}`);

    return sig.length === exp.length && timingSafeEqual(sig, exp);
  }
}

const secureTask = new SecureWebhookTask("verify", {
  secret: process.env.WEBHOOK_SECRET!,
});

const secureFlow = new Flow("secure-webhook", [secureTask]);
secureFlow.setRespondingTask(secureTask);
secureFlow.setTrigger(
  new HttpTrigger({
    path: "/webhooks/secure",
    method: "POST",
  })
);
```

### Step 3: Stripe Webhook Receiver

```typescript
import Stripe from "stripe";

class StripeWebhookTask extends Task<typeof StripeWebhookTask.schema> {
  override type = "stripe-webhook";

  static override schema = s.strictObject({
    webhookSecret: s.string(),
  });

  override async execute(input: Request) {
    const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!);
    const sig = input.headers.get("stripe-signature")!;
    const body = await input.text();

    let event: Stripe.Event;

    try {
      event = stripe.webhooks.constructEvent(
        body,
        sig,
        this.params.webhookSecret
      );
    } catch (err) {
      throw this.error("Webhook verification failed", { err });
    }

    // Handle event types
    switch (event.type) {
      case "checkout.session.completed":
        const session = event.data.object;
        // Process successful payment...
        break;

      case "customer.subscription.deleted":
        // Handle subscription cancellation...
        break;
    }

    return { received: true, type: event.type };
  }
}
```

### Step 4: GitHub Webhook Receiver

```typescript
class GitHubWebhookTask extends Task<typeof GitHubWebhookTask.schema> {
  override type = "github-webhook";

  static override schema = s.strictObject({
    secret: s.string(),
  });

  override async execute(input: Request) {
    const event = input.headers.get("x-github-event");
    const delivery = input.headers.get("x-github-delivery");
    const signature = input.headers.get("x-hub-signature-256");
    const body = await input.text();

    // Verify GitHub signature
    const expected = createHmac("sha256", this.params.secret)
      .update(body)
      .digest("hex");

    if (signature !== `sha256=${expected}`) {
      throw this.error("Invalid GitHub signature");
    }

    const payload = JSON.parse(body);

    switch (event) {
      case "push":
        console.log(`Push to ${payload.ref} by ${payload.pusher.name}`);
        break;

      case "pull_request":
        console.log(`PR ${payload.action}: ${payload.pull_request.title}`);
        break;

      case "issues":
        console.log(`Issue ${payload.action}: ${payload.issue.title}`);
        break;
    }

    return { event, delivery };
  }
}
```

### Step 5: Plugin-Based Webhook Receiver

For simpler cases, use plugin routes:

```typescript
import { createPlugin } from "bknd";
import { Hono } from "hono";

const webhooksPlugin = createPlugin({
  name: "webhooks",

  onServerInit: (server) => {
    const webhooks = new Hono();

    // Stripe
    webhooks.post("/stripe", async (c) => {
      const sig = c.req.header("stripe-signature");
      const body = await c.req.text();
      // Verify and process...
      return c.json({ received: true });
    });

    // GitHub
    webhooks.post("/github", async (c) => {
      const event = c.req.header("x-github-event");
      const body = await c.req.json();
      // Process...
      return c.json({ received: true });
    });

    // Generic
    webhooks.post("/:source", async (c) => {
      const source = c.req.param("source");
      const body = await c.req.json();
      console.log(`Webhook from ${source}:`, body);
      return c.json({ received: true });
    });

    server.route("/webhooks", webhooks);
  },
});
```

---

## Sending Outgoing Webhooks

Use Flows with EventTrigger to send webhooks when data changes.

### Step 1: Basic Outgoing Webhook

```typescript
import { App, Flow, FetchTask, EventTrigger } from "bknd";

// Task to send webhook
const sendWebhook = new FetchTask("send-webhook", {
  url: "https://example.com/webhook",
  method: "POST",
  headers: [
    { key: "Content-Type", value: "application/json" },
    { key: "X-Webhook-Source", value: "my-app" },
  ],
  body: "{{JSON.stringify(input)}}",  // Forward event data
});

const webhookFlow = new Flow("outgoing-webhook", [sendWebhook]);

// Trigger on data event
webhookFlow.setTrigger(
  new EventTrigger({
    event: "mutator-insert-after",  // After record created
    mode: "async",
  })
);

const app = new App({
  flows: { flows: [webhookFlow] },
});
```

### Step 2: Entity-Specific Webhook

```typescript
import { App, Flow, FetchTask, Task, EventTrigger } from "bknd";
import { s } from "bknd/utils";

// Filter task to check entity
class EntityFilterTask extends Task<typeof EntityFilterTask.schema> {
  override type = "entity-filter";

  static override schema = s.strictObject({
    targetEntity: s.string(),
  });

  override async execute(input: any) {
    if (input.entity?.name !== this.params.targetEntity) {
      throw this.error("Skip - wrong entity");
    }
    return input;
  }
}

const filterTask = new EntityFilterTask("filter", {
  targetEntity: "orders",
});

const sendWebhook = new FetchTask("send", {
  url: "https://api.example.com/orders/webhook",
  method: "POST",
  headers: [{ key: "Content-Type", value: "application/json" }],
  body: "{{JSON.stringify({ event: 'order.created', data: input.changed })}}",
});

const flow = new Flow("order-webhook", [filterTask, sendWebhook]);
flow.task(filterTask).asInputFor(sendWebhook);

flow.setTrigger(
  new EventTrigger({
    event: "mutator-insert-after",
    mode: "async",
  })
);
```

### Step 3: Multi-Destination Webhooks

```typescript
import { Flow, FetchTask, EventTrigger, Condition } from "bknd";

// Send to multiple endpoints
const sendSlack = new FetchTask("slack", {
  url: "https://hooks.slack.com/services/XXX/YYY/ZZZ",
  method: "POST",
  headers: [{ key: "Content-Type", value: "application/json" }],
  body: '{"text": "New order: {{input.changed.id}}"}',
});

const sendDiscord = new FetchTask("discord", {
  url: "https://discord.com/api/webhooks/XXX/YYY",
  method: "POST",
  headers: [{ key: "Content-Type", value: "application/json" }],
  body: '{"content": "New order: {{input.changed.id}}"}',
});

const sendCustom = new FetchTask("custom", {
  url: process.env.CUSTOM_WEBHOOK_URL!,
  method: "POST",
  headers: [{ key: "Content-Type", value: "application/json" }],
  body: "{{JSON.stringify(input)}}",
});

const flow = new Flow("multi-webhook", [sendSlack, sendDiscord, sendCustom]);

// All tasks run in parallel (no connections)
flow.setTrigger(
  new EventTrigger({
    event: "mutator-insert-after",
    mode: "async",
  })
);
```

### Step 4: Webhook with Retry Logic

```typescript
import { Flow, FetchTask, Task, Condition, EventTrigger } from "bknd";
import { s } from "bknd/utils";

class RetryTask extends Task<typeof RetryTask.schema> {
  override type = "retry-webhook";

  static override schema = s.strictObject({
    url: s.string(),
    maxRetries: s.number({ default: 3 }),
    delayMs: s.number({ default: 1000 }),
  });

  override async execute(input: any) {
    let lastError: Error | null = null;

    for (let attempt = 1; attempt <= this.params.maxRetries; attempt++) {
      try {
        const response = await fetch(this.params.url, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(input),
        });

        if (response.ok) {
          return { success: true, attempt };
        }

        lastError = new Error(`HTTP ${response.status}`);
      } catch (err) {
        lastError = err as Error;
      }

      // Wait before retry (exponential backoff)
      if (attempt < this.params.maxRetries) {
        await new Promise((r) => setTimeout(r, this.params.delayMs * attempt));
      }
    }

    throw this.error("All retries failed", { lastError: lastError?.message });
  }
}
```

---

## Available Events

Bknd emits these events that can trigger webhooks:

### Data Events

| Event Slug | Description | Payload |
|------------|-------------|---------|
| `mutator-insert-before` | Before record created | `{ entity, data }` |
| `mutator-insert-after` | After record created | `{ entity, data, changed }` |
| `mutator-update-before` | Before record updated | `{ entity, entityId, data }` |
| `mutator-update-after` | After record updated | `{ entity, entityId, data, changed }` |
| `mutator-delete-before` | Before record deleted | `{ entity, entityId }` |
| `mutator-delete-after` | After record deleted | `{ entity, entityId, data }` |

### Media Events

| Event Slug | Description | Payload |
|------------|-------------|---------|
| `file-uploaded` | File uploaded | `{ name, meta, etag, file, state }` |
| `file-deleted` | File deleted | `{ name }` |
| `file-access` | File accessed | `{ name }` |

### Example: Using Event Payload

```typescript
// Event payload structure for mutator-insert-after
interface InsertAfterPayload {
  entity: {
    name: string;       // Entity name, e.g., "orders"
    fields: Field[];    // Entity fields
  };
  data: Record<string, any>;     // Original input data
  changed: Record<string, any>;  // Resulting record with ID
}

class ProcessEventTask extends Task {
  override async execute(input: InsertAfterPayload) {
    const entityName = input.entity.name;
    const recordId = input.changed.id;
    const recordData = input.changed;

    // Send webhook with structured data
    await fetch("https://api.example.com/webhook", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        event: `${entityName}.created`,
        timestamp: new Date().toISOString(),
        data: recordData,
      }),
    });

    return { sent: true };
  }
}
```

---

## Complete Example: Order Notification System

```typescript
import { App, em, entity, text, number, Flow, FetchTask, Task, EventTrigger, Condition } from "bknd";
import { s } from "bknd/utils";

// Schema
const schema = em({
  orders: entity({
    customer_email: text().required(),
    total: number().required(),
    status: text().default("pending"),
  }),
});

// Filter for orders only
class OrderFilterTask extends Task<typeof OrderFilterTask.schema> {
  override type = "order-filter";
  static override schema = s.strictObject({});

  override async execute(input: any) {
    if (input.entity?.name !== "orders") {
      throw this.error("Not an order");
    }
    return input.changed;  // Pass order data
  }
}

// Format webhook payload
class FormatWebhookTask extends Task<typeof FormatWebhookTask.schema> {
  override type = "format-webhook";
  static override schema = s.strictObject({});

  override async execute(order: any) {
    return {
      event: "order.created",
      timestamp: new Date().toISOString(),
      order: {
        id: order.id,
        email: order.customer_email,
        total: order.total,
        status: order.status,
      },
    };
  }
}

const filterTask = new OrderFilterTask("filter", {});
const formatTask = new FormatWebhookTask("format", {});

// Send to multiple destinations
const sendSlack = new FetchTask("slack", {
  url: process.env.SLACK_WEBHOOK_URL!,
  method: "POST",
  headers: [{ key: "Content-Type", value: "application/json" }],
  body: '{"text": "New order #{{input.order.id}} - ${{input.order.total}}"}',
});

const sendExternal = new FetchTask("external", {
  url: process.env.EXTERNAL_WEBHOOK_URL!,
  method: "POST",
  headers: [
    { key: "Content-Type", value: "application/json" },
    { key: "X-API-Key", value: process.env.EXTERNAL_API_KEY! },
  ],
  body: "{{JSON.stringify(input)}}",
});

// Build flow
const orderWebhookFlow = new Flow("order-notifications", [
  filterTask,
  formatTask,
  sendSlack,
  sendExternal,
]);

// Connect: filter -> format -> [slack, external] (parallel)
orderWebhookFlow.task(filterTask).asInputFor(formatTask);
orderWebhookFlow.task(formatTask).asInputFor(sendSlack);
orderWebhookFlow.task(formatTask).asInputFor(sendExternal);

// Trigger on new orders
orderWebhookFlow.setTrigger(
  new EventTrigger({
    event: "mutator-insert-after",
    mode: "async",
  })
);

const app = new App({
  data: { schema },
  flows: { flows: [orderWebhookFlow] },
});
```

---

## Testing Webhooks

### Test Incoming Webhook

```bash
# Basic test
curl -X POST http://localhost:7654/webhooks/external \
  -H "Content-Type: application/json" \
  -H "X-Event-Type: test" \
  -d '{"test": true}'

# With signature (HMAC-SHA256)
PAYLOAD='{"test":true}'
SECRET="your-secret"
SIGNATURE=$(echo -n "$PAYLOAD" | openssl dgst -sha256 -hmac "$SECRET" | cut -d' ' -f2)

curl -X POST http://localhost:7654/webhooks/secure \
  -H "Content-Type: application/json" \
  -H "X-Webhook-Signature: sha256=$SIGNATURE" \
  -d "$PAYLOAD"
```

### Test Outgoing Webhook

Use webhook.site or similar:

```typescript
// Temporarily point to test URL
const sendWebhook = new FetchTask("send", {
  url: "https://webhook.site/your-unique-id",
  method: "POST",
  body: "{{JSON.stringify(input)}}",
});
```

Then create a record:

```bash
curl -X POST http://localhost:7654/api/data/orders \
  -H "Content-Type: application/json" \
  -d '{"customer_email": "test@example.com", "total": 99.99}'
```

---

## Common Pitfalls

### Webhook Not Receiving Data

**Problem:** Incoming webhook returns 200 but doesn't process

**Fix:** Check mode - async returns immediately:

```typescript
// Async mode processes in background
new HttpTrigger({ mode: "async" });

// For debugging, use sync
new HttpTrigger({ mode: "sync" });
```

### Signature Verification Fails

**Problem:** Valid webhooks rejected

**Fix:** Ensure you're reading raw body before parsing:

```typescript
// WRONG - body already parsed
const body = await input.json();
const sig = verify(JSON.stringify(body), signature);

// CORRECT - read raw text first
const bodyText = await input.text();
const verified = verify(bodyText, signature);
const body = JSON.parse(bodyText);
```

### Outgoing Webhook Not Firing

**Problem:** EventTrigger flow doesn't run

**Fix:** Check event name matches exactly:

```typescript
// Available events (use exact slugs)
"mutator-insert-after"   // Not "data:entity:created"
"mutator-update-after"   // Not "data:entity:updated"
"mutator-delete-after"   // Not "data:entity:deleted"
```

### All Entities Trigger Webhook

**Problem:** Webhook fires for every entity, not just target

**Fix:** Add entity filter task:

```typescript
class EntityFilter extends Task {
  async execute(input) {
    if (input.entity?.name !== "orders") {
      throw this.error("Skip");  // Stops flow
    }
    return input;
  }
}
```

### FetchTask Body Not Interpolating

**Problem:** `{{input}}` appears literally in body

**Fix:** Use proper template syntax:

```typescript
// WRONG
body: "{ data: {{input}} }"

// CORRECT
body: "{{JSON.stringify({ data: input })}}"
```

---

## DOs and DON'Ts

**DO:**
- Use `mode: "async"` for incoming webhooks (return 200 fast)
- Verify signatures for security-sensitive webhooks
- Use entity filter tasks for targeted outgoing webhooks
- Implement retry logic for critical outgoing webhooks
- Log webhook events for debugging
- Use environment variables for webhook URLs and secrets

**DON'T:**
- Block on incoming webhooks (external services have timeouts)
- Trust incoming data without verification
- Hardcode webhook secrets in code
- Forget to handle webhook failures gracefully
- Send sensitive data in webhook payloads without encryption
- Expose webhook endpoints without rate limiting

---

## Related Skills

- **bknd-custom-endpoint** - Create custom API endpoints (HTTP triggers)
- **bknd-protect-endpoint** - Secure webhook endpoints
- **bknd-api-discovery** - Explore available endpoints
- **bknd-client-setup** - Call webhooks from frontend
