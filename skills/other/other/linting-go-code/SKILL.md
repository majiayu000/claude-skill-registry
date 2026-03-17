---
name: linting-go-code
description: Lint and format Go code. Use when you need to run linters, fix lint errors, format code, or understand why a linter is complaining.
---

# Linting Go Code

All commands run from the Go module root (`installer/`).

## Lint

```bash
task lint
```

Runs golangci-lint (the master linter — all individual linters run through it) plus typos for spell checking. Auto-fixes what it can.

## Format

```bash
task fmt
```

Formats code through golangci-lint (gofumpt + goimports + golines). Never run these formatters standalone — always use `task fmt`.

## Nolint Directives

When suppressing a lint in code, the configuration requires both a specific linter name and an explanation:

```go
//nolint:gochecknoinits // Cobra requires an init function to set up the command structure.
```

Blanket `//nolint` without a linter name is not allowed.

## When Lints Fail

1. Read the linter's message — golangci-lint identifies which linter flagged the issue
2. Fix the code to satisfy the linter when possible
3. If the lint is a false positive, suppress with a `//nolint:lintername // reason` directive
4. For linter configuration details (which linters are enabled, thresholds, exclusions), read `.golangci.yml`
