---
name: subscription-patterns
description: |
  Subscription lifecycle patterns for Stripe + Convex/database backends.
  Invoke for: trial-to-paid flows, subscription state management, webhook handling,
  access control logic, cancel/resubscribe edge cases.
keywords:
  - subscription
  - trial
  - stripe
  - billing
  - access control
  - trial_end
  - webhook
  - cancel
  - resubscribe
---

# Subscription Lifecycle Patterns

Best practices for managing subscription states, trials, and access control with Stripe.

## Core Principle

**Stripe is the source of truth for billing. Your database caches state for access decisions.**

---

## Trial-to-Paid Flow

### The Right Way: Use Stripe's `trial_end`

When a user subscribes during their trial, honor remaining days:

```typescript
// In checkout session creation
const TRIAL_DURATION_MS = 14 * 24 * 60 * 60 * 1000;

// Calculate remaining trial
const trialEndMs = user?.trialEndsAt
  ?? (user?._creationTime ? user._creationTime + TRIAL_DURATION_MS : null);

const now = Date.now();
const hasRemainingTrial = trialEndMs && trialEndMs > now;
const trialEndSeconds = hasRemainingTrial ? Math.floor(trialEndMs / 1000) : undefined;

// Pass to Stripe - it handles billing delay
const session = await stripe.checkout.sessions.create({
  // ...
  subscription_data: {
    metadata: { userId },
    ...(trialEndSeconds && { trial_end: trialEndSeconds }),
  },
});
```

**Benefits:**
- Stripe delays first charge until `trial_end`
- User sees "trial ends on X" in Stripe customer portal
- No manual billing logic needed

### Prevent Zombie Trials

**Problem:** If trial data persists after subscription, canceled users may regain access.

**Solution:** Clear trial when subscription activates:

```typescript
// In webhook handler / updateFromStripe mutation
await db.patch(user._id, {
  subscriptionStatus: status,
  // Clear trial to prevent zombie access after cancel
  ...(status === "active" && { trialEndsAt: 0 }),
});
```

---

## Access Control Priority

Check states in this order (first match wins):

```typescript
function hasAccess(user): boolean {
  // 1. Active subscription - always grants access
  if (user.subscriptionStatus === "active") return true;

  // 2. Canceled but in paid period - access through period end
  if (user.subscriptionStatus === "canceled" &&
      user.currentPeriodEnd &&
      Date.now() < user.currentPeriodEnd) {
    return true;
  }

  // 3. Past due with grace period
  if (user.subscriptionStatus === "past_due" &&
      user.currentPeriodEnd &&
      Date.now() < user.currentPeriodEnd) {
    return true;
  }

  // 4. Locked states - explicitly deny (before trial check)
  const lockedStates = ["incomplete", "unpaid", "expired"];
  if (lockedStates.includes(user.subscriptionStatus)) {
    return false;
  }

  // 5. Trial active - fallback for non-subscribers
  if (user.trialEndsAt && Date.now() < user.trialEndsAt) {
    return true;
  }

  return false;
}
```

**Key insight:** Locked states block before trial check. This prevents edge cases where trial data could grant access.

---

## Edge Cases & Handling

### User Cancels During Trial
- `subscriptionStatus` = "canceled"
- `trialEndsAt` already cleared (was set to 0 when sub activated)
- Access continues until `currentPeriodEnd` (from Stripe trial_end)
- No zombie trial risk

### User Resubscribes After Cancel
- New checkout creates new subscription
- Fresh `trial_end` calculation (likely 0 - no trial remaining)
- Billing starts immediately

### User Never Had Trial (Direct Subscribe)
- No `trialEndsAt` or `_creationTime` for trial calc
- `trial_end` not passed to Stripe
- Billing starts immediately (correct)

### Webhook Arrives Out of Order
- Use `eventTimestamp` comparison
- Reject events older than last processed
- Use `eventId` for exact deduplication

---

## Webhook Event Handling

### Essential Events

| Event | Action |
|-------|--------|
| `checkout.session.completed` | Link customer, initial status |
| `customer.subscription.created` | Set status, period end |
| `customer.subscription.updated` | Update status, period end |
| `customer.subscription.deleted` | Set status to canceled/expired |
| `invoice.payment_succeeded` | Update period end |
| `invoice.payment_failed` | Set status to past_due |

### Idempotency Pattern

```typescript
// Check for duplicate event
if (user.lastStripeEventId === eventId) {
  return { success: false, reason: "duplicate_event" };
}

// Check for stale event
if (user.lastStripeEventTimestamp &&
    eventTimestamp < user.lastStripeEventTimestamp) {
  return { success: false, reason: "stale_event" };
}

// Process and record
await db.patch(user._id, {
  // ... updates
  lastStripeEventId: eventId,
  lastStripeEventTimestamp: eventTimestamp,
});
```

---

## Testing Checklist

### Trial Flow
- [ ] New user gets 14-day trial
- [ ] Trial countdown displays correctly
- [ ] Access denied after trial expires (hard cutoff)

### Subscribe During Trial
- [ ] Remaining trial days passed to Stripe
- [ ] Stripe subscription shows trial_end
- [ ] No charge until trial_end
- [ ] trialEndsAt cleared in database

### Cancel Flow
- [ ] Access continues until currentPeriodEnd
- [ ] No zombie trial access after period ends
- [ ] Resubscribe starts billing immediately

### Webhook Handling
- [ ] Out-of-order events handled correctly
- [ ] Duplicate events rejected
- [ ] Fallback works if customer not linked

---

## Common Pitfalls

### 1. Lazy Trial Calculation Gone Wrong
**Problem:** Calculating trial from `_creationTime` without clearing it.
**Fix:** Always clear `trialEndsAt` when subscription activates.

### 2. Checking Trial Before Locked States
**Problem:** User with `status=expired` might have valid trial dates.
**Fix:** Check locked states before trial in access logic.

### 3. Missing currentPeriodEnd
**Problem:** Some webhooks don't include period end.
**Fix:** Always set it from `invoice.payment_succeeded` as backup.

### 4. Not Using Stripe's trial_end
**Problem:** Custom trial logic that diverges from Stripe.
**Fix:** Let Stripe manage trial via `trial_end` parameter.

---

## Related Skills

- `billing-security` - Security patterns for payment integrations
- `stripe-health` - Webhook health diagnostics
- `reconciliation-patterns` - Syncing external service state
