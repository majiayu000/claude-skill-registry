---
name: wrangler-deploy
description: Cloudflare Wrangler deployment patterns for Pitchey. Activates when deploying, publishing, or releasing to Cloudflare Pages or Workers.
triggers:
  - deploy
  - wrangler
  - publish
  - cloudflare
  - pages
  - production
  - release
---

# Pitchey Deployment Patterns

## Project Details
- Frontend Project: `pitchey-5o8` (Cloudflare Pages)
- Worker Name: `pitchey-api-prod`
- Production API: https://pitchey-api-prod.ndlovucavelle.workers.dev
- Production Frontend: https://pitchey-5o8.pages.dev

## Deployment Commands

### Frontend (Pages)
```bash
# Build first
cd frontend && npm run build

# Preview deploy (get unique URL for testing)
npx wrangler pages deploy dist --project-name pitchey-5o8

# Production deploy (main branch)
npx wrangler pages deploy dist --project-name pitchey-5o8 --branch main

# Check deployment status
npx wrangler pages deployment list --project-name pitchey-5o8
```

### Backend (Workers)
```bash
cd worker
npx wrangler deploy --env production

# Verify deployment
curl -I https://pitchey-api-prod.ndlovucavelle.workers.dev/health
```

### Full Deploy Sequence
```bash
# 1. Build frontend
cd frontend && npm run build

# 2. Deploy frontend to production
npx wrangler pages deploy dist --project-name pitchey-5o8 --branch main

# 3. Deploy Worker API
cd ../worker && npx wrangler deploy --env production

# 4. Verify both
curl -s https://pitchey-api-prod.ndlovucavelle.workers.dev/health | jq
curl -s -o /dev/null -w "%{http_code}" https://pitchey-5o8.pages.dev
```

## Pre-Deploy Checklist
1. Run `npm run build` - must succeed with no errors
2. Run `npx wrangler types` if wrangler.jsonc bindings changed
3. Test locally with `npx wrangler dev --remote`
4. Deploy to preview first, test, then deploy to production

## Post-Deploy Verification
```bash
# Stream logs for errors (keep running)
npx wrangler tail pitchey-api-prod --status error --format pretty

# Quick health check
curl -s https://pitchey-api-prod.ndlovucavelle.workers.dev/health | jq

# Test key endpoints
curl -s "https://pitchey-api-prod.ndlovucavelle.workers.dev/api/browse?tab=trending&limit=1" | jq
```

## Rollback Procedures
```bash
# Rollback Worker to previous version
npx wrangler rollback

# List deployments to find version
npx wrangler deployments list

# Rollback to specific version
npx wrangler rollback --version VERSION_ID

# Pages rollback: redeploy previous git commit
git checkout PREVIOUS_COMMIT
npm run build
npx wrangler pages deploy dist --project-name pitchey-5o8 --branch main
```

## Common Deployment Issues

### Binding errors after deploy
```bash
npx wrangler types  # Regenerate types
```

### 500 errors after deploy
```bash
npx wrangler tail pitchey-api-prod --status error  # Check stack traces
```

### CORS errors
- Verify origins in wrangler.jsonc match frontend URL
- Check `Access-Control-Allow-Credentials: true` is set

### Build failures
- Check Node version matches (use 18+)
- Clear node_modules and reinstall: `rm -rf node_modules && npm install`