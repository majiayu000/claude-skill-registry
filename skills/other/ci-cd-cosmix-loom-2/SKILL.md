---
name: ci-cd
description: Designs and implements CI/CD pipelines for automated testing, building, deployment, and security scanning across multiple platforms. Covers pipeline optimization, test integration, artifact management, and release automation.
trigger-keywords: CI/CD, pipeline, workflow, GitHub Actions, GitLab CI, Jenkins, CircleCI, Travis CI, Azure Pipelines, build, deploy, deployment, release, artifact, stage, job, runner, action, automation, continuous integration, continuous deployment, continuous delivery, container registry, docker build, image push, canary deployment, blue-green deployment, rolling update, rollback, integration tests, smoke tests, security scanning, SAST, DAST, dependency scanning, secrets management, cache optimization, parallelization, monorepo CI, matrix build, self-hosted runner, ML pipeline, model training pipeline, model deployment
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
---

# CI/CD

## Overview

This skill covers the complete lifecycle of CI/CD pipeline design, implementation, and optimization across platforms including GitHub Actions, GitLab CI, Jenkins, CircleCI, and cloud-native solutions. It encompasses automated testing integration, security scanning, artifact management, deployment strategies, and specialized pipelines for ML workloads.

## When to Use

- Implementing or migrating CI/CD pipelines
- Optimizing build and test execution times
- Integrating security scanning (SAST, DAST, dependency checks)
- Setting up deployment automation with rollback strategies
- Configuring test suites in CI environments
- Managing artifacts and container registries
- Implementing ML model training and deployment pipelines
- Troubleshooting pipeline failures and flakiness

## Instructions

### 1. Analyze Requirements

- Identify build and test requirements
- Determine deployment targets and environments
- Assess security scanning needs (SAST, DAST, secrets, dependencies)
- Plan environment promotion strategy (dev → staging → production)
- Define quality gates and approval workflows
- Identify test suite composition (unit, integration, E2E)
- Determine artifact storage and retention policies

### 2. Design Pipeline Architecture

- Structure stages logically with clear dependencies
- Optimize for speed through parallelization and caching
- Design fail-fast strategy (lint → unit tests → integration tests → build)
- Plan secret management and secure credential handling
- Define deployment strategies (rolling, blue-green, canary)
- Architect for rollback and recovery procedures
- Design matrix builds for multi-platform support
- Plan monorepo CI strategies if applicable

### 3. Implement Testing Integration

- Configure unit test execution with coverage reporting
- Set up integration tests with service dependencies (databases, APIs)
- Implement E2E/smoke tests for critical user journeys
- Configure test parallelization and sharding
- Integrate test result reporting (JUnit, TAP, JSON)
- Set up flaky test detection and quarantine
- Configure performance/load testing stages
- Implement visual regression testing if applicable

### 4. Implement Security Scanning

- Integrate SAST (static analysis) tools (SonarQube, CodeQL, Semgrep)
- Configure DAST (dynamic analysis) for deployed environments
- Set up dependency/vulnerability scanning (Dependabot, Snyk, Trivy)
- Implement container image scanning
- Configure secrets detection (GitGuardian, TruffleHog)
- Set up license compliance checking
- Define security gate thresholds and failure policies

### 5. Implement Build and Artifact Management

- Configure dependency caching strategies
- Implement build output caching and layer caching (Docker)
- Set up artifact versioning and tagging
- Configure container registry integration
- Implement multi-stage builds for optimization
- Set up artifact signing and attestation
- Configure artifact retention and cleanup policies

### 6. Implement Deployment Automation

- Configure environment-specific deployments
- Implement deployment strategies (rolling, blue-green, canary)
- Set up health checks and readiness probes
- Configure smoke tests post-deployment
- Implement automated rollback on failure
- Set up deployment notifications (Slack, email, PagerDuty)
- Configure manual approval gates for production

### 7. Optimize Pipeline Performance

- Analyze pipeline execution times and bottlenecks
- Implement job parallelization for independent tasks
- Configure aggressive caching (dependencies, build outputs, Docker layers)
- Optimize test execution (parallel runners, test sharding)
- Use matrix builds efficiently
- Consider self-hosted runners for performance-critical workloads
- Implement conditional job execution (path filters, change detection)

### 8. Ensure Reliability and Observability

- Add retry logic for transient failures
- Implement comprehensive error handling
- Configure alerts for pipeline failures
- Set up metrics and dashboards for pipeline health
- Document runbooks and troubleshooting procedures
- Implement audit logging for deployments
- Configure SLO tracking for pipeline performance

## Best Practices

### Core Principles

1. **Fail Fast**: Run cheap, fast checks first (lint, type check, unit tests)
2. **Parallelize Aggressively**: Run independent jobs concurrently
3. **Cache Everything**: Dependencies, build outputs, Docker layers
4. **Secure by Default**: Secrets in vaults, least privilege, audit logs
5. **Environment Parity**: Keep dev/staging/prod as similar as possible
6. **Immutable Artifacts**: Build once, promote everywhere
7. **Automated Rollback**: Every deployment must be reversible
8. **Idempotent Operations**: Pipelines should be safely re-runnable

### Testing in CI/CD

1. **Test Pyramid**: More unit tests, fewer integration tests, minimal E2E
2. **Isolation**: Tests should not depend on execution order
3. **Determinism**: Eliminate flaky tests or quarantine them
4. **Fast Feedback**: Unit tests < 5min, full suite < 15min target
5. **Coverage Gates**: Enforce minimum coverage thresholds
6. **Service Mocking**: Use test doubles for external dependencies

### Security

1. **Shift Left**: Run security scans early in the pipeline
2. **Dependency Scanning**: Check for CVEs in all dependencies
3. **Secrets Management**: Never hardcode secrets, use secure vaults
4. **Least Privilege**: Minimal permissions for pipeline runners
5. **Supply Chain Security**: Verify and sign artifacts
6. **Audit Trail**: Log all deployments and access

### Performance

1. **Incremental Builds**: Only rebuild changed components
2. **Layer Caching**: Optimize Dockerfile layer order
3. **Dependency Locking**: Pin versions for reproducibility
4. **Resource Limits**: Prevent resource exhaustion
5. **Path Filtering**: Skip jobs when irrelevant files change

## Examples

### Example 1: GitHub Actions Workflow

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  NODE_VERSION: "20"
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: "npm"

      - name: Install dependencies
        run: npm ci

      - name: Run linter
        run: npm run lint

  test:
    runs-on: ubuntu-latest
    needs: lint
    services:
      postgres:
        image: postgres:16
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

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: "npm"

      - name: Install dependencies
        run: npm ci

      - name: Run tests
        run: npm test -- --coverage
        env:
          DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage/lcov.info

  build:
    runs-on: ubuntu-latest
    needs: test
    permissions:
      contents: read
      packages: write

    steps:
      - uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Log in to Container Registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=ref,event=branch
            type=ref,event=pr
            type=sha,prefix=
            type=raw,value=latest,enable=${{ github.ref == 'refs/heads/main' }}

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

  deploy-staging:
    runs-on: ubuntu-latest
    needs: build
    if: github.ref == 'refs/heads/develop'
    environment: staging

    steps:
      - uses: actions/checkout@v4

      - name: Deploy to staging
        uses: azure/k8s-deploy@v4
        with:
          namespace: staging
          manifests: |
            k8s/deployment.yaml
            k8s/service.yaml
          images: |
            ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}

  deploy-production:
    runs-on: ubuntu-latest
    needs: build
    if: github.ref == 'refs/heads/main'
    environment: production

    steps:
      - uses: actions/checkout@v4

      - name: Deploy to production
        uses: azure/k8s-deploy@v4
        with:
          namespace: production
          manifests: |
            k8s/deployment.yaml
            k8s/service.yaml
          images: |
            ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}
          strategy: canary
          percentage: 20
```

### Example 2: GitLab CI Pipeline

```yaml
stages:
  - validate
  - test
  - build
  - deploy

variables:
  DOCKER_TLS_CERTDIR: "/certs"
  IMAGE_TAG: $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA

.node-base:
  image: node:20-alpine
  cache:
    key: ${CI_COMMIT_REF_SLUG}
    paths:
      - node_modules/

lint:
  stage: validate
  extends: .node-base
  script:
    - npm ci
    - npm run lint
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH == "main"

test:
  stage: test
  extends: .node-base
  services:
    - postgres:16
  variables:
    POSTGRES_DB: test
    POSTGRES_USER: runner
    POSTGRES_PASSWORD: runner
    DATABASE_URL: postgresql://runner:runner@postgres:5432/test
  script:
    - npm ci
    - npm test -- --coverage
  coverage: '/Lines\s*:\s*(\d+\.?\d*)%/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage/cobertura-coverage.xml
      junit: junit.xml

build:
  stage: build
  image: docker:24
  services:
    - docker:24-dind
  script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
    - docker build -t $IMAGE_TAG .
    - docker push $IMAGE_TAG
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
    - if: $CI_COMMIT_BRANCH == "develop"

deploy-staging:
  stage: deploy
  image: bitnami/kubectl:latest
  script:
    - kubectl set image deployment/app app=$IMAGE_TAG -n staging
    - kubectl rollout status deployment/app -n staging --timeout=300s
  environment:
    name: staging
    url: https://staging.example.com
  rules:
    - if: $CI_COMMIT_BRANCH == "develop"

deploy-production:
  stage: deploy
  image: bitnami/kubectl:latest
  script:
    - kubectl set image deployment/app app=$IMAGE_TAG -n production
    - kubectl rollout status deployment/app -n production --timeout=300s
  environment:
    name: production
    url: https://example.com
  when: manual
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
```

### Example 3: Reusable Workflow (GitHub Actions)

```yaml
# .github/workflows/reusable-deploy.yml
name: Reusable Deploy Workflow

on:
  workflow_call:
    inputs:
      environment:
        required: true
        type: string
      image-tag:
        required: true
        type: string
    secrets:
      KUBE_CONFIG:
        required: true

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: ${{ inputs.environment }}

    steps:
      - uses: actions/checkout@v4

      - name: Set up kubectl
        uses: azure/setup-kubectl@v3

      - name: Configure kubeconfig
        run: |
          mkdir -p ~/.kube
          echo "${{ secrets.KUBE_CONFIG }}" | base64 -d > ~/.kube/config

      - name: Deploy
        run: |
          kubectl set image deployment/app \
            app=${{ inputs.image-tag }} \
            -n ${{ inputs.environment }}

          kubectl rollout status deployment/app \
            -n ${{ inputs.environment }} \
            --timeout=300s

      - name: Verify deployment
        run: |
          kubectl get pods -n ${{ inputs.environment }} -l app=app
          kubectl logs -n ${{ inputs.environment }} -l app=app --tail=50
```

### Example 4: Security Scanning Pipeline

```yaml
name: Security Scanning

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]
  schedule:
    - cron: "0 0 * * 0" # Weekly scan

jobs:
  sast:
    name: Static Analysis (SAST)
    runs-on: ubuntu-latest
    permissions:
      security-events: write
      contents: read

    steps:
      - uses: actions/checkout@v4

      - name: Initialize CodeQL
        uses: github/codeql-action/init@v3
        with:
          languages: javascript, python

      - name: Autobuild
        uses: github/codeql-action/autobuild@v3

      - name: Perform CodeQL Analysis
        uses: github/codeql-action/analyze@v3

      - name: SonarCloud Scan
        uses: SonarSource/sonarcloud-github-action@master
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
        with:
          args: >
            -Dsonar.organization=myorg
            -Dsonar.projectKey=myproject
            -Dsonar.qualitygate.wait=true

  dependency-scan:
    name: Dependency Vulnerability Scan
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Run Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: "fs"
          scan-ref: "."
          format: "sarif"
          output: "trivy-results.sarif"
          severity: "CRITICAL,HIGH"

      - name: Upload Trivy results to GitHub Security
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: "trivy-results.sarif"

      - name: Snyk Security Scan
        uses: snyk/actions/node@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
        with:
          args: --severity-threshold=high

  secrets-scan:
    name: Secrets Detection
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0 # Full history for secret detection

      - name: TruffleHog Scan
        uses: trufflesecurity/trufflehog@main
        with:
          path: ./
          base: ${{ github.event.repository.default_branch }}
          head: HEAD

      - name: GitGuardian Scan
        uses: GitGuardian/ggshield-action@v1
        env:
          GITHUB_PUSH_BEFORE_SHA: ${{ github.event.before }}
          GITHUB_PUSH_BASE_SHA: ${{ github.event.base }}
          GITHUB_DEFAULT_BRANCH: ${{ github.event.repository.default_branch }}
          GITGUARDIAN_API_KEY: ${{ secrets.GITGUARDIAN_API_KEY }}

  container-scan:
    name: Container Image Scan
    runs-on: ubuntu-latest
    needs: [sast, dependency-scan]

    steps:
      - uses: actions/checkout@v4

      - name: Build image
        run: docker build -t myapp:${{ github.sha }} .

      - name: Scan image with Trivy
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: "myapp:${{ github.sha }}"
          format: "sarif"
          output: "trivy-image-results.sarif"

      - name: Scan image with Grype
        uses: anchore/scan-action@v3
        with:
          image: "myapp:${{ github.sha }}"
          fail-build: true
          severity-cutoff: high
```

### Example 5: Test Integration with Parallelization

```yaml
name: Test Suite

on: [push, pull_request]

jobs:
  unit-tests:
    name: Unit Tests
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: [18, 20, 22]
        os: [ubuntu-latest, macos-latest, windows-latest]

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js ${{ matrix.node-version }}
        uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
          cache: "npm"

      - name: Install dependencies
        run: npm ci

      - name: Run unit tests
        run: npm run test:unit -- --coverage --maxWorkers=4

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage/coverage-final.json
          flags: unit-${{ matrix.os }}-node${{ matrix.node-version }}

  integration-tests:
    name: Integration Tests
    runs-on: ubuntu-latest
    strategy:
      matrix:
        shard: [1, 2, 3, 4]

    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: test
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432

      redis:
        image: redis:7
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 6379:6379

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: "npm"

      - name: Install dependencies
        run: npm ci

      - name: Run integration tests (shard ${{ matrix.shard }}/4)
        run: npm run test:integration -- --shard=${{ matrix.shard }}/4
        env:
          DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test
          REDIS_URL: redis://localhost:6379

      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: integration-test-results-${{ matrix.shard }}
          path: test-results/

  e2e-tests:
    name: E2E Tests
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: "npm"

      - name: Install dependencies
        run: npm ci

      - name: Install Playwright
        run: npx playwright install --with-deps

      - name: Build application
        run: npm run build

      - name: Run E2E tests
        run: npm run test:e2e

      - name: Upload Playwright report
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: playwright-report
          path: playwright-report/

  test-report:
    name: Generate Test Report
    runs-on: ubuntu-latest
    needs: [unit-tests, integration-tests, e2e-tests]
    if: always()

    steps:
      - uses: actions/checkout@v4

      - name: Download all test results
        uses: actions/download-artifact@v4
        with:
          path: test-results/

      - name: Generate combined report
        run: |
          npm install -g junit-viewer
          junit-viewer --results=test-results/ --save=test-report.html

      - name: Upload combined report
        uses: actions/upload-artifact@v4
        with:
          name: combined-test-report
          path: test-report.html
```

### Example 6: ML Pipeline (Model Training & Deployment)

```yaml
name: ML Pipeline

on:
  push:
    branches: [main]
    paths:
      - "models/**"
      - "training/**"
      - "data/**"
  workflow_dispatch:
    inputs:
      model-version:
        description: "Model version to train"
        required: true
        type: string

jobs:
  data-validation:
    name: Validate Training Data
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"
          cache: "pip"

      - name: Install dependencies
        run: |
          pip install pandas great-expectations dvc

      - name: Pull data with DVC
        run: |
          dvc remote modify origin --local auth basic
          dvc remote modify origin --local user ${{ secrets.DVC_USER }}
          dvc remote modify origin --local password ${{ secrets.DVC_PASSWORD }}
          dvc pull

      - name: Validate data schema
        run: python scripts/validate_data.py

      - name: Run Great Expectations
        run: great_expectations checkpoint run training_data_checkpoint

  train-model:
    name: Train ML Model
    runs-on: ubuntu-latest
    needs: data-validation

    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"
          cache: "pip"

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install mlflow wandb

      - name: Configure MLflow
        run: |
          echo "MLFLOW_TRACKING_URI=${{ secrets.MLFLOW_TRACKING_URI }}" >> $GITHUB_ENV
          echo "MLFLOW_TRACKING_USERNAME=${{ secrets.MLFLOW_USERNAME }}" >> $GITHUB_ENV
          echo "MLFLOW_TRACKING_PASSWORD=${{ secrets.MLFLOW_PASSWORD }}" >> $GITHUB_ENV

      - name: Train model
        run: |
          python training/train.py \
            --experiment-name "prod-training" \
            --model-version ${{ inputs.model-version || github.sha }} \
            --config training/config.yaml
        env:
          WANDB_API_KEY: ${{ secrets.WANDB_API_KEY }}

      - name: Upload model artifact
        uses: actions/upload-artifact@v4
        with:
          name: trained-model
          path: models/output/

  evaluate-model:
    name: Evaluate Model Performance
    runs-on: ubuntu-latest
    needs: train-model

    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"
          cache: "pip"

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Download model
        uses: actions/download-artifact@v4
        with:
          name: trained-model
          path: models/output/

      - name: Run model evaluation
        run: python evaluation/evaluate.py --model-path models/output/

      - name: Check performance thresholds
        run: |
          python evaluation/check_metrics.py \
            --min-accuracy 0.85 \
            --min-f1 0.80

      - name: Generate model card
        run: python scripts/generate_model_card.py

  deploy-model:
    name: Deploy Model to Production
    runs-on: ubuntu-latest
    needs: evaluate-model
    if: github.ref == 'refs/heads/main'
    environment: production

    steps:
      - uses: actions/checkout@v4

      - name: Download model
        uses: actions/download-artifact@v4
        with:
          name: trained-model
          path: models/output/

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1

      - name: Upload model to S3
        run: |
          aws s3 cp models/output/model.pkl \
            s3://my-ml-models/prod/${{ github.sha }}/model.pkl

      - name: Deploy to SageMaker
        run: |
          python deployment/deploy_sagemaker.py \
            --model-uri s3://my-ml-models/prod/${{ github.sha }}/model.pkl \
            --endpoint-name prod-ml-endpoint \
            --instance-type ml.m5.large

      - name: Run smoke tests
        run: python deployment/smoke_test.py --endpoint prod-ml-endpoint

      - name: Update model registry
        run: |
          python scripts/register_model.py \
            --version ${{ github.sha }} \
            --stage production \
            --metadata models/output/metadata.json
```

### Example 7: Monorepo CI with Path Filtering

```yaml
name: Monorepo CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  detect-changes:
    name: Detect Changed Services
    runs-on: ubuntu-latest
    outputs:
      api: ${{ steps.filter.outputs.api }}
      web: ${{ steps.filter.outputs.web }}
      worker: ${{ steps.filter.outputs.worker }}
      shared: ${{ steps.filter.outputs.shared }}

    steps:
      - uses: actions/checkout@v4

      - uses: dorny/paths-filter@v3
        id: filter
        with:
          filters: |
            api:
              - 'services/api/**'
              - 'packages/shared/**'
            web:
              - 'services/web/**'
              - 'packages/shared/**'
            worker:
              - 'services/worker/**'
              - 'packages/shared/**'
            shared:
              - 'packages/shared/**'

  test-api:
    name: Test API Service
    needs: detect-changes
    if: needs.detect-changes.outputs.api == 'true'
    runs-on: ubuntu-latest

    defaults:
      run:
        working-directory: services/api

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: "npm"
          cache-dependency-path: services/api/package-lock.json

      - name: Install dependencies
        run: npm ci

      - name: Run tests
        run: npm test

  test-web:
    name: Test Web Service
    needs: detect-changes
    if: needs.detect-changes.outputs.web == 'true'
    runs-on: ubuntu-latest

    defaults:
      run:
        working-directory: services/web

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: "npm"
          cache-dependency-path: services/web/package-lock.json

      - name: Install dependencies
        run: npm ci

      - name: Run tests
        run: npm test

      - name: Build
        run: npm run build

  test-worker:
    name: Test Worker Service
    needs: detect-changes
    if: needs.detect-changes.outputs.worker == 'true'
    runs-on: ubuntu-latest

    defaults:
      run:
        working-directory: services/worker

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: "npm"
          cache-dependency-path: services/worker/package-lock.json

      - name: Install dependencies
        run: npm ci

      - name: Run tests
        run: npm test

  build-and-deploy:
    name: Build and Deploy Changed Services
    needs: [detect-changes, test-api, test-web, test-worker]
    if: |
      always() &&
      (needs.test-api.result == 'success' || needs.test-api.result == 'skipped') &&
      (needs.test-web.result == 'success' || needs.test-web.result == 'skipped') &&
      (needs.test-worker.result == 'success' || needs.test-worker.result == 'skipped')
    runs-on: ubuntu-latest
    strategy:
      matrix:
        service:
          - name: api
            changed: ${{ needs.detect-changes.outputs.api == 'true' }}
          - name: web
            changed: ${{ needs.detect-changes.outputs.web == 'true' }}
          - name: worker
            changed: ${{ needs.detect-changes.outputs.worker == 'true' }}

    steps:
      - uses: actions/checkout@v4
        if: matrix.service.changed == 'true'

      - name: Build and push ${{ matrix.service.name }}
        if: matrix.service.changed == 'true'
        run: |
          docker build -t myapp-${{ matrix.service.name }}:${{ github.sha }} \
            services/${{ matrix.service.name }}
          docker push myapp-${{ matrix.service.name }}:${{ github.sha }}
```

### Example 8: Performance Optimization Pipeline

```yaml
name: Optimized CI Pipeline

on: [push, pull_request]

jobs:
  # Fast feedback jobs run first
  quick-checks:
    name: Quick Checks (< 2min)
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: "npm"

      - name: Cache node_modules
        uses: actions/cache@v4
        with:
          path: node_modules
          key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
          restore-keys: |
            ${{ runner.os }}-node-

      - name: Install dependencies
        run: npm ci --prefer-offline --no-audit

      - name: Parallel lint and type check
        run: |
          npm run lint &
          npm run type-check &
          wait

  unit-tests-fast:
    name: Unit Tests (Changed Files Only)
    runs-on: ubuntu-latest
    if: github.event_name == 'pull_request'

    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0 # Need full history for changed files

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: "npm"

      - name: Install dependencies
        run: npm ci --prefer-offline

      - name: Get changed files
        id: changed-files
        run: |
          echo "files=$(git diff --name-only origin/main...HEAD | \
            grep -E '\.(ts|tsx|js|jsx)$' | \
            xargs -I {} echo '--findRelatedTests {}' | \
            tr '\n' ' ')" >> $GITHUB_OUTPUT

      - name: Run tests for changed files only
        if: steps.changed-files.outputs.files != ''
        run: npm test -- ${{ steps.changed-files.outputs.files }}

  build-with-cache:
    name: Build with Aggressive Caching
    runs-on: ubuntu-latest
    needs: quick-checks

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: "npm"

      - name: Cache build output
        uses: actions/cache@v4
        with:
          path: |
            .next/cache
            dist/
            build/
          key: ${{ runner.os }}-build-${{ hashFiles('**/*.ts', '**/*.tsx', '**/*.js') }}
          restore-keys: |
            ${{ runner.os }}-build-

      - name: Install dependencies
        run: npm ci --prefer-offline

      - name: Build
        run: npm run build

      - name: Upload build artifacts
        uses: actions/upload-artifact@v4
        with:
          name: build-output
          path: dist/
          retention-days: 7

  docker-build-optimized:
    name: Docker Build with Layer Caching
    runs-on: ubuntu-latest
    needs: quick-checks

    steps:
      - uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Build with cache
        uses: docker/build-push-action@v5
        with:
          context: .
          push: false
          tags: myapp:${{ github.sha }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
          build-args: |
            BUILDKIT_INLINE_CACHE=1
```

## Pipeline Optimization Patterns

### Caching Strategy

1. **Dependency Caching**: Cache `node_modules`, `vendor/`, `.m2/`, etc.
2. **Build Output Caching**: Cache compiled artifacts between runs
3. **Docker Layer Caching**: Use BuildKit cache mounts and GitHub Actions cache
4. **Incremental Builds**: Only rebuild changed modules (Nx, Turborepo)

### Parallelization Strategies

1. **Job-Level Parallelization**: Run independent jobs concurrently
2. **Test Sharding**: Split test suite across multiple runners
3. **Matrix Builds**: Test multiple versions/platforms simultaneously
4. **Monorepo Path Filtering**: Only test changed services

### Conditional Execution

1. **Path Filters**: Skip jobs when irrelevant files change
2. **Changed Files Detection**: Test only affected code
3. **Branch-Specific Jobs**: Different pipelines for different branches
4. **Manual Triggers**: Allow on-demand pipeline execution

## ML-Specific Patterns

### Model Training Pipeline

1. **Data Validation**: Validate schema and quality before training
2. **Experiment Tracking**: Log metrics to MLflow/W&B
3. **Model Versioning**: Tag models with git SHA or semantic version
4. **Performance Gates**: Enforce minimum accuracy/F1 thresholds

### Model Deployment

1. **A/B Testing**: Deploy new model alongside existing
2. **Shadow Mode**: Run new model without affecting production
3. **Canary Rollout**: Gradually increase traffic to new model
4. **Automated Rollback**: Revert on performance degradation

## Troubleshooting Guide

### Common Issues

1. **Flaky Tests**: Implement retry logic, increase timeouts, fix race conditions
2. **Slow Pipelines**: Profile execution times, add caching, parallelize
3. **Secrets Exposure**: Use secret scanning, audit logs, rotate credentials
4. **Resource Exhaustion**: Set resource limits, use cleanup actions
5. **Network Timeouts**: Add retries, use artifact caching, increase timeouts

### Debugging Commands

```bash
# GitHub Actions local testing
act -j test --secret-file .env.secrets

# GitLab CI local testing
gitlab-runner exec docker test

# Jenkins pipeline validation
java -jar jenkins-cli.jar declarative-linter < Jenkinsfile

# Docker build debugging
DOCKER_BUILDKIT=1 docker build --progress=plain .

# Test pipeline with dry-run
kubectl apply --dry-run=client -f k8s/

# Validate workflow syntax
actionlint .github/workflows/*.yml
```
