---
name: api-ci-cd-github-actions
description: GitHub Actions, pipelines, deployment
---

# CI/CD Pipelines

> **Quick Guide:** GitHub Actions with Bun 1.2.2 for CI. Turborepo affected detection for monorepo optimization. Vercel remote cache (free). Quality gates: lint + type-check + test + build + coverage. Multi-environment deployments (preview/staging/prod). Secret scanning and dependency audits.

---

<critical_requirements>

## ⚠️ CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST use Turborepo affected detection `--filter=...[origin/main]` for PR builds - NEVER run full test suite on PRs)**

**(You MUST cache Bun dependencies `~/.bun/install/cache/` and Turborepo `.turbo/` - CI without caching wastes 70% of runtime)**

**(You MUST use named constants for all timeouts, retry counts, and thresholds - NO magic numbers in CI configs)**

**(You MUST implement quality gates (lint + type-check + test + build) as required status checks - block merge on failures)**

**(You MUST use GitHub Secrets for sensitive data and rotate them quarterly - NEVER commit secrets to repository)**

</critical_requirements>

---

**Detailed Resources:**

- For code examples, see [examples/](examples/) directory:
  - [core.md](examples/core.md) - Pipeline config, jobs, caching, reusable workflows, composite actions, matrix builds
  - [testing.md](examples/testing.md) - Affected detection, quality gates
  - [caching.md](examples/caching.md) - Remote caching, Turborepo
  - [security.md](examples/security.md) - OIDC auth, secrets rotation
  - [deployment.md](examples/deployment.md) - Multi-env, rollback
  - [monitoring.md](monitoring.md) - Datadog, GitHub Insights
- For decision frameworks and anti-patterns, see [reference.md](reference.md)

---

**Auto-detection:** GitHub Actions, CI/CD pipelines, Turborepo affected detection, Vercel remote cache, deployment automation, quality gates, OIDC authentication, secret rotation, CI monitoring, artifact attestations, SLSA provenance, supply chain security, reusable workflows, composite actions, matrix builds, workflow_call

**When to use:**

- Setting up GitHub Actions workflows with Bun and Turborepo
- Implementing Turborepo affected detection for faster PR builds
- Configuring Vercel remote cache for team sharing
- Setting up quality gates and branch protection rules
- Implementing OIDC authentication for AWS/GCP deployments
- Setting up automated secrets rotation
- Monitoring CI/CD performance and reliability
- Adding artifact attestations for supply chain security (SLSA compliance)

**When NOT to use:**

- Single-package projects (simpler CI tools like GitHub Actions without Turborepo may suffice)
- No monorepo architecture (standard CI pipelines without affected detection)
- Real-time deployment requirements (use feature flags + trunk-based development instead)
- Simple static sites with no build step (direct hosting without CI/CD)

**Key patterns covered:**

- GitHub Actions with Bun 1.2.2 and Turborepo caching
- Affected detection (turbo run test --filter=...[origin/main] for PRs)
- Vercel remote cache (free, zero-config for Turborepo)
- Quality gates (lint, type-check, test, build - parallel jobs with dependencies)
- OIDC authentication (AWS, GCP - no static credentials; Vercel uses project tokens)
- Automated secrets rotation (HashiCorp Vault, AWS Secrets Manager)
- CI monitoring (Datadog CI Visibility, GitHub Insights)
- Artifact attestations (SLSA v1.0 Build Level 2 provenance for supply chain security)
- Reusable workflows (workflow_call trigger, up to 10 nested levels)
- Composite actions (using: composite, shared setup logic)
- Matrix builds (include/exclude, fail-fast, dynamic matrices)

---

<philosophy>

## Philosophy

CI/CD pipelines automate testing, building, and deployment to ensure code quality and fast feedback loops. In a Turborepo monorepo, intelligent caching and affected detection are critical for maintaining fast CI times as the codebase grows.

**When to use GitHub Actions with Turborepo:**

- Monorepo architecture with multiple packages/apps
- Need for shared build cache across team and CI
- Fast PR feedback (< 5 minutes) with affected detection
- Multi-environment deployments (preview/staging/production)
- Team collaboration with automated quality gates

**When NOT to use:**

- Single-package projects (simpler CI tools may suffice)
- No monorepo (standard CI pipelines without Turborepo)
- Real-time deployment requirements (use feature flags + trunk-based development)

This document outlines **recommended best practices** for CI/CD pipelines in a Turborepo monorepo using Bun, following CLAUDE.md conventions (kebab-case files, named exports, named constants).

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Pipeline Configuration

GitHub Actions with Bun 1.2.2 is the recommended CI platform for this stack.

#### Constants

```typescript
// ci-config.ts - Shared CI configuration constants
export const BUN_VERSION = "1.2.2";
export const NODE_ENV_PRODUCTION = "production";
export const CACHE_RETENTION_DAYS = 30;
export const ARTIFACT_RETENTION_DAYS = 30;
export const MIN_COVERAGE_THRESHOLD = 80;
export const DEPLOY_APPROVAL_TIMEOUT_MINUTES = 60;
```

#### Workflow Structure

**Recommended workflows:**

- `ci.yml` - Continuous integration (lint, test, type-check, build)
- `preview.yml` - Preview deployments for pull requests
- `deploy.yml` - Production deployment from main branch
- `release.yml` - Semantic versioning and changelog generation
- `dependabot.yml` - Automated dependency updates (optional)
- `security.yml` - Secret scanning and vulnerability checks

#### Caching Configuration

**What to cache:**

```typescript
// ci-cache-config.ts
export const CACHE_PATHS = {
  BUN_DEPENDENCIES: "~/.bun/install/cache/",
  NODE_MODULES: "node_modules",
  TURBOREPO_CACHE: ".turbo/",
  NEXT_CACHE: ".next/cache/",
  TYPESCRIPT_BUILD_INFO: "tsconfig.tsbuildinfo",
} as const;
```

See [examples/core.md](examples/core.md) for complete workflow examples.

---

### Pattern 2: Affected Detection

Only test and build changed packages in monorepo using Turborepo filters.

#### Filter Syntax

```typescript
// turbo-filter-config.ts - Filter patterns for different scenarios
export const TURBO_FILTERS = {
  AFFECTED_SINCE_MAIN: "--filter=...[origin/main]",
  AFFECTED_APPS_ONLY: "--filter=./apps/*...[origin/main]",
  SPECIFIC_PACKAGE_WITH_DEPS: "--filter=@repo/ui...",
  SPECIFIC_PACKAGE_WITH_DEPENDENTS: "--filter=...@repo/api",
} as const;
```

**Key principle:** PRs use affected detection for fast feedback (< 5 min), main branch runs full test suite for comprehensive validation.

See [examples/testing.md](examples/testing.md) for PR vs main branch workflow examples.

---

### Pattern 3: Quality Gates

Automated checks that must pass before merge.

#### Required Checks Configuration

```typescript
// quality-gate-config.ts
export const QUALITY_GATES = {
  COVERAGE_THRESHOLD_STATEMENTS: 80,
  COVERAGE_THRESHOLD_BRANCHES: 75,
  COVERAGE_THRESHOLD_FUNCTIONS: 80,
  COVERAGE_THRESHOLD_LINES: 80,
  MAX_BUNDLE_SIZE_KB: 500,
  LINT_MAX_WARNINGS: 0,
} as const;
```

**Quality gate order:**

1. Linting (code style and static analysis)
2. Type checking (TypeScript errors)
3. Tests with coverage (functionality validation)
4. Build verification (production build succeeds)
5. Bundle size check (performance regression prevention)
6. Security audit (dependency vulnerabilities)

See [examples/testing.md](examples/testing.md) for comprehensive quality gate workflow.

</patterns>

---

<performance>

## Performance Optimization

**Goal: CI runtime < 5 minutes for PR builds**

### Parallelization Strategies

Run independent jobs in parallel to minimize total CI time:

```typescript
// ci-performance-config.ts
export const CI_PERFORMANCE_CONFIG = {
  TARGET_PR_DURATION_SECONDS: 300, // 5 minutes
  TARGET_MAIN_DURATION_SECONDS: 600, // 10 minutes
  TARGET_CACHE_HIT_RATE: 0.8, // 80%
  MAX_PARALLEL_JOBS: 10,
} as const;
```

**Parallelization techniques:**

- Separate install job, parallel lint/test/type-check jobs (saves 40% time)
- Matrix builds for multiple OS/versions (only on main, not PRs)
- Split test suites (unit || integration || e2e)
- Use GitHub's `concurrency` to cancel outdated runs

### Monitoring Targets

Track these metrics to ensure CI stays fast:

- **CI runtime:** < 5 min (PR), < 10 min (main)
- **Cache hit rate:** > 80% (Turborepo remote cache)
- **Failure rate:** < 5% (excluding flaky tests)
- **Time to deploy:** < 10 min (commit to production)

</performance>

---

<integration>

## Integration Guide

CI/CD pipelines integrate with multiple parts of the stack:

**Works with:**

- **Turborepo**: Affected detection, remote caching, parallel task execution
- **Bun**: Fast package installation, test runner, build tool
- **GitHub Actions**: Workflow orchestration, secret management, environments
- **Vercel**: Preview deployments, production hosting, remote cache provider
- **Testing libraries**: Vitest/Jest run via `turbo run test`

**Authentication integrations:**

- **AWS**: OIDC for S3, CloudFront, Lambda deployments
- **Vercel**: Project tokens (OIDC not yet supported for GitHub Actions)
- **Datadog**: API keys for CI monitoring
- **HashiCorp Vault**: JWT authentication for secret retrieval

</integration>

---

<critical_reminders>

## ⚠️ CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md**

**(You MUST use Turborepo affected detection `--filter=...[origin/main]` for PR builds - NEVER run full test suite on PRs)**

**(You MUST cache Bun dependencies `~/.bun/install/cache/` and Turborepo `.turbo/` - CI without caching wastes 70% of runtime)**

**(You MUST use named constants for all timeouts, retry counts, and thresholds - NO magic numbers in CI configs)**

**(You MUST implement quality gates (lint + type-check + test + build) as required status checks - block merge on failures)**

**(You MUST use GitHub Secrets for sensitive data and rotate them quarterly - NEVER commit secrets to repository)**

**Failure to follow these rules will result in slow CI (10+ min), security vulnerabilities (leaked credentials), and broken builds (missing quality gates).**

</critical_reminders>
