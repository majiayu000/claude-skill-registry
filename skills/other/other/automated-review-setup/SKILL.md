---
name: automated-review-setup
description: >
  Set up automated code quality tools: ESLint, Prettier, pre-commit hooks, and CI linting.
  Activate whenever the user sets up a new project, asks about code formatting, configures
  linters, sets up Git hooks, or mentions Husky, lint-staged, CODEOWNERS, or pre-commit
  hooks. Also activate when discussing consistent code style enforcement.
---

# Automated Code Review Setup

Automate code quality enforcement with linters, formatters, pre-commit hooks, and CI
checks. Catch issues before human review so reviewers can focus on logic and design.

## When to Use
- Setting up a new JavaScript/TypeScript project
- Adding linting or formatting to an existing project
- Configuring Git pre-commit hooks
- Setting up CI/CD quality gates
- Establishing CODEOWNERS for automatic reviewer assignment

## Core Patterns

### ESLint Configuration

Modern flat config for TypeScript projects.

```javascript
// eslint.config.js
import eslint from '@eslint/js';
import tseslint from 'typescript-eslint';
import eslintPluginImport from 'eslint-plugin-import';

export default tseslint.config(
  eslint.configs.recommended,
  ...tseslint.configs.recommended,
  {
    rules: {
      // Prevent common bugs
      'no-console': 'warn',
      'no-debugger': 'error',
      'no-unused-vars': 'off',
      '@typescript-eslint/no-unused-vars': ['error', {
        argsIgnorePattern: '^_',
        varsIgnorePattern: '^_',
      }],

      // Enforce code quality
      '@typescript-eslint/explicit-function-return-type': 'off',
      '@typescript-eslint/no-explicit-any': 'warn',
      '@typescript-eslint/no-non-null-assertion': 'warn',

      // Import organization
      'import/order': ['error', {
        groups: ['builtin', 'external', 'internal', 'parent', 'sibling'],
        'newlines-between': 'always',
        alphabetize: { order: 'asc' },
      }],
    },
  },
  {
    ignores: ['dist/', 'node_modules/', 'coverage/'],
  }
);
```

### Prettier Configuration

Set up Prettier for consistent formatting.

```json
// .prettierrc
{
  "semi": true,
  "singleQuote": true,
  "trailingComma": "all",
  "printWidth": 100,
  "tabWidth": 2,
  "arrowParens": "avoid",
  "endOfLine": "lf"
}
```

```json
// .prettierignore
dist
node_modules
coverage
pnpm-lock.yaml
package-lock.json
```

```json
// package.json scripts
{
  "scripts": {
    "lint": "eslint .",
    "lint:fix": "eslint . --fix",
    "format": "prettier --write .",
    "format:check": "prettier --check ."
  }
}
```

### Pre-Commit Hooks with Husky and lint-staged

Run linters only on staged files for fast feedback.

```bash
# Install
npm install -D husky lint-staged
npx husky init
```

```json
// package.json
{
  "lint-staged": {
    "*.{ts,tsx,js,jsx}": [
      "eslint --fix",
      "prettier --write"
    ],
    "*.{json,md,yml,yaml}": [
      "prettier --write"
    ],
    "*.{css,scss}": [
      "prettier --write"
    ]
  }
}
```

```bash
# .husky/pre-commit
npx lint-staged
```

```bash
# .husky/commit-msg (optional: enforce conventional commits)
npx --no -- commitlint --edit "$1"
```

### Python Pre-Commit Hooks

Use the pre-commit framework with Ruff for Python projects.

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-added-large-files
        args: ['--maxkb=500']

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.3.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
```

```bash
pip install pre-commit && pre-commit install
```

### CODEOWNERS

Automatically assign reviewers based on file ownership.

```
# .github/CODEOWNERS

# Default owners for everything
* @team-lead

# Frontend team owns UI code
/src/components/     @frontend-team
/src/hooks/          @frontend-team
/src/styles/         @frontend-team

# Backend team owns API and database
/src/api/            @backend-team
/src/db/             @backend-team
/src/middleware/      @backend-team

# Security-sensitive files require security review
/src/auth/           @security-team @backend-team
```

### CI Linting Pipeline

Run quality checks in CI to block merging of non-conforming code.

```yaml
# .github/workflows/quality.yml
name: Code Quality
on:
  pull_request:
    branches: [main, develop]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'npm'
      - run: npm ci
      - run: npm run lint
      - run: npm run format:check
      - run: npx tsc --noEmit

```

## Anti-Patterns
- Configuring rules as errors during initial adoption (use warnings first, tighten later)
- Running linters on the entire codebase in pre-commit hooks instead of only staged files
- Having linter and formatter conflict (ESLint style rules vs Prettier)
- Skipping hooks with `--no-verify` as a habit instead of fixing the issue
- Over-configuring ESLint with hundreds of rules instead of extending a standard config
- Not including a `.prettierrc` causing inconsistent formatting across editors
- Setting up CODEOWNERS without matching your team structure

## Quick Reference

| Tool | Purpose | Config File |
|------|---------|------------|
| ESLint | Catch bugs and enforce patterns | `eslint.config.js` |
| Prettier | Consistent formatting | `.prettierrc` |
| Husky | Git hook management | `.husky/` |
| lint-staged | Run tools on staged files only | `package.json` or `.lintstagedrc` |
| commitlint | Enforce commit message format | `commitlint.config.js` |
| CODEOWNERS | Auto-assign reviewers | `.github/CODEOWNERS` |
| Ruff | Python linting + formatting | `pyproject.toml` |
| pre-commit | Python/polyglot hook framework | `.pre-commit-config.yaml` |

| Setup Order |
|-------------|
| 1. Prettier (formatting baseline) |
| 2. ESLint (bug catching, disable style rules handled by Prettier) |
| 3. Husky + lint-staged (pre-commit enforcement) |
| 4. CI pipeline (final gate) |
| 5. CODEOWNERS (reviewer assignment) |
