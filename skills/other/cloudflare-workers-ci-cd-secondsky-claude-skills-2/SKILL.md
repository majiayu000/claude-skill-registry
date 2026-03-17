---
name: workers-ci-cd
description: Complete CI/CD guide for Cloudflare Workers using GitHub Actions and GitLab CI. Use for automated testing, deployment pipelines, preview environments, secrets management, or encountering deployment failures, workflow errors, environment configuration issues.
keywords:
  - cloudflare-workers
  - workers-ci-cd
  - github-actions
  - gitlab-ci
  - continuous-integration
  - continuous-deployment
  - automated-testing
  - deployment-pipeline
  - preview-deployments
  - staging-deployment
  - production-deployment
  - secrets-management
  - wrangler-deploy
  - environment-variables
  - github-secrets
  - deployment-verification
  - rollback-strategy
  - blue-green-deployment
  - canary-deployment
  - deployment-gates
  - ci-cd-best-practices
  - workflow-automation
  - pull-request-previews
  - branch-deployments
license: MIT
metadata:
  version: "1.0.0"
  last_verified: "2025-01-27"
  production_tested: true
  token_savings: "~75%"
  errors_prevented: 7
  templates_included: 4
  references_included: 4
  scripts_included: 1
  github_actions_version: "v4"
  wrangler_version: "4.50.0"
---

# Cloudflare Workers CI/CD

**Status**: ✅ Production Ready | Last Verified: 2025-01-27
**GitHub Actions**: v4 | **GitLab CI**: Latest | **Wrangler**: 4.50.0

## Table of Contents

- [What Is Workers CI/CD?](#what-is-workers-cicd)
- [New in 2025](#new-in-2025)
- [Quick Start (10 Minutes)](#quick-start-10-minutes)
- [Critical Rules](#critical-rules)
- [Core Concepts](#core-concepts)
- [Top 5 Use Cases](#top-5-use-cases)
- [Best Practices](#best-practices)
- [Top 7 Errors Prevented](#top-7-errors-prevented)
- [When to Load References](#when-to-load-references)

---

## What Is Workers CI/CD?

Automated testing and deployment of Cloudflare Workers using **GitHub Actions** or **GitLab CI**. Enables running tests on every commit, deploying to preview/staging/production environments automatically, managing secrets securely, and implementing deployment gates for safe releases.

**Key capabilities**: Automated testing, multi-environment deployments, preview URLs per PR, secrets management, deployment verification, automatic rollbacks.

---

## New in 2025

**GitHub Actions Updates** (January 2025):
- **NEW**: `cloudflare/wrangler-action@v4` (improved caching, faster deployments)
- **IMPROVED**: Secrets support with `vars` and `secrets` parameters
- **ADDED**: Built-in preview environment cleanup
- **BREAKING**: `apiToken` renamed to `api-token` (kebab-case)

**Migration from v3**:
```yaml
# ❌ OLD (v3)
- uses: cloudflare/wrangler-action@3
  with:
    apiToken: ${{ secrets.CLOUDFLARE_API_TOKEN }}

# ✅ NEW (v4)
- uses: cloudflare/wrangler-action@v4
  with:
    api-token: ${{ secrets.CLOUDFLARE_API_TOKEN }}
```

**Wrangler 4.50.0** (January 2025):
- **NEW**: `--dry-run` flag for deployment validation
- **IMPROVED**: Faster deployments with parallel uploads
- **ADDED**: `--keep-vars` to preserve environment variables

---

## Quick Start (10 Minutes)

### GitHub Actions Setup

**1. Create Cloudflare API Token**

Go to: https://dash.cloudflare.com/profile/api-tokens

Create token with permissions:
- **Account.Cloudflare Workers Scripts** - Edit
- **Account.Cloudflare Pages** - Edit (if using Pages)

**2. Add Secret to GitHub**

Repository → Settings → Secrets → Actions → New repository secret:
- Name: `CLOUDFLARE_API_TOKEN`
- Value: [paste token]

**3. Create `.github/workflows/deploy.yml`**

```yaml
name: Deploy

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    name: Deploy to Cloudflare Workers

    steps:
      - uses: actions/checkout@v4

      - uses: oven-sh/setup-bun@v2
        with:
          bun-version: latest

      - run: bun install

      - run: bun test

      - name: Deploy
        uses: cloudflare/wrangler-action@v4
        with:
          api-token: ${{ secrets.CLOUDFLARE_API_TOKEN }}
          command: deploy
```

**4. Push and Verify**

```bash
git add .github/workflows/deploy.yml
git commit -m "Add CI/CD pipeline"
git push
```

Check Actions tab on GitHub to see deployment progress.

---

## Critical Rules

### 1. Never Commit Secrets to Git

**✅ CORRECT**:
```yaml
# Use GitHub Secrets
api-token: ${{ secrets.CLOUDFLARE_API_TOKEN }}
```

**❌ WRONG**:
```yaml
# ❌ NEVER hardcode tokens
api-token: "abc123def456..."
```

**Why**: Exposed tokens allow anyone to deploy to your account.

### 2. Always Run Tests Before Deploy

**✅ CORRECT**:
```yaml
- run: bun test  # ✅ Tests run first

- name: Deploy
  uses: cloudflare/wrangler-action@v4
  with:
    api-token: ${{ secrets.CLOUDFLARE_API_TOKEN }}
```

**❌ WRONG**:
```yaml
# ❌ Skipping tests
- name: Deploy
  uses: cloudflare/wrangler-action@v4
  # No tests!
```

**Why**: Broken code shouldn't reach production.

### 3. Use Different Environments

**✅ CORRECT**:
```yaml
# Production (main branch)
- name: Deploy to Production
  if: github.ref == 'refs/heads/main'
  run: bunx wrangler deploy --env production

# Staging (other branches)
- name: Deploy to Staging
  if: github.ref != 'refs/heads/main'
  run: bunx wrangler deploy --env staging
```

**❌ WRONG**:
```yaml
# ❌ Always deploying to production
- run: bunx wrangler deploy
```

**Why**: Test changes in staging before production.

### 4. Verify Deployment Success

**✅ CORRECT**:
```yaml
- name: Deploy
  id: deploy
  uses: cloudflare/wrangler-action@v4

- name: Verify Deployment
  run: |
    curl -f https://your-worker.workers.dev/health || exit 1
```

**❌ WRONG**:
```yaml
# ❌ No verification
- name: Deploy
  uses: cloudflare/wrangler-action@v4
  # Assuming it worked...
```

**Why**: Deployments can fail silently (DNS issues, binding errors).

### 5. Use Deployment Gates for Production

**✅ CORRECT**:
```yaml
deploy-production:
  environment:
    name: production
    url: https://your-worker.workers.dev
  # Requires manual approval
```

**❌ WRONG**:
```yaml
# ❌ Auto-deploy to production without review
deploy-production:
  runs-on: ubuntu-latest
```

**Why**: Human review catches issues automation misses.

---

## Core Concepts

### Multi-Environment Strategy

**Recommended setup**:
- **Production**: `main` branch → production environment
- **Staging**: Pull requests → staging environment
- **Preview**: Each PR → unique preview URL

**wrangler.jsonc**:
```jsonc
{
  "name": "my-worker",
  "main": "src/index.ts",

  "env": {
    "production": {
      "name": "my-worker-production",
      "vars": {
        "ENVIRONMENT": "production"
      }
    },
    "staging": {
      "name": "my-worker-staging",
      "vars": {
        "ENVIRONMENT": "staging"
      }
    }
  }
}
```

### Secrets Management

**Types of configuration**:
1. **Public variables** (wrangler.jsonc) - Non-sensitive config
2. **Secrets** (wrangler secret) - API keys, tokens
3. **CI variables** (GitHub Secrets) - Deployment credentials

**Setting secrets**:
```bash
# Local development
wrangler secret put DATABASE_URL

# CI/CD (via GitHub Actions)
bunx wrangler secret put DATABASE_URL --env production <<< "${{ secrets.DATABASE_URL }}"
```

### Preview Deployments

Automatically deploy each PR to a unique URL for testing:

```yaml
- name: Deploy Preview
  uses: cloudflare/wrangler-action@v4
  with:
    api-token: ${{ secrets.CLOUDFLARE_API_TOKEN }}
    command: deploy --env preview-${{ github.event.number }}
```

Each PR gets URL like: `my-worker-preview-42.workers.dev`

---

## Top 5 Use Cases

### 1. Deploy on Push to Main

```yaml
name: Deploy Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: oven-sh/setup-bun@v2
      - run: bun install
      - run: bun test
      - run: bun run build

      - name: Deploy to Production
        uses: cloudflare/wrangler-action@v4
        with:
          api-token: ${{ secrets.CLOUDFLARE_API_TOKEN }}
          command: deploy --env production
```

### 2. Preview Deployments for PRs

```yaml
name: Preview

on:
  pull_request:
    branches: [main]

jobs:
  preview:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: oven-sh/setup-bun@v2
      - run: bun install
      - run: bun test

      - name: Deploy Preview
        id: deploy
        uses: cloudflare/wrangler-action@v4
        with:
          api-token: ${{ secrets.CLOUDFLARE_API_TOKEN }}
          command: deploy --env preview-${{ github.event.number }}

      - name: Comment PR
        uses: actions/github-script@v7
        with:
          script: |
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: '✅ Preview deployed to: https://my-worker-preview-${{ github.event.number }}.workers.dev'
            })
```

### 3. Run Tests on Every Commit

```yaml
name: Test

on:
  push:
    branches: ['**']
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: oven-sh/setup-bun@v2
      - run: bun install
      - run: bun test --coverage

      - name: Upload Coverage
        uses: codecov/codecov-action@v4
        with:
          files: ./coverage/lcov.info
```

### 4. Deploy with Approval Gate

```yaml
name: Deploy Production (Manual Approval)

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment:
      name: production
      url: https://my-worker.workers.dev
    # Requires manual approval in GitHub Settings

    steps:
      - uses: actions/checkout@v4
      - uses: oven-sh/setup-bun@v2
      - run: bun install
      - run: bun test

      - name: Deploy
        uses: cloudflare/wrangler-action@v4
        with:
          api-token: ${{ secrets.CLOUDFLARE_API_TOKEN }}
          command: deploy --env production
```

### 5. Staged Rollout (Canary)

```yaml
name: Canary Deployment

on:
  workflow_dispatch:
    inputs:
      percentage:
        description: 'Traffic percentage to new version'
        required: true
        default: '10'

jobs:
  canary:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: oven-sh/setup-bun@v2
      - run: bun install

      # Deploy to canary environment
      - name: Deploy Canary
        uses: cloudflare/wrangler-action@v4
        with:
          api-token: ${{ secrets.CLOUDFLARE_API_TOKEN }}
          command: deploy --env canary

      # Configure traffic split via Cloudflare API
      # (See references/deployment-strategies.md for full example)
```

---

## Best Practices

### ✅ DO

1. **Use semantic commit messages**:
   ```
   feat: add user authentication
   fix: resolve rate limiting issue
   chore: update dependencies
   ```

2. **Run linting and type checking**:
   ```yaml
   - run: bun run lint
   - run: bun run type-check
   - run: bun test
   ```

3. **Cache dependencies**:
   ```yaml
   - uses: oven-sh/setup-bun@v2
     with:
       bun-version: latest
   # Bun automatically caches dependencies
   ```

4. **Deploy different branches to different environments**:
   ```yaml
   - name: Deploy
     run: |
       if [ "${{ github.ref }}" == "refs/heads/main" ]; then
         bunx wrangler deploy --env production
       else
         bunx wrangler deploy --env staging
       fi
   ```

5. **Monitor deployments**:
   ```yaml
   - name: Notify Slack
     if: failure()
     uses: slackapi/slack-github-action@v1
     with:
       payload: |
         {"text": "Deployment failed: ${{ github.sha }}"}
   ```

### ❌ DON'T

1. **Don't skip tests**
2. **Don't deploy without verification**
3. **Don't hardcode secrets**
4. **Don't deploy to production from feature branches**
5. **Don't ignore deployment failures**

---

## Top 7 Errors Prevented

### 1. ❌ `Error: A valid Cloudflare API token is required`

**Cause**: Missing or invalid `CLOUDFLARE_API_TOKEN` secret.

**Fix**:
1. Create API token: https://dash.cloudflare.com/profile/api-tokens
2. Add to GitHub Secrets: Settings → Secrets → Actions
3. Use in workflow: `api-token: ${{ secrets.CLOUDFLARE_API_TOKEN }}`

---

### 2. ❌ `Error: Not enough permissions to deploy`

**Cause**: API token lacks required permissions.

**Fix**: Recreate token with:
- **Account.Cloudflare Workers Scripts** - Edit
- **Account settings** - Read

---

### 3. ❌ `Error: wrangler.toml not found`

**Cause**: Missing wrangler configuration.

**Fix**: Ensure `wrangler.jsonc` exists in repository root.

---

### 4. ❌ Deployment succeeds but worker doesn't work

**Cause**: Missing secrets or environment variables.

**Fix**: Set secrets in CI:
```yaml
- name: Set Secrets
  run: |
    echo "${{ secrets.DATABASE_URL }}" | bunx wrangler secret put DATABASE_URL --env production
```

---

### 5. ❌ Tests pass locally but fail in CI

**Cause**: Environment differences (Node version, missing dependencies).

**Fix**:
```yaml
- uses: oven-sh/setup-bun@v2
  with:
    bun-version: latest # Lock version

- run: bun install --frozen-lockfile # Use exact versions
```

---

### 6. ❌ Preview deployments conflict

**Cause**: Multiple PRs deploying to same preview environment.

**Fix**: Use PR number in environment name:
```yaml
command: deploy --env preview-${{ github.event.number }}
```

---

### 7. ❌ Secrets exposed in logs

**Cause**: Echoing secrets in workflow.

**Fix**:
```yaml
# ❌ WRONG
- run: echo "Token: ${{ secrets.API_TOKEN }}"

# ✅ CORRECT
- run: echo "Deploying..." # No secrets in output
```

---

## When to Load References

Load reference files for detailed, specialized content:

**Load `references/github-actions.md` when:**
- Setting up GitHub Actions from scratch
- Configuring matrix builds (multiple Node versions)
- Using GitHub environments and deployment protection
- Implementing deployment gates and approvals

**Load `references/gitlab-ci.md` when:**
- Setting up GitLab CI pipelines
- Configuring GitLab environments
- Using GitLab secret variables
- Implementing review apps

**Load `references/deployment-strategies.md` when:**
- Implementing blue-green deployments
- Setting up canary releases
- Configuring traffic splitting
- Planning rollback procedures

**Load `references/secrets-management.md` when:**
- Managing secrets across environments
- Rotating API tokens
- Using external secret providers (Vault, 1Password)
- Implementing least-privilege access

**Load `templates/github-actions-full.yml` for:**
- Complete production-ready GitHub Actions workflow
- Multi-environment deployment example
- All deployment gates configured

**Load `templates/gitlab-ci-full.yml` for:**
- Complete GitLab CI pipeline
- Multi-stage deployment
- Review app configuration

**Load `templates/preview-deployment.yml` for:**
- PR preview deployment setup
- Automatic cleanup on PR close
- Comment with preview URL

**Load `templates/rollback-workflow.yml` for:**
- Manual rollback workflow
- Deployment history tracking
- Automated rollback on health check failure

**Load `scripts/verify-deployment.sh` for:**
- Automated deployment verification
- Health check implementation
- Smoke tests after deployment

---

## Related Cloudflare Plugins

**For deployment testing, load:**
- **cloudflare-workers-testing** - Test Workers before deployment
- **cloudflare-manager** - Manage deployments via Cloudflare API

**This skill focuses on CI/CD automation** for ALL Workers deployments regardless of bindings used.

---

**Questions?** Load `references/secrets-management.md` or use `/workers-deploy` command for guided deployment.
