---
name: axum
description: |
  Axum framework guardrails, patterns, and best practices for AI-assisted development.
  Use when working with Axum projects, or when the user mentions Axum framework.
  Provides Tower integration, async handlers, extractors, and type-safe routing guidelines.
license: MIT
metadata:
  author: samuel
  version: "1.0"
  category: framework
  language: rust
  extensions: ".rs"
---

# Axum Framework Guide

> Applies to: Axum 0.7+, Rust Web APIs, Microservices
> Complements: `.claude/skills/rust-guide/SKILL.md`

## Core Principles

1. **Tower-First**: Axum is built on Tower; embrace `Service`, `Layer`, and middleware composition
2. **Type-Safe Extraction**: Use compile-time extractors for request data -- no manual parsing
3. **Async Throughout**: All handlers are async; never block the Tokio runtime
4. **Modular Routing**: Compose routers with `merge` and `nest`; separate public from protected routes
5. **Structured Errors**: Implement `IntoResponse` for custom error types; return appropriate HTTP status codes

## Project Structure

```
myproject/
├── Cargo.toml
├── src/
│   ├── main.rs                # Entry point (thin: env, tracing, bind, serve)
│   ├── lib.rs                 # Module declarations
│   ├── config.rs              # Configuration loading (env-based)
│   ├── routes/
│   │   ├── mod.rs             # Router composition (create_router)
│   │   ├── users.rs           # User-related route definitions
│   │   └── health.rs          # Health check route
│   ├── handlers/
│   │   ├── mod.rs
│   │   └── users.rs           # Handler functions (thin: extract, call service, respond)
│   ├── models/
│   │   ├── mod.rs
│   │   └── user.rs            # Domain types, DTOs, validation
│   ├── services/
│   │   ├── mod.rs
│   │   └── user_service.rs    # Business logic layer
│   ├── repositories/
│   │   ├── mod.rs
│   │   └── user_repository.rs # Database access layer
│   ├── extractors/
│   │   ├── mod.rs
│   │   └── auth.rs            # Custom extractors (AuthUser, Claims)
│   ├── middleware/
│   │   ├── mod.rs
│   │   └── logging.rs         # Custom Tower middleware
│   └── errors/
│       ├── mod.rs
│       └── app_error.rs       # AppError enum + IntoResponse
├── tests/
│   └── integration_tests.rs
└── migrations/
```

**Architectural rules:**
- Handlers are thin: extract request data, call service, return response
- Services contain business logic; they call repositories
- Repositories handle database access only
- Models define domain types and DTOs with validation
- Errors are defined per-layer and composed with `#[from]`

## Dependencies (Cargo.toml)

```toml
[dependencies]
# Web framework
axum = { version = "0.7", features = ["macros"] }
axum-extra = { version = "0.9", features = ["typed-header"] }
tokio = { version = "1.0", features = ["full"] }
tower = { version = "0.4", features = ["full"] }
tower-http = { version = "0.5", features = ["cors", "trace", "compression-gzip"] }

# Serialization
serde = { version = "1.0", features = ["derive"] }
serde_json = "1.0"

# Database
sqlx = { version = "0.7", features = ["runtime-tokio", "postgres", "uuid", "chrono"] }

# Validation
validator = { version = "0.16", features = ["derive"] }

# Error handling
thiserror = "1.0"
anyhow = "1.0"

# Logging
tracing = "0.1"
tracing-subscriber = { version = "0.3", features = ["env-filter"] }

# Configuration
config = "0.14"
dotenvy = "0.15"

# Utilities
uuid = { version = "1.0", features = ["v4", "serde"] }
chrono = { version = "0.4", features = ["serde"] }

[dev-dependencies]
axum-test = "14.0"
mockall = "0.12"
```

## Application Entry Point

```rust
// src/main.rs
#[tokio::main]
async fn main() -> anyhow::Result<()> {
    dotenvy::dotenv().ok();

    tracing_subscriber::registry()
        .with(tracing_subscriber::EnvFilter::try_from_default_env()
            .unwrap_or_else(|_| "myproject=debug,tower_http=debug".into()))
        .with(tracing_subscriber::fmt::layer())
        .init();

    let config = config::Config::load()?;
    let pool = sqlx::PgPool::connect(&config.database_url).await?;
    sqlx::migrate!("./migrations").run(&pool).await?;

    let state = AppState::new(pool, config.clone());
    let app = routes::create_router(state);

    let addr = SocketAddr::from(([0, 0, 0, 0], config.port));
    tracing::info!("Starting server on {}", addr);

    let listener = tokio::net::TcpListener::bind(addr).await?;
    axum::serve(listener, app)
        .with_graceful_shutdown(shutdown_signal())
        .await?;

    Ok(())
}

async fn shutdown_signal() {
    tokio::signal::ctrl_c().await
        .expect("Failed to install CTRL+C signal handler");
    tracing::info!("Shutdown signal received");
}
```

## Routing

### Router Composition

```rust
// src/routes/mod.rs
pub fn create_router(state: AppState) -> Router {
    let cors = CorsLayer::new()
        .allow_origin(Any)
        .allow_methods(Any)
        .allow_headers(Any);

    let public_routes = Router::new()
        .route("/health", get(handlers::health::health_check))
        .route("/api/v1/auth/register", post(handlers::users::register))
        .route("/api/v1/auth/login", post(handlers::users::login));

    let protected_routes = Router::new()
        .route("/api/v1/users", get(handlers::users::list_users))
        .route("/api/v1/users/:id", get(handlers::users::get_user))
        .route("/api/v1/users/:id", put(handlers::users::update_user))
        .route("/api/v1/users/:id", delete(handlers::users::delete_user))
        .layer(middleware::from_fn_with_state(
            state.clone(),
            app_middleware::auth::auth_middleware,
        ));

    Router::new()
        .merge(public_routes)
        .merge(protected_routes)
        .layer(TraceLayer::new_for_http())
        .layer(CompressionLayer::new())
        .layer(cors)
        .with_state(state)
}
```

### Routing Rules

- Use `merge` for flat route composition; use `nest` for path-prefix grouping
- Apply authentication middleware only to protected route groups
- Layer order matters: outermost layer runs first (CORS, Tracing, then Compression)
- Always call `.with_state(state)` last, after all routes and layers

## Handlers

Handlers are async functions that receive extractors and return `impl IntoResponse`.

```rust
// src/handlers/users.rs
pub async fn register(
    State(state): State<AppState>,
    Json(dto): Json<CreateUserDto>,
) -> AppResult<(StatusCode, Json<AuthResponse>)> {
    let service = UserService::new(state.pool, state.config);
    let response = service.register(dto).await?;
    Ok((StatusCode::CREATED, Json(response)))
}

pub async fn list_users(
    State(state): State<AppState>,
    Query(pagination): Query<PaginationQuery>,
    _auth_user: AuthUser,
) -> AppResult<Json<Vec<UserResponse>>> {
    let service = UserService::new(state.pool, state.config);
    let users = service.list_users(pagination.page, pagination.per_page).await?;
    Ok(Json(users))
}
```

### Handler Rules

- Keep handlers under 15 lines; delegate logic to services
- Always validate input via extractors or explicit `.validate()` calls
- Use `AppResult<T>` (a type alias for `Result<T, AppError>`) as the return type
- Extract `AuthUser` even if unused (`_auth_user`) to enforce authentication
- Return appropriate status codes: `CREATED` for POST, `NO_CONTENT` for DELETE

## Extractors

### Built-in Extractors

| Extractor | Purpose | Example |
|-----------|---------|---------|
| `State(state)` | Shared application state | `State(state): State<AppState>` |
| `Json(body)` | JSON request body | `Json(dto): Json<CreateUserDto>` |
| `Path(id)` | URL path parameters | `Path(id): Path<Uuid>` |
| `Query(params)` | Query string parameters | `Query(q): Query<PaginationQuery>` |
| `Extension(ext)` | Request extensions | `Extension(user): Extension<User>` |

### Custom Extractor

```rust
// src/extractors/auth.rs
pub struct AuthUser {
    pub user_id: Uuid,
    pub email: String,
    pub role: String,
}

#[async_trait]
impl FromRequestParts<AppState> for AuthUser {
    type Rejection = AppError;

    async fn from_request_parts(
        parts: &mut Parts,
        state: &AppState,
    ) -> Result<Self, Self::Rejection> {
        let TypedHeader(Authorization(bearer)) = parts
            .extract::<TypedHeader<Authorization<Bearer>>>()
            .await
            .map_err(|_| AppError::Unauthorized("Missing authorization header".into()))?;

        let claims = verify_token(bearer.token(), &state.config.jwt_secret)?;

        Ok(AuthUser {
            user_id: claims.sub,
            email: claims.email,
            role: claims.role,
        })
    }
}
```

### Extractor Rules

- Implement `FromRequestParts` (not `FromRequest`) when you only need headers/state
- Use `FromRequest` only when you need the body (consumes it)
- Extractor order in function signatures matters: body-consuming extractors must be last
- Always return your `AppError` type as the `Rejection`

## State Management

```rust
#[derive(Clone)]
pub struct AppState {
    pub pool: sqlx::PgPool,
    pub config: Config,
}

impl AppState {
    pub fn new(pool: sqlx::PgPool, config: Config) -> Self {
        Self { pool, config }
    }
}
```

### State Rules

- `AppState` must implement `Clone` (Axum requirement)
- Use `sqlx::PgPool` directly (it is `Arc`-wrapped internally)
- For mutable shared state, wrap in `Arc<tokio::sync::RwLock<T>>`
- Avoid `std::sync::Mutex` in async state; use `tokio::sync::Mutex` or `RwLock`
- Keep state lean: connection pools, config, caches -- not request-scoped data

## Error Handling

```rust
// src/errors/app_error.rs
#[derive(Error, Debug)]
pub enum AppError {
    #[error("Not found: {0}")]
    NotFound(String),

    #[error("Bad request: {0}")]
    BadRequest(String),

    #[error("Unauthorized: {0}")]
    Unauthorized(String),

    #[error("Forbidden: {0}")]
    Forbidden(String),

    #[error("Conflict: {0}")]
    Conflict(String),

    #[error("Validation error: {0}")]
    Validation(String),

    #[error("Internal server error")]
    Internal(#[from] anyhow::Error),

    #[error("Database error")]
    Database(#[from] sqlx::Error),
}

impl IntoResponse for AppError {
    fn into_response(self) -> Response {
        let (status, message) = match &self {
            AppError::NotFound(msg) => (StatusCode::NOT_FOUND, msg.clone()),
            AppError::BadRequest(msg) => (StatusCode::BAD_REQUEST, msg.clone()),
            AppError::Unauthorized(msg) => (StatusCode::UNAUTHORIZED, msg.clone()),
            AppError::Forbidden(msg) => (StatusCode::FORBIDDEN, msg.clone()),
            AppError::Conflict(msg) => (StatusCode::CONFLICT, msg.clone()),
            AppError::Validation(msg) => (StatusCode::UNPROCESSABLE_ENTITY, msg.clone()),
            AppError::Internal(err) => {
                tracing::error!("Internal error: {:?}", err);
                (StatusCode::INTERNAL_SERVER_ERROR, "Internal server error".into())
            }
            AppError::Database(err) => {
                tracing::error!("Database error: {:?}", err);
                (StatusCode::INTERNAL_SERVER_ERROR, "Database error".into())
            }
        };

        let body = Json(json!({
            "success": false,
            "error": { "code": status.as_u16(), "message": message }
        }));

        (status, body).into_response()
    }
}

pub type AppResult<T> = Result<T, AppError>;
```

### Error Handling Rules

- Always implement `IntoResponse` for your error type
- Never leak internal details (database errors, stack traces) to clients
- Log internal/database errors with `tracing::error!` before mapping to generic messages
- Use `thiserror` for enum definitions; `anyhow` for internal propagation
- Define `AppResult<T>` alias at the crate level for consistency

## Middleware and Tower Integration

### Route-Level Middleware

```rust
// Apply auth middleware to a route group
let protected = Router::new()
    .route("/api/v1/users", get(list_users))
    .layer(middleware::from_fn_with_state(state.clone(), auth_middleware));
```

### Custom Middleware Function

```rust
pub async fn auth_middleware(
    State(state): State<AppState>,
    request: Request,
    next: Next,
) -> Result<Response, AppError> {
    let token = request.headers()
        .get(AUTHORIZATION)
        .and_then(|h| h.to_str().ok())
        .and_then(|h| h.strip_prefix("Bearer "))
        .ok_or_else(|| AppError::Unauthorized("Missing token".into()))?;

    verify_token(token, &state.config.jwt_secret)?;
    Ok(next.run(request).await)
}
```

### Tower Layers (tower-http)

```rust
// Common layers -- add in create_router
.layer(TraceLayer::new_for_http())           // Request/response logging
.layer(CompressionLayer::new())              // Gzip response compression
.layer(CorsLayer::new().allow_origin(Any))   // CORS headers
.layer(TimeoutLayer::new(Duration::from_secs(30)))  // Request timeout
```

### Middleware Rules

- Use `middleware::from_fn_with_state` for middleware needing `AppState`
- Use `middleware::from_fn` for stateless middleware
- Layer ordering: outermost layer executes first on request, last on response
- Always add `TimeoutLayer` to prevent slow requests from exhausting resources
- Use `TraceLayer` for observability in all environments

## Commands

```bash
# Development
cargo run                           # Start server
cargo watch -x run                  # Watch mode (requires cargo-watch)
RUST_LOG=debug cargo run            # With debug logging

# Build
cargo build --release               # Production build
cargo check                         # Fast type-check

# Quality
cargo fmt                           # Format code
cargo clippy -- -D warnings         # Lint with deny
cargo audit                         # Vulnerability check

# Testing
cargo test                          # All tests
cargo test --test integration_tests # Integration only

# Database
sqlx migrate run                    # Run migrations
sqlx migrate add create_users       # Create new migration
```

## Best Practices Summary

- **Extractors**: Use custom extractors for reusable validation; `FromRequestParts` for headers, `FromRequest` for body
- **Error Handling**: One `AppError` enum per service; implement `IntoResponse`; log internal errors, sanitize client messages
- **Performance**: Use connection pooling (SQLx), enable compression (tower-http), add timeouts, use async throughout
- **Testing**: Use `axum-test` for integration tests; mock repositories for unit tests; use a separate test database
- **Security**: Validate all inputs with `validator`; use parameterized queries (SQLx); never expose internal errors

## Advanced Topics

For detailed handler examples, database integration, authentication flows, WebSocket support, and testing patterns, see:

- [references/patterns.md](references/patterns.md) -- Full CRUD handlers, repository pattern, JWT auth, WebSocket, integration testing

## External References

- [Axum Documentation](https://docs.rs/axum)
- [Tower Documentation](https://docs.rs/tower)
- [Tokio Documentation](https://tokio.rs)
- [SQLx Documentation](https://docs.rs/sqlx)
- [Axum Examples](https://github.com/tokio-rs/axum/tree/main/examples)
