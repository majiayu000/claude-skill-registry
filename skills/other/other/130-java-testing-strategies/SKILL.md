---
name: 130-java-testing-strategies
description: Use when you need to apply testing strategies for Java code — RIGHT-BICEP to guide test creation, A-TRIP for test quality characteristics, or CORRECT for verifying boundary conditions. This should trigger for requests such as Review Java code for testing strategies; Apply RIGHT-BICEP testing strategies in Java code; Apply A-TRIP testing strategies in Java code; Apply CORRECT boundary condition verification in Java code. Part of cursor-rules-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.15.0-SNAPSHOT
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
- **EDGE CASE**: If the user goal is ambiguous, stop and ask a clarifying question before editing files or running project-wide commands
- **EDGE CASE**: If required context, files, credentials, or tools are missing, report the blocker explicitly and ask whether to proceed with setup or fallback guidance
- **EDGE CASE**: If requested changes conflict with project constraints or safety boundaries, explain the conflict and ask for user confirmation on the preferred trade-off

## When to use this skill

- Review Java code for testing strategies
- Apply RIGHT-BICEP testing strategies in Java code
- Apply A-TRIP testing strategies in Java code
- Apply CORRECT boundary condition verification in Java code

## Workflow

1. **Compile project before test-strategy changes**

Run `./mvnw compile` or `mvn compile` and stop immediately if compilation fails.

2. **Read testing-strategies reference**

Read `references/130-java-testing-strategies.md` and map current tests to RIGHT-BICEP, A-TRIP, and CORRECT gaps.

3. **Apply strategy-driven test improvements**

Improve or add tests to cover missing boundaries, quality characteristics, and verification depth.

4. **Verify with full build**

Run `./mvnw clean verify` or `mvn clean verify` after applying improvements.

## Reference

For detailed guidance, examples, and constraints, see [references/130-java-testing-strategies.md](references/130-java-testing-strategies.md).
