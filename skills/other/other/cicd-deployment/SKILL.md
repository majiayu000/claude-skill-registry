---
name: cicd-deployment
description: "Manage CI/CD pipelines, build processes, deployment configurations, and release workflows. Use when the user says 'set up CI', 'create a pipeline', 'deploy this', 'fix the build', 'GitHub Actions', 'deployment failed', 'create release workflow', 'add a build step', 'configure staging', or 'set up preview deployments'. Also triggers on 'CI/CD', 'continuous integration', 'continuous deployment', 'pipeline configuration', 'build process', 'release management', 'deploy to production', or 'workflow automation'."
version: 1.0.0
---

# CI/CD Deployment Skill

## Purpose

CI/CD automates the path from code to production. Well-configured pipelines catch bugs before users, enforce quality gates, and make deploys boring. This skill covers pipeline creation, optimization, debugging, deployment strategies, and release management across platforms.

## When to Activate

- Setting up CI/CD for a new or existing project
- Debugging failed builds or deployments
- Adding or modifying pipeline stages (lint, test, deploy)
- Configuring deployment targets (staging, preview, production)
- Optimizing build times and reducing CI costs
- Designing release workflows (semantic versioning, changelogs)
- Setting up preview/ephemeral environments per PR
- Implementing rollback procedures

## Core Workflow

### Step 1: Detect Existing CI/CD

Search the repository for existing configuration:

```
.github/workflows/*.yml    # GitHub Actions
.circleci/config.yml       # CircleCI
Jenkinsfile                # Jenkins
.gitlab-ci.yml             # GitLab CI
bitbucket-pipelines.yml    # Bitbucket Pipelines
Dockerfile                 # Container builds
docker-compose.yml         # Multi-container orchestration
vercel.json                # Vercel
netlify.toml               # Netlify
fly.toml                   # Fly.io
render.yaml                # Render
railway.json               # Railway
appspec.yml                # AWS CodeDeploy
buildspec.yml              # AWS CodeBuild
cloudbuild.yaml            # Google Cloud Build
azure-pipelines.yml        # Azure DevOps
```

Also check `package.json` scripts, `Makefile`, and `Taskfile.yml` for build/deploy commands the pipeline may reference.

### Step 2: Understand the Stack

Before writing any pipeline config, identify:

- **Language & runtime**: Node.js, Python, Go, Rust, Java, etc.
- **Package manager**: npm, pnpm, yarn, pip, poetry, go modules, cargo
- **Build tool**: webpack, vite, esbuild, tsc, gradle, make
- **Test runner**: jest, vitest, pytest, go test, cargo test
- **Linter/formatter**: eslint, prettier, ruff, golangci-lint, clippy
- **Deployment target**: Vercel, AWS, GCP, Fly.io, Kubernetes, static hosting
- **Monorepo tooling**: turborepo, nx, lerna, pnpm workspaces

### Step 3: Apply or Modify Pipeline Configuration

Generate or modify pipeline config following these principles:

1. **Match project conventions** -- use the same scripts from package.json/Makefile
2. **Fail fast** -- run cheapest checks first (lint before full test suite)
3. **Cache aggressively** -- dependencies, build artifacts, Docker layers
4. **Minimize secrets** -- use OIDC where possible, scope secrets to environments
5. **Pin versions** -- actions, Docker images, runtime versions
6. **Set timeouts** -- every job and long-running step needs an explicit timeout

### Step 4: Validate

Before committing pipeline changes:

1. **Syntax check** -- use `actionlint` for GitHub Actions, `circleci config validate`, etc.
2. **Verify secret references** -- confirm every `${{ secrets.X }}` has a corresponding secret configured
3. **Confirm scripts exist** -- every `npm run X` or `make Y` must resolve to a real command
4. **Test locally** -- use `act` for GitHub Actions, `circleci local execute` for CircleCI
5. **Dry run** -- push to a feature branch first, never modify the default branch pipeline blindly

## Pipeline Architecture

A production-grade pipeline has five stages. Not every project needs all of them -- start simple and add stages as the project matures.

### Stage 1: Build

- Install dependencies with lockfile (`npm ci`, `pip install -r requirements.txt`)
- Enable dependency caching keyed on lockfile hash
- Compile/transpile source code
- Generate build artifacts and pass to downstream jobs

### Stage 2: Quality Gate

- Lint source code (eslint, ruff, clippy)
- Type-check (tsc --noEmit, mypy, pyright)
- Run unit tests with coverage reporting
- Security scan dependencies (npm audit, trivy, snyk)
- Check for secrets in code (gitleaks, trufflehog)

### Stage 3: Integration

- Run integration tests against real services (database, API)
- Execute database migrations in test environment
- Run E2E tests (Playwright, Cypress) against preview deployment
- Contract testing for microservices

### Stage 4: Deploy

- Deploy to preview/staging environment on PR
- Run smoke tests against staging
- Deploy to production on merge to default branch
- Use deployment strategy appropriate to risk (see `references/deployment-strategies.md`)

### Stage 5: Post-Deploy

- Run smoke tests against production
- Health check endpoints
- Notify team (Slack, Discord, email)
- Tag release, generate changelog
- Monitor error rates for regression

## Build Optimization

### Dependency Caching

Cache dependencies to avoid re-downloading on every build:

- **npm/pnpm/yarn**: Cache based on lockfile hash
- **pip**: Cache `~/.cache/pip` with requirements hash
- **Go**: Cache `~/go/pkg/mod` with go.sum hash
- **Docker**: Layer caching, BuildKit cache mounts
- **Turborepo/Nx**: Remote caching for monorepo builds

See `references/github-actions-patterns.md` for platform-specific examples.

### Parallel Execution

Run independent stages concurrently:

- Lint, type-check, and unit tests can run in parallel
- Different test suites (unit, integration, e2e) can run in parallel
- Multi-platform builds (linux/amd64, linux/arm64) can run in parallel

### Conditional Execution

Skip unnecessary work:

- **Path filters**: Only run frontend tests when frontend code changes
- **Skip patterns**: `[skip ci]` in commit message for docs-only changes
- **Branch filters**: Only deploy from default branch
- **Changed file detection**: Use tools like `dorny/paths-filter` or `tj-actions/changed-files`

### Artifact Management

- Upload build artifacts for downstream jobs instead of rebuilding
- Set retention policies to control storage costs
- Use artifact checksums to verify integrity across jobs

## Platform-Specific Patterns

Detailed patterns and examples are in the reference documents:

- `references/github-actions-patterns.md` -- Reusable workflows, caching, matrix builds, environment protection
- `references/deployment-strategies.md` -- Rolling, blue-green, canary, feature flags, preview environments
- `references/rollback-procedures.md` -- Platform-specific rollback, post-rollback checklist, when not to rollback

## Pipeline Health Checks

Use `scripts/check_pipeline_health.sh` to audit an existing pipeline configuration for common issues. It checks for:

- Detected CI system and config files
- Referenced scripts that may not exist
- Hardcoded secrets or tokens in pipeline files
- Dockerfile best practices
- Missing lockfiles or .gitignore

## Gotchas

### Secrets

Never hardcode secrets in pipeline files. Use the platform's secret store (GitHub Secrets, CircleCI Contexts, etc.). Verify that every referenced secret actually exists in the target environment before merging. Use OIDC federation for cloud providers instead of long-lived credentials where possible.

### Branch Protection

Pipeline changes on the default branch may require admin review. Always test pipeline changes in a feature branch first. Be aware that some CI platforms only read workflow files from the default branch for certain trigger types.

### Build Matrix Explosion

A matrix of 3 OS versions x 3 runtime versions = 9 jobs. Constrain matrices to what you actually deploy. Use `include`/`exclude` to target specific combinations. Consider running the full matrix only on release branches.

### Docker Cache Invalidation

Order Dockerfile instructions from least to most frequently changing. Copy `package.json` AND the lockfile before running `npm install`. Source code copies should come after dependency installation. Use `.dockerignore` to exclude `node_modules`, `.git`, and test fixtures.

### Flaky Tests in CI

Investigate environment differences before adding retry logic. Common causes: timing-dependent assertions, shared test state, missing environment variables, DNS resolution differences, file system ordering. Fix the root cause -- retries mask bugs.

### CI Cost Management

GitHub Actions minutes are finite on private repos. Use path filters to skip unnecessary runs. Cancel in-progress runs when a new commit is pushed to the same branch. Use self-hosted runners for heavy workloads. Monitor usage regularly.

### Timeout Defaults

Set explicit timeouts on every job and long-running step. Platform defaults (6 hours on GitHub Actions) are far too generous. A hanging build that consumes 6 hours of compute is expensive and blocks the pipeline. Typical timeouts: build (15 min), unit tests (10 min), e2e tests (20 min), deploy (10 min).

### Environment Parity

CI environments differ from local: different OS, different file system (case sensitivity), different network access, different available tools. Pin tool versions explicitly. Use Docker for reproducibility. Document required environment variables.
