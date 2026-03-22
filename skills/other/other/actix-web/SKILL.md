---
name: actix-web
description: |
  Actix-web framework guardrails, patterns, and best practices for AI-assisted development.
  Use when working with Actix-web projects, or when the user mentions Actix-web.
  Provides actor patterns, async handlers, extractors, and high-performance web guidelines.
license: MIT
metadata:
  author: samuel
  version: "1.0"
  category: framework
  language: rust
  extensions: ".rs"
---

# Actix-web Framework Guide

> Applies to: Actix-web 4+, Rust Web APIs, High-Performance Services
> Complements: `.claude/skills/rust-guide/SKILL.md`

## Core Principles

1. **Type-Safe Extraction**: Use extractors (`web::Json`, `web::Path`, `web::Query`) for request data
2. **Thin Handlers**: Handlers delegate to services; no business logic in handlers
3. **Structured Errors**: Implement `ResponseError` for all error types; never return raw strings
4. **Shared State via `web::Data`**: Application state is injected, never global
5. **Middleware for Cross-Cutting**: Auth, logging, CORS belong in middleware, not handlers

## Project Structure

```
myproject/
├── Cargo.toml
├── src/
│   ├── main.rs                # Entry point, server bootstrap
│   ├── config.rs              # Configuration loading
│   ├── routes.rs              # Route registration
│   ├── handlers/
│   │   ├── mod.rs
│   │   ├── users.rs           # User-related handlers
│   │   └── health.rs          # Health check endpoint
│   ├── models/
│   │   ├── mod.rs
│   │   └── user.rs            # Domain models + DTOs
│   ├── services/
│   │   ├── mod.rs
│   │   └── user_service.rs    # Business logic layer
│   ├── repositories/
│   │   ├── mod.rs
│   │   └── user_repository.rs # Database access layer
│   ├── middleware/
│   │   ├── mod.rs
│   │   └── auth.rs            # Authentication middleware
│   └── errors/
│       ├── mod.rs
│       └── app_error.rs       # Centralized error types
├── tests/
│   └── integration_tests.rs
└── migrations/
```

- `main.rs` bootstraps server, loads config, creates pool, wires routes
- Business logic lives in `services/`, not in handlers
- Database access isolated in `repositories/`
- One error enum per crate with `ResponseError` impl

## Dependencies (Cargo.toml)

```toml
[dependencies]
actix-web = "4"
actix-rt = "2"
actix-cors = "0.7"
serde = { version = "1.0", features = ["derive"] }
serde_json = "1.0"
sqlx = { version = "0.7", features = ["runtime-tokio", "postgres", "uuid", "chrono"] }
validator = { version = "0.16", features = ["derive"] }
thiserror = "1.0"
anyhow = "1.0"
log = "0.4"
env_logger = "0.10"
tracing = "0.1"
tracing-actix-web = "0.7"
uuid = { version = "1.0", features = ["v4", "serde"] }
chrono = { version = "0.4", features = ["serde"] }

[dev-dependencies]
actix-rt = "2"
```

## Application Entry Point

```rust
use actix_cors::Cors;
use actix_web::{middleware, web, App, HttpServer};
use sqlx::postgres::PgPoolOptions;

pub struct AppState {
    pub pool: sqlx::PgPool,
    pub config: config::Config,
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    dotenvy::dotenv().ok();
    env_logger::init_from_env(env_logger::Env::new().default_filter_or("info"));

    let config = config::Config::load().expect("Failed to load configuration");
    let pool = PgPoolOptions::new()
        .max_connections(10)
        .connect(&config.database_url)
        .await
        .expect("Failed to create database pool");

    sqlx::migrate!("./migrations")
        .run(&pool)
        .await
        .expect("Failed to run migrations");

    let app_state = web::Data::new(AppState {
        pool,
        config: config.clone(),
    });

    HttpServer::new(move || {
        let cors = Cors::default()
            .allow_any_origin()
            .allow_any_method()
            .allow_any_header()
            .max_age(3600);

        App::new()
            .app_data(app_state.clone())
            .wrap(cors)
            .wrap(middleware::Logger::default())
            .wrap(middleware::Compress::default())
            .configure(routes::configure)
    })
    .bind(format!("{}:{}", config.host, config.port))?
    .run()
    .await
}
```

## Routing

```rust
use actix_web::web;

pub fn configure(cfg: &mut web::ServiceConfig) {
    cfg.service(
        web::scope("/api/v1")
            .route("/health", web::get().to(handlers::health::health_check))
            .service(
                web::scope("/auth")
                    .route("/register", web::post().to(handlers::users::register))
                    .route("/login", web::post().to(handlers::users::login)),
            )
            .service(
                web::scope("/users")
                    .wrap(crate::middleware::auth::AuthMiddleware)
                    .route("", web::get().to(handlers::users::list_users))
                    .route("/{id}", web::get().to(handlers::users::get_user))
                    .route("/{id}", web::put().to(handlers::users::update_user))
                    .route("/{id}", web::delete().to(handlers::users::delete_user)),
            ),
    );
}
```

### Routing Guardrails

- Group routes by resource under `web::scope`
- Apply middleware at the scope level, not per-route
- Use `web::ServiceConfig` for modular route registration
- Version API routes (`/api/v1/...`)
- Keep route definitions separate from handler implementations

## Extractors

Extractors are how Actix-web injects request data into handler functions.

| Extractor | Purpose | Example |
|-----------|---------|---------|
| `web::Json<T>` | Deserialize JSON body | `body: web::Json<CreateDto>` |
| `web::Path<T>` | URL path parameters | `path: web::Path<Uuid>` |
| `web::Query<T>` | Query string parameters | `query: web::Query<PaginationQuery>` |
| `web::Data<T>` | Shared application state | `state: web::Data<AppState>` |
| `web::Form<T>` | URL-encoded form data | `form: web::Form<LoginForm>` |
| `HttpRequest` | Raw request (headers, extensions) | `req: HttpRequest` |

### Extractor Rules

- Always validate extracted data (use `validator` crate with `Validate` derive)
- Prefer typed extractors over manually parsing `HttpRequest`
- Use `web::Data` for immutable shared state (wrapped in `Arc` internally)
- Limit JSON body size with `.app_data(web::JsonConfig::default().limit(4096))`

## Handlers

Handlers are async functions that take extractors and return `impl Responder`.

```rust
use actix_web::{web, HttpResponse};

pub async fn register(
    state: web::Data<AppState>,
    body: web::Json<CreateUserDto>,
) -> AppResult<HttpResponse> {
    let service = UserService::new(state.pool.clone(), state.config.clone());
    let response = service.register(body.into_inner()).await?;
    Ok(HttpResponse::Created().json(response))
}

pub async fn get_user(
    state: web::Data<AppState>,
    path: web::Path<Uuid>,
) -> AppResult<HttpResponse> {
    let service = UserService::new(state.pool.clone(), state.config.clone());
    let user = service.get_user(path.into_inner()).await?;
    Ok(HttpResponse::Ok().json(user))
}
```

### Handler Rules

- Return `Result<HttpResponse, AppError>` (aliased as `AppResult<HttpResponse>`)
- Use `.into_inner()` to unwrap extractors before passing to services
- No business logic in handlers -- delegate to service layer
- One handler per HTTP method per resource action

## Application State

```rust
pub struct AppState {
    pub pool: sqlx::PgPool,
    pub config: Config,
}

// Register in HttpServer closure:
let app_state = web::Data::new(AppState { pool, config });
App::new().app_data(app_state.clone())

// Access in handlers:
pub async fn handler(state: web::Data<AppState>) -> impl Responder {
    let pool = &state.pool;
    // use pool...
}
```

### State Rules

- Wrap in `web::Data` (internally uses `Arc`)
- Clone `web::Data` in `HttpServer::new` closure (cheap Arc clone)
- Keep state immutable; use `tokio::sync::RwLock` if mutation is required
- Do not store request-scoped data in `AppState`

## Error Handling

```rust
use actix_web::{http::StatusCode, HttpResponse, ResponseError};

#[derive(Debug)]
pub enum AppError {
    NotFound(String),
    BadRequest(String),
    Unauthorized(String),
    Forbidden(String),
    Conflict(String),
    Validation(String),
    Internal(String),
    Database(sqlx::Error),
}

impl ResponseError for AppError {
    fn error_response(&self) -> HttpResponse {
        let (status, message) = match self {
            AppError::NotFound(msg) => (StatusCode::NOT_FOUND, msg.clone()),
            AppError::BadRequest(msg) => (StatusCode::BAD_REQUEST, msg.clone()),
            AppError::Unauthorized(msg) => (StatusCode::UNAUTHORIZED, msg.clone()),
            AppError::Forbidden(msg) => (StatusCode::FORBIDDEN, msg.clone()),
            AppError::Conflict(msg) => (StatusCode::CONFLICT, msg.clone()),
            AppError::Validation(msg) => (StatusCode::UNPROCESSABLE_ENTITY, msg.clone()),
            AppError::Internal(_) => (StatusCode::INTERNAL_SERVER_ERROR, "Internal error".into()),
            AppError::Database(_) => (StatusCode::INTERNAL_SERVER_ERROR, "Database error".into()),
        };
        HttpResponse::build(status).json(serde_json::json!({
            "success": false,
            "error": { "code": status.as_u16(), "message": message }
        }))
    }
}

pub type AppResult<T> = Result<T, AppError>;
```

### Error Handling Rules

- Implement `ResponseError` trait for all custom error types
- Use `From<T>` impls for automatic conversion: `sqlx::Error`, `validator::ValidationErrors`
- Log internal/database errors server-side; return generic messages to clients
- Define `AppResult<T>` type alias to reduce boilerplate

## Middleware

Actix-web middleware uses the `Transform` + `Service` traits.

```rust
pub struct AuthMiddleware;

impl<S, B> Transform<S, ServiceRequest> for AuthMiddleware
where
    S: Service<ServiceRequest, Response = ServiceResponse<B>, Error = Error> + 'static,
    B: 'static,
{
    type Response = ServiceResponse<B>;
    type Error = Error;
    type Transform = AuthMiddlewareService<S>;
    type InitError = ();
    type Future = Ready<Result<Self::Transform, Self::InitError>>;

    fn new_transform(&self, service: S) -> Self::Future {
        ok(AuthMiddlewareService { service: Rc::new(service) })
    }
}
```

### Middleware Rules

- Use `Transform` trait for middleware factories, `Service` for middleware logic
- Store authenticated user data in request extensions (`req.extensions_mut().insert(...)`)
- Apply middleware at scope level: `.service(web::scope("/protected").wrap(AuthMiddleware))`
- Use built-in middleware: `Logger`, `Compress`, `NormalizePath`, `DefaultHeaders`
- Order matters: middleware wraps from bottom to top (last `.wrap()` runs first)

## Configuration

```rust
use serde::Deserialize;

#[derive(Clone, Deserialize)]
pub struct Config {
    pub host: String,
    pub port: u16,
    pub database_url: String,
    pub jwt_secret: String,
    pub jwt_expiration_hours: i64,
}

impl Config {
    pub fn load() -> anyhow::Result<Self> {
        let config = config::Config::builder()
            .add_source(config::Environment::default().separator("__").try_parsing(true))
            .set_default("host", "127.0.0.1")?
            .set_default("port", 8080)?
            .build()?;
        Ok(config.try_deserialize()?)
    }
}
```

## Commands

```bash
# Development
cargo run                              # Start server
cargo watch -x run                     # Watch mode (requires cargo-watch)
RUST_LOG=actix_web=debug cargo run     # Debug logging

# Build
cargo build --release                  # Production build
cargo check                            # Fast type-check

# Quality
cargo fmt                              # Format code
cargo clippy -- -D warnings            # Lint with deny
cargo test                             # Run all tests
cargo tarpaulin                        # Coverage

# Database
sqlx migrate run                       # Run migrations
sqlx migrate add <name>                # Create migration
```

## Best Practices

### Application Structure
- Use `web::Data` for shared application state
- Organize routes with `web::scope` and `ServiceConfig`
- Service layer for business logic, repository layer for data access
- Keep handlers thin: extract, delegate, respond

### Performance
- Use connection pooling (`sqlx::PgPool` or `deadpool`)
- Enable `middleware::Compress` for response compression
- Use async/await throughout; avoid blocking operations
- Configure worker count for production: `.workers(num_cpus::get())`
- Set JSON payload limits to prevent abuse

### Security
- Validate all inputs with `validator` crate
- Use HTTPS in production (terminate at load balancer or use `actix-tls`)
- Implement rate limiting (`actix-governor` or custom middleware)
- Sanitize error messages: never expose internal details to clients
- Use `actix-cors` with explicit origins in production (not `allow_any_origin`)

### Testing
- Use `actix_web::test` module for integration tests
- Create test app with `test::init_service` and shared test state
- Assert on status codes, response bodies, and headers
- Test middleware independently from handlers

## Advanced Topics

For detailed patterns and examples, see:

- [references/patterns.md](references/patterns.md) -- Handler examples, database integration, authentication, actors, testing patterns

## External References

- [Actix-web Documentation](https://actix.rs/docs)
- [Actix-web GitHub](https://github.com/actix/actix-web)
- [Actix Examples](https://github.com/actix/examples)
- [SQLx Documentation](https://docs.rs/sqlx)
