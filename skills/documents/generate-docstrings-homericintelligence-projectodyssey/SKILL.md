---
name: generate-docstrings
description: "Create docstrings for functions and classes. Use when documenting code APIs."
mcp_fallback: none
category: generation
tier: 2
user-invocable: false
---

# Generate Docstrings

Write comprehensive docstrings for functions and classes following standard formats (Google, NumPy, reStructuredText).

## When to Use

- Adding documentation to undocumented functions
- Improving code documentation completeness
- Ensuring consistent docstring format
- Supporting API documentation generation

## Quick Reference

```python
# Google-style docstring format
def matrix_multiply(a: ExTensor, b: ExTensor) -> ExTensor:
    """Multiply two matrices using optimized Mojo kernels.

    Args:
        a: First matrix (shape: m x n)
        b: Second matrix (shape: n x k)

    Returns:
        Product matrix (shape: m x k)

    Raises:
        ValueError: If matrix dimensions don't align for multiplication

    Example:
        ```mojo
        >> a = ExTensor([[1, 2], [3, 4]], DType.float32)
        >>> b = ExTensor([[1, 0], [0, 1]], DType.float32)
        >>> c = matrix_multiply(a, b)
        ```
    """
    ...
```

## Workflow

1. **Analyze function**: Understand purpose, parameters, return value
2. **Choose format**: Select docstring style (Google is recommended)
3. **Write summary**: Clear one-line description
4. **Document parameters**: Type, description, constraints
5. **Document return**: Type and description of return value
6. **Add examples**: Practical usage examples

## Output Format

Docstring structure:

- One-line summary
- Extended description (if needed)
- Args section (parameter documentation)
- Returns section (return value documentation)
- Raises section (exceptions)
- Examples section (usage examples)

## References

- See `generate-api-docs` skill for API documentation generation
- See Google Python Style Guide for docstring conventions
- See PEP 257 for Python docstring conventions
