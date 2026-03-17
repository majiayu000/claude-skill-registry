---
name: ci-cd-pipeline
description: Automated CI/CD pipeline setup with GitHub Actions, deployment strategies, and automation workflows. Use for build automation, testing, and deployment.
---

# 🚀 CI/CD Pipeline Skill

## GitHub Actions Workflows

### Basic CI Workflow
```yaml
# .github/workflows/ci.yml
name: CI
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - run: npm run lint
      - run: npm test
      - run: npm run build
```

### Deploy to Vercel
```yaml
# .github/workflows/deploy.yml
name: Deploy
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          vercel-args: '--prod'
```

---

## Deployment Strategies

| Strategy | Description | Risk | Rollback |
|----------|-------------|------|----------|
| Rolling | Replace instances gradually | Low | Slow |
| Blue-Green | Switch between environments | Low | Fast |
| Canary | Route % traffic to new version | Medium | Fast |
| Recreate | Stop old, start new | High | Slow |

---

## Environment Management

### Secrets Setup
```yaml
env:
  DATABASE_URL: ${{ secrets.DATABASE_URL }}
  API_KEY: ${{ secrets.API_KEY }}

# Environment-specific
jobs:
  deploy-staging:
    environment: staging
  deploy-production:
    environment: production
    needs: deploy-staging
```

### Branch Protection
```yaml
on:
  push:
    branches:
      - main      # Production
      - develop   # Staging
      - 'feature/*'  # Feature branches
```

---

## Docker Build Pipeline

```yaml
jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}
      
      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          push: true
          tags: user/app:latest
```

---

## Pipeline Checklist

- [ ] Lint code
- [ ] Run unit tests
- [ ] Run integration tests
- [ ] Build application
- [ ] Security scan (SAST)
- [ ] Deploy to staging
- [ ] Run E2E tests
- [ ] Deploy to production
- [ ] Health check
- [ ] Notify team
