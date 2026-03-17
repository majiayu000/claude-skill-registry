---
name: ci-cd-pipelines
description: CI/CD pipeline design with GitHub Actions, GitLab CI, and best practices.
---

# CI/CD Pipelines

## GitHub Actions

```yaml
name: CI/CD

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
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - run: npm test

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: docker/setup-buildx-action@v3
      - uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      - uses: docker/build-push-action@v5
        with:
          push: true
          tags: ghcr.io/${{ github.repository }}:${{ github.sha }}

  deploy:
    needs: build
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment: production
    steps:
      - name: Deploy to Kubernetes
        run: |
          kubectl set image deployment/app \
            app=ghcr.io/${{ github.repository }}:${{ github.sha }}
```

## Pipeline Stages

```
Commit → Build → Test → Security → Deploy → Smoke Test
           │       │       │
           └───────┴───────┴── Parallel
```

## Best Practices

- **Fast feedback** - Tests < 10 min
- **Fail fast** - Critical checks first
- **Cache dependencies** - Avoid re-downloading
- **Immutable artifacts** - Tag with commit SHA
- **Environment parity** - Same image everywhere
- **Rollback ready** - Quick revert capability

## Secrets Management

```yaml
# GitHub Actions
env:
  DATABASE_URL: ${{ secrets.DATABASE_URL }}

# With OIDC (no secrets)
- uses: aws-actions/configure-aws-credentials@v4
  with:
    role-to-assume: arn:aws:iam::123456789:role/github-actions
    aws-region: us-east-1
```

## Deployment Strategies

| Strategy | Risk | Rollback |
|----------|------|----------|
| **Rolling** | Low | Slow |
| **Blue-Green** | Low | Fast |
| **Canary** | Very Low | Fast |
| **Recreate** | High | Fast |
