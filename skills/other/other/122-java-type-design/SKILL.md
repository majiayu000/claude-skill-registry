---
name: 122-java-type-design
description: Use when you need to review, improve, or refactor Java code for type design quality — including establishing clear type hierarchies, applying consistent naming conventions, eliminating primitive obsession with domain-specific value objects, leveraging generic type parameters, creating type-safe wrappers, designing fluent interfaces, ensuring precision-appropriate numeric types (BigDecimal for financial calculations), and improving type contrast through interfaces and method signature alignment. Part of the skills-for-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.13.0-SNAPSHOT
---
# Type Design Thinking in Java

Review and improve Java code using comprehensive type design principles that apply typography concepts to code structure and organization for maximum clarity and maintainability.

**What is covered in this Skill?**

- Clear type hierarchies: nested static classes, logical structure
- Consistent naming conventions: domain-driven patterns, uniform interface/implementation naming
- Strategic whitespace for readability
- Type-safe wrappers: value objects replacing primitive obsession (EmailAddress, Money)
- Generic type parameters: flexible reusable types, bounded parameters
- Domain-specific fluent interfaces: builder pattern, method chaining
- Type "weights": conceptual importance — core domain vs supporting vs utility
- Type contrast through interfaces: contract vs implementation separation
- Aligned method signatures: consistent parameter and return types across related classes
- Self-documenting code: clear descriptive names
- BigDecimal for precision-sensitive calculations (financial/monetary operations)
- Strategic type selection: Optional, Set vs List, interfaces over concrete types

**Scope:** The reference is organized by examples (good/bad code patterns) for each core area. Apply recommendations based on applicable examples.

## Constraints

Before applying any type design changes, ensure the project compiles. If compilation fails, stop immediately — do not proceed until resolved. After applying improvements, run full verification.

- **MANDATORY**: Run `./mvnw compile` or `mvn compile` before applying any change
- **SAFETY**: If compilation fails, stop immediately and do not proceed — compilation failure is a blocking condition
- **VERIFY**: Run `./mvnw clean verify` or `mvn clean verify` after applying improvements
- **BEFORE APPLYING**: Read the reference for detailed examples, good/bad patterns, and constraints

## When to use this skill

- Review Java code for type design
- Improve type design in Java code
- Fix primitive obsession in Java code
- Create value objects in Java code
- Create type hierarchies in Java code
- Create fluent interfaces in Java code

## Reference

For detailed guidance, examples, and constraints, see [references/122-java-type-design.md](references/122-java-type-design.md).
