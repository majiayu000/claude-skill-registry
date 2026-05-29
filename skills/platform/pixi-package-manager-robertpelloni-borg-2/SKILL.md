---
name: pixi-package-manager
description: Manage scientific Python dependencies and environments using pixi package manager with unified conda-forge and PyPI support. Use when setting up project environments, managing dependencies, creating reproducible workflows, or working with complex scientific packages requiring compiled libraries. Ideal for multi-environment projects, cross-platform development, and replacing conda/mamba workflows.
---

# Pixi Package Manager for Scientific Python

Master **pixi**, the modern package manager that unifies conda and PyPI ecosystems for fast, reproducible scientific Python development. Learn how to manage complex scientific dependencies, create isolated environments, and build reproducible workflows using `pyproject.toml` integration.

**Official Documentation**: https://pixi.sh
**GitHub**: https://github.com/prefix-dev/pixi

## Quick Reference Card

### Installation & Setup
```bash
# Install pixi (macOS/Linux)
curl -fsSL https://pixi.sh/install.sh | bash

# Install pixi (Windows)
iwr -useb https://pixi.sh/install.ps1 | iex

# Initialize new project with pyproject.toml
pixi init --format pyproject

# Initialize existing Python project
pixi init --format pyproject --import-environment
```

### Essential Commands
```bash
# Add dependencies
pixi add numpy scipy pandas              # conda packages
pixi add --pypi pytest-cov               # PyPI-only packages
pixi add --feature dev pytest ruff       # dev environment

# Install all dependencies
pixi install

# Run commands in environment
pixi run python script.py
pixi run pytest

# Shell with environment activated
pixi shell

# Add tasks
pixi task add test "pytest tests/"
pixi task add docs "sphinx-build docs/ docs/_build"

# Run tasks
pixi run test
pixi run docs

# Update dependencies
pixi update numpy                         # update specific
pixi update                              # update all

# List packages
pixi list
pixi tree numpy                          # show dependency tree
```

### Quick Decision Tree: Pixi vs UV vs Both

```
Need compiled scientific libraries (NumPy, SciPy, GDAL)?
├─ YES → Use pixi (conda-forge has pre-built binaries)
└─ NO → Consider uv for pure Python projects

Need multi-language support (Python + R, Julia, C++)?
├─ YES → Use pixi (supports conda ecosystem)
└─ NO → uv sufficient for Python-only

Need multiple environments (dev, test, prod, GPU, CPU)?
├─ YES → Use pixi features for environment management
└─ NO → Single environment projects work with either

Need reproducible environments across platforms?
├─ CRITICAL → Use pixi (lockfiles include all platforms)
└─ LESS CRITICAL → uv also provides lockfiles

Want to use both conda-forge AND PyPI packages?
├─ YES → Use pixi (seamless integration)
└─ ONLY PYPI → uv is simpler and faster

Legacy conda environment files (environment.yml)?
├─ YES → pixi can import and modernize
└─ NO → Start fresh with pixi or uv
```

## When to Use This Skill

- **Setting up scientific Python projects** with complex compiled dependencies (NumPy, SciPy, Pandas, scikit-learn, GDAL, netCDF4)
- **Building reproducible research environments** that work identically across different machines and platforms
- **Managing multi-language projects** that combine Python with R, Julia, C++, or Fortran
- **Creating multiple environment configurations** for different hardware (GPU/CPU), testing scenarios, or deployment targets
- **Replacing conda/mamba workflows** with faster, more reliable dependency resolution
- **Developing packages that depend on both conda-forge and PyPI** packages
- **Migrating from environment.yml or requirements.txt** to modern, reproducible workflows
- **Running automated scientific workflows** with task runners and CI/CD integration
- **Working with geospatial, climate, or astronomy packages** that require complex C/Fortran dependencies

## Core Concepts

### 1. Unified Package Management (conda + PyPI)

Pixi resolves dependencies from **both conda-forge and PyPI** in a single unified graph, ensuring compatibility:

```toml
[project]
name = "my-science-project"
dependencies = [
    "numpy>=1.24",      # from conda-forge (optimized builds)
    "pandas>=2.0",      # from conda-forge
]

[tool.pixi.pypi-dependencies]
my-custom-pkg = ">=1.0"        # PyPI-only package
```

**Why this matters for scientific Python:**
- Get optimized NumPy/SciPy builds from conda-forge (MKL, OpenBLAS)
- Use PyPI packages not available in conda
- Single lockfile ensures all dependencies are compatible

### 2. Multi-Platform Lockfiles

Pixi generates `pixi.lock` with dependency specifications for **all platforms** (Linux, macOS, Windows, different architectures):

```toml
# pixi.lock includes:
# - linux-64
# - osx-64, osx-arm64
# - win-64
```

**Benefits:**
- Commit lockfile to git → everyone gets identical environments
- Works on collaborator's different OS without changes
- CI/CD uses exact same versions as local development

### 3. Feature-Based Environments

Create multiple environments using **features** without duplicating dependencies:

```toml
[tool.pixi.feature.test.dependencies]
pytest = ">=7.0"
pytest-cov = ">=4.0"

[tool.pixi.feature.gpu.dependencies]
pytorch-cuda = "11.8.*"

[tool.pixi.environments]
test = ["test"]
gpu = ["gpu"]
gpu-test = ["gpu", "test"]  # combines features
```

### 4. Task Automation

Define reusable commands as tasks:

```toml
[tool.pixi.tasks]
test = "pytest tests/ -v"
format = "ruff format src/ tests/"
lint = "ruff check src/ tests/"
docs = "sphinx-build docs/ docs/_build"
analyse = { cmd = "python scripts/analyze.py", depends-on = ["test"] }
```

### 5. Fast Dependency Resolution

Pixi uses **rattler** (Rust-based conda resolver) for 10-100x faster resolution than conda:

- Parallel package downloads
- Efficient caching
- Smart dependency solver

### 6. pyproject.toml Integration

Pixi reads standard Python project metadata from `pyproject.toml`, enabling:
- Single source of truth for project configuration
- Compatibility with pip, uv, and other tools
- Standard Python packaging workflows

## Quick Start

### Minimal Example: Data Analysis Project

```bash
# Create new project
mkdir climate-analysis && cd climate-analysis
pixi init --format pyproject

# Add scientific stack
pixi add python=3.11 numpy pandas matplotlib xarray

# Add development tools
pixi add --feature dev pytest ipython ruff

# Create analysis script
cat > analyze.py << 'EOF'
import pandas as pd
import matplotlib.pyplot as plt

# Your analysis code
data = pd.read_csv("data.csv")
data.plot()
plt.savefig("output.png")
EOF

# Run in pixi environment
pixi run python analyze.py

# Or activate shell
pixi shell
python analyze.py
```

## Patterns

See [references/PATTERNS.md](references/PATTERNS.md) for detailed patterns including:
- Converting existing projects to Pixi
- Multi-environment scientific workflows
- Scientific library development
- Conda + PyPI dependency strategy
- Reproducible research environments
- Task dependencies and workflows

## File Templates

Ready-to-use templates are available in the `assets/` directory:

- **[assets/pyproject-pixi-example.toml](assets/pyproject-pixi-example.toml)** - Basic pixi project configuration
- **[assets/pyproject-multi-env.toml](assets/pyproject-multi-env.toml)** - Multi-environment configuration example
- **[assets/github-actions-pixi.yml](assets/github-actions-pixi.yml)** - GitHub Actions workflow for pixi

## Common Issues and Solutions

See [references/COMMON_ISSUES.md](references/COMMON_ISSUES.md) for solutions to:
- Package not found in conda-forge
- Conflicting dependencies
- Slow environment creation
- Platform-specific failures
- PyPI package installation fails
- Lockfile merge conflicts
- Editable install of local package

## Best Practices Checklist

### Project Setup
- [ ] Use `pixi init --format pyproject` for new projects
- [ ] Set explicit Python version constraint (`python>=3.11,<3.13`)
- [ ] Organize dependencies by source (conda vs PyPI)
- [ ] Create separate features for dev, test, docs environments
- [ ] Define useful tasks for common workflows
- [ ] Set up `.gitignore` to exclude `.pixi/` directory

### Dependency Management
- [ ] Prefer conda-forge for compiled scientific packages (NumPy, SciPy, GDAL)
- [ ] Use PyPI only for pure Python or conda-unavailable packages
- [ ] Pin exact versions for reproducible research
- [ ] Use version ranges for libraries (allow updates)
- [ ] Specify solve groups for independent environment solving
- [ ] Use `pixi update` regularly to get security patches

### Reproducibility
- [ ] Commit `pixi.lock` to version control
- [ ] Include all platforms in lockfile for cross-platform teams
- [ ] Document environment recreation steps in README
- [ ] Use exact version pins for published research
- [ ] Test environment from scratch periodically
- [ ] Archive environments for long-term preservation

### Performance
- [ ] Use pixi's parallel downloads (automatic)
- [ ] Leverage caching in CI/CD (`prefix-dev/setup-pixi` action)
- [ ] Keep environments minimal (only necessary dependencies)
- [ ] Use solve groups to isolate independent environments
- [ ] Clean old packages with `pixi clean cache`

### Development Workflow
- [ ] Define tasks for common operations (test, lint, format)
- [ ] Use task dependencies for complex workflows
- [ ] Create environment-specific tasks when needed
- [ ] Use `pixi shell` for interactive development
- [ ] Use `pixi run` for automated scripts and CI
- [ ] Test in clean environment before releasing

## Resources

### Official Documentation
- **Pixi Website**: https://pixi.sh
- **Documentation**: https://pixi.sh/latest/
- **GitHub Repository**: https://github.com/prefix-dev/pixi
- **Configuration Reference**: https://pixi.sh/latest/reference/project_configuration/

### Community & Support
- **Discord**: https://discord.gg/kKV8ZxyzY4
- **GitHub Discussions**: https://github.com/prefix-dev/pixi/discussions
- **Issue Tracker**: https://github.com/prefix-dev/pixi/issues

### Related Technologies
- **Conda-forge**: https://conda-forge.org/
- **Rattler**: https://github.com/mamba-org/rattler (underlying solver)
- **PyPI**: https://pypi.org/
- **UV Package Manager**: https://github.com/astral-sh/uv

### Complementary Skills
- **scientific-python-packaging**: Modern Python packaging patterns
- **scientific-python-testing**: Testing strategies with pytest
- **uv-package-manager**: Fast pure-Python package management

## Summary

Pixi revolutionizes scientific Python development by unifying conda and PyPI ecosystems with blazing-fast dependency resolution, reproducible multi-platform lockfiles, and seamless environment management. By leveraging `pyproject.toml` integration, pixi provides a modern, standards-compliant approach to managing complex scientific dependencies while maintaining compatibility with the broader Python ecosystem.

**Key advantages for scientific computing:**

1. **Optimized Scientific Packages**: Access conda-forge's pre-built binaries for NumPy, SciPy, and other compiled packages with MKL/OpenBLAS optimizations
2. **Complex Dependencies Made Simple**: Handle challenging packages like GDAL, netCDF4, and HDF5 that require C/Fortran/C++ system libraries
3. **True Reproducibility**: Multi-platform lockfiles ensure identical environments across Linux, macOS, and Windows
4. **Flexible Environment Management**: Feature-based environments for dev/test/prod, GPU/CPU, or any custom configuration
5. **Fast and Reliable**: 10-100x faster than conda with Rust-based parallel dependency resolution
6. **Task Automation**: Built-in task runner for scientific workflows, testing, and documentation
7. **Best of Both Worlds**: Seamlessly mix conda-forge optimized packages with PyPI's vast ecosystem

Whether you're conducting reproducible research, developing scientific software, or managing complex data analysis pipelines, pixi provides the robust foundation for modern scientific Python development. By replacing conda/mamba with pixi, you gain speed, reliability, and modern workflows while maintaining full access to the scientific Python ecosystem.

**Ready to get started?** Install pixi, initialize your project with `pixi init --format pyproject`, and experience the future of scientific Python package management.
