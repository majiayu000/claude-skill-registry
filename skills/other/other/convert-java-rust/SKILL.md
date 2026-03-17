---
name: convert-java-rust
description: Convert Java code to idiomatic Rust. Use when migrating Java projects to Rust, translating Java patterns to idiomatic Rust, or refactoring Java codebases. Extends meta-convert-dev with Java-to-Rust specific patterns.
---

# Convert Java to Rust

Convert Java code to idiomatic Rust. This skill extends `meta-convert-dev` with Java-to-Rust specific type mappings, idiom translations, and tooling.

## This Skill Extends

- `meta-convert-dev` - Foundational conversion patterns (APTV workflow, testing strategies)

For general concepts like the Analyze → Plan → Transform → Validate workflow, testing strategies, and common pitfalls, see the meta-skill first.

## This Skill Adds

- **Type mappings**: Java types → Rust types
- **Idiom translations**: Java patterns → idiomatic Rust
- **Error handling**: Java exceptions → Rust Result<T, E>
- **Concurrency**: Java threads/ExecutorService → Rust async/await
- **Memory/Ownership**: Garbage collection → ownership/borrowing
- **OOP patterns**: Java classes/inheritance → Rust structs/traits
- **Null safety**: null references → Option<T>
- **Metaprogramming**: Java annotations/reflection → Rust macros/traits

## This Skill Does NOT Cover

- General conversion methodology - see `meta-convert-dev`
- Java language fundamentals - see `lang-java-dev`
- Rust language fundamentals - see `lang-rust-dev`
- Reverse conversion (Rust → Java) - see `convert-rust-java`

---

## Quick Reference

| Java | Rust | Notes |
|----------|----------|-------|
| `String` | `String` / `&str` | Owned vs borrowed |
| `int` | `i32` | 32-bit signed integer |
| `long` | `i64` | 64-bit signed integer |
| `float` | `f32` | 32-bit float |
| `double` | `f64` | 64-bit float |
| `boolean` | `bool` | Direct mapping |
| `List<T>` | `Vec<T>` | Growable array |
| `Map<K, V>` | `HashMap<K, V>` | Hash table |
| `Set<T>` | `HashSet<T>` | Unique collection |
| `Optional<T>` | `Option<T>` | Nullable values |
| `null` | `None` in `Option<T>` | Explicit nullability |
| `throws Exception` | `Result<T, E>` | Type-safe errors |
| `interface` | `trait` | Behavioral contracts |
| `class` | `struct` + `impl` | Data + behavior |
| `@Override` | No annotation needed | Traits enforce signature |
| `synchronized` | `Mutex<T>` / `RwLock<T>` | Explicit locking |
| `Thread` | `std::thread` / `tokio::task` | OS threads / async tasks |

## When Converting Code

1. **Analyze source thoroughly** before writing target
2. **Map types first** - create type equivalence table
3. **Preserve semantics** over syntax similarity
4. **Adopt target idioms** - don't write "Java code in Rust syntax"
5. **Handle edge cases** - null checks, error paths, resource cleanup
6. **Test equivalence** - same inputs → same outputs

---

## Type System Mapping

### Primitive Types

| Java | Rust | Notes |
|----------|----------|-------|
| `boolean` | `bool` | Direct mapping |
| `byte` | `i8` | 8-bit signed integer |
| `short` | `i16` | 16-bit signed integer |
| `int` | `i32` | 32-bit signed integer (most common) |
| `long` | `i64` | 64-bit signed integer |
| `float` | `f32` | 32-bit floating point |
| `double` | `f64` | 64-bit floating point (most common) |
| `char` | `char` | Unicode scalar value (4 bytes in Rust) |
| `void` | `()` | Unit type |

**Note:** Java `char` is 16-bit UTF-16, Rust `char` is 32-bit Unicode scalar.

### Boxed Primitives

| Java | Rust | Notes |
|----------|----------|-------|
| `Integer` | `i32` | Primitives don't need boxing in Rust |
| `Long` | `i64` | No autoboxing/unboxing |
| `Double` | `f64` | Direct primitive usage |
| `Boolean` | `bool` | No wrapper types needed |
| `Character` | `char` | Direct usage |

### String Types

| Java | Rust | Notes |
|----------|----------|-------|
| `String` | `String` | Owned, heap-allocated UTF-8 |
| `String` (param) | `&str` | Borrowed string slice for parameters |
| `StringBuilder` | `String` | Use `String` with `push_str`, `push` |
| `char[]` | `Vec<char>` | Character array |
| `byte[]` | `Vec<u8>` | Byte array |

### Collection Types

| Java | Rust | Notes |
|----------|----------|-------|
| `ArrayList<T>` | `Vec<T>` | Growable array |
| `LinkedList<T>` | `std::collections::LinkedList<T>` | Doubly-linked list (rarely used) |
| `HashMap<K, V>` | `HashMap<K, V>` | Hash table, K must be Hash + Eq |
| `TreeMap<K, V>` | `BTreeMap<K, V>` | Ordered map, K must be Ord |
| `HashSet<T>` | `HashSet<T>` | Unique collection |
| `TreeSet<T>` | `BTreeSet<T>` | Ordered unique collection |
| `ArrayDeque<T>` | `VecDeque<T>` | Double-ended queue |
| `PriorityQueue<T>` | `BinaryHeap<T>` | Max-heap by default |
| `T[]` | `Vec<T>` | Dynamic array |
| `T[]` (fixed) | `[T; N]` | Fixed-size array |

### Nullable Types

| Java | Rust | Notes |
|----------|----------|-------|
| `@Nullable T` | `Option<T>` | Explicit nullability |
| `@NonNull T` | `T` | Non-null by default in Rust |
| `Optional<T>` | `Option<T>` | Direct mapping |
| `null` | `None` | Null variant |

### Error Types

| Java | Rust | Notes |
|----------|----------|-------|
| `throws Exception` | `Result<T, Error>` | Type-safe error handling |
| `try/catch` | `match result` or `?` | Pattern matching or propagation |
| `Throwable` | `Error` trait | Error interface |
| `RuntimeException` | `panic!` / `Result` | Unrecoverable vs recoverable |

### Composite Types

| Java | Rust | Notes |
|----------|----------|-------|
| `class Foo { }` | `struct Foo { }` + `impl Foo { }` | Data + behavior separation |
| `interface Bar { }` | `trait Bar { }` | Behavioral contract |
| `enum Status { }` | `enum Status { }` | Algebraic data types in Rust |
| `record Point(int x, int y)` | `struct Point { x: i32, y: i32 }` | Immutable by default in Rust |
| `Pair<K, V>` | `(K, V)` | Tuple |

### Generic Types

| Java | Rust | Notes |
|----------|----------|-------|
| `<T>` | `<T>` | Type parameter |
| `<T extends Foo>` | `<T: Foo>` | Bounded type parameter |
| `<T super Foo>` | No direct equivalent | Use trait objects |
| `<?>` | `_` (type inference) | Wildcard |
| `List<? extends T>` | `Vec<impl Trait>` | Bounded wildcard |
| `Class<T>` | `PhantomData<T>` | Type token |

---

## Idiom Translation

### Pattern 1: Null Checking

**Java:**
```java
public String getUserName(User user) {
    if (user == null) {
        return "Anonymous";
    }
    if (user.getName() == null || user.getName().isEmpty()) {
        return "Anonymous";
    }
    return user.getName();
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
- No null pointer exceptions possible at runtime
- Combinators like `and_then` and `unwrap_or` are idiomatic
- Pattern matching with guards is more expressive
- Borrowed references avoid unnecessary cloning

### Pattern 2: Exception Handling

**Java:**
```java
public Config readConfig(String path) throws IOException {
    String content = Files.readString(Path.of(path));
    return parseConfig(content);
}

public void processConfig(String path) {
    try {
        Config config = readConfig(path);
        apply(config);
    } catch (IOException e) {
        System.err.println("Failed to read config: " + e.getMessage());
    }
}
```

**Rust:**
```rust
use std::fs;
use std::path::Path;

fn read_config(path: &Path) -> Result<Config, std::io::Error> {
    let content = fs::read_to_string(path)?;
    parse_config(&content)
}

fn process_config(path: &Path) {
    match read_config(path) {
        Ok(config) => apply(config),
        Err(e) => eprintln!("Failed to read config: {}", e),
    }
}

// Or with the ? operator in a Result-returning function:
fn process_config(path: &Path) -> Result<(), std::io::Error> {
    let config = read_config(path)?;
    apply(config);
    Ok(())
}
```

**Why this translation:**
- `Result<T, E>` encodes success/failure in the type system
- The `?` operator propagates errors ergonomically (like Java `throws`)
- Pattern matching makes error handling explicit
- No hidden control flow (exceptions jumping up the stack)
- Errors are values, not exceptional control flow

### Pattern 3: Optional Chaining

**Java:**
```java
public String getCityName(User user) {
    return Optional.ofNullable(user)
        .map(User::getAddress)
        .map(Address::getCity)
        .map(City::getName)
        .orElse("Unknown");
}
```

**Rust:**
```rust
fn get_city_name(user: Option<&User>) -> &str {
    user.and_then(|u| u.address.as_ref())
        .and_then(|a| a.city.as_ref())
        .map(|c| c.name.as_str())
        .unwrap_or("Unknown")
}

// Or with pattern matching:
fn get_city_name(user: Option<&User>) -> &str {
    match user {
        Some(User {
            address: Some(Address {
                city: Some(City { name, .. }),
                ..
            }),
            ..
        }) => name,
        _ => "Unknown",
    }
}
```

**Why this translation:**
- Direct mapping from Java `Optional` to Rust `Option`
- Rust's `Option` methods are similar to Java's
- Pattern matching can destructure nested `Option`s
- Borrowed references avoid cloning

### Pattern 4: Stream/Iterator Operations

**Java:**
```java
List<String> names = users.stream()
    .filter(user -> user.getAge() > 18)
    .map(User::getName)
    .map(String::toUpperCase)
    .collect(Collectors.toList());

int totalAge = users.stream()
    .mapToInt(User::getAge)
    .sum();
```

**Rust:**
```rust
let names: Vec<String> = users
    .iter()
    .filter(|user| user.age > 18)
    .map(|user| user.name.to_uppercase())
    .collect();

let total_age: i32 = users
    .iter()
    .map(|user| user.age)
    .sum();
```

**Why this translation:**
- Rust iterators are zero-cost abstractions (like Java streams)
- Similar combinator API: `filter`, `map`, `collect`, `sum`
- Rust iterators are lazy (like Java streams)
- No need for specialized primitive streams (`mapToInt`, etc.)
- More explicit borrowing with `iter()` vs `into_iter()`

### Pattern 5: Builder Pattern

**Java:**
```java
public class Request {
    private final String url;
    private final String method;
    private final Map<String, String> headers;

    private Request(Builder builder) {
        this.url = builder.url;
        this.method = builder.method;
        this.headers = builder.headers;
    }

    public static class Builder {
        private String url;
        private String method = "GET";
        private Map<String, String> headers = new HashMap<>();

        public Builder url(String url) {
            this.url = url;
            return this;
        }

        public Builder method(String method) {
            this.method = method;
            return this;
        }

        public Builder header(String key, String value) {
            this.headers.put(key, value);
            return this;
        }

        public Request build() {
            return new Request(this);
        }
    }
}

// Usage
Request request = new Request.Builder()
    .url("https://api.example.com")
    .method("POST")
    .header("Content-Type", "application/json")
    .build();
```

**Rust:**
```rust
use std::collections::HashMap;

struct Request {
    url: String,
    method: String,
    headers: HashMap<String, String>,
}

struct RequestBuilder {
    url: String,
    method: String,
    headers: HashMap<String, String>,
}

impl RequestBuilder {
    fn new(url: impl Into<String>) -> Self {
        Self {
            url: url.into(),
            method: String::from("GET"),
            headers: HashMap::new(),
        }
    }

    fn method(mut self, method: impl Into<String>) -> Self {
        self.method = method.into();
        self
    }

    fn header(mut self, key: impl Into<String>, value: impl Into<String>) -> Self {
        self.headers.insert(key.into(), value.into());
        self
    }

    fn build(self) -> Request {
        Request {
            url: self.url,
            method: self.method,
            headers: self.headers,
        }
    }
}

// Usage
let request = RequestBuilder::new("https://api.example.com")
    .method("POST")
    .header("Content-Type", "application/json")
    .build();
```

**Why this translation:**
- Similar builder pattern structure
- Rust uses `self` consumption for method chaining
- No need for nested `Builder` class (separate struct)
- `impl Into<String>` accepts both `String` and `&str`
- More ergonomic with fewer allocations

### Pattern 6: Interface Implementation

**Java:**
```java
interface Reader {
    int read(byte[] buffer) throws IOException;
}

class FileReader implements Reader {
    private String path;

    @Override
    public int read(byte[] buffer) throws IOException {
        // Implementation
        return buffer.length;
    }
}

void processReader(Reader reader) throws IOException {
    byte[] buffer = new byte[1024];
    int bytesRead = reader.read(buffer);
    // Process buffer
}
```

**Rust:**
```rust
use std::io;

trait Reader {
    fn read(&mut self, buffer: &mut [u8]) -> io::Result<usize>;
}

struct FileReader {
    path: String,
}

impl Reader for FileReader {
    fn read(&mut self, buffer: &mut [u8]) -> io::Result<usize> {
        // Implementation
        Ok(buffer.len())
    }
}

fn process_reader<R: Reader>(reader: &mut R) -> io::Result<()> {
    let mut buffer = vec![0u8; 1024];
    let bytes_read = reader.read(&mut buffer)?;
    // Process buffer
    Ok(())
}
```

**Why this translation:**
- Rust traits are explicitly implemented with `impl Trait for Type`
- Generic functions use trait bounds (`<R: Reader>`)
- Mutable borrows (`&mut`) make mutation explicit
- The `?` operator replaces `throws` declarations
- No `@Override` annotation needed (enforced by trait)

### Pattern 7: Inheritance vs Composition

**Java:**
```java
abstract class Animal {
    private String name;

    public Animal(String name) {
        this.name = name;
    }

    public abstract void makeSound();

    public void sleep() {
        System.out.println(name + " is sleeping");
    }
}

class Dog extends Animal {
    public Dog(String name) {
        super(name);
    }

    @Override
    public void makeSound() {
        System.out.println("Woof!");
    }
}
```

**Rust:**
```rust
// Use traits instead of abstract classes
trait Animal {
    fn name(&self) -> &str;
    fn make_sound(&self);

    // Default implementation (like concrete methods in abstract class)
    fn sleep(&self) {
        println!("{} is sleeping", self.name());
    }
}

struct Dog {
    name: String,
}

impl Animal for Dog {
    fn name(&self) -> &str {
        &self.name
    }

    fn make_sound(&self) {
        println!("Woof!");
    }
}

// Alternative: Composition with delegation
struct AnimalData {
    name: String,
}

struct Dog {
    data: AnimalData,
}

impl Dog {
    fn make_sound(&self) {
        println!("Woof!");
    }

    fn sleep(&self) {
        println!("{} is sleeping", self.data.name);
    }
}
```

**Why this translation:**
- Rust favors composition over inheritance
- Traits define shared behavior without state
- No virtual method dispatch overhead by default
- More flexible than rigid class hierarchies
- Prefer trait bounds over inheritance for polymorphism

### Pattern 8: Static Methods and Factory Patterns

**Java:**
```java
class User {
    private String name;
    private int age;

    private User(String name, int age) {
        this.name = name;
        this.age = age;
    }

    public static User create(String name, int age) {
        if (age < 0) {
            throw new IllegalArgumentException("Age cannot be negative");
        }
        return new User(name, age);
    }

    public static User createAnonymous() {
        return new User("Anonymous", 0);
    }
}
```

**Rust:**
```rust
struct User {
    name: String,
    age: u32,
}

impl User {
    // Associated function (like static method)
    fn new(name: impl Into<String>, age: u32) -> Self {
        Self {
            name: name.into(),
            age,
        }
    }

    // Factory method with validation
    fn create(name: impl Into<String>, age: i32) -> Result<Self, &'static str> {
        if age < 0 {
            return Err("Age cannot be negative");
        }
        Ok(Self {
            name: name.into(),
            age: age as u32,
        })
    }

    // Named constructor
    fn anonymous() -> Self {
        Self {
            name: String::from("Anonymous"),
            age: 0,
        }
    }
}

// Usage
let user = User::new("Alice", 30);
let user2 = User::create("Bob", 25)?;
let anon = User::anonymous();
```

**Why this translation:**
- Rust uses associated functions instead of static methods
- No `static` keyword needed (no `self` parameter)
- Factory methods return `Result` for validation
- Named constructors are idiomatic (`new`, `with_capacity`, etc.)
- Private constructors not needed (use `pub` selectively)

---

## Paradigm Translation: OOP → Systems Programming

### Mental Model Shift: Object-Oriented → Ownership-Based

| Java Concept | Rust Approach | Key Insight |
|------------------|-------------------|-------------|
| Class with state | `struct` + `impl` blocks | Data and behavior separated but associated |
| Inheritance | Composition + traits | Favor composition over deep hierarchies |
| Polymorphism (subtyping) | Trait objects (`dyn Trait`) or generics | Static dispatch (generics) vs dynamic (trait objects) |
| Encapsulation | Module visibility + `pub` | Privacy at module level, not class level |
| Constructor | Associated function `new()` | No special constructor syntax |
| Garbage collection | Ownership + borrowing | Compiler-enforced memory safety |
| Null references | `Option<T>` | Null safety in type system |
| Exceptions | `Result<T, E>` | Errors as values |

### Memory Management Mental Model

| Java Model | Rust Model | Conceptual Translation |
|----------------|----------------|------------------------|
| Heap allocation automatic | Explicit (`Box`, `Vec`, `String`) | Ownership makes allocation visible |
| GC reclaims memory | Automatic via RAII (`Drop`) | Deterministic cleanup at scope end |
| References everywhere | Borrows (`&`, `&mut`) | Explicit lifetime tracking |
| No manual cleanup | No manual cleanup | Same safety, different mechanism |
| Shared mutable state | `Mutex`, `RefCell`, interior mutability | Mutation rules enforced by compiler |

### Concurrency Mental Model

| Java Model | Rust Model | Conceptual Translation |
|----------------|----------------|------------------------|
| `synchronized` blocks | `Mutex<T>` / `RwLock<T>` | Lock protects data, not code |
| Thread-safe by convention | Thread-safe by type system (`Send`, `Sync`) | Compiler prevents data races |
| `ExecutorService` | `tokio::Runtime` / `async-std` | Async runtime for task scheduling |
| `Future<T>` (Java 8+) | `Future` trait + `async`/`await` | First-class async support |
| Heavyweight threads | OS threads or lightweight async tasks | Choose cost based on use case |

---

## Error Handling

### Java Exception Model → Rust Result Model

Java uses exceptions for both expected and unexpected errors. Rust distinguishes between recoverable errors (`Result`) and unrecoverable errors (`panic!`).

**Mapping:**

| Java | Rust | Use Case |
|------|------|----------|
| Checked exceptions | `Result<T, E>` | Recoverable errors (expected) |
| Unchecked exceptions | `Result<T, E>` or `panic!` | Recoverable or programmer errors |
| `throws` clause | Return type `Result<T, E>` | Signature shows fallibility |
| `try/catch` | `match result` or `if let Err` | Explicit error handling |
| `try/catch` (propagate) | `?` operator | Early return on error |
| `finally` | RAII / `Drop` trait | Automatic cleanup |
| `throw new Exception()` | `Err(...)` or `panic!()` | Return error or abort |

### Pattern: Multiple Exception Types

**Java:**
```java
public Data processFile(String path) throws IOException, ParseException {
    String content = Files.readString(Path.of(path));
    return parseData(content);
}

try {
    Data data = processFile("config.json");
} catch (IOException e) {
    System.err.println("IO error: " + e.getMessage());
} catch (ParseException e) {
    System.err.println("Parse error: " + e.getMessage());
}
```

**Rust:**
```rust
use std::fs;
use std::path::Path;

// Define error enum to combine multiple error types
#[derive(Debug)]
enum ProcessError {
    Io(std::io::Error),
    Parse(String),
}

impl From<std::io::Error> for ProcessError {
    fn from(e: std::io::Error) -> Self {
        ProcessError::Io(e)
    }
}

fn process_file(path: &Path) -> Result<Data, ProcessError> {
    let content = fs::read_to_string(path)?;  // Auto-converts via From
    parse_data(&content).map_err(ProcessError::Parse)
}

match process_file(Path::new("config.json")) {
    Ok(data) => { /* use data */ },
    Err(ProcessError::Io(e)) => eprintln!("IO error: {}", e),
    Err(ProcessError::Parse(e)) => eprintln!("Parse error: {}", e),
}

// Or use anyhow/error-stack for simplified error handling:
use anyhow::Result;

fn process_file(path: &Path) -> Result<Data> {
    let content = fs::read_to_string(path)?;
    let data = parse_data(&content)?;
    Ok(data)
}
```

**Why this translation:**
- Custom error enums replace multiple exception types
- `From` trait enables automatic conversion with `?`
- Pattern matching handles different error cases
- `anyhow` crate provides ergonomic error handling for applications
- `thiserror` crate simplifies custom error types

### Pattern: Try-with-Resources

**Java:**
```java
try (BufferedReader reader = new BufferedReader(new FileReader("file.txt"))) {
    String line = reader.readLine();
    // Process line
} catch (IOException e) {
    System.err.println("Error: " + e.getMessage());
}
```

**Rust:**
```rust
use std::fs::File;
use std::io::{self, BufRead, BufReader};
use std::path::Path;

fn read_first_line(path: &Path) -> io::Result<String> {
    let file = File::open(path)?;
    let reader = BufReader::new(file);
    let mut line = String::new();
    reader.lines().next()
        .ok_or_else(|| io::Error::new(io::ErrorKind::UnexpectedEof, "Empty file"))?
}

// File is automatically closed when it goes out of scope (Drop trait)
match read_first_line(Path::new("file.txt")) {
    Ok(line) => println!("{}", line),
    Err(e) => eprintln!("Error: {}", e),
}
```

**Why this translation:**
- Rust's RAII (Drop trait) automatically cleans up resources
- No need for explicit try-with-resources syntax
- Scope-based cleanup is deterministic
- More type-safe than runtime resource management

---

## Concurrency Patterns

### Java Concurrency → Rust Concurrency

Rust provides both traditional OS threads and lightweight async/await concurrency.

### Pattern 1: Basic Threading

**Java:**
```java
public class Counter {
    private int count = 0;

    public synchronized void increment() {
        count++;
    }

    public synchronized int getCount() {
        return count;
    }
}

Counter counter = new Counter();

List<Thread> threads = new ArrayList<>();
for (int i = 0; i < 10; i++) {
    Thread t = new Thread(() -> {
        for (int j = 0; j < 1000; j++) {
            counter.increment();
        }
    });
    threads.add(t);
    t.start();
}

for (Thread t : threads) {
    t.join();
}

System.out.println("Count: " + counter.getCount());
```

**Rust:**
```rust
use std::sync::{Arc, Mutex};
use std::thread;

let counter = Arc::new(Mutex::new(0));
let mut handles = vec![];

for _ in 0..10 {
    let counter = Arc::clone(&counter);
    let handle = thread::spawn(move || {
        for _ in 0..1000 {
            let mut num = counter.lock().unwrap();
            *num += 1;
        }
    });
    handles.push(handle);
}

for handle in handles {
    handle.join().unwrap();
}

println!("Count: {}", *counter.lock().unwrap());
```

**Why this translation:**
- `Arc<Mutex<T>>` combines reference counting (Arc) with mutual exclusion (Mutex)
- Mutex protects the data, not the code block
- Type system prevents data races at compile time
- Explicit cloning makes shared ownership visible
- `move` closure captures ownership

### Pattern 2: ExecutorService → Tokio Async

**Java:**
```java
ExecutorService executor = Executors.newFixedThreadPool(4);

List<Future<String>> futures = new ArrayList<>();
for (String url : urls) {
    Future<String> future = executor.submit(() -> fetchUrl(url));
    futures.add(future);
}

List<String> results = new ArrayList<>();
for (Future<String> future : futures) {
    try {
        results.add(future.get());
    } catch (InterruptedException | ExecutionException e) {
        System.err.println("Error: " + e.getMessage());
    }
}

executor.shutdown();
```

**Rust:**
```rust
use tokio;

#[tokio::main]
async fn main() {
    let urls = vec!["url1", "url2", "url3"];

    let tasks: Vec<_> = urls
        .into_iter()
        .map(|url| tokio::spawn(async move { fetch_url(url).await }))
        .collect();

    let mut results = Vec::new();
    for task in tasks {
        match task.await {
            Ok(result) => results.push(result),
            Err(e) => eprintln!("Error: {}", e),
        }
    }
}

async fn fetch_url(url: &str) -> String {
    // Async HTTP request
    String::from(url)
}
```

**Why this translation:**
- Tokio provides async runtime (like ExecutorService)
- `async`/`await` syntax is more ergonomic than futures
- Tasks are lightweight (like virtual threads in Java 21)
- No need for explicit thread pool management
- Type-safe async with `Future` trait

### Pattern 3: CompletableFuture → Async/Await

**Java:**
```java
CompletableFuture<String> future1 = CompletableFuture.supplyAsync(() -> fetchData());
CompletableFuture<Integer> future2 = future1.thenApply(data -> parseData(data));
CompletableFuture<Void> future3 = future2.thenAccept(value -> processValue(value));

future3.exceptionally(ex -> {
    System.err.println("Error: " + ex.getMessage());
    return null;
});

future3.join();
```

**Rust:**
```rust
use tokio;

#[tokio::main]
async fn main() {
    match fetch_and_process().await {
        Ok(()) => println!("Success"),
        Err(e) => eprintln!("Error: {}", e),
    }
}

async fn fetch_and_process() -> Result<(), Box<dyn std::error::Error>> {
    let data = fetch_data().await?;
    let value = parse_data(&data).await?;
    process_value(value).await?;
    Ok(())
}

async fn fetch_data() -> Result<String, std::io::Error> {
    // Async operation
    Ok(String::from("data"))
}

async fn parse_data(data: &str) -> Result<i32, std::num::ParseIntError> {
    data.parse()
}

async fn process_value(value: i32) -> Result<(), std::io::Error> {
    println!("Value: {}", value);
    Ok(())
}
```

**Why this translation:**
- `async`/`await` is more readable than chaining futures
- `?` operator propagates errors through async chain
- No need for explicit `exceptionally` handlers
- Type-safe error handling with `Result`
- Composable async functions

---

## Memory & Ownership

### Java GC → Rust Ownership

The biggest paradigm shift from Java to Rust is memory management. Java uses garbage collection; Rust uses compile-time ownership tracking.

### Core Ownership Rules

1. **Each value has a single owner** (unlike Java where references are shared freely)
2. **When the owner goes out of scope, the value is dropped** (like Java finalization, but deterministic)
3. **Values can be borrowed immutably or mutably** (unlike Java where everything is mutable unless final)

### Pattern 1: Ownership Transfer

**Java:**
```java
// Java freely shares references
List<String> list1 = new ArrayList<>();
list1.add("hello");
List<String> list2 = list1;  // Both point to same list
list2.add("world");
System.out.println(list1.size());  // 2
```

**Rust:**
```rust
// Rust transfers ownership by default
let mut list1 = vec![String::from("hello")];
let list2 = list1;  // Ownership transferred to list2
// println!("{:?}", list1);  // Compile error: list1 moved

list2.push(String::from("world"));
println!("{}", list2.len());  // 2

// To share, use borrowing:
let mut list1 = vec![String::from("hello")];
let list2 = &list1;  // Borrow immutably
println!("{:?}", list1);  // OK: list1 still owns the data
println!("{:?}", list2);  // OK: borrowing
```

**Why this matters:**
- Rust prevents use-after-move bugs at compile time
- No runtime overhead (no reference counting)
- Clear ownership semantics

### Pattern 2: Cloning vs Borrowing

**Java:**
```java
void processData(List<String> data) {
    // Can mutate the list
    data.add("new item");
}

List<String> myData = new ArrayList<>();
processData(myData);  // myData is modified
```

**Rust:**
```rust
// Option 1: Borrow mutably
fn process_data(data: &mut Vec<String>) {
    data.push(String::from("new item"));
}

let mut my_data = vec![];
process_data(&mut my_data);  // my_data is modified

// Option 2: Borrow immutably (cannot modify)
fn read_data(data: &Vec<String>) {
    for item in data {
        println!("{}", item);
    }
    // data.push(...);  // Compile error: cannot mutate
}

read_data(&my_data);

// Option 3: Take ownership (consumes the value)
fn consume_data(data: Vec<String>) {
    // data is moved here, caller loses access
}

// my_data is gone after this
consume_data(my_data);
// println!("{:?}", my_data);  // Compile error
```

**Why this translation:**
- Explicit borrowing prevents accidental mutation
- Ownership transfer is visible in function signatures
- Compiler enforces no data races or aliasing bugs

### Pattern 3: Reference Counting (Rc/Arc)

**Java:**
```java
// Java automatically manages shared references
class Node {
    int value;
    List<Node> children;
}

Node parent = new Node();
Node child1 = new Node();
Node child2 = new Node();
parent.children.add(child1);
parent.children.add(child2);
// All nodes share references, GC cleans up when unreachable
```

**Rust:**
```rust
use std::rc::Rc;

struct Node {
    value: i32,
    children: Vec<Rc<Node>>,
}

let child1 = Rc::new(Node {
    value: 1,
    children: vec![],
});

let child2 = Rc::new(Node {
    value: 2,
    children: vec![],
});

let parent = Node {
    value: 0,
    children: vec![Rc::clone(&child1), Rc::clone(&child2)],
};

// Rc provides shared ownership with reference counting
// Arc for thread-safe reference counting
```

**Why this translation:**
- `Rc<T>` (single-threaded) or `Arc<T>` (thread-safe) for shared ownership
- Explicit cloning makes reference counting visible
- No cycles by default (use `Weak<T>` for weak references)
- More predictable than GC

---

## Metaprogramming

### Java Annotations/Reflection → Rust Macros/Traits

Java uses runtime reflection and annotations. Rust uses compile-time macros and traits.

### Pattern 1: Annotations → Derive Macros

**Java:**
```java
@Data  // Lombok annotation
@Entity
@Table(name = "users")
public class User {
    @Id
    @GeneratedValue
    private Long id;

    @Column(nullable = false)
    private String name;

    @Column(unique = true)
    private String email;
}
```

**Rust:**
```rust
use serde::{Serialize, Deserialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct User {
    pub id: Option<u64>,
    pub name: String,
    pub email: String,
}

// Or with a custom derive macro for ORM:
#[derive(Debug, Entity)]
#[table(name = "users")]
pub struct User {
    #[id]
    #[generated]
    pub id: Option<u64>,

    #[column(nullable = false)]
    pub name: String,

    #[column(unique = true)]
    pub email: String,
}
```

**Why this translation:**
- Derive macros generate code at compile time (no runtime reflection)
- Type-safe (errors caught during compilation)
- Zero runtime overhead
- `serde` is the standard serialization framework

### Pattern 2: Reflection → Trait Objects

**Java:**
```java
void processObject(Object obj) {
    if (obj instanceof String) {
        String s = (String) obj;
        System.out.println("String: " + s);
    } else if (obj instanceof Integer) {
        Integer i = (Integer) obj;
        System.out.println("Integer: " + i);
    }
}

// Or with reflection:
Class<?> clazz = obj.getClass();
Method method = clazz.getMethod("toString");
Object result = method.invoke(obj);
```

**Rust:**
```rust
// Prefer enums over runtime type checking
enum Value {
    String(String),
    Integer(i32),
}

fn process_value(value: Value) {
    match value {
        Value::String(s) => println!("String: {}", s),
        Value::Integer(i) => println!("Integer: {}", i),
    }
}

// Or use trait objects for polymorphism:
trait Printable {
    fn print(&self);
}

impl Printable for String {
    fn print(&self) {
        println!("String: {}", self);
    }
}

impl Printable for i32 {
    fn print(&self) {
        println!("Integer: {}", self);
    }
}

fn process_printable(obj: &dyn Printable) {
    obj.print();
}
```

**Why this translation:**
- Rust avoids runtime reflection (unsafe and slow)
- Enums are type-safe alternatives to instanceof
- Trait objects (`dyn Trait`) for runtime polymorphism
- Most metaprogramming done at compile time with macros

### Pattern 3: Custom Annotations → Attribute Macros

**Java:**
```java
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.METHOD)
public @interface Cached {
    int ttl() default 60;
}

public class Service {
    @Cached(ttl = 300)
    public Data fetchData(String key) {
        // Method implementation
    }
}

// Runtime processing with reflection
for (Method method : Service.class.getDeclaredMethods()) {
    if (method.isAnnotationPresent(Cached.class)) {
        Cached cached = method.getAnnotation(Cached.class);
        int ttl = cached.ttl();
        // Setup caching
    }
}
```

**Rust:**
```rust
// Define attribute macro (in a proc-macro crate)
#[proc_macro_attribute]
pub fn cached(attr: TokenStream, item: TokenStream) -> TokenStream {
    // Parse ttl from attr
    // Generate wrapper code that caches results
    // Return modified function
}

// Usage
#[cached(ttl = 300)]
pub fn fetch_data(key: &str) -> Data {
    // Method implementation
}

// Macro expands at compile time to:
pub fn fetch_data(key: &str) -> Data {
    // Check cache
    // If miss, call original function and cache result
}
```

**Why this translation:**
- Rust macros run at compile time
- No runtime reflection overhead
- Type-safe macro expansion
- More powerful than annotations (can generate arbitrary code)

---

## Serialization

### Jackson → Serde

Java uses Jackson for JSON serialization. Rust uses Serde, which is more flexible and type-safe.

### Pattern: JSON Serialization

**Java:**
```java
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.annotation.*;

@JsonIgnoreProperties(ignoreUnknown = true)
public class Config {
    @JsonProperty("api_key")
    private String apiKey;

    private String endpoint;

    @JsonIgnore
    private String internalState;

    @JsonProperty(access = JsonProperty.Access.READ_ONLY)
    private LocalDateTime createdAt;

    // Getters and setters
}

ObjectMapper mapper = new ObjectMapper();
String json = mapper.writeValueAsString(config);
Config parsed = mapper.readValue(json, Config.class);
```

**Rust:**
```rust
use serde::{Serialize, Deserialize};
use chrono::{DateTime, Utc};

#[derive(Debug, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
struct Config {
    #[serde(rename = "api_key")]
    api_key: String,

    endpoint: String,

    #[serde(skip)]
    internal_state: String,

    #[serde(skip_serializing)]
    created_at: DateTime<Utc>,
}

// Serialization
let json = serde_json::to_string(&config)?;
let pretty_json = serde_json::to_string_pretty(&config)?;

// Deserialization
let parsed: Config = serde_json::from_str(&json)?;
```

**Why this translation:**
- Serde is compile-time type-safe
- Zero runtime overhead
- More flexible than Jackson (works with JSON, YAML, TOML, MessagePack, etc.)
- Errors caught at compile time, not runtime

---

## Build and Dependencies

### Maven/Gradle → Cargo

Java uses Maven or Gradle. Rust uses Cargo, which is simpler and faster.

### Pattern: Dependency Management

**Java (Maven):**
```xml
<dependencies>
    <dependency>
        <groupId>com.fasterxml.jackson.core</groupId>
        <artifactId>jackson-databind</artifactId>
        <version>2.15.0</version>
    </dependency>

    <dependency>
        <groupId>org.junit.jupiter</groupId>
        <artifactId>junit-jupiter</artifactId>
        <version>5.10.0</version>
        <scope>test</scope>
    </dependency>
</dependencies>
```

**Java (Gradle):**
```kotlin
dependencies {
    implementation("com.fasterxml.jackson.core:jackson-databind:2.15.0")
    testImplementation("org.junit.jupiter:junit-jupiter:5.10.0")
}
```

**Rust (Cargo.toml):**
```toml
[dependencies]
serde = { version = "1.0", features = ["derive"] }
serde_json = "1.0"
tokio = { version = "1", features = ["full"] }

[dev-dependencies]
criterion = "0.5"
```

**Why this translation:**
- Cargo is simpler (one file vs XML/Groovy)
- Built-in features system
- Faster dependency resolution
- Lock file (Cargo.lock) ensures reproducible builds

### Common Commands

| Maven/Gradle | Cargo | Purpose |
|--------------|-------|---------|
| `mvn compile` / `gradle build` | `cargo build` | Compile |
| `mvn test` / `gradle test` | `cargo test` | Run tests |
| `mvn package` / `gradle jar` | `cargo build --release` | Build release |
| `mvn install` / `gradle publishToMavenLocal` | `cargo install` | Install binary |
| `mvn clean` / `gradle clean` | `cargo clean` | Clean build |
| `mvn dependency:tree` / `gradle dependencies` | `cargo tree` | Show deps |

---

## Testing

### JUnit → Cargo Test

Java uses JUnit for testing. Rust has built-in testing support.

### Pattern: Unit Tests

**Java:**
```java
import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

class CalculatorTest {
    private Calculator calculator;

    @BeforeEach
    void setUp() {
        calculator = new Calculator();
    }

    @Test
    void shouldAddTwoNumbers() {
        int result = calculator.add(2, 3);
        assertEquals(5, result);
    }

    @Test
    void shouldThrowOnDivisionByZero() {
        assertThrows(ArithmeticException.class, () -> {
            calculator.divide(10, 0);
        });
    }
}
```

**Rust:**
```rust
struct Calculator;

impl Calculator {
    fn add(&self, a: i32, b: i32) -> i32 {
        a + b
    }

    fn divide(&self, a: i32, b: i32) -> Result<i32, &'static str> {
        if b == 0 {
            Err("Division by zero")
        } else {
            Ok(a / b)
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn should_add_two_numbers() {
        let calculator = Calculator;
        let result = calculator.add(2, 3);
        assert_eq!(result, 5);
    }

    #[test]
    fn should_return_error_on_division_by_zero() {
        let calculator = Calculator;
        let result = calculator.divide(10, 0);
        assert!(result.is_err());
    }
}
```

**Why this translation:**
- Built-in test framework (no external dependency)
- Tests live next to code in `#[cfg(test)]` modules
- Assertions are macros: `assert!`, `assert_eq!`, `assert_ne!`
- No need for setup/teardown (use RAII pattern)

---

## Common Pitfalls

### Pitfall 1: Assuming Null Everywhere

**Problem:** In Java, any reference can be null. In Rust, values are non-null by default.

**Java:**
```java
String name = getName();  // Might be null
int length = name.length();  // NullPointerException!
```

**Rust:**
```rust
// Wrong: trying to use null
let name = get_name();  // Returns Option<String>
// let length = name.len();  // Compile error: Option has no len()

// Right: handle Option explicitly
let name = get_name();
let length = name.map(|s| s.len()).unwrap_or(0);

// Or with pattern matching:
match get_name() {
    Some(name) => println!("Length: {}", name.len()),
    None => println!("No name"),
}
```

### Pitfall 2: Mutating Shared References

**Problem:** In Java, shared references can be mutated freely. Rust enforces exclusive mutation.

**Java:**
```java
List<String> list = new ArrayList<>();
List<String> ref1 = list;
List<String> ref2 = list;
ref1.add("hello");  // OK
ref2.add("world");  // OK
```

**Rust:**
```rust
// Wrong: multiple mutable references
let mut list = vec![];
let ref1 = &mut list;
let ref2 = &mut list;  // Compile error: cannot borrow as mutable more than once
ref1.push("hello");
ref2.push("world");

// Right: use immutable borrows or take ownership
let mut list = vec![];
list.push("hello");
list.push("world");

// Or use interior mutability (RefCell, Mutex)
use std::cell::RefCell;
let list = RefCell::new(vec![]);
list.borrow_mut().push("hello");
list.borrow_mut().push("world");
```

### Pitfall 3: Expecting Inheritance

**Problem:** Java relies heavily on class inheritance. Rust favors composition and traits.

**Java:**
```java
class Animal { }
class Dog extends Animal { }

Animal animal = new Dog();  // Polymorphism via inheritance
```

**Rust:**
```rust
// Wrong: trying to use inheritance
// Rust has no inheritance!

// Right: use traits
trait Animal {
    fn make_sound(&self);
}

struct Dog;

impl Animal for Dog {
    fn make_sound(&self) {
        println!("Woof!");
    }
}

fn process_animal(animal: &dyn Animal) {
    animal.make_sound();
}

let dog = Dog;
process_animal(&dog);
```

### Pitfall 4: Checked Exceptions vs Result

**Problem:** Java uses checked exceptions that must be declared. Rust uses `Result` as a return type.

**Java:**
```java
// Java: throws in signature
public Data readFile(String path) throws IOException {
    // ...
}
```

**Rust:**
```rust
// Wrong: trying to throw exceptions
// Rust has no exceptions!

// Right: return Result
fn read_file(path: &Path) -> Result<Data, std::io::Error> {
    // ...
}

// Or use the ? operator to propagate
fn process() -> Result<(), std::io::Error> {
    let data = read_file(Path::new("file.txt"))?;
    Ok(())
}
```

### Pitfall 5: String Confusion

**Problem:** Java has one `String` type. Rust has `String` (owned) and `&str` (borrowed).

**Java:**
```java
String s1 = "hello";
String s2 = new String("world");
void process(String s) { }
```

**Rust:**
```rust
// Wrong: using only String
fn process(s: String) { }  // Takes ownership!

let s1 = String::from("hello");
process(s1);
// println!("{}", s1);  // Compile error: s1 was moved

// Right: use &str for parameters
fn process(s: &str) { }

let s1 = String::from("hello");
process(&s1);  // Borrow
println!("{}", s1);  // OK: still own s1

// String literals are &str
let s2 = "world";  // Type: &str
```

### Pitfall 6: Integer Overflow

**Problem:** Java silently wraps on integer overflow. Rust panics in debug mode.

**Java:**
```java
int max = Integer.MAX_VALUE;
int overflow = max + 1;  // Wraps to Integer.MIN_VALUE
```

**Rust:**
```rust
// Debug mode: panics on overflow
let max: i32 = i32::MAX;
// let overflow = max + 1;  // Panic in debug, wraps in release

// Right: use checked/wrapping/saturating arithmetic
let overflow = max.checked_add(1);  // Returns None
let wrapping = max.wrapping_add(1);  // Always wraps
let saturating = max.saturating_add(1);  // Clamps to max
```

### Pitfall 7: Cloning Performance

**Problem:** Java clones collections implicitly. Rust makes cloning explicit and visible.

**Java:**
```java
List<String> list1 = Arrays.asList("a", "b", "c");
List<String> list2 = new ArrayList<>(list1);  // Clone
```

**Rust:**
```rust
// Explicit cloning
let list1 = vec!["a", "b", "c"];
let list2 = list1.clone();  // Explicit, visible

// Prefer borrowing when possible
let list1 = vec!["a", "b", "c"];
process_list(&list1);  // Borrow, no clone
println!("{:?}", list1);  // Still available
```

---

## Tooling

| Java Tool | Rust Equivalent | Purpose |
|-----------|----------------|---------|
| Maven / Gradle | Cargo | Build system, dependency management |
| JUnit | Built-in `#[test]` | Unit testing |
| Mockito | `mockall` | Mocking |
| Javadoc | `cargo doc` (rustdoc) | Documentation generation |
| IntelliJ IDEA | VS Code + rust-analyzer | IDE |
| Eclipse | RustRover (JetBrains) | IDE |
| Checkstyle / PMD | `cargo clippy` | Linting |
| Google Java Format | `cargo fmt` (rustfmt) | Code formatting |
| JaCoCo | `cargo-tarpaulin` / `cargo-llvm-cov` | Code coverage |
| VisualVM | `perf` / `valgrind` / `flamegraph` | Profiling |

---

## Examples

### Example 1: Simple - HTTP Client

**Before (Java):**
```java
import java.net.http.*;
import java.net.URI;

public class HttpExample {
    public static void main(String[] args) throws Exception {
        HttpClient client = HttpClient.newHttpClient();
        HttpRequest request = HttpRequest.newBuilder()
            .uri(URI.create("https://api.example.com/data"))
            .build();

        HttpResponse<String> response = client.send(
            request,
            HttpResponse.BodyHandlers.ofString()
        );

        System.out.println(response.body());
    }
}
```

**After (Rust):**
```rust
use reqwest;

#[tokio::main]
async fn main() -> Result<(), reqwest::Error> {
    let response = reqwest::get("https://api.example.com/data")
        .await?
        .text()
        .await?;

    println!("{}", response);
    Ok(())
}
```

### Example 2: Medium - Data Processing Pipeline

**Before (Java):**
```java
import java.util.*;
import java.util.stream.*;

public class DataProcessor {
    public static class User {
        String name;
        int age;
        String city;

        public User(String name, int age, String city) {
            this.name = name;
            this.age = age;
            this.city = city;
        }
    }

    public static List<String> processUsers(List<User> users) {
        return users.stream()
            .filter(user -> user.age >= 18)
            .filter(user -> user.city.equals("NYC"))
            .map(user -> user.name.toUpperCase())
            .sorted()
            .collect(Collectors.toList());
    }

    public static void main(String[] args) {
        List<User> users = Arrays.asList(
            new User("Alice", 25, "NYC"),
            new User("Bob", 17, "LA"),
            new User("Charlie", 30, "NYC")
        );

        List<String> result = processUsers(users);
        System.out.println(result);
    }
}
```

**After (Rust):**
```rust
#[derive(Debug)]
struct User {
    name: String,
    age: u32,
    city: String,
}

fn process_users(users: &[User]) -> Vec<String> {
    users
        .iter()
        .filter(|user| user.age >= 18)
        .filter(|user| user.city == "NYC")
        .map(|user| user.name.to_uppercase())
        .collect::<Vec<_>>()
        .into_iter()
        .sorted()
        .collect()
}

fn main() {
    let users = vec![
        User {
            name: String::from("Alice"),
            age: 25,
            city: String::from("NYC"),
        },
        User {
            name: String::from("Bob"),
            age: 17,
            city: String::from("LA"),
        },
        User {
            name: String::from("Charlie"),
            age: 30,
            city: String::from("NYC"),
        },
    ];

    let result = process_users(&users);
    println!("{:?}", result);
}
```

### Example 3: Complex - Concurrent Web Server

**Before (Java):**
```java
import java.io.*;
import java.net.*;
import java.util.concurrent.*;

public class SimpleServer {
    private static final ExecutorService executor =
        Executors.newFixedThreadPool(10);

    public static void main(String[] args) throws IOException {
        ServerSocket serverSocket = new ServerSocket(8080);
        System.out.println("Server started on port 8080");

        while (true) {
            Socket clientSocket = serverSocket.accept();
            executor.submit(() -> handleClient(clientSocket));
        }
    }

    private static void handleClient(Socket socket) {
        try (
            BufferedReader in = new BufferedReader(
                new InputStreamReader(socket.getInputStream())
            );
            PrintWriter out = new PrintWriter(
                socket.getOutputStream(), true
            )
        ) {
            String request = in.readLine();
            System.out.println("Request: " + request);

            String response = processRequest(request);
            out.println("HTTP/1.1 200 OK");
            out.println("Content-Type: text/plain");
            out.println();
            out.println(response);
        } catch (IOException e) {
            System.err.println("Error handling client: " + e.getMessage());
        }
    }

    private static String processRequest(String request) {
        // Simulate processing
        return "Processed: " + request;
    }
}
```

**After (Rust):**
```rust
use tokio::net::{TcpListener, TcpStream};
use tokio::io::{AsyncBufReadExt, AsyncWriteExt, BufReader};

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let listener = TcpListener::bind("127.0.0.1:8080").await?;
    println!("Server started on port 8080");

    loop {
        let (socket, _) = listener.accept().await?;
        tokio::spawn(async move {
            if let Err(e) = handle_client(socket).await {
                eprintln!("Error handling client: {}", e);
            }
        });
    }
}

async fn handle_client(socket: TcpStream) -> Result<(), Box<dyn std::error::Error>> {
    let mut reader = BufReader::new(socket);
    let mut request = String::new();

    reader.read_line(&mut request).await?;
    println!("Request: {}", request.trim());

    let response = process_request(&request);

    let mut socket = reader.into_inner();
    socket.write_all(b"HTTP/1.1 200 OK\r\n").await?;
    socket.write_all(b"Content-Type: text/plain\r\n").await?;
    socket.write_all(b"\r\n").await?;
    socket.write_all(response.as_bytes()).await?;

    Ok(())
}

fn process_request(request: &str) -> String {
    format!("Processed: {}", request.trim())
}
```

**Why this translation:**
- Tokio provides async I/O (more efficient than thread pool)
- `async`/`await` syntax is more readable
- Type-safe error handling with `Result`
- Automatic resource cleanup (no explicit try-with-resources)
- Lightweight async tasks instead of OS threads

---

## See Also

For more examples and patterns, see:
- `meta-convert-dev` - Foundational patterns with cross-language examples
- `convert-golang-rust` - Similar GC → ownership translation
- `convert-python-rust` - Dynamic → static typing translation
- `lang-java-dev` - Java development patterns
- `lang-rust-dev` - Rust development patterns

Cross-cutting pattern skills:
- `patterns-concurrency-dev` - Async, threads, channels across languages
- `patterns-serialization-dev` - JSON, validation, annotations across languages
- `patterns-metaprogramming-dev` - Annotations, macros, reflection across languages
