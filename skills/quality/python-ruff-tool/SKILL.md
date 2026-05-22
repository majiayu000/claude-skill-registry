---
name: Python Ruff Linter & Formatter
description: "Use ruff to lint, format, and modernize Python code. Activate when: (1) Fixing PEP 8 violations, (2) Removing unused imports, (3) Upgrading deprecated Python syntax (UP rules), (4) Auto-fixing code quality issues, (5) Formatting Python files, or (6) Replacing Flake8, isort, pyupgrade, autoflake, or Black."
---

# Python Ruff Linter & Formatter

## Overview

Ruff is an extremely fast Python linter and code formatter written in Rust. It is 10-100x faster than traditional tools like Flake8 and Black, enabling sub-second feedback loops on even the largest codebases.

Ruff is a drop-in replacement for Flake8 (plus dozens of plugins), isort, pydocstyle, pyupgrade, autoflake, and more.

## Key Capabilities

- **Linting**: Over 800 lint rules from Flake8, isort, pyupgrade, pydocstyle, and more
- **Formatting**: Black-compatible code formatting
- **Auto-fix**: Automatically fix many violations with `--fix`
- **Modern Python**: Supports Python 3.8 through 3.13
- **Speed**: Written in Rust for maximum performance

## Quick Reference

### Basic Commands

```bash
# Lint all Python files in current directory
ruff check .

# Lint and auto-fix issues
ruff check --fix .

# Format Python files (like Black)
ruff format .

# Check formatting without modifying files
ruff format --check .

# Show diff of what would change
ruff format --diff .

# Lint specific file
ruff check path/to/file.py

# Watch mode for continuous linting
ruff check --watch .
```

### Useful Options

```bash
# Show rule explanations
ruff rule <RULE_CODE>

# Select specific rules
ruff check --select E,F,W .

# Ignore specific rules
ruff check --ignore E501 .

# Target Python version
ruff check --target-version py311 .

# Output format options
ruff check --output-format=json .
ruff check --output-format=github .

# Show statistics
ruff check --statistics .
```

## Rule Categories

| Prefix | Category | Description |
|--------|----------|-------------|
| E | pycodestyle errors | PEP 8 error violations |
| W | pycodestyle warnings | PEP 8 warning violations |
| F | Pyflakes | Logical errors, undefined names |
| UP | pyupgrade | Modernize Python syntax |
| I | isort | Import sorting |
| B | flake8-bugbear | Bug risk patterns |
| C4 | flake8-comprehensions | Comprehension improvements |
| SIM | flake8-simplify | Code simplification |
| RUF | Ruff-specific | Ruff's own rules |

### Python Modernization Rules (UP)

These rules upgrade deprecated Python syntax:

```bash
# Run only pyupgrade rules
ruff check --select UP .

# Common UP rules:
# UP001: Remove unnecessary encoding in open()
# UP003: Use {} instead of type()
# UP004: Remove useless object inheritance
# UP005: Replace deprecated unittest assertions
# UP006: Use type instead of Type for builtins
# UP007: Use X | Y for union types
# UP008: Use super() without arguments
# UP009: Remove unnecessary UTF-8 encoding declarations
# UP010: Remove unnecessary __future__ imports
# UP015: Remove unnecessary mode='r' in open()
# UP018: Use native str/bytes/int instead of literals
# UP032: Use f-strings instead of .format()
# UP034: Remove extraneous parentheses
# UP035: Replace deprecated imports
# UP036: Remove outdated version blocks
# UP037: Remove quotes from type annotations
```

## Configuration

### pyproject.toml

```toml
[tool.ruff]
# Target Python version
target-version = "py311"

# Line length (default 88, like Black)
line-length = 88

# Exclude patterns
exclude = [
    ".git",
    ".venv",
    "__pycache__",
    "build",
    "dist",
]

[tool.ruff.lint]
# Enable these rule sets
select = [
    "E",    # pycodestyle errors
    "W",    # pycodestyle warnings
    "F",    # Pyflakes
    "UP",   # pyupgrade
    "I",    # isort
    "B",    # flake8-bugbear
    "C4",   # flake8-comprehensions
    "SIM",  # flake8-simplify
]

# Ignore specific rules
ignore = [
    "E501",  # line too long (handled by formatter)
]

# Allow autofix for all rules
fixable = ["ALL"]

[tool.ruff.lint.isort]
# Known first-party imports
known-first-party = ["mypackage"]

[tool.ruff.format]
# Use double quotes (like Black)
quote-style = "double"

# Indent with spaces
indent-style = "space"

# Respect magic trailing commas
skip-magic-trailing-comma = false
```

## Common Workflows

### Modernize Python Codebase

```bash
# Check what would be upgraded
ruff check --select UP --diff .

# Apply all pyupgrade fixes
ruff check --select UP --fix .

# Check and fix all issues
ruff check --fix .
ruff format .
```

### CI/CD Integration

```bash
# Fail on any issues (good for CI)
ruff check .
ruff format --check .

# GitHub Actions output format
ruff check --output-format=github .
```

### Pre-commit Hook

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.8.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
```

## Best Practices

1. **Start with defaults**: Ruff's defaults are sensible; add rules incrementally
2. **Use --fix carefully**: Review auto-fixes before committing
3. **Target version**: Always set `target-version` to your minimum Python version
4. **Format after lint**: Run `ruff format` after `ruff check --fix`
5. **Exclude generated code**: Add build directories to exclude list

## Comparison with Other Tools

| Tool | Ruff Equivalent |
|------|-----------------|
| Flake8 | `ruff check` |
| Black | `ruff format` |
| isort | `ruff check --select I --fix` |
| pyupgrade | `ruff check --select UP --fix` |
| autoflake | `ruff check --select F401,F841 --fix` |

## Detailed Reference

For comprehensive documentation, see [references/ruff-rules.md](references/ruff-rules.md).

## External Links

- [Official Documentation](https://docs.astral.sh/ruff/)
- [GitHub Repository](https://github.com/astral-sh/ruff)
- [Rule Reference](https://docs.astral.sh/ruff/rules/)
