---
name: concurrency-patterns-go
description: >
  Apply safe, idiomatic Go concurrency patterns with goroutines and channels.
  Use when the user works with goroutines, channels, sync primitives, context
  cancellation, worker pools, fan-in/fan-out, select statements, or asks about
  concurrent Go programming and avoiding race conditions.
---

# Go Concurrency Patterns

Write safe, efficient concurrent Go code using goroutines, channels, sync
primitives, and context-based cancellation.

## When to Use
- Processing items concurrently (HTTP requests, file I/O, computations)
- Building worker pools for bounded concurrency
- Coordinating multiple goroutines with channels or sync primitives
- Implementing timeouts and cancellation with context.Context
- Designing fan-in/fan-out data pipelines

## Core Patterns

### Pattern 1: Goroutines with sync.WaitGroup

Spawn goroutines and wait for all to complete.

```go
func processItems(items []Item) error {
    var (
        wg   sync.WaitGroup
        mu   sync.Mutex
        errs []error
    )

    for _, item := range items {
        wg.Add(1)
        go func() {
            defer wg.Done()
            if err := process(item); err != nil {
                mu.Lock()
                errs = append(errs, fmt.Errorf("item %s: %w", item.ID, err))
                mu.Unlock()
            }
        }()
    }

    wg.Wait()
    return errors.Join(errs...)
}
```

### Pattern 2: Worker Pool with Bounded Concurrency

Limit concurrent work to avoid overwhelming resources.

```go
func workerPool(ctx context.Context, jobs <-chan Job, workers int) <-chan Result {
    results := make(chan Result, workers)

    var wg sync.WaitGroup
    for range workers {
        wg.Add(1)
        go func() {
            defer wg.Done()
            for job := range jobs {
                select {
                case <-ctx.Done():
                    return
                default:
                    result, err := processJob(ctx, job)
                    if err != nil {
                        results <- Result{Err: err}
                        continue
                    }
                    results <- Result{Data: result}
                }
            }
        }()
    }

    go func() {
        wg.Wait()
        close(results)
    }()

    return results
}

// Usage
func run(ctx context.Context) error {
    jobs := make(chan Job, 100)

    go func() {
        defer close(jobs)
        for _, j := range allJobs {
            select {
            case jobs <- j:
            case <-ctx.Done():
                return
            }
        }
    }()

    for result := range workerPool(ctx, jobs, 10) {
        if result.Err != nil {
            slog.Error("job failed", "error", result.Err)
            continue
        }
        handleResult(result.Data)
    }
    return nil
}
```

### Pattern 3: Fan-Out / Fan-In

Distribute work across multiple goroutines (fan-out), then merge results (fan-in).

```go
// Fan-out: send work to multiple processors
func fanOut(ctx context.Context, input <-chan Data, n int) []<-chan Result {
    outputs := make([]<-chan Result, n)
    for i := range n {
        outputs[i] = processStream(ctx, input)
    }
    return outputs
}

// Fan-in: merge multiple channels into one
func fanIn(ctx context.Context, channels ...<-chan Result) <-chan Result {
    merged := make(chan Result)
    var wg sync.WaitGroup

    for _, ch := range channels {
        wg.Add(1)
        go func() {
            defer wg.Done()
            for val := range ch {
                select {
                case merged <- val:
                case <-ctx.Done():
                    return
                }
            }
        }()
    }

    go func() {
        wg.Wait()
        close(merged)
    }()

    return merged
}
```

### Pattern 4: Context for Cancellation and Timeouts

Use context.Context to propagate deadlines and cancellation signals.

```go
func fetchWithTimeout(url string) ([]byte, error) {
    ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
    defer cancel()

    req, err := http.NewRequestWithContext(ctx, http.MethodGet, url, nil)
    if err != nil {
        return nil, fmt.Errorf("creating request: %w", err)
    }

    resp, err := http.DefaultClient.Do(req)
    if err != nil {
        return nil, fmt.Errorf("fetching %s: %w", url, err)
    }
    defer resp.Body.Close()

    return io.ReadAll(resp.Body)
}

// Graceful shutdown with context
func serve(ctx context.Context) error {
    srv := &http.Server{Addr: ":8080"}

    go func() {
        <-ctx.Done()
        shutdownCtx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
        defer cancel()
        srv.Shutdown(shutdownCtx)
    }()

    if err := srv.ListenAndServe(); err != http.ErrServerClosed {
        return fmt.Errorf("server error: %w", err)
    }
    return nil
}
```

### Pattern 5: Select Statement

Multiplex across multiple channel operations with non-blocking semantics.

```go
func monitor(ctx context.Context, data <-chan Event, ticks <-chan time.Time) error {
    for {
        select {
        case <-ctx.Done():
            return ctx.Err()

        case event, ok := <-data:
            if !ok {
                return nil // channel closed, done
            }
            if err := handleEvent(event); err != nil {
                return fmt.Errorf("handling event: %w", err)
            }

        case <-ticks:
            reportHealth()
        }
    }
}

// Non-blocking send
func trySend(ch chan<- Event, event Event) bool {
    select {
    case ch <- event:
        return true
    default:
        return false // channel full, drop or buffer
    }
}
```

### Pattern 6: Semaphore Pattern with Buffered Channels

Use a buffered channel as a simple semaphore for bounded concurrency
without a full worker pool.

```go
func processAll(ctx context.Context, items []Item, maxConcurrency int) error {
    sem := make(chan struct{}, maxConcurrency)
    g, ctx := errgroup.WithContext(ctx)

    for _, item := range items {
        sem <- struct{}{} // acquire
        g.Go(func() error {
            defer func() { <-sem }() // release
            return process(ctx, item)
        })
    }

    return g.Wait()
}
```

## Anti-Patterns

- **Goroutine leaks** -- Every goroutine must have a clear exit path. Always use
  context cancellation or channel closing to signal goroutines to stop.
  ```go
  // BAD: leaked goroutine if ctx is never cancelled
  go func() {
      for { doWork() }
  }()
  // GOOD
  go func() {
      for {
          select {
          case <-ctx.Done():
              return
          default:
              doWork()
          }
      }
  }()
  ```

- **Shared state without synchronization** -- Use channels for communication between
  goroutines, or protect shared data with `sync.Mutex`. Never read/write shared
  variables without coordination.

- **Closing channels from the receiver side** -- Only the sender should close a channel.
  Closing from the receiver causes panics if the sender writes again.

- **Unbounded goroutine spawning** -- Launching one goroutine per item in a large
  collection causes resource exhaustion. Use worker pools or semaphores.

- **Mixing mutexes and channels** -- Pick one coordination style per component.
  Mixing both creates complex, hard-to-reason-about code.

## Quick Reference

| Pattern | When to Use |
|---------|-------------|
| WaitGroup | Wait for N goroutines to finish |
| Worker pool | Bounded concurrency over a job stream |
| Fan-out/fan-in | Parallel processing with merged results |
| Context | Timeouts, cancellation, deadline propagation |
| Select | Multiplex channels, non-blocking ops |
| Semaphore (buffered chan) | Simple concurrency limiting |
| errgroup | Concurrent tasks with first-error-wins |

Always: `defer cancel()` after `context.WithTimeout/WithCancel`.
Always: `defer wg.Done()` at the top of goroutine functions.
