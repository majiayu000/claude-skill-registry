---
name: stripe-agent
description: Manages all Stripe billing operations for Unite-Hub including product/price creation, subscription management, checkout sessions, webhooks, and dual-mode (test/live) billing for staff vs. customer ...
---

# Stripe Agent Skill

**Agent ID**: `unite-hub.stripe-agent`
**Model**: `claude-sonnet-4-5-20250929`
**MCP Server**: `stripe` (via `@stripe/mcp`)

---

## Role

Manages all Stripe billing operations for Unite-Hub including product/price creation, subscription management, checkout sessions, webhooks, and dual-mode (test/live) billing for staff vs. customer separation.

---

## Capabilities

### 1. Product & Price Management

**Create Products**
```typescript
// Create a product for a pricing tier
mcp__stripe__create_product({
  name: "Unite Hub Professional",
  description: "Full CRM and AI marketing automation",
  metadata: {
    tier: "professional",
    features: "unlimited_contacts,ai_scoring,drip_campaigns"
  }
})
```

**Create Prices**
```typescript
// Monthly price (AUD, GST included)
mcp__stripe__create_price({
  product: "prod_xxx",
  unit_amount: 89500, // $895.00 AUD in cents
  currency: "aud",
  recurring: { interval: "month" },
  metadata: { tier: "professional", billing: "monthly", gst_included: "true" }
})

// Annual price (AUD, GST included)
mcp__stripe__create_price({
  product: "prod_xxx",
  unit_amount: 895000, // $8,950.00 AUD (2 months free)
  currency: "aud",
  recurring: { interval: "year" },
  metadata: { tier: "professional", billing: "annual", gst_included: "true" }
})
```

### 2. Checkout Sessions

**Create Checkout Session**
```typescript
mcp__stripe__create_checkout_session({
  mode: "subscription",
  customer_email: "customer@example.com",
  line_items: [{
    price: "price_xxx",
    quantity: 1
  }],
  success_url: "https://synthex.social/dashboard?success=true",
  cancel_url: "https://synthex.social/pricing?cancelled=true",
  metadata: {
    workspace_id: "uuid",
    tier: "professional"
  }
})
```

### 3. Subscription Management

**List Subscriptions**
```typescript
mcp__stripe__list_subscriptions({
  customer: "cus_xxx",
  status: "active"
})
```

**Update Subscription** (upgrade/downgrade)
```typescript
// Via API route, update subscription items
// Switch from starter to professional price
```

**Cancel Subscription**
```typescript
// Via API route with proper handling
// Options: immediate or at_period_end
```

### 4. Customer Management

**Create Customer**
```typescript
mcp__stripe__create_customer({
  email: "new@customer.com",
  name: "John Doe",
  metadata: {
    user_id: "uuid",
    workspace_id: "uuid"
  }
})
```

**List Customers**
```typescript
mcp__stripe__list_customers({
  email: "customer@example.com"
})
```

### 5. Invoice Management

**List Invoices**
```typescript
mcp__stripe__list_invoices({
  customer: "cus_xxx",
  status: "paid"
})
```

**Create Invoice**
```typescript
mcp__stripe__create_invoice({
  customer: "cus_xxx",
  auto_advance: true,
  metadata: {
    workspace_id: "uuid"
  }
})
```

---

## Dual-Mode Billing Architecture

Unite-Hub uses a dual-mode billing system to separate staff testing from real customer payments.

### Mode Determination Logic

```typescript
// From src/lib/billing/stripe-router.ts

// TEST Mode triggers:
// 1. Staff roles: founder, staff_admin, internal_team, super_admin
// 2. Registered sandbox emails (SANDBOX_STAFF_REGISTRY)
// 3. Internal domains: unite-group.in, disasterrecoveryqld.au, carsi.com.au

// LIVE Mode:
// All other users (real customers)
```

### Environment Variables Required

```env
# TEST Mode (for staff/internal)
STRIPE_TEST_SECRET_KEY=sk_test_...
STRIPE_TEST_WEBHOOK_SECRET=whsec_test_...
STRIPE_TEST_PRICE_STARTER=price_...
STRIPE_TEST_PRICE_PRO=price_...
STRIPE_TEST_PRICE_ELITE=price_...
NEXT_PUBLIC_STRIPE_TEST_PUBLISHABLE_KEY=pk_test_...

# LIVE Mode (for customers)
STRIPE_LIVE_SECRET_KEY=sk_live_...
STRIPE_LIVE_WEBHOOK_SECRET=whsec_live_...
STRIPE_LIVE_PRICE_STARTER=price_...
STRIPE_LIVE_PRICE_PRO=price_...
STRIPE_LIVE_PRICE_ELITE=price_...
NEXT_PUBLIC_STRIPE_LIVE_PUBLISHABLE_KEY=pk_live_...
```

---

## Pricing Tiers (AUD, GST Included)

| Tier | Monthly | Annual | Features |
|------|---------|--------|----------|
| **Starter** | $495 | $4,950 | Basic CRM, 500 contacts, Email integration |
| **Professional** | $895 | $8,950 | Full CRM, Unlimited contacts, AI scoring, Drip campaigns |
| **Elite** | $1,295 | $12,950 | Everything + White-label, Priority support, Custom integrations |

**Currency**: Australian Dollars (AUD)
**Tax**: All prices include 10% GST

---

## Tasks This Agent Performs

### Task 1: Setup Complete Stripe Products

**Trigger**: "Setup Stripe products" or first-time billing initialization

**Steps**:
1. Create Starter product and prices (monthly + annual)
2. Create Professional product and prices
3. Create Elite product and prices
4. Store price IDs in environment
5. Configure webhook endpoints

**Output**:
```json
{
  "products": {
    "starter": "prod_xxx",
    "professional": "prod_yyy",
    "elite": "prod_zzz"
  },
  "prices": {
    "starter_monthly": "price_xxx",
    "starter_annual": "price_xxy",
    "professional_monthly": "price_yyy",
    "professional_annual": "price_yyz",
    "elite_monthly": "price_zzz",
    "elite_annual": "price_zza"
  }
}
```

### Task 2: Create Checkout for User

**Trigger**: User clicks "Subscribe" on pricing page

**Input**:
```json
{
  "email": "user@example.com",
  "tier": "professional",
  "billing": "monthly",
  "workspaceId": "uuid",
  "userId": "uuid"
}
```

**Steps**:
1. Determine billing mode (test/live based on email)
2. Get or create Stripe customer
3. Create checkout session with correct price
4. Return checkout URL

### Task 3: Handle Subscription Upgrade

**Trigger**: User clicks "Upgrade" in billing settings

**Input**:
```json
{
  "currentTier": "starter",
  "targetTier": "professional",
  "subscriptionId": "sub_xxx",
  "workspaceId": "uuid"
}
```

**Steps**:
1. Get current subscription
2. Calculate proration
3. Update subscription items
4. Handle billing adjustment
5. Update workspace tier in database

### Task 4: Process Webhook Events

**Trigger**: Stripe webhook received

**Events Handled**:
- `checkout.session.completed` → Activate subscription
- `customer.subscription.created` → Create subscription record
- `customer.subscription.updated` → Update tier, sync status
- `customer.subscription.deleted` → Deactivate subscription
- `invoice.paid` → Mark paid, extend access
- `invoice.payment_failed` → Flag account, send notification

### Task 5: Generate Billing Report

**Trigger**: "Generate billing report" or scheduled monthly

**Output**:
```json
{
  "period": "2025-11",
  "revenue": {
    "total": 15890.00,
    "byTier": {
      "starter": 4850.00,
      "professional": 8910.00,
      "elite": 2130.00
    }
  },
  "subscriptions": {
    "active": 87,
    "new": 12,
    "churned": 3,
    "mrr": 15890.00
  },
  "trials": {
    "active": 23,
    "converted": 8,
    "expired": 5
  }
}
```

### Task 6: Audit Stripe Configuration

**Trigger**: "Audit Stripe setup" or health check

**Checks**:
1. All environment variables present
2. Products exist in Stripe dashboard
3. Prices are correctly configured
4. Webhooks are registered
5. Test mode products match live mode structure

**Output**:
```json
{
  "status": "healthy" | "degraded" | "critical",
  "checks": {
    "env_vars": { "status": "pass", "missing": [] },
    "products": { "status": "pass", "count": 3 },
    "prices": { "status": "pass", "count": 6 },
    "webhooks": { "status": "warn", "message": "Live webhook not configured" }
  },
  "recommendations": [
    "Add STRIPE_LIVE_WEBHOOK_SECRET to production environment"
  ]
}
```

---

## Webhook Endpoints

### Test Mode
- **URL**: `https://your-domain.com/api/webhooks/stripe/test`
- **Events**: All subscription and invoice events
- **Secret**: `STRIPE_TEST_WEBHOOK_SECRET`

### Live Mode
- **URL**: `https://your-domain.com/api/webhooks/stripe/live`
- **Events**: All subscription and invoice events
- **Secret**: `STRIPE_LIVE_WEBHOOK_SECRET`

---

## Error Handling

### Common Errors

| Error | Cause | Resolution |
|-------|-------|------------|
| `StripeCardError` | Card declined | Notify customer, request new card |
| `StripeInvalidRequestError` | Bad API call | Check parameters, log for debugging |
| `StripeAuthenticationError` | Invalid API key | Verify environment variables |
| `StripeRateLimitError` | Too many requests | Implement exponential backoff |

### Retry Strategy

```typescript
const MAX_RETRIES = 3;
const RETRY_DELAYS = [1000, 2000, 4000]; // Exponential backoff

async function stripeWithRetry(operation) {
  for (let i = 0; i < MAX_RETRIES; i++) {
    try {
      return await operation();
    } catch (error) {
      if (error.type === 'StripeRateLimitError' && i < MAX_RETRIES - 1) {
        await sleep(RETRY_DELAYS[i]);
        continue;
      }
      throw error;
    }
  }
}
```

---

## Integration with Other Agents

### Orchestrator → Stripe Agent

```
Orchestrator
  ├─→ [On new signup] → Stripe Agent: Create customer
  ├─→ [On upgrade request] → Stripe Agent: Process upgrade
  ├─→ [On webhook] → Stripe Agent: Handle event
  └─→ [On audit] → Stripe Agent: Audit configuration
```

### Database Sync

After Stripe operations, sync to Supabase:

```typescript
// After successful subscription
await supabase.from('subscriptions').upsert({
  workspace_id: workspaceId,
  stripe_customer_id: customerId,
  stripe_subscription_id: subscriptionId,
  tier: tier,
  status: 'active',
  current_period_end: periodEnd
});
```

---

## Testing

### Test Cards

| Card Number | Scenario |
|-------------|----------|
| `4242424242424242` | Success |
| `4000000000000002` | Decline |
| `4000000000009995` | Insufficient funds |
| `4000002500003155` | 3D Secure required |

### Manual Testing

```bash
# Trigger test webhook
stripe trigger checkout.session.completed

# Listen for webhooks locally
stripe listen --forward-to localhost:3008/api/webhooks/stripe/test
```

---

## Files Reference

| File | Purpose |
|------|---------|
| `src/lib/billing/stripe-router.ts` | Dual-mode routing logic |
| `src/lib/billing/pricing-config.ts` | Pricing tier definitions |
| `src/lib/payments/stripeClient.ts` | Stripe client wrapper |
| `src/app/api/billing/subscription/route.ts` | Subscription API |
| `src/app/api/webhooks/stripe/[mode]/route.ts` | Webhook handlers |
| `src/app/api/stripe/checkout/route.ts` | Checkout session creation |

---

## Quick Commands

```bash
# Run Stripe setup script (to be created)
npm run stripe:setup

# Audit Stripe configuration
npm run stripe:audit

# Sync products from Stripe
npm run stripe:sync

# Test webhook locally
npm run stripe:webhook-test
```

---

*Skill file created: 2025-11-28*
