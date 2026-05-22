---
name: ci-cd-pipeline
description: GitHub Actions workflow patterns, matrix builds, caching strategies, deployment pipelines, artifact management, and rollback procedures.
---

# CI/CD Pipeline Patterns

GitHub Actions workflows for consistent, fast, and reliable delivery pipelines.

## Workflow Structure

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]
  workflow_dispatch:        # manual trigger

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true  # cancel outdated runs on same branch

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - run: npm run lint

  test:
    runs-on: ubuntu-latest
    needs: lint              # runs after lint passes
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - run: npm test -- --coverage

  build:
    runs-on: ubuntu-latest
    needs: test
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - run: npm run build
```

## Matrix Builds

Test across multiple versions and operating systems in parallel.

```yaml
jobs:
  test:
    strategy:
      fail-fast: false       # don't cancel others if one fails
      matrix:
        node: ['18', '20', '22']
        os: [ubuntu-latest, macos-latest, windows-latest]
        exclude:
          - os: windows-latest
            node: '18'       # skip this combination

    runs-on: ${{ matrix.os }}
    name: Test Node ${{ matrix.node }} on ${{ matrix.os }}

    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node }}
          cache: 'npm'
      - run: npm ci
      - run: npm test
```

```yaml
# Python matrix example
jobs:
  test:
    strategy:
      matrix:
        python: ['3.10', '3.11', '3.12']
        django: ['4.2', '5.0']
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python }}
      - run: pip install django==${{ matrix.django }} -r requirements-test.txt
      - run: pytest
```

## Dependency Caching

```yaml
# Node.js: cache npm or yarn
- uses: actions/setup-node@v4
  with:
    node-version: '20'
    cache: 'npm'             # auto-caches ~/.npm

# Manual cache (more control)
- uses: actions/cache@v4
  id: npm-cache
  with:
    path: ~/.npm
    key: npm-${{ runner.os }}-${{ hashFiles('**/package-lock.json') }}
    restore-keys: |
      npm-${{ runner.os }}-

- run: npm ci
```

```yaml
# Python: cache pip
- uses: actions/cache@v4
  with:
    path: ~/.cache/pip
    key: pip-${{ runner.os }}-${{ hashFiles('**/requirements*.txt') }}
    restore-keys: |
      pip-${{ runner.os }}-

- run: pip install -r requirements.txt
```

```yaml
# Docker layer caching
- uses: docker/setup-buildx-action@v3

- uses: actions/cache@v4
  with:
    path: /tmp/.buildx-cache
    key: buildx-${{ runner.os }}-${{ github.sha }}
    restore-keys: |
      buildx-${{ runner.os }}-

- uses: docker/build-push-action@v5
  with:
    cache-from: type=local,src=/tmp/.buildx-cache
    cache-to: type=local,dest=/tmp/.buildx-cache-new,mode=max

# Prevent cache from growing unbounded
- run: |
    rm -rf /tmp/.buildx-cache
    mv /tmp/.buildx-cache-new /tmp/.buildx-cache
```

## Artifact Upload/Download Between Jobs

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci && npm run build

      - uses: actions/upload-artifact@v4
        with:
          name: build-output
          path: dist/
          retention-days: 7

  deploy:
    runs-on: ubuntu-latest
    needs: build
    steps:
      - uses: actions/download-artifact@v4
        with:
          name: build-output
          path: dist/

      - run: ls -la dist/    # verify artifact present
      - run: ./scripts/deploy.sh
```

## Environment Secrets Management

```yaml
# Repository secrets: Settings → Secrets and variables → Actions
# Environment secrets: require approval before use

jobs:
  deploy-production:
    environment: production     # requires approval + uses env secrets
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Deploy
        env:
          API_KEY: ${{ secrets.API_KEY }}
          DATABASE_URL: ${{ secrets.DATABASE_URL }}
        run: ./scripts/deploy.sh

      # Never echo secrets
      # ✅ GitHub masks them automatically in logs
      # ❌ Don't: run: echo ${{ secrets.API_KEY }}
```

## Full Deployment Pipeline

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '20', cache: 'npm' }
      - run: npm ci && npm run lint

  test:
    runs-on: ubuntu-latest
    needs: lint
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '20', cache: 'npm' }
      - run: npm ci && npm test

  build-and-push:
    runs-on: ubuntu-latest
    needs: test
    outputs:
      image-tag: ${{ steps.meta.outputs.tags }}

    steps:
      - uses: actions/checkout@v4

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
            type=sha,prefix=sha-
            type=raw,value=latest,enable=${{ github.ref == 'refs/heads/main' }}

      - uses: docker/build-push-action@v5
        with:
          push: true
          tags: ${{ steps.meta.outputs.tags }}

  deploy-staging:
    runs-on: ubuntu-latest
    needs: build-and-push
    environment: staging
    steps:
      - run: |
          ssh deploy@staging.example.com \
            "docker pull ghcr.io/${{ github.repository }}:latest && \
             docker compose up -d"

  smoke-test:
    runs-on: ubuntu-latest
    needs: deploy-staging
    steps:
      - run: |
          sleep 10
          curl -f https://staging.example.com/health || exit 1

  deploy-production:
    runs-on: ubuntu-latest
    needs: smoke-test
    environment: production       # requires manual approval
    steps:
      - run: |
          ssh deploy@prod.example.com \
            "docker pull ghcr.io/${{ github.repository }}:latest && \
             docker compose up -d"
```

## Conditional Job Execution

```yaml
jobs:
  deploy:
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    runs-on: ubuntu-latest
    steps:
      - run: echo "Deploying main branch"

  notify-failure:
    if: failure()               # only runs if previous job failed
    needs: [lint, test, build]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/github-script@v7
        with:
          script: |
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: 'CI failed. Please check the logs.'
            })
```

## Reusable Workflows and Composite Actions

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
      - run: npm ci && npm test
```

```yaml
# Caller workflow
jobs:
  test:
    uses: ./.github/workflows/reusable-test.yml
    with:
      node-version: '22'
    secrets:
      NPM_TOKEN: ${{ secrets.NPM_TOKEN }}
```

```yaml
# Composite action: .github/actions/setup-app/action.yml
name: Setup Application
description: Install deps and configure environment

runs:
  using: composite
  steps:
    - uses: actions/setup-node@v4
      with:
        node-version: '20'
        cache: 'npm'

    - run: npm ci
      shell: bash

    - run: npm run db:migrate
      shell: bash
      env:
        DATABASE_URL: ${{ env.DATABASE_URL }}
```

## Deployment Strategies

```yaml
# Blue-Green: switch traffic between two identical environments
- name: Deploy to Blue
  run: |
    kubectl set image deployment/app-blue app=my-image:${{ github.sha }}
    kubectl rollout status deployment/app-blue

- name: Run smoke tests on Blue
  run: curl -f https://blue.example.com/health

- name: Switch traffic to Blue
  run: |
    kubectl patch service app \
      -p '{"spec":{"selector":{"slot":"blue"}}}'

# Canary: gradual traffic shift
- name: Deploy Canary (10% traffic)
  run: |
    kubectl set image deployment/app-canary app=my-image:${{ github.sha }}
    kubectl patch virtualservice app \
      --type merge \
      -p '{"spec":{"http":[{"route":[
        {"destination":{"host":"app-stable"},"weight":90},
        {"destination":{"host":"app-canary"},"weight":10}
      ]}]}}'
```

## Rollback Procedures

```yaml
- name: Deploy with rollback on failure
  id: deploy
  run: |
    PREVIOUS_IMAGE=$(kubectl get deployment app -o jsonpath='{.spec.template.spec.containers[0].image}')
    echo "previous-image=$PREVIOUS_IMAGE" >> $GITHUB_OUTPUT

    kubectl set image deployment/app app=my-image:${{ github.sha }}
    kubectl rollout status deployment/app --timeout=5m || {
      echo "Rollback triggered"
      kubectl set image deployment/app app=$PREVIOUS_IMAGE
      kubectl rollout status deployment/app
      exit 1
    }
```

```bash
# Manual rollback command (kubectl)
kubectl rollout undo deployment/app
kubectl rollout undo deployment/app --to-revision=3

# Docker Compose rollback
docker compose pull && docker compose up -d
# or pin to previous image tag
IMAGE_TAG=sha-abc123 docker compose up -d
```

## Scheduled Jobs and PR Automation

```yaml
# Scheduled dependency update check
on:
  schedule:
    - cron: '0 9 * * 1'      # every Monday at 09:00 UTC

jobs:
  check-deps:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm outdated || true
      - run: npx npm-check-updates --errorLevel 2
```

```yaml
# Auto-label PR based on files changed
on:
  pull_request:
    types: [opened, synchronize]

jobs:
  label:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/labeler@v5
        with:
          repo-token: ${{ secrets.GITHUB_TOKEN }}
          configuration-path: .github/labeler.yml
```

## Status Badges

```markdown
<!-- README.md badges -->
![CI](https://github.com/owner/repo/actions/workflows/ci.yml/badge.svg)
![Coverage](https://codecov.io/gh/owner/repo/branch/main/graph/badge.svg)
```

**Key principle**: Fail fast in early stages (lint before test), cache aggressively, require approval gates for production, always have a rollback path.
