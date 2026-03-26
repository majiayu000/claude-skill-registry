---
created: 2025-12-16
modified: 2025-12-16
reviewed: 2025-12-16
name: hypothesis-testing
description: |
  Property-based testing with Hypothesis for discovering edge cases and validating invariants.
  Use when implementing comprehensive test coverage, testing complex logic with many inputs,
  or validating mathematical properties and invariants across input domains.
  Triggered by: hypothesis, property-based testing, @given, strategies, generative testing.
---

# Hypothesis Property-Based Testing

Hypothesis is a powerful property-based testing library that automatically generates test cases to find edge cases and validate properties of your code.

## Core Concept

**Traditional example-based testing:**
```python
def test_addition():
    assert add(2, 3) == 5
    assert add(0, 0) == 0
    assert add(-1, 1) == 0
```

**Property-based testing with Hypothesis:**
```python
from hypothesis import given
import hypothesis.strategies as st

@given(st.integers(), st.integers())
def test_addition_commutative(a, b):
    """Addition is commutative for ALL integers."""
    assert add(a, b) == add(b, a)
```

Hypothesis generates hundreds of test cases automatically, including edge cases you might not think of.

## Installation

```bash
# Install hypothesis with pytest integration
uv add --dev hypothesis pytest

# Optional plugins
uv add --dev hypothesis[numpy]      # NumPy strategies
uv add --dev hypothesis[pandas]     # Pandas strategies
uv add --dev hypothesis[django]     # Django model strategies
```

## Configuration

### pyproject.toml Configuration

```toml
[tool.pytest.ini_options]
# Hypothesis settings
addopts = [
    "--hypothesis-show-statistics",  # Show test statistics
    "--hypothesis-seed=0",            # Reproducible tests (optional)
]

[tool.hypothesis]
# Maximum number of examples to generate
max_examples = 200  # Default: 100, CI: 200+

# Deadline for each test case (milliseconds)
deadline = 1000  # Default: 200ms, None to disable

# Verbosity level (quiet, normal, verbose, debug)
verbosity = "normal"

# Fail fast on first error
derandomize = false  # Set to true for deterministic tests

# Database for example storage
database = ".hypothesis/examples"  # Store found failures

# Profile-specific settings
[tool.hypothesis.profiles.dev]
max_examples = 50
deadline = 1000
verbosity = "normal"

[tool.hypothesis.profiles.ci]
max_examples = 500
deadline = 5000
verbosity = "verbose"

[tool.hypothesis.profiles.debug]
max_examples = 10
deadline = null
verbosity = "debug"
```

### Activate Profile

```python
# tests/conftest.py
from hypothesis import settings, Verbosity

# Set default profile based on environment
import os
if os.getenv("CI"):
    settings.load_profile("ci")
else:
    settings.load_profile("dev")

# Or configure programmatically
settings.register_profile("custom", max_examples=100, deadline=500)
settings.load_profile("custom")
```

## Basic Usage

### Simple Property Tests

```python
from hypothesis import given, example
import hypothesis.strategies as st

# Test numeric properties
@given(st.integers())
def test_absolute_value_non_negative(x):
    """abs(x) is always non-negative."""
    assert abs(x) >= 0

@given(st.integers(), st.integers())
def test_addition_associative(a, b, c):
    """Addition is associative: (a + b) + c == a + (b + c)."""
    assert (a + b) + c == a + (b + c)

# Test string properties
@given(st.text())
def test_string_length(s):
    """Length of reversed string equals original."""
    assert len(s[::-1]) == len(s)

@given(st.text(), st.text())
def test_string_concatenation(s1, s2):
    """String concatenation length is sum of lengths."""
    result = s1 + s2
    assert len(result) == len(s1) + len(s2)

# Add explicit examples alongside generated ones
@given(st.integers())
@example(0)
@example(-1)
@example(2**31 - 1)
def test_with_explicit_examples(x):
    """Test with both generated and explicit examples."""
    assert process(x) is not None
```

### Testing Functions

```python
from hypothesis import given, assume
import hypothesis.strategies as st

def safe_divide(a: float, b: float) -> float:
    """Divide a by b, avoiding division by zero."""
    if b == 0:
        raise ValueError("Division by zero")
    return a / b

@given(st.floats(allow_nan=False, allow_infinity=False),
       st.floats(allow_nan=False, allow_infinity=False))
def test_safe_divide(a, b):
    """Test safe_divide with all valid floats."""
    assume(b != 0)  # Skip cases where b is zero

    result = safe_divide(a, b)

    # Properties to verify
    assert isinstance(result, float)
    assert result * b == pytest.approx(a)  # Inverse operation

@given(st.floats())
def test_divide_by_zero_raises(a):
    """Division by zero raises ValueError."""
    with pytest.raises(ValueError, match="Division by zero"):
        safe_divide(a, 0)
```

## Strategies

### Built-in Strategies

```python
import hypothesis.strategies as st

# Primitives
st.none()                    # None
st.booleans()                # True/False
st.integers()                # Any integer
st.integers(min_value=0, max_value=100)  # Bounded integers
st.floats()                  # Any float
st.floats(min_value=0.0, max_value=1.0)  # Bounded floats
st.decimals()                # Decimal numbers
st.fractions()               # Fraction objects
st.complex_numbers()         # Complex numbers

# Text and bytes
st.text()                    # Unicode strings
st.text(alphabet="abc")      # Limited alphabet
st.text(min_size=1, max_size=10)  # Bounded length
st.binary()                  # Bytes
st.characters()              # Single characters

# Collections
st.lists(st.integers())      # Lists of integers
st.lists(st.text(), min_size=1, max_size=10)  # Bounded lists
st.tuples(st.integers(), st.text())  # Fixed-size tuples
st.sets(st.integers())       # Sets
st.frozensets(st.text())     # Frozen sets
st.dictionaries(keys=st.text(), values=st.integers())  # Dicts

# Special types
st.uuids()                   # UUID objects
st.datetimes()               # datetime objects
st.dates()                   # date objects
st.times()                   # time objects
st.timedeltas()              # timedelta objects

# Constrained types
st.emails()                  # Valid email addresses
st.ip_addresses()            # IP addresses (v4 and v6)
st.urls()                    # Valid URLs
```

### Composite Strategies

```python
from hypothesis import given
from hypothesis.strategies import composite
import hypothesis.strategies as st

# Define custom strategy
@composite
def users(draw):
    """Generate user objects."""
    return {
        "id": draw(st.integers(min_value=1)),
        "name": draw(st.text(min_size=1, max_size=50)),
        "email": draw(st.emails()),
        "age": draw(st.integers(min_value=0, max_value=120)),
        "active": draw(st.booleans())
    }

@given(users())
def test_user_validation(user):
    """Test user validation with generated users."""
    assert user["id"] > 0
    assert len(user["name"]) > 0
    assert "@" in user["email"]
    assert 0 <= user["age"] <= 120

# Complex composite strategy
@composite
def http_requests(draw):
    """Generate HTTP request objects."""
    method = draw(st.sampled_from(["GET", "POST", "PUT", "DELETE"]))
    path = draw(st.text(alphabet="abcdefghijklmnopqrstuvwxyz/", min_size=1))
    headers = draw(st.dictionaries(
        keys=st.text(alphabet="abcdefghijklmnopqrstuvwxyz-", min_size=1),
        values=st.text()
    ))

    body = None
    if method in ["POST", "PUT"]:
        body = draw(st.one_of(st.none(), st.text(), st.binary()))

    return {
        "method": method,
        "path": f"/{path}",
        "headers": headers,
        "body": body
    }

@given(http_requests())
def test_request_handler(request):
    """Test HTTP request handler with various requests."""
    response = handle_request(request)
    assert response.status_code in [200, 201, 400, 404, 500]
```

### Data Classes and Models

```python
from dataclasses import dataclass
from hypothesis import given
from hypothesis.strategies import builds
import hypothesis.strategies as st

@dataclass
class Point:
    x: float
    y: float

# Generate Point instances
@given(builds(Point, x=st.floats(), y=st.floats()))
def test_point_distance(point):
    """Test distance calculation for points."""
    origin = Point(0.0, 0.0)
    distance = calculate_distance(origin, point)
    assert distance >= 0

# More complex model
@dataclass
class User:
    id: int
    name: str
    email: str
    age: int

# Strategy with validation
def valid_users():
    return builds(
        User,
        id=st.integers(min_value=1),
        name=st.text(min_size=1, max_size=100),
        email=st.emails(),
        age=st.integers(min_value=0, max_value=120)
    )

@given(valid_users())
def test_user_serialization(user):
    """Test user serialization round-trip."""
    json_data = user.to_json()
    restored = User.from_json(json_data)
    assert restored == user
```

### Strategy Combinators

```python
import hypothesis.strategies as st

# one_of: Choose from multiple strategies
st.one_of(st.none(), st.integers(), st.text())

# sampled_from: Sample from a list
st.sampled_from(["admin", "user", "guest"])

# just: Always return a specific value
st.just(42)

# lists with constraints
st.lists(
    st.integers(min_value=0),
    min_size=1,
    max_size=10,
    unique=True  # No duplicates
)

# dictionaries with constraints
st.dictionaries(
    keys=st.text(min_size=1),
    values=st.integers(),
    min_size=1,
    max_size=5
)

# tuples with mixed types
st.tuples(st.integers(), st.text(), st.booleans())

# fixed_dictionaries: Dictionary with specific keys
st.fixed_dictionaries({
    "id": st.integers(min_value=1),
    "name": st.text(),
    "optional": st.one_of(st.none(), st.text())
})

# recursive: Generate recursive structures
json_strategy = st.recursive(
    st.one_of(st.none(), st.booleans(), st.floats(), st.text()),
    lambda children: st.lists(children) | st.dictionaries(st.text(), children),
    max_leaves=10
)
```

## Advanced Patterns

### Stateful Testing

```python
from hypothesis.stateful import RuleBasedStateMachine, rule, invariant
import hypothesis.strategies as st

class ShoppingCartMachine(RuleBasedStateMachine):
    """Test shopping cart with stateful operations."""

    def __init__(self):
        super().__init__()
        self.cart = ShoppingCart()
        self.items_added = []

    @rule(item=st.text(min_size=1), quantity=st.integers(min_value=1, max_value=10))
    def add_item(self, item, quantity):
        """Add item to cart."""
        self.cart.add(item, quantity)
        self.items_added.append((item, quantity))

    @rule(item=st.text())
    def remove_item(self, item):
        """Remove item from cart."""
        try:
            self.cart.remove(item)
            self.items_added = [(i, q) for i, q in self.items_added if i != item]
        except ValueError:
            # Item not in cart, expected
            pass

    @rule()
    def clear_cart(self):
        """Clear entire cart."""
        self.cart.clear()
        self.items_added = []

    @invariant()
    def cart_is_consistent(self):
        """Cart item count matches what we've added."""
        expected_items = {item: qty for item, qty in self.items_added}
        actual_items = self.cart.get_items()
        assert expected_items == actual_items

    @invariant()
    def total_is_non_negative(self):
        """Cart total is always non-negative."""
        assert self.cart.get_total() >= 0

# Run the state machine
TestShoppingCart = ShoppingCartMachine.TestCase
```

### Shrinking and Example Database

```python
from hypothesis import given, settings, example
import hypothesis.strategies as st

@given(st.lists(st.integers()))
def test_list_processing(items):
    """Test list processing - Hypothesis will shrink failing examples."""
    result = process_list(items)
    assert result is not None

# When a test fails, Hypothesis:
# 1. Finds the failing input
# 2. Shrinks it to the simplest failing case
# 3. Stores it in .hypothesis/examples database
# 4. Replays it on future runs

# Example: If test fails on [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# Hypothesis shrinks to smallest failing case: [1, 2]

# Disable shrinking for debugging
@given(st.lists(st.integers()))
@settings(max_examples=100, phases=["generate"])  # Skip shrink phase
def test_without_shrinking(items):
    """Test without shrinking for faster debugging."""
    assert process_list(items) is not None
```

### Targeted Property Testing

```python
from hypothesis import given, target
import hypothesis.strategies as st

@given(st.lists(st.integers()))
def test_sort_with_targeting(items):
    """Guide Hypothesis toward larger lists."""
    # Target larger lists to test scalability
    target(float(len(items)))

    sorted_items = sorted(items)
    assert all(sorted_items[i] <= sorted_items[i+1]
               for i in range(len(sorted_items) - 1))

@given(st.floats(min_value=0.0, max_value=1.0))
def test_with_edge_targeting(probability):
    """Guide Hypothesis toward edge values (0.0 and 1.0)."""
    # Target values close to edges
    target(abs(probability - 0.5))  # Prefer extreme values

    result = simulate_with_probability(probability)
    assert 0 <= result <= 1
```

### Hypothesis with Async Code

```python
import pytest
from hypothesis import given
import hypothesis.strategies as st

# Async property test
@pytest.mark.asyncio
@given(st.integers())
async def test_async_function(value):
    """Test async function with property-based testing."""
    result = await async_process(value)
    assert result is not None

# Async with composite strategies
@pytest.mark.asyncio
@given(st.lists(st.integers(), min_size=1))
async def test_async_batch_processing(items):
    """Test async batch processing."""
    results = await process_batch(items)
    assert len(results) == len(items)
    assert all(r is not None for r in results)
```

## When to Use Hypothesis vs Example-Based Tests

### Use Hypothesis (Property-Based) When:

1. **Testing mathematical properties**
   ```python
   @given(st.integers(), st.integers())
   def test_addition_commutative(a, b):
       assert a + b == b + a
   ```

2. **Testing invariants across many inputs**
   ```python
   @given(st.lists(st.integers()))
   def test_sort_idempotent(items):
       sorted_once = sorted(items)
       sorted_twice = sorted(sorted_once)
       assert sorted_once == sorted_twice
   ```

3. **Finding edge cases**
   ```python
   @given(st.text())
   def test_parse_input(text):
       # Hypothesis will find weird edge cases like:
       # "", "\x00", "🔥", very long strings, etc.
       result = parse(text)
       assert result is not None
   ```

4. **Testing serialization round-trips**
   ```python
   @given(st.from_type(MyData))
   def test_serialization(data):
       json_str = data.to_json()
       restored = MyData.from_json(json_str)
       assert restored == data
   ```

5. **Testing APIs with many parameters**
   ```python
   @given(
       st.text(),
       st.integers(min_value=1),
       st.booleans(),
       st.sampled_from(["option1", "option2"])
   )
   def test_api_call(name, count, flag, option):
       response = api_call(name, count, flag, option)
       assert response.status in [200, 400]
   ```

### Use Example-Based Tests When:

1. **Testing specific known edge cases**
   ```python
   def test_empty_list():
       assert process([]) == []

   def test_single_item():
       assert process([1]) == [1]
   ```

2. **Testing exact business logic**
   ```python
   def test_discount_calculation():
       # Exact prices from requirements
       assert calculate_discount(100, 0.1) == 10
       assert calculate_discount(50, 0.2) == 10
   ```

3. **Testing error messages**
   ```python
   def test_validation_error_message():
       with pytest.raises(ValueError, match="Email must contain @"):
           validate_email("invalid")
   ```

4. **Testing integration with external systems**
   ```python
   def test_api_integration():
       # Specific API behavior
       response = api.get("/users/123")
       assert response["name"] == "Test User"
   ```

5. **Testing UI behavior**
   ```python
   def test_button_click():
       button.click()
       assert button.text == "Clicked"
   ```

### Hybrid Approach (Best Practice)

```python
from hypothesis import given, example
import hypothesis.strategies as st

# Combine property-based + example-based
@given(st.integers())
@example(0)           # Explicit edge case
@example(-1)          # Explicit edge case
@example(2**31 - 1)   # Explicit edge case
def test_absolute_value(x):
    """Test with both generated and explicit examples."""
    result = abs(x)
    assert result >= 0
    assert result == abs(-x)

# Property test + regression test
@given(st.lists(st.integers()))
@example([1, 2, 3])  # Known good case
@example([])         # Edge case
@example([42] * 1000)  # Performance edge case
def test_list_processing(items):
    """Test general property + specific known cases."""
    result = process_list(items)
    assert len(result) == len(items)
```

## Best Practices

### 1. Start with Simple Properties

```python
# Start simple
@given(st.integers())
def test_increment(x):
    assert x + 1 > x

# Then add complexity
@given(st.integers(), st.integers())
def test_addition_properties(a, b):
    # Commutative
    assert a + b == b + a
    # Associative
    assert (a + 1) + b == a + (1 + b)
```

### 2. Use assume() Sparingly

```python
# BAD: Too many assumes (slow)
@given(st.integers(), st.integers())
def test_slow(a, b):
    assume(a > 0)
    assume(b > 0)
    assume(a < 100)
    assume(b < 100)
    assert a + b < 200

# GOOD: Use constrained strategies
@given(st.integers(min_value=1, max_value=99),
       st.integers(min_value=1, max_value=99))
def test_fast(a, b):
    assert a + b < 200
```

### 3. Test Invariants, Not Implementation

```python
# BAD: Tests implementation details
@given(st.lists(st.integers()))
def test_sort_implementation(items):
    result = my_sort(items)
    # Checks specific algorithm behavior
    assert result.pivot_index == len(items) // 2

# GOOD: Tests invariants
@given(st.lists(st.integers()))
def test_sort_properties(items):
    result = my_sort(items)
    # Checks output properties
    assert len(result) == len(items)
    assert sorted(result) == result
    assert set(result) == set(items)
```

### 4. Use @example() for Regression Tests

```python
@given(st.lists(st.integers()))
@example([])              # Found bug with empty list
@example([1, 1, 1])       # Found bug with duplicates
@example([-2**31])        # Found bug with min int
def test_with_regressions(items):
    """Property test + regression tests."""
    result = process(items)
    assert result is not None
```

### 5. Configure for Different Environments

```python
from hypothesis import given, settings, Verbosity

# Development: Fast feedback
@given(st.lists(st.integers()))
@settings(max_examples=50, deadline=500)
def test_dev(items):
    assert process(items) is not None

# CI: Thorough testing
@given(st.lists(st.integers()))
@settings(max_examples=500, deadline=5000, verbosity=Verbosity.verbose)
def test_ci(items):
    assert process(items) is not None
```

## Common Patterns

### Testing Encoding/Decoding

```python
@given(st.from_type(MyData))
def test_json_roundtrip(data):
    """JSON encoding/decoding preserves data."""
    json_str = data.to_json()
    restored = MyData.from_json(json_str)
    assert restored == data

@given(st.binary())
def test_base64_roundtrip(data):
    """Base64 encoding/decoding preserves data."""
    encoded = base64.b64encode(data)
    decoded = base64.b64decode(encoded)
    assert decoded == data
```

### Testing Parsers

```python
@given(st.text())
def test_parser_does_not_crash(text):
    """Parser handles any input without crashing."""
    try:
        result = parse(text)
        # If parsing succeeds, verify result is valid
        assert isinstance(result, ParsedData)
    except ParseError:
        # Parse errors are expected for invalid input
        pass
```

### Testing Database Operations

```python
@given(st.lists(valid_users(), max_size=10))
def test_batch_insert(users):
    """Batch insert preserves all users."""
    db.batch_insert(users)

    for user in users:
        retrieved = db.get_user(user.id)
        assert retrieved == user

@given(valid_users())
def test_update_preserves_id(user):
    """Updating user preserves ID."""
    db.save(user)
    original_id = user.id

    user.name = "Updated Name"
    db.save(user)

    assert user.id == original_id
```

## CI Integration

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Install uv
        uses: astral-sh/setup-uv@v2

      - name: Set up Python
        run: uv python install 3.12

      - name: Install dependencies
        run: uv sync --all-extras --dev

      - name: Run hypothesis tests (CI profile)
        run: |
          uv run pytest \
            --hypothesis-show-statistics \
            --hypothesis-profile=ci \
            --hypothesis-seed=${{ github.run_number }}

      - name: Upload hypothesis database
        uses: actions/upload-artifact@v4
        if: failure()
        with:
          name: hypothesis-examples
          path: .hypothesis/
```

## Debugging Failing Tests

```python
from hypothesis import given, settings, Verbosity, Phase
import hypothesis.strategies as st

# Debug mode: Verbose output, no shrinking
@given(st.lists(st.integers()))
@settings(
    verbosity=Verbosity.debug,
    max_examples=10,
    phases=[Phase.generate],  # Skip shrinking
    print_blob=True           # Print input data
)
def test_debug(items):
    """Debug failing test with full output."""
    result = buggy_function(items)
    assert result is not None

# Reproduce specific failing example
@given(st.lists(st.integers()))
@example([1, 2, -2147483648])  # Specific failing case
def test_reproduce_failure(items):
    """Reproduce and fix specific failure."""
    result = process(items)
    assert result is not None
```

## Resources

- **Hypothesis Documentation**: https://hypothesis.readthedocs.io/
- **Hypothesis for Property-Based Testing**: https://increment.com/testing/in-praise-of-property-based-testing/
- **PBT vs Example-Based**: https://hypothesis.works/articles/what-is-property-based-testing/
- **Hypothesis Strategies**: https://hypothesis.readthedocs.io/en/latest/data.html
- **Stateful Testing**: https://hypothesis.readthedocs.io/en/latest/stateful.html

## Summary

Hypothesis provides property-based testing for Python:
- **@given decorator**: Generate test inputs automatically
- **Strategies**: Built-in and custom data generators
- **Shrinking**: Automatically minimize failing examples
- **Stateful testing**: Test complex state machines
- **Example database**: Store and replay failing cases
- **Use for**: Properties, invariants, round-trips, edge case discovery
- **Combine with**: Example-based tests for comprehensive coverage
- **CI integration**: Run with more examples in CI environments
