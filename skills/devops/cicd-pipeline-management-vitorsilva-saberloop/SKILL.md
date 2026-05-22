---
name: cicd-pipeline-management
description: Manage GitHub Actions workflows and deployment pipelines with multiple environments
version: 1.0.0
author: Saberloop Project
usage: |
  Use this skill for CI/CD pipeline tasks:
  - Creating new workflow files for automated processes
  - Updating deployment configurations for different environments
  - Managing environment-specific settings and secrets
  - Debugging workflow failures and optimization
  - Setting up artifact management and staging deployments
  
  Examples:
  "Create new workflow using the cicd-pipeline-management skill"
  "Update deployment configuration using the cicd-pipeline-management skill"
  "Set up staging pipeline using the cicd-pipeline-management skill"

# CI/CD Pipeline Management Skill

## Overview

This skill automates the management of GitHub Actions workflows and deployment pipelines for Saberloop, supporting multiple environments, artifact management, and automated testing/deployment processes.

## Pipeline Architecture

### Environments

| Environment | Purpose | Branch | Domain | Config File |
|------------|---------|--------|--------------|
| Development | Feature testing | `feature/*` | dev.saberloop.com |
| Staging | Pre-production validation | `main` | staging.saberloop.com |
| Production | Live deployment | `main` | saberloop.com |

### Workflow Types

| Workflow | Trigger | Purpose | Key Actions |
|----------|---------|---------|-------------|
| Test | Push/PR to any branch | Code validation | Tests, lint, build |
| Deploy Staging | Push to main | Staging deployment | Build, FTP upload |
| Deploy Production | Manual/Tagged release | Production deployment | Build, FTP upload |
| E2E Tests | Schedule/Manual | User flow validation | Playwright tests |
| Security | Schedule | Dependency scanning | Security audit |

## When to Use This Skill

Use this skill when ANY of these are true:
- [ ] Creating new automated processes
- [ ] Setting up deployment for new environments
- [ ] Debugging CI/CD failures
- [ ] Optimizing workflow performance
- [ ] Adding new testing or quality gates
- [ ] Managing secrets or environment variables

## Workflow Templates

### Step 1: Basic Test Workflow

**File:** `.github/workflows/test.yml`

```yaml
name: Test

on:
  push:
    branches: ['**']
  pull_request:
    branches: ['**']

jobs:
  test:
    runs-on: ubuntu-latest
    
    strategy:
      matrix:
        node-version: [20]
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4

    - name: Setup Node.js
      uses: actions/setup-node@v4
      with:
        node-version: ${{ matrix.node-version }}
        cache: 'npm'

    - name: Install dependencies
      run: npm install --no-save

    - name: Check for dead code (warning)
      run: npm run lint:dead-code || true

    - name: Check architecture rules (warning)
      run: npm run arch:test || true

    - name: Type check (warning)
      run: npm run typecheck || true

    - name: Run unit tests
      run: npm test -- --run

    - name: Install Playwright browsers
      run: npx playwright install --with-deps

    - name: Run E2E tests
      run: npm run test:e2e

    - name: Build production bundle
      run: npm run build

    - name: Upload test artifacts on failure
      if: failure()
      uses: actions/upload-artifact@v4
      with:
        name: test-results-${{ matrix.node-version }}
        path: |
          test-results/
          playwright-report/
        retention-days: 7

    - name: Upload coverage reports
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage/lcov.info
        flags: unittests
        name: codecov-umbrella

  mutation-testing:
    runs-on: ubuntu-latest
    needs: test
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4

    - name: Setup Node.js
      uses: actions/setup-node@v4
      with:
        node-version: '20'
        cache: 'npm'

    - name: Install dependencies
      run: npm install --no-save

    - name: Run mutation testing
      run: npm run test:mutation

    - name: Upload mutation report
      uses: actions/upload-artifact@v4
      with:
        name: mutation-report
        path: reports/mutation/
        retention-days: 30
```

### Step 2: Deployment Workflow

**File:** `.github/workflows/deploy-staging.yml`

```yaml
name: Deploy to Staging

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
    types: [opened, synchronize, reopened]

jobs:
  deploy-staging:
    runs-on: ubuntu-latest
    
    environment:
      name: staging
      url: https://staging.saberloop.com

    steps:
    - name: Checkout code
      uses: actions/checkout@v4

    - name: Setup Node.js
      uses: actions/setup-node@v4
      with:
        node-version: '20'
        cache: 'npm'

    - name: Configure environment
      run: |
        echo "DEPLOY_TARGET=staging" >> $GITHUB_ENV
        echo "VITE_USE_REAL_API=true" >> $GITHUB_ENV
        echo "VITE_APP_URL=https://staging.saberloop.com" >> $GITHUB_ENV

    - name: Install dependencies
      run: npm install --no-save

    - name: Run tests first
      run: |
        npm test -- --run
        npm run typecheck
        npm run arch:test

    - name: Build for staging
      run: npm run build:staging

    - name: Deploy to staging via FTP
      uses: SamKirkland/FTP-Deploy-Action@4.3.0
      with:
        server: ${{ secrets.FTP_SERVER_STAGING }}
        username: ${{ secrets.FTP_USERNAME }}
        password: ${{ secrets.FTP_PASSWORD }}
        local-dir: ./dist/
        server-dir: /staging.saberloop.com/

    - name: Run smoke tests
      run: npm run test:e2e -- --grep "smoke"

    - name: Notify deployment
      uses: 8398a7/action-slack@v3
      if: success()
      with:
        status: success
        text: "🚀 Staging deployment successful: ${{ github.sha }}"
        channel: '#deployments'

    - name: Notify deployment failure
      uses: 8398a7/action-slack@v3
      if: failure()
      with:
        status: failure
        text: "❌ Staging deployment failed: ${{ github.sha }}"
        channel: '#deployments'

    - name: Update deployment status
      if: success()
      run: |
        curl -X POST \
          -H "Authorization: Bearer ${{ secrets.DEPLOYMENT_API_TOKEN }}" \
          -H "Content-Type: application/json" \
          -d '{
            "environment": "staging",
            "commit": "${{ github.sha }}",
            "status": "success",
            "timestamp": "'$(date -u +%Y-%m-%dT%H:%M:%SZ)'"
          }' \
          https://api.saberloop.com/deployments
```

### Step 3: Production Deployment

**File:** `.github/workflows/deploy-production.yml`

```yaml
name: Deploy to Production

on:
  release:
    types: [published]
  workflow_dispatch:
    inputs:
      version:
        description: 'Version to deploy (optional)'
        required: false

jobs:
  deploy-production:
    runs-on: ubuntu-latest
    
    environment:
      name: production
      url: https://saberloop.com

    steps:
    - name: Checkout code
      uses: actions/checkout@v4
      with:
        ref: ${{ github.event.release.target_commitish || github.sha }}

    - name: Setup Node.js
      uses: actions/setup-node@v4
      with:
        node-version: '20'
        cache: 'npm'

    - name: Configure production environment
      run: |
        echo "DEPLOY_TARGET=production" >> $GITHUB_ENV
        echo "VITE_USE_REAL_API=true" >> $GITHUB_ENV
        echo "VITE_APP_URL=https://saberloop.com" >> $GITHUB_ENV

    - name: Install dependencies
      run: npm install --no-save

    - name: Run comprehensive tests
      run: |
        npm test -- --run
        npm run typecheck
        npm run arch:test
        npm run test:e2e

    - name: Run mutation testing
      run: npm run test:mutation

    - name: Build for production
      run: npm run build

    - name: Create deployment artifact
      run: |
        tar -czf production-build-${{ github.sha }}.tar.gz dist/
        echo "ARTIFACT_NAME=production-build-${{ github.sha }}.tar.gz" >> $GITHUB_ENV

    - name: Upload deployment artifact
      uses: actions/upload-artifact@v4
      with:
        name: production-build
        path: production-build-${{ github.sha }}.tar.gz
        retention-days: 30

    - name: Deploy to production via FTP
      uses: SamKirkland/FTP-Deploy-Action@4.3.0
      with:
        server: ${{ secrets.FTP_SERVER_PROD }}
        username: ${{ secrets.FTP_USERNAME }}
        password: ${{ secrets.FTP_PASSWORD_PROD }}
        local-dir: ./dist/
        server-dir: /saberloop.com/

    - name: Run production smoke tests
      run: npm run test:e2e -- --grep "production-smoke"

    - name: Warm up CDN cache
      run: |
        curl -I https://saberloop.com/
        curl -I https://saberloop.com/manifest.webmanifest
        curl -I https://saberloop.com/sw.js

    - name: Notify production deployment
      uses: 8398a7/action-slack@v3
      if: success()
      with:
        status: success
        text: "🎉 Production deployment successful: ${{ github.event.release.tag_name || github.sha }}"
        channel: '#deployments'

    - name: Create rollback point
      if: success()
      run: |
        git tag rollback-${{ github.sha }} HEAD
        git push origin rollback-${{ github.sha }}
        echo "Rollback tag created: rollback-${{ github.sha }}"
```

## Environment Configuration

### Step 1: Environment Variables

**File:** `.env.example`

```bash
# Base configuration
VITE_APP_TITLE=Saberloop
VITE_APP_VERSION=2.0.0

# API Configuration
VITE_USE_REAL_API=false
VITE_API_BASE_URL=http://localhost:3000/api

# Environment-specific
DEPLOY_TARGET=development
VITE_APP_URL=http://localhost:8888

# Feature Flags (for testing)
VITE_TEST_FEATURE_SHOW_ADS=false
VITE_TEST_FEATURE_PARTY_SESSION=true

# Telemetry
VITE_TELEMETRY_ENABLED=true
VITE_TELEMETRY_ENDPOINT=http://localhost:3100
```

**File:** `.env.staging`

```bash
# Staging configuration
DEPLOY_TARGET=staging
VITE_USE_REAL_API=true
VITE_API_BASE_URL=https://api.staging.saberloop.com
VITE_APP_URL=https://staging.saberloop.com

# Staging feature flags
VITE_TEST_FEATURE_SHOW_ADS=true
VITE_TEST_FEATURE_PARTY_SESSION=true
```

**File:** `.env.production`

```bash
# Production configuration
DEPLOY_TARGET=production
VITE_USE_REAL_API=true
VITE_API_BASE_URL=https://api.saberloop.com
VITE_APP_URL=https://saberloop.com

# Production feature flags
VITE_TEST_FEATURE_SHOW_ADS=true
VITE_TEST_FEATURE_PARTY_SESSION=false  # Might be disabled initially

# Production-only settings
VITE_TELEMETRY_ENABLED=true
VITE_TELEMETRY_ENDPOINT=https://telemetry.saberloop.com
```

### Step 2: Secrets Management

#### Required Secrets

| Secret | Purpose | Environment |
|--------|---------|-------------|
| `FTP_SERVER_PROD` | Production FTP server | Production |
| `FTP_SERVER_STAGING` | Staging FTP server | Staging |
| `FTP_USERNAME` | FTP username | All |
| `FTP_PASSWORD_PROD` | Production FTP password | Production |
| `DEPLOYMENT_API_TOKEN` | Deployment status API | All |
| `SLACK_WEBHOOK_URL` | Slack notifications | All |

#### GitHub Secrets Setup

```bash
# Using GitHub CLI
gh secret set FTP_SERVER_PROD --body "ftp.saberloop.com"
gh secret set FTP_USERNAME --body "deploy-user"
gh secret set FTP_PASSWORD_PROD --body "secure-password"

# List existing secrets
gh secret list

# Update secret
gh secret set FTP_USERNAME --body "new-user"
```

## Advanced Workflow Features

### Step 1: Matrix Builds

```yaml
strategy:
  matrix:
    include:
      - os: ubuntu-latest
        node-version: '20'
        environment: staging
      - os: windows-latest
        node-version: '18'
        environment: production
    fail-fast: false

jobs:
  test:
    runs-on: ${{ matrix.os }}
    steps:
      - name: Setup Node.js ${{ matrix.node-version }}
        uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
```

### Step 2: Conditional Workflows

```yaml
on:
  push:
    branches: [main]
    paths:
      - 'src/**'
      - 'package.json'
      - 'vite.config.js'
      - '!docs/**'  # Skip for docs-only changes

  pull_request:
    branches: [main]
    types: [opened, synchronize, reopened]

  schedule:
    - cron: '0 2 * * *'  # Daily at 2 AM UTC
    - cron: '0 6 * * 1'  # Weekly on Monday 6 AM UTC
```

### Step 3: Caching Strategies

```yaml
- name: Cache node modules
  uses: actions/cache@v3
  with:
    path: |
      ~/.npm
      node_modules
    key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
    restore-keys: |
      ${{ runner.os }}-node-

- name: Cache build artifacts
  uses: actions/cache@v3
  with:
    path: |
      dist/
      .vite/
    key: ${{ runner.os }}-build-${{ github.sha }}
    restore-keys: |
      ${{ runner.os }}-build-
```

## Quality Gates and Monitoring

### Step 1: Pre-deployment Checks

```yaml
- name: Quality Gate Checks
  run: |
    echo "🔍 Running quality gate checks..."
    
    # Check test coverage
    COVERAGE=$(npm run test:coverage 2>/dev/null | grep -o '[0-9]\+%' | tail -1)
    if [[ $(echo "$COVERAGE" | sed 's/%//') -lt 90 ]]; then
      echo "❌ Coverage below 90%: $COVERAGE"
      exit 1
    fi
    
    # Check bundle size
    BUNDLE_SIZE=$(du -sh dist/ | cut -f1)
    MAX_SIZE=5242880  # 5MB
    if [[ $BUNDLE_SIZE -gt $MAX_SIZE ]]; then
      echo "❌ Bundle size too large: $BUNDLE_SIZE bytes"
      exit 1
    fi
    
    # Check for security vulnerabilities
    npm audit --audit-level=moderate
    if [ $? -ne 0 ]; then
      echo "❌ Security vulnerabilities found"
      exit 1
    fi
    
    echo "✅ All quality gates passed"
```

### Step 2: Performance Monitoring

```yaml
- name: Performance Audit
  run: |
    # Lighthouse CI
    npm install -g @lhci/cli@0.12.x
    
    lhci autorun
    lhci upload \
      --target=temporary-public-storage \
      --token=${{ secrets.LHCI_TOKEN }} \
      --github-token=${{ secrets.GITHUB_TOKEN }}

- name: Update Performance Metrics
  run: |
    # Extract performance metrics
    PERFORMANCE=$(curl -s "https://api.saberloop.com/performance/${{ github.sha }}")
    
    echo "::set-output name=performance_score::${PERFORMANCE.score}"
    echo "::set-output name=lighthouse_score::${PERFORMANCE.lighthouse}"
```

### Step 3: Rollback Capabilities

```yaml
- name: Create Rollback Point
  if: success()
  run: |
    # Tag current commit for rollback
    git tag rollback-${{ github.sha }} HEAD
    git push origin rollback-${{ github.sha }}
    
    # Create rollback artifact
    echo "Rollback point: rollback-${{ github.sha }}" >> rollback.txt
    echo "Commit: ${{ github.sha }}" >> rollback.txt
    echo "Timestamp: $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> rollback.txt

- name: Upload Rollback Info
  if: success()
  uses: actions/upload-artifact@v4
  with:
    name: rollback-${{ github.sha }}
    path: rollback.txt
    retention-days: 90
```

## Troubleshooting

### Common Issues

#### Workflow Failures

```bash
# Debug workflow locally
act -j test  # Run test workflow locally

# Check specific job
act -j deploy-staging

# View workflow logs
gh run view --log  # View latest workflow logs
gh run list --workflow=test  # List test workflow runs
```

#### FTP Deployment Issues

```bash
# Test FTP connection manually
lftp -u $FTP_USERNAME -p $FTP_PASSWORD -e "open ftp.server.com; ls; exit"

# Check file permissions
lftp -u $FTP_USERNAME -p $FTP_PASSWORD -e "open ftp.server.com; chmod 755 /path/to/file; exit"

# Debug FTP deployment
curl -v -T dist/index.html ftp://ftp.server.com/path/test-upload.html
```

#### Cache Issues

```bash
# Clear npm cache
npm cache clean --force

# Clear GitHub Actions cache
gh api repos/:owner/:repo/actions/caches

# Check cache keys
gh api repos/:owner/:repo/actions/cache/keys
```

## Integration with Other Skills

This skill integrates with:
- **epic-hygiene-process** - For code quality gates in CI/CD
- **testing-suite-management** - For automated testing in workflows
- **feature-flag-management** - For environment-specific feature rollouts
- **pwa-feature-development** - For PWA-specific deployment requirements

---

**Version:** 1.0.0  
**Last Updated:** 2026-01-15  
**Compatible with:** Saberloop v2.0.0+