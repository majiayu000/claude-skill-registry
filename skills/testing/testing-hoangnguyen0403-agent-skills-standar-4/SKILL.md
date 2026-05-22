---
name: Java Testing Standards
description: Modern testing practices using JUnit 5, AssertJ, and Mockito.
metadata:
  labels: [java, testing, junit, assertj, mockito]
  triggers:
    files: ['**/*Test.java', '**/*IT.java']
    keywords: [test, assert, mock, verify, junit]
---

# Java Testing Standards

## **Priority: P0 (CRITICAL)**

High-reliability testing using JUnit 5 and fluent assertions.

## Implementation Guidelines

- **Framework**: Use JUnit 5 (Jupiter). Avoid JUnit 4.
- **Assertions**: Use AssertJ (`assertThat`) over JUnit `assertEquals`. It's more readable and provides better error messages.
- **Naming**: `MethodName_StateUnderTesting_ExpectedBehavior` or `@DisplayName("Should return X when Y")`.
- **Parameterized**: Use `@ParameterizedTest` with `@ValueSource` or `@MethodSource` for data-driven tests.
- **Mocking**: Use Mockito. Strictly limit mocking to external dependencies (I/O). Do not mock data objects.
- **Integration**: Use **Testcontainers** for real databases/brokers in integration tests (`*IT.java`).
- **Visibility**: Test classes and methods can be package-private in JUnit 5 (no `public` needed).

## Anti-Patterns

- **Logic in Tests**: Tests should be declarative. No loops or heavy if/else.
- **`System.out`**: Never print in tests. Use Assertions.
- **Legacy Assertions**: Avoid `assertTrue(a == b)`. Use `assertThat(a).isEqualTo(b)`.
- **Global State**: Tests must be isolated. No strict dependency on execution order.

## Code

For a full `Mockito` + `AssertJ` test class template:
[references/junit-template.md](references/junit-template.md)

```java
// JUnit 5 + AssertJ
import static org.assertj.core.api.Assertions.assertThat;

class UserServiceTest {

    @Test
    @DisplayName("Should detect active users")
    void shouldDetectActiveUsers() {
        // Arrange
        var user = new User("id", "active");

        // Act
        boolean isActive = service.isActive(user);

        // Assert
        assertThat(isActive)
            .as("Check active user status")
            .isTrue();
    }
}
```

## Related Topics

best-practices | quality-assurance
