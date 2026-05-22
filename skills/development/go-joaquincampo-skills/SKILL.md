---
name: go
description: "Go engineering best practices and idioms. This skill should be used when writing, reviewing, or refactoring Go code. Triggers on any .go file work, Go module operations, go test, go build, go run, go vet, go generate, or when the user mentions Go, golang, goroutines, channels, context, Go interfaces, Go error handling, Go testing, or Go concurrency. ALWAYS use this skill when Go code is involved, even for simple functions."
---

# Go Engineering Doctrine

Write Go that is explicit, boring, concrete, package-oriented, easy to test, easy to operate, and hard to misunderstand.

## Worldview

- Simplicity over cleverness
- Explicit over implicit
- Concrete over abstract
- Mechanical consistency over personal style
- Small surfaces over sprawling frameworks
- Boring code over surprising code

When in doubt, choose the option that makes the code easier to read, easier to test, and easier to change in six months.

## Canonical Defaults

- The standard library is the default. Every dependency must earn its place.
- `gofmt` is mandatory. No style debates. Formatting is solved mechanically.
- `go test` is the default test runner. `go test -race` for concurrency-sensitive code.
- `context.Context` is mandatory for request-scoped operations that may block or be canceled.
- `slog` for structured logging unless there is a clear reason not to.
- `staticcheck` is the default static analyzer.

---

## Reference Selection Guide

Read the relevant reference files before writing or reviewing code in that area.

| Task | Reference | Key Topics |
|------|-----------|------------|
| Error handling, wrapping, sentinel errors | `references/errors.md` | `%w`, `errors.Is`/`As`, log-or-return rule, error chains |
| Writing or reviewing tests | `references/testing.md` | Table-driven tests, httptest, mocking strategy, race detection, benchmarks |
| Goroutines, channels, synchronization | `references/concurrency.md` | Goroutine lifecycle, context cancellation, errgroup, channels vs mutexes |
| Creating packages, naming, project layout | `references/packages.md` | Package naming, export discipline, cmd/internal layout, avoiding circular imports |
| HTTP handlers, middleware, servers | `references/http.md` | Thin handlers, decode-validate-call-encode pattern, middleware, graceful shutdown |
| Setting up or configuring linters | `references/linting.md` | gofmt, staticcheck, golangci-lint config, recommended linter set |
| Considering or writing generics | `references/generics.md` | Concrete-first rule, good/bad uses, type constraints, common patterns |
| Configuration loading, env vars, startup | `references/config.md` | Explicit structs, validation at load, passing config pieces, secrets |
| Interface design, abstraction decisions | `references/interfaces.md` | Consumer-side interfaces, small interfaces, when to use/avoid |

**For general code review**, read: `references/errors.md`, `references/packages.md`, `references/interfaces.md`.

**For new service scaffolding**, read: `references/packages.md`, `references/http.md`, `references/config.md`.

**For debugging concurrency issues**, read: `references/concurrency.md`, `references/testing.md`.

**For refactoring or restructuring**, read: `references/packages.md`, `references/interfaces.md`, `references/errors.md`.

---

## Core Rules (Always Apply)

### 1. Standard Library First

Start with the standard library. Do not import a library to save a few lines. Good reasons to add a dependency: materially better correctness, interoperability, observability, or developer productivity in a repeated pattern. Bad reasons: "everyone uses it" or "the stdlib is verbose."

### 2. Favor Concrete Types

Accept and return concrete types by default. Introduce interfaces only when they simplify a real boundary. Do not design around imagined future implementations.

### 3. Interfaces Belong Where Consumed

Define interfaces in the package that uses them, not the package that implements them. Keep interfaces small. One-method interfaces are often ideal. If there is only one implementation and no real substitution boundary, skip the interface.

### 4. Errors Are Values

Handle errors explicitly. Wrap with context via `fmt.Errorf("operation: %w", err)`. Use `errors.Is`/`errors.As` for comparison. Log at process boundaries, not everywhere. Never discard errors silently.

### 5. Panic Is for Programmer Errors Only

Acceptable: impossible internal invariants, irrecoverable startup failures. Not acceptable: I/O failure, validation failure, request handling, control flow.

### 6. Context for Cancellation and Deadlines

Pass `context.Context` as the first parameter when work may block or be canceled. Do not store context in structs. Do not use context as a dependency bag.

### 7. Concurrency Is for Coordination

Every goroutine must have a lifecycle. Every spawned goroutine must be cancellable, bounded, or intentionally fire-and-forget. If sequential code is fast enough, keep it sequential.

### 8. Generics Are Not the Starting Point

Write the concrete version first. Use generics when they remove real duplication. If the generic version is harder to explain than the concrete version, prefer concrete.

### 9. Validate at Boundaries

Validate external input at ingress (HTTP handlers, CLI parsing, config loading, queue consumers). After validation, internal code assumes stronger invariants.

### 10. Keep Package APIs Small

Export the minimum. Keep implementation details unexported. Every exported name is a maintenance burden and a compatibility promise.

### 11. HTTP Handlers Should Be Thin

Handlers: decode input, validate, call application logic, encode output, map errors. Handlers should not: contain business workflows, direct SQL, hidden retries, or orchestrate the system.

### 12. Testing Is Part of Design

Prefer table-driven tests where they improve clarity. Test behavior, not implementation trivia. Prefer real types over mocks unless the boundary is expensive or external.

### 13. Logging Serves Operations

Prefer structured logs. Log at meaningful boundaries. Do not spam for every successful step. Do not both log and bubble the same error. Never log secrets.

### 14. Structs Are Data; Methods Are for Cohesion

Keep structs simple. Put methods on a type when behavior truly belongs to that type. Do not turn every data shape into an object with a large method set. Do not hide business workflows inside transport structs.

### 15. Prefer Explicit Constructors Only When They Add Value

Use a constructor when you need to enforce invariants, inject dependencies, or set safe defaults. Do not write constructors for every struct just because other languages do.

### 16. Reflection Is a Last Resort

Avoid reflection unless clearly necessary. If used, isolate it tightly and document why. Prefer explicit code over clever reflection.

### 17. Public APIs Evolve by Addition

For reusable packages: add, do not change or remove. Think about compatibility before exporting. Every public API is a promise.

---

## Red Flags

These indicate non-idiomatic or overengineered Go:

- Interfaces everywhere / giant "service" interfaces
- `util`, `common`, `helpers` packages
- Reflection in business logic
- Generics before concrete code exists
- Context stored on structs
- Hidden globals
- Panics in normal control flow
- Handlers full of business logic
- Excessive framework usage
- Logging at every stack layer
- Unbounded goroutines
- Channels where a mutex or plain function call would do
- Large exported surfaces with unclear compatibility intent

---

## Modus Operandi

1. Beautiful over ugly: tidy packages, short files, clear names, consistent formatting.
2. Explicit over implicit: state assumptions, make control flow obvious.
3. Simple over complex: use the simplest design that fully solves the problem.
4. Flat over nested: keep control flow shallow, prefer early returns.
5. Sparse over dense: short functions, small package APIs, concise comments.
6. Readability counts: optimize for the next reader, not the current author.
7. Practicality beats purity: use the boring, reliable solution first.
8. Errors must not pass silently: handle explicitly, wrap with context, return meaningfully.
9. One obvious way: recommend one best path, not five equal ones.
10. Now over never: deliver a correct, minimal solution first.
11. Never over right now: if something is unsafe or fragile, stop and say so.
12. Hard to explain equals bad idea: if the approach cannot be justified simply, simplify it.
