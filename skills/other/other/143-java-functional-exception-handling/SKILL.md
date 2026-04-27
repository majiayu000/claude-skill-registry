---
name: 143-java-functional-exception-handling
description: Use when you need to apply functional exception handling best practices in Java — including replacing exception overuse with Optional and VAVR Either types, designing error type hierarchies using sealed classes and enums, implementing monadic error composition pipelines, establishing functional control flow patterns, and reserving exceptions only for truly exceptional system-level failures. This should trigger for requests such as Improve the code with Functional Exception Handling; Apply Functional Exception Handling; Refactor the code with Functional Exception Handling. Part of cursor-rules-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.15.0-SNAPSHOT
---
# Java Functional Exception handling Best Practices

Identify and apply functional exception handling best practices in Java to improve error clarity, maintainability, and performance by eliminating exception overuse in favour of monadic error types.

**What is covered in this Skill?**

- `Optional<T>` for nullable values over throwing `NullPointerException` or `NotFoundException`
- VAVR `Either<L,R>` for predictable business-logic failures
- `CompletableFuture<T>` for async error handling
- Sealed classes and records for rich error type hierarchies with exhaustive pattern matching
- Enum-based error types for simple failure cases
- Functional composition: `flatMap`/`map`/`peek`/`peekLeft` for chaining operations that can fail
- Structured logging: warn/info for business failures, error for system failures
- Checked vs unchecked exception discipline
- Exception chaining with full causal context when exceptions are unavoidable

**Scope:** The reference is organized by examples (good/bad code patterns) for each core area. Apply recommendations based on applicable examples.

## Constraints

Before applying any functional exception handling changes, ensure the project validates. When introducing Either types, confirm the VAVR dependency (io.vavr:vavr) and SLF4J are present.

- **MANDATORY**: Run `./mvnw validate` or `mvn validate` before applying any changes
- **SAFETY**: If validation fails, stop immediately — do not proceed until the project is in a valid state
- **DEPENDENCY**: When introducing `Either` types, confirm VAVR (`io.vavr:vavr`) and SLF4J are present
- **VERIFY**: Run `./mvnw clean verify` or `mvn clean verify` after applying improvements
- **BEFORE APPLYING**: Read the reference for detailed good/bad examples, constraints, and safeguards for each functional exception handling pattern

## When to use this skill

- Improve the code with Functional Exception Handling
- Apply Functional Exception Handling
- Refactor the code with Functional Exception Handling

## Workflow

1. **Validate project before functional-exception changes**

Run `./mvnw validate` or `mvn validate` and stop immediately if validation fails.

2. **Check required dependencies**

When introducing `Either`, confirm VAVR (`io.vavr:vavr`) and SLF4J are present before implementation.

3. **Read functional-exception reference and identify targets**

Read `references/143-java-functional-exception-handling.md` and identify places to replace exception-heavy control flow with monadic error types.

4. **Apply functional exception-handling refactorings**

Implement selected `Optional`/`Either`/async error patterns with structured logging and clear error contracts.

5. **Verify with full build**

Run `./mvnw clean verify` or `mvn clean verify` after applying improvements.

## Reference

For detailed guidance, examples, and constraints, see [references/143-java-functional-exception-handling.md](references/143-java-functional-exception-handling.md).
