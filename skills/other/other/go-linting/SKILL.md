---
name: go-linting
description: Recommended Go linters and golangci-lint configuration. Use when setting up linting for a Go project or configuring CI/CD.
---

# Go Linting

> **Source**: Uber Go Style Guide

## Core Principle

More important than any "blessed" set of linters: **lint consistently across a codebase**.

Consistent linting helps catch common issues and establishes a high bar for code quality without being unnecessarily prescriptive.

---

## Minimum Recommended Linters

> **Source**: Uber Go Style Guide

These linters catch the most common issues while maintaining a high quality bar:

| Linter | Purpose |
|--------|---------|
| [errcheck](https://github.com/kisielk/errcheck) | Ensure errors are handled |
| [goimports](https://pkg.go.dev/golang.org/x/tools/cmd/goimports) | Format code and manage imports |
| [revive](https://github.com/mgechev/revive) | Common style mistakes (modern replacement for golint) |
| [govet](https://pkg.go.dev/cmd/vet) | Analyze code for common mistakes |
| [staticcheck](https://staticcheck.dev) | Various static analysis checks |

> **Note**: `revive` is the modern, faster successor to the now-deprecated `golint`.

---

## Lint Runner: golangci-lint

> **Source**: Uber Go Style Guide

Use [golangci-lint](https://github.com/golangci/golangci-lint) as your lint runner:

- **Performance**: Optimized for large codebases
- **Unified config**: Configure many linters at once
- **Extensible**: Add linters as needed for your project

See the [example .golangci.yml](https://github.com/uber-go/guide/blob/master/.golangci.yml) from uber-go/guide.

---

## Example Configuration

Create `.golangci.yml` in your project root:

```yaml
linters:
  enable:
    - errcheck
    - goimports
    - revive
    - govet
    - staticcheck

linters-settings:
  goimports:
    local-prefixes: github.com/your-org/your-repo
  revive:
    rules:
      - name: blank-imports
      - name: context-as-argument
      - name: error-return
      - name: error-strings
      - name: exported

run:
  timeout: 5m
```

### Running

```bash
# Install
go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest

# Run all linters
golangci-lint run

# Run on specific paths
golangci-lint run ./pkg/...
```

---

## Quick Reference

| Task | Command/Action |
|------|----------------|
| Install golangci-lint | `go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest` |
| Run linters | `golangci-lint run` |
| Run on path | `golangci-lint run ./pkg/...` |
| Config file | `.golangci.yml` in project root |
| CI integration | Run `golangci-lint run` in pipeline |

### Linter Selection Guidelines

| When you need... | Use |
|------------------|-----|
| Error handling coverage | errcheck |
| Import formatting | goimports |
| Style consistency | revive |
| Bug detection | govet, staticcheck |
| All of the above | golangci-lint with config |

---

## See Also

- For core style principles: `go-style-core`
- For testing best practices: `go-testing`
