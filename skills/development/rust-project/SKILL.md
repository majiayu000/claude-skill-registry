---
name: rust-project
description: Modern Rust project architecture guide for 2025. Use when creating Rust projects (CLI, web services, libraries). Covers workspace structure, error handling, async patterns, and idiomatic Rust best practices.
---
# Rust Project Architecture

## Core Principles

- **Ownership-first** — Embrace borrow checker, no unnecessary clones
- **Zero-cost abstractions** — Newtype, iterators, async/await
- **Workspace for scale** — Use Cargo workspace for multi-crate projects
- **Error precision** — thiserror for libs, anyhow for apps
- **Async with Tokio** — Tokio runtime + tracing for observability
- **No backwards compatibility** — Delete, don't deprecate. Change directly
- **LiteLLM for LLM APIs** — Use LiteLLM proxy for all LLM integrations

---

## No Backwards Compatibility

> **Delete unused code. Change directly. No compatibility layers.**

```rust
// ❌ BAD: Deprecated attribute kept around
#[deprecated(since = "0.2.0", note = "Use new_function instead")]
pub fn old_function() { ... }

// ❌ BAD: Type alias for renamed types
pub type OldName = NewName; // "for backwards compatibility"

// ❌ BAD: Unused parameters
fn process(_legacy: &str, data: &Data) { ... }

// ❌ BAD: Feature flags for old behavior
#[cfg(feature = "legacy")]
fn old_impl() { ... }

// ✅ GOOD: Just delete and update all usages
pub fn new_function() { ... }
// Then: Find & replace all old_function → new_function

// ✅ GOOD: Remove unused parameters entirely
fn process(data: &Data) { ... }
```

---

## LiteLLM for LLM APIs

> **Use LiteLLM proxy. Don't call provider APIs directly.**

```rust
// src/llm.rs
use async_openai::{Client, config::OpenAIConfig};

pub fn create_client(base_url: &str, api_key: &str) -> Client<OpenAIConfig> {
    let config = OpenAIConfig::new()
        .with_api_base(base_url)  // LiteLLM proxy URL
        .with_api_key(api_key);
    Client::with_config(config)
}

// Usage: connect to LiteLLM, use any model
let client = create_client("http://localhost:4000", &api_key);
let request = CreateChatCompletionRequestArgs::default()
    .model("gpt-4o")  // or "claude-3-opus", "gemini-pro", etc.
    .messages(vec![...])
    .build()?;
```

---

## Quick Start

### 1. Initialize Project

```bash
# Simple project
cargo new myapp
cd myapp

# Workspace project
mkdir myapp && cd myapp
cargo init --name app
```

### 2. Apply Tech Stack

| Layer | Recommendation |
|-------|----------------|
| Async Runtime | Tokio |
| Web Framework | Axum |
| Serialization | Serde |
| ORM / Database | SeaORM (async, Active Record) |
| CLI | Clap (derive) |
| Error (lib) | thiserror |
| Error (app) | anyhow |
| Logging | tracing + tracing-subscriber |
| HTTP Client | reqwest |
| Config | config-rs |

### Web Framework Selection

| Framework | Choose When |
|-----------|-------------|
| **Axum** (default) | Modern microservices, Tokio ecosystem, container deployment, Tower middleware |
| Actix Web | Maximum throughput, WebSocket-heavy, mature ecosystem needed |
| Rocket | Rapid prototyping, small teams, minimal boilerplate |

> Axum provides the best balance of performance, ergonomics, and Tokio integration for most projects.

### Database / ORM Selection

| Library | Choose When |
|---------|-------------|
| **SeaORM** (default) | CRUD-heavy services, rapid development, async-first, cross-database testing |
| SQLx | Raw SQL control, maximum performance, compile-time SQL validation |
| Diesel | Compile-time type safety, stable schema, synchronous workloads |

> SeaORM is recommended for its Active Record ergonomics, native async support, and seamless Axum integration.

### Version Strategy

> **Always use latest. Never pin in templates.**

```toml
[dependencies]
tokio = { version = "*", features = ["full"] }
axum = "*"
serde = { version = "*", features = ["derive"] }

# cargo update fetches latest compatible versions
# Cargo.lock ensures reproducible builds
```

### 3. Choose Project Structure

#### Simple Project (Single Crate)

```
myapp/
├── Cargo.toml
├── src/
│   ├── main.rs           # Entry point
│   ├── lib.rs            # Library root (optional)
│   ├── config.rs         # Configuration
│   ├── error.rs          # Error types
│   ├── handlers/         # HTTP handlers (web)
│   │   └── mod.rs
│   ├── services/         # Business logic
│   │   └── mod.rs
│   └── models/           # Domain types
│       └── mod.rs
├── tests/                # Integration tests
│   └── api_test.rs
└── benches/              # Benchmarks
    └── bench.rs
```

#### Workspace Project (Multi-Crate)

```
myapp/
├── Cargo.toml            # Workspace manifest
├── crates/
│   ├── app/              # Binary crate
│   │   ├── Cargo.toml
│   │   └── src/main.rs
│   ├── core/             # Business logic lib
│   │   ├── Cargo.toml
│   │   └── src/lib.rs
│   └── infra/            # Infrastructure lib
│       ├── Cargo.toml
│       └── src/lib.rs
├── config/
│   └── default.toml
└── Makefile
```

---

## Architecture Layers

### main.rs — Entry Point

Wire dependencies, start runtime. No business logic.

```rust
// src/main.rs
use anyhow::Result;
use sea_orm::Database;
use tracing_subscriber::{layer::SubscriberExt, util::SubscriberInitExt};

#[tokio::main]
async fn main() -> Result<()> {
    // Initialize tracing
    tracing_subscriber::registry()
        .with(tracing_subscriber::fmt::layer())
        .init();

    // Load config
    let config = myapp::config::load()?;

    // Connect to database (SeaORM)
    let db = Database::connect(&config.database_url).await?;

    // Build application state
    let state = myapp::AppState::new(db);

    // Build router
    let app = myapp::router::build(state);

    // Run server
    let listener = tokio::net::TcpListener::bind(&config.listen_addr).await?;
    tracing::info!("listening on {}", config.listen_addr);
    axum::serve(listener, app).await?;

    Ok(())
}
```

### lib.rs — Library Root

Re-export public API, define AppState.

```rust
// src/lib.rs
pub mod config;
pub mod db;
pub mod error;
pub mod handlers;
pub mod models;  // SeaORM entities
pub mod router;
pub mod services;

use sea_orm::DatabaseConnection;
use std::sync::Arc;

pub struct AppState {
    pub db: DatabaseConnection,
}

impl AppState {
    pub fn new(db: DatabaseConnection) -> Arc<Self> {
        Arc::new(Self { db })
    }
}
```

### error.rs — Error Handling

```rust
// src/error.rs
use axum::{http::StatusCode, response::{IntoResponse, Response}, Json};
use sea_orm::DbErr;
use serde_json::json;

#[derive(Debug, thiserror::Error)]
pub enum AppError {
    #[error("not found: {0}")]
    NotFound(String),

    #[error("validation error: {0}")]
    Validation(String),

    #[error("unauthorized")]
    Unauthorized,

    #[error("internal error")]
    Internal(#[from] anyhow::Error),

    #[error("database error: {0}")]
    Database(#[from] DbErr),
}

impl IntoResponse for AppError {
    fn into_response(self) -> Response {
        let (status, message) = match &self {
            AppError::NotFound(msg) => (StatusCode::NOT_FOUND, msg.clone()),
            AppError::Validation(msg) => (StatusCode::BAD_REQUEST, msg.clone()),
            AppError::Unauthorized => (StatusCode::UNAUTHORIZED, "unauthorized".into()),
            AppError::Internal(_) | AppError::Database(_) => {
                tracing::error!("Internal error: {:?}", self);
                (StatusCode::INTERNAL_SERVER_ERROR, "internal error".into())
            }
        };

        (status, Json(json!({ "error": message }))).into_response()
    }
}

pub type Result<T> = std::result::Result<T, AppError>;
```

### handlers/ — HTTP Layer

```rust
// src/handlers/user.rs
use axum::{extract::{Path, State}, Json};
use std::sync::Arc;
use crate::{error::Result, models::user, services, AppState};

pub async fn get_user(
    State(state): State<Arc<AppState>>,
    Path(id): Path<i64>,
) -> Result<Json<user::Model>> {
    let user = services::user::find_by_id(&state.db, id).await?;
    Ok(Json(user))
}

pub async fn create_user(
    State(state): State<Arc<AppState>>,
    Json(input): Json<CreateUserInput>,
) -> Result<Json<user::Model>> {
    let user = services::user::create(&state.db, input).await?;
    Ok(Json(user))
}
```

### services/ — Business Logic

```rust
// src/services/user.rs
use sea_orm::{ActiveModelTrait, DatabaseConnection, EntityTrait, Set};
use crate::{error::{AppError, Result}, models::user};

pub async fn find_by_id(db: &DatabaseConnection, id: i64) -> Result<user::Model> {
    user::Entity::find_by_id(id)
        .one(db)
        .await?
        .ok_or_else(|| AppError::NotFound(format!("user {}", id)))
}

pub async fn create(db: &DatabaseConnection, input: CreateUserInput) -> Result<user::Model> {
    let new_user = user::ActiveModel {
        email: Set(input.email),
        name: Set(input.name),
        ..Default::default()
    };

    let user = new_user.insert(db).await?;
    Ok(user)
}

// Find with relations
pub async fn find_with_posts(db: &DatabaseConnection, id: i64) -> Result<(user::Model, Vec<post::Model>)> {
    user::Entity::find_by_id(id)
        .find_with_related(post::Entity)
        .all(db)
        .await?
        .into_iter()
        .next()
        .ok_or_else(|| AppError::NotFound(format!("user {}", id)))
}
```

---

## Workspace Configuration

```toml
# Cargo.toml (workspace root)
[workspace]
resolver = "3"
members = ["crates/*"]

[workspace.package]
version = "0.1.0"
edition = "2024"
license = "MIT"

[workspace.dependencies]
tokio = { version = "*", features = ["full"] }
axum = "*"
serde = { version = "*", features = ["derive"] }
serde_json = "*"
sea-orm = { version = "*", features = ["sqlx-postgres", "runtime-tokio-native-tls"] }
thiserror = "*"
anyhow = "*"
tracing = "*"
tracing-subscriber = "*"
```

```toml
# crates/app/Cargo.toml
[package]
name = "app"
version.workspace = true
edition.workspace = true

[dependencies]
core.path = "../core"
infra.path = "../infra"
tokio.workspace = true
axum.workspace = true
anyhow.workspace = true
tracing.workspace = true
tracing-subscriber.workspace = true
```

---

## CLI Application

```rust
// src/main.rs
use clap::Parser;
use anyhow::Result;

#[derive(Parser)]
#[command(name = "myapp", version, about)]
struct Cli {
    /// Input file path
    #[arg(short, long)]
    input: PathBuf,

    /// Output format
    #[arg(short, long, default_value = "json")]
    format: OutputFormat,

    /// Verbose output
    #[arg(short, long)]
    verbose: bool,
}

#[derive(Clone, clap::ValueEnum)]
enum OutputFormat {
    Json,
    Yaml,
    Text,
}

fn main() -> Result<()> {
    let cli = Cli::parse();

    if cli.verbose {
        tracing_subscriber::fmt::init();
    }

    // Process input...
    Ok(())
}
```

---

## Testing

```rust
// tests/api_test.rs
use axum::{body::Body, http::{Request, StatusCode}};
use tower::ServiceExt;

#[tokio::test]
async fn test_get_user() {
    let app = create_test_app().await;

    let response = app
        .oneshot(
            Request::builder()
                .uri("/users/1")
                .body(Body::empty())
                .unwrap(),
        )
        .await
        .unwrap();

    assert_eq!(response.status(), StatusCode::OK);
}

// Unit test with mock
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_validate_email() {
        assert!(validate_email("test@example.com").is_ok());
        assert!(validate_email("invalid").is_err());
    }
}
```

---


## Extended Reference

Detailed material starting at `## Makefile` has been moved to [`reference/extended.md`](reference/extended.md) to keep this skill concise. Load that reference when the task requires the moved examples, command catalogs, checklists, platform details, or implementation templates.
