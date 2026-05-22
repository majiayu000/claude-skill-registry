---
name: deployment-engineer
description: Deployment automation specialist for CI/CD pipelines and infrastructure. Use when setting up deployment, configuring CI/CD, or managing releases.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Deployment Engineer

Specialist in deployment automation, CI/CD pipelines, and infrastructure management.

## When This Skill Activates

Activates when you:
- Set up deployment pipeline
- Configure CI/CD
- Manage releases
- Automate infrastructure

## CI/CD Pipeline

### Pipeline Stages

```yaml
stages:
  - lint
  - test
  - build
  - security
  - deploy-dev
  - deploy-staging
  - deploy-production
```

### GitHub Actions Example

```yaml
name: CI/CD

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - run: npm ci
      - run: npm run lint

  test:
    runs-on: ubuntu-latest
    needs: lint
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm ci
      - run: npm test

  build:
    runs-on: ubuntu-latest
    needs: test
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm ci
      - run: npm run build
      - uses: actions/upload-artifact@v4
        with:
          name: build
          path: dist/

  deploy-production:
    runs-on: ubuntu-latest
    needs: build
    if: github.ref == 'refs/heads/main'
    environment: production
    steps:
      - uses: actions/checkout@v4
      - uses: actions/download-artifact@v4
        with:
          name: build
          path: dist/
      - run: npm run deploy
```

## Deployment Strategies

### 1. Blue-Green Deployment

```
         ┌─────────┐
         │  Load   │
         │ Balancer│
         └────┬────┘
              │
     ┌────────┴────────┐
     │    Switch       │
     ├────────┬────────┤
     ▼        ▼        ▼
  ┌─────┐ ┌─────┐ ┌─────┐
  │Blue │ │Green│ │     │
  └─────┘ └─────┘ └─────┘
```

### 2. Rolling Deployment

```
┌─────────────────────────────────────┐
│ v1  v1  v1  v1  v1  v1  v1  v1  v1 │ → Old
│ v2  v2  v2  v2  v2  v2  v2  v2  v2 │ → New
└─────────────────────────────────────┘
    ▲                       ▲
    │                       │
  Start                  End
```

### 3. Canary Deployment

```
┌──────────────────────────────────────┐
│ v1  v1  v1  v1  v1  v1  v1  v1  v1  v1 │ → Old
│ v2  v2  v2  v2                        │ → Canary (5%)
└──────────────────────────────────────┘

Monitor metrics, then:
│ v1  v1  v1  v1                        │ → Old (50%)
│ v2  v2  v2  v2  v2  v2  v2  v2  v2  v2 │ → New (50%)
```

## Environment Configuration

### Environment Variables

```bash
# Production
NODE_ENV=production
DATABASE_URL=postgresql://...
API_KEY=sk-...
SENTRY_DSN=https://example.com/123

# Development
NODE_ENV=development
DATABASE_URL=postgresql://localhost:5432/dev
```

### Configuration Management

```typescript
// config/production.ts
export default {
  database: {
    url: process.env.DATABASE_URL,
    poolSize: 20,
  },
  redis: {
    url: process.env.REDIS_URL,
  },
};
```

## Health Checks

```typescript
// GET /health
app.get('/health', (req, res) => {
  const health = {
    status: 'ok',
    timestamp: new Date().toISOString(),
    checks: {
      database: 'ok',
      redis: 'ok',
      external_api: 'ok',
    },
  };

  if (Object.values(health.checks).some(v => v !== 'ok')) {
    health.status = 'degraded';
    return res.status(503).json(health);
  }

  res.json(health);
});
```

## Rollback Strategy

```bash
# Kubernetes
kubectl rollout undo deployment/app

# Docker
docker-compose down
docker-compose up -d --scale app=<previous-version>

# Git
git revert HEAD
git push
```

## Monitoring & Logging

### Metrics to Track

- Deployment frequency
- Lead time for changes
- Mean time to recovery (MTTR)
- Change failure rate

### Logging

```typescript
// Structured logging
logger.info('Deployment started', {
  version: process.env.VERSION,
  environment: process.env.NODE_ENV,
  timestamp: new Date().toISOString(),
});
```

## Scripts

Generate deployment config:
```bash
python scripts/generate_deploy.py <environment>
```

Validate deployment:
```bash
python scripts/validate_deploy.py
```

## References

- `references/pipelines.md` - CI/CD pipeline examples
- `references/kubernetes.md` - K8s deployment configs
- `references/monitoring.md` - Monitoring setup
