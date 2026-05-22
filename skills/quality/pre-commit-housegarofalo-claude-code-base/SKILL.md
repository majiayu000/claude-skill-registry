---
name: pre-commit
description: Configure pre-commit hooks for code quality, linting, formatting, and security checks. Automate code standards with Git hooks. Use for code quality enforcement, automated formatting, or security scanning before commits. Triggers on pre-commit, git hooks, husky, lint-staged.
---

# Pre-commit Hooks

Automate code quality checks with pre-commit hooks.

## Quick Reference

| Tool | Language | Purpose |
|------|----------|---------|
| `pre-commit` | Python | Multi-language hook framework |
| `husky` | JavaScript | Git hooks for Node.js projects |
| `lint-staged` | JavaScript | Run linters on staged files |
| `lefthook` | Go | Fast, polyglot Git hooks |

## 1. Pre-commit (Python Framework)

### Installation

```bash
# Install pre-commit
pip install pre-commit

# Install hooks in repository
pre-commit install

# Install commit-msg hook (for conventional commits)
pre-commit install --hook-type commit-msg
```

### Configuration (.pre-commit-config.yaml)

```yaml
repos:
  # General hooks
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-json
      - id: check-added-large-files
        args: ['--maxkb=500']
      - id: check-merge-conflict
      - id: detect-private-key
      - id: check-case-conflict

  # Python
  - repo: https://github.com/psf/black
    rev: 24.1.1
    hooks:
      - id: black

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.14
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks:
      - id: mypy
        additional_dependencies: [types-requests]

  # JavaScript/TypeScript
  - repo: https://github.com/pre-commit/mirrors-eslint
    rev: v8.56.0
    hooks:
      - id: eslint
        files: \.[jt]sx?$
        types: [file]
        additional_dependencies:
          - eslint@8.56.0
          - typescript
          - '@typescript-eslint/parser'
          - '@typescript-eslint/eslint-plugin'

  - repo: https://github.com/pre-commit/mirrors-prettier
    rev: v4.0.0-alpha.8
    hooks:
      - id: prettier
        types_or: [javascript, jsx, ts, tsx, json, yaml, markdown]

  # Security
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
        args: ['--baseline', '.secrets.baseline']

  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.18.1
    hooks:
      - id: gitleaks

  # Conventional commits
  - repo: https://github.com/compilerla/conventional-pre-commit
    rev: v3.1.0
    hooks:
      - id: conventional-pre-commit
        stages: [commit-msg]

default_language_version:
  python: python3.11
  node: 20.10.0

ci:
  autofix_prs: true
  autoupdate_schedule: weekly
```

### Commands

```bash
# Run on all files
pre-commit run --all-files

# Run specific hook
pre-commit run black --all-files

# Update hooks to latest versions
pre-commit autoupdate

# Skip hooks temporarily
git commit --no-verify -m "message"
# or
SKIP=black,ruff git commit -m "message"

# Clean cache
pre-commit clean
pre-commit gc
```

## 2. Husky + lint-staged (Node.js)

### Installation

```bash
# Install husky
npm install -D husky lint-staged
npx husky init

# This creates .husky directory with pre-commit hook
```

### Configuration

```json
// package.json
{
  "scripts": {
    "prepare": "husky"
  },
  "lint-staged": {
    "*.{js,jsx,ts,tsx}": [
      "eslint --fix",
      "prettier --write"
    ],
    "*.{json,md,yml,yaml}": [
      "prettier --write"
    ],
    "*.css": [
      "stylelint --fix",
      "prettier --write"
    ]
  }
}
```

```bash
# .husky/pre-commit
npx lint-staged
```

### Commit Message Hook

```bash
# .husky/commit-msg
npx --no -- commitlint --edit $1
```

```javascript
// commitlint.config.js
module.exports = {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'type-enum': [
      2,
      'always',
      ['feat', 'fix', 'docs', 'style', 'refactor', 'test', 'chore', 'ci']
    ],
    'subject-case': [2, 'always', 'lower-case'],
    'header-max-length': [2, 'always', 72]
  }
};
```

## 3. Common Hook Configurations

### Python Project

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-toml
      - id: check-added-large-files

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.14
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks:
      - id: mypy
        additional_dependencies:
          - types-requests
          - pydantic

  - repo: https://github.com/python-poetry/poetry
    rev: 1.7.0
    hooks:
      - id: poetry-check
      - id: poetry-lock
        args: [--check]

  - repo: local
    hooks:
      - id: pytest
        name: pytest
        entry: pytest
        language: system
        pass_filenames: false
        always_run: true
        stages: [push]
```

### JavaScript/TypeScript Project

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-json
      - id: check-yaml

  - repo: local
    hooks:
      - id: eslint
        name: eslint
        entry: npx eslint --fix
        language: system
        files: \.[jt]sx?$
        pass_filenames: true

      - id: prettier
        name: prettier
        entry: npx prettier --write
        language: system
        files: \.(js|jsx|ts|tsx|json|md|yml|yaml)$

      - id: tsc
        name: typescript
        entry: npx tsc --noEmit
        language: system
        files: \.tsx?$
        pass_filenames: false

      - id: test
        name: tests
        entry: npm test
        language: system
        pass_filenames: false
        stages: [push]
```

### Go Project

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml

  - repo: https://github.com/dnephin/pre-commit-golang
    rev: v0.5.1
    hooks:
      - id: go-fmt
      - id: go-vet
      - id: go-imports
      - id: go-cyclo
        args: [-over=15]
      - id: golangci-lint
      - id: go-build
      - id: go-mod-tidy
```

### Terraform/IaC Project

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-json

  - repo: https://github.com/antonbabenko/pre-commit-terraform
    rev: v1.86.0
    hooks:
      - id: terraform_fmt
      - id: terraform_validate
      - id: terraform_tflint
      - id: terraform_docs
        args:
          - --hook-config=--path-to-file=README.md
          - --hook-config=--add-to-existing-file=true
          - --hook-config=--create-file-if-not-exist=true
      - id: terraform_checkov
        args:
          - --args=--skip-check CKV_AWS_1

  - repo: https://github.com/bridgecrewio/checkov.git
    rev: 3.1.50
    hooks:
      - id: checkov
```

## 4. Security Hooks

```yaml
repos:
  # Detect secrets
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
        args: ['--baseline', '.secrets.baseline']
        exclude: package-lock\.json$

  # Gitleaks
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.18.1
    hooks:
      - id: gitleaks

  # Trivy
  - repo: https://github.com/aquasecurity/trivy
    rev: v0.48.3
    hooks:
      - id: trivy-config
      - id: trivy-fs
        args: ['--scanners', 'vuln,secret']

  # Bandit (Python security)
  - repo: https://github.com/PyCQA/bandit
    rev: 1.7.7
    hooks:
      - id: bandit
        args: ['-c', 'pyproject.toml']
        additional_dependencies: ['bandit[toml]']
```

## 5. CI Integration

### GitHub Actions

```yaml
name: Pre-commit

on:
  pull_request:
  push:
    branches: [main]

jobs:
  pre-commit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - uses: pre-commit/action@v3.0.1
        with:
          extra_args: --all-files
```

### pre-commit.ci

```yaml
# .pre-commit-config.yaml
ci:
  autofix_prs: true
  autofix_commit_msg: 'style: auto fixes from pre-commit.ci'
  autoupdate_schedule: weekly
  autoupdate_commit_msg: 'chore: pre-commit autoupdate'
  skip: [pytest]  # Skip slow hooks in CI
```

## 6. Lefthook (Alternative)

### Installation

```bash
# Install
npm install -D lefthook
# or
brew install lefthook

# Initialize
lefthook install
```

### Configuration (lefthook.yml)

```yaml
pre-commit:
  parallel: true
  commands:
    lint:
      glob: "*.{js,ts,jsx,tsx}"
      run: npx eslint --fix {staged_files}

    format:
      glob: "*.{js,ts,jsx,tsx,json,md}"
      run: npx prettier --write {staged_files}

    test:
      run: npm test -- --passWithNoTests
      skip:
        - merge
        - rebase

commit-msg:
  commands:
    commitlint:
      run: npx commitlint --edit {1}

pre-push:
  commands:
    typecheck:
      run: npx tsc --noEmit
```

## Best Practices

1. **Fast hooks** - Keep pre-commit hooks under 5 seconds
2. **Staged files only** - Use lint-staged for efficiency
3. **Skip for emergencies** - `--no-verify` when needed
4. **CI verification** - Run hooks in CI as backup
5. **Auto-fix when possible** - `--fix` flags
6. **Push hooks for slow checks** - Tests, type checking
7. **Baseline secrets** - Track known false positives
8. **Pin versions** - Reproducible environments
9. **Documentation** - README for setup instructions
10. **Team alignment** - Everyone uses same hooks
