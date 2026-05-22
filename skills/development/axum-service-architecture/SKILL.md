---
name: axum-service-architecture
description: Service architecture patterns for Axum applications including layered design (Router → Handler → Service → Repository), AppState with FromRef for dependency injection, Tower ServiceBuilder for middleware composition, and modular router organization. Use when designing service layers, managing dependencies, composing middleware stacks, or structuring Axum applications.
---

# Axum Service Architecture

*Production service architecture patterns for layered Axum applications*

## Version Context
- **Axum**: 0.8.7
- **Tower**: 0.5.2
- **Tower-HTTP**: 0.6.x

## When to Use This Skill

- Designing service layer architecture
- Managing application dependencies
- Composing middleware with Tower
- Organizing routers modularly
- Implementing dependency injection patterns
- Structuring production Axum applications

## Service Layer Architecture

### Layered Architecture Pattern

```
Client → Router → Tower Layers → Handler → Service → Repository → External
         (Axum)  (timeout/retry)  (extract) (domain)  (data)      (I/O)
```

**Benefits:**
- Clear separation of concerns
- Easy to test each layer independently
- Maintainable and scalable structure
- Explicit dependencies

### Architecture Example

```rust
use axum::{Router, routing::get};
use tower::ServiceBuilder;
use tower_http::{trace::TraceLayer, timeout::TimeoutLayer};
use std::time::Duration;

// Layer 1: Router (HTTP routing)
pub fn create_router(state: AppState) -> Router {
    Router::new()
        .route("/users", get(list_users).post(create_user))
        .route("/users/:id", get(get_user))
        .layer(
            ServiceBuilder::new()
                .layer(TraceLayer::new_for_http())
                .layer(TimeoutLayer::new(Duration::from_secs(30)))
        )
        .with_state(state)
}

// Layer 2: Handler (HTTP concerns, extraction)
async fn create_user(
    State(service): State<Arc<UserService>>,
    Json(payload): Json<CreateUserRequest>,
) -> Result<Json<UserResponse>, ApiError> {
    let user = service.create_user(payload).await?;
    Ok(Json(user.into()))
}

// Layer 3: Service (business logic)
impl UserService {
    pub async fn create_user(
        &self,
        request: CreateUserRequest,
    ) -> Result<User, UserError> {
        // Validation
        request.validate()?;

        // Business logic
        let user = User::new(request.email, request.name);

        // Delegate to repository
        self.repository.save_user(&user).await?;

        Ok(user)
    }
}

// Layer 4: Repository (data access)
#[async_trait]
pub trait UserRepository: Send + Sync {
    async fn save_user(&self, user: &User) -> Result<(), RepositoryError>;
    async fn find_user(&self, id: UserId) -> Result<User, RepositoryError>;
}
```

## Dependency Management with AppState

### AppState Pattern

```rust
use axum::extract::FromRef;
use std::sync::Arc;

/// Primary application state
#[derive(Clone, FromRef)]
pub struct AppState {
    pub database: Arc<Database>,
    pub cache: Arc<RedisClient>,
    pub config: Arc<Config>,
    pub user_service: Arc<UserService>,
    pub order_service: Arc<OrderService>,
}

impl AppState {
    /// Constructor with dependency wiring
    pub async fn new(config: Config) -> Result<Self, AppError> {
        let database = Arc::new(Database::connect(&config.database_url).await?);
        let cache = Arc::new(RedisClient::connect(&config.redis_url).await?);

        let user_service = Arc::new(UserService::new(
            database.clone(),
            cache.clone(),
        ));

        let order_service = Arc::new(OrderService::new(
            database.clone(),
            user_service.clone(),
        ));

        Ok(Self {
            database,
            cache,
            config: Arc::new(config),
            user_service,
            order_service,
        })
    }
}
```

### FromRef for Sub-Dependencies

```rust
// Extract specific dependencies from AppState
impl FromRef<AppState> for Arc<Database> {
    fn from_ref(app_state: &AppState) -> Self {
        app_state.database.clone()
    }
}

impl FromRef<AppState> for Arc<UserService> {
    fn from_ref(app_state: &AppState) -> Self {
        app_state.user_service.clone()
    }
}

// Handlers can extract exactly what they need
async fn handler(
    State(db): State<Arc<Database>>,  // Extracted via FromRef
    State(service): State<Arc<UserService>>,
) -> Result<Json<Response>, ApiError> {
    // Use only what's needed
    let data = service.process(db).await?;
    Ok(Json(data))
}
```

## Tower ServiceBuilder Pattern

### Middleware Composition

```rust
use tower::ServiceBuilder;
use tower_http::{
    trace::TraceLayer,
    timeout::TimeoutLayer,
    compression::CompressionLayer,
    cors::CorsLayer,
    limit::{RequestBodyLimitLayer, ConcurrencyLimitLayer},
};
use std::time::Duration;

pub fn build_middleware_stack() -> ServiceBuilder<
    tower::layer::util::Stack<
        TraceLayer<SharedClassifier>,
        tower::layer::util::Stack<TimeoutLayer, /* ... */>
    >
> {
    ServiceBuilder::new()
        // Observability (first - captures all requests)
        .layer(TraceLayer::new_for_http())

        // Security
        .layer(CorsLayer::permissive())

        // Performance
        .layer(CompressionLayer::new())
        .layer(RequestBodyLimitLayer::new(1024 * 1024)) // 1MB

        // Reliability
        .layer(TimeoutLayer::new(Duration::from_secs(30)))
        .layer(ConcurrencyLimitLayer::new(1000))
}

// Apply to router
let app = Router::new()
    .route("/", get(handler))
    .layer(build_middleware_stack())
    .with_state(state);
```

### Custom Middleware with State

```rust
use axum::middleware::{self, Next};
use axum::extract::{Request, State};

async fn auth_middleware(
    State(auth_service): State<Arc<AuthService>>,
    mut request: Request,
    next: Next,
) -> Result<Response, ApiError> {
    let token = request
        .headers()
        .get("authorization")
        .ok_or(ApiError::MissingAuth)?;

    let user = auth_service
        .validate_token(token)
        .await
        .map_err(ApiError::InvalidAuth)?;

    // Add authenticated user to extensions
    request.extensions_mut().insert(user);

    Ok(next.run(request).await)
}

// Apply with state
let app = Router::new()
    .route("/protected", get(protected_handler))
    .layer(middleware::from_fn_with_state(
        state.clone(),
        auth_middleware
    ))
    .with_state(state);
```

## Modular Router Organization

### Router Composition

```rust
use axum::Router;

pub fn create_app(state: AppState) -> Router {
    Router::new()
        .nest("/api/v1", api_v1_routes())
        .nest("/admin", admin_routes())
        .merge(health_routes())
        .with_state(state)
}

fn api_v1_routes() -> Router<AppState> {
    Router::new()
        .merge(user_routes())
        .merge(order_routes())
        .merge(product_routes())
}

fn user_routes() -> Router<AppState> {
    Router::new()
        .route("/users", get(list_users).post(create_user))
        .route("/users/:id", get(get_user).put(update_user).delete(delete_user))
}

fn order_routes() -> Router<AppState> {
    Router::new()
        .route("/orders", get(list_orders).post(create_order))
        .route("/orders/:id", get(get_order))
}

fn health_routes() -> Router<AppState> {
    Router::new()
        .route("/health", get(health_check))
        .route("/ready", get(readiness_check))
        .route("/metrics", get(metrics_handler))
}

fn admin_routes() -> Router<AppState> {
    Router::new()
        .route("/admin/users", get(admin_list_users))
        .layer(middleware::from_fn(require_admin_role))
}
```

## Configuration Management

### Type-Safe Configuration

```rust
use serde::{Deserialize, Serialize};
use std::time::Duration;

#[derive(Debug, Clone, Deserialize, Serialize)]
pub struct Config {
    pub server: ServerConfig,
    pub database: DatabaseConfig,
    pub redis: RedisConfig,
    pub observability: ObservabilityConfig,
}

#[derive(Debug, Clone, Deserialize, Serialize)]
pub struct ServerConfig {
    pub host: String,
    pub port: u16,
    #[serde(with = "humantime_serde")]
    pub request_timeout: Duration,
    pub max_connections: usize,
}

#[derive(Debug, Clone, Deserialize, Serialize)]
pub struct DatabaseConfig {
    pub url: String,
    pub max_connections: u32,
    #[serde(with = "humantime_serde")]
    pub connection_timeout: Duration,
}

impl Config {
    pub fn from_env() -> Result<Self, ConfigError> {
        let config = config::Config::builder()
            .add_source(config::File::with_name("config/default"))
            .add_source(config::Environment::with_prefix("APP"))
            .build()?;

        let config: Self = config.try_deserialize()?;
        config.validate()?;

        Ok(config)
    }

    pub fn validate(&self) -> Result<(), ConfigError> {
        if self.server.port == 0 {
            return Err(ConfigError::InvalidPort);
        }

        if self.database.max_connections == 0 {
            return Err(ConfigError::InvalidConnectionPool);
        }

        Ok(())
    }
}
```

## Service Container Pattern

### Dependency Injection Container

```rust
use async_trait::async_trait;

pub struct ServiceContainer {
    config: Arc<Config>,
    database: Arc<dyn DatabaseConnection>,
    cache: Arc<dyn CacheClient>,
    metrics: Arc<dyn MetricsCollector>,
}

#[async_trait]
pub trait DatabaseConnection: Send + Sync {
    async fn health_check(&self) -> Result<(), DatabaseError>;
    async fn get_connection(&self) -> Result<Connection, DatabaseError>;
}

impl ServiceContainer {
    pub async fn new(config: Config) -> Result<Self, ContainerError> {
        let config = Arc::new(config);

        let database = Arc::new(
            PostgresDatabase::connect(&config.database).await?
        );

        let cache = Arc::new(
            RedisCache::connect(&config.redis).await?
        );

        let metrics = Arc::new(PrometheusMetrics::new());

        Ok(Self {
            config,
            database,
            cache,
            metrics,
        })
    }

    pub fn user_service(&self) -> Arc<UserService> {
        Arc::new(UserService::new(
            self.database.clone(),
            self.cache.clone(),
            self.metrics.clone(),
        ))
    }

    pub fn into_app_state(self) -> AppState {
        AppState {
            database: self.database,
            cache: self.cache,
            config: self.config,
            user_service: self.user_service(),
        }
    }
}
```

## Best Practices

1. **Clear layer boundaries**: Each layer has a single responsibility
2. **Dependency direction**: Layers depend on abstractions, not implementations
3. **Explicit state**: Use AppState and FromRef for dependency management
4. **Middleware ordering**: Apply middleware in correct order (trace → auth → timeout)
5. **Modular routers**: Organize routes by domain/module
6. **Configuration validation**: Validate config at startup, fail fast
7. **Type-safe dependencies**: Use Arc<dyn Trait> for swappable implementations
8. **Health checks**: Verify all dependencies in health endpoints

## Common Dependencies

```toml
[dependencies]
axum = { version = "0.8", features = ["macros"] }
tower = { version = "0.5", features = ["full"] }
tower-http = { version = "0.6", features = [
    "trace", "timeout", "compression", "cors", "limit"
] }
config = "0.14"
serde = { version = "1", features = ["derive"] }
humantime-serde = "1"
```
