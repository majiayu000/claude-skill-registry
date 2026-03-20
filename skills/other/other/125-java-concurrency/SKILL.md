---
name: 125-java-concurrency
description: Use when you need to apply Java concurrency best practices — including thread safety fundamentals, ExecutorService thread pool management, concurrent design patterns like Producer-Consumer, asynchronous programming with CompletableFuture, immutability and safe publication, deadlock avoidance, virtual threads, scoped values, backpressure, cancellation discipline, and observability for concurrent systems. Part of the skills-for-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.13.0-SNAPSHOT
---
# Java rules for Concurrency objects

Identify and apply Java concurrency best practices to improve thread safety, scalability, and maintainability by using modern `java.util.concurrent` utilities and virtual threads.

**What is covered in this Skill?**

- Thread safety fundamentals: `ConcurrentHashMap`, `AtomicInteger`, `ReentrantLock`, `ReadWriteLock`, Java Memory Model
- `ExecutorService` thread pool configuration: sizing, keep-alive, bounded queues, rejection policies, graceful shutdown
- Producer-Consumer and Publish-Subscribe patterns with `BlockingQueue`
- `CompletableFuture` for non-blocking async composition (`thenApply`/`thenCompose`/`exceptionally`/`orTimeout`)
- Immutability and safe publication (`volatile`, static initializers)
- Lock contention and false-sharing performance optimization
- Virtual threads (`Executors.newVirtualThreadPerTaskExecutor()`) for I/O-bound scalability
- `ScopedValue` over `ThreadLocal` for immutable cross-task data
- Cooperative cancellation and `InterruptedException` discipline
- Backpressure with bounded queues and `CallerRunsPolicy`
- Deadlock avoidance via global lock ordering and `tryLock` with timeouts
- ForkJoin/parallel-stream discipline for CPU-bound work
- Virtual-thread pinning detection (JFR `VirtualThreadPinned`)
- Thread naming and `UncaughtExceptionHandler` observability
- Fit-for-purpose primitives: `LongAdder`, `CopyOnWriteArrayList`, `StampedLock`, `Semaphore`, `CountDownLatch`, `Phaser`

**Scope:** The reference is organized by examples (good/bad code patterns) for each core area. Apply recommendations based on applicable examples.

## Constraints

Before applying any concurrency changes, ensure the project compiles. If compilation fails, stop immediately — compilation failure is a blocking condition. After applying improvements, run full verification.

- **MANDATORY**: Run `./mvnw compile` or `mvn compile` before applying any change
- **SAFETY**: If compilation fails, stop immediately — compilation failure is a blocking condition that prevents any further processing
- **VERIFY**: Run `./mvnw clean verify` or `mvn clean verify` after applying improvements
- **BEFORE APPLYING**: Read the reference for detailed good/bad examples, constraints, and safeguards for each concurrency pattern

## When to use this skill

- Review Java code for concurrency

## Reference

For detailed guidance, examples, and constraints, see [references/125-java-concurrency.md](references/125-java-concurrency.md).
