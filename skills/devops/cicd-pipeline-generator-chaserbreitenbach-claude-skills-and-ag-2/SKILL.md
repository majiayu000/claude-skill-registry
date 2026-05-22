---
name: cicd-pipeline-generator
version: 1.0.0
description: |
  Configurable GitHub Actions workflow generator that produces complete CI/CD pipelines
  for any technology stack, including linting, testing, security scanning, and deployment.
author: QuantQuiver AI R&D
license: MIT

category: tooling
tags:
  - ci-cd
  - github-actions
  - devops
  - automation
  - testing
  - deployment
  - security-scanning

dependencies:
  skills: []
  python: ">=3.9"
  packages:
    - pyyaml
  tools:
    - bash
    - code_execution

triggers:
  - "generate CI/CD pipeline"
  - "create GitHub Actions"
  - "set up automated testing"
  - "CI/CD workflow"
  - "deployment pipeline"
  - "continuous integration"
  - "GitHub workflow"
---

# CI/CD Pipeline Generator

## Purpose

A configurable GitHub Actions workflow generator that produces complete CI/CD pipelines for any technology stack, including linting, testing, security scanning, and deployment stages.

**Problem Space:**
- Manual CI/CD setup is error-prone
- Security scanning often forgotten
- Inconsistent quality gates across projects
- Deployment strategies vary without standardization

**Solution Approach:**
- Stack detection and appropriate tool selection
- Configurable quality gates
- Built-in security scanning (SAST, dependency audit)
- Multi-environment deployment with approval gates

## When to Use

- New project setup
- Adding CI/CD to legacy projects
- Standardizing pipelines across organization
- Security compliance requirements
- When asked to "set up automated testing"
- When deploying to staging/production

## When NOT to Use

- Single-file scripts that don't need CI
- Projects with highly custom build processes (customize manually)
- When existing pipeline just needs minor tweaks

---

## Core Instructions

### Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    CI/CD PIPELINE STRUCTURE                     │
├─────────────────────────────────────────────────────────────────┤
│  STAGE 1: CODE QUALITY                                          │
│  ├── Linting (language-specific)                                │
│  ├── Formatting check                                           │
│  └── Type checking                                              │
├─────────────────────────────────────────────────────────────────┤
│  STAGE 2: SECURITY SCANNING                                     │
│  ├── Dependency audit                                           │
│  ├── SAST (static analysis)                                     │
│  ├── Secret scanning                                            │
│  └── Container scanning                                         │
├─────────────────────────────────────────────────────────────────┤
│  STAGE 3: TESTING                                               │
│  ├── Unit tests                                                 │
│  ├── Integration tests                                          │
│  └── Coverage reporting                                         │
├─────────────────────────────────────────────────────────────────┤
│  STAGE 4: BUILD                                                 │
│  ├── Application build                                          │
│  ├── Docker image build                                         │
│  └── Artifact upload                                            │
├─────────────────────────────────────────────────────────────────┤
│  STAGE 5: DEPLOY                                                │
│  ├── Staging (automatic)                                        │
│  ├── Production (manual approval)                               │
│  └── Notifications                                              │
└─────────────────────────────────────────────────────────────────┘
```

### Stack Detection Rules

```yaml
stack_detection:
  python:
    indicators:
      - "requirements.txt"
      - "pyproject.toml"
      - "setup.py"
      - "Pipfile"
    tools:
      lint: ["ruff", "flake8"]
      format: ["black", "autopep8"]
      type_check: ["mypy", "pyright"]
      test: ["pytest", "unittest"]
      security: ["bandit", "pip-audit", "safety"]

  nodejs:
    indicators:
      - "package.json"
    tools:
      lint: ["eslint"]
      format: ["prettier"]
      type_check: ["tsc"]  # if typescript
      test: ["jest", "mocha", "vitest"]
      security: ["npm audit", "snyk"]

  go:
    indicators:
      - "go.mod"
    tools:
      lint: ["golangci-lint"]
      format: ["gofmt"]
      type_check: null  # built-in
      test: ["go test"]
      security: ["gosec", "govulncheck"]

  rust:
    indicators:
      - "Cargo.toml"
    tools:
      lint: ["clippy"]
      format: ["rustfmt"]
      type_check: null  # built-in
      test: ["cargo test"]
      security: ["cargo-audit"]
```

### Standard Procedures

#### 1. Detect Technology Stack

Scan repository root for indicator files and determine primary language(s).

#### 2. Configure Pipeline Options

```python
class CICDConfig:
    # Stack configuration
    stacks: List[str] = ["python"]
    python_version: str = "3.11"
    node_version: str = "20"

    # Quality gates
    lint_enabled: bool = True
    format_check: bool = True
    type_check: bool = True

    # Testing
    test_enabled: bool = True
    coverage_threshold: int = 60

    # Security
    security_scan: bool = True
    dependency_audit: bool = True
    secret_scanning: bool = True
    container_scanning: bool = True

    # Build
    docker_build: bool = True
    docker_registry: str = "ghcr.io"

    # Deploy
    deploy_enabled: bool = True
    staging_auto_deploy: bool = True
    production_approval: bool = True
```

#### 3. Generate Workflow File

Output to `.github/workflows/ci.yml`

### Decision Framework

**Quality Gate Selection:**
- Always include: linting, unit tests
- Production apps: add security scanning, type checking
- Open source: add coverage badges, multiple Python/Node versions
- Enterprise: add approval gates, audit logging

**When to Use Matrix Builds:**
- Testing library compatibility across versions
- Cross-platform applications
- Multiple Python/Node version support

**Deployment Strategy:**
- Staging first, then production
- Production requires manual approval
- Use environment protection rules

---

## Templates

### Complete Python Pipeline

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop, 'feature/**']
  pull_request:
    branches: [main, develop]
  workflow_dispatch:
    inputs:
      deploy_environment:
        description: 'Environment to deploy to'
        required: false
        default: 'staging'
        type: choice
        options: [staging, production]

env:
  PYTHON_VERSION: '3.11'
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  lint:
    name: Lint & Format
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}
          cache: 'pip'

      - name: Install linting tools
        run: pip install ruff black mypy

      - name: Run Ruff
        run: ruff check . --output-format=github

      - name: Run Black
        run: black --check --diff .

      - name: Run mypy
        run: mypy . --ignore-missing-imports
        continue-on-error: true

  security:
    name: Security Scan
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}

      - name: Install security tools
        run: pip install pip-audit bandit

      - name: Dependency audit
        run: pip-audit -r requirements.txt --strict
        continue-on-error: true

      - name: Run Bandit
        run: bandit -r . -f json -o bandit-report.json || true

      - name: Upload security report
        uses: actions/upload-artifact@v4
        with:
          name: security-report
          path: bandit-report.json

      - name: Run Gitleaks
        uses: gitleaks/gitleaks-action@v2
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

  test:
    name: Tests
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}
          cache: 'pip'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov

      - name: Run tests
        run: pytest --cov=. --cov-report=xml --cov-fail-under=60

      - name: Upload coverage
        uses: codecov/codecov-action@v4
        with:
          files: coverage.xml

  build:
    name: Build Docker Image
    runs-on: ubuntu-latest
    needs: [lint, security, test]
    permissions:
      contents: read
      packages: write
    steps:
      - uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Log in to Registry
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
            type=sha,prefix=
            type=ref,event=branch
            type=semver,pattern={{version}}

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
    name: Deploy to Staging
    runs-on: ubuntu-latest
    needs: [build]
    if: github.ref == 'refs/heads/main' || github.ref == 'refs/heads/develop'
    environment:
      name: staging
      url: https://staging.example.com
    steps:
      - uses: actions/checkout@v4

      - name: Deploy to staging
        run: echo "Deploy commands here"

      - name: Health check
        run: |
          sleep 10
          curl -f https://staging.example.com/health || exit 1

  deploy-production:
    name: Deploy to Production
    runs-on: ubuntu-latest
    needs: [build, deploy-staging]
    if: github.ref == 'refs/heads/main'
    environment:
      name: production
      url: https://example.com
    steps:
      - uses: actions/checkout@v4

      - name: Deploy to production
        run: echo "Production deploy commands here"

      - name: Notify success
        if: success()
        run: echo "Deployment successful!"

      - name: Notify failure
        if: failure()
        run: echo "Deployment failed!"
```

### Node.js/TypeScript Pipeline

```yaml
name: Node.js CI/CD

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

env:
  NODE_VERSION: '20'

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'
      - run: npm ci
      - run: npm run lint
      - run: npx tsc --noEmit

  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'
      - run: npm ci
      - run: npm audit --audit-level=high

  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'
      - run: npm ci
      - run: npm test -- --coverage --coverageThreshold='{"global":{"lines":60}}'
```

---

## Examples

### Example 1: Python Web Application

**Input**: "Generate CI/CD for my Flask API with Docker deployment"

**Configuration Detected**:
- Stack: Python (Flask)
- Build: Docker
- Deploy: Staging + Production

**Output**: Complete workflow with lint, security, test, build, and deploy jobs.

### Example 2: Multi-Stack Monorepo

**Input**: "Set up CI for a repo with Python backend and React frontend"

**Output**: Separate job groups for Python and Node.js, parallel execution, unified deployment.

---

## Validation Checklist

Before generating pipeline:

- [ ] Technology stack correctly detected
- [ ] All indicator files checked
- [ ] Security scanning included for production apps
- [ ] Coverage threshold appropriate for project maturity
- [ ] Docker registry permissions documented
- [ ] Environment protection rules noted
- [ ] Secrets requirements listed

---

## Related Resources

- Skill: `repository-auditor` - Pre-audit code before CI setup
- Skill: `docker-stack-composer` - Multi-service Docker configs
- GitHub Actions Documentation: https://docs.github.com/en/actions
- Security scanning: Gitleaks, Trivy, Bandit

---

## Changelog

### 1.0.0 (January 2026)
- Initial release
- Python, Node.js, Go, Rust support
- Security scanning integration
- Multi-environment deployment
- Coverage reporting
