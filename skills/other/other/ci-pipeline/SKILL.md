---
name: ci-pipeline
description: GitHub Actions CI/CD pipelines with caching, matrix builds, and deployment strategies. Focuses on build speed, reliability, and security. Use when creating or optimizing CI/CD workflows, debugging pipeline failures, or implementing deployment automation.
---

# CI Pipeline

GitHub Actions CI/CD patterns for reliable, fast pipelines.

## When to Use

- Creating new GitHub Actions workflows
- Optimizing slow CI builds
- Debugging pipeline failures
- Implementing deployment strategies
- Adding security scanning

## MCP Workflow

```yaml
# 1. Find existing workflows
serena.list_dir(".github/workflows")

# 2. Check workflow patterns
serena.search_for_pattern("uses:|run:|cache:|matrix:", paths_include_glob=".github/workflows/*.yml")

# 3. Find reusable workflows
jetbrains.search_in_files_by_text("workflow_call", fileMask="*.yml")

# 4. GitHub Actions docs
context7.get-library-docs("/github/actions", "caching")
```

## Workflow Structure

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true  # Cancel outdated runs

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      # Job steps...
```

## Caching Strategies

### Gradle Cache

```yaml
- name: Cache Gradle
  uses: actions/cache@v4
  with:
    path: |
      ~/.gradle/caches
      ~/.gradle/wrapper
    key: gradle-${{ runner.os }}-${{ hashFiles('**/*.gradle*', '**/gradle-wrapper.properties') }}
    restore-keys: gradle-${{ runner.os }}-
```

### npm/pnpm Cache

```yaml
- name: Cache pnpm
  uses: actions/cache@v4
  with:
    path: ~/.pnpm-store
    key: pnpm-${{ runner.os }}-${{ hashFiles('**/pnpm-lock.yaml') }}
    restore-keys: pnpm-${{ runner.os }}-

# Or use setup action with built-in cache
- uses: pnpm/action-setup@v4
  with:
    version: 9
- uses: actions/setup-node@v4
  with:
    node-version: '22'
    cache: 'pnpm'
```

### uv (Python) Cache

```yaml
- name: Cache uv
  uses: actions/cache@v4
  with:
    path: ~/.cache/uv
    key: uv-${{ runner.os }}-${{ hashFiles('**/uv.lock') }}
    restore-keys: uv-${{ runner.os }}-
```

### Docker Layer Cache

```yaml
- name: Set up Docker Buildx
  uses: docker/setup-buildx-action@v3

- name: Build with cache
  uses: docker/build-push-action@v6
  with:
    context: .
    push: false
    cache-from: type=gha
    cache-to: type=gha,mode=max
```

## Matrix Builds

```yaml
jobs:
  test:
    strategy:
      fail-fast: false  # Don't cancel other jobs on failure
      matrix:
        os: [ubuntu-latest, macos-latest]
        node: [20, 22]
        exclude:
          - os: macos-latest
            node: 20
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node }}
```

## Job Dependencies

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    outputs:
      version: ${{ steps.version.outputs.value }}
    steps:
      - id: version
        run: echo "value=$(cat version.txt)" >> $GITHUB_OUTPUT

  deploy:
    needs: [build, test]  # Waits for both
    if: success()         # Only if both succeeded
    runs-on: ubuntu-latest
    steps:
      - run: echo "Deploying ${{ needs.build.outputs.version }}"
```

## Reusable Workflows

### Define Reusable Workflow

```yaml
# .github/workflows/build-and-test.yml
name: Build and Test

on:
  workflow_call:
    inputs:
      node-version:
        type: string
        default: '22'
    secrets:
      npm-token:
        required: false

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ inputs.node-version }}
      - run: npm ci
        env:
          NPM_TOKEN: ${{ secrets.npm-token }}
```

### Call Reusable Workflow

```yaml
jobs:
  build:
    uses: ./.github/workflows/build-and-test.yml
    with:
      node-version: '22'
    secrets:
      npm-token: ${{ secrets.NPM_TOKEN }}
```

## Security Patterns

### Minimal Permissions

```yaml
permissions:
  contents: read
  pull-requests: write  # Only what's needed

jobs:
  security:
    runs-on: ubuntu-latest
    permissions:
      security-events: write  # Job-level override
```

### Dependency Scanning

```yaml
- name: Scan dependencies
  uses: aquasecurity/trivy-action@master
  with:
    scan-type: 'fs'
    severity: 'CRITICAL,HIGH'
    exit-code: '1'  # Fail on findings
```

### Secret Scanning

```yaml
- name: Check for secrets
  uses: trufflesecurity/trufflehog@main
  with:
    path: ./
    base: ${{ github.event.repository.default_branch }}
    head: HEAD
```

## Deployment Strategies

### Environment-based Deployment

```yaml
jobs:
  deploy-staging:
    environment: staging
    runs-on: ubuntu-latest
    steps:
      - run: ./deploy.sh staging

  deploy-production:
    needs: deploy-staging
    environment:
      name: production
      url: https://app.example.com
    runs-on: ubuntu-latest
    steps:
      - run: ./deploy.sh production
```

### Manual Approval

```yaml
environment:
  name: production
  # Requires approval in repo settings
```

## Debugging Pipelines

### Enable Debug Logging

```yaml
# Set secret ACTIONS_STEP_DEBUG=true
# Or re-run with debug logging enabled in UI
```

### SSH Debug Session

```yaml
- name: Debug with tmate
  if: failure()
  uses: mxschmitt/action-tmate@v3
  with:
    limit-access-to-actor: true
```

### Artifact for Debugging

```yaml
- name: Upload logs on failure
  if: failure()
  uses: actions/upload-artifact@v4
  with:
    name: debug-logs
    path: |
      **/logs/
      **/test-results/
```

## Anti-Patterns

| Pattern | Problem | Solution |
|---------|---------|----------|
| No cache | Slow builds | Add appropriate caching |
| `if: always()` for deploy | Deploys broken code | Use `if: success()` |
| Secrets in logs | Security risk | Use `::add-mask::` |
| Single monolith job | Slow, no parallelism | Split into dependent jobs |
| No `concurrency` | Wasted resources | Cancel outdated runs |
| Hardcoded versions | Drift | Use variables or renovate |

## Speed Optimization Checklist

- [ ] Caching enabled for dependencies
- [ ] Docker layer caching configured
- [ ] Jobs run in parallel where possible
- [ ] `concurrency` cancels outdated runs
- [ ] `fail-fast: true` for matrix (if appropriate)
- [ ] Only checkout needed paths (`sparse-checkout`)
- [ ] Use `ubuntu-latest` (faster than macos/windows)

## Quality Checklist

- [ ] `permissions` uses least privilege
- [ ] Secrets not logged (masked)
- [ ] Security scanning enabled
- [ ] Deployment requires approval for production
- [ ] Status checks required for merge
- [ ] Workflows documented with comments
