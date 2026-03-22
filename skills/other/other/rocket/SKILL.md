---
name: rocket
description: |
  Rocket framework guardrails, patterns, and best practices for AI-assisted development.
  Use when working with Rocket projects, or when the user mentions Rocket framework.
  Provides type-safe routing, request guards, fairings, and macro-based handler guidelines.
license: MIT
metadata:
  author: samuel
  version: "1.0"
  category: framework
  language: rust
  extensions: ".rs"
---

# Rocket Framework Guide

> Applies to: Rocket 0.5+, Rust Web APIs, Type-Safe Web Applications
> Use with: `.claude/skills/rust-guide/SKILL.md`

## Overview

Rocket is a Rust web framework focused on ease of use, developer experience, and type safety. It uses Rust's type system to ensure correctness at compile time, with powerful features like request guards, fairings (middleware), and derive macros for minimal boilerplate.

### When to Use Rocket

- **Type-Safe APIs**: Maximum compile-time guarantees
- **Developer Experience**: Clean, expressive syntax with minimal boilerplate
- **Rapid Prototyping**: Quick to start; attribute macros handle routing
- **Form Handling**: Excellent support for HTML forms and multipart uploads
- **Traditional Web Apps**: Both APIs and server-rendered HTML

### When NOT to Use Rocket

- **Async-Heavy Workloads**: Consider Axum for pure async performance
- **Minimal Dependencies**: Rocket has heavier compile times
- **Maximum Control**: Use Axum/Actix for fine-grained middleware control

## Project Structure

```
myproject/
├── Cargo.toml
├── Rocket.toml                 # Rocket configuration (per-profile)
├── src/
│   ├── main.rs                 # Entry point (#[launch] or #[rocket::main])
│   ├── lib.rs                  # Library exports
│   ├── routes/
│   │   ├── mod.rs              # Route mounting functions
│   │   ├── users.rs            # User handlers
│   │   └── health.rs           # Health checks
│   ├── models/
│   │   ├── mod.rs
│   │   └── user.rs             # Domain + request/response models
│   ├── guards/                 # Request guards (auth, rate-limit, etc.)
│   │   ├── mod.rs
│   │   └── auth.rs
│   ├── fairings/               # Middleware (logging, CORS, timing)
│   │   ├── mod.rs
│   │   └── logging.rs
│   ├── db/
│   │   ├── mod.rs              # Database pool definition
│   │   └── pool.rs
│   ├── services/               # Business logic layer
│   │   ├── mod.rs
│   │   └── user_service.rs
│   ├── error.rs                # AppError + catchers
│   └── config.rs               # Custom config extraction
├── tests/
│   └── api_tests.rs            # Integration tests via Client
├── migrations/
└── static/                     # Static file serving
```

## Dependencies

```toml
[dependencies]
rocket = { version = "0.5", features = ["json", "secrets"] }
rocket_db_pools = { version = "0.1", features = ["sqlx_postgres"] }
sqlx = { version = "0.7", features = ["runtime-tokio", "postgres", "chrono", "uuid"] }
serde = { version = "1.0", features = ["derive"] }
serde_json = "1.0"
validator = { version = "0.16", features = ["derive"] }
jsonwebtoken = "9"
bcrypt = "0.15"
chrono = { version = "0.4", features = ["serde"] }
uuid = { version = "1", features = ["v4", "serde"] }
thiserror = "1.0"
dotenvy = "0.15"
tokio = { version = "1", features = ["full"] }

[dev-dependencies]
rocket = { version = "0.5", features = ["json", "secrets"] }
```

## Application Entry Point

```rust
#[macro_use] extern crate rocket;

use rocket::{Build, Rocket};
use rocket_db_pools::Database;

#[launch]
fn rocket() -> Rocket<Build> {
    dotenvy::dotenv().ok();

    rocket::build()
        .attach(DbPool::init())
        .attach(RequestLogger)
        .mount("/api", routes::api_routes())
        .mount("/health", routes::health_routes())
        .register("/", catchers![
            error::not_found,
            error::internal_error,
            error::unauthorized,
            error::bad_request,
        ])
}
```

## Configuration (Rocket.toml)

```toml
[default]
address = "0.0.0.0"
port = 8000
workers = 16
keep_alive = 5
log_level = "normal"
limits = { form = "64 kB", json = "1 MiB" }

[default.databases.db_pool]
url = "postgres://user:password@localhost/mydb"
min_connections = 5
max_connections = 20
connect_timeout = 5
idle_timeout = 300

[debug]
log_level = "debug"

[release]
secret_key = "generate-a-256-bit-base64-key"
log_level = "critical"
```

Custom config values via environment or Rocket.toml:

```rust
use rocket::serde::Deserialize;

#[derive(Debug, Deserialize)]
#[serde(crate = "rocket::serde")]
pub struct AppConfig {
    pub jwt_secret: String,
    pub jwt_expiration_hours: i64,
}

impl Default for AppConfig {
    fn default() -> Self {
        Self {
            jwt_secret: std::env::var("JWT_SECRET")
                .unwrap_or_else(|_| "development-secret-key".to_string()),
            jwt_expiration_hours: std::env::var("JWT_EXPIRATION_HOURS")
                .unwrap_or_else(|_| "24".to_string())
                .parse()
                .unwrap_or(24),
        }
    }
}
```

## Routing Macros

Rocket uses attribute macros on handler functions. The macro defines the HTTP method, path, and dynamic segments.

```rust
#[get("/")]                        // GET /
#[post("/users", data = "<input>")]// POST /users with body
#[put("/users/<id>", data = "<d>")] // PUT /users/:id with body
#[delete("/users/<id>")]           // DELETE /users/:id
#[get("/users?<limit>&<offset>")]  // GET /users?limit=&offset=
```

Mount routes via `Vec<Route>`:

```rust
pub fn api_routes() -> Vec<Route> {
    routes![register, login, get_user, list_users, delete_user]
}
```

## Request Guards

Request guards implement `FromRequest` and run before the handler. They are Rocket's primary mechanism for authentication, authorization, and request validation.

```rust
#[derive(Debug)]
pub struct AuthUser {
    pub user_id: Uuid,
    pub email: String,
    pub role: String,
}

#[rocket::async_trait]
impl<'r> FromRequest<'r> for AuthUser {
    type Error = AppError;

    async fn from_request(request: &'r Request<'_>) -> Outcome<Self, Self::Error> {
        let token = match request.headers().get_one("Authorization") {
            Some(h) if h.starts_with("Bearer ") => &h[7..],
            _ => return Outcome::Error((
                Status::Unauthorized,
                AppError::Unauthorized("Missing Authorization header".into()),
            )),
        };

        // Decode and validate JWT, return Outcome::Success or Outcome::Error
        // ...
    }
}
```

Compose guards for role-based access:

```rust
pub struct AdminUser(pub AuthUser);

#[rocket::async_trait]
impl<'r> FromRequest<'r> for AdminUser {
    type Error = AppError;

    async fn from_request(request: &'r Request<'_>) -> Outcome<Self, Self::Error> {
        let user = match AuthUser::from_request(request).await {
            Outcome::Success(u) => u,
            Outcome::Error(e) => return Outcome::Error(e),
            Outcome::Forward(s) => return Outcome::Forward(s),
        };
        if user.role != "admin" {
            return Outcome::Error((
                Status::Forbidden,
                AppError::Unauthorized("Admin access required".into()),
            ));
        }
        Outcome::Success(AdminUser(user))
    }
}
```

Optional auth: wrap in `Option<AuthUser>` or create an `OptionalUser` guard.

## Responders and Error Handling

Implement `Responder` for custom error types to return structured JSON errors:

```rust
#[derive(Error, Debug)]
pub enum AppError {
    #[error("Not found: {0}")]
    NotFound(String),
    #[error("Unauthorized: {0}")]
    Unauthorized(String),
    #[error("Validation: {0}")]
    Validation(String),
    #[error("Database error: {0}")]
    Database(#[from] sqlx::Error),
    #[error("Internal: {0}")]
    Internal(String),
}

impl<'r> Responder<'r, 'static> for AppError {
    fn respond_to(self, request: &'r Request<'_>) -> response::Result<'static> {
        let (status, body) = match &self {
            AppError::NotFound(m) => (Status::NotFound, json!({"error": m})),
            AppError::Unauthorized(m) => (Status::Unauthorized, json!({"error": m})),
            AppError::Validation(m) => (Status::BadRequest, json!({"error": m})),
            AppError::Database(_) => (Status::InternalServerError, json!({"error": "database error"})),
            AppError::Internal(_) => (Status::InternalServerError, json!({"error": "internal error"})),
        };
        Response::build_from(Json(body).respond_to(request)?)
            .status(status)
            .ok()
    }
}
```

Register catchers for unhandled status codes:

```rust
#[catch(404)]
pub fn not_found() -> Json<Value> { Json(json!({"error": "not found"})) }

#[catch(500)]
pub fn internal_error() -> Json<Value> { Json(json!({"error": "internal error"})) }

#[catch(401)]
pub fn unauthorized() -> Json<Value> { Json(json!({"error": "unauthorized"})) }
```

## Fairings (Middleware)

Fairings attach cross-cutting behavior to the request/response lifecycle.

```rust
pub struct RequestLogger;

#[rocket::async_trait]
impl Fairing for RequestLogger {
    fn info(&self) -> Info {
        Info { name: "Request Logger", kind: Kind::Request | Kind::Response }
    }

    async fn on_request(&self, request: &mut Request<'_>, _: &mut Data<'_>) {
        request.local_cache(|| Instant::now());
    }

    async fn on_response<'r>(&self, request: &'r Request<'_>, response: &mut Response<'r>) {
        let start = request.local_cache(|| Instant::now());
        println!("{} {} {} - {:?}", request.method(), request.uri(), response.status().code, start.elapsed());
    }
}
```

CORS fairing pattern:

```rust
pub struct Cors;

#[rocket::async_trait]
impl Fairing for Cors {
    fn info(&self) -> Info { Info { name: "CORS", kind: Kind::Response } }

    async fn on_response<'r>(&self, _: &'r Request<'_>, response: &mut Response<'r>) {
        response.set_header(Header::new("Access-Control-Allow-Origin", "*"));
        response.set_header(Header::new("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS"));
        response.set_header(Header::new("Access-Control-Allow-Headers", "Content-Type, Authorization"));
    }
}
```

## State Management

### Database Pool (rocket_db_pools)

```rust
use rocket_db_pools::{sqlx, Database, Connection};

#[derive(Database)]
#[database("db_pool")]
pub struct DbPool(sqlx::PgPool);

pub type DbConn = Connection<DbPool>;
```

Use in handlers:

```rust
#[get("/users/<id>")]
pub async fn get_user(mut db: DbConn, id: &str) -> Result<Json<User>, AppError> {
    let user = sqlx::query_as::<_, User>("SELECT * FROM users WHERE id = $1")
        .bind(id)
        .fetch_optional(&mut **db)
        .await?
        .ok_or_else(|| AppError::NotFound("user not found".into()))?;
    Ok(Json(user))
}
```

### Managed State

```rust
// Attach in build
rocket::build().manage(AppConfig::default())

// Extract in handler
#[get("/info")]
fn info(config: &State<AppConfig>) -> String {
    format!("JWT expiry: {}h", config.jwt_expiration_hours)
}
```

## Form Handling

```rust
#[derive(FromForm)]
pub struct UploadForm<'r> {
    pub name: String,
    pub description: Option<String>,
    pub file: TempFile<'r>,
}

#[post("/upload", data = "<form>")]
pub async fn upload(mut form: Form<UploadForm<'_>>, auth: AuthUser) -> Result<Json<Value>, AppError> {
    let filename = format!("uploads/{}_{}", auth.user_id, form.name);
    form.file.persist_to(&filename).await
        .map_err(|e| AppError::Internal(e.to_string()))?;
    Ok(Json(json!({"status": "uploaded", "filename": filename})))
}
```

Multipart with built-in validation:

```rust
#[derive(FromForm)]
pub struct ProfileForm<'r> {
    #[field(validate = len(1..100))]
    pub name: String,
    #[field(validate = contains('@'))]
    pub email: String,
    #[field(validate = len(..1_000_000))]
    pub avatar: Option<TempFile<'r>>,
}
```

## Commands

```bash
cargo run                          # Start dev server
cargo build --release              # Production build
cargo test                         # All tests
cargo test test_health_check       # Specific test
cargo fmt                          # Format
cargo clippy                       # Lint
cargo check                        # Fast type-check
cargo doc --open                   # Generate docs
ROCKET_LOG_LEVEL=debug cargo run   # Debug logging
```

## Best Practices

### DO

- Use request guards for authentication/authorization
- Implement `Responder` for custom error types
- Use fairings for cross-cutting concerns (logging, CORS, timing)
- Leverage Rocket's type system for compile-time validation
- Use `rocket_db_pools` for managed database connections
- Configure via `Rocket.toml` with per-profile settings
- Use derive macros (`FromForm`, `FromRequest`) to reduce boilerplate
- Test with `rocket::local::asynchronous::Client`
- Register catchers for all common HTTP error codes

### DON'T

- Use `unwrap()`/`expect()` in handler code
- Ignore validation errors from form or JSON input
- Store secrets in `Rocket.toml` (use environment variables)
- Block async handlers with synchronous operations
- Skip error catchers for 404, 401, 500
- Use global mutable state when `State<T>` or request-local cache suffices
- Forget to attach database pool via `.attach(DbPool::init())`

## Advanced Patterns

For detailed handler examples, database integration, authentication flows, form handling, and testing patterns, see:

- [references/patterns.md](references/patterns.md) -- CRUD handlers, Diesel/SQLx, JWT auth, testing with Client

## External References

- [Rocket Documentation](https://rocket.rs/v0.5/)
- [Rocket Guide](https://rocket.rs/v0.5/guide/)
- [Rocket API Reference](https://api.rocket.rs/v0.5/)
- [rocket_db_pools](https://crates.io/crates/rocket_db_pools)
- [Rocket GitHub](https://github.com/SergioBenitez/Rocket)
- [Rocket Examples](https://github.com/SergioBenitez/Rocket/tree/v0.5/examples)
