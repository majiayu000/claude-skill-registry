---
name: uv-project-migration
description: |
  Migrate existing Python projects to uv from pip, Poetry, Pipenv, or Conda.
  Learn how to convert dependency files, preserve development environment setup,
  validate the migration, and plan team rollout. Use when converting legacy
  projects to modern uv tooling, consolidating different package managers,
  or standardizing Python development workflows across teams.
allowed-tools: Bash, Read, Write, Edit
---

# uv Project Migration

## Purpose

Migrate existing Python projects to uv from pip, Poetry, Pipenv, or Conda. Transfer all
dependencies, preserve development configurations, validate functionality, and roll out
changes to your team.

## Quick Start

Convert an existing project to uv in three commands:

```bash
# From pip/requirements.txt project
cd my-legacy-project
uv init --requirements requirements.txt

# From Poetry project
cd my-poetry-project
uv init --pyproject

# Verify everything works
uv run pytest
```

Your project now uses uv with all original dependencies preserved.

## Instructions

### Step 1: Understanding When and Why to Migrate

**Benefits of migrating to uv:**
- 10-100x faster dependency resolution
- Simpler syntax than Poetry or Pipenv
- Single tool replaces pip, poetry, pipenv, virtualenv
- Better lock file format
- Excellent cross-platform support

**When to migrate:**
- Legacy pip + requirements.txt projects
- Poetry projects wanting better performance
- Pipenv projects needing simplified tooling
- Teams standardizing on one package manager

**When to NOT migrate:**
- Projects with complex Poetry features (build backends)
- Legacy Conda-dependent projects
- Projects with platform-specific wheels

### Step 2: Prepare Your Existing Project

**For pip/requirements.txt projects:**
```bash
cd my-project
ls -la
# Should have: requirements.txt, src/, tests/, setup.py or pyproject.toml
```

**For Poetry projects:**
```bash
cd my-poetry-project
cat pyproject.toml | head -20
# Should have: [tool.poetry] section with name, version, dependencies
```

**For Pipenv projects:**
```bash
cd my-pipenv-project
ls -la
# Should have: Pipfile, Pipfile.lock
```

**Backup your project:**
```bash
git add .
git commit -m "Backup before uv migration"
git branch backup-pre-uv-migration
```

### Step 3: Automatic requirements.txt Conversion

**For pip projects with requirements.txt:**

```bash
# Navigate to project
cd my-project

# Initialize uv with existing requirements
uv init --requirements requirements.txt

# This creates:
# - pyproject.toml (from requirements.txt)
# - .python-version (from current Python)
# - uv.lock (resolved lock file)
```

**Verify pyproject.toml was created:**
```bash
cat pyproject.toml
# Should contain all your dependencies from requirements.txt
```

**Complex requirements files:**
```bash
# If you have multiple requirements files
uv init
uv add --dev -r dev-requirements.txt
uv add -r prod-requirements.txt
```

### Step 4: Migrate from Poetry

**For Poetry projects (pyproject.toml):**

```bash
cd my-poetry-project

# Option A: Automatic conversion
uv init --pyproject
```

**If automatic fails, manual conversion:**

```bash
# 1. Create uv project
uv init

# 2. Copy dependencies from Poetry to uv
# Edit pyproject.toml:
# Change [tool.poetry] section → [project] section
# Change "poetry" dependencies format → standard format

# Before (Poetry):
[tool.poetry.dependencies]
python = "^3.11"
fastapi = "^0.104.0"

# After (uv/standard):
[project]
requires-python = ">=3.11"
dependencies = [
    "fastapi>=0.104.0,<1.0.0",
]

# 3. Add Poetry dev dependencies as uv groups
[dependency-groups]
dev = [
    "pytest>=8.0.0",
    "black>=23.0.0",
]
```

**Resolve dependencies:**
```bash
uv sync --all-groups
```

### Step 5: Migrate from Pipenv

**For Pipenv projects (Pipfile/Pipfile.lock):**

```bash
cd my-pipenv-project

# 1. Read Pipfile to understand structure
cat Pipfile

# 2. Create uv project
uv init

# 3. Convert Pipfile to pyproject.toml
# Edit pyproject.toml following this pattern:

# From Pipfile:
[packages]
django = ">=3.2"
requests = "~=2.31.0"

[dev-packages]
pytest = "*"
black = "*"

# To pyproject.toml:
[project]
dependencies = [
    "django>=3.2",
    "requests>=2.31.0,<2.32.0",
]

[dependency-groups]
dev = [
    "pytest",
    "black",
]
```

**Resolve dependencies:**
```bash
uv sync --all-groups
```

### Step 6: Testing and Validation

**Verify migration worked:**

```bash
# Check dependencies resolved
uv tree

# Run existing tests
uv run pytest

# Run linting/type-checking if applicable
uv run mypy src/
uv run ruff check src/

# Run application if applicable
uv run python -m myapp
```

**Compare lock files (if migrating from Poetry/Pipenv):**

```bash
# List dependencies from uv
uv tree > /tmp/uv-deps.txt

# Compare counts
wc -l /tmp/uv-deps.txt
# Should be similar to old package manager
```

**Performance comparison:**

```bash
# Original tool (e.g., poetry)
time poetry install

# New tool (uv)
time uv sync
# uv should be significantly faster
```

### Step 7: Team Onboarding and Rollout

**Prepare team documentation:**

```bash
# Create MIGRATION_GUIDE.md or update README.md
# Include:
# 1. Why we're migrating
# 2. What changed (commands, workflow)
# 3. Installation instructions
# 4. Common troubleshooting
```

**Update project documentation:**

```markdown
## Installation and Setup

### Prerequisites
- uv installed: `curl -LsSf https://astral.sh/uv/install.sh | sh`

### Setup Development Environment
```bash
cd project-directory
uv sync --all-groups      # Install all dependencies
uv run pytest             # Run tests
```

### Commands Changed
| Old Command | New Command | Notes |
|-------------|-------------|-------|
| poetry install | uv sync | No equivalent needed |
| poetry add requests | uv add requests | Simpler syntax |
| poetry run pytest | uv run pytest | Shorter prefix |
| pipenv install | uv sync | Automatic resolution |
| pip install -r requirements.txt | uv sync | All in pyproject.toml |
```

**Rollout strategy:**

```bash
# Step 1: Merge migration to main branch
git add pyproject.toml uv.lock
git commit -m "Migrate project to uv package manager"
git push

# Step 2: Team pulls and verifies
git pull
uv sync --all-groups
uv run pytest  # Verify tests pass

# Step 3: Update CI/CD pipelines
# (See uv-ci-cd-integration skill for details)

# Step 4: Optional: Remove old tool files
rm requirements.txt      # If migrating from pip
rm Pipfile Pipfile.lock  # If migrating from Pipenv
git add -A
git commit -m "Remove old package manager files"
```

## Examples

### Example 1: Migrate Simple pip Project

```bash
# Original project structure
ls -la
# pyproject.toml (minimal)
# requirements.txt (your dependencies)
# src/
# tests/

# Migrate
cd ~/my-project
uv init --requirements requirements.txt

# Verify
cat pyproject.toml
uv tree

# Test
uv run pytest

# Commit
git add .
git commit -m "Migrate to uv"
```

### Example 2: Migrate Poetry Project to uv

```bash
# Original Poetry project
cd ~/poetry-project
cat pyproject.toml | grep -A 10 "\[tool.poetry\]"

# Migrate (automatic)
uv init --pyproject

# If automatic fails, manual steps:
# Edit pyproject.toml to convert [tool.poetry] → [project]
# Ensure all dependencies are listed correctly

# Verify migration
uv sync --all-groups
uv tree
uv run pytest
```

### Example 3: Migrate Pipenv Project

```bash
# Original Pipenv project
cd ~/pipenv-project
cat Pipfile

# Convert Pipfile → pyproject.toml manually
# Edit Pipfile, copy/transform dependencies

# Create uv project
uv init

# Edit pyproject.toml with converted dependencies
# Run
uv sync --all-groups

# Verify
uv tree
uv run pytest
```

### Example 4: Multi-Stage Migration with Testing

```bash
# Step 1: Create feature branch
git checkout -b feature/migrate-to-uv

# Step 2: Setup uv
uv init --requirements requirements.txt

# Step 3: Validate thoroughly
uv sync --all-groups
uv run pytest
uv run mypy src/
uv run ruff check src/

# Step 4: Check for differences
uv tree
# Compare with original project structure

# Step 5: Commit and PR
git add pyproject.toml uv.lock
git commit -m "chore: migrate to uv package manager"
git push origin feature/migrate-to-uv

# Step 6: After merge, notify team
# - Update README.md with new commands
# - Create documentation for team setup
# - Remove old requirement files after validation
```

### Example 5: Rollback if Issues Found

```bash
# If migration has problems, rollback
git checkout main
git reset --hard HEAD~1  # Undo last commit

# Or restore from backup branch
git checkout backup-pre-uv-migration

# Debug the issue
# - Check pyproject.toml for syntax errors
# - Verify all dependencies listed
# - Try uv sync --all-groups again
```

### Example 6: Monorepo Migration

```bash
# Monorepo structure
ls -la
# project-a/
# project-b/
# shared-lib/

# Migrate project-a
cd project-a
uv init --requirements requirements.txt

# Add shared library as path dependency
uv add --editable ../shared-lib

# Migrate project-b
cd ../project-b
uv init --requirements requirements.txt

# Add shared library
uv add --editable ../shared-lib

# Sync everything
cd ..
uv sync --all-groups
```

## Requirements

- **uv installed** (install: `curl -LsSf https://astral.sh/uv/install.sh | sh`)
- **Existing Python project** with dependencies (pip, Poetry, Pipenv, or Conda)
- **Git repository** (recommended for backup/rollback)
- **Python 3.8+** available
- **Access to package index** (PyPI) during migration

## See Also

- [uv-project-setup](../uv-project-setup/SKILL.md) - Creating new projects from scratch
- [uv-dependency-management](../uv-dependency-management/SKILL.md) - Managing dependencies after migration
- [uv-ci-cd-integration](../uv-ci-cd-integration/SKILL.md) - Updating CI/CD pipelines for uv
- [uv-troubleshooting](../uv-troubleshooting/SKILL.md) - Troubleshooting migration issues
- [uv Documentation](https://docs.astral.sh/uv/guides/projects/) - Official migration guide
