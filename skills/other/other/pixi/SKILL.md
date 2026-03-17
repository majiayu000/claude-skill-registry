---
name: pixi
description: Comprehensive package and environment management using pixi - a fast, modern, cross-platform package manager. Use when working with pixi projects for (1) Project initialization and configuration, (2) Package management (adding, removing, updating conda/PyPI packages), (3) Environment management (creating, activating, managing multiple environments), (4) Feature management (defining and composing feature sets), (5) Task execution and management, (6) Global tool installation, (7) Dependency resolution and lock file management, or any other pixi-related operations. Supports Python, C++, R, Rust, Node.js and other languages via conda-forge ecosystem.
---

# Pixi Package Manager

## Overview

Pixi is a fast, modern package manager built on Rattler (Rust-based conda implementation) that provides reproducible, cross-platform environments. It combines conda and PyPI ecosystems, supports multiple languages, and includes built-in task management.

## Quick Start

### Check Installation

Before working with pixi, verify it's installed:

```bash
bash scripts/check_pixi.sh
```

If not installed, follow the installation instructions provided by the script.

### Common Workflows

**Initialize new project:**
```bash
pixi init my-project
cd my-project
pixi add python numpy pandas
```

**Add packages:**
```bash
pixi add <package>              # Conda package
pixi add --pypi <package>        # PyPI package
pixi add --feature dev pytest    # Add to specific feature
```

**Run commands:**
```bash
pixi run <task>                  # Run defined task
pixi exec <command>              # Execute command in environment
pixi shell                       # Activate environment shell
```

**Manage environments:**
```bash
pixi shell --environment <name>  # Activate specific environment
pixi run -e <name> <task>        # Run task in environment
```

## Core Capabilities

### 1. Project Initialization

Initialize new pixi projects with automatic manifest creation:

```bash
# Standard pixi.toml format
pixi init my-project

# Use pyproject.toml format
pixi init --format pyproject my-project
```

The manifest file (`pixi.toml` or `pyproject.toml`) defines:
- Project metadata (name, version, description)
- Dependencies (conda and PyPI packages)
- Tasks (commands to run)
- Features (optional dependency sets)
- Environments (combinations of features)
- Channels (package sources)
- Platforms (target operating systems)

### 2. Package Management

Add, remove, and manage packages from conda-forge and PyPI:

```bash
# Add packages
pixi add numpy pandas matplotlib
pixi add "python>=3.11,<3.12"
pixi add --pypi requests flask

# Add to specific feature
pixi add --feature dev pytest black ruff

# Remove packages
pixi remove numpy
pixi remove --feature dev pytest

# Update packages
pixi update                      # Update all
pixi update numpy                # Update specific package
pixi upgrade                     # Upgrade in manifest
```

**Package types:**
- Regular dependencies: Runtime requirements
- `--pypi`: PyPI packages (via uv integration)
- `--host`: Host dependencies (available at runtime)
- `--build`: Build dependencies (only during build)

### 3. Environment Management

Pixi supports multiple isolated environments within a single project. Each environment is a combination of features.

**Key concepts:**
- **Default feature**: Always included automatically in every environment
- **Custom features**: Named sets of dependencies, tasks, and configurations
- **Environments**: Combinations of features for different purposes

**Example configuration:**
```toml
[dependencies]
python = "3.11.*"
numpy = "*"

[feature.test.dependencies]
pytest = "*"
pytest-cov = "*"

[feature.dev.dependencies]
black = "*"
ruff = "*"

[environments]
test = ["test"]                  # Includes: default + test
dev = ["dev", "test"]            # Includes: default + dev + test
```

**Working with environments:**
```bash
# Activate environment
pixi shell --environment test

# Run task in environment
pixi run --environment test pytest

# Install specific environment
pixi install --environment dev

# List packages in environment
pixi list --environment test
```

For detailed environment and feature patterns, see [references/features-guide.md](references/features-guide.md).

### 4. Feature Management

Features are building blocks that define sets of packages and configurations. They enable:
- Separating development from production dependencies
- Supporting multiple Python versions
- Creating platform-specific configurations
- Managing hardware-specific dependencies (CUDA vs CPU)

**Common patterns:**

**Development features:**
```toml
[feature.dev.dependencies]
pytest = "*"
black = "*"
ruff = "*"
mypy = "*"

[feature.dev.tasks]
test = "pytest tests/"
format = "black ."
lint = "ruff check ."
```

**Python version features:**
```toml
[feature.py310.dependencies]
python = "3.10.*"

[feature.py311.dependencies]
python = "3.11.*"

[environments]
py310 = ["py310"]
py311 = ["py311"]
```

**Hardware features:**
```toml
[feature.cuda.dependencies]
pytorch-cuda = { version = "*", channel = "pytorch" }

[feature.cpu.dependencies]
pytorch-cpu = { version = "*", channel = "pytorch" }

[environments]
cuda = ["cuda"]
cpu = ["cpu"]
```

For comprehensive feature patterns and best practices, see [references/features-guide.md](references/features-guide.md).

### 5. Task Management

Define and run tasks within the pixi environment:

```bash
# Add tasks
pixi task add test "pytest tests/"
pixi task add format "black ."
pixi task add lint "ruff check ."

# Run tasks
pixi run test
pixi run format

# List tasks
pixi task list
```

**Task configuration in manifest:**
```toml
[tasks]
start = "python app.py"
test = "pytest tests/"
format = "black ."

# Task with dependencies
build = { cmd = "python setup.py build", depends-on = ["install"] }

# Feature-specific tasks
[feature.dev.tasks]
dev = "python app.py --reload"
```

### 6. Command Execution

Execute commands within the pixi environment:

```bash
# Run command in activated environment
pixi exec python script.py
pixi exec pytest tests/

# Temporary package installation and execution
pixi exec --spec ruff ruff check .
pixi exec --spec black black .

# Run in specific environment
pixi exec --environment test pytest
```

### 7. Global Tool Management

Install CLI tools system-wide, safely isolated:

```bash
# Install global tools
pixi global install gh ripgrep fd-find bat
pixi global install ruff black mypy

# List global tools
pixi global list

# Upgrade tools
pixi global upgrade ruff
pixi global upgrade-all

# Remove tools
pixi global remove bat
```

### 8. Project Information

Get information about the current project:

```bash
# Show project info
pixi info

# Detailed information
pixi info --extended

# JSON output
pixi info --json

# Use helper script
python scripts/pixi_info.py
```

### 9. Lock File Management

Pixi maintains a `pixi.lock` file for reproducible environments:

```bash
# Update lock file without installing
pixi lock

# Update lock for specific environment
pixi lock --environment test

# Install from lock file
pixi install --frozen
```

### 10. Maintenance

Clean up and maintain pixi projects:

```bash
# Remove environment directory
pixi clean

# Clean package cache
pixi clean cache

# Reinstall environment from scratch
pixi reinstall
```

## Reference Documentation

For detailed information, consult these references:

- **[cli-reference.md](references/cli-reference.md)** - Complete CLI command reference with all options and flags
- **[features-guide.md](references/features-guide.md)** - Comprehensive guide to features and multi-environment setup
- **[examples.md](references/examples.md)** - Real-world usage examples and common scenarios

## Workflow Decision Guide

**Starting a new project?**
→ Use `pixi init` and add dependencies with `pixi add`

**Adding packages?**
→ Use `pixi add` for conda packages, `pixi add --pypi` for PyPI packages
→ Use `--feature` flag to add to specific features

**Need multiple environments?**
→ Define features in manifest, compose them into environments
→ See [references/features-guide.md](references/features-guide.md) for patterns

**Running commands?**
→ Use `pixi run` for defined tasks
→ Use `pixi exec` for ad-hoc commands
→ Use `pixi shell` to activate environment interactively

**Managing dependencies?**
→ Use `pixi update` to update to newer compatible versions
→ Use `pixi upgrade` to upgrade and modify manifest
→ Use `pixi lock` to update lock file without installing

**Need global tools?**
→ Use `pixi global install` for system-wide CLI tools

**Troubleshooting?**
→ Run `pixi info` to check project status
→ Run `python scripts/pixi_info.py` for detailed information
→ Check [references/examples.md](references/examples.md) for common solutions

## Best Practices

1. **Use features for optional dependencies** - Keep default feature minimal with only production dependencies
2. **Leverage solve groups** - Ensure consistent versions across related environments
3. **Define tasks in manifest** - Make common operations easily repeatable
4. **Use semantic versioning** - Specify version constraints appropriately
5. **Commit lock file** - Ensure reproducible environments across team
6. **Use global install for tools** - Keep project dependencies clean
7. **Document environment purposes** - Add comments explaining each environment's use case

## Common Scenarios

### Data Science Project
```bash
pixi init data-project
pixi add python numpy pandas matplotlib jupyter scikit-learn
pixi add --feature dev pytest black
pixi task add notebook "jupyter lab"
pixi run notebook
```

### Web Application
```bash
pixi init web-app
pixi add python
pixi add --pypi fastapi uvicorn sqlalchemy
pixi add --feature dev --pypi pytest httpx
pixi task add dev "uvicorn app:app --reload"
pixi run dev
```

### Multi-Python Testing
```toml
[feature.py310.dependencies]
python = "3.10.*"

[feature.py311.dependencies]
python = "3.11.*"

[environments]
py310 = ["py310"]
py311 = ["py311"]
```

```bash
pixi run -e py310 pytest
pixi run -e py311 pytest
```

For more scenarios, see [references/examples.md](references/examples.md).

## Resources

### Scripts
- `scripts/check_pixi.sh` - Verify pixi installation
- `scripts/pixi_info.py` - Get detailed project information

### References
- `references/cli-reference.md` - Complete CLI command reference
- `references/features-guide.md` - Features and multi-environment guide
- `references/examples.md` - Usage examples and common scenarios

### Assets
- `assets/pixi.toml.template` - Basic project template

## External Resources

- Official documentation: https://pixi.prefix.dev/latest/
- GitHub repository: https://github.com/prefix-dev/pixi
- Conda-forge packages: https://conda-forge.org/
