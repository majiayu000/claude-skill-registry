---
name: go-concurrency
model: standard
description: Production Go concurrency patterns — goroutines, channels, sync primitives, context, worker pools, pipelines, and graceful shutdown. Use when building concurrent Go applications or debugging race conditions.
---

# Go Concurrency Patterns

Production patterns for Go concurrency including goroutines, channels, synchronization primitives, and context management.


## Installation

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install go-concurrency
```


## When to Use

- Building concurrent Go applications
- Implementing worker pools and pipelines
- Managing goroutine lifecycles and cancellation
- Debugging race conditions
- Implementing graceful shutdown

## Concurrency Primitives

| Primitive         | Purpose                          | When to Use                         |
| ----------------- | -------------------------------- | ----------------------------------- |
| `goroutine`       | Lightweight concurrent execution | Any concurrent work                 |
| `channel`         | Communication between goroutines | Passing data, signaling             |
| `select`          | Multiplex channel operations     | Waiting on multiple channels        |
| `sync.Mutex`      | Mutual exclusion                 | Protecting shared state             |
| `sync.WaitGroup`  | Wait for goroutines to complete  | Coordinating goroutine completion   |
| `context.Context` | Cancellation and deadlines       | Request-scoped lifecycle management |
| `errgroup.Group`  | Concurrent tasks with errors     | Parallel work that can fail         |

**Go Concurrency Mantra:** Don't communicate by sharing memory; share memory by communicating.

## Quick Start

```go
func main() {
    ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
    defer cancel()

    results := make(chan string, 10)
    var wg sync.WaitGroup

    for i := 0; i < 3; i++ {
        wg.Add(1)
        go func(id int) {
            defer wg.Done()
            select {
            case <-ctx.Done():
                return
            case results <- fmt.Sprintf("Worker %d done", id):
            }
        }(i)
    }

    go func() { wg.Wait(); close(results) }()

    for result := range results {
        fmt.Println(result)
    }
}
```

## Pattern 1: Worker Pool

```go
type Job struct {
    ID   int
    Data string
}

type Result struct {
    JobID  int
    Output string
    Err    error
}

func WorkerPool(ctx context.Context, numWorkers int, jobs <-chan Job) <-chan Result {
    results := make(chan Result)
    var wg sync.WaitGroup

    for i := 0; i < numWorkers; i++ {
        wg.Add(1)
        go func() {
            defer wg.Done()
            for job := range jobs {
                select {
                case <-ctx.Done():
                    return
                default:
                    results <- Result{
                        JobID:  job.ID,
                        Output: fmt.Sprintf("Processed: %s", job.Data),
                    }
                }
            }
        }()
    }

    go func() { wg.Wait(); close(results) }()
    return results
}

// Usage
func main() {
    ctx, cancel := context.WithCancel(context.Background())
    defer cancel()

    jobs := make(chan Job, 100)
    go func() {
        for i := 0; i < 50; i++ {
            jobs <- Job{ID: i, Data: fmt.Sprintf("job-%d", i)}
        }
        close(jobs)
    }()

    for result := range WorkerPool(ctx, 5, jobs) {
        fmt.Printf("Result: %+v\n", result)
    }
}
```

## Pattern 2: Fan-Out / Fan-In Pipeline

```go
// Stage 1: Generate values
func generate(ctx context.Context, nums ...int) <-chan int {
    out := make(chan int)
    go func() {
        defer close(out)
        for _, n := range nums {
            select {
            case <-ctx.Done(): return
            case out <- n:
            }
        }
    }()
    return out
}

// Stage 2: Transform (run multiple instances for fan-out)
func square(ctx context.Context, in <-chan int) <-chan int {
    out := make(chan int)
    go func() {
        defer close(out)
        for n := range in {
            select {
            case <-ctx.Done(): return
            case out <- n * n:
            }
        }
    }()
    return out
}

// Fan-in: Merge multiple channels into one
func merge(ctx context.Context, channels ...<-chan int) <-chan int {
    var wg sync.WaitGroup
    out := make(chan int)

    wg.Add(len(channels))
    for _, ch := range channels {
        go func(c <-chan int) {
            defer wg.Done()
            for n := range c {
                select {
                case <-ctx.Done(): return
                case out <- n:
                }
            }
        }(ch)
    }

    go func() { wg.Wait(); close(out) }()
    return out
}

// Usage: fan out to 3 squarers, fan in results
func main() {
    ctx, cancel := context.WithCancel(context.Background())
    defer cancel()

    in := generate(ctx, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
    c1 := square(ctx, in)
    c2 := square(ctx, in)
    c3 := square(ctx, in)

    for result := range merge(ctx, c1, c2, c3) {
        fmt.Println(result)
    }
}
```

## Pattern 3: errgroup with Cancellation

```go
import "golang.org/x/sync/errgroup"

func fetchAllURLs(ctx context.Context, urls []string) ([]string, error) {
    g, ctx := errgroup.WithContext(ctx)
    results := make([]string, len(urls))

    for i, url := range urls {
        i, url := i, url
        g.Go(func() error {
            req, err := http.NewRequestWithContext(ctx, "GET", url, nil)
            if err != nil {
                return fmt.Errorf("creating request for %s: %w", url, err)
            }
            resp, err := http.DefaultClient.Do(req)
            if err != nil {
                return fmt.Errorf("fetching %s: %w", url, err)
            }
            defer resp.Body.Close()
            results[i] = fmt.Sprintf("%s: %d", url, resp.StatusCode)
            return nil
        })
    }

    if err := g.Wait(); err != nil {
        return nil, err // First error cancels all others via ctx
    }
    return results, nil
}

// With concurrency limit
func fetchWithLimit(ctx context.Context, urls []string) ([]string, error) {
    g, ctx := errgroup.WithContext(ctx)
    g.SetLimit(10) // Max concurrent goroutines
    results := make([]string, len(urls))

    for i, url := range urls {
        i, url := i, url
        g.Go(func() error {
            result, err := fetchURL(ctx, url)
            if err != nil { return err }
            results[i] = result
            return nil
        })
    }

    return results, g.Wait()
}
```

## Pattern 4: Bounded Concurrency (Semaphore)

```go
import "golang.org/x/sync/semaphore"

type RateLimitedWorker struct {
    sem *semaphore.Weighted
}

func NewRateLimitedWorker(maxConcurrent int64) *RateLimitedWorker {
    return &RateLimitedWorker{sem: semaphore.NewWeighted(maxConcurrent)}
}

func (w *RateLimitedWorker) Do(ctx context.Context, tasks []func() error) []error {
    var (
        wg     sync.WaitGroup
        mu     sync.Mutex
        errors []error
    )

    for _, task := range tasks {
        if err := w.sem.Acquire(ctx, 1); err != nil {
            return []error{err}
        }
        wg.Add(1)
        go func(t func() error) {
            defer wg.Done()
            defer w.sem.Release(1)
            if err := t(); err != nil {
                mu.Lock()
                errors = append(errors, err)
                mu.Unlock()
            }
        }(task)
    }

    wg.Wait()
    return errors
}

// Simpler alternative: channel-based semaphore
type Semaphore chan struct{}

func NewSemaphore(n int) Semaphore       { return make(chan struct{}, n) }
func (s Semaphore) Acquire()             { s <- struct{}{} }
func (s Semaphore) Release()             { <-s }
```

## Pattern 5: Graceful Shutdown

```go
func main() {
    ctx, cancel := context.WithCancel(context.Background())

    sigCh := make(chan os.Signal, 1)
    signal.Notify(sigCh, syscall.SIGINT, syscall.SIGTERM)

    server := NewServer()
    server.Start(ctx)

    sig := <-sigCh
    fmt.Printf("Received signal: %v\n", sig)
    cancel() // Cancel context to stop all workers

    server.Shutdown(5 * time.Second)
}

type Server struct {
    wg sync.WaitGroup
}

func (s *Server) Start(ctx context.Context) {
    for i := 0; i < 5; i++ {
        s.wg.Add(1)
        go s.worker(ctx, i)
    }
}

func (s *Server) worker(ctx context.Context, id int) {
    defer s.wg.Done()
    ticker := time.NewTicker(time.Second)
    defer ticker.Stop()

    for {
        select {
        case <-ctx.Done():
            fmt.Printf("Worker %d cleaning up...\n", id)
            return
        case <-ticker.C:
            fmt.Printf("Worker %d working...\n", id)
        }
    }
}

func (s *Server) Shutdown(timeout time.Duration) {
    done := make(chan struct{})
    go func() { s.wg.Wait(); close(done) }()

    select {
    case <-done:
        fmt.Println("Clean shutdown completed")
    case <-time.After(timeout):
        fmt.Println("Shutdown timed out, forcing exit")
    }
}
```

## Pattern 6: Concurrent Map

```go
// sync.Map: optimized for read-heavy workloads with stable keys
type Cache struct {
    m sync.Map
}

func (c *Cache) Get(key string) (any, bool) { return c.m.Load(key) }
func (c *Cache) Set(key string, value any) { c.m.Store(key, value) }
func (c *Cache) GetOrSet(key string, val any) (any, bool) {
    return c.m.LoadOrStore(key, val)
}

// ShardedMap: better for write-heavy workloads
type ShardedMap struct {
    shards    []*shard
    numShards int
}

type shard struct {
    sync.RWMutex
    data map[string]any
}

func NewShardedMap(n int) *ShardedMap {
    m := &ShardedMap{shards: make([]*shard, n), numShards: n}
    for i := range m.shards {
        m.shards[i] = &shard{data: make(map[string]any)}
    }
    return m
}

func (m *ShardedMap) getShard(key string) *shard {
    h := 0
    for _, c := range key {
        h = 31*h + int(c)
    }
    return m.shards[h%m.numShards]
}

func (m *ShardedMap) Get(key string) (any, bool) {
    s := m.getShard(key)
    s.RLock()
    defer s.RUnlock()
    v, ok := s.data[key]
    return v, ok
}

func (m *ShardedMap) Set(key string, value any) {
    s := m.getShard(key)
    s.Lock()
    defer s.Unlock()
    s.data[key] = value
}
```

**When to use which:**
- `sync.Map` — Few keys, many reads, keys added once and rarely deleted
- `ShardedMap` — Many keys, frequent writes, need predictable performance

## Select Patterns

```go
// Timeout
select {
case v := <-ch:
    fmt.Println("Received:", v)
case <-time.After(time.Second):
    fmt.Println("Timeout!")
}

// Non-blocking send/receive
select {
case ch <- 42:
    fmt.Println("Sent")
default:
    fmt.Println("Channel full, skipping")
}

// Priority select: check high-priority first
for {
    select {
    case msg := <-highPriority:
        handle(msg)
    default:
        select {
        case msg := <-highPriority:
            handle(msg)
        case msg := <-lowPriority:
            handle(msg)
        }
    }
}
```

## Race Detection

```bash
go test -race ./...     # Tests with race detector
go build -race .        # Build with race detector
go run -race main.go    # Run with race detector
```

## Best Practices

**Do:**
- Use `context.Context` for cancellation and deadlines on every goroutine
- Close channels from the sender side only
- Use `errgroup` for concurrent operations that return errors
- Buffer channels when count is known upfront
- Prefer channels over mutexes for coordination
- Always run tests with `-race`

**Don't:**
- Leak goroutines — every goroutine must have an exit path
- Close a channel from the receiver — causes panic
- Use `time.Sleep` for synchronization — use proper primitives
- Ignore `ctx.Done()` in long-running goroutines
- Share memory without synchronization — use channels or mutexes

## NEVER Do

- **NEVER close a channel from the receiver** — Only the sender should close; receivers panic on closed channels
- **NEVER send on a closed channel** — Causes panic; design so sender controls close
- **NEVER use unbounded goroutine spawning** — Use worker pools or semaphores for bounded concurrency
- **NEVER ignore the `-race` flag in testing** — Data races are silent bugs that corrupt state
- **NEVER pass pointers to loop variables into goroutines** — Capture the value or use index closure pattern
- **NEVER use `time.Sleep` as synchronization** — Use channels, WaitGroups, or context
