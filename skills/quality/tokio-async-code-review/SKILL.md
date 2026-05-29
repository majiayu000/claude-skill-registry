---
name: tokio-async-code-review
description: Reviews tokio async runtime usage for task management, sync primitives, channel patterns, and runtime configuration. Covers Rust 2024 edition changes including async fn in traits, RPIT lifetime capture, LazyLock, and if-let temporary scoping. Use when reviewing Rust code that uses tokio, async/await patterns, spawn, channels, or async synchronization. Also covers tokio-util, tower, and hyper integration patterns.
---

# Tokio Async Code Review

## Review Workflow

1. **Check Cargo.toml** — Note tokio feature flags (`full`, `rt-multi-thread`, `macros`, `sync`, etc.). Missing features cause confusing compile errors.
2. **Check runtime setup** — Is `#[tokio::main]` or manual runtime construction used? Multi-thread vs current-thread?
3. **Scan for blocking** — Search for `std::fs`, `std::net`, `std::thread::sleep`, CPU-heavy loops in async functions.
4. **Check channel usage** — Match channel type to communication pattern (mpsc, broadcast, oneshot, watch).
5. **Check sync primitives** — Verify correct mutex type, proper guard lifetimes, no deadlock potential.

## Gates (objective passes before conclusions)

Complete in order for the review scope. Do not assert **Critical** or **Major** until the relevant gate passes.

1. **Dependency surface** — Read the crate (and workspace, if inherited) `Cargo.toml` that supplies `tokio`. **Pass:** Written note of `tokio` version and enabled features, or explicit statement that there is no direct `tokio` dependency and where it comes from (workspace/path).
2. **Runtime model** — Locate runtime construction (`#[tokio::main]`, `Runtime::builder`, tests, or library with no owned runtime). **Pass:** One line naming flavor (`multi_thread` / `current_thread` / tests-only / none) and where it is defined.
3. **Blocking inventory** — Search reviewed paths for blocking APIs (`std::fs::`, `std::net::` without async wrappers, `std::thread::sleep`, heavy CPU loops in `async fn`). **Pass:** Each hit listed as `path:line` (or tool output excerpt), or explicit “no blocking patterns found in reviewed async code” after the search.
4. **Protocol** — Load `beagle-rust:review-verification-protocol`. **Pass:** Its pass conditions met before any finding is reported (file:line evidence for asserted issues).

## Output Format

Report findings as:

```text
[FILE:LINE] ISSUE_TITLE
Severity: Critical | Major | Minor | Informational
Description of the issue and why it matters.
```

## Quick Reference

| Issue Type | Reference |
|------------|-----------|
| Task spawning, JoinHandle, structured concurrency | [references/task-management.md](references/task-management.md) |
| Mutex, RwLock, Semaphore, Notify, Barrier | [references/sync-primitives.md](references/sync-primitives.md) |
| mpsc, broadcast, oneshot, watch channel patterns | [references/channels.md](references/channels.md) |
| Pin, cancellation, Future internals, select!, blocking bridge | [references/pinning-cancellation.md](references/pinning-cancellation.md) |

## Review Checklist

### Runtime Configuration
- [ ] Tokio features in Cargo.toml match actual usage
- [ ] Runtime flavor matches workload (`multi_thread` for I/O-bound, `current_thread` for simpler cases)
- [ ] `#[tokio::test]` used for async tests (not manual runtime construction)
- [ ] Worker thread count configured appropriately for production

### Task Management
- [ ] `spawn` return values (`JoinHandle`) are tracked, not silently dropped
- [ ] `spawn_blocking` used for CPU-heavy or synchronous I/O operations
- [ ] Tasks respect cancellation (via `CancellationToken`, `select!`, or shutdown channels)
- [ ] `JoinError` (task panic or cancellation) is handled, not just unwrapped
- [ ] `tokio::select!` branches are cancellation-safe
- [ ] Native `async fn` in traits used instead of `async-trait` crate where possible (stable since Rust 1.75)
- [ ] RPIT lifetime capture reviewed in async contexts — `-> impl Future` now captures all in-scope lifetimes in edition 2024

### Sync Primitives
- [ ] `tokio::sync::Mutex` used when lock is held across `.await`; `std::sync::Mutex` for short non-async sections
- [ ] No mutex guard held across await points (deadlock risk)
- [ ] `Semaphore` used for limiting concurrent operations (not ad-hoc counters)
- [ ] `RwLock` used when read-heavy workload (many readers, infrequent writes)
- [ ] `Notify` used for simple signaling (not channel overhead)
- [ ] `std::sync::LazyLock` used instead of `once_cell::sync::Lazy` or `lazy_static!` for runtime-initialized singletons (stable since Rust 1.80)
- [ ] `if let` lock guard patterns reviewed for edition 2024 temporary scoping — temporaries drop earlier, may change borrow validity

### Channels
- [ ] Channel type matches pattern: mpsc for back-pressure, broadcast for fan-out, oneshot for request-response, watch for latest-value
- [ ] Bounded channels have appropriate capacity (not too small = deadlock, not too large = memory)
- [ ] `SendError` / `RecvError` handled (indicates other side dropped)
- [ ] Broadcast `Lagged` errors handled (receiver fell behind)
- [ ] Channel senders dropped when done to signal completion to receivers

### Timer and Sleep
- [ ] `tokio::time::sleep` used instead of `std::thread::sleep`
- [ ] `tokio::time::timeout` wraps operations that could hang
- [ ] `tokio::time::interval` used correctly (`.tick().await` for periodic work)

## Severity Calibration

### Critical
- Blocking I/O (`std::fs::read`, `std::net::TcpStream`) in async context without `spawn_blocking`
- Mutex guard held across `.await` point (deadlock potential)
- `std::thread::sleep` in async function (blocks runtime thread)
- Unbounded channel where back-pressure is needed (OOM risk)

### Major
- `JoinHandle` silently dropped (lost errors, zombie tasks)
- Missing `select!` cancellation safety consideration
- Wrong mutex type (std vs tokio) for the use case
- Missing timeout on network/external operations

### Minor
- `tokio::spawn` for trivially small async blocks (overhead > benefit)
- Overly large channel buffer without justification
- Manual runtime construction where `#[tokio::main]` suffices
- `std::sync::Mutex` where contention is high enough to benefit from tokio's async mutex

### Informational
- Suggestions to use `tokio-util` utilities (e.g., `CancellationToken`)
- Tower middleware patterns for service composition
- Structured concurrency with `JoinSet`
- Migration from `async-trait` crate to native `async fn` in traits
- Migration from `once_cell` / `lazy_static` to `std::sync::LazyLock`
- Using `#[expect(lint)]` instead of `#[allow(lint)]` for self-cleaning suppression

## Valid Patterns (Do NOT Flag)

- **`std::sync::Mutex` for short critical sections** — tokio docs recommend this when no `.await` is inside the lock
- **`tokio::spawn` without explicit join** — Valid for background tasks with proper shutdown signaling
- **Unbuffered channel capacity of 1** — Valid for synchronization barriers
- **`#[tokio::main(flavor = "current_thread")]` in simple binaries** — Not every app needs multi-thread runtime
- **`clone()` on `Arc<T>` before `spawn`** — Required for moving into tasks, not unnecessary cloning
- **Large broadcast channel capacity** — Valid when lagged errors are expensive (event sourcing)
- **Native `async fn` in traits without `async-trait`** — Stable since 1.75; the crate is still valid for `dyn` dispatch cases
- **`+ use<'a>` on `-> impl Future` returns** — Correct edition 2024 precise capture syntax to limit lifetime capture
- **`#[expect(clippy::type_complexity)]` on complex async types** — Self-cleaning alternative to `#[allow]`, warns when suppression is no longer needed

## Before Submitting Findings

After **Gates**, apply `beagle-rust:review-verification-protocol` to every reported issue (evidence and dispositions per that skill).
