---
name: convert-golang-rust
description: Convert Go code to idiomatic Rust. Use when migrating Go projects to Rust, translating Go patterns to idiomatic Rust, or refactoring Go codebases. Extends meta-convert-dev with Go-to-Rust specific patterns.
---

# Convert Go to Rust

Convert Go code to idiomatic Rust. This skill extends `meta-convert-dev` with Go-to-Rust specific type mappings, idiom translations, and tooling.

## This Skill Extends

- `meta-convert-dev` - Foundational conversion patterns (APTV workflow, testing strategies)

For general concepts like the Analyze → Plan → Transform → Validate workflow, testing strategies, and common pitfalls, see the meta-skill first.

## This Skill Adds

- **Type mappings**: Go types → Rust types
- **Idiom translations**: Go patterns → idiomatic Rust
- **Error handling**: Go error interface → Rust Result<T, E>
- **Async patterns**: Goroutines/channels → Tokio async/await
- **Memory/Ownership**: Garbage collection → ownership/borrowing
- **Interface patterns**: Go interface → Rust trait

## This Skill Does NOT Cover

- General conversion methodology - see `meta-convert-dev`
- Go language fundamentals - see `lang-go-dev`
- Rust language fundamentals - see `lang-rust-dev`
- Reverse conversion (Rust → Go) - see `convert-rust-golang`

---

## Quick Reference

| Go | Rust | Notes |
|----------|----------|-------|
| `string` | `String` / `&str` | Owned vs borrowed |
| `int` | `i32` / `i64` | Specify size explicitly |
| `uint` | `u32` / `u64` | Unsigned variants |
| `float64` | `f64` | Direct mapping |
| `bool` | `bool` | Direct mapping |
| `[]T` | `Vec<T>` | Owned slice |
| `[N]T` | `[T; N]` | Fixed-size array |
| `map[K]V` | `HashMap<K, V>` | Hash table |
| `chan T` | `mpsc::Sender<T>` / `Receiver<T>` | Channels |
| `interface{}` | Generic with trait bounds | Type-safe alternatives |
| `nil` | `None` in `Option<T>` | Explicit nullability |
| `error` | `Result<T, E>` | Type-safe errors |
| `struct` | `struct` | Similar syntax |
| `interface` | `trait` | Behavioral contracts |
| `defer` | RAII / `Drop` trait | Automatic cleanup |

## When Converting Code

1. **Analyze source thoroughly** before writing target
2. **Map types first** - create type equivalence table
3. **Preserve semantics** over syntax similarity
4. **Adopt target idioms** - don't write "Go code in Rust syntax"
5. **Handle edge cases** - nil checks, error paths, resource cleanup
6. **Test equivalence** - same inputs → same outputs

---

## Type System Mapping

### Primitive Types

| Go | Rust | Notes |
|----------|----------|-------|
| `bool` | `bool` | Direct mapping |
| `string` | `String` | Owned, heap-allocated UTF-8 |
| `string` (param) | `&str` | Borrowed string slice for parameters |
| `int` | `isize` | Platform-dependent signed integer |
| `int8` | `i8` | 8-bit signed |
| `int16` | `i16` | 16-bit signed |
| `int32` / `rune` | `i32` | 32-bit signed |
| `int64` | `i64` | 64-bit signed |
| `uint` | `usize` | Platform-dependent unsigned |
| `uint8` / `byte` | `u8` | 8-bit unsigned |
| `uint16` | `u16` | 16-bit unsigned |
| `uint32` | `u32` | 32-bit unsigned |
| `uint64` | `u64` | 64-bit unsigned |
| `float32` | `f32` | 32-bit float |
| `float64` | `f64` | 64-bit float |
| `complex64` | - | Use external crate (num-complex) |
| `complex128` | - | Use external crate (num-complex) |

### Collection Types

| Go | Rust | Notes |
|----------|----------|-------|
| `[]T` | `Vec<T>` | Growable, owned array |
| `[]T` (param) | `&[T]` | Borrowed slice for parameters |
| `[N]T` | `[T; N]` | Fixed-size array on stack |
| `map[K]V` | `HashMap<K, V>` | Hash table, K must be Hash + Eq |
| `map[K]V` (ordered) | `BTreeMap<K, V>` | Ordered map, K must be Ord |
| Set (manual) | `HashSet<T>` | Deduplicated collection |
| Set (ordered) | `BTreeSet<T>` | Ordered deduplicated collection |

### Composite Types

| Go | Rust | Notes |
|----------|----------|-------|
| `struct { ... }` | `struct { ... }` | Similar syntax, explicit visibility |
| `*T` | `Box<T>` | Heap allocation, single owner |
| `*T` (shared) | `Rc<T>` / `Arc<T>` | Reference counted (single/multi-threaded) |
| `interface { ... }` | `trait Trait { ... }` | Behavior definition |
| `struct + methods` | `impl Block` | Method implementation |
| `func(T) U` | `fn(T) -> U` | Function type |
| `func(T) U` (closure) | `Fn(T) -> U` | Closure trait |
| `chan T` | `mpsc::Sender<T>` | Channel sender |
| `<-chan T` | `mpsc::Receiver<T>` | Channel receiver |
| `chan<- T` | `mpsc::Sender<T>` | Send-only channel |

### Pointer and Reference Types

| Go | Rust | Notes |
|----------|----------|-------|
| `*T` (nullable) | `Option<Box<T>>` | Nullable heap pointer |
| `*T` (non-null) | `Box<T>` | Non-null owned heap pointer |
| `&T` (for mutation) | `&mut T` | Exclusive mutable reference |
| Pointer to slice | `&[T]` | Slice reference |
| Pointer to map | `&HashMap<K, V>` | Map reference |

---

## Idiom Translation

### Pattern 1: Error Handling with Multiple Returns

**Go:**
```go
func readFile(path string) ([]byte, error) {
    data, err := os.ReadFile(path)
    if err != nil {
        return nil, fmt.Errorf("failed to read %s: %w", path, err)
    }
    return data, nil
}
```

**Rust:**
```rust
use std::fs;
use std::path::Path;

fn read_file(path: &Path) -> Result<Vec<u8>, std::io::Error> {
    fs::read(path)
        .map_err(|e| std::io::Error::new(
            e.kind(),
            format!("failed to read {}: {}", path.display(), e)
        ))
}
```

**Why this translation:**
- Rust's `Result<T, E>` encodes success/failure in the type system
- The `?` operator propagates errors ergonomically
- Error wrapping uses `map_err` instead of manual checks
- Borrowed `&Path` instead of owned `String` for efficiency

### Pattern 2: Nil Checking

**Go:**
```go
func getUserName(user *User) string {
    if user == nil {
        return "Anonymous"
    }
    if user.Name == "" {
        return "Anonymous"
    }
    return user.Name
}
```

**Rust:**
```rust
fn get_user_name(user: Option<&User>) -> &str {
    user.and_then(|u| {
        if u.name.is_empty() {
            None
        } else {
            Some(u.name.as_str())
        }
    })
    .unwrap_or("Anonymous")
}

// Or more idiomatically with pattern matching:
fn get_user_name(user: Option<&User>) -> &str {
    match user {
        Some(u) if !u.name.is_empty() => &u.name,
        _ => "Anonymous",
    }
}
```

**Why this translation:**
- `Option<T>` makes nullability explicit in the type system
- Combinators like `and_then` and `unwrap_or` are idiomatic
- Pattern matching with guards is more readable
- Borrowed references avoid unnecessary cloning

### Pattern 3: Interface Implementation

**Go:**
```go
type Reader interface {
    Read(p []byte) (n int, err error)
}

type FileReader struct {
    path string
}

func (f *FileReader) Read(p []byte) (int, error) {
    // Implementation
    return len(p), nil
}

func processReader(r Reader) error {
    buf := make([]byte, 1024)
    n, err := r.Read(buf)
    if err != nil {
        return err
    }
    // Process n bytes
    return nil
}
```

**Rust:**
```rust
use std::io::{self, Read};

trait Reader {
    fn read(&mut self, buf: &mut [u8]) -> io::Result<usize>;
}

struct FileReader {
    path: String,
}

impl Reader for FileReader {
    fn read(&mut self, buf: &mut [u8]) -> io::Result<usize> {
        // Implementation
        Ok(buf.len())
    }
}

fn process_reader<R: Reader>(r: &mut R) -> io::Result<()> {
    let mut buf = vec![0u8; 1024];
    let n = r.read(&mut buf)?;
    // Process n bytes
    Ok(())
}
```

**Why this translation:**
- Rust traits are explicitly implemented with `impl Trait for Type`
- Generic functions use trait bounds (`<R: Reader>`)
- Mutable borrows (`&mut`) make mutation explicit
- The `?` operator replaces verbose error checking

### Pattern 4: Goroutines and Channels

**Go:**
```go
func processItems(items []string) []string {
    results := make(chan string, len(items))

    for _, item := range items {
        go func(s string) {
            results <- processItem(s)
        }(item)
    }

    var processed []string
    for i := 0; i < len(items); i++ {
        processed = append(processed, <-results)
    }
    return processed
}
```

**Rust:**
```rust
use tokio::task;

async fn process_items(items: Vec<String>) -> Vec<String> {
    let handles: Vec<_> = items
        .into_iter()
        .map(|item| {
            task::spawn(async move {
                process_item(item).await
            })
        })
        .collect();

    let mut processed = Vec::new();
    for handle in handles {
        if let Ok(result) = handle.await {
            processed.push(result);
        }
    }
    processed
}
```

**Why this translation:**
- Tokio's async/await is more explicit about async boundaries
- `task::spawn` creates async tasks similar to goroutines
- Awaiting task handles is more type-safe than channels
- Move semantics avoid accidental captures
- Alternative: Use channels with `tokio::sync::mpsc` for Go-like patterns

### Pattern 5: Defer for Cleanup

**Go:**
```go
func processFile(path string) error {
    f, err := os.Open(path)
    if err != nil {
        return err
    }
    defer f.Close()

    // Work with file
    return process(f)
}
```

**Rust:**
```rust
use std::fs::File;
use std::path::Path;

fn process_file(path: &Path) -> std::io::Result<()> {
    let f = File::open(path)?;

    // Work with file
    process(&f)
    // f.close() called automatically via Drop
}

// Or with explicit scope control:
fn process_file_scoped(path: &Path) -> std::io::Result<()> {
    let result = {
        let f = File::open(path)?;
        process(&f)
    }; // f dropped here
    result
}
```

**Why this translation:**
- Rust's RAII (Drop trait) automatically cleans up resources
- No need for explicit `defer` statements
- Scope-based cleanup is deterministic
- More type-safe than runtime defer

### Pattern 6: Type Assertions and Type Switches

**Go:**
```go
func handleValue(v interface{}) string {
    switch val := v.(type) {
    case string:
        return fmt.Sprintf("string: %s", val)
    case int:
        return fmt.Sprintf("int: %d", val)
    case error:
        return fmt.Sprintf("error: %v", val)
    default:
        return "unknown"
    }
}
```

**Rust:**
```rust
// Use enums instead of interface{} for type-safe variants
enum Value {
    String(String),
    Int(i32),
    Error(String),
}

fn handle_value(v: Value) -> String {
    match v {
        Value::String(s) => format!("string: {}", s),
        Value::Int(i) => format!("int: {}", i),
        Value::Error(e) => format!("error: {}", e),
    }
}

// Or use trait objects with downcasting (less idiomatic):
use std::any::Any;

fn handle_any(v: &dyn Any) -> String {
    if let Some(s) = v.downcast_ref::<String>() {
        format!("string: {}", s)
    } else if let Some(i) = v.downcast_ref::<i32>() {
        format!("int: {}", i)
    } else {
        "unknown".to_string()
    }
}
```

**Why this translation:**
- Rust enums are type-safe alternatives to `interface{}`
- Pattern matching exhaustively handles all variants
- Compiler ensures all cases are covered
- Avoid `Any` downcasting when possible (use enums instead)

### Pattern 7: Method Receivers (Value vs Pointer)

**Go:**
```go
type Counter struct {
    count int
}

// Pointer receiver (mutates)
func (c *Counter) Increment() {
    c.count++
}

// Value receiver (doesn't mutate)
func (c Counter) Value() int {
    return c.count
}
```

**Rust:**
```rust
struct Counter {
    count: i32,
}

impl Counter {
    // Mutable reference (mutates)
    fn increment(&mut self) {
        self.count += 1;
    }

    // Immutable reference (doesn't mutate)
    fn value(&self) -> i32 {
        self.count
    }

    // Consuming method (takes ownership)
    fn into_inner(self) -> i32 {
        self.count
    }
}
```

**Why this translation:**
- Rust makes mutability explicit: `&self`, `&mut self`, `self`
- Borrowing prevents accidental copies
- Consuming methods (`self`) transfer ownership
- More explicit control over mutation

### Pattern 8: Struct Embedding (Composition)

**Go:**
```go
type Base struct {
    ID int
}

func (b *Base) GetID() int {
    return b.ID
}

type Derived struct {
    Base
    Name string
}

func main() {
    d := Derived{
        Base: Base{ID: 1},
        Name: "test",
    }
    fmt.Println(d.GetID()) // Method promoted from Base
}
```

**Rust:**
```rust
struct Base {
    id: i32,
}

impl Base {
    fn get_id(&self) -> i32 {
        self.id
    }
}

struct Derived {
    base: Base,
    name: String,
}

impl Derived {
    // Explicit delegation (no automatic promotion)
    fn get_id(&self) -> i32 {
        self.base.get_id()
    }
}

// Or use Deref trait for automatic field access:
use std::ops::Deref;

impl Deref for Derived {
    type Target = Base;

    fn deref(&self) -> &Self::Target {
        &self.base
    }
}
```

**Why this translation:**
- Rust favors explicit composition over embedding
- No automatic method promotion (use delegation)
- `Deref` trait can provide field access convenience
- More explicit about the relationship

### Pattern 9: Context Propagation

**Go:**
```go
func fetchData(ctx context.Context, url string) ([]byte, error) {
    req, err := http.NewRequestWithContext(ctx, "GET", url, nil)
    if err != nil {
        return nil, err
    }

    resp, err := http.DefaultClient.Do(req)
    if err != nil {
        return nil, err
    }
    defer resp.Body.Close()

    return io.ReadAll(resp.Body)
}
```

**Rust:**
```rust
use tokio::time::{timeout, Duration};
use reqwest;

async fn fetch_data(url: &str, timeout_ms: u64) -> Result<Vec<u8>, reqwest::Error> {
    let response = timeout(
        Duration::from_millis(timeout_ms),
        reqwest::get(url)
    )
    .await
    .map_err(|_| reqwest::Error::from(std::io::Error::new(
        std::io::ErrorKind::TimedOut,
        "request timed out"
    )))??;

    response.bytes()
        .await
        .map(|b| b.to_vec())
}

// Or with explicit cancellation token:
use tokio_util::sync::CancellationToken;

async fn fetch_data_cancellable(
    url: &str,
    cancel_token: CancellationToken,
) -> Result<Vec<u8>, reqwest::Error> {
    tokio::select! {
        result = reqwest::get(url) => {
            result?.bytes().await.map(|b| b.to_vec())
        }
        _ = cancel_token.cancelled() => {
            Err(reqwest::Error::from(std::io::Error::new(
                std::io::ErrorKind::Interrupted,
                "cancelled"
            )))
        }
    }
}
```

**Why this translation:**
- Rust doesn't have built-in context; use timeout or cancellation tokens
- `tokio::select!` provides cancellation semantics
- Explicit timeout durations instead of context deadlines
- More type-safe cancellation handling

### Pattern 10: Variadic Functions

**Go:**
```go
func sum(nums ...int) int {
    total := 0
    for _, n := range nums {
        total += n
    }
    return total
}

func main() {
    fmt.Println(sum(1, 2, 3, 4))
}
```

**Rust:**
```rust
fn sum(nums: &[i32]) -> i32 {
    nums.iter().sum()
}

fn main() {
    println!("{}", sum(&[1, 2, 3, 4]));
}

// Or with macro for syntax sugar:
macro_rules! sum {
    ($($x:expr),*) => {
        {
            let nums = [$($x),*];
            nums.iter().sum::<i32>()
        }
    };
}

fn main() {
    println!("{}", sum!(1, 2, 3, 4));
}
```

**Why this translation:**
- Rust doesn't have variadic functions; use slices
- Macros can provide variadic-like syntax
- Iterator methods are more idiomatic than loops
- More explicit about allocation

---

## Error Handling

### Go Error Interface → Rust Result Type

Go's `error` interface and multiple return values translate to Rust's `Result<T, E>` enum.

**Philosophy Shift:**
- **Go**: Errors are values, checked explicitly via `if err != nil`
- **Rust**: Errors are types, propagated with `?` operator

### Basic Error Translation

**Go:**
```go
func divide(a, b float64) (float64, error) {
    if b == 0 {
        return 0, errors.New("division by zero")
    }
    return a / b, nil
}

func main() {
    result, err := divide(10, 0)
    if err != nil {
        log.Fatal(err)
    }
    fmt.Println(result)
}
```

**Rust:**
```rust
use std::error::Error;
use std::fmt;

#[derive(Debug)]
struct DivisionError;

impl fmt::Display for DivisionError {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "division by zero")
    }
}

impl Error for DivisionError {}

fn divide(a: f64, b: f64) -> Result<f64, DivisionError> {
    if b == 0.0 {
        Err(DivisionError)
    } else {
        Ok(a / b)
    }
}

fn main() -> Result<(), Box<dyn Error>> {
    let result = divide(10.0, 0.0)?;
    println!("{}", result);
    Ok(())
}
```

### Error Wrapping and Context

**Go:**
```go
func readConfig(path string) (*Config, error) {
    data, err := os.ReadFile(path)
    if err != nil {
        return nil, fmt.Errorf("failed to read config: %w", err)
    }

    var cfg Config
    if err := json.Unmarshal(data, &cfg); err != nil {
        return nil, fmt.Errorf("failed to parse config: %w", err)
    }

    return &cfg, nil
}
```

**Rust:**
```rust
use std::fs;
use std::path::Path;
use serde::Deserialize;
use thiserror::Error;

#[derive(Debug, Error)]
enum ConfigError {
    #[error("failed to read config: {0}")]
    ReadFailed(#[from] std::io::Error),

    #[error("failed to parse config: {0}")]
    ParseFailed(#[from] serde_json::Error),
}

#[derive(Deserialize)]
struct Config {
    // fields
}

fn read_config(path: &Path) -> Result<Config, ConfigError> {
    let data = fs::read_to_string(path)?;
    let cfg: Config = serde_json::from_str(&data)?;
    Ok(cfg)
}
```

### Custom Error Types

**Go:**
```go
type ValidationError struct {
    Field   string
    Message string
}

func (e *ValidationError) Error() string {
    return fmt.Sprintf("validation failed for %s: %s", e.Field, e.Message)
}

func validate(user *User) error {
    if user.Email == "" {
        return &ValidationError{
            Field:   "email",
            Message: "cannot be empty",
        }
    }
    return nil
}
```

**Rust:**
```rust
use thiserror::Error;

#[derive(Debug, Error)]
#[error("validation failed for {field}: {message}")]
struct ValidationError {
    field: String,
    message: String,
}

fn validate(user: &User) -> Result<(), ValidationError> {
    if user.email.is_empty() {
        return Err(ValidationError {
            field: "email".to_string(),
            message: "cannot be empty".to_string(),
        });
    }
    Ok(())
}
```

### Error Handling Best Practices

| Go Pattern | Rust Pattern | Notes |
|------------|--------------|-------|
| `if err != nil { return nil, err }` | `?` operator | Automatic propagation |
| `fmt.Errorf("context: %w", err)` | `map_err(\|e\| ...)` | Add context |
| Multiple error types | `enum` with `#[from]` | Type-safe error conversion |
| `errors.Is(err, target)` | `match` on error type | Pattern matching |
| `errors.As(err, &target)` | `downcast_ref` (rare) | Usually use enums instead |
| Sentinel errors | Unit variants in enum | `enum Error { NotFound }` |

---

## Concurrency Patterns

### Goroutines → Async Tasks

**Philosophy Shift:**
- **Go**: Goroutines are cheap threads, blocking is fine
- **Rust**: Async tasks are cooperative, blocking requires special handling

### Basic Goroutine Translation

**Go:**
```go
func fetchAll(urls []string) []Result {
    results := make(chan Result, len(urls))

    for _, url := range urls {
        go func(u string) {
            results <- fetch(u)
        }(url)
    }

    var out []Result
    for i := 0; i < len(urls); i++ {
        out = append(out, <-results)
    }
    return out
}
```

**Rust (with Tokio):**
```rust
use tokio::task;

async fn fetch_all(urls: Vec<String>) -> Vec<Result> {
    let handles: Vec<_> = urls
        .into_iter()
        .map(|url| task::spawn(async move { fetch(&url).await }))
        .collect();

    let mut out = Vec::new();
    for handle in handles {
        if let Ok(result) = handle.await {
            out.push(result);
        }
    }
    out
}

// Or using futures::join_all:
use futures::future::join_all;

async fn fetch_all(urls: Vec<String>) -> Vec<Result> {
    join_all(urls.iter().map(|url| fetch(url))).await
}
```

### Channels Translation

**Go:**
```go
func producer(ch chan<- int) {
    for i := 0; i < 10; i++ {
        ch <- i
    }
    close(ch)
}

func consumer(ch <-chan int) {
    for val := range ch {
        fmt.Println(val)
    }
}

func main() {
    ch := make(chan int, 5)
    go producer(ch)
    consumer(ch)
}
```

**Rust:**
```rust
use tokio::sync::mpsc;

async fn producer(tx: mpsc::Sender<i32>) {
    for i in 0..10 {
        let _ = tx.send(i).await;
    }
    // Channel closes when tx is dropped
}

async fn consumer(mut rx: mpsc::Receiver<i32>) {
    while let Some(val) = rx.recv().await {
        println!("{}", val);
    }
}

#[tokio::main]
async fn main() {
    let (tx, rx) = mpsc::channel(5);

    tokio::spawn(async move {
        producer(tx).await;
    });

    consumer(rx).await;
}
```

### Select Statement Translation

**Go:**
```go
func waitForFirst(ch1, ch2 <-chan string) string {
    select {
    case msg := <-ch1:
        return msg
    case msg := <-ch2:
        return msg
    case <-time.After(1 * time.Second):
        return "timeout"
    }
}
```

**Rust:**
```rust
use tokio::sync::mpsc;
use tokio::time::{sleep, Duration};

async fn wait_for_first(
    mut rx1: mpsc::Receiver<String>,
    mut rx2: mpsc::Receiver<String>,
) -> String {
    tokio::select! {
        Some(msg) = rx1.recv() => msg,
        Some(msg) = rx2.recv() => msg,
        _ = sleep(Duration::from_secs(1)) => "timeout".to_string(),
    }
}
```

### Worker Pool Pattern

**Go:**
```go
func workerPool(jobs <-chan Job, results chan<- Result, numWorkers int) {
    var wg sync.WaitGroup

    for i := 0; i < numWorkers; i++ {
        wg.Add(1)
        go func() {
            defer wg.Done()
            for job := range jobs {
                results <- process(job)
            }
        }()
    }

    wg.Wait()
    close(results)
}
```

**Rust:**
```rust
use tokio::sync::mpsc;
use tokio::task;

async fn worker_pool(
    mut jobs: mpsc::Receiver<Job>,
    results: mpsc::Sender<Result>,
    num_workers: usize,
) {
    let mut handles = vec![];

    for _ in 0..num_workers {
        let mut jobs = jobs.clone();
        let results = results.clone();

        let handle = task::spawn(async move {
            while let Some(job) = jobs.recv().await {
                let result = process(job).await;
                let _ = results.send(result).await;
            }
        });

        handles.push(handle);
    }

    drop(jobs); // Close the receiver

    for handle in handles {
        let _ = handle.await;
    }
    // results sender dropped, channel closes
}
```

### Sync Primitives Translation

| Go | Rust | Notes |
|----------|----------|-------|
| `sync.Mutex` | `std::sync::Mutex` | Blocking mutex |
| `sync.RWMutex` | `std::sync::RwLock` | Reader-writer lock |
| `sync.WaitGroup` | Manual with channels or `JoinHandle` | No direct equivalent |
| `sync.Once` | `std::sync::Once` | One-time initialization |
| `sync.Cond` | `std::sync::Condvar` | Condition variable |
| `atomic.*` | `std::sync::atomic::*` | Atomic operations |
| `chan T` | `tokio::sync::mpsc` | Async channels |
| `chan T` (sync) | `std::sync::mpsc` | Blocking channels |

### Async Best Practices

1. **Don't block in async**: Use `tokio::task::spawn_blocking` for CPU-bound work
2. **Prefer bounded channels**: Prevent unbounded memory growth
3. **Use `tokio::select!` carefully**: Branches are not evaluated in order
4. **Handle task panics**: Use `JoinHandle::await` and check results
5. **Use `Arc` for shared state**: Wrap with `Mutex` or `RwLock` for mutation

---

## Memory & Ownership

### Garbage Collection → Ownership System

**Philosophy Shift:**
- **Go**: GC handles memory, share references freely
- **Rust**: Ownership rules enforced at compile time, explicit sharing

### Ownership Rules in Rust

1. Each value has exactly one owner
2. When the owner goes out of scope, the value is dropped
3. Values can be borrowed (referenced) immutably or mutably
4. Only one mutable borrow OR multiple immutable borrows at a time

### Basic Ownership Translation

**Go:**
```go
func process() {
    data := []int{1, 2, 3, 4, 5}

    // Pass by reference (slice is a reference type)
    modifyData(data)

    // data is modified
    fmt.Println(data)
}

func modifyData(d []int) {
    d[0] = 99
}
```

**Rust:**
```rust
fn process() {
    let mut data = vec![1, 2, 3, 4, 5];

    // Pass mutable borrow
    modify_data(&mut data);

    // data is modified
    println!("{:?}", data);
}

fn modify_data(d: &mut Vec<i32>) {
    d[0] = 99;
}
```

### Shared Ownership (Reference Counting)

**Go:**
```go
type Cache struct {
    data map[string]*Value
}

func (c *Cache) Get(key string) *Value {
    return c.data[key] // Returns pointer, GC handles lifetime
}

func main() {
    cache := &Cache{data: make(map[string]*Value)}
    val := cache.Get("key")
    // val can outlive cache in Go (GC prevents dangling pointers)
}
```

**Rust:**
```rust
use std::sync::Arc;
use std::collections::HashMap;

struct Cache {
    data: HashMap<String, Arc<Value>>,
}

impl Cache {
    fn get(&self, key: &str) -> Option<Arc<Value>> {
        self.data.get(key).cloned() // Clone the Arc, not the Value
    }
}

fn main() {
    let cache = Cache { data: HashMap::new() };
    let val = cache.get("key");
    // val holds a reference count to Value
}
```

### Move Semantics

**Go:**
```go
func transfer() {
    data := []int{1, 2, 3}

    // Both variables point to same backing array
    newData := data

    // Both can be used
    fmt.Println(data)
    fmt.Println(newData)
}
```

**Rust:**
```rust
fn transfer() {
    let data = vec![1, 2, 3];

    // Ownership moved to new_data
    let new_data = data;

    // Error: data is no longer valid
    // println!("{:?}", data); // Compile error!

    println!("{:?}", new_data); // OK
}

// To keep using data, clone it:
fn transfer_with_clone() {
    let data = vec![1, 2, 3];
    let new_data = data.clone(); // Explicit copy

    println!("{:?}", data);     // OK
    println!("{:?}", new_data); // OK
}
```

### Borrowing Rules

**Go:**
```go
func example() {
    data := []int{1, 2, 3}

    // Can pass to multiple functions
    read1(data)
    read2(data)
    modify(data)
}

func read1(d []int) { /* read only */ }
func read2(d []int) { /* read only */ }
func modify(d []int) { d[0] = 99 }
```

**Rust:**
```rust
fn example() {
    let mut data = vec![1, 2, 3];

    // Multiple immutable borrows OK
    read1(&data);
    read2(&data);

    // Mutable borrow (must be exclusive)
    modify(&mut data);

    // Cannot have immutable and mutable borrows simultaneously:
    // read1(&data);
    // modify(&mut data); // Compile error!
}

fn read1(d: &Vec<i32>) { /* read only */ }
fn read2(d: &Vec<i32>) { /* read only */ }
fn modify(d: &mut Vec<i32>) { d[0] = 99; }
```

### Lifetime Annotations

**Go:**
```go
type Parser struct {
    source string
}

func (p *Parser) NextToken() string {
    // Returns slice of source string
    // GC ensures source outlives the token
    return p.source[0:5]
}
```

**Rust:**
```rust
struct Parser<'a> {
    source: &'a str,
}

impl<'a> Parser<'a> {
    fn next_token(&self) -> &'a str {
        // Lifetime 'a ensures returned slice
        // doesn't outlive source
        &self.source[0..5]
    }
}
```

### Interior Mutability

**Go:**
```go
type Counter struct {
    mu    sync.Mutex
    count int
}

func (c *Counter) Increment() {
    c.mu.Lock()
    defer c.mu.Unlock()
    c.count++
}

func (c *Counter) Value() int {
    c.mu.Lock()
    defer c.mu.Unlock()
    return c.count
}
```

**Rust:**
```rust
use std::sync::Mutex;

struct Counter {
    count: Mutex<i32>,
}

impl Counter {
    fn increment(&self) {
        let mut count = self.count.lock().unwrap();
        *count += 1;
    }

    fn value(&self) -> i32 {
        *self.count.lock().unwrap()
    }
}
```

### Memory Ownership Decision Tree

```
Does data need to be shared across threads?
├─ YES → Arc<T> (thread-safe reference counting)
│        ├─ Needs mutation? → Arc<Mutex<T>> or Arc<RwLock<T>>
│        └─ Read-only? → Arc<T>
└─ NO  → Single-threaded sharing
         ├─ Needs mutation? → Rc<RefCell<T>>
         ├─ Read-only? → Rc<T>
         └─ Exclusive ownership? → Box<T> or owned value
```

---

## Common Pitfalls

### 1. Trying to Return Borrowed References Without Lifetimes

**Problem:**
```rust
// Go allows this easily:
// func getData() *Data {
//     d := Data{}
//     return &d  // GC keeps this alive
// }

// Rust compile error:
fn get_data() -> &Data {
    let d = Data::new();
    &d  // Error: returns reference to local variable
}
```

**Solution:**
```rust
// Return owned value instead:
fn get_data() -> Data {
    Data::new()
}

// Or use Box for heap allocation:
fn get_data() -> Box<Data> {
    Box::new(Data::new())
}
```

### 2. Fighting the Borrow Checker with Cloning

**Problem:**
```rust
// Cloning everything to avoid borrow checker errors
fn process(data: Vec<Item>) -> Vec<Result> {
    data.clone() // Unnecessary clone
        .iter()
        .map(|item| expensive_operation(item.clone())) // Unnecessary clone
        .collect()
}
```

**Solution:**
```rust
// Use borrows instead:
fn process(data: &[Item]) -> Vec<Result> {
    data.iter()
        .map(|item| expensive_operation(item))
        .collect()
}
```

### 3. Blocking in Async Contexts

**Problem:**
```rust
// Go goroutines can block freely:
// go func() {
//     result := expensiveComputation() // Blocking is fine
//     ch <- result
// }()

// Rust async tasks should not block:
tokio::spawn(async {
    let result = expensive_computation(); // Blocks the runtime!
    result
});
```

**Solution:**
```rust
// Use spawn_blocking for CPU-bound work:
tokio::spawn(async {
    let result = tokio::task::spawn_blocking(|| {
        expensive_computation()
    })
    .await
    .unwrap();

    result
});
```

### 4. Misusing `unwrap()` and `expect()`

**Problem:**
```rust
// Go forces explicit error handling:
// val, err := doSomething()
// if err != nil { ... }

// Rust makes it easy to panic:
fn process() {
    let val = do_something().unwrap(); // Panics on error!
}
```

**Solution:**
```rust
// Propagate errors with ?:
fn process() -> Result<(), Error> {
    let val = do_something()?;
    Ok(())
}

// Or handle explicitly:
fn process() {
    match do_something() {
        Ok(val) => { /* use val */ },
        Err(e) => { /* handle error */ },
    }
}
```

### 5. Not Understanding String vs &str

**Problem:**
```rust
// Allocating strings unnecessarily:
fn greet(name: String) -> String {
    format!("Hello, {}", name)
}

let greeting = greet("World".to_string()); // Allocation
```

**Solution:**
```rust
// Use &str for parameters when not consuming:
fn greet(name: &str) -> String {
    format!("Hello, {}", name)
}

let greeting = greet("World"); // No unnecessary allocation
```

### 6. Mutex Deadlocks

**Problem:**
```rust
// Go: defer mu.Unlock() prevents deadlocks

// Rust: forgetting to drop lock guards
fn update(counter: &Mutex<i32>) {
    let mut count = counter.lock().unwrap();
    *count += 1;
    // count guard still held!

    let other = counter.lock().unwrap(); // Deadlock!
}
```

**Solution:**
```rust
// Drop lock guard explicitly or use scopes:
fn update(counter: &Mutex<i32>) {
    {
        let mut count = counter.lock().unwrap();
        *count += 1;
    } // count guard dropped here

    let other = counter.lock().unwrap(); // OK
}
```

### 7. Ignoring Result/Option Types

**Problem:**
```rust
// Compiler warns but doesn't error:
fn main() {
    do_something(); // Warning: unused Result
}
```

**Solution:**
```rust
// Handle or explicitly ignore:
fn main() {
    let _ = do_something(); // Explicitly ignore

    // Or handle:
    if let Err(e) = do_something() {
        eprintln!("Error: {}", e);
    }
}
```

### 8. Overusing Arc<Mutex<T>>

**Problem:**
```rust
// Wrapping everything in Arc<Mutex> because it compiles:
struct App {
    config: Arc<Mutex<Config>>,  // Config never changes!
    cache: Arc<Mutex<Cache>>,    // Could use RwLock
}
```

**Solution:**
```rust
// Use appropriate wrapper for the access pattern:
struct App {
    config: Arc<Config>,              // Read-only, no mutex needed
    cache: Arc<RwLock<Cache>>,       // Many readers, few writers
    counter: Arc<AtomicUsize>,       // Atomic operations are faster
}
```

---

## Tooling

### Translation and Analysis

| Tool | Purpose | Notes |
|------|---------|-------|
| `c2rust` | C to Rust transpiler | Produces unsafe Rust, needs manual cleanup |
| `go2rs` | Experimental Go→Rust | Very limited, not production-ready |
| Manual translation | Most reliable | Use this skill as guide |

### Rust Ecosystem Equivalents

| Category | Go | Rust | Notes |
|----------|-----|------|-------|
| HTTP Client | `net/http` | `reqwest` | Async-first |
| HTTP Server | `net/http` | `axum`, `actix-web` | Framework-based |
| JSON | `encoding/json` | `serde_json` | Type-safe serialization |
| CLI Parsing | `flag`, `cobra` | `clap` | Derive-based API |
| Logging | `log`, `zap` | `tracing`, `log` | Structured logging |
| Testing | `testing` | Built-in `cargo test` | Similar experience |
| Benchmarking | `testing` | `criterion` | Statistical analysis |
| Async Runtime | Built-in goroutines | `tokio`, `async-std` | Explicit runtime |
| Database | `database/sql` | `sqlx`, `diesel` | Type-safe queries |
| Error Handling | `errors` | `thiserror`, `anyhow` | Rich error types |
| Configuration | `viper` | `config`, `figment` | Type-safe configs |
| Templates | `text/template` | `tera`, `handlebars` | Compile-time checks |
| Channels | `chan` | `tokio::sync::mpsc` | Async-aware |
| Context | `context.Context` | Manual (timeout, cancel token) | No built-in equivalent |
| Reflection | `reflect` | Limited (`Any`, procedural macros) | Prefer static typing |

### Development Tools

| Tool | Purpose |
|------|---------|
| `cargo` | Build system and package manager |
| `rustfmt` | Code formatter (like `gofmt`) |
| `clippy` | Linter (more strict than `golint`) |
| `rust-analyzer` | LSP server for IDE support |
| `cargo-watch` | Auto-recompile on file changes |
| `cargo-expand` | Expand macros for debugging |
| `miri` | Detect undefined behavior |

### Migration Strategy

1. **Start with types**: Translate struct definitions and interfaces to Rust types
2. **Port tests**: Convert test cases to Rust (validates correctness)
3. **Translate functions**: Convert Go functions to Rust, starting with pure functions
4. **Handle concurrency**: Replace goroutines/channels with async/await
5. **Refine ownership**: Optimize borrows and eliminate unnecessary clones
6. **Benchmark**: Compare performance and iterate

---

## Examples

### Example 1: Simple - HTTP Client Request

**Before (Go):**
```go
package main

import (
    "encoding/json"
    "fmt"
    "io"
    "net/http"
)

type User struct {
    ID   int    `json:"id"`
    Name string `json:"name"`
}

func getUser(id int) (*User, error) {
    resp, err := http.Get(fmt.Sprintf("https://api.example.com/users/%d", id))
    if err != nil {
        return nil, err
    }
    defer resp.Body.Close()

    if resp.StatusCode != http.StatusOK {
        return nil, fmt.Errorf("unexpected status: %d", resp.StatusCode)
    }

    body, err := io.ReadAll(resp.Body)
    if err != nil {
        return nil, err
    }

    var user User
    if err := json.Unmarshal(body, &user); err != nil {
        return nil, err
    }

    return &user, nil
}
```

**After (Rust):**
```rust
use serde::Deserialize;
use reqwest;

#[derive(Debug, Deserialize)]
struct User {
    id: i32,
    name: String,
}

async fn get_user(id: i32) -> Result<User, reqwest::Error> {
    let url = format!("https://api.example.com/users/{}", id);

    let user = reqwest::get(&url)
        .await?
        .error_for_status()?
        .json::<User>()
        .await?;

    Ok(user)
}
```

**Key Changes:**
- `async/await` instead of blocking calls
- `reqwest` crate for ergonomic HTTP
- `serde` for type-safe JSON deserialization
- `?` operator for error propagation
- No manual body reading (handled by `.json()`)

---

### Example 2: Medium - Concurrent File Processing

**Before (Go):**
```go
package main

import (
    "fmt"
    "io/ioutil"
    "os"
    "path/filepath"
    "sync"
)

type FileResult struct {
    Path  string
    Lines int
    Err   error
}

func countLines(path string) (int, error) {
    data, err := ioutil.ReadFile(path)
    if err != nil {
        return 0, err
    }

    lines := 0
    for _, b := range data {
        if b == '\n' {
            lines++
        }
    }
    return lines, nil
}

func processDirectory(dir string) ([]FileResult, error) {
    files, err := filepath.Glob(filepath.Join(dir, "*.txt"))
    if err != nil {
        return nil, err
    }

    results := make(chan FileResult, len(files))
    var wg sync.WaitGroup

    for _, file := range files {
        wg.Add(1)
        go func(path string) {
            defer wg.Done()
            lines, err := countLines(path)
            results <- FileResult{
                Path:  path,
                Lines: lines,
                Err:   err,
            }
        }(file)
    }

    go func() {
        wg.Wait()
        close(results)
    }()

    var allResults []FileResult
    for result := range results {
        allResults = append(allResults, result)
    }

    return allResults, nil
}
```

**After (Rust):**
```rust
use std::path::{Path, PathBuf};
use tokio::fs;
use tokio::task;
use glob::glob;

#[derive(Debug)]
struct FileResult {
    path: PathBuf,
    lines: usize,
    error: Option<String>,
}

async fn count_lines(path: &Path) -> Result<usize, std::io::Error> {
    let data = fs::read(path).await?;

    Ok(data.iter().filter(|&&b| b == b'\n').count())
}

async fn process_directory(dir: &Path) -> Result<Vec<FileResult>, Box<dyn std::error::Error>> {
    let pattern = dir.join("*.txt").display().to_string();
    let files: Vec<PathBuf> = glob(&pattern)?
        .filter_map(Result::ok)
        .collect();

    let handles: Vec<_> = files
        .into_iter()
        .map(|path| {
            task::spawn(async move {
                let lines_result = count_lines(&path).await;

                FileResult {
                    path: path.clone(),
                    lines: lines_result.as_ref().map(|&l| l).unwrap_or(0),
                    error: lines_result.err().map(|e| e.to_string()),
                }
            })
        })
        .collect();

    let mut all_results = Vec::new();
    for handle in handles {
        if let Ok(result) = handle.await {
            all_results.push(result);
        }
    }

    Ok(all_results)
}

// Alternative with futures::join_all:
use futures::future::join_all;

async fn process_directory_v2(dir: &Path) -> Result<Vec<FileResult>, Box<dyn std::error::Error>> {
    let pattern = dir.join("*.txt").display().to_string();
    let files: Vec<PathBuf> = glob(&pattern)?
        .filter_map(Result::ok)
        .collect();

    let futures = files.into_iter().map(|path| async move {
        let lines_result = count_lines(&path).await;

        FileResult {
            path: path.clone(),
            lines: lines_result.as_ref().map(|&l| l).unwrap_or(0),
            error: lines_result.err().map(|e| e.to_string()),
        }
    });

    Ok(join_all(futures).await)
}
```

**Key Changes:**
- `tokio::task::spawn` instead of goroutines
- Async file I/O with `tokio::fs`
- Iterator methods for concise code
- Type-safe error handling with `Result`
- No manual channel management (collect into `Vec`)

---

### Example 3: Complex - Web Server with Middleware

**Before (Go):**
```go
package main

import (
    "context"
    "encoding/json"
    "log"
    "net/http"
    "time"
)

type Server struct {
    db    Database
    cache Cache
}

type Database interface {
    GetUser(ctx context.Context, id string) (*User, error)
    CreateUser(ctx context.Context, user *User) error
}

type Cache interface {
    Get(key string) (interface{}, bool)
    Set(key string, value interface{}, ttl time.Duration)
}

type User struct {
    ID        string    `json:"id"`
    Email     string    `json:"email"`
    CreatedAt time.Time `json:"created_at"`
}

type CreateUserRequest struct {
    Email string `json:"email"`
}

func (s *Server) loggingMiddleware(next http.HandlerFunc) http.HandlerFunc {
    return func(w http.ResponseWriter, r *http.Request) {
        start := time.Now()
        log.Printf("Started %s %s", r.Method, r.URL.Path)

        next(w, r)

        log.Printf("Completed in %v", time.Since(start))
    }
}

func (s *Server) getUser(w http.ResponseWriter, r *http.Request) {
    id := r.URL.Query().Get("id")
    if id == "" {
        http.Error(w, "missing id parameter", http.StatusBadRequest)
        return
    }

    // Check cache first
    if cached, ok := s.cache.Get("user:" + id); ok {
        user := cached.(*User)
        json.NewEncoder(w).Encode(user)
        return
    }

    // Fetch from database
    ctx, cancel := context.WithTimeout(r.Context(), 5*time.Second)
    defer cancel()

    user, err := s.db.GetUser(ctx, id)
    if err != nil {
        http.Error(w, err.Error(), http.StatusInternalServerError)
        return
    }

    // Cache the result
    s.cache.Set("user:"+id, user, 5*time.Minute)

    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(user)
}

func (s *Server) createUser(w http.ResponseWriter, r *http.Request) {
    var req CreateUserRequest
    if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
        http.Error(w, err.Error(), http.StatusBadRequest)
        return
    }

    user := &User{
        ID:        generateID(),
        Email:     req.Email,
        CreatedAt: time.Now(),
    }

    ctx, cancel := context.WithTimeout(r.Context(), 5*time.Second)
    defer cancel()

    if err := s.db.CreateUser(ctx, user); err != nil {
        http.Error(w, err.Error(), http.StatusInternalServerError)
        return
    }

    w.Header().Set("Content-Type", "application/json")
    w.WriteHeader(http.StatusCreated)
    json.NewEncoder(w).Encode(user)
}

func main() {
    server := &Server{
        db:    &PostgresDB{},
        cache: &RedisCache{},
    }

    http.HandleFunc("/users", server.loggingMiddleware(server.getUser))
    http.HandleFunc("/users/create", server.loggingMiddleware(server.createUser))

    log.Fatal(http.ListenAndServe(":8080", nil))
}

func generateID() string {
    return "user-123" // Simplified
}
```

**After (Rust):**
```rust
use axum::{
    extract::{Query, State},
    http::StatusCode,
    middleware::{self, Next},
    response::{IntoResponse, Response},
    routing::{get, post},
    Json, Router,
};
use serde::{Deserialize, Serialize};
use std::sync::Arc;
use std::time::{Duration, Instant};
use tokio::time::timeout;
use tracing::{info, instrument};

// Traits (Go interfaces)
#[async_trait::async_trait]
trait Database: Send + Sync {
    async fn get_user(&self, id: &str) -> Result<User, DatabaseError>;
    async fn create_user(&self, user: &User) -> Result<(), DatabaseError>;
}

#[async_trait::async_trait]
trait Cache: Send + Sync {
    async fn get(&self, key: &str) -> Option<User>;
    async fn set(&self, key: &str, value: User, ttl: Duration);
}

// Error types
#[derive(Debug)]
enum DatabaseError {
    NotFound,
    Internal(String),
}

#[derive(Debug, Clone, Serialize, Deserialize)]
struct User {
    id: String,
    email: String,
    created_at: chrono::DateTime<chrono::Utc>,
}

#[derive(Deserialize)]
struct CreateUserRequest {
    email: String,
}

#[derive(Deserialize)]
struct GetUserQuery {
    id: String,
}

// Shared server state
struct AppState {
    db: Arc<dyn Database>,
    cache: Arc<dyn Cache>,
}

// Logging middleware
#[instrument(skip(req, next))]
async fn logging_middleware(
    req: axum::extract::Request,
    next: Next,
) -> Response {
    let method = req.method().clone();
    let uri = req.uri().clone();
    let start = Instant::now();

    info!("Started {} {}", method, uri);

    let response = next.run(req).await;

    info!("Completed in {:?}", start.elapsed());

    response
}

// Handlers
#[instrument(skip(state))]
async fn get_user(
    Query(params): Query<GetUserQuery>,
    State(state): State<Arc<AppState>>,
) -> Result<Json<User>, AppError> {
    let cache_key = format!("user:{}", params.id);

    // Check cache first
    if let Some(user) = state.cache.get(&cache_key).await {
        return Ok(Json(user));
    }

    // Fetch from database with timeout
    let user = timeout(
        Duration::from_secs(5),
        state.db.get_user(&params.id)
    )
    .await
    .map_err(|_| AppError::Timeout)?
    .map_err(AppError::Database)?;

    // Cache the result
    state.cache.set(&cache_key, user.clone(), Duration::from_secs(300)).await;

    Ok(Json(user))
}

#[instrument(skip(state))]
async fn create_user(
    State(state): State<Arc<AppState>>,
    Json(req): Json<CreateUserRequest>,
) -> Result<(StatusCode, Json<User>), AppError> {
    let user = User {
        id: generate_id(),
        email: req.email,
        created_at: chrono::Utc::now(),
    };

    // Create user with timeout
    timeout(
        Duration::from_secs(5),
        state.db.create_user(&user)
    )
    .await
    .map_err(|_| AppError::Timeout)?
    .map_err(AppError::Database)?;

    Ok((StatusCode::CREATED, Json(user)))
}

// Error handling
enum AppError {
    Database(DatabaseError),
    Timeout,
}

impl IntoResponse for AppError {
    fn into_response(self) -> Response {
        let (status, message) = match self {
            AppError::Database(DatabaseError::NotFound) => {
                (StatusCode::NOT_FOUND, "User not found")
            }
            AppError::Database(DatabaseError::Internal(msg)) => {
                (StatusCode::INTERNAL_SERVER_ERROR, "Internal error")
            }
            AppError::Timeout => {
                (StatusCode::REQUEST_TIMEOUT, "Request timeout")
            }
        };

        (status, message).into_response()
    }
}

fn generate_id() -> String {
    "user-123".to_string() // Simplified
}

#[tokio::main]
async fn main() {
    tracing_subscriber::fmt::init();

    let state = Arc::new(AppState {
        db: Arc::new(PostgresDB::new()),
        cache: Arc::new(RedisCache::new()),
    });

    let app = Router::new()
        .route("/users", get(get_user))
        .route("/users/create", post(create_user))
        .layer(middleware::from_fn(logging_middleware))
        .with_state(state);

    let listener = tokio::net::TcpListener::bind("0.0.0.0:8080")
        .await
        .unwrap();

    info!("Server listening on {}", listener.local_addr().unwrap());

    axum::serve(listener, app).await.unwrap();
}

// Placeholder implementations
struct PostgresDB;
impl PostgresDB {
    fn new() -> Self { PostgresDB }
}

#[async_trait::async_trait]
impl Database for PostgresDB {
    async fn get_user(&self, id: &str) -> Result<User, DatabaseError> {
        // Implementation
        todo!()
    }

    async fn create_user(&self, user: &User) -> Result<(), DatabaseError> {
        // Implementation
        todo!()
    }
}

struct RedisCache;
impl RedisCache {
    fn new() -> Self { RedisCache }
}

#[async_trait::async_trait]
impl Cache for RedisCache {
    async fn get(&self, key: &str) -> Option<User> {
        // Implementation
        None
    }

    async fn set(&self, key: &str, value: User, ttl: Duration) {
        // Implementation
    }
}
```

**Key Changes:**
- `axum` framework for type-safe routing
- Middleware as async functions
- Traits with `async_trait` for interfaces
- State sharing via `Arc<AppState>`
- Structured error handling with `IntoResponse`
- `tracing` for structured logging
- Type-safe extractors (`Query`, `Json`, `State`)
- Explicit timeout handling
- Clone for cache storage (explicit copying)

---

## See Also

For more examples and patterns, see:
- `meta-convert-dev` - Foundational patterns with cross-language examples
- `lang-go-dev` - Go development patterns
- `lang-rust-dev` - Rust development patterns
- `lang-rust-library-dev` - Rust library-specific patterns
- `lang-rust-memory-eng` - Advanced Rust memory management
