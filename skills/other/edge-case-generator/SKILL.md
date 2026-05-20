---
name: edge-case-generator
description: Automatically identify potential boundary and exception cases from requirements, specifications, or existing code, and generate comprehensive test cases targeting boundary conditions, edge cases, and uncommon scenarios. Use this skill when analyzing programs, code repositories, functions, or APIs to discover and test corner cases, null handling, overflow conditions, empty inputs, concurrent access patterns, and other exceptional scenarios that are often missed in standard testing.
---

# Edge Case Generator

Systematically identify boundary conditions, edge cases, and exceptional scenarios, then generate comprehensive tests to validate software behavior under uncommon conditions.

## Core Capabilities

### 1. Edge Case Identification

Analyze code, specifications, or requirements to identify:

- **Boundary values**: Min/max limits, zero, empty, first/last elements
- **Null and undefined**: Missing data, null pointers, undefined references
- **Type boundaries**: Integer overflow, floating-point precision, type mismatches
- **Collection edge cases**: Empty collections, single element, duplicates
- **State transitions**: Invalid state sequences, concurrent modifications
- **Resource limits**: Memory exhaustion, timeout scenarios, disk full
- **Special characters**: Unicode, whitespace, control characters
- **Concurrency issues**: Race conditions, deadlocks, thread safety

### 2. Test Generation

Generate tests in multiple formats:

- Unit tests (pytest, Jest, JUnit, Go testing, etc.)
- Integration test scenarios
- Property-based tests (Hypothesis, QuickCheck, fast-check)
- Mutation testing scenarios
- Fuzz testing inputs

### 3. Multi-Language Support

Support major programming languages:
- Python, JavaScript/TypeScript, Java, C/C++, Go, Rust, C#, Ruby, PHP, Swift, Kotlin

## Edge Case Analysis Workflow

### Step 1: Identify Input Domains

Analyze each input parameter or data structure:

**For numeric inputs:**
```
- Minimum value (e.g., INT_MIN, 0, -∞)
- Maximum value (e.g., INT_MAX, 255, +∞)
- Zero
- One (unit value)
- Negative one
- Just below/above boundaries
- Overflow/underflow values
```

**For collections (arrays, lists, sets):**
```
- Empty collection
- Single element
- Two elements (minimal interaction)
- Maximum size (if bounded)
- All identical elements
- All unique elements
- Sorted vs unsorted
- Contains duplicates
```

**For strings:**
```
- Empty string ("")
- Single character
- Very long string (10K+ chars)
- Unicode characters (emoji, RTL, special)
- Whitespace only ("   ")
- Null terminator issues
- Special characters (\n, \t, \0)
```

**For pointers/references:**
```
- Null/None/undefined
- Dangling pointer
- Self-reference (circular)
- Uninitialized
```

### Step 2: Identify State and Preconditions

**Object state:**
```
- Uninitialized state
- Partially initialized
- Valid operational state
- Invalid/corrupted state
- Locked/busy state
- Disposed/freed state
```

**Precondition violations:**
```
- Missing required parameters
- Parameters in wrong order
- Invalid combinations
- Violated invariants
```

### Step 3: Identify Output Scenarios

**Success cases:**
```
- Typical successful execution
- Boundary successful case
- Empty result (valid but empty)
```

**Failure cases:**
```
- Expected exceptions/errors
- Timeout scenarios
- Partial failures
- Resource exhaustion
```

### Step 4: Identify Interaction Patterns

**Temporal patterns:**
```
- First operation
- Last operation
- Repeated operations
- Alternating operations
- Concurrent operations
```

**Dependency patterns:**
```
- Missing dependencies
- Circular dependencies
- Incompatible versions
- Network failures
```

### Step 5: Generate Test Cases

For each identified edge case, generate:

1. **Test name**: Descriptive name indicating the edge case
2. **Setup**: Initialize necessary state/fixtures
3. **Input**: The specific boundary or edge case input
4. **Expected behavior**: What should happen (success, specific exception, etc.)
5. **Assertions**: Verify the expected behavior
6. **Cleanup**: Restore state if necessary

## Edge Case Categories

### Category 1: Numeric Boundaries

```python
# Example: Testing a function that calculates factorial
def test_factorial_edge_cases():
    # Zero (boundary)
    assert factorial(0) == 1

    # One (boundary)
    assert factorial(1) == 1

    # Negative (invalid input)
    with pytest.raises(ValueError):
        factorial(-1)

    # Large value (overflow risk)
    with pytest.raises(OverflowError):
        factorial(10000)

    # Non-integer (type boundary)
    with pytest.raises(TypeError):
        factorial(3.5)
```

### Category 2: Collection Boundaries

```javascript
// Example: Testing an array processing function
describe('processArray edge cases', () => {
  test('empty array', () => {
    expect(processArray([])).toEqual([]);
  });

  test('single element', () => {
    expect(processArray([1])).toEqual([1]);
  });

  test('null input', () => {
    expect(() => processArray(null)).toThrow(TypeError);
  });

  test('undefined input', () => {
    expect(() => processArray(undefined)).toThrow(TypeError);
  });

  test('all identical elements', () => {
    expect(processArray([5, 5, 5, 5])).toEqual([5, 5, 5, 5]);
  });

  test('very large array', () => {
    const largeArray = new Array(1000000).fill(1);
    expect(() => processArray(largeArray)).not.toThrow();
  });
});
```

### Category 3: String Boundaries

```java
// Example: Testing string validation
@Test
public void testValidateString_EdgeCases() {
    // Empty string
    assertThrows(ValidationException.class, () -> validateString(""));

    // Null
    assertThrows(NullPointerException.class, () -> validateString(null));

    // Single character
    assertTrue(validateString("a"));

    // Whitespace only
    assertFalse(validateString("   "));

    // Special characters
    assertTrue(validateString("hello@world!"));

    // Unicode
    assertTrue(validateString("你好世界"));

    // Very long string
    String longString = "a".repeat(100000);
    assertDoesNotThrow(() -> validateString(longString));

    // Control characters
    assertFalse(validateString("hello\0world"));
}
```

### Category 4: Pointer/Reference Boundaries

```c
// Example: Testing pointer operations
void test_pointer_edge_cases() {
    // Null pointer
    assert(safe_strlen(NULL) == -1);

    // Empty string
    assert(safe_strlen("") == 0);

    // Single character
    assert(safe_strlen("a") == 1);

    // Very long string
    char long_str[10000];
    memset(long_str, 'a', 9999);
    long_str[9999] = '\0';
    assert(safe_strlen(long_str) == 9999);
}
```

### Category 5: Concurrency Edge Cases

```go
// Example: Testing concurrent access
func TestConcurrentAccess(t *testing.T) {
    cache := NewCache()

    // Race condition: multiple concurrent writes
    t.Run("concurrent writes", func(t *testing.T) {
        var wg sync.WaitGroup
        for i := 0; i < 100; i++ {
            wg.Add(1)
            go func(val int) {
                defer wg.Done()
                cache.Set("key", val)
            }(i)
        }
        wg.Wait()
        // Verify cache is in valid state
        _, ok := cache.Get("key")
        assert.True(t, ok)
    })

    // Deadlock scenario
    t.Run("potential deadlock", func(t *testing.T) {
        done := make(chan bool)
        go func() {
            cache.Set("key1", 1)
            cache.Set("key2", 2)
            done <- true
        }()

        select {
        case <-done:
            // Success
        case <-time.After(5 * time.Second):
            t.Fatal("Deadlock detected")
        }
    })
}
```

### Category 6: State Transition Edge Cases

```python
# Example: Testing state machine
def test_state_machine_edge_cases():
    machine = StateMachine()

    # Invalid initial transition
    with pytest.raises(InvalidStateError):
        machine.stop()  # Can't stop before starting

    # Double start
    machine.start()
    with pytest.raises(InvalidStateError):
        machine.start()  # Already started

    # Transition from error state
    machine.trigger_error()
    with pytest.raises(InvalidStateError):
        machine.resume()  # Can't resume from error

    # Valid state sequence
    machine.reset()
    machine.start()
    machine.pause()
    machine.resume()
    machine.stop()
    assert machine.state == "stopped"
```

### Category 7: Resource Limit Edge Cases

```python
# Example: Testing memory and resource limits
def test_resource_limits():
    # Memory exhaustion
    with pytest.raises(MemoryError):
        allocate_huge_buffer(size=10**15)

    # File handle exhaustion
    handles = []
    try:
        for i in range(10000):
            handles.append(open(f'/tmp/test_{i}', 'w'))
    except OSError as e:
        assert "Too many open files" in str(e)
    finally:
        for h in handles:
            h.close()

    # Timeout scenarios
    with pytest.raises(TimeoutError):
        slow_operation(timeout=0.001)  # Very short timeout

    # Disk full simulation
    with patch('os.write', side_effect=OSError("No space left on device")):
        with pytest.raises(OSError):
            write_large_file()
```

## Test Generation Patterns

### Pattern 1: Equivalence Partitioning

Divide input domain into equivalence classes:

```python
# For a function that accepts age (0-120)
# Partitions: Invalid (<0), Valid (0-120), Invalid (>120)

def test_age_validation():
    # Invalid: negative
    assert not is_valid_age(-1)
    assert not is_valid_age(-100)

    # Valid: boundaries
    assert is_valid_age(0)
    assert is_valid_age(120)

    # Valid: typical
    assert is_valid_age(25)
    assert is_valid_age(65)

    # Invalid: too large
    assert not is_valid_age(121)
    assert not is_valid_age(1000)
```

### Pattern 2: Boundary Value Analysis

Test at and around boundaries:

```javascript
// For array index access (0 to length-1)
describe('array access boundaries', () => {
  const arr = [10, 20, 30, 40, 50];

  test('before first element', () => {
    expect(() => arr.at(-1)).toThrow(RangeError);
  });

  test('first element (boundary)', () => {
    expect(arr.at(0)).toBe(10);
  });

  test('second element (just inside)', () => {
    expect(arr.at(1)).toBe(20);
  });

  test('last element (boundary)', () => {
    expect(arr.at(4)).toBe(50);
  });

  test('after last element', () => {
    expect(() => arr.at(5)).toThrow(RangeError);
  });
});
```

### Pattern 3: Property-Based Testing

Generate random edge cases automatically:

```python
from hypothesis import given, strategies as st

@given(st.lists(st.integers()))
def test_sort_properties(input_list):
    """Property: sorted list length equals input length"""
    result = sort(input_list)
    assert len(result) == len(input_list)

@given(st.lists(st.integers(), min_size=1))
def test_max_element_property(input_list):
    """Property: max element >= all elements"""
    max_val = find_max(input_list)
    assert all(max_val >= x for x in input_list)

@given(st.text())
def test_string_reverse_property(s):
    """Property: reversing twice returns original"""
    assert reverse(reverse(s)) == s
```

### Pattern 4: Mutation Testing

Test that tests actually catch bugs:

```python
# Original function
def is_even(n):
    return n % 2 == 0

# Mutant 1: Changed == to !=
def is_even_mutant1(n):
    return n % 2 != 0  # Should be caught by tests

# Test that catches this mutation
def test_is_even():
    assert is_even(0) == True   # Catches mutant1
    assert is_even(1) == False  # Catches mutant1
    assert is_even(2) == True   # Catches mutant1
```

## Common Edge Case Checklist

Use this checklist when analyzing code:

### Numeric Inputs
- [ ] Zero value
- [ ] Negative values
- [ ] Maximum value for type
- [ ] Minimum value for type
- [ ] Overflow/underflow
- [ ] NaN, Infinity (for floats)
- [ ] Precision loss
- [ ] Division by zero

### Collections
- [ ] Empty collection
- [ ] Single element
- [ ] Null/undefined collection
- [ ] Maximum capacity
- [ ] All elements identical
- [ ] Unsorted input
- [ ] Duplicates present
- [ ] Nested structures

### Strings
- [ ] Empty string
- [ ] Null/undefined
- [ ] Single character
- [ ] Whitespace only
- [ ] Very long string (>10K chars)
- [ ] Unicode/emoji
- [ ] Special characters
- [ ] Control characters

### Pointers/References
- [ ] Null pointer
- [ ] Dangling pointer
- [ ] Self-reference
- [ ] Circular references
- [ ] Uninitialized

### State/Lifecycle
- [ ] Before initialization
- [ ] After cleanup/disposal
- [ ] Invalid state transitions
- [ ] Reentrant calls
- [ ] Idempotency

### Concurrency
- [ ] Race conditions
- [ ] Deadlock potential
- [ ] Thread safety
- [ ] Atomic operations
- [ ] Lock ordering

### Resources
- [ ] Memory exhaustion
- [ ] File handle limits
- [ ] Network timeouts
- [ ] Disk full
- [ ] Permission denied

### Dependencies
- [ ] Missing dependencies
- [ ] Version mismatches
- [ ] Network unavailable
- [ ] Service down
- [ ] Corrupted data

## Language-Specific Patterns

For language-specific edge cases and test patterns, see the reference files:

- **Python**: See [references/python_edge_cases.md](references/python_edge_cases.md)
- **JavaScript/TypeScript**: See [references/javascript_edge_cases.md](references/javascript_edge_cases.md)
- **Java**: See [references/java_edge_cases.md](references/java_edge_cases.md)
- **C/C++**: See [references/c_cpp_edge_cases.md](references/c_cpp_edge_cases.md)

## Best Practices

1. **Prioritize edge cases**: Focus on cases most likely to cause failures
2. **Test both sides of boundaries**: Not just at the boundary, but just before and after
3. **Combine edge cases**: Test multiple edge conditions together
4. **Document assumptions**: Explain what each edge case tests
5. **Use descriptive names**: Test names should clearly indicate the edge case
6. **Isolate tests**: Each test should be independent
7. **Consider performance**: Some edge cases (large inputs) may be slow
8. **Property-based testing**: Use tools like Hypothesis/QuickCheck for automatic edge case generation

## Example: Complete Edge Case Analysis

Given a function specification:

```python
def binary_search(arr: list[int], target: int) -> int:
    """
    Find target in sorted array using binary search.
    Returns index if found, -1 otherwise.
    Requires: arr is sorted in ascending order
    """
```

**Generated edge case tests:**

```python
import pytest

class TestBinarySearchEdgeCases:
    """Comprehensive edge case tests for binary_search"""

    # Collection boundaries
    def test_empty_array(self):
        """Edge: Empty collection"""
        assert binary_search([], 5) == -1

    def test_single_element_found(self):
        """Edge: Single element - target present"""
        assert binary_search([5], 5) == 0

    def test_single_element_not_found(self):
        """Edge: Single element - target absent"""
        assert binary_search([5], 3) == -1

    def test_two_elements_first(self):
        """Edge: Minimal interaction - target is first"""
        assert binary_search([1, 2], 1) == 0

    def test_two_elements_second(self):
        """Edge: Minimal interaction - target is second"""
        assert binary_search([1, 2], 2) == 1

    # Position boundaries
    def test_target_at_start(self):
        """Edge: Target at first position"""
        assert binary_search([1, 2, 3, 4, 5], 1) == 0

    def test_target_at_end(self):
        """Edge: Target at last position"""
        assert binary_search([1, 2, 3, 4, 5], 5) == 4

    def test_target_before_range(self):
        """Edge: Target less than all elements"""
        assert binary_search([5, 10, 15], 3) == -1

    def test_target_after_range(self):
        """Edge: Target greater than all elements"""
        assert binary_search([5, 10, 15], 20) == -1

    # Duplicate elements
    def test_all_elements_same(self):
        """Edge: All elements identical"""
        arr = [5, 5, 5, 5, 5]
        assert binary_search(arr, 5) in range(len(arr))

    def test_duplicates_present(self):
        """Edge: Target appears multiple times"""
        # Should return any valid index
        result = binary_search([1, 2, 2, 2, 3], 2)
        assert result in [1, 2, 3]

    # Numeric boundaries
    def test_negative_values(self):
        """Edge: Negative numbers"""
        assert binary_search([-10, -5, 0, 5, 10], -5) == 1

    def test_zero_value(self):
        """Edge: Zero in array"""
        assert binary_search([-2, -1, 0, 1, 2], 0) == 2

    def test_large_values(self):
        """Edge: Near integer limits"""
        import sys
        max_int = sys.maxsize
        assert binary_search([0, max_int], max_int) == 1

    # Size boundaries
    def test_very_large_array(self):
        """Edge: Performance with large array"""
        arr = list(range(1000000))
        assert binary_search(arr, 999999) == 999999

    # Invalid inputs
    def test_null_array(self):
        """Edge: Null/None array"""
        with pytest.raises(TypeError):
            binary_search(None, 5)

    def test_unsorted_array(self):
        """Edge: Precondition violation - unsorted array"""
        # May return incorrect result or -1
        # This tests documentation compliance
        result = binary_search([5, 1, 3, 2, 4], 3)
        # Behavior is undefined, just ensure no crash
        assert isinstance(result, int)
```

This comprehensive test suite covers 18 distinct edge cases across multiple categories.
