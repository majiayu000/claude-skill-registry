---
name: devops
description: Deploy to Vercel (frontends, serverless), Railway (backends, services), Supabase (database, auth, storage), GitHub Actions CI/CD. Use for deployments, infrastructure, monitoring, CI/CD.
license: MIT
version: 3.0.0
---

# DevOps Skill

Deploy and manage cloud infrastructure across Vercel, Railway, Supabase, and GitHub Actions.

## When to Use

- Deploy frontends and serverless functions to Vercel
- Deploy backend services to Railway
- Manage databases, auth, and storage with Supabase
- Set up CI/CD pipelines with GitHub Actions
- Monitor deployments and debug production issues
- Manage environment variables and secrets

## Platform Selection

| Need | Choose |
|------|--------|
| Frontend / Next.js / static sites | Vercel |
| Serverless API routes / edge functions | Vercel |
| Long-running backend services | Railway |
| Background workers / cron jobs | Railway |
| PostgreSQL database | Supabase |
| User authentication | Supabase Auth |
| File/image storage | Supabase Storage |
| Realtime subscriptions | Supabase Realtime |
| Edge functions (Deno) | Supabase Edge Functions |
| CI/CD pipelines | GitHub Actions |

## Quick Start

```bash
# Vercel - deploy frontend
vercel deploy              # Preview deployment
vercel deploy --prod       # Production deployment

# Railway - deploy backend
railway up                 # Deploy current directory
railway logs               # View service logs

# Supabase - manage database
supabase db push           # Push migrations to remote
supabase migration new feat_name  # Create new migration

# GitHub Actions - CI/CD
gh workflow run deploy.yml  # Trigger workflow manually
gh run list                # View recent runs
```

## Command Reference

### Vercel

```bash
# Deployments
vercel deploy                           # Deploy to preview
vercel deploy --prod                    # Deploy to production
vercel ls                               # List recent deployments
vercel inspect <url>                    # Deployment details
vercel logs <url>                       # View function logs
vercel redeploy                         # Redeploy latest

# Environment variables
vercel env pull .env.local              # Pull env vars locally
vercel env add SECRET_KEY               # Add env var (interactive)
vercel env rm SECRET_KEY                # Remove env var

# Project management
vercel link                             # Link local dir to project
vercel project ls                       # List all projects

# Domains
vercel domains add example.com          # Add custom domain
vercel domains ls                       # List domains
```

### Railway

```bash
# Deployments
railway up                              # Deploy current directory
railway up --detach                     # Deploy without tailing logs
railway logs                            # View service logs
railway logs --tail                     # Follow live logs
railway status                          # Service status

# Environment variables
railway variables                       # List all env vars
railway variables set KEY=VALUE         # Set env var
railway variables get KEY               # Get specific var

# Services
railway service                         # Current service info
railway open                            # Open in browser

# Database
railway connect postgres                # Connect to Postgres shell
```

### Supabase

```bash
# Database
supabase db push                        # Push migrations to remote
supabase db reset                       # Reset LOCAL db only (never production!)
supabase migration new <name>           # Create migration file
supabase migration list                 # List migrations

# Edge Functions
supabase functions deploy <name>        # Deploy edge function
supabase functions serve                # Local dev server
supabase functions list                 # List deployed functions

# Auth
supabase auth list                      # List auth providers

# Storage
supabase storage create <bucket>        # Create storage bucket

# General
supabase link --project-ref <ref>       # Link to remote project
supabase db diff                        # Show schema diff
supabase gen types typescript           # Generate TS types from schema
```

### GitHub Actions

```bash
# Workflows
gh workflow list                        # List all workflows
gh workflow run <name>                  # Trigger workflow
gh run list                             # List recent runs
gh run view <id>                        # View run details
gh run view <id> --log                  # View run logs
gh run watch                            # Watch running workflow

# Secrets
gh secret set SECRET_KEY                # Set repo secret
gh secret list                          # List secrets
```

## Best Practices

**Security:** Never commit .env files, use platform-managed secrets, rotate keys regularly, use Supabase RLS policies
**Performance:** Use Vercel edge caching, Railway health checks, Supabase connection pooling (pgBouncer)
**Cost:** Stay on free tiers when possible, monitor usage in platform dashboards, use preview deployments to test before prod
**Development:** Use `vercel dev` / `supabase start` for local development, branch deploys for PRs

## Safety Guardrails

**NEVER do these:**
- `vercel remove` / `vercel project rm` -- deletes the project
- `railway delete` -- deletes the service
- `supabase db reset` on production -- destroys all data
- Commit secrets to git -- use platform env vars instead

**ALWAYS do these:**
- Test on preview/staging before production
- Use migrations for database changes (never raw SQL on prod)
- Keep deployment logs for debugging
- Set up health check endpoints

## Resources

- Vercel: https://vercel.com/docs
- Railway: https://docs.railway.com
- Supabase: https://supabase.com/docs
- GitHub Actions: https://docs.github.com/en/actions
