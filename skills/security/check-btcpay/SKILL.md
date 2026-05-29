---
name: check-btcpay
description: |
  Audit BTCPay Server configuration. Checks store settings, webhook health,
  payment notifications, and API connectivity. Use when: running BTCPay
  as payment processor, diagnosing webhook issues, or verifying setup.
  Keywords: btcpay, btcpayserver, greenfield, payment processor.
---

# /check-btcpay

Audit BTCPay Server configuration. Output findings as structured report.

## What This Does

1. Check Greenfield API connectivity
2. Audit store configuration
3. Review webhook endpoints + signature verification
4. Check payment notification settings
5. Verify Lightning node connection
6. Verify wallet hot/cold separation
7. Output prioritized findings (P0-P3)

**This is a primitive.** It only investigates and reports. Use `/log-production-issues` to create issues or `/check-production` for infra review.

## Process

### 1. API Connectivity (Greenfield API health)

```bash
export BTCPAY_URL="https://btcpay.example.com"
export BTCPAY_API_KEY="your-api-key"

# Greenfield health
curl -s -H "Authorization: token $BTCPAY_API_KEY" "$BTCPAY_URL/api/v1/health"

# List stores (requires valid API key)
curl -s -H "Authorization: token $BTCPAY_API_KEY" "$BTCPAY_URL/api/v1/stores" | jq
```

### 2. Store Configuration

```bash
# Set STORE_ID from the stores list above
export STORE_ID="store_id_here"

# Store details
curl -s -H "Authorization: token $BTCPAY_API_KEY" "$BTCPAY_URL/api/v1/stores/$STORE_ID" | jq

# Enabled payment methods
curl -s -H "Authorization: token $BTCPAY_API_KEY" "$BTCPAY_URL/api/v1/stores/$STORE_ID/payment-methods" | jq
```

### 3. Webhook Endpoints + Signature Verification

```bash
# List configured webhooks
curl -s -H "Authorization: token $BTCPAY_API_KEY" "$BTCPAY_URL/api/v1/stores/$STORE_ID/webhooks" | jq

# Webhook handlers in code
find . -path "*/api/*webhook*" -name "*.ts" 2>/dev/null | head -5

# Signature verification in handlers?
grep -rE "btcpay|webhook.*signature|hmac" --include="*.ts" . 2>/dev/null | grep -v node_modules | head -5
```

### 4. Payment Notification Settings

```bash
# In-app notification handlers (invoice paid/confirmed)
grep -rE "invoice.*(paid|confirmed|expired)|payment.*(received|settled)" --include="*.ts" . 2>/dev/null | grep -v node_modules | head -5

# Check for notification URL/config in app env
grep -rE "BTCPAY_.*(NOTIFY|NOTIFICATION|WEBHOOK)" --include="*.env*" . 2>/dev/null | head -5
```

### 5. Lightning Node Connection

```bash
# Confirm Lightning payment method enabled at store
curl -s -H "Authorization: token $BTCPAY_API_KEY" "$BTCPAY_URL/api/v1/stores/$STORE_ID/payment-methods" | jq

# Lightning node health checks in repo
grep -rE "lnd|lightning|lnurl|bolt11" --include="*.ts" . 2>/dev/null | grep -v node_modules | head -5
```

### 6. Wallet Hot/Cold Separation

```bash
# Look for hot wallet usage or private keys in repo
grep -rE "xprv|seed|mnemonic|private key" --include="*.ts" --include="*.env*" . 2>/dev/null | grep -v node_modules | head -5

# Watch-only setup hints (xpub descriptors)
grep -rE "xpub|ypub|zpub|descriptor" --include="*.ts" --include="*.env*" . 2>/dev/null | grep -v node_modules | head -5
```

### 7. Deep Audit

Spawn `btcpay-auditor` agent for comprehensive review:
- Invoice lifecycle handling (new, paid, confirmed, expired)
- Webhook signature verification and replay protection
- Store policies vs code expectations
- Lightning vs on-chain fallback behavior
- Wallet key custody and backup posture

## Output Format

```markdown
## BTCPay Audit

### P0: Critical (Payment Failures)
- Greenfield API unreachable - `GET /api/v1/health` fails
- Webhooks not receiving events (no active endpoints)
- Store has no enabled payment methods

### P1: Essential (Must Fix)
- Webhook signature not verified - security risk
- Invoice status handling missing (paid/confirmed/expired)
- Lightning payment method enabled but node not connected
- Notification URL missing or misconfigured

### P2: Important (Should Fix)
- No retry/backoff on webhook delivery failures
- Payment method config inconsistent between store and app
- Hot wallet usage detected without separation plan
- No monitoring of invoice settlement latency

### P3: Nice to Have
- Add separate store for test vs production
- Add automated webhook replay tooling
- Add dashboard for invoice outcomes

## Current Status
- Greenfield API: Unknown
- Stores: Unknown
- Webhooks: Unknown
- Notifications: Unknown
- Lightning: Unknown
- Wallet separation: Unknown

## Summary
- P0: 3 | P1: 4 | P2: 4 | P3: 3
- Recommendation: Fix API connectivity + webhook verification first
```

## Priority Mapping

| Gap | Priority |
|-----|----------|
| Greenfield API unreachable | P0 |
| No enabled payment methods | P0 |
| Webhooks not receiving events | P0 |
| Webhook signature not verified | P1 |
| Missing invoice status handling | P1 |
| Lightning node not connected | P1 |
| Notification URL missing | P1 |
| Missing retry/backoff | P2 |
| Config mismatch store vs app | P2 |
| Hot wallet without separation | P2 |
| Monitoring gaps | P2 |
| Optimization/analytics | P3 |

## Related

- `/check-lightning` - Lightning setup review
- `/check-bitcoin` - On-chain wallet review
- `/check-production` - Infra readiness
- `/log-production-issues` - Create issues from findings
