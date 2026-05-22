---
name: git-hooks
description: Git hooks setup with pre-commit, husky, and lint-staged for automated code quality. Use when user asks to "setup pre-commit hooks", "add husky", "lint on commit", "format before commit", "run tests on push", "setup git hooks", or automate code quality checks.
---

# Git Hooks

Automate code quality with Git hooks using pre-commit, Husky, or native hooks.

## Husky + lint-staged (Node.js Projects)

### Setup

```bash
# Install
npm install -D husky lint-staged

# Initialize husky
npx husky init

# This creates .husky/pre-commit
```

### Configure lint-staged

```json
// package.json
{
  "lint-staged": {
    "*.{js,jsx,ts,tsx}": [
      "eslint --fix",
      "prettier --write"
    ],
    "*.{json,md,yml}": "prettier --write",
    "*.css": ["stylelint --fix", "prettier --write"]
  }
}
```

### Pre-commit Hook

```bash
# .husky/pre-commit
npx lint-staged
```

### Pre-push Hook

```bash
# Create hook
echo "npm test" > .husky/pre-push
chmod +x .husky/pre-push
```

## Pre-commit Framework (Python/Polyglot)

### Setup

```bash
pip install pre-commit
pre-commit install
```

### Configuration

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-json
      - id: check-added-large-files

  - repo: https://github.com/psf/black
    rev: 24.1.0
    hooks:
      - id: black

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.14
    hooks:
      - id: ruff
        args: [--fix]

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks:
      - id: mypy

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

### Commands

```bash
pre-commit run --all-files  # Run on all files
pre-commit autoupdate       # Update hook versions
pre-commit install --hook-type pre-push
```

## Native Git Hooks

### Hook Locations

```
.git/hooks/
├── pre-commit      # Before commit
├── prepare-commit-msg  # Edit commit message
├── commit-msg      # Validate commit message
├── pre-push        # Before push
├── pre-rebase      # Before rebase
└── post-merge      # After merge
```

### Simple Pre-commit

```bash
#!/bin/sh
# .git/hooks/pre-commit

# Run linter
npm run lint
if [ $? -ne 0 ]; then
  echo "Lint failed. Commit aborted."
  exit 1
fi

# Run tests
npm test
if [ $? -ne 0 ]; then
  echo "Tests failed. Commit aborted."
  exit 1
fi
```

### Commit Message Validation

```bash
#!/bin/sh
# .git/hooks/commit-msg

commit_msg=$(cat "$1")

# Conventional commits pattern
pattern="^(feat|fix|docs|style|refactor|test|chore)(\(.+\))?: .{1,50}"

if ! echo "$commit_msg" | grep -qE "$pattern"; then
  echo "Invalid commit message format."
  echo "Use: type(scope): description"
  exit 1
fi
```

## Sharing Hooks

### Git Config (core.hooksPath)

```bash
# Store hooks in repo
mkdir .githooks
mv .git/hooks/* .githooks/

# Configure git to use them
git config core.hooksPath .githooks
```

### Team Setup

```json
// package.json
{
  "scripts": {
    "prepare": "husky || true"
  }
}
```

## Skip Hooks (Emergency)

```bash
git commit --no-verify -m "Emergency fix"
git push --no-verify
```
