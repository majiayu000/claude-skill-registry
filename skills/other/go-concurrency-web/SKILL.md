---
name: go-concurrency-web
description: Go concurrency patterns for high-throughput web applications including worker pools, rate limiting, race detection, and safe shared state management. Use when implementing background task processing, rate limiters, or concurrent request handling.
---

# Go Concurrency for Web Applications

## Quick Reference

| Topic | Reference |
|-------|-----------|
| Worker Pools & errgroup | [references/worker-pools.md](references/worker-pools.md) |
| Rate Limiting | [references/rate-limiting.md](references/rate-limiting.md) |
| Race Detection & Fixes | [references/race-detection.md](references/race-detection.md) |

## Core Rules

1. **Goroutines are cheap but not free** — each goroutine consumes ~2-8 KB of stack. Unbounded spawning under load leads to OOM.
2. **Always have a shutdown path** — every goroutine you start must have a way to exit. Use `context.Context`, channel closing, or `sync.WaitGroup`.
3. **Prefer channels for communication** — use channels to coordinate work between goroutines and signal completion.
4. **Use mutexes for state protection** — when goroutines share mutable state, protect it with `sync.Mutex`, `sync.RWMutex`, or `sync/atomic`.
5. **Never spawn raw goroutines in HTTP handlers** — use worker pools, `errgroup`, or other bounded concurrency primitives.

## Worker Pool Pattern

Use worker pools for background tasks dispatched from HTTP handlers. This bounds concurrency and provides graceful shutdown.

```go
// Worker pool for background tasks (e.g., sending emails)
type WorkerPool struct {
    jobs   chan Job
    wg     sync.WaitGroup
    logger *slog.Logger
}

type Job struct {
    ID      string
    Execute func(ctx context.Context) error
}

func NewWorkerPool(numWorkers int, queueSize int, logger *slog.Logger) *WorkerPool {
    wp := &WorkerPool{
        jobs:   make(chan Job, queueSize),
        logger: logger,
    }

    for i := 0; i < numWorkers; i++ {
        wp.wg.Add(1)
        go wp.worker(i)
    }

    return wp
}

func (wp *WorkerPool) worker(id int) {
    defer wp.wg.Done()
    for job := range wp.jobs {
        wp.logger.Info("processing job", "worker", id, "job_id", job.ID)
        if err := job.Execute(context.Background()); err != nil {
            wp.logger.Error("job failed", "worker", id, "job_id", job.ID, "err", err)
        }
    }
}

func (wp *WorkerPool) Submit(job Job) {
    wp.jobs <- job
}

func (wp *WorkerPool) Shutdown() {
    close(wp.jobs)
    wp.wg.Wait()
}
```

### Usage in HTTP Handler

```go
func (s *Server) handleCreateUser(w http.ResponseWriter, r *http.Request) {
    user, err := s.userService.Create(r.Context(), decodeUser(r))
    if err != nil {
        handleError(w, r, err)
        return
    }

    // Dispatch background task — never spawn raw goroutines in handlers
    s.workers.Submit(Job{
        ID: "welcome-email-" + user.ID,
        Execute: func(ctx context.Context) error {
            return s.emailService.SendWelcome(ctx, user)
        },
    })

    writeJSON(w, http.StatusCreated, user)
}
```

See [references/worker-pools.md](references/worker-pools.md) for sizing guidance, backpressure, error handling, retry patterns, and `errgroup` as a simpler alternative.

## Rate Limiting

Use `golang.org/x/time/rate` for token bucket rate limiting. Apply as middleware for global limits or per-IP/per-user limits.

Key points:
- Global rate limiting protects overall service capacity
- Per-IP rate limiting prevents individual clients from monopolizing resources
- Always return `429 Too Many Requests` with a `Retry-After` header

See [references/rate-limiting.md](references/rate-limiting.md) for middleware implementation, per-IP limiting, stale limiter cleanup, and API key-based limiting.

## Race Detection

Run the race detector in development and CI:

```bash
go test -race ./...
go build -race -o myserver ./cmd/server
```

The race detector catches concurrent reads and writes to shared memory. It does not catch logical races (e.g., TOCTOU bugs) or deadlocks.

See [references/race-detection.md](references/race-detection.md) for common web handler races, fixing strategies, and CI integration.

## Handler Safety

Every incoming HTTP request runs in its own goroutine. Any shared mutable state on the server struct is a potential data race.

```go
// BAD — shared state without protection
type Server struct {
    requestCount int // data race!
}

func (s *Server) handleRequest(w http.ResponseWriter, r *http.Request) {
    s.requestCount++ // concurrent writes = race condition
}

// GOOD — use atomic or mutex
type Server struct {
    requestCount atomic.Int64
}

func (s *Server) handleRequest(w http.ResponseWriter, r *http.Request) {
    s.requestCount.Add(1)
}

// GOOD — use mutex for complex state
type Server struct {
    mu    sync.RWMutex
    cache map[string]*CachedItem
}

func (s *Server) handleGetCached(w http.ResponseWriter, r *http.Request) {
    s.mu.RLock()
    item, ok := s.cache[r.PathValue("key")]
    s.mu.RUnlock()
    // ...
}
```

### Rules for Handler Safety

- **Request-scoped data is safe** — `r.Context()`, request body, URL params are isolated per request.
- **Server struct fields are shared** — any field on `*Server` accessed by handlers needs synchronization.
- **Database connections are safe** — `*sql.DB` manages its own connection pool with internal locking.
- **Maps are not safe** — use `sync.Map` or protect with a mutex.
- **Slices are not safe** — concurrent append or read/write requires a mutex.

## Anti-Patterns

### Unbounded goroutine spawning

```go
// BAD — no limit on concurrent goroutines
func (s *Server) handleWebhook(w http.ResponseWriter, r *http.Request) {
    go func() {
        // What if 10,000 requests arrive at once?
        s.processWebhook(r.Context(), decodeWebhook(r))
    }()
    w.WriteHeader(http.StatusAccepted)
}

// GOOD — use a worker pool
func (s *Server) handleWebhook(w http.ResponseWriter, r *http.Request) {
    webhook := decodeWebhook(r)
    s.workers.Submit(Job{
        ID:      "webhook-" + webhook.ID,
        Execute: func(ctx context.Context) error {
            return s.processWebhook(ctx, webhook)
        },
    })
    w.WriteHeader(http.StatusAccepted)
}
```

### Forgetting to propagate context

```go
// BAD — loses cancellation signal
func (s *Server) handleSearch(w http.ResponseWriter, r *http.Request) {
    results, err := s.search(context.Background(), r.URL.Query().Get("q"))
    // ...
}

// GOOD — use request context
func (s *Server) handleSearch(w http.ResponseWriter, r *http.Request) {
    results, err := s.search(r.Context(), r.URL.Query().Get("q"))
    // ...
}
```

### Goroutine leak from missing channel receiver

```go
// BAD — goroutine blocks forever if nobody reads the channel
func fetchWithTimeout(ctx context.Context, url string) (*Response, error) {
    ch := make(chan *Response)
    go func() {
        resp, _ := http.Get(url) // blocks forever if ctx cancels
        ch <- resp               // stuck here if nobody reads
    }()
    select {
    case resp := <-ch:
        return resp, nil
    case <-ctx.Done():
        return nil, ctx.Err() // goroutine leaked!
    }
}

// GOOD — use buffered channel so goroutine can exit
func fetchWithTimeout(ctx context.Context, url string) (*Response, error) {
    ch := make(chan *Response, 1) // buffered — goroutine can always send
    go func() {
        resp, _ := http.Get(url)
        ch <- resp
    }()
    select {
    case resp := <-ch:
        return resp, nil
    case <-ctx.Done():
        return nil, ctx.Err()
    }
}
```

### Using `time.Sleep` for coordination

```go
// BAD — sleeping to wait for goroutines
go doWork()
time.Sleep(5 * time.Second) // hoping it finishes

// GOOD — use sync primitives
var wg sync.WaitGroup
wg.Add(1)
go func() {
    defer wg.Done()
    doWork()
}()
wg.Wait()
```
