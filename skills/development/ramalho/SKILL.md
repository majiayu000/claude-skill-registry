---
name: ramalho-fluent-python
description: Write Python code in the style of Luciano Ramalho, author of Fluent Python. Emphasizes deep understanding of Python's data model, special methods, and advanced idioms. Use when writing code that leverages Python's full power elegantly.
---

# Luciano Ramalho Style Guide

## Overview

Luciano Ramalho's "Fluent Python" is the definitive guide to writing idiomatic Python by understanding *how the language works*. His approach: master the data model, and Python becomes a consistent, powerful tool.

## Core Philosophy

> "Python is a language that lets you work at multiple levels of abstraction."

> "The Python data model describes the API that you can use to make your own objects play well with the most idiomatic language features."

Ramalho believes in understanding Python's **data model deeply**—the special methods that make your objects work seamlessly with Python's syntax and built-ins.

## Design Principles

1. **Master the Data Model**: Special methods (`__init__`, `__repr__`, `__iter__`, etc.) are how objects integrate with Python.

2. **Leverage Duck Typing**: Program to protocols, not specific types. If it quacks like a duck...

3. **Understand Mutability**: Know when objects are mutable or immutable, and design accordingly.

4. **Use Descriptors**: They're the mechanism behind `@property`, `@classmethod`, and `@staticmethod`.

## When Writing Code

### Always

- Implement `__repr__` for debugging (unambiguous)
- Implement `__str__` for user display (readable)
- Make objects iterable when it makes sense (`__iter__`)
- Use `@property` for computed attributes
- Understand the difference between `__getattr__` and `__getattribute__`
- Use `__slots__` for memory-heavy classes with many instances

### Never

- Implement `__repr__` that can't be copy-pasted to recreate the object
- Confuse `__str__` and `__repr__` purposes
- Ignore hashability requirements (`__hash__` and `__eq__` together)
- Make mutable objects hashable
- Override `__getattribute__` unless absolutely necessary

### Prefer

- `collections.abc` base classes for custom collections
- `@dataclass` for data-holding classes (Python 3.7+)
- Named tuples for simple immutable records
- Protocol classes for structural subtyping (Python 3.8+)

## Code Patterns

### The Essential Special Methods

```python
class Vector:
    """A 2D vector that plays well with Python."""
    
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
    
    def __repr__(self):
        # Unambiguous, ideally valid Python
        return f'Vector({self.x!r}, {self.y!r})'
    
    def __str__(self):
        # Readable for end users
        return f'({self.x}, {self.y})'
    
    def __eq__(self, other):
        if not isinstance(other, Vector):
            return NotImplemented
        return self.x == other.x and self.y == other.y
    
    def __hash__(self):
        # Only if immutable! Combine with XOR
        return hash((self.x, self.y))
    
    def __abs__(self):
        # Support abs(vector)
        return (self.x ** 2 + self.y ** 2) ** 0.5
    
    def __bool__(self):
        # Support if vector:
        return bool(abs(self))
    
    def __add__(self, other):
        if not isinstance(other, Vector):
            return NotImplemented
        return Vector(self.x + other.x, self.y + other.y)
    
    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)
    
    def __rmul__(self, scalar):
        # Support: 3 * vector (not just vector * 3)
        return self * scalar
```

### Making Objects Iterable

```python
class Sentence:
    """An iterable of words in a sentence."""
    
    def __init__(self, text):
        self.text = text
        self.words = text.split()
    
    def __iter__(self):
        # Return an iterator (can be a generator)
        return iter(self.words)
    
    def __len__(self):
        return len(self.words)
    
    def __getitem__(self, index):
        # Enables s[0], s[1:3], iteration fallback
        return self.words[index]
    
    def __contains__(self, word):
        # Enables: 'hello' in sentence
        return word in self.words


# Generator-based iteration (lazy, memory-efficient)
class SentenceLazy:
    def __init__(self, text):
        self.text = text
    
    def __iter__(self):
        for match in re.finditer(r'\w+', self.text):
            yield match.group()
```

### Context Managers

```python
# Class-based context manager
class DatabaseConnection:
    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.connection = None
    
    def __enter__(self):
        self.connection = connect(self.connection_string)
        return self.connection
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()
        # Return True to suppress exception, False to propagate
        return False


# Generator-based (simpler for many cases)
from contextlib import contextmanager

@contextmanager
def database_connection(connection_string):
    conn = connect(connection_string)
    try:
        yield conn
    finally:
        conn.close()
```

### Descriptors (The Power Behind Properties)

```python
class Validated:
    """A descriptor that validates values."""
    
    def __set_name__(self, owner, name):
        self.storage_name = name
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, f'_{self.storage_name}', None)
    
    def __set__(self, instance, value):
        value = self.validate(value)
        setattr(instance, f'_{self.storage_name}', value)
    
    def validate(self, value):
        raise NotImplementedError


class PositiveNumber(Validated):
    def validate(self, value):
        if value <= 0:
            raise ValueError(f'{self.storage_name} must be positive')
        return value


class Order:
    quantity = PositiveNumber()
    price = PositiveNumber()
    
    def __init__(self, quantity, price):
        self.quantity = quantity  # Uses descriptor
        self.price = price        # Uses descriptor
```

### Modern Python: Dataclasses and Protocols

```python
from dataclasses import dataclass, field
from typing import Protocol

# Dataclass: Less boilerplate for data-holding classes
@dataclass
class Point:
    x: float
    y: float
    
    def distance_from_origin(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5


# Protocol: Structural subtyping (duck typing with type hints)
class Drawable(Protocol):
    def draw(self) -> None: ...

def render(item: Drawable) -> None:
    item.draw()  # Works with ANY object that has draw()


# Immutable dataclass
@dataclass(frozen=True)
class ImmutablePoint:
    x: float
    y: float
```

## Mental Model

Ramalho thinks of Python objects as **participants in protocols**:

1. **What protocols should this object support?** (Iterable? Comparable? Hashable?)
2. **What special methods implement those protocols?**
3. **What does Python do automatically when I implement them?**
4. **What constraints must I respect?** (e.g., hashable = immutable)

## Key Data Model Insights

| Protocol | Methods | Enables |
|----------|---------|---------|
| Iterable | `__iter__` | `for x in obj`, `list(obj)` |
| Sequence | `__getitem__`, `__len__` | `obj[i]`, `len(obj)`, iteration |
| Mapping | `__getitem__`, `__iter__`, `__len__` | `obj[key]`, `dict(obj)` |
| Callable | `__call__` | `obj()` |
| Context Manager | `__enter__`, `__exit__` | `with obj:` |
| Comparable | `__eq__`, `__lt__`, etc. | `==`, `<`, sorting |
| Hashable | `__hash__`, `__eq__` | `set()`, `dict` keys |

