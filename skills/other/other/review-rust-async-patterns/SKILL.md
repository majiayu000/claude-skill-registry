---
name: review-rust-async-patterns
description: Review and enforce Rust async/tokio concurrency patterns. Use when writing, reviewing, or debugging async Rust code. Covers blocking, mutexes, structured concurrency, cancellation safety, channels, graceful shutdown, timeouts, tracing, select! pitfalls, Send bounds, async drop, and stream processing.
---

# Tokio Concurrency Patterns, Footguns & Standards

A practical reference for Rust async concurrency with tokio — common anti-patterns, the correct alternatives, and rules to enforce in code review.

## Core Rules

1. **Never block the async runtime** — if it doesn't `.await`, it doesn't belong in an async fn
2. **Use the right mutex** — `tokio::sync::Mutex` across `.await`, `std::sync::Mutex` between `.await`s
3. **Structured concurrency** — `JoinSet` + `Semaphore`, never fire-and-forget
4. **Cancellation safety** — assume any `.await` can be the last line that runs
5. **Right channel for the job** — bounded `mpsc` by default
6. **Graceful shutdown** — `CancellationToken` + `TaskTracker` + timeout
7. **Spawn vs await** — spawn for concurrency, await for sequencing
8. **Timeout everything external** — wrap the *entire* operation
9. **Avoid `'static` infection** — don't spawn when you can await
10. **Structured tracing** — `#[instrument]` + `tracing`, never `println!`
11. **`select!` is not `match`** — understand branch cancellation and fairness
12. **`Send` bounds are contagious** — design your types to be `Send` from the start
13. **There is no async `Drop`** — cleanup must be explicit

---

## Rule 1: Never Block the Async Runtime

The async runtime uses a small pool of threads (usually equal to CPU cores). Block one thread and you've removed a significant fraction of your runtime's capacity. Block enough and the entire application deadlocks.

### The Footgun

```rust
// BAD — CPU-heavy work holds up the worker thread
async fn fetch_and_process(url: &str) -> Result<Data> {
    let body = reqwest::get(url).await?.text().await?;
    let parsed = expensive_parse(&body); // 500ms of CPU work, no .await
    Ok(parsed)
}

// BAD — synchronous I/O inside async context
async fn read_config() -> Result<Config> {
    let contents = std::fs::read_to_string("config.toml")?; // blocks thread
    Ok(toml::from_str(&contents)?)
}
```

### The Fix

```rust
// GOOD — offload CPU-bound work to the blocking thread pool
async fn fetch_and_process(url: &str) -> Result<Data> {
    let body = reqwest::get(url).await?.text().await?;
    let parsed = tokio::task::spawn_blocking(move || {
        expensive_parse(&body)
    }).await?;
    Ok(parsed)
}

// GOOD — use tokio's async filesystem operations
async fn read_config() -> Result<Config> {
    let contents = tokio::fs::read_to_string("config.toml").await?;
    Ok(toml::from_str(&contents)?)
}
```

### The Rule

> **If it takes longer than ~10-100us and doesn't have an `.await`, it doesn't belong in an async function.**
>
> | Work type | Solution |
> |-----------|----------|
> | CPU-bound work | `tokio::task::spawn_blocking` (or rayon for parallelism) |
> | Synchronous I/O | Tokio async equivalents (`tokio::fs`, `tokio::net`) |
> | FFI / C library calls | `spawn_blocking` |
> | Compression, hashing, large serialization | `spawn_blocking` |

---

## Rule 2: Use the Right Mutex

### The Footgun

```rust
// BAD — std::sync::Mutex held across an .await point
use std::sync::Mutex;

async fn update_cache(cache: Arc<Mutex<HashMap<String, Data>>>) {
    let mut guard = cache.lock().unwrap();
    // .await suspends here but the mutex is STILL HELD.
    // Another task on the same worker tries to lock → deadlock.
    let fresh = fetch_fresh_data(&guard).await;
    guard.insert("key".into(), fresh);
}
```

### The Fix

```rust
// GOOD — tokio::sync::Mutex is .await-aware
use tokio::sync::Mutex;

async fn update_cache(cache: Arc<Mutex<HashMap<String, Data>>>) {
    let mut guard = cache.lock().await;
    let fresh = fetch_fresh_data(&guard).await;
    guard.insert("key".into(), fresh);
}

// ALSO GOOD — std::sync::Mutex is FASTER when you don't hold across .await
use std::sync::Mutex;

async fn update_cache(cache: Arc<Mutex<HashMap<String, Data>>>) {
    let existing = {
        let guard = cache.lock().unwrap();
        guard.get("key").cloned()
    }; // guard dropped here, before .await

    let fresh = fetch_fresh_data(existing.as_ref()).await;

    {
        let mut guard = cache.lock().unwrap();
        guard.insert("key".into(), fresh);
    }
}
```

### The Rule

> | Scenario | Use |
> |----------|-----|
> | Lock held across `.await` | `tokio::sync::Mutex` |
> | Lock acquired and released between `.await` points | `std::sync::Mutex` (faster) |
>
> Simple test: if there's an `.await` between `.lock()` and the guard being dropped, you need tokio's mutex.

---

## Rule 3: Structured Concurrency with JoinSet

### The Footgun

```rust
// BAD — fire-and-forget. No error handling, no backpressure,
// panics are silently swallowed.
async fn process_all(items: Vec<Item>) {
    for item in items {
        tokio::spawn(async move {
            process(item).await;
        });
    }
    // Returns immediately. Are the tasks done? Who knows.
}

// ALSO BAD — unbounded concurrency
async fn process_all(items: Vec<Item>) -> Result<Vec<Output>> {
    let handles: Vec<_> = items
        .into_iter()
        .map(|item| tokio::spawn(async move { process(item).await }))
        .collect();

    let mut results = Vec::new();
    for handle in handles {
        results.push(handle.await??);
    }
    Ok(results)
}
```

### The Fix

```rust
// GOOD — JoinSet for structured concurrency
use tokio::task::JoinSet;

async fn process_all(items: Vec<Item>) -> Result<Vec<Output>> {
    let mut set = JoinSet::new();

    for item in items {
        set.spawn(async move { process(item).await });
    }

    let mut results = Vec::new();
    while let Some(res) = set.join_next().await {
        results.push(res??);
    }
    Ok(results)
}

// GOOD — bounded concurrency with semaphore
use tokio::sync::Semaphore;
use tokio::task::JoinSet;

async fn process_all(items: Vec<Item>) -> Result<Vec<Output>> {
    let semaphore = Arc::new(Semaphore::new(10));
    let mut set = JoinSet::new();

    for item in items {
        let permit = semaphore.clone().acquire_owned().await?;
        set.spawn(async move {
            let result = process(item).await;
            drop(permit);
            result
        });
    }

    let mut results = Vec::new();
    while let Some(res) = set.join_next().await {
        results.push(res??);
    }
    Ok(results)
}
```

### The Rule

> **Never fire-and-forget with `tokio::spawn` unless you genuinely don't care about the result.**
> - `JoinSet` to track spawned tasks and collect results
> - `Semaphore` to bound concurrency
> - When a `JoinSet` is dropped, all its tasks are cancelled — automatic cleanup

---

## Rule 4: Cancellation Safety

The most subtle footgun in async Rust. When a future is dropped (a `select!` branch loses, a timeout fires), execution stops at the last `.await` point. Any work done after the previous `.await` but before the next one is lost silently.

### The Footgun

```rust
// BAD — state loss on cancellation
async fn transfer(db: &Pool, from: AccountId, to: AccountId, amount: Decimal) -> Result<()> {
    db.execute(
        "UPDATE accounts SET balance = balance - $1 WHERE id = $2",
        &[&amount, &from],
    ).await?;

    // If cancelled HERE (between the two .awaits), money is debited
    // but never credited. The funds vanish.

    db.execute(
        "UPDATE accounts SET balance = balance + $1 WHERE id = $2",
        &[&amount, &to],
    ).await?;

    Ok(())
}

// This is how cancellation happens:
tokio::select! {
    result = transfer(&db, from, to, amount) => { /* ... */ }
    _ = tokio::time::sleep(Duration::from_secs(5)) => {
        // Timeout fires, transfer future is DROPPED mid-execution
    }
}
```

### The Fix

```rust
// GOOD — database transactions for atomicity
async fn transfer(db: &Pool, from: AccountId, to: AccountId, amount: Decimal) -> Result<()> {
    let mut tx = db.begin().await?;

    tx.execute(
        "UPDATE accounts SET balance = balance - $1 WHERE id = $2",
        &[&amount, &from],
    ).await?;
    tx.execute(
        "UPDATE accounts SET balance = balance + $1 WHERE id = $2",
        &[&amount, &to],
    ).await?;

    // Cancelled before this line → tx dropped → auto-rollback
    tx.commit().await?;
    Ok(())
}

// GOOD — mutable state outside the cancellable future
async fn process_messages(mut rx: mpsc::Receiver<Message>) {
    let mut buffer = Vec::new();

    loop {
        tokio::select! {
            Some(msg) = rx.recv() => {
                buffer.push(msg);
                if buffer.len() >= 100 {
                    flush(&mut buffer).await;
                }
            }
            _ = tokio::time::sleep(Duration::from_secs(5)) => {
                flush(&mut buffer).await;
            }
        }
    }
}
```

### The Rule

> **Assume any `.await` can be the last line that runs.**
> - Database transactions so partial work auto-rolls back
> - Mutable state outside `select!` branches
> - `tokio::select!` with `biased;` when ordering matters
> - Document cancellation safety in doc comments for public async fns
> - Read the tokio docs — they label which methods are cancellation-safe

---

## Rule 5: Channel Selection

### Quick Reference

| Channel | When to Use |
|---------|-------------|
| `mpsc` (bounded) | Multiple producers, single consumer. **The default choice.** |
| `mpsc` (unbounded) | Almost never correct in production. |
| `oneshot` | Single value, single send. Request/response patterns. |
| `broadcast` | Multiple consumers each get every message. Pub/sub. |
| `watch` | Latest-value-wins. Config reloading, state broadcasting. |

### The Footgun

```rust
// BAD — unbounded channel. Consumer slower than producer → OOM.
let (tx, mut rx) = mpsc::unbounded_channel();

// BAD — "bounded" with absurd buffer is effectively unbounded
let (tx, mut rx) = mpsc::channel(1_000_000);
```

### The Fix

```rust
// GOOD — bounded with reasonable buffer
let (tx, mut rx) = mpsc::channel(100);
tx.send(item).await?; // .await creates natural backpressure

// GOOD — oneshot for request/response
async fn query_actor(tx: &mpsc::Sender<ActorMessage>, query: Query) -> Result<Response> {
    let (reply_tx, reply_rx) = oneshot::channel();
    tx.send(ActorMessage::Query { query, reply: reply_tx }).await?;
    Ok(reply_rx.await?)
}

// GOOD — watch for "latest config" pattern
let (config_tx, config_rx) = watch::channel(initial_config);

config_tx.send_replace(new_config);

let mut rx = config_rx.clone();
loop {
    rx.changed().await?;
    let config = rx.borrow().clone();
    apply_config(&config);
}
```

### The Rule

> **Default to bounded `mpsc`.** Buffer size based on actual throughput: 32, 64, or 128 are common starting points.
>
> - Backpressure → bounded `mpsc`
> - Single request/response → `oneshot`
> - Pub/sub to multiple consumers → `broadcast`
> - "Give me the latest value" → `watch`
> - Unbounded channels are almost never correct in production

---

## Rule 6: Graceful Shutdown

### The Footgun

```rust
// BAD — hard abort, in-flight work is lost
#[tokio::main]
async fn main() {
    let server = start_server();
    server.await; // Ctrl+C → process dies, connections drop mid-response
}
```

### The Fix

```rust
// GOOD — CancellationToken + TaskTracker
use tokio_util::sync::CancellationToken;
use tokio_util::task::TaskTracker;

async fn run() {
    let token = CancellationToken::new();
    let tracker = TaskTracker::new();

    for i in 0..4 {
        let token = token.clone();
        tracker.spawn(async move {
            loop {
                tokio::select! {
                    _ = token.cancelled() => {
                        info!("Worker {i} shutting down");
                        break;
                    }
                    _ = do_work() => {}
                }
            }
        });
    }

    tokio::signal::ctrl_c().await.unwrap();
    info!("Shutdown signal received");

    token.cancel();
    tracker.close();

    if tokio::time::timeout(Duration::from_secs(30), tracker.wait())
        .await
        .is_err()
    {
        warn!("Timed out waiting for tasks, forcing shutdown");
    }
}
```

### The Rule

> **Every long-running async application needs a shutdown strategy.**
> - `CancellationToken` to propagate shutdown signals
> - `TaskTracker` to wait for in-flight work
> - Always have a timeout on graceful shutdown — don't wait forever
> - Child tokens for independent subsystem shutdown: `token.child_token()`

---

## Rule 7: Don't Spawn Where You Can Await

### The Footgun

```rust
// BAD — unnecessary spawn for sequential work
async fn handle_request(req: Request) -> Response {
    let user = tokio::spawn(async { get_user(req.user_id).await })
        .await
        .unwrap();
    let perms = tokio::spawn(async { get_permissions(user.id).await })
        .await
        .unwrap();
    build_response(user, perms)
}
```

Adds task overhead, breaks thread locality, swallows panics — for code that runs sequentially anyway.

### The Fix

```rust
// GOOD — sequential work just uses .await
async fn handle_request(req: Request) -> Response {
    let user = get_user(req.user_id).await;
    let perms = get_permissions(user.id).await;
    build_response(user, perms)
}

// GOOD — spawn/join only when you want actual concurrency
async fn handle_request(req: Request) -> Response {
    let (user, audit_log) = tokio::join!(
        get_user(req.user_id),
        get_audit_log(req.user_id),
    );
    build_response(user, audit_log)
}
```

### The Rule

> | Intent | Tool |
> |--------|------|
> | Run independently, possibly on another thread | `tokio::spawn` |
> | Wait for this to finish, then continue | `.await` |
> | Run these concurrently, wait for all | `tokio::join!` |
> | Run these concurrently, take the first | `tokio::select!` |

---

## Rule 8: Timeouts on Everything External

### The Footgun

```rust
// BAD — no timeout. Remote server hangs → you hang forever.
async fn call_service(client: &Client, url: &str) -> Result<Response> {
    Ok(client.get(url).send().await?)
}

// BAD — timeout only on request, not body read. Slow-loris drips bytes forever.
async fn call_service(client: &Client, url: &str) -> Result<String> {
    let resp = tokio::time::timeout(
        Duration::from_secs(5),
        client.get(url).send(),
    ).await??;
    let body = resp.text().await?; // can still hang indefinitely
    Ok(body)
}
```

### The Fix

```rust
// GOOD — wrap the ENTIRE operation
async fn call_service(client: &Client, url: &str) -> Result<String> {
    let body = tokio::time::timeout(Duration::from_secs(10), async {
        let resp = client.get(url).send().await?;
        let body = resp.text().await?;
        Ok::<_, anyhow::Error>(body)
    })
    .await
    .map_err(|_| anyhow!("service call timed out"))??;

    Ok(body)
}
```

### The Rule

> **Every `.await` on an external system should have a timeout.** No timeout = "wait forever."
> - Wrap the *entire* operation, not just part of it
> - Use `tokio::time::timeout`
> - Make timeout durations configurable, not hardcoded

---

## Rule 9: Avoid `'static` Lifetime Infections

### The Footgun

`tokio::spawn` requires `'static` futures — the spawned task can't borrow from the calling scope. This leads to excessive cloning and `Arc`-wrapping.

```rust
// BAD — cloning everything because spawn demands 'static
async fn process(db: &Database, items: &[Item]) {
    let db = db.clone();
    let items = items.to_vec();
    tokio::spawn(async move {
        for item in items {
            db.insert(&item).await;
        }
    }).await.unwrap();
}
```

### The Fix

```rust
// GOOD — don't spawn if you don't need concurrency
async fn process(db: &Database, items: &[Item]) {
    for item in items {
        db.insert(item).await;
    }
}

// GOOD — when you need concurrency, own the data
async fn process_concurrent(db: Arc<Database>, items: Vec<Item>) {
    let mut set = JoinSet::new();
    for item in items {
        let db = db.clone(); // Arc::clone is cheap
        set.spawn(async move {
            db.insert(&item).await
        });
    }
    while let Some(res) = set.join_next().await {
        res.unwrap();
    }
}
```

### The Rule

> **Don't reach for `tokio::spawn` reflexively — it forces `'static` and `Send` bounds on everything.**
> - No concurrency needed → just `.await`
> - Concurrency needed → `Arc` for shared state, owned data for the rest
> - Design data flow so tasks *own* their data rather than borrowing it

---

## Rule 10: Use `#[instrument]` for Async Tracing

### The Footgun

```rust
// BAD — println in concurrent code. Output is interleaved,
// you can't tell which task printed what.
async fn handle(req: Request) {
    println!("got request");
    let user = get_user(req.user_id).await;
    println!("got user: {:?}", user);
}
```

### The Fix

```rust
// GOOD — structured tracing with context propagation
use tracing::{info, instrument};

#[instrument(skip(db), fields(user_id = %req.user_id))]
async fn handle(req: Request, db: &Database) -> Result<Response> {
    info!("processing request");
    let user = get_user(&db, req.user_id).await?;
    info!(user_name = %user.name, "found user");
    Ok(build_response(user))
}
```

### The Rule

> **Use `tracing`, not `log` or `println!`, for async code.**
> - `#[instrument]` creates a span with function args automatically
> - `skip(field)` to exclude sensitive or large data
> - Spans propagate through `.await` points — you always know which request a log line belongs to
> - `tracing-subscriber` with JSON output in production

---

## Rule 11: `select!` Is Not `match`

`select!` looks like a match statement but has fundamentally different semantics. Every branch is a concurrent future. When one branch completes, the others are **cancelled** (dropped).

### The Footgun

```rust
// BAD — the non-winning branch's future is dropped, losing buffered data
async fn proxy(mut client: TcpStream, mut server: TcpStream) {
    let mut client_buf = vec![0u8; 4096];
    let mut server_buf = vec![0u8; 4096];

    loop {
        tokio::select! {
            n = client.read(&mut client_buf) => {
                let n = n?;
                if n == 0 { break; }
                server.write_all(&client_buf[..n]).await?;
            }
            n = server.read(&mut server_buf) => {
                let n = n?;
                if n == 0 { break; }
                client.write_all(&server_buf[..n]).await?;
            }
        }
        // Problem: if client.read completes, server.read is cancelled.
        // If server.read had partially filled server_buf, that data is lost.
        // (In this specific case read() is cancellation-safe, but many
        // other async fns are NOT.)
    }
}
```

```rust
// BAD — unfair select! starves the second branch
loop {
    tokio::select! {
        msg = high_priority_rx.recv() => { handle_high(msg).await; }
        msg = low_priority_rx.recv() => { handle_low(msg).await; }
    }
}
// If high_priority_rx always has messages, low_priority_rx is never checked
// because select! polls branches in order by default
```

### The Fix

```rust
// GOOD — use biased; when you WANT priority ordering (and understand it)
loop {
    tokio::select! {
        biased; // explicitly document the priority
        _ = shutdown.cancelled() => break, // always check shutdown first
        msg = high_priority_rx.recv() => { handle_high(msg).await; }
        msg = low_priority_rx.recv() => { handle_low(msg).await; }
    }
}

// GOOD — for bidirectional I/O, use tokio::io::copy_bidirectional
// or split into independent tasks
async fn proxy(client: TcpStream, server: TcpStream) -> Result<()> {
    let (client_read, client_write) = tokio::io::split(client);
    let (server_read, server_write) = tokio::io::split(server);

    let client_to_server = tokio::io::copy(&mut client_read, &mut server_write);
    let server_to_client = tokio::io::copy(&mut server_read, &mut client_write);

    tokio::try_join!(client_to_server, server_to_client)?;
    Ok(())
}
```

### The Rule

> **Before using `select!`, answer these questions for each branch:**
> 1. Is the future in this branch cancellation-safe? (Check tokio docs)
> 2. What happens to partially completed work when this branch loses?
> 3. Do I need priority ordering (`biased;`) or random fairness (default)?
>
> - Default `select!` randomly picks which branch to poll first — this is fairness, not a bug
> - `biased;` polls in source order — use it for shutdown checks and priority
> - If all branches do I/O on the same resource, consider splitting into separate tasks instead

---

## Rule 12: `Send` Bounds Are Contagious

`tokio::spawn` requires futures to be `Send` (movable between threads). A single non-`Send` type anywhere in the future's state poisons the entire chain.

### The Footgun

```rust
// BAD — Rc is !Send, so this future can't be spawned
use std::rc::Rc;

async fn process() {
    let data = Rc::new(vec![1, 2, 3]);
    some_async_operation().await; // Rc held across .await → future is !Send
    println!("{:?}", data);
}

tokio::spawn(process()); // ERROR: future is not Send

// BAD — MutexGuard from std held across .await makes future !Send on some platforms
async fn update(state: &std::sync::Mutex<State>) {
    let mut guard = state.lock().unwrap();
    guard.counter += 1;
    do_something().await; // guard held across .await → !Send
    guard.counter += 1;
}
```

### The Fix

```rust
// GOOD — use Arc instead of Rc for shared ownership across tasks
use std::sync::Arc;

async fn process() {
    let data = Arc::new(vec![1, 2, 3]);
    some_async_operation().await;
    println!("{:?}", data);
}

// GOOD — scope non-Send types so they don't live across .await
async fn update(state: &std::sync::Mutex<State>) {
    {
        let mut guard = state.lock().unwrap();
        guard.counter += 1;
    } // guard dropped BEFORE .await

    do_something().await;

    {
        let mut guard = state.lock().unwrap();
        guard.counter += 1;
    }
}
```

### The Rule

> **Design your types to be `Send + Sync` from the start.** Retrofitting it later is painful.
> - `Rc` → `Arc`
> - `Cell`/`RefCell` → `Mutex`/`RwLock` (or `tokio::sync` variants)
> - If a type is intentionally `!Send`, it can't be held across `.await` in a spawned task
> - Scope non-`Send` types tightly so they're dropped before `.await` points
> - Use `#[cfg(test)]` to test that your key futures are `Send`:
>
> ```rust
> fn assert_send<T: Send>(_: &T) {}
>
> #[test]
> fn futures_are_send() {
>     let fut = my_async_function();
>     assert_send(&fut);
> }
> ```

---

## Rule 13: There Is No Async `Drop`

Rust's `Drop` trait is synchronous. You cannot `.await` inside `drop()`. This means async cleanup (closing connections, flushing buffers, sending shutdown messages) cannot happen in destructors.

### The Footgun

```rust
// BAD — this does not do what you want
struct Connection {
    stream: TcpStream,
}

impl Drop for Connection {
    fn drop(&mut self) {
        // Cannot .await here. This silently does nothing useful.
        // The future is created but never polled.
        let _ = self.stream.shutdown();

        // This blocks the async runtime — also wrong
        // tokio::runtime::Handle::current().block_on(self.stream.shutdown());
    }
}
```

### The Fix

```rust
// GOOD — explicit async shutdown method
struct Connection {
    stream: TcpStream,
}

impl Connection {
    async fn shutdown(mut self) -> Result<()> {
        self.stream.flush().await?;
        self.stream.shutdown().await?;
        Ok(())
    }
}

// Caller is responsible for calling shutdown before dropping
let conn = Connection::new().await?;
// ... use conn ...
conn.shutdown().await?;

// GOOD — spawn a cleanup task if drop is unavoidable
impl Drop for Connection {
    fn drop(&mut self) {
        let stream = std::mem::replace(&mut self.stream, /* placeholder */);
        tokio::spawn(async move {
            let _ = stream.shutdown().await;
        });
    }
}
```

### The Rule

> **Never rely on `Drop` for async cleanup.**
> - Provide an explicit `async fn shutdown(self)` or `async fn close(self)` method
> - Document that callers must call it before dropping
> - If you must clean up in `Drop`, spawn a fire-and-forget task (last resort — you lose error handling)
> - Consider RAII wrappers that track whether shutdown was called and `warn!` in `Drop` if not

---

## Rule 14: Stream Processing

When processing a sequence of async values (not a one-shot future), use `tokio_stream` or `futures::Stream` instead of manual loops with channels.

### The Footgun

```rust
// BAD — manual buffering and batching with complex state
async fn process_events(mut rx: mpsc::Receiver<Event>) {
    let mut batch = Vec::new();
    let mut interval = tokio::time::interval(Duration::from_secs(1));

    loop {
        tokio::select! {
            Some(event) = rx.recv() => {
                batch.push(event);
                if batch.len() >= 100 {
                    flush_batch(&mut batch).await;
                }
            }
            _ = interval.tick() => {
                if !batch.is_empty() {
                    flush_batch(&mut batch).await;
                }
            }
        }
    }
}
```

### The Fix

```rust
// GOOD — stream combinators handle batching
use tokio_stream::StreamExt;
use tokio_stream::wrappers::ReceiverStream;

async fn process_events(rx: mpsc::Receiver<Event>) {
    let stream = ReceiverStream::new(rx);

    stream
        .chunks_timeout(100, Duration::from_secs(1))
        .for_each(|batch| async move {
            flush_batch(&batch).await;
        })
        .await;
}

// GOOD — transform and filter streams
async fn process_events(rx: mpsc::Receiver<RawEvent>) -> Result<()> {
    let stream = ReceiverStream::new(rx);

    let mut processed = stream
        .filter(|e| e.is_valid())
        .map(|e| transform(e))
        .throttle(Duration::from_millis(10));

    while let Some(event) = processed.next().await {
        handle(event).await?;
    }
    Ok(())
}
```

### The Rule

> **For sequences of async values, prefer stream combinators over manual `select!` + state machines.**
> - `chunks_timeout` for batching with both size and time limits
> - `filter`, `map`, `throttle` for transformation pipelines
> - `ReceiverStream` to adapt channels into streams
> - Manual `select!` loops are acceptable when you need complex multi-source coordination that stream combinators can't express

---

## Summary Cheat Sheet

| Rule | Anti-pattern | Fix |
|------|-------------|-----|
| Don't block the runtime | `std::fs`, CPU work in async | `spawn_blocking`, `tokio::fs` |
| Right mutex | `std::sync::Mutex` across `.await` | `tokio::sync::Mutex` or scope tightly |
| Structured concurrency | Fire-and-forget `tokio::spawn` | `JoinSet` + `Semaphore` |
| Cancellation safety | Multi-step mutations between `.await`s | Transactions, state outside `select!` |
| Right channel | Unbounded `mpsc` | Bounded `mpsc`, `oneshot`, `watch` |
| Graceful shutdown | Hard abort on Ctrl+C | `CancellationToken` + `TaskTracker` |
| Spawn vs await | `spawn` for sequential work | `.await`, `join!` for concurrency |
| Timeout everything | Bare `.await` on external calls | `tokio::time::timeout` wrapping full op |
| Avoid `'static` infection | Clone everything for `spawn` | Own data, `Arc` sparingly, avoid unnecessary spawns |
| Structured tracing | `println!` in concurrent code | `#[instrument]` + `tracing` |
| `select!` semantics | Assuming match-like behavior | Understand cancellation, use `biased;` |
| `Send` bounds | `Rc` / non-Send held across `.await` | `Arc`, scope non-Send types tightly |
| No async Drop | `.await` in `drop()` | Explicit `async fn shutdown(self)` |
| Stream processing | Manual `select!` + state machines | `tokio_stream` combinators |

---

## Code Review Checklist

When reviewing async Rust code, check:

- **No blocking calls** in async functions — `std::fs`, `std::thread::sleep`, CPU-heavy work without `spawn_blocking`
- **Mutex type matches usage** — `std::sync::Mutex` never held across `.await`, `tokio::sync::Mutex` when it must be
- **No fire-and-forget spawns** — all `tokio::spawn` results are collected via `JoinSet` or explicitly documented as intentionally detached
- **Cancellation safety** — multi-step operations use transactions or idempotent steps; state outside `select!` branches
- **Bounded channels** — no `unbounded_channel()` without documented justification
- **Shutdown path exists** — `CancellationToken` checked in long-running loops, `TaskTracker` waits for completion
- **Timeouts on external calls** — every HTTP/DB/RPC `.await` wrapped in `tokio::time::timeout`
- **No unnecessary spawns** — sequential work uses `.await`, concurrent work uses `join!` or `JoinSet`
- **`Send` compliance** — no `Rc`, `RefCell`, or non-Send guards held across `.await` in spawned futures
- **Tracing, not println** — `#[instrument]` on async functions, structured fields in log macros
- **`select!` branches are cancellation-safe** — verified against tokio docs for each method used
- **No `.await` in `Drop`** — async cleanup via explicit shutdown methods
- **Stream combinators** preferred over manual select-loop state machines for batching/throttling

---

## Verification

**After every unit of work, run `make ci` before moving on.** This ensures format, clippy, tests, and docs all pass. Do not proceed to the next task until CI is green.
