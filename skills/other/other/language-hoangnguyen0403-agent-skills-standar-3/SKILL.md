---
name: Language
description: Core idioms, style guides, and best practices for writing idiomatic Go code.
metadata:
  labels: [golang, style, idioms, best-practices]
  triggers:
    files: ['**/*.go', 'go.mod']
    keywords: [golang, go code, style, idiomatic]
---

# Golang Language Standards

## **Priority: P0 (CRITICAL)**

## Guidelines

- **Fmt**: Run `gofmt` or `goimports` on save.
- **Naming**: Use `camelCase` for internal, `PascalCase` for exported.
- **Packages**: Short, lowercase, singular, no underscores (e.g., `net/http` not `net_http`).
- **Interfaces**: Define where used, not where implemented. Small interfaces (1-2 methods).
- **Errors**: Return error as last return value. Handle immediately.
- **Variables**: Short names for small scope (`i`, `ctx`), descriptive for large scope.
- **Slices**: Prefer slices over arrays. Use `make()` for capacity.
- **Const**: Use `iota` for enums.

## Anti-Patterns

- **No `init`**: Use constructors, not `init()`.
- **No Globals**: Use DI, not global mutable state.
- **No `panic`**: Return errors, don't panic.
- **No `_` ignored errors**: Always check and handle errors.
- **No stutter**: `log.Error`, not `log.LogError`.

## references

- [Idioms](references/idioms.md)
- [Effective Go Summary](references/effective-go-summary.md)
