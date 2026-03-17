---
name: bug-to-patch-generator
description: Generate code fixes and patches from bug reports, failing test cases, error messages, and stack traces. Use this skill when debugging code, fixing test failures, addressing GitHub issues, resolving runtime errors, or patching security vulnerabilities. Analyzes the bug context, identifies root causes, and generates precise code patches with explanations and validation steps.
---

# Bug-to-Patch Generator

Automatically generate code fixes from bug reports, failing tests, error messages, and stack traces. Analyzes bug context, identifies root causes, and produces verified patches.

## Core Capabilities

### 1. Bug Analysis

Understand bugs from multiple sources:
- **Failing test cases** - Analyze test failures and expected vs actual behavior
- **Error messages** - Parse exceptions, stack traces, and error logs
- **Bug reports** - Process issue descriptions, reproduction steps, and screenshots
- **Crash dumps** - Interpret segmentation faults, core dumps, and memory errors
- **Runtime errors** - Handle assertion failures, type errors, and logic bugs

### 2. Root Cause Identification

Determine the underlying issue:
- Trace error back to source
- Identify incorrect logic or assumptions
- Find missing validation or edge cases
- Detect off-by-one errors and boundary issues
- Recognize concurrency problems
- Spot resource leaks and memory issues

### 3. Patch Generation

Create targeted fixes:
- Minimal, focused changes
- Preserve existing functionality
- Follow code style and patterns
- Include safety checks where needed
- Add comments explaining the fix
- Suggest related improvements

### 4. Patch Validation

Ensure fix correctness:
- Verify fix addresses the bug
- Check for regression risks
- Suggest validation tests
- Recommend manual verification steps
- Consider edge cases and side effects

## Bug-to-Patch Workflow

### Step 1: Gather Bug Context

Collect all relevant information:

**From failing tests:**
```python
FAILED tests/test_calculator.py::test_divide - ZeroDivisionError: division by zero

def test_divide():
    result = divide(10, 0)
    assert result == None  # Expected to return None for division by zero
```

**From error messages:**
```
Traceback (most recent call last):
  File "app.py", line 42, in process_data
    result = data[index]
IndexError: list index out of range
```

**From bug reports:**
```
Title: App crashes when processing empty file
Steps to reproduce:
1. Upload empty CSV file
2. Click "Process"
3. App crashes with NoneType error

Expected: Error message shown to user
Actual: Application crashes
```

### Step 2: Analyze the Bug

Identify the root cause:

**Questions to answer:**
- What is the exact error?
- Where does it occur? (file, line, function)
- What are the preconditions?
- What input triggers it?
- What was expected vs what happened?
- Is it a logic error, validation issue, or edge case?

**Common bug patterns:**
- Missing null/None checks
- Off-by-one errors
- Incorrect boundary conditions
- Missing error handling
- Wrong operator or comparison
- Race conditions
- Resource leaks
- Type mismatches

### Step 3: Locate Relevant Code

Find the code that needs fixing:

```python
# Read the source file
def divide(a, b):
    return a / b  # Bug: No check for b == 0
```

**Context needed:**
- The buggy function/method
- Related functions it calls
- Caller functions
- Test cases
- Similar correct implementations

### Step 4: Generate the Patch

Create minimal, focused fix:

**Patch format:**
```python
# Before (buggy code)
def divide(a, b):
    return a / b

# After (fixed code)
def divide(a, b):
    if b == 0:
        return None  # or raise ValueError("Cannot divide by zero")
    return a / b
```

**Patch components:**
1. Clear before/after comparison
2. Explanation of the fix
3. Why this approach was chosen
4. Potential alternatives
5. Edge cases now handled

### Step 5: Validate the Fix

Ensure correctness:

**Validation steps:**
```python
# Test that should now pass
def test_divide_by_zero():
    assert divide(10, 0) is None

# Additional tests for edge cases
def test_divide_normal():
    assert divide(10, 2) == 5

def test_divide_negative():
    assert divide(-10, 2) == -5
```

**Verification checklist:**
- [ ] Original test now passes
- [ ] Existing tests still pass (no regression)
- [ ] Edge cases handled
- [ ] Error messages are clear
- [ ] Performance not degraded

## Bug Fix Patterns

### Pattern 1: Missing Null/None Check

**Bug report:**
```
AttributeError: 'NoneType' object has no attribute 'upper'
```

**Buggy code:**
```python
def format_name(name):
    return name.upper()
```

**Root cause:** No validation for None input

**Patch:**
```python
def format_name(name):
    if name is None:
        return ""  # or raise ValueError("Name cannot be None")
    return name.upper()
```

**Explanation:**
- Added None check before accessing string method
- Returns empty string for None (or could raise exception)
- Prevents AttributeError

**Alternative approaches:**
```python
# Option 1: Raise exception
def format_name(name):
    if name is None:
        raise ValueError("Name cannot be None")
    return name.upper()

# Option 2: Use default parameter
def format_name(name=None):
    return (name or "").upper()

# Option 3: Type hint and early return
def format_name(name: str | None) -> str:
    if not name:
        return ""
    return name.upper()
```

### Pattern 2: Off-by-One Error

**Bug report:**
```
IndexError: list index out of range
```

**Failing test:**
```python
def test_get_last_element():
    arr = [1, 2, 3]
    assert get_element(arr, 3) == 3  # Want last element
```

**Buggy code:**
```python
def get_element(arr, index):
    return arr[index]  # index 3 is out of bounds for length 3
```

**Root cause:** Confusion between length and index (0-based)

**Patch:**
```python
def get_element(arr, index):
    if index < 0 or index >= len(arr):
        raise IndexError(f"Index {index} out of range for array of length {len(arr)}")
    return arr[index]
```

**Explanation:**
- Added bounds checking
- Clear error message
- Handles negative indices too

**Better alternative:**
```python
def get_element(arr, index):
    """Get element at index. Supports negative indexing."""
    try:
        return arr[index]
    except IndexError:
        raise IndexError(f"Index {index} out of range for array of length {len(arr)}")
```

### Pattern 3: Missing Error Handling

**Bug report:**
```
Application crashes when file doesn't exist
FileNotFoundError: [Errno 2] No such file or directory: 'config.json'
```

**Buggy code:**
```python
def load_config():
    with open('config.json') as f:
        return json.load(f)
```

**Root cause:** No handling for missing file

**Patch:**
```python
def load_config():
    try:
        with open('config.json') as f:
            return json.load(f)
    except FileNotFoundError:
        # Return default config
        return {"debug": False, "port": 8080}
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in config.json: {e}")
```

**Explanation:**
- Added FileNotFoundError handling with sensible default
- Also handles JSON parsing errors
- Provides clear error message for invalid JSON

**Alternative with logging:**
```python
import logging

def load_config():
    try:
        with open('config.json') as f:
            return json.load(f)
    except FileNotFoundError:
        logging.warning("config.json not found, using defaults")
        return {"debug": False, "port": 8080}
    except json.JSONDecodeError as e:
        logging.error(f"Invalid JSON in config.json: {e}")
        raise
```

### Pattern 4: Incorrect Logic/Condition

**Failing test:**
```python
def test_is_even():
    assert is_even(0) == True  # FAILS
    assert is_even(2) == True
    assert is_even(3) == False
```

**Buggy code:**
```python
def is_even(n):
    if n % 2:  # Bug: 0 % 2 == 0 which is falsy
        return False
    return True
```

**Root cause:** Incorrect boolean logic (0 is falsy)

**Patch:**
```python
def is_even(n):
    return n % 2 == 0  # Explicitly check equality
```

**Explanation:**
- Changed from implicit truthiness to explicit comparison
- Handles 0 correctly (0 % 2 == 0 is True)
- More readable and explicit

### Pattern 5: Race Condition

**Bug report:**
```
Intermittent test failure in multithreaded code
AssertionError: Expected counter=1000, got counter=987
```

**Buggy code:**
```python
class Counter:
    def __init__(self):
        self.count = 0

    def increment(self):
        self.count += 1  # Not atomic!
```

**Root cause:** Non-atomic operation in concurrent context

**Patch (Python):**
```python
import threading

class Counter:
    def __init__(self):
        self.count = 0
        self.lock = threading.Lock()

    def increment(self):
        with self.lock:
            self.count += 1
```

**Alternative using atomic operations:**
```python
from threading import Lock
from threading import local

class Counter:
    def __init__(self):
        self.count = 0
        self._lock = Lock()

    def increment(self):
        with self._lock:
            self.count += 1

# Or use atomic integer
from threading import Lock

class Counter:
    def __init__(self):
        from queue import Queue
        self._queue = Queue()
        self.count = 0

# Better: use threading.local or atomic types
import threading

class AtomicCounter:
    def __init__(self):
        self._value = 0
        self._lock = threading.Lock()

    def increment(self):
        with self._lock:
            self._value += 1
            return self._value

    @property
    def value(self):
        with self._lock:
            return self._value
```

### Pattern 6: Memory Leak

**Bug report:**
```
Application memory usage grows unbounded
Memory increases by ~100MB every hour
```

**Buggy code:**
```python
class Cache:
    def __init__(self):
        self.data = {}

    def store(self, key, value):
        self.data[key] = value  # Never clears old entries

    def get(self, key):
        return self.data.get(key)
```

**Root cause:** Unbounded cache growth

**Patch:**
```python
from collections import OrderedDict

class Cache:
    def __init__(self, max_size=1000):
        self.data = OrderedDict()
        self.max_size = max_size

    def store(self, key, value):
        if key in self.data:
            # Move to end (most recently used)
            self.data.move_to_end(key)
        else:
            self.data[key] = value

        # Evict oldest if over limit
        if len(self.data) > self.max_size:
            self.data.popitem(last=False)

    def get(self, key):
        if key in self.data:
            # Move to end (most recently used)
            self.data.move_to_end(key)
            return self.data[key]
        return None
```

**Explanation:**
- Implemented LRU cache with size limit
- Uses OrderedDict for efficient LRU tracking
- Automatically evicts oldest entries

### Pattern 7: Incorrect Exception Type

**Failing test:**
```python
def test_invalid_input():
    with pytest.raises(ValueError):
        process(-1)  # FAILS: raises TypeError instead
```

**Buggy code:**
```python
def process(value):
    if value < 0:
        raise TypeError("Value must be non-negative")  # Wrong exception type
    return value * 2
```

**Root cause:** Using TypeError instead of ValueError

**Patch:**
```python
def process(value):
    if value < 0:
        raise ValueError("Value must be non-negative")  # Correct exception
    return value * 2
```

**Explanation:**
- ValueError is for invalid values
- TypeError is for invalid types
- Changed to appropriate exception type

## Patch Presentation Format

### Structured Patch Template

```markdown
## Bug Fix: [Short description]

### Bug Details
- **Location:** [file:line]
- **Error:** [error message or test failure]
- **Root Cause:** [explanation of the underlying issue]
- **Severity:** [Critical/High/Medium/Low]

### Analysis
[Detailed explanation of why the bug occurs]

### Proposed Fix

#### Changes
```[language]
# File: [filename]

# Before (lines X-Y)
[buggy code]

# After
[fixed code]
```

#### Explanation
[Why this fix works and what it does]

#### Alternative Approaches
1. [Alternative 1]: [pros/cons]
2. [Alternative 2]: [pros/cons]

### Validation

#### Tests to Add/Modify
```[language]
[test code that validates the fix]
```

#### Manual Verification Steps
1. [Step 1]
2. [Step 2]
3. [Expected result]

#### Regression Checks
- [ ] Existing tests still pass
- [ ] No performance degradation
- [ ] No new edge cases introduced

### Related Issues
- Consider also fixing: [related code that may have same issue]
- Similar patterns in: [other files]
```

### Example Complete Patch

```markdown
## Bug Fix: Handle division by zero in calculator

### Bug Details
- **Location:** src/calculator.py:15
- **Error:** `ZeroDivisionError: division by zero`
- **Root Cause:** Missing validation for zero divisor
- **Severity:** High (causes crash)

### Analysis
The `divide` function performs division without checking if the divisor is zero.
When called with b=0, Python raises ZeroDivisionError, crashing the application.
The function should either return None, return infinity, or raise a custom exception
with a clear message.

### Proposed Fix

#### Changes
```python
# File: src/calculator.py

# Before (lines 14-15)
def divide(a, b):
    return a / b

# After
def divide(a, b):
    """Divide a by b. Returns None if b is zero."""
    if b == 0:
        return None
    return a / b
```

#### Explanation
Added a check for zero divisor before performing division. Returns None to indicate
invalid operation, which is consistent with other error cases in the codebase.
This prevents the uncaught exception and allows callers to handle the None return.

#### Alternative Approaches
1. **Raise custom exception**: `raise ValueError("Cannot divide by zero")`
   - Pros: Explicit error, forces caller to handle
   - Cons: More verbose for callers

2. **Return float('inf')**: Mathematical infinity
   - Pros: Mathematically correct for positive/negative infinity
   - Cons: May cause issues in downstream calculations

3. **Return 0**: Default to zero
   - Pros: Simple
   - Cons: Mathematically incorrect, hides errors

**Chosen approach: Return None** because it's consistent with the existing codebase
pattern of returning None for invalid operations.

### Validation

#### Tests to Add/Modify
```python
# tests/test_calculator.py

def test_divide_by_zero():
    """Test that division by zero returns None."""
    assert divide(10, 0) is None
    assert divide(0, 0) is None
    assert divide(-5, 0) is None

def test_divide_normal():
    """Test normal division still works."""
    assert divide(10, 2) == 5
    assert divide(10, 3) == pytest.approx(3.333, rel=0.001)
```

#### Manual Verification Steps
1. Run the failing test: `pytest tests/test_calculator.py::test_divide`
2. Verify it now passes
3. Run full test suite: `pytest`
4. Test in REPL: `divide(10, 0)` should return `None`

#### Regression Checks
- [x] All existing calculator tests pass
- [x] No performance impact (simple check)
- [x] Consistent with other error handling in codebase

### Related Issues
- Consider also checking `modulo` function for same issue
- `power` function may have similar edge cases (0^0, 0^-1)
```

## Best Practices

1. **Minimal changes** - Fix only what's broken, don't refactor unnecessarily
2. **Preserve behavior** - Ensure fix doesn't break working functionality
3. **Clear explanations** - Explain why the bug occurred and how fix addresses it
4. **Test thoroughly** - Add tests that would have caught the bug
5. **Consider alternatives** - Present multiple fix options when applicable
6. **Document the fix** - Add comments explaining non-obvious fixes
7. **Check for similar bugs** - Look for the same pattern elsewhere
8. **Validate edge cases** - Ensure fix handles all scenarios
9. **Follow code style** - Match existing patterns and conventions
10. **Suggest improvements** - Note related technical debt if relevant

## Common Pitfalls to Avoid

### Pitfall 1: Over-fixing
```python
# Bad: Refactoring unrelated code
def divide(a, b):
    # Also renamed parameters and restructured
    if divisor == 0:
        return None
    quotient = dividend / divisor
    return quotient

# Good: Minimal fix
def divide(a, b):
    if b == 0:
        return None
    return a / b
```

### Pitfall 2: Introducing New Bugs
```python
# Bad: Fix creates new issue
def get_first(arr):
    if len(arr) == 0:
        return None
    return arr[1]  # Bug! Should be arr[0]

# Good: Correct fix
def get_first(arr):
    if len(arr) == 0:
        return None
    return arr[0]
```

### Pitfall 3: Hiding the Real Problem
```python
# Bad: Silencing exceptions
def load_data():
    try:
        return dangerous_operation()
    except Exception:
        return None  # Hides the actual error!

# Good: Specific exception handling
def load_data():
    try:
        return dangerous_operation()
    except FileNotFoundError:
        return None  # Expected case
    # Let other exceptions propagate
```

## Language-Specific Fix Patterns

For language-specific bug patterns and fixes:

- **Python**: See [references/python_bugs.md](references/python_bugs.md)
- **JavaScript**: See [references/javascript_bugs.md](references/javascript_bugs.md)
- **Java**: See [references/java_bugs.md](references/java_bugs.md)
- **C/C++**: See [references/c_cpp_bugs.md](references/c_cpp_bugs.md)
