---
name: axum-web-framework
description: Production patterns for Axum 0.8.x HTTP services with Tower middleware, type-safe routing, state management with FromRef, extractors, and error handling. Use when building REST APIs, HTTP services, web applications, or adding middleware to Axum routers.
---

# Axum Web Framework

*Production patterns for Axum 0.8.x with Tower middleware and type-safe routing*

## Version Context
- **Axum**: 0.8.7 (latest stable)
- **Tower**: 0.5.2
- **Tower-HTTP**: 0.6.x
- **Tokio**: 1.48.0

## When to Use This Skill

- Building HTTP REST APIs
- Creating web services with Axum
- Adding middleware (timeout, tracing, compression)
- Managing application state
- Implementing custom extractors
- Handling HTTP errors and responses

## Minimal Production Application

```rust
use axum::{
    extract::State,
    routing::{get, post},
    Router,
};
use std::sync::Arc;
use tokio::net::TcpListener;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Build shared state
    let state = Arc::new(AppState::new().await?);

    // Build router
    let app = Router::new()
        .route("/health", get(health))
        .route("/users/:id", get(get_user))
        .with_state(state);

    // Start server
    let listener = TcpListener::bind("0.0.0.0:3000").await?;
    axum::serve(listener, app)
        .with_graceful_shutdown(shutdown_signal())
        .await?;

    Ok(())
}
```

## State Management with FromRef

```rust
use axum::extract::{State, FromRef};
use std::sync::Arc;

#[derive(Clone, FromRef)]
pub struct AppState {
    pub db: Arc<Database>,
    pub cache: Arc<Cache>,
    pub config: Arc<Config>,
}

impl AppState {
    pub async fn new() -> Result<Self, AppError> {
        let config = Arc::new(Config::load()?);
        let db = Arc::new(Database::connect(&config.db_url).await?);
        let cache = Arc::new(Cache::connect(&config.redis_url).await?);

        Ok(Self { db, cache, config })
    }
}

// Automatic sub-state extraction via FromRef
async fn handler(
    State(db): State<Arc<Database>>,
    State(config): State<Arc<Config>>,
) -> String {
    format!("DB: {}, Config: {:?}", db.status(), config.env)
}
```

## Router Composition

```rust
use axum::{Router, routing::{get, post, delete}};

pub fn create_router(state: Arc<AppState>) -> Router {
    Router::new()
        .merge(health_routes())
        .merge(user_routes())
        .merge(order_routes())
        .with_state(state)
}

fn health_routes<S: Clone + Send + Sync + 'static>() -> Router<S> {
    Router::new()
        .route("/health", get(health_check))
        .route("/ready", get(readiness_check))
        .route("/metrics", get(metrics))
}

fn user_routes() -> Router<Arc<AppState>> {
    Router::new()
        .route("/users", post(create_user).get(list_users))
        .route("/users/:id", get(get_user).put(update_user).delete(delete_user))
}
```

## Extractors

### Built-in Extractors

```rust
use axum::{
    extract::{Path, Query, Json, State},
    http::{HeaderMap, StatusCode},
};
use serde::{Deserialize, Serialize};

#[derive(Deserialize)]
pub struct CreateUserRequest {
    pub email: String,
    pub name: String,
}

#[derive(Deserialize)]
pub struct ListQuery {
    pub page: Option<u32>,
    pub limit: Option<u32>,
}

// Path extraction
async fn get_user(
    State(db): State<Arc<Database>>,
    Path(user_id): Path<String>,
) -> Result<Json<User>, AppError> {
    let user = db.users.find_by_id(&user_id).await?;
    Ok(Json(user))
}

// Query parameters
async fn list_users(
    State(db): State<Arc<Database>>,
    Query(params): Query<ListQuery>,
) -> Result<Json<Vec<User>>, AppError> {
    let page = params.page.unwrap_or(1);
    let limit = params.limit.unwrap_or(20);
    let users = db.users.list(page, limit).await?;
    Ok(Json(users))
}

// JSON body extraction
async fn create_user(
    State(db): State<Arc<Database>>,
    Json(payload): Json<CreateUserRequest>,
) -> Result<(StatusCode, Json<User>), AppError> {
    let user = db.users.create(&payload).await?;
    Ok((StatusCode::CREATED, Json(user)))
}
```

### Custom Extractors

```rust
use axum::{
    async_trait,
    extract::FromRequestParts,
    http::{request::Parts, StatusCode},
};

/// Authenticated user extractor
pub struct AuthenticatedUser {
    pub id: UserId,
    pub email: String,
}

#[async_trait]
impl<S> FromRequestParts<S> for AuthenticatedUser
where
    S: Send + Sync,
{
    type Rejection = (StatusCode, String);

    async fn from_request_parts(
        parts: &mut Parts,
        _state: &S,
    ) -> Result<Self, Self::Rejection> {
        // Extract JWT from Authorization header
        let auth_header = parts
            .headers
            .get("authorization")
            .and_then(|v| v.to_str().ok())
            .ok_or((StatusCode::UNAUTHORIZED, "Missing auth header".to_string()))?;

        let token = auth_header
            .strip_prefix("Bearer ")
            .ok_or((StatusCode::UNAUTHORIZED, "Invalid auth header".to_string()))?;

        // Validate token
        let claims = validate_token(token)
            .map_err(|_| (StatusCode::UNAUTHORIZED, "Invalid token".to_string()))?;

        Ok(AuthenticatedUser {
            id: claims.user_id,
            email: claims.email,
        })
    }
}

// Usage in handlers
async fn get_profile(
    user: AuthenticatedUser,
    State(db): State<Arc<Database>>,
) -> Result<Json<UserProfile>, AppError> {
    let profile = db.profiles.find_by_user_id(&user.id).await?;
    Ok(Json(profile))
}
```

## Middleware

### Tower Middleware Stack

```rust
use tower::{ServiceBuilder, limit::ConcurrencyLimitLayer, timeout::TimeoutLayer};
use tower_http::{
    trace::TraceLayer,
    compression::CompressionLayer,
    cors::CorsLayer,
    limit::RequestBodyLimitLayer,
};
use std::time::Duration;

pub fn create_app(state: Arc<AppState>) -> Router {
    Router::new()
        .route("/api/users", post(create_user))
        .layer(
            ServiceBuilder::new()
                // Observability
                .layer(TraceLayer::new_for_http())
                // Compression
                .layer(CompressionLayer::new())
                // CORS
                .layer(CorsLayer::permissive())
                // Limits
                .layer(RequestBodyLimitLayer::new(1024 * 1024)) // 1MB
                .layer(TimeoutLayer::new(Duration::from_secs(30)))
                .layer(ConcurrencyLimitLayer::new(1000))
        )
        .with_state(state)
}
```

### Custom Middleware

```rust
use axum::{
    extract::Request,
    middleware::{self, Next},
    response::Response,
};

/// Request ID middleware
pub async fn request_id_middleware(
    mut request: Request,
    next: Next,
) -> Response {
    let request_id = uuid::Uuid::new_v4();

    // Add to extensions for use in handlers
    request.extensions_mut().insert(RequestId(request_id));

    // Add to response headers
    let mut response = next.run(request).await;
    response.headers_mut().insert(
        "x-request-id",
        request_id.to_string().parse().unwrap(),
    );

    response
}

// Apply to router
let app = Router::new()
    .route("/users", get(list_users))
    .layer(middleware::from_fn(request_id_middleware))
    .with_state(state);
```

## Error Handling with IntoResponse

```rust
use axum::{
    response::{IntoResponse, Response},
    http::StatusCode,
    Json,
};

#[derive(Debug, thiserror::Error)]
pub enum AppError {
    #[error("not found")]
    NotFound,

    #[error("database error: {0}")]
    Database(#[from] sqlx::Error),

    #[error("validation error: {0}")]
    Validation(String),
}

impl IntoResponse for AppError {
    fn into_response(self) -> Response {
        let (status, message) = match self {
            AppError::NotFound => (StatusCode::NOT_FOUND, self.to_string()),
            AppError::Database(_) => (
                StatusCode::INTERNAL_SERVER_ERROR,
                "Internal error".to_string(),
            ),
            AppError::Validation(msg) => (StatusCode::BAD_REQUEST, msg),
        };

        let body = Json(serde_json::json!({
            "error": message,
        }));

        (status, body).into_response()
    }
}

// Handlers return Result
async fn handler() -> Result<Json<User>, AppError> {
    let user = db.find_user().await?; // Error automatically converted
    Ok(Json(user))
}
```

## Graceful Shutdown

```rust
use tokio::signal;

async fn shutdown_signal() {
    let ctrl_c = async {
        signal::ctrl_c()
            .await
            .expect("failed to install Ctrl+C handler");
    };

    #[cfg(unix)]
    let terminate = async {
        signal::unix::signal(signal::unix::SignalKind::terminate())
            .expect("failed to install signal handler")
            .recv()
            .await;
    };

    #[cfg(not(unix))]
    let terminate = std::future::pending::<()>();

    tokio::select! {
        _ = ctrl_c => {},
        _ = terminate => {},
    }

    tracing::info!("shutdown signal received");
}

// Usage
axum::serve(listener, app)
    .with_graceful_shutdown(shutdown_signal())
    .await?;
```

## Key Patterns

1. **State**: Use `Arc<AppState>` with `FromRef` for sub-state extraction
2. **Extractors**: Compose multiple extractors in handler signatures
3. **Middleware**: Apply Tower layers for cross-cutting concerns
4. **Errors**: Implement `IntoResponse` for custom error types
5. **Modularity**: Split routes into separate functions, merge with `.merge()`

## Common Dependencies

```toml
[dependencies]
axum = { version = "0.8", features = ["macros"] }
tokio = { version = "1", features = ["full"] }
tower = "0.5"
tower-http = { version = "0.6", features = ["trace", "cors", "compression"] }
serde = { version = "1", features = ["derive"] }
thiserror = "2"
```
