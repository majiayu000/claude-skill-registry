---
name: run-python-safely
description: Execute Python code safely by checking for dangerous operations first. ALWAYS use when running agent-generated Python code.
argument-hint: <-c "code" | -f file.py>
---

# Run Python Safely

Execute Python code safely by performing AST-based static analysis to detect potentially dangerous operations before execution.

## MANDATORY USAGE

**Agents MUST use this skill when executing any Python code they have generated.**

This is a CRITICAL RULE for all agents in this repository. Before running Python code via Bash:
1. Invoke this skill using the Skill tool
2. Pass the code or file path as the argument
3. Only proceed if the code passes safety checks

**Exceptions** (when you can skip this skill):
- Running tests via `uv run pytest`
- Running standard CLI commands (e.g., `ruff format`, `ty check`)
- User-provided scripts that have already been reviewed

## When to Use

Use this skill when you need to run Python code that you've generated. The skill analyzes the code for dangerous patterns and either:
- **Executes** the code if no issues are found
- **Blocks** execution and provides feedback if dangerous operations are detected

## Usage

```bash
# Execute inline code
uv run python .claude/skills/run-python-safely/scripts/run_python_safely.py -c "print(2 + 2)"

# Execute code from file
uv run python .claude/skills/run-python-safely/scripts/run_python_safely.py -f script.py
```

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Code executed successfully |
| 1 | Code blocked due to safety concerns |
| 2 | Usage error or file not found |
| 3 | Execution timed out (5 minute limit) |

## Output Format

### Safe Code (Executed)
```
[EXECUTED]
<stdout from executed code>
```

### Unsafe Code (Blocked)
```
[BLOCKED] Code execution blocked due to safety concerns:
  - Import: os (file system and process operations)
  - Builtin: eval (arbitrary code execution)

If this code is safe, ask the user for permission to run directly.
```

## Blocked Operations

### Imports
The following imports are blocked because they can access the file system, network, or execute arbitrary code:

- `os`, `sys`, `subprocess` - System and process operations
- `shutil` - High-level file operations
- `socket`, `requests`, `httpx`, `urllib`, `ftplib` - Network operations
- `pickle`, `shelve`, `marshal` - Serialization (arbitrary code execution risk)
- `ctypes` - C library access
- `multiprocessing`, `threading` - Process/thread spawning
- `importlib`, `builtins` - Dynamic import/builtin access

### Builtin Functions
These builtin functions are blocked:

- `eval`, `exec`, `compile` - Arbitrary code execution
- `open` - File system access
- `__import__` - Dynamic module import
- `getattr`, `setattr`, `delattr` - Dynamic attribute access
- `globals`, `locals`, `vars` - Namespace access
- `breakpoint` - Debugger invocation
- `input` - User input during execution

### Methods
These method names are blocked on any object (may have rare false positives):

- `write_text`, `write_bytes`, `touch` - File creation/writing
- `mkdir`, `rmdir`, `unlink`, `rmtree` - Directory/file deletion
- `rename`, `replace` - File/directory moving
- `symlink_to`, `hardlink_to`, `link_to` - Link creation
- `chmod`, `lchmod` - Permission modification

## When Code is Blocked

If the skill blocks code that you believe is safe:

1. Explain to the user what the code does
2. Ask the user for explicit permission to run it directly
3. If granted, use `python -c "code"` or `python script.py` directly

## Safe Operations

The following are always allowed:

- Standard library modules: `math`, `json`, `re`, `datetime`, `collections`, `itertools`, `functools`, `pathlib` (read operations), etc.
- All safe builtins: `print`, `len`, `str`, `int`, `list`, `dict`, `range`, `enumerate`, `zip`, `map`, `filter`, etc.
- Reading files via pathlib: `Path.read_text()`, `Path.read_bytes()`, `Path.exists()`, `Path.is_file()`, etc.
- Pure computation and data manipulation

## Intentionally Allowed Modules

The following modules are intentionally NOT blocked:

### `tempfile`
Allows agents to create temporary working files for intermediate results. The `tempfile` module creates files in system temp directories that are automatically cleaned up. This is useful for:
- Storing intermediate computation results
- Creating scratch files during data processing
- Writing temporary config files for subprocesses

**Note**: While `tempfile` can create files, these are confined to temp directories and don't pose the same risk as arbitrary filesystem access via `os` or `shutil`.

### `asyncio`
Allows agents to use async/await patterns for concurrent operations. While `asyncio` can spawn concurrent tasks, it doesn't directly cause filesystem damage or network access (those would still be blocked by their respective module checks).

## Examples

### Safe Code Examples

```python
# Math computation
import math
print(math.sqrt(16))

# JSON processing
import json
data = {"key": "value"}
print(json.dumps(data))

# List comprehension
squares = [x**2 for x in range(10)]
print(squares)
```

### Blocked Code Examples

```python
# BLOCKED: os import
import os
os.system("ls")

# BLOCKED: open builtin
with open("file.txt", "w") as f:
    f.write("data")

# BLOCKED: unlink method
from pathlib import Path
Path("file.txt").unlink()
```
