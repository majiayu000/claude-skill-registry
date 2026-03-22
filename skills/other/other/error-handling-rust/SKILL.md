---
name: error-handling-rust
description: >
  Implement idiomatic Rust error handling with Result, Option, and the ? operator.
  Use when the user handles errors in Rust, creates custom error types, uses
  thiserror or anyhow, implements the From trait for error conversion, or asks
  about Result/Option patterns and error composition strategies.
---

# Rust Error Handling

Handle errors idiomatically in Rust using Result, Option, the `?` operator,
and well-structured custom error types for robust, composable error propagation.

## When to Use
- Designing error types for a library or application
- Propagating errors with the ? operator
- Converting between error types with From
- Choosing between thiserror (libraries) and anyhow (applications)
- Handling Option and Result in method chains

## Core Patterns

### Pattern 1: Result and the ? Operator

Use `Result<T, E>` for operations that can fail. The `?` operator unwraps
success or returns the error early.

```rust
use std::fs;
use std::io;

fn read_config(path: &str) -> Result<Config, io::Error> {
    let content = fs::read_to_string(path)?;  // returns Err early if fails
    let config: Config = serde_json::from_str(&content)
        .map_err(|e| io::Error::new(io::ErrorKind::InvalidData, e))?;
    Ok(config)
}

// Chain multiple fallible operations
fn process_file(path: &str) -> Result<Summary, AppError> {
    let content = fs::read_to_string(path)?;    // io::Error -> AppError via From
    let data = parse_data(&content)?;            // ParseError -> AppError via From
    let summary = analyze(&data)?;               // AnalyzeError -> AppError via From
    Ok(summary)
}
```

### Pattern 2: Custom Error Types with thiserror

Use `thiserror` for library error types with automatic Display and From implementations.

```rust
use thiserror::Error;

#[derive(Debug, Error)]
pub enum StorageError {
    #[error("item not found: {id}")]
    NotFound { id: String },

    #[error("duplicate key: {key}")]
    DuplicateKey { key: String },

    #[error("connection failed after {attempts} attempts")]
    ConnectionFailed { attempts: u32 },

    #[error("serialization error")]
    Serialization(#[from] serde_json::Error),

    #[error("I/O error")]
    Io(#[from] std::io::Error),
}

// Usage
fn get_item(id: &str) -> Result<Item, StorageError> {
    let data = fs::read_to_string(format!("data/{id}.json"))?; // auto-converts io::Error
    let item: Item = serde_json::from_str(&data)?;              // auto-converts serde error
    Ok(item)
}
```

### Pattern 3: anyhow for Applications

Use `anyhow` in application code where you need flexible error context
without defining custom types for every error.

```rust
use anyhow::{Context, Result, bail, ensure};

fn load_config(path: &str) -> Result<Config> {
    let content = fs::read_to_string(path)
        .with_context(|| format!("failed to read config from {path}"))?;

    let config: Config = toml::from_str(&content)
        .context("invalid TOML in config file")?;

    ensure!(config.port > 0, "port must be positive, got {}", config.port);

    if config.workers == 0 {
        bail!("worker count must be at least 1");
    }

    Ok(config)
}

// anyhow errors display the full context chain:
// "failed to read config from app.toml: No such file or directory (os error 2)"
```

### Pattern 4: Option Handling

Use `Option<T>` for values that may be absent. Combine with combinators
for clean, chainable logic.

```rust
fn find_user_email(users: &HashMap<u64, User>, id: u64) -> Option<String> {
    users
        .get(&id)                          // Option<&User>
        .filter(|u| u.is_active)           // None if not active
        .and_then(|u| u.email.as_deref())  // Option<&str>
        .map(|e| e.to_lowercase())         // Option<String>
}

// Convert Option to Result with context
fn get_required_header(headers: &HeaderMap, name: &str) -> Result<&str, AppError> {
    headers
        .get(name)
        .and_then(|v| v.to_str().ok())
        .ok_or_else(|| AppError::MissingHeader(name.to_string()))
}

// unwrap_or, unwrap_or_default, unwrap_or_else
let port = config.port.unwrap_or(8080);
let name = user.nickname.unwrap_or_default(); // uses Default trait
let conn = pool.get().unwrap_or_else(|| create_new_connection());
```

### Pattern 5: Implementing From for Error Conversion

The `?` operator uses `From` to convert errors. Implement it manually when
thiserror's `#[from]` is not flexible enough.

```rust
#[derive(Debug)]
pub enum AppError {
    Database(String),
    Validation(String),
    External(Box<dyn std::error::Error + Send + Sync>),
}

impl std::fmt::Display for AppError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            AppError::Database(msg) => write!(f, "database error: {msg}"),
            AppError::Validation(msg) => write!(f, "validation error: {msg}"),
            AppError::External(err) => write!(f, "external error: {err}"),
        }
    }
}

impl std::error::Error for AppError {}

impl From<sqlx::Error> for AppError {
    fn from(err: sqlx::Error) -> Self {
        AppError::Database(err.to_string())
    }
}

impl From<std::io::Error> for AppError {
    fn from(err: std::io::Error) -> Self {
        AppError::External(Box::new(err))
    }
}
```

### Pattern 6: Error Composition Across Layers

Structure errors by layer: domain errors at the core, infrastructure
errors at the edges, conversion between layers at boundaries.

```rust
// Domain layer -- pure business errors
#[derive(Debug, Error)]
pub enum DomainError {
    #[error("insufficient funds: need {required}, have {available}")]
    InsufficientFunds { required: u64, available: u64 },

    #[error("account {0} is frozen")]
    AccountFrozen(String),
}

// Infrastructure layer -- wraps external crate errors
#[derive(Debug, Error)]
pub enum InfraError {
    #[error("database error")]
    Db(#[from] sqlx::Error),

    #[error("cache error")]
    Cache(#[from] redis::RedisError),
}

// Application layer -- combines both
#[derive(Debug, Error)]
pub enum AppError {
    #[error(transparent)]
    Domain(#[from] DomainError),

    #[error(transparent)]
    Infra(#[from] InfraError),
}

// Each layer uses ? with its own error type.
// Boundaries convert with From implementations.
```

## Anti-Patterns

- **Using `unwrap()` in production code** -- Panics on None/Err. Use `?`, `expect()`,
  or combinators. Reserve `unwrap()` for tests and provably-safe cases.

- **Stringly-typed errors** -- `Result<T, String>` loses type information. Define proper
  error enums even for simple cases.
  ```rust
  // BAD
  fn parse(s: &str) -> Result<Data, String> {
      Err(format!("invalid: {s}"))
  }
  // GOOD
  fn parse(s: &str) -> Result<Data, ParseError> { ... }
  ```

- **Ignoring errors with `let _ =`** -- Explicitly handle or log. If truly ignorable,
  add a comment explaining why.

- **`Box<dyn Error>` in library code** -- Libraries should expose concrete error types
  so consumers can match on variants. Use `Box<dyn Error>` only in application code
  or use `anyhow`.

- **Mixing thiserror and anyhow in libraries** -- Use thiserror for public error types
  in libraries; anyhow is for application-level convenience.

## Quick Reference

| Crate | Use In | Purpose |
|-------|--------|---------|
| thiserror | Libraries | Derive Error, Display, From |
| anyhow | Applications | Flexible context, bail!, ensure! |

| Method | Purpose |
|--------|---------|
| `?` | Propagate error, convert via From |
| `.context("msg")` | Add context (anyhow) |
| `.map_err(fn)` | Transform error type |
| `.ok_or(err)` | Option -> Result |
| `.ok_or_else(fn)` | Option -> Result (lazy) |
| `.unwrap_or(val)` | Provide default for Option/Result |

Rule of thumb: libraries use `thiserror`, applications use `anyhow`.
