---
name: check-stripe
description: |
  Audit Stripe integration: configuration, webhooks, subscription logic, security.
  Outputs structured findings. Use log-stripe-issues to create issues.
  Invoke for: Stripe audit, payment review, subscription analysis.
---

# /check-stripe

Audit Stripe integration. Output findings as structured report.

## What This Does

1. Check Stripe configuration (env vars, SDK)
2. Audit webhook setup and handling
3. Review subscription logic
4. Check security practices
5. Verify test/production separation
6. Output prioritized findings (P0-P3)

**This is a primitive.** It only investigates and reports. Use `/log-stripe-issues` to create GitHub issues or `/fix-stripe` to fix.

## Process

### 1. Configuration Check

```bash
# Stripe SDK installed?
grep -q "stripe" package.json 2>/dev/null && echo "✓ Stripe SDK" || echo "✗ Stripe SDK not installed"

# Environment variables
[ -n "$STRIPE_SECRET_KEY" ] || grep -q "STRIPE_SECRET_KEY" .env.local 2>/dev/null && echo "✓ STRIPE_SECRET_KEY" || echo "✗ STRIPE_SECRET_KEY missing"
[ -n "$STRIPE_WEBHOOK_SECRET" ] || grep -q "STRIPE_WEBHOOK_SECRET" .env.local 2>/dev/null && echo "✓ STRIPE_WEBHOOK_SECRET" || echo "✗ STRIPE_WEBHOOK_SECRET missing"
[ -n "$NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY" ] || grep -q "STRIPE_PUBLISHABLE_KEY" .env.local 2>/dev/null && echo "✓ Publishable key" || echo "✗ Publishable key missing"

# Test vs Production keys
grep "STRIPE_SECRET_KEY" .env.local 2>/dev/null | grep -q "sk_test" && echo "✓ Using test key (dev)" || echo "⚠ Check key type"
```

### 2. Webhook Audit

```bash
# Webhook endpoint exists?
find . -path "*/api/*webhook*" -name "route.ts" 2>/dev/null | head -3

# Webhook signature verification?
grep -rE "constructEvent|stripe\.webhooks\.constructEvent" --include="*.ts" . 2>/dev/null | grep -v node_modules | head -3

# Webhook event handling?
grep -rE "checkout\.session\.completed|invoice\.paid|customer\.subscription" --include="*.ts" . 2>/dev/null | grep -v node_modules | head -5
```

### 3. Security Check

```bash
# Hardcoded keys?
grep -rE "sk_live_|sk_test_|pk_live_|pk_test_" --include="*.ts" --include="*.tsx" . 2>/dev/null | grep -v node_modules | grep -v ".env"

# Secret key exposure?
grep -rE "STRIPE_SECRET_KEY" --include="*.tsx" . 2>/dev/null | grep -v node_modules

# Proper server-side usage?
grep -rE "stripe\." --include="*.tsx" . 2>/dev/null | grep -v node_modules | grep -v "loadStripe" | head -5
```

### 4. Subscription Logic

```bash
# Subscription status handling?
grep -rE "subscription\.status|active|canceled|past_due|trialing" --include="*.ts" . 2>/dev/null | grep -v node_modules | head -5

# Customer portal?
grep -rE "createBillingPortalSession|billing.*portal" --include="*.ts" . 2>/dev/null | grep -v node_modules | head -3

# Price/product IDs?
grep -rE "price_|prod_" --include="*.ts" . 2>/dev/null | grep -v node_modules | head -5
```

### 5. CLI Profile Check

```bash
# Stripe CLI configured?
command -v stripe >/dev/null && echo "✓ Stripe CLI installed" || echo "✗ Stripe CLI not installed"

# Check profiles
stripe config --list 2>/dev/null | head -5 || echo "Stripe CLI not configured"
```

### 6. Local Dev Webhook Sync Check

```bash
# Does pnpm dev auto-start stripe listener?
if grep -q "stripe.*listen" package.json 2>/dev/null; then
  echo "✓ Auto-starts stripe listen"

  # Is there a sync script?
  if [ -f scripts/dev-stripe.sh ] && grep -q "print-secret" scripts/dev-stripe.sh 2>/dev/null; then
    echo "✓ Webhook secret auto-sync configured"
  else
    echo "⚠ No webhook secret auto-sync - will get 400 errors after CLI restart"
  fi
else
  echo "○ Manual stripe listen (no auto-sync needed)"
fi
```

### 7. Deep Audit

Spawn `stripe-auditor` agent for comprehensive review:
- Checkout session parameters
- Subscription creation patterns
- Error handling in payment flows
- Idempotency key usage
- Customer creation/retrieval

## Output Format

```markdown
## Stripe Audit

### P0: Critical (Payment Failures)
- STRIPE_WEBHOOK_SECRET missing - Webhooks unverified (security risk)
- Hardcoded test key in production code

### P1: Essential (Must Fix)
- Webhook signature not verified - Security vulnerability
- No customer portal configured - Users can't manage subscriptions
- Subscription status not checked on protected routes
- Missing STRIPE_SECRET_KEY in production env

### P2: Important (Should Fix)
- No idempotency keys on payment operations
- Subscription cancellation not handled gracefully
- No retry logic on transient Stripe errors
- Stripe CLI not using profiles (sandbox vs production)
- No auto-sync of local webhook secret - `pnpm dev` auto-starts `stripe listen` but doesn't sync the ephemeral secret to `.env.local`. After CLI restart, webhooks will return 400.

### P3: Nice to Have
- Consider adding Stripe Tax
- Consider adding usage-based billing
- Add subscription analytics dashboard

## Current Status
- SDK: Installed
- Webhooks: Configured but unverified
- Subscriptions: Basic implementation
- Security: Issues found
- Test/Prod separation: Not enforced

## Summary
- P0: 2 | P1: 4 | P2: 4 | P3: 3
- Recommendation: Fix webhook verification and add customer portal
```

## Priority Mapping

| Gap | Priority |
|-----|----------|
| Missing webhook secret | P0 |
| Hardcoded keys | P0 |
| Webhook verification missing | P1 |
| No customer portal | P1 |
| Subscription status not checked | P1 |
| No idempotency keys | P2 |
| Poor error handling | P2 |
| Missing CLI profiles | P2 |
| No webhook secret auto-sync | P2 |
| Advanced features | P3 |

## Related

- `/log-stripe-issues` - Create GitHub issues from findings
- `/fix-stripe` - Fix Stripe issues
- `/stripe` - Full Stripe lifecycle management
- `/stripe-audit` - Comprehensive Stripe audit
- `/stripe-health` - Webhook health diagnostics
