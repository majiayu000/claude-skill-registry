---
name: fix-stripe
description: |
  Run /check-stripe, then fix the highest priority Stripe issue.
  Creates one fix per invocation. Invoke again for next issue.
  Use /log-stripe-issues to create issues without fixing.
---

# /fix-stripe

Fix the highest priority Stripe integration issue.

## What This Does

1. Invoke `/check-stripe` to audit Stripe integration
2. Identify highest priority issue
3. Fix that one issue
4. Verify the fix
5. Report what was done

**This is a fixer.** It fixes one issue at a time. Run again for next issue. Use `/stripe` for full lifecycle.

## Process

### 1. Run Primitive

Invoke `/check-stripe` skill to get prioritized findings.

### 2. Fix Priority Order

Fix in this order:
1. **P0**: Missing webhook secret, hardcoded keys
2. **P1**: Webhook verification, customer portal, subscription checks
3. **P2**: Idempotency, error handling
4. **P3**: Advanced features

### 3. Execute Fix

**Missing webhook secret (P0):**
Add to `.env.local`:
```
STRIPE_WEBHOOK_SECRET=whsec_...
```

Get from Stripe Dashboard or CLI:
```bash
stripe listen --print-secret
```

**Hardcoded keys (P0):**
Replace hardcoded keys with environment variables:
```typescript
// Before
const stripe = new Stripe('sk_test_...', { apiVersion: '2024-12-18.acacia' });

// After
const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, { apiVersion: '2024-12-18.acacia' });
```

**Webhook verification missing (P1):**
Update webhook handler:
```typescript
export async function POST(req: Request) {
  const body = await req.text();
  const signature = req.headers.get('stripe-signature')!;

  let event: Stripe.Event;
  try {
    event = stripe.webhooks.constructEvent(
      body,
      signature,
      process.env.STRIPE_WEBHOOK_SECRET!
    );
  } catch (err) {
    return new Response('Webhook signature verification failed', { status: 400 });
  }

  // Handle event...
}
```

**No customer portal (P1):**
Add billing portal endpoint:
```typescript
// app/api/stripe/portal/route.ts
export async function POST(req: Request) {
  const { customerId } = await req.json();

  const session = await stripe.billingPortal.sessions.create({
    customer: customerId,
    return_url: `${process.env.NEXT_PUBLIC_APP_URL}/settings`,
  });

  return Response.json({ url: session.url });
}
```

**Subscription status not checked (P1):**
Add subscription check middleware:
```typescript
async function requireActiveSubscription(userId: string) {
  const subscription = await getSubscription(userId);
  if (!subscription || subscription.status !== 'active') {
    throw new Error('Active subscription required');
  }
}
```

### 4. Verify

After fix:
```bash
# Test webhook verification
stripe trigger checkout.session.completed

# Check portal works
curl -X POST http://localhost:3000/api/stripe/portal \
  -H "Content-Type: application/json" \
  -d '{"customerId": "cus_test"}'
```

### 5. Report

```
Fixed: [P0] Webhook signature not verified

Updated: app/api/webhooks/stripe/route.ts
- Added signature verification with constructEvent()
- Added error handling for invalid signatures

Verified: stripe trigger checkout.session.completed → verified

Next highest priority: [P1] No customer portal
Run /fix-stripe again to continue.
```

## Branching

Before making changes:
```bash
git checkout -b fix/stripe-$(date +%Y%m%d)
```

## Single-Issue Focus

Payment integrations are critical. Fix one thing at a time:
- Test each change thoroughly
- Easy to rollback specific fixes
- Clear audit trail for PCI

Run `/fix-stripe` repeatedly to work through the backlog.

## Related

- `/check-stripe` - The primitive (audit only)
- `/log-stripe-issues` - Create issues without fixing
- `/stripe` - Full Stripe lifecycle
- `/stripe-health` - Webhook diagnostics
