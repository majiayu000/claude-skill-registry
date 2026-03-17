---
name: validate-lint
description: Run ESLint and Prettier validation to check code style, formatting, and best practices. Returns structured output with error/warning counts, rule violations, and affected files. Used for code quality gates and pre-commit validation.
---

# Validate Lint

Executes linting tools (ESLint, Prettier) to validate code style and formatting without making changes.

## Usage

This skill runs linting checks and returns structured validation results.

## Supported Tools

- **ESLint**: JavaScript/TypeScript linting
- **Prettier**: Code formatting validation
- Supports both npm scripts and direct tool invocation

## Output Format

### Success (No Errors)

```json
{
  "status": "success",
  "lint": {
    "status": "passing",
    "errors": 0,
    "warnings": 0,
    "files": []
  },
  "canProceed": true
}
```

### Errors/Warnings Found

```json
{
  "status": "warning",
  "lint": {
    "status": "failing",
    "errors": 5,
    "warnings": 12,
    "files": [
      "src/components/CharacterCard.tsx",
      "src/utils/helpers.ts"
    ],
    "rules": {
      "no-unused-vars": 3,
      "prefer-const": 2,
      "@typescript-eslint/no-explicit-any": 7
    }
  },
  "canProceed": false,
  "details": "5 linting error(s) must be fixed before proceeding"
}
```

## When to Use

- Quality gate validation (before commit/PR)
- Pre-refactor validation
- After code changes
- Conductor Phase 3 (Quality Assurance)
- Refactor agent validation

## Requirements

- ESLint installed (npm package)
- Configuration file (.eslintrc, eslint.config.js, or package.json)
- Optional: Prettier for formatting checks
