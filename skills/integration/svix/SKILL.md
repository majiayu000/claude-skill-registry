---
name: svix
description: >-
  You are an expert in Svix, the enterprise webhook delivery platform. You
  help developers send reliable webhooks to customers with automatic retries,
  signature verification, delivery monitoring, endpoint management, and event
  type filtering — replacing custom webhook infrastructure with a
  purpose-built service used by companies like Clerk, Resend, and Liveblocks.
license: Apache-2.0
compatibility: ''
metadata:
  author: terminal-skills
  version: 1.0.0
  category: Backend Development
  tags:
    - webhooks
    - api
    - delivery
    - retry
    - typescript
    - infrastructure
---

# Svix — Webhook Delivery Infrastructure

You are an expert in Svix, the enterprise webhook delivery platform. You help developers send reliable webhooks to customers with automatic retries, signature verification, delivery monitoring, endpoint management, and event type filtering — replacing custom webhook infrastructure with a purpose-built service used by companies like Clerk, Resend, and Liveblocks.

## Core Capabilities

### Sending Webhooks

```typescript
import { Svix } from "svix";

const svix = new Svix(process.env.SVIX_API_KEY!);

// Register an application (your customer/tenant)
await svix.application.create({
  uid: "customer-42",
  name: "Acme Corp",
});

// Send webhook event
await svix.message.create("customer-42", {
  eventType: "order.created",
  payload: {
    id: "ord-123",
    total: 99.99,
    items: [{ sku: "WIDGET-A", qty: 2 }],
    createdAt: new Date().toISOString(),
  },
});

// Customer adds their endpoint via your dashboard/API
await svix.endpoint.create("customer-42", {
  url: "https://customer-webhook.example.com/webhooks",
  filterTypes: ["order.created", "order.shipped", "order.refunded"],
  channels: ["orders"],
  rateLimit: 100,                         // Max 100 deliveries/sec to this endpoint
});

// Batch send
await Promise.all(
  customers.map(customerId =>
    svix.message.create(customerId, {
      eventType: "invoice.generated",
      payload: { invoiceId: "inv-456", amount: 299.99 },
    })
  )
);
```

### Webhook Verification (Consumer Side)

```typescript
import { Webhook } from "svix";

// Verify incoming webhooks in your API
app.post("/webhooks", (req, res) => {
  const wh = new Webhook(process.env.SVIX_SIGNING_SECRET!);

  try {
    const payload = wh.verify(req.body, {
      "svix-id": req.headers["svix-id"],
      "svix-timestamp": req.headers["svix-timestamp"],
      "svix-signature": req.headers["svix-signature"],
    });
    // payload is verified and safe to process
    handleWebhookEvent(payload);
    res.status(200).json({ received: true });
  } catch (err) {
    res.status(400).json({ error: "Invalid signature" });
  }
});
```

### Consumer Portal

```typescript
// Generate a magic link for customers to manage their endpoints
const dashboard = await svix.authentication.appPortalAccess("customer-42", {});
// dashboard.url → "https://app.svix.com/login#key=..." 
// Customer can view delivery logs, manage endpoints, retry failed deliveries
```

## Installation

```bash
npm install svix
```

## Best Practices

1. **Event types** — Define clear event types (`order.created`, `invoice.paid`); customers filter what they receive
2. **Signature verification** — Always verify webhook signatures; Svix uses HMAC-SHA256 with timestamp replay protection
3. **Idempotency** — Include unique event IDs in payload; consumers should handle duplicate deliveries
4. **Retry policy** — Svix auto-retries with exponential backoff (up to 3 days); failed deliveries are logged
5. **Consumer portal** — Give customers the Svix App Portal; self-service endpoint management, delivery logs
6. **Rate limiting** — Set per-endpoint rate limits; protect customer servers from webhook storms
7. **Event catalog** — Document all event types and payload schemas; publish as part of your API docs
8. **Self-hosted** — Svix is open-source; deploy on your own infra for data sovereignty
