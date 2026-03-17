---
name: 142-java-functional-programming
description: Use when you need to apply functional programming principles in Java — including writing immutable objects and Records, pure functions, functional interfaces, lambda expressions, Stream API pipelines, Optional for null safety, function composition, higher-order functions, pattern matching for instanceof and switch, sealed classes/interfaces for controlled hierarchies, Stream Gatherers for custom operations, currying/partial application, effect boundary separation, and concurrent-safe functional patterns.
metadata:
  author: Juan Antonio Breña Moral
  version: 0.12.0-SNAPSHOT
---
# Java Functional Programming rules

Identify and apply functional programming principles in Java to improve immutability, expressiveness, and maintainability.

**Core areas:** Immutable objects and Records (JEP 395), pure functions free of side effects, functional interfaces (`Function`, `Predicate`, `Consumer`, `Supplier`) and custom `@FunctionalInterface` types, lambda expressions and method references, Stream API (filter/map/reduce pipelines, parallel streams, `toUnmodifiable*` collectors), `Optional` idiomatic usage (`map`/`flatMap`/`filter`/`orElse*` over `isPresent()`+`get()`), function composition (`andThen`/`compose`), higher-order functions (memoization, currying, partial application), Pattern Matching for `instanceof` and `switch` (Java 21), sealed classes and interfaces (Java 17) for exhaustive domain hierarchies, Switch Expressions (Java 14) for concise multi-way conditionals, Stream Gatherers (JEP 461) for custom intermediate operations, effect-boundary separation (side effects at edges, pure core logic), and immutable collections (`List.of()`, `Collectors.toUnmodifiableList()`).

**Prerequisites:** Run `./mvnw compile` or `mvn compile` before applying any changes. If compilation fails, **stop immediately** — do not proceed until the project compiles successfully. Also verify that the project's `maven-compiler-plugin` source/target supports the Java features being used.

**Multi-step scope:** Step 1 validates compilation. Step 2 categorizes functional programming opportunities by impact (CRITICAL, MAINTAINABILITY, PERFORMANCE, EXPRESSIVENESS) and area (immutability violations, side effects, imperative patterns, type safety gaps). Step 3 converts mutable objects to immutable Records or final classes. Step 4 extracts pure functions from methods with side effects. Step 5 replaces imperative loops with declarative Stream API operations. Step 6 adopts `Optional` for null-safe method returns and functional chaining. Step 7 applies function composition, currying, and higher-order functions. Step 8 introduces sealed types, pattern matching, and switch expressions for type-safe conditional logic. Step 9 hardens collectors (merge functions for `toMap`, downstream collectors, unmodifiable results). Step 10 runs `./mvnw clean verify` to confirm all tests pass after changes.

**Before applying changes:** Read the reference for detailed good/bad examples, constraints, and safeguards for each functional programming pattern.

## Reference

For detailed guidance, examples, and constraints, see [references/142-java-functional-programming.md](references/142-java-functional-programming.md).
