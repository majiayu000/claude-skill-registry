---
name: unit-test-parameterized
description: Parameterized testing patterns with @ParameterizedTest, @ValueSource, @CsvSource. Run single test method with multiple input combinations. Use when testing multiple scenarios with similar logic.
category: testing
tags: [junit-5, parameterized-test, value-source, csv-source, method-source]
version: 1.0.1
---

# Parameterized Unit Tests with JUnit 5

Write efficient parameterized unit tests that run the same test logic with multiple input values. Reduce test duplication and improve test coverage using @ParameterizedTest.

## When to Use This Skill

Use this skill when:
- Testing methods with multiple valid inputs
- Testing boundary values systematically
- Testing multiple invalid inputs for error cases
- Want to reduce test duplication
- Testing multiple scenarios with similar assertions
- Need data-driven testing approach

## Setup: Parameterized Testing

### Maven
```xml
<dependency>
  <groupId>org.junit.jupiter</groupId>
  <artifactId>junit-jupiter</artifactId>
  <scope>test</scope>
</dependency>
<dependency>
  <groupId>org.assertj</groupId>
  <artifactId>assertj-core</artifactId>
  <scope>test</scope>
</dependency>
```

### Gradle
```kotlin
dependencies {
  testImplementation("org.junit.jupiter:junit-jupiter")
  testImplementation("org.assertj:assertj-core")
}
```

## Basic Pattern: @ValueSource

### Simple Value Testing

```java
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;
import static org.assertj.core.api.Assertions.*;

class StringUtilsTest {

  @ParameterizedTest
  @ValueSource(strings = {"hello", "world", "test"})
  void shouldCapitalizeAllStrings(String input) {
    String result = StringUtils.capitalize(input);
    assertThat(result).startsWith(input.substring(0, 1).toUpperCase());
  }

  @ParameterizedTest
  @ValueSource(ints = {1, 2, 3, 4, 5})
  void shouldBePositive(int number) {
    assertThat(number).isPositive();
  }

  @ParameterizedTest
  @ValueSource(booleans = {true, false})
  void shouldHandleBothBooleanValues(boolean value) {
    assertThat(value).isNotNull();
  }
}
```

## @MethodSource for Complex Data

### Factory Method Data Source

```java
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.MethodSource;
import java.util.stream.Stream;

class CalculatorTest {

  static Stream<org.junit.jupiter.params.provider.Arguments> additionTestCases() {
    return Stream.of(
      Arguments.of(1, 2, 3),
      Arguments.of(0, 0, 0),
      Arguments.of(-1, 1, 0),
      Arguments.of(100, 200, 300),
      Arguments.of(-5, -10, -15)
    );
  }

  @ParameterizedTest
  @MethodSource("additionTestCases")
  void shouldAddNumbersCorrectly(int a, int b, int expected) {
    int result = Calculator.add(a, b);
    assertThat(result).isEqualTo(expected);
  }
}
```

## @CsvSource for Tabular Data

### CSV-Based Test Data

```java
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;

class UserValidationTest {

  @ParameterizedTest
  @CsvSource({
    "alice@example.com, true",
    "bob@gmail.com, true",
    "invalid-email, false",
    "user@, false",
    "@example.com, false",
    "user name@example.com, false"
  })
  void shouldValidateEmailAddresses(String email, boolean expected) {
    boolean result = UserValidator.isValidEmail(email);
    assertThat(result).isEqualTo(expected);
  }

  @ParameterizedTest
  @CsvSource({
    "123-456-7890, true",
    "555-123-4567, true",
    "1234567890, false",
    "123-45-6789, false",
    "abc-def-ghij, false"
  })
  void shouldValidatePhoneNumbers(String phone, boolean expected) {
    boolean result = PhoneValidator.isValid(phone);
    assertThat(result).isEqualTo(expected);
  }
}
```

## @CsvFileSource for External Data

### CSV File-Based Testing

```java
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvFileSource;

class PriceCalculationTest {

  @ParameterizedTest
  @CsvFileSource(resources = "/test-data/prices.csv", numLinesToSkip = 1)
  void shouldCalculateTotalPrice(String product, double price, int quantity, double expected) {
    double total = PriceCalculator.calculateTotal(price, quantity);
    assertThat(total).isEqualTo(expected);
  }
}

// test-data/prices.csv:
// product,price,quantity,expected
// Laptop,999.99,1,999.99
// Mouse,29.99,3,89.97
// Keyboard,79.99,2,159.98
```

## @EnumSource for Enum Testing

### Enum-Based Test Data

```java
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.EnumSource;

enum Status { ACTIVE, INACTIVE, PENDING, DELETED }

class StatusHandlerTest {

  @ParameterizedTest
  @EnumSource(Status.class)
  void shouldHandleAllStatuses(Status status) {
    assertThat(status).isNotNull();
  }

  @ParameterizedTest
  @EnumSource(value = Status.class, names = {"ACTIVE", "INACTIVE"})
  void shouldHandleSpecificStatuses(Status status) {
    assertThat(status).isIn(Status.ACTIVE, Status.INACTIVE);
  }

  @ParameterizedTest
  @EnumSource(value = Status.class, mode = EnumSource.Mode.EXCLUDE, names = {"DELETED"})
  void shouldHandleStatusesExcludingDeleted(Status status) {
    assertThat(status).isNotEqualTo(Status.DELETED);
  }
}
```

## Custom Display Names

### Readable Test Output

```java
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;

class DiscountCalculationTest {

  @ParameterizedTest(name = "Discount of {0}% should be calculated correctly")
  @ValueSource(ints = {5, 10, 15, 20})
  void shouldApplyDiscount(int discountPercent) {
    double originalPrice = 100.0;
    double discounted = DiscountCalculator.apply(originalPrice, discountPercent);
    double expected = originalPrice * (1 - discountPercent / 100.0);
    
    assertThat(discounted).isEqualTo(expected);
  }

  @ParameterizedTest(name = "User role {0} should have {1} permissions")
  @CsvSource({
    "ADMIN, 100",
    "MANAGER, 50",
    "USER, 10"
  })
  void shouldHaveCorrectPermissions(String role, int expectedPermissions) {
    User user = new User(role);
    assertThat(user.getPermissionCount()).isEqualTo(expectedPermissions);
  }
}
```

## Combining Multiple Sources

### ArgumentsProvider for Complex Scenarios

```java
import org.junit.jupiter.api.extension.ExtensionContext;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.Arguments;
import org.junit.jupiter.params.provider.ArgumentsProvider;
import org.junit.jupiter.params.provider.ArgumentsSource;
import java.util.stream.Stream;

class RangeValidatorArgumentProvider implements ArgumentsProvider {
  @Override
  public Stream<? extends Arguments> provideArguments(ExtensionContext context) {
    return Stream.of(
      Arguments.of(0, 0, 100, true),      // Min boundary
      Arguments.of(100, 0, 100, true),    // Max boundary
      Arguments.of(50, 0, 100, true),     // Middle value
      Arguments.of(-1, 0, 100, false),    // Below range
      Arguments.of(101, 0, 100, false)    // Above range
    );
  }
}

class RangeValidatorTest {

  @ParameterizedTest
  @ArgumentsSource(RangeValidatorArgumentProvider.class)
  void shouldValidateRangeCorrectly(int value, int min, int max, boolean expected) {
    boolean result = RangeValidator.isInRange(value, min, max);
    assertThat(result).isEqualTo(expected);
  }
}
```

## Testing Edge Cases with Parameters

### Boundary Value Analysis

```java
class BoundaryValueTest {

  @ParameterizedTest
  @ValueSource(ints = {
    Integer.MIN_VALUE,    // Absolute minimum
    Integer.MIN_VALUE + 1, // Just above minimum
    -1,                    // Negative boundary
    0,                     // Zero boundary
    1,                     // Just above zero
    Integer.MAX_VALUE - 1, // Just below maximum
    Integer.MAX_VALUE      // Absolute maximum
  })
  void shouldHandleAllBoundaryValues(int value) {
    int incremented = MathUtils.increment(value);
    assertThat(incremented).isNotLessThan(value);
  }

  @ParameterizedTest
  @CsvSource({
    ",                    false", // null
    "'',                   false", // empty
    "'   ',                false", // whitespace only
    "a,                    true",  // single character
    "abc,                  true"   // normal
  })
  void shouldValidateStrings(String input, boolean expected) {
    boolean result = StringValidator.isValid(input);
    assertThat(result).isEqualTo(expected);
  }
}
```

## Repeat Tests

### Run Same Test Multiple Times

```java
import org.junit.jupiter.api.RepeatedTest;

class ConcurrencyTest {

  @RepeatedTest(100)
  void shouldHandleConcurrentAccess() {
    // Test that might reveal race conditions if run multiple times
    AtomicInteger counter = new AtomicInteger(0);
    counter.incrementAndGet();
    assertThat(counter.get()).isEqualTo(1);
  }
}
```

## Best Practices

- **Use @ParameterizedTest** to reduce test duplication
- **Use descriptive display names** with `(name = "...")`
- **Test boundary values** systematically
- **Keep test logic simple** - focus on single assertion
- **Organize test data logically** - group similar scenarios
- **Use @MethodSource** for complex test data
- **Use @CsvSource** for tabular test data
- **Document expected behavior** in test names

## Common Patterns

**Testing error conditions**:
```java
@ParameterizedTest
@ValueSource(strings = {"", " ", null})
void shouldThrowExceptionForInvalidInput(String input) {
  assertThatThrownBy(() -> Parser.parse(input))
    .isInstanceOf(IllegalArgumentException.class);
}
```

**Testing multiple valid inputs**:
```java
@ParameterizedTest
@ValueSource(ints = {1, 2, 3, 5, 8, 13})
void shouldBeInFibonacciSequence(int number) {
  assertThat(FibonacciChecker.isFibonacci(number)).isTrue();
}
```

## Troubleshooting

**Parameter not matching**: Verify number and type of parameters match test method signature.

**Display name not showing**: Check parameter syntax in `name = "..."`.

**CSV parsing error**: Ensure CSV format is correct and quote strings containing commas.

## References

- [JUnit 5 Parameterized Tests](https://junit.org/junit5/docs/current/user-guide/#writing-tests-parameterized-tests)
- [@ParameterizedTest Documentation](https://junit.org/junit5/docs/current/api/org.junit.jupiter.params/org/junit/jupiter/params/ParameterizedTest.html)
- [Boundary Value Analysis](https://en.wikipedia.org/wiki/Boundary-value_analysis)
