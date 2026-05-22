---
name: pythonic-conventions
description: Essential Pythonic idioms and conventions. Apply when writing or reviewing Python code to ensure idiomatic patterns like comprehensions, built-in functions, context managers, and unpacking.
user-invocable: false
---

# Pythonic Conventions

Essential Python idioms that make code more readable, concise, and efficient.

## Quick Reference

| Pattern | Use Instead Of |
|---------|----------------|
| List/dict/set comprehensions | Manual loops to build collections |
| `enumerate()` | Manual index tracking |
| `zip()` | Manual parallel iteration |
| `any()` / `all()` | Loop with flag variable |
| Context managers (`with`) | Manual resource cleanup |
| Unpacking | Index access for known structures |
| `in` operator | Manual membership loops |
| Walrus operator (`:=`) | Separate assignment + condition |
| Generator expressions | List comprehension when iterating once |
| `defaultdict` / `Counter` | Manual dict initialization |

---

## Comprehensions Over Loops

Use comprehensions to build lists, dicts, and sets. They're more readable and often faster.

### List Comprehensions

```python
# INCORRECT - manual loop
squares = []
for x in range(10):
    squares.append(x ** 2)

# CORRECT - list comprehension
squares = [x ** 2 for x in range(10)]

# CORRECT - with condition
even_squares = [x ** 2 for x in range(10) if x % 2 == 0]
```

### Dict Comprehensions

```python
# INCORRECT - manual loop
name_to_length = {}
for name in names:
    name_to_length[name] = len(name)

# CORRECT - dict comprehension
name_to_length = {name: len(name) for name in names}

# CORRECT - transform keys/values
upper_mapping = {k.upper(): v * 2 for k, v in mapping.items()}
```

### Set Comprehensions

```python
# INCORRECT - manual loop
unique_lengths = set()
for word in words:
    unique_lengths.add(len(word))

# CORRECT - set comprehension
unique_lengths = {len(word) for word in words}
```

### When NOT to Use Comprehensions

```python
# INCORRECT - comprehension too complex (nested + multiple conditions)
result = [
    transform(x, y)
    for x in items
    if is_valid(x)
    for y in x.children
    if y.active and y.score > threshold
]

# CORRECT - use a loop for complex logic
result = []
for x in items:
    if not is_valid(x):
        continue
    for y in x.children:
        if y.active and y.score > threshold:
            result.append(transform(x, y))
```

---

## Built-in Functions

### `enumerate()` for Index + Value

```python
# INCORRECT - manual index tracking
i = 0
for item in items:
    print(f"{i}: {item}")
    i += 1

# INCORRECT - range with index access
for i in range(len(items)):
    print(f"{i}: {items[i]}")

# CORRECT - enumerate
for i, item in enumerate(items):
    print(f"{i}: {item}")

# CORRECT - custom start index
for i, item in enumerate(items, start=1):
    print(f"{i}: {item}")
```

### `zip()` for Parallel Iteration

```python
# INCORRECT - manual parallel iteration
for i in range(len(names)):
    print(f"{names[i]}: {scores[i]}")

# CORRECT - zip
for name, score in zip(names, scores):
    print(f"{name}: {score}")

# CORRECT - strict mode (raises on length mismatch)
for name, score in zip(names, scores, strict=True):
    print(f"{name}: {score}")
```

### `any()` and `all()` for Boolean Checks

```python
# INCORRECT - loop with flag
has_negative = False
for x in numbers:
    if x < 0:
        has_negative = True
        break

# CORRECT - any()
has_negative = any(x < 0 for x in numbers)

# INCORRECT - loop with flag for all
all_positive = True
for x in numbers:
    if x <= 0:
        all_positive = False
        break

# CORRECT - all()
all_positive = all(x > 0 for x in numbers)
```

### `sum()`, `max()`, `min()` with Generators

```python
# INCORRECT - manual summation
total = 0
for item in items:
    total += item.value

# CORRECT - sum with generator
total = sum(item.value for item in items)

# CORRECT - max/min with key function
oldest = max(users, key=lambda u: u.age)
shortest = min(strings, key=len)
```

### `sorted()` with Key Functions

```python
# INCORRECT - manual sort key extraction
pairs = [(len(s), s) for s in strings]
pairs.sort()
sorted_strings = [s for _, s in pairs]

# CORRECT - sorted with key
sorted_strings = sorted(strings, key=len)

# CORRECT - sort by multiple criteria
sorted_users = sorted(users, key=lambda u: (u.department, -u.salary))
```

---

## Context Managers

Always use `with` for resource management.

```python
# INCORRECT - manual cleanup
f = open("file.txt")
try:
    data = f.read()
finally:
    f.close()

# CORRECT - context manager
with open("file.txt") as f:
    data = f.read()

# CORRECT - multiple resources
with open("input.txt") as infile, open("output.txt", "w") as outfile:
    outfile.write(infile.read())
```

### Common Context Managers

```python
# File I/O
with open(path) as f:
    ...

# Locks
with lock:
    ...

# Database connections
with connection.cursor() as cursor:
    ...

# Temporary directories
with tempfile.TemporaryDirectory() as tmpdir:
    ...

# Suppressing exceptions
with contextlib.suppress(FileNotFoundError):
    os.remove(path)
```

---

## Unpacking

### Tuple/List Unpacking

```python
# INCORRECT - index access
point = (3, 4)
x = point[0]
y = point[1]

# CORRECT - unpacking
x, y = point

# CORRECT - swap without temp variable
a, b = b, a

# CORRECT - extended unpacking
first, *rest = items
first, *middle, last = items
```

### Dict Unpacking

```python
# CORRECT - merge dicts
merged = {**defaults, **overrides}

# CORRECT - function kwargs
config = {"timeout": 30, "retries": 3}
response = fetch_data(url, **config)
```

### Unpacking in Loops

```python
# INCORRECT - index access
for pair in pairs:
    print(f"{pair[0]}: {pair[1]}")

# CORRECT - unpacking
for key, value in pairs:
    print(f"{key}: {value}")

# CORRECT - with enumerate
for i, (key, value) in enumerate(mapping.items()):
    print(f"{i}: {key}={value}")
```

---

## Membership Testing

```python
# INCORRECT - loop for membership
found = False
for item in items:
    if item == target:
        found = True
        break

# CORRECT - in operator
found = target in items

# CORRECT - use sets for repeated membership tests
allowed = {"admin", "moderator", "user"}
if role in allowed:
    ...
```

---

## Walrus Operator (`:=`)

Use assignment expressions to avoid redundant calls or lines.

```python
# INCORRECT - call twice or use temp variable
match = pattern.search(text)
if match:
    process(match.group())

# CORRECT - walrus operator
if match := pattern.search(text):
    process(match.group())

# CORRECT - in while loops
while chunk := file.read(8192):
    process(chunk)

# CORRECT - in comprehensions with filtering
results = [y for x in data if (y := expensive_compute(x)) is not None]
```

---

## Generators Over Lists

Use generator expressions when you only iterate once.

```python
# INCORRECT - creates full list in memory
total = sum([x ** 2 for x in range(1_000_000)])

# CORRECT - generator expression (no brackets)
total = sum(x ** 2 for x in range(1_000_000))

# CORRECT - generator function for complex logic
def read_large_file(path: Path) -> Iterator[str]:
    with open(path) as f:
        for line in f:
            if line.strip():
                yield line.strip()
```

---

## Collections Module

### `defaultdict`

```python
# INCORRECT - manual key initialization
groups = {}
for item in items:
    if item.category not in groups:
        groups[item.category] = []
    groups[item.category].append(item)

# CORRECT - defaultdict
from collections import defaultdict

groups = defaultdict(list)
for item in items:
    groups[item.category].append(item)
```

### `Counter`

```python
# INCORRECT - manual counting
counts = {}
for word in words:
    counts[word] = counts.get(word, 0) + 1

# CORRECT - Counter
from collections import Counter

counts = Counter(words)
most_common = counts.most_common(10)
```

---

## String Operations

### `str.join()` for Concatenation

```python
# INCORRECT - concatenation in loop
result = ""
for word in words:
    result += word + " "

# CORRECT - join
result = " ".join(words)
```

### F-strings Over Format/Concatenation

```python
# INCORRECT - old-style formatting
msg = "Hello, %s! You have %d messages." % (name, count)
msg = "Hello, {}! You have {} messages.".format(name, count)

# CORRECT - f-string
msg = f"Hello, {name}! You have {count} messages."

# CORRECT - f-string with expressions
msg = f"Total: {price * quantity:.2f}"
```

---

## Boolean Expressions

### Truthy/Falsy Checks

```python
# INCORRECT - explicit comparison
if len(items) > 0:
    ...
if len(items) == 0:
    ...
if value == None:
    ...
if value == True:
    ...

# CORRECT - truthy/falsy
if items:
    ...
if not items:
    ...
if value is None:
    ...
if value is True:  # Only when specifically checking True, not truthy
    ...
if value:  # Usually preferred for boolean check
    ...
```

### Chained Comparisons

```python
# INCORRECT - separate comparisons
if x > 0 and x < 10:
    ...

# CORRECT - chained comparison
if 0 < x < 10:
    ...
```

---

## Conditional Expressions

```python
# INCORRECT - if/else for simple assignment
if condition:
    value = x
else:
    value = y

# CORRECT - conditional expression
value = x if condition else y

# CORRECT - with function calls
status = "active" if user.is_active else "inactive"
```

---

## Dictionary Operations

### `dict.get()` with Default

```python
# INCORRECT - explicit key check
if key in d:
    value = d[key]
else:
    value = default

# CORRECT - get with default
value = d.get(key, default)
```

### `defaultdict` for Lazy Initialization

```python
# INCORRECT - check then set
if key not in d:
    d[key] = []
d[key].append(item)

# INCORRECT - setdefault (prefer defaultdict for clarity)
d.setdefault(key, []).append(item)

# CORRECT - defaultdict
from collections import defaultdict

d = defaultdict(list)
d[key].append(item)
```

---

## Exception Handling

### EAFP Over LBYL

Easier to Ask Forgiveness than Permission.

```python
# INCORRECT - LBYL (Look Before You Leap)
if key in mapping:
    value = mapping[key]
else:
    value = default

# CORRECT - EAFP
try:
    value = mapping[key]
except KeyError:
    value = default

# Even better for this case
value = mapping.get(key, default)
```

### Specific Exception Types

```python
# INCORRECT - bare except
try:
    result = risky_operation()
except:
    handle_error()

# INCORRECT - too broad
try:
    result = risky_operation()
except Exception:
    handle_error()

# CORRECT - specific exceptions
try:
    result = risky_operation()
except (ValueError, TypeError) as e:
    handle_error(e)
```
