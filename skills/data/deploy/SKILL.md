---
name: deploy
description: Deploy workflow for Vercel and Supabase Edge Functions
allowed-tools: Bash
model: sonnet
user-invocable: false
---

# Deploy Workflow

## Pre-deploy Checklist
1. `npm run typecheck` - passes
2. `npm run build` - passes
3. `npm run test` - passes (if available)
4. No `console.log` in production code
5. Environment variables set in hosting platform

## Vercel

**Preview:**
```bash
npx vercel --yes
```

**Production:**
```bash
npx vercel --prod --yes
```

## Supabase Edge Functions

**Single function:**
```bash
supabase functions deploy [name] --project-ref [ref]
```

**All functions:**
```bash
supabase functions deploy --project-ref [ref]
```

## Post-deploy
1. Verify production URL loads
2. Test critical user flows
3. Monitor error logs for 5 minutes
