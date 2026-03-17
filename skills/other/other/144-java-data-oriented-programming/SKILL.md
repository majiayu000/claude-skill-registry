---
name: 144-java-data-oriented-programming
description: Use when you need to apply data-oriented programming best practices in Java — including separating code (behavior) from data structures using records, designing immutable data with pure transformation functions, keeping data flat and denormalized with ID-based references, starting with generic data structures converting to specific types when needed, ensuring data integrity through pure validation functions, and creating flexible generic data access layers. Part of the skills-for-java project
metadata:
  author: Juan Antonio Breña Moral
  version: 0.12.0-SNAPSHOT
---
# Java Data-Oriented Programming Best Practices

Identify and apply data-oriented programming best practices in Java to improve code clarity, maintainability, and predictability by strictly separating data structures from behavior and ensuring all data transformations are explicit, pure, and traceable.

**Core areas:** Records for immutable data carriers over mutable POJOs, data-behavior separation with pure static utility classes holding operations, pure functions for data transformation that depend only on inputs and produce no side effects, flat denormalized data structures with ID-based references over deep nesting, generic `Map<String, Object>` representations for dynamic schemas converted to specific types when needed, `Optional<T>` and custom result types in validation functions instead of throwing exceptions, generic `DataStore<ID, T>` interfaces for flexible data access layers, composable `Function<A, B>` pipelines using `andThen` for explicit and traceable multi-step transformations.

**Prerequisites:** Run `./mvnw compile` before applying any changes. If compilation fails, **stop immediately** — do not proceed until the project compiles successfully.

**Multi-step scope:** Step 1 validates the project compiles. Step 2 categorizes data-oriented programming opportunities by impact (CRITICAL, MAINTAINABILITY, PERFORMANCE, CLARITY) and area (data-behavior separation, immutability violations, impure functions, nested data structures, generic vs specific types, validation approaches). Step 3 separates data from behavior by extracting Records as pure data carriers and moving operations to static utility classes. Step 4 establishes immutability throughout the codebase using Records, `List.copyOf()`, and `Collections.unmodifiableList()`. Step 5 extracts pure static functions for all data processing and transformation operations to eliminate side effects. Step 6 flattens complex nested object hierarchies using ID references and lookup patterns in flat `Map`-based stores. Step 7 implements generic and flexible data types starting with `Map<String, Object>` for dynamic schemas, converting to specific record types via explicit converter classes with validation. Step 8 establishes validation boundaries using pure functions that return `Optional<String>` error messages or result types instead of throwing exceptions for business validation. Step 9 designs flexible generic `DataStore<ID, T>` interfaces to decouple access logic from storage implementations. Step 10 creates composable data transformation pipelines using `Function.andThen()` with explicit tracing at each step. Step 11 runs `./mvnw clean verify` to confirm all tests pass after changes.

**Before applying changes:** Read the reference for detailed good/bad examples, constraints, and safeguards for each data-oriented programming pattern.

## Reference

For detailed guidance, examples, and constraints, see [references/144-java-data-oriented-programming.md](references/144-java-data-oriented-programming.md).
