---
name: integrating-stripe-webhooks
description: Use when implementing Stripe webhook endpoints and getting 'Raw body not available' or signature verification errors - provides raw body parsing solutions and subscription period field fixes across frameworks
---

# Integrating Stripe Webhooks

## Overview

Stripe webhooks require raw request bodies for signature verification. Most web frameworks parse JSON automatically, breaking verification. This skill provides framework-specific solutions for the raw body problem and documents common TypeScript type mismatches.

## When to Use

**Use this skill when:**
- Getting "Raw body not available" errors from Stripe webhooks
- Webhook signature verification fails with 400 errors
- Implementing new Stripe webhook endpoints
- Getting `TypeError: Cannot read property 'current_period_start'` from subscription events
- Webhooks return 404 (route registration issues)

**Don't use for:**
- General Stripe API integration (not webhooks)
- Frontend Stripe Elements implementation
- Stripe checkout session creation (use Stripe docs)

## Quick Reference

| Problem | Solution |
|---------|----------|
| Raw body not available | Configure custom body parser (see framework examples) |
| Signature verification fails | Use raw body bytes/buffer, not parsed JSON |
| 404 on webhook endpoint | Register webhook route inside API prefix |
| `current_period_start` undefined | Access from `subscription.items.data[0]` not root |
| URI validation errors | URL-encode dynamic parameters with `encodeURIComponent()` |

## Critical: Raw Body Parsing

**THE PROBLEM:** Stripe's `constructEvent()` requires the exact bytes received to verify the signature. JSON parsing modifies the body, breaking verification.

**THE SOLUTION:** Access raw body before any parsing middleware.

### Framework Examples

**Node.js - Fastify** (most common for new projects):

```typescript
// In main server file, BEFORE registering routes
server.addContentTypeParser('application/json',
  { parseAs: 'buffer' },
  async (req: any, body: Buffer) => {
    req.rawBody = body;  // Store for webhooks
    return JSON.parse(body.toString('utf8'));  // Parse for other routes
  }
);

// In webhook handler
const rawBody = (request as any).rawBody;
const event = stripe.webhooks.constructEvent(
  rawBody, signature, webhookSecret
);
```

**Node.js - Express**:

```javascript
// Define webhook route BEFORE express.json() middleware
app.post('/webhooks/stripe',
  express.raw({ type: 'application/json' }),
  (req, res) => {
    const event = stripe.webhooks.constructEvent(
      req.body,  // Already raw Buffer
      req.headers['stripe-signature'],
      webhookSecret
    );
  }
);

app.use(express.json());  // After webhook route
```

**Python - FastAPI**:

```python
@app.post('/webhooks/stripe')
async def stripe_webhook(request: Request):
    payload = await request.body()  # Use .body() not .json()
    signature = request.headers.get('stripe-signature')

    event = stripe.Webhook.construct_event(
        payload, signature, webhook_secret
    )
```

**General Pattern:** Get raw bytes/buffer → verify signature → use parsed event from Stripe.

## Common Mistakes

### 1. Subscription Period Fields Missing

**Error:** `TypeError: Cannot read property 'current_period_start' of undefined`

**Cause:** Stripe returns period dates in `subscription.items.data[0]`, not at subscription root. TypeScript types don't include these fields on `SubscriptionItem`.

**Fix:**
```typescript
// ❌ WRONG - fields don't exist here
new Date(subscription.current_period_start * 1000)

// ✅ CORRECT - get from first subscription item
const firstItem = subscription.items.data[0] as any;
const periodStart = firstItem?.current_period_start || subscription.billing_cycle_anchor;
const periodEnd = firstItem?.current_period_end || subscription.billing_cycle_anchor;

await updateOrg({
  start_date: new Date(periodStart * 1000),
  end_date: new Date(periodEnd * 1000),
});
```

### 2. Route Not Found (404)

**Cause:** Webhook routes registered outside API prefix.

```typescript
// ❌ WRONG - creates /webhooks/stripe instead of /api/v1/webhooks/stripe
export async function registerRoutes(server) {
  server.register(async (api) => {
    await api.register(subscriptionRoutes, { prefix: '/subscriptions' });
  }, { prefix: '/api/v1' });

  await server.register(webhookRoutes, { prefix: '/webhooks' });  // Outside!
}

// ✅ CORRECT - inside API prefix
export async function registerRoutes(server) {
  server.register(async (api) => {
    await api.register(subscriptionRoutes, { prefix: '/subscriptions' });
    await api.register(webhookRoutes, { prefix: '/webhooks' });  // Inside
  }, { prefix: '/api/v1' });
}
```

### 3. URL Encoding in Checkout URLs

**Error:** `"body/successUrl must match format 'uri'"`

**Cause:** Organization names or parameters with spaces not URL-encoded.

```typescript
// ❌ WRONG - "Broke Org" creates invalid URL
const successUrl = `${origin}/orgs?name=${orgName}&subscription=success`;

// ✅ CORRECT - encode dynamic parameters
const successUrl = `${origin}/orgs?name=${encodeURIComponent(orgName)}&subscription=success`;
```

## Implementation Checklist

**Server Setup:**
- [ ] Configure raw body parser BEFORE routes
- [ ] Register webhook routes inside API prefix (if using one)
- [ ] Set `STRIPE_WEBHOOK_SECRET` environment variable
- [ ] Verify webhook secret is configured before processing

**Webhook Handler:**
- [ ] Validate `stripe-signature` header exists
- [ ] Access raw body (not parsed JSON)
- [ ] Use `stripe.webhooks.constructEvent()` for verification
- [ ] Handle `SignatureVerificationError` separately
- [ ] Return 200 for received events (even if processing fails)
- [ ] Log all events with ID and type

**Subscription Events:**
- [ ] Get period dates from `subscription.items.data[0]`
- [ ] Cast to `any` to access TypeScript-missing fields
- [ ] Fallback to `billing_cycle_anchor` if items missing
- [ ] Store `org_id` in subscription metadata
- [ ] Update verification status based on subscription status

**Frontend:**
- [ ] URL-encode all dynamic parameters
- [ ] URL-encode organization names in success/cancel URLs
- [ ] Handle checkout errors gracefully
- [ ] Poll for verification after checkout success

## Testing Locally

```bash
# Install Stripe CLI
brew install stripe/stripe-cli/stripe

# Forward webhooks to local server
stripe listen --forward-to localhost:3000/api/v1/webhooks/stripe

# Trigger test events
stripe trigger customer.subscription.created
stripe trigger customer.subscription.updated
stripe trigger invoice.paid
```

## Real-World Impact

**Before applying these patterns:**
- Webhooks fail with 400 "Invalid signature"
- Subscription updates crash with undefined property errors
- Hours debugging TypeScript type mismatches
- Checkout fails with URL validation errors

**After applying:**
- Webhooks verify successfully
- Subscription data extracts correctly
- Type-safe with explicit casting
- Checkout URLs work with any organization name

## References

- [Stripe Webhook Signature Verification](https://stripe.com/docs/webhooks/signatures)
- [Stripe Subscription Object](https://stripe.com/docs/api/subscriptions/object)
- See framework documentation for body parsing middleware
