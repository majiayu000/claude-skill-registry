---
name: lint
description: How to lint and typecheck in this project. Load when implementing or verifying code.
allowed-tools: Bash
---

# Lint Skill

Project-specific linting and typechecking.

## Lint Commands

```bash
# Run linter
# TODO: Add your lint command
npx eslint {files}
# ruff check {files}
# golangci-lint run

# Auto-fix
npx eslint {files} --fix
# ruff check {files} --fix
```

## Typecheck Commands

```bash
# Run typecheck
# TODO: Add your typecheck command
npx tsc --noEmit
# mypy {files}
# go build ./...
```

## Common Issues

### Import Order
Run auto-fix to sort imports.

### Unused Variables
Remove or prefix with `_`.

### Type Errors
Check that types match expected signatures.
