---
name: python-gotchas
description: Complete Python gotchas reference. PROACTIVELY activate for: (1) Mutable default arguments, (2) Mutating lists while iterating, (3) is vs == comparison, (4) Late binding in closures, (5) Variable scope (LEGB), (6) Floating point precision, (7) Exception handling pitfalls, (8) Dict mutation during iteration, (9) Circular imports, (10) Class vs instance attributes. Provides: Problem explanations, code examples, fixes for each gotcha. Ensures bug-free Python code.
---

## Quick Reference

| Gotcha | Problem | Fix |
|--------|---------|-----|
| Mutable default | `def f(x=[])` | Use `None`, create in function |
| Iterate + mutate | Skips items | Iterate over copy `items[:]` |
| `is` vs `==` | Identity vs value | Use `is` only for `None` |
| Late binding | `lambda: i` captures var | `lambda i=i: i` |
| Float precision | `0.1 + 0.2 != 0.3` | `math.isclose()` |
| Dict mutation | RuntimeError | `list(d.keys())` |
| Class attribute | Shared mutable | Init in `__init__` |

| Falsy Values | Examples |
|--------------|----------|
| Boolean | `False` |
| None | `None` |
| Numbers | `0`, `0.0`, `0j` |
| Empty collections | `""`, `[]`, `{}`, `set()` |

| Scope Rule | Order |
|------------|-------|
| LEGB | Local → Enclosing → Global → Built-in |
| `global` | Access module-level variable |
| `nonlocal` | Access enclosing function variable |

## When to Use This Skill

Use for **debugging and prevention**:
- Understanding why code behaves unexpectedly
- Avoiding common Python pitfalls
- Reviewing code for subtle bugs
- Learning Python's evaluation rules
- Fixing mutable default arguments

**Related skills:**
- For fundamentals: see `python-fundamentals-313`
- For testing: see `python-testing`
- For type hints: see `python-type-hints`

---

# Python Common Gotchas and Pitfalls

## Overview

Python has several well-known pitfalls that trip up developers of all experience levels. Understanding these gotchas prevents subtle bugs and unexpected behavior.

## 1. Mutable Default Arguments

### The Problem

```python
# BAD: Mutable default argument
def add_item(item, items=[]):
    items.append(item)
    return items

# Unexpected behavior!
print(add_item("a"))  # ['a']
print(add_item("b"))  # ['a', 'b'] - NOT ['b']!
print(add_item("c"))  # ['a', 'b', 'c']
```

### Why It Happens

Default arguments are evaluated **once** when the function is defined, not each time it's called. The same list object is reused across all calls.

### The Fix

```python
# GOOD: Use None as default
def add_item(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items

# Works correctly
print(add_item("a"))  # ['a']
print(add_item("b"))  # ['b']
print(add_item("c"))  # ['c']
```

### Other Mutable Defaults

```python
# BAD: All mutable types have this issue
def bad_dict(data={}): ...
def bad_set(data=set()): ...
def bad_class(config=SomeClass()): ...

# GOOD: Always use None
def good_dict(data=None):
    if data is None:
        data = {}
    return data

def good_set(data=None):
    if data is None:
        data = set()
    return data
```

## 2. Mutating Lists While Iterating

### The Problem

```python
# BAD: Modifying list during iteration
numbers = [1, 2, 3, 4, 5, 6]
for num in numbers:
    if num % 2 == 0:
        numbers.remove(num)

print(numbers)  # [1, 3, 5] - missed 4!
```

### Why It Happens

The iterator uses indices internally. When you remove an item, all subsequent indices shift, causing items to be skipped.

### The Fixes

```python
# GOOD: Iterate over a copy
numbers = [1, 2, 3, 4, 5, 6]
for num in numbers[:]:  # Slice creates a copy
    if num % 2 == 0:
        numbers.remove(num)
print(numbers)  # [1, 3, 5]

# GOOD: Use list comprehension (preferred)
numbers = [1, 2, 3, 4, 5, 6]
numbers = [num for num in numbers if num % 2 != 0]
print(numbers)  # [1, 3, 5]

# GOOD: Use filter
numbers = [1, 2, 3, 4, 5, 6]
numbers = list(filter(lambda x: x % 2 != 0, numbers))
print(numbers)  # [1, 3, 5]

# GOOD: Iterate backwards (for in-place modification)
numbers = [1, 2, 3, 4, 5, 6]
for i in range(len(numbers) - 1, -1, -1):
    if numbers[i] % 2 == 0:
        del numbers[i]
print(numbers)  # [1, 3, 5]
```

## 3. `is` vs `==`

### The Problem

```python
# Comparing values vs identity
a = [1, 2, 3]
b = [1, 2, 3]

print(a == b)  # True - same values
print(a is b)  # False - different objects

# Integer interning gotcha
x = 256
y = 256
print(x is y)  # True (integers -5 to 256 are interned)

x = 257
y = 257
print(x is y)  # False! (outside interning range)
```

### The Rule

- Use `==` to compare **values**
- Use `is` only for **identity** (singletons like `None`, `True`, `False`)

```python
# GOOD: Correct usage
if value is None:
    ...

if value == other_value:
    ...

# BAD: Don't use `is` for value comparison
if value is 0:  # Wrong!
    ...
```

## 4. Variable Scope (LEGB)

### The Problem

```python
# Closure gotcha
functions = []
for i in range(3):
    functions.append(lambda: i)

# All return the same value!
print([f() for f in functions])  # [2, 2, 2]
```

### Why It Happens

The lambda captures the **variable** `i`, not its **value**. By the time lambdas are called, `i` is 2.

### The Fixes

```python
# GOOD: Capture value with default argument
functions = []
for i in range(3):
    functions.append(lambda i=i: i)  # Default arg captures value
print([f() for f in functions])  # [0, 1, 2]

# GOOD: Use functools.partial
from functools import partial

def return_value(x):
    return x

functions = [partial(return_value, i) for i in range(3)]
print([f() for f in functions])  # [0, 1, 2]
```

### UnboundLocalError

```python
# BAD: This raises UnboundLocalError
x = 10

def increment():
    x = x + 1  # Error! x is local but used before assignment
    return x

# GOOD: Use global (sparingly)
def increment():
    global x
    x = x + 1
    return x

# BETTER: Avoid global, pass as parameter
def increment(x):
    return x + 1
```

## 5. String Concatenation

### Implicit Concatenation Gotcha

```python
# Missing comma creates concatenation
items = [
    "apple"
    "banana"  # Oops! Missing comma
    "cherry"
]
print(items)  # ['applebanana', 'cherry']

# CORRECT
items = [
    "apple",
    "banana",
    "cherry",
]
```

### Type Mixing

```python
# BAD: Can't concatenate str and int
name = "User"
count = 42
# message = "Hello " + name + ", you have " + count + " messages"  # TypeError!

# GOOD: Use f-strings
message = f"Hello {name}, you have {count} messages"

# GOOD: Use str()
message = "Hello " + name + ", you have " + str(count) + " messages"
```

## 6. Late Binding in Closures

### The Problem

```python
# Class method gotcha
class MyClass:
    def __init__(self, callbacks=[]):  # BAD: Mutable default!
        self.callbacks = callbacks

    def add_callback(self, func):
        self.callbacks.append(func)

obj1 = MyClass()
obj2 = MyClass()
obj1.add_callback(lambda: print("Hello"))

# obj2 also has the callback!
print(len(obj2.callbacks))  # 1
```

### The Fix

```python
class MyClass:
    def __init__(self, callbacks=None):
        self.callbacks = callbacks if callbacks is not None else []

    def add_callback(self, func):
        self.callbacks.append(func)
```

## 7. Boolean Evaluation

### Falsy Values

```python
# These are all falsy
falsy_values = [
    False,
    None,
    0,
    0.0,
    0j,
    "",
    [],
    {},
    set(),
    range(0),
]

# Gotcha: Empty collections are falsy
data = []
if data:
    print("Has data")  # Not printed
else:
    print("No data")   # Printed

# But None and empty are different!
if data is None:
    print("Is None")      # Not printed
elif data == []:
    print("Is empty list")  # Printed
```

### Explicit Checks

```python
# BAD: Ambiguous check
def process(items):
    if not items:  # Could be None OR empty
        return

# GOOD: Be explicit about what you're checking
def process(items):
    if items is None:
        raise ValueError("items cannot be None")
    if len(items) == 0:
        return  # Early return for empty list
```

## 8. Floating Point Precision

### The Problem

```python
# Floating point arithmetic isn't exact
print(0.1 + 0.2)  # 0.30000000000000004
print(0.1 + 0.2 == 0.3)  # False!
```

### The Fixes

```python
import math
from decimal import Decimal

# GOOD: Use math.isclose for comparisons
print(math.isclose(0.1 + 0.2, 0.3))  # True

# GOOD: Use Decimal for financial calculations
price = Decimal("19.99")
tax = Decimal("0.0875")
total = price * (1 + tax)
print(total)  # 21.739125

# Round appropriately
print(round(total, 2))  # 21.74
```

## 9. Exception Handling

### Bare Except

```python
# BAD: Catches everything, including KeyboardInterrupt
try:
    risky_operation()
except:
    pass

# BAD: Too broad
try:
    risky_operation()
except Exception:
    pass  # Silently ignores all errors

# GOOD: Catch specific exceptions
try:
    risky_operation()
except ValueError as e:
    logger.error(f"Invalid value: {e}")
except ConnectionError as e:
    logger.error(f"Connection failed: {e}")
    raise  # Re-raise after logging
```

### Exception Variable Scope

```python
# Python 3: Exception variable is deleted after except block
try:
    1 / 0
except ZeroDivisionError as e:
    error = e  # Save if needed
    print(e)

# print(e)  # NameError! e is deleted
print(error)  # OK
```

## 10. Dictionary Key Ordering

### Modern Python (3.7+)

```python
# Since Python 3.7, dicts maintain insertion order
d = {"b": 2, "a": 1, "c": 3}
print(list(d.keys()))  # ['b', 'a', 'c'] - insertion order

# But comparison ignores order
d1 = {"a": 1, "b": 2}
d2 = {"b": 2, "a": 1}
print(d1 == d2)  # True
```

### Gotcha: Changing Dict During Iteration

```python
# BAD: RuntimeError
d = {"a": 1, "b": 2, "c": 3}
for key in d:
    if d[key] == 2:
        del d[key]  # RuntimeError: dictionary changed size during iteration

# GOOD: Iterate over copy of keys
d = {"a": 1, "b": 2, "c": 3}
for key in list(d.keys()):
    if d[key] == 2:
        del d[key]
print(d)  # {'a': 1, 'c': 3}

# GOOD: Dict comprehension
d = {"a": 1, "b": 2, "c": 3}
d = {k: v for k, v in d.items() if v != 2}
```

## 11. Import Gotchas

### Circular Imports

```python
# module_a.py
from module_b import func_b  # Fails if module_b imports from module_a

def func_a():
    return func_b()

# SOLUTION: Import inside function
def func_a():
    from module_b import func_b
    return func_b()

# OR: Import module, not function
import module_b

def func_a():
    return module_b.func_b()
```

### Module Name Shadowing

```python
# BAD: File named random.py shadows stdlib
# random.py (your file)
import random  # Imports YOUR file, not stdlib!
random.randint(1, 10)  # AttributeError

# Python 3.13 now warns about this!
```

## 12. Class Attribute vs Instance Attribute

```python
class MyClass:
    shared_list = []  # Class attribute - shared by all instances!

    def add_item(self, item):
        self.shared_list.append(item)

a = MyClass()
b = MyClass()
a.add_item("hello")
print(b.shared_list)  # ['hello'] - Oops!

# GOOD: Initialize in __init__
class MyClass:
    def __init__(self):
        self.items = []  # Instance attribute - unique to each instance

    def add_item(self, item):
        self.items.append(item)
```

## Quick Reference

| Gotcha | Problem | Solution |
|--------|---------|----------|
| Mutable defaults | `def f(x=[])` | Use `None`, create in function |
| Mutating while iterating | Skips items | Iterate over copy or use comprehension |
| `is` vs `==` | Identity vs equality | Use `is` only for `None`, `True`, `False` |
| Late binding | Captures variable, not value | Use default argument to capture |
| Falsy values | Empty != None | Be explicit in checks |
| Float precision | 0.1 + 0.2 != 0.3 | Use `math.isclose()` or `Decimal` |
| Bare except | Catches too much | Catch specific exceptions |
| Dict iteration | Can't modify during | Iterate over `list(d.keys())` |
| Circular imports | Import errors | Import inside function or import module |
| Class attributes | Shared unexpectedly | Initialize in `__init__` |
