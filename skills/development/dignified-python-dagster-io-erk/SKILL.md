---
name: dignified-python
description: Python coding standards with automatic version detection.
  Use when writing, reviewing, or refactoring Python to ensure adherence to LBYL exception
  handling patterns, modern type syntax (list[str], str | None), pathlib operations,
  ABC-based interfaces, absolute imports, and explicit error boundaries at CLI level.
  Also provides production-tested code smell patterns from Dagster Labs for API design,
  parameter complexity, and code organization. Essential for maintaining erk's dignified
  Python standards.
---

# Dignified Python Coding Standards

## Core Knowledge (ALWAYS Loaded)

@dignified-python-core.md

## Version Detection

**Identify the project's minimum Python version** by checking (in order):

1. `pyproject.toml` - Look for `requires-python` field (e.g., `requires-python = ">=3.12"`)
2. `setup.py` or `setup.cfg` - Look for `python_requires`
3. `.python-version` file - Contains version like `3.12` or `3.12.0`
4. Default to Python 3.12 if no version specifier found

**Once identified, load the appropriate version-specific file:**

- Python 3.10: Load `versions/python-3.10.md`
- Python 3.11: Load `versions/python-3.11.md`
- Python 3.12: Load `versions/python-3.12.md`
- Python 3.13: Load `versions/python-3.13.md`

## Conditional Loading (Load Based on Task Patterns)

Core files above cover 80%+ of Python code patterns. Only load these additional files when you detect specific patterns:

Pattern detection examples:

- If task mentions "click" or "CLI" -> Load `cli-patterns.md`
- If task mentions "subprocess" -> Load `subprocess.md`

## When to Read Each Reference Document

The `references/` directory contains detailed guidance for specialized topics. Load these on-demand when you encounter relevant patterns:

### `references/exception-handling.md`

**Read when**:

- Writing try/except blocks
- Wrapping third-party APIs that may raise
- Seeing or writing `from e` or `from None`
- Unsure if LBYL alternative exists

### `references/interfaces.md`

**Read when**:

- Creating ABC or Protocol classes
- Writing @abstractmethod decorators
- Designing gateway layer interfaces
- Choosing between ABC and Protocol

### `references/typing-advanced.md`

**Read when**:

- Using typing.cast()
- Creating Literal type aliases
- Narrowing types in conditional blocks

### `references/module-design.md`

**Read when**:

- Creating new Python modules
- Adding module-level code (beyond simple constants)
- Using @cache decorator at module level
- Seeing Path() or computation at module level
- Considering inline imports

### `references/api-design.md`

**Read when**:

- Adding default parameter values to functions
- Defining functions with 5 or more parameters
- Using ThreadPoolExecutor.submit()
- Reviewing function signatures

### `references/checklists.md`

**Read when**:

- Final review before committing Python code
- Unsure if you've followed all rules
- Need a quick lookup of requirements

## How to Use This Skill

1. **Core knowledge** is loaded automatically (LBYL, pathlib, basic imports, anti-patterns)
2. **Version detection** happens once - identify the minimum Python version and load the appropriate version file
3. **Reference documents** are loaded on-demand based on the triggers above
4. **Additional patterns** may require extra loading (CLI patterns, subprocess)
5. **Each file is self-contained** with complete guidance for its domain
