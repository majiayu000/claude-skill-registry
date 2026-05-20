---
name: 131-java-testing-unit-testing
description: Use when you need to review, improve, or write Java unit tests — including migrating from JUnit 4 to JUnit 5, adopting AssertJ for fluent assertions, structuring tests with Given-When-Then, ensuring test independence, applying parameterized tests, mocking dependencies with Mockito, verifying boundary conditions (RIGHT-BICEP, CORRECT, A-TRIP), leveraging JSpecify null-safety annotations, or eliminating testing anti-patterns such as reflection-based tests or shared mutable state.
metadata:
  author: Juan Antonio Breña Moral
  version: 0.12.0-SNAPSHOT
---
# Java Unit testing guidelines

Review and improve Java unit tests using modern JUnit 5, AssertJ, and Mockito best practices.

**Core areas:** JUnit 5 annotations (`@Test`, `@BeforeEach`, `@AfterEach`, `@DisplayName`, `@Nested`, `@ParameterizedTest`), AssertJ fluent assertions (`assertThat`, `assertThatThrownBy`), Given-When-Then test structure, descriptive test naming, single-responsibility tests, test independence and isolated state, parameterized tests with `@ValueSource`/`@CsvSource`/`@MethodSource`, Mockito dependency mocking (`@Mock`, `@InjectMocks`, `MockitoExtension`), code coverage guidance (JaCoCo), package-private test visibility, code-splitting strategies (small methods, helper functions), testing anti-patterns (reflection, shared state, hard-coded values, testing implementation details), state management (immutable objects, `@BeforeEach` reset), error handling (`assertThatThrownBy`, exception messages), JSpecify null-safety (`@NullMarked`, `@Nullable`), RIGHT-BICEP coverage principles, A-TRIP test quality characteristics, and CORRECT boundary condition verification.

**Prerequisites:** Run `./mvnw compile` or `mvn compile` before applying any change. If compilation fails, **stop immediately** and do not proceed — compilation failure is a blocking condition.

**Multi-step scope:** Step 1 validates the project compiles. Step 2 analyzes existing tests and categorizes issues by impact (CRITICAL, MAINTAINABILITY, PERFORMANCE, COVERAGE, RELIABILITY). Step 3 migrates to JUnit 5 with modern annotations. Step 4 adopts AssertJ for expressive assertions. Step 5 restructures tests using Given-When-Then with descriptive naming. Step 6 ensures test independence by eliminating shared state and order dependencies. Step 7 adds parameterized tests and boundary-condition coverage. Step 8 integrates Mockito mocking for external dependencies.

**Before applying changes:** Read the reference for detailed examples, good/bad patterns, and constraints.

## Reference

For detailed guidance, examples, and constraints, see [references/131-java-unit-testing.md](references/131-java-unit-testing.md).
