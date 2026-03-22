---
name: go-defensive
description: Use when hardening Go code at API boundaries — copying slices/maps, verifying interface compliance, using defer for cleanup, time.Time/time.Duration, or avoiding mutable globals. Also use when reviewing for robustness concerns like missing cleanup or unsafe crypto usage, even if the user doesn't mention "defensive programming." Does not cover error handling strategy (see go-error-handling).
license: Apache-2.0
compatibility: Uses crypto/rand.Text (Go 1.24+) in examples
metadata:
  sources: "Effective Go, Uber Style Guide, Go Wiki CodeReviewComments"
---

# Go Defensive Programming Patterns

## Defensive Checklist Priority

When hardening code at API boundaries, check in this order:

```
Reviewing an API boundary?
├─ 1. Error handling     → Return errors; don't panic (see go-error-handling)
├─ 2. Input validation   → Copy slices/maps received from callers
├─ 3. Output safety      → Copy slices/maps before returning to callers
├─ 4. Resource cleanup   → Use defer for Close/Unlock/Cancel
├─ 5. Interface checks   → var _ Interface = (*Type)(nil) for compile-time verification
├─ 6. Time correctness   → Use time.Time and time.Duration, not int/float
├─ 7. Enum safety        → Start iota at 1 so zero-value is invalid
└─ 8. Crypto safety      → crypto/rand for keys, never math/rand
```

---

## Quick Reference

| Pattern | Rule | Details |
|---------|------|---------|
| Boundary copies | Copy slices/maps on receive and return | [BOUNDARY-COPYING.md](references/BOUNDARY-COPYING.md) |
| Defer cleanup | `defer f.Close()` right after `os.Open` | Below |
| Interface check | `var _ I = (*T)(nil)` | See go-interfaces |
| Time types | `time.Time` / `time.Duration`, never raw int | [TIME-ENUMS-TAGS.md](references/TIME-ENUMS-TAGS.md) |
| Enum start | `iota + 1` so zero = invalid | Below |
| Crypto rand | `crypto/rand` for keys, never `math/rand` | Below |
| Must functions | Only at init; panic on failure | [MUST-FUNCTIONS.md](references/MUST-FUNCTIONS.md) |
| Panic/recover | Never expose panics across packages | [PANIC-RECOVER.md](references/PANIC-RECOVER.md) |
| Mutable globals | Replace with dependency injection | Below |

---

## Verify Interface Compliance

Use compile-time checks to verify interface implementation. See **go-interfaces**: Interface Satisfaction Checks for the full pattern.

```go
var _ http.Handler = (*Handler)(nil)
```

## Copy Slices and Maps at Boundaries

Slices and maps contain pointers to underlying data. Copy at API boundaries to prevent unintended modifications.

```go
// Receiving: copy incoming slice
d.trips = make([]Trip, len(trips))
copy(d.trips, trips)

// Returning: copy map before returning
result := make(map[string]int, len(s.counters))
for k, v := range s.counters { result[k] = v }
```

> Read [references/BOUNDARY-COPYING.md](references/BOUNDARY-COPYING.md) when copying slices or maps at API boundaries, or deciding when defensive copies are necessary vs. when they can be skipped.

## Defer to Clean Up

Use `defer` to clean up resources (files, locks). Avoids missed cleanup on multiple return paths.

```go
p.Lock()
defer p.Unlock()

if p.count < 10 {
  return p.count
}
p.count++
return p.count
```

Defer overhead is negligible. Place `defer f.Close()` immediately after
`os.Open` for clarity. Arguments to deferred functions are evaluated when
`defer` executes, not when the function runs. Multiple defers execute in
LIFO order.

## Struct Field Tags

> **Advisory**: Always add explicit field tags to structs that are marshaled or unmarshaled.

```go
type User struct {
    Name  string `json:"name"  yaml:"name"`
    Email string `json:"email" yaml:"email"`
}
```

Field tags are a **serialization contract** — renaming a struct field without
updating the tag silently breaks wire compatibility. Treat tags as part of
the public API for any type that crosses a serialization boundary.

## Start Enums at One

Start enums at non-zero to distinguish uninitialized from valid values.

```go
const (
  Add Operation = iota + 1  // Add=1, zero value = uninitialized
  Subtract
  Multiply
)
```

**Exception**: When zero is the sensible default (e.g., `LogToStdout = iota`).

## Time, Struct Tags, and Embedding

> Read [references/TIME-ENUMS-TAGS.md](references/TIME-ENUMS-TAGS.md) when using `time.Time`/`time.Duration` instead of raw ints, adding field tags to marshaled structs, or deciding whether to embed types in public structs.

## Avoid Mutable Globals

Inject dependencies instead of mutating package-level variables. This makes
code testable without global save/restore.

```go
type signer struct {
  now func() time.Time  // injected; tests replace with fixed time
}

func newSigner() *signer {
  return &signer{now: time.Now}
}
```

> Read [references/GLOBAL-STATE.md](references/GLOBAL-STATE.md) when deciding whether a global variable is appropriate, designing the New() + Default() package state pattern, or replacing mutable globals with dependency injection.

## Crypto Rand

Do not use `math/rand` or `math/rand/v2` to generate keys — this is a
**security concern**. Time-seeded generators have predictable output.

```go
import "crypto/rand"

func Key() string { return rand.Text() }
```

For text output, use `crypto/rand.Text` directly, or encode random bytes
with `encoding/hex` or `encoding/base64`.

---

## Panic and Recover

Use `panic` only for truly unrecoverable situations. Library functions
should avoid panic.

```go
func safelyDo(work *Work) {
    defer func() {
        if err := recover(); err != nil {
            log.Println("work failed:", err)
        }
    }()
    do(work)
}
```

**Key rules:**
- Never expose panics across package boundaries — always convert to errors
- Acceptable to panic in `init()` if a library truly cannot set itself up
- Use recover to isolate panics in server goroutine handlers

> Read [references/PANIC-RECOVER.md](references/PANIC-RECOVER.md) when writing panic recovery in HTTP servers, using panic as an internal control flow mechanism in parsers, or deciding between log.Fatal and panic.

## Must Functions

`Must` functions panic on error — use them **only** during program
initialization where failure means the program cannot run.

```go
var validID = regexp.MustCompile(`^[a-z][a-z0-9-]{0,62}$`)
var tmpl = template.Must(template.ParseFiles("index.html"))
```

> Read [references/MUST-FUNCTIONS.md](references/MUST-FUNCTIONS.md) when writing custom Must functions, deciding whether Must is appropriate for a given call site, or wrapping fallible initialization in a panicking helper.

---

## Related Skills

- **Error handling**: See [go-error-handling](../go-error-handling/SKILL.md) when choosing between returning errors and panicking, or wrapping errors at boundaries
- **Concurrency safety**: See [go-concurrency](../go-concurrency/SKILL.md) when protecting shared state with mutexes, atomics, or channels
- **Interface checks**: See [go-interfaces](../go-interfaces/SKILL.md) when adding compile-time interface satisfaction checks (`var _ I = (*T)(nil)`)
- **Data structure copying**: See [go-data-structures](../go-data-structures/SKILL.md) when working with slice/map internals or pointer aliasing
