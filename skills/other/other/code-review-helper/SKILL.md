---
name: code-review-helper
description: Assists with code review tasks including checking style, finding bugs, suggesting improvements. Use when reviewing code, analyzing pull requests, or when user mentions code review, PR review, or code quality.
license: MIT
---

# Code Review Helper

Assists with systematic code review including style checking, bug detection, and improvement suggestions.

## When to Use

- Reviewing pull requests
- Analyzing code quality
- Finding potential bugs
- Suggesting code improvements
- Checking style compliance

## Prerequisites

- Access to the code files
- (Optional) Language-specific linters installed

## Review Process

### 1. Quick Scan

Read through the code to understand:
- What it does
- Main components/functions
- Code organization

### 2. Style Check

Check for common style issues:

**Python**:
```bash
# If flake8 installed
flake8 filename.py

# Manual checks
# - Consistent indentation (4 spaces)
# - Descriptive variable names
# - Docstrings for functions
# - No lines > 88 characters (Black standard)
```

**JavaScript**:
```bash
# If eslint installed
npx eslint filename.js

# Manual checks
# - Consistent indentation (2 spaces typical)
# - Const/let instead of var
# - Semicolons consistent
# - CamelCase for variables, PascalCase for classes
```

### 3. Logic Review

Check for common issues:

- **Null/undefined checks**: Are inputs validated?
  ```javascript
  // ❌ Missing check
  function process(data) {
    return data.length; // What if data is null?
  }
  
  // ✓ With check
  function process(data) {
    if (!data) return 0;
    return data.length;
  }
  ```

- **Error handling**: Are exceptions caught?
  ```python
  # ❌ No error handling
  def read_file(path):
      return open(path).read()
  
  # ✓ With error handling
  def read_file(path):
      try:
          return open(path).read()
      except FileNotFoundError:
          print(f"Error: {path} not found")
          return None
  ```

- **Edge cases**: Are boundary conditions handled?
  ```python
  # Check for:
  # - Empty arrays/lists
  # - Zero values
  # - Negative numbers where unexpected
  # - Very large inputs
  ```

### 4. Security Check

Look for common security issues:

- **SQL injection** (if using SQL):
  ```python
  # ❌ Vulnerable
  query = f"SELECT * FROM users WHERE id = {user_id}"
  
  # ✓ Parameterized
  query = "SELECT * FROM users WHERE id = ?"
  cursor.execute(query, (user_id,))
  ```

- **Command injection**:
  ```python
  # ❌ Dangerous
  os.system(f"ls {user_input}")
  
  # ✓ Safe
  import subprocess
  subprocess.run(["ls", user_input])
  ```

- **Hardcoded secrets**:
  ```python
  # ❌ Exposed
  API_KEY = "sk-abc123..."
  
  # ✓ From environment
  API_KEY = os.environ.get("API_KEY")
  ```

### 5. Performance Review

Identify potential performance issues:

- **Unnecessary loops**:
  ```python
  # ❌ O(n²)
  for i in range(len(arr)):
      if arr[i] in arr:  # Searches entire array each time
          ...
  
  # ✓ O(n)
  arr_set = set(arr)
  for item in arr:
      if item in arr_set:
          ...
  ```

- **Resource leaks**:
  ```python
  # ❌ File not closed
  file = open("data.txt")
  data = file.read()
  
  # ✓ Properly closed
  with open("data.txt") as file:
      data = file.read()
  ```

### 6. Suggest Improvements

Look for opportunities to improve:

- **Simplification**:
  ```javascript
  // Before
  if (condition) {
    return true;
  } else {
    return false;
  }
  
  // After
  return condition;
  ```

- **Reusability**:
  ```python
  # If similar code repeated, suggest extracting function
  # If hardcoded values repeated, suggest constants
  ```

- **Readability**:
  ```python
  # Before
  if user.type == "A" or user.type == "B" or user.type == "C":
  
  # After
  ADMIN_TYPES = ["A", "B", "C"]
  if user.type in ADMIN_TYPES:
  ```

## Review Checklist

For each file reviewed, check:

- [ ] Style is consistent
- [ ] Variable names are descriptive
- [ ] Functions are documented
- [ ] Edge cases are handled
- [ ] Errors are handled appropriately
- [ ] No security vulnerabilities
- [ ] No obvious performance issues
- [ ] Code is readable and maintainable

## Example Review

**File**: `utils.py`

```python
def calculate(x, y):
    return x / y
```

**Review findings**:

1. **Missing docstring**: Add description of what function does
2. **No type hints**: Add parameter and return types
3. **Division by zero**: Need to handle y=0 case
4. **Vague name**: "calculate" doesn't indicate division

**Suggested improvement**:
```python
def divide(x: float, y: float) -> float:
    """
    Divide x by y.
    
    Args:
        x: Numerator
        y: Denominator
        
    Returns:
        Result of x / y
        
    Raises:
        ValueError: If y is zero
    """
    if y == 0:
        raise ValueError("Cannot divide by zero")
    return x / y
```

## Common Issues by Language

### Python
- Missing docstrings
- No type hints
- Not using `with` for files
- Mutable default arguments
- Catching bare `except`

### JavaScript
- Using `var` instead of `const`/`let`
- Missing `===` (using `==`)
- Not handling promises properly
- Missing error handling in async functions
- Not validating user inputs

### TypeScript
- Using `any` type
- Missing null checks
- Not leveraging type system
- Inconsistent interface usage

### Go
- Not checking errors
- Not closing resources
- Using `panic` unnecessarily
- Not using goroutines safely

## Tips

1. **Be constructive**: Frame suggestions as improvements, not criticisms
2. **Prioritize**: Focus on bugs and security first, style last
3. **Provide examples**: Show how to fix issues
4. **Consider context**: Understand the requirements before suggesting changes
5. **Check tests**: Verify that tests exist and cover edge cases

## Output Format

Structure your review as:

```
## Summary
Brief overview of the changes and overall code quality.

## Critical Issues
- [ ] Security vulnerabilities
- [ ] Bugs that would cause failures
- [ ] Data loss risks

## Important Issues  
- [ ] Performance problems
- [ ] Error handling gaps
- [ ] Missing edge case handling

## Suggestions
- [ ] Style improvements
- [ ] Code simplifications
- [ ] Better naming
- [ ] Additional tests

## Positive Notes
What the code does well.
```
