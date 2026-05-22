---
name: rust-production-reliability
description: Production reliability patterns including circuit breakers with exponential backoff, graceful shutdown management with signal handling, retry logic with jitter, rate limiting with token bucket, and security best practices. Use when hardening services for production, implementing fault tolerance, adding retry logic, or ensuring graceful degradation.
---

# Rust Production Reliability

*Production hardening patterns for fault-tolerant, reliable services*

## Version Context
- **Tokio**: 1.48.0
- **Tower**: 0.5.2

## When to Use This Skill

- Hardening services for production
- Implementing fault tolerance
- Adding retry logic with backoff
- Graceful shutdown coordination
- Rate limiting and load shedding
- Circuit breaker patterns
- Security hardening

## Circuit Breaker Pattern

### Basic Circuit Breaker

```rust
use std::sync::Arc;
use std::sync::atomic::{AtomicU32, AtomicU8, Ordering};
use std::time::{Duration, Instant};
use tokio::sync::RwLock;

#[derive(Clone)]
pub struct CircuitBreaker {
    max_failures: u32,
    failure_count: Arc<AtomicU32>,
    state: Arc<AtomicU8>, // 0=Closed, 1=Open, 2=HalfOpen
    last_failure_time: Arc<RwLock<Option<Instant>>>,
    timeout: Duration,
}

impl CircuitBreaker {
    const CLOSED: u8 = 0;
    const OPEN: u8 = 1;
    const HALF_OPEN: u8 = 2;

    pub fn new(max_failures: u32, timeout: Duration) -> Self {
        Self {
            max_failures,
            failure_count: Arc::new(AtomicU32::new(0)),
            state: Arc::new(AtomicU8::new(Self::CLOSED)),
            last_failure_time: Arc::new(RwLock::new(None)),
            timeout,
        }
    }

    /// Execute function with circuit breaker protection
    pub async fn call<F, T, E>(&self, f: F) -> Result<T, CircuitBreakerError<E>>
    where
        F: std::future::Future<Output = Result<T, E>>,
    {
        // Check if circuit should transition to half-open
        if self.state.load(Ordering::SeqCst) == Self::OPEN {
            let last_failure = *self.last_failure_time.read().await;
            if let Some(last_failure) = last_failure {
                if last_failure.elapsed() > self.timeout {
                    self.state.store(Self::HALF_OPEN, Ordering::SeqCst);
                } else {
                    return Err(CircuitBreakerError::CircuitOpen);
                }
            }
        }

        // Execute the function
        match f.await {
            Ok(result) => {
                // Success: reset failure count and close circuit
                self.failure_count.store(0, Ordering::SeqCst);
                self.state.store(Self::CLOSED, Ordering::SeqCst);
                Ok(result)
            }
            Err(e) => {
                // Failure: increment count and potentially open circuit
                let failures = self.failure_count.fetch_add(1, Ordering::SeqCst) + 1;
                *self.last_failure_time.write().await = Some(Instant::now());

                if failures >= self.max_failures {
                    self.state.store(Self::OPEN, Ordering::SeqCst);
                }

                Err(CircuitBreakerError::OperationFailed(e))
            }
        }
    }
}

#[derive(Debug, thiserror::Error)]
pub enum CircuitBreakerError<E> {
    #[error("circuit breaker is open")]
    CircuitOpen,
    #[error("operation failed")]
    OperationFailed(E),
}
```

## Graceful Shutdown

### Shutdown Manager

```rust
use tokio::sync::broadcast;
use tokio::task::JoinSet;
use std::time::Duration;

pub struct ShutdownManager {
    shutdown_tx: broadcast::Sender<()>,
    tasks: JoinSet<Result<(), Box<dyn std::error::Error + Send + Sync>>>,
}

impl ShutdownManager {
    pub fn new() -> Self {
        let (shutdown_tx, _) = broadcast::channel(1);
        Self {
            shutdown_tx,
            tasks: JoinSet::new(),
        }
    }

    /// Spawn a task with shutdown signal integration
    pub fn spawn_task<F, Fut>(&mut self, task: F)
    where
        F: FnOnce(broadcast::Receiver<()>) -> Fut + Send + 'static,
        Fut: std::future::Future<Output = Result<(), Box<dyn std::error::Error + Send + Sync>>> + Send + 'static,
    {
        let shutdown_rx = self.shutdown_tx.subscribe();
        self.tasks.spawn(task(shutdown_rx));
    }

    /// Initiate graceful shutdown with timeout
    pub async fn shutdown(mut self, timeout: Duration) -> Result<(), ShutdownError> {
        // Send shutdown signal to all tasks
        if let Err(_) = self.shutdown_tx.send(()) {
            tracing::warn!("no tasks listening for shutdown signal");
        }

        // Wait for all tasks to complete with timeout
        let start = Instant::now();
        let mut failed_tasks = Vec::new();

        while let Some(result) = self.tasks.join_next().await {
            if start.elapsed() > timeout {
                failed_tasks.push("timeout exceeded".to_string());
                break;
            }

            match result {
                Ok(Ok(())) => {
                    tracing::info!("task completed successfully");
                }
                Ok(Err(e)) => {
                    tracing::error!(error = %e, "task failed during shutdown");
                    failed_tasks.push(e.to_string());
                }
                Err(e) => {
                    tracing::error!(error = %e, "task panicked during shutdown");
                    failed_tasks.push(e.to_string());
                }
            }
        }

        if failed_tasks.is_empty() {
            tracing::info!("graceful shutdown completed successfully");
            Ok(())
        } else {
            Err(ShutdownError::TasksFailed(failed_tasks))
        }
    }
}

#[derive(Debug, thiserror::Error)]
pub enum ShutdownError {
    #[error("tasks failed during shutdown: {0:?}")]
    TasksFailed(Vec<String>),
}
```

### Signal Handling

```rust
use std::future;
use tokio::signal;

pub async fn shutdown_signal() {
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
    let terminate = future::pending::<()>();

    tokio::select! {
        _ = ctrl_c => {
            tracing::info!("received Ctrl+C signal");
        },
        _ = terminate => {
            tracing::info!("received SIGTERM signal");
        },
    }
}

// Usage in main
#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let listener = TcpListener::bind("0.0.0.0:3000").await?;

    axum::serve(listener, app)
        .with_graceful_shutdown(shutdown_signal())
        .await?;

    Ok(())
}
```

## Retry Logic

### Exponential Backoff with Jitter

```rust
use std::time::Duration;
use rand::Rng;

pub struct RetryPolicy {
    max_retries: u32,
    initial_delay: Duration,
    max_delay: Duration,
    multiplier: f64,
    jitter: bool,
}

impl RetryPolicy {
    pub fn new() -> Self {
        Self {
            max_retries: 3,
            initial_delay: Duration::from_millis(100),
            max_delay: Duration::from_secs(60),
            multiplier: 2.0,
            jitter: true,
        }
    }

    pub async fn execute<F, T, E>(&self, mut operation: F) -> Result<T, E>
    where
        F: FnMut() -> std::pin::Pin<Box<dyn std::future::Future<Output = Result<T, E>> + Send>>,
        E: std::fmt::Display,
    {
        let mut attempt = 0;

        loop {
            match operation().await {
                Ok(result) => return Ok(result),
                Err(e) if attempt >= self.max_retries => {
                    tracing::error!(
                        error = %e,
                        attempts = attempt + 1,
                        "operation failed after max retries"
                    );
                    return Err(e);
                }
                Err(e) => {
                    let delay = self.calculate_delay(attempt);

                    tracing::warn!(
                        error = %e,
                        attempt = attempt + 1,
                        delay_ms = delay.as_millis(),
                        "operation failed, retrying"
                    );

                    tokio::time::sleep(delay).await;
                    attempt += 1;
                }
            }
        }
    }

    fn calculate_delay(&self, attempt: u32) -> Duration {
        let base_delay = self.initial_delay.as_secs_f64()
            * self.multiplier.powi(attempt as i32);

        let delay = Duration::from_secs_f64(
            base_delay.min(self.max_delay.as_secs_f64())
        );

        if self.jitter {
            let jitter = rand::thread_rng().gen_range(0.0..=0.1);
            Duration::from_secs_f64(
                delay.as_secs_f64() * (1.0 + jitter)
            )
        } else {
            delay
        }
    }
}

// Usage
async fn fetch_with_retry(url: &str) -> Result<String, reqwest::Error> {
    let retry_policy = RetryPolicy::new();

    retry_policy.execute(|| {
        Box::pin(async move {
            reqwest::get(url).await?.text().await
        })
    }).await
}
```

## Rate Limiting

### Token Bucket Implementation

```rust
use std::sync::atomic::{AtomicU64, Ordering};
use std::time::{SystemTime, UNIX_EPOCH};

pub struct TokenBucket {
    max_tokens: u64,
    tokens: AtomicU64,
    refill_rate: u64, // tokens per second
    last_refill: AtomicU64, // timestamp in milliseconds
}

impl TokenBucket {
    pub fn new(refill_rate: u64, max_tokens: u64) -> Self {
        let now = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .unwrap()
            .as_millis() as u64;

        Self {
            max_tokens,
            tokens: AtomicU64::new(max_tokens),
            refill_rate,
            last_refill: AtomicU64::new(now),
        }
    }

    pub fn try_acquire(&self) -> bool {
        self.refill();

        let current_tokens = self.tokens.load(Ordering::SeqCst);
        if current_tokens > 0 {
            match self.tokens.compare_exchange_weak(
                current_tokens,
                current_tokens - 1,
                Ordering::SeqCst,
                Ordering::SeqCst,
            ) {
                Ok(_) => true,
                Err(_) => false, // Another thread consumed the token
            }
        } else {
            false
        }
    }

    fn refill(&self) {
        let now = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .unwrap()
            .as_millis() as u64;

        let last_refill = self.last_refill.load(Ordering::SeqCst);
        let time_passed = now - last_refill;

        if time_passed >= 1000 { // At least 1 second passed
            let tokens_to_add = (time_passed / 1000) * self.refill_rate;

            if tokens_to_add > 0 {
                let current_tokens = self.tokens.load(Ordering::SeqCst);
                let new_tokens = (current_tokens + tokens_to_add).min(self.max_tokens);

                self.tokens.store(new_tokens, Ordering::SeqCst);
                self.last_refill.store(now, Ordering::SeqCst);
            }
        }
    }
}

// Axum middleware integration
pub async fn rate_limit_middleware(
    State(rate_limiter): State<Arc<TokenBucket>>,
    request: Request,
    next: Next,
) -> Result<Response, StatusCode> {
    if !rate_limiter.try_acquire() {
        tracing::warn!("rate limit exceeded");
        return Err(StatusCode::TOO_MANY_REQUESTS);
    }

    Ok(next.run(request).await)
}
```

## Concurrency Control

### Semaphore for Bounded Concurrency

```rust
use tokio::sync::Semaphore;
use std::sync::Arc;

pub struct ConcurrentProcessor<T> {
    semaphore: Arc<Semaphore>,
    processor: Arc<dyn Fn(T) -> Result<(), ProcessError> + Send + Sync>,
}

impl<T> ConcurrentProcessor<T>
where
    T: Send + 'static,
{
    pub fn new<F>(max_concurrent: usize, processor: F) -> Self
    where
        F: Fn(T) -> Result<(), ProcessError> + Send + Sync + 'static,
    {
        Self {
            semaphore: Arc::new(Semaphore::new(max_concurrent)),
            processor: Arc::new(processor),
        }
    }

    pub async fn process(&self, item: T) -> Result<(), ProcessError> {
        let _permit = self.semaphore.acquire().await.unwrap();
        (self.processor)(item)
    }
}
```

## Timeout Management

### Composite Timeout Strategy

```rust
use tokio::time::{timeout, Duration};

pub async fn with_timeout<F, T>(
    operation: F,
    duration: Duration,
) -> Result<T, TimeoutError>
where
    F: std::future::Future<Output = Result<T, Box<dyn std::error::Error>>>,
{
    match timeout(duration, operation).await {
        Ok(Ok(result)) => Ok(result),
        Ok(Err(e)) => Err(TimeoutError::OperationFailed(e.to_string())),
        Err(_) => Err(TimeoutError::Timeout),
    }
}

#[derive(Debug, thiserror::Error)]
pub enum TimeoutError {
    #[error("operation timed out")]
    Timeout,
    #[error("operation failed: {0}")]
    OperationFailed(String),
}
```

## Health Checks

### Comprehensive Health Check

```rust
use axum::{extract::State, response::Json, http::StatusCode};

#[instrument(skip(state))]
pub async fn health_check(
    State(state): State<Arc<AppState>>,
) -> Result<Json<serde_json::Value>, StatusCode> {
    let mut checks = Vec::new();
    let mut overall_healthy = true;

    // Database health check with timeout
    let db_health = tokio::time::timeout(
        Duration::from_secs(5),
        check_database(&state.database)
    ).await
    .unwrap_or_else(|_| HealthCheckResult {
        name: "database".to_string(),
        is_healthy: false,
        message: Some("timeout".to_string()),
        duration_ms: 5000,
    });

    overall_healthy &= db_health.is_healthy;
    checks.push(db_health);

    let status = if overall_healthy { "healthy" } else { "unhealthy" };
    let http_status = if overall_healthy { StatusCode::OK } else { StatusCode::SERVICE_UNAVAILABLE };

    let response = json!({
        "status": status,
        "checks": checks,
        "timestamp": chrono::Utc::now(),
    });

    match http_status {
        StatusCode::OK => Ok(Json(response)),
        _ => Err(http_status),
    }
}
```

## Best Practices

1. **Circuit breakers** for external service calls
2. **Exponential backoff with jitter** for retries
3. **Graceful shutdown** with signal handling
4. **Rate limiting** to prevent overload
5. **Timeout all I/O** operations
6. **Bound concurrency** with semaphores
7. **Health checks** for all dependencies
8. **Metrics** for observability

## Common Dependencies

```toml
[dependencies]
tokio = { version = "1", features = ["full"] }
tower = { version = "0.5", features = ["timeout", "limit", "retry"] }
thiserror = "2"
tracing = "0.1"
rand = "0.8"
```
