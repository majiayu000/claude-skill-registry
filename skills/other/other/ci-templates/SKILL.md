---
name: ci-templates
description: "Use when setting up CI/CD pipelines. Teaches pipeline design principles and references platform-specific templates."
---

# CI/CD Templates

Principles for designing fast, reliable CI/CD pipelines. Platform-specific templates in `docs/ci-templates/`.

## When to Use

- Setting up a new CI/CD pipeline
- Optimizing slow pipelines
- Adding security scanning
- Migrating between CI platforms

## Core Principles

### 1. Fail Fast
Run quick checks first. Don't waste 10 minutes building if linting fails in 10 seconds.

```
Stage Order:
1. Lint/Format (seconds)
2. Type Check (seconds)
3. Unit Tests (minutes)
4. Integration Tests (minutes)
5. Build (minutes)
6. E2E Tests (minutes)
7. Deploy (varies)
```

### 2. Cache Dependencies
Never re-download what you already have.

| Framework | Cache Path |
|-----------|------------|
| PHP/Composer | `vendor/` |
| Node.js | `node_modules/` |
| Python | `.venv/` or `~/.cache/pip` |

### 3. Parallelize Independent Jobs
Jobs that don't depend on each other should run simultaneously.

```
✓ Good: lint + unit-tests + type-check (parallel)
✗ Bad: lint → unit-tests → type-check (sequential)
```

### 4. Use Artifacts for Handoffs
Don't rebuild between stages. Pass build artifacts.

### 5. Default to Public Images
Use Docker Hub, GitHub Container Registry, or official images by default. Custom registries are an optimization, not a requirement.

## Platform Support

| Platform | Template Location | Config File |
|----------|-------------------|-------------|
| GitLab CI | `docs/ci-templates/gitlab/` | `.gitlab-ci.yml` |
| GitHub Actions | `docs/ci-templates/github/` | `.github/workflows/*.yml` |

## Image Strategy

### Option 1: Public Images (Recommended Start)

No setup required. Works everywhere.

| Framework | Image | Notes |
|-----------|-------|-------|
| PHP | `php:8.3-cli` | Add extensions in `before_script` |
| Python | `python:3.12` | Add deps in `before_script` |
| Node | `node:20` | Works out of the box |
| Playwright | `mcr.microsoft.com/playwright:latest` | All browsers included |
| Security | `aquasec/trivy:latest` | Multi-language scanner |

### Option 2: Custom Registry (Optimization)

For faster builds, pre-bake dependencies into custom images.

Configure in `.claude/registry.json`:
```json
{
  "registry": "your-registry.example.com/images",
  "images": {
    "php": { "testing": "php:8.3-testing" },
    "node": { "base": "node:20-base" }
  }
}
```

See `docs/registry-config.md` for building custom images.

## Security Scanning

Always include security scanning. Use `allow_failure: true` initially to avoid blocking deploys while you fix issues.

| Scanner | What It Checks | Image |
|---------|----------------|-------|
| `composer audit` | PHP dependencies | `php:*` |
| `npm audit` | Node dependencies | `node:*` |
| `pip-audit` | Python dependencies | `python:*` |
| Trivy | Everything + containers | `aquasec/trivy` |
| Gitleaks | Secrets in code | `zricethezav/gitleaks` |

## Quick Start

### GitLab CI

```yaml
# .gitlab-ci.yml - minimal working example
stages: [test]

test:
  image: node:20
  script:
    - npm ci
    - npm test
  cache:
    paths: [node_modules/]
```

### GitHub Actions

```yaml
# .github/workflows/test.yml - minimal working example
name: Test
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '20' }
      - run: npm ci
      - run: npm test
```

## Template Reference

Full templates for common stacks:

| Stack | GitLab | GitHub |
|-------|--------|--------|
| Laravel/PHP | `docs/ci-templates/gitlab/laravel.yml` | `docs/ci-templates/github/laravel.yml` |
| Django/Python | `docs/ci-templates/gitlab/django.yml` | `docs/ci-templates/github/django.yml` |
| React/Node | `docs/ci-templates/gitlab/react.yml` | `docs/ci-templates/github/react.yml` |
| Full-Stack | `docs/ci-templates/gitlab/fullstack.yml` | `docs/ci-templates/github/fullstack.yml` |

## Checklist

When setting up a pipeline:

- [ ] Stages ordered by speed (fast first)
- [ ] Dependencies cached
- [ ] Independent jobs parallelized
- [ ] Artifacts passed between stages
- [ ] Security scanning included
- [ ] Works with public images (custom registry optional)

## Common Mistakes

1. **No caching** → Slow builds, wasted bandwidth
2. **Sequential everything** → 20 min pipeline that could be 5 min
3. **Hardcoded registry** → Breaks for contributors
4. **No security scanning** → Vulnerabilities ship to prod
5. **E2E tests blocking** → Flaky tests block all deploys

## Integration

These templates work with:
- `/laravel`, `/python`, `/react` commands
- `/architect security` for security scanning
- `system-architect` skill for infrastructure audits
