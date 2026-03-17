---
name: python-code-review
description: Reviews Python code for type safety, async patterns, error handling, and common mistakes. Use when reviewing .py files, checking type hints, async/await usage, or exception handling.
---

# Python Code Review

## Quick Reference

| Issue Type | Reference |
|------------|-----------|
| Indentation, line length, whitespace, naming | [references/pep8-style.md](references/pep8-style.md) |
| Missing/wrong type hints, Any usage | [references/type-safety.md](references/type-safety.md) |
| Blocking calls in async, missing await | [references/async-patterns.md](references/async-patterns.md) |
| Bare except, missing context, logging | [references/error-handling.md](references/error-handling.md) |
| Mutable defaults, print statements | [references/common-mistakes.md](references/common-mistakes.md) |

## Review Checklist

### PEP8 Style
- [ ] 4-space indentation (no tabs)
- [ ] Line length ≤79 characters (≤72 for docstrings/comments)
- [ ] Two blank lines around top-level definitions, one within classes
- [ ] Imports grouped: stdlib → third-party → local (blank line between groups)
- [ ] No whitespace inside brackets or before colons/commas
- [ ] Naming: `snake_case` for functions/variables, `CamelCase` for classes, `UPPER_CASE` for constants
- [ ] Inline comments separated by at least two spaces

### Type Safety
- [ ] Type hints on all function parameters and return types
- [ ] No `Any` unless necessary (with comment explaining why)
- [ ] Proper `T | None` syntax (Python 3.10+)

### Async Patterns
- [ ] No blocking calls (`time.sleep`, `requests`) in async functions
- [ ] Proper `await` on all coroutines

### Error Handling
- [ ] No bare `except:` clauses
- [ ] Specific exception types with context
- [ ] `raise ... from` to preserve stack traces

### Common Mistakes
- [ ] No mutable default arguments
- [ ] Using `logger` not `print()` for output
- [ ] f-strings preferred over `.format()` or `%`

## Valid Patterns (Do NOT Flag)

These patterns are intentional and correct - do not report as issues:

- **Type annotation vs type assertion** - Annotations declare types but are not runtime assertions; don't confuse with missing validation
- **Using `Any` when interacting with untyped libraries** - Required when external libraries lack type stubs
- **Empty `__init__.py` files** - Valid for package structure, no code required
- **`noqa` comments** - Valid when linter rule doesn't apply to specific case
- **Using `cast()` after runtime type check** - Correct pattern to inform type checker of narrowed type

## Context-Sensitive Rules

Only flag these issues when the specific conditions apply:

| Issue | Flag ONLY IF |
|-------|--------------|
| Generic exception handling | Specific exception types are available and meaningful |
| Unused variables | Variable lacks `_` prefix AND isn't used in f-strings, logging, or debugging |

## When to Load References

- Reviewing code formatting/style → pep8-style.md
- Reviewing function signatures → type-safety.md
- Reviewing `async def` functions → async-patterns.md
- Reviewing try/except blocks → error-handling.md
- General Python review → common-mistakes.md

## Review Questions

1. Does the code follow PEP8 formatting (indentation, line length, whitespace)?
2. Are imports properly grouped (stdlib → third-party → local)?
3. Do names follow conventions (snake_case, CamelCase, UPPER_CASE)?
4. Are all function signatures fully typed?
5. Are async functions truly non-blocking?
6. Do exceptions include meaningful context?
7. Are there any mutable default arguments?

## Before Submitting Findings

Load and follow [review-verification-protocol](../review-verification-protocol/SKILL.md) before reporting any issue.
