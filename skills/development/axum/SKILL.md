---
name: axum
description: |
  Production patterns for Axum 0.8 + SQLx. Covers State design, error handling, transactions, testing, and SQLx CLI usage.
  Use when: building Rust APIs with Axum, integrating error types, handling transactions, setting up tests, or SQLx CLI issues.
  Delegate to: database-engineer agent for schema design, migrations SQL content, and query optimization.
versions: Axum 0.8+, SQLx 0.8+, Rust 1.75+
---

# Axum + SQLx Skill

Production patterns for using Axum 0.8 with SQLx.

**For syntax and API details, use Context7:** `/tokio-rs/axum`, `/launchbadge/sqlx`

---

## Quick Start

```bash
cargo new my-api && cd my-api
cargo add axum tokio -F tokio/full
cargo add sqlx -F sqlx/runtime-tokio,sqlx/postgres,sqlx/uuid,sqlx/chrono
cargo add serde -F serde/derive
cargo add tower-http -F tower-http/cors,tower-http/trace
cargo add thiserror
```

```bash
# SQLx CLI
cargo install sqlx-cli --no-default-features -F postgres

# Migration setup
sqlx database create
sqlx migrate add create_users
sqlx migrate run
```

---

## Project Structure

```
my-api/
├── Cargo.toml
├── .env                     # DATABASE_URL
├── .sqlx/                   # Offline query cache (commit this)
├── migrations/              # SQL files (content by database-engineer)
└── src/
    ├── main.rs
    ├── config.rs
    ├── error.rs             # Unified error type
    ├── db.rs                # Pool setup
    └── users/
        ├── mod.rs
        ├── router.rs
        ├── handlers.rs
        ├── models.rs
        └── service.rs
```

---

## Core Patterns

### State + Pool Setup

```rust
use sqlx::postgres::PgPoolOptions;
use sqlx::PgPool;

// PgPool is already Arc internally - don't wrap in another Arc
#[derive(Clone)]
pub struct AppState {
    pub db: PgPool,
}

pub async fn create_pool(database_url: &str) -> Result<PgPool, sqlx::Error> {
    PgPoolOptions::new()
        .max_connections(10)
        .acquire_timeout(std::time::Duration::from_secs(3))
        .connect(database_url)
        .await
}
```

### Router Setup (Axum 0.8 Syntax)

```rust
pub fn router() -> Router<AppState> {
    Router::new()
        .route("/", get(list_users).post(create_user))
        .route("/{id}", get(get_user).put(update_user).delete(delete_user))
}
```

**Critical:** Axum 0.8 uses `{id}` not `:id` for path parameters.

### Unified Error Type

```rust
#[derive(thiserror::Error, Debug)]
pub enum AppError {
    #[error("not found")]
    NotFound,
    #[error("conflict: {0}")]
    Conflict(String),
    #[error("bad request: {0}")]
    BadRequest(String),
    #[error("database error")]
    Database(#[from] sqlx::Error),
}

#[derive(Serialize)]
struct ErrorBody {
    error: String,
}

impl IntoResponse for AppError {
    fn into_response(self) -> Response {
        let (status, message) = match &self {
            AppError::NotFound => (StatusCode::NOT_FOUND, self.to_string()),
            AppError::Conflict(msg) => (StatusCode::CONFLICT, msg.clone()),
            AppError::BadRequest(msg) => (StatusCode::BAD_REQUEST, msg.clone()),
            AppError::Database(e) => {
                if let sqlx::Error::RowNotFound = e {
                    (StatusCode::NOT_FOUND, "not found".to_string())
                } else if e.as_database_error().is_some_and(|e| e.is_unique_violation()) {
                    (StatusCode::CONFLICT, "already exists".to_string())
                } else {
                    tracing::error!("Database error: {:?}", e);
                    (StatusCode::INTERNAL_SERVER_ERROR, "internal error".to_string())
                }
            }
        };
        (status, Json(ErrorBody { error: message })).into_response()
    }
}
```

### Transaction Pattern

```rust
pub async fn create_user_with_profile(
    State(state): State<AppState>,
    Json(input): Json<CreateUserInput>,
) -> Result<Json<User>, AppError> {
    let mut tx = state.db.begin().await?;

    let user = sqlx::query_as!(User,
        "INSERT INTO users (id, email, name) VALUES ($1, $2, $3) RETURNING id, email, name",
        Uuid::new_v4(), input.email, input.name
    )
    .fetch_one(&mut *tx)  // Note: &mut *tx
    .await?;

    sqlx::query!("INSERT INTO profiles (user_id, bio) VALUES ($1, $2)", user.id, input.bio)
        .execute(&mut *tx)
        .await?;

    tx.commit().await?;
    Ok(Json(user))
}
```

**Key point:** Use `&mut *tx` to dereference the transaction.

---

## SQLx-Specific Patterns

> **Schema changes?** Delegate to `database-engineer` agent for migration SQL content, index design, and query optimization.

### Compile-Time Query Checking & Offline Mode

SQLx validates queries at compile time. For CI/CD without DB access:

```bash
# Generate offline cache locally (with DB access)
cargo sqlx prepare

# Commit .sqlx/ directory
git add .sqlx/

# In CI
SQLX_OFFLINE=true cargo build
```

### Type Mapping Gotchas

Common mappings that cause issues:

| Postgres | Rust | Gotcha |
|----------|------|--------|
| `UUID` | `uuid::Uuid` | Needs `sqlx/uuid` feature |
| `TIMESTAMPTZ` | `chrono::DateTime<Utc>` | Needs `sqlx/chrono` feature |
| `JSONB` | `serde_json::Value` | Needs `sqlx/json` feature |
| Nullable column | `Option<T>` | Mismatch = runtime error |

### Migrations (CLI Only)

```bash
sqlx migrate add create_users   # Create file
sqlx migrate run                # Run pending
sqlx migrate revert             # Revert last
sqlx migrate info               # Check status
```

**For migration SQL content, delegate to `database-engineer` agent.**

---

## Common Errors & Fixes

### Pool Exhausted / Timeout

**Symptom:** Requests hang or timeout.

**Fix:**
```rust
PgPoolOptions::new()
    .max_connections(10)
    .acquire_timeout(Duration::from_secs(3))  // Fail fast
    .idle_timeout(Duration::from_secs(600))
```

**Check:** Holding transactions too long? Awaiting all queries?

### DATABASE_URL Not Set (Compile Error)

**Fix for CI:**
```bash
cargo sqlx prepare              # Run locally first
SQLX_OFFLINE=true cargo build   # In CI
```

### fetch_one vs fetch_optional

```rust
// fetch_one - errors if no rows (RowNotFound)
// fetch_optional - returns None if no rows
// fetch_all - returns empty vec if no rows
```

**Rule:** Use `fetch_optional` for lookups, `fetch_one` only when row must exist.

### Migration Checksum Error

**Cause:** Migration file modified after running.

**Fix:** Never modify applied migrations. Create a new migration instead.

---

## Testing

Use `#[sqlx::test]` for automatic transaction isolation and rollback:

```rust
#[sqlx::test]
async fn test_create_user(pool: PgPool) {
    let user = create_user(&pool, "test@example.com", "Test").await.unwrap();
    assert_eq!(user.email, "test@example.com");
    // Automatically rolled back - no cleanup needed
}
```

### Integration Test with Axum

```rust
use axum::{body::Body, http::{Request, StatusCode}};
use tower::ServiceExt;

#[tokio::test]
async fn test_list_users() {
    let pool = setup_test_db().await;
    let app = create_app(AppState { db: pool });

    let response = app
        .oneshot(Request::builder().uri("/api/users").body(Body::empty()).unwrap())
        .await
        .unwrap();

    assert_eq!(response.status(), StatusCode::OK);
}
```

---

## Critical Rules

### Always

- Use `fetch_optional` for single-row lookups
- Map `sqlx::Error` to appropriate HTTP status codes
- Use `&mut *tx` when passing transaction to queries
- Commit `.sqlx/` directory for offline builds
- Run `cargo sqlx prepare` before CI/CD

### Never

- Wrap `PgPool` in `Arc` (already Arc internally)
- Modify migrations after applied
- Use `fetch_one` when row might not exist
- Hold transactions longer than necessary
- Use `:id` in Axum 0.8 routes (use `{id}`)
