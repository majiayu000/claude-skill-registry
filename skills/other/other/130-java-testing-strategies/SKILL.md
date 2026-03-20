---
name: 130-java-testing-strategies
description: Use when you need to apply testing strategies for Java code — RIGHT-BICEP to guide test creation, A-TRIP for test quality characteristics, or CORRECT for verifying boundary conditions. Part of the skills-for-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.13.0-SNAPSHOT
---
# Java testing strategies

Apply proven testing strategies (RIGHT-BICEP, A-TRIP, CORRECT) to design and verify Java unit tests.

**What is covered in this Skill?**

- **RIGHT-BICEP**: Key questions to guide test creation — Right results, Boundary conditions, Inverse relationships, Cross-checks, Error conditions, Performance
- **A-TRIP**: Characteristics of good tests — Automatic, Thorough, Repeatable, Independent, Professional
- **CORRECT**: Boundary condition verification — Conformance, Ordering, Range, Reference, Existence, Cardinality, Time


## Constraints

Before applying any test strategy changes, ensure the project compiles. If compilation fails, stop immediately — do not proceed until resolved. After applying improvements, run full verification.

- **MANDATORY**: Run `./mvnw compile` or `mvn compile` before applying any change
- **SAFETY**: If compilation fails, stop immediately and do not proceed — compilation failure is a blocking condition
- **VERIFY**: Run `./mvnw clean verify` or `mvn clean verify` after applying improvements
- **BEFORE APPLYING**: Read the reference for detailed examples, good/bad patterns, and constraints

## When to use this skill

- Review Java code for testing strategies
- Apply RIGHT-BICEP testing strategies in Java code
- Apply A-TRIP testing strategies in Java code
- Apply CORRECT boundary condition verification in Java code

## Reference

For detailed guidance, examples, and constraints, see [references/130-java-testing-strategies.md](references/130-java-testing-strategies.md).
