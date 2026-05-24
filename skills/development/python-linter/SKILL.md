---
name: python-linter
description: Guide coding agents to fix specific Python linter issues from Ruff. Use when encountering Ruff linter errors identified by alpha-numeric codes (e.g., B008, S108, PLC0415). Provides context-aware resolution strategies for common linter issues.
license: MIT
metadata:
  ruff_version: ">=0.12.0"
  related_python_guidelines: For general Python practices, use skill `python-guidelines`
---

# Python Linter Issue Resolution

## What I Do

Provide specific, context-aware guidance for resolving Python linter issues identified by Ruff's alpha-numeric rule codes. Each rule includes what the issue means, why it matters, and how to fix it with practical examples.

## How to Use This Skill

When you encounter a Ruff linter error:

1. **Identify the rule code** from the linter output (e.g., `B008`, `S108`, `PLC0415`)
2. **Look up the rule** in the sections below or reference files
3. **Apply the context-appropriate fix** based on your code's purpose
4. **Verify the fix** resolves the issue without introducing new problems

## Common Linter Issues

The following issues can often be fixed automatically by linter tools, but when they require manual intervention, the coding assistant should always resolve them as they are straightforward.

### E402: Module Level Import Not at Top of File

**What it means:** An import statement appears after code that is not an import, comment, or docstring.

**Why it matters:** PEP 8 requires all imports to be at the top of the file, before any other code (except for docstrings and comments). This ensures dependencies are clearly visible and avoids potential side effects from code executed before imports.

**How to fix:** Move the import statement to the top of the module, grouping it with other imports.

---

### B007: Loop Control Variable Not Used

**What it means:** A variable defined in a `for` loop is never used within the loop body.

**Why it matters:** It can signal a bug (the variable was intended to be used) or simply clutter the code. Using a specific naming convention for unused variables makes intent clear.

**How to fix:** Prefix the unused variable with an underscore (e.g., `_item` or just `_`).

---

### B008: Function Call in Default Argument

**What it means:** A function call is being used as a default argument value, which is evaluated only once at function definition time.

**Why it matters:** The function is called once when the module loads, not each time the function is called. This can lead to unexpected behavior with mutable returns or side effects.

**How to fix:**

#### Standard Case: Move initialization into function body

```python
# BEFORE (linter error)
def create_list() -> list[int]:
    return [1, 2, 3]

def process_data(items: list[int] = create_list()) -> list[int]:
    items.append(4)
    return items

# AFTER (fixed)
def process_data(items: list[int] | None = None) -> list[int]:
    if items is None:
        items = create_list()
    items.append(4)
    return items
```

#### Special Case: Typer CLI arguments (EXCEPTION - DO NOT FIX)

When using `typer.Option()` or `typer.Argument()`, function calls in defaults are **intentional and required**. Use this special annotation pattern:

```python
# CORRECT for Typer CLI
from typing import Annotated
import typer

def main(
    # Use Annotated with typer.Option/Argument - this is the correct pattern
    config: Annotated[
        str,
        typer.Option(
            help="Configuration file path",
            default="config.yaml"
        )
    ] = "config.yaml",  # Default value for the parameter itself
) -> None:
    """CLI command with proper Typer annotations."""
    ...
```

**Reference example:** See `references/typer-cli-pattern.md` for complete Typer CLI annotation patterns.

**Ruff documentation:** https://docs.astral.sh/ruff/rules/function-call-in-default-argument/

---

### S108: Hardcoded Temp File

**What it means:** Using hardcoded paths like `/tmp/`, `/var/tmp/`, or `C:\Temp\` for temporary files.

**Why it matters:** Security risk (predictable paths can be exploited), portability issues (paths differ across OS), and potential conflicts with other programs.

**How to fix:**

#### Production Code: Use tempfile module

```python
# [X] BEFORE (linter error)
with open("/tmp/data.txt", "w") as f:
    f.write(data)

# [OK] AFTER (fixed)
import tempfile

with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
    f.write(data)
    temp_path = f.name
```

#### Test Code: Use pytest's tmp_path fixture

```python
# [X] BEFORE (linter error in test)
def test_file_processing():
    test_file = "/tmp/test_data.txt"
    with open(test_file, "w") as f:
        f.write("test")
    result = process_file(test_file)
    os.remove(test_file)

# [OK] AFTER (fixed)
from pathlib import Path

def test_file_processing(tmp_path: Path):
    test_file = tmp_path / "test_data.txt"
    test_file.write_text("test")
    result = process_file(test_file)
    # No cleanup needed - pytest handles it
```

**When to use each approach:**
- **Production code (main codebase):** `tempfile.NamedTemporaryFile()`
- **Test modules (pytest):** `tmp_path: Path` fixture

**Ruff documentation:** https://docs.astral.sh/ruff/rules/hardcoded-temp-file/

---

### PLC0415: Import Outside Top-Level

**What it means:** Import statements are placed inside functions, methods, or class definitions instead of at module level.

**Why it matters:** PEP 8 recommends top-level imports for easier dependency identification, better IDE support, and catching import errors at module load time.

**How to fix:**

#### Standard Case: Move imports to top of file

```python
# [X] BEFORE (linter error)
def print_python_version():
    import platform
    print(platform.python_version())

# [OK] AFTER (fixed)
import platform

def print_python_version():
    print(platform.python_version())
```

#### Valid Exceptions (when nested imports are acceptable):

1. **Avoiding circular dependencies**
2. **Lazy loading expensive modules**
3. **Optional dependencies** (imports that may not be available)
4. **Type checking imports** (using `if TYPE_CHECKING:`)

```python
# [OK] ACCEPTABLE: Type checking imports
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mypy_extensions import TypedDict

# [OK] ACCEPTABLE: Optional dependency
def use_optional_feature():
    try:
        import optional_package
        return optional_package.feature()
    except ImportError:
        return None  # Graceful fallback
```

**Import organization standard:**

```python
# 1. Standard library imports
import os
import sys
from pathlib import Path

# 2. Third-party imports
import typer
from rich.console import Console

# 3. Local application imports
from .utils import helpers
from .core import processors
```

**Ruff documentation:** https://docs.astral.sh/ruff/rules/import-outside-top-level/

---

### NPY002: Legacy NumPy Random Generation

**What it means:** Usage of the legacy `numpy.random` functions (like `np.random.seed`, `np.random.normal`) instead of the modern `Generator` API.

**Why it matters:** The legacy `RandomState` methods are frozen and less efficient. The new `Generator` API (introduced in NumPy 1.17) is faster, has better statistical properties, and avoids global state issues.

**How to fix:**

#### Standard Case: Use default_rng()

```python
# [X] BEFORE (linter error)
import numpy as np

np.random.seed(1337)
data = np.random.normal(size=100)

# [OK] AFTER (fixed)
import numpy as np

# Create a Generator instance
rng = np.random.default_rng(1337)
data = rng.normal(size=100)
```

**Ruff documentation:** https://docs.astral.sh/ruff/rules/numpy-legacy-random/

---

### S311: Suspicious Non-Cryptographic Random Usage

**What it means:** Use of the standard `random` module for generating random numbers in potentially sensitive contexts.

**Why it matters:** Standard pseudo-random number generators (like Python's `random` or NumPy's `random`) are predictable and not cryptographically secure. They should not be used for security tokens, passwords, or authentication.

**How to fix:**

#### Security Context: Use secrets module
If generating passwords, tokens, or security keys, you **must** use the `secrets` module.

```python
# [X] BEFORE (security risk)
import random
token = random.randrange(1000000)

# [OK] AFTER (secure)
import secrets
token = secrets.randbelow(1000000)
```

#### Non-Security Context (Data Science/Simulation):
If the usage is purely for simulation, testing, or data analysis (and flagged incorrectly), you can replace with NumPy for better performance or ignore if security is not a concern.

```python
# [OK] Simulation/Science (not security sensitive)
# If performance matters, prefer NumPy over standard random
import numpy as np
rng = np.random.default_rng()
data = rng.random(100)
```

**Ruff documentation:** https://docs.astral.sh/ruff/rules/suspicious-non-cryptographic-random-usage/

---

## Additional Resources

For more detailed examples and edge cases:

- **Typer CLI patterns:** See `references/typer-cli-pattern.md`
- **Full rule index:** Browse all Ruff rules at https://docs.astral.sh/ruff/rules/

## When to Use This Skill

Activate this skill when:

- Ruff linter reports errors with alpha-numeric codes
- You need context-aware fixes (e.g., distinguishing test vs. production code)
- Working with Typer CLI and encountering B008 false positives
- Standardizing linter issue resolution across a team
- Onboarding developers to Ruff best practices

## Compatibility

- **Ruff:** Version 0.12.0 or higher
- **Python:** 3.8+
- **Frameworks:** Special handling for Typer, pytest
- **Related skills:** `python-guidelines`, `testing-strategy`
