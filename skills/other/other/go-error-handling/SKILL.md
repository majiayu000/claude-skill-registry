---
name: go-error-handling
description: Comprehensive Go error handling patterns from Google and Uber style guides. Covers returning errors, wrapping with %w, sentinel errors, choosing error types, handling errors once, error flow structure, and logging. Use when writing Go code that creates, returns, wraps, or handles errors.
---

# Go Error Handling

In Go, [errors are values](https://go.dev/blog/errors-are-values) - they are
created by code and consumed by code. This skill covers how to return,
structure, wrap, and handle errors effectively.

---

## Returning Errors

> **Normative**: Required per Google's canonical Go style guide.

### Use the `error` Type

Use `error` to signal that a function can fail. By convention, `error` is the
last result parameter.

```go
// Good:
func Good() error { /* ... */ }

func GoodLookup() (*Result, error) {
    // ...
    if err != nil {
        return nil, err
    }
    return res, nil
}
```

**Never return concrete error types from exported functions** - a concrete `nil`
pointer can become a non-nil interface value:

```go
// Bad: Concrete error type can cause subtle bugs
func Bad() *os.PathError { /*...*/ }

// Good: Always return the error interface
func Good() error { /*...*/ }
```

### Return Values on Error

When a function returns an error, callers must treat all non-error return values
as unspecified unless explicitly documented. Commonly, non-error return values
are their zero values.

**Tip**: Functions taking a `context.Context` should usually return an `error`
so callers can determine if the context was cancelled.

---

## Error Strings

> **Normative**: Required per Google's canonical Go style guide.

Error strings should **not** be capitalized and should **not** end with
punctuation:

```go
// Bad:
err := fmt.Errorf("Something bad happened.")

// Good:
err := fmt.Errorf("something bad happened")
```

**Exception**: Error strings may start with a capital letter if they begin with
an exported name, proper noun, or acronym.

**Rationale**: Error strings usually appear within other context before being
printed.

For **displayed messages** (logs, test failures, API responses), capitalization
is appropriate:

```go
// Good:
log.Infof("Operation aborted: %v", err)
log.Errorf("Operation aborted: %v", err)
t.Errorf("Op(%q) failed unexpectedly; err=%v", args, err)
```

---

## Handling Errors

> **Normative**: Required per Google's canonical Go style guide.

Code that encounters an error must make a **deliberate choice** about how to
handle it. Do not discard errors using `_` variables.

When a function returns an error, do one of:

1. **Handle and address the error immediately**
2. **Return the error to the caller**
3. **In exceptional situations**: call `log.Fatal` or (if absolutely necessary)
   `panic`

### Intentionally Ignoring Errors

In rare cases where ignoring an error is appropriate, add a comment explaining
why:

```go
// Good:
var b *bytes.Buffer
n, _ := b.Write(p) // never returns a non-nil error
```

### Using errgroup for Related Operations

When orchestrating related operations where only the first error is useful,
[`errgroup`](https://pkg.go.dev/golang.org/x/sync/errgroup) provides a
convenient abstraction:

```go
// Good: errgroup handles cancellation and first-error semantics
g, ctx := errgroup.WithContext(ctx)
g.Go(func() error { return task1(ctx) })
g.Go(func() error { return task2(ctx) })
if err := g.Wait(); err != nil {
    return err
}
```

---

## Avoid In-Band Errors

> **Normative**: Required per Google's canonical Go style guide.

Do not return special values like `-1`, `nil`, or empty string to signal errors:

```go
// Bad: In-band error value
// Lookup returns the value for key or -1 if there is no mapping for key.
func Lookup(key string) int

// Bad: Caller mistakes can attribute errors to wrong function
return Parse(Lookup(missingKey))
```

Use multiple return values instead:

```go
// Good: Explicit error or ok value
func Lookup(key string) (value string, ok bool)

// Good: Forces caller to handle the error case
value, ok := Lookup(key)
if !ok {
    return fmt.Errorf("no value for %q", key)
}
return Parse(value)
```

This prevents callers from writing `Parse(Lookup(key))` - it causes a
compile-time error since `Lookup(key)` has 2 outputs.

---

## Indent Error Flow

> **Normative**: Required per Google's canonical Go style guide.

Handle errors before proceeding with normal code. This improves readability by
enabling the reader to find the normal path quickly.

```go
// Good: Error handling first, normal code unindented
if err != nil {
    // error handling
    return // or continue, etc.
}
// normal code
```

```go
// Bad: Normal code hidden in else clause
if err != nil {
    // error handling
} else {
    // normal code that looks abnormal due to indentation
}
```

### Avoid If-with-Initializer for Long-Lived Variables

If you use a variable for more than a few lines, move the declaration out:

```go
// Good: Declaration separate from error check
x, err := f()
if err != nil {
    return err
}
// lots of code that uses x
// across multiple lines
```

```go
// Bad: Variable scoped to else block, hard to read
if x, err := f(); err != nil {
    return err
} else {
    // lots of code that uses x
    // across multiple lines
}
```

---

## Error Types

> **Advisory**: Recommended best practice.

If callers need to distinguish different error conditions programmatically, give
errors structure rather than relying on string matching. Choose the right error
type based on whether callers need to match errors and whether messages are
static or dynamic.

**Quick decision table**:

| Caller needs to match? | Message type | Use |
|------------------------|--------------|-----|
| No | static | `errors.New("message")` |
| No | dynamic | `fmt.Errorf("msg: %v", val)` |
| Yes | static | `var ErrFoo = errors.New("...")` |
| Yes | dynamic | custom `error` type |

For detailed coverage of sentinel errors, structured error types, and error
checking patterns, see [references/ERROR-TYPES.md](references/ERROR-TYPES.md).

---

## Error Wrapping

> **Advisory**: Recommended best practice.

The choice between `%v` and `%w` significantly impacts how errors are propagated
and inspected:

- **Use `%v`**: At system boundaries, for logging, to hide internal details
- **Use `%w`**: To preserve error chain for `errors.Is`/`errors.As` inspection

**Key rules**:
- Place `%w` at the **end**: `"context message: %w"`
- Add context that callers don't have; don't duplicate existing info
- If annotation adds nothing, just return `err` directly

For detailed coverage of wrapping patterns, placement, adding context, and
logging best practices, see [references/WRAPPING.md](references/WRAPPING.md).

---

## Handle Errors Once

> **Source**: Uber Go Style Guide

When a caller receives an error, it should handle each error **only once**.
Choose ONE response:

1. **Return the error** (wrapped or verbatim) for the caller to handle
2. **Log and degrade gracefully** (don't return the error)
3. **Match and handle** specific error cases, return others

**Never log AND return** - this causes duplicate logging as callers up the stack
will also handle the error.

```go
// Bad: Logs AND returns - causes noise in logs
u, err := getUser(id)
if err != nil {
    log.Printf("Could not get user %q: %v", id, err)
    return err  // Callers will also log this!
}

// Good: Wrap and return - let caller decide how to handle
u, err := getUser(id)
if err != nil {
    return fmt.Errorf("get user %q: %w", id, err)
}

// Good: Log and degrade gracefully (don't return error)
if err := emitMetrics(); err != nil {
    // Failure to write metrics should not break the application
    log.Printf("Could not emit metrics: %v", err)
}
// Continue execution...

// Good: Match specific errors, return others
tz, err := getUserTimeZone(id)
if err != nil {
    if errors.Is(err, ErrUserNotFound) {
        // User doesn't exist. Use UTC.
        tz = time.UTC
    } else {
        return fmt.Errorf("get user %q: %w", id, err)
    }
}
```

---

## Quick Reference

| Pattern | Guidance |
|---------|----------|
| Return type | Always use `error` interface, not concrete types |
| Error strings | Lowercase, no punctuation |
| Ignoring errors | Comment explaining why it's safe |
| In-band errors | Avoid; use multiple returns |
| Error flow | Handle errors first, no else clauses |
| Error type choice | Match needed + dynamic → custom type; static → sentinel |
| Sentinel errors | Use `errors.Is` for checking |
| %v vs %w | `%v` for boundaries, `%w` for chain preservation |
| %w placement | Always at the end: `"context: %w"` |
| Handle once | Choose ONE: return, log+degrade, or match+handle |
| Logging | Don't log and return; let caller decide |

---

## See Also

- **go-style-core**: Core Go style principles and formatting
- **go-naming**: Naming conventions including error naming (ErrFoo)
- **go-testing**: Testing patterns including error testing
- **go-defensive**: Defensive programming including panic handling
- **go-linting**: Linting tools that catch error handling issues

### Reference Files

- [references/ERROR-TYPES.md](references/ERROR-TYPES.md) - Sentinel errors,
  structured error types, choosing error types, and checking errors
- [references/WRAPPING.md](references/WRAPPING.md) - Error wrapping with %v vs
  %w, placement, adding context, and logging
