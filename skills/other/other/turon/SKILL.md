---
name: turon-api-design
description: Write Rust code in the style of Aaron Turon, former Rust team lead. Emphasizes API design, async Rust, and ecosystem architecture. Use when designing public APIs, async systems, or library interfaces.
---

# Aaron Turon Style Guide

## Overview

Aaron Turon led Rust's design and ecosystem efforts, shaping async/await, the API guidelines, and Rust's library ecosystem. His focus: APIs that are a pleasure to use and hard to misuse.

## Core Philosophy

> "APIs should be hard to use incorrectly."

> "Async Rust should feel like sync Rust."

Turon believes in **designing APIs from the user's perspective**. The best API is one where the obvious thing to do is the right thing to do.

## Design Principles

1. **User-First Design**: Design APIs by writing the code you wish you had.

2. **Pit of Success**: Make correct usage easy and incorrect usage hard.

3. **Consistency**: Follow Rust conventions—users shouldn't have to learn new patterns.

4. **Async Parity**: Async code should mirror sync code as much as possible.

## When Writing Code

### Always

- Follow the [Rust API Guidelines](https://rust-lang.github.io/api-guidelines/)
- Use standard naming conventions (`new`, `with_`, `into_`, `as_`)
- Implement standard traits (`Debug`, `Clone`, `Default` where sensible)
- Make illegal states unrepresentable
- Design with `?` operator in mind

### Never

- Surprise users with non-obvious behavior
- Require users to remember initialization order
- Mix async and blocking code without clear boundaries
- Create APIs that compile but do the wrong thing

### Prefer

- Builders for complex construction
- Type state for state machines
- `impl Trait` for return types in public APIs
- Extension traits for adding methods to foreign types

## Code Patterns

### User-First API Design

```rust
// Step 1: Write the code you wish you had
fn ideal_usage() {
    let client = HttpClient::new();
    
    let response = client
        .get("https://api.example.com/users")
        .header("Authorization", "Bearer token")
        .send()?;
    
    let users: Vec<User> = response.json()?;
}

// Step 2: Design API to make that code work
pub struct HttpClient { /* ... */ }

impl HttpClient {
    pub fn new() -> Self { /* ... */ }
    
    pub fn get(&self, url: &str) -> RequestBuilder {
        RequestBuilder::new(Method::GET, url)
    }
}

pub struct RequestBuilder { /* ... */ }

impl RequestBuilder {
    pub fn header(mut self, key: &str, value: &str) -> Self {
        self.headers.insert(key, value);
        self
    }
    
    pub fn send(self) -> Result<Response, Error> {
        // ...
    }
}
```

### Type State Pattern

```rust
// Compile-time state machine: impossible to misuse

// State types (zero-sized, no runtime cost)
pub struct Unconnected;
pub struct Connected;
pub struct Authenticated;

pub struct Connection<State> {
    inner: TcpStream,
    state: PhantomData<State>,
}

impl Connection<Unconnected> {
    pub fn new(stream: TcpStream) -> Self {
        Connection { inner: stream, state: PhantomData }
    }
    
    pub fn connect(self) -> Result<Connection<Connected>, Error> {
        // Perform connection handshake
        Ok(Connection { inner: self.inner, state: PhantomData })
    }
}

impl Connection<Connected> {
    pub fn authenticate(self, creds: &Credentials) 
        -> Result<Connection<Authenticated>, Error> 
    {
        // Perform authentication
        Ok(Connection { inner: self.inner, state: PhantomData })
    }
}

impl Connection<Authenticated> {
    pub fn query(&mut self, sql: &str) -> Result<Results, Error> {
        // Only authenticated connections can query
    }
}

// Usage: Compiler enforces correct order
let conn = Connection::new(stream)
    .connect()?
    .authenticate(&creds)?;

conn.query("SELECT * FROM users")?;

// This won't compile:
// let conn = Connection::new(stream);
// conn.query("...");  // ERROR: no method `query` on Connection<Unconnected>
```

### Async/Await Design

```rust
use std::future::Future;

// Async functions mirror sync functions
pub async fn fetch_user(id: u64) -> Result<User, Error> {
    let response = client.get(&format!("/users/{}", id)).send().await?;
    let user = response.json().await?;
    Ok(user)
}

// Async traits (with async-trait or native in future Rust)
#[async_trait]
pub trait Repository {
    async fn find(&self, id: u64) -> Result<Entity, Error>;
    async fn save(&self, entity: &Entity) -> Result<(), Error>;
}

// Returning futures from sync functions
pub fn spawn_fetch(id: u64) -> impl Future<Output = Result<User, Error>> {
    async move {
        fetch_user(id).await
    }
}

// Graceful cancellation
pub async fn fetch_with_timeout(
    id: u64, 
    timeout: Duration
) -> Result<User, Error> {
    tokio::time::timeout(timeout, fetch_user(id))
        .await
        .map_err(|_| Error::Timeout)?
}
```

### Extension Traits

```rust
// Add methods to types you don't own

pub trait ResultExt<T, E> {
    /// Log the error and convert to Option
    fn log_err(self) -> Option<T>
    where
        E: std::fmt::Display;
    
    /// Provide context for the error
    fn context(self, msg: &'static str) -> Result<T, ContextError<E>>;
}

impl<T, E> ResultExt<T, E> for Result<T, E> {
    fn log_err(self) -> Option<T>
    where
        E: std::fmt::Display,
    {
        match self {
            Ok(v) => Some(v),
            Err(e) => {
                log::error!("{}", e);
                None
            }
        }
    }
    
    fn context(self, msg: &'static str) -> Result<T, ContextError<E>> {
        self.map_err(|e| ContextError { context: msg, source: e })
    }
}

// Usage
let data = read_file(path).context("failed to read config")?;
let parsed = parse(data).log_err();
```

### Implementing Standard Traits

```rust
/// A user in the system.
///
/// Implements common traits for ease of use.
#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub struct User {
    id: u64,
    name: String,
    email: String,
}

impl User {
    pub fn new(id: u64, name: impl Into<String>, email: impl Into<String>) -> Self {
        User {
            id,
            name: name.into(),
            email: email.into(),
        }
    }
}

// Implement Display for user-facing output
impl std::fmt::Display for User {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{} <{}>", self.name, self.email)
    }
}

// Implement Default if there's a sensible default
impl Default for Config {
    fn default() -> Self {
        Config {
            timeout: Duration::from_secs(30),
            retries: 3,
            verbose: false,
        }
    }
}
```

## Mental Model

Turon designs APIs by asking:

1. **What will users write?** Start with usage, not implementation.
2. **Can they get it wrong?** If so, make wrong usage a compile error.
3. **Is it consistent?** Does it feel like idiomatic Rust?
4. **Is it discoverable?** Can users find what they need?

## API Guidelines Highlights

| Guideline | Example |
|-----------|---------|
| `new` for constructors | `Vec::new()` |
| `with_` for alternate constructors | `Vec::with_capacity(10)` |
| `into_` for conversions consuming self | `String::into_bytes()` |
| `as_` for cheap reference conversions | `str::as_bytes()` |
| `to_` for expensive conversions | `str::to_uppercase()` |
| `is_` for boolean queries | `Option::is_some()` |
| `_mut` suffix for mutable variants | `slice::iter_mut()` |

