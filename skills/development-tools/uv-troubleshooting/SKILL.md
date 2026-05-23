---
name: uv-troubleshooting
description: |
  Debug and resolve common uv issues. Learn to diagnose dependency resolution
  failures, handle version conflicts, fix cache problems, troubleshoot Python
  environment issues, optimize performance, and solve platform-specific problems.
  Use when uv commands fail, dependencies won't resolve, cache is corrupted,
  Python installation issues occur, or performance is slow.
allowed-tools: Bash, Read, Write, Edit
---

# uv Troubleshooting

## Purpose

Master troubleshooting uv issues, from dependency resolution failures to environment
setup problems. Quickly diagnose errors and get your project working again.

## Quick Start

Get help immediately when uv fails:

```bash
# See what's happening
uv sync --verbose

# Clear cache if something seems broken
uv cache clean

# Force fresh resolution
uv lock --upgrade

# Check your Python installation
uv python list
```

Most issues resolve with verbose output + cache clearing + fresh resolution.

## Instructions

### Step 1: Understanding uv Error Categories

uv errors fall into these categories:

**Resolution Errors** (versions don't match)
```
error: Failed to resolve version for package X
error: Incompatible versions required
```

**Environment Errors** (Python not found)
```
error: Python X.Y not found
error: No python version available
```

**Cache Errors** (corrupted data)
```
error: Cache is corrupted
error: Invalid cache entry
```

**Network Errors** (can't reach PyPI)
```
error: Failed to fetch from PyPI
error: Connection timeout
```

**Lock File Errors** (conflicts)
```
error: Lock file out of sync with pyproject.toml
```

### Step 2: Debugging Dependency Resolution

**Problem: "No matching version found"**

```bash
# Get verbose output to see what's being checked
uv add package-name --verbose

# Error message might say:
# error: No version of package-name found matching >=2.0,<2.5

# Solutions:
# 1. Check available versions
pip index versions package-name

# 2. Loosen version constraint
uv add "package-name>=2.0"      # Remove upper bound

# 3. Check if package was renamed
# Search PyPI website or use:
pip search package-name
```

**Problem: "Incompatible dependencies"**

```bash
# Show resolution process
uv add --dry-run package-a package-b

# If both can't work together, you'll see:
# error: Incompatible versions required for package-c:
#   package-a requires package-c>=1.0,<2.0
#   package-b requires package-c>=2.0,<3.0

# Solutions:
# 1. Try newer versions that might be compatible
uv add "package-a>=2.0" "package-b>=3.0"

# 2. Use separate dependency groups
uv add --group ml-cpu torch-cpu
uv add --group ml-gpu torch-gpu
# Install one group at a time

# 3. Contact maintainers if genuinely incompatible
```

**Problem: "Source conflicts"**

```bash
# Check your PyPI sources
cat pyproject.toml | grep -A 5 "\[tool.uv\]"

# If using custom PyPI index:
# Error might occur due to missing packages in custom index

# Solutions:
# 1. Add fallback to PyPI
[tool.uv]
index-url = "https://custom.index.com/simple"
extra-index-urls = ["https://pypi.org/simple"]

# 2. Or specify per-package
uv add --index-url https://custom.index.com requests
```

### Step 3: Handling Version Conflicts

**Problem: Lock file out of sync**

```bash
# Error message:
# error: The lock file uv.lock is out of sync with pyproject.toml

# Solution 1: Regenerate lock file
uv lock

# Solution 2: Force fresh resolution
uv lock --upgrade

# Solution 3: Clear cache and retry
uv cache clean
uv lock
```

**Problem: Pre-release versions causing issues**

```bash
# If you see error about pre-release being unavailable:
# error: pre-release version not found

# Check what's actually available
uv python list | grep 3.13

# Solution: Pin stable version instead
uv python pin 3.12   # Use stable instead of rc
```

**Problem: Transitive dependency conflict**

```bash
# When indirect dependencies conflict:
# package-a requires indirect-dep==1.0
# package-b requires indirect-dep==2.0

# Show dependency tree to find issue
uv tree

# Solution: Update one of the direct dependencies
# Find which needs updating with:
uv tree | grep indirect-dep

# Then update the direct package
uv add "package-a>=2.0"  # Might have updated indirect-dep
```

### Step 4: Cache Issues and Recovery

**Problem: Cache corruption**

```bash
# Symptoms:
# - Same operations fail each time
# - Error messages about cache
# - Slow/hanging operations

# Solution 1: Clean specific cache
uv cache clean all                # Clean everything
uv cache clean --all              # Alternative syntax

# Solution 2: Check cache location
uv cache dir
# On macOS: /Users/username/Library/Caches/uv
# On Linux: ~/.cache/uv
# On Windows: %APPDATA%\uv\cache

# Solution 3: Manual cache deletion (if needed)
rm -rf ~/.cache/uv                # Linux/macOS
rmdir %APPDATA%\uv\cache          # Windows
```

**Problem: Cache growing too large**

```bash
# Check cache size
du -sh ~/.cache/uv
# Or on macOS/Linux with homebrew-installed uv:
du -sh ~/Library/Caches/uv

# Solution: Clean unused cache
uv cache clean all

# Prevention: Set cache limits in pyproject.toml
[tool.uv]
# Limit cache to 2GB (example)
cache-size = "2G"
```

### Step 5: Environment and Python Issues

**Problem: "Python X.Y not found"**

```bash
# Error: Python 3.12 not found in PATH

# Step 1: Check what Python is available
which python
python --version

# Step 2: List uv's Python installations
uv python list

# Step 3: Install needed version
uv python install 3.12

# Step 4: Pin for project if needed
uv python pin 3.12

# Step 5: Verify
uv python list
python --version
```

**Problem: Wrong Python version being used**

```bash
# Check which Python uv is using
python --version

# Check project pinning
cat .python-version

# Solutions:
# 1. Pin correct version
uv python pin 3.12

# 2. Or remove pin to use system Python
rm .python-version

# 3. Check PATH if system Python is wrong
echo $PATH
# Make sure correct Python directory is first
```

**Problem: Virtual environment is broken**

```bash
# Symptoms:
# - Python imports fail
# - Packages installed but not found
# - Mysterious import errors

# Solution: Resync with fresh venv
uv sync --reinstall      # Reinstall all packages
# Or:
uv sync --force-reinstall-all  # Force all packages to reinstall
```

### Step 6: Performance Optimization

**Problem: Dependency resolution is slow**

```bash
# Example: `uv sync` takes 5+ minutes

# Solution 1: Use frozen lock file
uv sync --frozen         # Don't resolve, use existing lock

# Solution 2: Build cache
# Run `uv lock` once, then `uv sync` uses it

# Solution 3: Check for large transitive deps
uv tree | wc -l         # Count total dependencies
# If >100, you might have large dependency tree

# Solution 4: Disable network operations
uv sync --offline       # Use only cached packages
```

**Problem: Large lock files**

```bash
# If uv.lock is very large (>10MB)
wc -l uv.lock

# Solution 1: Trim unnecessary dependencies
uv remove unused-package

# Solution 2: Use extras to split optional deps
# Instead of: uv add package[all]
# Do: uv add package           # Core only
# Then: uv add --group extras package[optional]

# Solution 3: Check for duplicate versions
grep "^name = " uv.lock | sort | uniq -c | sort -rn
# If duplicates, investigate with:
uv tree | grep duplicate-package
```

### Step 7: Platform-Specific Issues

**Problem: Windows PATH issues**

```bash
# After installing uv, command not found

# Solution 1: Restart terminal/PowerShell
# uv installer modifies PATH, needs restart

# Solution 2: Add to PATH manually
# Find where uv installed:
where uv    # Command prompt
Get-Command uv  # PowerShell

# Solution 3: Use full path
c:\Users\username\.cargo\bin\uv --version
```

**Problem: macOS/Linux permissions**

```bash
# Error: Permission denied
# "Cannot install to /usr/local/bin"

# Solution 1: Use proper installation
curl -LsSf https://astral.sh/uv/install.sh | sh

# Solution 2: Check shell configuration
echo $PATH
# Ensure ~/.cargo/bin is in PATH

# Solution 3: Fix permissions
chmod +x ~/.cargo/bin/uv
```

**Problem: Docker build failures**

```bash
# Error building Docker image with uv

# Solution: Use official uv Docker image
FROM ghcr.io/astral-sh/uv:latest as base
FROM python:3.12-slim

# Or install uv in existing image
FROM python:3.12-slim
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.cargo/bin:$PATH"
COPY . /app
WORKDIR /app
RUN uv sync
```

## Examples

### Example 1: Debugging "No Python Found" Error

```bash
# Error when running uv sync:
# error: Failed to find python interpreter

# Step 1: Check what's available
uv python list
# Output shows no Python installed

# Step 2: Install Python 3.12
uv python install 3.12

# Step 3: Pin for project
uv python pin 3.12

# Step 4: Verify
uv python list
uv sync

# Result: Project now works
```

### Example 2: Resolving Version Conflicts

```bash
# Error when adding two packages:
# uv add package-a package-b
# error: Incompatible versions required for shared-lib

# Step 1: Get details with dry-run
uv add --dry-run package-a package-b
# Shows: package-a needs shared-lib>=1.0,<2.0
#        package-b needs shared-lib>=2.0

# Step 2: Check newer versions
uv add --dry-run "package-a>=2.0" "package-b>=3.0"
# Works! Newer versions are compatible

# Step 3: Add both
uv add "package-a>=2.0" "package-b>=3.0"

# Result: Both packages installed with compatible versions
```

### Example 3: Fixing Cache Corruption

```bash
# Symptoms:
# - Operations fail inconsistently
# - Error: "Cannot read cache entry"
# - uv hanging on sync

# Step 1: Identify cache issue
uv sync --verbose
# Shows cache corruption

# Step 2: Clean cache
uv cache clean all

# Step 3: Rebuild
uv lock --upgrade
uv sync

# Result: Everything works again
```

### Example 4: Windows PATH Setup

```bash
# After installing uv on Windows
# Error: "uv is not recognized as an internal or external command"

# Step 1: Verify uv is installed
where uv
# Returns: C:\Users\username\.cargo\bin\uv

# Step 2: Check if in PATH
$env:PATH -split ";" | Select-String ".cargo"
# Should show .cargo path

# Step 3: If missing, restart terminal
# Close and reopen PowerShell/Terminal

# Step 4: Verify works
uv --version
# uv 0.1.39
```

### Example 5: Docker Build Optimization

```dockerfile
# Original that fails
FROM python:3.12-slim
RUN pip install uv
COPY . /app
WORKDIR /app
RUN uv sync   # Fails: uv not in PATH

# Fixed version
FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
COPY . /app
WORKDIR /app
RUN uv sync

# Result: Docker image builds successfully
```

### Example 6: Troubleshooting Slow Resolution

```bash
# Problem: uv sync takes 2 minutes
# Project has 150+ transitive dependencies

# Step 1: Check what's slow
time uv lock --upgrade
# Takes 90 seconds

# Step 2: Use frozen lock after first sync
uv sync --frozen
# Takes 5 seconds (no resolution)

# Step 3: Only update lock when intentional
uv lock --upgrade    # Do this occasionally
uv sync --frozen     # Use this normally

# Result: 18x faster sync for daily development
```

## Requirements

- **uv installed** (install: `curl -LsSf https://astral.sh/uv/install.sh | sh`)
- **Python 3.8+** available (for basic operations)
- **Internet connection** (for downloading packages and resolving versions)
- **Git** (optional, for version control and rollback)
- **Understanding of dependency resolution** (recommended)

## See Also

- [uv-dependency-management](../uv-dependency-management/SKILL.md) - Proper dependency management to prevent issues
- [uv-python-version-management](../uv-python-version-management/SKILL.md) - Managing Python versions correctly
- [uv-project-migration](../uv-project-migration/SKILL.md) - Migration troubleshooting
- [uv-ci-cd-integration](../uv-ci-cd-integration/SKILL.md) - CI/CD specific issues
- [uv Documentation](https://docs.astral.sh/uv/guides/index/) - Official troubleshooting guide
