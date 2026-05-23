---
name: rust
description: Write Rust code following best practices. Use when developing Rust applications. Covers ownership, error handling, and async patterns.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Rust Development

## Project Structure

```
my-project/
├── Cargo.toml
├── src/
│   ├── main.rs
│   ├── lib.rs
│   └── handlers/
│       └── mod.rs
└── tests/
    └── integration.rs
```

## Error Handling

```rust
use thiserror::Error;

#[derive(Error, Debug)]
pub enum AppError {
    #[error("User not found: {0}")]
    NotFound(String),

    #[error("Database error: {0}")]
    Database(#[from] sqlx::Error),

    #[error("Validation error: {0}")]
    Validation(String),
}

// Using Result
async fn get_user(id: &str) -> Result<User, AppError> {
    let user = sqlx::query_as!(User, "SELECT * FROM users WHERE id = $1", id)
        .fetch_optional(&pool)
        .await?
        .ok_or_else(|| AppError::NotFound(id.to_string()))?;

    Ok(user)
}

// Using ? operator
fn process() -> Result<(), AppError> {
    let user = get_user("123")?;
    validate(&user)?;
    save(&user)?;
    Ok(())
}
```

## Ownership & Borrowing

```rust
// Ownership transfer
fn take_ownership(s: String) {
    println!("{}", s);
} // s is dropped here

// Borrowing (immutable)
fn borrow(s: &String) {
    println!("{}", s);
}

// Mutable borrowing
fn mutate(s: &mut String) {
    s.push_str(" world");
}

// Lifetimes
fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
    if x.len() > y.len() { x } else { y }
}
```

## Async with Tokio

```rust
use tokio;

#[tokio::main]
async fn main() {
    let result = fetch_data().await;
}

async fn fetch_all(urls: Vec<String>) -> Vec<Response> {
    let futures: Vec<_> = urls
        .into_iter()
        .map(|url| tokio::spawn(async move { fetch(&url).await }))
        .collect();

    let results = futures::future::join_all(futures).await;
    results.into_iter().filter_map(|r| r.ok()).collect()
}
```

## Axum Web Handler

```rust
use axum::{
    extract::{Path, State},
    http::StatusCode,
    Json,
};

async fn get_user(
    State(pool): State<PgPool>,
    Path(id): Path<String>,
) -> Result<Json<User>, (StatusCode, String)> {
    let user = sqlx::query_as!(User, "SELECT * FROM users WHERE id = $1", id)
        .fetch_optional(&pool)
        .await
        .map_err(|e| (StatusCode::INTERNAL_SERVER_ERROR, e.to_string()))?
        .ok_or((StatusCode::NOT_FOUND, "User not found".to_string()))?;

    Ok(Json(user))
}
```

## Testing

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_validation() {
        let result = validate("valid@email.com");
        assert!(result.is_ok());
    }

    #[tokio::test]
    async fn test_async_operation() {
        let result = fetch_data().await;
        assert!(result.is_ok());
    }
}
```

## Tooling

```bash
# Format
cargo fmt

# Lint
cargo clippy -- -D warnings

# Test
cargo test

# Build release
cargo build --release
```
