---
name: python-anti-slop
description: >
  Enforce production-quality Python code standards. Prevents generic AI patterns
  through PEP 8 compliance, type hints, and pandas conventions. Use when writing
  or reviewing Python data science code.
applies_to:
  - "**/*.py"
  - "**/*.ipynb"
tags: [python, pep8, pandas, data-science, type-hints]
related_skills:
  - r/anti-slop
  - text/anti-slop
version: 2.0.0
---

# Python Anti-Slop Skill for Data Science

## When to Use This Skill

Use python-anti-slop when:
- ✓ Writing new Python code for data analysis or packages
- ✓ Reviewing AI-generated Python code before committing
- ✓ Refactoring existing code for production quality
- ✓ Building data science pipelines
- ✓ Teaching or enforcing Python code standards
- ✓ Working with pandas, numpy, sklearn, matplotlib

Do NOT use when:
- Writing quick exploratory notebooks (though standards still help)
- Working with legacy code that cannot be changed
- Following different established style guides (e.g., Google Python Style)

## Quick Example

**Before (AI Slop)**:
```python
# Import libraries
import pandas as pd

# Load data
data = pd.read_csv("data.csv")

# Process
result = data[data['x'] > 0]
```

**After (Anti-Slop)**:
```python
from pathlib import Path
from typing import Optional

import pandas as pd


def load_customer_data(file_path: str) -> pd.DataFrame:
    """
    Load customer data from CSV file.

    Parameters
    ----------
    file_path : str
        Path to customer CSV file

    Returns
    -------
    pd.DataFrame
        Customer data with columns: id, name, revenue, status
    """
    data_path = Path(file_path)

    if not data_path.exists():
        raise FileNotFoundError(f"Data file not found: {file_path}")

    customer_data = pd.read_csv(data_path)

    return customer_data


def filter_active_customers(
    customer_data: pd.DataFrame,
    min_revenue: float = 0.0
) -> pd.DataFrame:
    """Filter customers by active status and minimum revenue."""
    active_customers = (
        customer_data
        .query("status == 'active' & revenue > @min_revenue")
        .copy()
    )

    return active_customers
```

**What changed**:
- ✓ Descriptive names (`customer_data` not `data`)
- ✓ Type hints for all function signatures
- ✓ Comprehensive docstrings (NumPy style)
- ✓ Import organization (stdlib, third-party, local)
- ✓ Input validation with specific errors
- ✓ pandas method chaining with `.copy()`

## When to Use What

| If you need to... | Do this | Details |
|-------------------|---------|---------|
| Name variables | Use `snake_case`, no `data`/`df`/`result` | reference/naming.md |
| Define functions | Add type hints + NumPy docstrings | reference/type-hints.md |
| Import packages | Organize: stdlib → third-party → local | reference/imports.md |
| Use pandas | Method chain with `.copy()` | reference/pandas.md |
| Handle errors | Specific exceptions + informative messages | reference/error-handling.md |
| Format code | Use `black` or `ruff format` | reference/formatting.md |
| Check types | Use `mypy` | reference/type-hints.md |
| Test code | Use `pytest` with fixtures | reference/testing.md |

## Core Workflow

### 5-Step Quality Check

1. **Type hints** - All functions have typed signatures
   ```python
   # Good
   def calculate_rate(numerator: float, denominator: float) -> float:
       return numerator / denominator

   # Bad
   def calculate_rate(numerator, denominator):
       return numerator / denominator
   ```

2. **Docstrings** - All functions documented (NumPy/Google style)
   ```python
   # Good
   def process_data(data: pd.DataFrame, threshold: float) -> pd.DataFrame:
       """
       Process data by filtering and transforming.

       Parameters
       ----------
       data : pd.DataFrame
           Input dataframe with 'value' column
       threshold : float
           Minimum value threshold

       Returns
       -------
       pd.DataFrame
           Filtered and processed data
       """
       ...
   ```

3. **Naming conventions** - All objects use `snake_case`
   ```python
   # Good
   customer_lifetime_value = calculate_clv(customer_data)

   # Bad
   customerLifetimeValue = calculate_clv(data)
   ```

4. **Import organization** - Grouped and sorted
   ```python
   # Good
   # Standard library
   import os
   from pathlib import Path
   from typing import List, Optional

   # Third-party
   import numpy as np
   import pandas as pd
   from sklearn.linear_model import LinearRegression

   # Local
   from my_package.utils import load_data
   ```

5. **Format and validate**
   ```bash
   black script.py
   ruff check script.py
   mypy script.py
   ```

## Quick Reference Checklist

Before committing Python code, verify:

- [ ] All functions have type hints
- [ ] All functions have docstrings (NumPy/Google style)
- [ ] All variables use `snake_case`
- [ ] No generic names (`data`, `df`, `result`, `temp`)
- [ ] Imports organized (stdlib → third-party → local)
- [ ] Use `.copy()` when modifying DataFrames
- [ ] Specific exception types (not bare `except:`)
- [ ] Informative error messages
- [ ] No mutable default arguments
- [ ] Formatted with `black` or `ruff`
- [ ] Passes `mypy` type checking
- [ ] Statistical tests report SE and CI

## Common Workflows

### Workflow 1: Clean Up AI-Generated Python Script

**Context**: AI generated a data analysis script with generic patterns.

**Steps**:

1. **Fix imports**
   ```python
   # Before
   from pandas import *
   import numpy as np
   from my_module import *

   # After
   from typing import Optional

   import numpy as np
   import pandas as pd

   from my_module import load_data, process_data
   ```

2. **Add type hints**
   ```python
   # Before
   def calculate_stats(data, column):
       return data[column].mean()

   # After
   def calculate_stats(data: pd.DataFrame, column: str) -> float:
       """Calculate mean for specified column."""
       return data[column].mean()
   ```

3. **Add docstrings**
   ```python
   # Before
   def filter_data(df, threshold):
       return df[df['value'] > threshold]

   # After
   def filter_data(
       data: pd.DataFrame,
       threshold: float
   ) -> pd.DataFrame:
       """
       Filter dataframe by value threshold.

       Parameters
       ----------
       data : pd.DataFrame
           Input dataframe with 'value' column
       threshold : float
           Minimum value to keep

       Returns
       -------
       pd.DataFrame
           Filtered dataframe
       """
       filtered_data = data.query("value > @threshold").copy()
       return filtered_data
   ```

4. **Fix pandas operations**
   ```python
   # Before
   df['new_col'] = df['value'] * 2  # modifies original
   result = df.groupby('category').agg({'value': 'mean'}).reset_index().sort_values('value')

   # After
   processed_data = data.copy()
   processed_data['new_col'] = processed_data['value'] * 2

   summary = (
       data
       .groupby('category')
       .agg(mean_value=('value', 'mean'))
       .reset_index()
       .sort_values('mean_value')
   )
   ```

5. **Format and validate**
   ```bash
   black script.py
   ruff check script.py
   mypy script.py
   ```

**Expected outcome**: Clean, type-safe, production-ready code

---

### Workflow 2: Add Error Handling

**Context**: Functions don't validate inputs or handle errors.

**Steps**:

1. **Add input validation**
   ```python
   def calculate_growth(initial: float, final: float, periods: int) -> float:
       """Calculate compound growth rate."""

       # Validate inputs
       if initial <= 0:
           raise ValueError(
               f"initial must be positive, got {initial}"
           )

       if periods <= 0:
           raise ValueError(
               f"periods must be positive, got {periods}"
           )

       growth_rate = (final / initial) ** (1 / periods) - 1
       return growth_rate
   ```

2. **Use specific exceptions**
   ```python
   # Before
   try:
       data = pd.read_csv(file_path)
   except:
       print("Error")
       return None

   # After
   try:
       data = pd.read_csv(file_path)
   except FileNotFoundError:
       raise FileNotFoundError(
           f"Data file not found: {file_path}\n"
           f"Current directory: {os.getcwd()}"
       )
   except pd.errors.ParserError as e:
       raise ValueError(
           f"Failed to parse CSV: {file_path}\n"
           f"Error: {str(e)}"
       ) from e
   ```

3. **Validate DataFrame structure**
   ```python
   def validate_columns(
       data: pd.DataFrame,
       required_cols: List[str]
   ) -> None:
       """Validate dataframe has required columns."""
       missing = set(required_cols) - set(data.columns)

       if missing:
           raise ValueError(
               f"Missing required columns: {missing}\n"
               f"Available: {list(data.columns)}"
           )
   ```

**Expected outcome**: Robust code with clear error messages

---

### Workflow 3: Prepare Module for Distribution

**Context**: Preparing code for PyPI or internal distribution.

**Steps**:

1. **Add type hints everywhere**
   ```bash
   mypy --strict my_module/
   ```

2. **Ensure all functions documented**
   ```python
   # Every public function needs docstring
   def public_function(arg: str) -> int:
       """
       Public API function.

       Parameters
       ----------
       arg : str
           Description

       Returns
       -------
       int
           Description
       """
       ...
   ```

3. **Format code**
   ```bash
   black my_module/
   ruff check my_module/ --fix
   ```

4. **Add tests**
   ```python
   # Use pytest with type-checked test functions
   def test_calculate_rate() -> None:
       """Test rate calculation."""
       result = calculate_rate(10.0, 2.0)
       assert result == 5.0
   ```

5. **Check test coverage**
   ```bash
   pytest --cov=my_module tests/
   ```

**Expected outcome**: Professional, distributable package

## Mandatory Rules Summary

### 1. Type Hints Required
**All function signatures must have type hints**

```python
from typing import List, Dict, Optional, Tuple

def process(data: pd.DataFrame, threshold: float = 0.5) -> pd.DataFrame:
    ...
```

### 2. Docstrings Required
**All functions need NumPy or Google style docstrings**

### 3. Naming: snake_case
**All objects use `snake_case`**
- Variables: `customer_data` not `customerData`
- Functions: `calculate_rate` not `calculateRate`
- No generic: `data`, `df`, `result`, `temp`

### 4. Import Organization
**Group and sort imports**
1. Standard library
2. Third-party (alphabetical)
3. Local imports

### 5. No Mutable Defaults
**Never use mutable default arguments**

```python
# Bad
def append_to_list(item, my_list=[]):
    ...

# Good
def append_to_list(item, my_list=None):
    if my_list is None:
        my_list = []
    ...
```

## PEP 8 Compliance

Follow [PEP 8](https://pep8.org/) style guide rigorously:

1. **Use automatic formatters**: `black`, `ruff`
2. **Type hints for clarity**: All public APIs
3. **Explicit over implicit**: Be clear about intentions
4. **Readable structure**: Format for humans

See **reference/pep8.md** for complete PEP 8 guidelines.

## Resources & Advanced Topics

### Reference Files

- **[reference/type-hints.md](reference/type-hints.md)** - Complete type hinting guide
- **[reference/pandas.md](reference/pandas.md)** - pandas method chaining and best practices
- **[reference/error-handling.md](reference/error-handling.md)** - Exception handling patterns
- **[reference/testing.md](reference/testing.md)** - pytest patterns and fixtures
- **[reference/imports.md](reference/imports.md)** - Import organization
- **[reference/formatting.md](reference/formatting.md)** - black, ruff, isort usage

### Related Skills

- **r/anti-slop** - For R users transitioning to Python
- **text/anti-slop** - For cleaning docstring prose

### Tools

- `black` - Uncompromising code formatter
- `ruff` - Fast linter and formatter
- `mypy` - Type checking
- `pytest` - Testing framework
- `isort` - Import sorting

## Integration with R Background

For R users, key differences:

| Concept | R | Python |
|---------|---|--------|
| Indexing | 1-based | 0-based |
| Assignment | `<-` or `=` | `=` only |
| Pipe equivalent | `\|>` | Method chaining `.` |
| Missing values | `NA` | `None`, `np.nan` |
| Data frames | `tibble` | `pd.DataFrame` |
| True/False | `TRUE`/`FALSE` | `True`/`False` |

See **reference/r-to-python.md** for complete migration guide.
