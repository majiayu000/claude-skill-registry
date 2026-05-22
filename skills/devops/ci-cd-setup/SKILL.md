---
name: ci-cd-setup
description: "Set up GitHub Actions or other CI/CD pipelines. Creates automated testing, building, and deployment workflows. Use when user says 'CI', 'CD', 'GitHub Actions', 'pipeline', 'automate testing', or 'deploy automation'."
allowed-tools: Read, Write, Edit
---

# CI/CD Setup

You are an expert at setting up CI/CD pipelines.

## When To Use

- User says "Set up CI", "GitHub Actions"
- User asks to "Automate testing/deployment"
- New project needs CI/CD
- Adding deployment automation

## Inputs

- Test command
- Build command
- Deployment target (if any)
- Branch strategy

## Outputs

- `.github/workflows/ci.yml`
- Optional: deployment workflow
- Documentation

## Basic CI Workflow

```yaml
name: CI

on:
  push:
    branches: [main, master]
  pull_request:
    branches: [main, master]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: "pip"

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Run tests
        run: pytest --cov=src --cov-report=xml

      - name: Upload coverage
        uses: codecov/codecov-action@v4
        with:
          file: coverage.xml
```

## Workflow Stages

| Stage | Purpose | When |
|-------|---------|------|
| Lint | Code style | Every push |
| Test | Unit/integration tests | Every push |
| Build | Create artifacts | On main/tags |
| Deploy staging | Deploy to staging | On main |
| Deploy prod | Deploy to production | On tags |

## Language-Specific Workflows

### Python

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: "pip"
      - run: pip install -r requirements.txt
      - run: pytest
```

### Node.js

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: "20"
          cache: "npm"
      - run: npm ci
      - run: npm test
```

### Go

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-go@v5
        with:
          go-version: "1.21"
      - run: go test ./...
```

## Full CI/CD Example

```yaml
name: CI/CD

on:
  push:
    branches: [main]
    tags: ['v*']
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: "pip"
      - run: pip install -r requirements.txt
      - run: pytest

  build:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main' || startsWith(github.ref, 'refs/tags/')
    steps:
      - uses: actions/checkout@v4
      - name: Build Docker image
        run: docker build -t myapp:${{ github.sha }} .
      - name: Push to registry
        run: |
          echo ${{ secrets.DOCKER_PASSWORD }} | docker login -u ${{ secrets.DOCKER_USERNAME }} --password-stdin
          docker push myapp:${{ github.sha }}

  deploy-staging:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    environment: staging
    steps:
      - name: Deploy to staging
        run: |
          ssh user@staging "docker pull myapp:${{ github.sha }} && docker-compose up -d"

  deploy-production:
    needs: build
    runs-on: ubuntu-latest
    if: startsWith(github.ref, 'refs/tags/')
    environment: production
    steps:
      - name: Deploy to production
        run: |
          ssh user@production "docker pull myapp:${{ github.sha }} && docker-compose up -d"
```

## Caching

### pip

```yaml
- uses: actions/setup-python@v5
  with:
    cache: "pip"
```

### npm

```yaml
- uses: actions/setup-node@v4
  with:
    cache: "npm"
```

### Custom cache

```yaml
- uses: actions/cache@v4
  with:
    path: ~/.cache/custom
    key: custom-${{ runner.os }}-${{ hashFiles('**/lockfile') }}
```

## Secrets Management

```yaml
steps:
  - name: Deploy
    env:
      API_KEY: ${{ secrets.API_KEY }}
    run: ./deploy.sh
```

Add secrets in: Settings → Secrets and variables → Actions

## Branch Protection

Recommended settings:
- Require pull request reviews
- Require status checks to pass
- Require branches to be up to date
- Include administrators

## Anti-Patterns

- No caching (slow builds)
- Secrets in workflow files
- No branch protection
- Missing status checks before merge
- Running tests only on main (should run on PRs)
- No environment separation

## Keywords

CI, CD, GitHub Actions, pipeline, automate testing, deploy, workflow
