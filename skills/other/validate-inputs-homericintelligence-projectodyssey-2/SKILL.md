---
name: validate-inputs
description: "Check function inputs for correctness and safety. Use when implementing defensive programming."
mcp_fallback: none
category: analysis
tier: 2
user-invocable: false
---

# Validate Inputs

Implement input validation to ensure functions receive correct data types, shapes, ranges, and formats.

## When to Use

- Adding defensive checks to functions
- Improving error messages for bad inputs
- Ensuring tensor shape/dtype correctness
- Validating configuration parameters

## Quick Reference

```python
# Input validation pattern
def validate_tensor(tensor):
    assert tensor is not None, "Tensor cannot be None"
    assert isinstance(tensor, ExTensor), "Must be ExTensor type"
    assert len(tensor.shape) > 0, "Tensor shape cannot be empty"
    assert tensor.dtype() in [DType.float32, DType.float64], "Invalid dtype"
    return True

# Usage with context
try:
    validate_tensor(input_data)
except AssertionError as e:
    raise ValueError(f"Invalid input: {e}")
```

## Workflow

1. **Document expectations**: Specify types, shapes, ranges for inputs
2. **Implement checks**: Add validation before processing
3. **Provide error messages**: Clear messages for validation failures
4. **Test edge cases**: Verify validation catches invalid inputs
5. **Document behavior**: Note what validation is performed

## Output Format

Input validation specification:

- Parameter name and type
- Constraints (shape, range, valid values)
- Error handling strategy
- Error messages returned
- Test cases for invalid inputs

## References

- See `generate-tests` skill for validation test cases
- See CLAUDE.md > Defensive Programming for best practices
- See `scan-vulnerabilities` skill for security validation
