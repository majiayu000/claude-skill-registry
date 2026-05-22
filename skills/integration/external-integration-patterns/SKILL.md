---
name: external-integration-patterns
user-invocable: false
description: "Patterns for reliable external service integration: env validation, health checks, error handling, observability. Invoke when integrating Stripe, Clerk, Sendgrid, or any external API."
---

# External Integration Patterns

Patterns for reliable external service integration.

## Triggers

Invoke this skill when:
- File path contains `webhook`, `api/`, `services/`
- Code imports external service SDKs (stripe, @clerk, @sendgrid, etc.)
- Env vars reference external services
- Implementing any third-party API integration
- Reviewing webhook handlers

## Core Principle

> External services fail. Your integration must be observable, recoverable, and fail loudly.

Silent failures are the worst failures. When Stripe doesn't deliver a webhook, when Clerk JWT validation fails, when Sendgrid rejects an email — you need to know immediately, not when a user complains.

## Required Patterns

### 1. Fail-Fast Env Validation

Validate environment variables at module load, not at runtime. Fail immediately with a clear message.

```typescript
// At module load, NOT inside a function
const REQUIRED = ['SERVICE_API_KEY', 'SERVICE_WEBHOOK_SECRET'];

for (const key of REQUIRED) {
  const value = process.env[key];
  if (!value) {
    throw new Error(`Missing required env var: ${key}`);
  }
  if (value !== value.trim()) {
    throw new Error(`${key} has trailing whitespace — check dashboard for invisible characters`);
  }
}

// Now safe to use
export const apiKey = process.env.SERVICE_API_KEY!;
```

**Why this matters:**
- Deploy fails immediately if config is wrong
- Error message tells you exactly what's missing
- No silent failures at 3am when a customer tries to checkout

### 2. Health Check Endpoint

Every external service should have a health check endpoint.

```typescript
// /api/health/route.ts or /api/health/[service]/route.ts
export async function GET() {
  const checks: Record<string, { ok: boolean; latency?: number; error?: string }> = {};

  // Check Stripe
  try {
    const start = Date.now();
    await stripe.balance.retrieve();
    checks.stripe = { ok: true, latency: Date.now() - start };
  } catch (e) {
    checks.stripe = { ok: false, error: e.message };
  }

  // Check database
  try {
    const start = Date.now();
    await db.query.users.findFirst();
    checks.database = { ok: true, latency: Date.now() - start };
  } catch (e) {
    checks.database = { ok: false, error: e.message };
  }

  const healthy = Object.values(checks).every(c => c.ok);

  return Response.json({
    status: healthy ? 'ok' : 'degraded',
    checks,
    timestamp: new Date().toISOString()
  }, { status: healthy ? 200 : 503 });
}
```

### 3. Structured Error Logging

Log every external service failure with full context.

```typescript
catch (error) {
  // Structured JSON for log aggregation
  console.error(JSON.stringify({
    level: 'error',
    service: 'stripe',
    operation: 'createCheckout',
    userId: user.id,
    input: { priceId, mode }, // Safe subset of input
    error: error.message,
    code: error.code || 'unknown',
    timestamp: new Date().toISOString()
  }));
  throw error;
}
```

**Required fields:**
- `service`: Which external service (stripe, clerk, sendgrid)
- `operation`: What you were trying to do
- `userId`: Who this affects (for debugging)
- `error`: The error message
- `timestamp`: When it happened

### 4. Webhook Reliability

Webhooks are inherently unreliable. Build for this reality.

```typescript
export async function handleWebhook(req: Request) {
  const body = await req.text();
  const sig = req.headers.get('stripe-signature')!;

  // 1. Verify signature FIRST (before any processing)
  let event: Stripe.Event;
  try {
    event = stripe.webhooks.constructEvent(body, sig, process.env.STRIPE_WEBHOOK_SECRET!);
  } catch (e) {
    console.error(JSON.stringify({
      level: 'error',
      source: 'webhook',
      service: 'stripe',
      error: 'Signature verification failed',
      message: e.message
    }));
    return new Response('Invalid signature', { status: 400 });
  }

  // 2. Log event received BEFORE processing
  console.log(JSON.stringify({
    level: 'info',
    source: 'webhook',
    service: 'stripe',
    eventType: event.type,
    eventId: event.id,
    timestamp: new Date().toISOString()
  }));

  // 3. Store event for reconciliation (optional but recommended)
  await db.insert(webhookEvents).values({
    provider: 'stripe',
    eventId: event.id,
    eventType: event.type,
    payload: event,
    processedAt: null
  });

  // 4. Return 200 quickly, process async if slow
  // (Stripe retries if response takes too long)
  await processEvent(event);

  return new Response('OK', { status: 200 });
}
```

### 5. Reconciliation Cron (Safety Net)

Don't rely 100% on webhooks. Periodically sync state as a backup.

```typescript
// Run hourly or daily
export async function reconcileSubscriptions() {
  const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!);

  // Fetch active subscriptions modified in last 24h
  const subs = await stripe.subscriptions.list({
    status: 'active',
    created: { gte: Math.floor(Date.now() / 1000) - 86400 }
  });

  for (const sub of subs.data) {
    // Update local state to match Stripe
    await db.update(subscriptions)
      .set({ status: sub.status, currentPeriodEnd: sub.current_period_end })
      .where(eq(subscriptions.stripeId, sub.id));
  }

  console.log(JSON.stringify({
    level: 'info',
    operation: 'reconcileSubscriptions',
    synced: subs.data.length,
    timestamp: new Date().toISOString()
  }));
}
```

### 6. Pull-on-Success Activation

Don't wait for webhook to grant access. Verify payment immediately after redirect.

```typescript
// /checkout/success/page.tsx
export default async function SuccessPage({ searchParams }) {
  const sessionId = searchParams.session_id;

  // Don't trust the URL alone — verify with Stripe
  const session = await stripe.checkout.sessions.retrieve(sessionId);

  if (session.payment_status === 'paid') {
    // Grant access immediately
    await grantAccess(session.customer);
  }

  // Webhook will come later as backup
  return <SuccessMessage />;
}
```

## Pre-Deploy Checklist

Before deploying any external integration:

### Environment Variables
- [ ] All required vars in `.env.example`
- [ ] Vars set on **both** dev and prod deployments
- [ ] No trailing whitespace (use `printf`, not `echo`)
- [ ] Format validated (sk_*, whsec_*, pk_*)

### Webhook Configuration
- [ ] Webhook URL uses canonical domain (no redirects)
- [ ] Secret matches between service dashboard and env vars
- [ ] Signature verification in handler
- [ ] Events logged before processing

### Observability
- [ ] Health check endpoint exists
- [ ] Error paths log with context
- [ ] Monitoring/alerting configured

### Reliability
- [ ] Reconciliation cron or pull-on-success pattern
- [ ] Idempotency for duplicate events
- [ ] Graceful handling of service downtime

## Quick Verification Script

```bash
#!/bin/bash
# scripts/verify-external-integration.sh

SERVICE=$1
echo "Checking $SERVICE integration..."

# Check env vars
for var in ${SERVICE}_API_KEY ${SERVICE}_WEBHOOK_SECRET; do
  if [ -z "${!var}" ]; then
    echo "❌ Missing $var"
    exit 1
  fi
  if [ "${!var}" != "$(echo "${!var}" | tr -d '\n')" ]; then
    echo "❌ $var has trailing newline"
    exit 1
  fi
done

# Check health endpoint
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3000/api/health)
if [ "$HTTP_CODE" != "200" ]; then
  echo "❌ Health check failed (HTTP $HTTP_CODE)"
  exit 1
fi

echo "✅ $SERVICE integration checks passed"
```

## Anti-Patterns to Avoid

```typescript
// ❌ BAD: Silent failure on missing config
const apiKey = process.env.API_KEY || '';

// ❌ BAD: No context in error log
catch (e) { console.log('Error'); throw e; }

// ❌ BAD: Trusting webhook without verification
const event = JSON.parse(body); // No signature check!

// ❌ BAD: 100% reliance on webhooks
// If webhook fails, user never gets access

// ❌ BAD: No logging of received events
// Debugging nightmare when things go wrong
```

## Service-Specific Notes

### Stripe
- Use `stripe.webhooks.constructEvent()` for signature verification
- Check Stripe Dashboard > Developers > Webhooks for delivery logs
- `customer_creation` param only valid in `payment`/`setup` mode

### Clerk
- `CONVEX_WEBHOOK_TOKEN` must match exactly between Clerk and Convex
- JWT template names are case-sensitive
- Webhook URL must not redirect

### Sendgrid
- Verify sender domain before going live
- Inbound parse webhooks need signature verification
- Rate limits apply — implement queuing for bulk sends
