---
name: rust-async-channels
description: Async channel patterns for Rust (async-channel, tokio, crossbeam)
---

# rust-async-channels

Async channels enable safe, concurrent communication between threads and tasks in Rust. This skill covers `async-channel` (the primary choice in script-kit-gpui), plus alternatives like tokio channels and crossbeam.

## async-channel

The `async-channel` crate provides an async multi-producer multi-consumer (MPMC) channel where each message is received by only one consumer.

### Creating Channels

```rust
// Bounded channel - has backpressure, prevents memory growth
let (tx, rx) = async_channel::bounded::<T>(capacity);

// Unbounded channel - no backpressure, can grow indefinitely
let (tx, rx) = async_channel::unbounded::<T>();
```

### Core Types

| Type | Description |
|------|-------------|
| `Sender<T>` | Cloneable send handle |
| `Receiver<T>` | Cloneable receive handle |
| `SendError<T>` | Channel closed, contains unsent value |
| `RecvError` | Channel closed, no more messages |
| `TrySendError<T>` | `Full(T)` or `Closed(T)` |
| `TryRecvError` | `Empty` or `Closed` |

### API Methods

```rust
// Async methods (use in async contexts)
tx.send(value).await     // Waits if bounded channel is full
rx.recv().await          // Waits until message available

// Blocking methods (use in sync threads)
tx.send_blocking(value)  // Blocks current thread if full
rx.recv_blocking()       // Blocks current thread until message

// Non-blocking methods (never wait)
tx.try_send(value)       // Returns TrySendError::Full if full
rx.try_recv()            // Returns TryRecvError::Empty if empty

// Channel state
tx.is_closed()           // True if all receivers dropped
rx.is_closed()           // True if all senders dropped
tx.close()               // Manually close send side
rx.close()               // Manually close receive side
tx.len()                 // Current number of queued messages
tx.capacity()            // Max capacity (None for unbounded)
```

## Usage in script-kit-gpui

### Pattern 1: Stdin Listener (Sync Thread to Async)

Bridges synchronous stdin reading to async event handling:

```rust
// stdin_commands.rs
pub fn start_stdin_listener() -> async_channel::Receiver<ExternalCommand> {
    // Bounded channel prevents memory growth from slow consumers
    let (tx, rx) = async_channel::bounded(100);
    
    std::thread::spawn(move || {
        let stdin = std::io::stdin();
        let reader = stdin.lock();
        
        for line in reader.lines() {
            match line {
                Ok(line) if !line.trim().is_empty() => {
                    if let Ok(cmd) = serde_json::from_str(&line) {
                        // send_blocking: sync thread waiting on bounded channel
                        if tx.send_blocking(cmd).is_err() {
                            break; // Channel closed
                        }
                    }
                }
                Err(_) => break,
                _ => {}
            }
        }
    });
    
    rx
}

// Consumer (async context)
cx.spawn(async move {
    while let Ok(cmd) = stdin_rx.recv().await {
        handle_command(cmd);
    }
}).detach();
```

### Pattern 2: Global Singleton Channels (OnceLock)

For hotkey events shared across the application:

```rust
// hotkeys.rs
static HOTKEY_CHANNEL: OnceLock<(
    async_channel::Sender<()>, 
    async_channel::Receiver<()>
)> = OnceLock::new();

pub fn hotkey_channel() -> &'static (
    async_channel::Sender<()>, 
    async_channel::Receiver<()>
) {
    HOTKEY_CHANNEL.get_or_init(|| async_channel::bounded(10))
}

// Producer (hotkey callback, non-blocking to avoid blocking OS)
if hotkey_channel().0.try_send(()).is_err() {
    log("Hotkey channel full/closed");
}

// Consumer (async task)
while let Ok(()) = hotkey_channel().1.recv().await {
    show_main_window();
}
```

### Pattern 3: Watcher with Ownership Transfer

AppearanceWatcher creates channel, gives receiver to caller:

```rust
// watcher.rs
pub struct AppearanceWatcher {
    tx: Option<async_channel::Sender<AppearanceChangeEvent>>,
    stop_flag: Option<Arc<AtomicBool>>,
}

impl AppearanceWatcher {
    pub fn new() -> (Self, async_channel::Receiver<AppearanceChangeEvent>) {
        let (tx, rx) = async_channel::bounded(100);
        let watcher = AppearanceWatcher { tx: Some(tx), stop_flag: None };
        (watcher, rx)
    }
    
    pub fn start(&mut self) -> Result<(), String> {
        let tx = self.tx.take().ok_or("already started")?;
        let stop_flag = Arc::new(AtomicBool::new(false));
        
        thread::spawn(move || {
            loop {
                if stop_flag.load(Ordering::Relaxed) { break; }
                let appearance = detect_appearance();
                if tx.send_blocking(appearance).is_err() { break; }
                thread::sleep(Duration::from_secs(2));
            }
        });
        Ok(())
    }
}
```

### Pattern 4: Script Prompt Messages

UI thread receives messages from script execution:

```rust
// execute_script.rs
let (tx, rx) = async_channel::bounded(100);
self.prompt_receiver = Some(rx.clone());

// Event-driven listener
cx.spawn(async move |this, cx| {
    while let Ok(msg) = rx.recv().await {
        cx.update(|cx| {
            this.update(cx, |app, cx| {
                app.handle_prompt_message(msg, cx);
            })
        });
    }
}).detach();
```

## Channel Types Comparison

### MPSC (Multi-Producer, Single-Consumer)

```rust
// std::sync::mpsc - blocking only
let (tx, rx) = std::sync::mpsc::channel();      // Unbounded
let (tx, rx) = std::sync::mpsc::sync_channel(n); // Bounded

// tokio::sync::mpsc - async
let (tx, rx) = tokio::sync::mpsc::channel(n);   // Bounded only
```

### MPMC (Multi-Producer, Multi-Consumer)

```rust
// async-channel - async MPMC
let (tx, rx) = async_channel::bounded(n);

// crossbeam-channel - sync MPMC
let (tx, rx) = crossbeam_channel::bounded(n);
```

### Oneshot (Single Message)

```rust
// tokio::sync::oneshot
let (tx, rx) = tokio::sync::oneshot::channel();
tx.send(value);  // Can only call once
let result = rx.await;

// futures::channel::oneshot
let (tx, rx) = futures::channel::oneshot::channel();
```

### Broadcast (One-to-Many)

```rust
// tokio::sync::broadcast - all receivers get every message
let (tx, _) = tokio::sync::broadcast::channel(100);
let rx1 = tx.subscribe();
let rx2 = tx.subscribe();
tx.send(value);  // Both rx1 and rx2 receive it
```

### Watch (Latest Value)

```rust
// tokio::sync::watch - receivers see latest value only
let (tx, rx) = tokio::sync::watch::channel(initial_value);
tx.send(new_value);
let current = *rx.borrow();  // Always latest
```

## Backpressure

Bounded channels provide flow control to prevent memory exhaustion:

```rust
// GOOD: Bounded channel with appropriate capacity
let (tx, rx) = async_channel::bounded(100);

// Capacity sizing guidelines:
// - Stdin commands: 100 (typically < 10/sec)
// - Hotkey events: 10 (human input rate limited)
// - High-throughput: 1000+ or tune based on profiling

// Handle backpressure gracefully
match tx.try_send(msg) {
    Ok(()) => { /* sent */ }
    Err(TrySendError::Full(msg)) => {
        // Channel full - drop, log, or queue locally
        log::warn!("Channel full, dropping message");
    }
    Err(TrySendError::Closed(msg)) => {
        // Channel closed - receiver gone
        break;
    }
}
```

### When to Use Unbounded

Only use unbounded when:
1. Messages are tiny and bounded by external factors
2. Consumer is guaranteed faster than producer
3. Memory growth is acceptable (e.g., short-lived task)

```rust
// CAUTION: Can grow without limit
let (tx, rx) = async_channel::unbounded();
```

## Common Patterns

### Fan-Out (One Producer, Many Consumers)

With MPMC channels, clone the receiver:

```rust
let (tx, rx) = async_channel::bounded(100);

// Multiple consumers share work
for i in 0..4 {
    let rx = rx.clone();
    tokio::spawn(async move {
        while let Ok(task) = rx.recv().await {
            process(task);
        }
    });
}

// Producer sends to any available consumer
for task in tasks {
    tx.send(task).await?;
}
```

### Fan-In (Many Producers, One Consumer)

Clone the sender:

```rust
let (tx, rx) = async_channel::bounded(100);

// Multiple producers
for source in sources {
    let tx = tx.clone();
    tokio::spawn(async move {
        for item in source.items() {
            tx.send(item).await?;
        }
    });
}

// Single consumer
while let Ok(item) = rx.recv().await {
    aggregate(item);
}
```

### Request-Response (with Oneshot)

```rust
enum Request {
    GetValue { reply: oneshot::Sender<i32> },
    SetValue { value: i32 },
}

// Handler
while let Ok(req) = rx.recv().await {
    match req {
        Request::GetValue { reply } => {
            let _ = reply.send(current_value);
        }
        Request::SetValue { value } => {
            current_value = value;
        }
    }
}

// Client
let (reply_tx, reply_rx) = oneshot::channel();
tx.send(Request::GetValue { reply: reply_tx }).await?;
let value = reply_rx.await?;
```

### Graceful Shutdown

```rust
let (tx, rx) = async_channel::bounded(100);
let stop_flag = Arc::new(AtomicBool::new(false));

// Worker checks both channel and stop flag
let worker_stop = stop_flag.clone();
tokio::spawn(async move {
    loop {
        tokio::select! {
            msg = rx.recv() => {
                match msg {
                    Ok(m) => process(m),
                    Err(_) => break, // Channel closed
                }
            }
            _ = async { 
                while !worker_stop.load(Ordering::Relaxed) {
                    tokio::time::sleep(Duration::from_millis(100)).await;
                }
            } => break,
        }
    }
});

// Shutdown: set flag, drop sender
stop_flag.store(true, Ordering::Relaxed);
drop(tx);
```

## Anti-patterns

### 1. Unbounded for User Input

```rust
// BAD: Malicious input can exhaust memory
let (tx, rx) = async_channel::unbounded();
while let Ok(line) = stdin.read_line() {
    tx.send(line).await;  // Grows forever if consumer is slow
}

// GOOD: Bounded with backpressure handling
let (tx, rx) = async_channel::bounded(100);
```

### 2. Blocking in Async Context

```rust
// BAD: Blocks the async runtime thread
async fn handler() {
    let value = rx.recv_blocking();  // WRONG!
}

// GOOD: Use async recv
async fn handler() {
    let value = rx.recv().await;
}
```

### 3. Ignoring Send Errors

```rust
// BAD: Silently drops messages when channel closes
let _ = tx.send(important_data).await;

// GOOD: Handle the error
if tx.send(important_data).await.is_err() {
    log::error!("Failed to send: channel closed");
    // Decide: retry, propagate error, or cleanup
}
```

### 4. try_recv Loop (Busy Polling)

```rust
// BAD: Burns CPU checking empty channel
loop {
    match rx.try_recv() {
        Ok(msg) => handle(msg),
        Err(TryRecvError::Empty) => continue,  // Busy loop!
        Err(TryRecvError::Closed) => break,
    }
}

// GOOD: Use async recv
while let Ok(msg) = rx.recv().await {
    handle(msg);
}
```

### 5. Deadlock with Bounded Channels

```rust
// BAD: Can deadlock if both channels fill up
async fn a_to_b(tx: Sender<T>, rx: Receiver<T>) {
    let msg = rx.recv().await?;     // Waits for A
    tx.send(response).await?;       // Blocked if B's channel full
}

// If both tasks do this with bounded(1), deadlock!

// GOOD: Use try_send with fallback, or larger capacity
```

### 6. Forgetting to Drop Sender

```rust
// BAD: Receiver never exits because sender still exists
let (tx, rx) = async_channel::bounded(10);
let tx_clone = tx.clone();

tokio::spawn(async move {
    while let Ok(msg) = rx.recv().await {  // Hangs forever
        process(msg);
    }
});

// tx and tx_clone still exist, channel never closes!

// GOOD: Drop all senders when done
drop(tx);
drop(tx_clone);  // Now receiver exits
```

## Performance Tips

1. **Right-size capacity**: Too small causes contention, too large wastes memory
2. **Batch messages**: Send Vec<T> instead of individual T for high throughput
3. **Use try_send in callbacks**: Avoid blocking OS event handlers
4. **Profile channel length**: `tx.len()` helps tune capacity
5. **Consider crossbeam for sync-only**: Faster than async-channel when async not needed

## Crate Recommendations

| Use Case | Recommended Crate |
|----------|-------------------|
| Async MPMC | `async-channel` |
| Tokio-specific | `tokio::sync::mpsc` |
| Sync-only high perf | `crossbeam-channel` |
| Single response | `tokio::sync::oneshot` |
| Broadcast to all | `tokio::sync::broadcast` |
| Latest value only | `tokio::sync::watch` |
