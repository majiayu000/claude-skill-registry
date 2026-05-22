---
name: deploy-ops
description: Deployment and DevOps automation skill for Fixlify. Automatically activates for deployment discussions, CI/CD, infrastructure, Vercel, Supabase migrations, and production releases. Handles staging, production, and rollback workflows.
version: 1.0.0
author: Fixlify Team
tags: [deployment, devops, vercel, supabase, ci-cd, infrastructure]
---

# Deploy Ops Skill

You are a senior DevOps engineer managing deployments for Fixlify's production infrastructure.

## Infrastructure Overview

```
┌─────────────────────────────────────────────────────────────┐
│                      FIXLIFY INFRASTRUCTURE                  │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐     ┌──────────────┐     ┌─────────────┐ │
│  │   Vercel     │     │   Supabase   │     │   External  │ │
│  │  (Frontend)  │────▶│  (Backend)   │────▶│   Services  │ │
│  └──────────────┘     └──────────────┘     └─────────────┘ │
│        │                    │                     │         │
│        ▼                    ▼                     ▼         │
│  - React App          - PostgreSQL          - Telnyx SMS    │
│  - Static Assets      - Edge Functions      - Mailgun       │
│  - API Routes         - Auth                - Stripe        │
│  - Preview Deploys    - Storage             - OpenAI        │
│                       - Realtime                            │
└─────────────────────────────────────────────────────────────┘
```

## Deployment Environments

| Environment | URL | Branch | Auto Deploy |
|-------------|-----|--------|-------------|
| Production | fixlify.app | main | Yes |
| Staging | staging.fixlify.app | staging | Yes |
| Preview | *.vercel.app | PR branches | Yes |

## Pre-Deployment Checklist

### Code Quality
- [ ] All tests pass (`npm test`)
- [ ] TypeScript compiles (`npm run build`)
- [ ] No linting errors (`npm run lint`)
- [ ] IDE diagnostics clean

### Database
- [ ] Migrations tested locally
- [ ] RLS policies reviewed
- [ ] No breaking schema changes (or migration plan ready)
- [ ] Backup created for production

### Security
- [ ] No secrets in code
- [ ] Environment variables set
- [ ] API keys rotated if needed

## Deployment Commands

### Vercel (Frontend)

```bash
# Preview deployment (automatic on PR)
git push origin feature/branch

# Production deployment
git checkout main
git merge staging
git push origin main

# Manual deployment
vercel --prod

# Rollback
vercel rollback
```

### Supabase (Backend)

```bash
# Link to project
supabase link --project-ref mqppvcrlvsgrsqelglod

# Push migrations to staging
supabase db push --db-url "postgres://..."

# Push to production
supabase db push

# Deploy edge functions
supabase functions deploy function-name

# Deploy all functions
supabase functions deploy
```

## Migration Workflow

### Creating Migrations

```bash
# Create new migration
supabase migration new migration_name

# Generate from diff
supabase db diff -f migration_name

# Test locally
supabase db reset
```

### Migration Best Practices

1. **Always reversible**: Include rollback SQL
2. **Small changes**: One concern per migration
3. **Test thoroughly**: Run on staging first
4. **Document**: Clear comments in SQL

```sql
-- Migration: add_client_tags
-- Description: Add tags support for clients
-- Rollback: DROP TABLE IF EXISTS client_tags;

CREATE TABLE IF NOT EXISTS client_tags (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  client_id UUID REFERENCES clients(id) ON DELETE CASCADE,
  tag TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- RLS
ALTER TABLE client_tags ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can manage own organization tags"
ON client_tags FOR ALL
USING (
  client_id IN (
    SELECT id FROM clients
    WHERE organization_id = (SELECT organization_id FROM profiles WHERE id = auth.uid())
  )
);
```

## Edge Function Deployment

### Function Structure
```
supabase/functions/
├── _shared/           # Shared utilities
│   ├── cors.ts
│   └── supabase-client.ts
├── function-name/
│   └── index.ts
└── .env              # Local env vars
```

### Deployment
```bash
# Single function
supabase functions deploy send-sms --no-verify-jwt

# All functions
supabase functions deploy

# Set secrets
supabase secrets set KEY=value
```

## Monitoring & Rollback

### Health Checks

```bash
# Check Vercel status
curl -I https://fixlify.app/api/health

# Check Supabase
curl -I https://mqppvcrlvsgrsqelglod.supabase.co/rest/v1/

# Check Edge Functions
curl https://mqppvcrlvsgrsqelglod.supabase.co/functions/v1/health
```

### Rollback Procedures

#### Frontend (Vercel)
```bash
# List deployments
vercel ls

# Rollback to previous
vercel rollback

# Rollback to specific deployment
vercel rollback [deployment-url]
```

#### Database (Supabase)
```sql
-- Check migration history
SELECT * FROM supabase_migrations.schema_migrations ORDER BY version DESC;

-- Manual rollback (use with caution)
-- Execute rollback SQL from migration file
```

## CI/CD Pipeline

### GitHub Actions Workflow

```yaml
name: Deploy

on:
  push:
    branches: [main, staging]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - run: npm run lint
      - run: npm run build
      - run: npm test

  deploy-staging:
    needs: test
    if: github.ref == 'refs/heads/staging'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: supabase/setup-cli@v1
      - run: supabase link --project-ref ${{ secrets.SUPABASE_PROJECT_ID }}
      - run: supabase db push
      - run: supabase functions deploy

  deploy-production:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: actions/checkout@v4
      - uses: supabase/setup-cli@v1
      - run: supabase link --project-ref ${{ secrets.SUPABASE_PROJECT_ID }}
      - run: supabase db push
      - run: supabase functions deploy
```

## Emergency Procedures

### Production Down

1. **Assess**: Check Vercel and Supabase dashboards
2. **Communicate**: Update status page
3. **Rollback**: `vercel rollback` if deployment-related
4. **Investigate**: Check logs in Vercel/Supabase
5. **Fix**: Deploy hotfix through proper channels
6. **Post-mortem**: Document incident

### Database Emergency

```sql
-- Kill long-running queries
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE duration > interval '5 minutes';

-- Check connections
SELECT count(*) FROM pg_stat_activity;
```

## Environment Variables

### Vercel
```env
VITE_SUPABASE_URL=https://mqppvcrlvsgrsqelglod.supabase.co
VITE_SUPABASE_ANON_KEY=...
VITE_STRIPE_PUBLISHABLE_KEY=...
```

### Supabase Secrets
```bash
supabase secrets list
supabase secrets set OPENAI_API_KEY=...
supabase secrets set TELNYX_API_KEY=...
supabase secrets set MAILGUN_API_KEY=...
```
