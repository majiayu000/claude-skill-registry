---
name: sentry-setup-tracing
description: Setup Sentry Tracing (Performance Monitoring) in any project. Use this when asked to add performance monitoring, enable tracing, track transactions/spans, or instrument application performance. Supports JavaScript, TypeScript, Python, Ruby, React, Next.js, and Node.js.
allowed-tools: Read, Edit, Write, Bash, Grep, Glob, AskUserQuestion
---

# SOURCE: getsentry/sentry-for-claude
# PATH: skills/sentry-setup-tracing/SKILL.md
# DO NOT EDIT: This file is synced from external source


# Setup Sentry Tracing

This skill helps configure Sentry's Tracing (Performance Monitoring) to track application performance, measure latency, and create distributed traces across services.

## When to Use This Skill

Invoke this skill when:
- User asks to "setup tracing" or "enable performance monitoring"
- User wants to "track transactions" or "measure latency"
- User requests "distributed tracing" or "span instrumentation"
- User mentions tracking API response times or page load performance
- User asks about `tracesSampleRate` or custom spans

## Platform Detection

Before configuring, detect the project's platform:

### JavaScript/TypeScript
Check `package.json` for:
- `@sentry/nextjs` - Next.js
- `@sentry/react` - React
- `@sentry/node` - Node.js
- `@sentry/browser` - Browser/vanilla JS
- `@sentry/vue` - Vue
- `@sentry/angular` - Angular
- `@sentry/sveltekit` - SvelteKit

### Python
Check for `sentry-sdk` in requirements

### Ruby
Check for `sentry-ruby` in Gemfile

---

## Core Concepts

Explain these concepts to the user:

| Concept | Description |
|---------|-------------|
| **Trace** | Complete journey of a request across services |
| **Transaction** | Single instance of a service being called (root span) |
| **Span** | Individual unit of work within a transaction |
| **Sample Rate** | Percentage of transactions to capture (0-1) |

---

## JavaScript/TypeScript Configuration

### Step 1: Locate Sentry Init

Find the `Sentry.init()` call:
- Next.js: `instrumentation-client.ts`, `sentry.server.config.ts`, `sentry.edge.config.ts`
- React: `src/index.tsx` or entry file
- Node.js: Entry point or config file
- Vue/Angular: Main app initialization

### Step 2: Enable Tracing

#### Browser/React - Add browserTracingIntegration

```javascript
import * as Sentry from "@sentry/react"; // or @sentry/browser

Sentry.init({
  dsn: "YOUR_DSN_HERE",

  // Add browser tracing integration
  integrations: [Sentry.browserTracingIntegration()],

  // Set sample rate (1.0 = 100% for testing, lower for production)
  tracesSampleRate: 1.0,

  // Configure which URLs receive trace headers for distributed tracing
  tracePropagationTargets: [
    "localhost",
    /^https:\/\/yourserver\.io\/api/,
  ],
});
```

#### Next.js - Configure All Init Files

**Client (`instrumentation-client.ts`):**
```typescript
import * as Sentry from "@sentry/nextjs";

Sentry.init({
  dsn: "YOUR_DSN_HERE",
  tracesSampleRate: 1.0,
  // Browser tracing is automatic in @sentry/nextjs
});
```

**Server (`sentry.server.config.ts`):**
```typescript
import * as Sentry from "@sentry/nextjs";

Sentry.init({
  dsn: "YOUR_DSN_HERE",
  tracesSampleRate: 1.0,
});
```

**Edge (`sentry.edge.config.ts`):**
```typescript
import * as Sentry from "@sentry/nextjs";

Sentry.init({
  dsn: "YOUR_DSN_HERE",
  tracesSampleRate: 1.0,
});
```

**Next.js 14+ App Router Requirement:**

For distributed tracing in App Router, add trace data to root layout metadata:

```typescript
// app/layout.tsx
import * as Sentry from "@sentry/nextjs";

export async function generateMetadata() {
  return {
    other: {
      ...Sentry.getTraceData(),
    },
  };
}
```

#### Node.js

```javascript
const Sentry = require("@sentry/node");

Sentry.init({
  dsn: "YOUR_DSN_HERE",
  tracesSampleRate: 1.0,
});
```

### Step 3: Configure Sampling

#### Option A: Uniform Sample Rate (Simple)

```javascript
Sentry.init({
  // Capture 20% of all transactions
  tracesSampleRate: 0.2,
});
```

#### Option B: Dynamic Sampling (Advanced)

```javascript
Sentry.init({
  tracesSampler: ({ name, attributes, parentSampled }) => {
    // Always skip health checks
    if (name.includes("healthcheck")) {
      return 0;
    }

    // Always capture auth transactions
    if (name.includes("auth")) {
      return 1;
    }

    // Sample comments at 1%
    if (name.includes("comment")) {
      return 0.01;
    }

    // Inherit parent sampling decision if available
    if (typeof parentSampled === "boolean") {
      return parentSampled;
    }

    // Default: 50%
    return 0.5;
  },
});
```

**Note:** If both `tracesSampleRate` and `tracesSampler` are set, `tracesSampler` takes precedence.

---

## Browser Tracing Integration Options

The `browserTracingIntegration()` accepts many configuration options:

```javascript
Sentry.init({
  integrations: [
    Sentry.browserTracingIntegration({
      // Trace propagation targets (which URLs get trace headers)
      tracePropagationTargets: ["localhost", /^https:\/\/api\./],

      // Modify spans before creation (e.g., parameterize URLs)
      beforeStartSpan: (context) => {
        return {
          ...context,
          name: context.name.replace(/\/users\/\d+/, "/users/:id"),
        };
      },

      // Filter unwanted spans
      shouldCreateSpanForRequest: (url) => {
        return !url.includes("healthcheck");
      },

      // Timing configurations
      idleTimeout: 1000,        // ms before finishing idle spans
      finalTimeout: 30000,      // max span duration
      childSpanTimeout: 15000,  // max child span duration

      // Feature toggles
      instrumentNavigation: true,  // Track URL changes
      instrumentPageLoad: true,    // Track initial page load
      enableLongTask: true,        // Track long tasks
      enableInp: true,             // Track Interaction to Next Paint

      // INP sampling (separate from tracesSampleRate)
      interactionsSampleRate: 1.0,
    }),
  ],
});
```

---

## Python Configuration

### Step 1: Enable Tracing

```python
import sentry_sdk

sentry_sdk.init(
    dsn="YOUR_DSN_HERE",
    traces_sample_rate=1.0,  # 100% for testing
)
```

### Step 2: Configure Sampling

#### Uniform Rate
```python
sentry_sdk.init(
    dsn="YOUR_DSN_HERE",
    traces_sample_rate=0.2,  # 20% of transactions
)
```

#### Dynamic Sampling
```python
def traces_sampler(sampling_context):
    transaction_name = sampling_context.get("transaction_context", {}).get("name", "")

    if "healthcheck" in transaction_name:
        return 0

    if "auth" in transaction_name:
        return 1.0

    # Inherit from parent if available
    if sampling_context.get("parent_sampled") is not None:
        return sampling_context["parent_sampled"]

    return 0.5

sentry_sdk.init(
    dsn="YOUR_DSN_HERE",
    traces_sampler=traces_sampler,
)
```

---

## Ruby Configuration

### Enable Tracing

```ruby
Sentry.init do |config|
  config.dsn = "YOUR_DSN_HERE"
  config.traces_sample_rate = 1.0  # 100% for testing
end
```

### Dynamic Sampling

```ruby
Sentry.init do |config|
  config.dsn = "YOUR_DSN_HERE"

  config.traces_sampler = lambda do |sampling_context|
    transaction_name = sampling_context[:transaction_context][:name]

    return 0 if transaction_name.include?("healthcheck")
    return 1.0 if transaction_name.include?("auth")

    0.5  # Default 50%
  end
end
```

---

## Custom Instrumentation

### JavaScript Custom Spans

#### Using startSpan (Recommended)

```javascript
// Synchronous operation
const result = Sentry.startSpan(
  { name: "expensive-calculation", op: "function" },
  () => {
    return calculateSomething();
  }
);

// Async operation
const result = await Sentry.startSpan(
  { name: "fetch-user-data", op: "http.client" },
  async () => {
    const response = await fetch("/api/user");
    return response.json();
  }
);

// With attributes
const result = await Sentry.startSpan(
  {
    name: "process-order",
    op: "task",
    attributes: {
      "order.id": orderId,
      "order.amount": amount,
    },
  },
  async () => {
    return processOrder(orderId);
  }
);
```

#### Nested Spans

```javascript
await Sentry.startSpan({ name: "checkout-flow", op: "transaction" }, async () => {
  // Child span 1
  await Sentry.startSpan({ name: "validate-cart", op: "validation" }, async () => {
    await validateCart();
  });

  // Child span 2
  await Sentry.startSpan({ name: "process-payment", op: "payment" }, async () => {
    await processPayment();
  });

  // Child span 3
  await Sentry.startSpan({ name: "send-confirmation", op: "email" }, async () => {
    await sendConfirmationEmail();
  });
});
```

#### Manual Span Control

```javascript
function middleware(req, res, next) {
  return Sentry.startSpanManual({ name: "middleware", op: "middleware" }, (span) => {
    res.once("finish", () => {
      span.setStatus({ code: res.statusCode < 400 ? 1 : 2 });
      span.end();
    });
    return next();
  });
}
```

#### Inactive Spans (Browser)

```javascript
let checkoutSpan;

// Start inactive span
function onStartCheckout() {
  checkoutSpan = Sentry.startInactiveSpan({ name: "checkout-flow" });
  Sentry.setActiveSpanInBrowser(checkoutSpan);
}

// End when done
function onCompleteCheckout() {
  checkoutSpan?.end();
}
```

### Python Custom Spans

#### Using Decorator (Simplest)

```python
import sentry_sdk

@sentry_sdk.trace
def expensive_function():
    # Automatically creates a span
    return do_work()

# With parameters (SDK 2.35.0+)
@sentry_sdk.trace(op="database", name="fetch-users")
def fetch_users():
    return db.query(User).all()
```

#### Using Context Manager

```python
import sentry_sdk

def process_order(order_id):
    with sentry_sdk.start_span(name="process-order", op="task") as span:
        span.set_data("order.id", order_id)

        # Nested span
        with sentry_sdk.start_span(name="validate-order", op="validation"):
            validate(order_id)

        with sentry_sdk.start_span(name="charge-payment", op="payment"):
            charge(order_id)

        return {"success": True}
```

#### Manual Transaction

```python
import sentry_sdk

with sentry_sdk.start_transaction(op="task", name="batch-process") as transaction:
    for item in items:
        with sentry_sdk.start_span(name=f"process-item-{item.id}"):
            process(item)

    transaction.set_tag("items_processed", len(items))
```

#### Centralized Configuration

```python
sentry_sdk.init(
    dsn="YOUR_DSN_HERE",
    traces_sample_rate=1.0,
    functions_to_trace=[
        {"qualified_name": "myapp.services.process_order"},
        {"qualified_name": "myapp.services.send_notification"},
    ],
)
```

---

## Distributed Tracing

### How It Works

Sentry propagates trace context via HTTP headers:
- `sentry-trace`: Contains trace ID, span ID, sampling decision
- `baggage`: Contains additional trace metadata

### Configure Trace Propagation Targets

Only URLs matching these patterns receive trace headers:

```javascript
Sentry.init({
  tracePropagationTargets: [
    "localhost",
    "https://api.yourapp.com",
    /^https:\/\/.*\.yourapp\.com\/api/,
  ],
});
```

### Server-Side Rendering (Meta Tags)

For SSR apps, inject trace data in HTML:

```javascript
// Server renders these meta tags
const traceData = Sentry.getTraceData();
// Include in HTML <head>:
// <meta name="sentry-trace" content="..." />
// <meta name="baggage" content="..." />
```

The browser SDK automatically reads these and continues the trace.

### Manual Propagation

For non-HTTP channels (WebSockets, message queues):

```javascript
// Sender
const traceData = Sentry.getTraceData();
sendMessage({
  ...payload,
  _traceHeaders: traceData,
});

// Receiver
Sentry.continueTrace(
  {
    sentryTrace: message._traceHeaders["sentry-trace"],
    baggage: message._traceHeaders["baggage"],
  },
  () => {
    processMessage(message);
  }
);
```

---

## Common Operation Types

Use consistent `op` values for better organization:

| Operation | Use Case |
|-----------|----------|
| `http.client` | Outgoing HTTP requests |
| `http.server` | Incoming HTTP requests |
| `db` | Database operations |
| `db.query` | Database queries |
| `cache` | Cache operations |
| `task` | Background tasks |
| `function` | Function execution |
| `ui.render` | UI rendering |
| `ui.action` | User interactions |
| `serialize` | Serialization |
| `middleware` | Middleware execution |

---

## What Gets Automatically Traced

### Browser (with browserTracingIntegration)
- Page loads
- Navigation/route changes
- XHR/fetch requests
- Long tasks
- Interaction to Next Paint (INP)

### Next.js
- API routes
- Server components
- Page renders
- Data fetching

### Node.js (with framework integrations)
- HTTP requests (Express, Fastify, etc.)
- Database queries (with ORM integrations)
- External API calls

### Python (with framework integrations)
- Django views, middleware, templates
- Flask routes
- FastAPI endpoints
- SQLAlchemy queries
- Celery tasks

---

## Disabling Tracing

**Important:** Setting `tracesSampleRate: 0` does NOT disable tracing - it still processes traces but never sends them.

To fully disable tracing, omit both sampling options:

```javascript
Sentry.init({
  dsn: "YOUR_DSN_HERE",
  // Do NOT include tracesSampleRate or tracesSampler
});
```

---

## Production Sampling Recommendations

| Traffic Level | Recommended Rate |
|---------------|-----------------|
| Development/Testing | `1.0` (100%) |
| Low traffic (<1K req/min) | `0.5` - `1.0` |
| Medium traffic (1K-10K req/min) | `0.1` - `0.5` |
| High traffic (>10K req/min) | `0.01` - `0.1` |

Use dynamic sampling to capture more of important transactions:

```javascript
tracesSampler: ({ name }) => {
  // Always capture errors and slow endpoints
  if (name.includes("checkout") || name.includes("payment")) {
    return 1.0;
  }
  // Sample most at 10%
  return 0.1;
},
```

---

## Verification Steps

After setup, verify tracing is working:

### JavaScript
```javascript
// Trigger a test transaction
await Sentry.startSpan(
  { name: "test-transaction", op: "test" },
  async () => {
    console.log("Tracing test");
    await new Promise(resolve => setTimeout(resolve, 100));
  }
);
```

### Python
```python
with sentry_sdk.start_transaction(op="test", name="test-transaction"):
    print("Tracing test")
```

**Check in Sentry:**
1. Go to **Performance** section
2. Look for your test transaction
3. Verify spans appear in the trace waterfall

---

## Common Issues and Solutions

### Issue: Transactions not appearing
**Solutions:**
1. Verify `tracesSampleRate > 0` or `tracesSampler` returns > 0
2. Check DSN is correct
3. For browser: Ensure `browserTracingIntegration()` is added
4. Wait a few minutes for data to process

### Issue: Distributed traces not connected
**Solutions:**
1. Check `tracePropagationTargets` includes your API URLs
2. Verify CORS allows `sentry-trace` and `baggage` headers
3. For SSR: Ensure trace meta tags are rendered

### Issue: Too many transactions (high volume)
**Solutions:**
1. Lower `tracesSampleRate`
2. Use `tracesSampler` to filter by transaction name
3. Use `shouldCreateSpanForRequest` to skip health checks

### Issue: Spans not nested correctly
**Solutions:**
1. Ensure parent span is still active when creating child
2. Use `startSpan` callback pattern (not manual)
3. For browser: Consider `parentSpanIsAlwaysRootSpan: false`

---

## Summary Checklist

```markdown
## Sentry Tracing Setup Complete

### Configuration Applied:
- [ ] `tracesSampleRate` or `tracesSampler` configured
- [ ] Browser: `browserTracingIntegration()` added
- [ ] `tracePropagationTargets` configured for APIs
- [ ] Next.js App Router: `getTraceData()` in metadata

### Sampling Strategy:
- [ ] Development: 100% sampling for testing
- [ ] Production: Appropriate rate based on traffic

### Custom Instrumentation (if applicable):
- [ ] Critical paths instrumented with custom spans
- [ ] Consistent `op` values used

### Next Steps:
1. Trigger some requests in your application
2. Check Sentry > Performance for transactions
3. Review trace waterfalls for span hierarchy
4. Adjust sampling rates based on volume
```

---

## Quick Reference

| Platform | Enable Tracing | Custom Span |
|----------|---------------|-------------|
| JS/Browser | `tracesSampleRate` + `browserTracingIntegration()` | `Sentry.startSpan()` |
| Next.js | `tracesSampleRate` (auto-integrated) | `Sentry.startSpan()` |
| Node.js | `tracesSampleRate` | `Sentry.startSpan()` |
| Python | `traces_sample_rate` | `@sentry_sdk.trace` or `start_span()` |
| Ruby | `traces_sample_rate` | `start_span()` |

| Sampling Option | Purpose |
|-----------------|---------|
| `tracesSampleRate` | Uniform percentage (0-1) |
| `tracesSampler` | Dynamic function (takes precedence) |
