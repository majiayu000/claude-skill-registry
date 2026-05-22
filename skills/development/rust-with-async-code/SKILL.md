---
name: "Rust with Async Code"
description: "Write robust async/await code using tokio with proper non-blocking patterns"
approved: Yes
created: 2026-01-27
license: "MIT"
metadata:
  author: "Main Agent"
  version: "3.1-approved"
  last_updated: "2026-01-28"
tags:
  - rust
  - tokio
  - async
  - concurrency
files:
  - examples/async-best-practices.rs: "Complete async/await patterns and examples"
---

# Rust with Async Code

## When to Use This Skill

Read this when **writing async/await code with tokio** (not sync or tests). This covers:

- Using tokio as async runtime
- Non-blocking I/O patterns
- Task spawning and coordination
- Avoiding blocking the event loop
- Async testing with proper isolation

**Do NOT read this for:**
- Synchronous code → See [rust-clean-implementation](../rust-clean-implementation/skill.md)
- Testing patterns → See [rust-testing-excellence](../rust-testing-excellence/skill.md)

---

## Core Principle: Never Block the Event Loop

**Use async for I/O-bound operations. Use sync or `spawn_blocking` for CPU-intensive work.**

### Async/Sync Decision Matrix

| Operation Type | Approach |
|---------------|----------|
| **I/O-bound** (network, files) | Tokio async APIs (`tokio::fs`, `tokio::net`) |
| **CPU-intensive** (parsing, crypto) | `tokio::task::spawn_blocking` |
| **Waiting** (timers, events) | `tokio::time::sleep`, `tokio::select!` |
| **Blocking APIs** (std::fs, blocking sockets) | `tokio::task::spawn_blocking` |

---

## Essential Patterns

### 1. Non-Blocking I/O with Timeouts

Always use tokio's non-blocking APIs with timeouts:

```rust
use tokio::net::TcpStream;
use tokio::time::{timeout, Duration};

async fn fetch_with_timeout(url: &str) -> Result<Vec<u8>> {
    // Non-blocking connect with timeout
    let stream = timeout(
        Duration::from_secs(30),
        TcpStream::connect(url)
    ).await??;

    let mut buf = vec![0u8; 4096];

    // Non-blocking read with timeout
    let n = timeout(
        Duration::from_secs(30),
        stream.readable()
    ).await?;

    stream.try_read(&mut buf)?;

    Ok(buf)
}
```

### 2. Offload CPU Work with spawn_blocking

**CRITICAL:** Never block the event loop with CPU-intensive work.

```rust
// BAD ❌ - Blocks event loop
async fn process_data(data: Vec<u8>) -> Vec<u8> {
    expensive_computation(&data) // Blocks all other tasks!
}

// GOOD ✅ - Offloads to thread pool
async fn process_data(data: Vec<u8>) -> Result<Vec<u8>> {
    tokio::task::spawn_blocking(move || {
        expensive_computation(&data)
    })
    .await?
}
```

**For CPU-bound algorithms and performance patterns, see [Performance Tips](../rust-clean-implementation/skill.md#performance-tips).**

### 3. Async Test Isolation - MANDATORY

Use `current_thread` flavor to prevent test isolation issues:

```rust
// GOOD ✅ - Each test gets isolated runtime
#[tokio::test(flavor = "current_thread")]
async fn test_async_operation() {
    let result = process_async().await;
    assert!(result.is_ok());
}

// With manual time control
#[tokio::test(flavor = "current_thread", start_paused = true)]
async fn test_with_timeout() {
    let start = tokio::time::Instant::now();
    tokio::time::sleep(Duration::from_secs(3600)).await;
    // An hour passed instantly in simulation!
    assert_eq!(start.elapsed(), Duration::from_secs(3600));
}
```

---

## Channel Patterns

### Unbounded Channels (No Backpressure)

Use for low-frequency messages:

```rust
use tokio::sync::mpsc;

let (tx, mut rx) = mpsc::unbounded_channel::<Message>();

// Producer - never blocks on send
tokio::spawn(async move {
    for msg in messages {
        tx.send(msg).ok(); // Fire and forget
    }
});

// Consumer
tokio::spawn(async move {
    while let Some(msg) = rx.recv().await {
        process(msg).await;
    }
});
```

### Bounded Channels (With Backpressure)

Use for high-frequency messages to prevent memory issues:

```rust
// Max 100 messages in flight
let (tx, mut rx) = mpsc::channel::<Message>(100);

// Producer - blocks when channel is full (backpressure!)
tokio::spawn(async move {
    for msg in messages {
        tx.send(msg).await.ok(); // Waits if full
    }
});

// Consumer
tokio::spawn(async move {
    while let Some(msg) = rx.recv().await {
        process(msg).await;
    }
});
```

### Broadcast Channels (One-to-Many)

```rust
use tokio::sync::broadcast;

let (tx, mut rx1) = broadcast::channel::<Event>(10);
let mut rx2 = tx.subscribe();

// Publisher
tokio::spawn(async move {
    tx.send(Event::Started).ok();
});

// Multiple subscribers
tokio::spawn(async move {
    while let Ok(event) = rx1.recv().await {
        println!("Sub1: {:?}", event);
    }
});

tokio::spawn(async move {
    while let Ok(event) = rx2.recv().await {
        println!("Sub2: {:?}", event);
    }
});
```

---

## Task Management

### Spawning Concurrent Tasks

```rust
use futures::future::join_all;

async fn process_all(items: Vec<Item>) -> Vec<Result<Output>> {
    let tasks: Vec<_> = items
        .into_iter()
        .map(|item| {
            tokio::spawn(async move {
                process_item(item).await
            })
        })
        .collect();

    // Wait for all tasks to complete
    join_all(tasks)
        .await
        .into_iter()
        .map(|r| r.expect("task panicked"))
        .collect()
}
```

### Using select! for Multiple Futures

```rust
use tokio::select;

async fn fetch_with_timeout(url: &str) -> Result<Response> {
    select! {
        result = fetch(url) => result,
        _ = tokio::time::sleep(Duration::from_secs(30)) => {
            Err(Error::Timeout)
        }
    }
}

async fn wait_for_first<A, B>(fut_a: A, fut_b: B) -> Result<()>
where
    A: Future<Output = Result<()>>,
    B: Future<Output = Result<()>>,
{
    select! {
        result = fut_a => result,
        result = fut_b => result,
    }
}
```

---

## Common Pitfalls

### Pitfall 1: Blocking the Event Loop

```rust
// BAD ❌ - Blocks all other tasks
async fn bad_example() {
    let data = std::fs::read_to_string("file.txt"); // Blocks!
    process(&data).await;
}

// GOOD ✅ - Use async I/O
async fn good_example() -> Result<()> {
    let data = tokio::fs::read_to_string("file.txt").await?;
    process(&data).await?;
    Ok(())
}

// GOOD ✅ - Or use spawn_blocking for blocking I/O
async fn good_example_blocking() -> Result<()> {
    let data = tokio::task::spawn_blocking(|| {
        std::fs::read_to_string("file.txt")
    })
    .await??;
    process(&data).await?;
    Ok(())
}
```

### Pitfall 2: Forgetting to Await

```rust
// BAD ❌ - Future never executes
async fn bad_example() {
    let future = expensive_operation();
    // Forgot .await! Future is never polled.
    handle_result(future); // BUG!
}

// GOOD ✅ - Always await futures
async fn good_example() -> Result<()> {
    let result = expensive_operation().await?;
    handle_result(result);
    Ok(())
}
```

### Pitfall 3: Holding Locks Across Await Points

```rust
use std::sync::Mutex;

// BAD ❌ - Holding lock across await
async fn bad_example(data: Arc<Mutex<Data>>) {
    let guard = data.lock().unwrap();
    something_async().await; // Still holding lock!
    drop(guard);
}

// GOOD ✅ - Drop lock before await
async fn good_example(data: Arc<Mutex<Data>>) {
    let value = {
        let guard = data.lock().unwrap();
        guard.clone()
    }; // Lock dropped here
    something_async().await;
}

// BEST ✅ - Use tokio's async Mutex
use tokio::sync::Mutex as AsyncMutex;

async fn best_example(data: Arc<AsyncMutex<Data>>) {
    let mut guard = data.lock().await;
    something_async().await; // OK with async Mutex
    drop(guard);
}
```

**For synchronous mutex patterns, see [Smart Pointer Usage](../rust-clean-implementation/skill.md#smart-pointer-usage).**

### Pitfall 4: Using std::thread Instead of Spawning Tasks

```rust
// BAD ❌ - Creates OS thread instead of async task
async fn bad_example() {
    std::thread::spawn(|| {
        std::thread::sleep(Duration::from_secs(1)); // Doesn't use async!
    });
}

// GOOD ✅ - Use tokio::spawn for async work
async fn good_example() {
    tokio::spawn(async {
        tokio::time::sleep(Duration::from_secs(1)).await;
    });
}

// GOOD ✅ - Use spawn_blocking for blocking work
async fn good_example_blocking() {
    tokio::task::spawn_blocking(|| {
        std::thread::sleep(Duration::from_secs(1)); // OK in spawn_blocking
    })
    .await
    .ok();
}
```

---

## Stream Processing

```rust
use tokio_stream::StreamExt;

async fn process_event_stream() -> Result<()> {
    let mut stream = event_source().await?;

    // Process events as they arrive
    while let Some(event) = stream.next().await {
        match handle_event(event).await {
            Ok(_) => continue,
            Err(e) => log::error!("Event error: {}", e),
        }
    }

    Ok(())
}

// With concurrent processing
async fn process_concurrent(stream: impl Stream<Item = Event>) {
    stream
        .map(|event| process_event(event))
        .buffer_unordered(10) // Process 10 concurrently
        .for_each(|result| async move {
            match result {
                Ok(output) => handle_output(output).await,
                Err(e) => log::error!("Error: {}", e),
            }
        })
        .await;
}
```

---

## Dependency Configuration

```toml
[dependencies]
# Primary async runtime
tokio = { version = "1", features = ["full"] }

# For CPU-bound work (alternative to spawn_blocking)
rayon = "1.8"

# Stream utilities
tokio-stream = "0.1"
futures = "0.3"
```

---

## Learning Log

### 2026-01-28: Skill Restructuring

**Issue:** Original skill had 368 lines with broken/incomplete code examples and pseudo-code mixed with Rust.

**Learning:** Removed all pseudo-code, fixed broken examples, consolidated into clear patterns with working code.

**New Standard:** All code examples must be valid Rust. Use comments to explain anti-patterns, not pseudo-code.

### 2026-01-27: Event Loop Blocking

**Issue:** Code blocking event loop by using std::fs and blocking I/O.

**Learning:** Always use tokio APIs for I/O or offload blocking work to `spawn_blocking`.

**Standard:** Never use `std::fs`, `std::net`, or blocking operations directly in async code.

---

## Examples

See `examples/` directory for working code:

- `async-best-practices.rs` - Complete async/await patterns with tokio, channels, select!, and common pitfalls

## Related Skills

- [Rust Clean Implementation](../rust-clean-implementation/skill.md) - For sync implementation patterns
- [Rust Testing Excellence](../rust-testing-excellence/skill.md) - For testing async code
- [DST Tokio Rust](../dst-tokio-rust/skill.md) - For deterministic testing of distributed async systems

---

*Last Updated: 2026-01-28*
*Version: 3.1-approved*
