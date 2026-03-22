---
name: pipeline-patterns
description: >
  Guide for designing CI/CD pipelines with artifact management, environment promotion,
  parallel jobs, quality gates, and notifications. Use when the user designs a CI/CD pipeline,
  asks about deployment workflows, needs to structure build-test-deploy stages, or wants to
  optimize pipeline performance. Trigger whenever CI/CD architecture or pipeline design is discussed.
---

# Pipeline Patterns

Design robust CI/CD pipelines with clear stage separation, proper artifact flow,
environment promotion, quality gates, and failure handling.

## When to Use
- User designs a new CI/CD pipeline
- User asks about build, test, deploy stage organization
- User needs environment promotion (dev -> staging -> prod)
- User wants to optimize pipeline speed with parallelism
- User asks about quality gates or approval workflows

## Core Patterns

### Pipeline Stage Architecture

Structure pipelines in clear stages with explicit dependencies and artifact passing.

```
Build --> Lint --|
                |--> Integration Tests --> Deploy Staging --> E2E Tests --> Deploy Prod
         Unit --|
```

```yaml
# GitHub Actions implementation
jobs:
  build:
    runs-on: ubuntu-latest
    outputs:
      image-tag: ${{ steps.meta.outputs.tags }}
    steps:
      - uses: actions/checkout@v4
      - id: meta
        uses: docker/metadata-action@v5
        with:
          images: ghcr.io/${{ github.repository }}
          tags: type=sha
      - uses: docker/build-push-action@v5
        with:
          push: true
          tags: ${{ steps.meta.outputs.tags }}

  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci && npm run lint

  unit-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci && npm test

  integration-test:
    needs: [build, lint, unit-test]
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env: { POSTGRES_DB: test, POSTGRES_PASSWORD: test }
        options: --health-cmd pg_isready --health-interval 5s --health-retries 5
    steps:
      - uses: actions/checkout@v4
      - run: npm ci && npm run test:integration

  deploy-staging:
    needs: integration-test
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - run: echo "Deploy ${{ needs.build.outputs.image-tag }} to staging"

  e2e-test:
    needs: deploy-staging
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npx playwright test --project=staging

  deploy-production:
    needs: e2e-test
    runs-on: ubuntu-latest
    environment:
      name: production
      url: https://myapp.com
    steps:
      - run: echo "Deploy ${{ needs.build.outputs.image-tag }} to production"
```

### Artifact Management

Build once, deploy everywhere. Pass artifacts between stages to ensure consistency.

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci && npm run build
      - uses: actions/upload-artifact@v4
        with:
          name: app-build-${{ github.sha }}
          path: dist/
          retention-days: 7

  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/download-artifact@v4
        with:
          name: app-build-${{ github.sha }}
          path: dist/
      - run: ./scripts/deploy.sh dist/
```

### Quality Gates

Enforce quality standards before promotion to the next environment.

```yaml
jobs:
  quality-gate:
    needs: [unit-test, lint, security-scan]
    runs-on: ubuntu-latest
    steps:
      - name: Check test coverage
        run: |
          COVERAGE=$(cat coverage/coverage-summary.json | jq '.total.lines.pct')
          if (( $(echo "$COVERAGE < 80" | bc -l) )); then
            echo "Coverage $COVERAGE% is below 80% threshold"
            exit 1
          fi

      - name: Check lint results
        run: |
          if [ "${{ needs.lint.result }}" != "success" ]; then
            echo "Lint check failed"
            exit 1
          fi

      - name: Check security scan
        run: |
          if [ "${{ needs.security-scan.result }}" != "success" ]; then
            echo "Security vulnerabilities found"
            exit 1
          fi
```

### Environment Promotion with Approvals

Use GitHub environments to enforce manual approvals for production deployments.

```yaml
jobs:
  deploy-staging:
    environment: staging
    runs-on: ubuntu-latest
    steps:
      - run: deploy --env staging

  smoke-test:
    needs: deploy-staging
    runs-on: ubuntu-latest
    steps:
      - run: curl -f https://staging.myapp.com/health

  deploy-production:
    needs: smoke-test
    environment:
      name: production         # Requires manual approval in GitHub settings
      url: https://myapp.com
    runs-on: ubuntu-latest
    steps:
      - run: deploy --env production
```

### Parallel Test Splitting

Split large test suites across parallel runners to reduce pipeline duration.

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        shard: [1, 2, 3, 4]
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - run: npx jest --shard=${{ matrix.shard }}/4

  merge-coverage:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - run: echo "Merge coverage from all shards"
```

## Anti-Patterns

- **Build per environment**: Build the artifact once and promote it. Rebuilding per environment risks deploying different code to staging and production.
- **No quality gates**: Deploying without coverage, lint, or security checks allows regressions to reach production.
- **Sequential everything**: Independent jobs like lint, unit tests, and security scans should run in parallel. Only use `needs` for true dependencies.
- **Skipping staging**: Always deploy to a staging environment before production. E2E tests against staging catch integration issues that unit tests miss.
- **No rollback plan**: Every deploy pipeline must have a documented and tested rollback path. If the pipeline cannot roll back, it is not production-ready.
- **Secrets in logs**: Never echo secrets. Use `add-mask` to redact sensitive values in output.

## Quick Reference

```
Pipeline Design Checklist:
[ ] Build once, deploy many (single artifact)
[ ] Parallel independent jobs (lint, test, scan)
[ ] Quality gates before promotion
[ ] Environment-specific configs (not rebuilt code)
[ ] Manual approval for production
[ ] Rollback procedure documented and tested
[ ] Notifications on failure
[ ] Artifact retention policy defined
[ ] Concurrency controls to prevent duplicate runs
[ ] Timeout limits on all jobs
```
