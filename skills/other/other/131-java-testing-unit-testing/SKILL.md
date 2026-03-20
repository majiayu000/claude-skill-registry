---
name: 131-java-testing-unit-testing
description: Use when you need to review, improve, or write Java unit tests — including migrating from JUnit 4 to JUnit 5, adopting AssertJ for fluent assertions, structuring tests with Given-When-Then, ensuring test independence, applying parameterized tests, mocking dependencies with Mockito, verifying boundary conditions (RIGHT-BICEP, CORRECT, A-TRIP), leveraging JSpecify null-safety annotations, or eliminating testing anti-patterns such as reflection-based tests or shared mutable state. Part of the skills-for-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.13.0-SNAPSHOT
---
# Java Unit testing guidelines

Review and improve Java unit tests using modern JUnit 5, AssertJ, and Mockito best practices.

**What is covered in this Skill?**

- JUnit 5 annotations: `@Test`, `@BeforeEach`, `@AfterEach`, `@DisplayName`, `@Nested`, `@ParameterizedTest`
- AssertJ fluent assertions: `assertThat`, `assertThatThrownBy`
- Given-When-Then test structure, descriptive test naming, single-responsibility tests
- Test independence and isolated state
- Parameterized tests: `@ValueSource`/`@CsvSource`/`@MethodSource`
- Mockito dependency mocking: `@Mock`, `@InjectMocks`, `MockitoExtension`
- Code coverage guidance (JaCoCo), package-private test visibility
- Testing anti-patterns: reflection, shared state, hard-coded values, testing implementation details
- Error handling: `assertThatThrownBy`, exception messages
- JSpecify null-safety: `@NullMarked`, `@Nullable`
- RIGHT-BICEP coverage principles, A-TRIP test quality, CORRECT boundary condition verification

**Scope:** The reference is organized by examples (good/bad code patterns) for each core area. Apply recommendations based on applicable examples.

## Constraints

Before applying any unit test changes, ensure the project compiles. If compilation fails, stop immediately — do not proceed until resolved. After applying improvements, run full verification.

- **MANDATORY**: Run `./mvnw compile` or `mvn compile` before applying any change
- **SAFETY**: If compilation fails, stop immediately and do not proceed — compilation failure is a blocking condition
- **VERIFY**: Run `./mvnw clean verify` or `mvn clean verify` after applying improvements
- **BEFORE APPLYING**: Read the reference for detailed examples, good/bad patterns, and constraints

## When to use this skill

- Review Java code for unit tests
- Apply best practices for unit tests in Java code

## Reference

For detailed guidance, examples, and constraints, see [references/131-java-testing-unit-testing.md](references/131-java-testing-unit-testing.md).
