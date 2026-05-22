---
name: ci-github-actions
description: Apply when setting up CI/CD pipelines: automated testing, linting, building, and deployment with GitHub Actions.
version: 1.1.0
tokens: ~700
confidence: high
sources:
  - https://docs.github.com/en/actions/quickstart
  - https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions
last_validated: 2025-12-10
next_review: 2025-12-24
tags: [ci, github-actions, automation, devops]
---

## When to Use

Apply when setting up CI/CD pipelines: automated testing, linting, building, and deployment with GitHub Actions.

## Patterns

### Pattern 1: Basic CI Workflow
```yaml
# Source: https://docs.github.com/en/actions/quickstart
# .github/workflows/ci.yml
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
      - uses: actions/checkout@v5

      - name: Setup Node.js
        uses: actions/setup-node@v6
        with:
          node-version: '22'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run linter
        run: npm run lint

      - name: Run tests
        run: npm test

      - name: Build
        run: npm run build
```

### Pattern 2: Matrix Testing
```yaml
# Source: https://docs.github.com/en/actions/using-jobs/using-a-matrix-for-your-jobs
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: [20, 22, 24]
        os: [ubuntu-latest, windows-latest]

    steps:
      - uses: actions/checkout@v5
      - uses: actions/setup-node@v6
        with:
          node-version: ${{ matrix.node-version }}
      - run: npm ci
      - run: npm test
```

### Pattern 3: Caching Dependencies
```yaml
# Source: https://docs.github.com/en/actions/using-workflows/caching-dependencies-to-speed-up-workflows
- name: Cache node modules
  uses: actions/cache@v4
  with:
    path: ~/.npm
    key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
    restore-keys: |
      ${{ runner.os }}-node-

# Or use setup-node cache option
- uses: actions/setup-node@v6
  with:
    node-version: '22'
    cache: 'npm'  # Automatic caching
```

### Pattern 4: Environment Secrets
```yaml
# Source: https://docs.github.com/en/actions/security-guides/encrypted-secrets
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production  # Use environment-specific secrets

    steps:
      - name: Deploy
        env:
          DATABASE_URL: ${{ secrets.DATABASE_URL }}
          API_KEY: ${{ secrets.API_KEY }}
        run: |
          npm run deploy
```

### Pattern 5: Conditional Jobs
```yaml
# Source: https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - run: npm test

  deploy:
    needs: test  # Run after test passes
    if: github.ref == 'refs/heads/main'  # Only on main
    runs-on: ubuntu-latest
    steps:
      - run: npm run deploy

  notify:
    needs: [test, deploy]
    if: failure()  # Only if previous jobs failed
    runs-on: ubuntu-latest
    steps:
      - run: echo "Build failed!"
```

### Pattern 6: Reusable Workflows
```yaml
# Source: https://docs.github.com/en/actions/using-workflows/reusing-workflows
# .github/workflows/reusable-test.yml
name: Reusable Test

on:
  workflow_call:
    inputs:
      node-version:
        required: false
        type: string
        default: '22'

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
      - uses: actions/setup-node@v6
        with:
          node-version: ${{ inputs.node-version }}
      - run: npm ci && npm test

# Usage in another workflow
jobs:
  call-tests:
    uses: ./.github/workflows/reusable-test.yml
    with:
      node-version: '22'
```

## Anti-Patterns

- **No caching** - Always cache dependencies
- **Secrets in logs** - Never echo secrets
- **Long monolithic workflows** - Split into jobs
- **No branch protection** - Require CI pass for merge

## Verification Checklist

- [ ] CI runs on PRs and main pushes
- [ ] Dependencies cached
- [ ] Secrets stored in GitHub Secrets
- [ ] Tests must pass before merge
- [ ] Build artifacts preserved if needed
