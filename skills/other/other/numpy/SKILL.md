---
name: numpy
description: NumPy numerical computing with arrays. Use for numerical operations.
---

# NumPy

NumPy is the bedrock of the Python ecosystem. v2.0 (2024) brought the first major ABI change in 15 years, improving performance and API consistency.

## When to Use

- **Linear Algebra**: Matrix multiplication, eigenvalues.
- **Array Manipulation**: Reshaping, broadcasting.
- **Foundation**: When building libraries (like PyTorch or Pandas).

## Core Concepts

### Broadcasting

The magic rule that allows `array(3x1) + array(3)` to work.

### Dtypes

Precision matters. `float32` vs `float64`.

### Stride Tricks

Efficient memory views without copying data.

## Best Practices (2025)

**Do**:

- **Check v2.0 compat**: Many old libraries broke with NumPy 2.0.
- **Use `numpy.strings`**: New string kernels in v2.0 are much faster.

**Don't**:

- **Don't write `for` loops**: Always vectorize operations.

## References

- [NumPy Documentation](https://numpy.org/)
