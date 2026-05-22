---
name: python3-bug
description: Debug functional issues in Python code using specs, logs, and observed behavior. Use when a feature isn't working as specified, when investigating runtime errors, or when scoping a problem before implementing a fix.
user-invocable: true
argument-hint: "<problem-description>"
---

# Python Functional Bug Investigation

The model investigates functional bugs using specifications, logs, and observed behavior to scope the problem before implementing fixes.

## Arguments

$ARGUMENTS

## Instructions

1. **Gather context** from user (spec, logs, reproduction steps)
2. **Scope the problem** (what works, what doesn't, boundaries)
3. **Form hypotheses** about root cause
4. **Investigate systematically** with evidence
5. **Propose fix** only after understanding root cause

---

## Phase 1: Problem Intake

### Required Information

Ask for these if not provided:

```text
SPECIFICATION
- [ ] What should the feature do? (spec, user story, acceptance criteria)
- [ ] What behavior is expected?

OBSERVED BEHAVIOR
- [ ] What actually happens?
- [ ] Error messages (exact text)
- [ ] Logs (relevant sections)

REPRODUCTION
- [ ] Steps to reproduce
- [ ] Input data that triggers the bug
- [ ] Environment (Python version, OS, dependencies)

CONTEXT
- [ ] When did it last work? (if ever)
- [ ] What changed recently?
- [ ] Is it intermittent or consistent?
```

### Intake Template

```text
## Bug Report

**Expected Behavior**:
[What should happen according to spec]

**Actual Behavior**:
[What is happening]

**Error/Logs**:
```

[Paste exact error messages or relevant log output]

```

**Reproduction Steps**:
1. [First step]
2. [Second step]
3. [Step where failure occurs]

**Environment**:
- Python: [version]
- OS: [os]
- Relevant packages: [list]

**Recent Changes**:
[What changed before this started happening]
```

---

## Phase 2: Problem Scoping

### Define Boundaries

Establish what works and what doesn't:

```text
WORKING
- [ ] [Feature X works correctly]
- [ ] [Feature Y works correctly]

NOT WORKING
- [ ] [Feature Z fails with error]
- [ ] [Feature W produces wrong output]

UNKNOWN
- [ ] [Feature V not tested yet]
```

### Narrow the Scope

```text
Questions to answer:
1. Is this a regression or never worked?
2. Does it fail for all inputs or specific ones?
3. Does it fail in all environments or specific ones?
4. Is the failure consistent or intermittent?
5. What's the smallest reproduction case?
```

### Create Minimal Reproduction

```python
# Minimal reproduction case
# Goal: Smallest code that demonstrates the bug

def test_reproduction():
    """Minimal reproduction of the bug."""
    # Setup
    input_data = {"key": "value"}  # Specific input that triggers bug

    # Action
    result = buggy_function(input_data)

    # Expected vs Actual
    assert result == expected, f"Got {result}, expected {expected}"
```

---

## Phase 3: Hypothesis Formation

### Generate Hypotheses

Based on symptoms, form multiple hypotheses:

```text
## Hypothesis List

H1: [Description of potential cause]
    Evidence for: [what supports this]
    Evidence against: [what contradicts this]
    Test: [how to verify]

H2: [Description of potential cause]
    Evidence for: [what supports this]
    Evidence against: [what contradicts this]
    Test: [how to verify]

H3: [Description of potential cause]
    Evidence for: [what supports this]
    Evidence against: [what contradicts this]
    Test: [how to verify]
```

### Common Bug Categories

| Category       | Symptoms                           | Investigation                  |
| -------------- | ---------------------------------- | ------------------------------ |
| Type Error     | AttributeError, TypeError          | Check types at boundary        |
| State Mutation | Intermittent, order-dependent      | Look for shared mutable state  |
| Race Condition | Intermittent, timing-dependent     | Check async/threading code     |
| Edge Case      | Specific inputs fail               | Test boundary conditions       |
| Integration    | Works in isolation, fails together | Check interface contracts      |
| Configuration  | Environment-dependent              | Compare working vs failing env |

---

## Phase 4: Systematic Investigation

### Tracing Approach

Follow the data flow:

```text
1. INPUT: What data enters the function?
   - Log: input values, types, shapes

2. PROCESSING: What transformations occur?
   - Add debug logging at each step
   - Check intermediate values

3. OUTPUT: What comes out?
   - Compare actual vs expected output
   - Check return type and structure

4. SIDE EFFECTS: What else changes?
   - Database writes
   - File system changes
   - External API calls
   - Global state modifications
```

### Debug Logging Pattern

```python
import logging

logger = logging.getLogger(__name__)

def investigate_function(data: InputType) -> OutputType:
    logger.debug(f"INPUT: data={data!r}, type={type(data)}")

    # Step 1
    intermediate1 = process_step1(data)
    logger.debug(f"STEP1: intermediate1={intermediate1!r}")

    # Step 2
    intermediate2 = process_step2(intermediate1)
    logger.debug(f"STEP2: intermediate2={intermediate2!r}")

    # Step 3
    result = process_step3(intermediate2)
    logger.debug(f"OUTPUT: result={result!r}, type={type(result)}")

    return result
```

### Hypothesis Testing

For each hypothesis:

```python
def test_hypothesis_1():
    """Test H1: [hypothesis description]"""
    # Setup to isolate this hypothesis
    # ...

    # Action that should reveal if H1 is correct
    # ...

    # Assertion that confirms or refutes H1
    # If this passes, H1 is likely correct
    # If this fails, H1 is refuted
```

---

## Phase 5: Root Cause Analysis

### Evidence Collection

```text
## Root Cause Evidence

**Confirmed Root Cause**: [description]

**Evidence**:
1. [File:line] - [what this shows]
2. [Log entry] - [what this shows]
3. [Test result] - [what this shows]

**Why This Causes the Bug**:
[Explanation of the causal chain from root cause to symptom]

**Eliminated Hypotheses**:
- H2: Ruled out because [evidence]
- H3: Ruled out because [evidence]
```

### Fix Requirements

Before implementing fix:

```text
## Fix Specification

**Root Cause**: [concise description]
**Location**: [file:line range]

**Fix Approach**:
[Description of what needs to change]

**Risks**:
- [Potential side effect 1]
- [Potential side effect 2]

**Test Coverage**:
- [ ] Test for original bug (regression test)
- [ ] Test for edge cases
- [ ] Test for potential side effects
```

---

## Phase 6: Fix Implementation

### Fix Checklist

```text
BEFORE FIX
- [ ] Root cause identified with evidence
- [ ] Minimal reproduction exists
- [ ] Test coverage plan created

DURING FIX
- [ ] Fix addresses root cause (not symptoms)
- [ ] Fix is minimal (no scope creep)
- [ ] Regression test written first

AFTER FIX
- [ ] Regression test passes
- [ ] Existing tests still pass
- [ ] Edge case tests added
- [ ] Code review if significant change
```

### Regression Test Pattern

```python
def test_bug_12345_description():
    """Regression test for bug #12345.

    Bug: [brief description of the original bug]
    Root cause: [what was wrong]
    Fix: [what was changed]
    """
    # Arrange: Setup that triggered the bug
    input_data = create_problematic_input()

    # Act: The operation that failed
    result = fixed_function(input_data)

    # Assert: Verify correct behavior
    assert result == expected_output
    # Also verify the specific fix worked
    assert result.specific_field == expected_value
```

---

## Investigation Report Format

```text
## Bug Investigation Report

**Issue**: [Brief description]
**Status**: [Investigating | Root Cause Found | Fixed | Cannot Reproduce]

### Problem Statement

**Expected**: [spec behavior]
**Actual**: [observed behavior]
**Impact**: [who/what is affected]

### Investigation Timeline

1. [timestamp] - [action taken] - [result]
2. [timestamp] - [action taken] - [result]
3. [timestamp] - [action taken] - [result]

### Hypotheses

| # | Hypothesis | Status | Evidence |
|---|------------|--------|----------|
| H1 | [description] | Confirmed/Refuted | [evidence] |
| H2 | [description] | Confirmed/Refuted | [evidence] |

### Root Cause

**Location**: [file:line]
**Description**: [what's wrong and why]
**Evidence**: [how we know this is the cause]

### Fix

**Approach**: [what will be changed]
**Files Modified**: [list]
**Tests Added**: [list]

### Verification

- [ ] Bug no longer reproduces
- [ ] Regression test passes
- [ ] Existing tests pass
- [ ] Edge cases covered
```

---

## Common Python Bug Patterns

### NoneType Errors

```python
# Bug: AttributeError: 'NoneType' has no attribute 'x'
# Cause: Function returns None unexpectedly

# Investigation
result = get_something()
print(f"result is None: {result is None}")  # Check this first

# Fix: Add proper None handling
if (result := get_something()) is None:
    raise ValueError("Expected result but got None")
return result.x
```

### Mutable Default Arguments

```python
# Bug: List accumulates across calls
def buggy(items=[]):  # WRONG: mutable default
    items.append(1)
    return items

# Fix
def fixed(items: list | None = None) -> list:
    if items is None:
        items = []
    items.append(1)
    return items
```

### Async/Await Issues

```python
# Bug: Coroutine never executed
async def fetch_data():
    return await api_call()

# WRONG: Missing await
result = fetch_data()  # Returns coroutine, not result

# Fix
result = await fetch_data()
```

### Import Errors

```python
# Bug: ImportError or circular import
# Investigation: Check import order and dependencies

# Fix: Use local imports for circular dependencies
def function_that_needs_other_module():
    from .other_module import OtherClass  # Local import
    return OtherClass()
```

---

## References

- [Python Debugging Techniques](https://docs.python.org/3/library/pdb.html)
- [Logging HOWTO](https://docs.python.org/3/howto/logging.html)
- [pytest Debugging](https://docs.pytest.org/en/stable/how-to/failures.html)
