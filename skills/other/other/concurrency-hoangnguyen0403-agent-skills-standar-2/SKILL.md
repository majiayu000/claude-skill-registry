---
name: Concurrency
description: Standards for safe concurrent programming using Goroutines, Channels, and Context.
metadata:
  labels: [golang, concurrency, goroutines, channels, context, sync]
  triggers:
    files: ['**/*.go']
    keywords: [goroutine, go keyword, channel, mutex, waitgroup, context]
---

# Golang Concurrency Standards

## **Priority: P0 (CRITICAL)**

## Principles

- **Share Memory by Communicating**: Don't communicate by sharing memory. Use channels.
- **Context is King**: Always pass `ctx` to efficient manage cancellation/timeouts.
- **Prevent Leaks**: Never start a goroutine without knowing how it will stop.
- **Race Detection**: Always run tests with `go test -race`.

## Primitives

- **Goroutines**: Lightweight threads. `go func() { ... }()`
- **Channels**: For data passing + synchronization.
- **WaitGroup**: Wait for a group of goroutines to finish.
- **ErrGroup**: WaitGroup + Error propagation (Preferred).
- **Mutex**: Protect shared state (simpler than channels for just state).

## Guidelines

- **Buffered vs Unbuffered**: Use unbuffered channels for strict synchronization. Use buffered only if you specifically need async decoupling/burst handling.
- **Closed Channels**: Panic if writing to closed. Reading from closed returns zero-value immediately.
- **Select**: Use `select` to handle multiple channels or timeouts.

## References

- [Concurrency Patterns](references/concurrency-patterns.md)
- [Context Usage](references/context-usage.md)
