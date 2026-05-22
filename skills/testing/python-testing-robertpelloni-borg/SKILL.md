---
name: python-testing
description: Write and organize tests for scientific Python packages using pytest following Scientific Python community best practices. Use when setting up test suites, writing unit tests, integration tests, testing numerical algorithms, configuring test fixtures, parametrizing tests, or setting up continuous integration. Ideal for testing scientific computations, validating numerical accuracy, and ensuring code correctness.
---

# Scientific Python Testing with pytest

A comprehensive guide to writing effective tests for scientific Python packages using pytest, following the [Scientific Python Community guidelines](https://learn.scientific-python.org/development/guides/pytest/) and [testing tutorial](https://learn.scientific-python.org/development/tutorials/test/). This skill focuses on modern testing patterns, fixtures, parametrization, and best practices specific to scientific computing.

## Quick Reference Card

**Common Testing Tasks - Quick Decisions:**

```python
# 1. Basic test → Use simple assert
def test_function():
    assert result == expected

# 2. Floating-point comparison → Use approx
from pytest import approx
assert result == approx(0.333, rel=1e-6)

# 3. Testing exceptions → Use pytest.raises
with pytest.raises(ValueError, match="must be positive"):
    function(-1)

# 4. Multiple inputs → Use parametrize
@pytest.mark.parametrize("input,expected", [(1,1), (2,4), (3,9)])
def test_square(input, expected):
    assert input**2 == expected

# 5. Reusable setup → Use fixture
@pytest.fixture
def sample_data():
    return np.array([1, 2, 3, 4, 5])

# 6. NumPy arrays → Use approx or numpy.testing
assert np.mean(data) == approx(3.0)
```

**Decision Tree:**
- Need multiple test cases with same logic? → **Parametrize**
- Need reusable test data/setup? → **Fixture**
- Testing floating-point results? → **pytest.approx**
- Testing exceptions/warnings? → **pytest.raises / pytest.warns**
- Complex numerical arrays? → **numpy.testing.assert_allclose**
- Organizing by speed? → **Markers and separate directories**

## When to Use This Skill

- Writing tests for scientific Python packages and libraries
- Testing numerical algorithms and scientific computations
- Setting up test infrastructure for research software
- Implementing continuous integration for scientific code
- Testing data analysis pipelines and workflows
- Validating scientific simulations and models
- Ensuring reproducibility and correctness of research code
- Testing code that uses NumPy, SciPy, Pandas, and other scientific libraries

## Core Concepts

### 1. Why pytest for Scientific Python

pytest is the de facto standard for testing Python packages because it:

- **Simple syntax**: Just use Python's `assert` statement
- **Detailed reporting**: Clear, informative failure messages
- **Powerful features**: Fixtures, parametrization, marks, plugins
- **Scientific ecosystem**: Native support for NumPy arrays, approximate comparisons
- **Community standard**: Used by NumPy, SciPy, Pandas, scikit-learn, and more

### 2. Test Structure and Organization

**Standard test directory layout:**

```text
my-package/
├── src/
│   └── my_package/
│       ├── __init__.py
│       ├── analysis.py
│       └── utils.py
├── tests/
│   ├── conftest.py
│   ├── test_analysis.py
│   └── test_utils.py
└── pyproject.toml
```

**Key principles:**

- Tests directory separate from source code (alongside `src/`)
- Test files named `test_*.py` (pytest discovery)
- Test functions named `test_*` (pytest discovery)
- No `__init__.py` in tests directory (avoid importability issues)
- Test against installed package, not local source

### 3. pytest Configuration

See [assets/pyproject-pytest.toml](assets/pyproject-pytest.toml) for a complete pytest configuration example.

Basic configuration in `pyproject.toml`:

```toml
[tool.pytest.ini_options]
minversion = "7.0"
addopts = [
    "-ra",              # Show summary of all test outcomes
    "--showlocals",     # Show local variables in tracebacks
    "--strict-markers", # Error on undefined markers
    "--strict-config",  # Error on config issues
]
testpaths = ["tests"]
```

## Testing Principles

Following the [Scientific Python testing recommendations](https://learn.scientific-python.org/development/principles/testing/), effective testing provides multiple benefits and should follow key principles:

### Advantages of Testing

- **Trustworthy code**: Well-tested code behaves as expected and can be relied upon
- **Living documentation**: Tests communicate intent and expected behavior, validated with each run
- **Preventing failure**: Tests protect against implementation errors and unexpected dependency changes
- **Confidence when making changes**: Thorough test suites enable adding features, fixing bugs, and refactoring with confidence

### Fundamental Principles

**1. Any test case is better than none**

When in doubt, write the test that makes sense at the time:
- Test critical behaviors, features, and logic
- Write clear, expressive, well-documented tests
- Tests are documentation of developer intentions
- Good tests make it clear what they are testing and how

Don't get bogged down in taxonomy when learning—focus on writing tests that work.

**2. As long as that test is correct**

It's surprisingly easy to write tests that pass when they should fail:
- **Check that your test fails when it should**: Deliberately break the code and verify the test fails
- **Keep it simple**: Excessive mocks and fixtures make it difficult to know what's being tested
- **Test one thing at a time**: A single test should test a single behavior

**3. Start with Public Interface Tests**

Begin by testing from the perspective of a user:
- Test code as users will interact with it
- Keep tests simple and readable for documentation purposes
- Focus on supported use cases
- Avoid testing private attributes
- Minimize use of mocks/patches

**4. Organize Tests into Suites**

Divide tests by type and execution time for efficiency:
- **Unit tests**: Fast, isolated tests of individual components
- **Integration tests**: Tests of component interactions and dependencies
- **End-to-end tests**: Complete workflow testing

Benefits:
- Run relevant tests quickly and frequently
- "Fail fast" by running fast suites first
- Easier to read and reason about
- Avoid false positives from expected external failures

### Outside-In Testing Approach

The recommended approach is **outside-in**, starting from the user's perspective:

1. **Public Interface Tests**: Test from user perspective, focusing on behavior and features
2. **Integration Tests**: Test that components work together and with dependencies
3. **Unit Tests**: Test individual units in isolation, optimized for speed

This approach ensures you're building the right thing before optimizing implementation details.

## Quick Start

### Minimal Test Example

```python
# tests/test_basic.py

def test_simple_math():
    """Test basic arithmetic."""
    assert 4 == 2**2

def test_string_operations():
    """Test string methods."""
    result = "hello world".upper()
    assert result == "HELLO WORLD"
    assert "HELLO" in result
```

### Scientific Test Example

```python
# tests/test_scientific.py
import numpy as np
from pytest import approx

from my_package.analysis import compute_mean, fit_linear

def test_compute_mean():
    """Test mean calculation."""
    data = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    result = compute_mean(data)
    assert result == approx(3.0)

def test_fit_linear():
    """Test linear regression."""
    x = np.array([0, 1, 2, 3, 4])
    y = np.array([0, 2, 4, 6, 8])
    slope, intercept = fit_linear(x, y)
    
    assert slope == approx(2.0)
    assert intercept == approx(0.0)
```

## Testing Patterns

See [references/TEST_PATTERNS.md](references/TEST_PATTERNS.md) for detailed patterns including:
- Writing simple, focused tests
- Testing for failures
- Approximate comparisons
- Using fixtures
- Parametrized tests
- Test organization with markers
- Mocking and monkeypatching
- Testing against installed version
- Import best practices

## Scientific Python Testing Patterns

See [references/SCIENTIFIC_PATTERNS.md](references/SCIENTIFIC_PATTERNS.md) for scientific-specific patterns:
- Testing numerical algorithms
- Testing with different NumPy dtypes
- Testing random/stochastic code
- Testing data pipelines
- Property-based testing with Hypothesis

## Running pytest

### Basic Usage

```bash
# Run all tests
pytest

# Run specific file
pytest tests/test_analysis.py

# Run specific test
pytest tests/test_analysis.py::test_mean

# Run tests matching pattern
pytest -k "mean or median"

# Verbose output
pytest -v

# Show local variables in failures
pytest -l  # or --showlocals

# Stop at first failure
pytest -x

# Show stdout/stderr
pytest -s
```

### Debugging Tests

```bash
# Drop into debugger on failure
pytest --pdb

# Drop into debugger at start of each test
pytest --trace

# Run last failed tests
pytest --lf

# Run failed tests first, then rest
pytest --ff

# Show which tests would be run (dry run)
pytest --collect-only
```

### Coverage

```bash
# Install pytest-cov
pip install pytest-cov

# Run with coverage
pytest --cov=my_package

# With coverage report
pytest --cov=my_package --cov-report=html

# With missing lines
pytest --cov=my_package --cov-report=term-missing

# Fail if coverage below threshold
pytest --cov=my_package --cov-fail-under=90
```

See [assets/pyproject-pytest.toml](assets/pyproject-pytest.toml) for complete coverage configuration.

## File Templates and Examples

Ready-to-use templates are available in the `assets/` directory:

- **[assets/pyproject-pytest.toml](assets/pyproject-pytest.toml)** - Complete pytest configuration with coverage
- **[assets/conftest-example.py](assets/conftest-example.py)** - Example conftest.py with shared fixtures
- **[assets/github-actions-tests.yml](assets/github-actions-tests.yml)** - GitHub Actions workflow for testing

## Common Pitfalls and Solutions

See [references/COMMON_PITFALLS.md](references/COMMON_PITFALLS.md) for solutions to:
- Testing implementation instead of behavior
- Non-deterministic tests
- Exact floating-point comparisons
- Testing too much in one test

## Testing Checklist

- [ ] Tests are in `tests/` directory separate from source
- [ ] Test files named `test_*.py`
- [ ] Test functions named `test_*`
- [ ] Tests run against installed package (use src/ layout)
- [ ] pytest configured in `pyproject.toml`
- [ ] Using `pytest.approx` for floating-point comparisons
- [ ] Tests check exceptions with `pytest.raises`
- [ ] Tests check warnings with `pytest.warns`
- [ ] Parametrized tests for multiple inputs
- [ ] Fixtures for reusable setup
- [ ] Markers used for test organization
- [ ] Random tests use fixed seeds
- [ ] Tests are independent (can run in any order)
- [ ] Each test focuses on one behavior
- [ ] Coverage > 80% (preferably > 90%)
- [ ] All tests pass before committing
- [ ] Slow tests marked with `@pytest.mark.slow`
- [ ] Integration tests marked appropriately
- [ ] CI configured to run tests automatically

## Continuous Integration

See [assets/github-actions-tests.yml](assets/github-actions-tests.yml) for a complete GitHub Actions workflow example.

## Resources

- **Scientific Python pytest Guide**: <https://learn.scientific-python.org/development/guides/pytest/>
- **Scientific Python Testing Tutorial**: <https://learn.scientific-python.org/development/tutorials/test/>
- **Scientific Python Testing Principles**: <https://learn.scientific-python.org/development/principles/testing/>
- **pytest Documentation**: <https://docs.pytest.org/>
- **pytest-cov**: <https://pytest-cov.readthedocs.io/>
- **pytest-mock**: <https://pytest-mock.readthedocs.io/>
- **Hypothesis (property-based testing)**: <https://hypothesis.readthedocs.io/>
- **NumPy testing utilities**: <https://numpy.org/doc/stable/reference/routines.testing.html>
- **Testing best practices**: <https://docs.python-guide.org/writing/tests/>

## Summary

Testing scientific Python code with pytest, following Scientific Python community principles, provides:

1. **Confidence**: Know your code works correctly
2. **Reproducibility**: Ensure consistent behavior across environments
3. **Documentation**: Tests show how code should be used and communicate developer intent
4. **Refactoring safety**: Change code without breaking functionality
5. **Regression prevention**: Catch bugs before they reach users
6. **Scientific rigor**: Validate numerical accuracy and physical correctness

**Key testing principles:**

- Start with **public interface tests** from the user's perspective
- Organize tests into **suites** (unit, integration, e2e) by type and speed
- Follow **outside-in** approach: public interface → integration → unit tests
- Keep tests **simple, focused, and independent**
- Test **behavior rather than implementation**
- Use pytest's powerful features (fixtures, parametrization, markers) effectively
- Always verify tests **fail when they should** to avoid false confidence

**Remember**: Any test is better than none, but well-organized tests following these principles create trustworthy, maintainable scientific software that the community can rely on.
