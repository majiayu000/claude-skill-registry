---
name: static-reasoning-verifier
description: "Verify code correctness statically against specifications using type checking, contract verification, and formal methods. Use when: (1) Verifying type safety and null safety in Python, Java, or C/C++ code, (2) Checking design-by-contract specifications (preconditions, postconditions, invariants), (3) Validating code against formal specifications, (4) Ensuring code quality and correctness before runtime, (5) Finding potential bugs through static analysis. Supports Python (mypy, contracts), Java (javac, JML), and provides verification scripts and contract specification guidelines."
---

# Static Reasoning Verifier

Verify code correctness statically against specifications through type checking, contract verification, and formal reasoning.

## Quick Start

### Verify Python Code

```bash
# Type checking and contract verification
python scripts/verify_python.py src/app.py

# Strict mode (enforce all type annotations)
python scripts/verify_python.py src/ --strict
```

### Verify Java Code

```bash
# Type checking, null safety, and JML contracts
python scripts/verify_java.py src/Main.java

# Strict mode (enforce JML contracts)
python scripts/verify_java.py src/ --strict
```

## Verification Types

### 1. Type Checking

Verify type correctness using static type checkers:

**Python (mypy)**:
```python
def add(a: int, b: int) -> int:
    return a + b

result: int = add(5, 10)  # ✅ Type safe
result: str = add(5, 10)  # ❌ Type error
```

**Java**:
```java
public int add(int a, int b) {
    return a + b;
}

int result = add(5, 10);    // ✅ Type safe
String result = add(5, 10); // ❌ Compile error
```

### 2. Contract Verification

Verify preconditions, postconditions, and invariants:

**Python**:
```python
def sqrt(x: float) -> float:
    """
    Calculate square root.

    Requires:
        - x >= 0

    Ensures:
        - result * result ≈ x
    """
    assert x >= 0, "Input must be non-negative"
    result = x ** 0.5
    assert abs(result * result - x) < 1e-10
    return result
```

**Java (JML)**:
```java
/*@ requires x >= 0;
  @ ensures \result >= 0;
  @ ensures \result * \result <= x;
  @*/
public static int sqrt(int x) {
    // Implementation
}
```

### 3. Null Safety

Verify null pointer safety:

**Java**:
```java
public @NonNull String getName(@NonNull User user) {
    return user.getName();  // Safe - user cannot be null
}
```

**Python**:
```python
from typing import Optional

def find_user(user_id: int) -> Optional[User]:
    """May return None if user not found."""
    return database.get_user(user_id)
```

## Verification Workflow

### 1. Write Specifications

Define contracts for functions/methods:

```python
def divide(a: float, b: float) -> float:
    """
    Divide two numbers.

    Precondition:
        - b != 0

    Postcondition:
        - result * b ≈ a

    Raises:
        ValueError: If b is zero
    """
    if b == 0:
        raise ValueError("Division by zero")
    return a / b
```

### 2. Add Type Annotations

```python
from typing import List, Optional

def process_items(items: List[int], threshold: int = 0) -> List[int]:
    """Filter items above threshold."""
    return [item for item in items if item > threshold]
```

### 3. Run Verification

```bash
# Verify implementation matches specifications
python scripts/verify_python.py src/
```

### 4. Review Issues

```
Found 3 issue(s): 1 error(s), 2 warning(s)

ERRORS:
  ❌ src/utils.py:15 [type]
     Argument 1 to "divide" has incompatible type "str"; expected "float"
     💡 Check argument type matches function signature

WARNINGS:
  ⚠️  src/math.py:42 [contract]
     Function 'sqrt' has parameters but no preconditions specified
     💡 Add 'Requires:' section in docstring or @requires decorator
```

### 5. Fix Issues

Update code to satisfy specifications:

```python
# Before (type error)
result = divide("10", 5)

# After (type safe)
result = divide(10.0, 5.0)
```

## Python Verification

### Type Checking with mypy

The verification script uses mypy for static type checking:

```bash
python scripts/verify_python.py src/ --strict
```

**Checks**:
- Type compatibility
- Function signatures
- Return types
- Optional/None handling

**Example**:
```python
def greet(name: str) -> str:
    return f"Hello, {name}"

greet("Alice")  # ✅ Valid
greet(123)      # ❌ Type error: expected str, got int
```

### Contract Verification

Checks design-by-contract specifications:

**Decorator-based**:
```python
from contracts import requires, ensures

@requires(lambda x: x >= 0)
@ensures(lambda result: result >= 0)
def sqrt(x: float) -> float:
    return x ** 0.5
```

**Docstring-based**:
```python
def withdraw(account: Account, amount: float) -> None:
    """
    Withdraw money from account.

    Requires:
        - amount > 0
        - amount <= account.balance

    Ensures:
        - account.balance == old(account.balance) - amount
    """
    assert amount > 0
    assert amount <= account.balance
    account.balance -= amount
```

See **[python_contracts.md](references/python_contracts.md)** for complete guide on Python design-by-contract patterns.

## Java Verification

### Type and Null Safety

The verification script uses javac for compilation and type checking:

```bash
python scripts/verify_java.py src/ --strict
```

**Checks**:
- Type compatibility
- Null safety annotations (@NonNull, @Nullable)
- Method signatures
- Generic type parameters

**Example**:
```java
public @NonNull String formatUser(@NonNull User user) {
    // user cannot be null
    return user.getName() + " (" + user.getEmail() + ")";
}

public @Nullable User findUser(int userId) {
    // May return null
    return database.getUser(userId);
}
```

### JML Contract Verification

Checks Java Modeling Language specifications:

```java
public class BankAccount {
    private double balance;

    /*@ invariant balance >= 0;
      @*/

    /*@ requires amount > 0;
      @ requires amount <= balance;
      @ ensures balance == \old(balance) - amount;
      @ assignable balance;
      @*/
    public void withdraw(double amount) {
        balance -= amount;
    }

    /*@ requires amount > 0;
      @ ensures balance == \old(balance) + amount;
      @ assignable balance;
      @*/
    public void deposit(double amount) {
        balance += amount;
    }
}
```

See **[java_jml.md](references/java_jml.md)** for complete JML specification guide.

## Common Verification Patterns

### Range Validation

```python
def set_age(person: Person, age: int) -> None:
    """
    Requires: 0 <= age <= 150
    Ensures: person.age == age
    """
    assert 0 <= age <= 150, "Age must be between 0 and 150"
    person.age = age
```

### Collection Constraints

```python
def process_batch(items: List[Item]) -> None:
    """
    Requires:
        - len(items) > 0
        - len(items) <= 1000
    """
    assert len(items) > 0, "Batch cannot be empty"
    assert len(items) <= 1000, "Batch too large"
    # Process items
```

### State Invariants

```python
class Stack:
    """
    Invariant:
        - 0 <= self.size <= self.capacity
        - All elements before size are not None
    """

    def push(self, item):
        """
        Requires: not self.is_full() and item is not None
        Ensures: self.size == old(self.size) + 1
        """
        assert not self.is_full()
        assert item is not None
        self.items[self.size] = item
        self.size += 1
        self._check_invariant()
```

## Best Practices

### 1. Write Contracts First

Define specifications before implementation:

```python
def sort_list(items: List[int]) -> List[int]:
    """
    Sort list in ascending order.

    Requires:
        - items is a list

    Ensures:
        - len(result) == len(items)
        - result is sorted ascending
        - result contains same elements as items
    """
    # Implementation here
```

### 2. Keep Contracts Simple

```python
# ✅ Good - Simple, clear
def withdraw(amount: float):
    """Requires: amount > 0 and amount <= balance"""
    assert amount > 0 and amount <= self.balance

# ❌ Bad - Too complex
def withdraw(amount: float):
    """Requires: (amount > 0 and amount <= balance) or (overdraft_allowed and amount <= balance + overdraft_limit)"""
```

### 3. Use Type Annotations Consistently

```python
# ✅ Good - All parameters and return types annotated
def calculate_total(items: List[Item], tax_rate: float) -> float:
    return sum(item.price for item in items) * (1 + tax_rate)

# ❌ Bad - Missing annotations
def calculate_total(items, tax_rate):
    return sum(item.price for item in items) * (1 + tax_rate)
```

### 4. Verify Early and Often

```bash
# Verify after every significant change
python scripts/verify_python.py src/

# Integrate into CI/CD
make verify  # Run verification in build pipeline
```

### 5. Document Side Effects

```python
def update_database(user: User) -> None:
    """
    Update user in database.

    Requires:
        - user.id is set

    Ensures:
        - Database contains updated user

    Side effects:
        - Modifies database
        - May raise DatabaseError
    """
```

## Troubleshooting

### Type Errors

**Problem**: Incompatible type error

**Solution**:
```python
# Add explicit type annotation or cast
result: int = int(value)  # Cast to int
result = cast(int, value)  # Type cast
```

**Problem**: Optional type handling

**Solution**:
```python
def get_name(user: Optional[User]) -> str:
    if user is None:
        return "Unknown"
    return user.name  # Safe - checked for None
```

### Contract Violations

**Problem**: Precondition failure

**Solution**:
```python
# Add validation before calling
if amount > 0 and amount <= account.balance:
    account.withdraw(amount)
else:
    raise ValueError("Invalid withdrawal amount")
```

**Problem**: Postcondition failure

**Solution**:
```python
# Verify implementation satisfies postcondition
def sqrt(x: float) -> float:
    result = x ** 0.5
    # Check postcondition
    assert abs(result * result - x) < 1e-10
    return result
```

## Reference Documentation

### Python Contracts
See **[python_contracts.md](references/python_contracts.md)** for:
- Design by contract patterns
- Preconditions, postconditions, invariants
- Decorator-based contracts (icontract, deal)
- Docstring specifications
- Type annotations as contracts
- Common contract patterns
- Verification checklist

### Java JML
See **[java_jml.md](references/java_jml.md)** for:
- JML syntax and semantics
- Preconditions (@requires)
- Postconditions (@ensures)
- Class invariants
- Quantifiers and pure methods
- Assignable clauses
- Null safety with JML
- OpenJML verification tools
- Loop invariants
- Contract inheritance

## Integration with Development Workflow

### Pre-commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

echo "Running static verification..."
python scripts/verify_python.py src/

if [ $? -ne 0 ]; then
    echo "Verification failed. Commit aborted."
    exit 1
fi
```

### CI/CD Pipeline

```yaml
# .github/workflows/verify.yml
name: Static Verification

on: [push, pull_request]

jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install mypy

      - name: Run verification
        run: python scripts/verify_python.py src/ --strict
```

### IDE Integration

Most IDEs support type checking and linting:
- **VS Code**: Python extension with mypy integration
- **PyCharm**: Built-in type checker
- **IntelliJ IDEA**: Java type checking and JML plugins
