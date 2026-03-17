---
name: semantic-bug-detector
description: "Detect semantic-level bugs by analyzing whether code behavior matches its intended purpose inferred from function/variable names, comments, docstrings, and documentation. Use when users need to: (1) Find logic errors where implementation contradicts stated intent, (2) Identify off-by-one errors and boundary mismatches, (3) Detect inverted logic or wrong operators, (4) Catch missing edge case handling, (5) Verify code matches its documentation. Highlights mismatches between intent and implementation across multiple programming languages."
---

# Semantic Bug Detector

Detect bugs where code behavior doesn't match its intended purpose.

## Overview

This skill analyzes code to find semantic bugs—errors where the implementation contradicts the intent expressed through names, comments, and documentation. Unlike syntax errors or type errors, semantic bugs are logically valid code that does the wrong thing.

## How to Use

Provide code with any of:
1. **Function/variable names** that express intent
2. **Comments** describing what code should do
3. **Docstrings** specifying behavior
4. **Documentation** stating requirements

The skill will:
- Infer intended behavior from these sources
- Analyze actual implementation
- Identify mismatches
- Report semantic bugs with explanations

## Detection Workflow

### Step 1: Extract Intent

Gather intent signals from multiple sources:

**Names**: `is_even`, `get_last_n_elements`, `calculate_average`
- Infer expected behavior from naming conventions
- Identify predicates (is_, has_, can_)
- Recognize operations (get_, set_, calculate_)

**Comments**: `// Returns first n elements`, `# Check if x is positive`
- Parse inline comments
- Extract stated purpose
- Identify boundary specifications

**Docstrings**:
```python
"""Calculate the average of a list of numbers.
Returns the sum divided by the count."""
```
- Parse structured documentation
- Extract preconditions and postconditions
- Identify range specifications

### Step 2: Analyze Implementation

Examine actual code behavior:

**Control flow**: Conditions, loops, branches
**Operations**: Arithmetic, logical, comparison operators
**Boundaries**: Array indices, range limits
**Edge cases**: Empty input, null values, zero divisors

### Step 3: Compare Intent vs Implementation

Check for common mismatches:

**Off-by-one errors**: Using `n+1` when should use `n`
**Inverted logic**: Returning opposite boolean value
**Wrong operator**: Using `*` when should use `/`
**Boundary errors**: Inclusive when should be exclusive
**Missing checks**: Not handling empty/null input

### Step 4: Report Findings

For each bug found, provide:
- **Location**: Function/line where bug occurs
- **Intent**: What the code should do
- **Actual**: What the code actually does
- **Bug type**: Category of semantic error
- **Fix**: Suggested correction

## Example: Off-by-One Error

**Code**:
```python
def get_last_n_elements(arr, n):
    """Returns the last n elements from the array."""
    return arr[-n-1:]
```

**Analysis**:

1. **Intent from name**: "get_last_n_elements" → should return exactly n elements
2. **Intent from docstring**: "Returns the last n elements" → confirms n elements
3. **Actual behavior**: `arr[-n-1:]` returns n+1 elements
4. **Mismatch**: Returns n+1 instead of n

**Report**:
```
BUG: Off-by-one error in get_last_n_elements

Location: Line 3, return statement
Intent: Return the last n elements (from name and docstring)
Actual: Returns the last n+1 elements
Bug Type: Off-by-one error
Severity: High

Explanation:
The slice arr[-n-1:] starts at index -(n+1), which includes
one extra element. Should use arr[-n:] to get exactly n elements.

Fix:
return arr[-n:]
```

## Example: Inverted Logic

**Code**:
```python
def is_even(x):
    """Check if x is even."""
    return x % 2 == 1
```

**Analysis**:

1. **Intent from name**: "is_even" → should return True for even numbers
2. **Intent from docstring**: "Check if x is even" → confirms even check
3. **Actual behavior**: `x % 2 == 1` returns True for odd numbers
4. **Mismatch**: Logic is inverted

**Report**:
```
BUG: Inverted logic in is_even

Location: Line 3, return statement
Intent: Return True when x is even (from name and docstring)
Actual: Returns True when x is odd
Bug Type: Inverted boolean logic
Severity: High

Explanation:
x % 2 == 1 is True for odd numbers, not even numbers.
The condition is inverted from the stated intent.

Fix:
return x % 2 == 0
```

## Example: Boundary Mismatch

**Code**:
```python
def in_range(x, start, end):
    """Check if x is in range [start, end)."""
    return start <= x <= end
```

**Analysis**:

1. **Intent from docstring**: "[start, end)" → half-open interval, excludes end
2. **Actual behavior**: `start <= x <= end` includes end
3. **Mismatch**: Uses inclusive end when should be exclusive

**Report**:
```
BUG: Boundary mismatch in in_range

Location: Line 3, return statement
Intent: Check if x in [start, end) - half-open interval (from docstring)
Actual: Checks if x in [start, end] - closed interval
Bug Type: Boundary error (inclusive vs exclusive)
Severity: Medium

Explanation:
The notation [start, end) means start is included but end is excluded.
The condition start <= x <= end includes end, violating the spec.

Fix:
return start <= x < end
```

## Example: Wrong Operator

**Code**:
```python
def calculate_average(numbers):
    """Calculate the average of a list of numbers."""
    return sum(numbers) * len(numbers)
```

**Analysis**:

1. **Intent from name**: "calculate_average" → should compute mean
2. **Intent from docstring**: "Calculate the average" → confirms mean calculation
3. **Actual behavior**: Multiplies sum by count instead of dividing
4. **Mismatch**: Wrong arithmetic operator

**Report**:
```
BUG: Wrong operator in calculate_average

Location: Line 3, return statement
Intent: Calculate average (sum / count) from name and docstring
Actual: Calculates sum * count
Bug Type: Wrong arithmetic operator
Severity: High

Explanation:
Average is calculated by dividing sum by count, not multiplying.
Using * instead of / produces incorrect result.

Fix:
return sum(numbers) / len(numbers)
```

## Example: Missing Edge Case

**Code**:
```python
def find_max(numbers):
    """Find the maximum number in the list."""
    max_val = numbers[0]
    for num in numbers[1:]:
        if num > max_val:
            max_val = num
    return max_val
```

**Analysis**:

1. **Intent from name**: "find_max" → should find maximum
2. **Intent from docstring**: "Find the maximum number in the list"
3. **Actual behavior**: Crashes on empty list (IndexError)
4. **Mismatch**: Doesn't handle empty input

**Report**:
```
BUG: Missing edge case handling in find_max

Location: Line 3, accessing numbers[0]
Intent: Find maximum number in list (from name and docstring)
Actual: Crashes with IndexError when list is empty
Bug Type: Missing edge case (empty input)
Severity: High

Explanation:
The function assumes the list is non-empty by accessing numbers[0]
without checking. This causes a crash on empty input.

Fix:
if not numbers:
    raise ValueError("Cannot find max of empty list")
max_val = numbers[0]
...
```

## Common Bug Categories

### Off-by-One Errors

**Indicators**: "first n", "last n", "range", "iterate"
**Bugs**: Using `n+1` instead of `n`, `<=` instead of `<`
**See**: [bug_patterns.md](references/bug_patterns.md#off-by-one-errors)

### Inverted Logic

**Indicators**: "is_", "has_", "can_", boolean predicates
**Bugs**: Returning opposite value, wrong comparison
**See**: [bug_patterns.md](references/bug_patterns.md#inverted-logic)

### Boundary Mismatches

**Indicators**: "[a, b]", "[a, b)", range specifications
**Bugs**: Inclusive when should be exclusive
**See**: [bug_patterns.md](references/bug_patterns.md#boundary-mismatches)

### Wrong Operator

**Indicators**: "sum", "product", "average", "ratio"
**Bugs**: Using `*` instead of `/`, `or` instead of `and`
**See**: [bug_patterns.md](references/bug_patterns.md#wrong-operator)

### Missing Edge Cases

**Indicators**: "process", "find", "calculate"
**Bugs**: Not handling empty/null input, division by zero
**See**: [bug_patterns.md](references/bug_patterns.md#missing-edge-cases)

## Detection Strategies

### Strategy 1: Name-Behavior Analysis

1. Parse function/variable name
2. Infer expected behavior from naming conventions
3. Analyze implementation
4. Flag if behavior contradicts name

**Example**: `is_even` should return `True` for even numbers

### Strategy 2: Comment-Code Verification

1. Extract comments and docstrings
2. Parse stated intent
3. Verify implementation matches
4. Report discrepancies

**Example**: Comment says "first n elements" but code returns `n+1`

### Strategy 3: Boundary Checking

1. Identify range specifications in docs
2. Check implementation boundaries
3. Verify inclusive/exclusive semantics

**Example**: Doc says "[start, end)" but code uses `<=` for end

### Strategy 4: Operator Validation

1. Identify operation from name/docs
2. Verify correct operator used
3. Check initialization values

**Example**: `calculate_average` should use `/` not `*`

### Strategy 5: Edge Case Coverage

1. Identify potential edge cases
2. Check if code handles them
3. Flag missing checks

**Example**: Function processing list should handle empty list

## Multi-Language Support

The skill works across languages by focusing on semantic patterns:

**Python**: Docstrings, naming conventions, type hints
**JavaScript/TypeScript**: JSDoc, naming, type annotations
**Java**: Javadoc, naming conventions, method signatures
**C/C++**: Doxygen comments, naming, function signatures
**Go**: Doc comments, naming conventions
**Rust**: Doc comments, naming, type system

Language-specific syntax is handled, but detection focuses on universal semantic patterns.

## Report Format

For each bug, provide:

```
BUG: <Bug type> in <function/location>

Location: <File:line or function name>
Intent: <What code should do based on names/docs>
Actual: <What code actually does>
Bug Type: <Category of semantic error>
Severity: <High/Medium/Low>

Explanation:
<Detailed explanation of the mismatch>

Fix:
<Suggested code correction>
```

## References

Detailed bug pattern catalog:

- **[bug_patterns.md](references/bug_patterns.md)**: Comprehensive catalog of semantic bug patterns with examples

Load this reference when:
- Need detailed examples of specific bug types
- Working with unfamiliar bug patterns
- Want to see more language-specific examples

## Tips

1. **Check names first**: Function/variable names are strong intent signals
2. **Trust documentation**: Docstrings usually state correct behavior
3. **Look for contradictions**: Mismatch between name and implementation is red flag
4. **Verify boundaries**: Range specifications are common source of bugs
5. **Consider edge cases**: Empty/null input often reveals bugs
6. **Check operators**: Arithmetic and logical operators are frequently wrong
7. **Test predicates**: Boolean functions should match their names
8. **Validate loops**: Loop boundaries are prone to off-by-one errors
