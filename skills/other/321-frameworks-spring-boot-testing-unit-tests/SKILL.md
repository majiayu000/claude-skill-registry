---
name: 321-frameworks-spring-boot-testing-unit-tests
description: Use when you need to write unit tests for Spring Boot applications — including pure unit tests with @ExtendWith(MockitoExtension.class) for @Service/@Component, slice tests with @WebMvcTest and @MockitoBean for controllers, @JsonTest for JSON serialization, parameterized tests with @CsvSource/@MethodSource, test profiles, and @TestConfiguration. For framework-agnostic Java use @131-java-testing-unit-testing. For integration tests use @322-frameworks-spring-boot-testing-integration-tests. This should trigger for requests such as Review Java code for Spring Boot unit tests; Apply best practices for Spring Boot unit tests in Java code. Part of cursor-rules-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.15.0-SNAPSHOT
---
# Spring Boot Unit Testing with Mockito

Apply Spring Boot unit testing guidelines with Mockito.

**What is covered in this Skill?**

- Pure unit tests: @ExtendWith(MockitoExtension.class), @Mock, @InjectMocks for @Service/@Component (no Spring context)
- Slice tests: @WebMvcTest, @MockitoBean for controllers (Spring Boot 4.0.x — @MockBean removed)
- @JsonTest for JSON serialization with correct JSON value assertions (extractingJsonPathStringValue, etc.)
- Parameterized tests: @ParameterizedTest with @CsvSource or @MethodSource over copy-pasted methods
- Java records for domain objects in tests
- @TestConfiguration, @ActiveProfiles, @Primary fixed-clock beans for deterministic test setup
- Modern mocking API: @MockitoBean / @MockitoSpyBean; @MockBean/@SpyBean are deprecated/removed in Boot 4.0.x

**Scope:** Apply recommendations based on the reference rules and good/bad code examples. For integration tests use @322-frameworks-spring-boot-testing-integration-tests.

## Constraints

Before applying any test changes, ensure the project compiles. If compilation fails, stop immediately. After applying improvements, run full verification.

- **MANDATORY**: Run `./mvnw compile` or `mvn compile` before applying any change
- **SAFETY**: If compilation fails, stop immediately
- **VERIFY**: Run `./mvnw clean verify` or `mvn clean verify` after applying improvements
- **BEFORE APPLYING**: Read the reference for detailed rules and good/bad patterns
- **EDGE CASE**: If request scope is ambiguous, stop and ask a clarifying question before applying changes
- **EDGE CASE**: If required inputs, files, or tooling are missing, report what is missing and ask whether to proceed with setup guidance

## When to use this skill

- Review Java code for Spring Boot unit tests
- Apply best practices for Spring Boot unit tests in Java code

## Workflow

1. **Read reference and assess project context**

Read `references/321-frameworks-spring-boot-testing-unit-tests.md` and inspect the current project setup before proposing changes.

2. **Gather scope and decide target improvements**

Identify requested outcomes, constraints, and the minimum safe set of changes to apply.

3. **Apply framework-aligned changes**

Implement or refactor configuration/code following the reference patterns and project conventions.

4. **Run verification and report results**

Execute appropriate build/tests and summarize what changed, what was verified, and any follow-up actions.

## Reference

For detailed guidance, examples, and constraints, see [references/321-frameworks-spring-boot-testing-unit-tests.md](references/321-frameworks-spring-boot-testing-unit-tests.md).
