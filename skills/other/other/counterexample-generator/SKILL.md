---
name: counterexample-generator
description: Generate concrete counterexamples when formal verification, assertions, or specifications fail. Use this skill when debugging failed proofs, understanding why verification fails, creating minimal reproducing examples, analyzing assertion violations, investigating invariant breaks, or diagnosing specification mismatches. Produces concrete input values, execution traces, and state information that demonstrate the failure.
---

# Counterexample Generator

Systematically generate counterexamples that demonstrate why verification fails. Provides concrete input values, execution traces, and diagnostic information to help understand and fix specification or implementation issues.

## Core Capabilities

### 1. Precondition Violation Detection

Generate inputs that violate preconditions:
- **Invalid parameter values** - Out-of-range inputs
- **Null/undefined references** - Missing required objects
- **State violations** - Invalid object states
- **Type mismatches** - Incorrect types
- **Constraint violations** - Broken business rules

### 2. Postcondition Failure Analysis

Find executions where postconditions fail:
- **Return value violations** - Wrong return values
- **State inconsistencies** - Incorrect final states
- **Invariant breaks** - Invariants violated after execution
- **Side effect errors** - Unexpected modifications
- **Exception failures** - Wrong or missing exceptions

### 3. Invariant Violation Discovery

Identify cases where invariants break:
- **Class invariant violations** - Object consistency broken
- **Loop invariant violations** - Invariant not maintained
- **Data structure violations** - Consistency broken
- **Temporal violations** - Time-based properties fail
- **Concurrency violations** - Race conditions exposed

### 4. Execution Trace Generation

Produce detailed execution paths:
- **Step-by-step traces** - Line-by-line execution
- **State snapshots** - Variable values at each step
- **Branch decisions** - Which paths taken
- **Call stacks** - Function call hierarchy
- **Symbolic execution** - Constraint-based paths

## Counterexample Generation Workflow

### Step 1: Identify the Failure

Understand what verification failed:

**From verification tools:**
```
Verification failed: Postcondition violated
Function: withdraw
Line: 15
Property: account.balance == old(account.balance) - amount
```

**From assertions:**
```python
AssertionError: assert result >= 0
  in function: sqrt
  with input: x = -1
```

**From test failures:**
```
Test failed: test_binary_search
Expected: 2
Actual: -1
```

**Analysis questions:**
- What property failed?
- Where did it fail?
- What was being verified?
- What are the inputs/state?

### Step 2: Analyze the Specification

Understand what should be true:

**Example specification:**
```python
def withdraw(account: Account, amount: float) -> float:
    """
    Preconditions:
        - account is not None
        - amount > 0
        - account.balance >= amount

    Postconditions:
        - account.balance == old(account.balance) - amount
        - result == account.balance
        - account.balance >= 0
    """
```

**Identify constraints:**
- Precondition: `account.balance >= amount`
- Postcondition: `account.balance == old(account.balance) - amount`
- Invariant: `account.balance >= 0`

### Step 3: Generate Counterexample Inputs

Find concrete values that cause failure:

**Manual generation:**
```python
# Try to violate postcondition
# If amount = 100, old balance = 50
# Then: 50 - 100 = -50 (violates balance >= 0 invariant!)

counterexample = {
    'account': Account(balance=50),
    'amount': 100
}
```

**Systematic generation:**
1. Start with boundary values
2. Try edge cases
3. Use constraint solving
4. Employ random testing
5. Apply mutation testing

### Step 4: Execute and Trace

Run the counterexample and capture details:

**Execution trace:**
```python
Initial state:
  account.balance = 50
  amount = 100

Step 1: Enter withdraw function
  Precondition check: account.balance >= amount?
  50 >= 100 → False

  Should raise error, but code doesn't check!

Step 2: Execute: account.balance -= amount
  account.balance = 50 - 100 = -50

Step 3: Return account.balance
  result = -50

Postcondition check:
  account.balance == old(account.balance) - amount?
  -50 == 50 - 100 → True (passes)

  account.balance >= 0?
  -50 >= 0 → False (FAILS!)

COUNTEREXAMPLE FOUND:
  Invariant violation: balance became negative
```

### Step 5: Present the Counterexample

Format for clarity and debugging:

**Counterexample report:**
```markdown
## Counterexample: Invariant Violation in withdraw()

### Failed Property
Invariant: account.balance >= 0

### Inputs
- account.balance = 50
- amount = 100

### Execution Trace
1. Initial: account.balance = 50
2. Check: balance >= amount → 50 >= 100 → False
   (Missing precondition enforcement!)
3. Execute: balance -= amount → balance = -50
4. Return: -50

### Why It Fails
The function doesn't enforce the precondition that
`account.balance >= amount`. When amount > balance,
the withdrawal proceeds anyway, violating the
invariant that balance must be non-negative.

### Root Cause
Missing validation:
```python
if account.balance < amount:
    raise InsufficientFundsError()
```

### Fix
Add precondition check before withdrawal.
```

## Counterexample Patterns

### Pattern 1: Boundary Value Violation

**Specification:**
```python
def sqrt(x: float) -> float:
    """
    Precondition: x >= 0
    Postcondition: result >= 0 and abs(result * result - x) < 1e-10
    """
    return x ** 0.5
```

**Verification failure:**
```
Postcondition violated when x < 0
```

**Counterexample:**
```python
# Counterexample
input: x = -1

# Execution:
result = (-1) ** 0.5 = (1.5707963267948966e-308+6.123233995736766e-17j)
# Returns complex number, not float!

# Why it fails:
# Python returns complex for sqrt of negative
# Violates postcondition: result should be float

# Trace:
Initial state: x = -1
Step 1: Compute (-1) ** 0.5
Step 2: Result is complex number
Step 3: Return complex (type violation)

# Fix needed:
if x < 0:
    raise ValueError("Cannot compute sqrt of negative number")
```

### Pattern 2: Off-By-One Error

**Specification:**
```python
def binary_search(arr: List[int], target: int) -> int:
    """
    Precondition: arr is sorted
    Postcondition:
        If result >= 0: arr[result] == target
        If result == -1: target not in arr
    """
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid  # BUG: should be mid + 1
        else:
            right = mid - 1
    return -1
```

**Counterexample:**
```python
# Counterexample
input:
  arr = [1, 2, 3, 4, 5]
  target = 5

# Execution trace:
Iteration 1:
  left = 0, right = 4, mid = 2
  arr[2] = 3 < 5
  left = 2  # Bug! Infinite loop starts

Iteration 2:
  left = 2, right = 4, mid = 3
  arr[3] = 4 < 5
  left = 3

Iteration 3:
  left = 3, right = 4, mid = 3
  arr[3] = 4 < 5
  left = 3  # Stuck! left doesn't advance

... (infinite loop)

# Why it fails:
Setting left = mid instead of left = mid + 1
causes infinite loop when target is in right half

# Minimal counterexample:
arr = [1, 2], target = 2
→ Infinite loop
```

### Pattern 3: Invariant Violation

**Specification:**
```python
class Stack:
    """
    Invariant:
        - 0 <= size <= capacity
        - size == len(items)
    """
    def __init__(self, capacity):
        self.capacity = capacity
        self.items = []
        self.size = 0

    def push(self, item):
        self.items.append(item)
        self.size += 1  # BUG: doesn't check capacity
```

**Counterexample:**
```python
# Counterexample
Initial state:
  capacity = 2
  items = []
  size = 0

Operations:
  push(1) → items = [1], size = 1 ✓
  push(2) → items = [1, 2], size = 2 ✓
  push(3) → items = [1, 2, 3], size = 3 ✗

# Invariant violation:
size > capacity
3 > 2 → FAILS

# Why it fails:
No check that size < capacity before push

# Fix:
def push(self, item):
    if self.size >= self.capacity:
        raise StackOverflowError()
    self.items.append(item)
    self.size += 1
```

### Pattern 4: State Inconsistency

**Specification:**
```python
class BankAccount:
    """
    Invariant: balance >= 0
    """
    def __init__(self, balance):
        self.balance = balance

    def transfer_to(self, other, amount):
        """
        Postcondition:
            self.balance == old(self.balance) - amount
            other.balance == old(other.balance) + amount
        """
        self.balance -= amount
        # BUG: Missing other.balance += amount
```

**Counterexample:**
```python
# Counterexample
Initial state:
  account1.balance = 100
  account2.balance = 50

Operation:
  account1.transfer_to(account2, 30)

# Execution trace:
Step 1: account1.balance -= 30
  account1.balance = 70

Step 2: [Missing code!]
  account2.balance unchanged = 50

Final state:
  account1.balance = 70
  account2.balance = 50

# Postcondition check:
account2.balance == old(account2.balance) + amount?
50 == 50 + 30?
50 == 80? → FALSE

# Money disappeared:
old total = 100 + 50 = 150
new total = 70 + 50 = 120
Lost: 30

# Counterexample demonstrates:
Money is lost, violates conservation invariant
```

### Pattern 5: Race Condition

**Specification:**
```python
class Counter:
    """
    Thread-safe counter
    Invariant: value equals number of increments
    """
    def __init__(self):
        self.value = 0

    def increment(self):
        # BUG: Not atomic
        temp = self.value
        temp += 1
        self.value = temp
```

**Counterexample:**
```python
# Counterexample (concurrent execution)
Initial state:
  value = 0

Thread 1:                    Thread 2:
  temp1 = value (0)
                              temp2 = value (0)
  temp1 += 1 (1)
                              temp2 += 1 (1)
  value = temp1 (1)
                              value = temp2 (1)

Final state:
  value = 1

# Expected:
2 increments → value should be 2

# Actual:
value = 1

# Why it fails:
Non-atomic read-modify-write
Lost update: Thread 2 overwrites Thread 1

# Interleaving trace:
T1: Read value=0
T2: Read value=0
T1: Compute 0+1=1
T2: Compute 0+1=1
T1: Write value=1
T2: Write value=1 (overwrites!)
Result: value=1 (should be 2)
```

### Pattern 6: Loop Invariant Violation

**Specification:**
```python
def find_max(arr: List[int]) -> int:
    """
    Loop invariant:
        max_val is the maximum of arr[0:i]
    Postcondition:
        result is maximum of all elements
    """
    max_val = arr[0]
    for i in range(len(arr)):  # BUG: should be range(1, len(arr))
        if arr[i] > max_val:
            max_val = arr[i]
    return max_val
```

**Counterexample:**
```python
# Counterexample
input: arr = [5, 3, 8, 2]

# Execution trace:
Initial: max_val = 5, i = 0

Iteration 1 (i=0):
  arr[0] > max_val?
  5 > 5? → False
  max_val remains 5

Iteration 2 (i=1):
  arr[1] > max_val?
  3 > 5? → False
  max_val remains 5

Iteration 3 (i=2):
  arr[2] > max_val?
  8 > 5? → True
  max_val = 8

Iteration 4 (i=3):
  arr[3] > max_val?
  2 > 8? → False
  max_val remains 8

Result: 8 ✓ (correct, but inefficient)

# Better counterexample showing actual bug:
input: arr = [1, 2, 3, 5, 4]

If we compare with itself at i=0:
  Loop invariant violated on first iteration
  Compares element with itself unnecessarily

# Real bug revealed with:
input: arr = []  # Empty array

Execution:
  max_val = arr[0] → IndexError!

# Counterexample demonstrates:
Missing check for empty array
```

### Pattern 7: Arithmetic Overflow

**Specification:**
```python
def midpoint(left: int, right: int) -> int:
    """
    Postcondition: left <= result <= right
    """
    return (left + right) // 2  # BUG: Overflow possible
```

**Counterexample:**
```python
# Counterexample (in languages with fixed-size integers)
input:
  left = 2_000_000_000
  right = 2_000_000_000

# Execution:
Step 1: left + right = 4_000_000_000
  (Overflow in 32-bit signed integer! Max = 2_147_483_647)
  Wraps to negative: -294_967_296

Step 2: -294_967_296 // 2 = -147_483_648

Result: -147_483_648

# Postcondition check:
left <= result <= right?
2_000_000_000 <= -147_483_648 <= 2_000_000_000?
FALSE

# Why it fails:
Integer overflow in addition

# Fix:
return left + (right - left) // 2
```

## Counterexample Generation Techniques

### Technique 1: Boundary Value Analysis

Test at boundaries of valid ranges:

```python
# For specification: 0 <= x <= 100
Test values:
  - Minimum: 0
  - Just above minimum: 1
  - Just below maximum: 99
  - Maximum: 100
  - Below minimum: -1 (counterexample)
  - Above maximum: 101 (counterexample)
```

### Technique 2: Constraint Solving

Use SMT solvers to find satisfying inputs:

```python
# Specification:
# Precondition: x > 0 and y > 0
# Postcondition: result > x and result > y

# Find counterexample where postcondition fails:
# We want: NOT (result > x and result > y)
# Which is: result <= x OR result <= y

# SMT constraint:
# x > 0 AND y > 0 AND (result <= x OR result <= y)

# Solver finds:
x = 10, y = 5
result = 7  # 7 <= 10, so postcondition fails
```

### Technique 3: Symbolic Execution

Execute code symbolically to find violations:

```python
def abs_diff(a, b):
    if a > b:
        return a - b
    else:
        return b - a

# Symbolic execution:
Path 1: a > b
  Constraint: a > b
  Return: a - b

Path 2: a <= b
  Constraint: a <= b
  Return: b - a

# Check postcondition: result >= 0
Path 1: a - b >= 0? (a > b, so yes)
Path 2: b - a >= 0? (a <= b, so yes)

# No counterexample found (correct!)
```

### Technique 4: Mutation Testing

Mutate code and find tests that don't catch it:

```python
# Original:
def is_even(n):
    return n % 2 == 0

# Mutant:
def is_even(n):
    return n % 2 == 1  # Mutation: == to ==

# Counterexample for specification:
input: n = 4
expected: True (even)
actual: False (mutant says odd)

# This shows missing test case
```

## Counterexample Report Template

```markdown
## Counterexample Report

### Failed Property
[Precondition/Postcondition/Invariant that failed]

### Location
File: [filename]
Function: [function name]
Line: [line number]

### Counterexample Inputs
[Concrete input values that trigger the failure]

### Expected Behavior
[What should happen according to specification]

### Actual Behavior
[What actually happened]

### Execution Trace
[Step-by-step execution showing the failure]

### Root Cause
[Why the failure occurs]

### Suggested Fix
[How to fix the issue]

### Minimal Example
[Simplest input that demonstrates the problem]
```

## Example Complete Report

```markdown
## Counterexample Report

### Failed Property
Postcondition: result >= 0

### Location
File: math_utils.py
Function: sqrt
Line: 12

### Counterexample Inputs
```python
x = -4
```

### Expected Behavior
According to specification:
- Should raise ValueError for x < 0
- Should only return non-negative float values

### Actual Behavior
```python
result = sqrt(-4)
# Returns: (1.2246467991473532e-16+2j)
# Type: <class 'complex'>
```

Function returns a complex number instead of raising an exception.

### Execution Trace
```python
1. Function called with x = -4
2. Precondition check: x >= 0? → False (should fail here!)
3. No explicit check implemented
4. Compute: (-4) ** 0.5
5. Python evaluates to complex: 2j
6. Return complex number
7. Postcondition: result >= 0? → Type error (can't compare complex to int)
```

### Root Cause
Missing precondition enforcement. The function assumes input validation
but doesn't implement it. Python's ** operator returns complex numbers
for negative bases with fractional exponents.

### Suggested Fix
```python
def sqrt(x: float) -> float:
    if x < 0:
        raise ValueError(f"Cannot compute sqrt of negative number: {x}")
    return x ** 0.5
```

### Minimal Example
Simplest failing input:
```python
sqrt(-1)  # Any negative number fails
```

### Additional Test Cases
Based on this counterexample, add tests:
```python
def test_sqrt_negative():
    with pytest.raises(ValueError):
        sqrt(-1)

def test_sqrt_zero():
    assert sqrt(0) == 0

def test_sqrt_positive():
    assert abs(sqrt(4) - 2.0) < 1e-10
```
```

## Best Practices

1. **Start simple** - Find minimal counterexamples first
2. **Be concrete** - Use specific values, not symbolic
3. **Show execution** - Provide step-by-step traces
4. **Explain clearly** - Make the failure obvious
5. **Suggest fixes** - Show how to resolve the issue
6. **Test the fix** - Verify the counterexample is resolved
7. **Generalize** - Identify similar potential failures
8. **Document** - Record counterexamples for regression testing
9. **Automate** - Use tools to generate counterexamples
10. **Verify minimal** - Ensure counterexample is simplest possible

## Tools and Techniques

### Static Analysis Tools
- **Dafny** - Auto-generates counterexamples for failed proofs
- **Frama-C** - C verification with counterexample generation
- **Z3/SMT solvers** - Constraint-based counterexample finding
- **CBMC** - Bounded model checking for C

### Dynamic Analysis
- **Property-based testing** - Hypothesis, QuickCheck
- **Fuzzing** - AFL, LibFuzzer
- **Concolic execution** - KLEE, Symbolic PathFinder
- **Mutation testing** - Mutmut, PIT

### Manual Techniques
- Boundary value analysis
- Equivalence partitioning
- State transition testing
- Path coverage analysis

## Common Counterexample Scenarios

### Scenario 1: Missing Validation
```python
# Bug: No input validation
def divide(a, b):
    return a / b

# Counterexample: b = 0 → ZeroDivisionError
```

### Scenario 2: Wrong Boundary
```python
# Bug: Off-by-one in condition
if x <= 100:  # Should be x < 100

# Counterexample: x = 100 (incorrectly included)
```

### Scenario 3: Type Confusion
```python
# Bug: Assumes integer
def double(x):
    return x * 2

# Counterexample: x = "hello" → "hellohello" (string, not number)
```

### Scenario 4: Unhandled Case
```python
# Bug: Missing else
if x > 0:
    return 1
elif x < 0:
    return -1
# Missing: x == 0

# Counterexample: x = 0 → None (should return 0)
```

### Scenario 5: Resource Leak
```python
# Bug: File not closed on exception
def read_file(path):
    f = open(path)
    data = f.read()
    # Missing: f.close()
    return data

# Counterexample: Exception during read → file not closed
```
