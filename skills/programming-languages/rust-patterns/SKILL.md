---
name: rust-patterns
description: Rust backend patterns including Axum, Tokio, error handling with anyhow/thiserror, and tracing.
agents: [rex]
triggers: [rust, axum, tokio, cargo, clippy]
---

# Rust Backend Patterns

Production Rust patterns for backend services using Axum, Tokio, and the broader Rust ecosystem.

## Core Stack

| Component | Library | Purpose |
|-----------|---------|---------|
| Language | Rust (Edition 2021+) | Systems programming |
| Build | Cargo | Package management and build |
| Linting | Clippy pedantic | Code quality |
| Formatting | rustfmt | Code formatting |
| Async | Tokio | Async runtime |
| Error Handling | anyhow + thiserror | Application/library errors |
| Serialization | Serde | JSON/YAML/etc |
| Logging | tracing | Structured logging |
| HTTP | Axum | Web framework |

## Context7 Library IDs

Query these libraries for current best practices:

- **Tokio**: `/websites/rs_tokio_tokio`
- **Serde**: `/websites/serde_rs`
- **Anyhow**: `/dtolnay/anyhow`
- **Thiserror**: `/dtolnay/thiserror`
- **Tracing**: `/tokio-rs/tracing`
- **Clippy**: `/rust-lang/rust-clippy`
- **Axum**: `/tokio-rs/axum`

## Execution Rules

1. **Clippy pedantic always.** Run with `-W clippy::pedantic`
2. **No unwrap in production.** Use `?` or proper error handling
3. **Type safety.** Leverage Rust's type system fully
4. **Documentation.** Doc comments on all public items
5. **Tests.** Unit tests alongside code, integration tests in `tests/`

## Error Handling Patterns

### Application Errors with anyhow

```rust
use anyhow::{Context, Result};

fn do_thing() -> Result<()> {
    let data = fetch_data()
        .context("failed to fetch data")?;
    process(data)
        .context("failed to process")?;
    Ok(())
}
```

### Library Errors with thiserror

```rust
use thiserror::Error;

#[derive(Error, Debug)]
pub enum ServiceError {
    #[error("user not found: {id}")]
    UserNotFound { id: String },
    
    #[error("validation failed: {0}")]
    Validation(String),
    
    #[error(transparent)]
    Database(#[from] sqlx::Error),
}
```

## Async Patterns with Tokio

### Basic Async

```rust
use tokio::time::{sleep, Duration};

async fn poll_until_ready() -> Result<Data> {
    loop {
        if let Some(data) = check_status().await? {
            return Ok(data);
        }
        sleep(Duration::from_secs(1)).await;
    }
}
```

### Concurrent Operations

```rust
use tokio::try_join;

async fn fetch_all() -> Result<(User, Posts)> {
    let (user, posts) = try_join!(
        fetch_user(),
        fetch_posts()
    )?;
    Ok((user, posts))
}
```

### Channels for Coordination

```rust
use tokio::sync::mpsc;

async fn worker(mut rx: mpsc::Receiver<Job>) {
    while let Some(job) = rx.recv().await {
        process(job).await;
    }
}
```

## Structured Logging with tracing

```rust
use tracing::{info, warn, instrument, span, Level};

#[instrument(skip(secret))]
fn process_request(id: &str, secret: &str) {
    info!(request_id = %id, "processing request");
}

// Manual spans
fn complex_operation() {
    let span = span!(Level::INFO, "complex_op");
    let _enter = span.enter();
    
    info!("starting operation");
    // ... work ...
    info!("completed operation");
}
```

## Axum Web Framework

### Basic Route Setup

```rust
use axum::{Router, routing::{get, post}, extract::State, Json};

async fn create_app(db: Database) -> Router {
    Router::new()
        .route("/health", get(health_check))
        .route("/users", post(create_user))
        .with_state(AppState { db })
}

async fn health_check() -> &'static str {
    "ok"
}

async fn create_user(
    State(state): State<AppState>,
    Json(req): Json<CreateUserRequest>,
) -> Result<Json<User>, AppError> {
    let user = state.db.create_user(req).await?;
    Ok(Json(user))
}
```

### Custom Error Type for Axum

```rust
use axum::{response::IntoResponse, http::StatusCode};

struct AppError(anyhow::Error);

impl IntoResponse for AppError {
    fn into_response(self) -> axum::response::Response {
        (
            StatusCode::INTERNAL_SERVER_ERROR,
            format!("Something went wrong: {}", self.0),
        ).into_response()
    }
}

impl<E> From<E> for AppError where E: Into<anyhow::Error> {
    fn from(err: E) -> Self {
        Self(err.into())
    }
}
```

## Validation Commands

```bash
cargo fmt --all -- --check
cargo clippy --workspace --all-targets --all-features -- -D warnings -W clippy::pedantic
cargo test --workspace --all-features
cargo build --release
```

## Guidelines

- Use `tracing` for logging, never `println!`
- Handle errors with `anyhow` context
- Keep functions small and focused
- Write doc comments on all public items
- Prefer `?` over explicit match for error propagation
- Use `#[must_use]` on functions returning values
