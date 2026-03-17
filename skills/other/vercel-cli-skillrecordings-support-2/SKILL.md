---
name: vercel-cli
description: Deploy and manage Vercel projects via CLI. Use when deploying apps, managing environment variables, configuring domains, or pushing secrets to Vercel. Triggers on deploy, vercel, env vars, production.
allowed-tools: Read, Bash, Glob, Grep
---

# Vercel CLI Skill

Deploy and manage Vercel projects via CLI. Org: `skillrecordings`.

## ⚠️ CRITICAL: Environment Variable Newlines

**NEVER use heredocs (`<<<`) or plain `echo` to pipe values to `vercel env add`.**

These add trailing newlines that WILL break secrets silently:
```bash
# ❌ BAD - adds newline
echo "secret" | vercel env add MY_VAR production
vercel env add MY_VAR production <<< "secret"

# ✅ GOOD - no newline
echo -n 'secret' | vercel env add MY_VAR production
```

Always use `echo -n` (no newline flag) when piping values.

## Prerequisites

```bash
bun add -g vercel
vercel login
```

## Project Setup (Monorepo)

This is a Turborepo. Each app deploys as a separate Vercel project.

### Link all projects at once (preferred)

```bash
vercel link --repo
```

This links all apps to their Vercel projects using Git integration.

### Link individual app

```bash
cd apps/web
vercel link --project support-web
```

### First-time project creation

```bash
cd apps/web
vercel --yes
# Creates project, prompts for settings
```

## Deployments

### Preview deployment (PR/branch)

```bash
vercel
# or from root:
vercel --cwd apps/web
```

### Production deployment

```bash
vercel --prod
# or from root:
vercel --cwd apps/web --prod
```

### Deploy without waiting

```bash
vercel --no-wait
```

### Force rebuild (skip cache)

```bash
vercel --force
```

### Deploy with build logs

```bash
vercel --logs
```

## Environment Variables

### List env vars

```bash
vercel env ls
vercel env ls production
vercel env ls preview feature-branch
```

### Add env var

```bash
# Interactive (prompts for value)
vercel env add MY_VAR

# With value piped (MUST use echo -n to avoid newline!)
echo -n 'secret-value' | vercel env add MY_VAR production

# Sensitive (hidden in dashboard)
vercel env add API_KEY --sensitive
```

### Push from local .env to Vercel

To push all vars from a local .env file:

```bash
# Parse .env and push each var (excludes comments and empty lines)
while IFS='=' read -r key value; do
  [[ -z "$key" || "$key" =~ ^# ]] && continue
  echo -n "$value" | vercel env add "$key" production
done < .env.local
```

Or push specific vars:

```bash
# Read from .env.local and push to production
source .env.local
echo -n "$FRONT_API_TOKEN" | vercel env add FRONT_API_TOKEN production
echo -n "$INNGEST_SIGNING_KEY" | vercel env add INNGEST_SIGNING_KEY production
```

### Pull env vars to local file

```bash
vercel env pull .env.local
vercel env pull --environment=preview .env.preview
```

### Run command with env vars (no file)

```bash
vercel env run -- bun run dev
vercel env run -e production -- bun run build
```

### Remove env var

```bash
vercel env rm MY_VAR production
```

### Update existing env var

```bash
# Remove then add (no update command exists)
vercel env rm MY_VAR production -y
echo -n 'new-value' | vercel env add MY_VAR production
```

## Project Management

### List projects

```bash
vercel project ls
vercel project ls --json
```

### Inspect project

```bash
vercel project inspect
vercel project inspect support-web
```

### Remove project

```bash
vercel project rm support-web
```

## Domains

### List domains

```bash
vercel domains ls
```

### Webhook URLs (no wildcards)

Use the **exact** Vercel app domain for webhooks. Wildcards are not supported by most providers.

```bash
# Find the exact production domain for the current project
vercel project inspect | rg -n "Domains|domain"

# Or list deployments and pick the latest
vercel ls
```

### Add domain

```bash
vercel domains add example.com
```

### Alias deployment to domain

```bash
vercel alias <deployment-url> my-custom-domain.com
```

## Logs

### View deployment logs

```bash
vercel logs <deployment-url>
vercel logs <deployment-url> --follow
```

## CI/CD Usage

Use `VERCEL_TOKEN` env var or `--token` flag:

```bash
vercel --token $VERCEL_TOKEN --prod
```

## Monorepo vercel.json

Each app should have its own `vercel.json`:

```json
{
  "$schema": "https://openapi.vercel.sh/vercel.json",
  "framework": "nextjs"
}
```

Root `vercel.json` for shared settings (optional):

```json
{
  "$schema": "https://openapi.vercel.sh/vercel.json",
  "ignoreCommand": "npx turbo-ignore"
}
```

## Common Patterns

### Deploy only if app changed (turbo-ignore)

```bash
bun add -D turbo-ignore
```

In app's `vercel.json`:
```json
{
  "ignoreCommand": "npx turbo-ignore"
}
```

### Capture deployment URL in CI

```bash
DEPLOY_URL=$(vercel --prod 2>&1)
echo "Deployed to: $DEPLOY_URL"
```

### Promote preview to production

```bash
vercel promote <deployment-url>
```

## Scope

Always deploy to skillrecordings org:

```bash
vercel --scope skillrecordings
```

Or set globally:
```bash
vercel switch skillrecordings
```

## Troubleshooting

### Clear local Vercel cache

```bash
rm -rf .vercel
vercel link
```

### Check current link status

```bash
cat .vercel/project.json
```

### Redeploy with fresh build

```bash
vercel --force --logs
```
