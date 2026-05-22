---
name: frappe-testing-cicd
description: >
  Use when setting up CI/CD pipelines for Frappe apps, configuring GitHub Actions test workflows, or adding linting and security scanning.
  Prevents broken CI from incorrect test matrix configuration, missing MariaDB/Redis services, and uncaught code quality issues.
  Covers GitHub Actions workflows, test matrix (Python/Node versions), semgrep rules, pre-commit hooks, linting (ruff, eslint), CI test environment setup.
  Keywords: CI/CD, GitHub Actions, test matrix, semgrep, pre-commit, linting, ruff, eslint, continuous integration.
license: MIT
compatibility: "Claude Code, Claude.ai Projects, Claude API. Frappe v14-v16."
metadata:
  author: OpenAEC-Foundation
  version: "2.0"
---

# CI/CD Pipelines

## Quick Reference

| Task | Tool / File |
|------|------------|
| Install pre-commit hooks | `pre-commit install --hook-type pre-commit --hook-type commit-msg` |
| Run all pre-commit checks | `pre-commit run --all-files` |
| Run linter | `ruff check .` |
| Run formatter | `ruff format .` |
| Run ESLint | `npx eslint "**/*.js" --quiet` |
| Run tests in CI | `bench --site test_site run-tests --app myapp` |
| Run parallel tests | `bench --site test_site run-parallel-tests --total-builds 2 --build-number 0` |
| Generate coverage | `coverage run -m pytest && coverage xml` |
| Generate JUnit XML | `bench --site test_site run-tests --junit-xml-output report.xml` |

## Decision Tree: CI/CD Setup

```
Setting up CI for a Frappe app?
├─ Start with GitHub Actions workflow
│   ├─ ALWAYS include MariaDB + Redis services
│   ├─ ALWAYS use test matrix for Python versions
│   └─ Optionally add PostgreSQL for dual-DB support
├─ Add pre-commit hooks
│   ├─ ALWAYS include ruff (Python linting + formatting)
│   ├─ ALWAYS include eslint + prettier (JS/Vue)
│   └─ Add commitlint for conventional commits
├─ Add security scanning?
│   └─ YES → Add semgrep with Frappe-specific rules
└─ Need release automation?
    └─ YES → Add tag-based release workflow
```

## GitHub Actions Workflow for Frappe Apps

### Standard Server Test Workflow

```yaml
name: Server Tests
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

concurrency:
  group: server-tests-${{ github.ref }}
  cancel-in-progress: true

jobs:
  test:
    runs-on: ubuntu-latest
    timeout-minutes: 60

    strategy:
      fail-fast: false
      matrix:
        python-version: ["3.11", "3.12"]
        db: ["mariadb"]

    services:
      mariadb:
        image: mariadb:11.4
        ports:
          - 3306:3306
        env:
          MARIADB_ROOT_PASSWORD: db_root
        options: >-
          --health-cmd="healthcheck.sh --connect --innodb_initialized"
          --health-interval=5s
          --health-timeout=5s
          --health-retries=10

      redis-cache:
        image: redis:alpine
        ports:
          - 13000:6379
      redis-queue:
        image: redis:alpine
        ports:
          - 11000:6379

    steps:
      - name: Checkout frappe
        uses: actions/checkout@v4
        with:
          repository: frappe/frappe
          path: frappe-bench/apps/frappe

      - name: Checkout app
        uses: actions/checkout@v4
        with:
          path: frappe-bench/apps/myapp

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}

      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: 20

      - name: Install bench
        run: pip install frappe-bench

      - name: Init bench
        working-directory: frappe-bench
        run: |
          bench init --skip-assets --skip-redis-config-generation .
          bench set-config -g db_root_password db_root
          bench set-config -g redis_cache redis://localhost:13000
          bench set-config -g redis_queue redis://localhost:11000

      - name: Install app
        working-directory: frappe-bench
        run: |
          bench get-app --skip-assets myapp ./apps/myapp
          bench setup requirements --dev
          bench new-site test_site \
            --db-root-password db_root \
            --admin-password admin \
            --no-mariadb-socket
          bench --site test_site install-app myapp
          bench build --apps myapp

      - name: Run tests
        working-directory: frappe-bench
        run: bench --site test_site run-tests --app myapp --failfast

      - name: Upload coverage
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: coverage-${{ matrix.python-version }}-${{ matrix.db }}
          path: frappe-bench/sites/coverage.xml
```

### PostgreSQL Support (Additional Matrix Entry)

```yaml
    strategy:
      matrix:
        include:
          - python-version: "3.12"
            db: "postgres"

    services:
      postgres:
        image: postgres:16
        ports:
          - 5432:5432
        env:
          POSTGRES_PASSWORD: db_root
        options: >-
          --health-cmd pg_isready
          --health-interval=10s
          --health-timeout=5s
          --health-retries=5
```

When using PostgreSQL, change the `bench new-site` command:
```bash
bench new-site test_site \
  --db-type postgres \
  --db-root-password db_root \
  --admin-password admin
```

## Pre-Commit Configuration

### Minimal .pre-commit-config.yaml for Frappe Apps

```yaml
exclude: "node_modules|.git"
default_stages: [pre-commit]
fail_fast: false

repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: trailing-whitespace
        files: "myapp.*"
        exclude: ".*json$|.*txt$|.*csv$|.*md$|.*svg$"
      - id: check-merge-conflict
      - id: check-ast
      - id: check-json
      - id: check-toml
      - id: check-yaml
      - id: debug-statements

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.8.0
    hooks:
      - id: ruff
        args: [--select=I, --fix]
        name: ruff (import sorter)
      - id: ruff
        name: ruff (linter)
      - id: ruff-format
        name: ruff (formatter)

  - repo: https://github.com/pre-commit/mirrors-prettier
    rev: v2.7.1
    hooks:
      - id: prettier
        types_or: [javascript, vue, scss]
        exclude: ".*dist.*|node_modules"

  - repo: https://github.com/pre-commit/mirrors-eslint
    rev: v8.44.0
    hooks:
      - id: eslint
        types: [javascript]
        args: [--quiet]
        exclude: ".*dist.*|node_modules"

  - repo: https://github.com/alessandrojcm/commitlint-pre-commit-hook
    rev: v9.16.0
    hooks:
      - id: commitlint
        stages: [commit-msg]
        additional_dependencies:
          - conventional-changelog-conventionalcommits
```

ALWAYS run `pre-commit install --hook-type pre-commit --hook-type commit-msg` after cloning.

## Ruff Configuration (pyproject.toml)

```toml
[tool.ruff]
line-length = 110
target-version = "py311"

[tool.ruff.lint]
select = [
    "F",   # Pyflakes
    "E",   # pycodestyle errors
    "W",   # pycodestyle warnings
    "I",   # isort
    "UP",  # pyupgrade
    "B",   # flake8-bugbear
    "RUF", # Ruff-specific rules
]
ignore = [
    "E501",  # line too long (handled by formatter)
    "F401",  # unused import (common in __init__.py)
    "F403",  # wildcard import (Frappe convention)
    "F405",  # undefined from wildcard (Frappe convention)
    "E402",  # module-level import order (Frappe convention)
]

[tool.ruff.format]
quote-style = "double"
indent-style = "tab"
docstring-code-format = true

[tool.ruff.lint.per-file-ignores]
# Ignore in auto-generated boilerplate
"**/doctype/**/boilerplate/**" = ["ALL"]
```

**Rules**:
- ALWAYS use `indent-style = "tab"` for Frappe projects — this is the framework convention
- ALWAYS ignore F401/F403/F405 — Frappe uses wildcard imports by convention
- NEVER set `line-length` below 110 — Frappe standard is 110 characters

## ESLint Configuration

```json
{
    "env": {
        "browser": true,
        "node": true,
        "es2021": true
    },
    "extends": "eslint:recommended",
    "globals": {
        "frappe": "readonly",
        "cur_frm": "readonly",
        "__": "readonly",
        "cur_dialog": "readonly",
        "cur_page": "readonly",
        "cur_list": "readonly"
    },
    "rules": {
        "no-unused-vars": ["warn", { "argsIgnorePattern": "^_" }],
        "no-console": "warn"
    }
}
```

ALWAYS declare Frappe globals (`frappe`, `cur_frm`, `__`, etc.) — otherwise ESLint reports false positives.

## Semgrep Security Rules

```yaml
# .semgrep/frappe-security.yml
rules:
  - id: frappe-sql-injection
    pattern: frappe.db.sql($X.format(...))
    message: "NEVER use .format() in SQL — use parameterized queries"
    severity: ERROR
    languages: [python]

  - id: frappe-raw-sql-concat
    pattern: frappe.db.sql($X + ...)
    message: "NEVER concatenate strings in SQL — use parameterized queries"
    severity: ERROR
    languages: [python]

  - id: frappe-eval-usage
    pattern: eval(...)
    message: "NEVER use eval() — use frappe.safe_eval() instead"
    severity: ERROR
    languages: [python]
```

Add to CI:
```yaml
      - name: Run Semgrep
        uses: returntocorp/semgrep-action@v1
        with:
          config: .semgrep/
```

## Test Coverage

### Setup coverage.py

```ini
# .coveragerc
[run]
source = myapp
omit =
    */test_*.py
    */tests/*
    */setup.py

[report]
exclude_lines =
    pragma: no cover
    if frappe.flags.in_test:
    if TYPE_CHECKING:
```

### CI Coverage Step

```yaml
      - name: Run tests with coverage
        working-directory: frappe-bench
        run: |
          cd apps/myapp
          coverage run -m pytest
          coverage xml -o ../../sites/coverage.xml

      - name: Upload to Codecov
        uses: codecov/codecov-action@v4
        with:
          file: frappe-bench/sites/coverage.xml
          token: ${{ secrets.CODECOV_TOKEN }}
```

## Release Workflow

```yaml
name: Release
on:
  push:
    tags:
      - "v*"

jobs:
  release:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Generate changelog
        id: changelog
        uses: mikepenz/release-changelog-builder-action@v4
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

      - name: Create GitHub Release
        uses: softprops/action-gh-release@v2
        with:
          body: ${{ steps.changelog.outputs.changelog }}
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

## Branch Protection Rules

ALWAYS configure these branch protection rules for `main` and `develop`:

1. **Require status checks**: Server Tests must pass before merging
2. **Require pull request reviews**: At least 1 approval
3. **Require up-to-date branches**: Force rebase before merge
4. **Require linear history**: Enforce squash or rebase merging

Configure via GitHub CLI:
```bash
gh api repos/{owner}/{repo}/branches/main/protection -X PUT \
  -f "required_status_checks[strict]=true" \
  -f "required_status_checks[contexts][]=Server Tests" \
  -f "required_pull_request_reviews[required_approving_review_count]=1"
```

## Common CI Failures and Fixes

| Failure | Cause | Fix |
|---------|-------|-----|
| `MariaDB not ready` | Health check too short | Increase `--health-retries` to 10+ |
| `Redis connection refused` | Wrong port mapping | Verify port mapping matches `bench set-config` |
| `ModuleNotFoundError` | Missing app install | Ensure `bench get-app` and `bench install-app` both run |
| `Site not found` | Missing `bench new-site` | ALWAYS create site before running tests |
| `Permission denied on bench` | pip install location | Use `pip install frappe-bench` without sudo |
| `Assets build failed` | Node version mismatch | Use Node 18 or 20 (NEVER Node 16) |
| `frappe.exceptions.DoesNotExistError` | Missing test fixtures | Ensure `test_records.json` exists for dependent DocTypes |
| `Timeout in parallel tests` | Too many parallel builds | Reduce `--total-builds` or increase `timeout-minutes` |

## See Also

- [references/examples.md](references/examples.md) — Complete workflow examples
- [references/anti-patterns.md](references/anti-patterns.md) — CI/CD mistakes to avoid
- [references/github-actions.md](references/github-actions.md) — Full GitHub Actions reference
- [references/linting.md](references/linting.md) — Linting and formatting deep dive
- [frappe-testing-unit](../frappe-testing-unit/) — Unit and integration testing
