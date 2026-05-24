---
name: uv-dependency-management
description: |
  Manage Python project dependencies with uv. Learn how to add, remove, and update
  dependencies, organize them into groups (dev, test, lint, docs), pin versions,
  handle conflicts, and manage lock files for reproducible installations across environments.
  Use when adding or updating packages, organizing development dependencies, resolving
  version conflicts, or managing lock files in CI/CD pipelines.
allowed-tools: Bash, Read, Write, Edit
---

# uv Dependency Management

## Purpose

Master dependency management with uv, including adding/removing packages, version
constraints, dependency groups for development and production, lock files, and
resolving version conflicts.

## Quick Start

Add a dependency and see it in your lock file:

```bash
# Add a package with version constraint
uv add "requests>=2.31.0"

# View your dependency tree
uv tree

# Update all dependencies to latest compatible versions
uv lock --upgrade
```

Your `pyproject.toml` is automatically updated, and `uv.lock` ensures reproducible installs.

## Instructions

### Step 1: Understand Dependency Scopes

uv manages three types of dependencies:

**Main Dependencies** (project requirements)
```toml
[project]
dependencies = [
    "fastapi>=0.104.0",
    "sqlalchemy>=2.0.0",
]
```

**Optional Dependencies** (extras for features)
```toml
[project.optional-dependencies]
database = ["psycopg2-binary>=2.9.0"]
aws = ["boto3>=1.34.0"]
```

**Development Groups** (dev-only tools)
```toml
[dependency-groups]
dev = ["pytest>=8.0.0", "black>=23.0.0"]
test = ["pytest-cov>=4.1.0"]
lint = ["ruff>=0.1.0", "mypy>=1.7.0"]
```

### Step 2: Add Dependencies

**Add to main project:**
```bash
uv add requests httpx
uv add "fastapi>=0.104.0"
uv add "django>=4.2,<5.0"
```

**Add to specific group:**
```bash
uv add --dev pytest                    # Add to 'dev' group
uv add --group test pytest-cov        # Add to 'test' group
uv add --group lint ruff mypy         # Add to 'lint' group
```

**Add with extras:**
```bash
uv add "pandas[excel,plot]"
uv add --dev "pytest[cov]"
```

### Step 3: Use Version Constraints

**Common patterns (semantic versioning):**
```bash
uv add "requests"                   # Latest
uv add "requests>=2.31.0"          # Minimum version
uv add "requests>=2.31.0,<3.0.0"   # Range (major bump)
uv add "requests~=2.31.0"          # Compatible release (~= 2.31.x)
uv add "requests==2.31.0"          # Exact version (production)
```

**Recommended approach:**
- Development: `>=` (flexible, want latest)
- Production: `>=X,<Y` (range, tested with that version)
- Stable packages: `~=` (compatible releases)

### Step 4: Remove and Update Dependencies

**Remove a package:**
```bash
uv remove requests
uv remove pytest black              # Remove multiple
```

**Update to specific version:**
```bash
uv add "requests@2.32.0"
```

**Update all dependencies:**
```bash
uv sync --upgrade                   # Update and sync
uv lock --upgrade                   # Just update lock file
```

### Step 5: Organize with Dependency Groups

Define logical groupings in `pyproject.toml`:

```toml
[dependency-groups]
dev = [
    "pytest>=8.0.0",
    "pytest-cov>=4.1.0",
    "black>=23.0.0",
]
lint = [
    "ruff>=0.1.0",
    "mypy>=1.7.0",
    "pylint>=3.0.0",
]
docs = [
    "mkdocs>=1.5.0",
    "mkdocs-material>=9.0.0",
]
```

**Install specific groups:**
```bash
uv sync --group dev --group lint    # Install groups
uv sync --all-groups                # Install everything
uv sync --no-dev                    # Only main deps (production)
```

### Step 6: Understand Lock Files

**Lock file (`uv.lock`):**
- Records exact versions of all dependencies
- Ensures reproducible installs across machines
- Should be committed to version control
- Automatically updated when you change `pyproject.toml`

**Workflow:**
```bash
# After changing pyproject.toml
uv sync              # Installs from lock or creates new lock

# To explicitly update lock file
uv lock --upgrade    # Update all to latest compatible

# In CI/CD (use frozen to prevent surprises)
uv sync --frozen     # Fails if lock is out of sync
```

### Step 7: Handle Dependency Conflicts

**Problem:** Two packages need incompatible versions of same library

**Solution 1: Check if newer versions are compatible**
```bash
uv add "package-a"
uv add "package-b"   # Might fail with version conflict

# Try adding with different constraints
uv add "package-a>=1.0,<2.0"
uv add "package-b>=2.0,<3.0"
```

**Solution 2: Use separate dependency groups**
```toml
[dependency-groups]
ml-cpu = ["torch-cpu>=2.0"]
ml-gpu = ["torch-gpu>=2.0"]
```

```bash
# Install one group at a time
uv sync --group ml-cpu
```

**Solution 3: Investigate and pick winning version**
```bash
# See what's needed
uv add --dry-run "package-a" "package-b"

# One might need updating
uv add "package-a>=2.0"
uv add "package-b>=3.0"
```

## Examples

### Example 1: Web API Project Setup

```bash
# Initialize and add web dependencies
uv init my-api
cd my-api
uv add fastapi uvicorn sqlalchemy pydantic

# Add development tools
uv add --group dev pytest pytest-asyncio
uv add --group lint ruff mypy black

# Verify setup
uv tree
```

**Resulting pyproject.toml:**
```toml
[project]
name = "my-api"
version = "0.1.0"
dependencies = [
    "fastapi>=0.104.0",
    "uvicorn>=0.24.0",
    "sqlalchemy>=2.0.0",
    "pydantic>=2.5.0",
]

[dependency-groups]
dev = ["pytest>=8.0.0", "pytest-asyncio>=0.21.0"]
lint = ["ruff>=0.1.0", "mypy>=1.7.0", "black>=23.0.0"]
```

### Example 2: Library with Optional Features

```bash
# Create library with core deps
uv init my-library
uv add "click>=8.1.0"

# Add optional features as extras
uv add --group excel "openpyxl>=3.0.0"
uv add --group database "sqlalchemy>=2.0.0"
uv add --group async "aiohttp>=3.8.0"

# Setup development tools
uv add --dev pytest
```

### Example 3: Resolving Version Conflicts

```bash
# Trying to add packages with conflicting requirements
uv add package-a                    # Works fine
uv add package-b                    # Fails - needs different version of shared lib

# View what's going on
uv add --dry-run package-b

# Try different constraints
uv add "package-a>=1.0,<1.5"
uv add "package-b>=2.0,<2.5"

# Check if it works
uv tree
```

### Example 4: Data Science Project

```bash
# Create project
uv init data-pipeline
cd data-pipeline

# Data science core
uv add pandas numpy scikit-learn

# Analysis tools
uv add jupyter matplotlib seaborn plotly

# Development
uv add --group dev pytest pytest-cov

# Final tree
uv tree
```

### Example 5: Update Strategy for Production

```bash
# Initial setup with compatible ranges
uv add "requests>=2.31.0,<3.0.0"
uv add "fastapi>=0.104.0,<1.0.0"

# After testing on latest patch
uv add "requests@2.31.3"
uv add "fastapi@0.104.1"

# Lock file is frozen for production
git add uv.lock
git commit -m "Pin exact versions for production"

# CI/CD uses frozen lock
uv sync --frozen
```

### Example 6: Monorepo with Path Dependencies

```bash
# Main project
uv init main-app
cd main-app

# Add local packages (editable)
uv add --editable ../shared-lib
uv add --editable ../utils-lib

# Now imports work from both packages
```

## Requirements

- **uv installed** (install: `curl -LsSf https://astral.sh/uv/install.sh | sh`)
- **Understanding of PEP 508** version specifiers (recommended)
- **Project with pyproject.toml** (created by `uv init`)
- **Python 3.8+** available

## See Also

- [uv-project-setup](../uv-project-setup/SKILL.md) - Initial project creation
- [uv-python-version-management](../uv-python-version-management/SKILL.md) - Managing Python versions
- [uv-troubleshooting](../uv-troubleshooting/SKILL.md) - Resolving dependency issues
- [uv Documentation](https://docs.astral.sh/uv/concepts/dependencies/) - Official guide
