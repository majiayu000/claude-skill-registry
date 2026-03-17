---
name: python-github-actions
description: Complete Python GitHub Actions system. PROACTIVELY activate for: (1) uv-based CI workflows (10-100x faster), (2) Matrix testing across Python versions, (3) Dependency caching with setup-uv, (4) Parallel test execution, (5) Reusable workflows, (6) Publishing to PyPI with trusted publishing, (7) Code coverage with codecov, (8) Security scanning. Provides: Workflow templates, caching config, matrix strategies, composite actions. Ensures fast, reliable CI/CD pipelines.
---

## Quick Reference

| Action | Purpose | Speed |
|--------|---------|-------|
| `astral-sh/setup-uv@v4` | Install uv + caching | 10-100x faster |
| `actions/setup-python@v5` | Traditional pip | Baseline |

| uv CI Pattern | Code |
|---------------|------|
| Setup | `uses: astral-sh/setup-uv@v4` with `enable-cache: true` |
| Install Python | `uv python install ${{ matrix.python-version }}` |
| Sync deps | `uv sync --all-extras` |
| Run tests | `uv run pytest` |

| Matrix Strategy | Config |
|-----------------|--------|
| Python versions | `python-version: ["3.11", "3.12", "3.13"]` |
| Operating systems | `os: [ubuntu-latest, windows-latest, macos-latest]` |
| Fail fast | `fail-fast: false` for full coverage |

| Optimization | Technique |
|--------------|-----------|
| Caching | `enable-cache: true` with setup-uv |
| Parallel jobs | Split lint/test/build |
| Concurrency | `cancel-in-progress: true` |
| Path filters | `paths: ["src/**", "tests/**"]` |

## When to Use This Skill

Use for **CI/CD pipelines**:
- Setting up GitHub Actions for Python projects
- Caching dependencies for fast builds
- Matrix testing across Python versions
- Publishing packages to PyPI
- Code coverage and security scanning

**Related skills:**
- For package management: see `python-package-management`
- For testing: see `python-testing`
- For type checking: see `python-type-hints`

---

# Python GitHub Actions Optimization

## Overview

GitHub Actions is the primary CI/CD platform for Python projects. This guide covers best practices for fast, reliable, and efficient Python workflows.

## Quick Start Workflow

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.11", "3.12", "3.13"]

    steps:
      - uses: actions/checkout@v4

      - name: Install uv
        uses: astral-sh/setup-uv@v4

      - name: Set up Python ${{ matrix.python-version }}
        run: uv python install ${{ matrix.python-version }}

      - name: Install dependencies
        run: uv sync --all-extras --dev

      - name: Run linting
        run: uv run ruff check .

      - name: Run type checking
        run: uv run mypy src

      - name: Run tests
        run: uv run pytest --cov
```

## Modern uv-Based Workflow

### Setup with uv

```yaml
name: CI with uv

on:
  push:
    branches: [main]
  pull_request:

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install uv
        uses: astral-sh/setup-uv@v4
        with:
          version: "latest"
          enable-cache: true  # Automatic caching!

      - name: Lint with ruff
        run: |
          uv run ruff check .
          uv run ruff format --check .

  type-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: astral-sh/setup-uv@v4
        with:
          enable-cache: true

      - name: Type check with mypy
        run: uv run mypy src

  test:
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        python-version: ["3.11", "3.12", "3.13"]

    steps:
      - uses: actions/checkout@v4

      - uses: astral-sh/setup-uv@v4
        with:
          enable-cache: true

      - name: Set up Python
        run: uv python install ${{ matrix.python-version }}

      - name: Install dependencies
        run: uv sync --all-extras

      - name: Run tests
        run: uv run pytest -v --cov --cov-report=xml

      - name: Upload coverage
        uses: codecov/codecov-action@v4
        with:
          file: ./coverage.xml
```

### Dependency Caching with uv

```yaml
# uv handles caching automatically with setup-uv
- uses: astral-sh/setup-uv@v4
  with:
    enable-cache: true
    cache-dependency-glob: "uv.lock"

# This caches:
# - Downloaded packages
# - Python installations
# - Virtual environments
```

## Traditional pip-Based Workflow

### Manual Caching Setup

```yaml
name: CI with pip

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: "pip"  # Built-in pip caching
          cache-dependency-path: |
            requirements.txt
            requirements-dev.txt

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install -r requirements-dev.txt

      - name: Run tests
        run: pytest
```

### Advanced Caching

```yaml
- name: Cache pip packages
  uses: actions/cache@v4
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements*.txt') }}
    restore-keys: |
      ${{ runner.os }}-pip-

- name: Cache pre-commit hooks
  uses: actions/cache@v4
  with:
    path: ~/.cache/pre-commit
    key: pre-commit-${{ hashFiles('.pre-commit-config.yaml') }}
```

## Parallel and Matrix Builds

### Efficient Matrix Strategy

```yaml
jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      fail-fast: false  # Don't cancel all on first failure
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        python-version: ["3.11", "3.12", "3.13"]
        exclude:
          # Skip Python 3.13 on Windows (if issues)
          - os: windows-latest
            python-version: "3.13"

    steps:
      - uses: actions/checkout@v4

      - uses: astral-sh/setup-uv@v4
        with:
          enable-cache: true

      - run: uv python install ${{ matrix.python-version }}
      - run: uv sync
      - run: uv run pytest
```

### Split by Test Type

```yaml
jobs:
  unit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v4
      - run: uv sync
      - run: uv run pytest tests/unit -v

  integration:
    runs-on: ubuntu-latest
    needs: unit  # Run after unit tests pass
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v4
      - run: uv sync
      - run: uv run pytest tests/integration -v

  e2e:
    runs-on: ubuntu-latest
    needs: integration
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v4
      - run: uv sync
      - run: uv run pytest tests/e2e -v
```

## Reusable Workflows

### Composite Action

```yaml
# .github/actions/python-setup/action.yml
name: Python Setup
description: Set up Python environment with uv

inputs:
  python-version:
    description: Python version to use
    default: "3.12"

runs:
  using: composite
  steps:
    - name: Install uv
      uses: astral-sh/setup-uv@v4
      with:
        enable-cache: true

    - name: Set up Python
      shell: bash
      run: uv python install ${{ inputs.python-version }}

    - name: Install dependencies
      shell: bash
      run: uv sync --all-extras
```

```yaml
# .github/workflows/ci.yml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: ./.github/actions/python-setup
        with:
          python-version: "3.12"
      - run: uv run pytest
```

### Reusable Workflow

```yaml
# .github/workflows/python-test.yml
name: Reusable Python Test

on:
  workflow_call:
    inputs:
      python-version:
        type: string
        default: "3.12"

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: astral-sh/setup-uv@v4
        with:
          enable-cache: true

      - run: uv python install ${{ inputs.python-version }}
      - run: uv sync
      - run: uv run pytest
```

```yaml
# .github/workflows/ci.yml
jobs:
  test-3-11:
    uses: ./.github/workflows/python-test.yml
    with:
      python-version: "3.11"

  test-3-12:
    uses: ./.github/workflows/python-test.yml
    with:
      python-version: "3.12"
```

## YAML Anchors (2025 Feature)

```yaml
# Reduce repetition with anchors
name: CI

on: [push, pull_request]

# Define anchor
x-common-steps: &common-steps
  - uses: actions/checkout@v4
  - uses: astral-sh/setup-uv@v4
    with:
      enable-cache: true

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      *common-steps  # Reference anchor
      - run: uv run ruff check .

  test:
    runs-on: ubuntu-latest
    steps:
      *common-steps  # Reuse same steps
      - run: uv sync
      - run: uv run pytest
```

## Publishing to PyPI

```yaml
name: Publish

on:
  release:
    types: [published]

jobs:
  publish:
    runs-on: ubuntu-latest
    permissions:
      id-token: write  # Required for trusted publishing

    steps:
      - uses: actions/checkout@v4

      - uses: astral-sh/setup-uv@v4

      - name: Build package
        run: uv build

      - name: Publish to PyPI
        uses: pypa/gh-action-pypi-publish@release/v1
        # No password needed with trusted publishing!
```

## Comprehensive CI/CD Example

```yaml
name: CI/CD

on:
  push:
    branches: [main]
  pull_request:
  release:
    types: [published]

env:
  PYTHON_VERSION: "3.12"

jobs:
  # ========== Quality Checks ==========
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v4
        with:
          enable-cache: true
      - run: uv sync --only-dev
      - run: uv run ruff check .
      - run: uv run ruff format --check .

  type-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v4
        with:
          enable-cache: true
      - run: uv sync
      - run: uv run mypy src

  # ========== Tests ==========
  test:
    needs: [lint, type-check]
    runs-on: ${{ matrix.os }}
    strategy:
      fail-fast: false
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        python-version: ["3.11", "3.12", "3.13"]

    steps:
      - uses: actions/checkout@v4

      - uses: astral-sh/setup-uv@v4
        with:
          enable-cache: true

      - run: uv python install ${{ matrix.python-version }}
      - run: uv sync

      - name: Run tests
        run: uv run pytest -v --cov --cov-report=xml

      - name: Upload coverage
        if: matrix.os == 'ubuntu-latest' && matrix.python-version == '3.12'
        uses: codecov/codecov-action@v4
        with:
          file: ./coverage.xml
          fail_ci_if_error: true

  # ========== Security ==========
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v4
      - run: uv sync
      - run: uv run pip-audit  # Check for known vulnerabilities
      - run: uv run bandit -r src  # Security linting

  # ========== Build ==========
  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v4

      - name: Build package
        run: uv build

      - name: Upload artifact
        uses: actions/upload-artifact@v4
        with:
          name: dist
          path: dist/

  # ========== Publish ==========
  publish:
    if: github.event_name == 'release'
    needs: build
    runs-on: ubuntu-latest
    permissions:
      id-token: write

    steps:
      - uses: actions/download-artifact@v4
        with:
          name: dist
          path: dist/

      - name: Publish to PyPI
        uses: pypa/gh-action-pypi-publish@release/v1
```

## Performance Optimization Tips

### 1. Use uv for Fastest Installs

```yaml
# uv is 10-100x faster than pip
- uses: astral-sh/setup-uv@v4
  with:
    enable-cache: true
```

### 2. Fail Fast (or Not)

```yaml
strategy:
  fail-fast: true   # Cancel all on first failure (faster feedback)
  fail-fast: false  # Run all (complete coverage)
```

### 3. Job Dependencies

```yaml
jobs:
  lint:
    runs-on: ubuntu-latest

  test:
    needs: lint  # Only run if lint passes
    runs-on: ubuntu-latest
```

### 4. Concurrency Control

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true  # Cancel previous runs on same branch
```

### 5. Skip Unnecessary Runs

```yaml
on:
  push:
    paths:
      - "src/**"
      - "tests/**"
      - "pyproject.toml"
    paths-ignore:
      - "**.md"
      - "docs/**"
```

### 6. ARM64 Runners (2025)

```yaml
# Free ARM64 runners for public repos
runs-on: ubuntu-24.04-arm64  # Faster for ARM-native workloads
```

## Common Issues & Solutions

### Issue: Slow pip install

```yaml
# Solution: Use uv
- uses: astral-sh/setup-uv@v4
  with:
    enable-cache: true
```

### Issue: Cache not working

```yaml
# Solution: Verify cache key matches dependency files
- uses: actions/cache@v4
  with:
    path: ~/.cache
    key: deps-${{ hashFiles('uv.lock', 'pyproject.toml') }}
```

### Issue: Python version not found

```yaml
# Solution: Use uv to manage Python versions
- uses: astral-sh/setup-uv@v4
- run: uv python install 3.13  # Works even for newest versions
```

### Issue: Tests fail on Windows

```yaml
# Solution: Normalize line endings
- uses: actions/checkout@v4
  with:
    # Prevent Windows line ending issues
    persist-credentials: false

# Or in .gitattributes
# *.py text eol=lf
```
