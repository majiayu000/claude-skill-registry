---
name: github-actions-cicd
description: Set up GitHub Actions CI/CD pipelines for testing, building, and deploying to Kubernetes. Use when implementing continuous integration and deployment for Phase 5. (project)
allowed-tools: Bash, Write, Read, Glob, Edit, Grep
---

# GitHub Actions CI/CD Skill

## Quick Start

1. **Read Phase 5 Constitution** - `constitution-prompt-phase-5.md`
2. **Create workflows directory** - `.github/workflows/`
3. **Set up CI pipeline** - Test, lint, build on PR
4. **Set up CD pipeline** - Deploy to staging/production
5. **Configure secrets** - Docker registry, K8s credentials
6. **Add branch protection** - Require CI to pass

## Workflow Structure

```
.github/
└── workflows/
    ├── ci.yaml           # Test & build on PR
    ├── cd-staging.yaml   # Deploy to staging
    ├── cd-production.yaml # Deploy to production
    └── security.yaml     # Security scanning
```

## CI Pipeline (Pull Requests)

Create `.github/workflows/ci.yaml`:

```yaml
name: CI Pipeline

on:
  pull_request:
    branches: [main, develop]
  push:
    branches: [main, develop]

env:
  REGISTRY: ghcr.io
  IMAGE_PREFIX: ${{ github.repository }}

jobs:
  # Backend Tests
  backend-test:
    name: Backend Tests
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: ./backend

    services:
      postgres:
        image: postgres:16-alpine
        env:
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
          POSTGRES_DB: todo_test
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v4

      - name: Install uv
        uses: astral-sh/setup-uv@v4
        with:
          version: "latest"

      - name: Set up Python
        run: uv python install 3.13

      - name: Install dependencies
        run: uv sync --frozen

      - name: Run linting
        run: uv run ruff check .

      - name: Run type checking
        run: uv run mypy src/

      - name: Run tests
        env:
          DATABASE_URL: postgresql://test:test@localhost:5432/todo_test
          BETTER_AUTH_SECRET: test-secret
          GEMINI_API_KEY: test-key
        run: uv run pytest tests/ -v --cov=src --cov-report=xml

      - name: Upload coverage
        uses: codecov/codecov-action@v4
        with:
          files: ./backend/coverage.xml
          flags: backend

  # Frontend Tests
  frontend-test:
    name: Frontend Tests
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: ./frontend

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
          cache-dependency-path: './frontend/package-lock.json'

      - name: Install dependencies
        run: npm ci

      - name: Run linting
        run: npm run lint

      - name: Run type checking
        run: npm run type-check

      - name: Run tests
        run: npm test -- --coverage

      - name: Build
        run: npm run build
        env:
          NEXT_PUBLIC_API_URL: http://localhost:8000

  # Build Docker Images
  build-images:
    name: Build Images
    runs-on: ubuntu-latest
    needs: [backend-test, frontend-test]
    if: github.event_name == 'push'

    permissions:
      contents: read
      packages: write

    strategy:
      matrix:
        service:
          - name: backend
            context: ./backend
            dockerfile: ./backend/Dockerfile
          - name: frontend
            context: ./frontend
            dockerfile: ./frontend/Dockerfile
          - name: notification-service
            context: ./services/notification
            dockerfile: ./services/notification/Dockerfile
          - name: recurring-service
            context: ./services/recurring
            dockerfile: ./services/recurring/Dockerfile

    steps:
      - uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Login to GHCR
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_PREFIX }}/${{ matrix.service.name }}
          tags: |
            type=sha,prefix=
            type=ref,event=branch
            type=semver,pattern={{version}}

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: ${{ matrix.service.context }}
          file: ${{ matrix.service.dockerfile }}
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

  # Helm Chart Validation
  helm-lint:
    name: Helm Lint
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Set up Helm
        uses: azure/setup-helm@v4
        with:
          version: v3.14.0

      - name: Lint charts
        run: helm lint ./helm/evolution-todo

      - name: Template validation
        run: |
          helm template evolution-todo ./helm/evolution-todo \
            --values ./helm/evolution-todo/values.yaml \
            --debug
```

## CD Pipeline (Staging)

Create `.github/workflows/cd-staging.yaml`:

```yaml
name: CD Staging

on:
  push:
    branches: [develop]
  workflow_dispatch:

env:
  REGISTRY: ghcr.io
  IMAGE_PREFIX: ${{ github.repository }}
  CLUSTER_NAME: todo-staging
  NAMESPACE: todo-staging

jobs:
  deploy-staging:
    name: Deploy to Staging
    runs-on: ubuntu-latest
    environment: staging

    steps:
      - uses: actions/checkout@v4

      - name: Install doctl
        uses: digitalocean/action-doctl@v2
        with:
          token: ${{ secrets.DIGITALOCEAN_ACCESS_TOKEN }}

      - name: Save DigitalOcean kubeconfig
        run: doctl kubernetes cluster kubeconfig save ${{ env.CLUSTER_NAME }}

      - name: Set up Helm
        uses: azure/setup-helm@v4
        with:
          version: v3.14.0

      - name: Deploy with Helm
        run: |
          helm upgrade --install evolution-todo ./helm/evolution-todo \
            --namespace ${{ env.NAMESPACE }} \
            --create-namespace \
            --values ./helm/evolution-todo/values-staging.yaml \
            --set global.image.tag=${{ github.sha }} \
            --set backend.env.DATABASE_URL=${{ secrets.STAGING_DATABASE_URL }} \
            --set backend.env.GEMINI_API_KEY=${{ secrets.GEMINI_API_KEY }} \
            --set backend.env.BETTER_AUTH_SECRET=${{ secrets.BETTER_AUTH_SECRET }} \
            --wait \
            --timeout 10m

      - name: Verify deployment
        run: |
          kubectl rollout status deployment/backend -n ${{ env.NAMESPACE }}
          kubectl rollout status deployment/frontend -n ${{ env.NAMESPACE }}

      - name: Run smoke tests
        run: |
          FRONTEND_URL=$(kubectl get svc frontend -n ${{ env.NAMESPACE }} -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
          curl -f http://$FRONTEND_URL/health || exit 1
```

## CD Pipeline (Production)

Create `.github/workflows/cd-production.yaml`:

```yaml
name: CD Production

on:
  release:
    types: [published]
  workflow_dispatch:
    inputs:
      version:
        description: 'Version to deploy'
        required: true

env:
  REGISTRY: ghcr.io
  IMAGE_PREFIX: ${{ github.repository }}
  CLUSTER_NAME: todo-production
  NAMESPACE: todo-app

jobs:
  deploy-production:
    name: Deploy to Production
    runs-on: ubuntu-latest
    environment: production

    steps:
      - uses: actions/checkout@v4

      - name: Determine version
        id: version
        run: |
          if [ "${{ github.event_name }}" == "release" ]; then
            echo "version=${{ github.event.release.tag_name }}" >> $GITHUB_OUTPUT
          else
            echo "version=${{ github.event.inputs.version }}" >> $GITHUB_OUTPUT
          fi

      - name: Install doctl
        uses: digitalocean/action-doctl@v2
        with:
          token: ${{ secrets.DIGITALOCEAN_ACCESS_TOKEN }}

      - name: Save DigitalOcean kubeconfig
        run: doctl kubernetes cluster kubeconfig save ${{ env.CLUSTER_NAME }}

      - name: Set up Helm
        uses: azure/setup-helm@v4
        with:
          version: v3.14.0

      - name: Deploy with Helm
        run: |
          helm upgrade --install evolution-todo ./helm/evolution-todo \
            --namespace ${{ env.NAMESPACE }} \
            --values ./helm/evolution-todo/values-production.yaml \
            --set global.image.tag=${{ steps.version.outputs.version }} \
            --set backend.env.DATABASE_URL=${{ secrets.PROD_DATABASE_URL }} \
            --set backend.env.GEMINI_API_KEY=${{ secrets.GEMINI_API_KEY }} \
            --set backend.env.BETTER_AUTH_SECRET=${{ secrets.BETTER_AUTH_SECRET }} \
            --set kafka.brokers=${{ secrets.REDPANDA_BROKERS }} \
            --wait \
            --timeout 15m

      - name: Verify deployment
        run: |
          kubectl rollout status deployment/backend -n ${{ env.NAMESPACE }} --timeout=5m
          kubectl rollout status deployment/frontend -n ${{ env.NAMESPACE }} --timeout=5m

      - name: Notify success
        if: success()
        uses: slackapi/slack-github-action@v1
        with:
          payload: |
            {
              "text": "Production deployment successful: ${{ steps.version.outputs.version }}"
            }
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK }}

      - name: Rollback on failure
        if: failure()
        run: |
          helm rollback evolution-todo -n ${{ env.NAMESPACE }}
```

## Security Scanning

Create `.github/workflows/security.yaml`:

```yaml
name: Security Scanning

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 0 * * 0'  # Weekly on Sunday

jobs:
  trivy-scan:
    name: Trivy Vulnerability Scan
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Run Trivy vulnerability scanner (repo)
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          scan-ref: '.'
          format: 'sarif'
          output: 'trivy-results.sarif'

      - name: Upload Trivy scan results
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: 'trivy-results.sarif'

  dependency-review:
    name: Dependency Review
    runs-on: ubuntu-latest
    if: github.event_name == 'pull_request'

    steps:
      - uses: actions/checkout@v4

      - name: Dependency Review
        uses: actions/dependency-review-action@v4
        with:
          fail-on-severity: high
```

## Required Secrets

Configure in GitHub Settings → Secrets and variables → Actions:

| Secret | Description | Used In |
|--------|-------------|---------|
| `DIGITALOCEAN_ACCESS_TOKEN` | DO API token | CD pipelines |
| `STAGING_DATABASE_URL` | Staging Neon DB URL | CD Staging |
| `PROD_DATABASE_URL` | Production Neon DB URL | CD Production |
| `GEMINI_API_KEY` | Google AI API key | All deployments |
| `BETTER_AUTH_SECRET` | Auth secret | All deployments |
| `REDPANDA_BROKERS` | Redpanda Cloud brokers | Production |
| `SLACK_WEBHOOK` | Slack notifications | CD Production |

## Branch Protection Rules

Configure in GitHub Settings → Branches → Branch protection rules:

```yaml
# For main branch
- Require pull request before merging
- Require status checks to pass:
  - backend-test
  - frontend-test
  - helm-lint
- Require branches to be up to date
- Require signed commits (optional)
- Include administrators
```

## Verification Checklist

- [ ] `.github/workflows/` directory created
- [ ] CI pipeline runs on PRs
- [ ] Docker images build and push to GHCR
- [ ] Helm charts lint successfully
- [ ] Staging deployment works
- [ ] Production deployment works
- [ ] All secrets configured
- [ ] Branch protection rules set
- [ ] Security scanning enabled

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Tests fail | Missing env vars | Add to workflow env |
| Push denied | No GHCR permission | Check `packages: write` |
| Helm deploy fails | Bad values | Run `helm template` locally |
| K8s auth fails | Bad kubeconfig | Check doctl token |

## References

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Build Push Action](https://github.com/docker/build-push-action)
- [Helm GitHub Actions](https://github.com/azure/setup-helm)
- [DigitalOcean Action](https://github.com/digitalocean/action-doctl)
- [Phase 5 Constitution](../../../constitution-prompt-phase-5.md)
