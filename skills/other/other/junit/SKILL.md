---
name: junit
description: JUnit Java testing framework. Use for Java testing.
---

# JUnit 5

JUnit is the programmer-friendly testing framework for Java and the JVM. JUnit 5 is the current major version, composed of the JUnit Platform, JUnit Jupiter, and JUnit Vintage.

## When to Use

- **Java Projects**: The standard. Spring Boot starts with `spring-boot-starter-test` which includes JUnit 5.
- **Unit & Integration**: From testing a single method to spinning up a database context (with Testcontainers).

## Quick Start (JUnit 5 / Jupiter)

```java
import static org.junit.jupiter.api.Assertions.assertEquals;
import org.junit.jupiter.api.Test;

class CalculatorTest {

    @Test
    void addition() {
        assertEquals(2, 1 + 1, "Optional failure message");
    }
}
```

## Core Concepts

### Lifecycle Annotations

- `@BeforeEach` / `@AfterEach`: Run before/after every test method.
- `@BeforeAll` / `@AfterAll`: Run once per class (must be static).

### Parameterized Tests

Running the same test with different inputs.

```java
@ParameterizedTest
@ValueSource(strings = { "racecar", "radar", "able was I ere I saw elba" })
void palindromes(String candidate) {
    assertTrue(StringUtils.isPalindrome(candidate));
}
```

### Assertions

`assertThrows`, `assertTimeout`, `assertAll` (Grouped assertions).

## Best Practices (2025)

**Do**:

- **Use `@DisplayName`**: Give tests readable sentences as names ("Should return 404 when user not found").
- **Use AssertJ**: JUnit assertions are basic. AssertJ (`assertThat(actual).isEqualTo(expected)`) is fluent and better.
- **Testcontainers**: For integration tests, use Testcontainers with JUnit 5 annotations to spin up real Docker DBs.

**Don't**:

- **Don't use `System.out.println`**: Use a logger or assertions.
- **Don't use JUnit 4**: `@Test` (org.junit.Test) is old. Use `@Test` (org.junit.jupiter.api.Test).

## References

- [JUnit 5 User Guide](https://junit.org/junit5/docs/current/user-guide/)
