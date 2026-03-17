---
name: lang-rust-dev
description: Foundational Rust patterns covering core syntax, traits, generics, lifetimes, and common idioms. Use when writing Rust code, understanding ownership basics, working with Option/Result, or needing guidance on which specialized Rust skill to use. This is the entry point for Rust development.
---

# Rust Fundamentals

Foundational Rust patterns and core language features. This skill serves as both a reference for common patterns and an index to specialized Rust skills.

## Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                      Rust Skill Hierarchy                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│                    ┌───────────────────┐                        │
│                    │   lang-rust-dev   │ ◄── You are here       │
│                    │   (foundation)    │                        │
│                    └─────────┬─────────┘                        │
│                              │                                  │
│     ┌────────────┬───────────┼───────────┬────────────┐        │
│     │            │           │           │            │        │
│     ▼            ▼           ▼           ▼            ▼        │
│ ┌────────┐ ┌──────────┐ ┌────────┐ ┌─────────┐ ┌──────────┐   │
│ │ errors │ │  cargo   │ │library │ │ memory  │ │ profiling│   │
│ │  -dev  │ │   -dev   │ │  -dev  │ │  -eng   │ │   -eng   │   │
│ └────────┘ └──────────┘ └────────┘ └─────────┘ └──────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**This skill covers:**
- Core syntax (structs, enums, match, impl blocks)
- Traits and generics basics
- Lifetime fundamentals
- Option and Result patterns
- Iterators and closures
- Common idioms and conventions

**This skill does NOT cover (see specialized skills):**
- Error handling with error-stack → `lang-rust-errors-dev`
- Cargo.toml and dependencies → `lang-rust-cargo-dev`
- Library/crate publishing → `lang-rust-library-dev`
- Documentation patterns → `lang-rust-docs-dev`
- Memory safety engineering → `lang-rust-memory-eng`
- Benchmarking → `lang-rust-benchmarking-eng`
- Profiling/debugging → `lang-rust-profiling-eng`

---

## Quick Reference

| Task | Pattern |
|------|---------|
| Create struct | `struct Name { field: Type }` |
| Create enum | `enum Name { Variant1, Variant2(T) }` |
| Implement trait | `impl Trait for Type { ... }` |
| Generic function | `fn name<T: Trait>(x: T) -> T` |
| Lifetime annotation | `fn name<'a>(x: &'a str) -> &'a str` |
| Error propagation | `let x = fallible()?;` |
| Pattern match | `match value { Pattern => expr }` |
| Iterate | `for item in collection { ... }` |
| Map/filter | `iter.map(\|x\| ...).filter(\|x\| ...)` |

---

## Skill Routing

Use this table to find the right specialized skill:

| When you need to... | Use this skill |
|---------------------|----------------|
| Handle errors with Result/Report types | `lang-rust-errors-dev` |
| Configure Cargo.toml, add dependencies | `lang-rust-cargo-dev` |
| Design public APIs, publish crates | `lang-rust-library-dev` |
| Write documentation, rustdoc | `lang-rust-docs-dev` |
| Understand ownership deeply, unsafe code | `lang-rust-memory-eng` |
| Write benchmarks, measure performance | `lang-rust-benchmarking-eng` |
| Profile code, find bottlenecks | `lang-rust-profiling-eng` |

---

## Core Types

### Structs

```rust
// Named fields
struct User {
    name: String,
    email: String,
    age: u32,
}

// Tuple struct
struct Point(f64, f64);

// Unit struct
struct Marker;

// Creating instances
let user = User {
    name: String::from("Alice"),
    email: String::from("alice@example.com"),
    age: 30,
};

// Struct update syntax
let user2 = User {
    email: String::from("bob@example.com"),
    ..user  // Take remaining fields from user
};

// Destructuring
let User { name, email, .. } = user2;
```

### Enums

```rust
// Simple enum
enum Direction {
    North,
    South,
    East,
    West,
}

// Enum with data
enum Message {
    Quit,
    Move { x: i32, y: i32 },
    Write(String),
    ChangeColor(u8, u8, u8),
}

// Using enums
let msg = Message::Move { x: 10, y: 20 };

match msg {
    Message::Quit => println!("Quit"),
    Message::Move { x, y } => println!("Move to {x}, {y}"),
    Message::Write(text) => println!("Write: {text}"),
    Message::ChangeColor(r, g, b) => println!("Color: {r},{g},{b}"),
}
```

### Option and Result

```rust
// Option: value that might not exist
fn find_user(id: u32) -> Option<User> {
    if id == 1 {
        Some(User { /* ... */ })
    } else {
        None
    }
}

// Using Option
match find_user(1) {
    Some(user) => println!("Found: {}", user.name),
    None => println!("Not found"),
}

// Option methods
let name = find_user(1)
    .map(|u| u.name)
    .unwrap_or_else(|| String::from("Anonymous"));

// Result: operation that might fail
fn parse_config(path: &str) -> Result<Config, ConfigError> {
    let content = std::fs::read_to_string(path)?;
    let config = serde_json::from_str(&content)?;
    Ok(config)
}

// Error propagation with ?
fn process() -> Result<(), Error> {
    let config = parse_config("config.json")?;  // Returns early on error
    // ... use config
    Ok(())
}
```

---

## Pattern Matching

### Match Expressions

```rust
let x = 5;

match x {
    1 => println!("one"),
    2 | 3 => println!("two or three"),
    4..=6 => println!("four through six"),
    n if n > 10 => println!("greater than ten: {n}"),
    _ => println!("something else"),
}

// Destructuring in match
let point = (3, 4);
match point {
    (0, 0) => println!("origin"),
    (x, 0) => println!("on x-axis at {x}"),
    (0, y) => println!("on y-axis at {y}"),
    (x, y) => println!("at ({x}, {y})"),
}
```

### If Let and Let Else

```rust
// if let: match single pattern
if let Some(user) = find_user(1) {
    println!("Found: {}", user.name);
}

// let else: match or diverge
fn get_name(id: u32) -> String {
    let Some(user) = find_user(id) else {
        return String::from("Unknown");
    };
    user.name
}
```

---

## Traits

### Defining Traits

```rust
trait Summary {
    // Required method
    fn summarize(&self) -> String;

    // Default implementation
    fn preview(&self) -> String {
        format!("{}...", &self.summarize()[..50])
    }
}
```

### Implementing Traits

```rust
struct Article {
    title: String,
    content: String,
}

impl Summary for Article {
    fn summarize(&self) -> String {
        format!("{}: {}", self.title, self.content)
    }
}

// Use the trait
let article = Article { /* ... */ };
println!("{}", article.summarize());
```

### Common Standard Traits

| Trait | Purpose | Derive? |
|-------|---------|---------|
| `Debug` | Debug formatting `{:?}` | Yes |
| `Clone` | Explicit duplication | Yes |
| `Copy` | Implicit copying | Yes (if all fields Copy) |
| `Default` | Default value | Yes |
| `PartialEq` / `Eq` | Equality comparison | Yes |
| `PartialOrd` / `Ord` | Ordering | Yes |
| `Hash` | Hash for HashMap keys | Yes |
| `Display` | User-facing formatting | No |
| `From` / `Into` | Type conversion | No |

```rust
#[derive(Debug, Clone, PartialEq, Eq, Hash, Default)]
struct Config {
    name: String,
    value: i32,
}
```

### Trait Bounds

```rust
// Function with trait bound
fn print_summary<T: Summary>(item: &T) {
    println!("{}", item.summarize());
}

// Multiple bounds
fn process<T: Summary + Clone>(item: T) { /* ... */ }

// Where clause (cleaner for complex bounds)
fn complex<T, U>(t: T, u: U) -> String
where
    T: Summary + Clone,
    U: Debug + Default,
{
    // ...
}
```

---

## Generics

### Generic Functions

```rust
fn largest<T: PartialOrd>(list: &[T]) -> &T {
    let mut largest = &list[0];
    for item in list {
        if item > largest {
            largest = item;
        }
    }
    largest
}
```

### Generic Structs

```rust
struct Wrapper<T> {
    value: T,
}

impl<T> Wrapper<T> {
    fn new(value: T) -> Self {
        Wrapper { value }
    }

    fn get(&self) -> &T {
        &self.value
    }
}

// Conditional implementation
impl<T: Display> Wrapper<T> {
    fn print(&self) {
        println!("{}", self.value);
    }
}
```

### Generic Enums

```rust
// Option and Result are generic enums
enum Option<T> {
    Some(T),
    None,
}

enum Result<T, E> {
    Ok(T),
    Err(E),
}
```

---

## Lifetimes

### Basic Lifetime Annotations

```rust
// Lifetime ensures returned reference is valid
fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
    if x.len() > y.len() { x } else { y }
}

// Usage
let s1 = String::from("short");
let s2 = String::from("longer string");
let result = longest(&s1, &s2);
```

### Lifetime in Structs

```rust
// Struct containing references
struct Excerpt<'a> {
    text: &'a str,
}

impl<'a> Excerpt<'a> {
    fn level(&self) -> i32 {
        3  // Doesn't use the reference, no annotation needed
    }

    fn announce(&self, announcement: &str) -> &'a str {
        println!("Attention: {announcement}");
        self.text
    }
}
```

### Lifetime Elision

The compiler infers lifetimes in common cases:

```rust
// These are equivalent:
fn first_word(s: &str) -> &str { /* ... */ }
fn first_word<'a>(s: &'a str) -> &'a str { /* ... */ }

// Rules:
// 1. Each input reference gets its own lifetime
// 2. If exactly one input lifetime, output gets same
// 3. If &self, output gets lifetime of self
```

---

## Iterators

### Creating Iterators

```rust
let v = vec![1, 2, 3, 4, 5];

// Borrowing iterator
for x in &v {
    println!("{x}");
}

// Consuming iterator
for x in v {
    println!("{x}");
}

// Mutable iterator
let mut v = vec![1, 2, 3];
for x in &mut v {
    *x *= 2;
}
```

### Iterator Adapters

```rust
let v = vec![1, 2, 3, 4, 5];

// map: transform each element
let doubled: Vec<_> = v.iter().map(|x| x * 2).collect();

// filter: keep matching elements
let evens: Vec<_> = v.iter().filter(|x| *x % 2 == 0).collect();

// chain adapters
let result: Vec<_> = v.iter()
    .filter(|x| *x > 2)
    .map(|x| x * 10)
    .collect();

// find: first matching element
let found = v.iter().find(|x| **x > 3);

// fold: accumulate
let sum: i32 = v.iter().fold(0, |acc, x| acc + x);
// Or use sum()
let sum: i32 = v.iter().sum();
```

### Common Iterator Methods

| Method | Purpose |
|--------|---------|
| `map` | Transform elements |
| `filter` | Keep matching elements |
| `filter_map` | Filter and transform in one |
| `flat_map` | Map and flatten |
| `take(n)` | First n elements |
| `skip(n)` | Skip first n elements |
| `enumerate` | Add index to elements |
| `zip` | Combine two iterators |
| `collect` | Collect into container |
| `fold` | Reduce to single value |
| `find` | First matching element |
| `any` / `all` | Boolean predicates |

---

## Closures

### Closure Syntax

```rust
// Full syntax
let add = |a: i32, b: i32| -> i32 { a + b };

// Type inference
let add = |a, b| a + b;

// Single expression (no braces needed)
let double = |x| x * 2;

// Capturing environment
let multiplier = 3;
let multiply = |x| x * multiplier;
```

### Closure Traits

| Trait | Captures | Can be called |
|-------|----------|---------------|
| `Fn` | Immutable borrow | Multiple times |
| `FnMut` | Mutable borrow | Multiple times |
| `FnOnce` | Takes ownership | Once |

```rust
// Function taking a closure
fn apply<F>(f: F, x: i32) -> i32
where
    F: Fn(i32) -> i32,
{
    f(x)
}

let result = apply(|x| x * 2, 5);
```

### Move Closures

```rust
// Force closure to take ownership
let s = String::from("hello");
let print = move || println!("{s}");
// s is no longer valid here

print();  // Works because closure owns s
```

---

## Common Idioms

### Builder Pattern

```rust
struct RequestBuilder {
    url: String,
    method: String,
    headers: Vec<(String, String)>,
}

impl RequestBuilder {
    fn new(url: impl Into<String>) -> Self {
        Self {
            url: url.into(),
            method: String::from("GET"),
            headers: Vec::new(),
        }
    }

    fn method(mut self, method: impl Into<String>) -> Self {
        self.method = method.into();
        self
    }

    fn header(mut self, key: impl Into<String>, value: impl Into<String>) -> Self {
        self.headers.push((key.into(), value.into()));
        self
    }

    fn build(self) -> Request {
        Request { /* ... */ }
    }
}

// Usage
let request = RequestBuilder::new("https://api.example.com")
    .method("POST")
    .header("Content-Type", "application/json")
    .build();
```

### Newtype Pattern

```rust
// Wrap primitive types for type safety
struct UserId(u64);
struct OrderId(u64);

fn process_user(id: UserId) { /* ... */ }
fn process_order(id: OrderId) { /* ... */ }

// Can't mix them up
let user_id = UserId(1);
let order_id = OrderId(1);
// process_user(order_id);  // Compile error!
```

### Type State Pattern

```rust
// Compile-time state machine
struct Request<State> {
    url: String,
    _state: std::marker::PhantomData<State>,
}

struct Unvalidated;
struct Validated;

impl Request<Unvalidated> {
    fn validate(self) -> Result<Request<Validated>, Error> {
        // Validation logic
        Ok(Request {
            url: self.url,
            _state: std::marker::PhantomData,
        })
    }
}

impl Request<Validated> {
    fn send(self) -> Response {
        // Only valid requests can be sent
    }
}
```

---

## Troubleshooting

### Ownership Errors

**Problem:** `value borrowed here after move`

```rust
let s = String::from("hello");
let s2 = s;
println!("{s}");  // Error: s was moved to s2
```

**Fix:** Clone if you need both, or use references:
```rust
let s = String::from("hello");
let s2 = s.clone();
println!("{s}");  // Works
```

### Lifetime Errors

**Problem:** `missing lifetime specifier`

```rust
fn get_first(s: &str, t: &str) -> &str {
    s  // Error: which lifetime?
}
```

**Fix:** Add explicit lifetimes:
```rust
fn get_first<'a>(s: &'a str, _t: &str) -> &'a str {
    s
}
```

### Trait Bound Errors

**Problem:** `the trait X is not implemented for Y`

```rust
fn print_it<T>(x: T) {
    println!("{}", x);  // Error: T doesn't implement Display
}
```

**Fix:** Add trait bound:
```rust
fn print_it<T: std::fmt::Display>(x: T) {
    println!("{}", x);
}
```

### Mutability Errors

**Problem:** `cannot borrow as mutable`

```rust
let v = vec![1, 2, 3];
v.push(4);  // Error: v is not mutable
```

**Fix:** Make it mutable:
```rust
let mut v = vec![1, 2, 3];
v.push(4);
```

---

## Module System

Rust uses a module system to organize code into logical units with explicit visibility control.

### Module Basics

```rust
// src/lib.rs or src/main.rs

// Inline module
mod math {
    pub fn add(a: i32, b: i32) -> i32 {
        a + b
    }

    fn private_helper() -> i32 {
        42
    }
}

// Use items from module
use math::add;

fn main() {
    let sum = add(2, 3);
    // math::private_helper();  // Error: function is private
}
```

### File-Based Modules

```
src/
├── main.rs          # Crate root
├── lib.rs           # Library crate root (if both bin and lib)
├── config.rs        # mod config;
└── network/
    ├── mod.rs       # mod network;
    ├── client.rs    # mod client; (in mod.rs)
    └── server.rs    # mod server; (in mod.rs)
```

```rust
// src/main.rs
mod config;           // Loads from src/config.rs
mod network;          // Loads from src/network/mod.rs

use config::Settings;
use network::client::Client;

// src/network/mod.rs
pub mod client;       // Loads from src/network/client.rs
pub mod server;
```

### Visibility Rules

```rust
mod outer {
    pub mod inner {
        pub fn public_fn() {}           // Visible everywhere
        pub(crate) fn crate_fn() {}     // Visible in crate
        pub(super) fn parent_fn() {}    // Visible in parent module
        pub(in crate::outer) fn outer_fn() {}  // Visible in specific path
        fn private_fn() {}              // Only this module
    }
}
```

### Re-exports

```rust
// src/lib.rs - Flatten the public API
mod internal {
    pub mod config {
        pub struct Settings { /* ... */ }
    }
    pub mod network {
        pub struct Client { /* ... */ }
    }
}

// Re-export for cleaner external API
pub use internal::config::Settings;
pub use internal::network::Client;

// External users can now:
// use mycrate::Settings;
// Instead of:
// use mycrate::internal::config::Settings;
```

### Prelude Pattern

```rust
// src/prelude.rs
pub use crate::config::Settings;
pub use crate::error::{Error, Result};
pub use crate::traits::{Serialize, Deserialize};

// Users can import everything commonly needed:
// use mycrate::prelude::*;
```

### Path Types

| Path | Meaning |
|------|---------|
| `crate::` | Start from crate root |
| `self::` | Current module |
| `super::` | Parent module |
| `::path` | External crate (Rust 2018+: crate name) |

---

## Concurrency

Rust provides fearless concurrency through its ownership system. The type system prevents data races at compile time.

### Threads

```rust
use std::thread;

// Spawn a thread
let handle = thread::spawn(|| {
    println!("Hello from thread!");
});

handle.join().unwrap();  // Wait for thread to finish

// Move data into thread
let data = vec![1, 2, 3];
let handle = thread::spawn(move || {
    println!("Data: {:?}", data);
});
```

### Message Passing (Channels)

```rust
use std::sync::mpsc;  // Multiple producer, single consumer

let (tx, rx) = mpsc::channel();

// Clone sender for multiple producers
let tx2 = tx.clone();

thread::spawn(move || {
    tx.send("Hello").unwrap();
});

thread::spawn(move || {
    tx2.send("World").unwrap();
});

// Receive messages
for received in rx {
    println!("Got: {received}");
}
```

### Shared State (Mutex, Arc)

```rust
use std::sync::{Arc, Mutex};

// Arc: Atomic Reference Counted (thread-safe Rc)
// Mutex: Mutual exclusion for safe mutable access
let counter = Arc::new(Mutex::new(0));

let mut handles = vec![];

for _ in 0..10 {
    let counter = Arc::clone(&counter);
    let handle = thread::spawn(move || {
        let mut num = counter.lock().unwrap();
        *num += 1;
    });
    handles.push(handle);
}

for handle in handles {
    handle.join().unwrap();
}

println!("Result: {}", *counter.lock().unwrap());
```

### Async/Await

```rust
// Requires async runtime (tokio, async-std)
// Cargo.toml: tokio = { version = "1", features = ["full"] }

use tokio;

async fn fetch_data(url: &str) -> Result<String, reqwest::Error> {
    reqwest::get(url).await?.text().await
}

async fn process() {
    let data = fetch_data("https://api.example.com").await.unwrap();
    println!("{data}");
}

// Run async main
#[tokio::main]
async fn main() {
    process().await;
}

// Concurrent execution
async fn fetch_all() {
    let (a, b) = tokio::join!(
        fetch_data("https://api.example.com/a"),
        fetch_data("https://api.example.com/b"),
    );
}
```

### Send and Sync Traits

| Trait | Meaning |
|-------|---------|
| `Send` | Safe to send between threads |
| `Sync` | Safe to share references between threads |

```rust
// Most types are Send + Sync automatically
// Rc is not Send (use Arc instead)
// Cell/RefCell are not Sync (use Mutex instead)
```

**See also:** `patterns-concurrency-dev` for cross-language concurrency patterns

---

## Serialization

Rust uses the serde framework for serialization and deserialization.

### Basic Serde Usage

```rust
// Cargo.toml:
// serde = { version = "1.0", features = ["derive"] }
// serde_json = "1.0"

use serde::{Serialize, Deserialize};

#[derive(Debug, Serialize, Deserialize)]
struct User {
    name: String,
    email: String,
    age: u32,
}

fn main() -> Result<(), serde_json::Error> {
    let user = User {
        name: String::from("Alice"),
        email: String::from("alice@example.com"),
        age: 30,
    };

    // Serialize to JSON
    let json = serde_json::to_string(&user)?;
    println!("{json}");

    // Deserialize from JSON
    let parsed: User = serde_json::from_str(&json)?;
    println!("{:?}", parsed);

    Ok(())
}
```

### Serde Attributes

```rust
#[derive(Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]  // All fields as camelCase
struct Config {
    #[serde(rename = "api_key")]    // Custom field name
    key: String,

    #[serde(default)]               // Use Default if missing
    retries: u32,

    #[serde(skip_serializing_if = "Option::is_none")]
    email: Option<String>,

    #[serde(skip)]                  // Never serialize/deserialize
    internal_state: u32,

    #[serde(flatten)]               // Flatten nested struct
    metadata: Metadata,
}

#[derive(Serialize, Deserialize)]
struct Metadata {
    version: String,
    author: String,
}
```

### Enum Serialization

```rust
#[derive(Serialize, Deserialize)]
#[serde(tag = "type")]  // Internally tagged
enum Message {
    #[serde(rename = "text")]
    Text { content: String },

    #[serde(rename = "image")]
    Image { url: String, width: u32 },
}

// Serializes as: {"type": "text", "content": "Hello"}
```

### Custom Serialization

```rust
use serde::{Serializer, Deserializer};

#[derive(Serialize, Deserialize)]
struct Data {
    #[serde(serialize_with = "serialize_as_string")]
    #[serde(deserialize_with = "deserialize_from_string")]
    value: u64,
}

fn serialize_as_string<S>(value: &u64, s: S) -> Result<S::Ok, S::Error>
where
    S: Serializer,
{
    s.serialize_str(&value.to_string())
}

fn deserialize_from_string<'de, D>(d: D) -> Result<u64, D::Error>
where
    D: Deserializer<'de>,
{
    let s: String = Deserialize::deserialize(d)?;
    s.parse().map_err(serde::de::Error::custom)
}
```

### Other Formats

```rust
// YAML: serde_yaml = "0.9"
let yaml = serde_yaml::to_string(&data)?;
let parsed: Data = serde_yaml::from_str(&yaml)?;

// TOML: toml = "0.8"
let toml = toml::to_string(&data)?;
let parsed: Data = toml::from_str(&toml)?;

// MessagePack: rmp-serde = "1.1"
let msgpack = rmp_serde::to_vec(&data)?;
let parsed: Data = rmp_serde::from_slice(&msgpack)?;
```

**See also:** `patterns-serialization-dev` for cross-language serialization patterns

---

## Build and Dependencies

Rust uses Cargo as its build system and package manager.

### Cargo.toml Basics

```toml
[package]
name = "myproject"
version = "0.1.0"
edition = "2021"
authors = ["Your Name <you@example.com>"]
description = "A brief description"
license = "MIT OR Apache-2.0"
repository = "https://github.com/user/project"

[dependencies]
serde = { version = "1.0", features = ["derive"] }
tokio = { version = "1", features = ["full"] }
reqwest = "0.11"

[dev-dependencies]
criterion = "0.5"

[build-dependencies]
cc = "1.0"

[features]
default = ["json"]
json = ["serde_json"]
full = ["json", "yaml"]

[[bin]]
name = "myapp"
path = "src/main.rs"

[[bench]]
name = "my_benchmark"
harness = false
```

### Dependency Specification

```toml
# Version requirements
exact = "=1.0.0"        # Exactly 1.0.0
caret = "^1.2.3"        # >=1.2.3, <2.0.0 (default)
tilde = "~1.2.3"        # >=1.2.3, <1.3.0
wildcard = "1.*"        # >=1.0.0, <2.0.0

# Features
serde = { version = "1.0", features = ["derive"], default-features = false }

# Git dependencies
mylib = { git = "https://github.com/user/mylib", branch = "main" }
mylib = { git = "https://github.com/user/mylib", tag = "v1.0.0" }
mylib = { git = "https://github.com/user/mylib", rev = "abc123" }

# Path dependencies (local development)
mylib = { path = "../mylib" }

# Optional dependencies
serde_json = { version = "1.0", optional = true }
```

### Common Cargo Commands

| Command | Purpose |
|---------|---------|
| `cargo build` | Compile the project |
| `cargo build --release` | Compile with optimizations |
| `cargo run` | Build and run |
| `cargo test` | Run tests |
| `cargo check` | Fast type checking (no codegen) |
| `cargo clippy` | Lint code |
| `cargo fmt` | Format code |
| `cargo doc --open` | Generate and open docs |
| `cargo update` | Update dependencies |
| `cargo add <crate>` | Add a dependency |
| `cargo tree` | Show dependency tree |

### Workspace Configuration

```toml
# Root Cargo.toml
[workspace]
members = [
    "crates/core",
    "crates/cli",
    "crates/web",
]
resolver = "2"

[workspace.package]
version = "0.1.0"
edition = "2021"
license = "MIT"

[workspace.dependencies]
serde = { version = "1.0", features = ["derive"] }
tokio = { version = "1", features = ["full"] }
```

```toml
# crates/core/Cargo.toml
[package]
name = "myproject-core"
version.workspace = true
edition.workspace = true

[dependencies]
serde.workspace = true
```

### Build Scripts

```rust
// build.rs - Runs before compilation
fn main() {
    // Tell Cargo to rerun if file changes
    println!("cargo:rerun-if-changed=src/proto/schema.proto");

    // Set environment variable for compilation
    println!("cargo:rustc-env=BUILD_VERSION=1.0.0");

    // Add link search path
    println!("cargo:rustc-link-search=/usr/local/lib");
}
```

**See also:** `lang-rust-cargo-dev` for advanced Cargo configuration

---

## Testing

Rust has built-in testing support with `cargo test`.

### Unit Tests

```rust
// src/lib.rs

pub fn add(a: i32, b: i32) -> i32 {
    a + b
}

fn private_helper() -> i32 {
    42
}

#[cfg(test)]
mod tests {
    use super::*;  // Import from parent module

    #[test]
    fn test_add() {
        assert_eq!(add(2, 3), 5);
    }

    #[test]
    fn test_add_negative() {
        assert_eq!(add(-1, 1), 0);
    }

    #[test]
    fn test_private_helper() {
        // Can test private functions
        assert_eq!(private_helper(), 42);
    }

    #[test]
    #[should_panic(expected = "divide by zero")]
    fn test_panic() {
        divide(1, 0);
    }

    #[test]
    fn test_result() -> Result<(), String> {
        let result = parse_number("42")?;
        assert_eq!(result, 42);
        Ok(())
    }
}
```

### Integration Tests

```
tests/
├── integration_test.rs    # Each file is a separate test crate
└── common/
    └── mod.rs             # Shared test utilities
```

```rust
// tests/integration_test.rs
use myproject::add;

mod common;  // Load shared utilities

#[test]
fn test_add_integration() {
    common::setup();
    assert_eq!(add(2, 3), 5);
}
```

### Assertions

```rust
#[test]
fn test_assertions() {
    // Equality
    assert_eq!(actual, expected);
    assert_ne!(actual, not_expected);

    // Boolean
    assert!(condition);
    assert!(!condition);

    // With custom message
    assert_eq!(result, 42, "Expected 42, got {}", result);

    // Debug assertions (only in debug builds)
    debug_assert!(condition);
}
```

### Test Attributes

```rust
#[test]
fn normal_test() {}

#[test]
#[ignore]  // Skip by default, run with --ignored
fn slow_test() {}

#[test]
#[should_panic]
fn test_panics() {
    panic!("This should panic");
}

#[test]
#[should_panic(expected = "specific message")]
fn test_specific_panic() {
    panic!("specific message here");
}
```

### Running Tests

```bash
cargo test                    # Run all tests
cargo test test_name          # Run tests matching name
cargo test -- --nocapture     # Show println! output
cargo test -- --test-threads=1  # Run sequentially
cargo test --ignored          # Run ignored tests
cargo test --test integration # Run specific test file
```

### Test Organization

```rust
// Group related tests
mod parsing_tests {
    use super::*;

    #[test]
    fn test_parse_number() { /* ... */ }

    #[test]
    fn test_parse_string() { /* ... */ }
}

// Setup and teardown
struct TestFixture {
    temp_dir: tempfile::TempDir,
}

impl TestFixture {
    fn new() -> Self {
        Self {
            temp_dir: tempfile::tempdir().unwrap(),
        }
    }
}

impl Drop for TestFixture {
    fn drop(&mut self) {
        // Cleanup happens automatically
    }
}

#[test]
fn test_with_fixture() {
    let fixture = TestFixture::new();
    // Use fixture.temp_dir
}
```

### Mocking (with mockall)

```rust
// Cargo.toml: mockall = "0.11"

use mockall::{automock, predicate::*};

#[automock]
trait Database {
    fn get_user(&self, id: u32) -> Option<User>;
}

#[test]
fn test_with_mock() {
    let mut mock = MockDatabase::new();
    mock.expect_get_user()
        .with(eq(1))
        .returning(|_| Some(User { name: "Alice".into() }));

    let result = process_user(&mock, 1);
    assert!(result.is_ok());
}
```

### Property-Based Testing (with proptest)

```rust
// Cargo.toml: proptest = "1.0"

use proptest::prelude::*;

proptest! {
    #[test]
    fn test_add_commutative(a: i32, b: i32) {
        prop_assert_eq!(add(a, b), add(b, a));
    }

    #[test]
    fn test_parse_roundtrip(s in "[a-z]{1,10}") {
        let parsed = parse(&s);
        prop_assert!(parsed.is_ok());
    }
}
```

---

## Metaprogramming

Rust provides powerful metaprogramming through macros. There are two main types: declarative macros (`macro_rules!`) and procedural macros (derive, attribute, and function-like).

### Declarative Macros (macro_rules!)

```rust
// Simple macro
macro_rules! say_hello {
    () => {
        println!("Hello!");
    };
}

say_hello!();  // Prints: Hello!

// Macro with arguments
macro_rules! create_function {
    ($name:ident) => {
        fn $name() {
            println!("Called {:?}", stringify!($name));
        }
    };
}

create_function!(foo);
foo();  // Prints: Called "foo"

// Macro with expression repetition
macro_rules! vec_of_strings {
    ($($x:expr),* $(,)?) => {
        vec![$($x.to_string()),*]
    };
}

let v = vec_of_strings!["a", "b", "c"];
```

### Fragment Specifiers

| Specifier | Matches | Example |
|-----------|---------|---------|
| `$x:ident` | Identifier | `foo`, `MyStruct` |
| `$x:expr` | Expression | `1 + 2`, `foo()` |
| `$x:ty` | Type | `i32`, `Vec<String>` |
| `$x:pat` | Pattern | `Some(x)`, `_` |
| `$x:stmt` | Statement | `let x = 1;` |
| `$x:block` | Block | `{ ... }` |
| `$x:item` | Item | `fn foo() {}` |
| `$x:path` | Path | `std::io::Error` |
| `$x:tt` | Token tree | Any single token |
| `$x:literal` | Literal | `"hello"`, `42` |

### Macro Patterns

```rust
// Multiple match arms
macro_rules! calculate {
    // Single value
    ($e:expr) => { $e };
    // Two values with operator
    ($left:expr, $op:tt, $right:expr) => {
        $left $op $right
    };
}

let a = calculate!(5);        // 5
let b = calculate!(5, +, 3);  // 8

// Recursive macro for variadic arguments
macro_rules! sum {
    ($x:expr) => { $x };
    ($x:expr, $($rest:expr),+) => {
        $x + sum!($($rest),+)
    };
}

let total = sum!(1, 2, 3, 4);  // 10
```

### Derive Macros

Derive macros generate trait implementations automatically.

```rust
// Using built-in derives
#[derive(Debug, Clone, PartialEq, Eq, Hash, Default)]
struct User {
    name: String,
    age: u32,
}

// Using third-party derives
use serde::{Serialize, Deserialize};

#[derive(Serialize, Deserialize)]
struct Config {
    host: String,
    port: u16,
}
```

### Creating Custom Derive Macros

```rust
// In a proc-macro crate (Cargo.toml: proc-macro = true)
use proc_macro::TokenStream;
use quote::quote;
use syn::{parse_macro_input, DeriveInput};

#[proc_macro_derive(MyTrait)]
pub fn derive_my_trait(input: TokenStream) -> TokenStream {
    let input = parse_macro_input!(input as DeriveInput);
    let name = input.ident;

    let expanded = quote! {
        impl MyTrait for #name {
            fn describe(&self) -> String {
                format!("This is a {}", stringify!(#name))
            }
        }
    };

    TokenStream::from(expanded)
}

// Usage
#[derive(MyTrait)]
struct MyStruct;
```

### Derive Macro with Attributes

```rust
// Macro definition
#[proc_macro_derive(Builder, attributes(builder))]
pub fn derive_builder(input: TokenStream) -> TokenStream {
    let input = parse_macro_input!(input as DeriveInput);
    // Parse #[builder(...)] attributes
    // Generate builder pattern implementation
    // ...
}

// Usage
#[derive(Builder)]
struct Command {
    #[builder(default = "false")]
    verbose: bool,

    #[builder(each = "arg")]
    args: Vec<String>,
}
```

### Attribute Macros

```rust
// Macro definition (in proc-macro crate)
#[proc_macro_attribute]
pub fn route(attr: TokenStream, item: TokenStream) -> TokenStream {
    let attr = parse_macro_input!(attr as LitStr);
    let item = parse_macro_input!(item as ItemFn);
    let fn_name = &item.sig.ident;

    let expanded = quote! {
        #item

        inventory::submit! {
            Route {
                path: #attr,
                handler: #fn_name,
            }
        }
    };

    TokenStream::from(expanded)
}

// Usage
#[route("/api/users")]
fn get_users() -> Response {
    // ...
}
```

### Function-like Procedural Macros

```rust
// Macro definition
#[proc_macro]
pub fn sql(input: TokenStream) -> TokenStream {
    let input = parse_macro_input!(input as LitStr);
    let query = input.value();

    // Validate SQL at compile time
    // Generate typed query code
    let expanded = quote! {
        Query::new(#query)
    };

    TokenStream::from(expanded)
}

// Usage
let query = sql!("SELECT * FROM users WHERE id = $1");
```

### Common Proc-Macro Crates

| Crate | Purpose | Example |
|-------|---------|---------|
| `syn` | Parse Rust code | `parse_macro_input!` |
| `quote` | Generate Rust code | `quote! { ... }` |
| `proc-macro2` | TokenStream utilities | Span manipulation |
| `darling` | Derive macro helpers | Attribute parsing |

### Macro Hygiene

```rust
macro_rules! using_x {
    ($e:expr) => {
        {
            let x = 42;  // This x is hygienic
            $e           // $e refers to caller's x
        }
    };
}

let x = 10;
let result = using_x!(x + 1);  // Uses caller's x=10, not macro's x=42
assert_eq!(result, 11);
```

### Debug Macros

```rust
// Print macro expansion
// Run: cargo expand
// Or: cargo expand --lib path::to::module

// Compile-time debugging
macro_rules! debug_macro {
    ($($arg:tt)*) => {
        compile_error!(concat!("Debug: ", stringify!($($arg)*)));
    };
}
```

### See Also

- `patterns-metaprogramming-dev` - Cross-language macro/decorator patterns

---

## Cross-Cutting Patterns

For cross-language comparison and translation patterns, see:

- `patterns-concurrency-dev` - Async/await, threads, channels
- `patterns-serialization-dev` - JSON, validation, struct tags
- `patterns-metaprogramming-dev` - Decorators, macros, annotations

---

## References

- [The Rust Book](https://doc.rust-lang.org/book/)
- [Rust by Example](https://doc.rust-lang.org/rust-by-example/)
- [Rust Reference](https://doc.rust-lang.org/reference/)
- Specialized skills: `lang-rust-errors-dev`, `lang-rust-cargo-dev`, `lang-rust-library-dev`, `lang-rust-docs-dev`, `lang-rust-memory-eng`
