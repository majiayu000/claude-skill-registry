---
name: rust-crate
description: Work with Rust crates in the Traceway workspace — add types, implement storage backends, or extend the daemon. Use when modifying Rust code.
metadata:
  author: traceway
  version: "1.0.0"
---

# Working with Rust Crates

Use this skill when the user asks to modify Rust code, add types, implement storage backends, or extend the daemon.

## Workspace layout

```
crates/
├── trace/              # Core types (Span, Trace, SpanKind, EvalRun) — foundational, no deps on other crates
├── storage/            # StorageBackend trait + in-memory SpanStore
├── storage-sqlite/     # SQLite backend (local/dev default)
├── storage-postgres/   # Postgres backend (cloud mode)
├── storage-turbopuffer/# Turbopuffer vector search (secondary index)
├── auth/               # JWT + API key middleware for Axum
├── daemon/             # Binary (traceway) — wires storage, API, auth, OTLP ingest
└── memfs/              # FUSE filesystem — SKIP (needs macFUSE)
```

## Adding a new type to `trace`

All shared types live in `crates/trace/src/lib.rs`. Follow these patterns:

```rust
use serde::{Deserialize, Serialize};
use utoipa::ToSchema;
use uuid::Uuid;

pub type MyEntityId = Uuid;

#[derive(Debug, Clone, Serialize, Deserialize, ToSchema)]
pub struct MyEntity {
    id: MyEntityId,
    name: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    description: Option<String>,
}

// Private fields with read-only accessors
impl MyEntity {
    pub fn id(&self) -> MyEntityId { self.id }
    pub fn name(&self) -> &str { &self.name }
}
```

Key patterns:
- Derive `Serialize`, `Deserialize`, `ToSchema` on all public types
- Use `#[serde(skip_serializing_if = "Option::is_none")]` for optional fields
- Private fields with public accessor methods (immutability guarantee)
- `SpanKind` is a tagged enum: `#[serde(tag = "type", rename_all = "snake_case")]`
- UUIDv7 for time-sortable IDs: `Uuid::now_v7()`

## Implementing a StorageBackend

The `StorageBackend` trait in `crates/storage/src/lib.rs` defines the interface:

```rust
#[async_trait]
pub trait StorageBackend: Send + Sync {
    async fn span(&self, id: SpanId) -> Result<Option<Span>>;
    async fn create_span(&mut self, span: Span) -> Result<SpanId>;
    async fn complete_span(&mut self, id: SpanId, output: Value) -> Result<()>;
    async fn fail_span(&mut self, id: SpanId, error: String) -> Result<()>;
    async fn spans(&self, filter: &SpanFilter) -> Result<Vec<Span>>;
    async fn trace(&self, id: TraceId) -> Result<Option<Vec<Span>>>;
    // ... more methods
}
```

## Error handling

Use `thiserror` — never `unwrap()` in production paths:

```rust
#[derive(Debug, thiserror::Error)]
pub enum MyError {
    #[error("not found: {0}")]
    NotFound(String),
    #[error("database error: {0}")]
    Database(#[from] sqlx::Error),
    #[error("serialization error: {0}")]
    Serde(#[from] serde_json::Error),
}
```

## Logging

Use the `tracing` crate, never `println!`:

```rust
tracing::info!("Starting processing");
tracing::warn!(id = %entity_id, "Entity not found in cache");
tracing::error!(error = %e, "Failed to persist span");
```

## Async patterns

Everything is async on Tokio runtime:

```rust
use tokio::sync::RwLock;
use std::sync::Arc;

let store = Arc::new(RwLock::new(backend));

// Read lock
let guard = store.read().await;
let span = guard.span(id).await?;

// Write lock
let mut guard = store.write().await;
guard.create_span(span).await?;
```

## Build commands

```bash
# Check specific crates (skip memfs — needs macFUSE)
cargo check -p trace -p storage -p daemon

# Build daemon (local mode)
cargo build -p daemon

# Build daemon (cloud mode with Postgres)
cargo build -p daemon --features cloud

# Run daemon
cargo run -p daemon -- --foreground

# Format
cargo fmt

# Lint
cargo clippy -p trace -p storage -p daemon
```

## Key conventions

- **No unwrap()** in production paths — use `?` or proper error handling
- **Async everywhere** — Tokio runtime
- **Private fields** with read-only accessors for core types
- **SpanBuilder** for construction, `.complete(output)` / `.fail(error)` consume spans
- **UUIDv7** for time-sortable IDs
- **409 Conflict** when modifying terminal spans
- **New public types** need `Serialize`/`Deserialize`/`ToSchema`
- **Skip memfs** — it needs macFUSE which may not be installed

## After modifying Rust code

1. Run check: `cargo check -p trace -p storage -p daemon`
2. Run clippy: `cargo clippy -p trace -p storage -p daemon`
3. Format: `cargo fmt`
