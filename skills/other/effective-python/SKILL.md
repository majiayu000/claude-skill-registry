---
name: effective-python
description: Review existing Python code and write new Python code following the 90 best practices from "Effective Python" by Brett Slatkin (2nd Edition). Use when writing Python, reviewing Python code, or wanting idiomatic, Pythonic solutions.
---

# Effective Python Skill

Apply the 90 items from Brett Slatkin's "Effective Python" (2nd Edition) to review existing code and write new Python code. This skill operates in two modes: **Review Mode** (analyze code for violations) and **Write Mode** (produce idiomatic Python from scratch).

## Reference Files

This skill includes categorized reference files with all 90 items:

- `ref-01-pythonic-thinking.md` — Items 1-10: PEP 8, f-strings, bytes/str, walrus operator, unpacking, enumerate, zip, slicing
- `ref-02-lists-and-dicts.md` — Items 11-18: Slicing, sorting, dict ordering, defaultdict, __missing__
- `ref-03-functions.md` — Items 19-26: Exceptions vs None, closures, *args/**kwargs, keyword-only args, decorators
- `ref-04-comprehensions-generators.md` — Items 27-36: Comprehensions, generators, yield from, itertools
- `ref-05-classes-interfaces.md` — Items 37-43: Composition, @classmethod, super(), mix-ins, public attrs
- `ref-06-metaclasses-attributes.md` — Items 44-51: @property, descriptors, __getattr__, __init_subclass__, class decorators
- `ref-07-concurrency.md` — Items 52-64: subprocess, threads, Lock, Queue, coroutines, asyncio
- `ref-08-robustness-performance.md` — Items 65-76: try/except, contextlib, datetime, decimal, profiling, data structures
- `ref-09-testing-debugging.md` — Items 77-85: TestCase, mocks, dependency injection, pdb, tracemalloc
- `ref-10-collaboration.md` — Items 86-90: Docstrings, packages, root exceptions, virtual environments

## How to Use This Skill

**Before responding**, read the relevant reference files based on the code's topic. For a general review, read all files. For targeted work (e.g., writing async code), read the specific reference (e.g., `ref-07-concurrency.md`).

---

## Mode 1: Code Review

When the user asks you to **review** existing Python code, follow this process:

### Step 1: Read Relevant References
Determine which chapters apply to the code under review and read those reference files. If unsure, read all of them.

### Step 2: Analyze the Code
For each relevant item from the book, check whether the code follows or violates the guideline. Focus on:

1. **Style and Idiom** (Items 1-10): Is it Pythonic? Does it use f-strings, unpacking, enumerate, zip properly?
2. **Data Structures** (Items 11-18): Are lists and dicts used correctly? Is sorting done with key functions?
3. **Function Design** (Items 19-26): Do functions raise exceptions instead of returning None? Are args well-structured?
4. **Comprehensions & Generators** (Items 27-36): Are comprehensions preferred over map/filter? Are generators used for large sequences?
5. **Class Design** (Items 37-43): Is composition preferred over deep nesting? Are mix-ins used correctly?
6. **Metaclasses & Attributes** (Items 44-51): Are plain attributes used instead of getter/setter methods? Is @property used appropriately?
7. **Concurrency** (Items 52-64): Are threads used only for I/O? Is asyncio structured correctly?
8. **Robustness** (Items 65-76): Is error handling structured with try/except/else/finally? Are the right data structures chosen?
9. **Testing** (Items 77-85): Are tests well-structured? Are mocks used appropriately?
10. **Collaboration** (Items 86-90): Are docstrings present? Are APIs stable?

### Step 3: Report Findings
For each issue found, report:
- **Item number and name** (e.g., "Item 4: Prefer Interpolated F-Strings")
- **Location** in the code
- **What's wrong** (the anti-pattern)
- **How to fix it** (the Pythonic way)
- **Priority**: Critical (bugs/correctness), Important (maintainability), Suggestion (style)

### Step 4: Provide Fixed Code
Offer a corrected version of the code with all issues addressed, with comments explaining each change.

---

## Mode 2: Writing New Code

When the user asks you to **write** new Python code, follow these principles:

### Always Apply These Core Practices

1. **Follow PEP 8** — Use consistent naming (snake_case for functions/variables, PascalCase for classes). Use `pylint` and `black`-compatible style.

2. **Use f-strings** for string formatting (Item 4). Never use % or .format() for simple cases.

3. **Use unpacking** instead of indexing (Item 6). Prefer `first, second = my_list` over `my_list[0]`.

4. **Use enumerate** instead of range(len(...)) (Item 7).

5. **Use zip** to iterate over multiple lists in parallel (Item 8). Use `zip_longest` from itertools when lengths differ.

6. **Avoid else blocks** after for/while loops (Item 9).

7. **Use assignment expressions** (:= walrus operator) to reduce repetition when appropriate (Item 10).

8. **Raise exceptions** instead of returning None for failure cases (Item 20).

9. **Use keyword-only arguments** for clarity (Item 25). Use positional-only args to separate API from implementation (Item 25).

10. **Use functools.wraps** on all decorators (Item 26).

11. **Prefer comprehensions** over map/filter (Item 27). Keep them simple — no more than two expressions (Item 28).

12. **Use generators** for large sequences instead of returning lists (Item 30).

13. **Prefer composition** over deeply nested classes (Item 37).

14. **Use @classmethod** for polymorphic constructors (Item 39).

15. **Always call super().__init__** (Item 40).

16. **Use plain attributes** instead of getter/setter methods. Use @property for special behavior (Item 44).

17. **Use try/except/else/finally** structure correctly (Item 65).

18. **Write docstrings** for every module, class, and function (Item 84).

### Code Structure Template

When writing new modules or classes, follow this structure:

```python
"""Module docstring describing purpose."""

# Standard library imports
# Third-party imports
# Local imports

# Module-level constants

class MyClass:
    """Class docstring describing purpose and usage.

    Attributes:
        attr_name: Description of attribute.
    """

    def __init__(self, param: type) -> None:
        """Initialize with description of params."""
        self.param = param  # Use public attributes (Item 42)

    @classmethod
    def from_alternative(cls, data):
        """Alternative constructor (Item 39)."""
        return cls(processed_data)

    def method(self, arg: type) -> return_type:
        """Method docstring.

        Args:
            arg: Description.

        Returns:
            Description of return value.

        Raises:
            ValueError: When arg is invalid (Item 20).
        """
        pass
```

### Concurrency Guidelines

- Use `subprocess` for managing child processes (Item 52)
- Use threads **only** for blocking I/O, never for parallelism (Item 53)
- Use `threading.Lock` to prevent data races (Item 54)
- Use `Queue` for coordinating work between threads (Item 55)
- Use `asyncio` for highly concurrent I/O (Item 60)
- Never mix blocking calls in async code (Item 62)

### Testing Guidelines

- Subclass `TestCase` and use `setUp`/`tearDown` (Item 78)
- Use `unittest.mock` for complex dependencies (Item 78)
- Encapsulate dependencies to make code testable (Item 79)
- Use `pdb.set_trace()` or `breakpoint()` for debugging (Item 80)
- Use `tracemalloc` for memory debugging (Item 81)

---

## Priority of Items by Impact

When time is limited, focus on these highest-impact items first:

### Critical (Correctness & Bugs)
- Item 20: Raise exceptions instead of returning None
- Item 53: Use threads for I/O only, not parallelism
- Item 54: Use Lock to prevent data races
- Item 40: Initialize parent classes with super()
- Item 65: Use try/except/else/finally correctly
- Item 73: Use datetime instead of time module for timezone handling

### Important (Maintainability)
- Item 1: Follow PEP 8 style
- Item 4: Use f-strings
- Item 19: Never unpack more than 3 variables
- Item 25: Use keyword-only and positional-only arguments
- Item 26: Use functools.wraps for decorators
- Item 37: Compose classes instead of deep nesting
- Item 42: Prefer public attributes over private
- Item 44: Use plain attributes over getter/setter
- Item 84: Write docstrings for all public APIs

### Suggestions (Polish & Optimization)
- Item 7: Use enumerate instead of range
- Item 8: Use zip for parallel iteration
- Item 10: Use walrus operator to reduce repetition
- Item 27: Use comprehensions over map/filter
- Item 30: Use generators for large sequences
- Item 70: Profile before optimizing (cProfile)
