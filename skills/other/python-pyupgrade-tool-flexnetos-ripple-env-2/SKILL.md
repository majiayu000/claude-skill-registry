---
name: Python Pyupgrade Syntax Modernizer
description: "Use pyupgrade to automatically upgrade Python syntax to newer versions. Activate when: (1) Migrating code from Python 2 to 3, (2) Removing deprecated syntax like 'class Foo(object)', (3) Converting old-style string formatting to f-strings, (4) Updating type hints to modern union syntax (X | Y), (5) Removing obsolete __future__ imports, or (6) Upgrading to a newer Python minimum version."
---

# Python Pyupgrade Syntax Modernizer

## Overview

Pyupgrade is a tool (and pre-commit hook) that automatically upgrades Python syntax for newer versions of the language. It scans your code and applies modern syntax patterns appropriate for your target Python version.

**Key benefit**: Pyupgrade automates tedious manual refactoring when upgrading Python versions, ensuring consistent modern syntax across your codebase.

## Key Capabilities

- **Version-targeted upgrades**: Specify minimum Python version (3.6+ through 3.14+)
- **Safe transformations**: Conservative approach that won't break working code
- **Pre-commit integration**: Seamlessly integrates into CI/CD workflows
- **Comprehensive coverage**: Handles strings, types, imports, classes, and more

## Quick Reference

### Basic Commands

```bash
# Upgrade file to latest Python syntax
pyupgrade file.py

# Upgrade to specific Python version
pyupgrade --py311-plus file.py

# Process entire directory recursively
find . -name "*.py" -exec pyupgrade --py311-plus {} +

# Dry run (show what would change)
pyupgrade --py311-plus file.py && git diff

# Keep percent formatting (opt-out)
pyupgrade --keep-percent-format file.py

# Keep mock imports (opt-out)
pyupgrade --keep-mock file.py
```

### Version Flags

| Flag | Minimum Python | Key Features Enabled |
|------|----------------|---------------------|
| `--py36-plus` | 3.6 | f-strings, variable annotations |
| `--py37-plus` | 3.7 | async/await improvements |
| `--py38-plus` | 3.8 | Walrus operator, positional-only params |
| `--py39-plus` | 3.9 | `dict \| dict`, `list[int]` generics |
| `--py310-plus` | 3.10 | `X \| Y` union types, match statements |
| `--py311-plus` | 3.11 | Exception groups, tomllib |
| `--py312-plus` | 3.12 | Type parameter syntax |
| `--py313-plus` | 3.13 | Latest syntax features |
| `--py314-plus` | 3.14 | Bleeding edge features |

## Transformations

### Set Literals

```python
# Before
set([1, 2, 3])
set((1, 2, 3))

# After
{1, 2, 3}
```

### Dictionary Comprehensions

```python
# Before
dict((a, b) for a, b in items)

# After
{a: b for a, b in items}
```

### String Formatting (f-strings)

```python
# Before
"Hello, {}".format(name)
"Hello, %s" % name
"Value: {value}".format(value=x)

# After (--py36-plus)
f"Hello, {name}"
f"Hello, {name}"
f"Value: {x}"
```

### Class Definitions

```python
# Before
class MyClass(object):
    __metaclass__ = ABCMeta

# After
class MyClass:
    pass  # with ABCMeta via class MyClass(metaclass=ABCMeta)
```

### Super Calls

```python
# Before
class Child(Parent):
    def method(self):
        super(Child, self).method()

# After
class Child(Parent):
    def method(self):
        super().method()
```

### Type Hints (--py310-plus)

```python
# Before
from typing import Optional, Union, List, Dict

def func(x: Optional[int]) -> Union[str, int]:
    items: List[Dict[str, int]] = []

# After
def func(x: int | None) -> str | int:
    items: list[dict[str, int]] = []
```

### __future__ Imports

```python
# Before (when targeting 3.10+)
from __future__ import annotations, division, print_function

# After
from __future__ import annotations  # only keeps needed ones
```

### Collections Imports

```python
# Before
from collections import Mapping, MutableMapping

# After
from collections.abc import Mapping, MutableMapping
```

### Mock Imports

```python
# Before
from mock import Mock, patch

# After (unless --keep-mock)
from unittest.mock import Mock, patch
```

### Invalid Escape Sequences

```python
# Before
regex = "\d+\s+"

# After
regex = r"\d+\s+"
```

### Six Library Removal

```python
# Before
import six
if six.PY2:
    text_type = unicode
else:
    text_type = str

# After
text_type = str
```

### Exception Handling

```python
# Before
OSError
IOError
EnvironmentError

# After (all aliased to OSError in Python 3)
OSError
OSError
OSError
```

### Comparison Operators

```python
# Before
if x is 1:
    pass

# After
if x == 1:
    pass
```

## Configuration

### Pre-commit Integration

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/asottile/pyupgrade
    rev: v3.21.2
    hooks:
      - id: pyupgrade
        args: [--py311-plus]
```

### Combining with Other Tools

**With Ruff**: If using Ruff, you can use its UP rules instead:

```toml
# pyproject.toml
[tool.ruff.lint]
select = ["UP"]
target-version = "py311"
```

**With Black**: Run pyupgrade before Black for consistent formatting:

```bash
pyupgrade --py311-plus file.py
black file.py
```

## Common Workflows

### Upgrade Entire Codebase

```bash
# Find all Python files and upgrade
find . -name "*.py" -not -path "./.venv/*" -exec pyupgrade --py311-plus {} +

# Or using xargs for better parallelism
find . -name "*.py" -not -path "./.venv/*" | xargs -P 4 pyupgrade --py311-plus
```

### Check Before Commit

```bash
# Stage files, then check
git add -A
git diff --cached --name-only --diff-filter=ACMR | \
  grep "\.py$" | \
  xargs -r pyupgrade --py311-plus
```

### Gradual Migration

```bash
# Start with conservative upgrade
pyupgrade --py38-plus file.py

# Then progressively upgrade
pyupgrade --py39-plus file.py
pyupgrade --py310-plus file.py
pyupgrade --py311-plus file.py
```

## Best Practices

1. **Use version control**: Always commit before running pyupgrade
2. **Run tests after**: Verify functionality after transformations
3. **Match your target**: Use the flag matching your minimum Python version
4. **Review changes**: Some transformations may need manual adjustment
5. **Combine with formatters**: Run Black/Ruff format after pyupgrade

## Caveats

- **F-string complexity**: Won't create f-strings if they would be longer or harder to read
- **Timid approach**: Intentionally conservative to avoid breaking code
- **Manual review**: Some edge cases may need manual attention

## Detailed Reference

For complete transformation examples, see [references/pyupgrade-transforms.md](references/pyupgrade-transforms.md).

## External Links

- [GitHub Repository](https://github.com/asottile/pyupgrade)
- [PyPI Package](https://pypi.org/project/pyupgrade/)
