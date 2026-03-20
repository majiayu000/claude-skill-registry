---
name: 144-java-data-oriented-programming
description: Use when you need to apply data-oriented programming best practices in Java — including separating code (behavior) from data structures using records, designing immutable data with pure transformation functions, keeping data flat and denormalized with ID-based references, starting with generic data structures converting to specific types when needed, ensuring data integrity through pure validation functions, and creating flexible generic data access layers. Part of the skills-for-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.13.0-SNAPSHOT
---
# Java Data-Oriented Programming Best Practices

Apply data-oriented programming in Java: separate data from behavior with records, use immutable data structures, pure functions for transformations, flat denormalized structures with ID references, generic-to-specific type conversion when needed, pure validation functions, and flexible generic data access layers. All transformations should be explicit, traceable, and composed of clear pure functional steps.

**What is covered in this Skill?**

- Separation of concerns: data structures (records, POJOs) vs behavior (utility classes, services)
- Immutability: records, final fields, transformations produce new instances
- Pure data transformations: functions depending only on inputs, no side effects
- Flat and denormalized data: ID references instead of deep nesting
- Generic until specific: Map&lt;String,Object&gt; for dynamic data, convert to records when processing
- Data integrity: pure validation functions returning validation results
- Flexible generic data access: generic CRUD interfaces, interchangeable implementations

**Scope:** The reference is organized by examples (good/bad code patterns) for each core area. Apply recommendations based on applicable examples.

## Constraints

Before applying any data-oriented programming recommendations, ensure the project compiles. Compilation failure is a blocking condition. After applying improvements, run full verification.

- **MANDATORY**: Run `./mvnw compile` or `mvn compile` before applying any change
- **SAFETY**: If compilation fails, stop immediately — do not proceed until resolved
- **VERIFY**: Run `./mvnw clean verify` or `mvn clean verify` after applying improvements
- **BEFORE APPLYING**: Read the reference for detailed good/bad examples, constraints, and safeguards for each data-oriented programming pattern

## When to use this skill

- Review Java code for data-oriented programming
- Apply best practices for data-oriented programming in Java code

## Reference

For detailed guidance, examples, and constraints, see [references/144-java-data-oriented-programming.md](references/144-java-data-oriented-programming.md).
