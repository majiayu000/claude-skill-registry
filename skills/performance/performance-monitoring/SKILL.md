---
name: sentry-performance-monitoring
description: Use when setting up performance monitoring, distributed tracing, or profiling with Sentry. Covers transactions, spans, and performance insights.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
---

# Sentry - Performance Monitoring

Track application performance with transactions, spans, and distributed tracing.

## Enable Performance Monitoring

```typescript
import * as Sentry from "@sentry/browser";

Sentry.init({
  dsn: "...",
  tracesSampleRate: 0.2, // 20% of transactions
  integrations: [
    Sentry.browserTracingIntegration(),
  ],
});
```

## Transactions

### Automatic Transactions

```typescript
// Browser: Page loads and navigations
Sentry.init({
  integrations: [
    Sentry.browserTracingIntegration({
      tracePropagationTargets: ["localhost", /^https:\/\/api\.example\.com/],
    }),
  ],
});
```

### Manual Transactions

```typescript
const transaction = Sentry.startTransaction({
  op: "task",
  name: "Process Order",
});

try {
  // Your code here
  processOrder(order);
  transaction.setStatus("ok");
} catch (error) {
  transaction.setStatus("internal_error");
  throw error;
} finally {
  transaction.finish();
}
```

## Spans

### Create Child Spans

```typescript
const transaction = Sentry.startTransaction({ name: "checkout" });

const validationSpan = transaction.startChild({
  op: "validation",
  description: "Validate cart items",
});
await validateCart(cart);
validationSpan.finish();

const paymentSpan = transaction.startChild({
  op: "payment",
  description: "Process payment",
});
await processPayment(payment);
paymentSpan.finish();

transaction.finish();
```

### Span Data

```typescript
const span = transaction.startChild({
  op: "db.query",
  description: "SELECT * FROM users WHERE id = ?",
  data: {
    "db.system": "postgresql",
    "db.name": "production",
  },
});
```

## Distributed Tracing

### Propagate Trace Context

```typescript
// Frontend
Sentry.init({
  integrations: [
    Sentry.browserTracingIntegration({
      tracePropagationTargets: [
        "localhost",
        /^https:\/\/api\.yoursite\.com/,
      ],
    }),
  ],
});

// This automatically adds sentry-trace and baggage headers
```

### Backend Continuation

```typescript
// Express.js
import * as Sentry from "@sentry/node";

app.use(Sentry.Handlers.requestHandler());
app.use(Sentry.Handlers.tracingHandler());

// The transaction is automatically continued from incoming headers
```

## Sampling

### Static Sampling

```typescript
Sentry.init({
  tracesSampleRate: 0.1, // 10% of transactions
});
```

### Dynamic Sampling

```typescript
Sentry.init({
  tracesSampler: (samplingContext) => {
    // Always sample errors
    if (samplingContext.parentSampled !== undefined) {
      return samplingContext.parentSampled;
    }

    // High priority endpoints
    if (samplingContext.name.includes("/checkout")) {
      return 1.0;
    }

    // Don't sample health checks
    if (samplingContext.name.includes("/health")) {
      return 0;
    }

    // Default rate
    return 0.1;
  },
});
```

## Web Vitals

```typescript
// Automatically captured with browserTracingIntegration
// LCP, FID, CLS, FCP, TTFB

Sentry.init({
  integrations: [
    Sentry.browserTracingIntegration({
      enableLongTask: true, // Track long tasks
    }),
  ],
});
```

## Custom Metrics

```typescript
// Capture custom metrics
Sentry.metrics.increment("button_clicked", 1, {
  tags: { button: "checkout" },
});

Sentry.metrics.distribution("cart_value", cart.total, {
  unit: "dollar",
  tags: { currency: "USD" },
});

Sentry.metrics.gauge("active_users", activeCount);

Sentry.metrics.set("unique_visitors", visitorId);
```

## Profiling

```typescript
// Node.js
import * as Sentry from "@sentry/node";
import { nodeProfilingIntegration } from "@sentry/profiling-node";

Sentry.init({
  dsn: "...",
  integrations: [nodeProfilingIntegration()],
  tracesSampleRate: 1.0,
  profilesSampleRate: 1.0,
});
```

## Best Practices

1. Start with low sample rates, increase as needed
2. Use dynamic sampling for important transactions
3. Propagate trace context to all services
4. Add meaningful span descriptions
5. Track business-critical user flows
6. Use custom metrics for business KPIs
7. Enable profiling for performance-critical code
