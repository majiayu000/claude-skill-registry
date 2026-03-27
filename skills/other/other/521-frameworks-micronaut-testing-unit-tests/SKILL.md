---
name: 521-frameworks-micronaut-testing-unit-tests
description: Use when you need to write unit tests for Micronaut applications — Mockito-first with @ExtendWith(MockitoExtension.class), @MicronautTest with @MockBean, HttpClient @Client("/") assertions, @Property overrides, @ParameterizedTest, and *Test vs *IT naming. For framework-agnostic Java use @131-java-testing-unit-testing. Part of the skills-for-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.13.0-SNAPSHOT
---
# Micronaut Unit Testing

Apply fast testing strategies for Micronaut: Mockito-first, narrow @MicronautTest when HTTP or DI replacement is required.

**What is covered in this Skill?**

- Pure JUnit 5 + Mockito without container boot
- @MicronautTest with @MockBean factory methods for collaborators
- HttpClient blocking exchanges against the embedded server
- @Property for deterministic configuration in tests
- @ParameterizedTest with @CsvSource / @MethodSource
- Naming: *Test → Surefire; *IT → Failsafe when configured
- When to escalate to `@522`

**Scope:** Apply recommendations based on the reference rules and good/bad code examples.

## Constraints

Compile before test refactors; verify the full suite after.

- **MANDATORY**: Run `./mvnw compile` or `mvn compile` before applying any change
- **SAFETY**: If compilation fails, stop immediately
- **VERIFY**: Run `./mvnw clean verify` or `mvn clean verify` after applying improvements
- **BEFORE APPLYING**: Read the reference for detailed rules and examples

## When to use this skill

- Add or improve unit tests in a Micronaut project
- Reduce unnecessary @MicronautTest usage with Mockito-first tests

## Reference

For detailed guidance, examples, and constraints, see [references/521-frameworks-micronaut-testing-unit-tests.md](references/521-frameworks-micronaut-testing-unit-tests.md).
