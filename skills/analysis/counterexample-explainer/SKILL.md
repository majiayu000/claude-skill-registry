---
name: counterexample-explainer
description: Explain why counterexamples violate specifications by analyzing formal specifications (temporal logic, invariants, pre/postconditions, code contracts), informal requirements (user stories, acceptance criteria), test specifications (assertions, property-based tests), and providing step-by-step traces showing state changes, comparing expected vs actual behavior, identifying root causes, and assessing violation impact. Use when debugging test failures, understanding model checker output, explaining runtime assertion violations, analyzing static analysis warnings, or teaching specification concepts. Produces structured markdown explanations with traces, comparisons, state diagrams, and cause chains. Triggers when users ask why something failed, explain a violation, understand a counterexample, debug a specification, or analyze why a test fails.
---

# Counterexample Explainer

## Overview

Analyze counterexamples that violate specifications and produce clear, structured explanations showing step-by-step how and why the violation occurs, with root cause analysis and impact assessment.

## Workflow

### 1. Understand the Specification

Identify what property is being checked.

**Questions to ask:**
- What is the specification or requirement?
- Is it formal (invariant, temporal logic) or informal (requirement doc)?
- What should happen vs what actually happened?
- Is this from a test failure, model checker, or runtime error?

See [specification-types.md](references/specification-types.md) for comprehensive specification catalog.

**Common specification types:**

**Formal specifications:**
- Invariants: `balance >= 0`
- Temporal logic: `G(request → F grant)`
- Pre/postconditions: `@requires(x > 0)`, `@ensures(result >= 0)`
- State machines: Valid state transitions
- Concurrency: Atomicity, deadlock freedom

**Informal requirements:**
- User stories with acceptance criteria
- Functional requirements
- API contracts
- Expected behavior descriptions

**Test specifications:**
- Assertions: `assert result == expected`
- Property-based tests
- Integration test expectations

### 2. Collect Counterexample Information

Gather all relevant data about the violation.

**From test failures:**
```bash
# Run test to get failure details
pytest test_file.py::test_name -v

# Get stack trace
pytest test_file.py::test_name -v --tb=long

# Get variable values at failure
pytest test_file.py::test_name -v -l
```

**Information to extract:**
- Input values that triggered failure
- Expected output/behavior
- Actual output/behavior
- Intermediate state changes
- Stack trace or execution path
- Error messages

**From runtime violations:**
```python
# Assertion failure
AssertionError: balance must be non-negative
  File "account.py", line 45
  assert self.balance >= 0

# Extract:
# - Variable: self.balance
# - Expected: >= 0
# - Actual: (check value)
```

**From model checkers:**
```
Counterexample trace:
State 0: request=false, grant=false
State 1: request=true, grant=false
State 2: request=true, grant=false
...
State 50: request=true, grant=false (VIOLATION)

Property violated: G(request → F grant)
```

### 3. Identify Violation Point

Pinpoint exactly where and when specification is broken.

**For invariants:**
- Find the operation that breaks the invariant
- Identify the state transition that causes violation
- Note variable values before and after

**For temporal properties:**
- Identify the state where property fails
- Trace back to find root cause
- Show path through states

**For assertions:**
- Locate the assertion that fails
- Check values of variables in assertion
- Find operation that produced wrong value

**Example analysis:**

```python
# Specification
assert balance >= 0  # Invariant

# Counterexample
initial_balance = 100
withdraw(150)
# balance is now -50

# Violation point: withdraw operation
# Before: balance = 100 (satisfies invariant)
# After: balance = -50 (violates invariant)
```

### 4. Generate Step-by-Step Trace

Show execution path leading to violation.

See [explanation-patterns.md](references/explanation-patterns.md) for detailed patterns.

**Trace structure:**

```markdown
## Counterexample Trace

**Specification:** [What property should hold]

### Initial State
- [variable1]: [value]
- [variable2]: [value]
- Status: ✅ Satisfies specification

### Step 1: [Operation/Event]
**Action:** [What happened]

**State Changes:**
- [variable]: [old_value] → [new_value]

**Status:** ✅ Still satisfies specification

**Why this matters:** [Explanation of significance]

### Step 2: [Operation/Event]
**Action:** [What happened]

**State Changes:**
- [variable]: [old_value] → [new_value]

**Status:** ❌ VIOLATES specification

**Violation Details:**
- Expected: [what should be true]
- Actual: [what is actually true]
- Violated property: [specific clause/condition]

**Why it violates:** [Clear explanation]

### Final State
- [variable1]: [value]
- [variable2]: [value]
- Status: ❌ Specification violated
```

**Example:**

```markdown
## Balance Invariant Violation

**Specification:** Account balance must remain non-negative (`balance >= 0`)

### Initial State
- account.balance: 100
- Status: ✅ Satisfies invariant (100 >= 0)

### Step 1: User initiates withdrawal
**Action:** `withdraw(150)` called

**Validation Check:**
- Amount to withdraw: 150
- Current balance: 100
- Sufficient funds? NO (150 > 100)

**Expected behavior:** Reject withdrawal, raise InsufficientFundsError

**Actual behavior:** Withdrawal proceeds (bug: no validation)

### Step 2: System processes withdrawal
**Action:** Balance updated

**State Changes:**
- account.balance: 100 → -50

**Status:** ❌ VIOLATES INVARIANT

**Violation Details:**
- Expected: balance >= 0
- Actual: balance = -50
- Violated property: balance >= 0 (non-negativity)

**Why it violates:**
-50 is NOT >= 0. The balance has gone negative, which violates the core
invariant that account balances must never be negative.

### Final State
- account.balance: -50
- Status: ❌ Overdraft occurred

### Root Cause
Missing validation in `withdraw` method:

```python
def withdraw(self, amount):
    # BUG: No check if amount > balance
    self.balance -= amount  # This can go negative!

# Should be:
def withdraw(self, amount):
    if amount > self.balance:
        raise InsufficientFundsError(f"Cannot withdraw {amount}, balance is {self.balance}")
    self.balance -= amount
```
```

### 5. Compare Expected vs Actual

Show side-by-side what should happen vs what happened.

```markdown
## Expected vs Actual Behavior

| Aspect | Expected (Specification) | Actual (Counterexample) | Match? |
|--------|-------------------------|-------------------------|--------|
| [Property 1] | [Expected value] | [Actual value] | ✅/❌ |
| [Property 2] | [Expected value] | [Actual value] | ✅/❌ |
| [Property 3] | [Expected value] | [Actual value] | ✅/❌ |

**Key Differences:**
- [Property X]: Expected [value] but got [value]

**Why this matters:**
[Explanation of impact]
```

### 6. Identify Root Cause

Find the underlying bug or design flaw.

**Common root causes:**

**Missing validation:**
```python
# Root cause: No input validation
def divide(a, b):
    return a / b  # Crashes when b=0

# Fix: Add validation
def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
```

**Wrong algorithm:**
```python
# Root cause: Using > instead of <
def sort_ascending(arr):
    for i in range(len(arr)):
        for j in range(i+1, len(arr)):
            if arr[i] > arr[j]:  # BUG: should be <
                arr[i], arr[j] = arr[j], arr[i]
```

**Race conditions:**
```python
# Root cause: Non-atomic update
def increment_counter():
    count = get_count()  # Read
    count += 1           # Modify
    set_count(count)     # Write
    # Another thread can interleave here
```

**Off-by-one errors:**
```python
# Root cause: Loop doesn't process last element
for i in range(len(arr) - 1):  # BUG: should be len(arr)
    process(arr[i])
# Last element never processed
```

### 7. Assess Impact

Explain consequences of the violation.

```markdown
## Impact Analysis

**What Went Wrong:**
[Brief description of violation]

**Immediate Consequences:**
- [Direct effect 1]
- [Direct effect 2]

**Downstream Effects:**
1. [Cascading effect 1]
2. [Cascading effect 2]

**Severity:** [Critical/High/Medium/Low]

**Real-World Impact:**
[What this means for users/system]

**Example Scenario:**
[Concrete example of harm]
```

### 8. Present Complete Explanation

Combine all analysis into clear explanation.

**Explanation structure:**

```markdown
# Counterexample Explanation: [Title]

## Summary
[One-sentence description of violation]

## Specification
**What should happen:**
[Specification statement]

**In plain English:**
[Non-technical explanation]

## Counterexample
**What actually happened:**
[Description of violation]

**Input:** [Input that triggered violation]
**Output:** [Actual output]
**Expected:** [What should have happened]

## Detailed Trace

[Step-by-step execution showing violation]

## Root Cause

**Bug location:** [File and line number]

**Problem:**
[Explanation of bug]

**Fix:**
```code
[Corrected code]
```

## Impact

**Severity:** [Level]
**Consequences:** [List of effects]

## Related Issues

- [Similar violations]
- [Other tests that might fail]
```

## Example Workflows

### Example 1: Test Failure Explanation

**User provides:**
```python
def test_sort_ascending():
    result = sort([3, 1, 4, 1, 5])
    assert result == [1, 1, 3, 4, 5]  # FAILS

AssertionError: assert [5, 4, 3, 1, 1] == [1, 1, 3, 4, 5]
```

**Explanation:**

```markdown
# Sort Function Violation

## Summary
Sort function produces descending order instead of specified ascending order.

## Specification
**Function:** `sort(array)` should arrange elements in ascending order
**Formal property:** For all i < j: result[i] <= result[j]

## Counterexample

**Input:** [3, 1, 4, 1, 5]
**Expected:** [1, 1, 3, 4, 5] (ascending)
**Actual:** [5, 4, 3, 1, 1] (descending)

### Why This Violates Specification

The spec requires ascending order, meaning:
- result[0] <= result[1] <= result[2] <= ...

But actual output has:
- result[0]=5 > result[1]=4 (VIOLATES: should be <=)

Every comparison is reversed.

## Root Cause

**Bug in comparison operator:**

```python
# Current (wrong)
if arr[i] > arr[j]:
    swap(arr[i], arr[j])

# Should be
if arr[i] < arr[j]:  # Changed > to <
    swap(arr[i], arr[j])
```

The function uses `>` which sorts in descending order.
To sort ascending, use `<`.

## Impact
- All sorted outputs are backwards
- Any code depending on ascending order will fail
- Binary search will not work on these results
```

### Example 2: Temporal Logic Violation

**User provides:**
```
Property: G(request → F grant)
"All requests are eventually granted"

Counterexample:
t=0: request=false, grant=false
t=1: request=true, grant=false
t=2: request=true, grant=false
...
t=100: request=true, grant=false
```

**Explanation:**

```markdown
# Unfulfilled Request Violation

## Summary
Request made at t=1 is never granted, violating the guarantee that all
requests are eventually granted.

## Specification

**Temporal Logic:** `G(request → F grant)`

**Plain English:**
"Whenever a request is made, it will eventually be granted at some future time"

## Counterexample Timeline

```
t=0:  request=false, grant=false
      ✅ No pending requests

t=1:  User makes request
      request=true, grant=false
      ℹ️  Request pending - must be granted eventually

t=2:  System continues
      request=true, grant=false
      ⚠️  Request still pending (acceptable if grant happens later)

[... time passes ...]

t=100: Request still pending
       request=true, grant=false
       ❌ VIOLATION: Grant never occurred
```

## Why This Violates G(request → F grant)

At t=1, `request` becomes true. The specification `G(request → F grant)`
requires:
- When request is true, `F grant` (eventually grant) must hold
- This means at some future time t > 1, grant must become true

However, the trace shows grant stays false forever. The "eventually grant"
promise is broken.

## Root Cause

**Missing queue processing:**

```python
def handle_request(request):
    request_queue.append(request)  # Added to queue
    # BUG: Never calls process_queue()!

# Fix: Process the queue
def handle_request(request):
    request_queue.append(request)
    process_queue()  # Grant requests from queue
```

Requests are enqueued but never processed.

## Impact

- Users wait indefinitely
- System appears frozen
- Resources (memory) accumulate as queue grows
- Eventually runs out of memory (separate bug)
```

## Tips for Clear Explanations

**Be specific:**
- Point to exact lines where violation occurs
- Show actual values, not just variable names
- Include concrete examples

**Use visuals:**
- State diagrams for state machines
- Timelines for temporal properties
- Tables for expected vs actual
- Code diffs for fixes

**Explain impact:**
- Why does this violation matter?
- What are the consequences?
- How serious is it?

**Provide fix:**
- Show what code should be
- Explain why fix works
- Note if fix has trade-offs

**Use plain language:**
- Avoid jargon when possible
- Explain formal notation
- Give intuitive explanations

## Common Violation Types

**Boundary violations:**
- Array index out of bounds
- Negative when should be non-negative
- Overflow/underflow

**Logic errors:**
- Wrong operator (>, < vs >=, <=)
- Missing negation
- Incorrect boolean logic

**Missing checks:**
- No null/None validation
- No bounds checking
- No error handling

**Concurrency issues:**
- Race conditions
- Deadlocks
- Lost updates

**State violations:**
- Invalid state transitions
- Inconsistent state
- Missing state reset

## Reference

For detailed specification types and explanation patterns:
- [specification-types.md](references/specification-types.md) - Comprehensive specification catalog
- [explanation-patterns.md](references/explanation-patterns.md) - Detailed explanation templates and examples
