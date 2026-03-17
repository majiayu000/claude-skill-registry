---
name: go-code-review
description: Reviews Go code for idiomatic patterns, error handling, concurrency safety, and common mistakes. Use when reviewing .go files, checking error handling, goroutine usage, or interface design.
---

# Go Code Review

## Quick Reference

| Issue Type | Reference |
|------------|-----------|
| Missing error checks, wrapped errors | [references/error-handling.md](references/error-handling.md) |
| Race conditions, channel misuse | [references/concurrency.md](references/concurrency.md) |
| Interface pollution, naming | [references/interfaces.md](references/interfaces.md) |
| Resource leaks, defer misuse | [references/common-mistakes.md](references/common-mistakes.md) |

## Review Checklist

- [ ] All errors are checked (no `_ = err`)
- [ ] Errors wrapped with context (`fmt.Errorf("...: %w", err)`)
- [ ] Resources closed with `defer` immediately after creation
- [ ] No goroutine leaks (channels closed, contexts canceled)
- [ ] Interfaces defined by consumers, not producers
- [ ] Interface names end in `-er` (Reader, Writer, Handler)
- [ ] Exported names have doc comments
- [ ] No naked returns in functions > 5 lines
- [ ] Context passed as first parameter
- [ ] Mutexes protect shared state, not methods

## When to Load References

- Reviewing error return patterns → error-handling.md
- Reviewing goroutines/channels → concurrency.md
- Reviewing type definitions → interfaces.md
- General Go review → common-mistakes.md

## Review Questions

1. Are all error returns checked and wrapped?
2. Are goroutines properly managed with context cancellation?
3. Are resources (files, connections) closed with defer?
4. Are interfaces minimal and defined where used?

## Valid Patterns (Do NOT Flag)

These patterns are acceptable and should NOT be flagged as issues:

- **`_ = err` with reason comment** - Intentionally ignored errors with explanation
  ```go
  _ = conn.Close() // Best effort cleanup, already handling primary error
  ```
- **Empty interface `interface{}`** - For truly generic code (pre-generics codebases)
- **Naked returns in short functions** - Acceptable in functions < 5 lines with named returns
- **Channel without close** - When consumer stops via context cancellation, not channel close
- **Mutex protecting struct fields** - Even if accessed only via methods, this is correct encapsulation
- **`//nolint` directives with reason** - Acceptable when accompanied by explanation
  ```go
  //nolint:errcheck // Error logged but not returned per API contract
  ```
- **Defer in loop** - When function scope cleanup is intentional (e.g., processing files in batches)
- **Functional options pattern** - `type Option func(*T)` with `With*` constructors is idiomatic for configurable types
  ```go
  func NewServer(addr string, opts ...Option) *Server { ... }
  ```
- **`sync.Pool` for hot paths** - Acceptable for reducing allocation pressure in performance-critical code
  ```go
  var bufPool = sync.Pool{New: func() any { return new(bytes.Buffer) }}
  ```

## Context-Sensitive Rules

Only flag these issues when the specific conditions apply:

| Issue | Flag ONLY IF |
|-------|--------------|
| Missing error check | Error return is actionable (can retry, log, or propagate) |
| Goroutine leak | No context cancellation path exists for the goroutine |
| Missing defer | Resource isn't explicitly closed before next acquisition or return |
| Interface pollution | Interface has > 1 method AND only one consumer exists |

## Before Submitting Findings

Load and follow [review-verification-protocol](../review-verification-protocol/SKILL.md) before reporting any issue.
