---
name: python-project-template
description: Generate standardized Python project structure with pyproject.toml, UV environment, pytest configuration, and workspace-hub compliance. Creates production-ready project scaffolding.
version: 1.0.0
category: workspace-hub
type: skill
trigger: manual
auto_execute: false
capabilities:
  - project_scaffolding
  - pyproject_generation
  - dependency_configuration
  - testing_setup
  - uv_environment
tools:
  - Write
  - Bash
  - Read
related_skills:
  - pytest-fixture-generator
  - repo-readiness
  - agent-os-framework
---

# Python Project Template

> Generate standardized Python project structure compliant with workspace-hub standards.

## Quick Start

```bash
# Create new project
/python-project-template my-project

# Create with specific type
/python-project-template my-project --type library

# Create in specific directory
/python-project-template my-project --path /path/to/projects
```

## When to Use

**USE when:**
- Starting a new Python project
- Adding a new repository to workspace-hub
- Standardizing an existing project
- Creating reusable modules

**DON'T USE when:**
- Project already has proper structure
- Non-Python projects
- One-off scripts (use scripts/ directory instead)

## Prerequisites

- Python 3.9+
- UV package manager installed
- Git initialized in parent directory

## Overview

Creates a complete Python project with:

1. **pyproject.toml** - Modern Python packaging configuration
2. **UV environment** - Fast dependency management
3. **Test structure** - pytest with fixtures and coverage
4. **Source layout** - Modular src/ organization
5. **Documentation** - README, CLAUDE.md, .agent-os/
6. **Quality tools** - ruff, black, mypy configuration

## Project Structure Generated

```
my-project/
├── pyproject.toml          # Project configuration
├── README.md               # Project documentation
├── CLAUDE.md               # AI agent instructions
├── .gitignore              # Git ignore patterns
├── .python-version         # Python version
├── src/
│   └── my_project/
│       ├── __init__.py     # Package init
│       └── core.py         # Core module
├── tests/
│   ├── __init__.py
│   ├── conftest.py         # pytest fixtures
│   └── test_core.py        # Example test
├── config/
│   └── settings.yaml       # Configuration
├── scripts/
│   └── run.sh              # Execution script
├── docs/
│   └── README.md           # Documentation index
├── data/
│   ├── raw/                # Raw data
│   └── processed/          # Processed data
├── reports/                # Generated reports
└── .agent-os/
    └── product/
        ├── mission.md      # Project mission
        └── tech-stack.md   # Technology stack
```

## Core Templates

### 1. pyproject.toml

```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "{{project_name}}"
version = "0.1.0"
description = "{{description}}"
readme = "README.md"
license = {text = "MIT"}
requires-python = ">=3.9"
authors = [
    {name = "{{author}}", email = "{{email}}"}
]
keywords = ["{{keywords}}"]
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
]

dependencies = [
    "pandas>=2.0.0",
    "numpy>=1.24.0",
    "pyyaml>=6.0",
    "plotly>=5.15.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-cov>=4.1.0",
    "ruff>=0.1.0",
    "black>=23.0.0",
    "mypy>=1.5.0",
]

[tool.setuptools.packages.find]
where = ["src"]

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_functions = ["test_*"]
addopts = "-v --cov=src --cov-report=term-missing --cov-fail-under=80"
markers = [
    "unit: Unit tests",
    "integration: Integration tests",
    "slow: Slow tests",
]

[tool.ruff]
line-length = 100
target-version = "py39"
select = ["E", "F", "I", "N", "W", "UP"]

[tool.black]
line-length = 100
target-version = ["py39"]

[tool.mypy]
python_version = "3.9"
warn_return_any = true
warn_unused_configs = true
```

### 2. conftest.py

```python
"""
ABOUTME: Pytest configuration and fixtures for {{project_name}}
ABOUTME: Provides shared fixtures and test utilities
"""

import sys
from pathlib import Path

import pytest

# Add src to path for imports
src_path = Path(__file__).parent.parent / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))


@pytest.fixture
def sample_data():
    """Provide sample test data."""
    return {
        "name": "test",
        "value": 42,
        "items": [1, 2, 3],
    }


@pytest.fixture
def temp_config(tmp_path):
    """Create temporary configuration file."""
    config_file = tmp_path / "config.yaml"
    config_file.write_text("""
settings:
  debug: true
  output_dir: ./output
""")
    return config_file


@pytest.fixture(scope="session")
def project_root():
    """Return project root directory."""
    return Path(__file__).parent.parent
```

### 3. CLAUDE.md Template

```markdown
# Claude Code - {{project_name}}

> AI agent instructions for {{project_name}}

## Project Overview

{{description}}

## Critical Rules

1. **TDD Mandatory**: Write tests before implementation
2. **UV Environment**: Always use UV for dependency management
3. **File Organization**: Follow workspace-hub standards

## File Organization

**NEVER save to root. Use:**
- `/src` - Source code
- `/tests` - Test files
- `/docs` - Documentation
- `/config` - Configuration
- `/scripts` - Utility scripts
- `/data` - Data files
- `/reports` - Generated reports

## Key Commands

```bash
# Setup environment
uv venv && source .venv/bin/activate
uv pip install -e ".[dev]"

# Run tests
pytest

# Format code
black src tests
ruff check src tests --fix

# Type check
mypy src
```

## Documentation References

- @README.md - Project overview
- @.agent-os/product/mission.md - Project mission
- @docs/README.md - Documentation index
```

### 4. Core Module Template

```python
"""
ABOUTME: Core module for {{project_name}}
ABOUTME: Provides main functionality and utilities
"""

import logging
from pathlib import Path
from typing import Any, Dict, Optional

import yaml

logger = logging.getLogger(__name__)


def load_config(config_path: Path) -> Dict[str, Any]:
    """
    Load configuration from YAML file.

    Args:
        config_path: Path to configuration file

    Returns:
        Configuration dictionary

    Raises:
        FileNotFoundError: If config file doesn't exist
        yaml.YAMLError: If YAML parsing fails
    """
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with open(config_path) as f:
        config = yaml.safe_load(f)

    logger.info(f"Loaded configuration from {config_path}")
    return config


def process_data(data: Dict[str, Any], config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Process data according to configuration.

    Args:
        data: Input data dictionary
        config: Optional configuration

    Returns:
        Processed data dictionary
    """
    config = config or {}
    result = data.copy()

    # Add processing logic here
    logger.debug(f"Processing data with config: {config}")

    return result


class {{ProjectClass}}:
    """Main class for {{project_name}} functionality."""

    def __init__(self, config_path: Optional[Path] = None):
        """
        Initialize {{ProjectClass}}.

        Args:
            config_path: Optional path to configuration file
        """
        self.config = {}
        if config_path:
            self.config = load_config(config_path)

        self._setup_logging()

    def _setup_logging(self):
        """Configure logging for the class."""
        logging.basicConfig(
            level=self.config.get("log_level", "INFO"),
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )

    def run(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute main processing.

        Args:
            data: Input data

        Returns:
            Processed results
        """
        logger.info("Starting processing")
        result = process_data(data, self.config)
        logger.info("Processing complete")
        return result
```

## Usage Examples

### Example 1: Create Basic Project

```bash
# Invoke skill
/python-project-template my-analysis-tool

# Result: Complete project structure created
# - pyproject.toml configured
# - src/my_analysis_tool/ with core module
# - tests/ with conftest.py and example test
# - UV environment ready
```

### Example 2: Create Library Project

```bash
# Create library project
/python-project-template my-library --type library

# Additional features:
# - Package publishing configuration
# - Documentation with Sphinx
# - API reference structure
```

### Example 3: Create Data Pipeline Project

```bash
# Create data pipeline project
/python-project-template data-pipeline --type pipeline

# Additional features:
# - data/raw/ and data/processed/ directories
# - reports/ for output
# - scripts/ with execution templates
```

## Execution Checklist

**Project Creation:**
- [ ] Create directory structure
- [ ] Generate pyproject.toml
- [ ] Create src/ module structure
- [ ] Setup tests/ with conftest.py
- [ ] Generate CLAUDE.md
- [ ] Create .agent-os/ structure
- [ ] Initialize git repository
- [ ] Create UV environment
- [ ] Install dependencies
- [ ] Run initial tests

**Post-Creation:**
- [ ] Update project description
- [ ] Add project-specific dependencies
- [ ] Configure CI/CD (optional)
- [ ] Run repo-readiness check

## Error Handling

### Directory Exists
```
Error: Directory 'my-project' already exists

Options:
1. Use different name
2. Use --force to overwrite
3. Use --update to add missing files
```

### UV Not Installed
```
Error: UV package manager not found

Install UV:
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Best Practices

1. **Use descriptive project names** - kebab-case for directories, snake_case for Python
2. **Update dependencies** - Keep pyproject.toml current
3. **Run tests early** - Verify setup with `pytest` immediately
4. **Configure IDE** - Use generated configs for VS Code/PyCharm
5. **Document as you go** - Keep README.md updated

## Integration Points

### With repo-readiness
```bash
# After project creation
/repo-readiness

# Verifies:
# - CLAUDE.md present
# - .agent-os/ configured
# - Tests passing
# - Environment setup
```

### With agent-os-framework
```bash
# Enhance with full agent-os
/agent-os-framework my-project

# Adds:
# - Complete .agent-os/ structure
# - Mission and roadmap templates
# - Decision log
```

## Related Skills

- [pytest-fixture-generator](../pytest-fixture-generator/SKILL.md) - Enhanced testing
- [repo-readiness](../repo-readiness/SKILL.md) - Verify project setup
- [agent-os-framework](../agent-os-framework/SKILL.md) - Full product documentation

## References

- [Python Packaging Guide](https://packaging.python.org/)
- [UV Documentation](https://github.com/astral-sh/uv)
- [workspace-hub Standards](../../../docs/modules/standards/)

---

## Version History

- **1.0.0** (2026-01-14): Initial release - standardized Python project generation with pyproject.toml, UV support, pytest configuration, and workspace-hub compliance
