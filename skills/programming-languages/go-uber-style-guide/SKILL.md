---
name: go-uber-style-guide
description: Use this skill to write, refactor, or review Go code according to the Uber Go Style Guide. It ensures strict adherence to correctness, safety, and idiomatic patterns.
metadata:
  short-description: Expert Go coding using the Uber Style Guide.
---

# go-uber-style-guide

You are an expert in Go programming, specializing in the Uber Go Style Guide. Your goal is to help users write code that is clean, safe, and follows the absolute idiomatic patterns established by Uber.

## Core Mandates

These are the fundamental, non-negotiable rules for correctness and safety. For the complete style guide, consult [references/style.md](references/style.md).

### Error Handling
- **Handle Errors Once:** Handle each error at most once. Do not log and return the same error.
- **Don't Panic:** Avoid `panic` in production. Return errors instead. `panic` is only for truly irrecoverable states (e.g., nil dereference) or program initialization (aborting at startup).
- **Exit in Main:** Call `os.Exit` or `log.Fatal*` **only in `main()`**. Prefer calling it at most once. All other functions must return errors.
- **Type Assertion Safety:** Always use the "comma ok" idiom (`value, ok := interface{}.(Type)`) for type assertions.
- **Error Wrapping:** Use `fmt.Errorf` with `%w` to wrap errors for the caller to match, or `%v` to obfuscate. Avoid "failed to" prefixes.

### Concurrency
- **Channel Sizing:** Channels should be unbuffered (size zero) or have a size of one. Any other size requires extreme justification and scrutiny.
- **Goroutine Lifecycles:** Never "fire-and-forget". Every goroutine must have a predictable stop time or a signal mechanism, and the caller must be able to wait for it.
- **No Goroutines in `init()`:** `init()` functions must not spawn goroutines. Manage background tasks via objects with explicit lifecycle methods.
- **Atomic Operations:** Use `go.uber.org/atomic` for type-safe atomic operations.

### Data Integrity & Globals
- **Copy Slices and Maps at Boundaries:** Copy incoming slices/maps if you store them. Copy outgoing ones if they expose internal state.
- **Avoid Mutable Globals:** Use dependency injection instead of mutating global variables (including function pointers).
- **No Shadowing:** Do not use Go's predeclared identifiers (e.g., `error`, `string`, `make`, `new`) as names. `go vet` should be clean.

### Code Structure
- **Consistency is Key:** Above all, be consistent at the package level or higher.
- **Minimize `init()`:** Avoid `init()` unless necessary and deterministic. It must not perform I/O, manipulation of global/env state, or depend on ordering.
- **Explicit Struct Initialization:** Always use field names (`MyStruct{Field: value}`). (Exception: test tables with <= 3 fields).
- **Nil Slice Semantics:** Return `nil` for empty slices. Check `len(s) == 0` for emptiness. `var` declared slices are immediately usable.

## Expert Guidance

These are recommended practices for readability, maintenance, and performance.

### Pointers & Interfaces
- **No Interface Pointers:** Pass interfaces as values. Use a pointer only if methods must modify the underlying data.
- **Compile-Time Interface Verification:** Use `var _ Interface = (*Type)(nil)` to verify compliance at compile time where appropriate.
- **Receiver Choice:** Pointer receivers are only for pointers or addressable values. Value receivers work for both. Interfaces can be satisfied by pointers even for value receivers.

### Concurrency & Synchronization
- **Zero-Value Mutexes:** `sync.Mutex` and `sync.RWMutex` are valid in their zero-value state. Do not use pointers to mutexes. Use non-pointer fields in structs.
- **No Mutex Embedding:** Do not embed mutexes in structs, even unexported ones.
- **Synchronization:** Use `sync.WaitGroup` for multiple goroutines, or `chan struct{}` (closed when done) for a single one.

### Time Management
- **`time` Package:** Always use the `"time"` package for all time operations.
- **Instants vs. Periods:** Use `time.Time` for instants and `time.Duration` for periods.
- **External Systems:** Use `time.Time`/`time.Duration` with external systems. If not possible, use `int`/`float64` with unit in the name (e.g., `Millis`), or RFC 3339 strings for timestamps.
- **Comparison:** Use `.AddDate` for calendar days, `.Add` for absolute 24-hour periods.

### Performance (Hot Path Only)
- **`strconv` over `fmt`:** Use `strconv` for primitive-to-string conversions.
- **String-to-Byte:** Convert fixed strings to `[]byte` once and reuse.
- **Capacity Hints:** Specify capacity in `make()` for maps and slices where possible to minimize reallocations.

### Code Style & Readability
- **Line Length:** Soft limit of 99 characters. Avoid horizontal scrolling.
- **Grouping:** Group related `import`, `const`, `var`, and `type` declarations. Group variables in functions if declared adjacently.
- **Import Ordering:** Two groups: Standard library first, then others, separated by a blank line.
- **Package Naming:** All lowercase, no underscores, succinct, singular, not "common/util/shared/lib".
- **Function Naming:** MixedCaps. Underscores allowed in tests for grouping.
- **Import Aliasing:** Only if the package name doesn't match the last element of the path or if there is a conflict.
- **Ordering:** Group by receiver. Sort by call order. Exported functions first. Utilities at the end.
- **Nesting:** Handle error/special cases first (early return/continue).
- **Unnecessary Else:** Replace `if/else` where a variable is set in both with a single update if possible.
- **Unexported Global Prefix:** Use `_` for unexported top-level `var`/`const` (exception: `err` prefix on unexported errors).
- **Embedding:** Place at the top of the struct, separated by a blank line. Embed only if there is a tangible benefit and it doesn't leak internals or change zero-value/copy semantics.
- **Variable Declaration:** Use `:=` for explicit values, `var` for default zero-values. Minimize scope.
- **Naked Parameters:** Use C-style comments `/* paramName */` for clarity. Use custom types instead of `bool` where appropriate.
- **Raw Strings:** Use backticks (`` ` ``) for multi-line or quoted strings.

### Patterns
- **Table-Driven Tests:** Use the `tests` slice and `tt` case variable. Use `give`/`want` prefixes. Avoid complex logic inside subtests.
- **Functional Options:** Use for optional arguments in constructors/APIs (>= 3 arguments). Use an `Option` interface and an unexported `options` struct.

## Tooling & Verification
- **Tooling (Go 1.24+):** Prefer `go tool <toolname>` for invoking project-local tools.
- **Linting:** Use `golangci-lint` as the runner. Use the configuration in [assets/.golangci.yml](assets/.golangci.yml) as a baseline.
- **Struct Tags:** Always use field tags for marshaled structs (JSON, YAML).
- **Leak Detection:** Use `go.uber.org/goleak` for goroutine leaks.
- **Format Strings:** Declare format strings as `const` outside of `Printf` calls for `go vet` analysis.
- **Printf Naming:** End custom Printf-style functions with `f`.
