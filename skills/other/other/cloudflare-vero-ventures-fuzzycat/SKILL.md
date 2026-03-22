---
name: cloudflare
description: >
  Manage Cloudflare Turnstile CAPTCHA via REST API. Check widget status, list site keys,
  view solve rates and analytics, and validate challenge tokens. Use for CAPTCHA
  administration and debugging.
allowed-tools: Bash, Read, Grep, Glob
---

# Cloudflare Turnstile API

Manage FuzzyCat's Cloudflare Turnstile CAPTCHA integration.

## Authentication

```bash
TURNSTILE_SITE_KEY=$(grep NEXT_PUBLIC_TURNSTILE_SITE_KEY .env.local | cut -d'"' -f2)
TURNSTILE_SECRET=$(grep TURNSTILE_SECRET_KEY .env.local | cut -d'"' -f2)
```

## Common Commands

### Validate a Turnstile Token

```bash
# Server-side validation (this is what our backend does)
curl -s -X POST "https://challenges.cloudflare.com/turnstile/v0/siteverify" \
  -H "Content-Type: application/json" \
  -d "{
    \"secret\": \"$TURNSTILE_SECRET\",
    \"response\": \"<token-from-client>\"
  }" | python3 -m json.tool

# Response: {"success": true/false, "challenge_ts": "...", "hostname": "..."}
```

### Test Keys (for development)

Cloudflare provides special test site keys and secrets that always pass, always fail, or force
an interactive challenge. See: https://developers.cloudflare.com/turnstile/troubleshooting/testing/

## Wrangler CLI

```bash
# Available via npx (v1.x legacy)
npx wrangler --version

# Note: Turnstile management requires the Cloudflare dashboard or API with an
# account-level API token. The Turnstile keys in .env.local are widget-level
# (site key + secret), not account-level API tokens.
```

## DNS Management

Domain `fuzzycatapp.com` DNS is on **Namecheap** (registrar-servers.com nameservers),
NOT on Cloudflare. To manage DNS records, use the Namecheap dashboard or API.

## FuzzyCat-Specific

- **Site key**: `0x4AAAAAACgH2wVefrJpTaCh`
- **Used on**: Login, signup, forgot-password, enrollment forms
- **Key files**: `components/shared/captcha.tsx`, `lib/turnstile.ts`
- **CSP**: Turnstile requires `https://challenges.cloudflare.com` in script-src
