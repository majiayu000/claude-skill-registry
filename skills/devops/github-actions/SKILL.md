---
name: github-actions
version: 1.0.0
description: CI/CD automation and workflow orchestration using GitHub Actions for builds, tests, deployments, and repository automation
author: workspace-hub
category: automation
type: skill
capabilities:
  - ci_cd_pipelines
  - matrix_builds
  - reusable_workflows
  - composite_actions
  - artifact_management
  - secret_management
  - environment_deployments
  - scheduled_automation
tools:
  - github-cli
  - act
  - yaml-lint
tags: [github, actions, ci-cd, automation, workflows, devops, pipelines, testing, deployment]
platforms: [github, linux, macos, windows]
related_skills:
  - yaml-configuration
  - bash-cli-framework
  - git-sync-manager
---

# GitHub Actions Skill

Master GitHub Actions for CI/CD pipelines, automated testing, deployments, and repository automation. This skill covers workflow syntax, triggers, jobs, matrix builds, caching, artifacts, reusable workflows, and secrets management.

## When to Use This Skill

### USE when:
- Building CI/CD pipelines for GitHub repositories
- Automating tests across multiple OS/language versions
- Creating release and deployment workflows
- Publishing packages to npm, PyPI, Docker Hub
- Automating issue triage and PR management
- Scheduling periodic maintenance tasks
- Building reusable workflow components
- Implementing GitOps deployment patterns

### DON'T USE when:
- Repository not hosted on GitHub (use Jenkins, GitLab CI)
- Need complex DAG-based workflow orchestration (use Airflow)
- Require visual workflow design (use n8n, Activepieces)
- Self-hosted runners not available for compute-intensive tasks
- Need real-time event processing (use dedicated message queues)

## Prerequisites

### GitHub Repository Setup
```bash
# Create workflow directory
mkdir -p .github/workflows

# Verify GitHub CLI installed
gh --version

# Authenticate with GitHub
gh auth login

# Check workflow permissions
gh api repos/{owner}/{repo}/actions/permissions
```

### Local Testing with act
```bash
# Install act for local workflow testing
# macOS
brew install act

# Linux
curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash

# Verify installation
act --version

# Run workflow locally
act -l                    # List available workflows
act push                  # Simulate push event
act pull_request          # Simulate PR event
act -j build              # Run specific job
```

### Workflow Linting
```bash
# Install actionlint
brew install actionlint   # macOS
go install github.com/rhysd/actionlint/cmd/actionlint@latest  # Go

# Lint workflows
actionlint .github/workflows/*.yml

# YAML validation
pip install yamllint
yamllint .github/workflows/
```

## Core Capabilities

### 1. Basic Workflow Structure

```yaml
# .github/workflows/ci.yml
name: CI Pipeline

# Workflow triggers
on:
  push:
    branches: [main, develop]
    paths:
      - 'src/**'
      - 'tests/**'
      - 'pyproject.toml'
  pull_request:
    branches: [main]
    types: [opened, synchronize, reopened]
  workflow_dispatch:
    inputs:
      environment:
        description: 'Deployment environment'
        required: true
        default: 'staging'
        type: choice
        options:
          - staging
          - production
      debug:
        description: 'Enable debug mode'
        required: false
        type: boolean
        default: false

# Environment variables for all jobs
env:
  PYTHON_VERSION: '3.11'
  NODE_VERSION: '20'
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

# Concurrency control
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

# Workflow permissions
permissions:
  contents: read
  packages: write
  pull-requests: write

jobs:
  lint:
    name: Code Quality
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}
          cache: 'pip'

      - name: Install linters
        run: |
          pip install ruff mypy

      - name: Run linting
        run: |
          ruff check src/
          ruff format --check src/

      - name: Type checking
        run: mypy src/ --ignore-missing-imports

  test:
    name: Test Suite
    needs: lint
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
          pip install -e ".[dev]"

      - name: Run tests
        run: |
          pytest tests/ -v --cov=src --cov-report=xml --cov-report=html

      - name: Upload coverage
        uses: codecov/codecov-action@v4
        with:
          files: ./coverage.xml
          fail_ci_if_error: true

  build:
    name: Build Package
    needs: test
    runs-on: ubuntu-latest
    outputs:
      version: ${{ steps.version.outputs.version }}
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}

      - name: Install build tools
        run: pip install build

      - name: Get version
        id: version
        run: |
          VERSION=$(python -c "import tomllib; print(tomllib.load(open('pyproject.toml', 'rb'))['project']['version'])")
          echo "version=$VERSION" >> $GITHUB_OUTPUT

      - name: Build package
        run: python -m build

      - name: Upload artifacts
        uses: actions/upload-artifact@v4
        with:
          name: dist-${{ steps.version.outputs.version }}
          path: dist/
          retention-days: 5
```

### 2. Matrix Builds for Cross-Platform Testing

```yaml
# .github/workflows/matrix-test.yml
name: Cross-Platform Tests

on:
  push:
    branches: [main]
  pull_request:

jobs:
  test-matrix:
    name: Test (${{ matrix.os }}, Python ${{ matrix.python-version }})
    runs-on: ${{ matrix.os }}

    strategy:
      fail-fast: false
      max-parallel: 4
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        python-version: ['3.10', '3.11', '3.12']
        include:
          # Additional configuration for specific combinations
          - os: ubuntu-latest
            python-version: '3.12'
            coverage: true
          # Experimental Python version
          - os: ubuntu-latest
            python-version: '3.13-dev'
            experimental: true
        exclude:
          # Skip Windows + Python 3.10 (known issues)
          - os: windows-latest
            python-version: '3.10'

    continue-on-error: ${{ matrix.experimental || false }}

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
          cache: 'pip'
          cache-dependency-path: |
            pyproject.toml
            requirements*.txt

      - name: Install dependencies (Unix)
        if: runner.os != 'Windows'
        run: |
          pip install -e ".[dev]"

      - name: Install dependencies (Windows)
        if: runner.os == 'Windows'
        run: |
          pip install -e ".[dev]"
        shell: pwsh

      - name: Run tests
        run: |
          pytest tests/ -v --tb=short
        env:
          CI: true
          PLATFORM: ${{ matrix.os }}

      - name: Run tests with coverage
        if: matrix.coverage
        run: |
          pytest tests/ -v --cov=src --cov-report=xml

      - name: Upload coverage
        if: matrix.coverage
        uses: codecov/codecov-action@v4
        with:
          files: ./coverage.xml

  test-summary:
    name: Test Summary
    needs: test-matrix
    if: always()
    runs-on: ubuntu-latest
    steps:
      - name: Check matrix results
        run: |
          if [ "${{ needs.test-matrix.result }}" == "failure" ]; then
            echo "Some matrix jobs failed"
            exit 1
          fi
          echo "All matrix jobs passed"
```

### 3. Caching Strategies

```yaml
# .github/workflows/caching.yml
name: Build with Caching

on: [push, pull_request]

jobs:
  build-with-cache:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      # Python pip cache
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'
          cache-dependency-path: |
            requirements.txt
            requirements-dev.txt

      # Node modules cache
      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
          cache-dependency-path: package-lock.json

      # Custom cache for build artifacts
      - name: Cache build outputs
        uses: actions/cache@v4
        id: build-cache
        with:
          path: |
            build/
            dist/
            .pytest_cache/
          key: build-${{ runner.os }}-${{ hashFiles('src/**', 'pyproject.toml') }}
          restore-keys: |
            build-${{ runner.os }}-

      # Docker layer cache
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Cache Docker layers
        uses: actions/cache@v4
        with:
          path: /tmp/.buildx-cache
          key: docker-${{ runner.os }}-${{ hashFiles('Dockerfile') }}
          restore-keys: |
            docker-${{ runner.os }}-

      # Rust cargo cache
      - name: Cache Cargo
        uses: actions/cache@v4
        with:
          path: |
            ~/.cargo/bin/
            ~/.cargo/registry/index/
            ~/.cargo/registry/cache/
            ~/.cargo/git/db/
            target/
          key: cargo-${{ runner.os }}-${{ hashFiles('**/Cargo.lock') }}
          restore-keys: |
            cargo-${{ runner.os }}-

      - name: Skip build if cached
        if: steps.build-cache.outputs.cache-hit == 'true'
        run: echo "Using cached build artifacts"

      - name: Build
        if: steps.build-cache.outputs.cache-hit != 'true'
        run: |
          pip install -e ".[dev]"
          python -m build

      - name: Run tests
        run: pytest tests/ -v
```

### 4. Artifact Management

```yaml
# .github/workflows/artifacts.yml
name: Build and Release Artifacts

on:
  push:
    tags: ['v*']
  workflow_dispatch:

jobs:
  build-artifacts:
    name: Build (${{ matrix.os }})
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        include:
          - os: ubuntu-latest
            artifact_name: app-linux-x64
            asset_name: app-linux-x64.tar.gz
          - os: macos-latest
            artifact_name: app-macos-x64
            asset_name: app-macos-x64.tar.gz
          - os: windows-latest
            artifact_name: app-windows-x64
            asset_name: app-windows-x64.zip

    steps:
      - uses: actions/checkout@v4

      - name: Build application
        run: |
          echo "Building for ${{ matrix.os }}"
          mkdir -p dist
          # Build commands here

      - name: Package (Unix)
        if: runner.os != 'Windows'
        run: |
          tar -czvf ${{ matrix.asset_name }} -C dist .

      - name: Package (Windows)
        if: runner.os == 'Windows'
        run: |
          Compress-Archive -Path dist/* -DestinationPath ${{ matrix.asset_name }}
        shell: pwsh

      - name: Upload artifact
        uses: actions/upload-artifact@v4
        with:
          name: ${{ matrix.artifact_name }}
          path: ${{ matrix.asset_name }}
          retention-days: 30
          compression-level: 9

  create-release:
    name: Create Release
    needs: build-artifacts
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - uses: actions/checkout@v4

      - name: Download all artifacts
        uses: actions/download-artifact@v4
        with:
          path: artifacts/
          merge-multiple: false

      - name: List artifacts
        run: find artifacts/ -type f

      - name: Generate changelog
        id: changelog
        run: |
          # Extract changelog for this version
          VERSION=${GITHUB_REF#refs/tags/}
          echo "version=$VERSION" >> $GITHUB_OUTPUT

          # Generate release notes
          cat << EOF > release_notes.md
          ## What's Changed

          See [CHANGELOG.md](CHANGELOG.md) for details.

          ## Assets
          - \`app-linux-x64.tar.gz\` - Linux (x64)
          - \`app-macos-x64.tar.gz\` - macOS (x64)
          - \`app-windows-x64.zip\` - Windows (x64)
          EOF

      - name: Create Release
        uses: softprops/action-gh-release@v2
        with:
          name: Release ${{ steps.changelog.outputs.version }}
          body_path: release_notes.md
          draft: false
          prerelease: ${{ contains(github.ref, 'alpha') || contains(github.ref, 'beta') }}
          files: |
            artifacts/**/*
          generate_release_notes: true
```

### 5. Reusable Workflows

```yaml
# .github/workflows/reusable-python-ci.yml
name: Reusable Python CI

on:
  workflow_call:
    inputs:
      python-version:
        description: 'Python version to use'
        required: false
        type: string
        default: '3.11'
      test-command:
        description: 'Test command to run'
        required: false
        type: string
        default: 'pytest tests/ -v'
      coverage:
        description: 'Enable coverage reporting'
        required: false
        type: boolean
        default: true
      install-extras:
        description: 'Package extras to install'
        required: false
        type: string
        default: 'dev'
    secrets:
      CODECOV_TOKEN:
        description: 'Codecov upload token'
        required: false
    outputs:
      coverage-percent:
        description: 'Test coverage percentage'
        value: ${{ jobs.test.outputs.coverage }}

jobs:
  lint:
    name: Lint
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ inputs.python-version }}
          cache: 'pip'

      - name: Install linters
        run: pip install ruff

      - name: Run ruff
        run: ruff check .

  test:
    name: Test
    needs: lint
    runs-on: ubuntu-latest
    outputs:
      coverage: ${{ steps.coverage.outputs.percent }}
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ inputs.python-version }}
          cache: 'pip'

      - name: Install dependencies
        run: pip install -e ".[${{ inputs.install-extras }}]"

      - name: Run tests
        run: ${{ inputs.test-command }}

      - name: Run tests with coverage
        if: inputs.coverage
        run: |
          pip install pytest-cov
          pytest tests/ -v --cov=src --cov-report=xml --cov-report=term-missing

      - name: Extract coverage
        if: inputs.coverage
        id: coverage
        run: |
          COVERAGE=$(python -c "import xml.etree.ElementTree as ET; print(f\"{float(ET.parse('coverage.xml').getroot().get('line-rate')) * 100:.1f}\")")
          echo "percent=$COVERAGE" >> $GITHUB_OUTPUT

      - name: Upload coverage
        if: inputs.coverage && secrets.CODECOV_TOKEN
        uses: codecov/codecov-action@v4
        with:
          token: ${{ secrets.CODECOV_TOKEN }}
          files: ./coverage.xml
```

```yaml
# .github/workflows/ci.yml - Using the reusable workflow
name: CI

on:
  push:
    branches: [main]
  pull_request:

jobs:
  python-ci:
    uses: ./.github/workflows/reusable-python-ci.yml
    with:
      python-version: '3.11'
      test-command: 'pytest tests/ -v --tb=short'
      coverage: true
      install-extras: 'dev,test'
    secrets:
      CODECOV_TOKEN: ${{ secrets.CODECOV_TOKEN }}
```

### 6. Composite Actions

```yaml
# .github/actions/setup-project/action.yml
name: 'Setup Project'
description: 'Set up Python environment with dependencies and caching'

inputs:
  python-version:
    description: 'Python version'
    required: false
    default: '3.11'
  install-dev:
    description: 'Install dev dependencies'
    required: false
    default: 'true'
  working-directory:
    description: 'Working directory'
    required: false
    default: '.'

outputs:
  python-path:
    description: 'Path to Python executable'
    value: ${{ steps.setup-python.outputs.python-path }}
  cache-hit:
    description: 'Whether cache was hit'
    value: ${{ steps.pip-cache.outputs.cache-hit }}

runs:
  using: 'composite'
  steps:
    - name: Set up Python
      id: setup-python
      uses: actions/setup-python@v5
      with:
        python-version: ${{ inputs.python-version }}

    - name: Get pip cache dir
      id: pip-cache-dir
      shell: bash
      run: echo "dir=$(pip cache dir)" >> $GITHUB_OUTPUT

    - name: Cache pip
      id: pip-cache
      uses: actions/cache@v4
      with:
        path: ${{ steps.pip-cache-dir.outputs.dir }}
        key: pip-${{ runner.os }}-${{ inputs.python-version }}-${{ hashFiles('**/pyproject.toml', '**/requirements*.txt') }}
        restore-keys: |
          pip-${{ runner.os }}-${{ inputs.python-version }}-
          pip-${{ runner.os }}-

    - name: Install base dependencies
      shell: bash
      working-directory: ${{ inputs.working-directory }}
      run: |
        python -m pip install --upgrade pip wheel setuptools

    - name: Install project
      shell: bash
      working-directory: ${{ inputs.working-directory }}
      run: |
        if [ "${{ inputs.install-dev }}" == "true" ]; then
          pip install -e ".[dev]"
        else
          pip install -e .
        fi
```

```yaml
# Using the composite action
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Project
        uses: ./.github/actions/setup-project
        with:
          python-version: '3.11'
          install-dev: 'true'

      - name: Run tests
        run: pytest tests/ -v
```

### 7. Secrets and Environment Management

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]
  workflow_dispatch:
    inputs:
      environment:
        type: environment
        description: 'Select environment'
        required: true

jobs:
  deploy-staging:
    name: Deploy to Staging
    runs-on: ubuntu-latest
    environment:
      name: staging
      url: https://staging.example.com
    steps:
      - uses: actions/checkout@v4

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1

      - name: Deploy to staging
        env:
          DATABASE_URL: ${{ secrets.DATABASE_URL }}
          API_KEY: ${{ secrets.API_KEY }}
          ENVIRONMENT: staging
        run: |
          echo "Deploying to staging..."
          # Deployment commands

  deploy-production:
    name: Deploy to Production
    needs: deploy-staging
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    environment:
      name: production
      url: https://example.com
    concurrency:
      group: production-deploy
      cancel-in-progress: false
    steps:
      - uses: actions/checkout@v4

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1

      - name: Deploy to production
        env:
          DATABASE_URL: ${{ secrets.DATABASE_URL }}
          API_KEY: ${{ secrets.API_KEY }}
          ENVIRONMENT: production
        run: |
          echo "Deploying to production..."
          # Deployment commands

      - name: Notify on failure
        if: failure()
        uses: slackapi/slack-github-action@v1
        with:
          payload: |
            {
              "text": "Production deployment failed!",
              "blocks": [
                {
                  "type": "section",
                  "text": {
                    "type": "mrkdwn",
                    "text": "*Production Deployment Failed*\nWorkflow: ${{ github.workflow }}\nRun: ${{ github.run_id }}"
                  }
                }
              ]
            }
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK }}
```

### 8. Container Builds and Registry Publishing

```yaml
# .github/workflows/docker.yml
name: Docker Build and Push

on:
  push:
    branches: [main]
    tags: ['v*']
  pull_request:
    branches: [main]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  build-and-push:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
      id-token: write  # For signing

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set up QEMU
        uses: docker/setup-qemu-action@v3

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Login to Container Registry
        if: github.event_name != 'pull_request'
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
            type=semver,pattern={{major}}
            type=sha,prefix=

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          platforms: linux/amd64,linux/arm64
          push: ${{ github.event_name != 'pull_request' }}
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
          build-args: |
            VERSION=${{ github.ref_name }}
            BUILD_DATE=${{ github.event.head_commit.timestamp }}

      - name: Sign image
        if: github.event_name != 'pull_request'
        uses: sigstore/cosign-installer@v3

      - name: Sign container image
        if: github.event_name != 'pull_request'
        run: |
          cosign sign --yes ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}@${{ steps.build-and-push.outputs.digest }}
```

### 9. Scheduled Workflows and Maintenance

```yaml
# .github/workflows/maintenance.yml
name: Repository Maintenance

on:
  schedule:
    # Run every Monday at 6 AM UTC
    - cron: '0 6 * * 1'
  workflow_dispatch:

permissions:
  contents: write
  issues: write
  pull-requests: write

jobs:
  dependency-update:
    name: Update Dependencies
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Update dependencies
        run: |
          pip install pip-tools
          pip-compile --upgrade requirements.in -o requirements.txt
          pip-compile --upgrade requirements-dev.in -o requirements-dev.txt

      - name: Create PR if changes
        uses: peter-evans/create-pull-request@v6
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
          commit-message: 'chore(deps): update dependencies'
          title: 'chore(deps): Weekly dependency update'
          body: |
            Automated weekly dependency update.

            Please review the changes and merge if CI passes.
          branch: deps/weekly-update
          delete-branch: true
          labels: dependencies,automated

  stale-issues:
    name: Close Stale Issues
    runs-on: ubuntu-latest
    steps:
      - uses: actions/stale@v9
        with:
          repo-token: ${{ secrets.GITHUB_TOKEN }}
          stale-issue-message: |
            This issue has been automatically marked as stale because it has not had recent activity.
            It will be closed in 7 days if no further activity occurs.
          stale-pr-message: |
            This PR has been automatically marked as stale because it has not had recent activity.
            It will be closed in 7 days if no further activity occurs.
          stale-issue-label: 'stale'
          stale-pr-label: 'stale'
          days-before-stale: 60
          days-before-close: 7
          exempt-issue-labels: 'pinned,security,enhancement'
          exempt-pr-labels: 'pinned,security'

  security-scan:
    name: Security Audit
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          ignore-unfixed: true
          format: 'sarif'
          output: 'trivy-results.sarif'
          severity: 'CRITICAL,HIGH'

      - name: Upload Trivy scan results
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: 'trivy-results.sarif'

      - name: Python safety check
        run: |
          pip install safety
          safety check --full-report || true
```

### 10. PR Automation and Checks

```yaml
# .github/workflows/pr-checks.yml
name: PR Checks

on:
  pull_request:
    types: [opened, synchronize, reopened, edited]

permissions:
  contents: read
  pull-requests: write

jobs:
  validate-pr:
    name: Validate PR
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Check PR title
        uses: amannn/action-semantic-pull-request@v5
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          types: |
            feat
            fix
            docs
            style
            refactor
            perf
            test
            build
            ci
            chore
            revert
          requireScope: false
          subjectPattern: ^.{1,50}$
          subjectPatternError: |
            PR title must be 50 characters or less

      - name: Check for breaking changes
        if: contains(github.event.pull_request.title, '!')
        run: |
          echo "::warning::This PR contains breaking changes"

      - name: Add size labels
        uses: codelytv/pr-size-labeler@v1
        with:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          xs_label: 'size/xs'
          xs_max_size: 10
          s_label: 'size/s'
          s_max_size: 100
          m_label: 'size/m'
          m_max_size: 500
          l_label: 'size/l'
          l_max_size: 1000
          xl_label: 'size/xl'
          fail_if_xl: false
          message_if_xl: |
            This PR is very large. Please consider breaking it into smaller PRs.

  auto-assign:
    name: Auto Assign
    runs-on: ubuntu-latest
    steps:
      - name: Auto-assign author
        uses: kentaro-m/auto-assign-action@v1
        with:
          configuration-path: '.github/auto-assign.yml'

  label-pr:
    name: Label PR
    runs-on: ubuntu-latest
    steps:
      - uses: actions/labeler@v5
        with:
          repo-token: ${{ secrets.GITHUB_TOKEN }}
          configuration-path: .github/labeler.yml
```

## Integration Examples

### Integration with Slack Notifications

```yaml
# .github/workflows/notify.yml
name: Slack Notifications

on:
  workflow_run:
    workflows: ["CI Pipeline"]
    types: [completed]

jobs:
  notify:
    runs-on: ubuntu-latest
    steps:
      - name: Notify Slack
        uses: slackapi/slack-github-action@v1
        with:
          payload: |
            {
              "blocks": [
                {
                  "type": "header",
                  "text": {
                    "type": "plain_text",
                    "text": "${{ github.event.workflow_run.conclusion == 'success' && 'Build Succeeded' || 'Build Failed' }}"
                  }
                },
                {
                  "type": "section",
                  "fields": [
                    {
                      "type": "mrkdwn",
                      "text": "*Repository:*\n${{ github.repository }}"
                    },
                    {
                      "type": "mrkdwn",
                      "text": "*Branch:*\n${{ github.event.workflow_run.head_branch }}"
                    },
                    {
                      "type": "mrkdwn",
                      "text": "*Commit:*\n<${{ github.event.workflow_run.head_commit.url }}|${{ github.event.workflow_run.head_sha }}>"
                    },
                    {
                      "type": "mrkdwn",
                      "text": "*Author:*\n${{ github.event.workflow_run.head_commit.author.name }}"
                    }
                  ]
                },
                {
                  "type": "actions",
                  "elements": [
                    {
                      "type": "button",
                      "text": {
                        "type": "plain_text",
                        "text": "View Run"
                      },
                      "url": "${{ github.event.workflow_run.html_url }}"
                    }
                  ]
                }
              ]
            }
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK }}
          SLACK_WEBHOOK_TYPE: INCOMING_WEBHOOK
```

### Integration with AWS Deployment

```yaml
# .github/workflows/aws-deploy.yml
name: AWS Deployment

on:
  push:
    branches: [main]

jobs:
  deploy-lambda:
    runs-on: ubuntu-latest
    permissions:
      id-token: write
      contents: read
    steps:
      - uses: actions/checkout@v4

      - name: Configure AWS credentials (OIDC)
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ secrets.AWS_ROLE_ARN }}
          aws-region: us-east-1

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install SAM CLI
        run: pip install aws-sam-cli

      - name: Build
        run: sam build

      - name: Deploy
        run: |
          sam deploy \
            --no-confirm-changeset \
            --no-fail-on-empty-changeset \
            --stack-name my-app \
            --capabilities CAPABILITY_IAM \
            --parameter-overrides Environment=production
```

## Best Practices

### 1. Security Best Practices
```yaml
# Always pin action versions with SHA
- uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11  # v4.1.1

# Use minimum required permissions
permissions:
  contents: read
  packages: write

# Never hardcode secrets
env:
  API_KEY: ${{ secrets.API_KEY }}  # Good
  # API_KEY: "sk-1234567890"       # Never do this

# Use OIDC for cloud provider authentication
- uses: aws-actions/configure-aws-credentials@v4
  with:
    role-to-assume: ${{ secrets.AWS_ROLE_ARN }}
```

### 2. Performance Optimization
```yaml
# Use caching aggressively
- uses: actions/cache@v4
  with:
    path: ~/.cache/pip
    key: pip-${{ hashFiles('requirements.txt') }}

# Use matrix fail-fast wisely
strategy:
  fail-fast: false  # Continue other jobs on failure

# Limit concurrent runs
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```

### 3. Maintainability
```yaml
# Use reusable workflows
jobs:
  test:
    uses: ./.github/workflows/reusable-test.yml

# Extract common steps into composite actions
- uses: ./.github/actions/setup-project

# Use environment variables for configuration
env:
  PYTHON_VERSION: '3.11'
  NODE_VERSION: '20'
```

### 4. Error Handling
```yaml
# Use continue-on-error for non-critical steps
- name: Optional step
  continue-on-error: true
  run: optional-command

# Add timeout to prevent stuck jobs
jobs:
  build:
    timeout-minutes: 30

# Always clean up resources
- name: Cleanup
  if: always()
  run: cleanup-command
```

## Troubleshooting

### Common Issues

**Issue: Workflow not triggering**
```yaml
# Check trigger paths
on:
  push:
    paths:
      - 'src/**'  # Only triggers for src/ changes

# Verify branch names match
on:
  push:
    branches:
      - main
      - 'release/*'  # Use quotes for patterns
```

**Issue: Cache not restoring**
```yaml
# Verify cache key matches
- uses: actions/cache@v4
  with:
    path: ~/.cache/pip
    key: pip-${{ runner.os }}-${{ hashFiles('**/requirements.txt') }}
    restore-keys: |
      pip-${{ runner.os }}-
```

**Issue: Secrets not available**
```yaml
# Secrets not available in forks
- name: Deploy
  if: github.event.pull_request.head.repo.full_name == github.repository
  env:
    SECRET: ${{ secrets.MY_SECRET }}
```

**Issue: Permission denied**
```yaml
# Add required permissions
permissions:
  contents: write
  packages: write
  pull-requests: write
```

### Debugging Workflows

```yaml
# Enable debug logging
jobs:
  debug:
    runs-on: ubuntu-latest
    steps:
      - name: Dump context
        env:
          GITHUB_CONTEXT: ${{ toJson(github) }}
          JOB_CONTEXT: ${{ toJson(job) }}
          STEPS_CONTEXT: ${{ toJson(steps) }}
        run: |
          echo "GitHub context:"
          echo "$GITHUB_CONTEXT"
          echo "Job context:"
          echo "$JOB_CONTEXT"
```

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-01-17 | Initial release with comprehensive CI/CD patterns |

## Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Workflow Syntax Reference](https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions)
- [GitHub Actions Marketplace](https://github.com/marketplace?type=actions)
- [act - Local Testing](https://github.com/nektos/act)
- [actionlint - Workflow Linter](https://github.com/rhysd/actionlint)

---

*This skill provides production-ready patterns for GitHub Actions workflows, tested across multiple repositories and CI/CD pipelines.*
