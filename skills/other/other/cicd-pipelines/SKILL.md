---
name: cicd-pipelines
description: Use when the DevOp is setting up CI/CD pipelines, configuring GitHub Actions, GitLab CI, build automation, deployment strategies (blue-green, canary, rolling), or managing build artifacts. Activates for pipeline creation, build optimization, or deployment configuration.
version: 1.0.0
---

# CI/CD Pipeline Expertise

## When This Applies

Apply this guidance when:
- Creating or modifying CI/CD pipeline configurations
- Setting up automated builds, tests, and deployments
- Choosing deployment strategies
- Optimizing build times
- Managing artifacts and releases

## Pipeline Design Principles

### Standard Pipeline Stages

```
Commit → Build → Test → Quality → Deploy (staging) → Deploy (production)
```

1. **Build** — Compile, bundle, create artifacts
2. **Test** — Unit tests, integration tests, e2e tests
3. **Quality** — Linting, type checking, security scanning
4. **Deploy Staging** — Deploy to staging environment
5. **Deploy Production** — Deploy to production (manual gate)

### GitHub Actions Template

```yaml
name: CI/CD Pipeline
on:
  push:
    branches: [development, main]
  pull_request:
    branches: [development]

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

  test:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - run: npm test -- --coverage
      - uses: actions/upload-artifact@v4
        with:
          name: coverage
          path: coverage/

  deploy-staging:
    needs: test
    if: github.ref == 'refs/heads/development'
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - run: echo "Deploy to staging"

  deploy-production:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment: production
    steps:
      - run: echo "Deploy to production"
```

## Deployment Strategies

| Strategy | Risk | Downtime | Rollback | Use When |
|----------|------|----------|----------|----------|
| **Rolling** | Low | Zero | Slow | Standard updates |
| **Blue-Green** | Low | Zero | Instant | Need instant rollback |
| **Canary** | Very Low | Zero | Fast | High-risk changes |
| **Recreate** | High | Yes | Slow | Database migrations |

### Blue-Green

- Run two identical environments (blue = current, green = new)
- Deploy to green, test, then switch traffic
- Keep blue running for instant rollback

### Canary

- Route 5-10% of traffic to new version
- Monitor error rates and performance
- Gradually increase if healthy
- Roll back immediately if problems detected

## Build Optimization

1. **Cache dependencies** — Use CI cache for node_modules, pip cache
2. **Parallel jobs** — Run independent tests in parallel
3. **Incremental builds** — Only rebuild what changed
4. **Slim base images** — Alpine-based images build faster
5. **Skip unnecessary steps** — Use path filters to skip irrelevant jobs

## Security in Pipelines

- Store secrets in CI/CD secret management (never in code)
- Use short-lived tokens where possible
- Pin action versions to specific SHAs (not tags)
- Run security scanning (dependency audit, SAST) in pipeline
- Restrict who can trigger production deployments
