# CI/CD Patterns

Continuous Integration and Deployment patterns for modern applications.

> **Template Usage:** Customize for your CI provider (GitHub Actions, GitLab CI, CircleCI) and deployment target (Vercel, AWS, etc.).

## GitHub Actions Structure

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main, dev]
  pull_request:
    branches: [main, dev]

# Cancel in-progress runs on new commits
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

env:
  NODE_VERSION: '20'
  PNPM_VERSION: '8'

jobs:
  # Lint, typecheck, test in parallel
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: pnpm/action-setup@v2
        with:
          version: ${{ env.PNPM_VERSION }}

      - uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'pnpm'

      - name: Install dependencies
        run: pnpm install --frozen-lockfile

      - name: Lint
        run: pnpm lint

      - name: Type check
        run: pnpm typecheck

      - name: Test
        run: pnpm test

  # Build to verify it works
  build:
    runs-on: ubuntu-latest
    needs: quality
    steps:
      - uses: actions/checkout@v4

      - uses: pnpm/action-setup@v2
        with:
          version: ${{ env.PNPM_VERSION }}

      - uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'pnpm'

      - name: Install dependencies
        run: pnpm install --frozen-lockfile

      - name: Build
        run: pnpm build
        env:
          DATABASE_URL: ${{ secrets.DATABASE_URL }}
```

## Caching Strategies

```yaml
# Node modules caching
- uses: actions/setup-node@v4
  with:
    node-version: '20'
    cache: 'pnpm'  # or 'npm', 'yarn'

# Custom cache for build artifacts
- name: Cache Next.js build
  uses: actions/cache@v4
  with:
    path: |
      .next/cache
    key: nextjs-${{ runner.os }}-${{ hashFiles('**/pnpm-lock.yaml') }}-${{ hashFiles('**/*.ts', '**/*.tsx') }}
    restore-keys: |
      nextjs-${{ runner.os }}-${{ hashFiles('**/pnpm-lock.yaml') }}-
      nextjs-${{ runner.os }}-

# Turbo cache for monorepos
- name: Cache Turbo
  uses: actions/cache@v4
  with:
    path: .turbo
    key: turbo-${{ runner.os }}-${{ hashFiles('**/pnpm-lock.yaml') }}-${{ github.sha }}
    restore-keys: |
      turbo-${{ runner.os }}-${{ hashFiles('**/pnpm-lock.yaml') }}-
      turbo-${{ runner.os }}-
```

## Environment Variables

```yaml
# Secrets from GitHub
env:
  DATABASE_URL: ${{ secrets.DATABASE_URL }}
  API_KEY: ${{ secrets.API_KEY }}

# Environment-specific secrets
- name: Deploy to staging
  env:
    DATABASE_URL: ${{ secrets.STAGING_DATABASE_URL }}
  run: pnpm deploy:staging

- name: Deploy to production
  env:
    DATABASE_URL: ${{ secrets.PROD_DATABASE_URL }}
  run: pnpm deploy:prod

# Using GitHub environments for approval
jobs:
  deploy-prod:
    runs-on: ubuntu-latest
    environment: production  # Requires approval
    steps:
      - run: pnpm deploy:prod
```

## Preview Deployments

```yaml
# .github/workflows/preview.yml
name: Preview Deployment

on:
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  deploy-preview:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Deploy to Vercel Preview
        uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          github-token: ${{ secrets.GITHUB_TOKEN }}
          # Creates preview URL and comments on PR

      # Or custom preview
      - name: Deploy Preview
        id: deploy
        run: |
          PREVIEW_URL=$(pnpm deploy:preview)
          echo "url=$PREVIEW_URL" >> $GITHUB_OUTPUT

      - name: Comment PR
        uses: actions/github-script@v7
        with:
          script: |
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: '🚀 Preview deployed: ${{ steps.deploy.outputs.url }}'
            })
```

## Production Deployment

```yaml
# .github/workflows/deploy.yml
name: Deploy Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: actions/checkout@v4

      - name: Setup
        uses: ./.github/actions/setup  # Reusable action

      - name: Run migrations
        run: pnpm db:migrate:deploy
        env:
          DATABASE_URL: ${{ secrets.PROD_DATABASE_URL }}

      - name: Deploy
        run: pnpm deploy:prod
        env:
          VERCEL_TOKEN: ${{ secrets.VERCEL_TOKEN }}

      - name: Notify Slack
        if: always()
        uses: 8398a7/action-slack@v3
        with:
          status: ${{ job.status }}
          fields: repo,message,commit,author
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK }}
```

## Database Migrations in CI

```yaml
# Run migrations on deploy
- name: Run database migrations
  run: |
    pnpm prisma migrate deploy
  env:
    DATABASE_URL: ${{ secrets.DATABASE_URL }}

# Generate types after migration
- name: Generate types
  run: pnpm prisma generate

# Validate migrations before merge
- name: Validate migrations
  run: |
    pnpm prisma migrate diff \
      --from-schema-datamodel prisma/schema.prisma \
      --to-schema-datasource prisma/schema.prisma \
      --exit-code
```

## Rollback Strategy

```yaml
# Manual rollback workflow
name: Rollback

on:
  workflow_dispatch:
    inputs:
      version:
        description: 'Version to rollback to'
        required: true
        type: string

jobs:
  rollback:
    runs-on: ubuntu-latest
    environment: production
    steps:
      - name: Rollback deployment
        run: |
          vercel rollback ${{ inputs.version }} --token=${{ secrets.VERCEL_TOKEN }}

      - name: Notify team
        run: |
          curl -X POST ${{ secrets.SLACK_WEBHOOK }} \
            -d '{"text":"⚠️ Production rolled back to ${{ inputs.version }}"}'
```

## Reusable Workflows

```yaml
# .github/workflows/reusable-test.yml
name: Reusable Test Workflow

on:
  workflow_call:
    inputs:
      node-version:
        required: false
        type: string
        default: '20'
    secrets:
      DATABASE_URL:
        required: true

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ inputs.node-version }}
      - run: npm ci
      - run: npm test
        env:
          DATABASE_URL: ${{ secrets.DATABASE_URL }}

# Usage in another workflow
jobs:
  test:
    uses: ./.github/workflows/reusable-test.yml
    with:
      node-version: '20'
    secrets:
      DATABASE_URL: ${{ secrets.DATABASE_URL }}
```

## Git Hooks (Lefthook)

```yaml
# lefthook.yml
pre-commit:
  parallel: true
  commands:
    lint:
      glob: "*.{js,ts,tsx}"
      run: pnpm eslint --fix {staged_files}
      stage_fixed: true

    format:
      glob: "*.{js,ts,tsx,json,md}"
      run: pnpm prettier --write {staged_files}
      stage_fixed: true

    typecheck:
      run: pnpm typecheck

pre-push:
  commands:
    test:
      run: pnpm test

    build:
      run: pnpm build
```

## Dependabot Configuration

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
      day: "monday"
    open-pull-requests-limit: 10
    groups:
      # Group minor/patch updates
      dependencies:
        patterns:
          - "*"
        update-types:
          - "minor"
          - "patch"
    ignore:
      # Ignore major updates for stability
      - dependency-name: "*"
        update-types: ["version-update:semver-major"]

  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
```

## Matrix Builds

```yaml
# Test across multiple versions
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: [18, 20, 22]
        os: [ubuntu-latest, macos-latest]
      fail-fast: false  # Continue other jobs if one fails

    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
      - run: npm ci
      - run: npm test
```

## Notifications

```yaml
# Slack notification
- name: Slack Notification
  uses: 8398a7/action-slack@v3
  with:
    status: ${{ job.status }}
    fields: repo,message,commit,author,action,eventName,ref,workflow
  env:
    SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK }}
  if: always()

# Discord notification
- name: Discord Notification
  uses: sarisia/actions-status-discord@v1
  if: always()
  with:
    webhook: ${{ secrets.DISCORD_WEBHOOK }}
    status: ${{ job.status }}

# GitHub comment on PR
- name: Comment on PR
  uses: actions/github-script@v7
  if: github.event_name == 'pull_request'
  with:
    script: |
      github.rest.issues.createComment({
        issue_number: context.issue.number,
        owner: context.repo.owner,
        repo: context.repo.repo,
        body: '✅ All checks passed!'
      })
```

## Checklist

### Workflow Structure
- [ ] Concurrency configured to cancel stale runs
- [ ] Jobs run in parallel where possible
- [ ] Dependencies between jobs defined
- [ ] Timeouts configured

### Caching
- [ ] Node modules cached
- [ ] Build artifacts cached
- [ ] Cache keys include lockfile hash

### Security
- [ ] Secrets stored in GitHub Secrets
- [ ] Environment-specific secrets
- [ ] Production requires approval
- [ ] Dependabot configured

### Quality Gates
- [ ] Lint runs on all PRs
- [ ] Type check runs on all PRs
- [ ] Tests run on all PRs
- [ ] Build verified before merge

### Deployment
- [ ] Preview deployments for PRs
- [ ] Auto-deploy main to production
- [ ] Database migrations automated
- [ ] Rollback strategy defined

### Notifications
- [ ] Team notified on failures
- [ ] Deployment status posted
- [ ] PR comments for preview URLs
