---
name: pip
description: pip Python package manager. Use for Python packages.
---

# pip

pip is the standard package manager for Python. v24+ (2025) focuses on performance and standard compliance (PEP 668).

## When to Use

- **Python**: It is the default.
- **Virtual Environments**: Always use inside a `venv`.

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate

pip install requests
pip freeze > requirements.txt
```

## Core Concepts

### PyPI

The Python Package Index.

### Wheels (.whl)

Pre-compiled binary packages. Much faster to install than Source Distributions (.tar.gz).

### PEP 668 (Externally Managed)

Prevents `pip install` outside venv on modern Linux distros (Debian 12+, Ubuntu 24.04) to protect system packages.

## Best Practices (2025)

**Do**:

- **Use `uv`**: The new hotness. `uv pip install` is 100x faster than standard pip. Compatible API.
- **Use `pip-tools`**: Compile `requirements.in` to `requirements.txt` with hashes for security.
- **Always Venv**: Never install global packages.

**Don't**:

- **Don't use `sudo pip`**: This breaks your OS.

## References

- [pip Documentation](https://pip.pypa.io/)
