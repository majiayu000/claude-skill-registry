---
name: go-concurrency
description: Use when writing concurrent Go code — goroutines, channels, mutexes, or thread-safety guarantees. Also use when parallelizing work, fixing data races, or protecting shared state, even if the user doesn't explicitly mention concurrency primitives. Does not cover context.Context patterns (see go-context).
license: Apache-2.0
compatibility: Requires go.uber.org/atomic for atomic operation wrappers
metadata:
  sources: "Effective Go, Google Style Guide, Uber Style Guide"
---

# Go Concurrency

## Goroutine Lifetimes

> **Normative**: When you spawn goroutines, make it clear when or whether they
> exit.

Goroutines can leak by blocking on channel sends/receives. The GC **will not
terminate** a blocked goroutine even if no other goroutine holds a reference to
the channel. Even non-leaking in-flight goroutines cause panics (send on closed
channel), data races, memory issues, and resource leaks.

### Core Rules

1. **Every goroutine needs a stop mechanism** — a predictable end time, a
   cancellation signal, or both
2. **Code must be able to wait** for the goroutine to finish
3. **No goroutines in `init()`** — expose lifecycle methods (`Close`, `Stop`,
   `Shutdown`) instead
4. **Keep synchronization scoped** — constrain to function scope, factor logic
   into synchronous functions

```go
// Good: Clear lifetime with WaitGroup
var wg sync.WaitGroup
for item := range queue {
    wg.Add(1)
    go func() { defer wg.Done(); process(ctx, item) }()
}
wg.Wait()
```

```go
// Bad: No way to stop or wait
go func() { for { flush(); time.Sleep(delay) } }()
```

**Test for leaks** with [go.uber.org/goleak](https://pkg.go.dev/go.uber.org/goleak).

> **Principle**: Never start a goroutine without knowing how it will stop.

> Read [references/GOROUTINE-PATTERNS.md](references/GOROUTINE-PATTERNS.md) when
> implementing stop/done channel patterns, goroutine waiting strategies, or
> lifecycle-managed workers.

---

## Share by Communicating

> "Do not communicate by sharing memory; instead, share memory by communicating."

This is Go's foundational concurrency design principle. Use **channels** for
ownership transfer and orchestration — when one goroutine produces a value and
another consumes it. Use **mutexes** when multiple goroutines access shared
state and channels would add unnecessary complexity.

**Default to channels.** Fall back to `sync.Mutex` / `sync.RWMutex` when the
problem is naturally about protecting a shared data structure (e.g., a cache or
counter) rather than passing data between goroutines.

---

## Synchronous Functions

> **Normative**: Prefer synchronous functions over asynchronous ones.

| Benefit | Why |
|---|---|
| Localized goroutines | Lifetimes easier to reason about |
| Avoids leaks and races | Easier to prevent resource leaks and data races |
| Easier to test | Check input/output without polling |
| Caller flexibility | Caller adds concurrency when needed |

> **Advisory**: It is quite difficult (sometimes impossible) to remove
> unnecessary concurrency at the caller side. Let the caller add concurrency
> when needed.

> Read [references/GOROUTINE-PATTERNS.md](references/GOROUTINE-PATTERNS.md) when
> writing synchronous-first APIs that callers may wrap in goroutines.

---

## Zero-value Mutexes

The zero-value of `sync.Mutex` and `sync.RWMutex` is valid — almost never need
a pointer to a mutex.

```go
// Good: Zero-value is valid    // Bad: Unnecessary pointer
var mu sync.Mutex                mu := new(sync.Mutex)
```

**Don't embed mutexes** — use a named `mu` field to keep `Lock`/`Unlock` as
implementation details, not exported API.

> Read [references/SYNC-PRIMITIVES.md](references/SYNC-PRIMITIVES.md) when
> implementing mutex-protected structs or deciding how to structure mutex fields.

---

## Channel Direction

> **Normative**: Specify channel direction where possible.

Direction prevents errors (compiler catches closing a receive-only channel),
conveys ownership, and is self-documenting.

```go
func produce(out chan<- int) { /* send-only */ }
func consume(in <-chan int)  { /* receive-only */ }
func transform(in <-chan int, out chan<- int) { /* both */ }
```

### Channel Size: One or None

Channels should have size **zero** (unbuffered) or **one**. Any other size
requires justification for:

- How the size was determined
- What prevents the channel from filling under load
- What happens when writers block

```go
c := make(chan int)    // unbuffered — Good
c := make(chan int, 1) // size one — Good
c := make(chan int, 64) // arbitrary — needs justification
```

> Read [references/SYNC-PRIMITIVES.md](references/SYNC-PRIMITIVES.md) when
> reviewing detailed channel direction examples with error-prone patterns.

---

## Atomic Operations

Use `atomic.Bool`, `atomic.Int64`, etc. (stdlib `sync/atomic` since Go 1.19, or
[go.uber.org/atomic](https://pkg.go.dev/go.uber.org/atomic)) for type-safe
atomic operations. Raw `int32`/`int64` fields make it easy to forget atomic
access on some code paths.

```go
// Good: Type-safe              // Bad: Easy to forget
var running atomic.Bool          var running int32 // atomic
running.Store(true)              atomic.StoreInt32(&running, 1)
running.Load()                   running == 1 // race!
```

> Read [references/SYNC-PRIMITIVES.md](references/SYNC-PRIMITIVES.md) when
> choosing between sync/atomic and go.uber.org/atomic, or implementing atomic
> state flags in structs.

---

## Documenting Concurrency

> **Advisory**: Document thread-safety when it's not obvious from the operation
> type.

Go users assume read-only operations are safe for concurrent use, and mutating
operations are not. Document concurrency when:

1. **Read vs mutating is unclear** — e.g., a `Lookup` that mutates LRU state
2. **API provides synchronization** — e.g., thread-safe clients
3. **Interface has concurrency requirements** — document in type definition

---

## Context Usage

> For context.Context guidance (parameter placement, struct storage, custom
> types, derivation patterns), see the dedicated
> [go-context](../go-context/SKILL.md) skill.

---

## Buffer Pooling with Channels

Use a buffered channel as a free list to reuse allocated buffers. This "leaky
buffer" pattern uses `select` with `default` for non-blocking operations.

> Read [references/BUFFER-POOLING.md](references/BUFFER-POOLING.md) when
> implementing a worker pool with reusable buffers or choosing between
> channel-based pools and `sync.Pool`.

---

## Advanced Patterns

> Read [references/ADVANCED-PATTERNS.md](references/ADVANCED-PATTERNS.md) when
> implementing request-response multiplexing with channels of channels, or
> CPU-bound parallel computation across cores.

---

## Related Skills

- **Context propagation**: See [go-context](../go-context/SKILL.md) when passing cancellation, deadlines, or request-scoped values through goroutines
- **Error handling**: See [go-error-handling](../go-error-handling/SKILL.md) when propagating errors from goroutines or using errgroup
- **Defensive hardening**: See [go-defensive](../go-defensive/SKILL.md) when protecting shared state at API boundaries or using defer for cleanup
- **Interface design**: See [go-interfaces](../go-interfaces/SKILL.md) when choosing receiver types for types with sync primitives

### External Resources

- [Never start a goroutine without knowing how it will
  stop](https://dave.cheney.net/2016/12/22/never-start-a-goroutine-without-knowing-how-it-will-stop)
  — Dave Cheney
- [Rethinking Classical Concurrency
  Patterns](https://www.youtube.com/watch?v=5zXAHh5tJqQ) — Bryan Mills
  (GopherCon 2018)
- [When Go programs end](https://changelog.com/gotime/165) — Go Time podcast
- [go.uber.org/goleak](https://pkg.go.dev/go.uber.org/goleak) — Goroutine leak
  detector for testing
- [go.uber.org/atomic](https://pkg.go.dev/go.uber.org/atomic) — Type-safe
  atomic operations
