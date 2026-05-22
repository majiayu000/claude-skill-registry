---
name: python-guidelines
description: Universal Python development guidelines and best practices
license: MIT
compatibility: opencode
metadata:
    related_coding_principles: For general coding standards, use skill `coding-principles`
    related_python_cli: For CLI development patterns, use skill `python-cli`
---

# Python Guidelines

## What I Do

Provide universal Python development guidelines that apply across different Python projects and domains.

## Universal Python Best Practices

### Project Structure

```text
# Universal Python project structure
project/
├── src/                  # Main source code
│   └── package/          # Importable package
├── tests/                # Test suite
├── docs/                 # Documentation
├── scripts/              # Utility scripts
├── pyproject.toml        # Project configuration
├── README.md             # Project overview
└── .gitignore            # Version control ignore
```

### Dependency Management

```bash
# Universal Python dependency management
# Use uv for all package operations
uv add package-name          # Add production dependency
uv add package-name --dev    # Add development dependency
uv remove package-name       # Remove dependency
uv sync --all-extras -U     # Update all dependencies
```

### Type Hints and Annotations

```python
# Universal type hint patterns
from typing import List, Dict, Optional, Union

# Function with complete type annotations
def process_data(
    input_data: List[Dict[str, Union[int, str]]],
    config: Optional[Dict[str, str]] = None
) -> Dict[str, List[float]]:
    """Process data with type-safe operations"""
    # Implementation with type-checked operations
    return processed_results
```

## When to Use Me

Use this skill when:

- Setting up new Python projects
- Standardizing Python development across teams
- Creating reusable Python patterns
- Implementing maintainable Python code

## Universal Python Examples

### Import Organization

```python
# Universal import structure
# 1. Standard library imports
import os
import sys
from pathlib import Path

# 2. Third-party imports
import numpy as np
import pandas as pd

# 3. Local application imports
from .utils import helpers
from .core import processors
```

### Error Handling Patterns

```python
# Universal Python error handling
class DataValidationError(Exception):
    """Custom exception for data validation issues"""
    pass

def validate_input(data: dict) -> None:
    """Validate input data with specific error messages"""
    if not data:
        raise DataValidationError("Input data cannot be empty")
    if "required_field" not in data:
        raise DataValidationError("Missing required field: required_field")
```

### Testing Patterns

```python
# Universal Python testing structure
import pytest
from hypothesis import given, strategies as st

class TestDataProcessor:
    """Test suite for data processor"""

    @pytest.fixture
    def sample_data(self):
        """Provide sample data for testing"""
        return {"input": [1, 2, 3], "expected": [2, 4, 6]}

    def test_process_data(self, sample_data):
        """Test data processing with sample input"""
        result = process_data(sample_data["input"])
        assert result == sample_data["expected"]

    @given(st.lists(st.integers()))
    def test_process_data_properties(self, input_list):
        """Property-based testing for data processor"""
        result = process_data(input_list)
        assert len(result) == len(input_list)
        assert all(isinstance(x, int) for x in result)
```

## Best Practices

1. **Consistency**: Apply same patterns across all Python projects
2. **Type Safety**: Use complete type annotations
3. **Testing**: Implement comprehensive test coverage
4. **Documentation**: Use Google-style docstrings

## Compatibility

Works with:

- Python 3.8+ projects
- Any Python application type
- Cross-project standardization
- Organizational Python guidelines
