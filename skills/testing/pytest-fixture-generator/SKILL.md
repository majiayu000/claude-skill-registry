---
name: pytest-fixture-generator
description: Generate standardized pytest configuration with fixtures, markers, and coverage settings. Creates conftest.py and pytest.ini for workspace-hub compliant testing.
version: 1.0.0
category: workspace-hub
type: skill
trigger: manual
auto_execute: false
capabilities:
  - pytest_configuration
  - fixture_generation
  - coverage_setup
  - marker_configuration
  - path_management
tools:
  - Write
  - Read
  - Bash
related_skills:
  - python-project-template
  - repo-readiness
---

# Pytest Fixture Generator

> Generate standardized pytest configuration compliant with workspace-hub testing standards.

## Quick Start

```bash
# Generate pytest configuration
/pytest-fixture-generator

# Generate with specific markers
/pytest-fixture-generator --markers unit,integration,slow

# Generate for specific module structure
/pytest-fixture-generator --src-path src/modules
```

## When to Use

**USE when:**
- Setting up new Python project testing
- Standardizing existing test configuration
- Adding fixtures for data processing projects
- Configuring coverage requirements

**DON'T USE when:**
- Non-Python projects
- Tests already fully configured
- Different testing framework needed

## Prerequisites

- Python 3.9+
- pytest>=7.4.0
- pytest-cov>=4.1.0
- Project with src/ structure

## Overview

Generates complete pytest configuration including:

1. **pytest.ini** - pytest configuration with markers
2. **conftest.py** - Shared fixtures and path setup
3. **Coverage config** - .coveragerc or pyproject.toml
4. **Test templates** - Example test files

## Generated Files

### pytest.ini

```ini
[pytest]
testpaths = tests
python_files = test_*.py *_test.py
python_classes = Test*
python_functions = test_*

# Markers for test categorization
markers =
    unit: Unit tests (fast, isolated)
    integration: Integration tests (may use external resources)
    slow: Slow running tests (> 1 second)
    llm: Tests requiring LLM API (may be skipped in CI)
    scrapy: Web scraping tests
    selenium: Browser automation tests
    database: Database interaction tests
    api: External API tests
    etl: ETL pipeline tests

# Default options
addopts =
    -v
    --strict-markers
    --tb=short
    --cov=src
    --cov-report=term-missing
    --cov-fail-under=80

# Async support
asyncio_mode = auto

# Timeout for tests
timeout = 300

# Filter warnings
filterwarnings =
    ignore::DeprecationWarning
    ignore::PendingDeprecationWarning
```

### conftest.py

```python
"""
ABOUTME: Pytest configuration and shared fixtures for testing
ABOUTME: Provides path setup, common fixtures, and test utilities
"""

import sys
from pathlib import Path
from typing import Any, Dict, Generator
import pytest
import logging

# ============================================================================
# Path Configuration
# ============================================================================

# Get project root
PROJECT_ROOT = Path(__file__).parent.parent
SRC_PATH = PROJECT_ROOT / "src"
MODULES_PATH = SRC_PATH / "modules"

# Add paths to sys.path for imports (deduplicated)
paths_to_add = [str(SRC_PATH), str(MODULES_PATH)]
for path in paths_to_add:
    if path not in sys.path:
        sys.path.insert(0, path)


# ============================================================================
# Platform-specific Skipping
# ============================================================================

def is_windows() -> bool:
    """Check if running on Windows."""
    return sys.platform.startswith('win')


def is_orcaflex_available() -> bool:
    """Check if OrcaFlex is available."""
    try:
        import OrcFxAPI
        return True
    except ImportError:
        return False


# Skip markers
skip_if_not_windows = pytest.mark.skipif(
    not is_windows(),
    reason="Windows-only test"
)

skip_if_no_orcaflex = pytest.mark.skipif(
    not is_orcaflex_available(),
    reason="OrcaFlex not available"
)


# ============================================================================
# Logging Configuration
# ============================================================================

@pytest.fixture(scope="session")
def configure_logging():
    """Configure logging for test session."""
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    return logging.getLogger("test")


# ============================================================================
# Path Fixtures
# ============================================================================

@pytest.fixture(scope="session")
def project_root() -> Path:
    """Return project root directory."""
    return PROJECT_ROOT


@pytest.fixture(scope="session")
def data_dir(project_root) -> Path:
    """Return data directory path."""
    return project_root / "data"


@pytest.fixture(scope="session")
def raw_data_dir(data_dir) -> Path:
    """Return raw data directory path."""
    return data_dir / "raw"


@pytest.fixture(scope="session")
def test_data_dir() -> Path:
    """Return test fixtures directory."""
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def temp_output_dir(tmp_path) -> Path:
    """Return temporary output directory for test."""
    output_dir = tmp_path / "output"
    output_dir.mkdir(exist_ok=True)
    return output_dir


# ============================================================================
# Sample Data Fixtures
# ============================================================================

@pytest.fixture
def sample_dict() -> Dict[str, Any]:
    """Provide sample dictionary data."""
    return {
        "name": "test_item",
        "value": 42,
        "enabled": True,
        "items": [1, 2, 3, 4, 5],
        "metadata": {
            "created": "2026-01-14",
            "author": "tester"
        }
    }


@pytest.fixture
def sample_list() -> list:
    """Provide sample list data."""
    return [
        {"id": 1, "value": 10},
        {"id": 2, "value": 20},
        {"id": 3, "value": 30},
    ]


@pytest.fixture
def sample_dataframe():
    """Provide sample pandas DataFrame."""
    import pandas as pd
    return pd.DataFrame({
        "id": [1, 2, 3, 4, 5],
        "name": ["a", "b", "c", "d", "e"],
        "value": [10.0, 20.0, 30.0, 40.0, 50.0],
        "category": ["x", "y", "x", "y", "x"]
    })


@pytest.fixture
def sample_time_series():
    """Provide sample time series DataFrame."""
    import pandas as pd
    import numpy as np

    dates = pd.date_range("2026-01-01", periods=100, freq="D")
    return pd.DataFrame({
        "date": dates,
        "value": np.random.randn(100).cumsum() + 100,
        "volume": np.random.randint(100, 1000, 100)
    })


# ============================================================================
# Configuration Fixtures
# ============================================================================

@pytest.fixture
def temp_config(tmp_path) -> Path:
    """Create temporary YAML configuration file."""
    config_file = tmp_path / "config.yaml"
    config_file.write_text("""
metadata:
  name: test-config
  version: 1.0.0

settings:
  debug: true
  log_level: DEBUG
  output_dir: ./output

input:
  source: data/input.csv
  encoding: utf-8

output:
  format: html
  path: reports/output.html
""")
    return config_file


@pytest.fixture
def temp_csv(tmp_path, sample_dataframe) -> Path:
    """Create temporary CSV file with sample data."""
    csv_path = tmp_path / "test_data.csv"
    sample_dataframe.to_csv(csv_path, index=False)
    return csv_path


# ============================================================================
# Mock Fixtures
# ============================================================================

@pytest.fixture
def mock_api_response() -> Dict[str, Any]:
    """Provide mock API response."""
    return {
        "status": "success",
        "data": [
            {"id": 1, "result": "ok"},
            {"id": 2, "result": "ok"},
        ],
        "metadata": {
            "total": 2,
            "page": 1
        }
    }


@pytest.fixture
def mock_error_response() -> Dict[str, Any]:
    """Provide mock error response."""
    return {
        "status": "error",
        "error": {
            "code": "INVALID_INPUT",
            "message": "Input validation failed"
        }
    }


# ============================================================================
# Cleanup Fixtures
# ============================================================================

@pytest.fixture(autouse=True)
def cleanup_after_test():
    """Cleanup after each test."""
    yield
    # Add cleanup logic here if needed


@pytest.fixture(scope="session", autouse=True)
def cleanup_after_session():
    """Cleanup after test session."""
    yield
    # Add session cleanup here if needed


# ============================================================================
# Helper Functions
# ============================================================================

def assert_dataframe_equal(df1, df2, **kwargs):
    """Assert two DataFrames are equal with helpful error messages."""
    import pandas as pd
    pd.testing.assert_frame_equal(df1, df2, **kwargs)


def assert_dict_subset(subset: Dict, superset: Dict):
    """Assert subset dict is contained in superset."""
    for key, value in subset.items():
        assert key in superset, f"Key '{key}' not found"
        assert superset[key] == value, f"Value mismatch for '{key}'"


# Make helpers available to tests
@pytest.fixture
def df_equal():
    """Provide DataFrame equality assertion."""
    return assert_dataframe_equal


@pytest.fixture
def dict_subset():
    """Provide dict subset assertion."""
    return assert_dict_subset
```

### Example Test File

```python
"""
ABOUTME: Example test file demonstrating pytest patterns
ABOUTME: Shows usage of fixtures and markers
"""

import pytest


class TestExampleUnit:
    """Unit tests for example module."""

    @pytest.mark.unit
    def test_basic_functionality(self, sample_dict):
        """Test basic functionality with sample data."""
        assert sample_dict["name"] == "test_item"
        assert sample_dict["value"] == 42

    @pytest.mark.unit
    def test_list_processing(self, sample_list):
        """Test list processing."""
        assert len(sample_list) == 3
        total = sum(item["value"] for item in sample_list)
        assert total == 60

    @pytest.mark.unit
    def test_dataframe_operations(self, sample_dataframe):
        """Test DataFrame operations."""
        assert len(sample_dataframe) == 5
        assert "value" in sample_dataframe.columns
        assert sample_dataframe["value"].sum() == 150.0


class TestExampleIntegration:
    """Integration tests demonstrating external resource usage."""

    @pytest.mark.integration
    def test_config_loading(self, temp_config):
        """Test loading configuration file."""
        import yaml

        with open(temp_config) as f:
            config = yaml.safe_load(f)

        assert config["metadata"]["name"] == "test-config"
        assert config["settings"]["debug"] is True

    @pytest.mark.integration
    def test_csv_processing(self, temp_csv, sample_dataframe):
        """Test CSV file processing."""
        import pandas as pd

        loaded = pd.read_csv(temp_csv)
        assert len(loaded) == len(sample_dataframe)

    @pytest.mark.integration
    @pytest.mark.slow
    def test_time_series_analysis(self, sample_time_series):
        """Test time series analysis (may be slow)."""
        assert len(sample_time_series) == 100
        assert sample_time_series["date"].dtype == "datetime64[ns]"


class TestExampleMarkers:
    """Tests demonstrating various markers."""

    @pytest.mark.unit
    def test_fast_operation(self):
        """Fast unit test."""
        result = 1 + 1
        assert result == 2

    @pytest.mark.slow
    def test_slow_operation(self):
        """Slow test (marked for selective execution)."""
        import time
        time.sleep(0.1)
        assert True

    @pytest.mark.skip(reason="Not implemented yet")
    def test_future_feature(self):
        """Test for future feature."""
        pass

    @pytest.mark.xfail(reason="Known bug, tracked in issue #123")
    def test_known_bug(self):
        """Test for known bug."""
        assert False


@pytest.mark.parametrize("input_val,expected", [
    (1, 2),
    (2, 4),
    (3, 6),
    (0, 0),
    (-1, -2),
])
def test_parametrized_doubling(input_val, expected):
    """Parametrized test for doubling function."""
    result = input_val * 2
    assert result == expected
```

## Usage Examples

### Example 1: Generate Basic Configuration

```bash
# Generate for standard project
/pytest-fixture-generator

# Creates:
# - pytest.ini
# - tests/conftest.py
# - tests/test_example.py
```

### Example 2: Custom Markers

```bash
# Generate with domain-specific markers
/pytest-fixture-generator --markers unit,integration,api,database,etl
```

### Example 3: Specific Coverage Target

```bash
# Generate with 90% coverage requirement
/pytest-fixture-generator --coverage 90
```

## Execution Checklist

**Setup:**
- [ ] pytest and pytest-cov installed
- [ ] Project has src/ directory structure
- [ ] tests/ directory exists

**Generation:**
- [ ] Generate pytest.ini
- [ ] Generate conftest.py
- [ ] Create example test file
- [ ] Configure coverage

**Verification:**
- [ ] Run `pytest --collect-only` to verify discovery
- [ ] Run `pytest -v` to execute tests
- [ ] Check coverage report

## Common Fixtures Reference

| Fixture | Scope | Purpose |
|---------|-------|---------|
| `project_root` | session | Project root path |
| `data_dir` | session | Data directory path |
| `test_data_dir` | session | Test fixtures path |
| `temp_output_dir` | function | Temporary output |
| `sample_dict` | function | Sample dictionary |
| `sample_dataframe` | function | Sample DataFrame |
| `sample_time_series` | function | Time series data |
| `temp_config` | function | Temp YAML config |
| `temp_csv` | function | Temp CSV file |

## Marker Reference

| Marker | Purpose | Example |
|--------|---------|---------|
| `@pytest.mark.unit` | Unit tests | Fast, isolated |
| `@pytest.mark.integration` | Integration tests | External resources |
| `@pytest.mark.slow` | Slow tests | > 1 second |
| `@pytest.mark.skip` | Skip test | Not ready |
| `@pytest.mark.xfail` | Expected failure | Known bug |
| `@pytest.mark.parametrize` | Multiple inputs | Test matrix |

## Best Practices

1. **Use markers consistently** - All tests should have at least one marker
2. **Minimize fixture scope** - Use function scope unless sharing is needed
3. **Keep fixtures focused** - One purpose per fixture
4. **Document fixtures** - Add docstrings explaining usage
5. **Use tmp_path** - For temporary files (auto-cleaned)

## Error Handling

### Tests Not Discovered
```
Error: No tests collected

Check:
1. Test files match pattern: test_*.py
2. Test functions start with: test_
3. pytest.ini testpaths is correct
```

### Coverage Below Threshold
```
FAIL Required test coverage of 80% not reached. Total coverage: 75.00%

Options:
1. Add more tests
2. Reduce threshold temporarily
3. Exclude non-critical paths
```

## Related Skills

- [python-project-template](../python-project-template/SKILL.md) - Full project setup
- [repo-readiness](../repo-readiness/SKILL.md) - Verify test configuration

## References

- [pytest Documentation](https://docs.pytest.org/)
- [pytest-cov Documentation](https://pytest-cov.readthedocs.io/)
- [Testing Framework Standards](../../../docs/modules/standards/TESTING_FRAMEWORK_STANDARDS.md)

---

## Version History

- **1.0.0** (2026-01-14): Initial release - standardized pytest configuration with fixtures, markers, and coverage
