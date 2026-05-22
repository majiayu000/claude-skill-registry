---
name: env-var-hygiene
description: "Environment variable management across Vercel, Convex, and other platforms. Invoke for: trailing whitespace issues, cross-platform parity, Invalid character errors, webhook secrets, API key management, production deployment, dev vs prod configuration."
---

# Environment Variable Hygiene

Best practices for managing environment variables across deployment platforms.

## Triggers

Invoke when user mentions:
- "env var", "environment variable", "production deploy"
- "webhook secret", "API key", "token"
- "Invalid character in header", "ERR_INVALID_CHAR"
- "silent failure", "webhook not working"
- "Vercel", "Convex", "deployment", "secrets"

## Core Principles

### 1. Trailing Whitespace Kills

Env vars with `\n` or trailing spaces cause cryptic errors:
- "Invalid character in header content" (HTTP headers)
- Webhook signature mismatch
- Silent authentication failures

**Root Cause:** Copy-paste or `echo` introduces invisible characters.

**Prevention:**
```bash
# ✅ Use printf, not echo
printf '%s' 'sk_live_xxx' | vercel env add STRIPE_SECRET_KEY production

# ✅ Trim when setting
npx convex env set --prod KEY "$(echo 'value' | tr -d '\n')"

# ❌ Don't use echo directly
echo "sk_live_xxx" | vercel env add KEY production  # May add \n
```

### 2. Cross-Platform Parity

Shared tokens (webhook secrets, auth tokens) must be identical across platforms:
- Vercel ↔ Convex
- Frontend ↔ Backend
- Dev ↔ Staging ↔ Prod (within each platform)

**Common Pitfall:** Set token on one platform, forget the other.

**Prevention:**
```bash
# Generate token once
TOKEN=$(openssl rand -hex 32)

# Set on ALL platforms
npx convex env set --prod CONVEX_WEBHOOK_TOKEN "$(printf '%s' "$TOKEN")"
printf '%s' "$TOKEN" | vercel env add CONVEX_WEBHOOK_TOKEN production
```

### 3. Validate Format Before Use

API keys have specific formats. Validate before deployment:

| Service | Pattern | Example |
|---------|---------|---------|
| Stripe Secret | `sk_(test\|live)_[A-Za-z0-9]+` | `sk_live_xxx` |
| Stripe Public | `pk_(test\|live)_[A-Za-z0-9]+` | `pk_live_xxx` |
| Stripe Webhook | `whsec_[A-Za-z0-9]+` | `whsec_xxx` |
| Stripe Price | `price_[A-Za-z0-9]+` | `price_xxx` |
| Clerk Secret | `sk_(test\|live)_[A-Za-z0-9]+` | `sk_live_xxx` |

### 4. Dev ≠ Prod

Separate deployments have separate env var stores:
- Setting `.env.local` doesn't affect production
- Convex dev and prod are separate deployments
- Vercel has per-environment variables

**Always verify prod separately:**
```bash
# Convex
npx convex env list --prod

# Vercel
vercel env ls --environment=production
```

### 5. CLI Environment Gotcha

`CONVEX_DEPLOYMENT=prod:xxx npx convex data` may return dev data.

**Always use explicit flags:**
```bash
# ❌ Unreliable
CONVEX_DEPLOYMENT=prod:xxx npx convex data

# ✅ Reliable
npx convex run --prod module:function
npx convex env list --prod
```

## Quick Reference

### Setting Env Vars Safely

**Convex:**
```bash
# Dev
npx convex env set KEY "value"

# Prod (use --prod flag)
npx convex env set --prod KEY "$(printf '%s' 'value')"
```

**Vercel:**
```bash
# Production
printf '%s' 'value' | vercel env add KEY production

# With explicit environment
vercel env add KEY production --force
```

### Checking Env Vars

**Convex:**
```bash
npx convex env list           # dev
npx convex env list --prod    # prod
```

**Vercel:**
```bash
vercel env ls                              # all
vercel env ls --environment=production     # prod only
```

### Detecting Issues

**Trailing whitespace:**
```bash
# Check Convex prod
npx convex env list --prod | while IFS= read -r line; do
  if [[ "$line" =~ [[:space:]]$ ]]; then
    echo "WARNING: $(echo "$line" | cut -d= -f1) has trailing whitespace"
  fi
done
```

**Format validation:**
```bash
# Validate Stripe key format
value=$(npx convex env list --prod | grep "^STRIPE_SECRET_KEY=" | cut -d= -f2-)
[[ "$value" =~ ^sk_(test|live)_[A-Za-z0-9]+$ ]] || echo "Invalid format"
```

## References

See `references/` directory:
- `format-patterns.md` - Regex patterns for common services
- `platform-specifics.md` - Vercel, Convex, Railway platform details
- `hygiene-checklist.md` - Pre-deployment validation checklist
- `parity-verification.md` - Cross-platform token verification

## Related Commands

- `/pre-deploy` - Comprehensive pre-deployment checklist
- `/env-parity-check` - Cross-platform token verification
- `/stripe-check` - Stripe-specific environment audit

---

*Based on 2026-01-17 incident: Trailing `\n` in `STRIPE_SECRET_KEY` caused "Invalid character in header" error. Token mismatch between Vercel and Convex caused silent webhook failures.*
