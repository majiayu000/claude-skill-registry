---
name: Tracing Observability
description: Structured logging and distributed tracing for Rust.
metadata:
  labels: [rust, tracing, logging, observability]
  triggers:
    files: ['**/main.rs', '**/lib.rs']
    keywords: [tracing, info, debug, span, instrument, subscriber]
---

# Tracing Standards

## Setup

```rust
use tracing::Level;
use tracing_subscriber::{fmt, prelude::*, EnvFilter};

fn main() {
    tracing_subscriber::registry()
        .with(fmt::layer())
        .with(EnvFilter::from_default_env()
            .add_directive(Level::INFO.into()))
        .init();

    tracing::info!("Application started");
}
```

## Log Levels

```rust
use tracing::{trace, debug, info, warn, error};

fn process() {
    trace!("Very detailed info");
    debug!("Debug information");
    info!("Normal operation");
    warn!("Warning condition");
    error!("Error occurred");
}
```

## Structured Fields

```rust
use tracing::{info, warn};

fn handle_request(user_id: u64, path: &str) {
    info!(user_id, path, "Processing request");

    // Named fields
    info!(
        user.id = user_id,
        request.path = path,
        request.method = "GET",
        "Request received"
    );

    // Debug formatting
    let data = vec![1, 2, 3];
    info!(?data, "Data received");

    // Display formatting
    let error = std::io::Error::new(std::io::ErrorKind::NotFound, "missing");
    warn!(%error, "Operation failed");
}
```

## Spans

```rust
use tracing::{span, Level, info_span};

fn process_order(order_id: u64) {
    let span = info_span!("process_order", order_id);
    let _guard = span.enter();

    // All logs within this scope include order_id
    tracing::info!("Starting order processing");
    validate_order();
    charge_payment();
    tracing::info!("Order completed");
}

// Async spans
async fn fetch_data() {
    let span = info_span!("fetch_data");
    async {
        // async work
    }.instrument(span).await;
}
```

## #[instrument] Macro

```rust
use tracing::instrument;

#[instrument]
fn calculate(x: i32, y: i32) -> i32 {
    x + y
}

// Skip sensitive fields
#[instrument(skip(password))]
fn login(username: &str, password: &str) -> bool {
    true
}

// Custom span name and level
#[instrument(name = "db_query", level = "debug")]
async fn query_database(sql: &str) -> Result<Vec<Row>, Error> {
    // ...
}

// Add fields
#[instrument(fields(request_id = %uuid::Uuid::new_v4()))]
async fn handle_request() {
    // ...
}

// Skip all, add specific
#[instrument(skip_all, fields(user_id))]
fn process_user(user_id: u64, sensitive_data: &str) {
    // ...
}
```

## Subscribers

```rust
use tracing_subscriber::{fmt, prelude::*, EnvFilter, Layer};

fn setup_tracing() {
    // JSON output for production
    let json_layer = fmt::layer()
        .json()
        .with_target(true)
        .with_current_span(true);

    // Pretty output for development
    let pretty_layer = fmt::layer()
        .pretty()
        .with_file(true)
        .with_line_number(true);

    // Filter by RUST_LOG env var
    let filter = EnvFilter::try_from_default_env()
        .unwrap_or_else(|_| EnvFilter::new("info"));

    tracing_subscriber::registry()
        .with(filter)
        .with(if cfg!(debug_assertions) {
            pretty_layer.boxed()
        } else {
            json_layer.boxed()
        })
        .init();
}
```

## OpenTelemetry Integration

```rust
use opentelemetry::sdk::trace::TracerProvider;
use tracing_opentelemetry::OpenTelemetryLayer;

fn setup_otel() {
    let provider = TracerProvider::builder()
        .with_simple_exporter(opentelemetry_jaeger::new_agent_pipeline())
        .build();

    let tracer = provider.tracer("my-service");

    tracing_subscriber::registry()
        .with(tracing_subscriber::fmt::layer())
        .with(OpenTelemetryLayer::new(tracer))
        .init();
}
```

## Error Handling

```rust
use tracing::{error, instrument};

#[instrument(err)]
fn fallible_operation() -> Result<(), Error> {
    // Automatically logs error if Err is returned
    Err(Error::new("something failed"))
}

// With error level
#[instrument(err(level = Level::WARN))]
fn maybe_warn() -> Result<(), Error> {
    // ...
}

// Manual error logging
fn handle_error() {
    if let Err(e) = operation() {
        error!(error = %e, "Operation failed");
    }
}
```

## Best Practices

1. **Structured logging**: Use fields, not string interpolation
2. **Span context**: Wrap related operations in spans
3. **Skip sensitive**: Use `skip` for passwords, tokens
4. **Env filter**: Configure via `RUST_LOG` env var
5. **Async**: Use `.instrument(span)` for async code
