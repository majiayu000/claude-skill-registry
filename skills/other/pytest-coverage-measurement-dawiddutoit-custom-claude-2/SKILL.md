---
name: pytest-coverage-measurement
description: |
  Measure and track test coverage: coverage thresholds by layer, coverage reporting (HTML/terminal), identifying coverage gaps, branch coverage vs line coverage, coverage-driven testing. Includes layer-specific targets (domain 95%, application 85%, adapters 75%).

  Use when: Measuring test coverage, setting coverage thresholds, identifying untested code paths, tracking coverage improvements, ensuring code quality gates.
allowed-tools: Read, Bash, Write
---

# Pytest Coverage Measurement

## Purpose

Code coverage measures how much of your code is tested. This skill provides strategies for meaningful coverage measurement and improving test quality.


## When to Use This Skill

Use when measuring test coverage with "measure coverage", "track coverage", "identify untested code", or "set coverage thresholds".

Do NOT use for writing tests (use layer-specific testing skills), pytest configuration (use `pytest-configuration`), or fixing low coverage (identify gaps first, then use appropriate testing skill).
## Quick Start

Generate coverage report:

```bash
# Generate HTML coverage report
pytest --cov=app --cov-report=html --cov-report=term-missing

# View HTML report
open htmlcov/index.html

# Fail if coverage below threshold
pytest --cov=app --cov-fail-under=80
```

## Instructions

### Step 1: Configure Coverage in pyproject.toml

```toml
[tool.pytest.ini_options]
addopts = [
    "--cov=app",                        # Source to measure
    "--cov-report=html",                # HTML report
    "--cov-report=term-missing",        # Terminal with missing lines
    "--cov-fail-under=80",              # Fail if < 80%
]

[tool.coverage.run]
source = ["app"]
branch = true  # Measure branch coverage (if/else paths)

omit = [
    "*/tests/*",
    "*/__pycache__/*",
    "*/venv/*",
    "*/.venv/*",
]

[tool.coverage.report]
precision = 2
show_missing = true
skip_covered = false  # Show all files, including 100% covered

# Lines to exclude from coverage
exclude_lines = [
    "pragma: no cover",                 # Manual exclusion
    "def __repr__",                     # Repr methods
    "raise NotImplementedError",        # Abstract methods
    "if TYPE_CHECKING:",                # Type checking only
    "if __name__ == .__main__.:",       # CLI entry points
    "@(abc\\.)?abstractmethod",         # Abstract methods
    "class .*\\bProtocol\\):",          # Protocols
]

[tool.coverage.html]
directory = "htmlcov"  # Output directory
```

### Step 2: Understand Line vs Branch Coverage

```python
from __future__ import annotations


# Line coverage: counts executed lines
# Branch coverage: counts each if/else path

def validate_order(order: Order) -> bool:
    """Example of branch coverage."""
    if not order.line_items:  # Branch 1: True
        return False  # Branch 2: False (2 paths)

    if order.total_price < 0:  # Branch 3: True
        return False  # Branch 4: False (2 more paths)

    return True  # Branch 5: Total 4 unique paths


# Test 1: Only tests the happy path
def test_valid_order():
    order = Order(line_items=[item], total_price=Money(100))
    assert validate_order(order) is True
    # Coverage: 5 lines, 2 branches (50% branch coverage)


# Test 2-5: Cover all paths for 100% branch coverage
def test_empty_items():
    order = Order(line_items=[], total_price=Money(100))
    assert validate_order(order) is False

def test_negative_total():
    order = Order(line_items=[item], total_price=Money(-100))
    assert validate_order(order) is False

def test_valid_order_all_paths():
    order = Order(line_items=[item], total_price=Money(100))
    assert validate_order(order) is True
    # Coverage: 5 lines, 4 branches (100% branch coverage)
```

### Step 3: Set Coverage Targets by Layer

```python
# Domain Layer: 95-100% coverage
# app/extraction/domain/
# app/storage/domain/
# app/reporting/domain/
#
# Pure business logic, no dependencies → easy to test exhaustively


# Application Layer: 85-95% coverage
# app/extraction/application/
# app/storage/application/
# app/reporting/application/
#
# Use cases, orchestration → test main paths, some error paths


# Adapter Layer: 75-85% coverage
# app/extraction/adapters/
# app/storage/adapters/
# app/reporting/adapters/
#
# External integrations → test critical paths, less error paths


# Infrastructure Layer: 60-75% coverage
# app/shared/
# Configuration, setup code → test critical paths only
```

### Step 4: Run Coverage and Analyze Report

```bash
# Generate full report
pytest --cov=app --cov-report=html --cov-report=term-missing

# Output shows missing lines:
# Name                     Stmts  Miss  Cover   Missing
# ------------------------------------------------
# app/extraction/domain/entities.py    45     0   100%
# app/extraction/domain/value_objects  20     0   100%
# app/extraction/application/use_cases 60     5    92%   45-47, 89-91
# app/reporting/domain/entities.py     30     0   100%
# ------------------------------------------------
# TOTAL                              500    50    85%
```

### Step 5: Identify Coverage Gaps

```bash
# Coverage by directory
pytest --cov=app/extraction --cov-report=term-missing

# Coverage for specific file
pytest --cov=app/extraction/domain --cov-report=term-missing

# View HTML report for interactive analysis
open htmlcov/app_extraction_domain_entities_py.html

# Check branch coverage specifically
pytest --cov=app --cov-report=term-missing:skip-covered
```

### Step 6: Exclude Lines Appropriately

```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    # Type checking only imports, never executed at runtime
    from myapp.domain.entities import Order


class BaseRepository(Protocol):
    """Protocol for repositories."""

    def save(self, entity: Entity) -> None:  # pragma: no cover
        """Abstract method, no implementation."""
        ...


def __repr__(self) -> str:  # pragma: no cover
    """Repr method, low value to test."""
    return f"Order(id={self.id})"


if __name__ == "__main__":  # pragma: no cover
    # CLI entry point, tested separately
    main()


@abstractmethod
def abstract_method(self) -> None:  # pragma: no cover
    """Abstract method, no implementation."""
    pass
```

### Step 7: Track Coverage Trends

```python
# Save coverage data to JSON for tracking
pytest --cov=app --cov-report=json

# Then analyze coverage.json to track improvements over time
import json

with open("coverage.json") as f:
    data = json.load(f)

total_coverage = data["totals"]["percent_covered"]
print(f"Total coverage: {total_coverage}%")

# Track per module
for module, coverage in data["files"].items():
    print(f"{module}: {coverage['summary']['percent_covered']}%")
```

### Step 8: Create Coverage Badges and Reports

```bash
# Generate coverage report that CI/CD can use
pytest --cov=app --cov-report=xml --cov-report=term

# Upload to coverage tracking services:
# - codecov.io
# - coveralls.io
# - codeclimate.com
```

### Step 9: Enforce Coverage in CI/CD

```yaml
# GitHub Actions example
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Install uv
        run: curl -LsSf https://astral.sh/uv/install.sh | sh

      - name: Install dependencies
        run: uv sync

      - name: Run tests with coverage
        run: uv run pytest --cov=app --cov-report=xml --cov-fail-under=80

      - name: Upload coverage to codecov
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage.xml
          fail_ci_if_error: true
```

### Step 10: Coverage-Driven Test Development

```python
# Process:
# 1. Run coverage before writing tests
# 2. Identify untested lines
# 3. Write tests to cover them
# 4. Re-run coverage to verify

from app.extraction.domain.value_objects import ProductTitle

# Before tests:
# ProductTitle: 20 lines, 0% covered

# Run tests:
# pytest --cov=app/extraction/domain --cov-report=term-missing

# See missing lines in output:
# ProductTitle: 20 lines, 5 missing → 75% covered

# Write tests for missing lines:
# - test_valid_title
# - test_title_too_long
# - test_immutability
# - test_equality
# - test_hashing

# After tests:
# ProductTitle: 20 lines, 0 missing → 100% covered
```

## Examples

### Example 1: Complete Coverage Configuration

```toml
[tool.pytest.ini_options]
addopts = [
    "--strict-markers",
    "--cov=app",
    "--cov-report=html",
    "--cov-report=term-missing",
    "--cov-report=xml",
    "--cov-fail-under=80",
]

[tool.coverage.run]
source = ["app"]
branch = true
omit = [
    "*/tests/*",
    "*/__pycache__/*",
    "*/venv/*",
    "*/.venv/*",
]

[tool.coverage.report]
precision = 2
show_missing = true
skip_covered = false

exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise NotImplementedError",
    "if TYPE_CHECKING:",
    "if __name__ == .__main__.:",
    "@(abc\\.)?abstractmethod",
    "class .*\\bProtocol\\):",
]

[[tool.coverage.paths]]
source = ["app"]
tests = ["tests"]

[tool.coverage.html]
directory = "htmlcov"

[tool.coverage.xml]
output = "coverage.xml"
```

### Example 2: Layer-Specific Coverage Tracking

```python
# Create script to track coverage by layer
import subprocess
import json
from pathlib import Path

def get_coverage_by_module():
    """Get coverage report for each module."""
    result = subprocess.run(
        ["pytest", "--cov=app", "--cov-report=json"],
        capture_output=True,
        text=True,
    )

    with open("coverage.json") as f:
        data = json.load(f)

    # Organize by layer
    layers = {
        "domain": [],
        "application": [],
        "adapters": [],
        "infrastructure": [],
    }

    for module, coverage_data in data["files"].items():
        percent = coverage_data["summary"]["percent_covered"]

        if "domain" in module:
            layers["domain"].append((module, percent))
        elif "application" in module:
            layers["application"].append((module, percent))
        elif "adapters" in module:
            layers["adapters"].append((module, percent))
        else:
            layers["infrastructure"].append((module, percent))

    # Print summary
    for layer_name, modules in layers.items():
        if modules:
            avg = sum(p for _, p in modules) / len(modules)
            print(f"{layer_name}: {avg:.1f}%")
            for module, percent in modules:
                print(f"  {module}: {percent:.1f}%")

if __name__ == "__main__":
    get_coverage_by_module()
```

### Example 3: Identifying Coverage Gaps

```bash
# Find uncovered code in specific module
pytest --cov=app/extraction/domain --cov-report=term-missing app/extraction/domain

# View which lines need tests
# app/extraction/domain/entities.py:45 if order.total < 0:
# app/extraction/domain/entities.py:46     raise ValueError()
# app/extraction/domain/entities.py:47
# app/extraction/domain/entities.py:89 except InvalidOrderException:
# app/extraction/domain/entities.py:90     logger.error()
# app/extraction/domain/entities.py:91

# Write tests to cover those lines
def test_negative_total_raises_error():
    """Test line 45-46."""
    with pytest.raises(ValueError):
        Order(..., total_price=Money(-100))

def test_invalid_order_caught():
    """Test line 89-91."""
    # Test code that triggers the exception handler
```

## Requirements

- Python 3.11+
- pytest >= 7.0
- pytest-cov >= 4.0

## See Also

- [pytest-configuration](../pytest-configuration/SKILL.md) - Coverage configuration details
- [pytest-domain-model-testing](../pytest-domain-model-testing/SKILL.md) - Achieving 95%+ on domain
- [PYTHON_UNIT_TESTING_BEST_PRACTICES.md](../../artifacts/2025-11-09/testing-research/PYTHON_UNIT_TESTING_BEST_PRACTICES.md) - Section: "Coverage Targets & Measurement"
- [PROJECT_UNIT_TESTING_STRATEGY.md](../../artifacts/2025-11-09/testing-research/PROJECT_UNIT_TESTING_STRATEGY.md) - Section: "Coverage Tracking Approach"
