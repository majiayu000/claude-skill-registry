---
name: python-package-builder
description: "Build and publish professional Python packages to PyPI. Use when creating pip-installable packages, converting scripts to packages, setting up pyproject.toml/setup.py, adding CLI interfaces, writing tests, or preparing for PyPI upload. Covers bioinformatics tool packaging."
license: Proprietary
---

# Python Package Development for PyPI

## Project Structure

```
package-name/
├── src/
│   └── package_name/
│       ├── __init__.py
│       ├── core.py
│       ├── cli.py
│       └── utils.py
├── tests/
│   ├── __init__.py
│   ├── test_core.py
│   └── conftest.py
├── docs/
│   └── README.md
├── pyproject.toml
├── README.md
├── LICENSE
├── CHANGELOG.md
└── .gitignore
```

## pyproject.toml (Modern Standard)

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "package-name"
version = "0.1.0"
description = "Brief description of the package"
readme = "README.md"
license = {text = "MIT"}
requires-python = ">=3.9"
authors = [
    {name = "MD BABU MIA", email = "md.babu.mia@mssm.edu"}
]
keywords = ["bioinformatics", "single-cell", "genomics"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Science/Research",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Topic :: Scientific/Engineering :: Bio-Informatics",
]
dependencies = [
    "pandas>=1.5.0",
    "numpy>=1.21.0",
    "requests>=2.28.0",
]

[project.optional-dependencies]
dev = ["pytest>=7.0", "pytest-cov", "black", "mypy", "ruff"]
docs = ["sphinx", "sphinx-rtd-theme"]

[project.scripts]
package-name = "package_name.cli:main"

[project.urls]
Homepage = "https://github.com/mdbabumiamssm/package-name"
Documentation = "https://package-name.readthedocs.io"
Repository = "https://github.com/mdbabumiamssm/package-name"

[tool.hatch.build.targets.wheel]
packages = ["src/package_name"]

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]

[tool.black]
line-length = 88
target-version = ['py39', 'py310', 'py311']

[tool.ruff]
line-length = 88
select = ["E", "F", "I", "UP"]
```

## Package __init__.py

```python
"""Package description."""

__version__ = "0.1.0"
__author__ = "MD BABU MIA"
__email__ = "md.babu.mia@mssm.edu"

from .core import MainClass, main_function
from .utils import helper_function

__all__ = ["MainClass", "main_function", "helper_function"]
```

## CLI with Click

```python
# cli.py
import click
from .core import run_analysis

@click.group()
@click.version_option()
def main():
    """Package description for CLI."""
    pass

@main.command()
@click.option('--input', '-i', required=True, help='Input file path')
@click.option('--output', '-o', default='output/', help='Output directory')
@click.option('--threads', '-t', default=4, type=int, help='Number of threads')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
def analyze(input, output, threads, verbose):
    """Run the analysis pipeline."""
    click.echo(f"Processing: {input}")
    result = run_analysis(input, output, threads, verbose)
    click.echo(f"Complete! Output: {result}")

if __name__ == "__main__":
    main()
```

## Environment Variable Configuration

```python
# config.py
import os
from dataclasses import dataclass
from typing import Optional

@dataclass
class Config:
    """Configuration from environment variables."""
    email: Optional[str] = None
    api_key: Optional[str] = None
    output_dir: str = "./output"
    
    def __post_init__(self):
        self.email = self.email or os.getenv("NCBI_EMAIL")
        self.api_key = self.api_key or os.getenv("NCBI_API_KEY")
        
    def validate(self):
        if not self.email:
            raise ValueError("Email required. Set NCBI_EMAIL or pass email=")
```

## Testing with pytest

```python
# tests/test_core.py
import pytest
from package_name import MainClass, main_function

class TestMainClass:
    def test_initialization(self):
        obj = MainClass(param="test")
        assert obj.param == "test"
    
    def test_method(self):
        obj = MainClass(param="test")
        result = obj.process()
        assert result is not None

@pytest.fixture
def sample_data():
    return {"key": "value", "count": 10}

def test_main_function(sample_data):
    result = main_function(sample_data)
    assert "processed" in result
```

## Build and Publish

```bash
# Install build tools
pip install build twine

# Build package
python -m build

# Check distribution
twine check dist/*

# Upload to TestPyPI first
twine upload --repository testpypi dist/*

# Upload to PyPI
twine upload dist/*
```

## GitHub Actions CI/CD

```yaml
# .github/workflows/publish.yml
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install build twine
      - name: Build
        run: python -m build
      - name: Publish
        env:
          TWINE_USERNAME: __token__
          TWINE_PASSWORD: ${{ secrets.PYPI_TOKEN }}
        run: twine upload dist/*
```

See `references/bioinformatics_packaging.md` for domain-specific patterns.
