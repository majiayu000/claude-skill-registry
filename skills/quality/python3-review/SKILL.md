---
name: python3-review
description: Comprehensive Python code review checking patterns, types, security, and performance. Use when reviewing Python code for quality issues, when auditing code before merge, or when assessing technical debt in a Python codebase.
user-invocable: true
argument-hint: "<file-paths-or-module>"
---

# Python Code Review

The model performs comprehensive code review across multiple quality dimensions.

## Arguments

$ARGUMENTS

## Instructions

1. **Read target files** from arguments
2. **Check each dimension** listed below
3. **Report findings** with severity and location
4. **Suggest fixes** with code examples

---

## Review Dimensions

### 1. Type Safety

**Check for:**

- Missing type hints on function parameters and return types
- Use of `Any` without justification
- Legacy typing imports (`List`, `Dict`, `Optional`, `Union`)
- Missing Protocol definitions for duck typing
- Incorrect use of TypeVar, Generic, or ParamSpec

**Severity**: High (type errors cause runtime failures)

```python
# Bad - missing types
def process(data):
    return data.get("value")

# Good - complete types
def process(data: dict[str, int]) -> int | None:
    return data.get("value")
```

### 2. Error Handling

**Check for:**

- Bare `except:` or `except Exception:`
- Swallowed exceptions (catch and ignore)
- Missing context in re-raised exceptions
- Exceptions that should use `add_note()`
- Non-specific exception types

**Severity**: High (silent failures cause data corruption)

```python
# Bad - swallowed exception
try:
    result = risky_call()
except Exception:
    pass  # Silent failure

# Good - specific handling with context
try:
    result = risky_call()
except ConnectionError as e:
    e.add_note(f"Failed connecting to {host}")
    raise
```

### 3. Security

**Check for:**

- SQL queries with string formatting (injection risk)
- `subprocess.run(..., shell=True)` with user input
- Hardcoded credentials or API keys
- `eval()` or `exec()` with external input
- Pickle with untrusted data
- Path traversal vulnerabilities
- Missing input validation

**Severity**: Critical (security vulnerabilities)

```python
# Bad - SQL injection risk
query = f"SELECT * FROM users WHERE id = {user_id}"

# Good - parameterized query
query = "SELECT * FROM users WHERE id = ?"
cursor.execute(query, (user_id,))
```

### 4. Performance

**Check for:**

- List membership checks instead of sets (`in list` vs `in set`)
- String concatenation in loops
- Repeated function calls that could be cached
- N+1 query patterns
- Synchronous I/O in async contexts
- Missing `__slots__` for data classes with many instances

**Severity**: Medium (degraded performance)

```python
# Bad - O(n) lookup on each iteration
valid_codes = [200, 201, 204]
for code in codes:
    if code in valid_codes:  # O(n) each time
        process(code)

# Good - O(1) lookup
VALID_CODES = {200, 201, 204}
for code in codes:
    if code in VALID_CODES:  # O(1) each time
        process(code)
```

### 5. Modern Patterns

**Check for:**

- Legacy typing imports when builtin generics available
- Missing walrus operator opportunities
- If/elif chains that should be match-case
- `unittest.mock` in pytest tests
- Manual implementations duplicating stdlib

**Severity**: Low (technical debt)

```python
# Bad - legacy pattern
from typing import Optional

result = expensive_call()
if result:
    process(result)

# Good - modern pattern
if result := expensive_call():
    process(result)
```

### 6. Code Structure

**Check for:**

- Functions longer than 50 lines
- Classes with too many responsibilities
- Deep nesting (more than 3 levels)
- Circular imports
- Missing `__all__` in public modules
- Dead code (unreachable or unused)

**Severity**: Medium (maintainability)

### 7. Documentation

**Check for:**

- Public functions without docstrings
- Outdated docstrings (don't match signature)
- Missing type information in docstrings when types unclear
- Complex logic without explanatory comments

**Severity**: Low (maintainability)

---

## Report Format

For each finding, report:

````text
## [SEVERITY] [Category]: [Brief Description]

**Location**: `file.py:123` in `function_name`

**Issue**: Detailed explanation of the problem.

**Fix**:
```python
# Suggested fix with code example
````

**Impact**: Why this matters (security, performance, reliability).

````

---

## Review Checklist

```text
TYPE SAFETY
- [ ] All functions have complete type hints
- [ ] No legacy typing imports (List, Dict, Optional, Union)
- [ ] TypeVar/Protocol used appropriately
- [ ] Generic types are correct

ERROR HANDLING
- [ ] No bare except clauses
- [ ] No swallowed exceptions
- [ ] Exceptions have context (add_note or from)
- [ ] Specific exception types used

SECURITY
- [ ] No SQL injection vulnerabilities
- [ ] No command injection (shell=True with user input)
- [ ] No hardcoded secrets
- [ ] Input validation present

PERFORMANCE
- [ ] Sets used for membership testing
- [ ] No string concatenation in loops
- [ ] Appropriate caching used
- [ ] Async patterns correct

MODERN PATTERNS
- [ ] Builtin generics used (list, dict, not List, Dict)
- [ ] Walrus operator where beneficial
- [ ] Match-case for dispatch
- [ ] pytest-mock instead of unittest.mock

STRUCTURE
- [ ] Functions under 50 lines
- [ ] No deep nesting (>3 levels)
- [ ] No circular imports
- [ ] __all__ defined in public modules

DOCUMENTATION
- [ ] Public functions have docstrings
- [ ] Docstrings match signatures
- [ ] Complex logic commented
````

---

## Summary Format

End the review with:

```text
## Review Summary

**Files Reviewed**: [count]
**Total Findings**: [count]

| Severity | Count |
|----------|-------|
| Critical | X     |
| High     | X     |
| Medium   | X     |
| Low      | X     |

**Top Issues**:
1. [Most important issue]
2. [Second most important issue]
3. [Third most important issue]

**Recommendation**: [APPROVE / REQUEST CHANGES / BLOCK]
```

---

## References

- [OWASP Python Security](https://owasp.org/www-project-web-security-testing-guide/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- [PEP 8 - Style Guide](https://peps.python.org/pep-0008/)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)
