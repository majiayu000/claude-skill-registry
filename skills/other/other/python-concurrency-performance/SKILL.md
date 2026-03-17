---
name: python-concurrency-performance
description: Use when designing or reviewing concurrent Python code — selecting between asyncio, threads, or multiprocessing; structuring cancellation and deadline propagation; bounding fan-out and backpressure. Also use when diagnosing race conditions, deadlocks, slow throughput, or thread/task leaks under load.
---

# Python Concurrency and Performance

## Overview

Correct concurrency starts with matching the model to the workload, not the developer's preference.
This skill encodes defaults for model selection, cancellation/deadline behavior, and lifecycle safety—prioritizing explicit control over implicit magic.

Treat these recommendations as preferred defaults.
When project constraints demand deviation, call out tradeoffs and compensating controls.

## When to Use

- Selecting between `asyncio`, `threading`, `multiprocessing`, or `concurrent.futures`
- Propagating deadlines or cancellation through async call chains
- Bounding fan-out, backpressure, or semaphore-guarded concurrency
- Diagnosing race conditions, deadlocks, or priority inversion
- Profiling throughput bottlenecks before and after optimization
- Verifying no task or thread leaks on shutdown or lifecycle transitions

### When NOT to Use

- Pure CPU-bound numeric work better served by NumPy/C extensions
- Single-threaded scripting with no concurrent I/O
- Distributed systems coordination (use a workflow/orchestration skill instead)

## Quick Reference

- Choose the concurrency model by workload profile (I/O-bound → asyncio/threads; CPU-bound → multiprocessing).
- Keep cancellation and cleanup explicit—never rely on garbage collection to close resources.
- Bound fan-out and backpressure with semaphores or queue limits; unbounded spawning invites OOM.
- Measure before optimizing; re-measure after every change to confirm the win.
- Verify no task/thread leaks on any lifecycle-sensitive change (startup, shutdown, reconnect).

## Common Mistakes

- **Defaulting to threads for I/O-bound work** — `asyncio` avoids thread-safety bugs entirely for network I/O; threads add synchronization overhead for no gain.
- **Ignoring cancellation propagation** — a cancelled parent that doesn't cancel children leaks tasks and holds connections open.
- **Unbounded `gather` / `submit` calls** — spawning thousands of tasks without a semaphore or bounded executor starves the event loop or exhausts OS threads.
- **Optimizing without profiling** — guessing at bottlenecks leads to complex code that solves the wrong problem; always profile first.
- **Missing shutdown verification** — tests that don't assert clean shutdown mask slow resource leaks that surface only in production under load.

## Scope Note

- Treat these recommendations as preferred defaults for common cases, not universal rules.
- If a default conflicts with project constraints or worsens the outcome, suggest a better-fit alternative and explain why it is better for this case.
- When deviating, call out tradeoffs and compensating controls (tests, observability, migration, rollback).

## Invocation Notice

- Inform the user when this skill is being invoked by name: `python-concurrency-performance`.

## References

- `references/concurrency-models.md`
- `references/deadlines-cancellation-lifecycle.md`
- `references/leak-detection.md`
