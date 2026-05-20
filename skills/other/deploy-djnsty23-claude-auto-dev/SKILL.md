---
name: deploy
description: Deploy workflow for Vercel, Supabase, and CI/CD pipelines. Use for deployment and CI/CD setup.
triggers:
  - ci
  - deploy
allowed-tools: Bash
model: opus
user-invocable: true
---

# Deploy & CI/CD

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

**Token handling:** System env var may belong to a different Supabase account. Source the project's `.env` first:
```bash
export $(grep SUPABASE_ACCESS_TOKEN .env) && supabase functions deploy [name] --project-ref [ref]
```

If you get 401 Unauthorized, the token is wrong — do not retry. Check which token the project needs vs what's in the env.

## Post-deploy
1. Verify production URL loads
2. Test critical user flows
3. Monitor error logs for 5 minutes

---

## CI/CD Workflows

### Standard CI Template

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - run: npm run typecheck
      - run: npm run lint
      - run: npm run test
      - run: npm run build
```

### Vercel Deploy Workflow

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          vercel-args: '--prod'
```

### Supabase Edge Functions Deploy

```yaml
# .github/workflows/supabase.yml
name: Deploy Edge Functions

on:
  push:
    branches: [main]
    paths:
      - 'supabase/functions/**'

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: supabase/setup-cli@v1
      - run: supabase functions deploy --project-ref ${{ secrets.SUPABASE_PROJECT_REF }}
        env:
          SUPABASE_ACCESS_TOKEN: ${{ secrets.SUPABASE_ACCESS_TOKEN }}
```

## Best Practices

**DO:**
- Cache npm dependencies
- Run typecheck before tests
- Use matrix for multiple Node versions
- Add path filters for selective runs
- Store secrets in GitHub Secrets

**DON'T:**
- Commit secrets to workflow files
- Skip typecheck/lint in CI
- Use `npm install` (use `npm ci`)
- Run all jobs on every file change

## Common Fixes

| Error | Solution |
|-------|----------|
| `npm ci` fails | Check package-lock.json committed |
| Type errors | Run `npm run typecheck` locally |
| Secret missing | Add to Settings > Secrets |
| Cache miss | Check cache key matches |

## Environment Matrix

```yaml
strategy:
  matrix:
    node-version: [18, 20, 22]
    os: [ubuntu-latest, windows-latest]
```

## Quick Commands

| Say | Action |
|-----|--------|
| `add ci` | Create GitHub Actions workflow |
| `fix ci` | Debug failing workflow |
| `add deploy action` | Add deployment workflow |
