---
name: rust-tracing
description: Structured logging with tracing and tracing-subscriber
triggers:
  - tracing
  - logging
  - info!
  - debug!
  - error!
  - warn!
  - trace!
  - span
  - "#[instrument]"
  - subscriber
  - EnvFilter
  - RUST_LOG
---

# rust-tracing

Structured logging and diagnostics for Rust applications using the `tracing` ecosystem.

## Why tracing over log?

| Feature | `log` | `tracing` |
|---------|-------|-----------|
| Structured fields | Limited | Native support |
| Spans (context) | No | Yes - track execution flow |
| Async-aware | No | Yes - spans work across await points |
| Performance | Good | Better - compile-time filtering |
| Composable output | No | Yes - multiple subscribers/layers |

`tracing` provides **spans** (periods of time) and **events** (moments in time), enabling you to track execution flow through async code and attach structured context to all logs within a scope.

## Key Macros

### Event Macros (moments in time)

```rust
use tracing::{trace, debug, info, warn, error};

// Basic usage
info!("Application started");
error!("Connection failed");

// With structured fields (key = value)
info!(user = "alice", action = "login", "User logged in");
debug!(bytes = 1024, duration_ms = 42, "Request completed");

// With Display formatting (%)
warn!(path = %file_path.display(), "File not found");

// With Debug formatting (?)
error!(error = ?e, "Operation failed");

// Field shorthand (variable name = field name)
let user_id = 42;
info!(user_id, "Processing request");  // Same as: user_id = user_id
```

### Span Macros (periods of time)

```rust
use tracing::{span, trace_span, debug_span, info_span, warn_span, error_span, Level};

// Create a span
let span = info_span!("process_request", request_id = 42);

// Enter the span (RAII guard)
let _guard = span.enter();
// All events here are within the span

// Alternative: in_scope for synchronous code
info_span!("json_parse").in_scope(|| {
    serde_json::from_str(&data)
})
```

## Spans

### Manual Span Management

```rust
use tracing::{span, Level};

let span = span!(Level::INFO, "my_operation", id = 123);
let _enter = span.enter();

// Work happens here, within the span context
info!("Working...");  // This event is associated with the span

// Span exits when _enter is dropped
```

### The `#[instrument]` Attribute

Automatically creates spans for functions:

```rust
use tracing::instrument;

// Basic - creates span with function name
#[instrument]
pub fn process_request(id: u32) {
    info!("Processing");
}

// Skip sensitive or large arguments
#[instrument(skip(password, large_data))]
pub fn authenticate(user: &str, password: &str, large_data: &[u8]) {
    // ...
}

// Custom span name and level
#[instrument(name = "handle_req", level = "debug")]
pub fn handler(req: Request) {
    // ...
}

// Add computed fields
#[instrument(fields(request_id = %req.id()))]
pub fn process(req: &Request) {
    // ...
}

// For async functions - works across await points
#[instrument]
pub async fn async_operation() {
    // Span stays active across awaits
    some_async_call().await;
}
```

### Recording Dynamic Values in Spans

```rust
use tracing::{info_span, field};

// Declare field with Empty, record later
let span = info_span!("request", status = field::Empty);
let _guard = span.enter();

// ... do work ...

// Record the value later
span.record("status", 200);
```

## Subscriber Setup

### Basic Setup (script-kit-gpui pattern)

```rust
use tracing_subscriber::{
    fmt::{self, format::FmtSpan},
    layer::SubscriberExt,
    util::SubscriberInitExt,
    EnvFilter,
};

pub fn init_logging() {
    // Environment filter with sensible defaults
    let env_filter = EnvFilter::try_from_default_env()
        .unwrap_or_else(|_| EnvFilter::new("info,gpui=warn,hyper=warn"));

    tracing_subscriber::registry()
        .with(env_filter)
        .with(fmt::layer().with_target(true).compact())
        .init();
}
```

### Multi-Output Setup (JSON file + pretty stderr)

This is the pattern used in script-kit-gpui:

```rust
use tracing_subscriber::{
    fmt::{self, format::FmtSpan, MakeWriter},
    layer::SubscriberExt,
    registry::LookupSpan,
    util::SubscriberInitExt,
    EnvFilter,
};
use tracing_appender::non_blocking::WorkerGuard;
use std::fs::OpenOptions;

pub struct LoggingGuard {
    _file_guard: WorkerGuard,
}

pub fn init() -> LoggingGuard {
    let log_path = dirs::home_dir()
        .unwrap()
        .join(".myapp/logs/app.jsonl");
    
    let file = OpenOptions::new()
        .create(true)
        .append(true)
        .open(&log_path)
        .unwrap();

    // Non-blocking writer prevents UI freeze
    let (non_blocking_file, file_guard) = tracing_appender::non_blocking(file);

    let env_filter = EnvFilter::try_from_default_env()
        .unwrap_or_else(|_| EnvFilter::new("info,gpui=warn,hyper=warn"));

    // JSON layer for file output (machine-readable)
    let json_layer = fmt::layer()
        .json()
        .with_writer(non_blocking_file)
        .with_timer(fmt::time::UtcTime::rfc_3339())
        .with_target(true)
        .with_level(true)
        .with_span_events(FmtSpan::NONE);

    // Pretty layer for stderr (human-readable)
    let pretty_layer = fmt::layer()
        .with_writer(std::io::stderr)
        .with_ansi(true)
        .with_target(true)
        .compact();

    tracing_subscriber::registry()
        .with(env_filter)
        .with(json_layer)
        .with(pretty_layer)
        .init();

    LoggingGuard { _file_guard: file_guard }
}
```

**Critical**: Keep the `LoggingGuard` alive for the entire program! Dropping it stops logging.

## Usage in script-kit-gpui

### Cargo.toml Dependencies

```toml
tracing = "0.1"
tracing-subscriber = { version = "0.3", features = ["json", "env-filter", "time"] }
tracing-appender = "0.2"
```

### Common Patterns

```rust
// Module-level import
use tracing::{debug, error, info, warn};

// Simple events with structured fields
info!(
    event_type = "app_lifecycle",
    action = "started",
    log_path = %log_path.display(),
    "Application started"
);

// Error logging with context
error!(
    path = %theme_path.display(),
    error = %e,
    "Failed to read theme file"
);

// Conditional debug logging
debug!(path = %script_path.display(), "Using development script path");

// Warning with structured data
warn!(
    error = %e,
    "Auto-save failed"
);
```

### Function Instrumentation

```rust
use tracing::{info, instrument};

#[instrument]
pub fn get_all_displays() -> Result<Vec<DisplayInfo>> {
    // Automatically creates span "get_all_displays"
    info!(display_count = displays.len(), "Got all displays");
    Ok(displays)
}

#[instrument(skip_all, fields(query = %query, limit = limit))]
pub fn search_files(query: &str, onlyin: Option<&str>, limit: usize) -> Vec<FileResult> {
    debug!("Starting mdfind search");
    // ...
}
```

## Filtering

### RUST_LOG Environment Variable

```bash
# Set default level
RUST_LOG=info ./myapp

# Per-module filtering
RUST_LOG=myapp=debug,gpui=warn ./myapp

# Multiple targets
RUST_LOG=myapp::logging=trace,myapp::ui=debug ./myapp

# With spans
RUST_LOG=myapp[span_name]=trace ./myapp

# Regex patterns (with regex feature)
RUST_LOG="myapp::api.*=debug" ./myapp
```

### EnvFilter Syntax

```rust
use tracing_subscriber::EnvFilter;

// From environment or default
let filter = EnvFilter::try_from_default_env()
    .unwrap_or_else(|_| EnvFilter::new("info"));

// Programmatic construction
let filter = EnvFilter::new("info")
    .add_directive("gpui=warn".parse().unwrap())
    .add_directive("hyper=warn".parse().unwrap());
```

### Common Filter Patterns

| Pattern | Effect |
|---------|--------|
| `info` | All targets at INFO |
| `myapp=debug` | myapp crate at DEBUG |
| `warn,myapp=info` | Default WARN, myapp at INFO |
| `myapp::module=trace` | Specific module at TRACE |
| `[span_name]=debug` | Spans named "span_name" at DEBUG |

## Performance

### Compile-Time Filtering

```toml
# Cargo.toml - disable levels at compile time
[dependencies]
tracing = { version = "0.1", features = ["release_max_level_info"] }
```

Available features:
- `max_level_off` / `release_max_level_off`
- `max_level_error` / `release_max_level_error`
- `max_level_warn` / `release_max_level_warn`
- `max_level_info` / `release_max_level_info`
- `max_level_debug` / `release_max_level_debug`
- `max_level_trace` / `release_max_level_trace`

### Conditional Compilation Pattern (script-kit-gpui)

```rust
// Debug-only logging
#[cfg(debug_assertions)]
pub fn log_debug(category: &str, message: &str) {
    tracing::debug!(category = category, "{}", message);
}

#[cfg(not(debug_assertions))]
pub fn log_debug(_category: &str, _message: &str) {
    // No-op in release builds
}
```

### Non-Blocking File Output

Always use `tracing_appender::non_blocking` for file output to prevent blocking the main thread:

```rust
let (non_blocking, guard) = tracing_appender::non_blocking(file);
// Keep guard alive!
```

## Anti-patterns

### 1. Dropping the Guard

```rust
// BAD: Guard dropped immediately, logging stops
fn init() {
    let (non_blocking, _guard) = tracing_appender::non_blocking(file);
    // _guard dropped here!
}

// GOOD: Return and store the guard
fn init() -> WorkerGuard {
    let (non_blocking, guard) = tracing_appender::non_blocking(file);
    // ... setup ...
    guard  // Caller must keep this alive
}
```

### 2. Span::enter() in Async Code

```rust
// BAD: Guard held across await point
async fn bad_async() {
    let span = info_span!("work");
    let _guard = span.enter();  // DON'T DO THIS
    async_operation().await;    // Guard still held!
}

// GOOD: Use instrument attribute
#[instrument]
async fn good_async() {
    async_operation().await;
}

// GOOD: Or use in_scope for sync portions
async fn also_good() {
    let result = info_span!("sync_work").in_scope(|| {
        sync_operation()
    });
    async_operation().await;
}
```

### 3. Logging Sensitive Data

```rust
// BAD: Password in logs
info!(password = password, "Login attempt");

// GOOD: Skip sensitive fields
#[instrument(skip(password))]
fn login(user: &str, password: &str) {
    info!("Login attempt");
}

// GOOD: Use field::Empty and record sanitized version
info!(password = "[REDACTED]", "Login attempt");
```

### 4. Excessive Allocations

```rust
// BAD: Allocates even if debug is disabled
debug!("Data: {}", expensive_format(&large_data));

// GOOD: Use structured fields - no allocation if level disabled
debug!(data = ?large_data, "Processing");

// GOOD: Use Display/Debug sigils
debug!(data = %large_data.len(), "Data size");
```

### 5. Not Filtering Noisy Dependencies

```rust
// BAD: All output at same level
let filter = EnvFilter::new("debug");

// GOOD: Filter noisy crates
let filter = EnvFilter::new("debug,hyper=warn,reqwest=warn,gpui=warn");
```

## Quick Reference

```rust
// Event macros (levels)
trace!(...);  // Most verbose
debug!(...);
info!(...);
warn!(...);
error!(...);  // Most important

// Span macros
trace_span!("name", field = value);
debug_span!("name");
info_span!("name");
warn_span!("name");
error_span!("name");

// Field formatting
info!(plain = value);           // Value trait
info!(debug = ?value);          // Debug trait
info!(display = %value);        // Display trait
info!(shorthand);               // Same as: shorthand = shorthand

// Instrument attribute
#[instrument]                   // Basic
#[instrument(skip(arg))]        // Skip arguments
#[instrument(level = "debug")]  // Custom level
#[instrument(name = "custom")]  // Custom span name
#[instrument(fields(f = %v))]   // Custom fields
```
