---
name: layer-components
description: Use when creating or modifying code in nomarr/components/. Components contain heavy domain logic (ML, analytics, tagging). Only ml/backend_essentia.py may import Essentia.
---

# Components Layer

**Purpose:** Contain heavy, domain-specific logic (analytics, tagging, ML, etc.).

Components are the **workhorses** that do the real computational work:
- ML inference and embeddings
- Tag aggregation and resolution
- Statistical analysis
- Complex data transformations

**Rule:** Heavy business logic lives here. Wiring lives in services. Control flow lives in workflows.

---

## Directory Structure

```
components/
├── analytics/          # Tag statistics, co-occurrence
├── ml/                 # ML inference, embeddings, calibration
│   └── ml_backend_essentia_comp.py  # ONLY file that imports Essentia
├── tagging/            # Tag parsing, writing, aggregation
├── queue/              # Queue operations
├── library/            # Library file operations
├── metadata/           # Metadata extraction
├── platform/           # GPU, bootstrap
└── workers/            # Worker crash handling, job recovery
```

---

## Allowed Imports

```python
# ✅ Allowed
from nomarr.persistence import Database
from nomarr.helpers.dto import ProcessFileResult
from nomarr.components.ml.model_loading import load_model  # Cross-component OK
from nomarr.helpers.files_helper import discover_audio_files
```

## Forbidden Imports

```python
# ❌ NEVER import these in components
from nomarr.services import ...      # No services
from nomarr.workflows import ...     # No workflows
from nomarr.interfaces import ...    # No interfaces
from pydantic import BaseModel       # No Pydantic

# ❌ ESSENTIA ONLY IN backend_essentia.py
import essentia_tensorflow  # Only in ml_backend_essentia_comp.py
```

---

## Essentia Isolation Rule

**Only `nomarr/components/ml/ml_backend_essentia_comp.py` may import Essentia.**

All other ML code calls functions in that file:

```python
# In ml_backend_essentia_comp.py:
try:
    import essentia_tensorflow as essentia_tf
except ImportError:
    essentia_tf = None

def compute_embeddings_essentia(file_path: str, ...) -> np.ndarray:
    if essentia_tf is None:
        raise RuntimeError("Essentia not installed")
    # ... use essentia_tf
```

---

## LibraryPath Authority

**`path_comp` is the sole authority for `LibraryPath` construction.**

All raw user paths and DB paths must flow through:
- `build_library_path_from_input()` — for API/CLI/user-provided paths
- `build_library_path_from_db()` — for paths retrieved from database

Components are responsible for:
- Calling factory functions before any filesystem access
- Checking `path.is_valid()` before proceeding
- Never accepting raw path strings where `LibraryPath` exists

Raw strings are never acceptable substitutes for `LibraryPath` once constructed. Deviations are architectural violations.

---

## Function Style

Components prefer **stateless, pure functions** over classes:

```python
# ✅ Good - stateless function
def compute_tag_statistics(db: Database, library_id: int) -> TagStats:
    rows = _query_tag_data(db, library_id)
    stats = _aggregate_tag_stats(rows)
    return TagStats(stats)

# ❌ Avoid - stateful class (unless truly needed)
class TagStatsComputer:
    def __init__(self, db: Database):
        self.db = db  # Unnecessary state
```

---

## Naming Conventions

- **Module:** `snake_case_comp.py` (e.g., `analytics_comp.py`, `ml_embed_comp.py`)
- **Public functions:** `compute_embeddings`, `aggregate_mood_tags`
- **Private helpers:** `_load_model`, `_format_tag_stats`

---

## Complexity & Private Helpers

Components are where **large, complex functions are acceptable** if well-structured.

Use `_private` helpers to keep public functions readable:

```python
# Before - too large
def compute_tag_statistics(db: Database, library_id: int) -> TagStats:
    # 40 lines of querying
    # 40 lines of aggregation
    # 40 lines of formatting
    ...

# After - split into phases
def compute_tag_statistics(db: Database, library_id: int) -> TagStats:
    rows = _query_tag_data(db, library_id)
    stats = _aggregate_tag_stats(rows)
    formatted = _format_tag_stats(stats)
    return TagStats(formatted)

def _query_tag_data(db: Database, library_id: int) -> list[dict]: ...
def _aggregate_tag_stats(rows: list[dict]) -> dict[str, int]: ...
def _format_tag_stats(stats: dict[str, int]) -> dict[str, Any]: ...
```

---

## Example: Worker Crash Handling

```python
def should_restart_worker(restart_count: int, last_restart_ms: int) -> RestartDecision:
    """
    Decide whether to restart a crashed worker or mark it as failed.
    
    Uses two-tier limits:
    - Rapid: 5 restarts in 5 minutes (catches OOM loops)
    - Lifetime: 20 total restarts (catches slow thrashing)
    """
    current_time_ms = now_ms()
    
    if restart_count >= 5 and (current_time_ms - last_restart_ms) < 300_000:
        return RestartDecision(action="mark_failed", reason="Rapid restart limit exceeded")
    
    if restart_count >= 20:
        return RestartDecision(action="mark_failed", reason="Lifetime restart limit exceeded")
    
    backoff = calculate_backoff(restart_count)
    return RestartDecision(action="restart", backoff_seconds=backoff)
```

---

## Validation Checklist

Before committing component code, verify:

- [ ] Does this file import from services, workflows, or interfaces? **→ Violation**
- [ ] Does this file import Essentia directly (and isn't `ml_backend_essentia_comp.py`)? **→ Violation**
- [ ] Does this accept raw path strings where `LibraryPath` should be used? **→ Violation**
- [ ] Is this doing orchestration instead of computation? **→ Should be a workflow**
- [ ] Are heavy functions split into `_private` helpers? **→ Recommended**
- [ ] Does the module name end in `_comp.py`? **→ Convention**

---

## Layer Scripts

This skill includes validation scripts in `.github/skills/layer-components/scripts/`:

### `lint.py`

Runs all linters on the components layer:

```powershell
python .github/skills/layer-components/scripts/lint.py
```

Executes: ruff, mypy, vulture, bandit, radon, lint-imports

### `check_naming.py`

Validates components naming conventions:

```powershell
python .github/skills/layer-components/scripts/check_naming.py
```

Checks:
- Files must end in `_comp.py`
- Essentia imports only allowed in `ml_backend_essentia_comp.py`
