---
name: 521-frameworks-micronaut-testing-unit-tests
description: Use when you need to write unit tests for Micronaut applications — Mockito-first with @ExtendWith(MockitoExtension.class), @MicronautTest with @MockBean, HttpClient @Client(/) assertions, @Property overrides, @ParameterizedTest, and *Test vs *IT naming. For framework-agnostic Java use @131-java-testing-unit-testing. This should trigger for requests such as Add or improve unit tests in a Micronaut project; Reduce unnecessary @MicronautTest usage with Mockito-first tests. Part of cursor-rules-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.15.0-SNAPSHOT
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
- **EDGE CASE**: If request scope is ambiguous, stop and ask a clarifying question before applying changes
- **EDGE CASE**: If required inputs, files, or tooling are missing, report what is missing and ask whether to proceed with setup guidance

## When to use this skill

- Add or improve unit tests in a Micronaut project
- Reduce unnecessary @MicronautTest usage with Mockito-first tests

## Workflow

1. **Read reference and assess project context**

Read `references/521-frameworks-micronaut-testing-unit-tests.md` and inspect the current project setup before proposing changes.

2. **Gather scope and decide target improvements**

Identify requested outcomes, constraints, and the minimum safe set of changes to apply.

3. **Apply framework-aligned changes**

Implement or refactor configuration/code following the reference patterns and project conventions.

4. **Run verification and report results**

Execute appropriate build/tests and summarize what changed, what was verified, and any follow-up actions.

## Reference

For detailed guidance, examples, and constraints, see [references/521-frameworks-micronaut-testing-unit-tests.md](references/521-frameworks-micronaut-testing-unit-tests.md).
