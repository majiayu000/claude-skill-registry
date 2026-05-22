---
name: rust-async-runtime
description: Production patterns for Tokio 1.48.0 async runtime including task spawning, channels (mpsc, oneshot, broadcast, watch), synchronization primitives, graceful shutdown, and lifecycle management. Use when spawning background tasks, managing concurrency, implementing graceful shutdown, or coordinating async work.
---

# Rust Async Runtime

*Production patterns for Tokio async runtime with task management and lifecycle control*

## Version Context
- **Tokio**: 1.48.0 (latest)
- **Futures**: 0.3.x
- **Async-trait**: 0.1.x

## When to Use This Skill

- Spawning background tasks
- Managing concurrent operations
- Implementing graceful shutdown
- Using channels for communication
- Coordinating async work
- CPU-bound work in async context
- Task cancellation and cleanup

## Task Management

### Spawning Tasks

```rust
use tokio::task;

// Spawn a task on the runtime
async fn spawn_example() {
    let handle = task::spawn(async {
        expensive_operation().await
    });

    // Wait for completion
    let result = handle.await.unwrap();
}

// Spawn blocking work (CPU-bound)
async fn spawn_blocking_example() {
    let result = task::spawn_blocking(|| {
        // CPU-intensive work that would block async runtime
        compute_fibonacci(40)
    }).await.unwrap();
}
```

### Task Tracking with JoinSet

```rust
use tokio::task::JoinSet;

/// Track multiple tasks with JoinSet
async fn join_set_example() {
    let mut set = JoinSet::new();

    // Spawn multiple tasks
    for i in 0..10 {
        set.spawn(async move {
            sleep(Duration::from_secs(i)).await;
            i * 2
        });
    }

    // Wait for all tasks
    while let Some(res) = set.join_next().await {
        match res {
            Ok(value) => println!("Task completed: {}", value),
            Err(e) => eprintln!("Task failed: {}", e),
        }
    }
}
```

## Channels

### Multi-Producer Single-Consumer (mpsc)

```rust
use tokio::sync::mpsc;

async fn mpsc_example() {
    let (tx, mut rx) = mpsc::channel(100);

    // Spawn producers
    for i in 0..3 {
        let tx = tx.clone();
        task::spawn(async move {
            tx.send(i).await.unwrap();
        });
    }

    drop(tx); // Drop original sender

    // Consumer
    while let Some(value) = rx.recv().await {
        println!("Received: {}", value);
    }
}
```

### Oneshot Channel (Single Value)

```rust
use tokio::sync::oneshot;

async fn oneshot_example() {
    let (tx, rx) = oneshot::channel();

    task::spawn(async move {
        tx.send(42).unwrap();
    });

    let value = rx.await.unwrap();
    println!("Received: {}", value);
}
```

### Broadcast Channel (Multiple Consumers)

```rust
use tokio::sync::broadcast;

async fn broadcast_example() {
    let (tx, mut rx1) = broadcast::channel(16);
    let mut rx2 = tx.subscribe();

    task::spawn(async move {
        tx.send(10).unwrap();
        tx.send(20).unwrap();
    });

    assert_eq!(rx1.recv().await.unwrap(), 10);
    assert_eq!(rx2.recv().await.unwrap(), 10);
}
```

### Watch Channel (Always Latest Value)

```rust
use tokio::sync::watch;

async fn watch_example() {
    let (tx, mut rx) = watch::channel(0);

    task::spawn(async move {
        tx.send(10).unwrap();
        tx.send(20).unwrap();
    });

    rx.changed().await.unwrap();
    println!("Latest value: {}", *rx.borrow());
}
```

## Synchronization

### Async Mutex

```rust
use tokio::sync::Mutex;
use std::sync::Arc;

async fn mutex_example() {
    let data = Arc::new(Mutex::new(0));

    let mut handles = vec![];

    for _ in 0..10 {
        let data = Arc::clone(&data);
        let handle = task::spawn(async move {
            let mut lock = data.lock().await;
            *lock += 1;
        });
        handles.push(handle);
    }

    for handle in handles {
        handle.await.unwrap();
    }

    println!("Final value: {}", *data.lock().await);
}
```

### Semaphore for Bounded Concurrency

```rust
use tokio::sync::Semaphore;
use std::sync::Arc;

async fn semaphore_example() {
    let semaphore = Arc::new(Semaphore::new(3)); // Max 3 concurrent

    let mut handles = vec![];

    for i in 0..10 {
        let permit = semaphore.clone();
        let handle = task::spawn(async move {
            let _permit = permit.acquire().await.unwrap();
            println!("Task {} running", i);
            sleep(Duration::from_secs(1)).await;
            println!("Task {} done", i);
        });
        handles.push(handle);
    }

    for handle in handles {
        handle.await.unwrap();
    }
}
```

## Time Management

### Timeouts and Intervals

```rust
use tokio::time::{timeout, interval, sleep, Duration};

// Timeout a future
async fn timeout_example() {
    let result = timeout(Duration::from_secs(5), async {
        expensive_operation().await
    }).await;

    match result {
        Ok(value) => println!("Completed: {:?}", value),
        Err(_) => println!("Timeout!"),
    }
}

// Periodic execution
async fn interval_example() {
    let mut interval = interval(Duration::from_secs(1));

    for _ in 0..5 {
        interval.tick().await;
        println!("Tick!");
    }
}
```

## Graceful Shutdown

### Shutdown Manager

```rust
use tokio::sync::broadcast;
use tokio::task::JoinSet;

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

    pub fn spawn<F, Fut>(&mut self, task: F)
    where
        F: FnOnce(broadcast::Receiver<()>) -> Fut + Send + 'static,
        Fut: Future<Output = Result<(), Box<dyn std::error::Error + Send + Sync>>> + Send + 'static,
    {
        let shutdown_rx = self.shutdown_tx.subscribe();
        self.tasks.spawn(task(shutdown_rx));
    }

    pub async fn shutdown(mut self, timeout_duration: Duration) -> Result<(), ShutdownError> {
        // Send shutdown signal
        let _ = self.shutdown_tx.send(());

        // Wait for tasks with timeout
        let shutdown_timeout = sleep(timeout_duration);
        tokio::pin!(shutdown_timeout);

        loop {
            tokio::select! {
                _ = &mut shutdown_timeout => {
                    // Timeout - abort remaining tasks
                    self.tasks.abort_all();
                    return Err(ShutdownError::Timeout);
                }
                Some(result) = self.tasks.join_next() => {
                    match result {
                        Ok(Ok(())) => continue,
                        Ok(Err(e)) => eprintln!("Task error: {}", e),
                        Err(e) => eprintln!("Join error: {}", e),
                    }
                }
                else => break,
            }
        }

        Ok(())
    }
}

// Usage
async fn shutdown_example() {
    let mut manager = ShutdownManager::new();

    manager.spawn(|mut shutdown| async move {
        loop {
            tokio::select! {
                _ = sleep(Duration::from_secs(1)) => {
                    println!("Working...");
                }
                _ = shutdown.recv() => {
                    println!("Shutting down task");
                    break;
                }
            }
        }
        Ok(())
    });

    // Simulate shutdown signal
    sleep(Duration::from_secs(5)).await;
    manager.shutdown(Duration::from_secs(10)).await.unwrap();
}
```

## Best Practices

### 1. Avoid Blocking the Runtime

```rust
// ❌ Bad: Blocks the async runtime
async fn bad_blocking() {
    std::thread::sleep(Duration::from_secs(1)); // Blocks!
}

// ✅ Good: Use async sleep
async fn good_async_sleep() {
    tokio::time::sleep(Duration::from_secs(1)).await;
}

// ✅ Good: Use spawn_blocking for CPU work
async fn good_cpu_work() {
    let result = task::spawn_blocking(|| {
        expensive_computation()
    }).await.unwrap();
}
```

### 2. Structured Concurrency

```rust
// Use select! for racing futures
async fn select_example() {
    let result = tokio::select! {
        value = fetch_from_cache() => Ok(value),
        value = fetch_from_db() => Ok(value),
        _ = sleep(Duration::from_secs(5)) => Err("Timeout"),
    };
}

// Use join! to wait for multiple futures
async fn join_example() {
    let (user, orders, profile) = tokio::join!(
        fetch_user(),
        fetch_orders(),
        fetch_profile(),
    );
}

// Use try_join! to fail fast
async fn try_join_example() -> Result<_, Error> {
    let (user, orders) = tokio::try_join!(
        fetch_user(),
        fetch_orders(),
    )?;
    Ok((user, orders))
}
```

## Common Pitfalls

1. **Don't mix blocking and async**: Use `spawn_blocking` for sync code
2. **Avoid holding locks across awaits**: Minimize critical sections
3. **Use bounded channels**: Prevent unbounded memory growth
4. **Track spawned tasks**: Always wait for tasks or handle cancellation
5. **Set timeouts**: Don't let operations run forever
6. **Handle panics**: Tasks that panic will poison shared state

## Common Dependencies

```toml
[dependencies]
tokio = { version = "1", features = ["full"] }
futures = "0.3"
async-trait = "0.1"
```
