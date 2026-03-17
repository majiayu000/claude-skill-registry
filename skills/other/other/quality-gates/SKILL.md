---
name: quality-gates
model: fast
category: testing
description: Quality checkpoints at every development stage — pre-commit through post-deploy — with configuration examples, threshold tables, bypass protocols, and CI/CD integration. Use when setting up quality automation, configuring CI pipelines, establishing coverage thresholds, or defining deployment requirements.
version: 1.0
---

# Quality Gates

Enforce quality checkpoints at every stage of the development lifecycle. Each gate defines what is checked, when it runs, and whether it blocks progression.


## Installation

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install quality-gates
```


---

## When to Use

- **Before committing** — catch lint errors, formatting issues, type errors, and secrets before they enter history
- **Before merging** — ensure full test suites pass, coverage thresholds are met, and code has been reviewed
- **Before deploying** — validate integration tests, security scans, and performance budgets in staging
- **During code review** — verify that all automated gates have passed and manual review criteria are satisfied
- **After deploying** — monitor health checks, error rates, and performance baselines

---

## Gate Overview

| Gate | When | Checks | Blocking? |
|------|------|--------|-----------|
| Pre-commit | `git commit` | Lint, format, type-check, secrets scan | Yes |
| Pre-push | `git push` | Unit tests, build verification | Yes |
| Pre-merge | PR/MR approval | Full test suite, code review, coverage threshold | Yes |
| Pre-deploy (staging) | Deploy to staging | Integration tests, smoke tests, security scan | Yes |
| Pre-deploy (production) | Deploy to production | Staging verification, load test, rollback plan | Yes |
| Post-deploy | After production deploy | Health checks, error rate monitoring, perf baselines | Alerting |

---

## Pre-commit Setup

### Husky + lint-staged (Node.js)

```json
{
  "lint-staged": {
    "*.{js,ts,tsx}": ["eslint --fix", "prettier --write"],
    "*.{json,md,yaml}": ["prettier --write"]
  }
}
```

```bash
npx husky init
echo "npx lint-staged" > .husky/pre-commit
```

### Pre-commit framework (Python)

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.6.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.11.0
    hooks:
      - id: mypy
```

### Secrets Scanning (pre-commit hook)

```bash
#!/bin/sh
# .git/hooks/pre-commit
gitleaks protect --staged --verbose
if [ $? -ne 0 ]; then
  echo "Secrets detected. Commit blocked."
  exit 1
fi
```

---

## CI/CD Gate Configuration

### GitHub Actions

```yaml
name: Quality Gates
on:
  pull_request:
    branches: [main]

jobs:
  lint-and-typecheck:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm ci
      - run: npm run lint
      - run: npm run typecheck

  unit-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm ci
      - run: npm test -- --coverage
      - name: Check coverage threshold
        run: |
          COVERAGE=$(jq '.total.lines.pct' coverage/coverage-summary.json)
          if (( $(echo "$COVERAGE < 80" | bc -l) )); then
            echo "Coverage $COVERAGE% is below 80% threshold"
            exit 1
          fi

  security-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm audit --audit-level=high
      - uses: gitleaks/gitleaks-action@v2

  build:
    needs: [lint-and-typecheck, unit-tests, security-scan]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm ci
      - run: npm run build
```

Set these as **required status checks** in branch protection rules so PRs cannot merge until all gates pass.

---

## Coverage Gates

| Type | Minimum Threshold | Notes |
|------|-------------------|-------|
| Unit tests | 80% line coverage | Per-file and aggregate |
| Integration tests | 60% of integration points | API endpoints, DB queries |
| E2E tests | 100% of critical paths | Auth, checkout, core workflows |
| No decrease rule | 0% regression allowed | New code must not lower overall coverage |

### Enforcing Thresholds

```json
// jest.config.js or vitest.config.ts
{
  "coverageThreshold": {
    "global": {
      "branches": 75,
      "functions": 80,
      "lines": 80,
      "statements": 80
    }
  }
}
```

For the **no decrease rule**, compare coverage against the base branch in CI and fail if the delta is negative.

---

## Security Gates

### Dependency Scanning

| Ecosystem | Tool | Command |
|-----------|------|---------|
| Node.js | npm audit | `npm audit --audit-level=high` |
| Python | pip-audit | `pip-audit --strict` |
| Rust | cargo audit | `cargo audit` |
| Go | govulncheck | `govulncheck ./...` |
| Universal | Trivy | `trivy fs --severity HIGH,CRITICAL .` |

### Secret Detection

| Tool | Use Case | Command |
|------|----------|---------|
| gitleaks | Pre-commit and CI | `gitleaks protect --staged` |
| TruffleHog | Deep history scan | `trufflehog git file://. --only-verified` |
| detect-secrets | Baseline-aware scanning | `detect-secrets scan --baseline .secrets.baseline` |

---

## Performance Gates

### Bundle Size Budgets

```json
{
  "bundlesize": [
    { "path": "dist/main.*.js", "maxSize": "150 kB" },
    { "path": "dist/vendor.*.js", "maxSize": "250 kB" },
    { "path": "dist/**/*.css", "maxSize": "30 kB" }
  ]
}
```

### Lighthouse CI Thresholds

```json
{
  "ci": {
    "assert": {
      "assertions": {
        "categories:performance": ["error", { "minScore": 0.9 }],
        "categories:accessibility": ["error", { "minScore": 0.95 }],
        "categories:best-practices": ["error", { "minScore": 0.9 }],
        "first-contentful-paint": ["error", { "maxNumericValue": 2000 }],
        "largest-contentful-paint": ["error", { "maxNumericValue": 2500 }],
        "cumulative-layout-shift": ["error", { "maxNumericValue": 0.1 }]
      }
    }
  }
}
```

### API Response Time Limits

| Endpoint Type | P50 | P95 | P99 |
|---------------|-----|-----|-----|
| Read (GET) | < 100ms | < 300ms | < 500ms |
| Write (POST/PUT) | < 200ms | < 500ms | < 1000ms |
| Search/aggregate | < 300ms | < 800ms | < 2000ms |
| Health check | < 50ms | < 100ms | < 200ms |

Enforce via load testing tools (k6, Artillery) in CI with pass/fail thresholds.

---

## Review Gates

### Required Approvals

| Change Scope | Approvals Required |
|--------------|--------------------|
| Standard code changes | 1 approval minimum |
| Infrastructure, auth, payments, data models | 2 approvals |
| Dependency updates, cryptographic changes | Security team approval |

### CODEOWNERS

```text
# .github/CODEOWNERS
*                    @team/engineering
/infra/              @team/platform
/src/auth/           @team/security
/src/payments/       @team/payments @team/security
*.sql                @team/data-engineering
Dockerfile           @team/platform
```

---

## Gate Bypass Protocol

### When Bypass Is Acceptable

- Hotfixes for production incidents with active user impact
- Trivial changes (typos, comments) where automated checks are overkill
- Dependency updates that break CI due to upstream issues (not your code)

### Required Documentation for Every Bypass

1. **Reason** — why the gate cannot pass right now
2. **Risk assessment** — what could go wrong by skipping
3. **Follow-up ticket** — link to an issue that tracks resolving the bypass
4. **Approver** — name of the senior engineer or lead who authorized the bypass

---

## NEVER Do

1. **NEVER disable gates permanently** — fix the root cause, don't remove the guardrail
2. **NEVER commit secrets** — even to "test" branches; git history is forever
3. **NEVER skip tests to unblock a deploy** — if tests fail, the code is not ready
4. **NEVER merge with failing required checks** — admin merge bypasses erode team trust
5. **NEVER set coverage thresholds to 0%** — even a low threshold is better than none
6. **NEVER bypass security scans for speed** — vulnerabilities in production cost far more than CI minutes
7. **NEVER rely solely on post-deploy gates** — catching issues after users are impacted is damage control, not quality
8. **NEVER treat alerting gates as optional** — post-deploy monitoring exists because pre-deploy gates cannot catch everything; ignoring alerts defeats the purpose
