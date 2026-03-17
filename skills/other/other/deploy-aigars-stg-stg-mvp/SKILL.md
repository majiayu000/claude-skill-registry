---
name: deploy
description: Deploy Second Turn Games to Vercel with pre-flight checks
invocation: user
---

# Deployment Helper

You are a deployment assistant for Second Turn Games deployed on Vercel.

## Pre-Deployment Checklist

Before deploying, run these verifications:

1. **Build design system first**: `pnpm build:ds`
2. **Build marketplace**: `pnpm build:marketplace`
3. **Type check**: `pnpm type-check`
4. **Lint**: `pnpm lint`
5. **Check for uncommitted changes**: `git status`

If any check fails, report the error and help fix it before proceeding.

## Deployment Commands

| Environment | Command | Notes |
|-------------|---------|-------|
| Preview | `npx vercel` | Creates preview deployment |
| Production | `npx vercel --prod` | Deploys to production (requires confirmation) |

## Environment Variables

Ensure these are configured in Vercel dashboard:

**Required:**
- `NEXT_PUBLIC_SUPABASE_URL`
- `NEXT_PUBLIC_SUPABASE_ANON_KEY`
- `SUPABASE_SERVICE_ROLE_KEY`
- `STRIPE_SECRET_KEY`
- `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY`
- `RESEND_API_KEY`
- `RESEND_FROM_EMAIL`
- `NEXT_PUBLIC_APP_URL`
- `TURNSTILE_SECRET_KEY`
- `NEXT_PUBLIC_TURNSTILE_SITE_KEY`

**Shipping (Unisend):**
- `UNISEND_API_URL`
- `UNISEND_USERNAME`
- `UNISEND_PASSWORD`

**Production Only:**
- `CRON_SECRET`

## Post-Deployment Verification

After deployment:
1. Check deployment URL is accessible
2. Verify `/api/health` endpoint responds
3. Test locale routing: `/en`, `/lv`, `/lt`, `/et`
4. Verify Stripe webhook endpoint is reachable

## Vercel Project Info

- Project: `stg-mvp-marketplace`
- Org: `team_wtOtQ06JFYv0bQM0kq5P64RF`

Use the Vercel MCP tools to check deployment status, logs, and environment variables.
