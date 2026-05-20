---
name: 141-java-refactoring-with-modern-features
description: Use when you need to refactor Java code to adopt modern Java features (Java 8+) — including migrating anonymous classes to lambdas, replacing Iterator loops with Stream API, adopting Optional for null safety, switching from legacy Date/Calendar to java.time, using collection factory methods, migrating to CompletableFuture for async operations, applying text blocks, var inference, or leveraging Java 25 features like flexible constructor bodies and module import declarations. Part of the skills-for-java project
metadata:
  author: Juan Antonio Breña Moral
  version: 0.12.0-SNAPSHOT
---
# Modern Java Development Guidelines (Java 8+)

Identify and apply modern Java (Java 8+) refactoring opportunities to improve readability, maintainability, and performance.

**Core areas:** Lambda expressions and method references (over anonymous classes), Stream API for declarative collection processing, `Optional` for null-safe APIs, `java.time` API (replacing `Date`/`Calendar`), default interface methods, `var` type inference, unmodifiable collection factory methods (`List.of()`, `Set.of()`, `Map.of()`), `CompletableFuture` for composable async programming, text blocks for multi-line strings, Java 25 Flexible Constructor Bodies (JEP 513), and Java 25 Module Import Declarations (JEP 511).

**Prerequisites:** Run `./mvnw compile` or `mvn compile` before applying any changes. If compilation fails, **stop immediately** — do not proceed until the project compiles successfully.

**Multi-step scope:** Step 1 validates compilation. Step 2 categorizes refactoring opportunities by impact (CRITICAL, MAINTAINABILITY, PERFORMANCE, READABILITY). Step 3 applies lambda/method-reference conversions. Step 4 replaces imperative loops with Stream API pipelines. Step 5 introduces Optional for null-safe method returns. Step 6 migrates legacy date/time to `java.time`. Step 7 adopts collection factory methods and async CompletableFuture patterns. Step 8 applies text blocks, var, and Java 25 features where applicable. Step 9 runs `./mvnw clean verify` to confirm all tests pass after changes.

**Before applying changes:** Read the reference for detailed good/bad examples, constraints, and safeguards for each modern Java feature.

## Reference

For detailed guidance, examples, and constraints, see [references/141-java-refactoring-with-modern-features.md](references/141-java-refactoring-with-modern-features.md).
