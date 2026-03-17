---
name: go-concurrency
description: Go concurrency patterns including goroutine lifecycle management, channel usage, mutex handling, and sync primitives. Use when writing concurrent Go code, spawning goroutines, working with channels, or documenting thread-safety guarantees. Based on Google and Uber Go Style Guides.
---

# Go Concurrency

This skill covers concurrency patterns and best practices from Google's Go Style
Guide and Uber's Go Style Guide, including goroutine management, channel usage,
mutex handling, and synchronization.

---

## Goroutine Lifetimes

> **Normative**: When you spawn goroutines, make it clear when or whether they
> exit.

### Why Goroutine Lifetimes Matter

Goroutines can leak by blocking on channel sends or receives. The garbage
collector **will not terminate** a goroutine blocked on a channel even if no
other goroutine has a reference to the channel.

Even when goroutines do not leak, leaving them in-flight when no longer needed
causes:
- **Panics**: Sending on a closed channel causes a panic
- **Data races**: Modifying still-in-use inputs after the result isn't needed
- **Memory issues**: Unpredictable memory usage from long-lived goroutines
- **Resource leaks**: Preventing unused objects from being garbage collected

```go
// Bad: Sending on closed channel causes panic
ch := make(chan int)
ch <- 42
close(ch)
ch <- 13 // panic
```

### Make Lifetimes Obvious

Write concurrent code so goroutine lifetimes are evident. Keep
synchronization-related code constrained within function scope and factor logic
into synchronous functions.

```go
// Good: Goroutine lifetimes are clear
func (w *Worker) Run(ctx context.Context) error {
    var wg sync.WaitGroup
    for item := range w.q {
        wg.Add(1)
        go func() {
            defer wg.Done()
            process(ctx, item) // Returns when context is cancelled
        }()
    }
    wg.Wait() // Prevent spawned goroutines from outliving this function
}
```

```go
// Bad: Careless about when goroutines finish
func (w *Worker) Run() {
    for item := range w.q {
        go process(item) // When does this finish? What if it never does?
    }
}
```

### Don't Fire-and-Forget Goroutines

Every goroutine must have a predictable stop mechanism:
- A predictable time at which it will stop running, OR
- A way to signal that it should stop
- Code must be able to block and wait for the goroutine to finish

> **Source**: Uber Go Style Guide

```go
// Bad: No way to stop or wait for this goroutine
go func() {
    for {
        flush()
        time.Sleep(delay)
    }
}()
```

```go
// Good: Stop/done channel pattern for controlled shutdown
var (
    stop = make(chan struct{}) // tells the goroutine to stop
    done = make(chan struct{}) // tells us that the goroutine exited
)
go func() {
    defer close(done)
    ticker := time.NewTicker(delay)
    defer ticker.Stop()
    for {
        select {
        case <-ticker.C:
            flush()
        case <-stop:
            return
        }
    }
}()

// To shut down:
close(stop)  // signal the goroutine to stop
<-done       // and wait for it to exit
```

### Waiting for Goroutines

Use `sync.WaitGroup` for multiple goroutines:

```go
var wg sync.WaitGroup
for i := 0; i < N; i++ {
    wg.Add(1)
    go func() {
        defer wg.Done()
        // work...
    }()
}
wg.Wait()
```

Use a done channel for a single goroutine:

```go
done := make(chan struct{})
go func() {
    defer close(done)
    // work...
}()
<-done // wait for goroutine to finish
```

### No Goroutines in init()

`init()` functions should not spawn goroutines. If a package needs a background
goroutine, expose an object that manages the goroutine's lifetime with a method
(`Close`, `Stop`, `Shutdown`) to stop and wait for it.

> **Source**: Uber Go Style Guide

```go
// Bad: Spawns uncontrollable background goroutine
func init() {
    go doWork()
}
```

```go
// Good: Explicit lifecycle management
type Worker struct {
    stop chan struct{}
    done chan struct{}
}

func NewWorker() *Worker {
    w := &Worker{
        stop: make(chan struct{}),
        done: make(chan struct{}),
    }
    go w.doWork()
    return w
}

func (w *Worker) Shutdown() {
    close(w.stop)
    <-w.done
}
```

### Testing for Goroutine Leaks

Use [go.uber.org/goleak](https://pkg.go.dev/go.uber.org/goleak) to test for
goroutine leaks in packages that spawn goroutines.

> **Principle**: Never start a goroutine without knowing how it will stop.

---

## Zero-value Mutexes

The zero-value of `sync.Mutex` and `sync.RWMutex` is valid, so you almost never
need a pointer to a mutex.

> **Source**: Uber Go Style Guide

```go
// Bad: Unnecessary pointer
mu := new(sync.Mutex)
mu.Lock()
```

```go
// Good: Zero-value is valid
var mu sync.Mutex
mu.Lock()
```

### Don't Embed Mutexes

If you use a struct by pointer, the mutex should be a non-pointer field. Do not
embed the mutex on the struct, even if the struct is not exported.

```go
// Bad: Embedded mutex exposes Lock/Unlock as part of API
type SMap struct {
    sync.Mutex // Lock() and Unlock() become methods of SMap
    data map[string]string
}

func (m *SMap) Get(k string) string {
    m.Lock()
    defer m.Unlock()
    return m.data[k]
}
```

```go
// Good: Named field keeps mutex as implementation detail
type SMap struct {
    mu   sync.Mutex
    data map[string]string
}

func (m *SMap) Get(k string) string {
    m.mu.Lock()
    defer m.mu.Unlock()
    return m.data[k]
}
```

With the bad example, `Lock` and `Unlock` methods are unintentionally part of
the exported API. With the good example, the mutex is an implementation detail
hidden from callers.

---

## Synchronous Functions

> **Normative**: Prefer synchronous functions over asynchronous functions.

### Why Prefer Synchronous Functions?

1. **Localized goroutines**: Keeps goroutines within a call, making lifetimes
   easier to reason about
2. **Avoids leaks and races**: Easier to prevent resource leaks and data races
3. **Easier to test**: Caller can pass input and check output without polling
4. **Caller flexibility**: Caller can add concurrency by calling in a separate
   goroutine

```go
// Good: Synchronous function - caller controls concurrency
func ProcessItems(items []Item) ([]Result, error) {
    var results []Result
    for _, item := range items {
        result, err := processItem(item)
        if err != nil {
            return nil, err
        }
        results = append(results, result)
    }
    return results, nil
}

// Caller can add concurrency if needed:
go func() {
    results, err := ProcessItems(items)
    // handle results
}()
```

> **Advisory**: It is quite difficult (sometimes impossible) to remove
> unnecessary concurrency at the caller side. Let the caller add concurrency
> when needed.

---

## Channel Direction

> **Normative**: Specify channel direction where possible.

### Why Specify Direction?

1. **Prevents errors**: Compiler catches mistakes like closing a receive-only
   channel
2. **Conveys ownership**: Makes clear who sends and who receives
3. **Self-documenting**: Function signature tells the story

```go
// Good: Direction specified - clear ownership
func sum(values <-chan int) int {
    total := 0
    for v := range values {
        total += v
    }
    return total
}
```

```go
// Bad: No direction - allows accidental misuse
func sum(values chan int) (out int) {
    for v := range values {
        out += v
    }
    close(values) // Bug! This compiles but shouldn't happen.
}
```

### Channel Size: One or None

Channels should usually have a size of one or be unbuffered. Any other size must
be subject to scrutiny. Consider:
- How is the size determined?
- What prevents the channel from filling up under load?
- What happens when writers block?

> **Source**: Uber Go Style Guide

```go
// Bad: Arbitrary buffer size
c := make(chan int, 64) // "Ought to be enough for anybody!"
```

```go
// Good: Deliberate sizing
c := make(chan int, 1) // Size of one
c := make(chan int)    // Unbuffered, size of zero
```

### Common Patterns

```go
func produce(out chan<- int) { /* send-only */ }
func consume(in <-chan int)  { /* receive-only */ }
func transform(in <-chan int, out chan<- int) { /* both directions */ }
```

---

## Atomic Operations

Use [go.uber.org/atomic](https://pkg.go.dev/go.uber.org/atomic) for type-safe
atomic operations. The standard `sync/atomic` package operates on raw types
(`int32`, `int64`, etc.), making it easy to forget to use atomic operations
consistently.

> **Source**: Uber Go Style Guide

```go
// Bad: Easy to forget atomic operation
type foo struct {
    running int32 // atomic
}

func (f *foo) start() {
    if atomic.SwapInt32(&f.running, 1) == 1 {
        return // already running
    }
    // start the Foo
}

func (f *foo) isRunning() bool {
    return f.running == 1 // race! forgot atomic.LoadInt32
}
```

```go
// Good: Type-safe atomic operations
type foo struct {
    running atomic.Bool
}

func (f *foo) start() {
    if f.running.Swap(true) {
        return // already running
    }
    // start the Foo
}

func (f *foo) isRunning() bool {
    return f.running.Load() // can't accidentally read non-atomically
}
```

The `go.uber.org/atomic` package adds type safety by hiding the underlying type
and includes convenient types like `atomic.Bool`, `atomic.Int64`, etc.

---

## Documenting Concurrency

> **Advisory**: Document thread-safety when it's not obvious from the operation
> type.

Go users assume read-only operations are safe for concurrent use, and mutating
operations are not. Document concurrency when:

1. **Read vs mutating is unclear** - e.g., a `Lookup` that mutates LRU state
2. **API provides synchronization** - e.g., thread-safe clients
3. **Interface has concurrency requirements** - document in type definition

---

## Buffer Pooling with Channels

Use a buffered channel as a free list to reuse allocated buffers. This "leaky
buffer" pattern uses `select` with `default` for non-blocking operations.

See [references/BUFFER-POOLING.md](references/BUFFER-POOLING.md) for the full
pattern with examples and production alternatives using `sync.Pool`.

---

## Quick Reference

| Topic | Guidance | Type |
|-------|----------|------|
| Goroutine lifetimes | Make exit conditions clear | Normative |
| Fire-and-forget | Don't do it - always have stop mechanism | Normative |
| Zero-value mutexes | Valid; don't use pointers | Advisory |
| Mutex embedding | Don't embed; use named field | Advisory |
| Synchronous functions | Prefer over async | Normative |
| Channel direction | Always specify | Normative |
| Channel size | One or none by default | Advisory |
| Atomic operations | Use go.uber.org/atomic | Advisory |
| Concurrency docs | Document when not obvious | Advisory |

### Concurrency Checklist

Before spawning a goroutine, answer:
- [ ] How will this goroutine exit?
- [ ] Can I signal it to stop?
- [ ] Can I wait for it to finish?
- [ ] Who owns the channels it uses?
- [ ] What happens when the context is cancelled?
- [ ] Should this be a synchronous function instead?

### Anti-Patterns to Avoid

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| Fire-and-forget goroutines | Resource leaks, undefined behavior | Use WaitGroup, done channel, or context |
| Goroutines in init() | Uncontrollable lifecycle | Use explicit object with Shutdown method |
| Embedded mutexes | Leaks Lock/Unlock into API | Use named `mu` field |
| Pointer to mutex | Unnecessary indirection | Zero-value is valid |
| Arbitrary channel buffers | Hidden blocking issues | Default to 0 or 1 |
| Raw sync/atomic | Easy to forget atomic reads | Use go.uber.org/atomic |
| Undocumented thread-safety | Callers may race | Document when unclear |

---

## See Also

- **go-style-core**: Foundational style principles (clarity, simplicity)
- **go-error-handling**: Error handling patterns in concurrent code
- **go-defensive**: Defensive programming including validation and safety
- **go-documentation**: General documentation conventions

### External Resources

- [Never start a goroutine without knowing how it will
  stop](https://dave.cheney.net/2016/12/22/never-start-a-goroutine-without-knowing-how-it-will-stop)
  - Dave Cheney
- [Rethinking Classical Concurrency
  Patterns](https://www.youtube.com/watch?v=5zXAHh5tJqQ) - Bryan Mills
  (GopherCon 2018)
- [When Go programs end](https://changelog.com/gotime/165) - Go Time podcast
- [go.uber.org/goleak](https://pkg.go.dev/go.uber.org/goleak) - Goroutine leak
  detector for testing
- [go.uber.org/atomic](https://pkg.go.dev/go.uber.org/atomic) - Type-safe atomic
  operations
