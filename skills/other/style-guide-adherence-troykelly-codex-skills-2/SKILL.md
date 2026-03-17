---
name: style-guide-adherence
description: Use when writing code - follow Google style guides where available, otherwise follow established best practices for the language
---

# Style Guide Adherence

## Overview

Follow established style guides. Consistency over personal preference.

**Core principle:** Code is read more than written. Consistent style aids reading.

**Priority order:**
1. Project-specific style guide (if exists)
2. Google style guide (if available for language)
3. Language community best practices

## Google Style Guides

### Available Guides

| Language | Guide URL |
|----------|-----------|
| TypeScript/JavaScript | https://google.github.io/styleguide/tsguide.html |
| Python | https://google.github.io/styleguide/pyguide.html |
| Go | https://google.github.io/styleguide/go/ |
| Java | https://google.github.io/styleguide/javaguide.html |
| C++ | https://google.github.io/styleguide/cppguide.html |
| Shell | https://google.github.io/styleguide/shellguide.html |
| HTML/CSS | https://google.github.io/styleguide/htmlcssguide.html |

### Key Principles (All Languages)

| Principle | Description |
|-----------|-------------|
| Consistency | Match surrounding code style |
| Clarity | Prefer readable over clever |
| Simplicity | Simplest solution that works |
| Documentation | Document the why, not the what |

## TypeScript/JavaScript Style

### Naming

```typescript
// Classes: PascalCase
class UserService { }

// Interfaces: PascalCase (no I prefix)
interface User { }  // NOT IUser

// Functions/methods: camelCase
function fetchUserData() { }

// Variables/parameters: camelCase
const userName = 'Alice';

// Constants: UPPER_SNAKE_CASE
const MAX_RETRIES = 3;

// Private members: no underscore prefix
class Service {
  private cache: Map<string, Data>;  // NOT _cache
}

// Files: kebab-case
// user-service.ts, not userService.ts or UserService.ts
```

### Formatting

```typescript
// Indent: 2 spaces
// Line length: 80 characters (100 max)
// Semicolons: required
// Quotes: single for strings
// Trailing commas: yes in multiline

const config = {
  name: 'app',
  version: '1.0.0',
  features: [
    'auth',
    'logging',
  ],
};
```

### Imports

```typescript
// Order: external, then internal, then relative
// Alphabetize within groups

import { something } from 'external-lib';
import { other } from 'another-external';

import { internal } from '@/lib/internal';

import { local } from './local';
import { nearby } from '../nearby';
```

## Python Style

### Naming

```python
# Classes: PascalCase
class UserService:
    pass

# Functions/variables: snake_case
def fetch_user_data():
    pass

user_name = 'Alice'

# Constants: UPPER_SNAKE_CASE
MAX_RETRIES = 3

# Private: single underscore prefix
class Service:
    def __init__(self):
        self._cache = {}  # internal use

    def __private_method(self):  # name mangling
        pass

# Files: snake_case
# user_service.py
```

### Formatting

```python
# Indent: 4 spaces
# Line length: 80 characters
# Use Black formatter for consistency

# Imports order (use isort):
# 1. Standard library
# 2. Third-party
# 3. Local

import os
import sys

import requests
from flask import Flask

from myapp.utils import helper
```

### Docstrings

```python
def calculate_total(items: list[Item], tax_rate: float) -> float:
    """Calculate the total price including tax.

    Args:
        items: List of items to sum.
        tax_rate: Tax rate as decimal (e.g., 0.08 for 8%).

    Returns:
        Total price including tax.

    Raises:
        ValueError: If tax_rate is negative.
    """
    if tax_rate < 0:
        raise ValueError("Tax rate cannot be negative")

    subtotal = sum(item.price for item in items)
    return subtotal * (1 + tax_rate)
```

## Go Style

### Naming

```go
// Exported: PascalCase
type UserService struct { }
func FetchUser() { }

// Unexported: camelCase
type internalCache struct { }
func fetchFromDB() { }

// Acronyms: consistent case
type HTTPClient struct { }  // or httpClient for unexported
var userID string          // NOT userId

// Files: snake_case
// user_service.go
```

### Formatting

Use `gofmt` - no options, no debate.

```bash
# Format all files
gofmt -w .

# Or use goimports for imports too
goimports -w .
```

## Enforcing Style

### Automated Tools

| Language | Formatter | Linter |
|----------|-----------|--------|
| TypeScript | Prettier | ESLint |
| Python | Black | Pylint, Ruff |
| Go | gofmt | golangci-lint |
| Rust | rustfmt | clippy |

### Configuration Files

Ensure these exist in the project:

**TypeScript/JavaScript:**
- `.eslintrc.js` or `eslint.config.js`
- `.prettierrc`

**Python:**
- `pyproject.toml` (Black, isort, mypy)
- `.pylintrc` or `ruff.toml`

**Go:**
- `.golangci.yml`

### Pre-commit Hooks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: format
        name: Format code
        entry: pnpm format
        language: system
      - id: lint
        name: Lint code
        entry: pnpm lint
        language: system
```

## When Project Style Differs

If project has established style that differs from Google:

1. **Follow project style** - Consistency within project wins
2. **Document the difference** - Note in CONTRIBUTING.md
3. **Don't mix styles** - All code should match

```markdown
<!-- CONTRIBUTING.md -->
## Code Style

This project uses [specific style] which differs from Google style:
- We use tabs instead of spaces
- Line length is 120 characters
- [Other differences]
```

## Checking Style

Before committing:

```bash
# Run formatter
pnpm format  # or black, gofmt, etc.

# Run linter
pnpm lint    # or pylint, golangci-lint, etc.

# Fix auto-fixable issues
pnpm lint:fix
```

## Checklist

Before committing:

- [ ] Code formatted with project formatter
- [ ] No linting errors
- [ ] Naming follows conventions
- [ ] Imports organized
- [ ] Line length within limits
- [ ] Consistent with surrounding code

## Common Mistakes

| Mistake | Correction |
|---------|------------|
| Inconsistent naming | Follow project conventions |
| Long lines | Break at logical points |
| Mixed quote styles | Use project standard |
| Unorganized imports | Use import sorter |
| Manual formatting | Use automated formatter |

## Integration

This skill is applied by:
- `issue-driven-development` - Step 7
- `comprehensive-review` - Style criterion

This skill ensures:
- Readable code
- Easy reviews
- Reduced cognitive load
- Team consistency
