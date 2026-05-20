---
name: 125-java-concurrency
description: Use when you need to apply Java concurrency best practices — including thread safety fundamentals, ExecutorService thread pool management, concurrent design patterns like Producer-Consumer, asynchronous programming with CompletableFuture, immutability and safe publication, deadlock avoidance, virtual threads and structured concurrency, scoped values, backpressure, cancellation discipline, and observability for concurrent systems. Part of the skills-for-java project
metadata:
  author: Juan Antonio Breña Moral
  version: 0.12.0-SNAPSHOT
---
# Java rules for Concurrency objects

Identify and apply Java concurrency best practices to improve thread safety, scalability, and maintainability by using modern `java.util.concurrent` utilities, virtual threads, and structured concurrency.

**Core areas:** Thread safety fundamentals (`ConcurrentHashMap`, `AtomicInteger`, `ReentrantLock`, `ReadWriteLock`, Java Memory Model), `ExecutorService` thread pool configuration (sizing, keep-alive, bounded queues, rejection policies, graceful shutdown), Producer-Consumer and Publish-Subscribe concurrent design patterns (`BlockingQueue`), `CompletableFuture` for non-blocking async composition (`thenApply`/`thenCompose`/`exceptionally`/`orTimeout`), immutability and safe publication (`volatile`, static initializers), lock contention and false-sharing performance optimization, virtual threads (`Executors.newVirtualThreadPerTaskExecutor()`) for I/O-bound scalability, `StructuredTaskScope` for lifecycle-scoped task management, `ScopedValue` over `ThreadLocal` for immutable cross-task data, cooperative cancellation and `InterruptedException` discipline, backpressure with bounded queues and `CallerRunsPolicy`, deadlock avoidance via global lock ordering and `tryLock` with timeouts, `ForkJoin`/parallel-stream discipline for CPU-bound work, virtual-thread pinning detection (JFR `VirtualThreadPinned`), thread naming and `UncaughtExceptionHandler` observability, and fit-for-purpose primitives (`LongAdder`, `CopyOnWriteArrayList`, `StampedLock`, `Semaphore`, `CountDownLatch`, `Phaser`).

**Prerequisites:** Run `./mvnw compile` or `mvn compile` before applying any change. If compilation fails, **stop immediately** — compilation failure is a blocking condition that prevents any further processing.

**Multi-step scope:** Step 1 validates the project compiles. Step 2 analyzes existing concurrency patterns and categorizes issues by impact (CRITICAL, MAINTAINABILITY, PERFORMANCE, SCALABILITY). Step 3 applies thread safety fundamentals — replacing unsafe collections with `java.util.concurrent` equivalents and atomic classes. Step 4 refactors thread pool management to use properly configured `ExecutorService` instances with bounded queues and rejection policies. Step 5 implements concurrent design patterns (Producer-Consumer via `BlockingQueue`, Publish-Subscribe). Step 6 migrates asynchronous operations to `CompletableFuture` with proper chaining and timeout handling. Step 7 adopts modern Java concurrency features — virtual threads for I/O-bound tasks, `StructuredTaskScope` for related task groups, and `ScopedValue` instead of `ThreadLocal`. Step 8 enforces cancellation and interruption discipline — never swallowing `InterruptedException`, using `Future.cancel(true)`, and preferring `lockInterruptibly`. Step 9 adds backpressure and overload protection — bounded queues, semaphores/bulkheads, and `CallerRunsPolicy`. Step 10 eliminates deadlock risks via lock ordering, minimized lock scope, and `tryLock` with timeouts. Step 11 adds observability — named threads, `UncaughtExceptionHandler`, JFR metrics, and structured logging. Step 12 runs `./mvnw clean verify` to confirm all tests pass after changes.

**Before applying changes:** Read the reference for detailed good/bad examples, constraints, and safeguards for each concurrency pattern.

## Reference

For detailed guidance, examples, and constraints, see [references/125-java-concurrency.md](references/125-java-concurrency.md).
