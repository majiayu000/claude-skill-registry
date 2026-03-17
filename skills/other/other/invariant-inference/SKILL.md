---
name: invariant-inference
description: Automatically infer loop invariants for code verification and correctness proofs. Use when analyzing loops to identify properties that hold throughout execution, generating assertions for verification, proving loop correctness, or documenting loop behavior. Supports Python, Java, C/C++, and language-agnostic analysis. Generates invariants as code assertions (assert statements). Triggers when users ask to infer invariants, find loop properties, generate loop assertions, prove loop correctness, or verify loop behavior.
---

# Invariant Inference

## Overview

Analyze loops and automatically infer invariants—properties that remain true throughout loop execution. Generate these as code assertions for verification and correctness proofs.

## Workflow

### 1. Identify the Loop

First, locate and understand the loop to analyze:

**Loop types to recognize:**
- `for` loops with index variables
- `while` loops with conditions
- `do-while` loops
- Iterator-based loops
- Recursive functions (treated as implicit loops)

**Extract key information:**
- Loop variable(s) and their initial values
- Loop condition (when it terminates)
- Loop body (what happens each iteration)
- Variables modified in the loop
- Variables read but not modified

### 2. Analyze Loop Structure

Understand what the loop does:

**Categorize the loop:**
- **Accumulation**: Building up a sum, product, or collection
- **Search**: Looking for an element or condition
- **Transformation**: Modifying elements in a data structure
- **Generation**: Creating new data based on input
- **Traversal**: Visiting all elements
- **Sorting/Partitioning**: Rearranging elements

**Identify patterns:**
- Array/list iteration with bounds
- Counter increments/decrements
- Pointer advancement
- Collection building
- Flag-based early termination

### 3. Infer Invariant Categories

Generate invariants for each applicable category. See [invariant-patterns.md](references/invariant-patterns.md) for comprehensive patterns.

#### Bounds Invariants

Properties about variable ranges:

```python
# Loop: for i in range(n)
assert 0 <= i < n

# Loop: while i < len(arr)
assert 0 <= i <= len(arr)

# Loop: two pointers
while left < right:
    assert 0 <= left <= right < len(arr)
```

#### Relationship Invariants

Properties relating variables:

**Sum/Accumulation:**
```python
total = 0
for i in range(len(arr)):
    assert total == sum(arr[0:i])  # Invariant before update
    total += arr[i]
assert total == sum(arr)  # Post-condition
```

**Max/Min:**
```python
max_val = arr[0]
for i in range(1, len(arr)):
    assert max_val == max(arr[0:i])
    if arr[i] > max_val:
        max_val = arr[i]
```

**Product:**
```python
product = 1
for i in range(len(arr)):
    assert product == arr[0] * arr[1] * ... * arr[i-1]
    product *= arr[i]
```

#### Progress Invariants

Properties showing termination:

```python
# Decreasing to zero
while n > 0:
    assert n > 0  # Still positive
    n -= 1
    assert n >= 0  # Non-negative after decrement

# Increasing to limit
i = 0
while i < n:
    assert i < n  # Not yet at limit
    i += 1
    assert i <= n  # At most n
```

#### Data Structure Invariants

Properties about structure integrity:

**Sorted sublists:**
```python
# Insertion sort
for i in range(1, len(arr)):
    assert is_sorted(arr[0:i])  # Prefix is sorted
    # ... insert arr[i] into sorted position
```

**Partition property:**
```python
# Partitioning around pivot
while left < right:
    assert all(arr[j] <= pivot for j in range(0, left))
    assert all(arr[j] >= pivot for j in range(right, len(arr)))
    # ... move pointers
```

**Size invariants:**
```python
result = []
for i in range(len(items)):
    assert len(result) == i  # Processed i items so far
    if condition(items[i]):
        result.append(items[i])
```

### 4. Generate Assertions

Convert inferred invariants into code assertions:

#### Python Format

```python
def find_maximum(arr):
    """Find maximum element in array."""
    assert len(arr) > 0, "Array must not be empty"  # Pre-condition

    max_val = arr[0]

    for i in range(1, len(arr)):
        # Loop invariants
        assert 0 < i < len(arr), "Index in valid range"
        assert max_val == max(arr[0:i]), "max_val is maximum so far"
        assert max_val in arr[0:i], "max_val is from processed elements"

        if arr[i] > max_val:
            max_val = arr[i]

    assert max_val == max(arr), "max_val is maximum of entire array"  # Post-condition
    return max_val
```

#### Java Format

```java
public int findMaximum(int[] arr) {
    assert arr.length > 0 : "Array must not be empty";

    int maxVal = arr[0];

    for (int i = 1; i < arr.length; i++) {
        assert i > 0 && i < arr.length : "Index in valid range";
        assert maxVal == max(arr, 0, i) : "maxVal is maximum so far";

        if (arr[i] > maxVal) {
            maxVal = arr[i];
        }
    }

    assert maxVal == max(arr, 0, arr.length) : "maxVal is maximum";
    return maxVal;
}
```

#### C/C++ Format

```c
int find_maximum(int arr[], int n) {
    assert(n > 0);  // Pre-condition

    int max_val = arr[0];

    for (int i = 1; i < n; i++) {
        assert(i >= 1 && i < n);  // Bounds
        assert(max_val >= arr[0]);  // max_val is at least first element
        // Note: Can't easily express "max of subarray" in C without helper

        if (arr[i] > max_val) {
            max_val = arr[i];
        }
    }

    return max_val;
}
```

### 5. Verify Invariants

Check that inferred invariants are correct:

#### Initialization

Invariant must be true before the loop starts:

```python
# Loop: total = 0; for i in range(n): total += arr[i]
# Invariant: total == sum(arr[0:i])
# Check: Before loop, i=0, total=0, sum(arr[0:0])=0 ✓
```

#### Maintenance

Invariant remains true after each iteration:

```python
# Assume invariant true at start of iteration i
# Show it's true at start of iteration i+1
# Before: total == sum(arr[0:i])
# Execute: total += arr[i]
# After: total == sum(arr[0:i]) + arr[i] == sum(arr[0:i+1]) ✓
```

#### Termination

Invariant + termination condition proves post-condition:

```python
# After loop: i == n (termination) and total == sum(arr[0:i]) (invariant)
# Therefore: total == sum(arr[0:n]) == sum(arr) ✓
```

### 6. Handle Complex Cases

#### Nested Loops

Generate invariants for each nesting level:

```python
# Matrix sum
total = 0
for i in range(rows):
    assert total == sum(matrix[0:i, :])  # Outer invariant

    for j in range(cols):
        assert total == sum(matrix[0:i, :]) + sum(matrix[i, 0:j])  # Inner
        total += matrix[i][j]
```

#### Multiple Variables

Track relationships between variables:

```python
# Two pointers
left, right = 0, len(arr) - 1
while left < right:
    assert 0 <= left <= right < len(arr)
    assert left + right == len(arr) - 1  # Relationship invariant
    # (only true if they move symmetrically)
    left += 1
    right -= 1
```

#### Early Exit

Handle break/return statements:

```python
# Search with early exit
found = False
for i in range(len(arr)):
    assert not found or arr[i-1] == target  # If found, previous element was it

    if arr[i] == target:
        found = True
        break

assert not found or target in arr[0:i+1]  # Post-condition
```

#### Loop with Side Effects

Track effects on external state:

```python
# Modifying a list
for i in range(len(arr)):
    assert len(arr) remains constant  # Size doesn't change
    assert arr[0:i] are processed correctly
    arr[i] = transform(arr[i])
```

## Example Workflows

### Example 1: Simple Accumulation

**User request:**
> "Infer invariants for this sum loop"

```python
def array_sum(arr):
    total = 0
    for i in range(len(arr)):
        total += arr[i]
    return total
```

**Response:**

```python
def array_sum(arr):
    assert len(arr) >= 0  # Pre-condition: valid array

    total = 0
    for i in range(len(arr)):
        # Loop invariants
        assert 0 <= i < len(arr), "Index in valid range"
        assert total == sum(arr[0:i]), "total is sum of elements so far"

        total += arr[i]

    assert total == sum(arr), "total is sum of entire array"  # Post-condition
    return total
```

**Explanation:**
- Bounds: `0 <= i < len(arr)`
- Relationship: `total == sum(arr[0:i])`
- Progress: `i` increases each iteration
- Post-condition follows from invariant + termination

### Example 2: Search Loop

**User request:**
> "What are the invariants for binary search?"

```python
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
```

**Response:**

```python
def binary_search(arr, target):
    assert is_sorted(arr), "Array must be sorted"  # Pre-condition

    left, right = 0, len(arr) - 1

    while left <= right:
        # Loop invariants
        assert 0 <= left <= len(arr), "left in valid range"
        assert -1 <= right < len(arr), "right in valid range"
        assert left <= right + 1, "Valid search range"

        # Critical invariant: if target exists, it's in [left, right]
        assert (target not in arr or
                any(arr[i] == target for i in range(left, right + 1))), \
               "Target in current range if it exists"

        mid = (left + right) // 2

        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            assert arr[mid] < target, "All elements left of mid < target"
            left = mid + 1
        else:
            assert arr[mid] > target, "All elements right of mid > target"
            right = mid - 1

    assert left > right, "Search range exhausted"
    assert target not in arr, "Target not found implies not in array"
    return -1
```

### Example 3: Insertion Sort

**User request:**
> "Generate invariants for insertion sort"

```python
def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
```

**Response:**

```python
def insertion_sort(arr):
    for i in range(1, len(arr)):
        # Outer loop invariant
        assert is_sorted(arr[0:i]), "arr[0:i] is sorted"
        assert set(arr) == set(original_arr), "Elements unchanged (only reordered)"

        key = arr[i]
        j = i - 1

        while j >= 0 and arr[j] > key:
            # Inner loop invariants
            assert -1 <= j < i, "j in valid range"
            assert arr[j] > key, "Current element larger than key"
            assert is_sorted(arr[0:j]), "Left part still sorted"
            assert arr[j+2:i+1] are shifted right and sorted

            arr[j + 1] = arr[j]
            j -= 1

        arr[j + 1] = key
        assert is_sorted(arr[0:i+1]), "arr[0:i+1] is now sorted"

    assert is_sorted(arr), "Entire array is sorted"
```

## Tips for Effective Invariant Inference

**Start with obvious properties:**
- Variable bounds (0 <= i < n)
- Loop counter relationships
- Data structure sizes

**Look for accumulation patterns:**
- Sums, products, counts
- Max/min tracking
- Collection building

**Identify preservation properties:**
- What stays constant? (array length, set of elements)
- What grows/shrinks monotonically?
- What relationships are maintained?

**Think about the loop's purpose:**
- Why is this loop here?
- What should be true when it finishes?
- What must be true for each iteration to work?

**Verify your invariants:**
- Check initialization (true before loop)
- Check maintenance (preserved by loop body)
- Check that invariant + termination ⟹ post-condition

**Be specific:**
- Weak: `i >= 0`
- Better: `0 <= i < len(arr)`
- Best: `0 <= i < len(arr) and sum_val == sum(arr[0:i])`

**Use helper predicates for clarity:**
```python
def is_sorted(arr):
    return all(arr[i] <= arr[i+1] for i in range(len(arr)-1))

def is_partition(arr, pivot, left, right):
    return (all(arr[i] <= pivot for i in range(left)) and
            all(arr[i] >= pivot for i in range(right, len(arr))))
```

## Reference

For comprehensive invariant patterns across different loop types and languages, see [invariant-patterns.md](references/invariant-patterns.md).
