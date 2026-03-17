---
name: pseudocode-to-python-code
description: Convert pseudocode, algorithm descriptions, or specifications into complete, executable Python code. Handles natural language descriptions, structured pseudocode, and formal algorithm specifications. Generates production-ready code with type hints, docstrings, error handling, and test cases. Use when users need to (1) convert pseudocode to Python, (2) implement algorithms from descriptions, (3) translate algorithm specifications to code, (4) generate Python implementations from textbook pseudocode, or (5) create executable code from high-level algorithm designs.
---

# Pseudocode to Python Code

Convert pseudocode and algorithm descriptions into complete, executable Python code with proper structure, documentation, and tests.

## Workflow

### 1. Understand the Input

Identify the input format and extract the algorithm logic:

**Natural language description:**
- Example: "Sort an array using bubble sort"
- Extract: Algorithm name, input/output, basic steps

**Structured pseudocode:**
- Example: "FOR i FROM 0 TO n-1 DO..."
- Parse: Control structures, data operations, logic flow

**Algorithm specification:**
- Example: "Precondition: array is non-empty. Postcondition: array is sorted"
- Identify: Constraints, requirements, expected behavior

**Mixed format:**
- Combine natural language with pseudocode keywords
- Extract both high-level intent and specific logic

### 2. Analyze Algorithm Structure

Break down the algorithm into components:

1. **Identify data structures:** Arrays, dictionaries, sets, queues, stacks, trees, graphs
2. **Identify control flow:** Loops (for, while), conditionals (if/else), recursion
3. **Identify operations:** Sorting, searching, insertion, deletion, traversal
4. **Identify edge cases:** Empty input, single element, duplicates, boundaries
5. **Identify complexity:** Time and space complexity considerations

### 3. Map to Python Constructs

Use [references/pseudocode-patterns.md](references/pseudocode-patterns.md) for common mappings:

**Control structures:**
- IF/ELSE → `if/elif/else`
- FOR loops → `for i in range()` or `for item in collection`
- WHILE loops → `while condition:`
- REPEAT-UNTIL → `while True:` with `break`

**Data structures:**
- Arrays → `list`
- Hash maps → `dict`
- Sets → `set`
- Stacks → `list` with `append()`/`pop()`
- Queues → `collections.deque`
- Priority queues → `heapq`

**Common operations:**
- Swap → `a, b = b, a`
- Min/Max → `min()`, `max()`
- Sort → `sorted()` or `list.sort()`
- Search → `in` operator, `list.index()`, or binary search

### 4. Generate Python Code

Follow this structure using [assets/template.py](assets/template.py) as a base:

**Module header:**
```python
#!/usr/bin/env python3
"""
Brief description of what this module does.

Implements [algorithm name] with [key features].
"""

from typing import List, Dict, Optional, Tuple, Set, Any
```

**Main function:**
```python
def algorithm_name(param1: type1, param2: type2) -> return_type:
    """Brief description.

    Detailed explanation of the algorithm, including approach and complexity.

    Args:
        param1: Description with constraints
        param2: Description with constraints

    Returns:
        Description of return value

    Raises:
        ValueError: When input is invalid
        TypeError: When input type is wrong

    Examples:
        >>> algorithm_name([3, 1, 2])
        [1, 2, 3]
    """
    # Input validation
    if not param1:
        raise ValueError("param1 cannot be empty")

    # Main algorithm implementation
    # Use clear variable names and comments for complex logic
    result = implementation_here

    return result
```

**Helper functions:**
- Extract complex logic into separate functions
- Each function should have a single responsibility
- Include type hints and docstrings

**Test cases:**
```python
def test_algorithm_name():
    """Test algorithm_name with various inputs."""
    # Test 1: Normal case
    assert algorithm_name([3, 1, 2]) == [1, 2, 3]

    # Test 2: Edge case - empty
    try:
        algorithm_name([])
        assert False, "Should raise ValueError"
    except ValueError:
        pass

    # Test 3: Edge case - single element
    assert algorithm_name([1]) == [1]

    # Test 4: Edge case - duplicates
    assert algorithm_name([2, 1, 2]) == [1, 2, 2]

    # Test 5: Edge case - already sorted
    assert algorithm_name([1, 2, 3]) == [1, 2, 3]

    print("✓ All tests passed!")
```

**Main block:**
```python
if __name__ == "__main__":
    # Run tests
    test_algorithm_name()

    # Example usage
    example_input = [3, 1, 4, 1, 5, 9, 2, 6]
    result = algorithm_name(example_input)
    print(f"Input: {example_input}")
    print(f"Output: {result}")
```

### 5. Apply Python Idioms

Consult [references/python-idioms.md](references/python-idioms.md) for best practices:

**Use list comprehensions:**
```python
# Instead of loops
result = [transform(x) for x in items if condition(x)]
```

**Use built-in functions:**
```python
# Instead of manual loops
total = sum(items)
maximum = max(items)
```

**Use enumerate and zip:**
```python
for i, item in enumerate(items):
    process(i, item)

for a, b in zip(list1, list2):
    process(a, b)
```

**Use appropriate data structures:**
- `collections.defaultdict` for counting/grouping
- `collections.Counter` for frequency counting
- `collections.deque` for queues
- `heapq` for priority queues

### 6. Add Error Handling

Include appropriate error handling:

```python
def function(param):
    """Function with error handling."""
    # Validate input
    if param is None:
        raise ValueError("param cannot be None")

    if not isinstance(param, expected_type):
        raise TypeError(f"Expected {expected_type}, got {type(param)}")

    # Check constraints
    if param < 0:
        raise ValueError("param must be non-negative")

    # Implementation
    try:
        result = risky_operation(param)
    except SpecificError as e:
        # Handle or re-raise with context
        raise RuntimeError(f"Operation failed: {e}") from e

    return result
```

### 7. Create Comprehensive Tests

Generate test cases covering:

1. **Normal cases:** Typical inputs with expected outputs
2. **Edge cases:**
   - Empty input ([], "", None)
   - Single element
   - Two elements
   - Large input
3. **Boundary conditions:**
   - Minimum/maximum values
   - First/last elements
4. **Special cases:**
   - Duplicates
   - Negative numbers
   - Zero
   - Already sorted/processed
5. **Error cases:**
   - Invalid input types
   - Out-of-range values
   - Constraint violations

### 8. Provide Mapping Summary

After generating code, provide a summary:

```
Pseudocode to Python Mapping Summary:
======================================

Algorithm: [Name]
Complexity: Time O(...), Space O(...)

Key Mappings:
1. FOR i FROM 1 TO n → for i in range(1, n + 1)
2. ARRAY[n] → list of size n
3. IF condition THEN → if condition:
4. SWAP(a, b) → a, b = b, a

Data Structures Used:
- Input: List[int]
- Auxiliary: Dict[str, int] for tracking

Functions Generated:
- main_function(): Main algorithm implementation
- helper_function(): Helper for [specific task]

Test Cases: 5 tests covering normal and edge cases
```

## Common Patterns

### Pattern 1: Simple Algorithm Translation

User provides clear pseudocode:
```
FOR i FROM 0 TO n-1
    FOR j FROM 0 TO n-i-1
        IF array[j] > array[j+1]
            SWAP array[j] and array[j+1]
```

1. Identify: Bubble sort with nested loops
2. Map: FOR → `for`, SWAP → tuple unpacking
3. Generate: Complete function with type hints
4. Add: Input validation and tests
5. Provide: Mapping summary

### Pattern 2: Natural Language Description

User describes algorithm in English:
"Create a function that finds the longest common subsequence of two strings"

1. Understand: LCS problem, dynamic programming
2. Design: 2D DP table approach
3. Implement: DP solution with proper structure
4. Test: Multiple test cases including edge cases
5. Document: Explain approach in docstring

### Pattern 3: Algorithm Specification

User provides formal specification:
"Precondition: Binary tree is not empty. Find the lowest common ancestor of two nodes."

1. Parse: Constraints and requirements
2. Choose: Appropriate algorithm (recursive traversal)
3. Implement: With precondition checks
4. Validate: Test with various tree structures
5. Document: Complexity and approach

### Pattern 4: Class-Based Design

User describes object-oriented algorithm:
"Implement a stack with min() operation in O(1)"

1. Design: Class structure with required methods
2. Implement: Using auxiliary stack pattern
3. Add: `__init__`, `push`, `pop`, `min`, `is_empty`
4. Test: Class methods with various scenarios
5. Document: Class and method docstrings

## Important Notes

### Code Quality Standards

- **Type hints:** Always include for parameters and return values
- **Docstrings:** Google-style for all functions and classes
- **Error handling:** Validate inputs and handle edge cases
- **Testing:** Minimum 3-5 test cases covering normal and edge cases
- **Comments:** Explain complex logic, not obvious code
- **Naming:** Use descriptive names following PEP 8

### Python Version

- Target Python 3.7+ for compatibility
- Use modern features: f-strings, type hints, dataclasses
- Avoid deprecated features

### Performance Considerations

- Use built-in functions when possible (faster)
- Choose appropriate data structures
- Consider time/space complexity
- Avoid premature optimization
- Document complexity in docstrings

### When to Use Helper Functions

Extract helper functions when:
- Logic is complex or repeated
- Function exceeds ~50 lines
- Separate concern improves clarity
- Testing individual components is beneficial

### Testing Philosophy

- Tests should be simple and readable
- Use descriptive test names
- Test one thing per test case
- Include assertion messages for clarity
- Run tests in `if __name__ == "__main__"` block

## Resources

- **[references/pseudocode-patterns.md](references/pseudocode-patterns.md):** Common pseudocode to Python mappings
- **[references/python-idioms.md](references/python-idioms.md):** Python best practices and idioms
- **[assets/template.py](assets/template.py):** Python script template structure
