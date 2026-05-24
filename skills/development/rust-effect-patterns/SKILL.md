---
name: rust-effect-patterns
description: Translating Effect-TS patterns to Rust idioms. Result/Option handling, error propagation, service architecture, and effectful computation patterns. Use when implementing functional error handling, building Effect-like abstractions in Rust, or translating Effect-TS concepts. Trigger phrases include "Result", "Option", "thiserror", "anyhow", "Effect in Rust", "functional error handling", or "Railway-Oriented Programming".
---

# Rust Effect Patterns

## Overview

This skill translates Effect-TS architectural patterns to Rust idioms, focusing on functional error handling, service composition, and effect-like computation. While Rust doesn't have Effect runtime, it provides powerful primitives (`Result`, `Option`, trait systems) that achieve similar goals through different mechanisms.

**Key capabilities:**
- Railway-Oriented Programming with `Result<T, E>`
- Optional values with `Option<T>` and combinators
- Structured error handling with `thiserror` and `anyhow`
- Service-like patterns with traits and dependency injection
- Async effect composition with `tokio` and `futures`

## Canonical Sources

**TMNL Codebase:**
- `.edin/EFFECT_PATTERNS.md` — Effect-TS service patterns (conceptual reference)
- `src-ava/` — Rust domain code with thiserror usage
- AVA Cargo workspace — Structured error handling patterns

**Rust Ecosystem:**
- `thiserror` — Derive macro for custom error types (https://docs.rs/thiserror)
- `anyhow` — Dynamic error handling (https://docs.rs/anyhow)
- `tokio` — Async runtime (https://docs.rs/tokio)
- `futures` — Async combinators (https://docs.rs/futures)

**Conceptual References:**
- Effect-TS services → Rust traits with associated types
- Effect.Service<>() → Trait + struct implementations
- Context.Tag → Dependency injection via generics
- Layer composition → Trait bounds and `impl Trait`

## Pattern 1: Result<T, E> — The Effect.Effect Equivalent

### Basic Result Usage

**Effect-TS:**
```typescript
const operation = Effect.gen(function* () {
  const config = yield* ConfigService;
  return yield* Effect.try(() => doThing(config));
});
```

**Rust Equivalent:**
```rust
fn operation() -> Result<String, MyError> {
    let config = load_config()?;
    do_thing(&config)
}

// Or with Result::map for transformations
fn operation() -> Result<i32, MyError> {
    load_config()
        .and_then(|config| do_thing(&config))
        .map(|result| result.len() as i32)
}
```

**Pattern:** Use `?` operator for short-circuit error propagation (Effect's `yield*`).

### Result Combinators (Effect Chain Equivalent)

| Effect-TS | Rust Result |
|-----------|-------------|
| `Effect.map(f)` | `.map(f)` |
| `Effect.flatMap(f)` | `.and_then(f)` |
| `Effect.catchAll(f)` | `.or_else(f)` |
| `Effect.tapError(f)` | `.map_err(f)` |
| `Effect.ensuring(fin)` | N/A — use RAII/Drop |

**Example:**
```rust
use std::fs;

fn read_user_config(path: &str) -> Result<Config, ConfigError> {
    fs::read_to_string(path)
        .map_err(ConfigError::from)  // Effect.mapError
        .and_then(|content| parse_config(&content))  // Effect.flatMap
        .or_else(|_| load_default_config())  // Effect.catchAll
}
```

## Pattern 2: Option<T> — Optional Values

**Effect-TS:**
```typescript
const maybeValue = Option.fromNullable(value);
const result = pipe(
  maybeValue,
  Option.map((v) => v.toString()),
  Option.getOrElse(() => "default")
);
```

**Rust Equivalent:**
```rust
let maybe_value = Some(value);  // or None
let result = maybe_value
    .map(|v| v.to_string())
    .unwrap_or_else(|| "default".to_string());

// Or with ? operator (requires function returning Option)
fn process(input: Option<i32>) -> Option<String> {
    let value = input?;  // Short-circuit if None
    Some(value.to_string())
}
```

**Pattern:** `Option<T>` is Rust's built-in Maybe monad, use `?` for short-circuiting.

## Pattern 3: Error Types — thiserror vs anyhow

### Decision Tree

```
Need custom error type?
│
├─ Library code / Public API?
│  └─ Use: thiserror (transparent errors)
│     Example: AVA domain errors
│
├─ Application code / Internal?
│  ├─ Need rich context?
│  │  └─ Use: anyhow (dynamic errors)
│  │     Example: CLI tools, app logic
│  │
│  └─ Need type safety?
│     └─ Use: thiserror
│
└─ Propagating errors from dependencies?
   └─ Use: anyhow::Result<T>
```

### thiserror — Structured Custom Errors

**Use when:** Library code, public APIs, need specific error variants.

```rust
use thiserror::Error;

#[derive(Error, Debug)]
pub enum ConfigError {
    #[error("Configuration file not found: {path}")]
    NotFound { path: String },

    #[error("Invalid configuration format")]
    InvalidFormat(#[from] serde_json::Error),

    #[error("Missing required field: {0}")]
    MissingField(String),

    #[error(transparent)]
    IoError(#[from] std::io::Error),
}

fn load_config(path: &str) -> Result<Config, ConfigError> {
    let content = std::fs::read_to_string(path)
        .map_err(|_| ConfigError::NotFound {
            path: path.to_string(),
        })?;

    let config: Config = serde_json::from_str(&content)?;  // Auto-converts via #[from]
    validate_config(&config)?;
    Ok(config)
}
```

**Key Features:**
- `#[error("...")]` — Display message with interpolation
- `#[from]` — Auto-conversion from source error type
- `#[source]` — Error chain for `std::error::Error::source()`
- `#[transparent]` — Forward Display/Debug to wrapped error

**TMNL Example:** See `src-ava/ava-domain/src/errors.rs` for AVA domain errors.

### anyhow — Dynamic Error Handling

**Use when:** Application code, rapid prototyping, need context chains.

```rust
use anyhow::{Context, Result};

fn process_user(id: u64) -> Result<User> {
    let db = connect_database()
        .context("Failed to connect to database")?;

    let user = db.find_user(id)
        .with_context(|| format!("User {} not found", id))?;

    validate_user(&user)
        .context("User validation failed")?;

    Ok(user)
}
```

**Key Features:**
- `Result<T>` is alias for `Result<T, anyhow::Error>`
- `.context("...")` — Add contextual information
- `.with_context(|| ...)` — Lazy context (only evaluated on error)
- Automatic error chain preservation

**Pattern:** Use `anyhow` for application entrypoints, `thiserror` for reusable libraries.

## Pattern 4: Service Patterns — Traits as Effect Services

### Effect.Service<>() in Rust

**Effect-TS:**
```typescript
class MyService extends Effect.Service<MyService>()("app/MyService", {
  effect: Effect.gen(function* () {
    const config = yield* ConfigService;
    const doThing = (input: string) => Effect.succeed(input.length);
    return { doThing } as const;
  }),
  dependencies: [ConfigService.Default],
}) {}
```

**Rust Equivalent (Trait + Impl):**
```rust
// Service interface (the "Tag")
pub trait MyService {
    fn do_thing(&self, input: &str) -> Result<usize, MyError>;
}

// Service implementation
pub struct MyServiceImpl {
    config: Config,
}

impl MyServiceImpl {
    pub fn new(config: Config) -> Self {
        Self { config }
    }
}

impl MyService for MyServiceImpl {
    fn do_thing(&self, input: &str) -> Result<usize, MyError> {
        // Use self.config for logic
        Ok(input.len())
    }
}

// Usage (dependency injection via generics)
fn use_service<S: MyService>(service: &S, input: &str) -> Result<usize, MyError> {
    service.do_thing(input)
}
```

**Pattern:** Trait defines interface, struct holds state, impl provides behavior.

### Dependency Injection via Traits

**Effect-TS Layer composition:**
```typescript
const AppLayer = Layer.mergeAll(
  ConfigService.Default,
  DatabaseService.Default,
  ApiService.Default
);
```

**Rust Equivalent (Generic bounds):**
```rust
pub struct AppContext<C, D, A>
where
    C: ConfigService,
    D: DatabaseService,
    A: ApiService,
{
    config: C,
    database: D,
    api: A,
}

impl<C, D, A> AppContext<C, D, A>
where
    C: ConfigService,
    D: DatabaseService,
    A: ApiService,
{
    pub fn new(config: C, database: D, api: A) -> Self {
        Self { config, database, api }
    }

    pub fn run(&self) -> Result<(), AppError> {
        let db_url = self.config.database_url()?;
        self.database.connect(&db_url)?;
        self.api.start()?;
        Ok(())
    }
}
```

**Pattern:** Generic type parameters + trait bounds = Effect Layer dependencies.

### Alternative: Trait Objects (Dynamic Dispatch)

```rust
pub struct AppContext {
    config: Box<dyn ConfigService>,
    database: Box<dyn DatabaseService>,
}

impl AppContext {
    pub fn new(
        config: Box<dyn ConfigService>,
        database: Box<dyn DatabaseService>,
    ) -> Self {
        Self { config, database }
    }
}
```

**Trade-off:**
- **Generics**: Static dispatch, monomorphization, no runtime overhead
- **Trait objects**: Dynamic dispatch, single code path, runtime indirection

**Prefer generics** unless you need runtime polymorphism (plugin systems, config-driven behavior).

## Pattern 5: Async Effects — Effect.Effect → async/await

### Basic Async Pattern

**Effect-TS:**
```typescript
const fetchUser = (id: number): Effect.Effect<User, FetchError> =>
  Effect.tryPromise({
    try: () => fetch(`/api/users/${id}`).then(r => r.json()),
    catch: (error) => new FetchError({ cause: error }),
  });
```

**Rust Equivalent:**
```rust
use tokio;

async fn fetch_user(id: u64) -> Result<User, FetchError> {
    let url = format!("https://api.example.com/users/{}", id);
    let response = reqwest::get(&url)
        .await
        .map_err(FetchError::from)?;

    let user: User = response.json()
        .await
        .map_err(FetchError::from)?;

    Ok(user)
}

// Usage
#[tokio::main]
async fn main() -> Result<(), FetchError> {
    let user = fetch_user(42).await?;
    println!("{:?}", user);
    Ok(())
}
```

**Pattern:** `async fn` returns `Future<Output = Result<T, E>>`, use `.await?` for propagation.

### Combining Async Results

**Effect-TS:**
```typescript
const parallel = Effect.all([fetchUser(1), fetchUser(2), fetchUser(3)]);
const sequential = Effect.gen(function* () {
  const user1 = yield* fetchUser(1);
  const user2 = yield* fetchUser(2);
  return [user1, user2];
});
```

**Rust Parallel:**
```rust
use futures::future;

async fn fetch_multiple_parallel(ids: &[u64]) -> Result<Vec<User>, FetchError> {
    let futures = ids.iter().map(|&id| fetch_user(id));
    future::try_join_all(futures).await
}
```

**Rust Sequential:**
```rust
async fn fetch_multiple_sequential(ids: &[u64]) -> Result<Vec<User>, FetchError> {
    let mut users = Vec::new();
    for &id in ids {
        users.push(fetch_user(id).await?);
    }
    Ok(users)
}
```

**Combinators:**
- `try_join!` — Parallel execution, fail-fast
- `try_join_all` — Dynamic parallel (Vec of futures)
- Sequential — Use `for` loop with `.await?`

## Pattern 6: Effect Streams → Rust Streams

**Effect-TS:**
```typescript
const stream = Stream.fromIterable([1, 2, 3])
  .pipe(
    Stream.map((n) => n * 2),
    Stream.filter((n) => n > 2),
    Stream.runCollect
  );
```

**Rust Equivalent (futures crate):**
```rust
use futures::stream::{self, StreamExt};

async fn process_stream() -> Vec<i32> {
    stream::iter(vec![1, 2, 3])
        .map(|n| n * 2)
        .filter(|&n| futures::future::ready(n > 2))
        .collect::<Vec<_>>()
        .await
}
```

**Rust Equivalent (tokio channels for concurrency):**
```rust
use tokio::sync::mpsc;

async fn process_events() -> Result<(), MyError> {
    let (tx, mut rx) = mpsc::channel(100);

    // Producer
    tokio::spawn(async move {
        for i in 1..=10 {
            tx.send(i).await.unwrap();
        }
    });

    // Consumer
    while let Some(event) = rx.recv().await {
        println!("Received: {}", event);
    }

    Ok(())
}
```

**Pattern:** Use `futures::stream` for sync-like streams, `tokio::sync::mpsc` for async channels.

## Pattern 7: Context Propagation — Effect Context → Generic Bounds

**Effect-TS:**
```typescript
const withContext = Effect.gen(function* () {
  const logger = yield* Logger;
  const db = yield* Database;

  yield* logger.info("Starting query");
  return yield* db.query("SELECT * FROM users");
});
```

**Rust Equivalent:**
```rust
async fn with_context<L, D>(logger: &L, db: &D) -> Result<Vec<User>, DbError>
where
    L: Logger,
    D: Database,
{
    logger.info("Starting query").await;
    db.query("SELECT * FROM users").await
}

// Or with Arc for shared state
use std::sync::Arc;

async fn with_context_shared(
    logger: Arc<dyn Logger>,
    db: Arc<dyn Database>,
) -> Result<Vec<User>, DbError> {
    logger.info("Starting query").await;
    db.query("SELECT * FROM users").await
}
```

**Pattern:** Pass services explicitly as parameters, use `Arc<dyn Trait>` for shared ownership.

## Pattern 8: Railway-Oriented Programming

### Early Return Pattern

```rust
fn process_order(order_id: u64) -> Result<Receipt, OrderError> {
    let order = find_order(order_id)?;  // Early return on error

    if !order.is_valid() {
        return Err(OrderError::Invalid);
    }

    let payment = process_payment(&order)?;
    let shipment = schedule_shipment(&order)?;

    Ok(Receipt {
        order_id: order.id,
        payment_id: payment.id,
        tracking: shipment.tracking_number,
    })
}
```

### Combinator Chain Pattern

```rust
fn process_order_functional(order_id: u64) -> Result<Receipt, OrderError> {
    find_order(order_id)
        .and_then(validate_order)
        .and_then(process_payment)
        .and_then(schedule_shipment)
        .map(|shipment| Receipt::from(shipment))
}
```

**Pattern:** Use `?` for imperative style, combinators for functional style.

## TMNL Integration

### Tauri Command Error Handling

```rust
use serde::Serialize;

#[derive(Debug, thiserror::Error)]
pub enum TauriError {
    #[error("File not found: {0}")]
    FileNotFound(String),

    #[error("Permission denied")]
    PermissionDenied,

    #[error(transparent)]
    IoError(#[from] std::io::Error),
}

// Tauri requires errors to be String or serializable
impl Serialize for TauriError {
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: serde::Serializer,
    {
        serializer.serialize_str(&self.to_string())
    }
}

#[tauri::command]
async fn read_config(path: String) -> Result<Config, TauriError> {
    let content = tokio::fs::read_to_string(&path)
        .await
        .map_err(|_| TauriError::FileNotFound(path))?;

    let config: Config = serde_json::from_str(&content)
        .map_err(|e| TauriError::IoError(e.into()))?;

    Ok(config)
}
```

**Pattern:** Use `thiserror` for domain errors, implement `Serialize` for Tauri IPC.

### AVA Domain Error Example

```rust
// From src-ava/ava-domain/
use thiserror::Error;

#[derive(Error, Debug)]
pub enum DomainError {
    #[error("Entity not found: {entity_type} with id {id}")]
    NotFound {
        entity_type: String,
        id: String,
    },

    #[error("Validation failed: {0}")]
    ValidationError(String),

    #[error("Business rule violation: {0}")]
    BusinessRuleViolation(String),

    #[error(transparent)]
    DatabaseError(#[from] sqlx::Error),
}

pub type DomainResult<T> = Result<T, DomainError>;
```

**Pattern:** Domain-specific error types with `thiserror`, type aliases for Result.

## Testing Effect-Like Patterns

### Result Testing

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_success_path() {
        let result = process_order(42);
        assert!(result.is_ok());
        let receipt = result.unwrap();
        assert_eq!(receipt.order_id, 42);
    }

    #[test]
    fn test_error_path() {
        let result = process_order(999);
        assert!(result.is_err());
        match result.unwrap_err() {
            OrderError::NotFound => {},
            _ => panic!("Expected NotFound error"),
        }
    }
}
```

### Async Testing

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[tokio::test]
    async fn test_async_fetch() {
        let result = fetch_user(1).await;
        assert!(result.is_ok());
    }

    #[tokio::test]
    async fn test_parallel_fetch() {
        let users = fetch_multiple_parallel(&[1, 2, 3]).await;
        assert_eq!(users.unwrap().len(), 3);
    }
}
```

## Anti-Patterns

### 1. Unwrap in Production Code

**WRONG:**
```rust
fn read_file(path: &str) -> String {
    std::fs::read_to_string(path).unwrap()  // Panics on error!
}
```

**RIGHT:**
```rust
fn read_file(path: &str) -> Result<String, std::io::Error> {
    std::fs::read_to_string(path)
}
```

### 2. Mixing anyhow and thiserror Incorrectly

**WRONG:**
```rust
// Library code returning anyhow::Error
pub fn parse_config(input: &str) -> anyhow::Result<Config> {
    // Loses type information for callers
}
```

**RIGHT:**
```rust
// Library code with specific error type
pub fn parse_config(input: &str) -> Result<Config, ConfigError> {
    // Callers can match on specific variants
}
```

### 3. Ignoring Error Context

**WRONG:**
```rust
let config = load_config(path).map_err(|_| "Failed to load config")?;
```

**RIGHT:**
```rust
let config = load_config(path)
    .with_context(|| format!("Failed to load config from {}", path))?;
```

### 4. Overusing ? Without Propagation Path

**WRONG:**
```rust
fn main() {
    let result = process()?;  // main can't return Result by default
    println!("{:?}", result);
}
```

**RIGHT:**
```rust
fn main() -> anyhow::Result<()> {
    let result = process()?;
    println!("{:?}", result);
    Ok(())
}
```

## Quick Reference

### Error Handling Cheat Sheet

| Effect-TS | Rust |
|-----------|------|
| `Effect.succeed(x)` | `Ok(x)` |
| `Effect.fail(e)` | `Err(e)` |
| `Effect.try(() => x)` | `fn() -> Result<T, E>` |
| `yield*` | `?` operator |
| `Effect.map(f)` | `.map(f)` |
| `Effect.flatMap(f)` | `.and_then(f)` |
| `Effect.catchAll(f)` | `.or_else(f)` |
| `Effect.mapError(f)` | `.map_err(f)` |
| `Effect.option` | `.ok()` |

### Common Result Combinators

```rust
// Transform success value
result.map(|x| x * 2)

// Chain dependent operations
result.and_then(|x| do_thing(x))

// Provide default on error
result.or_else(|_| Ok(default_value))

// Transform error type
result.map_err(|e| MyError::from(e))

// Convert to Option
result.ok()

// Unwrap with custom panic message
result.expect("Operation failed")
```

## Further Reading

- **Rust Book**: [Error Handling](https://doc.rust-lang.org/book/ch09-00-error-handling.html)
- **thiserror docs**: https://docs.rs/thiserror
- **anyhow docs**: https://docs.rs/anyhow
- **Railway-Oriented Programming**: https://fsharpforfunandprofit.com/rop/
- **TMNL Effect Patterns**: `.edin/EFFECT_PATTERNS.md`
