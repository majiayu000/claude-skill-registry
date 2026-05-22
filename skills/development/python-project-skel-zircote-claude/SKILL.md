---
name: python-project-skel
description: Generate production-ready Python project skeletons with Astral UV package manager, Hatchling build backend with dynamic versioning, and modern tooling (ruff, mypy, pytest, bandit). Use when creating new Python projects, initializing Python packages, setting up src-layout projects, scaffolding Python libraries, or starting a new Python application. Supports Python 3.14+ by default with configurable version. Output to current directory, specified path, or tarball.
---

# Python Project Skeleton Generator

Creates production-ready Python project structures following modern best practices.

## Quick Start

Generate a project in the current directory:
```
Project name: my-awesome-project
```

The skill prompts for required info and generates a complete project structure.

## Configuration Options

| Option | Default | Description |
|--------|---------|-------------|
| Project name | (required) | Kebab-case name (e.g., `my-project`) |
| Package name | (derived) | Snake_case from project name |
| Python version | 3.14 | Minimum Python version |
| License | MIT | License type |
| Author name | (optional) | For pyproject.toml |
| Author email | (optional) | For pyproject.toml |
| Description | (optional) | Project description |
| Output mode | cwd | `cwd`, `path`, or `tarball` |

## Generated Structure

```
{project-name}/
├── pyproject.toml          # Full config with all tools
├── README.md
├── LICENSE
├── Makefile                # UV-based dev targets
├── src/{package_name}/
│   ├── __init__.py         # With __version__ = "0.1.0"
│   ├── py.typed            # PEP 561 marker
│   └── main.py             # Entry point stub
└── tests/
    ├── __init__.py
    ├── conftest.py         # pytest fixtures
    └── test_main.py        # Example test
```

## Included Tool Configurations

**pyproject.toml sections:**
- `[build-system]` - Hatchling backend
- `[project]` - Dynamic version, classifiers, URLs
- `[project.optional-dependencies]` - dev group
- `[dependency-groups]` - UV compatibility
- `[tool.hatch.version]` - Points to `__init__.py`
- `[tool.ruff]` - Format + lint (E, W, F, I, B, C4, UP, ARG, SIM)
- `[tool.mypy]` - Strict configuration
- `[tool.pytest]` - Native TOML (pytest 9.0+)
- `[tool.coverage]` - 80% threshold
- `[tool.bandit]` - Security scanning

**Makefile targets:**
- `help` - Categorized target list
- `install`, `install-dev` - UV-based installation
- `test`, `test-cov`, `coverage` - Testing variants
- `lint`, `typecheck`, `security` - Quality tools
- `format`, `format-check` - Ruff formatting
- `quality` - All checks combined
- `build`, `clean` - Package building

## Output Modes

1. **cwd** (default) - Create project in current working directory
2. **path** - Create at specified absolute or relative path
3. **tarball** - Create `.tar.gz` archive (useful for distribution)

## Usage

Run the generator script:
```bash
python scripts/generate_project.py \
    --name my-project \
    --python-version 3.14 \
    --output-mode cwd
```

Or invoke interactively - the skill will prompt for required values.

## Post-Generation Steps

After generation:
```bash
cd {project-name}
uv sync                    # Install dependencies
make test                  # Run tests
make quality               # Run all quality checks
```

## Customization

The generated project is a starting point. Common modifications:
- Add dependencies to `[project.dependencies]`
- Adjust tool configs in pyproject.toml
- Add additional test files
- Extend Makefile with project-specific targets
