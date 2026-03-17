---
name: 143-java-functional-exception-handling
description: Use when you need to apply functional exception handling best practices in Java — including replacing exception overuse with Optional and VAVR Either types, designing error type hierarchies using sealed classes and enums, implementing monadic error composition pipelines, establishing functional control flow patterns, and reserving exceptions only for truly exceptional system-level failures.
metadata:
  author: Juan Antonio Breña Moral
  version: 0.12.0-SNAPSHOT
---
# Java Functional Exception handling Best Practices

Identify and apply functional exception handling best practices in Java to improve error clarity, maintainability, and performance by eliminating exception overuse in favour of monadic error types.

**Core areas:** `Optional<T>` for nullable values over throwing `NullPointerException` or `NotFoundException`, VAVR `Either<L,R>` for predictable business-logic failures, `CompletableFuture<T>` for async error handling, sealed classes and records for rich error type hierarchies with exhaustive pattern matching, enum-based error types for simple failure cases, functional composition with `flatMap`/`map`/`peek`/`peekLeft` for chaining operations that can fail, structured logging at appropriate severity levels (warn/info for business failures, error for system failures), checked vs unchecked exception discipline, and exception chaining with full causal context when exceptions are unavoidable.

**Prerequisites:** Run `./mvnw validate` before applying any changes. If validation fails, **stop immediately** — do not proceed until the project is in a valid state. Also confirm the VAVR dependency (`io.vavr:vavr`) and SLF4J are present when introducing `Either` types.

**Multi-step scope:** Step 1 validates the project compiles. Step 2 categorizes error handling opportunities by impact (CRITICAL, MAINTAINABILITY, PERFORMANCE, EXPRESSIVENESS) and area (exception overuse, monadic gaps, error type design, functional composition). Step 3 replaces exceptions for nullable/not-found cases with `Optional`. Step 4 replaces multiple checked exceptions for business logic with VAVR `Either<L,R>` types. Step 5 designs comprehensive error types — enums for simple cases, sealed classes/records for complex hierarchies. Step 6 implements monadic composition pipelines (`flatMap`/`map`) to replace imperative try-catch control flow. Step 7 aligns logging to functional patterns (warn/info for functional errors, error only for system failures). Step 8 reserves `RuntimeException` subclasses only for programming errors and truly exceptional system failures. Step 9 adds JavaDoc documenting `Either` return types and their left/right values. Step 10 runs `./mvnw clean verify` to confirm all tests pass after changes.

**Before applying changes:** Read the reference for detailed good/bad examples, constraints, and safeguards for each functional exception handling pattern.

## Reference

For detailed guidance, examples, and constraints, see [references/143-java-functional-exception-handling.md](references/143-java-functional-exception-handling.md).
