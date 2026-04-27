---
name: 322-frameworks-spring-boot-testing-integration-tests
description: Use when you need to write or improve integration tests — including Testcontainers with @ServiceConnection, @DataJdbcTest persistence slices, TestRestTemplate or MockMvcTester for HTTP, data isolation, and container lifecycle management for Spring Boot 4.0.x. This should trigger for requests such as Review Java code for Spring Boot integration tests; Apply best practices for Spring Boot integration tests in Java code. Part of cursor-rules-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.15.0-SNAPSHOT
---
# Spring Boot Integration Testing

Apply Spring Boot integration testing guidelines for Spring Boot 4.0.x.

**What is covered in this Skill?**

- Integration test scope and purpose (verify wiring and contracts, not unit-test duplication)
- Testcontainers with @ServiceConnection for zero-config wiring (preferred)
- @DynamicPropertySource as fallback for containers without built-in service connection support
- Static @Container instances shared across test methods for performance
- MockMvcTester for fluent AssertJ-based HTTP assertions (Spring Boot 4.0.x)
- TestRestTemplate for full HTTP stack testing
- @DataJdbcTest / @DataJpaTest persistence slices (load only persistence layer, start faster)
- Data isolation: each test owns its scenario; no shared mutable state or ordering assumptions
- @MockitoBean for mock registration (Spring Boot 4.0.x — @MockBean removed)
- Resource lifecycle: Testcontainers JUnit integration for teardown; *IT / integration test separation

**Scope:** Apply recommendations based on the reference rules and good/bad code examples.

## Constraints

Before applying any integration test changes, ensure the project compiles. If compilation fails, stop immediately. After applying improvements, run full verification.

- **MANDATORY**: Run `./mvnw compile` or `mvn compile` before applying any change
- **SAFETY**: If compilation fails, stop immediately
- **VERIFY**: Run `./mvnw clean verify` or `mvn clean verify` after applying improvements
- **BEFORE APPLYING**: Read the reference for detailed rules and good/bad patterns
- **EDGE CASE**: If request scope is ambiguous, stop and ask a clarifying question before applying changes
- **EDGE CASE**: If required inputs, files, or tooling are missing, report what is missing and ask whether to proceed with setup guidance

## When to use this skill

- Review Java code for Spring Boot integration tests
- Apply best practices for Spring Boot integration tests in Java code

## Workflow

1. **Read reference and assess project context**

Read `references/322-frameworks-spring-boot-testing-integration-tests.md` and inspect the current project setup before proposing changes.

2. **Gather scope and decide target improvements**

Identify requested outcomes, constraints, and the minimum safe set of changes to apply.

3. **Apply framework-aligned changes**

Implement or refactor configuration/code following the reference patterns and project conventions.

4. **Run verification and report results**

Execute appropriate build/tests and summarize what changed, what was verified, and any follow-up actions.

## Reference

For detailed guidance, examples, and constraints, see [references/322-frameworks-spring-boot-testing-integration-tests.md](references/322-frameworks-spring-boot-testing-integration-tests.md).
