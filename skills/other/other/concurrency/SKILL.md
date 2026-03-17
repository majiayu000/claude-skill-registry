---
name: PHP Concurrency
description: Handling concurrency and non-blocking I/O in modern PHP.
metadata:
  labels: [php, concurrency, fibers, async]
  triggers:
    files: ['**/*.php']
    keywords: [Fiber, suspend, resume, non-blocking, async]
---

# PHP Concurrency

## **Priority: P2 (MEDIUM)**

## Structure

```text
src/
└── Async/
    ├── Schedulers/
    └── Clients/
```

## Implementation Guidelines

- **Fibers**: Use `Fiber` for low-level cooperative multitasking (8.1+).
- **Yield Control**: Apply `Fiber::suspend()` to yield within Fibers.
- **I/O Bound**: Target I/O tasks only; avoid for CPU intensive work.
- **Frameworks**: Prefer **Amp** or **ReactPHP** for complex events.
- **Self-Contained**: Ensure Fibers manage their own state/exceptions.
- **Incremental**: Refactor single bottlenecks before full async.

## Anti-Patterns

- **Implicit Flows**: **No Deep Suspend**: Keep Fiber logic traceable.
- **Internal Blocking**: **No Blocking I/O**: Don't block inside Fibers.
- **Custom Schedulers**: **No DIY Schedulers**: Use proven async libs.

## References

- [Fiber Implementation Guide](references/implementation.md)
