---
name: writing-github-actions
description: Write GitHub Actions workflows with proper syntax, reusable workflows, composite actions, matrix builds, caching, and security best practices. Use when creating CI/CD workflows for GitHub-hosted projects or automating GitHub repository tasks.
---

# Writing GitHub Actions

Create GitHub Actions workflows for CI/CD pipelines, automated testing, deployments, and repository automation using YAML-based configuration with native GitHub integration.

## Purpose

GitHub Actions is the native CI/CD platform for GitHub repositories. This skill covers workflow syntax, triggers, job orchestration, reusable patterns, optimization techniques, and security practices specific to GitHub Actions.

**Core Focus:**
- Workflow YAML syntax and structure
- Reusable workflows and composite actions
- Matrix builds and parallel execution
- Caching and optimization strategies
- Secrets management and OIDC authentication
- Concurrency control and artifact management

**Not Covered:**
- CI/CD pipeline design strategy → See `building-ci-pipelines`
- GitOps deployment patterns → See `gitops-workflows`
- Infrastructure as code → See `infrastructure-as-code`
- Testing frameworks → See `testing-strategies`

## When to Use This Skill

Trigger this skill when:
- Creating CI/CD workflows for GitHub repositories
- Automating tests, builds, and deployments via GitHub Actions
- Setting up reusable workflows across multiple repositories
- Optimizing workflow performance with caching and parallelization
- Implementing security best practices for GitHub Actions
- Troubleshooting GitHub Actions YAML syntax or behavior

## Workflow Fundamentals

### Basic Workflow Structure

```yaml
name: CI
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - run: npm test
```

**Key Components:**
- `name`: Workflow display name
- `on`: Trigger events (push, pull_request, schedule, workflow_dispatch)
- `jobs`: Job definitions (run in parallel by default)
- `runs-on`: Runner type (ubuntu-latest, windows-latest, macos-latest)
- `steps`: Sequential operations (uses actions or run commands)

### Common Triggers

```yaml
# Code events
on:
  push:
    branches: [main, develop]
    paths: ['src/**']
  pull_request:
    types: [opened, synchronize, reopened]

# Manual trigger
on:
  workflow_dispatch:
    inputs:
      environment:
        type: choice
        options: [dev, staging, production]

# Scheduled
on:
  schedule:
    - cron: '0 2 * * *'  # Daily at 2 AM UTC
```

For complete trigger reference, see `references/triggers-events.md`.

## Decision Frameworks

### Reusable Workflow vs Composite Action

**Use Reusable Workflow when:**
- Standardizing entire CI/CD jobs across repositories
- Need complete job replacement with inputs/outputs
- Want secrets to inherit by default
- Orchestrating multiple steps with job-level configuration

**Use Composite Action when:**
- Packaging 5-20 step sequences for reuse
- Need step-level abstraction within jobs
- Want to distribute via marketplace or private repos
- Require local file access without artifacts

| Feature | Reusable Workflow | Composite Action |
|---------|------------------|------------------|
| Scope | Complete job | Step sequence |
| Trigger | `workflow_call` | `uses:` in step |
| Secrets | Inherit by default | Must pass explicitly |
| File Sharing | Requires artifacts | Same runner/workspace |

For detailed patterns, see `references/reusable-workflows.md` and `references/composite-actions.md`.

### Caching Strategy

**Use Built-in Setup Action Caching (Recommended):**
```yaml
- uses: actions/setup-node@v4
  with:
    node-version: '20'
    cache: 'npm'  # or 'yarn', 'pnpm'
```

Available for: Node.js, Python (pip), Java (maven/gradle), .NET, Go

**Use Manual Caching when:**
- Need custom cache keys
- Caching build outputs or non-standard paths
- Implementing multi-layer cache strategies

```yaml
- uses: actions/cache@v4
  with:
    path: ~/.npm
    key: ${{ runner.os }}-deps-${{ hashFiles('**/package-lock.json') }}
    restore-keys: ${{ runner.os }}-deps-
```

For optimization techniques, see `references/caching-strategies.md`.

### Self-Hosted vs GitHub-Hosted Runners

**Use GitHub-Hosted Runners when:**
- Standard build environments sufficient
- No private network access required
- Within budget or free tier limits

**Use Self-Hosted Runners when:**
- Need specific hardware (GPU, ARM, high memory)
- Require private network/VPN access
- High usage volume (cost optimization)
- Custom software must be pre-installed

## Common Patterns

### Multi-Job Workflow with Dependencies

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
      - run: npm run build
      - uses: actions/upload-artifact@v4
        with:
          name: dist
          path: dist/

  test:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/download-artifact@v5
        with:
          name: dist
      - run: npm test

  deploy:
    needs: [build, test]
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: actions/download-artifact@v5
      - run: ./deploy.sh
```

**Key Elements:**
- `needs:` creates job dependencies (sequential execution)
- Artifacts pass data between jobs
- `if:` enables conditional execution
- `environment:` enables protection rules and environment secrets

### Matrix Builds

```yaml
jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      fail-fast: false
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        node: [18, 20, 22]
    steps:
      - uses: actions/checkout@v5
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node }}
      - run: npm test
```

Result: 9 jobs (3 OS × 3 Node versions)

For advanced matrix patterns, see `examples/matrix-build.yml`.

### Concurrency Control

```yaml
# Cancel in-progress runs on new push
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

# Single deployment per environment
jobs:
  deploy:
    concurrency:
      group: production-deployment
      cancel-in-progress: false
    steps: [...]
```

## Reusable Workflows

### Defining a Reusable Workflow

File: `.github/workflows/reusable-build.yml`

```yaml
name: Reusable Build
on:
  workflow_call:
    inputs:
      node-version:
        type: string
        default: '20'
    secrets:
      NPM_TOKEN:
        required: false
    outputs:
      artifact-name:
        value: ${{ jobs.build.outputs.artifact }}

jobs:
  build:
    runs-on: ubuntu-latest
    outputs:
      artifact: build-output
    steps:
      - uses: actions/checkout@v5
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ inputs.node-version }}
      - run: npm ci && npm run build
      - uses: actions/upload-artifact@v4
        with:
          name: build-output
          path: dist/
```

### Calling a Reusable Workflow

```yaml
jobs:
  build:
    uses: ./.github/workflows/reusable-build.yml
    with:
      node-version: '20'
    secrets: inherit  # Same org only
```

For complete reusable workflow guide, see `references/reusable-workflows.md`.

## Composite Actions

### Defining a Composite Action

File: `.github/actions/setup-project/action.yml`

```yaml
name: 'Setup Project'
description: 'Install dependencies and setup environment'

inputs:
  node-version:
    description: 'Node.js version'
    default: '20'

outputs:
  cache-hit:
    value: ${{ steps.cache.outputs.cache-hit }}

runs:
  using: "composite"
  steps:
    - uses: actions/setup-node@v4
      with:
        node-version: ${{ inputs.node-version }}
        cache: 'npm'

    - id: cache
      uses: actions/cache@v4
      with:
        path: node_modules
        key: ${{ runner.os }}-deps-${{ hashFiles('**/package-lock.json') }}

    - if: steps.cache.outputs.cache-hit != 'true'
      shell: bash
      run: npm ci
```

**Key Requirements:**
- `runs.using: "composite"` marks action type
- `shell:` required for all `run` steps
- Access inputs via `${{ inputs.name }}`

### Using a Composite Action

```yaml
steps:
  - uses: actions/checkout@v5
  - uses: ./.github/actions/setup-project
    with:
      node-version: '20'
  - run: npm run build
```

For detailed composite action patterns, see `references/composite-actions.md`.

## Security Best Practices

### Secrets Management

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production  # Uses environment secrets
    steps:
      - env:
          API_KEY: ${{ secrets.API_KEY }}
        run: ./deploy.sh
```

### OIDC Authentication (No Long-Lived Credentials)

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    permissions:
      id-token: write  # Required for OIDC
      contents: read
    steps:
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::123456789012:role/GitHubActionsRole
          aws-region: us-east-1
      - run: aws s3 sync ./dist s3://my-bucket
```

### Minimal Permissions

```yaml
# Workflow-level
permissions:
  contents: read
  pull-requests: write

# Job-level
jobs:
  deploy:
    permissions:
      contents: write
      deployments: write
    steps: [...]
```

### Action Pinning

```yaml
# Pin to commit SHA (not tags)
- uses: actions/checkout@8ade135a41bc03ea155e62e844d188df1ea18608  # v5.0.0
```

**Enable Dependabot:**

File: `.github/dependabot.yml`

```yaml
version: 2
updates:
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
```

For comprehensive security guide, see `references/security-practices.md`.

## Optimization Techniques

Use built-in caching in setup actions (`cache: 'npm'`), run independent jobs in parallel, add conditional execution with `if:`, and minimize checkout depth (`fetch-depth: 1`).

For detailed optimization strategies, see `references/caching-strategies.md`.

## Context Variables

Common contexts: `github.*`, `secrets.*`, `inputs.*`, `matrix.*`, `runner.*`

```yaml
- run: echo "Branch: ${{ github.ref }}, Event: ${{ github.event_name }}"
```

For complete syntax reference, see `references/workflow-syntax.md`.

## Progressive Disclosure

### Detailed References

For comprehensive coverage of specific topics:

- **references/workflow-syntax.md** - Complete YAML syntax reference
- **references/reusable-workflows.md** - Advanced reusable workflow patterns
- **references/composite-actions.md** - Composite action deep dive
- **references/caching-strategies.md** - Optimization and caching techniques
- **references/security-practices.md** - Comprehensive security guide
- **references/triggers-events.md** - All trigger types and event filters
- **references/marketplace-actions.md** - Recommended actions catalog

### Working Examples

Complete workflow templates ready to use:

- **examples/basic-ci.yml** - Simple CI workflow
- **examples/matrix-build.yml** - Matrix strategy examples
- **examples/reusable-deploy.yml** - Reusable deployment workflow
- **examples/composite-setup/** - Composite action template
- **examples/monorepo-workflow.yml** - Monorepo with path filters
- **examples/security-scan.yml** - Security scanning workflow

### Validation Scripts

- **scripts/validate-workflow.sh** - Validate YAML syntax

## Related Skills

- `building-ci-pipelines` - CI/CD pipeline design strategy
- `gitops-workflows` - GitOps deployment patterns
- `infrastructure-as-code` - Terraform/Pulumi integration
- `testing-strategies` - Test frameworks and coverage
- `security-hardening` - SAST/DAST tools
- `git-workflows` - Understanding branches and PRs
