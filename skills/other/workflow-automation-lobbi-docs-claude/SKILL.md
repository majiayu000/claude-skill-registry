---
name: Workflow Automation
description: Expertise in CI/CD pipeline creation, process automation, and team workflow optimization. Activates when working with "automate", "pipeline", "workflow", "CI/CD", "process", or automation tools.
version: 1.0.0
---

# Workflow Automation Skill

## Overview

Design and implement automated workflows for development teams, including CI/CD pipelines, release automation, code quality gates, deployment processes, and team collaboration workflows. This skill encompasses GitHub Actions, Harness pipelines, automated testing workflows, release management, and process optimization strategies.

## Core Competencies

### GitHub Actions Workflows

**Design Comprehensive CI Workflows:**

Create multi-stage CI pipelines with proper job dependencies:

```yaml
# .github/workflows/ci.yml
name: Continuous Integration

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]
  workflow_dispatch:

env:
  NODE_VERSION: '20'
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  setup:
    name: Setup and Cache
    runs-on: ubuntu-latest
    outputs:
      cache-key: ${{ steps.cache-key.outputs.key }}
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'

      - name: Generate cache key
        id: cache-key
        run: echo "key=${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}" >> $GITHUB_OUTPUT

      - name: Install dependencies
        run: npm ci

  lint:
    name: Lint Code
    needs: setup
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run ESLint
        run: npm run lint -- --format json --output-file eslint-report.json
        continue-on-error: true

      - name: Annotate code
        uses: ataylorme/eslint-annotate-action@v2
        with:
          repo-token: ${{ secrets.GITHUB_TOKEN }}
          report-json: eslint-report.json

      - name: Upload ESLint results
        uses: actions/upload-artifact@v4
        with:
          name: eslint-report
          path: eslint-report.json

  type-check:
    name: Type Check
    needs: setup
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run TypeScript compiler
        run: npm run type-check

  unit-tests:
    name: Unit Tests
    needs: setup
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run unit tests
        run: npm run test:unit -- --coverage

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage/coverage-final.json
          flags: unit
          name: unit-tests

      - name: Upload test results
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: unit-test-results
          path: |
            coverage/
            test-results/

  integration-tests:
    name: Integration Tests
    needs: setup
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_DB: test_db
          POSTGRES_USER: test_user
          POSTGRES_PASSWORD: test_pass
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432

      redis:
        image: redis:7-alpine
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
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run database migrations
        run: npm run migrate
        env:
          DATABASE_URL: postgresql://test_user:test_pass@localhost:5432/test_db

      - name: Run integration tests
        run: npm run test:integration -- --coverage
        env:
          DATABASE_URL: postgresql://test_user:test_pass@localhost:5432/test_db
          REDIS_URL: redis://localhost:6379

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage/coverage-final.json
          flags: integration
          name: integration-tests

  e2e-tests:
    name: E2E Tests
    needs: [unit-tests, integration-tests]
    runs-on: ubuntu-latest
    timeout-minutes: 30
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Install Playwright browsers
        run: npx playwright install --with-deps

      - name: Run E2E tests
        run: npm run test:e2e

      - name: Upload Playwright report
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: playwright-report
          path: playwright-report/
          retention-days: 30

  security-scan:
    name: Security Scan
    needs: setup
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run npm audit
        run: npm audit --audit-level=moderate
        continue-on-error: true

      - name: Run Snyk security scan
        uses: snyk/actions/node@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
        with:
          args: --severity-threshold=high

      - name: Run Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          scan-ref: '.'
          format: 'sarif'
          output: 'trivy-results.sarif'

      - name: Upload Trivy results to GitHub Security
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: 'trivy-results.sarif'

  build:
    name: Build Application
    needs: [lint, type-check, unit-tests, integration-tests]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Build application
        run: npm run build

      - name: Upload build artifacts
        uses: actions/upload-artifact@v4
        with:
          name: dist
          path: dist/

  docker-build:
    name: Build Docker Image
    needs: [build, security-scan]
    runs-on: ubuntu-latest
    if: github.event_name == 'push'
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
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}
            type=sha,prefix={{branch}}-
            type=raw,value=latest,enable={{is_default_branch}}

      - name: Build and push Docker image
        uses: docker/build-push-action@v5
        with:
          context: .
          platforms: linux/amd64,linux/arm64
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
          build-args: |
            NODE_VERSION=${{ env.NODE_VERSION }}
            BUILD_DATE=${{ github.event.head_commit.timestamp }}
            VCS_REF=${{ github.sha }}

  quality-gate:
    name: Quality Gate
    needs: [lint, type-check, unit-tests, integration-tests, e2e-tests, security-scan]
    runs-on: ubuntu-latest
    steps:
      - name: Download all artifacts
        uses: actions/download-artifact@v4

      - name: Check quality metrics
        run: |
          echo "All quality checks passed"
          echo "Ready for deployment"

      - name: Post summary
        run: |
          echo "## CI Pipeline Summary" >> $GITHUB_STEP_SUMMARY
          echo "✅ Linting passed" >> $GITHUB_STEP_SUMMARY
          echo "✅ Type checking passed" >> $GITHUB_STEP_SUMMARY
          echo "✅ Unit tests passed" >> $GITHUB_STEP_SUMMARY
          echo "✅ Integration tests passed" >> $GITHUB_STEP_SUMMARY
          echo "✅ E2E tests passed" >> $GITHUB_STEP_SUMMARY
          echo "✅ Security scan passed" >> $GITHUB_STEP_SUMMARY
```

**Implement Automated Release Workflow:**

Create release automation with changelog generation:

```yaml
# .github/workflows/release.yml
name: Release

on:
  push:
    tags:
      - 'v*'

permissions:
  contents: write
  packages: write

jobs:
  create-release:
    name: Create Release
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Generate changelog
        id: changelog
        uses: mikepenz/release-changelog-builder-action@v4
        with:
          configuration: '.github/changelog-config.json'
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

      - name: Create GitHub Release
        uses: softprops/action-gh-release@v1
        with:
          body: ${{ steps.changelog.outputs.changelog }}
          draft: false
          prerelease: ${{ contains(github.ref, 'beta') || contains(github.ref, 'alpha') }}
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

  publish-npm:
    name: Publish to NPM
    needs: create-release
    runs-on: ubuntu-latest
    if: startsWith(github.ref, 'refs/tags/v')
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          registry-url: 'https://registry.npmjs.org'

      - name: Install dependencies
        run: npm ci

      - name: Build
        run: npm run build

      - name: Publish to NPM
        run: npm publish
        env:
          NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }}

  deploy-production:
    name: Deploy to Production
    needs: create-release
    runs-on: ubuntu-latest
    environment:
      name: production
      url: https://app.example.com
    steps:
      - uses: actions/checkout@v4

      - name: Setup kubectl
        uses: azure/setup-kubectl@v3

      - name: Setup Helm
        uses: azure/setup-helm@v3

      - name: Azure Login
        uses: azure/login@v1
        with:
          creds: ${{ secrets.AZURE_CREDENTIALS }}

      - name: Get AKS credentials
        run: |
          az aks get-credentials \
            --resource-group ${{ secrets.RESOURCE_GROUP }} \
            --name ${{ secrets.CLUSTER_NAME }}

      - name: Deploy with Helm
        run: |
          helm upgrade --install app \
            ./deployment/helm/app \
            --namespace production \
            --create-namespace \
            --values ./deployment/helm/app/values-prod.yaml \
            --set image.tag=${{ github.ref_name }} \
            --wait \
            --timeout 10m

      - name: Run smoke tests
        run: |
          kubectl run smoke-test \
            --image=curlimages/curl:latest \
            --restart=Never \
            --rm \
            -i \
            -- curl -f https://app.example.com/health
```

### Harness Pipeline Configuration

**Design Enterprise CI/CD Pipeline:**

Configure Harness pipelines for complex deployment scenarios:

```yaml
# harness/pipelines/production-deploy.yml
pipeline:
  name: Production Deployment Pipeline
  identifier: prod_deployment
  projectIdentifier: platform
  orgIdentifier: engineering
  tags:
    env: production
    team: platform
  stages:
    - stage:
        name: Build and Test
        identifier: build_test
        type: CI
        spec:
          cloneCodebase: true
          infrastructure:
            type: KubernetesDirect
            spec:
              connectorRef: k8s_delegate
              namespace: harness-builds
              automountServiceAccountToken: true
          execution:
            steps:
              - step:
                  type: Run
                  name: Install Dependencies
                  identifier: install_deps
                  spec:
                    connectorRef: docker_hub
                    image: node:20-alpine
                    shell: Bash
                    command: npm ci

              - step:
                  type: Run
                  name: Run Tests
                  identifier: run_tests
                  spec:
                    connectorRef: docker_hub
                    image: node:20-alpine
                    shell: Bash
                    command: |
                      npm run lint
                      npm run test:unit
                      npm run test:integration
                  failureStrategies:
                    - onFailure:
                        errors:
                          - AllErrors
                        action:
                          type: Abort

              - step:
                  type: Run
                  name: Security Scan
                  identifier: security_scan
                  spec:
                    connectorRef: docker_hub
                    image: aquasec/trivy:latest
                    shell: Bash
                    command: trivy fs --security-checks vuln,config .

              - step:
                  type: BuildAndPushDockerRegistry
                  name: Build and Push Image
                  identifier: build_push
                  spec:
                    connectorRef: docker_registry
                    repo: platform/app
                    tags:
                      - <+pipeline.sequenceId>
                      - <+pipeline.executionId>
                      - latest
                    optimize: true
                    caching: true

    - stage:
        name: Deploy to Staging
        identifier: deploy_staging
        type: Deployment
        spec:
          deploymentType: Kubernetes
          service:
            serviceRef: app_service
            serviceInputs:
              serviceDefinition:
                type: Kubernetes
                spec:
                  artifacts:
                    primary:
                      primaryArtifactRef: <+input>
                      sources:
                        - identifier: docker_image
                          type: DockerRegistry
                          spec:
                            tag: <+pipeline.sequenceId>
          environment:
            environmentRef: staging
            deployToAll: false
            infrastructureDefinitions:
              - identifier: staging_k8s
          execution:
            steps:
              - step:
                  type: K8sRollingDeploy
                  name: Rolling Deployment
                  identifier: rolling_deploy
                  spec:
                    skipDryRun: false
                    pruningEnabled: true

              - step:
                  type: ShellScript
                  name: Run Smoke Tests
                  identifier: smoke_tests
                  spec:
                    shell: Bash
                    source:
                      type: Inline
                      spec:
                        script: |
                          #!/bin/bash
                          set -e

                          echo "Running smoke tests..."
                          curl -f https://staging.example.com/health
                          echo "Smoke tests passed"
                  timeout: 5m

            rollbackSteps:
              - step:
                  type: K8sRollingRollback
                  name: Rollback Deployment
                  identifier: rollback

    - stage:
        name: Approval
        identifier: approval
        type: Approval
        spec:
          execution:
            steps:
              - step:
                  type: HarnessApproval
                  name: Manual Approval
                  identifier: manual_approval
                  spec:
                    approvalMessage: Please review and approve deployment to production
                    includePipelineExecutionHistory: true
                    approvers:
                      userGroups:
                        - account.ProductionApprovers
                    minimumCount: 2
                    disallowPipelineExecutor: false
                  timeout: 1d

    - stage:
        name: Deploy to Production
        identifier: deploy_production
        type: Deployment
        spec:
          deploymentType: Kubernetes
          service:
            serviceRef: app_service
            serviceInputs:
              serviceDefinition:
                type: Kubernetes
                spec:
                  artifacts:
                    primary:
                      primaryArtifactRef: <+input>
                      sources:
                        - identifier: docker_image
                          type: DockerRegistry
                          spec:
                            tag: <+pipeline.sequenceId>
          environment:
            environmentRef: production
            deployToAll: false
            infrastructureDefinitions:
              - identifier: prod_k8s_us_east
              - identifier: prod_k8s_eu_west
          execution:
            steps:
              - step:
                  type: K8sBlueGreenDeploy
                  name: Blue Green Deployment
                  identifier: bg_deploy
                  spec:
                    skipDryRun: false
                    pruningEnabled: false

              - step:
                  type: ShellScript
                  name: Health Check
                  identifier: health_check
                  spec:
                    shell: Bash
                    source:
                      type: Inline
                      spec:
                        script: |
                          #!/bin/bash
                          set -e

                          for i in {1..10}; do
                            if curl -f https://app.example.com/health; then
                              echo "Health check passed"
                              exit 0
                            fi
                            echo "Attempt $i failed, retrying..."
                            sleep 10
                          done

                          echo "Health check failed"
                          exit 1
                  timeout: 5m

              - step:
                  type: K8sBGSwapServices
                  name: Swap Traffic
                  identifier: swap_traffic
                  spec:
                    skipDryRun: false

              - step:
                  type: ShellScript
                  name: Monitor Metrics
                  identifier: monitor_metrics
                  spec:
                    shell: Bash
                    source:
                      type: Inline
                      spec:
                        script: |
                          #!/bin/bash
                          # Monitor error rates and latency for 5 minutes
                          for i in {1..30}; do
                            ERROR_RATE=$(curl -s "https://monitoring.example.com/api/v1/query?query=rate(http_requests_total{status=~\"5..\"}[5m])" | jq '.data.result[0].value[1]' -r)

                            if (( $(echo "$ERROR_RATE > 0.01" | bc -l) )); then
                              echo "Error rate too high: $ERROR_RATE"
                              exit 1
                            fi

                            sleep 10
                          done
                  timeout: 10m

            rollbackSteps:
              - step:
                  type: K8sBGSwapServices
                  name: Rollback Traffic
                  identifier: rollback_traffic

  notificationRules:
    - name: Pipeline Failed
      pipelineEvents:
        - type: PipelineFailed
      notificationMethod:
        type: Slack
        spec:
          userGroups:
            - account.DevOps
          webhookUrl: <+secrets.getValue("slack_webhook")>

    - name: Production Deployed
      pipelineEvents:
        - type: StageSuccess
      notificationMethod:
        type: Email
        spec:
          userGroups:
            - account.Engineering
          recipients:
            - engineering@example.com
```

### Automation Scripts

**Create Reusable Workflow Templates:**

Build modular automation scripts for common tasks:

```bash
#!/bin/bash
# scripts/automation/deploy.sh

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_prerequisites() {
    log_info "Checking prerequisites..."

    command -v kubectl >/dev/null 2>&1 || {
        log_error "kubectl is required but not installed."
        exit 1
    }

    command -v helm >/dev/null 2>&1 || {
        log_error "helm is required but not installed."
        exit 1
    }

    command -v docker >/dev/null 2>&1 || {
        log_error "docker is required but not installed."
        exit 1
    }
}

build_image() {
    local tag=$1
    log_info "Building Docker image with tag: $tag"

    docker build \
        -f deployment/docker/Dockerfile \
        -t "$DOCKER_REGISTRY/$IMAGE_NAME:$tag" \
        --build-arg NODE_VERSION=20 \
        --build-arg BUILD_DATE="$(date -u +'%Y-%m-%dT%H:%M:%SZ')" \
        --build-arg VCS_REF="$(git rev-parse --short HEAD)" \
        .
}

push_image() {
    local tag=$1
    log_info "Pushing Docker image with tag: $tag"

    docker push "$DOCKER_REGISTRY/$IMAGE_NAME:$tag"
}

deploy_helm() {
    local environment=$1
    local tag=$2

    log_info "Deploying to $environment with tag: $tag"

    helm upgrade --install "$RELEASE_NAME" \
        ./deployment/helm/app \
        --namespace "$NAMESPACE" \
        --create-namespace \
        --values "./deployment/helm/app/values-$environment.yaml" \
        --set "image.tag=$tag" \
        --wait \
        --timeout 10m
}

run_smoke_tests() {
    local url=$1
    log_info "Running smoke tests against $url"

    for i in {1..10}; do
        if curl -f -s "$url/health" > /dev/null; then
            log_info "Smoke tests passed"
            return 0
        fi
        log_warn "Attempt $i failed, retrying..."
        sleep 5
    done

    log_error "Smoke tests failed"
    return 1
}

# Main deployment function
deploy() {
    local environment=$1
    local version=${2:-$(git rev-parse --short HEAD)}

    check_prerequisites

    log_info "Starting deployment to $environment"
    log_info "Version: $version"

    # Build and push image
    build_image "$version"
    push_image "$version"

    # Deploy with Helm
    deploy_helm "$environment" "$version"

    # Run smoke tests
    case $environment in
        production)
            run_smoke_tests "https://app.example.com"
            ;;
        staging)
            run_smoke_tests "https://staging.example.com"
            ;;
        *)
            log_warn "Skipping smoke tests for $environment"
            ;;
    esac

    log_info "Deployment completed successfully"
}

# Parse command line arguments
case ${1:-} in
    production|staging|development)
        deploy "$@"
        ;;
    *)
        echo "Usage: $0 {production|staging|development} [version]"
        exit 1
        ;;
esac
```

**Create Database Migration Workflow:**

Automate database schema changes:

```bash
#!/bin/bash
# scripts/automation/migrate.sh

set -euo pipefail

# Database migration automation
run_migrations() {
    local environment=$1
    local direction=${2:-up}

    log_info "Running $direction migrations for $environment"

    # Load environment-specific configuration
    case $environment in
        production)
            DB_URL="$PRODUCTION_DB_URL"
            ;;
        staging)
            DB_URL="$STAGING_DB_URL"
            ;;
        development)
            DB_URL="$DEVELOPMENT_DB_URL"
            ;;
    esac

    # Create backup before migration
    if [ "$environment" = "production" ]; then
        log_info "Creating database backup..."
        backup_database "$environment"
    fi

    # Run migrations
    if [ "$direction" = "up" ]; then
        npm run migrate:up
    else
        npm run migrate:down
    fi

    log_info "Migrations completed"
}

backup_database() {
    local environment=$1
    local timestamp=$(date +%Y%m%d_%H%M%S)
    local backup_file="backup_${environment}_${timestamp}.sql"

    pg_dump "$DB_URL" > "$backup_file"

    # Upload to cloud storage
    aws s3 cp "$backup_file" "s3://backups/$backup_file"

    log_info "Backup created: $backup_file"
}

run_migrations "$@"
```

## Process Optimization

**Implement Branch Protection Rules:**

Configure automated branch protection:

```yaml
# .github/branch-protection.yml
rules:
  - pattern: main
    required_status_checks:
      strict: true
      contexts:
        - ci/lint
        - ci/type-check
        - ci/unit-tests
        - ci/integration-tests
        - ci/e2e-tests
        - ci/security-scan
    required_pull_request_reviews:
      required_approving_review_count: 2
      dismiss_stale_reviews: true
      require_code_owner_reviews: true
    restrictions:
      users: []
      teams:
        - core-team
        - platform-team
    enforce_admins: true
    required_signatures: true
    allow_force_pushes: false
    allow_deletions: false

  - pattern: develop
    required_status_checks:
      strict: true
      contexts:
        - ci/lint
        - ci/type-check
        - ci/unit-tests
    required_pull_request_reviews:
      required_approving_review_count: 1
      dismiss_stale_reviews: true
    enforce_admins: false
    allow_force_pushes: false
```

**Create Automated Dependency Updates:**

Implement automated dependency management:

```yaml
# .github/workflows/dependency-update.yml
name: Dependency Updates

on:
  schedule:
    - cron: '0 0 * * 1' # Weekly on Monday
  workflow_dispatch:

jobs:
  update-dependencies:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Update dependencies
        run: |
          npm update
          npm outdated || true

      - name: Run tests
        run: |
          npm ci
          npm run test

      - name: Create Pull Request
        uses: peter-evans/create-pull-request@v5
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
          commit-message: 'chore: update dependencies'
          title: 'chore: automated dependency updates'
          body: |
            This PR contains automated dependency updates.

            Please review the changes and ensure all tests pass.
          branch: chore/dependency-updates
          labels: dependencies, automated
```

## Related Resources

- **DevOps Practices Skill** - For deployment and infrastructure automation
- **Code Quality Skill** - For quality gate implementation in pipelines
- **Integration Patterns Skill** - For API and service integration in workflows
- **GitHub Actions Documentation** - https://docs.github.com/actions
- **Harness Documentation** - https://developer.harness.io
