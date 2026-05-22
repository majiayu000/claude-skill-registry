---
name: go-concurrency
description: Use when Go concurrency with goroutines, channels, and sync patterns. Use when writing concurrent Go code.
allowed-tools:
  - Bash
  - Read
---

# Go Concurrency

Master Go's concurrency model using goroutines, channels, and synchronization
primitives for building concurrent applications.

## Goroutines

**Creating goroutines:**

```go
package main

import (
    "fmt"
    "time"
)

func sayHello() {
    fmt.Println("Hello from goroutine")
}

func main() {
    // Launch goroutine
    go sayHello()

    // Anonymous function goroutine
    go func() {
        fmt.Println("Hello from anonymous goroutine")
    }()

    // Give goroutines time to execute
    time.Sleep(time.Second)
}
```

**Goroutines with parameters:**

```go
func printNumber(n int) {
    fmt.Println(n)
}

func main() {
    for i := 0; i < 10; i++ {
        go printNumber(i)
    }
    time.Sleep(time.Second)
}
```

## Channels

**Basic channel operations:**

```go
func main() {
    // Create unbuffered channel
    ch := make(chan int)

    // Send in goroutine (non-blocking)
    go func() {
        ch <- 42
    }()

    // Receive (blocks until value available)
    value := <-ch
    fmt.Println(value) // 42
}
```

**Buffered channels:**

```go
func main() {
    // Buffered channel with capacity 2
    ch := make(chan string, 2)

    // Can send up to 2 values without blocking
    ch <- "first"
    ch <- "second"

    fmt.Println(<-ch) // first
    fmt.Println(<-ch) // second
}
```

**Channel direction:**

```go
// Send-only channel
func send(ch chan<- int) {
    ch <- 42
}

// Receive-only channel
func receive(ch <-chan int) int {
    return <-ch
}

func main() {
    ch := make(chan int)

    go send(ch)
    value := receive(ch)

    fmt.Println(value)
}
```

**Closing channels:**

```go
func main() {
    ch := make(chan int, 3)

    ch <- 1
    ch <- 2
    ch <- 3
    close(ch) // Close channel

    // Receive until channel is closed
    for value := range ch {
        fmt.Println(value)
    }

    // Check if channel is closed
    value, ok := <-ch
    fmt.Printf("Value: %d, Open: %v\n", value, ok) // Value: 0, Open: false
}
```

## Select Statement

**Multiplexing channels:**

```go
func main() {
    ch1 := make(chan string)
    ch2 := make(chan string)

    go func() {
        time.Sleep(time.Second)
        ch1 <- "from ch1"
    }()

    go func() {
        time.Sleep(2 * time.Second)
        ch2 <- "from ch2"
    }()

    // Wait for both
    for i := 0; i < 2; i++ {
        select {
        case msg1 := <-ch1:
            fmt.Println(msg1)
        case msg2 := <-ch2:
            fmt.Println(msg2)
        }
    }
}
```

**Select with default:**

```go
func main() {
    ch := make(chan int, 1)

    select {
    case val := <-ch:
        fmt.Println(val)
    default:
        fmt.Println("No value ready") // Executed
    }
}
```

**Select with timeout:**

```go
func main() {
    ch := make(chan string)

    go func() {
        time.Sleep(2 * time.Second)
        ch <- "result"
    }()

    select {
    case msg := <-ch:
        fmt.Println(msg)
    case <-time.After(time.Second):
        fmt.Println("Timeout") // Executed after 1 second
    }
}
```

## Worker Pools

**Implementing worker pool pattern:**

```go
func worker(id int, jobs <-chan int, results chan<- int) {
    for job := range jobs {
        fmt.Printf("Worker %d processing job %d\n", id, job)
        time.Sleep(time.Second)
        results <- job * 2
    }
}

func main() {
    jobs := make(chan int, 100)
    results := make(chan int, 100)

    // Start 3 workers
    for w := 1; w <= 3; w++ {
        go worker(w, jobs, results)
    }

    // Send 5 jobs
    for j := 1; j <= 5; j++ {
        jobs <- j
    }
    close(jobs)

    // Collect results
    for a := 1; a <= 5; a++ {
        <-results
    }
}
```

## sync.WaitGroup

**Waiting for goroutines to complete:**

```go
import (
    "fmt"
    "sync"
    "time"
)

func worker(id int, wg *sync.WaitGroup) {
    defer wg.Done() // Decrement counter when done

    fmt.Printf("Worker %d starting\n", id)
    time.Sleep(time.Second)
    fmt.Printf("Worker %d done\n", id)
}

func main() {
    var wg sync.WaitGroup

    for i := 1; i <= 5; i++ {
        wg.Add(1) // Increment counter
        go worker(i, &wg)
    }

    wg.Wait() // Wait for all to complete
    fmt.Println("All workers done")
}
```

## sync.Mutex

**Protecting shared state:**

```go
import (
    "fmt"
    "sync"
)

type Counter struct {
    mu    sync.Mutex
    value int
}

func (c *Counter) Increment() {
    c.mu.Lock()
    c.value++
    c.mu.Unlock()
}

func (c *Counter) Value() int {
    c.mu.Lock()
    defer c.mu.Unlock()
    return c.value
}

func main() {
    var wg sync.WaitGroup
    counter := Counter{}

    for i := 0; i < 1000; i++ {
        wg.Add(1)
        go func() {
            defer wg.Done()
            counter.Increment()
        }()
    }

    wg.Wait()
    fmt.Println(counter.Value()) // 1000
}
```

## sync.RWMutex

**Read-write locks:**

```go
type Cache struct {
    mu    sync.RWMutex
    items map[string]string
}

func (c *Cache) Get(key string) (string, bool) {
    c.mu.RLock() // Read lock
    defer c.mu.RUnlock()
    val, ok := c.items[key]
    return val, ok
}

func (c *Cache) Set(key, value string) {
    c.mu.Lock() // Write lock
    defer c.mu.Unlock()
    c.items[key] = value
}

func main() {
    cache := Cache{items: make(map[string]string)}

    // Multiple readers can access simultaneously
    var wg sync.WaitGroup
    for i := 0; i < 10; i++ {
        wg.Add(1)
        go func() {
            defer wg.Done()
            cache.Get("key")
        }()
    }

    wg.Wait()
}
```

## sync.Once

**Execute once initialization:**

```go
var (
    instance *Database
    once     sync.Once
)

type Database struct {
    conn string
}

func GetDatabase() *Database {
    once.Do(func() {
        fmt.Println("Initializing database")
        instance = &Database{conn: "connected"}
    })
    return instance
}

func main() {
    var wg sync.WaitGroup

    for i := 0; i < 10; i++ {
        wg.Add(1)
        go func() {
            defer wg.Done()
            db := GetDatabase() // Only initializes once
            fmt.Println(db.conn)
        }()
    }

    wg.Wait()
}
```

## Context Package

**Using context for cancellation:**

```go
import (
    "context"
    "fmt"
    "time"
)

func worker(ctx context.Context, id int) {
    for {
        select {
        case <-ctx.Done():
            fmt.Printf("Worker %d cancelled\n", id)
            return
        default:
            fmt.Printf("Worker %d working\n", id)
            time.Sleep(500 * time.Millisecond)
        }
    }
}

func main() {
    ctx, cancel := context.WithCancel(context.Background())

    for i := 1; i <= 3; i++ {
        go worker(ctx, i)
    }

    time.Sleep(2 * time.Second)
    cancel() // Cancel all workers
    time.Sleep(time.Second)
}
```

**Context with timeout:**

```go
func slowOperation(ctx context.Context) error {
    select {
    case <-time.After(3 * time.Second):
        return nil
    case <-ctx.Done():
        return ctx.Err()
    }
}

func main() {
    ctx, cancel := context.WithTimeout(
        context.Background(),
        2*time.Second,
    )
    defer cancel()

    err := slowOperation(ctx)
    if err != nil {
        fmt.Println("Operation timed out:", err)
    }
}
```

**Context with values:**

```go
func processRequest(ctx context.Context) {
    userID := ctx.Value("userID")
    fmt.Println("Processing for user:", userID)
}

func main() {
    ctx := context.WithValue(
        context.Background(),
        "userID",
        "user123",
    )
    processRequest(ctx)
}
```

## Error Handling in Concurrent Code

**Using errgroup:**

```go
import (
    "context"
    "fmt"
    "golang.org/x/sync/errgroup"
    "time"
)

func fetchUser(ctx context.Context, id int) error {
    time.Sleep(time.Second)
    if id == 3 {
        return fmt.Errorf("user %d not found", id)
    }
    fmt.Printf("Fetched user %d\n", id)
    return nil
}

func main() {
    g, ctx := errgroup.WithContext(context.Background())

    userIDs := []int{1, 2, 3, 4, 5}

    for _, id := range userIDs {
        id := id // Capture loop variable
        g.Go(func() error {
            return fetchUser(ctx, id)
        })
    }

    // Wait for all goroutines
    if err := g.Wait(); err != nil {
        fmt.Println("Error:", err)
    }
}
```

## Fan-Out Fan-In Pattern

**Distributing work and collecting results:**

```go
func generator(nums ...int) <-chan int {
    out := make(chan int)
    go func() {
        for _, n := range nums {
            out <- n
        }
        close(out)
    }()
    return out
}

func square(in <-chan int) <-chan int {
    out := make(chan int)
    go func() {
        for n := range in {
            out <- n * n
        }
        close(out)
    }()
    return out
}

func merge(cs ...<-chan int) <-chan int {
    out := make(chan int)
    var wg sync.WaitGroup

    wg.Add(len(cs))
    for _, c := range cs {
        go func(ch <-chan int) {
            defer wg.Done()
            for n := range ch {
                out <- n
            }
        }(c)
    }

    go func() {
        wg.Wait()
        close(out)
    }()

    return out
}

func main() {
    in := generator(1, 2, 3, 4, 5)

    // Fan out
    c1 := square(in)
    c2 := square(in)

    // Fan in
    for n := range merge(c1, c2) {
        fmt.Println(n)
    }
}
```

## When to Use This Skill

Use go-concurrency when you need to:

- Execute multiple operations concurrently
- Build concurrent servers or workers
- Implement producer-consumer patterns
- Process data streams concurrently
- Handle multiple I/O operations simultaneously
- Implement timeout and cancellation
- Coordinate multiple goroutines
- Build fan-out/fan-in pipelines
- Share state safely between goroutines
- Implement rate limiting or throttling

## Best Practices

- Use channels for communication, mutexes for state
- Close channels from sender side only
- Always use WaitGroup to wait for goroutines
- Pass contexts for cancellation and deadlines
- Use buffered channels judiciously
- Protect shared state with mutexes
- Avoid goroutine leaks with proper cleanup
- Use select with default for non-blocking ops
- Prefer sync.Once for initialization
- Document goroutine ownership and lifecycle

## Common Pitfalls

- Goroutine leaks (forgetting to exit)
- Race conditions from unprotected shared state
- Deadlocks from improper channel usage
- Sending on closed channels (panics)
- Not checking channel close status
- Overusing mutexes instead of channels
- Creating too many goroutines
- Forgetting to call WaitGroup.Done()
- Passing loop variables to goroutines
- Not handling context cancellation

## Resources

- [Go Concurrency Patterns](https://go.dev/blog/pipelines)
- [Effective Go - Concurrency](https://go.dev/doc/effective_go#concurrency)
- [Go by Example - Goroutines](https://gobyexample.com/goroutines)
- [errgroup Package](https://pkg.go.dev/golang.org/x/sync/errgroup)
- [Context Package](https://pkg.go.dev/context)
