---
name: axum
description: |
  Axum 0.8+ production patterns with SQLx.
  Use when: setup or building Rust APIs, async database, error handling.
  Do not use for: API design decisions (use api-design skill).
  Workflow: api-design (design) → this skill (implementation).
references:
  - examples.md
---

# Axum + SQLx

**For latest APIs, use context7.**

---

## Core Philosophy

Axum is built on **Tower** - a composable middleware stack.

```
Request → [Layer₁ → Layer₂ → ... → Handler] → Response
```

Everything is a **Service** (request → response). Layers wrap services to add behavior. This enables:
- Reusable middleware
- Type-safe composition
- Zero-cost abstractions

```rust
// Each layer wraps the inner service, forming a pipeline
Router::new()
    .route("/users/{id}", get(get_user))
    .layer(CompressionLayer::new())   // Layer 3: outermost
    .layer(TimeoutLayer::new(...))    // Layer 2
    .layer(TraceLayer::new_for_http()) // Layer 1: innermost
```

---

## Project Structure

```
src/
├── main.rs
├── lib.rs             # AppState, re-exports
├── error.rs           # AppError (RFC 9457)
├── extractors.rs      # Db, ValidatedJson
├── response.rs        # Created<T>, Ok<T>
└── features/
    └── users/
        ├── mod.rs
        ├── router.rs
        ├── handlers.rs
        └── models.rs  # Entity + repository
migrations/
.sqlx/                 # Commit this
```

---

## Abstractions

### Response Types

```rust
async fn create(...) -> Result<Created<User>, AppError>  // 201
async fn get(...) -> Result<Ok<User>, AppError>          // 200
async fn delete(...) -> Result<NoContent, AppError>      // 204
```

### Db Extractor

```rust
async fn handler(Db(db): Db, Path(id): Path<Uuid>) -> Result<Ok<User>, AppError>
```

### Repository

```rust
User::find_or_404(&db, id).await?
User::create(&db, input).await?
```

---

## Decision Guide

### Query Method

| Situation | Method |
|-----------|--------|
| Must exist | `fetch_one` |
| May not exist | `fetch_optional` → `.ok_or(AppError::NotFound)` |
| List | `fetch_all` |

### Transaction Scope

Keep transactions short. No external calls inside tx.

```rust
// ✅ External call outside tx
let external = api.call().await?;
let mut tx = db.begin().await?;
// DB only
tx.commit().await?;
```

### Pool Config

```rust
PgPoolOptions::new()
    .max_connections(10)
    .acquire_timeout(Duration::from_secs(3))  // Required
```

---

## Security

| Item | Value |
|------|-------|
| Password | argon2id (64MB) |
| JWT access | 15-30 min |
| JWT refresh | 90 days (web), 1 year (mobile) |
| CORS | Explicit origins |

---

## Checklist

- [ ] Response types (`Created`, `Ok`, `NoContent`)
- [ ] RFC 9457 error responses
- [ ] `Db` extractor
- [ ] Repository pattern
- [ ] Tower layers for cross-cutting concerns
- [ ] `acquire_timeout` set
- [ ] using compile time query check. and `.sqlx/` must be committed
