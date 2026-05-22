---
name: ci-cd-patterns
description: CI/CD pipeline patterns, GitHub Actions templates, and automation best practices. Reference this skill when setting up CI/CD.
---

# CI/CD Patterns Skill
# Project Autopilot - Pipeline patterns and templates
# Copyright (c) 2026 Jeremy McSpadden <jeremy@fluxlabs.net>

Comprehensive patterns for CI/CD pipeline configuration.

---

## Pipeline Stages

### Standard Pipeline Flow

```
┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
│  Lint   │ →  │  Test   │ →  │  Build  │ →  │ Deploy  │ →  │ Verify  │
│         │    │         │    │         │    │         │    │         │
│ ESLint  │    │ Unit    │    │ Docker  │    │ Staging │    │ Smoke   │
│ Prettier│    │ Integr. │    │ Bundle  │    │ Prod    │    │ Health  │
│ Types   │    │ E2E     │    │ Assets  │    │         │    │         │
└─────────┘    └─────────┘    └─────────┘    └─────────┘    └─────────┘
```

### Job Dependencies

```yaml
jobs:
  lint:        # No dependencies, runs first
  test:
    needs: lint
  build:
    needs: test
  deploy-staging:
    needs: build
    if: github.ref == 'refs/heads/develop'
  deploy-production:
    needs: build
    if: github.event_name == 'release'
```

---

## GitHub Actions Templates

### Basic Node.js

```yaml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Lint
        run: npm run lint

      - name: Type check
        run: npm run type-check

      - name: Test
        run: npm test -- --coverage

      - name: Build
        run: npm run build
```

### With Services (Database)

```yaml
jobs:
  test:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: test
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

      redis:
        image: redis:7
        ports:
          - 6379:6379

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - run: npm ci

      - name: Run migrations
        run: npm run db:migrate
        env:
          DATABASE_URL: postgres://postgres:postgres@localhost:5432/test

      - name: Test
        run: npm test
        env:
          DATABASE_URL: postgres://postgres:postgres@localhost:5432/test
          REDIS_URL: redis://localhost:6379
```

### Matrix Testing

```yaml
jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      fail-fast: false
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        node: [18, 20, 22]
        exclude:
          - os: windows-latest
            node: 18

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js ${{ matrix.node }}
        uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node }}
          cache: 'npm'

      - run: npm ci
      - run: npm test
```

### Caching Strategies

```yaml
steps:
  # npm cache
  - uses: actions/setup-node@v4
    with:
      node-version: '20'
      cache: 'npm'

  # Custom cache
  - name: Cache node_modules
    uses: actions/cache@v4
    with:
      path: node_modules
      key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
      restore-keys: |
        ${{ runner.os }}-node-

  # Turborepo cache
  - name: Cache turbo
    uses: actions/cache@v4
    with:
      path: .turbo
      key: ${{ runner.os }}-turbo-${{ github.sha }}
      restore-keys: |
        ${{ runner.os }}-turbo-

  # Docker layer cache
  - name: Set up Docker Buildx
    uses: docker/setup-buildx-action@v3

  - name: Build and push
    uses: docker/build-push-action@v5
    with:
      cache-from: type=gha
      cache-to: type=gha,mode=max
```

---

## Security Scanning

### Dependency Scanning

```yaml
jobs:
  security:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Run npm audit
        run: npm audit --audit-level=high

      - name: Run Snyk
        uses: snyk/actions/node@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
        with:
          args: --severity-threshold=high
```

### Code Scanning (CodeQL)

```yaml
jobs:
  codeql:
    runs-on: ubuntu-latest
    permissions:
      security-events: write

    steps:
      - uses: actions/checkout@v4

      - name: Initialize CodeQL
        uses: github/codeql-action/init@v2
        with:
          languages: javascript

      - name: Autobuild
        uses: github/codeql-action/autobuild@v2

      - name: Perform CodeQL Analysis
        uses: github/codeql-action/analyze@v2
```

### Secret Scanning

```yaml
jobs:
  secrets:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Detect secrets
        uses: gitleaks/gitleaks-action@v2
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

---

## Deployment Workflows

### Deploy to Vercel

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Deploy to Vercel
        uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          vercel-args: ${{ github.ref == 'refs/heads/main' && '--prod' || '' }}
```

### Deploy to AWS

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1

      - name: Login to ECR
        uses: aws-actions/amazon-ecr-login@v2

      - name: Build and push to ECR
        run: |
          docker build -t $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG .
          docker push $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG

      - name: Deploy to ECS
        uses: aws-actions/amazon-ecs-deploy-task-definition@v1
        with:
          task-definition: task-definition.json
          service: my-service
          cluster: my-cluster
```

### Deploy to Kubernetes

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Set up kubectl
        uses: azure/setup-kubectl@v3

      - name: Configure kubeconfig
        run: |
          echo "${{ secrets.KUBE_CONFIG }}" | base64 -d > kubeconfig
          export KUBECONFIG=kubeconfig

      - name: Deploy
        run: |
          kubectl set image deployment/my-app \
            my-app=${{ env.IMAGE_TAG }}
          kubectl rollout status deployment/my-app
```

---

## Optimization Best Practices

### Reduce Build Time

```yaml
# 1. Use caching
- uses: actions/cache@v4

# 2. Run jobs in parallel
jobs:
  lint:
  test:
  # Both run simultaneously

# 3. Skip unnecessary work
- name: Check for changes
  uses: dorny/paths-filter@v2
  id: changes
  with:
    filters: |
      src:
        - 'src/**'

- name: Run tests
  if: steps.changes.outputs.src == 'true'
  run: npm test
```

### Reduce Flakiness

```yaml
# Retry failed tests
- name: Test with retry
  uses: nick-fields/retry@v2
  with:
    timeout_minutes: 10
    max_attempts: 3
    command: npm test

# Increase timeouts for slow tests
- name: E2E tests
  run: npm run test:e2e
  timeout-minutes: 30
```

### Concurrency Control

```yaml
# Cancel in-progress runs
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

# Or queue runs
concurrency:
  group: deploy-${{ github.ref }}
  cancel-in-progress: false
```

---

## Workflow Triggers

### Common Triggers

```yaml
on:
  # Push to specific branches
  push:
    branches: [main, develop]
    paths-ignore:
      - '**.md'
      - 'docs/**'

  # Pull request events
  pull_request:
    branches: [main]
    types: [opened, synchronize, reopened]

  # Release events
  release:
    types: [published]

  # Schedule (cron)
  schedule:
    - cron: '0 0 * * *'  # Daily at midnight

  # Manual trigger
  workflow_dispatch:
    inputs:
      environment:
        description: 'Deploy environment'
        required: true
        default: 'staging'
        type: choice
        options:
          - staging
          - production
```

---

## Artifacts and Reports

```yaml
steps:
  - name: Run tests
    run: npm test -- --coverage

  # Upload coverage
  - name: Upload coverage
    uses: codecov/codecov-action@v3
    with:
      files: ./coverage/lcov.info

  # Upload test results
  - name: Upload test results
    uses: actions/upload-artifact@v4
    if: always()
    with:
      name: test-results
      path: |
        coverage/
        test-results/

  # Upload build artifacts
  - name: Upload build
    uses: actions/upload-artifact@v4
    with:
      name: build
      path: dist/
      retention-days: 7
```
