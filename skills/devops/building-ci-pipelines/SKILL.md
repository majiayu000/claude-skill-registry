---
name: building-ci-pipelines
description: Constructs secure, efficient CI/CD pipelines with supply chain security (SLSA), monorepo optimization, caching strategies, and parallelization patterns for GitHub Actions, GitLab CI, and Argo Workflows. Use when setting up automated testing, building, or deployment workflows.
---

# Building CI Pipelines

## Purpose

CI/CD pipelines automate testing, building, and deploying software. This skill provides patterns for constructing robust, secure, and efficient pipelines across GitHub Actions, GitLab CI, Argo Workflows, and Jenkins. Focus areas: supply chain security (SLSA), monorepo optimization, caching, and parallelization.

## When to Use This Skill

Invoke when:
- Setting up continuous integration for new projects
- Implementing automated testing workflows
- Building container images with security provenance
- Optimizing slow CI pipelines (especially monorepos)
- Implementing SLSA supply chain security
- Configuring multi-platform builds
- Setting up GitOps automation
- Migrating from legacy CI systems

## Platform Selection

**GitHub-hosted** → GitHub Actions (SLSA native, 10K+ actions, OIDC)
**GitLab-hosted** → GitLab CI (parent-child pipelines, built-in security)
**Kubernetes** → Argo Workflows (DAG-based, event-driven)
**Legacy** → Jenkins (migrate when possible)

### Platform Comparison

| Feature | GitHub Actions | GitLab CI | Argo | Jenkins |
|---------|---------------|-----------|------|---------|
| Ease of Use | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| SLSA | Native | Manual | Good | Manual |
| Monorepo | Good | Excellent | Manual | Plugins |

## Quick Start Patterns

### Pattern 1: Basic CI (Lint → Test → Build)

```yaml
# GitHub Actions
name: CI
on: [push, pull_request]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm run lint

  test:
    needs: lint
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm test

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm run build
```

### Pattern 2: Matrix Strategy (Multi-Platform)

```yaml
test:
  runs-on: ${{ matrix.os }}
  strategy:
    matrix:
      os: [ubuntu-latest, windows-latest, macos-latest]
      node-version: [18, 20, 22]
  steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-node@v4
      with:
        node-version: ${{ matrix.node-version }}
    - run: npm test
```

9 jobs (3 OS × 3 versions) in parallel: 5 min vs 45 min sequential.

### Pattern 3: Monorepo Affected (Turborepo)

```yaml
build:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
      with:
        fetch-depth: 0  # Required for affected detection

    - uses: actions/setup-node@v4
      with:
        node-version: 20

    - name: Build affected
      run: npx turbo run build --filter='...[origin/main]'
      env:
        TURBO_TOKEN: ${{ secrets.TURBO_TOKEN }}
        TURBO_TEAM: ${{ vars.TURBO_TEAM }}
```

60-80% CI time reduction for monorepos.

### Pattern 4: SLSA Level 3 Provenance

```yaml
name: SLSA Build
on:
  push:
    tags: ['v*']

permissions:
  id-token: write
  contents: read
  packages: write

jobs:
  build:
    runs-on: ubuntu-latest
    outputs:
      digest: ${{ steps.build.outputs.digest }}
    steps:
      - uses: actions/checkout@v4
      - name: Build container
        id: build
        uses: docker/build-push-action@v5
        with:
          push: true
          tags: ghcr.io/${{ github.repository }}:${{ github.sha }}

  provenance:
    needs: build
    permissions:
      id-token: write
      actions: read
      packages: write
    uses: slsa-framework/slsa-github-generator/.github/workflows/generator_container_slsa3.yml@v1.10.0
    with:
      image: ghcr.io/${{ github.repository }}
      digest: ${{ needs.build.outputs.digest }}
      registry-username: ${{ github.actor }}
    secrets:
      registry-password: ${{ secrets.GITHUB_TOKEN }}
```

Verification:
```bash
cosign verify-attestation --type slsaprovenance \
  --certificate-identity-regexp "^https://github.com/slsa-framework" \
  --certificate-oidc-issuer https://token.actions.githubusercontent.com \
  ghcr.io/myorg/myapp@sha256:abcd...
```

### Pattern 5: OIDC Federation (No Credentials)

```yaml
deploy:
  runs-on: ubuntu-latest
  permissions:
    id-token: write
    contents: read
  steps:
    - uses: actions/checkout@v4

    - name: Configure AWS credentials
      uses: aws-actions/configure-aws-credentials@v4
      with:
        role-to-assume: arn:aws:iam::123456789012:role/GitHubActionsRole
        aws-region: us-east-1

    - name: Deploy
      run: aws s3 sync ./dist s3://my-bucket
```

Benefits: No stored credentials, 1-hour lifetime, full audit trail.

### Pattern 6: Security Scanning

```yaml
security:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
      with:
        fetch-depth: 0

    - name: Gitleaks (secret detection)
      uses: gitleaks/gitleaks-action@v2

    - name: Snyk (vulnerability scan)
      uses: snyk/actions/node@master
      env:
        SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}

    - name: SBOM generation
      uses: anchore/sbom-action@v0
      with:
        format: spdx-json
        output-file: sbom.spdx.json
```

## Caching

### Automatic Dependency Caching

```yaml
- uses: actions/setup-node@v4
  with:
    node-version: 20
    cache: 'npm'  # Auto-caches ~/.npm
- run: npm ci
```

Supported: npm, yarn, pnpm, pip, poetry, cargo, go

### Manual Cache Control

```yaml
- uses: actions/cache@v4
  with:
    path: |
      ~/.cargo/bin
      ~/.cargo/registry
      target/
    key: ${{ runner.os }}-cargo-${{ hashFiles('**/Cargo.lock') }}
    restore-keys: |
      ${{ runner.os }}-cargo-
```

### Multi-Layer Caching (Nx)

```yaml
- name: Nx Cloud (build outputs)
  run: npx nx affected -t build
  env:
    NX_CLOUD_ACCESS_TOKEN: ${{ secrets.NX_CLOUD_ACCESS_TOKEN }}

- name: Vite Cache
  uses: actions/cache@v4
  with:
    path: '**/node_modules/.vite'
    key: vite-${{ hashFiles('package-lock.json') }}

- name: TypeScript Cache
  uses: actions/cache@v4
  with:
    path: '**/tsconfig.tsbuildinfo'
    key: tsc-${{ hashFiles('tsconfig.json') }}
```

Result: 70-90% build time reduction.

## Parallelization

### Job-Level Parallelization

```yaml
jobs:
  unit-tests:
    steps:
      - run: npm run test:unit

  integration-tests:
    steps:
      - run: npm run test:integration

  e2e-tests:
    steps:
      - run: npm run test:e2e
```

All three run simultaneously.

### Test Sharding

```yaml
test:
  strategy:
    matrix:
      shard: [1, 2, 3, 4]
  steps:
    - run: npm test -- --shard=${{ matrix.shard }}/4
```

20min test suite → 5min (4x speedup).

## Language Examples

### Python

```yaml
test:
  strategy:
    matrix:
      python-version: ['3.10', '3.11', '3.12']
  steps:
    - uses: actions/setup-python@v5
      with:
        python-version: ${{ matrix.python-version }}
    - run: pipx install poetry
    - run: poetry install
    - run: poetry run ruff check .
    - run: poetry run mypy .
    - run: poetry run pytest --cov
```

### Rust

```yaml
test:
  strategy:
    matrix:
      os: [ubuntu-latest, windows-latest, macos-latest]
      rust: [stable, nightly]
  steps:
    - uses: dtolnay/rust-toolchain@master
      with:
        toolchain: ${{ matrix.rust }}
        components: rustfmt, clippy
    - uses: Swatinem/rust-cache@v2
    - run: cargo fmt -- --check
    - run: cargo clippy -- -D warnings
    - run: cargo test
```

### Go

```yaml
test:
  steps:
    - uses: actions/setup-go@v5
      with:
        go-version: '1.23'
        cache: true
    - run: go mod verify
    - uses: golangci/golangci-lint-action@v4
    - run: go test -v -race -coverprofile=coverage.txt ./...
```

### TypeScript

```yaml
test:
  strategy:
    matrix:
      node-version: [18, 20, 22]
  steps:
    - uses: pnpm/action-setup@v3
      with:
        version: 8
    - uses: actions/setup-node@v4
      with:
        node-version: ${{ matrix.node-version }}
        cache: 'pnpm'
    - run: pnpm install --frozen-lockfile
    - run: pnpm run lint
    - run: pnpm run type-check
    - run: pnpm test
```

## Best Practices

### Security

**DO:**
- Use OIDC instead of long-lived credentials
- Pin actions to commit SHA: `actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11`
- Restrict permissions: `permissions: { contents: read }`
- Scan secrets (Gitleaks) on every commit
- Generate SLSA provenance for releases

**DON'T:**
- Expose secrets in logs
- Use `pull_request_target` without validation
- Trust unverified third-party actions

### Performance

**DO:**
- Use affected detection for monorepos
- Cache dependencies and build outputs
- Parallelize independent jobs
- Fail fast: `strategy.fail-fast: true`
- Use remote caching (Turborepo/Nx Cloud)

**DON'T:**
- Rebuild everything on every commit
- Run long tests in PR checks
- Use generic cache keys

### Debugging

```yaml
# Enable debug logging
env:
  ACTIONS_STEP_DEBUG: true
  ACTIONS_RUNNER_DEBUG: true

# SSH into runner
- uses: mxschmitt/action-tmate@v3
```

## Advanced Patterns

For detailed guides, see references:

- **github-actions-patterns.md** - Reusable workflows, composite actions, matrix strategies, OIDC setup
- **gitlab-ci-patterns.md** - Parent-child pipelines, dynamic generation, runner configuration
- **argo-workflows-guide.md** - DAG templates, artifact passing, event-driven triggers
- **slsa-security-framework.md** - SLSA Levels 1-4, provenance generation, cosign verification
- **monorepo-ci-strategies.md** - Turborepo/Nx/Bazel affected detection algorithms
- **caching-strategies.md** - Multi-layer caching, Docker optimization, cache invalidation
- **parallelization-patterns.md** - Test sharding, job dependencies, DAG design
- **secrets-management.md** - OIDC for AWS/GCP/Azure, Vault integration, rotation

## Examples

Complete runnable workflows:

- **examples/github-actions-basic/** - Starter template (lint/test/build)
- **examples/github-actions-monorepo/** - Turborepo with remote caching
- **examples/github-actions-slsa/** - SLSA Level 3 provenance
- **examples/gitlab-ci-monorepo/** - Parent-child dynamic pipeline
- **examples/argo-workflows-dag/** - Diamond DAG parallelization
- **examples/multi-language-matrix/** - Cross-platform testing

## Utility Scripts

Token-free execution:

- **scripts/validate_workflow.py** - Validate YAML syntax and best practices
- **scripts/generate_github_workflow.py** - Generate workflow from template
- **scripts/analyze_ci_performance.py** - CI metrics analysis
- **scripts/setup_oidc_aws.py** - Automate AWS OIDC setup

## Related Skills

**testing-strategies** - Test execution strategies (unit, integration, E2E)
**deploying-applications** - Deployment automation and GitOps
**auth-security** - Secrets management and authentication
**observability** - Pipeline monitoring and alerting
