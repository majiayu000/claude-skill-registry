# CI/CD Skill — GitHub Actions & Deployment Pipelines

## When to Use

Reference this skill when:

- Setting up GitHub Actions workflows
- Configuring PR checks and status gates
- Setting up preview deployments
- Configuring production deployment pipelines
- Adding automated testing to CI

## GitHub Actions Patterns

### PR Check Workflow

```yaml
# .github/workflows/pr-check.yml
name: PR Check

on:
  pull_request:
    branches: [main]

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  lint-and-type:
    name: Lint & Type Check
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: oven-sh/setup-bun@v2
      - run: bun install --frozen-lockfile
      - run: bun lint
      - run: bun typecheck

  test:
    name: Unit Tests
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: oven-sh/setup-bun@v2
      - run: bun install --frozen-lockfile
      - run: bun test --coverage
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: coverage
          path: coverage/

  e2e:
    name: E2E Tests
    runs-on: ubuntu-latest
    needs: [lint-and-type]
    steps:
      - uses: actions/checkout@v4
      - uses: oven-sh/setup-bun@v2
      - run: bun install --frozen-lockfile
      - run: bunx playwright install --with-deps chromium
      - run: bun test:e2e
      - uses: actions/upload-artifact@v4
        if: failure()
        with:
          name: playwright-report
          path: playwright-report/

  security:
    name: Security Audit
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: oven-sh/setup-bun@v2
      - run: bun install --frozen-lockfile
      - run: bun audit || true
      - name: Check for secrets
        run: |
          if grep -rn "sk_live\|pk_live\|ghp_\|AKIA" --include="*.ts" --include="*.tsx" --include="*.js" --include="*.env*" .; then
            echo "::error::Potential secrets found in code"
            exit 1
          fi
```

### Preview Deployment Workflow

```yaml
# .github/workflows/preview.yml
name: Preview Deploy

on:
  pull_request:
    branches: [main]

jobs:
  deploy:
    name: Deploy Preview
    runs-on: ubuntu-latest
    permissions:
      pull-requests: write
    steps:
      - uses: actions/checkout@v4
      - uses: oven-sh/setup-bun@v2
      - run: bun install --frozen-lockfile
      - uses: amondnet/vercel-action@v25
        id: deploy
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
      - uses: actions/github-script@v7
        with:
          script: |
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: `Preview deployed: ${{ steps.deploy.outputs.preview-url }}`
            })
```

### Production Deployment Workflow

```yaml
# .github/workflows/production.yml
name: Production Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    name: Deploy Production
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: actions/checkout@v4
      - uses: oven-sh/setup-bun@v2
      - run: bun install --frozen-lockfile
      - run: bun test
      - run: bun build
      - uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          vercel-args: "--prod"
```

## Branch Protection Rules

Configure on GitHub:

```
Branch: main
- Require PR reviews: 1
- Require status checks: lint-and-type, test, security
- Require branches to be up to date
- No force pushes
- No deletions

Branch: prod
- Require PR reviews: 2
- Require all status checks
- Restrict who can push: release team only
```

## Environment Variables

### Required Secrets (GitHub Settings > Secrets)

```
VERCEL_TOKEN          — Vercel deployment token
VERCEL_ORG_ID         — Vercel organization ID
VERCEL_PROJECT_ID     — Vercel project ID
DATABASE_URL          — PostgreSQL connection string (for E2E)
```

### Environment Protection Rules

```
production:
  - Required reviewers: 1+
  - Wait timer: 5 minutes (optional)
  - Deployment branches: main only
```

## Caching Strategy

```yaml
# Bun cache for faster CI
- uses: actions/cache@v4
  with:
    path: ~/.bun/install/cache
    key: ${{ runner.os }}-bun-${{ hashFiles('bun.lockb') }}
    restore-keys: |
      ${{ runner.os }}-bun-
```

## Database Migrations in CI

```yaml
# Run migrations before E2E tests
- name: Run migrations
  run: bunx prisma migrate deploy
  env:
    DATABASE_URL: ${{ secrets.DATABASE_URL }}

# Validate schema matches
- name: Validate Prisma schema
  run: bunx prisma validate
```

## Monitoring Deployment Health

After deploying, verify the deployment:

```yaml
- name: Health check
  run: |
    for i in {1..10}; do
      STATUS=$(curl -s -o /dev/null -w "%{http_code}" ${{ steps.deploy.outputs.preview-url }}/api/health)
      if [ "$STATUS" = "200" ]; then
        echo "Health check passed"
        exit 0
      fi
      sleep 5
    done
    echo "Health check failed"
    exit 1
```

## Key Principles

1. **Fast feedback** — Lint and type check run first (fastest), E2E last (slowest)
2. **Cancel in progress** — New pushes cancel old CI runs on same PR
3. **Fail fast** — Security and lint block before expensive test runs
4. **Cache aggressively** — Bun cache, Playwright browser cache
5. **Environment gates** — Production requires human approval
6. **No secrets in code** — Use GitHub Secrets, never commit credentials
