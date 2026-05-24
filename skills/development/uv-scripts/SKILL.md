---
name: uv-scripts
description: Use when running or authoring standalone Python scripts with uv, especially when choosing Python versions, adding one-off dependencies, using no-project mode, or embedding inline script metadata.
---

# UV Scripts

## Overview
Use `uv run` to execute standalone scripts with automatic dependency management. Prefer inline metadata for self-contained scripts and `--no-project` when you are inside a project but do not need project code.

## Quick Reference

| Need | Command |
| --- | --- |
| Run a script | `uv run script.py` |
| Run module | `uv run -m http.server 8000` |
| Run from stdin | `uv run -` |
| Here-doc | `uv run - <<EOF ... EOF` |
| Skip project install | `uv run --no-project script.py` |
| One-off deps | `uv run --with requests --with rich script.py` |
| Pick Python | `uv run --python 3.12 script.py` |
| Init script metadata | `uv init --script script.py --python 3.12` |
| Add script deps | `uv add --script script.py requests rich` |
| Lock script deps | `uv lock --script script.py` |

## Running a Script Without Dependencies

```bash
uv run example.py
uv run example.py arg1 arg2
```

Run a module:

```bash
uv run -m http.server 8000
uv run -m pytest
```

Read from stdin:

```bash
echo 'print("hello")' | uv run -
```

Here-doc:

```bash
uv run - <<EOF
print("hello")
EOF
```

## Project vs. No-Project Mode

- In a project (directory with `pyproject.toml`), `uv run` installs the project first.
- If the script does not need project code, use `--no-project` to skip installation.
- The `--no-project` flag must be before the script name.

```bash
uv run --no-project example.py
```

If you use inline script metadata, project dependencies are ignored automatically and `--no-project` is not required.

## Running a Script With Dependencies

Use `--with` to add per-invocation dependencies:

```bash
uv run --with rich example.py
uv run --with 'rich>12,<13' example.py
uv run --with rich --with requests example.py
```

In a project, these dependencies are added on top of project dependencies. Use `--no-project` to avoid that.

## Inline Script Metadata (Recommended)

Initialize inline metadata:

```bash
uv init --script example.py --python 3.12
```

Add dependencies:

```bash
uv add --script example.py 'requests<3' 'rich'
```

Example script:

```python
# /// script
# dependencies = [
#   "requests<3",
#   "rich",
# ]
# ///

import requests
from rich.pretty import pprint

resp = requests.get("https://peps.python.org/api/peps.json")
data = resp.json()
pprint([(k, v["title"]) for k, v in data.items()][:10])
```

Notes:
- The `dependencies` field must be provided even if empty.
- Inline metadata ignores project dependencies; `--no-project` is not required.

Specify a Python requirement in metadata:

```python
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
```

`uv run` will locate (and download if needed) the required Python version.

## Shebang for Executable Scripts

```python
#!/usr/bin/env -S uv run --script

print("Hello, world!")
```

Make executable and run:

```bash
chmod +x greet
./greet
```

Dependencies are supported in this mode via inline metadata.

## Locking and Reproducibility

Lock dependencies for a script:

```bash
uv lock --script example.py
```

This creates `example.py.lock` next to the script. Subsequent `uv run --script`, `uv add --script`, and `uv export --script` reuse the lock.

To improve reproducibility across time, add `exclude-newer`:

```python
# /// script
# dependencies = ["requests"]
# [tool.uv]
# exclude-newer = "2023-10-16T00:00:00Z"
# ///
```

## Alternative Package Indexes

```bash
uv add --index "https://example.com/simple" --script example.py 'requests<3' 'rich'
```

This adds `tool.uv.index` metadata to the script.

## Python Version Selection

```bash
uv run --python 3.10 example.py
```

## Windows GUI Scripts

On Windows, `.pyw` scripts run with `pythonw`:

```bash
uv run example.pyw
```

Dependencies still work, e.g. `uv run --with PyQt5 example_pyqt.pyw`.

## Common Mistakes

- Using `python script.py` after installing deps manually instead of `uv run`.
- Forgetting `--no-project` in project directories when you do not need project code.
- Placing `--no-project` after the script name.
- Omitting the `# /// script` metadata block when you want self-contained scripts.
- Assuming inline metadata uses project dependencies (it ignores them).
