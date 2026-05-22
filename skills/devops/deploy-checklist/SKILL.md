---
name: deploy-checklist
description: Pre-deployment verification for Vercel-hosted Next.js projects. Use before deploying or when user mentions deploy, ship, or release.
---
# Deploy Checklist

Before any deployment, verify:

## Code Quality
1. Run `npm run typecheck` — zero errors
2. Run `npm run lint` — zero warnings
3. Run `npm test` — all passing

## Environment
4. Check `.env.example` is up to date with any new variables
5. Verify Vercel environment variables are set for production
6. Confirm no hardcoded localhost URLs or dev API keys

## Database
7. Run `npx prisma migrate status` — no pending migrations
8. Verify migration is safe (no destructive changes without confirmation)

## Stripe (if SkillsFrame)
9. Confirm webhook endpoint is registered in Stripe dashboard
10. Verify webhook signing secret is in production env

## Final
11. Create a git tag: `git tag -a v{version} -m "Release {version}"`
12. Push: `git push origin main --tags`

Report any failures. Do NOT proceed if any check fails.
