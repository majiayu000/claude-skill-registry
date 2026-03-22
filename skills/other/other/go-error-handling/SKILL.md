---
name: go-error-handling
description: Use when writing Go code that returns, wraps, or handles errors — choosing between sentinel errors, custom types, and fmt.Errorf (%w vs %v), structuring error flow, or deciding whether to log or return. Also use when propagating errors across package boundaries or using errors.Is/As, even if the user doesn't ask about error strategy. Does not cover panic/recover patterns (see go-defensive).
license: Apache-2.0
compatibility: Requires Go 1.13+ for errors.Is/errors.As and fmt.Errorf %w wrapping. Structured logging examples use slog (Go 1.21+).
metadata:
  sources: "Google Style Guide, Uber Style Guide"
allowed-tools: Bash(bash:*)
---

# Go Error Handling

## Available Scripts

- **`scripts/check-errors.sh`** — Detects error handling anti-patterns: string comparison on `err.Error()`, bare `return err` without context, and log-and-return violations. Run `bash scripts/check-errors.sh --help` for options.

In Go, [errors are values](https://go.dev/blog/errors-are-values) — they are
created by code and consumed by code.

## Choosing an Error Strategy

1. System boundary (RPC, IPC, storage)? → Wrap with `%v` to avoid leaking internals
2. Caller needs to match specific conditions? → Sentinel or typed error, wrap with `%w`
3. Caller just needs debugging context? → `fmt.Errorf("...: %w", err)`
4. Leaf function, no wrapping needed? → Return the error directly

**Default**: wrap with `%w` and place it at the end of the format string.

---

## Core Rules

### Never Return Concrete Error Types

**Never return concrete error types from exported functions** — a concrete `nil`
pointer can become a non-nil interface:

```go
// Bad: Concrete type can cause subtle bugs
func Bad() *os.PathError { /*...*/ }

// Good: Always return the error interface
func Good() error { /*...*/ }
```

### Error Strings

Error strings should **not** be capitalized and should **not** end with
punctuation. Exception: exported names, proper nouns, or acronyms.

```go
// Bad
err := fmt.Errorf("Something bad happened.")

// Good
err := fmt.Errorf("something bad happened")
```

For displayed messages (logs, test failures, API responses), capitalization is
appropriate.

### Return Values on Error

When a function returns an error, callers must treat all non-error return values
as unspecified unless explicitly documented.

**Tip**: Functions taking a `context.Context` should usually return an `error`
so callers can determine if the context was cancelled.

---

## Handling Errors

When encountering an error, make a **deliberate choice** — do not discard
with `_`:

1. **Handle immediately** — address the error and continue
2. **Return to caller** — optionally wrapped with context
3. **In exceptional cases** — `log.Fatal` or `panic`

To intentionally ignore: add a comment explaining why.

```go
n, _ := b.Write(p) // never returns a non-nil error
```

For related concurrent operations, use
[`errgroup`](https://pkg.go.dev/golang.org/x/sync/errgroup):

```go
g, ctx := errgroup.WithContext(ctx)
g.Go(func() error { return task1(ctx) })
g.Go(func() error { return task2(ctx) })
if err := g.Wait(); err != nil { return err }
```

### Avoid In-Band Errors

Don't return `-1`, `nil`, or empty string to signal errors. Use multiple
returns:

```go
// Bad: In-band error value
func Lookup(key string) int  // returns -1 for missing

// Good: Explicit error or ok value
func Lookup(key string) (string, bool)
```

This prevents callers from writing `Parse(Lookup(key))` — it causes a
compile-time error since `Lookup(key)` has 2 outputs.

---

## Error Flow

Handle errors before normal code. Early returns keep the happy path unindented:

```go
// Good: Error first, normal code unindented
if err != nil {
    return err
}
// normal code
```

**Handle errors once** — either log or return, never both:

```
Error encountered?
├─ Caller can act on it? → Return (with context via %w)
├─ Top of call chain? → Log and handle
└─ Neither? → Log at appropriate level, continue
```

> Read [references/ERROR-FLOW.md](references/ERROR-FLOW.md) when structuring complex error flows, deciding between logging vs returning, implementing the handle-once pattern, or choosing structured logging levels.

---

## Error Types

> **Advisory**: Recommended best practice.

| Caller needs to match? | Message type | Use |
|------------------------|--------------|-----|
| No | static | `errors.New("message")` |
| No | dynamic | `fmt.Errorf("msg: %v", val)` |
| Yes | static | `var ErrFoo = errors.New("...")` |
| Yes | dynamic | custom `error` type |

**Default**: Wrap with `fmt.Errorf("...: %w", err)`. Escalate to sentinels for
`errors.Is()`, to custom types for `errors.As()`.

> Read [references/ERROR-TYPES.md](references/ERROR-TYPES.md) when defining sentinel errors, creating custom error types, or choosing error strategies for a package API.

---

## Error Wrapping

> **Advisory**: Recommended best practice.

- **Use `%v`**: At system boundaries, for logging, to hide internal details
- **Use `%w`**: To preserve error chain for `errors.Is`/`errors.As`

**Key rules**: Place `%w` at the end. Add context callers don't have. If
annotation adds nothing, return `err` directly.

> Read [references/WRAPPING.md](references/WRAPPING.md) when deciding between %v and %w, wrapping errors across package boundaries, or adding contextual information.

> **Validation**: After implementing error handling, run `bash scripts/check-errors.sh` to detect common anti-patterns. Then run `go vet ./...` to catch additional issues.

---

## Related Skills

- **Error naming**: See [go-naming](../go-naming/SKILL.md) when naming sentinel errors (`ErrFoo`) or custom error types
- **Testing errors**: See [go-testing](../go-testing/SKILL.md) when testing error semantics with `errors.Is`/`errors.As` or writing error-checking helpers
- **Panic handling**: See [go-defensive](../go-defensive/SKILL.md) when deciding between panic and error returns, or writing recover guards
- **Guard clauses**: See [go-control-flow](../go-control-flow/SKILL.md) when structuring early-return error flow or reducing nesting
- **Logging decisions**: See [go-logging](../go-logging/SKILL.md) when choosing log levels, configuring structured logging, or deciding what context to include in log messages

