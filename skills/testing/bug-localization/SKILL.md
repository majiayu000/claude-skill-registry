---
name: bug-localization
description: Identify the precise location of bugs in source code, modules, and systems. Use this skill when debugging applications, investigating test failures, analyzing error reports, tracing runtime issues, or performing root cause analysis. Analyzes stack traces, error messages, failing tests, and code patterns to pinpoint buggy functions, classes, files, or modules with confidence rankings and supporting evidence.
---

# Bug Localization

Precisely identify the location of bugs in source code by analyzing error messages, stack traces, failing tests, and code patterns. Provides ranked suspect locations with confidence scores and evidence.

## Core Capabilities

### 1. Error Analysis

Extract information from error sources:
- **Stack traces** - Parse and analyze call stacks
- **Error messages** - Interpret exception details
- **Failing tests** - Analyze test failures and assertions
- **Crash reports** - Process crash dumps and core files
- **Log messages** - Trace execution through logs
- **Debugger output** - Interpret breakpoint and watch data

### 2. Code Analysis

Examine code for bug indicators:
- **Data flow** - Trace variables and values
- **Control flow** - Analyze execution paths
- **Type mismatches** - Detect type-related issues
- **Null/undefined access** - Find potential null dereferences
- **Boundary violations** - Detect array/buffer overflows
- **Concurrency issues** - Identify race conditions

### 3. Suspect Ranking

Prioritize likely bug locations:
- **Confidence scores** - Rank suspects by likelihood
- **Evidence strength** - Quantify supporting evidence
- **Historical data** - Consider past bug patterns
- **Code complexity** - Factor in cyclomatic complexity
- **Recent changes** - Weigh recent modifications
- **Code churn** - Consider frequently modified code

### 4. Investigation Guidance

Provide actionable next steps:
- **Verification steps** - How to confirm the bug
- **Debugging strategies** - Where to set breakpoints
- **Test cases** - Tests to reproduce the bug
- **Related code** - Other potentially affected areas

## Bug Localization Workflow

### Step 1: Gather Evidence

Collect all available information:

**From stack trace:**
```python
Traceback (most recent call last):
  File "app.py", line 45, in process_order
    total = calculate_total(items)
  File "billing.py", line 23, in calculate_total
    price = item['price'] * item['quantity']
KeyError: 'price'
```

**Extract:**
- Error type: `KeyError`
- Missing key: `'price'`
- Exception location: `billing.py:23`
- Call chain: `app.py:45` → `billing.py:23`
- Function: `calculate_total`
- Context: Processing items dict

**From failing test:**
```python
FAILED tests/test_auth.py::test_login_with_valid_credentials
AssertionError: assert False is True
Expected: User logged in successfully
Actual: Login failed with invalid credentials
```

**Extract:**
- Test file: `tests/test_auth.py`
- Test function: `test_login_with_valid_credentials`
- Failure type: Assertion mismatch
- Expected behavior: Successful login
- Actual behavior: Failed login

### Step 2: Analyze Error Context

Understand what caused the error:

**For KeyError example:**
- **Direct cause**: Accessing non-existent 'price' key
- **Root causes** (hypotheses):
  1. Item dict missing 'price' field
  2. Key name mismatch ('price' vs 'Price')
  3. Item is None or wrong type
  4. Data corruption in item dict

**For login test failure:**
- **Direct cause**: Login returned False
- **Root causes** (hypotheses):
  1. Credential validation logic incorrect
  2. Database query failing
  3. Password hashing mismatch
  4. Session creation failure

### Step 3: Locate Suspect Code

Identify likely buggy locations:

**Primary suspects (KeyError):**
```
1. billing.py:23 (95% confidence)
   - Direct location of exception
   - Line: price = item['price'] * item['quantity']
   - Issue: No validation before dict access

2. app.py:40-45 (70% confidence)
   - Calls calculate_total with items
   - Possible: Items data structure incorrect
   - Need to verify items content

3. Data source (50% confidence)
   - Where items are created/loaded
   - Possible: Missing field in data
   - Check database schema or API response
```

**Code locations to examine:**
```python
# billing.py:20-25 (Primary suspect)
def calculate_total(items):
    total = 0
    for item in items:
        price = item['price'] * item['quantity']  # Line 23 - BUG HERE
        total += price
    return total

# app.py:40-45 (Secondary suspect)
def process_order(order_id):
    order = get_order(order_id)
    items = order.get('items', [])
    total = calculate_total(items)  # Line 45
    return total
```

### Step 4: Rank Suspects

Assign confidence scores:

**Ranking factors:**
- **Stack trace depth** - Closer to exception = higher confidence
- **Error message** - Directly mentioned code = higher
- **Code complexity** - More complex = more likely
- **Recent changes** - Recently modified = higher
- **Test coverage** - Low coverage = higher risk

**Example ranking:**
```
Rank 1: billing.py:23 in calculate_total() - 95%
  Evidence:
  - Direct exception location
  - No null/existence check before dict access
  - Simple fix: Add key validation

Rank 2: app.py:45 in process_order() - 70%
  Evidence:
  - Calls buggy function
  - items might be malformed
  - Check: order.get('items') might return bad data

Rank 3: models.py:78 in get_order() - 50%
  Evidence:
  - Data source for items
  - Possible missing fields in database
  - Check: Database schema and migrations

Rank 4: api.py:112 in create_order() - 30%
  Evidence:
  - Creates order data
  - Might not include all required fields
  - Check: API contract validation
```

### Step 5: Provide Investigation Plan

Guide debugging efforts:

**Immediate actions:**
1. Add validation in `billing.py:23`
2. Add logging before line 23 to inspect `item`
3. Check what `items` contains at `app.py:45`

**Verification steps:**
1. Add print: `print(f"Item: {item}")` before line 23
2. Run failing test again
3. Check if 'price' exists in item dict

**Long-term fixes:**
1. Add schema validation for items
2. Use type hints and static analysis
3. Add integration test for full order flow

## Localization Patterns

### Pattern 1: Stack Trace Analysis

**Error:**
```
Traceback (most recent call last):
  File "main.py", line 100, in run
    result = processor.execute()
  File "processor.py", line 45, in execute
    data = self.transform(input_data)
  File "processor.py", line 78, in transform
    return data.upper()
AttributeError: 'NoneType' object has no attribute 'upper'
```

**Analysis:**
```
Stack trace (bottom to top):
1. processor.py:78 - data.upper() fails (EXCEPTION POINT)
2. processor.py:45 - self.transform(input_data) called
3. main.py:100 - processor.execute() triggered

Primary suspect: processor.py:78
  - Directly referenced in error
  - Calls .upper() on None
  - Confidence: 95%

Secondary suspect: processor.py:45
  - Passes input_data to transform
  - input_data might be None
  - Confidence: 80%

Tertiary suspect: main.py:100
  - Initial call site
  - Processor initialization might be wrong
  - Confidence: 40%
```

**Localization:**
```python
# processor.py:75-80 (PRIMARY SUSPECT - 95%)
def transform(self, data):
    if data is None:  # MISSING CHECK
        return ""
    return data.upper()  # Line 78 - Bug location

# processor.py:43-46 (SECONDARY - 80%)
def execute(self):
    input_data = self.get_input()  # Might return None
    data = self.transform(input_data)  # Line 45
    return self.process(data)

# main.py:98-101 (TERTIARY - 40%)
def run(self):
    processor = Processor(config)
    result = processor.execute()  # Line 100
    return result
```

**Evidence:**
- Direct: `AttributeError` on line 78
- Contextual: `data` is `None`
- Root cause: No null check before `.upper()`

### Pattern 2: Assertion Failure Localization

**Failing test:**
```python
def test_calculate_discount():
    # Given
    price = 100.0
    discount_percent = 20.0

    # When
    result = calculate_discount(price, discount_percent)

    # Then
    assert result == 80.0  # FAILS: result is 120.0
```

**Analysis:**
```
Test expectation: 80.0
Actual result: 120.0
Difference: +40 (opposite direction)

Hypothesis:
- Expected: price - (price * discount / 100) = 100 - 20 = 80
- Actual: price + (price * discount / 100) = 100 + 20 = 120
- Likely bug: Using + instead of -
```

**Localization:**
```python
# utils.py:15-20 (PRIMARY SUSPECT - 98%)
def calculate_discount(price, discount_percent):
    discount_amount = price * (discount_percent / 100)
    # Bug: Should be subtraction, not addition
    return price + discount_amount  # Line 18 - WRONG OPERATOR
    # Should be: return price - discount_amount
```

**Evidence:**
- Symptoms match operator error (+ vs -)
- Result is exactly price + discount (not price - discount)
- High confidence: 98%

### Pattern 3: Boundary Error Localization

**Error:**
```
IndexError: list index out of range
  File "search.py", line 56, in find_median
    median = sorted_list[len(sorted_list) / 2]
```

**Analysis:**
```
Error type: IndexError
Location: search.py:56
Expression: sorted_list[len(sorted_list) / 2]

Issues identified:
1. Division result might be float (Python 3)
2. Index calculation might be off-by-one
3. Empty list not handled

Confidence: 99% - obvious bug
```

**Localization:**
```python
# search.py:52-58 (PRIMARY SUSPECT - 99%)
def find_median(numbers):
    sorted_list = sorted(numbers)

    # BUG 1: len() / 2 returns float in Python 3
    # BUG 2: No empty list check
    # BUG 3: Even-length list not handled
    median = sorted_list[len(sorted_list) / 2]  # Line 56

    return median

# CORRECT VERSION:
def find_median(numbers):
    if not numbers:
        raise ValueError("Cannot find median of empty list")

    sorted_list = sorted(numbers)
    n = len(sorted_list)
    mid = n // 2  # Integer division

    if n % 2 == 0:
        # Even length: average of middle two
        return (sorted_list[mid - 1] + sorted_list[mid]) / 2
    else:
        # Odd length: middle element
        return sorted_list[mid]
```

**Evidence:**
- Error message points to exact line
- Multiple bugs in single line
- Fix requires complete rewrite

### Pattern 4: Logic Error Localization

**Bug report:**
```
Issue: Users are seeing incorrect order totals
Expected: Total = sum of (price * quantity) for each item
Actual: Total is always just the price of the last item

Example:
Item 1: $10 × 2 = $20
Item 2: $15 × 1 = $15
Expected total: $35
Actual total: $15
```

**Analysis:**
```
Pattern: Total equals last item only
Hypothesis: Loop variable overwriting instead of accumulating

Suspects:
1. Total calculation loop (HIGH)
2. Item price calculation (LOW)
3. Database query (LOW)
```

**Localization:**
```python
# orders.py:34-40 (PRIMARY SUSPECT - 90%)
def calculate_order_total(items):
    total = 0
    for item in items:
        item_total = item.price * item.quantity
        total = item_total  # Line 38 - BUG: Should be +=
        # Should be: total += item_total
    return total

# Evidence:
# - total = item_total overwrites instead of adds
# - Result matches last item only
# - Classic accumulation bug
```

**Fix:**
```python
def calculate_order_total(items):
    total = 0
    for item in items:
        item_total = item.price * item.quantity
        total += item_total  # FIXED: Use +=
    return total
```

### Pattern 5: Concurrency Bug Localization

**Bug report:**
```
Issue: Intermittent race condition
Symptom: Counter value incorrect under high load
Expected: counter = 1000 after 1000 increments
Actual: counter = 987 (varies)
```

**Analysis:**
```
Characteristics:
- Non-deterministic (varies each run)
- Happens under concurrent access
- Counter less than expected (lost updates)

Root cause: Race condition in increment operation
```

**Localization:**
```python
# counter.py:15-20 (PRIMARY SUSPECT - 95%)
class Counter:
    def __init__(self):
        self.value = 0

    def increment(self):
        # BUG: Non-atomic read-modify-write
        temp = self.value  # Read
        temp = temp + 1    # Modify
        self.value = temp  # Write
        # Race condition: Another thread can modify between read and write

# Evidence:
# - Symptom matches race condition
# - No synchronization
# - Multiple threads accessing shared state

# FIX:
import threading

class Counter:
    def __init__(self):
        self.value = 0
        self.lock = threading.Lock()

    def increment(self):
        with self.lock:
            self.value += 1  # Atomic under lock
```

## Investigation Strategies

### Strategy 1: Binary Search

For large codebases, narrow down location:

```
1. Identify entry point and exception point
2. Find midpoint in call chain
3. Add logging/breakpoint at midpoint
4. Run to see if bug is before or after
5. Repeat on relevant half
```

### Strategy 2: Data Flow Tracing

Track variable values through execution:

```
1. Identify problematic variable (e.g., None value)
2. Trace backwards to find where it's set
3. Check each assignment point
4. Find where it becomes incorrect
```

**Example:**
```python
# Trace None value backwards
data = transform(input)      # 3. input is None, where from?
input = get_data(source)     # 2. get_data returns None, why?
source = config.get('src')   # 1. config.get returns None - BUG HERE
```

### Strategy 3: Differential Analysis

Compare working vs broken code:

```
1. Find a working version (git history)
2. Identify what changed
3. Focus on changed code
4. Bug likely in recent modifications
```

### Strategy 4: Hypothesis Testing

Form and test hypotheses:

```
1. List possible causes
2. For each, predict what evidence would prove it
3. Gather evidence (logging, debugging)
4. Eliminate hypotheses that don't match
5. Focus on remaining candidates
```

## Confidence Scoring

### High Confidence (80-100%)

Indicators:
- Direct exception location
- Error message mentions specific line
- Simple, obvious bug (typo, wrong operator)
- Reproducible with minimal steps

### Medium Confidence (50-79%)

Indicators:
- In call stack but not exception point
- Indirect evidence (symptoms match)
- Complex logic errors
- Multiple possible causes

### Low Confidence (20-49%)

Indicators:
- Distant from exception
- Weak circumstantial evidence
- Many intervening layers
- Speculative root cause

### Very Low Confidence (<20%)

Indicators:
- No direct connection to error
- Pure speculation
- Many assumptions required
- Better to gather more evidence

## Reporting Format

### Bug Location Report Template

```markdown
## Bug Localization Report

### Summary
[One-line description of the bug]

### Evidence
- Error type: [Exception/Assertion/Logic error]
- Error message: [Full message]
- Location: [File:line where error occurs]
- Test case: [Failing test if applicable]

### Primary Suspect (XX% confidence)
**Location:** [file:line]
**Function:** [function_name]
**Issue:** [Description of suspected bug]
**Evidence:**
- [Evidence item 1]
- [Evidence item 2]

**Code snippet:**
```[language]
[Relevant code with bug location marked]
```

### Secondary Suspects
**Suspect 2 (XX% confidence)**
[Similar format]

**Suspect 3 (XX% confidence)**
[Similar format]

### Investigation Steps
1. [Verification step 1]
2. [Verification step 2]
3. [Debugging step 3]

### Recommended Fix
[Brief description of how to fix]

### Related Code
[Other code that might be affected]
```

### Example Report

```markdown
## Bug Localization Report

### Summary
KeyError when calculating order total due to missing 'price' field in item dict

### Evidence
- Error type: KeyError
- Error message: KeyError: 'price'
- Location: billing.py:23 in calculate_total()
- Call chain: app.py:45 → billing.py:23

### Primary Suspect (95% confidence)
**Location:** billing.py:23
**Function:** calculate_total
**Issue:** No validation before accessing item['price']
**Evidence:**
- Direct exception location
- No null/existence check
- Simple dict access without safety

**Code snippet:**
```python
def calculate_total(items):
    total = 0
    for item in items:
        price = item['price'] * item['quantity']  # ← BUG HERE
        total += price
    return total
```

### Secondary Suspects

**Suspect 2 (70% confidence)**
**Location:** app.py:45
**Function:** process_order
**Issue:** items data might be malformed
**Code:**
```python
items = order.get('items', [])
total = calculate_total(items)  # Passes potentially bad data
```

**Suspect 3 (50% confidence)**
**Location:** models.py:78
**Function:** get_order
**Issue:** Database might be missing 'price' field

### Investigation Steps
1. Add logging: `print(f"Item structure: {item}")` before line 23
2. Run failing test to see actual item content
3. Check database schema for items table
4. Verify API response includes 'price' field

### Recommended Fix
```python
def calculate_total(items):
    total = 0
    for item in items:
        # Add validation
        if 'price' not in item or 'quantity' not in item:
            raise ValueError(f"Invalid item: {item}")
        price = item['price'] * item['quantity']
        total += price
    return total
```

### Related Code
- models.py: Item model definition
- api.py: Order creation endpoint
- validators.py: Data validation utilities
```

## Best Practices

1. **Start with evidence** - Don't guess, analyze error messages and traces
2. **Use confidence scores** - Quantify certainty, don't claim absolute knowledge
3. **Provide multiple suspects** - Bugs aren't always where they appear
4. **Show your reasoning** - Explain why each location is suspect
5. **Suggest verification** - How to confirm the bug location
6. **Consider context** - Recent changes, code complexity, bug history
7. **Think systematically** - Use data flow, control flow, and call graphs
8. **Prioritize** - Focus on highest-confidence locations first
9. **Be specific** - File:line precision, not just "somewhere in this module"
10. **Recommend next steps** - Debugging strategies, not just identification
