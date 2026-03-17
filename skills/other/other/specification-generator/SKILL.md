---
name: specification-generator
description: Generate formal specifications including preconditions, postconditions, invariants, and contracts from code or requirements. Use this skill when documenting APIs, creating formal verification annotations, defining function contracts, specifying class invariants, writing design-by-contract code, or preparing code for formal verification. Supports multiple specification languages including JML, ACSL, Dafny, Eiffel contracts, and documentation annotations.
---

# Specification Generator

Systematically generate formal specifications from code and requirements. Produces preconditions, postconditions, invariants, and behavioral contracts that enable verification, documentation, and design-by-contract programming.

## Core Capabilities

### 1. Precondition Generation

Define required conditions before execution:
- **Parameter validation** - Valid ranges, types, states
- **Object state requirements** - Required object states
- **Resource availability** - Files exist, connections open
- **Authorization checks** - Permission requirements
- **Null safety** - Non-null parameter requirements
- **Invariant satisfaction** - Class invariants must hold

### 2. Postcondition Generation

Specify guaranteed outcomes after execution:
- **Return value constraints** - Valid return ranges and properties
- **State modifications** - How object state changes
- **Side effects** - File writes, database updates
- **Exception conditions** - When exceptions are thrown
- **Resource management** - Resources properly released
- **Invariant preservation** - Invariants still hold

### 3. Invariant Generation

Identify properties that always hold:
- **Class invariants** - Properties true for all instances
- **Loop invariants** - Properties preserved by iterations
- **Data structure invariants** - Consistency conditions
- **Representation invariants** - Internal consistency
- **Temporal invariants** - Time-based properties

### 4. Contract Generation

Create complete behavioral specifications:
- **Method contracts** - Full pre/post conditions
- **Interface contracts** - API behavioral guarantees
- **Type contracts** - Type-level properties
- **Protocol contracts** - Valid call sequences
- **Frame conditions** - What doesn't change

## Specification Generation Workflow

### Step 1: Analyze Code or Requirements

Understand what needs to be specified:

**For existing code:**
- Read function/method implementation
- Identify parameters and return type
- Find state modifications
- Detect resource usage
- Locate error conditions

**For requirements:**
- Extract functional requirements
- Identify constraints and rules
- Find boundary conditions
- Determine error scenarios
- Specify expected behavior

**Example code:**
```python
def withdraw(account, amount):
    if account.balance < amount:
        raise InsufficientFundsError()
    account.balance -= amount
    return account.balance
```

**Analysis:**
- Parameters: account (object), amount (number)
- Return: new balance (number)
- State change: account.balance decreases
- Error: raises exception if insufficient funds
- Constraints: amount should be positive, account must exist

### Step 2: Identify Contract Elements

Determine what to specify:

**Preconditions (requires/assume):**
- What must be true before execution?
- Parameter validity requirements
- Object state requirements

**Postconditions (ensures/guarantee):**
- What is guaranteed after execution?
- Return value properties
- State changes

**Invariants:**
- What is always true?
- Class-level properties
- Loop properties

**Example identification:**
```python
# withdraw function
Preconditions:
- account is not None
- amount > 0
- account.balance >= amount (to succeed without exception)

Postconditions:
- If successful: account.balance == old(account.balance) - amount
- If successful: return value == new balance
- If insufficient: raises InsufficientFundsError
- account object still valid

Invariants (Account class):
- balance >= 0 (always)
- account_number is immutable
```

### Step 3: Choose Specification Language

Select appropriate format:

**Specification languages:**

| Language | Use Case | Example |
|----------|----------|---------|
| JML (Java) | Java programs | `//@ requires`, `//@ ensures` |
| ACSL (C) | C programs | `/*@ requires`, `/*@ ensures` |
| Dafny | Verified code | `requires`, `ensures` |
| Eiffel | Design-by-contract | `require`, `ensure` |
| Python docstring | Documentation | `:param:`, `:raises:`, `:returns:` |
| TypeScript | Type annotations | Type predicates, assertions |
| Hoare logic | Formal proofs | `{P} S {Q}` notation |

**Example language choice:**
- Java method → Use JML
- C function → Use ACSL
- Python function → Use docstring assertions
- Verification task → Use Dafny

### Step 4: Write Specifications

Generate formal contracts:

**Format depends on language:**

**JML (Java):**
```java
/*@ requires amount > 0;
  @ requires account != null;
  @ requires account.balance >= amount;
  @ ensures account.balance == \old(account.balance) - amount;
  @ ensures \result == account.balance;
  @ signals (InsufficientFundsError e) account.balance < amount;
  @*/
public int withdraw(Account account, int amount) {
    // implementation
}
```

**ACSL (C):**
```c
/*@ requires amount > 0;
  @ requires \valid(account);
  @ requires account->balance >= amount;
  @ ensures account->balance == \old(account->balance) - amount;
  @ ensures \result == account->balance;
  @*/
int withdraw(Account *account, int amount) {
    // implementation
}
```

**Dafny:**
```dafny
method Withdraw(account: Account, amount: int) returns (newBalance: int)
    requires amount > 0
    requires account.balance >= amount
    ensures account.balance == old(account.balance) - amount
    ensures newBalance == account.balance
    modifies account
{
    // implementation
}
```

**Python (docstring):**
```python
def withdraw(account: Account, amount: float) -> float:
    """
    Withdraw amount from account.

    :param account: The account to withdraw from
    :param amount: The amount to withdraw (must be positive)
    :raises InsufficientFundsError: If balance < amount
    :raises ValueError: If amount <= 0
    :returns: The new account balance

    Preconditions:
        - account is not None
        - amount > 0
        - account.balance >= amount (for successful withdrawal)

    Postconditions:
        - account.balance == old_balance - amount
        - return value == account.balance
        - If insufficient funds: InsufficientFundsError raised
        - account.balance >= 0 (invariant preserved)
    """
    # implementation
```

### Step 5: Verify Specifications

Ensure specifications are correct:

**Verification steps:**
1. Check preconditions are sufficient (not too strong)
2. Verify postconditions are achievable (not too weak)
3. Confirm invariants always hold
4. Test specifications with examples
5. Use formal verification tools if available

**Example verification:**
```python
# Test preconditions
assert amount > 0  # Valid
assert account is not None  # Valid
assert account.balance >= amount  # Valid for success case

# Test postconditions
old_balance = account.balance
result = withdraw(account, 100)
assert account.balance == old_balance - 100  # Check
assert result == account.balance  # Check

# Test invariants
assert account.balance >= 0  # Should always hold
```

## Specification Patterns

### Pattern 1: Simple Function Contract

**Code:**
```python
def sqrt(x):
    """Compute square root."""
    return x ** 0.5
```

**Generated specification:**
```python
def sqrt(x: float) -> float:
    """
    Compute the square root of x.

    :param x: The number to compute square root of
    :returns: The square root of x
    :raises ValueError: If x < 0

    Preconditions:
        - x >= 0

    Postconditions:
        - result >= 0
        - abs(result * result - x) < 1e-10  # Precision tolerance
        - If x == 0, then result == 0
        - If x == 1, then result == 1
    """
    if x < 0:
        raise ValueError("Cannot compute square root of negative number")
    return x ** 0.5
```

**JML version:**
```java
/*@ requires x >= 0;
  @ ensures \result >= 0;
  @ ensures Math.abs(\result * \result - x) < 1e-10;
  @ ensures x == 0 ==> \result == 0;
  @ ensures x == 1 ==> \result == 1;
  @ signals (IllegalArgumentException e) x < 0;
  @*/
public double sqrt(double x) {
    if (x < 0) throw new IllegalArgumentException();
    return Math.sqrt(x);
}
```

### Pattern 2: Array/Collection Modification

**Code:**
```python
def sort_list(items):
    """Sort list in-place."""
    items.sort()
```

**Generated specification:**
```python
def sort_list(items: List[int]) -> None:
    """
    Sort list in ascending order (in-place).

    :param items: List to sort (modified in-place)

    Preconditions:
        - items is not None
        - All elements in items are comparable

    Postconditions:
        - len(items) == len(old(items))  # Same length
        - set(items) == set(old(items))  # Same elements
        - For all i, j: i < j implies items[i] <= items[j]  # Sorted
        - items is sorted in ascending order

    Frame conditions:
        - Only items is modified
        - No other data structures affected
    """
    if items is None:
        raise ValueError("items cannot be None")
    items.sort()
```

**ACSL version:**
```c
/*@ requires \valid(arr + (0..len-1));
  @ ensures \forall integer i, j;
  @     0 <= i < j < len ==> arr[i] <= arr[j];
  @ ensures Permutation{Pre,Post}(arr, 0, len-1);
  @ assigns arr[0..len-1];
  @*/
void sort_array(int *arr, int len) {
    // implementation
}
```

### Pattern 3: Class Invariants

**Code:**
```python
class BankAccount:
    def __init__(self, account_number, initial_balance):
        self.account_number = account_number
        self.balance = initial_balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if self.balance < amount:
            raise InsufficientFundsError()
        self.balance -= amount
```

**Generated specification:**
```python
class BankAccount:
    """
    Bank account with balance and account number.

    Class Invariants:
        - balance >= 0 (balance never negative)
        - account_number is immutable (never changes after init)
        - account_number is unique (within system)
    """

    def __init__(self, account_number: str, initial_balance: float) -> None:
        """
        Create new bank account.

        Preconditions:
            - account_number is not None and not empty
            - initial_balance >= 0
            - account_number not already in use

        Postconditions:
            - self.account_number == account_number
            - self.balance == initial_balance
            - Invariants established
        """
        if not account_number:
            raise ValueError("Account number required")
        if initial_balance < 0:
            raise ValueError("Initial balance cannot be negative")

        self.account_number = account_number
        self.balance = initial_balance

    def deposit(self, amount: float) -> None:
        """
        Deposit amount into account.

        Preconditions:
            - amount > 0
            - Invariants hold

        Postconditions:
            - self.balance == old(self.balance) + amount
            - Invariants still hold

        Frame conditions:
            - Only self.balance modified
            - account_number unchanged
        """
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self.balance += amount
        assert self.balance >= 0  # Invariant check

    def withdraw(self, amount: float) -> None:
        """
        Withdraw amount from account.

        Preconditions:
            - amount > 0
            - self.balance >= amount
            - Invariants hold

        Postconditions:
            - self.balance == old(self.balance) - amount
            - Invariants still hold

        Exceptional postconditions:
            - If balance < amount: InsufficientFundsError raised
            - If balance < amount: balance unchanged
        """
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if self.balance < amount:
            raise InsufficientFundsError()
        self.balance -= amount
        assert self.balance >= 0  # Invariant check
```

**JML version:**
```java
public class BankAccount {
    /*@ invariant balance >= 0;
      @ invariant account_number != null;
      @*/
    private /*@ spec_public @*/ double balance;
    private /*@ spec_public @*/ final String account_number;

    /*@ requires account_number != null;
      @ requires initial_balance >= 0;
      @ ensures this.account_number == account_number;
      @ ensures this.balance == initial_balance;
      @*/
    public BankAccount(String account_number, double initial_balance) {
        // implementation
    }

    /*@ requires amount > 0;
      @ ensures balance == \old(balance) + amount;
      @ assignable balance;
      @*/
    public void deposit(double amount) {
        // implementation
    }

    /*@ requires amount > 0;
      @ requires balance >= amount;
      @ ensures balance == \old(balance) - amount;
      @ signals (InsufficientFundsError e) \old(balance) < amount;
      @ assignable balance;
      @*/
    public void withdraw(double amount) throws InsufficientFundsError {
        // implementation
    }
}
```

### Pattern 4: Loop Invariants

**Code:**
```python
def sum_array(arr):
    total = 0
    for i in range(len(arr)):
        total += arr[i]
    return total
```

**Generated specification with loop invariants:**
```python
def sum_array(arr: List[int]) -> int:
    """
    Compute sum of all elements in array.

    Preconditions:
        - arr is not None

    Postconditions:
        - result == sum of all elements in arr
    """
    total = 0

    # Loop invariant:
    # - 0 <= i <= len(arr)
    # - total == sum(arr[0:i])
    # - total is sum of elements seen so far

    for i in range(len(arr)):
        # At this point:
        # - Invariant holds at loop entry
        # - i < len(arr)

        total += arr[i]

        # At this point:
        # - total == sum(arr[0:i+1])
        # - Invariant holds for next iteration

    # At loop exit:
    # - i == len(arr)
    # - total == sum(arr[0:len(arr)]) == sum(arr)

    return total
```

**Dafny version:**
```dafny
method SumArray(arr: array<int>) returns (total: int)
    requires arr != null
    ensures total == sum(arr[..])
{
    total := 0;
    var i := 0;

    while i < arr.Length
        invariant 0 <= i <= arr.Length
        invariant total == sum(arr[..i])
    {
        total := total + arr[i];
        i := i + 1;
    }
}
```

### Pattern 5: Binary Search Contract

**Code:**
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

**Generated specification:**
```python
def binary_search(arr: List[int], target: int) -> int:
    """
    Search for target in sorted array using binary search.

    Preconditions:
        - arr is not None
        - arr is sorted in ascending order:
          For all i, j: 0 <= i < j < len(arr) implies arr[i] <= arr[j]

    Postconditions:
        - If result >= 0: arr[result] == target
        - If result >= 0: 0 <= result < len(arr)
        - If result == -1: target not in arr
        - If multiple occurrences: returns any valid index
    """
    if arr is None:
        raise ValueError("Array cannot be None")

    left, right = 0, len(arr) - 1

    # Loop invariant:
    # - 0 <= left <= right + 1 <= len(arr)
    # - If target in arr, then target in arr[left:right+1]
    # - All elements in arr[0:left] < target
    # - All elements in arr[right+1:] > target

    while left <= right:
        mid = (left + right) // 2

        if arr[mid] == target:
            # Postcondition: arr[mid] == target
            return mid
        elif arr[mid] < target:
            left = mid + 1
            # Invariant maintained: arr[0:left] < target
        else:
            right = mid - 1
            # Invariant maintained: arr[right+1:] > target

    # Loop exit: left > right
    # Invariant implies target not in arr
    return -1
```

**ACSL version:**
```c
/*@ requires \valid_read(arr + (0..len-1));
  @ requires Sorted(arr, 0, len-1);
  @
  @ behavior found:
  @   ensures 0 <= \result < len;
  @   ensures arr[\result] == target;
  @
  @ behavior not_found:
  @   ensures \result == -1;
  @   ensures \forall integer i; 0 <= i < len ==> arr[i] != target;
  @
  @ complete behaviors;
  @ disjoint behaviors;
  @*/
int binary_search(int *arr, int len, int target) {
    int left = 0, right = len - 1;

    /*@ loop invariant 0 <= left <= right + 1 <= len;
      @ loop invariant \forall integer i; 0 <= i < left ==> arr[i] < target;
      @ loop invariant \forall integer i; right < i < len ==> arr[i] > target;
      @ loop variant right - left;
      @*/
    while (left <= right) {
        int mid = left + (right - left) / 2;
        if (arr[mid] == target) return mid;
        else if (arr[mid] < target) left = mid + 1;
        else right = mid - 1;
    }
    return -1;
}
```

### Pattern 6: Linked List Operations

**Code:**
```python
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

def reverse_list(head):
    prev = None
    current = head
    while current:
        next_node = current.next
        current.next = prev
        prev = current
        current = next_node
    return prev
```

**Generated specification:**
```python
class Node:
    """
    Linked list node.

    Invariants:
        - data can be any value
        - next is either None or a Node
    """
    def __init__(self, data: Any) -> None:
        """
        Create new node.

        Postconditions:
            - self.data == data
            - self.next == None
        """
        self.data = data
        self.next = None

def reverse_list(head: Optional[Node]) -> Optional[Node]:
    """
    Reverse a singly linked list in-place.

    Preconditions:
        - head is None or points to valid linked list
        - List is acyclic (no cycles)

    Postconditions:
        - Returns new head of reversed list
        - If head is None, returns None
        - Number of nodes unchanged
        - All data values preserved
        - Order of data values is reversed
        - Original list structure modified
        - If original: A -> B -> C -> None
          Then result: C -> B -> A -> None

    Frame conditions:
        - Only next pointers modified
        - data values unchanged
        - No new nodes created
        - No nodes deleted
    """
    prev = None
    current = head

    # Loop invariant:
    # - prev points to reversed portion
    # - current points to unreversed portion
    # - prev is reverse of head[0:processed]
    # - current is head[processed:]

    while current is not None:
        next_node = current.next
        current.next = prev
        prev = current
        current = next_node

        # Invariant maintained:
        # - Moved one node from unreversed to reversed
        # - All processed nodes are reversed and point to prev

    # Loop exit: current is None
    # prev points to new head (last original node)
    # All nodes reversed

    return prev
```

### Pattern 7: Concurrency Specifications

**Code:**
```python
from threading import Lock

class Counter:
    def __init__(self):
        self.value = 0
        self.lock = Lock()

    def increment(self):
        with self.lock:
            self.value += 1
```

**Generated specification:**
```python
class Counter:
    """
    Thread-safe counter.

    Class Invariants:
        - value >= 0
        - lock is always valid
        - value reflects total increments

    Concurrency Properties:
        - increment is atomic
        - Multiple threads can safely call increment
        - No race conditions
        - Each increment increases value by exactly 1
    """

    def __init__(self) -> None:
        """
        Create new counter.

        Postconditions:
            - self.value == 0
            - self.lock is initialized
            - Thread-safe operations enabled
        """
        self.value = 0
        self.lock = Lock()

    def increment(self) -> None:
        """
        Atomically increment counter by 1.

        Preconditions:
            - Counter is initialized

        Postconditions:
            - self.value == old(self.value) + 1
            - Operation is atomic (thread-safe)

        Concurrency guarantees:
            - Mutual exclusion: Only one thread in critical section
            - Progress: Non-blocking (eventually acquires lock)
            - No deadlock: Lock always released
            - Visibility: Changes visible to all threads
        """
        with self.lock:
            # Critical section
            old_value = self.value
            self.value += 1
            # Postcondition: self.value == old_value + 1
```

## Specification Templates

### Template 1: Simple Function
```python
def function_name(param1: Type1, param2: Type2) -> ReturnType:
    """
    [Brief description]

    :param param1: [Description]
    :param param2: [Description]
    :returns: [Description]
    :raises ExceptionType: [When]

    Preconditions:
        - [Condition on param1]
        - [Condition on param2]
        - [State requirement]

    Postconditions:
        - [Property of return value]
        - [State change]
        - [Side effect]
    """
```

### Template 2: Class with Invariants
```python
class ClassName:
    """
    [Description]

    Class Invariants:
        - [Property 1 always true]
        - [Property 2 always true]
    """

    def __init__(self, ...):
        """
        Preconditions: [...]
        Postconditions: [Invariants established]
        """

    def method(self, ...):
        """
        Preconditions: [Invariants hold, ...]
        Postconditions: [Invariants still hold, ...]
        """
```

### Template 3: Loop with Invariant
```python
# Loop invariant:
# - [Property true at loop entry and after each iteration]
# - [Relates loop variable to progress]
# - [Relates accumulator to partial result]

while condition:
    # Invariant holds here

    # Loop body

    # Invariant maintained
```

## Best Practices

1. **Be precise** - Specifications should be unambiguous
2. **Be complete** - Cover all cases (success and failure)
3. **Be minimal** - Don't over-specify implementation details
4. **Be verifiable** - Specifications should be checkable
5. **Document assumptions** - Make preconditions explicit
6. **Specify side effects** - Document state changes
7. **Include invariants** - Especially for classes and loops
8. **Handle exceptions** - Specify exceptional postconditions
9. **Consider concurrency** - Add thread-safety guarantees if needed
10. **Keep readable** - Specifications are documentation

## Common Specification Elements

### Quantifiers
- **For all** (∀): `for all i: 0 <= i < len(arr) implies arr[i] >= 0`
- **Exists** (∃): `exists i: 0 <= i < len(arr) and arr[i] == target`

### Old values
- `old(variable)` - Value before execution
- `\old(x)` (JML/ACSL) - Previous value of x

### Comparison operators
- `==` - Equality
- `!=` - Inequality
- `<, <=, >, >=` - Ordering
- `==>` - Implication
- `&&, ||` - Logical and/or

### Set operations
- `set(arr)` - Set of elements
- `len(arr)` - Length/size
- `arr[i:j]` - Slice/range

## Verification Considerations

### Static verification
- Use tools like Dafny, Why3, Frama-C
- Specifications must be formal and complete
- Proofs may require additional lemmas

### Runtime verification
- Add assertions to check contracts
- Use design-by-contract libraries
- Enable in development, optional in production

### Testing
- Specifications guide test generation
- Each precondition → boundary test
- Each postcondition → assertion in test
