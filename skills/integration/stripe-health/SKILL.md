---
name: stripe-health
description: "Stripe webhook health diagnostics. Invoke for: webhook delivery failures, pending_webhooks issues, redirect problems (307/308), subscription sync failures, pre-deployment webhook verification, incident investigation involving Stripe."
---

# /stripe-health - Stripe Webhook Health Check

Run a comprehensive diagnostic on Stripe webhook integration.

## When to Use

- Before deploying changes to webhook handlers
- When subscription sync issues are reported
- After configuring new webhook endpoints
- As part of incident investigation

## Diagnostic Steps

### 1. Check Webhook Endpoints

```bash
# List all webhook endpoints for this project
stripe webhook_endpoints list --api-key "$STRIPE_SECRET_KEY" 2>&1 | jq '.data[] | {id, url, status, enabled_events}'
```

**Red flags:**
- Multiple endpoints for same URL (duplicate signing secrets)
- Status != "enabled"
- Missing critical events (checkout.session.completed, customer.subscription.*)

### 2. Check for Redirects (CRITICAL)

```bash
# Get the webhook URL from endpoints, then check for redirects
WEBHOOK_URL=$(stripe webhook_endpoints list --api-key "$STRIPE_SECRET_KEY" 2>&1 | jq -r '.data[0].url')
echo "Testing: $WEBHOOK_URL"
curl -s -I -X POST "$WEBHOOK_URL" 2>&1 | head -5
```

**Red flags:**
- HTTP 307/308/301/302 = REDIRECT = Stripe won't deliver webhooks
- Must return 4xx or 5xx, NOT 3xx

### 3. Check Recent Event Delivery

```bash
# Check last 5 events and their pending_webhooks count
stripe events list --limit 5 --api-key "$STRIPE_SECRET_KEY" 2>&1 | jq '.data[] | {id, type, created: (.created | todate), pending_webhooks}'
```

**Red flags:**
- pending_webhooks > 0 for old events = delivery failing
- pending_webhooks should decrease over time

### 4. Check for Failed Deliveries

```bash
# Look for events with high pending_webhooks (failures)
stripe events list --limit 20 --api-key "$STRIPE_SECRET_KEY" 2>&1 | jq '[.data[] | select(.pending_webhooks > 0)] | length'
```

**Red flags:**
- More than 2-3 events with pending_webhooks > 0

### 5. Test Live Delivery

```bash
# Resend a recent event and watch logs
RECENT_EVENT=$(stripe events list --limit 1 --type checkout.session.completed --api-key "$STRIPE_SECRET_KEY" 2>&1 | jq -r '.data[0].id')
ENDPOINT_ID=$(stripe webhook_endpoints list --api-key "$STRIPE_SECRET_KEY" 2>&1 | jq -r '.data[0].id')

echo "Resending $RECENT_EVENT to $ENDPOINT_ID..."
stripe events resend "$RECENT_EVENT" --webhook-endpoint "$ENDPOINT_ID" --api-key "$STRIPE_SECRET_KEY"

echo ""
echo "Watch Vercel logs for delivery confirmation..."
echo "Run: vercel logs your-app --json | grep webhook"
```

## Health Report Format

```
STRIPE WEBHOOK HEALTH CHECK
===========================
Endpoints: [count] configured
  - [url] (status: [enabled/disabled])

Redirect Check: [PASS/FAIL]
  - [url] returns [status code]

Recent Delivery: [PASS/WARN/FAIL]
  - [X] events with pending_webhooks > 0

Recommendation: [action if any issues found]
```

## Common Issues & Fixes

| Symptom | Likely Cause | Fix |
|---------|--------------|-----|
| pending_webhooks stays high | Redirect or wrong URL | `curl -I` the URL, update to canonical domain |
| Duplicate endpoints | Created endpoint twice | Delete older one, keep one with matching secret |
| Events not appearing | Wrong events enabled | Update endpoint to include required events |
| Signature verification fails | Wrong secret in env | Get secret from Stripe dashboard, update env |
