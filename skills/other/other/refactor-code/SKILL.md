---
name: refactor-code
description: "Restructure code for improved clarity and maintainability. Use when addressing code smells or technical debt."
mcp_fallback: none
category: generation
tier: 2
user-invocable: false
---

# Refactor Code

Apply systematic refactoring techniques to improve code clarity, maintainability, and performance without changing functionality.

## When to Use

- Addressing code smells identified in reviews
- Reducing cyclomatic complexity
- Extracting methods and classes
- Improving naming and organization

## Quick Reference

```python
# Common refactoring patterns

# Extract method
# BEFORE: Long function with multiple responsibilities
def process_data(data):
    result = validate(data)
    formatted = format_data(result)
    return save(formatted)

# AFTER: Clear single responsibility
def process_data(data):
    validated = _validate_and_format(data)
    return save(validated)

def _validate_and_format(data):
    return format_data(validate(data))
```

## Workflow

1. **Identify refactoring targets**: From code review or analysis tools
2. **Plan changes**: Document what will change and why
3. **Apply refactoring**: Use IDE refactoring tools or manual changes
4. **Run tests**: Verify all tests still pass
5. **Verify performance**: Check no performance regression

## Output Format

Refactoring report:

- Issues addressed
- Refactoring techniques applied
- Metrics before/after (complexity, lines of code)
- Test coverage status
- Performance impact

## References

- See `detect-code-smells` skill for identifying issues
- See CLAUDE.md > SOLID principles for refactoring goals
- See `run-tests` skill for verification
