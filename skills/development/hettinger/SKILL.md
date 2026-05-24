---
name: hettinger-idiomatic-python
description: Write Python code in the style of Raymond Hettinger, Python core developer. Emphasizes beautiful, idiomatic code using iterators, generators, and built-in tools elegantly. Use when transforming code into clean, Pythonic solutions.
---

# Raymond Hettinger Style Guide

## Overview

Raymond Hettinger is a Python core developer famous for his talks on transforming code into beautiful, idiomatic Python. His mantra "There must be a better way!" drives the pursuit of elegant solutions using Python's rich toolkit.

## Core Philosophy

> "There must be a better way!"

> "If you copy-paste code, you're doing it wrong."

> "The goal is not to teach Python, but to teach programming using Python."

Hettinger believes Python's beauty lies in its tools—iterators, generators, decorators—and knowing when and how to use them transforms mediocre code into elegant solutions.

## Design Principles

1. **Use the Right Tool**: Python has tools for everything. Find them.

2. **Iterate, Don't Index**: Let Python handle the iteration machinery.

3. **Compose Small Functions**: Build complex behavior from simple, reusable pieces.

4. **Embrace Generators**: Lazy evaluation is memory-efficient and composable.

## When Writing Code

### Always

- Use `collections` module (Counter, defaultdict, deque, namedtuple)
- Use `itertools` for iterator algebra
- Use `functools` for function composition
- Prefer generators over building lists
- Use descriptive names that read like prose
- Chain operations fluently when appropriate

### Never

- Build lists just to iterate over them once
- Write nested loops when `itertools.product` works
- Manually implement what `itertools` provides
- Use indices when direct iteration works
- Repeat code—abstract it

### Prefer

- `collections.Counter` over manual counting
- `collections.defaultdict` over `.setdefault()`
- `itertools.chain` over nested loops
- `itertools.groupby` over manual grouping
- Generator expressions over list comprehensions (when iterating once)
- `functools.lru_cache` over manual memoization

## Code Patterns

### The Collections Module

```python
# BAD: Manual counting
word_counts = {}
for word in words:
    if word in word_counts:
        word_counts[word] += 1
    else:
        word_counts[word] = 1

# GOOD: Counter
from collections import Counter
word_counts = Counter(words)

# Bonus: most_common gives sorted results
top_ten = word_counts.most_common(10)


# BAD: Manual grouping
groups = {}
for item in items:
    key = get_key(item)
    if key not in groups:
        groups[key] = []
    groups[key].append(item)

# GOOD: defaultdict
from collections import defaultdict
groups = defaultdict(list)
for item in items:
    groups[get_key(item)].append(item)


# BAD: Tuple indexing
point = (10, 20, 30)
x = point[0]
y = point[1]

# GOOD: namedtuple
from collections import namedtuple
Point = namedtuple('Point', ['x', 'y', 'z'])
point = Point(10, 20, 30)
print(point.x, point.y)  # Clear and self-documenting
```

### The itertools Module

```python
from itertools import chain, groupby, product, combinations, islice

# Flatten nested lists
nested = [[1, 2], [3, 4], [5, 6]]
flat = list(chain.from_iterable(nested))  # [1, 2, 3, 4, 5, 6]

# All combinations
for a, b in combinations([1, 2, 3, 4], 2):
    print(a, b)  # (1,2), (1,3), (1,4), (2,3), (2,4), (3,4)

# Cartesian product (replaces nested loops)
# BAD:
for x in xs:
    for y in ys:
        for z in zs:
            process(x, y, z)

# GOOD:
for x, y, z in product(xs, ys, zs):
    process(x, y, z)

# Take first N items from any iterable
first_ten = list(islice(huge_generator, 10))

# Group consecutive items
data = [('A', 1), ('A', 2), ('B', 3), ('B', 4)]
for key, group in groupby(data, key=lambda x: x[0]):
    print(key, list(group))
```

### Generator Excellence

```python
# BAD: Build entire list in memory
def get_squares(n):
    result = []
    for i in range(n):
        result.append(i ** 2)
    return result

# GOOD: Generator (lazy, memory-efficient)
def get_squares(n):
    for i in range(n):
        yield i ** 2

# BETTER: Generator expression
squares = (i ** 2 for i in range(n))

# Chaining generators (no intermediate lists!)
def pipeline(data):
    cleaned = (clean(item) for item in data)
    validated = (item for item in cleaned if is_valid(item))
    transformed = (transform(item) for item in validated)
    return transformed

# Only processes items as needed
for result in pipeline(huge_dataset):
    process(result)
```

### Decorator Patterns

```python
from functools import wraps, lru_cache, partial

# Memoization made easy
@lru_cache(maxsize=128)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

# Custom decorator template
def my_decorator(func):
    @wraps(func)  # Preserves function metadata
    def wrapper(*args, **kwargs):
        # Before
        result = func(*args, **kwargs)
        # After
        return result
    return wrapper

# Decorator with arguments
def repeat(times):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(3)
def greet(name):
    print(f"Hello, {name}!")
```

### Sorting Idioms

```python
# Sort by key
students = [('Alice', 85), ('Bob', 90), ('Charlie', 85)]

# Sort by grade (descending), then name (ascending)
sorted_students = sorted(students, key=lambda s: (-s[1], s[0]))

# Using operator module (faster)
from operator import itemgetter, attrgetter

# For tuples/lists
sorted_students = sorted(students, key=itemgetter(1), reverse=True)

# For objects
sorted_users = sorted(users, key=attrgetter('last_name', 'first_name'))
```

## Mental Model

Hettinger approaches code by asking:

1. **Is there a built-in for this?** Check `collections`, `itertools`, `functools` first
2. **Can I use a generator?** Process one item at a time, not all at once
3. **Can I compose existing tools?** Chain small operations together
4. **Would a decorator help?** Cross-cutting concerns belong in decorators

## Signature Hettinger Moves

- Replace manual loops with `sum()`, `any()`, `all()`, `max()`, `min()`
- Replace index access with `zip()`, `enumerate()`, unpacking
- Replace manual caching with `@lru_cache`
- Replace nested loops with `itertools.product`
- Replace manual counting with `collections.Counter`

