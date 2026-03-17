---
name: static-bug-detector
description: Analyze source code statically to detect potential functional bugs including null dereferences, incorrect condition checks, unreachable code, inconsistent state updates, logic errors, resource leaks, and type mismatches. Report suspicious code locations with detailed explanations, severity levels, and confidence assessments. Use when reviewing code for bugs, performing code audits, or when the user asks to find bugs, detect issues, analyze code for problems, or perform static analysis.
---

# Static Bug Detector

## Overview

Perform static analysis on source code to identify potential functional bugs. Detect common bug patterns, analyze control flow and data flow, and report suspicious locations with explanations, severity levels, and confidence assessments.

## Bug Detection Workflow

### Step 1: Understand the Code

Analyze the code structure and semantics:

1. **Identify language:**
   - Determine programming language
   - Understand language-specific semantics
   - Note language idioms and conventions

2. **Parse code structure:**
   - Functions/methods
   - Classes/types
   - Control flow (if, loops, etc.)
   - Data flow (assignments, returns)

3. **Build context:**
   - Variable declarations and types
   - Function signatures
   - Class hierarchies
   - Dependencies

4. **Identify scope:**
   - What code to analyze
   - Entry points
   - Critical paths

### Step 2: Detect Bug Patterns

Scan for common bug patterns:

1. **Null dereference bugs:**
   - Variables from nullable sources
   - Dereferences without null checks
   - Null checks after use
   - Undocumented null returns

2. **Incorrect conditions:**
   - Always true/false conditions
   - Assignment in condition (= vs ==)
   - Redundant conditions
   - Inverted logic
   - Wrong operators

3. **Unreachable code:**
   - Code after return/throw
   - Always-false branches
   - Dead code paths

4. **Inconsistent state:**
   - Partial state updates
   - Updates without validation
   - Non-atomic operations
   - Broken invariants

5. **Logic errors:**
   - Off-by-one errors
   - Wrong operator precedence
   - Infinite loops
   - Incorrect boolean logic

6. **Resource issues:**
   - Resource leaks
   - Double free/close
   - Use after free/close

7. **Type issues:**
   - Type mismatches
   - Implicit coercion
   - Invalid casts

### Step 3: Analyze Severity

Assess the impact of each bug:

**High Severity:**
- Causes crashes or exceptions
- Data corruption
- Security vulnerabilities
- Guaranteed runtime errors

**Medium Severity:**
- Incorrect behavior
- Potential errors (context-dependent)
- Performance issues
- Maintainability problems

**Low Severity:**
- Code smells
- Redundant code
- Minor inefficiencies
- Style issues that might hide bugs

### Step 4: Assess Confidence

Determine confidence in the bug report:

**High Confidence (90-100%):**
- Clear violation of language semantics
- Guaranteed to cause error
- Well-known bug pattern
- No ambiguity

**Medium Confidence (60-89%):**
- Likely bug but context-dependent
- May be intentional in rare cases
- Suspicious pattern
- Needs verification

**Low Confidence (30-59%):**
- Unusual but possibly valid
- Could be intentional design
- Needs more context
- Style issue that might hide bug

**Factors:**
- Code context available
- Language semantics clarity
- Pattern recognition
- Documentation consistency

### Step 5: Generate Report

Produce structured bug report:

1. **For each bug:**
   - Bug type/category
   - Location (file, line, range)
   - Severity level
   - Confidence level
   - Description
   - Why it's a bug
   - Potential impact
   - Recommendation/fix

2. **Organize by:**
   - Severity (high first)
   - Confidence (high first)
   - Location (file order)
   - Bug type (grouped)

3. **Include:**
   - Code context
   - Example fixes
   - Related bugs
   - Summary statistics

## Bug Categories

For detailed patterns and examples, see [detection_patterns.md](references/detection_patterns.md).

### Quick Reference

| Bug Category | Common Patterns | Severity | Detection Difficulty |
|--------------|----------------|----------|---------------------|
| Null Dereference | No null check, null after use | High | Easy |
| Incorrect Conditions | = vs ==, always true/false | High-Medium | Easy |
| Unreachable Code | After return, dead branch | Low | Easy |
| Inconsistent State | Partial update, no validation | High-Medium | Medium |
| Logic Errors | Off-by-one, wrong precedence | High-Medium | Medium |
| Resource Issues | Leaks, double close | Medium | Medium |
| Type Issues | Mismatch, implicit coercion | Medium-Low | Easy |

## Examples

### Example 1: Null Dereference

**Input Code (Java):**
```java
public String getUserName(int userId) {
    User user = userRepository.findById(userId);
    return user.getName();
}
```

**Analysis Output:**
```markdown
## Bug: Potential null dereference

**Location:** line 3
**Severity:** High
**Confidence:** High (95%)

### Description
Variable 'user' may be null but is dereferenced without null check.

### Why This Is a Bug
Method 'findById' may return null if user not found. Calling 'getName()'
on null will throw NullPointerException.

### Potential Impact
- Runtime NullPointerException
- Application crash
- Poor user experience

### Recommendation
Add null check before dereferencing:

```java
public String getUserName(int userId) {
    User user = userRepository.findById(userId);
    if (user == null) {
        return null;  // or throw exception
    }
    return user.getName();
}
```

Or use Optional:
```java
public Optional<String> getUserName(int userId) {
    return Optional.ofNullable(userRepository.findById(userId))
                   .map(User::getName);
}
```
```

### Example 2: Incorrect Condition

**Input Code (C):**
```c
int status = getStatus();
if (status = SUCCESS) {
    printf("Operation successful\n");
}
```

**Analysis Output:**
```markdown
## Bug: Assignment in condition

**Location:** line 2
**Severity:** High
**Confidence:** High (98%)

### Description
Using assignment operator '=' instead of comparison operator '==' in condition.

### Why This Is a Bug
Expression 'status = SUCCESS' assigns SUCCESS to status and evaluates to
SUCCESS value. This is almost always a typo for 'status == SUCCESS'.

### Potential Impact
- Condition always evaluates to true (if SUCCESS is non-zero)
- Original status value lost
- Logic error in program flow

### Recommendation
Change to comparison operator:

```c
if (status == SUCCESS) {
    printf("Operation successful\n");
}
```

Most compilers warn about this. Enable warnings: -Wall -Wextra
```

### Example 3: Off-by-One Error

**Input Code (Python):**
```python
def process_array(arr):
    for i in range(len(arr) + 1):
        print(arr[i])
```

**Analysis Output:**
```markdown
## Bug: Off-by-one error (array index out of bounds)

**Location:** line 2-3
**Severity:** High
**Confidence:** High (100%)

### Description
Loop iterates one past the end of array, causing IndexError.

### Why This Is a Bug
range(len(arr) + 1) produces indices 0 to len(arr) inclusive. Array
indices are 0 to len(arr)-1, so arr[len(arr)] is out of bounds.

### Potential Impact
- IndexError exception
- Program crash
- Incorrect behavior

### Recommendation
Remove the +1:

```python
def process_array(arr):
    for i in range(len(arr)):
        print(arr[i])
```

Or use idiomatic iteration:
```python
def process_array(arr):
    for item in arr:
        print(item)
```
```

### Example 4: Resource Leak

**Input Code (Python):**
```python
def read_config(path):
    f = open(path)
    config = json.load(f)
    return config
```

**Analysis Output:**
```markdown
## Bug: Resource leak

**Location:** line 2
**Severity:** Medium
**Confidence:** High (90%)

### Description
File opened but never closed, causing resource leak.

### Why This Is a Bug
File handle opened on line 2 is never closed. If exception occurs during
json.load or in normal execution, file remains open.

### Potential Impact
- File descriptor leak
- Resource exhaustion with many calls
- File locking issues on Windows

### Recommendation
Use context manager to ensure cleanup:

```python
def read_config(path):
    with open(path) as f:
        config = json.load(f)
        return config
```

Or ensure close in finally:
```python
def read_config(path):
    f = open(path)
    try:
        config = json.load(f)
        return config
    finally:
        f.close()
```
```

### Example 5: Inconsistent State Update

**Input Code (Java):**
```java
public class BankAccount {
    private double balance;

    public void transfer(BankAccount target, double amount) {
        this.balance -= amount;
        // Missing: target.balance += amount
    }
}
```

**Analysis Output:**
```markdown
## Bug: Incomplete state update

**Location:** line 5
**Severity:** High
**Confidence:** Medium (75%)

### Description
Transfer method deducts from source but doesn't add to target, leaving
system in inconsistent state.

### Why This Is a Bug
Money is removed from source account but never added to target account.
This violates the invariant that total money in system is constant.

### Potential Impact
- Money disappears from system
- Data corruption
- Accounting errors
- Loss of funds

### Recommendation
Complete the transfer operation:

```java
public void transfer(BankAccount target, double amount) {
    if (this.balance < amount) {
        throw new InsufficientFundsException();
    }
    this.balance -= amount;
    target.balance += amount;
}
```

Consider making atomic with synchronization or transactions.
```

### Example 6: Unreachable Code

**Input Code (JavaScript):**
```javascript
function calculate(x) {
    if (x < 0) {
        return -x;
    }
    return x;
    console.log("Calculated");  // Unreachable
}
```

**Analysis Output:**
```markdown
## Bug: Unreachable code

**Location:** line 6
**Severity:** Low
**Confidence:** High (100%)

### Description
Statement is unreachable because function returns unconditionally on line 5.

### Why This Is a Bug
All code paths return before line 6. The console.log statement can never
execute, indicating dead code or logic error.

### Potential Impact
- Dead code clutters codebase
- May indicate incomplete refactoring
- Confusing for maintainers

### Recommendation
Remove unreachable code:

```javascript
function calculate(x) {
    if (x < 0) {
        return -x;
    }
    return x;
}
```

Or if logging was intended, move before return:
```javascript
function calculate(x) {
    let result = x < 0 ? -x : x;
    console.log("Calculated");
    return result;
}
```
```

## Report Format

### Summary Section

```markdown
# Static Analysis Report

**Files Analyzed:** X
**Bugs Found:** Y
**High Severity:** A
**Medium Severity:** B
**Low Severity:** C

## Summary by Category
- Null Dereference: X bugs
- Incorrect Conditions: Y bugs
- Unreachable Code: Z bugs
- Inconsistent State: A bugs
- Logic Errors: B bugs
- Resource Issues: C bugs
- Type Issues: D bugs
```

### Individual Bug Reports

```markdown
## Bug #N: [Bug Type]

**Location:** [File]:[Line] or [Line Range]
**Severity:** [High/Medium/Low]
**Confidence:** [High/Medium/Low] ([Percentage]%)

### Description
[What the bug is]

### Why This Is a Bug
[Explanation of the problem]

### Potential Impact
[What could go wrong]

### Recommendation
[How to fix it]

### Code Context
```[language]
[Code snippet with line numbers]
```

### Example Fix
```[language]
[Corrected code]
```
```

## Best Practices

### Analysis Guidelines

1. **Be thorough:** Check all common bug patterns
2. **Be precise:** Provide exact locations
3. **Be clear:** Explain why it's a bug
4. **Be helpful:** Suggest concrete fixes
5. **Be honest:** Indicate confidence levels
6. **Be practical:** Prioritize by severity
7. **Be respectful:** Avoid judgmental language

### Reporting Guidelines

1. **Prioritize:** High severity and confidence first
2. **Group:** Related bugs together
3. **Contextualize:** Show relevant code
4. **Explain:** Why it's a bug, not just what
5. **Suggest:** Concrete fixes, not just problems
6. **Quantify:** Confidence and severity levels
7. **Summarize:** Overall statistics

### Confidence Calibration

**Report High Confidence when:**
- Clear language violation
- Guaranteed runtime error
- Well-documented bug pattern
- No reasonable alternative interpretation

**Report Medium Confidence when:**
- Suspicious but context-dependent
- Likely bug but could be intentional
- Requires domain knowledge
- Multiple interpretations possible

**Report Low Confidence when:**
- Unusual but possibly valid
- Style issue that might hide bug
- Insufficient context
- Language-specific idiom

## Limitations

### What This Skill Can Detect

✅ Null dereferences
✅ Incorrect conditions
✅ Unreachable code
✅ Logic errors
✅ Resource leaks
✅ Type mismatches
✅ Off-by-one errors
✅ Inconsistent state updates

### What This Skill Cannot Detect

❌ Concurrency bugs (race conditions, deadlocks)
❌ Performance issues (without profiling)
❌ Security vulnerabilities (requires specialized analysis)
❌ Design flaws (architectural issues)
❌ Business logic errors (requires domain knowledge)
❌ Integration issues (requires runtime context)

### False Positives

Some reported bugs may be intentional:
- Defensive programming patterns
- Language-specific idioms
- Framework conventions
- Performance optimizations

Always verify bugs in context before fixing.

## Resources

- **Detection patterns:** See [detection_patterns.md](references/detection_patterns.md) for comprehensive bug patterns and examples
- **Static analysis tools:** Compare with automated tools (ESLint, PyLint, FindBugs, etc.)
- **Code review best practices:** Guidelines for manual code review
