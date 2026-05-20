---
name: uv-python-tool-installer
description: Install Python command-line tools with a single command using uvx.sh (Astral's uv-based installer). Use when you need to install Python tools like ruff, black, mypy, or any PyPI package as a command-line tool. This skill provides simple curl commands for installing Python tools on macOS, Linux, and Windows.
---

# Uv Python Tool Installer

Install Python tools with a single command. Powered by [uv](https://docs.astral.sh/uv/).

## Quick Start

### macOS and Linux

```bash
curl -LsSf uvx.sh/<package>/install.sh | sh
```

Replace `<package>` with any PyPI package name.

### Windows

```bash
powershell -ExecutionPolicy ByPass -c "irm https://uvx.sh/<package>/install.ps1 | iex"
```

## Examples

### Install ruff

```bash
curl -LsSf uvx.sh/ruff/install.sh | sh
```

### Install a specific version

```bash
curl -LsSf uvx.sh/ruff/0.8.3/install.sh | sh
```

### Passing arguments

```bash
# Force installation
curl -LsSf uvx.sh/ruff/install.sh | sh -s -- --force

# Install from a specific index
curl -LsSf uvx.sh/cmake/install.sh | sh -s -- --index https://download.pytorch.org/whl/cpu
```

## Scripts

### `install.sh`

Simple bash script to install Python tools:

```bash
#!/bin/bash
# Install Python tools using uvx.sh
# Usage: ./install.sh <package> [version] [--force] [--index URL]

PACKAGE=$1
VERSION=$2
shift 2

if [ -n "$VERSION" ]; then
    URL="https://uvx.sh/${PACKAGE}/${VERSION}/install.sh"
else
    URL="https://uvx.sh/${PACKAGE}/install.sh"
fi

curl -LsSf "$URL" | sh -s -- "$@"
```

**Usage:**
```bash
./scripts/install.sh ruff
./scripts/install.sh ruff 0.8.3
./scripts/install.sh ruff 0.8.3 --force
```

## Common Python Tools

- `ruff` - Fast Python linter
- `black` - Python code formatter  
- `mypy` - Static type checker
- `httpie` - Modern HTTP client
- `pipx` - Install and run Python applications in isolated environments
- `jupyter` - Jupyter notebooks
- `poetry` - Python dependency management

## Notes

- Tools are installed to `~/.local/bin` by default
- Ensure `~/.local/bin` is in your PATH
- Uses `uv` under the hood for fast, reliable installation
- Works with any PyPI package that provides command-line tools
