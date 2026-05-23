---
name: elixir-performance-review
description: Reviews Elixir code for performance issues including GenServer bottlenecks, memory usage, and concurrency patterns. Use when reviewing high-throughput code or investigating performance issues.
---

# Elixir Performance Review

## Quick Reference

| Issue Type | Reference |
|------------|-----------|
| Mailbox overflow, blocking calls | [references/genserver-bottlenecks.md](references/genserver-bottlenecks.md) |
| When to use ETS, read/write concurrency | [references/ets-patterns.md](references/ets-patterns.md) |
| Binary handling, large messages | [references/memory.md](references/memory.md) |
| Task patterns, flow control | [references/concurrency.md](references/concurrency.md) |

## Review Checklist

### GenServer
- [ ] Not a single-process bottleneck for all requests
- [ ] No blocking operations in handle_call/cast
- [ ] Proper timeout configuration
- [ ] Consider ETS for read-heavy state

### Memory
- [ ] Large binaries not copied between processes
- [ ] Streams used for large data transformations
- [ ] No unbounded data accumulation

### Concurrency
- [ ] Task.Supervisor for dynamic tasks (not raw Task.async)
- [ ] No unbounded process spawning
- [ ] Proper backpressure for message producers

### Database
- [ ] Preloading to avoid N+1 queries
- [ ] Pagination for large result sets
- [ ] Indexes for frequent queries

## Valid Patterns (Do NOT Flag)

- **Single GenServer for low-throughput** - Not all state needs horizontal scaling
- **Synchronous calls for critical paths** - Consistency may require it
- **In-memory state without ETS** - ETS has overhead for small state
- **Enum over Stream for small collections** - Stream overhead not worth it

## Context-Sensitive Rules

| Issue | Flag ONLY IF |
|-------|--------------|
| GenServer bottleneck | Handles > 1000 req/sec OR blocking I/O in callbacks |
| Use streams | Processing > 10k items OR reading large files |
| Use ETS | Read:write ratio > 10:1 AND concurrent access |

## Before Submitting Findings

Load and follow [review-verification-protocol](../review-verification-protocol/SKILL.md) before reporting any issue.
