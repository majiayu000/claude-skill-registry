---
name: unit-test-boundary-conditions
description: Edge case and boundary testing patterns for unit tests. Testing minimum/maximum values, null cases, empty collections, and numeric precision. Pure JUnit 5 unit tests. Use when ensuring code handles limits and special cases correctly.
category: testing
tags: [junit-5, boundary-testing, edge-cases, parameterized-test]
version: 1.0.1
---

# Unit Testing Boundary Conditions and Edge Cases

Test boundary conditions, edge cases, and limit values systematically. Verify code behavior at limits, with null/empty inputs, and overflow scenarios.

## When to Use This Skill

Use this skill when:
- Testing minimum and maximum values
- Testing null and empty inputs
- Testing whitespace-only strings
- Testing overflow/underflow scenarios
- Testing collections with zero/one/many items
- Verifying behavior at API boundaries
- Want comprehensive edge case coverage

## Setup: Boundary Testing

### Maven
```xml
<dependency>
  <groupId>org.junit.jupiter</groupId>
  <artifactId>junit-jupiter</artifactId>
  <scope>test</scope>
</dependency>
<dependency>
  <groupId>org.junit.jupiter</groupId>
  <artifactId>junit-jupiter-params</artifactId>
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
  testImplementation("org.junit.jupiter:junit-jupiter-params")
  testImplementation("org.assertj:assertj-core")
}
```

## Numeric Boundary Testing

### Integer Limits

```java
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;
import static org.assertj.core.api.Assertions.*;

class IntegerBoundaryTest {

  @ParameterizedTest
  @ValueSource(ints = {Integer.MIN_VALUE, Integer.MIN_VALUE + 1, 0, Integer.MAX_VALUE - 1, Integer.MAX_VALUE})
  void shouldHandleIntegerBoundaries(int value) {
    assertThat(value).isNotNull();
  }

  @Test
  void shouldHandleIntegerOverflow() {
    int maxInt = Integer.MAX_VALUE;
    int result = Math.addExact(maxInt, 1); // Will throw ArithmeticException
    
    assertThatThrownBy(() -> Math.addExact(Integer.MAX_VALUE, 1))
      .isInstanceOf(ArithmeticException.class);
  }

  @Test
  void shouldHandleIntegerUnderflow() {
    assertThatThrownBy(() -> Math.subtractExact(Integer.MIN_VALUE, 1))
      .isInstanceOf(ArithmeticException.class);
  }

  @Test
  void shouldHandleZero() {
    int result = MathUtils.divide(0, 5);
    assertThat(result).isZero();

    assertThatThrownBy(() -> MathUtils.divide(5, 0))
      .isInstanceOf(ArithmeticException.class);
  }
}
```

## String Boundary Testing

### Null, Empty, and Whitespace

```java
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;

class StringBoundaryTest {

  @ParameterizedTest
  @ValueSource(strings = {"", " ", "  ", "\t", "\n"})
  void shouldConsiderEmptyAndWhitespaceAsInvalid(String input) {
    boolean result = StringUtils.isNotBlank(input);
    assertThat(result).isFalse();
  }

  @Test
  void shouldHandleNullString() {
    String result = StringUtils.trim(null);
    assertThat(result).isNull();
  }

  @Test
  void shouldHandleSingleCharacter() {
    String result = StringUtils.capitalize("a");
    assertThat(result).isEqualTo("A");

    String result2 = StringUtils.trim("x");
    assertThat(result2).isEqualTo("x");
  }

  @Test
  void shouldHandleVeryLongString() {
    String longString = "x".repeat(1000000);
    
    assertThat(longString.length()).isEqualTo(1000000);
    assertThat(StringUtils.isNotBlank(longString)).isTrue();
  }

  @Test
  void shouldHandleSpecialCharacters() {
    String special = "!@#$%^&*()_+-={}[]|\\:;<>?,./";
    
    assertThat(StringUtils.length(special)).isEqualTo(31);
  }
}
```

## Collection Boundary Testing

### Empty, Single, and Large Collections

```java
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;

class CollectionBoundaryTest {

  @Test
  void shouldHandleEmptyList() {
    List<String> empty = List.of();
    
    assertThat(empty).isEmpty();
    assertThat(CollectionUtils.first(empty)).isNull();
    assertThat(CollectionUtils.count(empty)).isZero();
  }

  @Test
  void shouldHandleSingleElementList() {
    List<String> single = List.of("only");
    
    assertThat(single).hasSize(1);
    assertThat(CollectionUtils.first(single)).isEqualTo("only");
    assertThat(CollectionUtils.last(single)).isEqualTo("only");
  }

  @Test
  void shouldHandleLargeList() {
    List<Integer> large = new ArrayList<>();
    for (int i = 0; i < 100000; i++) {
      large.add(i);
    }

    assertThat(large).hasSize(100000);
    assertThat(CollectionUtils.first(large)).isZero();
    assertThat(CollectionUtils.last(large)).isEqualTo(99999);
  }

  @Test
  void shouldHandleNullInCollection() {
    List<String> withNull = new ArrayList<>(List.of("a", null, "c"));
    
    assertThat(withNull).contains(null);
    assertThat(CollectionUtils.filterNonNull(withNull)).hasSize(2);
  }

  @Test
  void shouldHandleDuplicatesInCollection() {
    List<Integer> duplicates = List.of(1, 1, 2, 2, 3, 3);
    
    assertThat(duplicates).hasSize(6);
    Set<Integer> unique = new HashSet<>(duplicates);
    assertThat(unique).hasSize(3);
  }
}
```

## Floating Point Boundary Testing

### Precision and Special Values

```java
class FloatingPointBoundaryTest {

  @Test
  void shouldHandleFloatingPointPrecision() {
    double result = 0.1 + 0.2;
    
    // Floating point comparison needs tolerance
    assertThat(result).isCloseTo(0.3, within(0.0001));
  }

  @Test
  void shouldHandleSpecialFloatingPointValues() {
    assertThat(Double.POSITIVE_INFINITY).isGreaterThan(Double.MAX_VALUE);
    assertThat(Double.NEGATIVE_INFINITY).isLessThan(Double.MIN_VALUE);
    assertThat(Double.NaN).isNotEqualTo(Double.NaN); // NaN != NaN
  }

  @Test
  void shouldHandleVerySmallAndLargeNumbers() {
    double tiny = Double.MIN_VALUE;
    double huge = Double.MAX_VALUE;

    assertThat(tiny).isGreaterThan(0);
    assertThat(huge).isPositive();
  }

  @Test
  void shouldHandleZeroInDivision() {
    double result = 1.0 / 0.0;
    
    assertThat(result).isEqualTo(Double.POSITIVE_INFINITY);

    double result2 = -1.0 / 0.0;
    assertThat(result2).isEqualTo(Double.NEGATIVE_INFINITY);

    double result3 = 0.0 / 0.0;
    assertThat(result3).isNaN();
  }
}
```

## Date/Time Boundary Testing

### Min/Max Dates and Edge Cases

```java
class DateTimeBoundaryTest {

  @Test
  void shouldHandleMinAndMaxDates() {
    LocalDate min = LocalDate.MIN;
    LocalDate max = LocalDate.MAX;

    assertThat(min).isBefore(max);
    assertThat(DateUtils.isValid(min)).isTrue();
    assertThat(DateUtils.isValid(max)).isTrue();
  }

  @Test
  void shouldHandleLeapYearBoundary() {
    LocalDate leapYearEnd = LocalDate.of(2024, 2, 29);
    
    assertThat(leapYearEnd).isNotNull();
    assertThat(LocalDate.of(2024, 2, 29)).isEqualTo(leapYearEnd);
  }

  @Test
  void shouldHandleInvalidDateInNonLeapYear() {
    assertThatThrownBy(() -> LocalDate.of(2023, 2, 29))
      .isInstanceOf(DateTimeException.class);
  }

  @Test
  void shouldHandleYearBoundaries() {
    LocalDate newYear = LocalDate.of(2024, 1, 1);
    LocalDate lastDay = LocalDate.of(2024, 12, 31);

    assertThat(newYear).isBefore(lastDay);
  }

  @Test
  void shouldHandleMidnightBoundary() {
    LocalTime midnight = LocalTime.MIDNIGHT;
    LocalTime almostMidnight = LocalTime.of(23, 59, 59);

    assertThat(almostMidnight).isBefore(midnight);
  }
}
```

## Array Index Boundary Testing

### First, Last, and Out of Bounds

```java
class ArrayBoundaryTest {

  @Test
  void shouldHandleFirstElementAccess() {
    int[] array = {1, 2, 3, 4, 5};
    
    assertThat(array[0]).isEqualTo(1);
  }

  @Test
  void shouldHandleLastElementAccess() {
    int[] array = {1, 2, 3, 4, 5};
    
    assertThat(array[array.length - 1]).isEqualTo(5);
  }

  @Test
  void shouldThrowOnNegativeIndex() {
    int[] array = {1, 2, 3};
    
    assertThatThrownBy(() -> {
      int value = array[-1];
    }).isInstanceOf(ArrayIndexOutOfBoundsException.class);
  }

  @Test
  void shouldThrowOnOutOfBoundsIndex() {
    int[] array = {1, 2, 3};
    
    assertThatThrownBy(() -> {
      int value = array[10];
    }).isInstanceOf(ArrayIndexOutOfBoundsException.class);
  }

  @Test
  void shouldHandleEmptyArray() {
    int[] empty = {};
    
    assertThat(empty.length).isZero();
    assertThatThrownBy(() -> {
      int value = empty[0];
    }).isInstanceOf(ArrayIndexOutOfBoundsException.class);
  }
}
```

## Concurrent and Thread Boundary Testing

### Null and Race Conditions

```java
import java.util.concurrent.*;

class ConcurrentBoundaryTest {

  @Test
  void shouldHandleNullInConcurrentMap() {
    ConcurrentHashMap<String, String> map = new ConcurrentHashMap<>();
    
    map.put("key", "value");
    assertThat(map.get("nonexistent")).isNull();
  }

  @Test
  void shouldHandleConcurrentModification() {
    List<Integer> list = new CopyOnWriteArrayList<>(List.of(1, 2, 3, 4, 5));
    
    // Should not throw ConcurrentModificationException
    for (int num : list) {
      if (num == 3) {
        list.add(6);
      }
    }

    assertThat(list).hasSize(6);
  }

  @Test
  void shouldHandleEmptyBlockingQueue() throws InterruptedException {
    BlockingQueue<String> queue = new LinkedBlockingQueue<>();
    
    assertThat(queue.poll()).isNull();
  }
}
```

## Parameterized Boundary Testing

### Multiple Boundary Cases

```java
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;

class ParameterizedBoundaryTest {

  @ParameterizedTest
  @CsvSource({
    "null,            false", // null
    "'',              false", // empty
    "'   ',           false", // whitespace
    "a,               true",  // single char
    "abc,             true"   // normal
  })
  void shouldValidateStringBoundaries(String input, boolean expected) {
    boolean result = StringValidator.isValid(input);
    assertThat(result).isEqualTo(expected);
  }

  @ParameterizedTest
  @ValueSource(ints = {Integer.MIN_VALUE, 0, 1, -1, Integer.MAX_VALUE})
  void shouldHandleNumericBoundaries(int value) {
    assertThat(value).isNotNull();
  }
}
```

## Best Practices

- **Test explicitly at boundaries** - don't rely on random testing
- **Test null and empty separately** from valid inputs
- **Use parameterized tests** for multiple boundary cases
- **Test both sides of boundaries** (just below, at, just above)
- **Verify error messages** are helpful for invalid boundaries
- **Document why** specific boundaries matter
- **Test overflow/underflow** for numeric operations

## Common Pitfalls

- Testing only "happy path" without boundary cases
- Forgetting null/empty cases
- Not testing floating point precision
- Not testing collection boundaries (empty, single, many)
- Not testing string boundaries (null, empty, whitespace)

## Troubleshooting

**Floating point comparison fails**: Use `isCloseTo(expected, within(tolerance))`.

**Collection boundaries unclear**: List cases explicitly: empty (0), single (1), many (>1).

**Date boundary confusing**: Use `LocalDate.MIN`, `LocalDate.MAX` for clear boundaries.

## References

- [Integer.MIN_VALUE/MAX_VALUE](https://docs.oracle.com/javase/8/docs/api/java/lang/Integer.html)
- [Double.MIN_VALUE/MAX_VALUE](https://docs.oracle.com/javase/8/docs/api/java/lang/Double.html)
- [AssertJ Floating Point Assertions](https://assertj.github.io/assertj-core-features-highlight.html#assertions-on-numbers)
- [Boundary Value Analysis](https://en.wikipedia.org/wiki/Boundary-value_analysis)
