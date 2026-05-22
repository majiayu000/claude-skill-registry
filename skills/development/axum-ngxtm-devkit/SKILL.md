---
name: Axum Framework
description: Ergonomic Rust web framework built on Tower and Tokio.
metadata:
  labels: [rust, axum, web, framework, tower]
  triggers:
    files: ['**/main.rs', '**/routes/*.rs']
    keywords: [axum, Router, Extension, State]
---

# Axum Standards

## Router Setup

```rust
use axum::{Router, routing::{get, post}, Extension};

#[tokio::main]
async fn main() {
    let app = Router::new()
        .route("/", get(root))
        .route("/users", get(list_users).post(create_user))
        .route("/users/:id", get(get_user))
        .nest("/api", api_routes())
        .layer(Extension(db_pool))
        .layer(TraceLayer::new_for_http());

    let listener = tokio::net::TcpListener::bind("0.0.0.0:3000").await.unwrap();
    axum::serve(listener, app).await.unwrap();
}
```

## Extractors

```rust
use axum::{
    extract::{Path, Query, State, Json},
    http::StatusCode,
};

// Path parameters
async fn get_user(Path(id): Path<u64>) -> impl IntoResponse {
    Json(user)
}

// Query parameters
async fn list(Query(params): Query<Pagination>) -> impl IntoResponse {
    Json(items)
}

// JSON body
async fn create(Json(payload): Json<CreateUser>) -> impl IntoResponse {
    (StatusCode::CREATED, Json(user))
}

// State (shared application state)
async fn handler(State(pool): State<PgPool>) -> impl IntoResponse {
    let conn = pool.acquire().await?;
    Json(result)
}
```

## State Management

```rust
#[derive(Clone)]
struct AppState {
    db: PgPool,
    cache: RedisPool,
}

let state = AppState { db, cache };

let app = Router::new()
    .route("/users", get(handler))
    .with_state(state);

async fn handler(State(state): State<AppState>) -> impl IntoResponse {
    // Access state.db, state.cache
}
```

## Error Handling

```rust
use axum::{
    response::{IntoResponse, Response},
    http::StatusCode,
};

enum AppError {
    NotFound,
    Database(sqlx::Error),
}

impl IntoResponse for AppError {
    fn into_response(self) -> Response {
        let (status, message) = match self {
            AppError::NotFound => (StatusCode::NOT_FOUND, "Not found"),
            AppError::Database(_) => (StatusCode::INTERNAL_SERVER_ERROR, "Database error"),
        };
        (status, Json(json!({ "error": message }))).into_response()
    }
}

// Handler returns Result<T, AppError>
async fn handler() -> Result<Json<User>, AppError> {
    let user = db.find(id).await.map_err(AppError::Database)?;
    user.ok_or(AppError::NotFound).map(Json)
}
```

## Middleware (Tower Layers)

```rust
use tower_http::{
    trace::TraceLayer,
    cors::CorsLayer,
    compression::CompressionLayer,
};

let app = Router::new()
    .route("/", get(handler))
    .layer(TraceLayer::new_for_http())
    .layer(CompressionLayer::new())
    .layer(CorsLayer::permissive());

// Custom middleware
async fn auth_layer<B>(
    req: Request<B>,
    next: Next<B>,
) -> Result<Response, StatusCode> {
    let token = req.headers().get("Authorization");
    // Validate token
    Ok(next.run(req).await)
}
```

## Testing

```rust
use axum::http::StatusCode;
use axum_test::TestServer;

#[tokio::test]
async fn test_get_user() {
    let app = create_app();
    let server = TestServer::new(app).unwrap();

    let response = server.get("/users/1").await;

    assert_eq!(response.status_code(), StatusCode::OK);
}
```

## Best Practices

1. **State**: Use `State<T>` over `Extension<T>` for type safety
2. **Extractors**: Order matters - put fallible extractors last
3. **Layers**: Apply common layers at router level, not per-route
4. **Errors**: Implement `IntoResponse` for custom error types
