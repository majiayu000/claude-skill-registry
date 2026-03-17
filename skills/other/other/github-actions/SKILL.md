---
name: github-actions
description: GitHub Actions CI/CD expert skill. Use when creating, debugging, optimizing, or securing GitHub Actions workflows, implementing DevSecOps pipelines, setting up deployment strategies, configuring matrix builds, caching, reusable workflows, OIDC authentication, or troubleshooting CI/CD failures.
---

You are operating as a Principal DevOps Engineer with 10+ years of CI/CD experience, specializing in GitHub Actions pipelines for production workloads.

## Pipeline Design Principles

**Fail fast → Parallelize → Cache → Build once → Deploy many**

```
1. Fast feedback (lint, format)      → <1 min
2. Unit tests                        → 1-5 min
3. Security scanning (SAST, SCA)     → 2-5 min
4. Integration tests                 → 5-15 min
5. Build artifacts                   → 2-5 min
6. E2E tests (main branch only)      → 15-30 min
7. Deploy (with approval gates)      → 2-10 min
```

## Workflow Structure

```yaml
name: CI/CD
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

permissions:
  contents: read

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - # lint steps

  test:
    runs-on: ubuntu-latest
    needs: [lint]
    strategy:
      matrix:
        shard: [1, 2, 3]
    steps:
      - uses: actions/checkout@v4
      - # test steps with sharding

  build:
    runs-on: ubuntu-latest
    needs: [test]
    steps:
      - uses: actions/checkout@v4
      - # build and upload artifact

  deploy:
    runs-on: ubuntu-latest
    needs: [build]
    if: github.ref == 'refs/heads/main'
    environment:
      name: production
      url: https://example.com
    steps:
      - # download artifact and deploy
```

## Caching Strategies

### Node.js
```yaml
- uses: actions/setup-node@v4
  with:
    node-version: '22'
    cache: 'npm'
- run: npm ci
```

### Go
```yaml
- uses: actions/setup-go@v5
  with:
    go-version: '1.23'
    cache: true
- run: go build ./...
```

### Docker Layer Caching
```yaml
- uses: docker/build-push-action@v6
  with:
    context: .
    cache-from: type=gha
    cache-to: type=gha,mode=max
```

### Custom Cache
```yaml
- uses: actions/cache@v4
  with:
    path: |
      ~/.cache/custom
      ./build-cache
    key: ${{ runner.os }}-custom-${{ hashFiles('**/lockfile') }}
    restore-keys: |
      ${{ runner.os }}-custom-
```

## Security Best Practices

### OIDC Authentication (no static credentials)

**AWS:**
```yaml
permissions:
  id-token: write
  contents: read
steps:
  - uses: aws-actions/configure-aws-credentials@v4
    with:
      role-to-assume: arn:aws:iam::123456789:role/GitHubActionsRole
      aws-region: us-east-1
```

**GCP:**
```yaml
permissions:
  id-token: write
  contents: read
steps:
  - uses: google-github-actions/auth@v2
    with:
      workload_identity_provider: projects/123/locations/global/workloadIdentityPools/gh/providers/gh
      service_account: deploy@project.iam.gserviceaccount.com
```

### Pin Actions to SHA
```yaml
# Good - pinned to SHA
- uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11 # v4.1.1

# Acceptable - pinned to major version
- uses: actions/checkout@v4

# Bad - unpinned
- uses: actions/checkout@main
```

### Minimal Permissions
```yaml
# Global - restrictive
permissions:
  contents: read

# Per-job - grant only what's needed
jobs:
  deploy:
    permissions:
      contents: read
      id-token: write
      packages: write
```

### Security Scanning Pipeline
```yaml
jobs:
  secret-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - uses: trufflesecurity/trufflehog@main

  sast:
    runs-on: ubuntu-latest
    permissions:
      security-events: write
    steps:
      - uses: actions/checkout@v4
      - uses: github/codeql-action/init@v3
        with:
          languages: go  # or javascript, python
      - uses: github/codeql-action/analyze@v3

  sca:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm audit --audit-level=high  # or govulncheck, pip-audit

  container-scan:
    needs: [build]
    runs-on: ubuntu-latest
    steps:
      - uses: aquasecurity/trivy-action@master
        with:
          image-ref: ${{ needs.build.outputs.image }}
          severity: CRITICAL,HIGH
```

## Reusable Workflows

### Define
```yaml
# .github/workflows/reusable-deploy.yml
on:
  workflow_call:
    inputs:
      environment:
        required: true
        type: string
      image-tag:
        required: true
        type: string
    secrets:
      DEPLOY_KEY:
        required: true

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: ${{ inputs.environment }}
    steps:
      - # deployment steps
```

### Consume
```yaml
jobs:
  deploy-staging:
    uses: ./.github/workflows/reusable-deploy.yml
    with:
      environment: staging
      image-tag: ${{ needs.build.outputs.tag }}
    secrets:
      DEPLOY_KEY: ${{ secrets.STAGING_DEPLOY_KEY }}
```

## Docker Build & Push

```yaml
jobs:
  docker:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    steps:
      - uses: actions/checkout@v4

      - uses: docker/setup-buildx-action@v3

      - uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - uses: docker/metadata-action@v5
        id: meta
        with:
          images: ghcr.io/${{ github.repository }}
          tags: |
            type=sha
            type=ref,event=branch
            type=semver,pattern={{version}}

      - uses: docker/build-push-action@v6
        with:
          context: .
          push: ${{ github.event_name != 'pull_request' }}
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
          platforms: linux/amd64,linux/arm64
```

## Matrix Builds

```yaml
strategy:
  fail-fast: false
  matrix:
    os: [ubuntu-latest, macos-latest]
    go-version: ['1.22', '1.23']
    include:
      - os: ubuntu-latest
        go-version: '1.23'
        coverage: true
    exclude:
      - os: macos-latest
        go-version: '1.22'
```

## Deployment Patterns

| Pattern | Use Case | Implementation |
|---------|----------|----------------|
| **Direct** | Simple apps | Push to main → deploy |
| **Blue-Green** | Zero downtime | Deploy to inactive, switch traffic |
| **Canary** | Gradual rollout | Route % of traffic, monitor, promote |
| **Rolling** | Kubernetes | Rolling update with health checks |

### Multi-Environment
```yaml
deploy-staging:
  needs: [build, test]
  if: github.ref == 'refs/heads/main'
  environment: staging

deploy-production:
  needs: [deploy-staging]
  environment:
    name: production
  # Manual approval via GitHub Environments
```

## Troubleshooting

| Error Pattern | Common Cause | Fix |
|---------------|--------------|-----|
| "Module not found" | Missing dep or cache | Clear cache, `npm ci` |
| "Timeout" | Job too slow | Add caching, increase timeout |
| "Permission denied" | Missing permissions | Add to `permissions:` block |
| "Resource not accessible" | Token scope | Check GITHUB_TOKEN permissions |
| "Cannot connect to Docker" | Docker not available | Use correct runner |
| Intermittent failures | Flaky tests | Add retries, fix timing |

### Debug Logging
```yaml
# Add repository secrets:
# ACTIONS_RUNNER_DEBUG = true
# ACTIONS_STEP_DEBUG = true
```

### Local Testing
```bash
# Use act for local GitHub Actions testing
act -j build
act push --secret-file .secrets
```

## CLI Quick Reference

```bash
# List workflows
gh workflow list

# View recent runs
gh run list --limit 20

# View specific run details
gh run view <run-id>

# Re-run failed jobs
gh run rerun <run-id> --failed

# Download logs
gh run view <run-id> --log

# Trigger workflow manually
gh workflow run ci.yml -f param=value

# Watch run in real-time
gh run watch
```

## Optimization Checklist

- [ ] Dependency caching enabled (50-90% faster)
- [ ] Unnecessary `needs` dependencies removed
- [ ] Path filters to skip irrelevant runs
- [ ] `concurrency` with `cancel-in-progress` for PRs
- [ ] Job timeouts set to prevent hung builds
- [ ] Matrix builds for cross-platform testing
- [ ] Test sharding for large test suites
- [ ] Docker layer caching with BuildKit
- [ ] Artifacts: build once, deploy many
- [ ] Reusable workflows for DRY pipelines

For detailed references see [references/patterns.md](references/patterns.md)
