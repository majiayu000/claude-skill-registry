---
name: 322-frameworks-spring-boot-testing-integration-tests
description: Use when you need to write or improve integration tests — including Testcontainers with @ServiceConnection, @DataJdbcTest persistence slices, TestRestTemplate or MockMvcTester for HTTP, data isolation, and container lifecycle management for Spring Boot 4.0.x. Part of the skills-for-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.14.0-SNAPSHOT
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

## When to use this skill

- Review Java code for Spring Boot integration tests
- Apply best practices for Spring Boot integration tests in Java code

## Reference

For detailed guidance, examples, and constraints, see [references/322-frameworks-spring-boot-testing-integration-tests.md](references/322-frameworks-spring-boot-testing-integration-tests.md).
