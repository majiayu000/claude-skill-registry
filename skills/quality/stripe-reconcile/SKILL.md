---
name: stripe-reconcile
description: |
  Fix issues found by stripe-audit. Reconciles configuration drift,
  fixes code patterns, and resolves discrepancies.
---

# Stripe Reconcile

Fix issues identified by the audit.

## Branching

Assumes you start on `master`/`main`. Before making code changes:

```bash
git checkout -b fix/stripe-reconcile-$(date +%Y%m%d)
```

Configuration-only changes (env vars, dashboard settings) don't require a branch. Code changes do.

## Objective

Take audit findings and fix them. Configuration issues get fixed directly. Code issues get delegated to Codex.

## Process

**1. Triage Findings**

From the audit report, categorize:

**Configuration fixes** (do directly):
- Missing env vars
- Wrong webhook URL
- Dashboard settings

**Code fixes** (delegate to Codex):
- Missing trial_end handling
- Idempotency implementation
- Access control corrections

**Design issues** (may need stripe-design):
- Wrong checkout mode
- Missing webhook events
- Architectural problems

**2. Fix Configuration**

For env var issues:
```bash
# Example: missing prod webhook secret
npx convex env set --prod STRIPE_WEBHOOK_SECRET "whsec_..."
```

For webhook URL issues:
- Update in Stripe Dashboard
- Or use Stripe CLI: `stripe webhook_endpoints update <id> --url "https://..."`

Verify fixes immediately.

**3. Delegate Code Fixes to Codex**

For each code issue, create a focused Codex task:

```bash
codex exec --full-auto "Fix: [specific issue from audit]. \
Current code in [file]. Problem: [what's wrong]. \
Fix: [what it should do]. Reference [pattern file] for correct approach. \
Run pnpm typecheck after." \
--output-last-message /tmp/codex-fix.md 2>/dev/null
```

Then review: `git diff --stat && pnpm typecheck`

**4. Verify Each Fix**

After fixing, verify:
- Configuration: `npx convex env list --prod | grep STRIPE`
- Webhook URL: `curl -I -X POST <url>`
- Code: `pnpm typecheck && pnpm test`

**5. Re-audit**

After all fixes, run a quick re-audit to confirm issues resolved.

## Common Fixes

**Missing env var on prod**
```bash
npx convex env set --prod STRIPE_WEBHOOK_SECRET "$(printf '%s' 'whsec_...')"
```
(Use printf to avoid trailing newlines)

**Webhook URL redirect**
Update to canonical domain in Stripe Dashboard. If `example.com` redirects to `www.example.com`, use `www.example.com`.

**Missing trial_end handling**
In checkout session creation, calculate remaining trial and pass to Stripe:
```typescript
const trialEnd = user.trialEndsAt && user.trialEndsAt > Date.now()
  ? Math.floor(user.trialEndsAt / 1000)
  : undefined;
// Pass in subscription_data.trial_end
```

**Missing idempotency**
Store `lastStripeEventId` on user, check before processing webhook.

## Output

For each finding:
- What was fixed
- How it was fixed
- Verification result

Any remaining issues that couldn't be auto-fixed.
