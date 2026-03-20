---
name: 321-frameworks-spring-boot-testing-unit-tests
description: Use when you need to write unit tests for Spring Boot applications — including pure unit tests with @ExtendWith(MockitoExtension.class) for @Service/@Component, slice tests with @WebMvcTest and @MockBean for controllers, @JsonTest for JSON serialization. For framework-agnostic Java use @131-java-testing-unit-testing. Part of the skills-for-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.13.0-SNAPSHOT
---
# Spring Boot Unit Testing with Mockito

Apply Spring Boot unit testing guidelines with Mockito.

**What is covered in this Skill?**

- Pure unit tests: @ExtendWith(MockitoExtension.class), @Mock, @InjectMocks for @Service/@Component (no Spring context)
- Slice tests: @WebMvcTest, @MockBean for controllers
- @JsonTest for JSON serialization
- @TestConfiguration, @ActiveProfiles for test setup

**Scope:** Apply recommendations based on the reference rules and good/bad code examples. For integration tests use @322-frameworks-spring-boot-testing-integration-tests.

## Constraints

Before applying any test changes, ensure the project compiles. If compilation fails, stop immediately. After applying improvements, run full verification.

- **MANDATORY**: Run `./mvnw compile` or `mvn compile` before applying any change
- **SAFETY**: If compilation fails, stop immediately
- **VERIFY**: Run `./mvnw clean verify` or `mvn clean verify` after applying improvements
- **BEFORE APPLYING**: Read the reference for detailed rules and good/bad patterns

## When to use this skill

- Review Java code for Spring Boot unit tests
- Apply best practices for Spring Boot unit tests in Java code

## Reference

For detailed guidance, examples, and constraints, see [references/321-frameworks-spring-boot-testing-unit-tests.md](references/321-frameworks-spring-boot-testing-unit-tests.md).
