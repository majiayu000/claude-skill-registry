---
name: wide-event-observability
description: Design and implement wide-event logging with tail sampling for context-rich, queryable observability
when_to_use: When designing logging/observability systems, debugging production incidents with inadequate context, or replacing scattered log statements with canonical log lines
---

# Wide-Event Logging & Observability

You are an observability architect implementing **wide events / canonical log lines** with **tail sampling** to transform logging from "grep text files" to "query structured events with business context."

## Core Philosophy (from loggingsucks.com)

**Traditional logging is broken** because:
1. **Optimized for writing, not querying** - scattered log statements create noise, not insight
2. **Missing business context** - logs lack user tier, feature flags, cart value, account age
3. **String search inadequacy** - grep can't correlate events across services or understand relationships
4. **Multi-search debugging nightmare** - requires multiple searches to understand one request

**The Solution**: Emit **ONE comprehensive event per request per service** containing:
- Technical metadata (timestamps, IDs, duration)
- Business context (user subscription, cart value, feature flags)
- Error details when applicable
- Complete request context in a single queryable event

## Wide Event Structure

```typescript
interface WideEvent {
  // Correlation & Identity
  timestamp: string;           // ISO 8601
  request_id: string;          // Correlation across services
  trace_id?: string;           // Distributed tracing
  span_id?: string;

  // Service Context
  service: string;             // "checkout-api"
  version: string;             // "2.1.0"
  deployment_id: string;       // "deploy_abc123"
  region: string;              // "us-east-1"

  // Request Details
  method: string;              // "POST"
  path: string;                // "/api/checkout"
  status_code: number;         // 200
  duration_ms: number;         // 245
  outcome: 'success' | 'error';

  // Business Context (HIGH VALUE)
  user: {
    id: string;
    subscription: 'free' | 'premium' | 'enterprise';
    account_age_days: number;
    lifetime_value_cents: number;
  };

  // Feature Flags (for rollout debugging)
  feature_flags: {
    new_checkout_flow?: boolean;
    beta_payment_ui?: boolean;
  };

  // Domain-Specific Context
  cart?: {
    total_cents: number;
    item_count: number;
    currency: string;
  };

  payment?: {
    provider: 'stripe' | 'paypal';
    method: 'card' | 'bank';
    latency_ms: number;
    attempt: number;
  };

  // Error Details (when applicable)
  error?: {
    type: string;              // "PaymentDeclinedError"
    code: string;              // "card_declined"
    message: string;
    retriable: boolean;
    provider_code?: string;    // Stripe/PayPal specific
  };
}
```

## Tail Sampling Strategy

**Sampling decision happens AFTER request completes:**

```typescript
function shouldSample(event: WideEvent): boolean {
  // ALWAYS keep errors (100%)
  if (event.status_code >= 500) return true;
  if (event.error) return true;

  // ALWAYS keep slow requests (tune threshold to your p99)
  if (event.duration_ms > 2000) return true;

  // ALWAYS keep VIPs / important cohorts
  if (event.user?.subscription === 'enterprise') return true;
  if (event.user?.lifetime_value_cents > 10000_00) return true;

  // ALWAYS keep feature-flagged traffic (for rollout debugging)
  if (event.feature_flags?.new_checkout_flow) return true;

  // Randomly sample the rest (1-5%)
  return Math.random() < 0.05;
}
```

**Why this works:**
- Keep 100% of the signal (errors, slow requests, VIPs, rollouts)
- Sample the noise (successful fast requests from regular users)
- Massive cost savings while retaining debugging power

## Implementation Rules

### Rule 1: One Wide Event Per Request

Replace "diary logs" with a **request-scoped event builder** that accumulates context during handling and emits **once in `finally`**.

**❌ BAD: Scattered logs**
```typescript
app.post('/checkout', async (req, res) => {
  logger.info('Checkout started');
  logger.info(`User: ${req.user.id}`);

  const cart = await getCart(req.user.id);
  logger.info(`Cart total: ${cart.total}`);

  try {
    const payment = await processPayment(cart);
    logger.info(`Payment successful: ${payment.id}`);
    res.json({ ok: true });
  } catch (err) {
    logger.error(`Payment failed: ${err.message}`);
    throw err;
  }
});
```

**✅ GOOD: Wide event**
```typescript
app.post('/checkout', async (req, res) => {
  const event = req.wideEvent; // Request-scoped builder

  const cart = await getCart(req.user.id);
  event.cart = {
    total_cents: cart.total,
    item_count: cart.items.length,
    currency: cart.currency
  };

  try {
    const paymentStart = Date.now();
    const payment = await processPayment(cart);

    event.payment = {
      provider: payment.provider,
      latency_ms: Date.now() - paymentStart,
      attempt: payment.attempt
    };

    res.json({ ok: true });
  } catch (err: any) {
    event.error = {
      type: err.name,
      code: err.code,
      message: err.message,
      retriable: err.retriable
    };
    throw err;
  }
  // Event emitted automatically in middleware's res.on('finish')
});
```

### Rule 2: Log What Happened to the Request

Do **not** log internal step-by-step narration unless absolutely required. The wide event is the authoritative record.

**Exception**: Infrastructure-level events (service startup, shutdown, health checks) can still be separate structured logs.

### Rule 3: OpenTelemetry Doesn't Add Context For You

If using OTel tracing, **enrich spans/events** with business fields explicitly:

```typescript
import { trace } from '@opentelemetry/api';

const span = trace.getActiveSpan();
if (span) {
  span.setAttributes({
    'user.subscription': user.subscription,
    'user.account_age_days': user.accountAgeDays,
    'feature_flags.new_checkout_flow': flags.newCheckoutFlow,
    'cart.total_cents': cart.totalCents
  });
}
```

**OTel is a delivery mechanism, not a decision-maker.** You must instrument business context deliberately.

### Rule 4: Schema Discipline

Define a stable schema (even if flexible) and normalize keys:

**❌ BAD: Inconsistent keys**
```typescript
{ userId: '123' }          // One endpoint
{ user_id: '123' }         // Another endpoint
{ id: '123' }              // Yet another
```

**✅ GOOD: Consistent schema**
```typescript
{
  user: {
    id: '123',
    subscription: 'premium',
    account_age_days: 730
  }
}
```

Use a TypeScript interface or JSON Schema to enforce consistency.

### Rule 5: Security/PII

**Never log:**
- Raw secrets (tokens, passwords, API keys)
- Credit card numbers, SSNs, passwords
- Full request bodies for sensitive endpoints

**Prefer:**
- Hashed/opaque identifiers where possible
- Redaction layer for known sensitive keys
- User ID instead of email/name

```typescript
function redactSensitive(event: WideEvent): WideEvent {
  const redacted = { ...event };

  // Remove sensitive fields
  delete redacted.password;
  delete redacted.creditCard;
  delete redacted.ssn;

  // Hash PII if needed
  if (redacted.email) {
    redacted.email_hash = hashEmail(redacted.email);
    delete redacted.email;
  }

  return redacted;
}
```

## Implementation Guide: Express/Node.js

### Step 1: Wide Event Middleware

```typescript
// observability/wideEvent.ts
import type { Request, Response, NextFunction } from 'express';
import crypto from 'crypto';

export interface WideEvent {
  timestamp: string;
  request_id: string;
  trace_id?: string;
  service: string;
  version: string;
  deployment_id: string;
  region: string;
  method: string;
  path: string;
  status_code?: number;
  duration_ms?: number;
  outcome?: 'success' | 'error';
  user?: {
    id: string;
    subscription: string;
    account_age_days: number;
    lifetime_value_cents: number;
  };
  feature_flags?: Record<string, boolean>;
  error?: {
    type: string;
    code: string;
    message: string;
    retriable: boolean;
  };
  [key: string]: any;
}

function getOrCreateRequestId(req: Request): string {
  const existing = req.header('x-request-id');
  return existing ?? crypto.randomUUID();
}

export function wideEventMiddleware(
  logger: { info: (obj: any, msg?: string) => void }
) {
  return function (req: Request, res: Response, next: NextFunction) {
    const start = Date.now();
    const request_id = getOrCreateRequestId(req);

    // Build initial event
    const event: WideEvent = {
      timestamp: new Date().toISOString(),
      request_id,
      service: process.env.SERVICE_NAME || 'unknown',
      version: process.env.SERVICE_VERSION || '0.0.0',
      deployment_id: process.env.DEPLOYMENT_ID || 'local',
      region: process.env.REGION || 'local',
      method: req.method,
      path: req.path,
    };

    // Attach to request for handlers to enrich
    (req as any).wideEvent = event;

    // Include request id in response headers
    res.setHeader('x-request-id', request_id);

    // Emit event when response finishes
    res.on('finish', () => {
      event.status_code = res.statusCode;
      event.duration_ms = Date.now() - start;
      event.outcome = res.statusCode >= 500 ? 'error' : 'success';

      // Tail sampling decision
      if (shouldSample(event)) {
        logger.info(event, 'request_complete');
      }
    });

    next();
  };
}

function shouldSample(event: WideEvent): boolean {
  // Always keep errors
  if (event.status_code && event.status_code >= 500) return true;
  if (event.error) return true;

  // Always keep slow requests (tune to your p99)
  if (event.duration_ms && event.duration_ms > 2000) return true;

  // Always keep VIPs
  if (event.user?.subscription === 'enterprise') return true;
  if (event.user?.lifetime_value_cents && event.user.lifetime_value_cents > 10000_00) return true;

  // Always keep feature-flagged traffic
  if (event.feature_flags && Object.keys(event.feature_flags).length > 0) return true;

  // Sample the rest (5%)
  return Math.random() < 0.05;
}
```

### Step 2: Enrich in Route Handlers

```typescript
import express from 'express';

const app = express();

app.use(wideEventMiddleware(logger));

app.post('/api/checkout', async (req, res) => {
  const event = (req as any).wideEvent;

  // Add user context
  const user = req.user; // From auth middleware
  event.user = {
    id: user.id,
    subscription: user.subscription,
    account_age_days: daysSince(user.createdAt),
    lifetime_value_cents: user.lifetimeValueCents,
  };

  // Add feature flags
  event.feature_flags = req.featureFlags; // From feature flag middleware

  // Add business context
  const cart = await getCart(user.id);
  event.cart = {
    total_cents: cart.totalCents,
    item_count: cart.items.length,
    currency: cart.currency,
  };

  try {
    const paymentStart = Date.now();
    const payment = await processPayment(cart, user);

    event.payment = {
      provider: payment.provider,
      method: payment.method,
      latency_ms: Date.now() - paymentStart,
      attempt: payment.attempt,
    };

    res.json({ ok: true, orderId: payment.orderId });
  } catch (err: any) {
    event.error = {
      type: err.name,
      code: err.code || 'unknown',
      message: err.message,
      retriable: err.retriable ?? false,
      provider_code: err.providerCode,
    };

    res.status(err.statusCode || 500).json({
      error: err.code,
      message: err.message,
    });
  }
});
```

### Step 3: Logger Configuration

```typescript
import pino from 'pino';

const logger = pino({
  level: process.env.LOG_LEVEL || 'info',
  formatters: {
    level: (label) => ({ level: label }),
  },
  redact: {
    paths: [
      'password',
      'creditCard',
      'ssn',
      'authToken',
      'apiKey',
      'authorization',
      'cookie',
    ],
    remove: true,
  },
  // Send to stdout for CloudWatch/Datadog ingestion
  transport: process.env.NODE_ENV === 'development'
    ? { target: 'pino-pretty' }
    : undefined,
});

export default logger;
```

## Implementation Guide: React/Frontend

### Goal on the Client

Use the same philosophy: **emit fewer, better events** with business context.

```typescript
// observability/clientLogger.ts
interface ClientWideEvent {
  timestamp: string;
  session_id: string;
  user_id?: string;
  route: string;
  build_version: string;

  // Correlate with backend
  request_id?: string;

  // Device/Network context
  device: {
    type: 'mobile' | 'tablet' | 'desktop';
    os: string;
    browser: string;
  };

  network: {
    effectiveType: string; // 4g, 3g, etc.
    downlink?: number;
  };

  // Feature flags
  feature_flags?: Record<string, boolean>;

  // Error details
  error?: {
    type: string;
    message: string;
    stack?: string;
    componentStack?: string;
  };

  // Business context
  action?: string; // "checkout_submit", "payment_attempt"
  outcome?: 'success' | 'error';
  duration_ms?: number;
}

class ClientLogger {
  private sessionId: string;

  constructor() {
    this.sessionId = this.getOrCreateSessionId();
    this.setupErrorHandlers();
  }

  private getOrCreateSessionId(): string {
    let sessionId = sessionStorage.getItem('session_id');
    if (!sessionId) {
      sessionId = crypto.randomUUID();
      sessionStorage.setItem('session_id', sessionId);
    }
    return sessionId;
  }

  private setupErrorHandlers() {
    // Unhandled errors
    window.addEventListener('error', (event) => {
      this.logError({
        type: 'UnhandledError',
        message: event.message,
        stack: event.error?.stack,
      });
    });

    // Unhandled promise rejections
    window.addEventListener('unhandledrejection', (event) => {
      this.logError({
        type: 'UnhandledRejection',
        message: String(event.reason),
      });
    });
  }

  logEvent(event: Partial<ClientWideEvent>) {
    const fullEvent: ClientWideEvent = {
      timestamp: new Date().toISOString(),
      session_id: this.sessionId,
      user_id: this.getUserId(),
      route: window.location.pathname,
      build_version: process.env.REACT_APP_VERSION || 'unknown',
      device: this.getDeviceContext(),
      network: this.getNetworkContext(),
      feature_flags: this.getFeatureFlags(),
      ...event,
    };

    // Send to backend or observability service
    this.send(fullEvent);
  }

  logError(error: { type: string; message: string; stack?: string }) {
    this.logEvent({
      error,
      outcome: 'error',
    });
  }

  private getUserId(): string | undefined {
    // Get from auth context
    return window.__USER_ID__;
  }

  private getDeviceContext() {
    const ua = navigator.userAgent;
    return {
      type: this.detectDeviceType(ua),
      os: this.detectOS(ua),
      browser: this.detectBrowser(ua),
    };
  }

  private getNetworkContext() {
    const connection = (navigator as any).connection;
    return {
      effectiveType: connection?.effectiveType || 'unknown',
      downlink: connection?.downlink,
    };
  }

  private getFeatureFlags(): Record<string, boolean> {
    return window.__FEATURE_FLAGS__ || {};
  }

  private send(event: ClientWideEvent) {
    // Send to backend or observability service
    if (navigator.sendBeacon) {
      navigator.sendBeacon('/api/events', JSON.stringify(event));
    } else {
      fetch('/api/events', {
        method: 'POST',
        body: JSON.stringify(event),
        headers: { 'Content-Type': 'application/json' },
      }).catch(() => {
        // Ignore errors in logging
      });
    }
  }
}

export const clientLogger = new ClientLogger();
```

### React Error Boundary

```typescript
import React from 'react';
import { clientLogger } from './observability/clientLogger';

class ErrorBoundary extends React.Component<
  { children: React.ReactNode },
  { hasError: boolean }
> {
  constructor(props: any) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError() {
    return { hasError: true };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    clientLogger.logError({
      type: 'ReactError',
      message: error.message,
      stack: error.stack,
      componentStack: errorInfo.componentStack,
    });
  }

  render() {
    if (this.state.hasError) {
      return <div>Something went wrong. Please refresh the page.</div>;
    }
    return this.props.children;
  }
}
```

### Log Business Actions

```typescript
function CheckoutButton({ cart }: { cart: Cart }) {
  const handleCheckout = async () => {
    const start = Date.now();

    try {
      const response = await fetch('/api/checkout', {
        method: 'POST',
        body: JSON.stringify(cart),
      });

      const requestId = response.headers.get('x-request-id');

      if (!response.ok) {
        throw new Error('Checkout failed');
      }

      clientLogger.logEvent({
        action: 'checkout_submit',
        outcome: 'success',
        duration_ms: Date.now() - start,
        request_id: requestId,
        cart: {
          total_cents: cart.totalCents,
          item_count: cart.items.length,
        },
      });
    } catch (error: any) {
      clientLogger.logEvent({
        action: 'checkout_submit',
        outcome: 'error',
        duration_ms: Date.now() - start,
        error: {
          type: error.name,
          message: error.message,
        },
      });
    }
  };

  return <button onClick={handleCheckout}>Checkout</button>;
}
```

## Query Examples (Proving the Value)

These demonstrate the shift from grep → analytics on structured events.

### Query 1: Checkout Failures for Premium Users with Feature Flag

```sql
-- CloudWatch Insights / DataDog / Elastic
SELECT
  error.code,
  COUNT(*) as count,
  AVG(duration_ms) as avg_duration
FROM events
WHERE
  path = '/api/checkout'
  AND outcome = 'error'
  AND user.subscription = 'premium'
  AND feature_flags.new_checkout_flow = true
  AND timestamp > NOW() - INTERVAL '1 hour'
GROUP BY error.code
ORDER BY count DESC
```

**Before wide events:** Multiple searches across logs, manual correlation, no way to filter by feature flag.

**After wide events:** Single query with all context.

### Query 2: Payment Latency by Provider and Region

```sql
SELECT
  payment.provider,
  region,
  PERCENTILE(payment.latency_ms, 95) as p95,
  PERCENTILE(payment.latency_ms, 99) as p99
FROM events
WHERE
  path = '/api/checkout'
  AND payment.provider IS NOT NULL
  AND timestamp > NOW() - INTERVAL '24 hours'
GROUP BY payment.provider, region
```

**Insight:** Identify if Stripe is slower in eu-west-1 than us-east-1.

### Query 3: Feature Flag Rollout Impact

```sql
SELECT
  feature_flags.new_checkout_flow as has_flag,
  AVG(duration_ms) as avg_duration,
  SUM(CASE WHEN error IS NOT NULL THEN 1 ELSE 0 END) / COUNT(*) as error_rate
FROM events
WHERE
  path = '/api/checkout'
  AND timestamp > NOW() - INTERVAL '1 hour'
GROUP BY has_flag
```

**Insight:** Compare error rate and latency between flag enabled vs disabled cohorts.

### Query 4: High-Value User Checkout Journey

```sql
SELECT *
FROM events
WHERE
  request_id = 'req_abc123'
ORDER BY timestamp
```

**Insight:** See complete request journey across all services with one query using request_id.

## Migration Strategy

### Phase 1: Add Wide Event Middleware (Week 1)

1. Add wide event middleware to main HTTP server
2. Emit basic technical metadata (method, path, status, duration)
3. Keep existing logs (dual logging)
4. Verify events in logs

### Phase 2: Enrich with Business Context (Week 2-3)

1. Add user context (subscription, tier, LTV)
2. Add feature flags
3. Add domain-specific context (cart, payment, order)
4. Document schema

### Phase 3: Implement Tail Sampling (Week 4)

1. Add sampling logic (keep errors, slow requests, VIPs)
2. Monitor sampling rates
3. Adjust thresholds

### Phase 4: Remove Scattered Logs (Week 5-6)

1. Remove redundant log statements
2. Keep only wide events
3. Update runbooks to use new queries

## Success Metrics

Track these to measure improvement:

1. **Mean Time to Resolution (MTTR)**: Should decrease as debugging becomes faster
2. **Log Volume**: Should decrease 80-90% with tail sampling
3. **Query Complexity**: Shift from multi-step grep to single structured queries
4. **Context Completeness**: % of events with business context fields populated

## Common Pitfalls

### Pitfall 1: "We already use structured logging"

**Response**: Structured logging (JSON) is necessary but not sufficient. You must also:
- Emit ONE event per request (not many)
- Include business context (not just technical)
- Use tail sampling (not log everything)

### Pitfall 2: "OpenTelemetry will handle this"

**Response**: OTel is a delivery mechanism. It doesn't decide:
- What business context to capture
- When to sample
- What fields to include

You must instrument business context explicitly.

### Pitfall 3: "We'll add context later"

**Response**: Context must be captured at the moment it's available:
- User subscription tier at auth time
- Cart value when cart is loaded
- Feature flags when flags are evaluated

Adding context retroactively is impossible.

### Pitfall 4: "Sampling will lose important data"

**Response**: Tail sampling keeps 100% of:
- Errors
- Slow requests
- VIPs
- Feature-flagged traffic

You only sample the noise (successful fast requests from regular users).

## Definition of Done

Do not complete until:

- [ ] ONE canonical wide event emitted per request for main HTTP layer
- [ ] Events include consistent correlation IDs (request_id, trace_id)
- [ ] Events include stable field names with documented schema
- [ ] Handlers enrich events with business context (tier, flags, cart/order IDs)
- [ ] Tail sampling implemented with "keep errors/slow/VIPs/flagged" rules
- [ ] Sensitive fields redacted; secrets never logged
- [ ] At least 3 example queries documented demonstrating debugging wins
- [ ] Migration plan documented with phases and rollback strategy
- [ ] Team trained on querying wide events (not grepping logs)

## References

- [Logging Sucks](https://loggingsucks.com/) - Original philosophy
- [OpenTelemetry](https://opentelemetry.io/) - Delivery mechanism (not decision-maker)
- [Structured Logging Best Practices](https://www.structlog.org/)
- [Tail-Based Sampling](https://opentelemetry.io/docs/concepts/sampling/)
