---
name: ci-cd-patterns
description: Provides CI/CD pipeline best practices for GitHub Actions, deployment strategies, and pipeline optimization. Use when setting up pipelines, configuring GitHub Actions, managing deployments, or when user mentions 'CI', 'CD', 'pipeline', 'GitHub Actions', 'deploy', 'workflow', 'build'.
---

# CI/CD Patterns

Best practices for building reliable, secure, and fast CI/CD pipelines with GitHub Actions.

## Pipeline Stages

A well-structured pipeline follows this progression. Each stage gates the next.

```
lint --> test --> build --> security-scan --> deploy-staging --> deploy-production
```

| Stage | Purpose | Failure Means |
|-------|---------|---------------|
| Lint | Code style, formatting | Code doesn't meet standards |
| Test | Unit + integration tests | Broken functionality |
| Build | Compile, bundle | Code won't package |
| Security Scan | Dependency + code analysis | Vulnerabilities detected |
| Deploy Staging | Pre-production verification | Environment issue |
| Deploy Production | Live release | Requires approval gate |

## GitHub Actions: Complete Workflow Templates

### Standard CI Workflow

```yaml
name: CI

on:
  pull_request:
    branches: [main]
  push:
    branches: [main]

# Cancel in-progress runs for the same branch/PR
concurrency:
  group: ci-${{ github.ref }}
  cancel-in-progress: true

permissions:
  contents: read

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: npm

      - run: npm ci
      - run: npm run lint
      - run: npm run format:check

  test:
    runs-on: ubuntu-latest
    needs: lint
    strategy:
      matrix:
        node-version: [18, 20, 22]
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
          cache: npm

      - run: npm ci
      - run: npm test -- --coverage

      - uses: actions/upload-artifact@v4
        if: matrix.node-version == 20
        with:
          name: coverage-report
          path: coverage/
          retention-days: 7

  build:
    runs-on: ubuntu-latest
    needs: test
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: npm

      - run: npm ci
      - run: npm run build

      - uses: actions/upload-artifact@v4
        with:
          name: build-output
          path: dist/
          retention-days: 7
```

### Deployment Workflow with Approval Gate

```yaml
name: Deploy

on:
  push:
    branches: [main]
  workflow_dispatch:
    inputs:
      environment:
        description: Target environment
        required: true
        default: staging
        type: choice
        options:
          - staging
          - production

permissions:
  contents: read
  deployments: write

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: npm
      - run: npm ci
      - run: npm run build

      - uses: actions/upload-artifact@v4
        with:
          name: deploy-artifact
          path: dist/

  deploy-staging:
    needs: build
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - uses: actions/download-artifact@v4
        with:
          name: deploy-artifact
          path: dist/

      - name: Deploy to staging
        env:
          DEPLOY_TOKEN: ${{ secrets.STAGING_DEPLOY_TOKEN }}
        run: |
          # Deploy script here -- uses secret, never echo it
          echo "Deploying to staging..."

  deploy-production:
    needs: deploy-staging
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    # CRITICAL: Production requires manual approval via GitHub Environments
    environment: production
    steps:
      - uses: actions/download-artifact@v4
        with:
          name: deploy-artifact
          path: dist/

      - name: Deploy to production
        env:
          DEPLOY_TOKEN: ${{ secrets.PRODUCTION_DEPLOY_TOKEN }}
        run: |
          echo "Deploying to production..."
```

### Docker Build and Push

```yaml
name: Docker

on:
  push:
    tags: ['v*']

permissions:
  contents: read
  packages: write

jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: docker/setup-buildx-action@v3

      - uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - uses: docker/build-push-action@v6
        with:
          context: .
          push: true
          tags: |
            ghcr.io/${{ github.repository }}:${{ github.ref_name }}
            ghcr.io/${{ github.repository }}:latest
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

## Secret Management

### Rules

| Rule | Rationale |
|------|-----------|
| Never echo secrets in logs | CI logs are often accessible to contributors |
| Use GitHub Environment secrets for deploy tokens | Scoped to specific environments |
| Rotate secrets on schedule | Reduces blast radius of leaks |
| Use OIDC where possible | No long-lived credentials |
| Minimal secret scope | Each secret should access only what it needs |

### Masking Secrets

```yaml
steps:
  - name: Use secret safely
    env:
      # Secret is automatically masked in logs
      API_KEY: ${{ secrets.API_KEY }}
    run: |
      # NEVER do this:
      # echo "Key is $API_KEY"

      # SAFE: Use secret in commands without printing
      curl -s -H "Authorization: Bearer $API_KEY" https://api.example.com/health

  - name: Mask dynamic values
    run: |
      TOKEN=$(generate-token)
      echo "::add-mask::$TOKEN"
      # Now $TOKEN is masked in all subsequent log output
      echo "Token generated successfully"
```

### OIDC for Cloud Providers (No Stored Secrets)

```yaml
permissions:
  id-token: write
  contents: read

steps:
  - uses: aws-actions/configure-aws-credentials@v4
    with:
      role-to-assume: arn:aws:iam::123456789:role/github-deploy
      aws-region: us-east-1
      # No AWS_ACCESS_KEY_ID or AWS_SECRET_ACCESS_KEY needed
```

## Caching Strategies

### Dependency Caching

```yaml
# Node.js -- built into setup-node
- uses: actions/setup-node@v4
  with:
    node-version: 20
    cache: npm

# Python
- uses: actions/setup-python@v5
  with:
    python-version: '3.12'
    cache: pip

# Go
- uses: actions/setup-go@v5
  with:
    go-version: '1.22'
    cache: true

# Rust
- uses: actions/cache@v4
  with:
    path: |
      ~/.cargo/bin/
      ~/.cargo/registry/index/
      ~/.cargo/registry/cache/
      target/
    key: rust-${{ hashFiles('**/Cargo.lock') }}
    restore-keys: rust-
```

### Custom Cache

```yaml
- uses: actions/cache@v4
  with:
    path: .cache/expensive-operation
    key: expensive-${{ hashFiles('src/**') }}
    restore-keys: |
      expensive-
```

### Cache Sizing

| What to Cache | Impact | Size Concern |
|---------------|--------|-------------|
| `node_modules` (via npm ci) | HIGH | Use `setup-node` cache instead |
| Build output | MEDIUM | Only if build is slow (>2 min) |
| Docker layers | HIGH | Use `cache-from: type=gha` |
| Test fixtures | LOW | Usually not worth caching |

## Deployment Patterns

### Blue-Green Deployment

Two identical environments. Switch traffic atomically.

```
Current traffic --> Blue (v1.0)
                    Green (v1.1) <-- Deploy here, test, then switch

After switch:
Current traffic --> Green (v1.1)
                    Blue (v1.0) <-- Rollback target
```

| Pros | Cons |
|------|------|
| Instant rollback | Requires 2x infrastructure |
| Zero downtime | Database migrations need care |
| Full environment testing | Higher cost |

### Canary Deployment

Route a small percentage of traffic to the new version.

```
95% traffic --> v1.0 (stable)
 5% traffic --> v1.1 (canary)

Monitor metrics. If healthy:
50% --> v1.0, 50% --> v1.1
Then: 100% --> v1.1
```

| Pros | Cons |
|------|------|
| Low risk | Slower rollout |
| Real traffic testing | Complex routing setup |
| Gradual confidence | Stateful apps need care |

### Rolling Deployment

Replace instances one at a time.

```
Instance 1: v1.0 --> v1.1  (update, health check, continue)
Instance 2: v1.0 --> v1.1
Instance 3: v1.0 --> v1.1
```

| Pros | Cons |
|------|------|
| No extra infrastructure | Mixed versions during rollout |
| Simple to implement | Slower rollback (re-deploy) |
| Works with most platforms | Must be backward compatible |

## Matrix Builds

Test across multiple versions and platforms efficiently.

```yaml
strategy:
  fail-fast: false  # Don't cancel other jobs if one fails
  matrix:
    os: [ubuntu-latest, macos-latest, windows-latest]
    node-version: [18, 20, 22]
    exclude:
      # Skip combinations that don't matter
      - os: macos-latest
        node-version: 18
    include:
      # Add specific extra combinations
      - os: ubuntu-latest
        node-version: 20
        coverage: true

steps:
  - run: npm test

  - if: matrix.coverage
    run: npm run test:coverage
```

## Pipeline Optimization

### Speed Improvements

| Technique | Savings | Complexity |
|-----------|---------|------------|
| Dependency caching | 30-60s | Low |
| Parallel jobs | 40-70% | Low |
| `cancel-in-progress` | Avoid wasted runs | Low |
| Docker layer caching | 1-5 min | Medium |
| Selective test running | Variable | Medium |
| Self-hosted runners | Variable | High |

### Conditional Execution

```yaml
# Only run when relevant files change
on:
  push:
    paths:
      - 'src/**'
      - 'tests/**'
      - 'package.json'
      - 'package-lock.json'
    paths-ignore:
      - '**.md'
      - 'docs/**'

# Skip CI for documentation-only changes
jobs:
  test:
    if: |
      !contains(github.event.head_commit.message, '[skip ci]') &&
      !contains(github.event.head_commit.message, '[docs only]')
```

### Reusable Workflows

```yaml
# .github/workflows/reusable-test.yml
on:
  workflow_call:
    inputs:
      node-version:
        required: false
        type: string
        default: '20'
    secrets:
      NPM_TOKEN:
        required: false

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ inputs.node-version }}
          cache: npm
      - run: npm ci
      - run: npm test
```

```yaml
# .github/workflows/ci.yml -- caller
jobs:
  test:
    uses: ./.github/workflows/reusable-test.yml
    with:
      node-version: '20'
    secrets: inherit
```

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| Force-push in deploy scripts | Can overwrite production state | Use atomic deploys, never `git push --force` in CI |
| Secrets in workflow files | Exposed in repo history | Use GitHub Secrets or OIDC |
| `echo $SECRET` in logs | Leaked credentials | Never echo; use `::add-mask::` for dynamic values |
| No approval gate for production | Accidental deploys | Use GitHub Environments with required reviewers |
| `npm install` instead of `npm ci` | Non-deterministic builds | Always `npm ci` in CI (uses lockfile) |
| No `concurrency` control | Wasted compute, race conditions | Add `cancel-in-progress` for PR builds |
| Hardcoded versions in actions | Breaks without notice | Pin to major version (`@v4`) or SHA |
| Running tests only on main | Broken PRs get merged | Run on `pull_request` trigger |
| Single monolithic job | Slow, no parallelism | Split into lint/test/build/deploy jobs |
| No timeout on jobs | Hung builds waste minutes | Set `timeout-minutes` on every job |
| `permissions: write-all` | Excessive permissions | Use minimal `permissions` per job |

## Workflow Security Checklist

- [ ] `permissions` block set with minimal scope on every workflow
- [ ] Secrets used via `${{ secrets.NAME }}`, never hardcoded
- [ ] Third-party actions pinned to commit SHA or trusted major version
- [ ] `pull_request_target` workflows do NOT checkout PR code (code injection risk)
- [ ] Production deploys require approval via GitHub Environments
- [ ] No `--force` push commands in any workflow
- [ ] `concurrency` groups prevent parallel deploys to same environment
- [ ] `timeout-minutes` set on all jobs (default 360 min is too long)
- [ ] Artifacts have `retention-days` set (don't accumulate forever)
- [ ] OIDC used instead of long-lived cloud credentials where possible
