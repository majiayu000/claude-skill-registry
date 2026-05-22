---
name: refactoring-patterns
description: This skill provides patterns for safe, systematic refactoring including extract, rename, move, and simplification operations with proper testing and rollback strategies.
context: fork
user-invocable: false
---

# Refactoring Patterns Skill

Systematic refactoring with safety checks and verification.

## When to Use

- Extracting methods, classes, or modules
- Renaming identifiers safely across codebase
- Moving code between files or modules
- Simplifying complex code
- Modernizing legacy patterns

## Reference Documents

- [Extract Patterns](./references/extract-patterns.md) - Extract method/class/module patterns
- [Rename Patterns](./references/rename-patterns.md) - Safe renaming across codebase
- [Move Patterns](./references/move-patterns.md) - Moving code between files/modules
- [Simplify Patterns](./references/simplify-patterns.md) - Reducing complexity patterns

## Core Principles

### 1. Never Refactor Without Tests

```markdown
BEFORE refactoring:
1. Ensure tests exist for code being changed
2. Run tests to confirm they pass
3. Note coverage percentage

DURING refactoring:
4. Run tests after each small change
5. Keep changes atomic and reversible

AFTER refactoring:
6. Run full test suite
7. Verify coverage didn't decrease
```

### 2. Small, Incremental Changes

```
BAD:  One massive PR that changes everything
GOOD: Series of small PRs, each working state

Commit 1: Add new class
Commit 2: Add tests for new class
Commit 3: Migrate first usage
Commit 4: Migrate remaining usages
Commit 5: Remove old code
```

### 3. Preserve Behavior

Refactoring changes structure, not behavior.

```python
# BEFORE
def calculate_total(items):
    total = 0
    for item in items:
        total += item.price * item.quantity
    return total

# AFTER (same behavior, different structure)
def calculate_total(items):
    return sum(item.price * item.quantity for item in items)
```

## Refactoring Workflow

### Step 1: Identify the Smell

| Code Smell | Refactoring |
|------------|-------------|
| Long method | Extract Method |
| Large class | Extract Class |
| Duplicated code | Extract Method/Class |
| Long parameter list | Introduce Parameter Object |
| Data clumps | Extract Class |
| Primitive obsession | Replace Primitive with Object |
| Switch statements | Replace with Polymorphism |
| Parallel inheritance | Collapse Hierarchy |

### Step 2: Ensure Test Coverage

```bash
# Check current coverage
pytest --cov=module_to_refactor --cov-report=term-missing

# If coverage < 80%, add tests first
pytest tests/test_module.py -v
```

### Step 3: Apply Refactoring

Execute refactoring in small steps:

```markdown
Extract Method Example:
1. [ ] Identify code to extract
2. [ ] Create new method with extracted code
3. [ ] Replace original code with method call
4. [ ] Run tests
5. [ ] Commit
```

### Step 4: Verify

```bash
# Run tests
pytest

# Check for regressions
git diff HEAD~1 --stat

# Review changes
git diff HEAD~1 path/to/file.py
```

## Common Refactorings

### Extract Method

```python
# BEFORE
def process_order(order):
    # Validate order
    if not order.items:
        raise ValueError("Order has no items")
    if order.total <= 0:
        raise ValueError("Order total must be positive")

    # Calculate discount
    discount = 0
    if order.customer.is_premium:
        discount = order.total * 0.1

    # Process payment
    payment = Payment(amount=order.total - discount)
    payment.process()

# AFTER
def process_order(order):
    validate_order(order)
    discount = calculate_discount(order)
    process_payment(order, discount)

def validate_order(order):
    if not order.items:
        raise ValueError("Order has no items")
    if order.total <= 0:
        raise ValueError("Order total must be positive")

def calculate_discount(order):
    if order.customer.is_premium:
        return order.total * 0.1
    return 0

def process_payment(order, discount):
    payment = Payment(amount=order.total - discount)
    payment.process()
```

### Extract Class

```python
# BEFORE
class Order:
    def __init__(self):
        self.items = []
        self.shipping_address_line1 = ""
        self.shipping_address_line2 = ""
        self.shipping_city = ""
        self.shipping_state = ""
        self.shipping_zip = ""
        self.shipping_country = ""

    def format_shipping_address(self):
        return f"{self.shipping_address_line1}\n{self.shipping_city}, {self.shipping_state}"

# AFTER
class Address:
    def __init__(self, line1, line2, city, state, zip_code, country):
        self.line1 = line1
        self.line2 = line2
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.country = country

    def format(self):
        return f"{self.line1}\n{self.city}, {self.state}"

class Order:
    def __init__(self):
        self.items = []
        self.shipping_address = None
```

### Rename

```bash
# Safe rename using IDE/tools
# In VS Code: F2 on symbol
# In PyCharm: Shift+F6

# Manual rename with verification
grep -rn "old_name" --include="*.py"
# Replace all occurrences
sed -i 's/old_name/new_name/g' path/to/files/*.py
# Run tests
pytest
```

## Safety Checklist

Before refactoring:
- [ ] Tests exist and pass
- [ ] Coverage is adequate (>80%)
- [ ] Changes are scoped and understood
- [ ] Rollback plan exists

During refactoring:
- [ ] Make one change at a time
- [ ] Run tests after each change
- [ ] Commit working states

After refactoring:
- [ ] All tests pass
- [ ] Coverage maintained or improved
- [ ] No behavior changes (unless intentional)
- [ ] Code review completed

## Quick Reference

| Refactoring | When to Use | Risk |
|-------------|-------------|------|
| Rename | Unclear names | Low |
| Extract Method | Long methods | Low |
| Inline Method | Unnecessary indirection | Low |
| Extract Class | Large class | Medium |
| Move Method | Method in wrong class | Medium |
| Replace Conditional with Polymorphism | Complex conditionals | High |
| Change Method Signature | API changes | High |
