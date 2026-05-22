---
name: layer-helpers
description: Use when creating or modifying code in nomarr/helpers/. Helpers are pure utilities with NO nomarr.* imports. Only stdlib and third-party libraries allowed.
---

# Helpers Layer

**Purpose:** Provide pure utilities and shared data types used across all layers.

Helpers are **stateless utilities** that:
- Perform generic operations (file handling, time, SQL fragments)
- Define DTOs (data transfer objects)
- Define exceptions
- Have **no knowledge of Nomarr's domain**

---

## Directory Structure

```
helpers/
├── files_helper.py           # Path utilities, file discovery
├── file_validation_helper.py # Path validation
├── logging_helper.py         # Logging utilities
├── time_helper.py            # Time utilities (now_ms, etc.)
├── exceptions.py             # Domain exceptions
├── dataclasses.py            # Shared dataclasses
└── dto/                      # Data transfer objects
    ├── processing_dto.py     # FileDict, ProcessingResult, etc.
    ├── library_dto.py        # LibraryDict, etc.
    ├── analytics_dto.py      # AnalyticsResult, etc.
    └── __init__.py
```

---

## Import Rules

**Helpers may ONLY import:**

```python
# ✅ Allowed
import os
import pathlib
from datetime import datetime
from typing import TypedDict
import yaml  # Third-party OK
```

**DTO cross-imports are allowed (one-way only):**

```python
# ✅ Allowed - sibling DTO imports within helpers/dto/
from nomarr.helpers.dto.tags_dto import Tags  # OK in processing_dto.py
from nomarr.helpers.dto.path_dto import LibraryPath  # OK in ml_dto.py
```

The dependency direction must be acyclic. If `A` imports `B`, then `B` must not import `A`.

**Helpers must NEVER import from higher layers:**

```python
# ❌ NEVER import any higher-layer nomarr.* modules
from nomarr.persistence import Database
from nomarr.services import ConfigService
from nomarr.workflows import ...
from nomarr.components import ...
from nomarr.interfaces import ...
```

This is a **hard rule**. Helpers are the foundation—they cannot depend on anything above them.

---

## No Config at Import Time

Helpers must **never** read config files or environment variables at import time:

```python
# ❌ Wrong - reads at import
import os
DEFAULT_PATH = os.environ.get("NOMARR_PATH", "/data")  # NO!

# ✅ Correct - function parameter
def get_data_path(config_path: str | None = None) -> str:
    ...
```

---

## DTO Pattern

DTOs are typed dictionaries or dataclasses for cross-layer data:

```python
# helpers/dto/processing_dto.py
from typing import TypedDict

class FileDict(TypedDict):
    _key: str
    _id: str
    file_path: str
    library_key: str
    status: str
    discovered_at: int
    processed_at: int | None
```

### DTO Placement Rules

- **Cross-layer DTOs** (used by multiple layers): `helpers/dto/<domain>.py`
- **Single-service DTOs** (used only in one service): Define in service file

---

## Pure Utility Functions

Helpers should be **pure** (no side effects, deterministic output):

```python
# ✅ Good - pure function
def normalize_path(path: str) -> str:
    return str(pathlib.Path(path).resolve())

# ✅ Good - utility with explicit inputs
def now_ms() -> int:
    return int(datetime.now().timestamp() * 1000)

# ❌ Bad - hidden state/side effects
_cached_time: int | None = None

def get_time() -> int:
    global _cached_time
    if _cached_time is None:
        _cached_time = int(datetime.now().timestamp() * 1000)
    return _cached_time
```

---

## Exceptions

Domain exceptions live in `helpers/exceptions.py`:

```python
# helpers/exceptions.py
class NomarrError(Exception):
    """Base exception for all Nomarr errors."""

class LibraryNotFoundError(NomarrError):
    """Raised when a library is not found."""

class ConfigurationError(NomarrError):
    """Raised when configuration is invalid."""
```

---

## What Belongs Here vs Elsewhere

| If it... | Put it in... |
|----------|-------------|
| Does file path manipulation | `helpers/files_helper.py` |
| Formats time/timestamps | `helpers/time_helper.py` |
| Is a cross-layer DTO | `helpers/dto/<domain>.py` |
| Is a domain exception | `helpers/exceptions.py` |
| Does tag parsing logic | `components/tagging/` (not helper) |
| Does DB queries | `persistence/` (not helper) |
| Has any business logic | `components/` (not helper) |
| Constructs/validates library paths | `components/infrastructure/path_comp.py` (not helper) |

---

## Library Path Restriction

Helpers MUST NOT construct, resolve, or validate library paths. All library path construction and validation occurs exclusively in `path_comp` via `LibraryPath` factories.

- Helpers define `LibraryPath` DTO in `helpers/dto/path_dto.py`
- Helpers MUST NOT call `build_library_path_from_input()` or `build_library_path_from_db()`
- Any helper needing a path must receive a validated `LibraryPath` DTO as a parameter
- Raw strings are never acceptable substitutes for `LibraryPath` once constructed

---

## Validation Checklist

Before committing helper code, verify:

- [ ] Does this file import from any `nomarr.*` module? **→ Violation (hard rule)**
- [ ] Does this file read config/env at import time? **→ Violation**
- [ ] Does this contain business logic? **→ Move to components**
- [ ] Does this construct or validate library paths? **→ Violation (use path_comp)**
- [ ] Is this DTO used across layers? **→ Put in `helpers/dto/`**
- [ ] Are functions pure (no hidden state)? **→ Preferred**

---

## Layer Scripts

This skill includes validation scripts in `.github/skills/layer-helpers/scripts/`:

### `lint.py`

Runs all linters on the helpers layer:

```powershell
python .github/skills/layer-helpers/scripts/lint.py
```

Executes: ruff, mypy, vulture, bandit, radon, lint-imports

### `check_naming.py`

Validates helpers naming conventions:

```powershell
python .github/skills/layer-helpers/scripts/check_naming.py
```

Checks:
- Files must end in `_helper.py` or `_dto.py` (exceptions: `exceptions.py`, `dataclasses.py`)
- No stateful classes (classes with `__init__` storing state)
- No `nomarr.*` imports (hard rule)
