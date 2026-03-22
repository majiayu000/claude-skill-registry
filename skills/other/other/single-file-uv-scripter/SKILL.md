---
name: single-file-uv-scripter
description: "Creates self-contained Python scripts with inline PEP 723 metadata for UV. Embeds dependencies directly in script headers for zero-config execution via `uv run`. Triggers on keywords: uv script, single file script, inline dependencies, PEP 723, self-contained python, uv run script, standalone script"
project-agnostic: true
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
---

# Single-File UV Scripter

Creates self-contained Python scripts with inline dependency declarations per PEP 723. Scripts execute via `uv run script.py` with automatic dependency resolution.

## Inline Metadata Format

```python
# /// script
# dependencies = [
#   "package-name",
#   "package>=1.0,<2.0",
# ]
# requires-python = ">=3.12"
# ///
```

### Syntax Rules

| Element | Format | Required |
|---------|--------|----------|
| Open marker | `# /// script` | Yes |
| Close marker | `# ///` | Yes |
| Dependencies | TOML array, each line `# ` prefixed | Yes (can be empty `[]`) |
| Python version | `requires-python = ">=3.X"` | Recommended |

### UV-Specific Extensions

```python
# /// script
# dependencies = ["requests"]
# requires-python = ">=3.12"
# [tool.uv]
# exclude-newer = "2024-01-15T00:00:00Z"
# ///
```

- `exclude-newer`: RFC 3339 timestamp for reproducible builds (pins to releases before date)
- `index`: Alternative PyPI index URL

## Template

```python
#!/usr/bin/env -S uv run
# /// script
# dependencies = [
#   "DEPENDENCY",
# ]
# requires-python = ">=3.12"
# ///
"""One-line description of script purpose."""
from __future__ import annotations

# imports here

def main() -> None:
    """Entry point."""
    pass

if __name__ == "__main__":
    main()
```

## Commands

| Action | Command |
|--------|---------|
| Initialize | `uv init --script name.py --python 3.12` |
| Add dep | `uv add --script name.py 'pkg>=1.0'` |
| Run | `uv run name.py [args]` |
| Make executable | `chmod +x name.py` then `./name.py` |

## Shebang Options

```python
#!/usr/bin/env -S uv run                    # Standard
#!/usr/bin/env -S uv run --quiet            # Suppress UV output
#!/usr/bin/env -S uv run --python 3.12      # Pin Python version
```

## Common Patterns

### CLI with Arguments
```python
#!/usr/bin/env -S uv run
# /// script
# dependencies = ["typer>=0.9", "rich"]
# requires-python = ">=3.12"
# ///
import typer
app = typer.Typer()

@app.command()
def main(name: str) -> None:
    print(f"Hello {name}")

if __name__ == "__main__":
    app()
```

### HTTP Client
```python
#!/usr/bin/env -S uv run
# /// script
# dependencies = ["httpx>=0.27"]
# requires-python = ">=3.12"
# ///
import httpx

def main() -> None:
    r = httpx.get("https://api.example.com/data")
    print(r.json())

if __name__ == "__main__":
    main()
```

### Data Processing
```python
#!/usr/bin/env -S uv run
# /// script
# dependencies = ["polars>=1.0", "rich"]
# requires-python = ">=3.12"
# ///
import polars as pl
from rich import print

def main() -> None:
    df = pl.read_csv("data.csv")
    print(df.describe())

if __name__ == "__main__":
    main()
```

## Constraints

- Metadata block MUST appear before any Python code (after shebang/encoding is OK)
- Project dependencies are IGNORED when running inline-metadata scripts
- Each script is isolated: deps resolved fresh per script
- Empty deps array required if no dependencies: `dependencies = []`

## Workflow

1. **Create**: Write script with inline metadata block
2. **Test**: `uv run script.py` (UV auto-installs deps)
3. **Iterate**: `uv add --script script.py 'new-pkg'` to add deps
4. **Deploy**: Script is self-contained, copy anywhere with UV installed

## Type Checking

Standard `pyright` fails on PEP 723 scripts because inline deps aren't in pyproject.toml.

**Run pyright with script's dependencies:**
```bash
uvx --from pyright --with typer --with rich pyright script.py
```

Replace `--with` args with the script's actual dependencies.

**Auto-extract deps and type-check:**
```bash
script="path/to/script.py"
deps=$(python3 -c "
import re, tomllib
with open('$script') as f: c = f.read()
m = re.search(r'# /// script\n(.*?)\n# ///', c, re.DOTALL)
if m:
    t = '\n'.join(l.lstrip('# ') for l in m.group(1).split('\n'))
    print(' '.join('--with ' + re.split(r'[<>=!]', d)[0] for d in tomllib.loads(t).get('dependencies', [])))
")
eval "uvx --from pyright $deps pyright $script"
```
