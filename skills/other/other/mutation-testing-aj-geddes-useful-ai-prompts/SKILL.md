---
name: mutation-testing
description: Evaluate test suite quality by introducing code mutations and verifying tests catch them. Use for mutation testing, test quality, mutant detection, Stryker, PITest, and test effectiveness analysis.
---

# Mutation Testing

## Overview

Mutation testing assesses test suite quality by introducing small changes (mutations) to source code and verifying that tests fail. If tests don't catch a mutation, it indicates gaps in test coverage or test quality. This technique helps identify weak or ineffective tests.

## When to Use

- Evaluating test suite effectiveness
- Finding untested code paths
- Improving test quality metrics
- Validating critical business logic is well-tested
- Identifying redundant or weak tests
- Measuring real test coverage beyond line coverage
- Ensuring tests actually verify behavior

## Key Concepts

- **Mutant**: Modified version of code with small change
- **Killed**: Test fails when mutation is introduced (good)
- **Survived**: Test passes despite mutation (test gap)
- **Equivalent**: Mutation that doesn't change behavior
- **Mutation Score**: Percentage of mutants killed
- **Mutation Operators**: Types of changes (arithmetic, conditional, etc.)

## Instructions

### 1. **Stryker for JavaScript/TypeScript**

```bash
# Install Stryker
npm install --save-dev @stryker-mutator/core @stryker-mutator/jest-runner

# Initialize configuration
npx stryker init

# Run mutation testing
npx stryker run
```

```javascript
// stryker.conf.json
{
  "$schema": "./node_modules/@stryker-mutator/core/schema/stryker-schema.json",
  "packageManager": "npm",
  "reporters": ["html", "clear-text", "progress", "dashboard"],
  "testRunner": "jest",
  "jest": {
    "projectType": "custom",
    "configFile": "jest.config.js",
    "enableFindRelatedTests": true
  },
  "coverageAnalysis": "perTest",
  "mutate": [
    "src/**/*.ts",
    "!src/**/*.spec.ts",
    "!src/**/*.test.ts"
  ],
  "thresholds": {
    "high": 80,
    "low": 60,
    "break": 50
  }
}

// Example source code
// src/calculator.ts
export class Calculator {
  add(a: number, b: number): number {
    return a + b;
  }

  subtract(a: number, b: number): number {
    return a - b;
  }

  multiply(a: number, b: number): number {
    return a * b;
  }

  divide(a: number, b: number): number {
    if (b === 0) {
      throw new Error('Division by zero');
    }
    return a / b;
  }

  isPositive(n: number): boolean {
    return n > 0;
  }
}

// ❌ Weak tests - mutations will survive
describe('Calculator - Weak Tests', () => {
  const calc = new Calculator();

  test('add returns a number', () => {
    const result = calc.add(2, 3);
    expect(typeof result).toBe('number');
    // This test won't catch mutations like: return a - b; or return a * b;
  });

  test('divide with non-zero divisor', () => {
    expect(() => calc.divide(10, 2)).not.toThrow();
    // Doesn't verify the actual result!
  });
});

// ✅ Strong tests - will kill mutations
describe('Calculator - Strong Tests', () => {
  const calc = new Calculator();

  describe('add', () => {
    test('adds two positive numbers', () => {
      expect(calc.add(2, 3)).toBe(5);
    });

    test('adds negative numbers', () => {
      expect(calc.add(-2, -3)).toBe(-5);
    });

    test('adds zero', () => {
      expect(calc.add(5, 0)).toBe(5);
      expect(calc.add(0, 5)).toBe(5);
    });
  });

  describe('subtract', () => {
    test('subtracts numbers correctly', () => {
      expect(calc.subtract(5, 3)).toBe(2);
      expect(calc.subtract(3, 5)).toBe(-2);
    });
  });

  describe('multiply', () => {
    test('multiplies numbers', () => {
      expect(calc.multiply(3, 4)).toBe(12);
      expect(calc.multiply(-2, 3)).toBe(-6);
    });

    test('multiply by zero', () => {
      expect(calc.multiply(5, 0)).toBe(0);
    });
  });

  describe('divide', () => {
    test('divides numbers correctly', () => {
      expect(calc.divide(10, 2)).toBe(5);
      expect(calc.divide(7, 2)).toBe(3.5);
    });

    test('throws error on division by zero', () => {
      expect(() => calc.divide(10, 0)).toThrow('Division by zero');
    });
  });

  describe('isPositive', () => {
    test('returns true for positive numbers', () => {
      expect(calc.isPositive(1)).toBe(true);
      expect(calc.isPositive(100)).toBe(true);
    });

    test('returns false for zero and negative', () => {
      expect(calc.isPositive(0)).toBe(false);
      expect(calc.isPositive(-1)).toBe(false);
    });
  });
});
```

### 2. **PITest for Java**

```xml
<!-- pom.xml -->
<plugin>
    <groupId>org.pitest</groupId>
    <artifactId>pitest-maven</artifactId>
    <version>1.14.2</version>
    <configuration>
        <targetClasses>
            <param>com.example.service.*</param>
        </targetClasses>
        <targetTests>
            <param>com.example.service.*Test</param>
        </targetTests>
        <mutators>
            <mutator>DEFAULTS</mutator>
        </mutators>
        <outputFormats>
            <outputFormat>HTML</outputFormat>
            <outputFormat>XML</outputFormat>
        </outputFormats>
        <timestampedReports>false</timestampedReports>
        <mutationThreshold>80</mutationThreshold>
        <coverageThreshold>90</coverageThreshold>
    </configuration>
</plugin>
```

```bash
# Run mutation testing
mvn org.pitest:pitest-maven:mutationCoverage
```

```java
// src/main/java/OrderValidator.java
public class OrderValidator {

    public boolean isValidOrder(Order order) {
        if (order == null) {
            return false;
        }

        if (order.getItems().isEmpty()) {
            return false;
        }

        if (order.getTotal() <= 0) {
            return false;
        }

        return true;
    }

    public double calculateDiscount(double total, String customerTier) {
        if (customerTier.equals("GOLD")) {
            return total * 0.2;
        } else if (customerTier.equals("SILVER")) {
            return total * 0.1;
        }
        return 0;
    }

    public int categorizeOrderSize(int itemCount) {
        if (itemCount <= 5) {
            return 1; // Small
        } else if (itemCount <= 20) {
            return 2; // Medium
        } else {
            return 3; // Large
        }
    }
}

// ❌ Weak tests that allow mutations to survive
@Test
public void testOrderValidation_Weak() {
    OrderValidator validator = new OrderValidator();

    Order order = new Order();
    order.addItem(new Item("Product", 10.0));
    order.setTotal(10.0);

    // Only tests one scenario
    assertTrue(validator.isValidOrder(order));
}

// ✅ Strong tests that kill mutations
public class OrderValidatorTest {

    private OrderValidator validator;

    @Before
    public void setUp() {
        validator = new OrderValidator();
    }

    @Test
    public void isValidOrder_withNullOrder_returnsFalse() {
        assertFalse(validator.isValidOrder(null));
    }

    @Test
    public void isValidOrder_withEmptyItems_returnsFalse() {
        Order order = new Order();
        order.setTotal(10.0);
        assertFalse(validator.isValidOrder(order));
    }

    @Test
    public void isValidOrder_withZeroTotal_returnsFalse() {
        Order order = new Order();
        order.addItem(new Item("Product", 0));
        order.setTotal(0);
        assertFalse(validator.isValidOrder(order));
    }

    @Test
    public void isValidOrder_withNegativeTotal_returnsFalse() {
        Order order = new Order();
        order.addItem(new Item("Product", -10.0));
        order.setTotal(-10.0);
        assertFalse(validator.isValidOrder(order));
    }

    @Test
    public void isValidOrder_withValidOrder_returnsTrue() {
        Order order = new Order();
        order.addItem(new Item("Product", 10.0));
        order.setTotal(10.0);
        assertTrue(validator.isValidOrder(order));
    }

    @Test
    public void calculateDiscount_goldTier_returns20Percent() {
        assertEquals(20.0, validator.calculateDiscount(100.0, "GOLD"), 0.01);
    }

    @Test
    public void calculateDiscount_silverTier_returns10Percent() {
        assertEquals(10.0, validator.calculateDiscount(100.0, "SILVER"), 0.01);
    }

    @Test
    public void calculateDiscount_regularTier_returnsZero() {
        assertEquals(0.0, validator.calculateDiscount(100.0, "BRONZE"), 0.01);
    }

    @Test
    public void categorizeOrderSize_smallOrder() {
        assertEquals(1, validator.categorizeOrderSize(3));
        assertEquals(1, validator.categorizeOrderSize(5));
    }

    @Test
    public void categorizeOrderSize_mediumOrder() {
        assertEquals(2, validator.categorizeOrderSize(6));
        assertEquals(2, validator.categorizeOrderSize(20));
    }

    @Test
    public void categorizeOrderSize_largeOrder() {
        assertEquals(3, validator.categorizeOrderSize(21));
        assertEquals(3, validator.categorizeOrderSize(100));
    }

    // Test boundary conditions
    @Test
    public void categorizeOrderSize_boundaries() {
        assertEquals(1, validator.categorizeOrderSize(5));
        assertEquals(2, validator.categorizeOrderSize(6));
        assertEquals(2, validator.categorizeOrderSize(20));
        assertEquals(3, validator.categorizeOrderSize(21));
    }
}
```

### 3. **mutmut for Python**

```bash
# Install mutmut
pip install mutmut

# Run mutation testing
mutmut run

# Show results
mutmut results

# Show specific mutant
mutmut show 1

# Apply mutation to see what changed
mutmut apply 1
```

```python
# src/string_utils.py
def is_palindrome(s: str) -> bool:
    """Check if string is palindrome."""
    clean = ''.join(c.lower() for c in s if c.isalnum())
    return clean == clean[::-1]

def count_words(text: str) -> int:
    """Count words in text."""
    if not text:
        return 0
    return len(text.split())

def truncate(text: str, max_length: int) -> str:
    """Truncate text to max length."""
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."

# ❌ Weak tests
def test_palindrome_basic():
    """Weak: Only tests one case."""
    assert is_palindrome("racecar") == True

# ✅ Strong tests that will catch mutations
def test_is_palindrome_simple():
    assert is_palindrome("racecar") == True
    assert is_palindrome("hello") == False

def test_is_palindrome_with_spaces():
    assert is_palindrome("race car") == True
    assert is_palindrome("not a palindrome") == False

def test_is_palindrome_with_punctuation():
    assert is_palindrome("A man, a plan, a canal: Panama") == True

def test_is_palindrome_case_insensitive():
    assert is_palindrome("RaceCar") == True
    assert is_palindrome("Racecar") == True

def test_is_palindrome_empty():
    assert is_palindrome("") == True

def test_is_palindrome_single_char():
    assert is_palindrome("a") == True

def test_count_words_basic():
    assert count_words("hello world") == 2
    assert count_words("one") == 1

def test_count_words_multiple_spaces():
    assert count_words("hello  world") == 2
    assert count_words("  leading spaces") == 2

def test_count_words_empty():
    assert count_words("") == 0
    assert count_words("   ") == 0

def test_truncate_short_text():
    assert truncate("hello", 10) == "hello"

def test_truncate_exact_length():
    assert truncate("hello", 5) == "hello"

def test_truncate_long_text():
    result = truncate("hello world", 5)
    assert result == "hello..."
    assert len(result) == 8  # 5 + "..."

def test_truncate_zero_length():
    assert truncate("hello", 0) == "..."
```

### 4. **Mutation Testing Reports**

```bash
# Stryker HTML report shows:
# - Mutation score: 85.5%
# - Mutants killed: 94
# - Mutants survived: 16
# - Mutants timeout: 0
# - Mutants no coverage: 10

# Example mutations:
# ❌ Survived: Changed > to >= in isPositive
#    No test checks boundary condition
#
# ✅ Killed: Changed + to - in add method
#    Test expects specific result
#
# ❌ Survived: Removed if condition check
#    Missing test for that edge case
```

## Common Mutation Operators

### Arithmetic Mutations
- `+` → `-`, `*`, `/`
- `-` → `+`, `*`, `/`
- `*` → `+`, `-`, `/`
- `/` → `+`, `-`, `*`

### Conditional Mutations
- `>` → `>=`, `<`, `==`
- `<` → `<=`, `>`, `==`
- `==` → `!=`
- `&&` → `||`
- `||` → `&&`

### Return Value Mutations
- `return true` → `return false`
- `return x` → `return x + 1`
- `return` → Remove return statement

### Statement Mutations
- Remove method calls
- Remove conditional blocks
- Remove increments/decrements

## Improving Mutation Score

```typescript
// Low mutation score example
function processUser(user: User): boolean {
  if (user.age >= 18) {
    user.isAdult = true;
    sendWelcomeEmail(user);
    return true;
  }
  return false;
}

// ❌ Weak test - Mutation: >= to > survives
test('processes adult user', () => {
  const user = { age: 25 };
  expect(processUser(user)).toBe(true);
});

// ✅ Strong test - Catches >= to > mutation
test('processes user who is exactly 18', () => {
  const user = { age: 18 };
  expect(processUser(user)).toBe(true);
  expect(user.isAdult).toBe(true);
});

test('rejects user who is 17', () => {
  const user = { age: 17 };
  expect(processUser(user)).toBe(false);
  expect(user.isAdult).toBeUndefined();
});
```

## Best Practices

### ✅ DO
- Target critical business logic for mutation testing
- Aim for 80%+ mutation score on important code
- Review survived mutants to improve tests
- Mark equivalent mutants to exclude them
- Use mutation testing in CI for critical modules
- Test boundary conditions thoroughly
- Verify actual behavior, not just code execution

### ❌ DON'T
- Expect 100% mutation score everywhere
- Run mutation testing on all code (too slow)
- Ignore equivalent mutants
- Test getters/setters with mutations
- Run mutations on generated code
- Skip mutation testing on complex logic
- Focus only on line coverage

## Tools

- **JavaScript/TypeScript**: Stryker Mutator
- **Java**: PITest, Major
- **Python**: mutmut, Cosmic Ray
- **C#**: Stryker.NET
- **Ruby**: Mutant
- **PHP**: Infection

## Integration with CI

```yaml
# .github/workflows/mutation-testing.yml
name: Mutation Testing

on:
  pull_request:
    paths:
      - 'src/**'

jobs:
  mutation:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
      - run: npm ci
      - run: npx stryker run
      - name: Check mutation score
        run: |
          SCORE=$(jq '.mutationScore' stryker-reports/mutation-score.json)
          if (( $(echo "$SCORE < 80" | bc -l) )); then
            echo "Mutation score $SCORE% is below threshold"
            exit 1
          fi
```

## Examples

See also: test-data-generation, continuous-testing, code-metrics-analysis for comprehensive test quality measurement.
