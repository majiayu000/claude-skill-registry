---
name: cicd-automation
description: CI/CD pipeline design, GitHub Actions, and deployment automation. Auto-triggers when setting up pipelines, automating deployments, or configuring workflows.
---

# CI/CD Automation Skill

## Pipeline Design Principles

### Stages
1. **Build**: Compile, bundle, create artifacts
2. **Test**: Unit, integration, E2E tests
3. **Scan**: Security, dependencies, quality
4. **Deploy**: Staging, then production
5. **Verify**: Smoke tests, health checks

### Best Practices
- Fail fast (run quick checks first)
- Parallelize independent jobs
- Cache dependencies aggressively
- Use immutable artifacts
- Never store secrets in code

## GitHub Actions Patterns

### Basic CI Workflow
```yaml
name: CI
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4

    - name: Setup Node
      uses: actions/setup-node@v4
      with:
        node-version: '20'
        cache: 'npm'

    - name: Install dependencies
      run: npm ci

    - name: Run tests
      run: npm test

    - name: Run linter
      run: npm run lint
```

### Matrix Testing
```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: [18, 20, 22]
        os: [ubuntu-latest, macos-latest]
    steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-node@v4
      with:
        node-version: ${{ matrix.node-version }}
    - run: npm test
```

### Caching
```yaml
- name: Cache node modules
  uses: actions/cache@v4
  with:
    path: ~/.npm
    key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
    restore-keys: |
      ${{ runner.os }}-node-
```

### Deployment Workflow
```yaml
name: Deploy
on:
  push:
    branches: [main]

jobs:
  deploy-staging:
    runs-on: ubuntu-latest
    environment: staging
    steps:
    - uses: actions/checkout@v4
    - name: Deploy to staging
      run: ./deploy.sh staging
      env:
        DEPLOY_KEY: ${{ secrets.STAGING_DEPLOY_KEY }}

  deploy-production:
    needs: deploy-staging
    runs-on: ubuntu-latest
    environment:
      name: production
      url: https://myapp.com
    steps:
    - uses: actions/checkout@v4
    - name: Deploy to production
      run: ./deploy.sh production
      env:
        DEPLOY_KEY: ${{ secrets.PROD_DEPLOY_KEY }}
```

### Reusable Workflows
```yaml
# .github/workflows/reusable-build.yml
name: Reusable Build
on:
  workflow_call:
    inputs:
      environment:
        required: true
        type: string
    secrets:
      deploy_key:
        required: true

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - run: echo "Building for ${{ inputs.environment }}"

# Caller workflow
jobs:
  call-build:
    uses: ./.github/workflows/reusable-build.yml
    with:
      environment: production
    secrets:
      deploy_key: ${{ secrets.DEPLOY_KEY }}
```

## Security Scanning

### Dependency Scanning
```yaml
- name: Run npm audit
  run: npm audit --audit-level=high

- name: Snyk scan
  uses: snyk/actions/node@master
  env:
    SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
```

### SAST (Static Analysis)
```yaml
- name: CodeQL Analysis
  uses: github/codeql-action/analyze@v3
```

### Secret Scanning
```yaml
- name: Gitleaks scan
  uses: gitleaks/gitleaks-action@v2
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

## Deployment Patterns

### Feature Flags
```yaml
- name: Deploy with feature flag
  run: |
    if [[ "${{ github.ref }}" == "refs/heads/main" ]]; then
      FEATURE_FLAG=enabled ./deploy.sh
    else
      FEATURE_FLAG=disabled ./deploy.sh
    fi
```

### Rollback
```yaml
- name: Deploy
  id: deploy
  run: ./deploy.sh

- name: Rollback on failure
  if: failure() && steps.deploy.outcome == 'failure'
  run: ./rollback.sh
```

### Canary Deployment
```yaml
- name: Deploy canary (10%)
  run: ./deploy.sh --canary 10

- name: Run smoke tests
  run: ./smoke-tests.sh

- name: Full rollout
  if: success()
  run: ./deploy.sh --canary 100
```

## Artifacts and Releases

```yaml
- name: Build artifact
  run: npm run build

- name: Upload artifact
  uses: actions/upload-artifact@v4
  with:
    name: build-${{ github.sha }}
    path: dist/
    retention-days: 7

- name: Create release
  if: startsWith(github.ref, 'refs/tags/')
  uses: softprops/action-gh-release@v1
  with:
    files: dist/*
```
