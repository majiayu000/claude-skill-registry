---
name: uv-python-version-management
description: |
  Manages Python versions with uv. Learn how to discover available Python versions, install specific versions, pin project-specific versions using .python-version files, and runs tools with different Python versions. Use when setting up new projects, ensuring team uses same Python version, testing across multiple versions, or managing legacy projects with older Python requirements.
allowed-tools: Bash, Read, Write, Edit
---

# uv Python Version Management

## Purpose

Discover, install, and manage Python versions across your projects and tools. Ensure
consistent Python versions within teams and easily test across multiple versions.

## Quick Start

Find and pin a Python version for your project:

```bash
# See what Python versions are available
uv python list

# Install a specific version
uv python install 3.12

# Pin it for your project
uv python pin 3.12

# Verify
cat .python-version
```

Now anyone using this project automatically uses Python 3.12.

## Instructions

### Step 1: Understand Python Version Management

uv helps with three related tasks:

**Python Discovery:** Find what versions are available
```bash
uv python list        # Show installed and available versions
```

**Python Installation:** Install specific versions
```bash
uv python install 3.12
```

**Project Pinning:** Ensure team uses same version
```bash
uv python pin 3.12    # Create .python-version file
```

### Step 2: Discover Available Python Versions

**List all known versions:**
```bash
uv python list
```

**Output example:**
```
3.9.19   (installed)
3.10.14  (installed)
3.11.7   (installed)
3.12.1   (installed) ← Currently in use
3.13.0rc1
3.13.0
```

**See only installed:**
```bash
uv python list --only-installed
```

**Find latest of a version:**
```bash
uv python list | grep "3.12"
```

### Step 3: Install Python Versions

**Install specific version:**
```bash
uv python install 3.12          # Latest 3.12.x
uv python install 3.12.1        # Exact version
uv python install 3.11.5        # Older version for testing
```

**Install multiple versions:**
```bash
uv python install 3.11 3.12 3.13
```

**This is automated - no manual compilation needed.**

### Step 4: Pin Project Python Version

**Create .python-version file:**
```bash
cd my-project
uv python pin 3.12
cat .python-version
# Output: 3.12
```

**What this does:**
- Creates `.python-version` file in project root
- Any `uv` command in that directory uses Python 3.12
- Team members automatically get same version
- Commit to git for consistency

**Pin specific patch version:**
```bash
uv python pin 3.12.1
```

### Step 5: Run Tools with Specific Python

**Test code with different Python versions:**
```bash
uvx --python 3.10 pytest tests/
uvx --python 3.11 pytest tests/
uvx --python 3.12 pytest tests/
```

**Useful for:**
- Testing backward compatibility
- Ensuring minimum Python requirement works
- Validating code on pre-release versions

### Step 6: Python Versions in CI/CD

**GitHub Actions with matrix:**
```yaml
strategy:
  matrix:
    python-version: ["3.10", "3.11", "3.12", "3.13"]
steps:
  - uses: astral-sh/setup-uv@v6
  - run: uv python install ${{ matrix.python-version }}
  - run: uv sync --all-groups
  - run: uv run pytest
```

**GitLab CI with matrix:**
```yaml
test:
  parallel:
    matrix:
      - PYTHON_VERSION: ["3.10", "3.11", "3.12"]
  image: python:${PYTHON_VERSION}
  before_script:
    - uv python install ${PYTHON_VERSION}
  script:
    - uv sync --all-groups
    - uv run pytest
```

### Step 7: Handle Pre-Release Versions

**Check for pre-release versions:**
```bash
uv python list | grep rc
uv python list | grep alpha
uv python list | grep beta
```

**Install pre-release:**
```bash
uv python install 3.13.0rc1
```

**Pin pre-release for testing:**
```bash
uv python pin 3.13.0rc1
```

## Examples

### Example 1: Find and Install Python 3.12

```bash
# See what's available
uv python list

# Find Python 3.12
uv python list | grep "3.12"

# Install it
uv python install 3.12

# Verify installation
python --version
```

### Example 2: Project Setup with Pinned Version

```bash
# Create new project
uv init my-app
cd my-app

# Pin to Python 3.12
uv python pin 3.12

# Team member clones and uses it
cd my-app                 # Automatically uses 3.12
python --version          # Python 3.12.1
```

### Example 3: Test Backward Compatibility

```bash
# Test with minimum supported version
uvx --python 3.10 pytest tests/

# Test with current version
uvx --python 3.12 pytest tests/

# Test with pre-release
uvx --python 3.13.0rc1 pytest tests/

# All run without installing Python versions globally
```

### Example 4: CI/CD Matrix Testing

```yaml
# .github/workflows/test.yml
name: Tests
on: [push]

jobs:
  test:
    strategy:
      matrix:
        python-version: ["3.10", "3.11", "3.12", "3.13"]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v6
      - run: uv python install ${{ matrix.python-version }}
      - run: uv sync --all-groups
      - run: uv run pytest
```

### Example 5: Docker Build with Pinned Version

```dockerfile
FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
WORKDIR /app
COPY .python-version pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev
COPY . .
CMD ["python", "-m", "myapp"]
```

### Example 6: Legacy Project Migration

```bash
# Old project on Python 3.9
cd legacy-project

# Check current version
python --version          # Python 3.9.13

# Upgrade to 3.12
uv python install 3.12
uv python pin 3.12

# Test with new version
uv run pytest

# Commit for team
git add .python-version
git commit -m "Upgrade to Python 3.12"
```

## Requirements

- **uv installed** (install: `curl -LsSf https://astral.sh/uv/install.sh | sh`)
- **Internet connection** (to download Python versions)
- **Disk space** (each Python version ~100-200 MB)
- **Administrator access** (on Windows, might need for installation)

## See Also

- [uv-project-setup](../uv-project-setup/SKILL.md) - Creating new projects
- [uv-ci-cd-integration](../uv-ci-cd-integration/SKILL.md) - Python versions in CI/CD
- [uv-troubleshooting](../uv-troubleshooting/SKILL.md) - When things go wrong
- [uv Documentation](https://docs.astral.sh/uv/guides/python-versions/) - Official guide
