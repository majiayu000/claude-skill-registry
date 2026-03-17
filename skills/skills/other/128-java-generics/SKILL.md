---
name: 128-java-generics
description: Use when you need to review, improve, or refactor Java code for generics quality — including avoiding raw types, applying the PECS (Producer Extends Consumer Super) principle for wildcards, using bounded type parameters, designing effective generic methods, leveraging the diamond operator, understanding type erasure implications, handling generic inheritance correctly, preventing heap pollution with @SafeVarargs, and integrating generics with modern Java features like Records, sealed types, and pattern matching. Part of the skills-for-java project
metadata:
  author: Juan Antonio Breña Moral
  version: 0.12.0-SNAPSHOT
---
# Java Generics Best Practices

Review and improve Java code using comprehensive generics best practices that enforce compile-time type safety and enable flexible, reusable APIs.

**Core areas:** Type safety (avoiding raw types, eliminating unsafe casts), code reusability (generic methods and types for multiple type contexts), API clarity (PECS wildcards — `? extends` for producers, `? super` for consumers), performance optimization (eliminating boxing/casting overhead), diamond operator for type inference, type erasure awareness (type tokens, factory patterns, array creation), generic inheritance and variance (invariance, covariance, contravariance), `@SafeVarargs` for heap pollution prevention, wildcard capture helpers, self-bounded generics (CRTP) for fluent builders, proper wildcard API design with `Comparator<? super T>` and `Function<? super T, ? extends R>`, arrays-vs-generics covariance pitfalls, serialization with `TypeReference`/`TypeToken`, eliminating unchecked warnings, generic naming conventions (`T`, `E`, `K/V`, `?`), typesafe heterogeneous containers, and integration with Records, sealed types, and pattern matching.

**Prerequisites:** Run `./mvnw compile` or `mvn compile` before applying any change. If compilation fails, **stop immediately** and do not proceed — compilation failure is a blocking condition.

**Multi-step scope:** Step 1 validates the project compiles. Step 2 analyzes Java code to identify generics issues categorized by impact (CRITICAL, MAINTAINABILITY, PERFORMANCE, TYPE_SAFETY) and area (raw types, wildcard misuse, bounded parameter opportunities, type erasure problems, modern feature integration gaps). Step 3 eliminates raw types and unsafe casts with proper parameterization. Step 4 applies PECS wildcards and bounded type parameters for flexible APIs. Step 5 introduces diamond operator, generic methods, and type tokens for type erasure scenarios. Step 6 integrates generics with Records, sealed types, and pattern matching. Step 7 validates all changes compile and all tests pass with `./mvnw clean verify`.

**Before applying changes:** Read the reference for detailed examples, good/bad patterns, and constraints.

## Reference

For detailed guidance, examples, and constraints, see [references/128-java-generics.md](references/128-java-generics.md).
