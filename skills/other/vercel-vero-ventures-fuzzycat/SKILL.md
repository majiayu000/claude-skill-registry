---
name: vercel
description: >
  Manage Vercel deployments via CLI. Check deployment status, view logs, manage environment
  variables, inspect domains, trigger builds, and debug production issues.
  Use for any deployment or hosting task.
allowed-tools: Bash, Read, Grep, Glob
---

# Vercel CLI

Manage FuzzyCat's Vercel deployments. The CLI is installed at `~/.bun/bin/vercel` and
already authenticated.

## Common Commands

### Deployments

```bash
# List recent deployments
vercel ls

# Get latest deployment URL
vercel ls --json 2>/dev/null | python3 -c "
import sys,json
deploys=json.load(sys.stdin)
if deploys: print(f\"{deploys[0]['url']} | {deploys[0]['state']} | {deploys[0]['createdAt']}\")"

# Get deployment details
vercel inspect <deployment-url>

# View deployment logs
vercel logs <deployment-url>

# View real-time logs (streaming)
vercel logs <deployment-url> --follow
```

### Environment Variables

```bash
# List all env vars
vercel env ls

# List env vars for specific environment
vercel env ls --environment production

# Pull env vars to a file
vercel env pull /tmp/prod-env.txt --environment production

# Add an env var (all environments)
vercel env add VAR_NAME

# Add env var for specific environment
vercel env add VAR_NAME production

# Remove an env var
vercel env rm VAR_NAME
```

### Domains

```bash
# List domains
vercel domains ls

# Inspect domain
vercel domains inspect fuzzycatapp.com

# Add a domain
vercel domains add subdomain.fuzzycatapp.com
```

### Projects

```bash
# Project info
vercel project ls

# Link current directory to project
vercel link
```

### Manual Deployment

```bash
# Deploy to preview
vercel

# Deploy to production (prefer auto-deploy via git push)
vercel --prod

# Note: Auto-deploys from GitHub are the standard workflow.
# Manual vercel --prod should be avoided unless auto-deploys are broken.
```

### Debugging

```bash
# Check build output
vercel logs <url> --output json 2>/dev/null | python3 -c "
import sys,json
for line in sys.stdin:
    try:
        entry = json.loads(line)
        if entry.get('type') == 'error':
            print(f\"ERROR: {entry.get('text','')}\")
    except: pass"

# Check function logs (serverless)
vercel logs <url> --follow

# Check if deployment is healthy
curl -sL https://www.fuzzycatapp.com/api/health | python3 -m json.tool
```

## Production Checks

```bash
# Quick health check
curl -sL https://www.fuzzycatapp.com/api/health | jq .status

# Check API v1
curl -sL https://www.fuzzycatapp.com/api/v1/health | python3 -m json.tool

# Check deployment status
vercel ls 2>/dev/null | head -5
```

## FuzzyCat-Specific

- **Project**: `fuzzy-cat-apps-projects/fuzzycat`
- **Production URL**: `https://www.fuzzycatapp.com`
- **Framework**: Next.js (auto-detected by Vercel)
- **Build command**: `next build` (Vercel default)
- **Preview deploys**: Currently disabled via `vercel.json` `ignoreCommand`
- **Auto-deploys**: Triggered by pushes to `main` branch on GitHub
- **Environments**: Development, Preview, Production (each with separate env vars)
