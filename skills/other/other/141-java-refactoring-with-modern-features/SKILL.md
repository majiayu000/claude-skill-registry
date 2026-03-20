---
name: 141-java-refactoring-with-modern-features
description: Use when you need to refactor Java code to adopt modern Java features (Java 8+) — including migrating anonymous classes to lambdas, replacing Iterator loops with Stream API, adopting Optional for null safety, switching from legacy Date/Calendar to java.time, using collection factory methods, applying text blocks, var inference, or leveraging Java 25 features like flexible constructor bodies and module import declarations. Part of the skills-for-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.13.0-SNAPSHOT
---
# Modern Java Development Guidelines (Java 8+)

Identify and apply modern Java (Java 8+) refactoring opportunities to improve readability, maintainability, and performance.

**What is covered in this Skill?**

- Lambda expressions and method references (over anonymous classes)
- Stream API for declarative collection processing
- `Optional` for null-safe APIs
- `java.time` API (replacing `Date`/`Calendar`)
- Default interface methods, `var` type inference
- Unmodifiable collection factory methods (`List.of()`, `Set.of()`, `Map.of()`)
- Text blocks for multi-line strings
- Java 25 Flexible Constructor Bodies (JEP 513)
- Java 25 Module Import Declarations (JEP 511)

**Scope:** The reference is organized by examples (good/bad code patterns) for each core area. Apply recommendations based on applicable examples.

## Constraints

Before applying any modern Java refactoring, ensure the project compiles. If compilation fails, stop immediately — do not proceed until the project compiles successfully. After applying improvements, run full verification.

- **MANDATORY**: Run `./mvnw compile` or `mvn compile` before applying any changes
- **SAFETY**: If compilation fails, stop immediately — do not proceed until the project compiles successfully
- **VERIFY**: Run `./mvnw clean verify` or `mvn clean verify` after applying improvements
- **BEFORE APPLYING**: Read the reference for detailed good/bad examples, constraints, and safeguards for each modern Java feature

## When to use this skill

- Review Java code for modern Java development
- Apply best practices for modern Java development in Java code

## Reference

For detailed guidance, examples, and constraints, see [references/141-java-refactoring-with-modern-features.md](references/141-java-refactoring-with-modern-features.md).
