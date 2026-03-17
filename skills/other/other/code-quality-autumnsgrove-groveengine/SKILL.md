---
name: code-quality
description: Maintain Python code quality using Black formatting, Ruff linting, and mypy type checking. Use when formatting code, running linters, fixing style issues, or adding type hints.
---

# Code Quality Skill

## When to Activate

Activate this skill when:
- Formatting Python code
- Running linters
- Adding type annotations
- Fixing code style issues
- Setting up quality tools

## Quick Commands

```bash
# Format with Black
uv run black .
uv run black --check .  # Dry run

# Lint with Ruff
uv run ruff check .
uv run ruff check --fix .  # Auto-fix

# Type check with mypy
uv run mypy .

# All checks
uv run black . && uv run ruff check . && uv run mypy .
```

## Tool Overview

| Tool | Purpose | Speed | Auto-fix |
|------|---------|-------|----------|
| **Black** | Code formatting | Fast | Yes |
| **Ruff** | Linting & imports | Very Fast | Most rules |
| **mypy** | Type checking | Moderate | No |

## Installation

```bash
uv add --dev black ruff mypy
```

## Black - Code Formatting

Zero-config formatting with consistent style.

```bash
uv run black .                # Format all
uv run black --check .        # Dry run
uv run black --diff .         # Show changes
```

### Configuration
```toml
[tool.black]
line-length = 88
target-version = ['py311']
```

## Ruff - Fast Linting

Rust-based linter replacing flake8, isort, pylint, and 50+ tools.

```bash
uv run ruff check .               # Check
uv run ruff check --fix .         # Auto-fix
uv run ruff check --show-source . # Show context
```

### Configuration
```toml
[tool.ruff]
line-length = 88
target-version = "py311"
select = ["E", "W", "F", "I", "B", "SIM"]
ignore = ["E501"]  # Black handles line length

[tool.ruff.per-file-ignores]
"__init__.py" = ["F401"]
"tests/*" = ["S101"]
```

### Common Issues
- **F401**: Unused import (auto-fixable)
- **F841**: Unused variable
- **I001**: Import sorting (auto-fixable)
- **B008**: Mutable default argument

## mypy - Type Checking

Static type checker for Python.

```python
def greet(name: str) -> str:
    return f"Hello, {name}"

greet(123)  # mypy error: incompatible type "int"
```

### Configuration
```toml
[tool.mypy]
python_version = "3.11"
warn_return_any = true
disallow_untyped_defs = false  # Enable gradually
check_untyped_defs = true
```

### Common Type Hints
```python
from typing import Optional, List, Dict

def find_user(user_id: int) -> Optional[Dict[str, str]]:
    return database.get(user_id)

def process_items(items: List[str]) -> int:
    return len(items)
```

## Unified Configuration

```toml
# pyproject.toml
[tool.black]
line-length = 88
target-version = ['py311']

[tool.ruff]
line-length = 88
target-version = "py311"
select = ["E", "W", "F", "I", "B", "SIM"]

[tool.mypy]
python_version = "3.11"
warn_return_any = true
```

## Skipping Rules

```python
import os  # noqa: F401       # Ignore Ruff rule

# fmt: off                     # Disable Black
matrix = [[1, 2, 3], [4, 5, 6]]
# fmt: on
```

## Workflow Best Practices

### Development (before commit)
```bash
uv run black . && uv run ruff check --fix . && uv run mypy .
```

### CI/CD (strict, no auto-fix)
```bash
uv run black --check . && uv run ruff check . && uv run mypy --strict .
```

## Gradual Adoption

1. **Start with Black** - Zero config, immediate benefits
2. **Add Ruff** - Basic rules first, expand gradually
3. **Introduce mypy** - Lenient initially, increase strictness

## Code Style Principles

### Clarity Over Cleverness
```python
# ❌ Clever but unclear
result = [x for x in range(10) if x % 2 == 0 if x > 5]

# ✅ Clear and readable
even_numbers = [x for x in range(10) if x % 2 == 0]
result = [x for x in even_numbers if x > 5]
```

### Meaningful Names
```python
# ❌ Unclear
def proc(d, x):
    return d[x] if x in d else None

# ✅ Clear
def get_user_by_id(users_dict, user_id):
    return users_dict.get(user_id)
```

### Early Returns
```python
# ❌ Nested
def process(amount, user):
    if amount > 0:
        if user.has_payment():
            return charge(user, amount)

# ✅ Early returns
def process(amount, user):
    if amount <= 0:
        return "Invalid amount"
    if not user.has_payment():
        return "No payment method"
    return charge(user, amount)
```

## Related Resources

See `AgentUsage/code_quality.md` and `AgentUsage/code_style_guide.md` for:
- IDE integration
- Pre-commit hook setup
- Comprehensive style guidelines
- Error handling patterns
