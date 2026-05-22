---
name: debug-troubleshoot
description: Systematic debugging approach for Rust async code with Tokio, Turso, and redb. Use when diagnosing runtime issues, performance problems, async deadlocks, database connection issues, or panics.
---

# Debug and Troubleshoot

Systematic debugging approach for Rust async code with Tokio, Turso, and redb.

## Purpose
Diagnose and resolve runtime issues, performance problems, and unexpected behavior in the memory system.

## Debugging Tools

### 1. Logging with tracing

#### Setup
```rust
use tracing::{debug, info, warn, error, instrument};

#[instrument]
async fn problematic_function(id: &str) -> Result<Data> {
    debug!("Starting operation for id: {}", id);

    let data = fetch_data(id).await
        .map_err(|e| {
            error!("Failed to fetch data: {:?}", e);
            e
        })?;

    info!("Successfully fetched data");
    Ok(data)
}
```

#### Run with Logging
```bash
# Info level
RUST_LOG=info cargo run

# Debug level
RUST_LOG=debug cargo run

# Trace level (very verbose)
RUST_LOG=trace cargo run

# Specific module
RUST_LOG=memory_core::storage=debug cargo run

# Multiple modules
RUST_LOG=memory_core=debug,memory_storage_turso=trace cargo run
```

### 2. Console Debugging

#### Add Tracing Subscriber
```rust
use tracing_subscriber::{fmt, prelude::*, EnvFilter};

fn init_tracing() {
    tracing_subscriber::registry()
        .with(fmt::layer())
        .with(EnvFilter::from_default_env())
        .init();
}
```

#### Pretty Printing
```bash
# Colored output
RUST_LOG=debug cargo run 2>&1 | less -R

# JSON format (for parsing)
RUST_LOG_FORMAT=json RUST_LOG=debug cargo run
```

### 3. Tokio Console

#### Enable
```toml
# Cargo.toml
[dependencies]
tokio = { version = "1", features = ["full", "tracing"] }
console-subscriber = "0.1"
```

```rust
fn main() {
    console_subscriber::init();
    // Rest of code
}
```

#### Run
```bash
# Terminal 1: Run app
cargo run --features tokio-console

# Terminal 2: Run console
tokio-console
```

**Shows**:
- Active tasks
- Task spawn history
- Resource usage
- Blocking detection

### 4. LLDB/GDB Debugger

```bash
# Build with debug symbols
cargo build

# Run under debugger
rust-lldb target/debug/memory-core

# Set breakpoint
(lldb) b src/lib.rs:42

# Run
(lldb) run

# Inspect variables
(lldb) p variable_name

# Stack trace
(lldb) bt
```

## Common Issues

### 1. Async Deadlocks

#### Symptoms
- Program hangs
- No errors, just stops responding
- High CPU usage with no progress

#### Diagnosis
```rust
// Add timeout to detect hangs
use tokio::time::{timeout, Duration};

let result = timeout(
    Duration::from_secs(5),
    potentially_hanging_operation()
).await;

match result {
    Ok(Ok(data)) => println!("Success"),
    Ok(Err(e)) => println!("Operation failed: {}", e),
    Err(_) => println!("TIMEOUT! Possible deadlock"),
}
```

#### Common Causes

**Cause 1: Holding lock across await**
```rust
// WRONG - Can deadlock
let mut data = mutex.lock().await;
async_operation().await;  // Lock held during async operation
data.update();

// RIGHT
let value = {
    let data = mutex.lock().await;
    data.clone()  // Clone needed data
}; // Lock released
async_operation().await;
```

**Cause 2: Circular task dependencies**
```rust
// Task A waits for B, B waits for A
let (tx1, rx1) = oneshot::channel();
let (tx2, rx2) = oneshot::channel();

tokio::spawn(async move {
    rx2.await;  // Waits for task 2
    tx1.send(());
});

tokio::spawn(async move {
    rx1.await;  // Waits for task 1
    tx2.send(());
});
// DEADLOCK!
```

### 2. Database Connection Issues

#### Turso Connection Failures

```rust
#[instrument]
async fn check_turso_health(client: &TursoClient) -> Result<()> {
    debug!("Checking Turso connection");

    match client.execute("SELECT 1").await {
        Ok(_) => {
            info!("Turso connection healthy");
            Ok(())
        }
        Err(e) => {
            error!("Turso connection failed: {:?}", e);

            // Check specific errors
            if e.to_string().contains("timeout") {
                warn!("Connection timeout - network issue?");
            } else if e.to_string().contains("auth") {
                error!("Authentication failed - check token");
            }

            Err(e)
        }
    }
}
```

#### redb Lock Issues

```rust
// Diagnose lock problems
#[instrument]
fn debug_redb_locks(db: &Database) {
    debug!("Checking redb transactions");

    // Try to acquire write lock
    match db.begin_write() {
        Ok(txn) => {
            debug!("Write lock acquired successfully");
            drop(txn);
        }
        Err(e) => {
            error!("Cannot acquire write lock: {:?}", e);
            warn!("Possible long-running read transaction");
        }
    }
}
```

**Fix**: Ensure short-lived transactions
```rust
// WRONG - Long-lived transaction
let read_txn = db.begin_read()?;
expensive_computation();  // Transaction held too long
let value = read_txn.get(...)?;

// RIGHT - Short transaction
let value = {
    let read_txn = db.begin_read()?;
    read_txn.get(...)?
}; // Transaction dropped
expensive_computation();
```

### 3. Memory Leaks

#### Detect with Valgrind
```bash
cargo build
valgrind --leak-check=full \
         --show-leak-kinds=all \
         ./target/debug/memory-core
```

#### Common Causes

**Cause 1: Circular Arc references**
```rust
// Can leak if not careful
struct Node {
    next: Option<Arc<Mutex<Node>>>,
}

// Use Weak to break cycles
struct Node {
    next: Option<Weak<Mutex<Node>>>,
}
```

**Cause 2: Unbounded channels**
```rust
// WRONG - Can grow indefinitely
let (tx, mut rx) = mpsc::unbounded_channel();

// RIGHT - Bounded with backpressure
let (tx, mut rx) = mpsc::channel(100);
```

### 4. Performance Issues

#### Profile with Flamegraph
```bash
# Install
cargo install flamegraph

# Run profiler
cargo flamegraph --dev

# View flamegraph.svg
firefox flamegraph.svg
```

#### Common Bottlenecks

**Issue: Excessive cloning**
```rust
// Use Arc for shared ownership
let data = Arc::new(expensive_data);

// Clone Arc (cheap), not data
for _ in 0..100 {
    let data_clone = data.clone();  // Just increments refcount
    tokio::spawn(async move {
        process(data_clone).await;
    });
}
```

**Issue: Synchronous redb in async context**
```rust
// WRONG - Blocks executor
async fn save_data(db: &Database, data: Data) {
    let txn = db.begin_write().unwrap();  // Sync, blocks!
    // ...
}

// RIGHT - Use spawn_blocking
async fn save_data(db: Database, data: Data) {
    tokio::task::spawn_blocking(move || {
        let txn = db.begin_write()?;
        // ... sync operations ...
        txn.commit()
    }).await??;
}
```

**Issue: Too many concurrent tasks**
```rust
// WRONG - Spawns thousands of tasks
for item in huge_list {
    tokio::spawn(process(item));
}

// RIGHT - Limit concurrency
use tokio::sync::Semaphore;

let semaphore = Arc::new(Semaphore::new(10));
for item in huge_list {
    let permit = semaphore.clone().acquire_owned().await?;
    tokio::spawn(async move {
        let _permit = permit;  // Released on drop
        process(item).await
    });
}
```

### 5. Panic Debugging

#### Get Full Backtrace
```bash
RUST_BACKTRACE=full cargo run
```

#### Add Panic Hook
```rust
use std::panic;

fn main() {
    panic::set_hook(Box::new(|panic_info| {
        error!("PANIC: {:?}", panic_info);
        // Log to file, send to monitoring, etc.
    }));

    // Rest of code
}
```

#### Common Panics

**Unwrap on None/Err**
```rust
// WRONG
let value = option.unwrap();  // Panics if None

// RIGHT
let value = option.expect("Expected value to be present");
// Or
let value = option.ok_or_else(|| anyhow!("Missing value"))?;
```

**Index out of bounds**
```rust
// WRONG
let item = vec[index];  // Panics if index >= len

// RIGHT
let item = vec.get(index)
    .ok_or_else(|| anyhow!("Index {} out of bounds", index))?;
```

## Debugging Workflow

### 1. Reproduce the Issue
- Create minimal reproduction
- Identify conditions that trigger it
- Make it deterministic if possible

### 2. Add Instrumentation
```rust
#[instrument(skip(self))]
async fn problematic_function(&self, id: &str) -> Result<Data> {
    debug!("Starting with id: {}", id);

    let step1 = self.step1(id).await?;
    debug!("Step1 complete: {:?}", step1);

    let step2 = self.step2(step1).await?;
    debug!("Step2 complete: {:?}", step2);

    Ok(step2)
}
```

### 3. Run with Logging
```bash
RUST_LOG=debug cargo run 2>&1 | tee debug.log
```

### 4. Analyze Logs
- Look for patterns before failure
- Check timing (slow operations?)
- Verify expected flow

### 5. Form Hypothesis
- What could cause this behavior?
- Is it related to concurrency?
- Is it a logic error?
- Is it an external dependency?

### 6. Test Hypothesis
- Add specific logging
- Add assertions
- Create targeted test
- Modify code to test theory

### 7. Fix and Verify
- Implement fix
- Add regression test
- Verify fix works
- Verify no new issues

## Testing for Bugs

### Stress Tests
```rust
#[tokio::test]
async fn stress_test_concurrent_access() {
    let memory = create_test_memory().await;
    let mut handles = vec![];

    // Spawn 1000 concurrent operations
    for i in 0..1000 {
        let mem = memory.clone();
        handles.push(tokio::spawn(async move {
            mem.operation(i).await
        }));
    }

    // All should succeed
    for handle in handles {
        handle.await.unwrap().unwrap();
    }
}
```

## Troubleshooting Checklist

- [ ] Can you reproduce the issue?
- [ ] Is it in production, test, or both?
- [ ] Recent changes related to the issue?
- [ ] Error messages or panics?
- [ ] Logs show expected flow?
- [ ] Performance degradation?
- [ ] Resource usage (CPU, memory, connections)?
- [ ] External dependencies healthy?
- [ ] Database connections working?
- [ ] Locks or deadlocks?
- [ ] Async tasks completing?
