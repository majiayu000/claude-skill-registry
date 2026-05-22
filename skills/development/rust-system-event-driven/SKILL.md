---
name: rust-system-event-driven
description: Rust event-driven system programming best practices for async runtimes, channels, sockets, terminals, and concurrency. This skill should be used when writing, reviewing, or refactoring Rust applications with async I/O, multi-threading, terminal interfaces, or network communication. Triggers on tasks involving tokio, async/await, channels, sockets, TTY handling, signals, and streaming I/O.
---

# Rust System Event-Driven Best Practices

Comprehensive best practices guide for event-driven system programming in Rust. Contains 42 rules across 8 categories, prioritized by impact to guide async runtime usage, channel communication, threading, networking, and terminal handling.

## When to Apply

Reference these guidelines when:
- Building async applications with Tokio or async-std
- Implementing network servers or clients
- Writing terminal user interfaces (TUIs)
- Managing concurrent tasks and shared state
- Handling Unix signals and graceful shutdown

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Async Runtime Patterns | CRITICAL | `async-` |
| 2 | Channel Communication | CRITICAL | `chan-` |
| 3 | Threading & Synchronization | HIGH | `sync-` |
| 4 | Socket & Network I/O | HIGH | `net-` |
| 5 | Terminal & TTY Handling | MEDIUM-HIGH | `term-` |
| 6 | Signal & Process Control | MEDIUM | `sig-` |
| 7 | File I/O Streaming | MEDIUM | `io-` |
| 8 | Event Loop Architecture | LOW-MEDIUM | `loop-` |

## Quick Reference

### 1. Async Runtime Patterns (CRITICAL)

- [`async-spawn-blocking`](references/async-spawn-blocking.md) - Use spawn_blocking for CPU-bound work
- [`async-select-biased`](references/async-select-biased.md) - Use biased select for priority handling
- [`async-no-std-block`](references/async-no-std-block.md) - Avoid std blocking calls in async context
- [`async-cancellation-safe`](references/async-cancellation-safe.md) - Design cancellation-safe async operations
- [`async-task-local`](references/async-task-local.md) - Use task-local storage for request context
- [`async-structured-concurrency`](references/async-structured-concurrency.md) - Use JoinSet for structured concurrency

### 2. Channel Communication (CRITICAL)

- [`chan-bounded-backpressure`](references/chan-bounded-backpressure.md) - Use bounded channels for backpressure
- [`chan-oneshot-response`](references/chan-oneshot-response.md) - Use oneshot channels for request-response
- [`chan-broadcast-fanout`](references/chan-broadcast-fanout.md) - Use broadcast channels for fan-out
- [`chan-watch-state`](references/chan-watch-state.md) - Use watch channels for shared state
- [`chan-graceful-shutdown`](references/chan-graceful-shutdown.md) - Use channel closure for graceful shutdown

### 3. Threading & Synchronization (HIGH)

- [`sync-arc-mutex-shared`](references/sync-arc-mutex-shared.md) - Use Arc<Mutex> for shared mutable state
- [`sync-rwlock-read-heavy`](references/sync-rwlock-read-heavy.md) - Use RwLock for read-heavy workloads
- [`sync-atomic-counters`](references/sync-atomic-counters.md) - Use atomics for simple counters and flags
- [`sync-avoid-lock-await`](references/sync-avoid-lock-await.md) - Avoid holding std Mutex across await
- [`sync-semaphore-limit`](references/sync-semaphore-limit.md) - Use Semaphore to limit concurrency
- [`sync-parking-lot`](references/sync-parking-lot.md) - Use parking_lot for high-contention locks

### 4. Socket & Network I/O (HIGH)

- [`net-split-reader-writer`](references/net-split-reader-writer.md) - Split sockets into reader and writer halves
- [`net-framing-codec`](references/net-framing-codec.md) - Use framing for message-based protocols
- [`net-connection-pool`](references/net-connection-pool.md) - Use connection pools for repeated connections
- [`net-timeout-all-io`](references/net-timeout-all-io.md) - Add timeouts to all network operations
- [`net-tcp-nodelay`](references/net-tcp-nodelay.md) - Set TCP_NODELAY for low-latency protocols
- [`net-graceful-disconnect`](references/net-graceful-disconnect.md) - Implement graceful connection shutdown

### 5. Terminal & TTY Handling (MEDIUM-HIGH)

- [`term-raw-mode-restore`](references/term-raw-mode-restore.md) - Always restore terminal state on exit
- [`term-alternate-screen`](references/term-alternate-screen.md) - Use alternate screen for full-screen apps
- [`term-async-event-stream`](references/term-async-event-stream.md) - Use async event stream for terminal input
- [`term-buffered-output`](references/term-buffered-output.md) - Buffer terminal output for performance
- [`term-handle-resize`](references/term-handle-resize.md) - Handle terminal resize events

### 6. Signal & Process Control (MEDIUM)

- [`sig-ctrl-c-graceful`](references/sig-ctrl-c-graceful.md) - Handle Ctrl-C for graceful shutdown
- [`sig-unix-signals`](references/sig-unix-signals.md) - Handle Unix signals asynchronously
- [`sig-child-reap`](references/sig-child-reap.md) - Reap child processes to avoid zombies
- [`sig-timeout-shutdown`](references/sig-timeout-shutdown.md) - Set shutdown timeout to force exit

### 7. File I/O Streaming (MEDIUM)

- [`io-async-file-ops`](references/io-async-file-ops.md) - Use async file operations in async context
- [`io-stream-large-files`](references/io-stream-large-files.md) - Stream large files instead of loading entirely
- [`io-copy-bidirectional`](references/io-copy-bidirectional.md) - Use copy_bidirectional for proxying
- [`io-pipe-communication`](references/io-pipe-communication.md) - Use pipes for process communication
- [`io-flush-before-read`](references/io-flush-before-read.md) - Flush writes before expecting responses

### 8. Event Loop Architecture (LOW-MEDIUM)

- [`loop-actor-model`](references/loop-actor-model.md) - Use actor pattern for stateful components
- [`loop-event-types`](references/loop-event-types.md) - Use typed events over dynamic dispatch
- [`loop-state-machine`](references/loop-state-machine.md) - Model protocol state as type-safe state machine
- [`loop-layered-architecture`](references/loop-layered-architecture.md) - Separate I/O from business logic
- [`loop-cancellation-token`](references/loop-cancellation-token.md) - Use CancellationToken for coordinated shutdown

## How to Use

Read individual reference files for detailed explanations and code examples:

- [Section definitions](references/_sections.md) - Category structure and impact levels
- [Rule template](assets/templates/_template.md) - Template for adding new rules

## Reference Files

| File | Description |
|------|-------------|
| [references/_sections.md](references/_sections.md) | Category definitions and ordering |
| [assets/templates/_template.md](assets/templates/_template.md) | Template for new rules |
| [metadata.json](metadata.json) | Version and reference information |
