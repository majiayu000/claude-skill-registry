---
name: inngest-events
description: Design and send Inngest events. Covers event schema and payload format, naming conventions, IDs for idempotency, the ts param, fan-out patterns, and system events like inngest/function.failed.
---

# Inngest Events

Master Inngest event design and delivery patterns. Events are the foundation of Inngest - learn to design robust event schemas, implement idempotency, leverage fan-out patterns, and handle system events effectively.

> **These skills are focused on TypeScript.** For Python or Go, refer to the [Inngest documentation](https://www.inngest.com/llms.txt) for language-specific guidance. Core concepts apply across all languages.

## Event Payload Format

Every Inngest event is a JSON object with required and optional properties:

### Required Properties

```typescript
type Event = {
  name: string; // Event type (triggers functions)
  data: object; // Payload data (any nested JSON)
};
```

### Complete Schema

```typescript
type EventPayload = {
  name: string; // Required: event type
  data: Record<string, any>; // Required: event data
  id?: string; // Optional: deduplication ID
  ts?: number; // Optional: timestamp (Unix ms)
  v?: string; // Optional: schema version
};
```

### Basic Event Example

```typescript
await inngest.send({
  name: "billing/invoice.paid",
  data: {
    customerId: "cus_NffrFeUfNV2Hib",
    invoiceId: "in_1J5g2n2eZvKYlo2C0Z1Z2Z3Z",
    userId: "user_03028hf09j2d02",
    amount: 1000,
    metadata: {
      accountId: "acct_1J5g2n2eZvKYlo2C0Z1Z2Z3Z",
      accountName: "Acme.ai"
    }
  }
});
```

## Event Naming Conventions

**Use the Object-Action pattern:** `domain/noun.verb`

### Recommended Patterns

```typescript
// ✅ Good: Clear object-action pattern
"billing/invoice.paid";
"user/profile.updated";
"order/item.shipped";
"ai/summary.completed";

// ✅ Good: Domain prefixes for organization
"stripe/customer.created";
"intercom/conversation.assigned";
"slack/message.posted";

// ❌ Avoid: Unclear or inconsistent
"payment"; // What happened?
"user_update"; // Use dots, not underscores
"invoiceWasPaid"; // Too verbose
```

### Naming Guidelines

- **Past tense:** Events describe what happened (`created`, `updated`, `failed`)
- **Dot notation:** Use dots for hierarchy (`billing/invoice.paid`)
- **Prefixes:** Group related events (`api/user.created`, `webhook/stripe.received`)
- **Consistency:** Establish patterns and stick to them

## Event IDs and Idempotency

**When to use IDs:** Prevent duplicate processing when events might be sent multiple times.

### Basic Deduplication

```typescript
await inngest.send({
  id: "cart-checkout-completed-ed12c8bde", // Unique per event type
  name: "storefront/cart.checkout.completed",
  data: {
    cartId: "ed12c8bde",
    items: ["item1", "item2"]
  }
});
```

### ID Best Practices

```typescript
// ✅ Good: Specific to event type and instance
id: `invoice-paid-${invoiceId}`;
id: `user-signup-${userId}-${timestamp}`;
id: `order-shipped-${orderId}-${trackingNumber}`;

// ❌ Bad: Generic IDs shared across event types
id: invoiceId; // Could conflict with other events
id: "user-action"; // Too generic
id: customerId; // Same customer, different events
```

**Deduplication window:** 24 hours from first event reception

See **inngest-durable-functions** for idempotency configuration.

## The `ts` Parameter for Delayed Delivery

**When to use:** Schedule events for future processing or maintain event ordering.

### Future Scheduling

```typescript
const oneHourFromNow = Date.now() + 60 * 60 * 1000;

await inngest.send({
  name: "trial/reminder.send",
  ts: oneHourFromNow, // Deliver in 1 hour
  data: {
    userId: "user_123",
    trialExpiresAt: "2024-02-15T12:00:00Z"
  }
});
```

### Maintaining Event Order

```typescript
// Events with timestamps are processed in chronological order
const events = [
  {
    name: "user/action.performed",
    ts: 1640995200000, // Earlier
    data: { action: "login" }
  },
  {
    name: "user/action.performed",
    ts: 1640995260000, // Later
    data: { action: "purchase" }
  }
];

await inngest.send(events);
```

## Fan-Out Patterns

**Use case:** One event triggers multiple independent functions for reliability and parallel processing.

### Basic Fan-Out Implementation

```typescript
// Send single event
await inngest.send({
  name: "user/signup.completed",
  data: {
    userId: "user_123",
    email: "user@example.com",
    plan: "pro"
  }
});

// Multiple functions respond to same event
const sendWelcomeEmail = inngest.createFunction(
  { id: "send-welcome-email" },
  { event: "user/signup.completed" },
  async ({ event, step }) => {
    await step.run("send-email", async () => {
      return sendEmail({
        to: event.data.email,
        template: "welcome"
      });
    });
  }
);

const createTrialSubscription = inngest.createFunction(
  { id: "create-trial" },
  { event: "user/signup.completed" },
  async ({ event, step }) => {
    await step.run("create-subscription", async () => {
      return stripe.subscriptions.create({
        customer: event.data.stripeCustomerId,
        trial_period_days: 14
      });
    });
  }
);

const addToCrm = inngest.createFunction(
  { id: "add-to-crm" },
  { event: "user/signup.completed" },
  async ({ event, step }) => {
    await step.run("crm-sync", async () => {
      return crm.contacts.create({
        email: event.data.email,
        plan: event.data.plan
      });
    });
  }
);
```

### Fan-Out Benefits

- **Independence:** Functions run separately; one failure doesn't affect others
- **Parallel execution:** All functions run simultaneously
- **Selective replay:** Re-run only failed functions
- **Cross-service:** Trigger functions in different codebases/languages

### Advanced Fan-Out with `waitForEvent`

In expressions, `event` = the **original** triggering event, `async` = the **new** event being matched. See [Expression Syntax Reference](../references/expressions.md) for full details.

```typescript
const orchestrateOnboarding = inngest.createFunction(
  { id: "orchestrate-onboarding" },
  { event: "user/signup.completed" },
  async ({ event, step }) => {
    // Fan out to multiple services
    await step.sendEvent("fan-out", [
      { name: "email/welcome.send", data: event.data },
      { name: "subscription/trial.create", data: event.data },
      { name: "crm/contact.add", data: event.data }
    ]);

    // Wait for all to complete
    const [emailResult, subResult, crmResult] = await Promise.all([
      step.waitForEvent("email-sent", {
        event: "email/welcome.sent",
        timeout: "5m",
        if: `event.data.userId == async.data.userId`
      }),
      step.waitForEvent("subscription-created", {
        event: "subscription/trial.created",
        timeout: "5m",
        if: `event.data.userId == async.data.userId`
      }),
      step.waitForEvent("crm-synced", {
        event: "crm/contact.added",
        timeout: "5m",
        if: `event.data.userId == async.data.userId`
      })
    ]);

    // Complete onboarding
    await step.run("complete-onboarding", async () => {
      return completeUserOnboarding(event.data.userId);
    });
  }
);
```

See **inngest-steps** for additional patterns including `step.invoke`.

## System Events

Inngest emits system events for function lifecycle monitoring:

### Available System Events

```typescript
// Function execution events
"inngest/function.failed"; // Function failed after retries
"inngest/function.finished"; // Function finished - completed or failed
"inngest/function.cancelled"; // Function cancelled before completion
```

### Handling Failed Functions

```typescript
const handleFailures = inngest.createFunction(
  { id: "handle-failed-functions" },
  { event: "inngest/function.failed" },
  async ({ event, step }) => {
    const { function_id, run_id, error } = event.data;

    await step.run("log-failure", async () => {
      logger.error("Function failed", {
        functionId: function_id,
        runId: run_id,
        error: error.message,
        stack: error.stack
      });
    });

    // Alert on critical function failures
    if (function_id.includes("critical")) {
      await step.run("send-alert", async () => {
        return alerting.sendAlert({
          title: `Critical function failed: ${function_id}`,
          severity: "high",
          runId: run_id
        });
      });
    }

    // Auto-retry certain failures
    if (error.code === "RATE_LIMIT_EXCEEDED") {
      await step.run("schedule-retry", async () => {
        return inngest.send({
          name: "retry/function.requested",
          ts: Date.now() + 5 * 60 * 1000, // Retry in 5 minutes
          data: { originalRunId: run_id }
        });
      });
    }
  }
);
```

## Sending Events

### Client Setup

```typescript
// inngest/client.ts
import { Inngest } from "inngest";

export const inngest = new Inngest({
  id: "my-app"
});
// You must set INNGEST_EVENT_KEY environment variable in production
```

### Single Event

```typescript
const result = await inngest.send({
  name: "order/placed",
  data: {
    orderId: "ord_123",
    customerId: "cus_456",
    amount: 2500,
    items: [
      { id: "item_1", quantity: 2 },
      { id: "item_2", quantity: 1 }
    ]
  }
});

// Returns event IDs for tracking
console.log(result.ids); // ["01HQ8PTAESBZPBDS8JTRZZYY3S"]
```

### Batch Events

```typescript
const orderItems = await getOrderItems(orderId);

// Convert to events
const events = orderItems.map((item) => ({
  name: "inventory/item.reserved",
  data: {
    itemId: item.id,
    orderId: orderId,
    quantity: item.quantity,
    warehouseId: item.warehouseId
  }
}));

// Send all at once (up to 512kb)
await inngest.send(events);
```

### Sending from Functions

```typescript
inngest.createFunction(
  { id: "process-order" },
  { event: "order/placed" },
  async ({ event, step }) => {
    // Use step.sendEvent() instead of inngest.send() in functions
    // for reliability and deduplication
    await step.sendEvent("trigger-fulfillment", {
      name: "fulfillment/order.received",
      data: {
        orderId: event.data.orderId,
        priority: event.data.customerTier === "premium" ? "high" : "normal"
      }
    });
  }
);
```

## Event Design Best Practices

### Schema Versioning

```typescript
// Use version field to track schema changes
await inngest.send({
  name: "user/profile.updated",
  v: "2024-01-15.1", // Schema version
  data: {
    userId: "user_123",
    changes: {
      email: "new@example.com",
      preferences: { theme: "dark" }
    },
    // New field in v2 schema
    auditInfo: {
      changedBy: "user_456",
      reason: "user_requested"
    }
  }
});
```

### Rich Context Data

```typescript
// Include enough context for all consumers
await inngest.send({
  name: "payment/charge.succeeded",
  data: {
    // Primary identifiers
    chargeId: "ch_123",
    customerId: "cus_456",

    // Amount details
    amount: 2500,
    currency: "usd",

    // Context for different consumers
    subscription: {
      id: "sub_789",
      plan: "pro_monthly"
    },
    invoice: {
      id: "inv_012",
      number: "INV-2024-001"
    },

    // Metadata for debugging
    paymentMethod: {
      type: "card",
      last4: "4242",
      brand: "visa"
    },
    metadata: {
      source: "stripe_webhook",
      environment: "production"
    }
  }
});
```

**Event design principles:**

1. **Self-contained:** Include all data consumers need
2. **Immutable:** Never modify event schemas after sending
3. **Traceable:** Include correlation IDs and audit trails
4. **Actionable:** Provide enough context for business logic
5. **Debuggable:** Include metadata for troubleshooting
