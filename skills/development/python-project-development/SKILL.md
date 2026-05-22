---
name: python-project-development
description: Creates production-ready Python projects including CLI tools, packages, and distributable libraries. Use when building CLI tools with argparse/click, packaging for PyPI, setting up pyproject.toml, or creating entry points. Triggers include "CLI tool", "Python package", "pyproject.toml", "publish to PyPI", "entry points", or "build wheel".
compatibility: Designed for Claude Code
allowed-tools: Read Grep Glob Bash mcp__context7__resolve-library-id mcp__context7__get-library-docs
user-invocable: false
---

# Python Project Development

Comprehensive guide for building production-ready Python CLI tools and distributable packages.

## When to Use This Skill

- Building command-line tools with argparse or click
- Creating Python libraries for distribution
- Publishing packages to PyPI
- Setting up modern pyproject.toml configuration
- Creating installable packages with dependencies
- Building wheels and source distributions

## Quick Start: CLI Tool

```python
#!/usr/bin/env python3
"""Brief description of what this script does."""
import sys
from pathlib import Path
from dataclasses import dataclass
from typing import Final

@dataclass(frozen=True, slots=True)
class Config:
  """Immutable configuration."""
  input_dir: Path
  max_size: int = 1000
  verbose: bool = False

def main() -> int:
  """Entry point. Returns exit code."""
  try:
    # Parse args, validate input, process
    return 0
  except ValueError as e:
    print(f"Error: {e}", file=sys.stderr)
    return 1

if __name__ == "__main__":
  sys.exit(main())
```

## Quick Start: Package Structure

```
my-package/
├── pyproject.toml
├── README.md
├── LICENSE
├── src/
│   └── my_package/
│       ├── __init__.py
│       ├── cli.py
│       └── core.py
└── tests/
    └── test_core.py
```

## Minimal pyproject.toml

```toml
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "my-package"
version = "0.1.0"
description = "A short description"
authors = [{name = "Your Name", email = "you@example.com"}]
readme = "README.md"
requires-python = ">=3.8"
dependencies = ["click>=8.0"]

[project.optional-dependencies]
dev = ["pytest>=7.0", "ruff>=0.1"]

[project.scripts]
my-cli = "my_package.cli:main"

[tool.setuptools.packages.find]
where = ["src"]
```

## CLI Standards

- **Types**: All functions typed (`-> ReturnType`), `dataclass(slots=True)` for data
- **Performance**: O(n) algorithms, frozenset for lookups, generators for large data
- **Stdlib-first**: Zero external deps unless justified
- **Exit codes**: 0=success, 1=error, 2+=specific failures
- **Error handling**: Catch specific exceptions, fail fast, clear messages

## CLI with Click

```python
# src/my_package/cli.py
import click

@click.group()
@click.version_option()
def cli():
    """My awesome CLI tool."""
    pass

@cli.command()
@click.argument("name")
@click.option("--greeting", default="Hello", help="Greeting to use")
def greet(name: str, greeting: str):
    """Greet someone."""
    click.echo(f"{greeting}, {name}!")

def main():
    cli()

if __name__ == "__main__":
    main()
```

## CLI with argparse

```python
import argparse
import sys

def main():
    parser = argparse.ArgumentParser(description="My tool", prog="my-tool")
    parser.add_argument("--version", action="version", version="%(prog)s 1.0.0")

    subparsers = parser.add_subparsers(dest="command", help="Commands")

    process_parser = subparsers.add_parser("process", help="Process data")
    process_parser.add_argument("input_file", help="Input file")
    process_parser.add_argument("-o", "--output", default="output.txt")

    args = parser.parse_args()

    if args.command == "process":
        return process_data(args.input_file, args.output)

    parser.print_help()
    return 1

if __name__ == "__main__":
    sys.exit(main())
```

## Full pyproject.toml Template

```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "my-package"
version = "1.0.0"
description = "Package description"
readme = "README.md"
requires-python = ">=3.8"
license = {text = "MIT"}
authors = [{name = "Name", email = "email@example.com"}]
keywords = ["example", "package"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
]
dependencies = [
    "click>=8.0.0",
    "pydantic>=2.0.0",
]

[project.optional-dependencies]
dev = ["pytest>=7.0", "ruff>=0.1", "mypy>=1.0"]

[project.urls]
Homepage = "https://github.com/user/my-package"
Documentation = "https://my-package.readthedocs.io"
Repository = "https://github.com/user/my-package"

[project.scripts]
my-cli = "my_package.cli:main"

[tool.setuptools]
package-dir = {"" = "src"}

[tool.setuptools.packages.find]
where = ["src"]

[tool.setuptools.package-data]
my_package = ["py.typed", "data/*.json"]

[tool.ruff]
line-length = 100
target-version = "py38"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W", "UP"]

[tool.mypy]
python_version = "3.8"
warn_return_any = true
disallow_untyped_defs = true

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-v --cov=my_package"
```

## Building and Publishing

```bash
# Install build tools
uv pip install build twine

# Build distribution
python -m build

# Check distribution
twine check dist/*

# Test on TestPyPI first
twine upload --repository testpypi dist/*

# Publish to PyPI
twine upload dist/*
```

## Editable Install for Development

```bash
# Install in development mode
uv pip install -e .

# With optional dependencies
uv pip install -e ".[dev]"
```

## Dynamic Versioning

```toml
[build-system]
requires = ["setuptools>=61.0", "setuptools-scm>=8.0"]
build-backend = "setuptools.build_meta"

[project]
name = "my-package"
dynamic = ["version"]

[tool.setuptools_scm]
write_to = "src/my_package/_version.py"
```

## Including Data Files

```toml
[tool.setuptools.package-data]
my_package = ["data/*.json", "templates/*.html", "py.typed"]
```

```python
# Accessing data files
from importlib.resources import files

data = files("my_package").joinpath("data/config.json").read_text()
```

## Security Checklist

- [ ] No hardcoded secrets/paths
- [ ] Validate all user input (paths, patterns)
- [ ] Use `Path.resolve()` to prevent traversal
- [ ] Catch `PermissionError`, `FileNotFoundError`
- [ ] Timeout on subprocess calls
- [ ] No `eval()`, `exec()`, `__import__()`

## Publishing Checklist

- [ ] Code is tested (pytest passing)
- [ ] Documentation complete (README, docstrings)
- [ ] Version number updated
- [ ] CHANGELOG.md updated
- [ ] License file included
- [ ] pyproject.toml complete
- [ ] Package builds without errors
- [ ] Installation tested in clean environment
- [ ] Tested on TestPyPI first
- [ ] Git tag created for release

## Reusable Components

Use battle-tested components from `scripts/`:

- `cli_template.py` - Production CLI scaffold with argparse
- `log_component.py` - ANSI colored logging
- `subprocess_helpers.py` - Safe subprocess wrappers with retry/timeout
- `common_utils.py` - has(), find_files(), safe file ops

See `references/patterns.md` for common CLI patterns and `references/stdlib_perf.md` for performance tips.

## Resources

- **Python Packaging Guide**: https://packaging.python.org/
- **PyPI**: https://pypi.org/
- **setuptools**: https://setuptools.pypa.io/
- **Click**: https://click.palletsprojects.com/
