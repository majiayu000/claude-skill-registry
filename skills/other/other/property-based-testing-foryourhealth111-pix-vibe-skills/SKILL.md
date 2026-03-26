---
created: 2025-12-16
modified: 2025-12-16
reviewed: 2025-12-16
name: property-based-testing
description: |
  Property-based testing with fast-check (TypeScript/JavaScript) and Hypothesis (Python).
  Generate test cases automatically, find edge cases, and test mathematical properties.
  Use when user mentions property-based testing, fast-check, Hypothesis, generating
  test data, QuickCheck-style testing, or finding edge cases automatically.
allowed-tools: Bash, Read, Edit, Write, Grep, Glob, TodoWrite
---

# Property-Based Testing

Expert knowledge for property-based testing - automatically generating test cases to verify code properties rather than testing specific examples.

## Core Expertise

**Property-Based Testing Concept**
- **Traditional testing**: Test specific examples
- **Property-based testing**: Test properties that should hold for all inputs
- **Generators**: Automatically create diverse test inputs
- **Shrinking**: Minimize failing cases to simplest example
- **Coverage**: Explore edge cases humans might miss

**When to Use Property-Based Testing**
- Mathematical operations (commutative, associative properties)
- Encoders/decoders (roundtrip properties)
- Parsers and serializers
- Data transformations
- API contracts
- Invariants and constraints

## TypeScript/JavaScript (fast-check)

### Installation

```bash
# Using Bun
bun add -d fast-check

# Using npm
npm install -D fast-check
```

### Basic Example

```typescript
import { test } from 'vitest'
import * as fc from 'fast-check'

// Traditional example-based test
test('reverse twice returns original', () => {
  expect(reverse(reverse([1, 2, 3]))).toEqual([1, 2, 3])
})

// Property-based test
test('reverse twice returns original - property based', () => {
  fc.assert(
    fc.property(
      fc.array(fc.integer()), // Generate random arrays of integers
      (arr) => {
        expect(reverse(reverse(arr))).toEqual(arr)
      }
    )
  )
})
// fast-check automatically generates 100s of test cases!
```

### Built-in Generators

```typescript
import * as fc from 'fast-check'

// Numbers
fc.integer()                          // Any integer
fc.integer({ min: 0, max: 100 })      // Range
fc.nat()                              // Natural numbers (≥ 0)
fc.float()                            // Floating-point
fc.double()                           // Double precision

// Strings
fc.string()                           // Any string
fc.string({ minLength: 1, maxLength: 10 })
fc.hexaString()                       // Hex strings
fc.asciiString()                      // ASCII only
fc.unicodeString()                    // Unicode
fc.emailAddress()                     // Email format

// Arrays and Objects
fc.array(fc.integer())                // Array of integers
fc.array(fc.string(), { minLength: 1, maxLength: 5 })
fc.set(fc.integer())                  // Unique values
fc.record({                           // Objects
  name: fc.string(),
  age: fc.nat(),
})

// Booleans and Constants
fc.boolean()
fc.constant('value')
fc.constantFrom('a', 'b', 'c')        // Pick from options

// Dates
fc.date()
fc.date({ min: new Date('2020-01-01') })

// Complex Types
fc.tuple(fc.string(), fc.integer())   // Fixed-size tuple
fc.oneof(fc.string(), fc.integer())   // Union type
fc.option(fc.string())                // string | null
```

### Custom Generators

```typescript
// Generate user objects
const userArbitrary = fc.record({
  id: fc.nat(),
  name: fc.string({ minLength: 1, maxLength: 50 }),
  email: fc.emailAddress(),
  age: fc.integer({ min: 18, max: 120 }),
  roles: fc.array(fc.constantFrom('admin', 'user', 'guest'), {
    minLength: 1,
    maxLength: 3,
  }),
})

test('user validation properties', () => {
  fc.assert(
    fc.property(userArbitrary, (user) => {
      const validated = validateUser(user)
      expect(validated.age).toBeGreaterThanOrEqual(18)
      expect(validated.name.length).toBeGreaterThan(0)
      expect(validated.roles.length).toBeGreaterThan(0)
    })
  )
})

// Generate using map
const positiveNumberArbitrary = fc.nat().map((n) => n + 1)

// Generate using chain (dependent values)
const emailAndDomainArbitrary = fc.string().chain((domain) =>
  fc.record({
    email: fc.constant(`user@${domain}.com`),
    domain: fc.constant(domain),
  })
)
```

### Common Properties to Test

#### Roundtrip Property (Encode/Decode)

```typescript
test('JSON serialization roundtrip', () => {
  fc.assert(
    fc.property(
      fc.record({
        name: fc.string(),
        age: fc.nat(),
        tags: fc.array(fc.string()),
      }),
      (obj) => {
        const serialized = JSON.stringify(obj)
        const deserialized = JSON.parse(serialized)
        expect(deserialized).toEqual(obj)
      }
    )
  )
})
```

#### Idempotence (f(f(x)) = f(x))

```typescript
test('sort is idempotent', () => {
  fc.assert(
    fc.property(fc.array(fc.integer()), (arr) => {
      const sorted = sort(arr)
      const doubleSorted = sort(sorted)
      expect(doubleSorted).toEqual(sorted)
    })
  )
})
```

#### Commutativity (f(a, b) = f(b, a))

```typescript
test('addition is commutative', () => {
  fc.assert(
    fc.property(fc.integer(), fc.integer(), (a, b) => {
      expect(add(a, b)).toBe(add(b, a))
    })
  )
})
```

#### Associativity ((a + b) + c = a + (b + c))

```typescript
test('addition is associative', () => {
  fc.assert(
    fc.property(fc.integer(), fc.integer(), fc.integer(), (a, b, c) => {
      expect(add(add(a, b), c)).toBe(add(a, add(b, c)))
    })
  )
})
```

#### Identity (f(x, identity) = x)

```typescript
test('multiplication identity', () => {
  fc.assert(
    fc.property(fc.integer(), (n) => {
      expect(multiply(n, 1)).toBe(n)
    })
  )
})
```

#### Inverse (f(g(x)) = x)

```typescript
test('encryption/decryption inverse', () => {
  fc.assert(
    fc.property(fc.string(), fc.string(), (plaintext, key) => {
      const encrypted = encrypt(plaintext, key)
      const decrypted = decrypt(encrypted, key)
      expect(decrypted).toBe(plaintext)
    })
  )
})
```

### Shrinking (Simplifying Failing Cases)

```typescript
// When a property fails, fast-check automatically shrinks
// the input to the minimal failing case

test('finds minimal failing case', () => {
  fc.assert(
    fc.property(fc.array(fc.integer()), (arr) => {
      // This will fail for arrays containing 42
      expect(arr).not.toContain(42)
    })
  )
})

// Output:
// Property failed after 1 tests
// Shrunk 5 time(s)
// Counterexample: [[42]]  ← Minimal failing case!
```

### Configuration

```typescript
test('configured property test', () => {
  fc.assert(
    fc.property(fc.array(fc.integer()), (arr) => {
      expect(sort(arr)).toBeSorted()
    }),
    {
      numRuns: 1000,      // Run 1000 tests (default: 100)
      seed: 42,           // Reproducible tests
      endOnFailure: true, // Stop after first failure
      verbose: true,      // Show all generated values
    }
  )
})
```

### Preconditions (Filtering)

```typescript
test('division properties for non-zero divisors', () => {
  fc.assert(
    fc.property(fc.integer(), fc.integer(), (a, b) => {
      fc.pre(b !== 0) // Skip cases where b is 0

      const result = divide(a, b)
      expect(multiply(result, b)).toBeCloseTo(a)
    })
  )
})
```

## Python (Hypothesis)

### Installation

```bash
# Using uv
uv add --dev hypothesis

# Using pip
pip install hypothesis
```

### Basic Example

```python
from hypothesis import given, strategies as st
import pytest

# Traditional example-based test
def test_reverse_twice_example():
    assert reverse(reverse([1, 2, 3])) == [1, 2, 3]

# Property-based test
@given(st.lists(st.integers()))
def test_reverse_twice_property(arr):
    assert reverse(reverse(arr)) == arr
    # Hypothesis automatically generates 100s of test cases!
```

### Built-in Strategies

```python
from hypothesis import strategies as st

# Numbers
st.integers()                          # Any integer
st.integers(min_value=0, max_value=100)
st.floats()                            # Floating-point
st.floats(min_value=0.0, max_value=1.0, allow_nan=False)
st.decimals()                          # Decimal precision

# Strings
st.text()                              # Any string
st.text(min_size=1, max_size=10)
st.text(alphabet='abc')                # Limited alphabet
st.binary()                            # Bytes

# Collections
st.lists(st.integers())                # List of integers
st.lists(st.text(), min_size=1, max_size=5)
st.sets(st.integers())                 # Unique values
st.dictionaries(keys=st.text(), values=st.integers())

# Booleans and Constants
st.booleans()
st.just('value')                       # Constant
st.sampled_from(['a', 'b', 'c'])      # Pick from options

# Dates and Times
st.dates()
st.datetimes()
st.times()
st.timedeltas()

# Complex Types
st.tuples(st.text(), st.integers())   # Fixed-size tuple
st.one_of(st.text(), st.integers())   # Union type
```

### Custom Strategies

```python
from hypothesis import strategies as st
from dataclasses import dataclass

@dataclass
class User:
    id: int
    name: str
    email: str
    age: int

# Strategy for generating users
users = st.builds(
    User,
    id=st.integers(min_value=1),
    name=st.text(min_size=1, max_size=50),
    email=st.emails(),
    age=st.integers(min_value=18, max_value=120),
)

@given(users)
def test_user_validation(user):
    validated = validate_user(user)
    assert validated.age >= 18
    assert len(validated.name) > 0
```

```python
# Using map
positive_numbers = st.integers(min_value=0).map(lambda n: n + 1)

# Using flatmap (dependent values)
@st.composite
def email_and_domain(draw):
    domain = draw(st.text(min_size=1))
    return {
        'email': f'user@{domain}.com',
        'domain': domain,
    }
```

### Common Properties to Test

#### Roundtrip Property

```python
import json
from hypothesis import given, strategies as st

@given(st.dictionaries(
    keys=st.text(),
    values=st.one_of(st.integers(), st.text(), st.booleans())
))
def test_json_roundtrip(obj):
    serialized = json.dumps(obj)
    deserialized = json.loads(serialized)
    assert deserialized == obj
```

#### Idempotence

```python
@given(st.lists(st.integers()))
def test_sort_idempotent(arr):
    sorted_once = sorted(arr)
    sorted_twice = sorted(sorted_once)
    assert sorted_once == sorted_twice
```

#### Commutativity

```python
@given(st.integers(), st.integers())
def test_addition_commutative(a, b):
    assert add(a, b) == add(b, a)
```

#### Associativity

```python
@given(st.integers(), st.integers(), st.integers())
def test_addition_associative(a, b, c):
    assert add(add(a, b), c) == add(a, add(b, c))
```

#### Identity

```python
@given(st.integers())
def test_multiplication_identity(n):
    assert multiply(n, 1) == n
```

#### Inverse

```python
@given(st.text(), st.text(min_size=1))
def test_encryption_inverse(plaintext, key):
    encrypted = encrypt(plaintext, key)
    decrypted = decrypt(encrypted, key)
    assert decrypted == plaintext
```

### Shrinking (Simplifying Failing Cases)

```python
from hypothesis import given, strategies as st

@given(st.lists(st.integers()))
def test_finds_minimal_failing_case(arr):
    # This will fail for arrays containing 42
    assert 42 not in arr

# Output:
# Falsifying example: test_finds_minimal_failing_case(
#     arr=[42]  ← Minimal failing case!
# )
```

### Configuration and Settings

```python
from hypothesis import given, settings, strategies as st

@settings(max_examples=1000, deadline=None)
@given(st.lists(st.integers()))
def test_with_custom_settings(arr):
    assert sort(arr) == sorted(arr)

# Global settings
from hypothesis import settings, Verbosity

settings.register_profile("ci", max_examples=1000, verbosity=Verbosity.verbose)
settings.register_profile("dev", max_examples=100)
settings.load_profile("dev")
```

### Assumptions (Preconditions)

```python
from hypothesis import given, assume, strategies as st

@given(st.integers(), st.integers())
def test_division_properties(a, b):
    assume(b != 0)  # Skip cases where b is 0

    result = divide(a, b)
    assert abs(multiply(result, b) - a) < 0.0001
```

### Stateful Testing

```python
from hypothesis.stateful import RuleBasedStateMachine, rule, invariant
from hypothesis import strategies as st

class ShoppingCartMachine(RuleBasedStateMachine):
    def __init__(self):
        super().__init__()
        self.cart = ShoppingCart()
        self.items = []

    @rule(item=st.text(min_size=1), price=st.floats(min_value=0.01, max_value=1000))
    def add_item(self, item, price):
        self.cart.add(item, price)
        self.items.append((item, price))

    @rule()
    def clear_cart(self):
        self.cart.clear()
        self.items = []

    @invariant()
    def total_matches_items(self):
        expected_total = sum(price for _, price in self.items)
        assert abs(self.cart.total() - expected_total) < 0.01

# Run stateful test
TestCart = ShoppingCartMachine.TestCase
```

## Real-World Examples

### TypeScript: URL Parser

```typescript
import * as fc from 'fast-check'

test('URL parsing roundtrip', () => {
  fc.assert(
    fc.property(
      fc.webUrl(), // Built-in URL generator
      (url) => {
        const parsed = parseURL(url)
        const reconstructed = buildURL(parsed)
        expect(normalizeURL(reconstructed)).toBe(normalizeURL(url))
      }
    )
  )
})
```

### Python: Data Validation

```python
from hypothesis import given, strategies as st
from pydantic import BaseModel, ValidationError

class Product(BaseModel):
    name: str
    price: float
    quantity: int

@given(st.builds(
    Product,
    name=st.text(min_size=1),
    price=st.floats(min_value=0.01, max_value=10000),
    quantity=st.integers(min_value=0, max_value=1000),
))
def test_product_validation_accepts_valid_data(product):
    # Should not raise
    validated = Product(**product.dict())
    assert validated.price > 0
    assert validated.quantity >= 0
```

### TypeScript: List Operations

```typescript
test('filter and map compose correctly', () => {
  fc.assert(
    fc.property(
      fc.array(fc.integer()),
      fc.func(fc.boolean()),
      fc.func(fc.integer()),
      (arr, predicate, transform) => {
        const result1 = arr.filter(predicate).map(transform)
        const result2 = arr.map(transform).filter((_, i) =>
          predicate(arr[i])
        )
        // Order might differ but length should match
        expect(result1.length).toBe(result2.length)
      }
    )
  )
})
```

### Python: Cache Behavior

```python
from hypothesis import given, strategies as st

@given(st.text(), st.integers())
def test_cache_returns_same_value(key, value):
    cache = Cache()

    # First set
    cache.set(key, value)
    result1 = cache.get(key)

    # Second get should return same value
    result2 = cache.get(key)

    assert result1 == value
    assert result2 == value
```

## Best Practices

**Start with Properties**
- Identify mathematical properties (commutative, associative)
- Look for roundtrip properties (encode/decode)
- Test invariants (things that should always be true)
- Verify contracts and postconditions

**Complement Example-Based Tests**
```typescript
// Use both approaches
test('addition examples', () => {
  expect(add(2, 3)).toBe(5)
  expect(add(-1, 1)).toBe(0)
})

test('addition properties', () => {
  fc.assert(
    fc.property(fc.integer(), fc.integer(), (a, b) => {
      expect(add(a, b)).toBe(add(b, a)) // Commutative
      expect(add(a, 0)).toBe(a)          // Identity
    })
  )
})
```

**Shrinking is Your Friend**
- Don't ignore shrunk counterexamples
- Minimal failing cases reveal root causes
- Shrinking finds edge cases you'd never write by hand

**Performance Considerations**
```typescript
// Limit expensive tests
fc.assert(
  fc.property(fc.array(fc.integer()), (arr) => {
    expensiveOperation(arr)
  }),
  { numRuns: 50 } // Reduce from default 100
)
```

**Reproducibility**
```python
# Set seed for reproducible failures
@settings(derandomize=True)
@given(st.lists(st.integers()))
def test_reproducible(arr):
    assert process(arr) is not None
```

## Common Pitfalls

**Overly Permissive Assertions**
```typescript
// ❌ BAD: Too weak
fc.assert(
  fc.property(fc.array(fc.integer()), (arr) => {
    expect(sort(arr)).toBeDefined() // Passes even if sort is broken!
  })
)

// ✅ GOOD: Specific properties
fc.assert(
  fc.property(fc.array(fc.integer()), (arr) => {
    const sorted = sort(arr)
    // Check actual properties
    for (let i = 1; i < sorted.length; i++) {
      expect(sorted[i]).toBeGreaterThanOrEqual(sorted[i - 1])
    }
  })
)
```

**Too Many Assumptions**
```python
# ❌ BAD: Filters out too many cases
@given(st.integers(), st.integers())
def test_slow(a, b):
    assume(a > 100)
    assume(a < 110)
    assume(b > 200)
    assume(b < 210)
    # Better to use specific strategy!

# ✅ GOOD: Generate what you need
@given(st.integers(min_value=101, max_value=109),
       st.integers(min_value=201, max_value=209))
def test_fast(a, b):
    # No filtering needed
```

**Testing Implementation, Not Properties**
```typescript
// ❌ BAD: Tests implementation
fc.assert(
  fc.property(fc.array(fc.integer()), (arr) => {
    const spy = vi.spyOn(Math, 'max')
    sort(arr)
    expect(spy).toHaveBeenCalled() // Testing how it's implemented
  })
)

// ✅ GOOD: Tests properties
fc.assert(
  fc.property(fc.array(fc.integer()), (arr) => {
    const sorted = sort(arr)
    // Test what it does, not how
    expect(sorted.length).toBe(arr.length)
    expect(new Set(sorted)).toEqual(new Set(arr))
  })
)
```

## CI/CD Integration

### TypeScript

```json
{
  "scripts": {
    "test": "vitest",
    "test:property": "vitest --grep 'property'",
    "test:ci": "vitest --run --coverage"
  }
}
```

### Python

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v1
      - run: uv sync
      - run: uv run pytest --hypothesis-show-statistics
```

## Troubleshooting

**Tests taking too long**
```typescript
// Reduce number of runs
fc.assert(property, { numRuns: 50 })
```

```python
@settings(max_examples=50)
@given(...)
```

**Hard to find failing case**
```typescript
// Increase attempts
fc.assert(property, { numRuns: 10000 })
```

**Flaky property tests**
```python
# Use seed for reproducibility
@settings(derandomize=True)
```

**Too many filtered cases**
```
Hypothesis: Unable to satisfy assumptions
```
→ Use more specific generators instead of `assume()`

## See Also

- `vitest-testing` - Unit testing framework
- `python-testing` - Python pytest testing
- `test-quality-analysis` - Detecting test smells
- `mutation-testing` - Validate test effectiveness

## References

- fast-check: https://fast-check.dev/
- Hypothesis: https://hypothesis.readthedocs.io/
- Property-Based Testing: https://fsharpforfunandprofit.com/posts/property-based-testing/
