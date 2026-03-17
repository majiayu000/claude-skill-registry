---
name: deploy-automation
description: |
  One-click deploy to production. User just says "deploy".
  Use when: user wants to publish their app.
  Triggers: "deploy", "publish", "go live", "опубликуй".
---

# Deploy Automation

Deploy to production with one command.

## Platform Selection

Based on template:

| Template | Platform | Why |
|----------|----------|-----|
| nextjs-supabase | Vercel | Native Next.js support |
| fastapi-postgres | Fly.io | Docker + persistent DB |
| hono-drizzle | Cloudflare | Edge-native |
| landing-page | Netlify/Vercel | Static hosting |

## Deploy Process

### Vercel (Next.js)
1. Check Vercel CLI installed
2. Set environment variables
3. `vercel --prod`
4. Return production URL

### Fly.io (FastAPI)
1. Generate Dockerfile if missing
2. Create fly.toml
3. Set secrets
4. `fly deploy`
5. Return production URL

### Cloudflare (Hono)
1. Configure wrangler.toml
2. Set secrets
3. `wrangler deploy`
4. Return workers.dev URL

### Netlify (Static)
1. Build static files
2. `netlify deploy --prod`
3. Return production URL

## Pre-Deploy Checks

- [ ] All tests pass
- [ ] No console.log
- [ ] Environment variables set
- [ ] Build succeeds
- [ ] No security issues

## Environment Variables

Template for each platform:

```bash
# Supabase
NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_SUPABASE_ANON_KEY=
SUPABASE_SERVICE_ROLE_KEY=

# PostgreSQL
DATABASE_URL=
SECRET_KEY=

# General
NODE_ENV=production
```

## User Experience

User: "Deploy this"

1. "Deploying to [platform]..."
2. Run pre-deploy checks
3. Build production
4. Deploy
5. "✅ Live at https://your-app.vercel.app"

## Custom Domains

After initial deploy:
- "Add domain" → configure DNS
- Auto-SSL via platform
- "✅ Live at https://yourdomain.com"
