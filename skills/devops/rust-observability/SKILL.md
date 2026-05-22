---
name: rust-observability
description: Production observability with tracing, OpenTelemetry, and Prometheus metrics including structured logging, instrumented functions, distributed tracing, health checks, and request correlation. Use when adding logging, metrics, tracing, or health endpoints to Rust services.
---

# Rust Observability

*Production observability with tracing, metrics, and structured logging*

## Version Context
- **tracing**: 0.1.x
- **tracing-subscriber**: 0.3.x
- **opentelemetry**: 0.26.x
- **metrics**: 0.24.x
- **metrics-exporter-prometheus**: 0.17.x

## When to Use This Skill

- Adding structured logging
- Instrumenting functions with traces
- Setting up OpenTelemetry
- Exposing Prometheus metrics
- Implementing health checks
- Request correlation and tracing
- Performance monitoring

## Structured Logging

### Basic Tracing Setup

```rust
use tracing::{info, warn, error, debug, trace};
use tracing_subscriber::{layer::SubscriberExt, util::SubscriberInitExt};

/// Initialize logging for development
pub fn init_tracing() {
    tracing_subscriber::registry()
        .with(
            tracing_subscriber::EnvFilter::try_from_default_env()
                .unwrap_or_else(|_| "info,my_app=debug".into())
        )
        .with(tracing_subscriber::fmt::layer())
        .init();
}

/// Initialize structured JSON logging for production
pub fn init_json_tracing() {
    tracing_subscriber::registry()
        .with(
            tracing_subscriber::EnvFilter::try_from_default_env()
                .unwrap_or_else(|_| "info".into())
        )
        .with(tracing_subscriber::fmt::layer().json())
        .init();
}

// Usage
fn main() {
    init_tracing();

    info!("Application starting");
    debug!(version = env!("CARGO_PKG_VERSION"), "Debug information");
    warn!(retry_count = 3, "Retry limit approaching");
    error!(error = "connection failed", "Database connection error");
}
```

### Instrumented Functions

```rust
use tracing::{instrument, info, Span};

/// Automatic span creation with function name
#[instrument]
async fn fetch_user(user_id: &str) -> Result<User, UserError> {
    info!("Fetching user from database");

    let user = db.find_user(user_id).await?;

    info!(email = %user.email, "User fetched successfully");

    Ok(user)
}

/// Custom span name and fields
#[instrument(
    name = "user.create",
    skip(db, payload),
    fields(
        user.email = %payload.email,
        user.name = %payload.name,
    )
)]
async fn create_user(
    db: &Database,
    payload: CreateUserRequest,
) -> Result<User, UserError> {
    let span = Span::current();

    let user = db.users.create(payload).await?;

    // Add fields dynamically
    span.record("user.id", &user.id.to_string());

    Ok(user)
}

/// Skip sensitive fields
#[instrument(skip(password))]
async fn authenticate(username: &str, password: &str) -> Result<Session, AuthError> {
    // password is not logged
    verify_credentials(username, password).await
}
```

## OpenTelemetry Integration

### Setup OpenTelemetry

```rust
use opentelemetry::{global, sdk::Resource, KeyValue};
use opentelemetry_otlp::WithExportConfig;
use tracing_subscriber::layer::SubscriberExt;
use tracing_opentelemetry::OpenTelemetryLayer;

pub fn init_telemetry() -> Result<(), Box<dyn std::error::Error>> {
    // Configure OpenTelemetry
    global::set_text_map_propagator(
        opentelemetry::sdk::propagation::TraceContextPropagator::new()
    );

    // Create OTLP exporter
    let tracer = opentelemetry_otlp::new_pipeline()
        .tracing()
        .with_exporter(
            opentelemetry_otlp::new_exporter()
                .tonic()
                .with_endpoint("http://localhost:4317")
        )
        .with_trace_config(
            opentelemetry::sdk::trace::config().with_resource(Resource::new(vec![
                KeyValue::new("service.name", "my-service"),
                KeyValue::new("service.version", env!("CARGO_PKG_VERSION")),
                KeyValue::new("deployment.environment", "production"),
            ]))
        )
        .install_batch(opentelemetry::runtime::Tokio)?;

    // Configure tracing subscriber with OpenTelemetry layer
    tracing_subscriber::registry()
        .with(
            tracing_subscriber::EnvFilter::try_from_default_env()
                .unwrap_or_else(|_| "info".into())
        )
        .with(tracing_subscriber::fmt::layer())
        .with(OpenTelemetryLayer::new(tracer))
        .init();

    Ok(())
}

// Shutdown gracefully
pub fn shutdown_telemetry() {
    global::shutdown_tracer_provider();
}
```

## Prometheus Metrics

### Initialize Metrics

```rust
use metrics::{counter, gauge, histogram, describe_counter, describe_histogram, Unit};
use metrics_exporter_prometheus::PrometheusBuilder;

/// Initialize Prometheus metrics
pub fn init_metrics() -> Result<(), Box<dyn std::error::Error>> {
    PrometheusBuilder::new()
        .with_http_listener(([0, 0, 0, 0], 9090))
        .install()?;

    // Describe metrics
    describe_counter!(
        "http_requests_total",
        Unit::Count,
        "Total HTTP requests"
    );

    describe_histogram!(
        "http_request_duration_seconds",
        Unit::Seconds,
        "HTTP request duration"
    );

    describe_counter!(
        "users_created_total",
        Unit::Count,
        "Total users created"
    );

    Ok(())
}
```

### Usage in Handlers

```rust
#[instrument(skip(state))]
async fn create_user(
    State(state): State<Arc<AppState>>,
    Json(payload): Json<CreateUserRequest>,
) -> Result<Json<User>, AppError> {
    // Increment counter
    counter!("http_requests_total", "method" => "POST", "endpoint" => "/users").increment(1);

    let start = std::time::Instant::now();

    let user = state.user_service.create_user(payload).await?;

    // Record histogram
    let duration = start.elapsed();
    histogram!(
        "http_request_duration_seconds",
        "method" => "POST",
        "endpoint" => "/users",
        "status" => "200"
    ).record(duration.as_secs_f64());

    // Business metric
    counter!("users_created_total", "source" => "api").increment(1);

    Ok(Json(user))
}
```

## Health Checks

### Health Endpoint

```rust
use axum::{extract::State, response::Json, http::StatusCode};
use serde_json::json;

#[derive(serde::Serialize)]
pub struct HealthResponse {
    status: String,
    version: String,
    checks: Vec<HealthCheck>,
}

#[derive(serde::Serialize)]
pub struct HealthCheck {
    name: String,
    status: String,
    duration_ms: u64,
}

#[instrument(skip(state))]
pub async fn health_check(
    State(state): State<Arc<AppState>>,
) -> Result<Json<HealthResponse>, StatusCode> {
    let mut checks = Vec::new();
    let mut all_healthy = true;

    // Database health check
    let start = std::time::Instant::now();
    let db_healthy = state.database.ping().await.is_ok();
    checks.push(HealthCheck {
        name: "database".to_string(),
        status: if db_healthy { "healthy" } else { "unhealthy" }.to_string(),
        duration_ms: start.elapsed().as_millis() as u64,
    });
    all_healthy &= db_healthy;

    // Cache health check
    let start = std::time::Instant::now();
    let cache_healthy = state.cache.ping().await.is_ok();
    checks.push(HealthCheck {
        name: "cache".to_string(),
        status: if cache_healthy { "healthy" } else { "unhealthy" }.to_string(),
        duration_ms: start.elapsed().as_millis() as u64,
    });
    all_healthy &= cache_healthy;

    let response = HealthResponse {
        status: if all_healthy { "healthy" } else { "unhealthy" }.to_string(),
        version: env!("CARGO_PKG_VERSION").to_string(),
        checks,
    };

    if all_healthy {
        Ok(Json(response))
    } else {
        Err(StatusCode::SERVICE_UNAVAILABLE)
    }
}

/// Readiness check (Kubernetes)
#[instrument(skip(state))]
pub async fn readiness_check(
    State(state): State<Arc<AppState>>,
) -> Result<StatusCode, StatusCode> {
    // Quick check if ready to serve traffic
    if state.database.ping().await.is_ok() {
        Ok(StatusCode::OK)
    } else {
        Err(StatusCode::SERVICE_UNAVAILABLE)
    }
}
```

## Request Correlation

### Request ID Middleware

```rust
use axum::{
    extract::Request,
    middleware::Next,
    response::Response,
};
use uuid::Uuid;

#[derive(Clone, Debug)]
pub struct RequestId(pub Uuid);

pub async fn request_id_middleware(
    mut request: Request,
    next: Next,
) -> Response {
    // Extract or generate request ID
    let request_id = request
        .headers()
        .get("x-request-id")
        .and_then(|h| h.to_str().ok())
        .and_then(|s| Uuid::parse_str(s).ok())
        .unwrap_or_else(Uuid::new_v4);

    // Add to extensions
    request.extensions_mut().insert(RequestId(request_id));

    // Create span with request ID
    let span = info_span!(
        "http_request",
        request_id = %request_id,
        method = %request.method(),
        uri = %request.uri(),
    );

    let _guard = span.enter();

    info!("Request started");

    let mut response = next.run(request).await;

    // Add to response headers
    response.headers_mut().insert(
        "x-request-id",
        request_id.to_string().parse().unwrap(),
    );

    info!("Request completed");

    response
}
```

## Best Practices

1. **Use structured fields**: Log key-value pairs, not formatted strings
2. **Instrument at boundaries**: HTTP handlers, database calls, external services
3. **Set appropriate levels**: ERROR for failures, WARN for issues, INFO for important events
4. **Include correlation IDs**: Request IDs, trace IDs, user IDs
5. **Record durations**: Use histogram metrics for timing
6. **Implement health checks**: /health and /ready endpoints
7. **Expose metrics**: Prometheus endpoint on separate port
8. **Skip sensitive data**: Don't log passwords, tokens, PII
9. **Use spans for context**: Group related logs with spans

## Common Dependencies

```toml
[dependencies]
# Tracing
tracing = "0.1"
tracing-subscriber = { version = "0.3", features = ["json", "env-filter"] }
tracing-opentelemetry = "0.27"

# OpenTelemetry
opentelemetry = { version = "0.26", features = ["trace"] }
opentelemetry-otlp = { version = "0.26", features = ["trace"] }

# Metrics
metrics = "0.24"
metrics-exporter-prometheus = "0.17"

# Utilities
uuid = { version = "1", features = ["v4", "serde"] }
```
