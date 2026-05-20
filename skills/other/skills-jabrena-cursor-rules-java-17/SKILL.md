---
name: 122-java-type-design
description: Use when you need to review, improve, or refactor Java code for type design quality — including establishing clear type hierarchies, applying consistent naming conventions, eliminating primitive obsession with domain-specific value objects, leveraging generic type parameters, creating type-safe wrappers, designing fluent interfaces, ensuring precision-appropriate numeric types (BigDecimal for financial calculations), and improving type contrast through interfaces and method signature alignment.
metadata:
  author: Juan Antonio Breña Moral
  version: 0.12.0-SNAPSHOT
---
# Type Design Thinking in Java

Review and improve Java code using comprehensive type design principles that apply typography concepts to code structure and organization for maximum clarity and maintainability.

**Core areas:** Clear type hierarchies (nested static classes, logical structure), consistent naming conventions (domain-driven patterns, uniform interface/implementation naming), strategic whitespace for readability, type-safe wrappers (value objects replacing primitive obsession, EmailAddress, Money), generic type parameters (flexible reusable types, bounded parameters), domain-specific fluent interfaces (builder pattern, method chaining), type "weights" (conceptual importance assignment — core domain vs supporting vs utility), type contrast through interfaces (contract vs implementation separation), aligned method signatures (consistent parameter and return types across related classes), self-documenting code (clear descriptive names), BigDecimal for precision-sensitive calculations (financial/monetary operations), and strategic type selection (Optional, Set vs List, interfaces over concrete types).

**Prerequisites:** Run `./mvnw compile` or `mvn compile` before applying any change. If compilation fails, **stop immediately** and do not proceed — compilation failure is a blocking condition.

**Multi-step scope:** Step 1 validates the project compiles. Step 2 analyzes Java code to identify type design issues categorized by impact (CRITICAL, MAINTAINABILITY, TYPE_SAFETY, READABILITY) and area (naming conventions, type hierarchies, generic usage, primitive obsession, type safety, precision). Step 3 applies naming convention improvements and type hierarchy restructuring. Step 4 eliminates primitive obsession by creating domain-specific value objects and records. Step 5 introduces proper generic type parameters with appropriate bounds and type-safe wrappers. Step 6 implements precision-appropriate numeric types and strategic collection/type selection. Step 7 validates all changes compile and all tests pass with `./mvnw clean verify`.

**Before applying changes:** Read the reference for detailed examples, good/bad patterns, and constraints.

## Reference

For detailed guidance, examples, and constraints, see [references/122-java-type-design.md](references/122-java-type-design.md).
