---
name: deployment-audit-skill
description: Use DigitalOcean MCP and related tools to check deployment health, crash logs, environment consistency, and runtime issues for Unite-Hub / Synthex. Use when diagnosing deployment failures or verifying readiness.
allowed-tools: Run, Read
---

# Deployment Audit Skill

## Purpose
Continuously monitor and troubleshoot deployments on DigitalOcean and Vercel for Synthex / Unite-Hub.

## Typical Tasks
1. Retrieve crash logs via DO CLI / MCP
   - `doctl apps list`
   - `doctl apps logs <app-id> --type=run_restarted`
   - `doctl apps logs <app-id> <component> --type=run_restarted`
2. Check environment variable consistency across:
   - `.env.local`
   - Vercel project settings
   - DigitalOcean app spec
3. Validate:
   - Correct Supabase URLs and keys
   - Correct Stripe keys (test vs live)
   - Correct callback/redirect URLs

## Output
- Human-readable audit summary in `docs/audit/DEPLOYMENT_HEALTH.md`
- Issue entries in `docs/audit/AUDIT_ISSUES_REGISTRY.json`

## Environment Checklist

### Required Variables
```
NEXT_PUBLIC_SUPABASE_URL
NEXT_PUBLIC_SUPABASE_ANON_KEY
SUPABASE_SERVICE_ROLE_KEY
NEXTAUTH_URL
NEXTAUTH_SECRET
GOOGLE_CLIENT_ID
GOOGLE_CLIENT_SECRET
ANTHROPIC_API_KEY
```

### Optional Variables
```
STRIPE_SECRET_KEY
STRIPE_WEBHOOK_SECRET
SENDGRID_API_KEY
RESEND_API_KEY
SEMRUSH_API_KEY
DATAFORSEO_LOGIN
DATAFORSEO_PASSWORD
```

## Health Check Process

### Step 1: Environment Sync
Compare variables across:
- Local `.env.local`
- Vercel environment variables
- DigitalOcean app spec

Flag mismatches.

### Step 2: Build Verification
- Run `npm run build`
- Check for TypeScript errors
- Check for missing dependencies
- Verify all routes compile

### Step 3: Runtime Validation
- Check recent deploy logs
- Look for crash patterns
- Identify memory/CPU spikes
- Flag slow endpoints

### Step 4: API Health
- Ping key API endpoints
- Verify authentication works
- Check database connectivity
- Validate external service connections

## Common Issues & Fixes

### Issue: "Module not found"
**Cause**: Missing dependency
**Fix**: `npm install <module>`

### Issue: "Invalid environment variable"
**Cause**: Variable not set or wrong format
**Fix**: Check `.env.local` and deployment settings

### Issue: "Memory limit exceeded"
**Cause**: Heavy computation or memory leak
**Fix**: Optimize code, increase limit, or add caching

### Issue: "Database connection timeout"
**Cause**: Too many connections or network issue
**Fix**: Enable connection pooling, check Supabase status
