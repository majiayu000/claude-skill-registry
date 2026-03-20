---
name: 128-java-generics
description: Use when you need to review, improve, or refactor Java code for generics quality — including avoiding raw types, applying the PECS (Producer Extends Consumer Super) principle for wildcards, using bounded type parameters, designing effective generic methods, leveraging the diamond operator, understanding type erasure implications, handling generic inheritance correctly, preventing heap pollution with @SafeVarargs, and integrating generics with modern Java features like Records, sealed types, and pattern matching. Part of the skills-for-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.13.0-SNAPSHOT
---
# Java Generics Best Practices

Review and improve Java code using comprehensive generics best practices that enforce compile-time type safety and enable flexible, reusable APIs.

**What is covered in this Skill?**

- Type safety: avoiding raw types, eliminating unsafe casts
- Code reusability: generic methods and types for multiple type contexts
- PECS wildcards: `? extends` for producers, `? super` for consumers
- Diamond operator for type inference
- Type erasure awareness: type tokens, factory patterns, array creation
- Generic inheritance and variance: invariance, covariance, contravariance
- `@SafeVarargs` for heap pollution prevention
- Wildcard capture helpers, self-bounded generics (CRTP) for fluent builders
- Proper wildcard API design: `Comparator<? super T>`, `Function<? super T, ? extends R>`
- Arrays-vs-generics covariance pitfalls, serialization with `TypeReference`/`TypeToken`
- Generic naming conventions (`T`, `E`, `K/V`, `?`), typesafe heterogeneous containers
- Integration with Records, sealed types, and pattern matching

**Scope:** The reference is organized by examples (good/bad code patterns) for each core area. Apply recommendations based on applicable examples.

## Constraints

Before applying any generics changes, ensure the project compiles. If compilation fails, stop immediately — do not proceed until resolved. After applying improvements, run full verification.

- **MANDATORY**: Run `./mvnw compile` or `mvn compile` before applying any change
- **SAFETY**: If compilation fails, stop immediately and do not proceed — compilation failure is a blocking condition
- **VERIFY**: Run `./mvnw clean verify` or `mvn clean verify` after applying improvements
- **BEFORE APPLYING**: Read the reference for detailed examples, good/bad patterns, and constraints

## When to use this skill

- Review Java code for generics
- Apply best practices for generics in Java code

## Reference

For detailed guidance, examples, and constraints, see [references/128-java-generics.md](references/128-java-generics.md).
