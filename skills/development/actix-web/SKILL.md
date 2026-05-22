---
name: Actix-web Framework
description: High-performance Rust web framework with actor model foundation.
metadata:
  labels: [rust, actix-web, web, framework]
  triggers:
    files: ['**/main.rs', '**/handlers/*.rs']
    keywords: [actix_web, HttpServer, web, App]
---

# Actix-web Standards

## Handler Functions

```rust
use actix_web::{web, HttpResponse, Result};

// Path parameters
async fn get_user(path: web::Path<u64>) -> Result<HttpResponse> {
    let user_id = path.into_inner();
    Ok(HttpResponse::Ok().json(user))
}

// Query parameters
#[derive(Deserialize)]
struct Pagination {
    page: Option<u32>,
    limit: Option<u32>,
}

async fn list_users(query: web::Query<Pagination>) -> Result<HttpResponse> {
    let page = query.page.unwrap_or(1);
    Ok(HttpResponse::Ok().json(users))
}

// JSON body
async fn create_user(body: web::Json<CreateUser>) -> Result<HttpResponse> {
    let user = body.into_inner();
    Ok(HttpResponse::Created().json(created))
}
```

## Extractors

| Extractor | Purpose |
|-----------|---------|
| `web::Path<T>` | URL path parameters |
| `web::Query<T>` | Query string |
| `web::Json<T>` | JSON request body |
| `web::Form<T>` | Form data |
| `web::Data<T>` | Application state |
| `HttpRequest` | Full request access |

**Custom Extractors**:
```rust
impl FromRequest for AuthUser {
    type Error = Error;
    type Future = Ready<Result<Self, Self::Error>>;

    fn from_request(req: &HttpRequest, _: &mut Payload) -> Self::Future {
        // Extract and validate auth header
    }
}
```

## State Management

```rust
struct AppState {
    db: PgPool,
    cache: RedisPool,
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    let state = web::Data::new(AppState {
        db: create_pool().await,
        cache: create_cache().await,
    });

    HttpServer::new(move || {
        App::new()
            .app_data(state.clone())
            .service(handlers)
    })
    .bind("127.0.0.1:8080")?
    .run()
    .await
}

// Access in handlers
async fn handler(state: web::Data<AppState>) -> Result<HttpResponse> {
    let conn = state.db.acquire().await?;
    Ok(HttpResponse::Ok().finish())
}
```

## Middleware

```rust
use actix_web::middleware::{Logger, Compress, NormalizePath};

App::new()
    .wrap(Logger::default())
    .wrap(Compress::default())
    .wrap(NormalizePath::trim())
    .wrap(custom_middleware)

// Custom middleware
async fn auth_middleware(
    req: ServiceRequest,
    srv: &Service,
) -> Result<ServiceResponse, Error> {
    // Validate token
    srv.call(req).await
}
```

## Error Handling

```rust
use actix_web::{error, HttpResponse};

#[derive(Debug, thiserror::Error)]
enum ApiError {
    #[error("Not found")]
    NotFound,
    #[error("Database error")]
    Database(#[from] sqlx::Error),
}

impl error::ResponseError for ApiError {
    fn error_response(&self) -> HttpResponse {
        match self {
            ApiError::NotFound => HttpResponse::NotFound().json({"error": "Not found"}),
            ApiError::Database(_) => HttpResponse::InternalServerError().finish(),
        }
    }
}
```

## Routing

```rust
App::new()
    .route("/", web::get().to(index))
    .service(
        web::scope("/api/v1")
            .route("/users", web::get().to(list_users))
            .route("/users/{id}", web::get().to(get_user))
            .route("/users", web::post().to(create_user))
    )
```

## Best Practices

1. **Concurrency**: Use `.workers(N)` to control thread pool size
2. **Timeouts**: Configure `keep_alive` and client timeouts
3. **Graceful Shutdown**: Handle SIGTERM properly
4. **Testing**: Use `actix_web::test` for integration tests
