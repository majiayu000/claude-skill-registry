---
name: layer-workflows
description: Use when creating or modifying code in nomarr/workflows/. Workflows implement use cases, accept dependencies as parameters, orchestrate components, and return DTOs.
---

# Workflows Layer

**Purpose:** Implement core use cases ("what Nomarr does").

Workflows contain the **story** of how Nomarr performs operations. They are recipes that:
1. Accept dependencies as parameters (DB, config, ML backends)
2. Orchestrate components to perform work
3. Return DTOs

---

## Allowed Imports

```python
# ✅ Allowed
from nomarr.persistence import Database
from nomarr.components.ml import compute_embeddings, run_inference
from nomarr.components.tagging import predictions_to_tags
from nomarr.helpers.dto import ProcessFileResult
```

## Forbidden Imports

```python
# ❌ NEVER import these in workflows
from nomarr.services import ProcessingService  # Workflows don't call services
from nomarr.interfaces import ...              # No interface imports
from pydantic import BaseModel                 # No Pydantic
```

---

## File & Function Naming

- **File:** `verb_object_wf.py` (e.g., `scan_library_direct_wf.py`, `process_file_wf.py`)
- **Function:** `verb_object_workflow(...)` as the primary entrypoint
- **One public workflow per file**
- Everything else is `_private_helper`

---

## Complexity Rule: Clear Sequences

Workflows should read like a **recipe**:

```python
def process_file_workflow(
    db: Database,
    file_path: str,
    models_dir: str,
    namespace: str,
) -> ProcessFileResult:
    # Step 1: Load file
    file_record = load_file_from_db(db, file_path)
    
    # Step 2: Compute embeddings
    embeddings = compute_all_embeddings(file_path, models_dir)
    
    # Step 3: Run inference
    predictions = run_inference_for_heads(embeddings, models_dir)
    
    # Step 4: Convert to tags
    tags = predictions_to_tags(predictions, namespace)
    
    # Step 5: Write tags
    write_tags_to_db(db, file_record.id, tags)
    
    return ProcessFileResult(file=file_path, tags_written=len(tags))
```

**Judge by clarity, not line count.** Many component calls are fine if they form a clear sequence.

---

## Accept All Dependencies as Parameters

Workflows receive everything via parameters—no global config reading:

```python
# ✅ Good - dependencies injected
def process_file_workflow(
    db: Database,
    file_path: str,
    models_dir: str,
) -> ProcessFileResult:
    ...

# ❌ Bad - reading globals
def process_file_workflow(file_path: str) -> ProcessFileResult:
    from nomarr.config import db, models_dir  # NO GLOBALS
    ...
```

---

## When to Extract

### Extract to a component if:
- Workflow is doing non-trivial computation itself
- Complex branching logic embedded in workflow
- Heavy domain math/ML/statistics

### Split into private helpers if:
- Workflow becomes hard to read
- Large, reusable sub-sequences

```python
# Before - hard to read
def complex_workflow(db: Database, ...) -> Result:
    # 50 lines of discovery
    # 50 lines of validation
    # 50 lines of processing

# After - split with private helpers
def complex_workflow(db: Database, ...) -> Result:
    discovered = _discover_and_validate(db, ...)
    processed = _process_files(db, discovered, ...)
    return Result(...)
```

---

## Size Guidelines

- Soft limit: ~300–400 LOC per workflow module
- If multiple exported workflows with different user stories → split files
- Exception: analytics-style modules can group related read-only workflows

---

## Validation Checklist

Before committing workflow code, verify:

- [ ] Does this file import from services or interfaces? **→ Violation**
- [ ] Does this file import Pydantic? **→ Violation**
- [ ] Does this workflow read global config? **→ Accept as parameter instead**
- [ ] Is the workflow doing heavy computation? **→ Extract to component**
- [ ] Does the function return a DTO? **→ Required**
- [ ] Is there one public workflow per file? **→ Required**
- [ ] Does the file name end in `_wf.py`? **→ Convention**

---

## Layer Scripts

This skill includes validation scripts in `.github/skills/layer-workflows/scripts/`:

### `lint.py`

Runs all linters on the workflows layer:

```powershell
python .github/skills/layer-workflows/scripts/lint.py
```

Executes: ruff, mypy, vulture, bandit, radon, lint-imports

### `check_naming.py`

Validates workflows naming conventions:

```powershell
python .github/skills/layer-workflows/scripts/check_naming.py
```

Checks:
- Files must end in `_wf.py`
- Each file must have exactly one `*_workflow` function
- Internal helpers must be `_private`
