---
name: rust
description: 'Rust language expertise for writing safe, performant, production-quality
  Rust code. Use for Rust development, ownership patterns, error handling, async/await,
  and cargo management. Triggers: rust, car'
---

---
name: rust
description: Rust language expertise for writing safe, performant, production-quality Rust code. Use for Rust development, ownership patterns, error handling, async/await, and cargo management. Triggers: rust, cargo, rustc, ownership, borrowing, lifetime, Result, Option, traits, crates.
---

# Rust Language Expertise

## Overview

This skill provides guidance for writing safe, efficient, and idiomatic Rust code. It covers Rust's ownership system, error handling patterns, traits and generics, async programming, and cargo ecosystem.

## Key Concepts

### Ownership, Borrowing, and Lifetimes

```rust
// Ownership rules:
// 1. Each value has exactly one owner
// 2. When the owner goes out of scope, the value is dropped
// 3. Ownership can be transferred (moved) or borrowed

// Move semantics
fn take_ownership(s: String) {
    println!("{}", s);
} // s is dropped here

fn main() {
    let s = String::from("hello");
    take_ownership(s);
    // s is no longer valid here
}

// Borrowing (references)
fn borrow(s: &String) {
    println!("{}", s);
}

fn borrow_mut(s: &mut String) {
    s.push_str(" world");
}

// Lifetimes ensure references are valid
fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
    if x.len() > y.len() { x } else { y }
}

// Struct with lifetime annotations
struct Parser<'a> {
    input: &'a str,
    position: usize,
}

impl<'a> Parser<'a> {
    fn new(input: &'a str) -> Self {
        Parser { input, position: 0 }
    }

    fn peek(&self) -> Option<char> {
        self.input[self.position..].chars().next()
    }
}

// Common lifetime elision patterns
impl Config {
    // fn get(&self, key: &str) -> Option<&str>
    // is short for:
    // fn get<'a, 'b>(&'a self, key: &'b str) -> Option<&'a str>
    fn get(&self, key: &str) -> Option<&str> {
        self.map.get(key).map(|s| s.as_str())
    }
}
```

### Error Handling

```rust
use std::error::Error;
use std::fmt;
use std::io;

// Using thiserror for custom errors
use thiserror::Error;

#[derive(Error, Debug)]
pub enum AppError {
    #[error("IO error: {0}")]
    Io(#[from] io::Error),

    #[error("Parse error at line {line}: {message}")]
    Parse { line: usize, message: String },

    #[error("Not found: {0}")]
    NotFound(String),

    #[error("Validation failed: {0}")]
    Validation(String),
}

// Using anyhow for application code
use anyhow::{Context, Result, bail, ensure};

fn read_config(path: &str) -> Result<Config> {
    let content = std::fs::read_to_string(path)
        .with_context(|| format!("Failed to read config from {}", path))?;

    let config: Config = serde_json::from_str(&content)
        .context("Failed to parse config JSON")?;

    ensure!(!config.name.is_empty(), "Config name cannot be empty");

    if config.port == 0 {
        bail!("Invalid port number");
    }

    Ok(config)
}

// The ? operator for propagating errors
fn process_file(path: &str) -> Result<Vec<Record>, AppError> {
    let content = std::fs::read_to_string(path)?; // io::Error -> AppError via From
    let records = parse_records(&content)?;
    Ok(records)
}

// Option handling
fn find_user(users: &[User], name: &str) -> Option<&User> {
    users.iter().find(|u| u.name == name)
}

fn get_user_email(users: &[User], name: &str) -> Option<String> {
    users
        .iter()
        .find(|u| u.name == name)
        .and_then(|u| u.email.clone())
}

// Converting between Option and Result
fn require_user(users: &[User], name: &str) -> Result<&User, AppError> {
    users
        .iter()
        .find(|u| u.name == name)
        .ok_or_else(|| AppError::NotFound(format!("User: {}", name)))
}
```

### Traits and Generics

```rust
// Defining traits
trait Repository<T> {
    fn get(&self, id: &str) -> Option<&T>;
    fn save(&mut self, item: T) -> Result<(), Box<dyn Error>>;

    // Default implementation
    fn exists(&self, id: &str) -> bool {
        self.get(id).is_some()
    }
}

// Trait bounds
fn process<T: Clone + Debug>(item: &T) {
    let cloned = item.clone();
    println!("{:?}", cloned);
}

// where clauses for complex bounds
fn merge<T, U, V>(a: T, b: U) -> V
where
    T: IntoIterator<Item = V>,
    U: IntoIterator<Item = V>,
    V: Ord + Clone,
{
    let mut result: Vec<V> = a.into_iter().chain(b.into_iter()).collect();
    result.sort();
    result.dedup();
    result.into_iter().next().unwrap()
}

// Associated types
trait Iterator {
    type Item;
    fn next(&mut self) -> Option<Self::Item>;
}

// Implementing traits
struct InMemoryRepo<T> {
    items: HashMap<String, T>,
}

impl<T: Clone> Repository<T> for InMemoryRepo<T> {
    fn get(&self, id: &str) -> Option<&T> {
        self.items.get(id)
    }

    fn save(&mut self, item: T) -> Result<(), Box<dyn Error>> {
        // Implementation
        Ok(())
    }
}

// Blanket implementations
impl<T: Display> ToString for T {
    fn to_string(&self) -> String {
        format!("{}", self)
    }
}
```

### Iterators

```rust
// Iterator combinators
fn process_users(users: Vec<User>) -> Vec<String> {
    users
        .into_iter()
        .filter(|u| u.active)
        .map(|u| u.email)
        .filter_map(|email| email)  // Remove None values
        .collect()
}

// Custom iterator
struct Counter {
    current: usize,
    max: usize,
}

impl Iterator for Counter {
    type Item = usize;

    fn next(&mut self) -> Option<Self::Item> {
        if self.current < self.max {
            let val = self.current;
            self.current += 1;
            Some(val)
        } else {
            None
        }
    }
}

// Useful iterator methods
fn examples(numbers: Vec<i32>) {
    // Fold/reduce
    let sum: i32 = numbers.iter().fold(0, |acc, x| acc + x);

    // Any/all
    let has_positive = numbers.iter().any(|&x| x > 0);
    let all_positive = numbers.iter().all(|&x| x > 0);

    // Find
    let first_even = numbers.iter().find(|&&x| x % 2 == 0);

    // Partition
    let (evens, odds): (Vec<_>, Vec<_>) = numbers.iter().partition(|&&x| x % 2 == 0);

    // Enumerate
    for (index, value) in numbers.iter().enumerate() {
        println!("{}: {}", index, value);
    }

    // Zip
    let other = vec![1, 2, 3];
    let pairs: Vec<_> = numbers.iter().zip(other.iter()).collect();
}
```

## Best Practices

### Cargo and Project Structure

```toml
# Cargo.toml
[package]
name = "myproject"
version = "0.1.0"
edition = "2021"
rust-version = "1.75"

[dependencies]
tokio = { version = "1.35", features = ["full"] }
serde = { version = "1.0", features = ["derive"] }
thiserror = "1.0"
anyhow = "1.0"

[dev-dependencies]
criterion = "0.5"
mockall = "0.12"

[features]
default = []
full = ["feature-a", "feature-b"]
feature-a = []
feature-b = ["dep:optional-dep"]

[[bench]]
name = "my_benchmark"
harness = false
```

### Workspace Structure

```
myworkspace/
├── Cargo.toml          # Workspace root
├── crates/
│   ├── core/
│   │   ├── Cargo.toml
│   │   └── src/
│   ├── api/
│   │   ├── Cargo.toml
│   │   └── src/
│   └── cli/
│       ├── Cargo.toml
│       └── src/
```

```toml
# Root Cargo.toml
[workspace]
members = ["crates/*"]
resolver = "2"

[workspace.dependencies]
serde = { version = "1.0", features = ["derive"] }
tokio = { version = "1.35", features = ["full"] }
```

### Async/Await

```rust
use tokio::sync::{mpsc, Mutex};
use std::sync::Arc;

async fn fetch_data(url: &str) -> Result<String> {
    let response = reqwest::get(url).await?;
    let body = response.text().await?;
    Ok(body)
}

// Concurrent execution
async fn fetch_all(urls: Vec<String>) -> Vec<Result<String>> {
    let futures: Vec<_> = urls.iter().map(|url| fetch_data(url)).collect();
    futures::future::join_all(futures).await
}

// Shared state with Arc<Mutex<T>>
struct AppState {
    counter: Arc<Mutex<u64>>,
}

impl AppState {
    async fn increment(&self) -> u64 {
        let mut counter = self.counter.lock().await;
        *counter += 1;
        *counter
    }
}

// Channel communication
async fn producer_consumer() {
    let (tx, mut rx) = mpsc::channel(32);

    tokio::spawn(async move {
        for i in 0..10 {
            tx.send(i).await.unwrap();
        }
    });

    while let Some(value) = rx.recv().await {
        println!("Received: {}", value);
    }
}
```

## Common Patterns

### Builder Pattern

```rust
#[derive(Default)]
pub struct RequestBuilder {
    url: Option<String>,
    method: Method,
    headers: HashMap<String, String>,
    body: Option<Vec<u8>>,
    timeout: Duration,
}

impl RequestBuilder {
    pub fn new() -> Self {
        Self {
            method: Method::GET,
            timeout: Duration::from_secs(30),
            ..Default::default()
        }
    }

    pub fn url(mut self, url: impl Into<String>) -> Self {
        self.url = Some(url.into());
        self
    }

    pub fn method(mut self, method: Method) -> Self {
        self.method = method;
        self
    }

    pub fn header(mut self, key: impl Into<String>, value: impl Into<String>) -> Self {
        self.headers.insert(key.into(), value.into());
        self
    }

    pub fn body(mut self, body: impl Into<Vec<u8>>) -> Self {
        self.body = Some(body.into());
        self
    }

    pub fn build(self) -> Result<Request, BuildError> {
        let url = self.url.ok_or(BuildError::MissingUrl)?;
        Ok(Request {
            url,
            method: self.method,
            headers: self.headers,
            body: self.body,
            timeout: self.timeout,
        })
    }
}
```

### Newtype Pattern

```rust
// Type safety through newtype
#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub struct UserId(String);

impl UserId {
    pub fn new(id: impl Into<String>) -> Self {
        UserId(id.into())
    }

    pub fn as_str(&self) -> &str {
        &self.0
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub struct OrderId(String);

// Now these are different types - can't mix them up
fn get_user(id: UserId) -> Option<User> { /* ... */ }
fn get_order(id: OrderId) -> Option<Order> { /* ... */ }
```

### Testing

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_basic() {
        let result = add(2, 3);
        assert_eq!(result, 5);
    }

    #[test]
    fn test_with_result() -> Result<(), Box<dyn Error>> {
        let config = parse_config("valid config")?;
        assert_eq!(config.name, "test");
        Ok(())
    }

    #[test]
    #[should_panic(expected = "divide by zero")]
    fn test_panic() {
        divide(1, 0);
    }

    // Async tests with tokio
    #[tokio::test]
    async fn test_async_function() {
        let result = fetch_data("http://example.com").await;
        assert!(result.is_ok());
    }

    // Property-based testing with proptest
    use proptest::prelude::*;

    proptest! {
        #[test]
        fn test_parse_roundtrip(s in "[a-z]+") {
            let parsed = parse(&s)?;
            let serialized = serialize(&parsed);
            prop_assert_eq!(s, serialized);
        }
    }
}
```

## Anti-Patterns

### Avoid These Practices

```rust
// BAD: Unnecessary clone
fn process(items: &Vec<String>) {
    for item in items.clone() {  // Unnecessary allocation
        println!("{}", item);
    }
}

// GOOD: Iterate by reference
fn process(items: &[String]) {
    for item in items {
        println!("{}", item);
    }
}

// BAD: Using unwrap/expect in library code
fn parse_config(s: &str) -> Config {
    serde_json::from_str(s).unwrap()  // Panics on invalid input
}

// GOOD: Return Result and let caller handle errors
fn parse_config(s: &str) -> Result<Config, serde_json::Error> {
    serde_json::from_str(s)
}

// BAD: Excessive use of Rc<RefCell<T>>
struct Node {
    value: i32,
    children: Vec<Rc<RefCell<Node>>>,
}

// GOOD: Consider arena allocation or indices
struct Arena {
    nodes: Vec<Node>,
}
struct Node {
    value: i32,
    children: Vec<usize>,  // Indices into arena
}

// BAD: String concatenation in loops
fn build_message(parts: &[&str]) -> String {
    let mut result = String::new();
    for part in parts {
        result = result + part + ", ";  // Creates new String each iteration
    }
    result
}

// GOOD: Use push_str or collect
fn build_message(parts: &[&str]) -> String {
    parts.join(", ")
}

// BAD: Boxing errors unnecessarily
fn parse(s: &str) -> Result<Data, Box<dyn Error>> {
    // For libraries, use concrete error types
}

// GOOD: Use concrete error types in libraries
fn parse(s: &str) -> Result<Data, ParseError> {
    // thiserror for library errors, anyhow for applications
}

// BAD: Unsafe without justification
unsafe fn get_unchecked(slice: &[i32], index: usize) -> i32 {
    *slice.get_unchecked(index)
}

// GOOD: Safe by default, unsafe with clear invariants
fn get_unchecked(slice: &[i32], index: usize) -> i32 {
    // SAFETY: Caller must ensure index < slice.len()
    // Only use when bounds checking is a proven bottleneck
    debug_assert!(index < slice.len());
    unsafe { *slice.get_unchecked(index) }
}

// BAD: Ignoring must_use
let _ = fs::remove_file("temp.txt");  // Error silently ignored

// GOOD: Handle the result
fs::remove_file("temp.txt").ok();  // Explicitly ignore
// or
fs::remove_file("temp.txt")?;  // Propagate error
```
