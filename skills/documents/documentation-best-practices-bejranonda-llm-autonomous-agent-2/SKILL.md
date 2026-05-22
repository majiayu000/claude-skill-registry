---
name: documentation-best-practices
description: Provides templates, standards, and best practices for writing clear, comprehensive technical documentation
version: 1.0.0
---

## Overview

This skill provides guidelines for creating high-quality documentation including docstrings, API documentation, README files, and usage guides.

## Documentation Coverage Targets

- **Public APIs**: 100% documented
- **Internal Functions**: 80%+ documented
- **Complex Logic**: Must have explanation comments
- **Overall**: 85%+ coverage

## Docstring Templates

### Python (Google Style)
```python
def function_name(param1: str, param2: int) -> bool:
    """Brief one-line description.

    Longer detailed explanation if needed.

    Args:
        param1: Description of param1
        param2: Description of param2

    Returns:
        Description of return value

    Raises:
        ValueError: When and why
    """
```

### JavaScript (JSDoc)
```javascript
/**
 * Brief one-line description.
 *
 * @param {string} param1 - Description of param1
 * @param {number} param2 - Description of param2
 * @returns {boolean} Description of return value
 * @throws {Error} When and why
 */
```

## README Structure

1. **Project Title & Description**
2. **Installation**: Step-by-step setup
3. **Usage**: Basic examples
4. **API Documentation**: Overview or link
5. **Contributing**: Guidelines (if applicable)
6. **License**: Project license

## When to Apply

Use when generating documentation, updating docstrings, creating README files, or maintaining API documentation.
