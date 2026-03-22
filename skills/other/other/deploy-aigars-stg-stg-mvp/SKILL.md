---
name: deploy
description: Deploy Second Turn Games to Vercel with pre-flight checks
invocation: user
---

# Deployment Helper

You are a deployment assistant for Second Turn Games deployed on Vercel.

Vercel deploys automatically from the `main` branch. Deployment = pushing to main.

## Pre-Flight Checks (MANDATORY — run before any push to main)

Run these in order. **Stop and fix any failure before continuing.**

```bash
pnpm build:marketplace   # Runs next build — catches ESLint, hook ordering, type errors
pnpm type-check          # Redundant but fast; catches any remaining TS issues
git status               # Verify no uncommitted changes
```

> `pnpm build:marketplace` is the definitive gate. It runs the full Next.js build including ESLint. `pnpm type-check` alone does NOT catch ESLint violations (e.g. hooks-rules-of-hooks, unused vars).

If `pnpm build:marketplace` fails, fix the errors first. Do not push.

## Deployment (git push to main)

```bash
git push origin staging
git checkout main
git merge staging --ff-only
git push origin main
git checkout staging
```

This is the only deployment mechanism. Do not use `npx vercel --prod` — it bypasses the monorepo build pipeline.

## Environment Variables

Ensure these are configured in Vercel dashboard:

**Required:**
- `NEXT_PUBLIC_SUPABASE_URL`
- `NEXT_PUBLIC_SUPABASE_ANON_KEY`
- `SUPABASE_SERVICE_ROLE_KEY`
- `RESEND_API_KEY`
- `RESEND_FROM_EMAIL`
- `NEXT_PUBLIC_APP_URL`
- `TURNSTILE_SECRET_KEY`
- `NEXT_PUBLIC_TURNSTILE_SITE_KEY`

**Payments (EveryPay):**
- `EVERYPAY_API_URL`
- `EVERYPAY_API_USERNAME`
- `EVERYPAY_API_SECRET`
- `EVERYPAY_ACCOUNT_ID`

**Shipping (Unisend):**
- `UNISEND_API_URL`
- `UNISEND_USERNAME`
- `UNISEND_PASSWORD`

**Production Only:**
- `CRON_SECRET`

## Post-Deployment Verification

After pushing, use Vercel MCP to monitor the deployment:

1. `list_deployments` — confirm new deployment triggered on main
2. `get_deployment_build_logs` — watch for build errors
3. Check deployment URL is accessible
4. Verify `/api/health` endpoint responds

## Vercel Project Info

- Project: `stg-mvp-marketplace`
- Org: `team_wtOtQ06JFYv0bQM0kq5P64RF`
