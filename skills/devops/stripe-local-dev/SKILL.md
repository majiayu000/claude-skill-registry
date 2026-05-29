---
name: stripe-local-dev
description: |
  Fix Stripe webhook 400 errors in local development. The problem: `stripe listen`
  generates a new secret each time it starts, but your app uses a stale secret from
  .env.local. This skill auto-syncs the ephemeral secret before your dev server starts.

  Auto-invoke when: stripe webhooks return 400, "signature verification failed",
  "No signatures found matching", webhooks not working locally, checkout succeeds
  but subscription doesn't update, STRIPE_WEBHOOK_SECRET mismatch, setting up
  stripe listen, configuring pnpm dev with Stripe.
---

# /stripe-local-dev

Ensure Stripe webhooks work in local development by auto-syncing ephemeral secrets.

## The Problem

Stripe CLI generates a **new webhook secret** every time `stripe listen` starts. If your dev script auto-starts the listener but doesn't sync the secret, you get:

```
Webhook error: signature verification failed
No signatures found matching the expected signature for payload
```

## The Solution Pattern

**Auto-start requires auto-sync.** Use `dev-stripe.sh`:

1. Extract secret via `stripe listen --print-secret`
2. Sync to environment (Convex env OR .env.local)
3. THEN start forwarding

## Architecture Decision

| Webhook Location | Secret Sync Target | Restart? | Recommendation |
|-----------------|-------------------|----------|----------------|
| Convex HTTP (`convex/http.ts`) | `npx convex env set` | No | Best |
| Next.js API Route | `.env.local` | Yes | Requires orchestration |

**Prefer Convex HTTP webhooks** - secret sync is instant, no restart needed.

## Implementation

### Option A: Convex HTTP Webhooks (Recommended)

Copy script:
```bash
cp ~/.claude/skills/stripe-local-dev/scripts/dev-stripe-convex.sh scripts/dev-stripe.sh
chmod +x scripts/dev-stripe.sh
```

Update package.json:
```json
"stripe:listen": "./scripts/dev-stripe.sh"
```

### Option B: Next.js API Webhooks

Copy script:
```bash
cp ~/.claude/skills/stripe-local-dev/scripts/dev-stripe-nextjs.sh scripts/dev-stripe.sh
chmod +x scripts/dev-stripe.sh
```

Update package.json:
```json
"stripe:listen": "./scripts/dev-stripe.sh"
```

**Note**: Next.js needs restart to pick up env changes. The script warns about this.

## Verification

After setup, run:
```bash
pnpm dev
# Then in another terminal:
stripe trigger checkout.session.completed
# Check logs for 200 response, not 400
```

## Quick Diagnostics

| Symptom | Cause | Fix |
|---------|-------|-----|
| All webhooks return 400 | Stale secret | Restart `pnpm dev` or run sync script |
| "signature verification failed" | Secret mismatch | Check CLI output matches env |
| Works once, fails after restart | No auto-sync | Add `dev-stripe.sh` script |
| CLI shows delivered, app shows error | Wrong env target | Check sync target (Convex vs .env.local) |

## Related Skills

- `/check-stripe` - Audit Stripe integration
- `/stripe-health` - Webhook health diagnostics
- `/stripe-audit` - Comprehensive Stripe audit
