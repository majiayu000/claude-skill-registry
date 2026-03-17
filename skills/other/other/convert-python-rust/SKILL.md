---
name: convert-python-rust
description: Convert Python code to idiomatic Rust. Use when migrating Python projects to Rust, translating Python patterns to idiomatic Rust, or refactoring Python codebases for performance, safety, and concurrency. Extends meta-convert-dev with Python-to-Rust specific patterns.
---

# Convert Python to Rust

Convert Python code to idiomatic Rust. This skill extends `meta-convert-dev` with Python-to-Rust specific type mappings, idiom translations, and tooling for transforming dynamic, garbage-collected Python code into static, ownership-based Rust.

## This Skill Extends

- `meta-convert-dev` - Foundational conversion patterns (APTV workflow, testing strategies)

For general concepts like the Analyze → Plan → Transform → Validate workflow, testing strategies, and common pitfalls, see the meta-skill first.

## This Skill Adds

- **Type mappings**: Python types → Rust types (dynamic → static)
- **Idiom translations**: Python patterns → idiomatic Rust
- **Error handling**: Exceptions → Result<T, E>
- **Async patterns**: asyncio → tokio/async-std
- **Memory/Ownership**: GC + dynamic typing → ownership + borrowing + static types
- **Type system**: Duck typing → generics + traits

## This Skill Does NOT Cover

- General conversion methodology - see `meta-convert-dev`
- Python language fundamentals - see `lang-python-dev`
- Rust language fundamentals - see `lang-rust-dev`
- Reverse conversion (Rust → Python) - see `convert-rust-python`

---

## Quick Reference

| Python | Rust | Notes |
|--------|------|-------|
| `int` | `i32`, `i64`, `i128`, `num_bigint::BigInt` | Python has arbitrary precision |
| `float` | `f64` | Default float |
| `bool` | `bool` | Direct mapping |
| `str` | `String`, `&str` | Owned vs borrowed |
| `bytes` | `Vec<u8>`, `&[u8]` | Owned vs borrowed |
| `list[T]` | `Vec<T>` | Growable array |
| `tuple` | `(T, U, ...)` | Fixed-size tuple |
| `dict[K, V]` | `HashMap<K, V>`, `BTreeMap<K, V>` | Hash vs ordered |
| `set[T]` | `HashSet<T>`, `BTreeSet<T>` | Hash vs ordered |
| `None` | `Option<T>` | Explicit nullable |
| `Union[T, U]` | `enum { A(T), B(U) }` | Tagged union |
| `Callable[[Args], Ret]` | `Fn(Args) -> Ret` | Function trait |
| `async def` | `async fn` | Async function |
| `@dataclass` | `#[derive(Debug, Clone)]` struct | Data classes |
| `Exception` | `Result<T, E>` | Error handling |

## When Converting Code

1. **Analyze source thoroughly** before writing target
2. **Map types first** - create type equivalence table
3. **Handle arbitrary-precision integers** - decide if `i64` is enough or if you need `BigInt`
4. **Preserve semantics** over syntax similarity
5. **Adopt Rust idioms** - don't write "Python code in Rust syntax"
6. **Handle edge cases** - None, exceptions, dynamic typing assumptions
7. **Test equivalence** - same inputs → same outputs

---

## Type System Mapping

### Primitive Types

| Python | Rust | Notes |
|--------|------|-------|
| `int` | `i32` | Default for small integers |
| `int` | `i64` | Large integers (64-bit) |
| `int` | `i128` | Very large integers (128-bit) |
| `int` | `num_bigint::BigInt` | **Python default** - arbitrary precision |
| `float` | `f64` | IEEE 754 double precision |
| `bool` | `bool` | Direct mapping |
| `str` | `String` | Owned, heap-allocated UTF-8 |
| `str` | `&str` | Borrowed string slice |
| `bytes` | `Vec<u8>` | Owned byte vector |
| `bytes` | `&[u8]` | Borrowed byte slice |
| `bytearray` | `Vec<u8>` | Mutable byte vector |
| `None` | `Option<T>` | Use `None` variant |
| `...` (Ellipsis) | - | No direct equivalent |

**Critical Note on Integers**: Python's `int` type has **arbitrary precision** and never overflows. Rust integers are fixed-size and **can overflow** (panic in debug, wrap in release). Always validate range or use `BigInt` for Python-like behavior.

### Collection Types

| Python | Rust | Notes |
|--------|------|-------|
| `list[T]` | `Vec<T>` | Owned, growable, ordered |
| `tuple` | `(T, U, ...)` | Fixed-size, immutable |
| `tuple[T, ...]` | `Vec<T>` | Variable-length tuple → Vec |
| `dict[K, V]` | `HashMap<K, V>` | Hash-based, unordered |
| `dict[K, V]` | `BTreeMap<K, V>` | Tree-based, ordered |
| `set[T]` | `HashSet<T>` | Hash-based, unique values |
| `set[T]` | `BTreeSet<T>` | Tree-based, ordered unique |
| `frozenset[T]` | `HashSet<T>` | Immutable by default in Rust |
| `collections.deque` | `VecDeque<T>` | Double-ended queue |
| `collections.OrderedDict` | `indexmap::IndexMap<K, V>` | Insertion-order map |
| `collections.defaultdict` | `HashMap` + `entry()` API | Use `or_insert()` pattern |
| `collections.Counter` | `HashMap<T, usize>` | Count occurrences |

### Composite Types

| Python | Rust | Notes |
|--------|------|-------|
| `class` (data) | `struct` | Data containers |
| `class` (behavior) | `trait` + `impl` | Behavior contracts |
| `@dataclass` | `#[derive(Debug, Clone)]` struct | Auto-derive common traits |
| `typing.Protocol` | `trait` | Structural types → nominal traits |
| `typing.TypedDict` | `struct` | Named fields |
| `typing.NamedTuple` | `struct` or tuple | Prefer struct for clarity |
| `enum.Enum` | `enum` | Algebraic data types |
| `typing.Literal["a", "b"]` | `enum { A, B }` | Literal types → enums |
| `typing.Union[T, U]` | `enum { A(T), B(U) }` | Tagged union |
| `typing.Optional[T]` | `Option<T>` | Nullable types |
| `typing.Callable[[Args], Ret]` | `Fn(Args) -> Ret` | Function types |
| `typing.Generic[T]` | `<T>` | Generic types |

### Type Annotations → Generics + Traits

| Python | Rust | Notes |
|--------|------|-------|
| `def f(x: T) -> T` | `fn f<T>(x: T) -> T` | Unconstrained generic |
| `def f(x: Iterable[T])` | `fn f<T, I: IntoIterator<Item=T>>` | Trait bound |
| `def f(x: Sequence[T])` | `fn f<T>(x: &[T])` | Slice for sequences |
| `x: Any` | **Avoid** - use generics | `Any` is a code smell |
| `x: object` | **Avoid** - use generics | No Object root in Rust |

---

## Idiom Translation

### Pattern 1: None Handling (Optional Chaining)

**Python:**
```python
# Optional chaining with walrus operator
if user := get_user(user_id):
    name = user.name
else:
    name = "Anonymous"

# Or simpler
name = user.name if user else "Anonymous"
```

**Rust:**
```rust
// Option combinators
let name = get_user(user_id)
    .map(|u| u.name.clone())
    .unwrap_or_else(|| "Anonymous".to_string());

// Or with as_ref() to avoid moving
let name = get_user(user_id)
    .as_ref()
    .map(|u| u.name.as_str())
    .unwrap_or("Anonymous");
```

**Why this translation:**
- Python uses truthiness (`if user`) while Rust uses explicit `Option<T>`
- Rust's combinator methods (`map`, `unwrap_or`) are more explicit about handling the `None` case
- `as_ref()` converts `Option<T>` to `Option<&T>` to avoid consuming the value

### Pattern 2: List Comprehensions → Iterator Chains

**Python:**
```python
# List comprehension
squared_evens = [x * x for x in numbers if x % 2 == 0]

# Generator expression
total = sum(x * x for x in numbers if x % 2 == 0)
```

**Rust:**
```rust
// Iterator chain (collect for Vec)
let squared_evens: Vec<i32> = numbers
    .iter()
    .filter(|x| *x % 2 == 0)
    .map(|x| x * x)
    .collect();

// Iterator chain (sum for aggregation)
let total: i32 = numbers
    .iter()
    .filter(|x| *x % 2 == 0)
    .map(|x| x * x)
    .sum();
```

**Why this translation:**
- Python list comprehensions are eager; Rust iterators are lazy (more efficient)
- Rust requires explicit `collect()` to materialize into a collection
- Terminal operations like `sum()` consume the iterator automatically

### Pattern 3: Dictionary Operations

**Python:**
```python
# Get with default
value = config.get("timeout", 30)

# Setdefault pattern
cache.setdefault(key, expensive_compute())

# Dictionary comprehension
squared = {k: v * v for k, v in items.items()}
```

**Rust:**
```rust
// Get with default
let value = config.get("timeout").copied().unwrap_or(30);

// Entry API (doesn't compute if present)
let value = cache.entry(key).or_insert_with(|| expensive_compute());

// Collect from iterator
let squared: HashMap<K, i32> = items
    .into_iter()
    .map(|(k, v)| (k, v * v))
    .collect();
```

**Why this translation:**
- Rust's `entry()` API is more efficient than Python's `setdefault()` for expensive defaults
- `or_insert_with()` takes a closure, only calling it if the key is missing
- Rust's iterator `collect()` can build many collection types, including `HashMap`

### Pattern 4: String Formatting

**Python:**
```python
# f-strings (Python 3.6+)
message = f"User {user.name} has {count} items"

# format method
message = "User {} has {} items".format(user.name, count)

# % formatting (old style)
message = "User %s has %d items" % (user.name, count)
```

**Rust:**
```rust
// format! macro (heap-allocated)
let message = format!("User {} has {} items", user.name, count);

// print! / println! macros (direct output)
println!("User {} has {} items", user.name, count);

// write! macro (into a buffer)
use std::fmt::Write;
let mut buf = String::new();
write!(&mut buf, "User {} has {} items", user.name, count).unwrap();
```

**Why this translation:**
- Rust's `format!` macro is compile-time checked for type safety
- `{}` is the default placeholder; use `{:?}` for debug output, `{:#?}` for pretty-print
- Rust doesn't have string interpolation; use macros instead

### Pattern 5: Duck Typing → Traits

**Python:**
```python
# Duck typing - if it has a .read() method, it's file-like
def process_data(file_like):
    data = file_like.read()
    return parse(data)

# Works with files, StringIO, BytesIO, etc.
```

**Rust:**
```rust
// Trait bounds - explicit interface
use std::io::Read;

fn process_data<R: Read>(mut reader: R) -> Result<Data, Error> {
    let mut data = String::new();
    reader.read_to_string(&mut data)?;
    parse(&data)
}

// Works with File, Cursor, TcpStream, etc. (anything implementing Read)
```

**Why this translation:**
- Python relies on runtime checks (duck typing); Rust checks at compile time
- Rust traits are explicit contracts, catching errors early
- Generic functions in Rust are monomorphized (one compiled version per concrete type)

### Pattern 6: Context Managers → RAII

**Python:**
```python
# with statement for resource management
with open("data.txt") as f:
    data = f.read()
# File automatically closed

# Custom context manager
with lock_held(mutex):
    # Critical section
    pass
# Lock automatically released
```

**Rust:**
```rust
// RAII - Drop trait handles cleanup
{
    let f = File::open("data.txt")?;
    let mut data = String::new();
    f.read_to_string(&mut data)?;
    // File automatically closed when f goes out of scope
}

// Mutex guard - RAII
{
    let guard = mutex.lock().unwrap();
    // Critical section - guard holds the lock
    // Lock automatically released when guard is dropped
}
```

**Why this translation:**
- Python uses `__enter__` / `__exit__` protocols; Rust uses `Drop` trait
- Rust's ownership system guarantees cleanup at scope exit (compile-time enforced)
- No need for explicit `with` statement - scope-based cleanup is automatic

### Pattern 7: Dynamic Attribute Access

**Python:**
```python
# Dynamic attribute access
value = getattr(obj, "field", default)
setattr(obj, "field", value)
hasattr(obj, "field")

# Dynamic method calls
method = getattr(obj, method_name)
result = method(*args)
```

**Rust:**
```rust
// Static access only - use enums for dynamic behavior
enum Field {
    Name(String),
    Age(u32),
    Email(String),
}

impl Object {
    fn get_field(&self, field: &str) -> Option<Field> {
        match field {
            "name" => Some(Field::Name(self.name.clone())),
            "age" => Some(Field::Age(self.age)),
            "email" => Some(Field::Email(self.email.clone())),
            _ => None,
        }
    }
}

// For true dynamic behavior, use HashMap
struct DynamicObject {
    fields: HashMap<String, Value>,
}
```

**Why this translation:**
- Rust has no runtime reflection for dynamic attribute access
- Use enums for known variants, `HashMap` for truly dynamic data
- Trade runtime flexibility for compile-time safety and performance

### Pattern 8: Exception Chaining

**Python:**
```python
# Exception chaining
try:
    data = fetch_data(url)
except NetworkError as e:
    raise ProcessingError(f"Failed to fetch {url}") from e

# Catching and re-raising
try:
    risky_operation()
except Exception:
    logger.error("Operation failed")
    raise
```

**Rust:**
```rust
// Error conversion with context
fn fetch_data(url: &str) -> Result<Data, ProcessingError> {
    let data = fetch(url)
        .map_err(|e| ProcessingError::FetchFailed {
            url: url.to_string(),
            source: e,
        })?;
    Ok(data)
}

// Using anyhow for error context
use anyhow::Context;

fn fetch_data(url: &str) -> anyhow::Result<Data> {
    fetch(url)
        .context(format!("Failed to fetch {}", url))?;
    Ok(data)
}
```

**Why this translation:**
- Rust doesn't have exception chaining; use nested error types or libraries like `anyhow`
- `map_err()` transforms errors explicitly
- `?` operator propagates errors up the call stack (like re-raising)

### Pattern 9: Multiple Return Values

**Python:**
```python
# Tuple unpacking
def parse_coord(s):
    parts = s.split(",")
    return int(parts[0]), int(parts[1])

x, y = parse_coord("10,20")
```

**Rust:**
```rust
// Tuple return
fn parse_coord(s: &str) -> Result<(i32, i32), ParseError> {
    let parts: Vec<&str> = s.split(',').collect();
    let x = parts[0].parse()?;
    let y = parts[1].parse()?;
    Ok((x, y))
}

let (x, y) = parse_coord("10,20")?;

// Named struct (preferred for clarity)
#[derive(Debug)]
struct Coord { x: i32, y: i32 }

fn parse_coord(s: &str) -> Result<Coord, ParseError> {
    let parts: Vec<&str> = s.split(',').collect();
    Ok(Coord {
        x: parts[0].parse()?,
        y: parts[1].parse()?,
    })
}
```

**Why this translation:**
- Both languages support tuple returns
- Rust prefers named structs for complex returns (better documentation, field names)
- Rust requires explicit error handling (hence `Result`)

### Pattern 10: Decorators → Macros or Trait Implementations

**Python:**
```python
# Function decorator
@cache
def expensive_func(x):
    return compute(x)

# Class decorator
@dataclass
class Point:
    x: int
    y: int

# Property decorator
@property
def full_name(self):
    return f"{self.first} {self.last}"
```

**Rust:**
```rust
// Procedural macro (like class decorator)
#[derive(Debug, Clone, PartialEq)]
struct Point {
    x: i32,
    y: i32,
}

// Manual memoization (no decorator syntax)
use std::collections::HashMap;
use std::cell::RefCell;

thread_local! {
    static CACHE: RefCell<HashMap<i32, i32>> = RefCell::new(HashMap::new());
}

fn expensive_func(x: i32) -> i32 {
    CACHE.with(|cache| {
        cache.borrow_mut().entry(x).or_insert_with(|| compute(x)).clone()
    })
}

// Computed properties (no @property syntax)
impl Person {
    fn full_name(&self) -> String {
        format!("{} {}", self.first, self.last)
    }
}
```

**Why this translation:**
- Rust has no decorator syntax; use `#[derive(...)]` for common patterns
- Function decorators require manual implementation or crates like `cached`
- Properties are just methods in Rust (no special syntax)

---

## Error Handling

### Python Exception Model → Rust Result Model

| Python | Rust | Notes |
|--------|------|-------|
| `raise Exception("error")` | `return Err(Error::Message)` | Exceptions → Result |
| `try: ... except E: ...` | `match result { Ok(v) => ..., Err(e) => ... }` | Pattern matching |
| `try: ... except: ...` | **Anti-pattern** - always specify error type | No catch-all |
| `try: ... finally: ...` | RAII / Drop trait | Automatic cleanup |
| `raise ... from ...` | Nested error types or `anyhow::Context` | Error chains |
| `assert x, "msg"` | `assert!(x, "msg")` | Panic for invariants |

### Exception Hierarchy Translation

**Python:**
```python
# Exception hierarchy
class AppError(Exception):
    pass

class NetworkError(AppError):
    def __init__(self, url, status):
        self.url = url
        self.status = status
        super().__init__(f"Network error for {url}: {status}")

class ParseError(AppError):
    def __init__(self, message):
        self.message = message
        super().__init__(message)

# Raising exceptions
if response.status_code != 200:
    raise NetworkError(url, response.status_code)

# Catching exceptions
try:
    data = fetch_and_parse(url)
except NetworkError as e:
    log.error(f"Network error: {e.url} returned {e.status}")
    retry()
except ParseError as e:
    log.error(f"Parse error: {e.message}")
    return None
```

**Rust:**
```rust
// Error enum with thiserror
use thiserror::Error;

#[derive(Debug, Error)]
enum AppError {
    #[error("Network error for {url}: {status}")]
    Network { url: String, status: u16 },

    #[error("Parse error: {message}")]
    Parse { message: String },

    #[error(transparent)]
    Io(#[from] std::io::Error),
}

// Returning errors
fn fetch(url: &str) -> Result<Data, AppError> {
    let response = http_get(url)?;
    if response.status() != 200 {
        return Err(AppError::Network {
            url: url.to_string(),
            status: response.status(),
        });
    }
    Ok(response.data())
}

// Handling errors
match fetch_and_parse(url) {
    Ok(data) => process(data),
    Err(AppError::Network { url, status }) => {
        log::error!("Network error: {} returned {}", url, status);
        retry()?;
    }
    Err(AppError::Parse { message }) => {
        log::error!("Parse error: {}", message);
        return None;
    }
    Err(e) => return Err(e),
}
```

**Why this translation:**
- Python uses exception inheritance; Rust uses enum variants
- Rust's `thiserror` crate provides `Display` and `Error` trait implementations
- `?` operator propagates errors (like Python's exception unwinding)
- Pattern matching is more explicit than try-except blocks

### Error Propagation Patterns

**Python:**
```python
# Implicit propagation (exception bubbles up)
def outer():
    return inner()  # Exceptions propagate automatically

def inner():
    raise ValueError("error")
```

**Rust:**
```rust
// Explicit propagation with ?
fn outer() -> Result<Data, Error> {
    let data = inner()?;  // ? propagates Err variants
    Ok(data)
}

fn inner() -> Result<Data, Error> {
    Err(Error::Message("error".to_string()))
}
```

**Why this translation:**
- Python exceptions propagate implicitly; Rust requires explicit `?` or pattern matching
- Rust's approach forces you to think about error handling at each call site
- Type system ensures errors are handled or explicitly propagated

---

## Async Patterns

### Python asyncio → Rust tokio/async-std

| Python | Rust (tokio) | Notes |
|--------|--------------|-------|
| `async def f(): ...` | `async fn f() { ... }` | Async function |
| `await coro` | `coro.await` | Await syntax |
| `asyncio.run(coro)` | `tokio::runtime::Runtime::new()?.block_on(coro)` | Run async code |
| `asyncio.gather(*coros)` | `tokio::join!(coros)` or `futures::join_all` | Concurrent execution |
| `asyncio.create_task(coro)` | `tokio::spawn(coro)` | Background task |
| `asyncio.sleep(secs)` | `tokio::time::sleep(Duration::from_secs(secs))` | Async sleep |
| `asyncio.wait_for(coro, timeout)` | `tokio::time::timeout(duration, coro)` | Timeout |
| `asyncio.Queue` | `tokio::sync::mpsc::channel` | Async channel |
| `asyncio.Lock` | `tokio::sync::Mutex` | Async mutex |

### Basic Async Function Translation

**Python:**
```python
import asyncio

async def fetch_user(user_id: int) -> User:
    async with aiohttp.ClientSession() as session:
        async with session.get(f"/users/{user_id}") as response:
            data = await response.json()
            return User(**data)

# Running async code
async def main():
    user = await fetch_user(123)
    print(user)

asyncio.run(main())
```

**Rust:**
```rust
use tokio;
use reqwest;

async fn fetch_user(user_id: u32) -> Result<User, reqwest::Error> {
    let url = format!("/users/{}", user_id);
    let user = reqwest::get(&url)
        .await?
        .json::<User>()
        .await?;
    Ok(user)
}

// Running async code
#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let user = fetch_user(123).await?;
    println!("{:?}", user);
    Ok(())
}
```

**Why this translation:**
- Both use `async`/`await` syntax
- Python's context managers become RAII in Rust (automatic cleanup)
- Rust requires explicit error handling (`Result` + `?`)
- `#[tokio::main]` macro sets up the async runtime automatically

### Concurrent Execution

**Python:**
```python
# asyncio.gather for concurrent execution
users, orders = await asyncio.gather(
    fetch_users(),
    fetch_orders()
)

# asyncio.create_task for background tasks
task1 = asyncio.create_task(fetch_users())
task2 = asyncio.create_task(fetch_orders())
users = await task1
orders = await task2
```

**Rust:**
```rust
// tokio::join! for concurrent execution (fixed number)
let (users, orders) = tokio::join!(
    fetch_users(),
    fetch_orders()
);

// tokio::spawn for background tasks
let task1 = tokio::spawn(fetch_users());
let task2 = tokio::spawn(fetch_orders());
let users = task1.await??;  // First ? for JoinError, second for task error
let orders = task2.await??;

// futures::join_all for dynamic list
use futures::future::join_all;
let tasks: Vec<_> = ids.into_iter().map(fetch_user).collect();
let users = join_all(tasks).await;
```

**Why this translation:**
- `tokio::join!` is macro-based (compile-time), similar to `asyncio.gather`
- `tokio::spawn` creates a separate task (like `create_task`)
- Spawned tasks return `JoinHandle`, requiring double `??` to unwrap both join and task errors

### Async Streams/Generators

**Python:**
```python
# Async generator
async def fetch_pages(url: str):
    page = 1
    while True:
        response = await fetch(f"{url}?page={page}")
        if not response.ok:
            break
        yield await response.json()
        page += 1

# Consuming async generator
async for page in fetch_pages(url):
    process(page)
```

**Rust:**
```rust
// Async stream (using async-stream crate)
use async_stream::stream;
use futures::stream::Stream;

fn fetch_pages(url: String) -> impl Stream<Item = Result<Page, Error>> {
    stream! {
        let mut page = 1;
        loop {
            let response = fetch(&format!("{}?page={}", url, page)).await?;
            if !response.status().is_success() {
                break;
            }
            yield response.json::<Page>().await?;
            page += 1;
        }
    }
}

// Consuming async stream
use futures::stream::StreamExt;

let mut pages = fetch_pages(url);
while let Some(result) = pages.next().await {
    match result {
        Ok(page) => process(page),
        Err(e) => eprintln!("Error: {}", e),
    }
}
```

**Why this translation:**
- Python's `async for` → Rust's `StreamExt::next()` in a loop
- Rust requires `async-stream` crate for generator-like syntax
- Streams yield `Result` for error handling (Python would raise exceptions)

### Cancellation and Timeouts

**Python:**
```python
# Timeout with asyncio.wait_for
try:
    result = await asyncio.wait_for(fetch_data(url), timeout=5.0)
except asyncio.TimeoutError:
    print("Request timed out")

# Manual cancellation
task = asyncio.create_task(long_operation())
# ... later
task.cancel()
try:
    await task
except asyncio.CancelledError:
    print("Task was cancelled")
```

**Rust:**
```rust
// Timeout with tokio::time::timeout
use tokio::time::{timeout, Duration};

match timeout(Duration::from_secs(5), fetch_data(url)).await {
    Ok(Ok(result)) => println!("Success: {:?}", result),
    Ok(Err(e)) => println!("Request failed: {}", e),
    Err(_) => println!("Request timed out"),
}

// Manual cancellation via drop
let handle = tokio::spawn(long_operation());
// ... later
handle.abort();  // Cancel the task
match handle.await {
    Ok(result) => println!("Completed: {:?}", result),
    Err(e) if e.is_cancelled() => println!("Task was cancelled"),
    Err(e) => println!("Task failed: {}", e),
}
```

**Why this translation:**
- Python uses `asyncio.wait_for`; Rust uses `tokio::time::timeout`
- Rust's `timeout` returns `Result<Result<T, E>, Elapsed>` (nested Results)
- Cancellation in Rust happens via `abort()` on `JoinHandle`

---

## Memory & Ownership

### Python GC → Rust Ownership

| Python Model | Rust Model | Translation |
|--------------|------------|-------------|
| Reference counting + cycle detection | Ownership + borrowing | Explicit ownership transfer |
| Shared references everywhere | `&T` (immutable) or `&mut T` (mutable) | Borrow checker enforces aliasing rules |
| Mutable by default | Immutable by default (`let` vs `let mut`) | Explicit mutability |
| No lifetime tracking | Explicit lifetimes (`'a`) | Compiler ensures references are valid |
| `del` or rely on GC | `Drop` trait (RAII) | Automatic, deterministic cleanup |

### Ownership Decision Patterns

**Python (shared references):**
```python
# Python allows multiple mutable references
class Cache:
    def __init__(self):
        self.data = {}

    def get(self, key):
        return self.data.get(key)

    def set(self, key, value):
        self.data[key] = value

# Multiple references to cache
cache = Cache()
ref1 = cache
ref2 = cache
ref1.set("key", "value")
print(ref2.get("key"))  # Works fine
```

**Rust (explicit ownership):**
```rust
use std::collections::HashMap;

struct Cache {
    data: HashMap<String, String>,
}

impl Cache {
    fn new() -> Self {
        Self { data: HashMap::new() }
    }

    // Borrow immutably (read-only)
    fn get(&self, key: &str) -> Option<&String> {
        self.data.get(key)
    }

    // Borrow mutably (write access)
    fn set(&mut self, key: String, value: String) {
        self.data.insert(key, value);
    }
}

// Single owner, multiple borrows
let mut cache = Cache::new();
cache.set("key".to_string(), "value".to_string());
println!("{:?}", cache.get("key"));

// For shared ownership, use Rc/Arc
use std::rc::Rc;
use std::cell::RefCell;

let cache = Rc::new(RefCell::new(Cache::new()));
let ref1 = Rc::clone(&cache);
let ref2 = Rc::clone(&cache);
ref1.borrow_mut().set("key".to_string(), "value".to_string());
println!("{:?}", ref2.borrow().get("key"));
```

**Why this translation:**
- Python's GC allows unrestricted shared mutable state
- Rust enforces "either one mutable reference OR many immutable references"
- For Python-like shared mutability, use `Rc<RefCell<T>>` (single-threaded) or `Arc<Mutex<T>>` (multi-threaded)

### Avoiding Clone Overhead

**Python (cloning is implicit and cheap):**
```python
def process_items(items):
    # Items can be passed around freely
    for item in items:
        handle(item)
        transform(item)
```

**Rust (explicit borrowing to avoid clones):**
```rust
// BAD: Unnecessary cloning
fn process_items(items: Vec<Item>) {
    for item in items.clone() {  // Clones entire vector!
        handle(&item);
        transform(&item);
    }
}

// GOOD: Borrow instead
fn process_items(items: &[Item]) {
    for item in items {
        handle(item);  // item is &Item
        transform(item);
    }
}

// If mutation needed, use &mut
fn process_items_mut(items: &mut [Item]) {
    for item in items {
        transform_in_place(item);  // item is &mut Item
    }
}
```

**Why this translation:**
- Python's reference counting makes passing references cheap
- Rust's ownership requires explicit choices: move, borrow, or clone
- Prefer borrowing (`&T`, `&mut T`) over cloning for performance

### Lifetime Elision and Annotations

**Python (no lifetime concept):**
```python
class Parser:
    def __init__(self, source):
        self.source = source

    def parse(self):
        # Can reference self.source freely
        return self.source.split()
```

**Rust (explicit lifetimes):**
```rust
// Lifetime elision - compiler infers lifetimes
struct Parser<'a> {
    source: &'a str,
}

impl<'a> Parser<'a> {
    fn new(source: &'a str) -> Self {
        Self { source }
    }

    fn parse(&self) -> Vec<&'a str> {
        self.source.split_whitespace().collect()
    }
}

// The 'a lifetime ties the parser to the source string
// Parser cannot outlive the source
```

**Why this translation:**
- Python's GC allows references to outlive their source
- Rust's borrow checker prevents dangling references at compile time
- Explicit lifetimes document reference validity constraints

---

## Type System Translation

### Duck Typing → Generics + Traits

**Python (duck typing):**
```python
# Any object with .read() method works
def process_file(file_like):
    data = file_like.read()
    return parse(data)

# Works with files, StringIO, BytesIO, etc.
with open("data.txt") as f:
    process_file(f)
```

**Rust (trait bounds):**
```rust
use std::io::Read;

fn process_file<R: Read>(mut reader: R) -> Result<Data, Error> {
    let mut data = String::new();
    reader.read_to_string(&mut data)?;
    parse(&data)
}

// Works with File, Cursor, TcpStream, etc.
let f = File::open("data.txt")?;
process_file(f)?;
```

**Why this translation:**
- Python checks method existence at runtime (duck typing)
- Rust checks trait implementation at compile time
- Generics with trait bounds provide type safety without runtime overhead

### TypedDict / NamedTuple → Struct

**Python:**
```python
from typing import TypedDict, NamedTuple

# TypedDict (Python 3.8+)
class User(TypedDict):
    id: int
    name: str
    email: str

# NamedTuple
class Point(NamedTuple):
    x: int
    y: int

user: User = {"id": 1, "name": "Alice", "email": "alice@example.com"}
point = Point(x=10, y=20)
```

**Rust:**
```rust
// Struct with derive macros
#[derive(Debug, Clone, PartialEq)]
struct User {
    id: u32,
    name: String,
    email: String,
}

#[derive(Debug, Clone, Copy, PartialEq)]
struct Point {
    x: i32,
    y: i32,
}

let user = User {
    id: 1,
    name: "Alice".to_string(),
    email: "alice@example.com".to_string(),
};

let point = Point { x: 10, y: 20 };
```

**Why this translation:**
- Python's `TypedDict` is for type hints; Rust's structs are enforced at compile time
- Rust's `#[derive]` macros auto-generate common trait implementations
- Rust structs require owned data (`String` not `&str` for struct fields)

### Union Types → Enums

**Python:**
```python
from typing import Union

# Union type
def process(value: Union[int, str]) -> str:
    if isinstance(value, int):
        return f"Number: {value}"
    else:
        return f"String: {value}"

result = process(42)
result = process("hello")
```

**Rust:**
```rust
// Tagged union (enum)
enum Value {
    Number(i32),
    Text(String),
}

fn process(value: Value) -> String {
    match value {
        Value::Number(n) => format!("Number: {}", n),
        Value::Text(s) => format!("String: {}", s),
    }
}

let result = process(Value::Number(42));
let result = process(Value::Text("hello".to_string()));
```

**Why this translation:**
- Python's `Union` is a type hint checked by mypy/pyright
- Rust's enums are tagged unions, enforcing exhaustive pattern matching
- Rust catches missing match cases at compile time

### Protocol (Structural) → Trait (Nominal)

**Python:**
```python
from typing import Protocol

# Structural typing
class Drawable(Protocol):
    def draw(self) -> None:
        ...

# Any class with a draw() method satisfies Drawable
class Circle:
    def draw(self) -> None:
        print("Drawing circle")

def render(obj: Drawable) -> None:
    obj.draw()

render(Circle())  # Works due to structural typing
```

**Rust:**
```rust
// Nominal typing - must explicitly implement trait
trait Drawable {
    fn draw(&self);
}

struct Circle;

impl Drawable for Circle {
    fn draw(&self) {
        println!("Drawing circle");
    }
}

fn render<T: Drawable>(obj: &T) {
    obj.draw();
}

render(&Circle);  // Only works if Circle explicitly implements Drawable
```

**Why this translation:**
- Python's `Protocol` uses structural typing (method signature match)
- Rust's traits require explicit `impl Trait for Type` declarations
- Rust's approach enables better error messages and clearer intent

---

## Common Pitfalls

### 1. Arbitrary Precision Integer Overflow

**Problem:**
```rust
// Python: unlimited integer size
# x = 10 ** 100  # Works fine

// Rust: fixed-size integers
let x: i32 = 10_i32.pow(100);  // PANIC! Overflow in debug mode
```

**Solution:**
```rust
// Use appropriate size or BigInt
use num_bigint::BigInt;
use num_traits::pow::Pow;

let x = BigInt::from(10).pow(100_u32);  // No overflow
```

**Why this matters:** Python integers never overflow; Rust integers panic (debug) or wrap (release).

### 2. Mutable Aliasing

**Problem:**
```rust
// Python: multiple mutable references allowed
# items = [1, 2, 3]
# ref1 = items
# ref2 = items
# ref1.append(4)
# ref2.append(5)

// Rust: borrow checker prevents this
let mut items = vec![1, 2, 3];
let ref1 = &mut items;
let ref2 = &mut items;  // ERROR: cannot borrow as mutable more than once
```

**Solution:**
```rust
// Use scopes to separate borrows
{
    let ref1 = &mut items;
    ref1.push(4);
}
{
    let ref2 = &mut items;
    ref2.push(5);
}

// Or use interior mutability (Rc<RefCell<T>> or Arc<Mutex<T>>)
```

**Why this matters:** Rust prevents data races at compile time; Python allows them.

### 3. String Ownership

**Problem:**
```rust
// Python: strings are immutable but freely aliased
# name = user.get("name")
# print(name)

// Rust: String vs &str confusion
fn get_name(user: &HashMap<String, String>) -> &str {
    user.get("name").unwrap()  // Returns &String, not &str
}
```

**Solution:**
```rust
// Use .as_str() or accept &str
fn get_name(user: &HashMap<String, String>) -> &str {
    user.get("name").unwrap().as_str()
}

// Or return Option<&str>
fn get_name(user: &HashMap<String, String>) -> Option<&str> {
    user.get("name").map(|s| s.as_str())
}
```

**Why this matters:** Rust distinguishes owned (`String`) and borrowed (`&str`) strings.

### 4. Truthiness vs Explicit Boolean

**Problem:**
```rust
// Python: truthy/falsy values
# if items:  # Empty list is falsy
#     process(items)

// Rust: explicit boolean checks required
if items {  // ERROR: expected `bool`, found `Vec<T>`
    process(&items);
}
```

**Solution:**
```rust
// Explicitly check for emptiness
if !items.is_empty() {
    process(&items);
}

// Or check for None
if let Some(value) = option {
    process(value);
}
```

**Why this matters:** Rust has no implicit truthiness; always use explicit boolean expressions.

### 5. Default Arguments vs Builder Pattern

**Problem:**
```rust
// Python: default arguments
# def connect(host, port=80, timeout=30):
#     ...

// Rust: no default arguments
fn connect(host: &str, port: u16, timeout: u64) -> Connection {
    // All arguments required!
}
```

**Solution:**
```rust
// Use Option for optional parameters
fn connect(host: &str, port: Option<u16>, timeout: Option<u64>) -> Connection {
    let port = port.unwrap_or(80);
    let timeout = timeout.unwrap_or(30);
    // ...
}

// Or use builder pattern
struct ConnectionBuilder {
    host: String,
    port: u16,
    timeout: u64,
}

impl ConnectionBuilder {
    fn new(host: String) -> Self {
        Self { host, port: 80, timeout: 30 }
    }

    fn port(mut self, port: u16) -> Self {
        self.port = port;
        self
    }

    fn timeout(mut self, timeout: u64) -> Self {
        self.timeout = timeout;
        self
    }

    fn connect(self) -> Connection {
        // ...
    }
}

// Usage
let conn = ConnectionBuilder::new("localhost")
    .port(8080)
    .timeout(60)
    .connect();
```

**Why this matters:** Rust has no default arguments; use `Option` or builder pattern for ergonomics.

### 6. List Modification During Iteration

**Problem:**
```rust
// Python: modifying list during iteration (undefined behavior)
# for item in items:
#     if condition(item):
#         items.remove(item)  # Dangerous!

// Rust: borrow checker prevents this
for item in &items {
    if condition(item) {
        items.remove(item);  // ERROR: cannot borrow as mutable while borrowed
    }
}
```

**Solution:**
```rust
// Collect indices to remove, then remove in reverse
let to_remove: Vec<usize> = items.iter()
    .enumerate()
    .filter(|(_, item)| condition(item))
    .map(|(i, _)| i)
    .collect();

for &i in to_remove.iter().rev() {
    items.remove(i);
}

// Or use retain
items.retain(|item| !condition(item));
```

**Why this matters:** Rust prevents iterator invalidation at compile time.

### 7. Global Mutable State

**Problem:**
```rust
// Python: global mutable state is easy
# counter = 0
# def increment():
#     global counter
#     counter += 1

// Rust: global mutable state requires unsafe or synchronization
static mut COUNTER: i32 = 0;  // Unsafe!

fn increment() {
    unsafe {
        COUNTER += 1;  // Requires unsafe block
    }
}
```

**Solution:**
```rust
// Use static with Mutex or Atomic
use std::sync::Mutex;

static COUNTER: Mutex<i32> = Mutex::new(0);

fn increment() {
    let mut counter = COUNTER.lock().unwrap();
    *counter += 1;
}

// Or use atomic types for simple counters
use std::sync::atomic::{AtomicI32, Ordering};

static COUNTER: AtomicI32 = AtomicI32::new(0);

fn increment() {
    COUNTER.fetch_add(1, Ordering::SeqCst);
}
```

**Why this matters:** Rust makes global mutable state explicit and safe via synchronization primitives.

### 8. Exception vs Result Propagation

**Problem:**
```rust
// Python: exceptions propagate automatically
# def outer():
#     return inner()  # Exceptions bubble up

# def inner():
#     raise ValueError("error")

// Rust: forgetting ? operator
fn outer() -> Result<Data, Error> {
    let data = inner();  // ERROR: expected `Data`, found `Result<Data, Error>`
    Ok(data)
}
```

**Solution:**
```rust
// Use ? operator to propagate errors
fn outer() -> Result<Data, Error> {
    let data = inner()?;  // ? unwraps Ok or returns Err
    Ok(data)
}

// Or match explicitly
fn outer() -> Result<Data, Error> {
    match inner() {
        Ok(data) => Ok(data),
        Err(e) => Err(e),
    }
}
```

**Why this matters:** Rust errors must be explicitly handled or propagated with `?`.

---

## Tooling

### Code Translation Tools

| Tool | Purpose | Notes |
|------|---------|-------|
| `py2rs` | Python → Rust transpiler | Experimental, limited support |
| `PyO3` | Python ↔ Rust FFI | Call Rust from Python or vice versa |
| `maturin` | Build Python extensions in Rust | For keeping Python interface, Rust backend |
| Manual translation | Full control | Recommended for production code |

### Type Checking and Linting

| Python | Rust | Purpose |
|--------|------|---------|
| `mypy` | `rustc` | Static type checking |
| `pylint` | `clippy` | Linting and best practices |
| `black` | `rustfmt` | Code formatting |
| `isort` | - | Import sorting (built into `rustfmt`) |

### Testing Frameworks

| Python | Rust | Purpose |
|--------|------|---------|
| `pytest` | Built-in `#[test]` + `cargo test` | Unit testing |
| `hypothesis` | `proptest` | Property-based testing |
| `unittest.mock` | `mockall` | Mocking |
| `pytest-benchmark` | `criterion` | Benchmarking |

### Async Runtime

| Python | Rust | Purpose |
|--------|------|---------|
| `asyncio` | `tokio` | Async runtime (most popular) |
| `trio` | `async-std` | Alternative async runtime |
| `uvloop` | - | Faster event loop (not needed in Rust) |

### Common Crate Equivalents

| Python Package | Rust Crate | Purpose |
|----------------|------------|---------|
| `requests` | `reqwest` | HTTP client |
| `aiohttp` | `reqwest` (async) | Async HTTP client |
| `flask` / `fastapi` | `axum`, `actix-web` | Web framework |
| `pydantic` | `serde` | Serialization/validation |
| `click` / `argparse` | `clap` | CLI argument parsing |
| `logging` | `tracing`, `log` | Logging/tracing |
| `datetime` | `chrono` | Date/time handling |
| `pathlib` | `std::path` | Path manipulation |
| `json` | `serde_json` | JSON parsing |
| `re` | `regex` | Regular expressions |
| `sqlite3` | `rusqlite` | SQLite database |
| `sqlalchemy` | `diesel`, `sqlx` | ORM / SQL toolkit |
| `pytest` | `cargo test` | Testing framework |

---

## Examples

### Example 1: Simple - HTTP GET Request

**Before (Python):**
```python
import requests

def fetch_user(user_id: int) -> dict:
    """Fetch user data from API."""
    response = requests.get(f"https://api.example.com/users/{user_id}")
    response.raise_for_status()
    return response.json()

# Usage
try:
    user = fetch_user(123)
    print(f"User: {user['name']}")
except requests.HTTPError as e:
    print(f"HTTP error: {e}")
except Exception as e:
    print(f"Error: {e}")
```

**After (Rust):**
```rust
use reqwest;
use serde::Deserialize;

#[derive(Debug, Deserialize)]
struct User {
    name: String,
    // other fields...
}

async fn fetch_user(user_id: u32) -> Result<User, reqwest::Error> {
    let url = format!("https://api.example.com/users/{}", user_id);
    let user = reqwest::get(&url)
        .await?
        .error_for_status()?
        .json::<User>()
        .await?;
    Ok(user)
}

// Usage
#[tokio::main]
async fn main() {
    match fetch_user(123).await {
        Ok(user) => println!("User: {}", user.name),
        Err(e) => eprintln!("Error: {}", e),
    }
}
```

**Key changes:**
- Python dict → Rust struct with `serde::Deserialize`
- `requests` → `reqwest` (async by default)
- Exception handling → `Result<T, E>` + `?` operator
- `async`/`await` syntax is similar in both languages

### Example 2: Medium - Configuration Parser with Validation

**Before (Python):**
```python
from pathlib import Path
from typing import Optional
import json
from dataclasses import dataclass

@dataclass
class Config:
    host: str
    port: int
    timeout: int = 30

    def validate(self):
        if not (1 <= self.port <= 65535):
            raise ValueError(f"Invalid port: {self.port}")
        if self.timeout < 0:
            raise ValueError(f"Invalid timeout: {self.timeout}")

def load_config(path: Path) -> Config:
    """Load and validate configuration from JSON file."""
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")

    with path.open() as f:
        data = json.load(f)

    config = Config(**data)
    config.validate()
    return config

# Usage
try:
    config = load_config(Path("config.json"))
    print(f"Server: {config.host}:{config.port}")
except (FileNotFoundError, ValueError, json.JSONDecodeError) as e:
    print(f"Configuration error: {e}")
    exit(1)
```

**After (Rust):**
```rust
use serde::{Deserialize, Serialize};
use std::fs;
use std::path::Path;
use thiserror::Error;

#[derive(Debug, Error)]
enum ConfigError {
    #[error("Config file not found: {0}")]
    NotFound(String),

    #[error("Failed to read config: {0}")]
    Io(#[from] std::io::Error),

    #[error("Failed to parse config: {0}")]
    Parse(#[from] serde_json::Error),

    #[error("Invalid port: {0} (must be 1-65535)")]
    InvalidPort(u16),

    #[error("Invalid timeout: {0} (must be non-negative)")]
    InvalidTimeout(i32),
}

#[derive(Debug, Deserialize, Serialize)]
struct Config {
    host: String,
    port: u16,
    #[serde(default = "default_timeout")]
    timeout: u32,
}

fn default_timeout() -> u32 {
    30
}

impl Config {
    fn validate(&self) -> Result<(), ConfigError> {
        if self.port == 0 {
            return Err(ConfigError::InvalidPort(self.port));
        }
        // port is u16, so max is already 65535
        Ok(())
    }
}

fn load_config(path: &Path) -> Result<Config, ConfigError> {
    if !path.exists() {
        return Err(ConfigError::NotFound(path.display().to_string()));
    }

    let content = fs::read_to_string(path)?;
    let config: Config = serde_json::from_str(&content)?;
    config.validate()?;
    Ok(config)
}

// Usage
fn main() {
    match load_config(Path::new("config.json")) {
        Ok(config) => {
            println!("Server: {}:{}", config.host, config.port);
        }
        Err(e) => {
            eprintln!("Configuration error: {}", e);
            std::process::exit(1);
        }
    }
}
```

**Key changes:**
- `@dataclass` → `struct` with `#[derive(Deserialize)]`
- Default values via `#[serde(default = "fn")]`
- Custom error enum with `thiserror` for better error messages
- Port validation simplified via `u16` type (0-65535 range enforced by type)
- File I/O errors automatically converted via `#[from]`

### Example 3: Complex - Concurrent Web Scraper with Rate Limiting

**Before (Python):**
```python
import asyncio
import aiohttp
from typing import List, Dict, Optional
from dataclasses import dataclass
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class Article:
    title: str
    url: str
    excerpt: str

class RateLimiter:
    """Token bucket rate limiter."""
    def __init__(self, rate: int, per: float):
        self.rate = rate
        self.per = per
        self.allowance = rate
        self.last_check = asyncio.get_event_loop().time()

    async def acquire(self):
        """Acquire a token, waiting if necessary."""
        current = asyncio.get_event_loop().time()
        elapsed = current - self.last_check
        self.last_check = current

        self.allowance += elapsed * (self.rate / self.per)
        if self.allowance > self.rate:
            self.allowance = self.rate

        if self.allowance < 1.0:
            sleep_time = (1.0 - self.allowance) * (self.per / self.rate)
            await asyncio.sleep(sleep_time)
            self.allowance = 0.0
        else:
            self.allowance -= 1.0

class Scraper:
    def __init__(self, base_url: str, max_concurrent: int = 5, rate_limit: int = 10):
        self.base_url = base_url
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.rate_limiter = RateLimiter(rate=rate_limit, per=1.0)

    async def fetch_page(self, session: aiohttp.ClientSession, url: str) -> Optional[str]:
        """Fetch a single page with rate limiting."""
        await self.rate_limiter.acquire()

        async with self.semaphore:
            try:
                logger.info(f"Fetching {url}")
                async with session.get(url, timeout=10) as response:
                    response.raise_for_status()
                    return await response.text()
            except aiohttp.ClientError as e:
                logger.error(f"Failed to fetch {url}: {e}")
                return None
            except asyncio.TimeoutError:
                logger.error(f"Timeout fetching {url}")
                return None

    async def parse_article(self, html: str, url: str) -> Optional[Article]:
        """Parse article from HTML."""
        try:
            soup = BeautifulSoup(html, 'html.parser')
            title = soup.find('h1').get_text(strip=True)
            excerpt = soup.find('p').get_text(strip=True)[:200]
            return Article(title=title, url=url, excerpt=excerpt)
        except Exception as e:
            logger.error(f"Failed to parse {url}: {e}")
            return None

    async def scrape_articles(self, paths: List[str]) -> List[Article]:
        """Scrape multiple articles concurrently."""
        async with aiohttp.ClientSession() as session:
            tasks = []
            for path in paths:
                url = f"{self.base_url}{path}"
                tasks.append(self.fetch_and_parse(session, url))

            results = await asyncio.gather(*tasks)
            return [article for article in results if article is not None]

    async def fetch_and_parse(self, session: aiohttp.ClientSession, url: str) -> Optional[Article]:
        """Fetch and parse a single article."""
        html = await self.fetch_page(session, url)
        if html:
            return await self.parse_article(html, url)
        return None

# Usage
async def main():
    scraper = Scraper("https://example.com", max_concurrent=5, rate_limit=10)
    paths = [f"/article/{i}" for i in range(20)]

    articles = await scraper.scrape_articles(paths)

    logger.info(f"Scraped {len(articles)} articles")
    for article in articles[:5]:
        print(f"{article.title}: {article.excerpt}")

if __name__ == "__main__":
    asyncio.run(main())
```

**After (Rust):**
```rust
use reqwest;
use scraper::{Html, Selector};
use tokio;
use tokio::sync::Semaphore;
use tokio::time::{sleep, Duration, Instant};
use std::sync::Arc;
use thiserror::Error;
use tracing::{info, error};

#[derive(Debug, Clone)]
struct Article {
    title: String,
    url: String,
    excerpt: String,
}

#[derive(Debug, Error)]
enum ScraperError {
    #[error("HTTP request failed: {0}")]
    Request(#[from] reqwest::Error),

    #[error("Failed to parse HTML")]
    Parse,

    #[error("Timeout")]
    Timeout,
}

/// Token bucket rate limiter
struct RateLimiter {
    rate: f64,
    per: f64,
    allowance: tokio::sync::Mutex<(f64, Instant)>,
}

impl RateLimiter {
    fn new(rate: usize, per: f64) -> Self {
        Self {
            rate: rate as f64,
            per,
            allowance: tokio::sync::Mutex::new((rate as f64, Instant::now())),
        }
    }

    async fn acquire(&self) {
        let mut guard = self.allowance.lock().await;
        let (mut allowance, mut last_check) = *guard;

        let current = Instant::now();
        let elapsed = current.duration_since(last_check).as_secs_f64();
        last_check = current;

        allowance += elapsed * (self.rate / self.per);
        if allowance > self.rate {
            allowance = self.rate;
        }

        if allowance < 1.0 {
            let sleep_time = (1.0 - allowance) * (self.per / self.rate);
            drop(guard);  // Release lock before sleeping
            sleep(Duration::from_secs_f64(sleep_time)).await;
            allowance = 0.0;
        } else {
            allowance -= 1.0;
        }

        *guard = (allowance, last_check);
    }
}

struct Scraper {
    base_url: String,
    client: reqwest::Client,
    semaphore: Arc<Semaphore>,
    rate_limiter: Arc<RateLimiter>,
}

impl Scraper {
    fn new(base_url: String, max_concurrent: usize, rate_limit: usize) -> Self {
        Self {
            base_url,
            client: reqwest::Client::new(),
            semaphore: Arc::new(Semaphore::new(max_concurrent)),
            rate_limiter: Arc::new(RateLimiter::new(rate_limit, 1.0)),
        }
    }

    async fn fetch_page(&self, url: &str) -> Result<String, ScraperError> {
        self.rate_limiter.acquire().await;

        let _permit = self.semaphore.acquire().await.unwrap();

        info!("Fetching {}", url);

        let response = tokio::time::timeout(
            Duration::from_secs(10),
            self.client.get(url).send()
        )
        .await
        .map_err(|_| ScraperError::Timeout)??;

        let html = response.error_for_status()?.text().await?;
        Ok(html)
    }

    fn parse_article(&self, html: &str, url: String) -> Result<Article, ScraperError> {
        let document = Html::parse_document(html);

        let title_selector = Selector::parse("h1").unwrap();
        let p_selector = Selector::parse("p").unwrap();

        let title = document
            .select(&title_selector)
            .next()
            .ok_or(ScraperError::Parse)?
            .text()
            .collect::<String>()
            .trim()
            .to_string();

        let excerpt = document
            .select(&p_selector)
            .next()
            .ok_or(ScraperError::Parse)?
            .text()
            .collect::<String>()
            .chars()
            .take(200)
            .collect();

        Ok(Article { title, url, excerpt })
    }

    async fn fetch_and_parse(&self, url: String) -> Option<Article> {
        match self.fetch_page(&url).await {
            Ok(html) => {
                match self.parse_article(&html, url.clone()) {
                    Ok(article) => Some(article),
                    Err(e) => {
                        error!("Failed to parse {}: {}", url, e);
                        None
                    }
                }
            }
            Err(e) => {
                error!("Failed to fetch {}: {}", url, e);
                None
            }
        }
    }

    async fn scrape_articles(&self, paths: &[&str]) -> Vec<Article> {
        let tasks: Vec<_> = paths
            .iter()
            .map(|path| {
                let url = format!("{}{}", self.base_url, path);
                self.fetch_and_parse(url)
            })
            .collect();

        let results = futures::future::join_all(tasks).await;
        results.into_iter().flatten().collect()
    }
}

#[tokio::main]
async fn main() {
    tracing_subscriber::fmt::init();

    let scraper = Scraper::new(
        "https://example.com".to_string(),
        5,  // max_concurrent
        10, // rate_limit
    );

    let paths: Vec<_> = (0..20).map(|i| format!("/article/{}", i)).collect();
    let path_refs: Vec<&str> = paths.iter().map(|s| s.as_str()).collect();

    let articles = scraper.scrape_articles(&path_refs).await;

    info!("Scraped {} articles", articles.len());
    for article in articles.iter().take(5) {
        println!("{}: {}", article.title, article.excerpt);
    }
}

// Cargo.toml dependencies:
// [dependencies]
// reqwest = { version = "0.11", features = ["json"] }
// tokio = { version = "1", features = ["full"] }
// scraper = "0.17"
// thiserror = "1"
// tracing = "0.1"
// tracing-subscriber = "0.3"
// futures = "0.3"
```

**Key changes:**
- `asyncio.Semaphore` → `tokio::sync::Semaphore` (same pattern)
- Rate limiter uses `tokio::sync::Mutex` for shared state
- `aiohttp` → `reqwest` (async HTTP client)
- `BeautifulSoup` → `scraper` crate (HTML parsing)
- `logging` → `tracing` (structured logging)
- `asyncio.gather` → `futures::future::join_all`
- Error handling via `Result` + `thiserror` instead of exceptions
- `Arc<T>` for shared ownership across async tasks
- Explicit lifetime management (no GC)

---

## See Also

For more examples and patterns, see:
- `meta-convert-dev` - Foundational patterns with cross-language examples
- `lang-python-dev` - Python development patterns
- `lang-rust-dev` - Rust development patterns
