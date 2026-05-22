---
name: software-developer
description: Use when implementing production-quality bioinformatics software with proper error handling, logging, testing, and documentation, following software engineering best practices.
success_criteria:
  - Code passes all tests (unit, integration, type checking)
  - Follows project style guide and linting rules
  - Includes comprehensive error handling
  - Docstrings provided for all public functions/classes
  - No security vulnerabilities detected
  - Code reviewed by copilot before handoff
  - Documentation complete and accurate
metadata:
    skill-author: David Angeles Albores
    category: bioinformatics-workflow
    workflow: software-development
    integrates-with: [systems-architect, copilot, biologist-commentator]
allowed-tools: [Read, Write, Edit, Bash, Skill]
---

# Software Developer Skill

## Purpose

Implement production-quality bioinformatics software from technical specifications with comprehensive testing, documentation, and error handling.

## When to Use This Skill

Use this skill when you need to:
- Implement software from architecture specification
- Write production-ready code (not exploratory analysis)
- Create command-line tools or packages
- Build reusable libraries
- Ensure code quality through testing

## Workflow Integration

**Pattern: Receive Spec → Implement → Test → Document → Deliver**
```
Systems Architect provides technical spec
    ↓
Software Developer implements
    ↓  (copilot reviews continuously)
Biologist Commentator validates biological correctness
    ↓
Production-ready software
```

## Core Capabilities

### 1. Implementation from Spec
- Translate architecture into working code
- Modular, reusable functions/classes
- Follow coding standards (PEP 8)
- Type hints for clarity

### 2. Error Handling
- Try/except with informative messages
- Validate inputs
- Graceful failure
- Logging for debugging

### 3. Testing
- Unit tests (pytest)
- Integration tests
- Edge case coverage
- >80% code coverage goal

### 4. Documentation
- Docstrings (Google style)
- README with usage examples
- API reference
- Troubleshooting guide

### 5. CLI Interface
- argparse or Click
- Help messages
- Progress bars for long operations
- Sensible defaults

## Standard Package Structure

Use `assets/package_structure_template/`:

```
project_name/
├── src/
│   ├── __init__.py
│   ├── module1.py
│   ├── module2.py
│   └── cli.py
├── tests/
│   ├── test_module1.py
│   ├── test_module2.py
│   ├── fixtures/
│   └── test_data/
├── docs/
│   ├── usage.md
│   └── api.md
├── README.md
├── setup.py
├── pyproject.toml
├── requirements.txt
├── environment.yml
└── .gitignore
```

## Code Quality Standards

### Docstring Format (Google Style)
```python
def calculate_cpm(counts: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate counts per million (CPM) normalization.

    Parameters
    ----------
    counts : pd.DataFrame
        Raw count matrix (genes × samples)

    Returns
    -------
    pd.DataFrame
        CPM-normalized counts

    Raises
    ------
    ValueError
        If counts contain negative values

    Examples
    --------
    >>> counts = pd.DataFrame({'A': [10, 20], 'B': [30, 40]})
    >>> cpm = calculate_cpm(counts)
    >>> cpm['A'].sum()  # Should be ~1,000,000
    1000000.0
    """
    if (counts < 0).any().any():
        raise ValueError("Counts cannot be negative")

    return (counts / counts.sum(axis=0)) * 1e6
```

### Error Handling
```python
# ✅ Good: Informative error messages
try:
    data = pd.read_csv(filepath)
except FileNotFoundError:
    raise FileNotFoundError(
        f"Data file not found: {filepath}\n"
        f"Expected location: {Path(filepath).absolute()}"
    )
except pd.errors.EmptyDataError:
    raise ValueError(
        f"Data file is empty: {filepath}\n"
        f"Check that file was generated correctly"
    )
```

### Logging
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def process_samples(sample_list):
    logger.info(f"Processing {len(sample_list)} samples")
    for i, sample in enumerate(sample_list):
        logger.debug(f"Processing sample {i+1}/{len(sample_list)}: {sample}")
        # ... processing code ...
    logger.info("Processing complete")
```

### Testing with pytest
```python
# tests/test_normalization.py
import pytest
import pandas as pd
import numpy as np
from src.normalization import calculate_cpm

def test_cpm_sum_equals_million():
    """Test that CPM normalization sums to ~1 million."""
    counts = pd.DataFrame({'A': [10, 20, 30], 'B': [40, 50, 60]})
    cpm = calculate_cpm(counts)
    assert np.allclose(cpm.sum(axis=0), 1e6)

def test_cpm_raises_on_negative():
    """Test that negative counts raise ValueError."""
    counts = pd.DataFrame({'A': [-10, 20], 'B': [30, 40]})
    with pytest.raises(ValueError, match="negative"):
        calculate_cpm(counts)

def test_cpm_handles_zero_sum():
    """Test behavior when column sums to zero."""
    counts = pd.DataFrame({'A': [0, 0], 'B': [10, 20]})
    # Should handle gracefully (decide behavior: NaN or raise)
```

## CLI Template

See `assets/cli_template.py`:

```python
#!/usr/bin/env python3
"""
QC Pipeline CLI

Usage:
    qc_pipeline samples.csv --output results/
"""

import click
import logging
from pathlib import Path

@click.command()
@click.argument('sample_file', type=click.Path(exists=True))
@click.option('--output', '-o', default='results/', help='Output directory')
@click.option('--threads', '-t', default=4, help='Number of threads')
@click.option('--verbose', '-v', is_flag=True, help='Verbose logging')
def main(sample_file, output, threads, verbose):
    """Run QC pipeline on samples."""

    # Setup logging
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=level)
    logger = logging.getLogger(__name__)

    # Validate inputs
    output_dir = Path(output)
    output_dir.mkdir(parents=True, exist_ok=True)

    logger.info(f"Processing samples from {sample_file}")
    logger.info(f"Output directory: {output_dir}")
    logger.info(f"Using {threads} threads")

    # Main logic
    try:
        # ... pipeline code ...
        logger.info("Pipeline complete!")
    except Exception as e:
        logger.error(f"Pipeline failed: {e}")
        raise

if __name__ == '__main__':
    main()
```

## Testing Strategy

### 1. Unit Tests
Test individual functions in isolation.

### 2. Integration Tests
Test components working together.

### 3. Regression Tests
Save expected outputs, compare to current.

### 4. Edge Case Tests
- Empty input
- Single element
- All zeros
- Missing values
- Very large input

## Copilot Integration

During implementation:
1. Write code section
2. Copilot reviews immediately
3. Fix critical issues before proceeding
4. Iterate until approved
5. Move to next section

## Quality Checklist

Before delivery:
- [ ] All code passes tests (pytest)
- [ ] >80% test coverage
- [ ] All public functions documented
- [ ] Error messages are actionable
- [ ] CLI help message clear
- [ ] README with installation + usage
- [ ] Example data/workflow provided
- [ ] Copilot approved (no critical issues)
- [ ] Biologist validated (biological correctness)

## References

For detailed standards:
- `references/coding_standards.md` - PEP 8, naming, function length
- `references/testing_patterns.md` - pytest, fixtures, mocking
- `references/error_handling_guide.md` - Exception hierarchy, logging
- `references/documentation_standards.md` - Docstrings, README, API docs

## Scripts

Available in `scripts/`:
- `project_template_generator.py` - Creates project structure
- `test_runner.py` - Runs pytest with coverage

## Success Criteria

Code is ready for production when:
- [ ] Implements full specification
- [ ] All tests pass
- [ ] Coverage >80%
- [ ] Documentation complete
- [ ] CLI functional
- [ ] Copilot approved
- [ ] Biologist validated
- [ ] Ready for deployment
