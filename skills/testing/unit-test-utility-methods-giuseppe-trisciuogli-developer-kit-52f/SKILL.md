---
name: unit-test-utility-methods
description: Unit tests for utility/helper classes and static methods. Test pure functions and helper logic. Use when validating utility code correctness.
category: testing
tags: [junit-5, unit-testing, utility, static-methods, pure-functions]
version: 1.0.1
---

# Unit Testing Utility Classes and Static Methods

Test static utility methods using JUnit 5. Focus on pure functions without side effects, edge cases, and boundary conditions.

## When to Use This Skill

Use this skill when:
- Testing utility classes with static helper methods
- Testing pure functions with no state or side effects
- Testing string manipulation and formatting utilities
- Testing calculation and conversion utilities
- Testing collections and array utilities
- Want simple, fast tests without mocking complexity
- Testing data transformation and validation helpers

## Basic Pattern: Static Utility Testing

### Simple String Utility

```java
import org.junit.jupiter.api.Test;
import static org.assertj.core.api.Assertions.*;

class StringUtilsTest {

  @Test
  void shouldCapitalizeFirstLetter() {
    String result = StringUtils.capitalize("hello");
    assertThat(result).isEqualTo("Hello");
  }

  @Test
  void shouldHandleEmptyString() {
    String result = StringUtils.capitalize("");
    assertThat(result).isEmpty();
  }

  @Test
  void shouldHandleNullInput() {
    String result = StringUtils.capitalize(null);
    assertThat(result).isNull();
  }

  @Test
  void shouldHandleSingleCharacter() {
    String result = StringUtils.capitalize("a");
    assertThat(result).isEqualTo("A");
  }

  @Test
  void shouldNotChangePascalCase() {
    String result = StringUtils.capitalize("Hello");
    assertThat(result).isEqualTo("Hello");
  }
}
```

## Testing Null Handling

### Null-Safe Utility Methods

```java
class NullSafeUtilsTest {

  @Test
  void shouldReturnDefaultValueWhenNull() {
    Object result = NullSafeUtils.getOrDefault(null, "default");
    assertThat(result).isEqualTo("default");
  }

  @Test
  void shouldReturnValueWhenNotNull() {
    Object result = NullSafeUtils.getOrDefault("value", "default");
    assertThat(result).isEqualTo("value");
  }

  @Test
  void shouldReturnFalseWhenStringIsNull() {
    boolean result = NullSafeUtils.isNotBlank(null);
    assertThat(result).isFalse();
  }

  @Test
  void shouldReturnTrueWhenStringHasContent() {
    boolean result = NullSafeUtils.isNotBlank("   text   ");
    assertThat(result).isTrue();
  }
}
```

## Testing Calculations and Conversions

### Math Utilities

```java
class MathUtilsTest {

  @Test
  void shouldCalculatePercentage() {
    double result = MathUtils.percentage(25, 100);
    assertThat(result).isEqualTo(25.0);
  }

  @Test
  void shouldHandleZeroDivisor() {
    double result = MathUtils.percentage(50, 0);
    assertThat(result).isZero();
  }

  @Test
  void shouldRoundToTwoDecimalPlaces() {
    double result = MathUtils.round(3.14159, 2);
    assertThat(result).isEqualTo(3.14);
  }

  @Test
  void shouldHandleNegativeNumbers() {
    int result = MathUtils.absoluteValue(-42);
    assertThat(result).isEqualTo(42);
  }
}
```

## Testing Collection Utilities

### List/Set/Map Operations

```java
class CollectionUtilsTest {

  @Test
  void shouldFilterList() {
    List<Integer> numbers = List.of(1, 2, 3, 4, 5);
    List<Integer> evenNumbers = CollectionUtils.filter(numbers, n -> n % 2 == 0);
    assertThat(evenNumbers).containsExactly(2, 4);
  }

  @Test
  void shouldReturnEmptyListWhenNoMatches() {
    List<Integer> numbers = List.of(1, 3, 5);
    List<Integer> evenNumbers = CollectionUtils.filter(numbers, n -> n % 2 == 0);
    assertThat(evenNumbers).isEmpty();
  }

  @Test
  void shouldHandleNullList() {
    List<Integer> result = CollectionUtils.filter(null, n -> true);
    assertThat(result).isEmpty();
  }

  @Test
  void shouldJoinStringsWithSeparator() {
    String result = CollectionUtils.join(List.of("a", "b", "c"), "-");
    assertThat(result).isEqualTo("a-b-c");
  }

  @Test
  void shouldHandleEmptyList() {
    String result = CollectionUtils.join(List.of(), "-");
    assertThat(result).isEmpty();
  }

  @Test
  void shouldDeduplicateList() {
    List<String> input = List.of("apple", "banana", "apple", "cherry", "banana");
    Set<String> unique = CollectionUtils.deduplicate(input);
    assertThat(unique).containsExactlyInAnyOrder("apple", "banana", "cherry");
  }
}
```

## Testing String Transformations

### Format and Parse Utilities

```java
class FormatUtilsTest {

  @Test
  void shouldFormatCurrencyWithSymbol() {
    String result = FormatUtils.formatCurrency(1234.56);
    assertThat(result).isEqualTo("$1,234.56");
  }

  @Test
  void shouldHandleNegativeCurrency() {
    String result = FormatUtils.formatCurrency(-100.00);
    assertThat(result).isEqualTo("-$100.00");
  }

  @Test
  void shouldParsePhoneNumber() {
    String result = FormatUtils.parsePhoneNumber("5551234567");
    assertThat(result).isEqualTo("(555) 123-4567");
  }

  @Test
  void shouldFormatDate() {
    LocalDate date = LocalDate.of(2024, 1, 15);
    String result = FormatUtils.formatDate(date, "yyyy-MM-dd");
    assertThat(result).isEqualTo("2024-01-15");
  }

  @Test
  void shouldSluggifyString() {
    String result = FormatUtils.sluggify("Hello World! 123");
    assertThat(result).isEqualTo("hello-world-123");
  }
}
```

## Testing Data Validation

### Validator Utilities

```java
class ValidatorUtilsTest {

  @Test
  void shouldValidateEmailFormat() {
    boolean valid = ValidatorUtils.isValidEmail("user@example.com");
    assertThat(valid).isTrue();

    boolean invalid = ValidatorUtils.isValidEmail("invalid-email");
    assertThat(invalid).isFalse();
  }

  @Test
  void shouldValidatePhoneNumber() {
    boolean valid = ValidatorUtils.isValidPhone("555-123-4567");
    assertThat(valid).isTrue();

    boolean invalid = ValidatorUtils.isValidPhone("12345");
    assertThat(invalid).isFalse();
  }

  @Test
  void shouldValidateUrlFormat() {
    boolean valid = ValidatorUtils.isValidUrl("https://example.com");
    assertThat(valid).isTrue();

    boolean invalid = ValidatorUtils.isValidUrl("not a url");
    assertThat(invalid).isFalse();
  }

  @Test
  void shouldValidateCreditCardNumber() {
    boolean valid = ValidatorUtils.isValidCreditCard("4532015112830366");
    assertThat(valid).isTrue();

    boolean invalid = ValidatorUtils.isValidCreditCard("1234567890123456");
    assertThat(invalid).isFalse();
  }
}
```

## Testing Parameterized Scenarios

### Multiple Test Cases with @ParameterizedTest

```java
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;
import org.junit.jupiter.params.provider.CsvSource;

class StringUtilsParametrizedTest {

  @ParameterizedTest
  @ValueSource(strings = {"", " ", "null", "undefined"})
  void shouldConsiderFalsyValuesAsEmpty(String input) {
    boolean result = StringUtils.isEmpty(input);
    assertThat(result).isTrue();
  }

  @ParameterizedTest
  @CsvSource({
    "hello,HELLO",
    "world,WORLD",
    "javaScript,JAVASCRIPT",
    "123ABC,123ABC"
  })
  void shouldConvertToUpperCase(String input, String expected) {
    String result = StringUtils.toUpperCase(input);
    assertThat(result).isEqualTo(expected);
  }
}
```

## Testing with Mockito for External Dependencies

### Utility with Dependency (Rare Case)

```java
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class DateUtilsTest {

  @Mock
  private Clock clock;

  @Test
  void shouldGetCurrentDateFromClock() {
    Instant fixedTime = Instant.parse("2024-01-15T10:30:00Z");
    when(clock.instant()).thenReturn(fixedTime);

    LocalDate result = DateUtils.today(clock);
    
    assertThat(result).isEqualTo(LocalDate.of(2024, 1, 15));
  }
}
```

## Edge Cases and Boundary Testing

```java
class MathUtilsEdgeCaseTest {

  @Test
  void shouldHandleMaxIntegerValue() {
    int result = MathUtils.increment(Integer.MAX_VALUE);
    assertThat(result).isEqualTo(Integer.MAX_VALUE);
  }

  @Test
  void shouldHandleMinIntegerValue() {
    int result = MathUtils.decrement(Integer.MIN_VALUE);
    assertThat(result).isEqualTo(Integer.MIN_VALUE);
  }

  @Test
  void shouldHandleVeryLargeNumbers() {
    BigDecimal result = MathUtils.add(
      new BigDecimal("999999999999.99"),
      new BigDecimal("0.01")
    );
    assertThat(result).isEqualTo(new BigDecimal("1000000000000.00"));
  }

  @Test
  void shouldHandleFloatingPointPrecision() {
    double result = MathUtils.multiply(0.1, 0.2);
    assertThat(result).isCloseTo(0.02, within(0.0001));
  }
}
```

## Best Practices

- **Test pure functions exclusively** - no side effects or state
- **Cover happy path and edge cases** - null, empty, extreme values
- **Use descriptive test names** - clearly state what's being tested
- **Keep tests simple and short** - utility tests should be quick to understand
- **Use @ParameterizedTest** for testing multiple similar scenarios
- **Avoid mocking when not needed** - only mock external dependencies
- **Test boundary conditions** - min/max values, empty collections, null inputs

## Common Pitfalls

- Testing framework behavior instead of utility logic
- Over-mocking when pure functions need no mocks
- Not testing null/empty edge cases
- Not testing negative numbers and extreme values
- Test methods too large - split complex scenarios

## Troubleshooting

**Floating point precision issues**: Use `isCloseTo()` with delta instead of exact equality.

**Null handling inconsistency**: Decide whether utility returns null or throws exception, then test consistently.

**Complex utility logic belongs elsewhere**: Consider refactoring into testable units.

## References

- [JUnit 5 Parameterized Tests](https://junit.org/junit5/docs/current/user-guide/#writing-tests-parameterized-tests)
- [AssertJ Assertions](https://assertj.github.io/assertj-core-features-highlight.html)
- [Testing Edge Cases and Boundaries](https://www.baeldung.com/testing-properties-methods-using-mockito)
