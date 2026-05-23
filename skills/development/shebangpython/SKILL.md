---
name: shebangpython
description: Validate Python shebangs and PEP 723 inline script metadata. Use when checking if Python files have correct shebangs based on their dependency requirements, when fixing incorrect shebang patterns, or when adding PEP 723 script blocks to standalone scripts with external dependencies.
user-invocable: true
argument-hint: "[file-paths...]"
---

# Python Shebang Validation

The model validates Python shebangs against dependency requirements and ensures correct PEP 723 inline script metadata.

## Arguments

$ARGUMENTS

## Instructions

If file paths provided above:

1. Read each file using the Read tool
2. Check for shebang presence and correctness
3. Validate against the rules below
4. Check execute bit status
5. Fix any misalignments with this guidance
6. Report findings for each file

If no arguments provided:

1. Ask the user which files or directories need shebang validation
2. Suggest searching for Python files that might need shebangs
3. Offer to check if existing shebangs are correct

---

## Shebang Selection Rules

### Rule 1: Stdlib-only executable scripts

**Pattern**: `#!/usr/bin/env python3`

**Conditions**:

- File is executable
- Has no external dependencies
- Uses only Python standard library

**Reasoning**: No dependency installation required, standard Python interpreter sufficient.

### Rule 2: Package executables

**Pattern**: `#!/usr/bin/env python3`

**Conditions**:

- File is part of installed package
- Has setup.py or pyproject.toml managing dependencies

**Reasoning**: Dependencies installed via package manager, not script metadata.

### Rule 3: Standalone scripts with external dependencies

**Pattern**: `#!/usr/bin/env -S uv --quiet run --active --script`

**Conditions**:

- File is executable standalone script
- Requires external packages

**Reasoning**: PEP 723 inline metadata declares dependencies, uv installs them automatically.

### Rule 4: Non-executable files

**Pattern**: No shebang line

**Conditions**:

- File is library module
- Imported by other code
- Not directly executable

**Reasoning**: Not intended for direct execution.

---

## UV Shebang Command Structure

The shebang: `#!/usr/bin/env -S uv --quiet run --active --script`

### Component Breakdown

| Component           | Position                        | Purpose                                                       |
| ------------------- | ------------------------------- | ------------------------------------------------------------- |
| `#!/usr/bin/env -S` | Prefix                          | Shebang invoking env with -S flag for multiple arguments      |
| `uv`                | Command                         | The uv binary on PATH                                         |
| `--quiet`           | GLOBAL flag (before subcommand) | Suppresses progress output from uv                            |
| `run`               | Subcommand                      | Executes Python scripts with automatic environment management |
| `--active`          | run flag (after subcommand)     | Prefer active virtual environment over isolated environment   |
| `--script`          | run flag (after subcommand)     | Indicates file contains PEP 723 inline script metadata        |

### Command Syntax Pattern

```text
uv [GLOBAL_FLAGS] SUBCOMMAND [SUBCOMMAND_FLAGS] [ARGS]
```

### Flag Ordering Rule

Global flags modify the uv binary behavior and MUST appear before the subcommand.
Subcommand flags modify that specific subcommand's behavior and MUST appear after the subcommand.

**Valid**: `uv --quiet run --active --script`
**Invalid**: `uv run --quiet --active --script` (--quiet is global flag)

### Invalid Variations

The model MUST reject these malformed shebangs:

- `#!/usr/bin/env -S uv run --quiet --active --script` (--quiet in wrong position)
- `#!/usr/bin/env -S uv --quiet run --script` (missing --active)
- `#!/usr/bin/env -S uv run --active --script` (missing --quiet)
- `#!/usr/bin/env -S uv --quiet --active run --script` (--active in wrong position)

---

## Execute Bit Requirement

All files with shebangs MUST have execute permission set.

```bash
chmod +x filename
```

Without execute bit, the shebang is ignored by the kernel.

---

## Mandatory Verification Format

For each file, output in this exact order:

1. **Current shebang**: [exact line from file or "none"]
2. **PEP 723 metadata dependencies**: [exact list or "none"]
3. **External package count**: [number with evidence]
4. **Import analysis**:
   - stdlib: [list]
   - external: [list]
5. **Rule condition evaluation**:
   - Rule 1: [condition 1 MET/NOT MET] [condition 2 MET/NOT MET] [condition 3 MET/NOT MET]
   - Rule 2: [condition 1 MET/NOT MET] [condition 2 MET/NOT MET]
   - Rule 3: [condition 1 MET/NOT MET] [condition 2 MET/NOT MET]
   - Rule 4: [condition 1 MET/NOT MET]
6. **Applicable rule**: [number] because [one-sentence justification citing specific unmet/met conditions]
7. **Execute bit**: [executable/not executable via test command]
8. **Verdict**: CORRECT / INCORRECT [if incorrect, Edit the file to fix]

---

## Transformation Examples

### Example 1: Remove redundant PEP 723 from stdlib-only script

**Before** (invalid - no external dependencies):

```python
#!/usr/bin/env -S uv --quiet run --active --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///

from __future__ import annotations

import re
from pathlib import Path
```

**After** (corrected):

```python
#!/usr/bin/env python3

from __future__ import annotations

import re
from pathlib import Path
```

### Example 2: Add PEP 723 to script with external dependencies

**Before** (invalid - missing PEP 723):

```python
#!/usr/bin/env python

from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console
from rich.panel import Panel
```

**After** (corrected):

```python
#!/usr/bin/env -S uv --quiet run --active --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "typer>=0.19.2",
# ]
# ///

from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console
from rich.panel import Panel
```

---

## References

- [PEP 723 - Inline Script Metadata](https://peps.python.org/pep-0723/)
- [uv CLI Reference](https://docs.astral.sh/uv/reference/cli/)
- [uv run Subcommand](https://docs.astral.sh/uv/reference/cli/#uv-run)
