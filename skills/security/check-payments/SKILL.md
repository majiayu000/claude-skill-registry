---
name: check-payments
description: |
  Multi-provider payment audit. Runs check-stripe, check-bitcoin, check-lightning.
  Outputs consolidated findings. Use log-*-issues to create GitHub issues.
  Invoke for: comprehensive payment review, multi-provider audit.
---

# /check-payments

Audit all payment providers. Orchestrates provider checks, consolidates output.

## What This Does

1. Detect configured payment providers
2. Run applicable provider checks
3. Consolidate findings into one P0-P3 report

**This is a primitive.** Investigate only. No fixes.

## Process

### 1. Detect Providers

Run detection below. Note which providers are present.

### 2. Run Checks

Run only applicable checks:
- `/check-stripe`
- `/check-bitcoin`
- `/check-lightning`
- `/check-btcpay`

### 3. Consolidate Findings

Merge findings into one report. Deduplicate overlaps. Keep P0-P3.

## Provider Detection

```bash
# Stripe: package + env
grep -q "stripe" package.json 2>/dev/null && echo "✓ Stripe SDK" || echo "✗ Stripe SDK"
env | grep -q "STRIPE_" && echo "✓ STRIPE_* vars" || grep -q "STRIPE_" .env.local 2>/dev/null && echo "✓ STRIPE_* vars (file)" || echo "✗ STRIPE_* vars"

# Bitcoin: CLI + env
command -v bitcoin-cli >/dev/null && echo "✓ bitcoin-cli" || echo "✗ bitcoin-cli"
env | grep -q "BITCOIN_" && echo "✓ BITCOIN_* vars" || grep -q "BITCOIN_" .env.local 2>/dev/null && echo "✓ BITCOIN_* vars (file)" || echo "✗ BITCOIN_* vars"

# Lightning: CLI + env
command -v lncli >/dev/null && echo "✓ lncli" || echo "✗ lncli"
env | grep -q "LND_" && echo "✓ LND_* vars" || grep -q "LND_" .env.local 2>/dev/null && echo "✓ LND_* vars (file)" || echo "✗ LND_* vars"

# BTCPay: env only
env | grep -q "BTCPAY_" && echo "✓ BTCPAY_* vars" || grep -q "BTCPAY_" .env.local 2>/dev/null && echo "✓ BTCPAY_* vars (file)" || echo "✗ BTCPAY_* vars"
```

## Output Format

```markdown
## Payments Audit

### P0: Critical
- Stripe: Webhooks unverified (missing STRIPE_WEBHOOK_SECRET)
- Bitcoin: RPC creds missing in prod

### P1: Essential
- Lightning: LND_* vars missing
- BTCPay: No webhook signature verification

### P2: Important
- Stripe: No idempotency keys
- Bitcoin: No retry/backoff on RPC errors

### P3: Nice to Have
- Add payment analytics dashboard

## Provider Status
- Stripe: Present
- Bitcoin: Not detected
- Lightning: Present
- BTCPay: Present

## Summary
- P0: 1 | P1: 2 | P2: 2 | P3: 1
```

## Related

- `/check-stripe`
- `/check-bitcoin`
- `/check-lightning`
- `/check-btcpay`
- `/log-stripe-issues`
- `/log-bitcoin-issues`
- `/log-lightning-issues`
