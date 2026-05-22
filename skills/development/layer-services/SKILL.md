---
name: layer-services
description: Use when creating or modifying code in nomarr/services/. Services own runtime wiring, long-lived resources (DB, queues, workers), and call workflows. No complex business logic here.
---

# Services Layer

**Purpose:** Own runtime wiring and long-lived resources (config, DB, queues, workers) and expose a clean API for interfaces.

Services are:
- **Dependency coordinators** (wire config, DB, ML backends, queues, workers)
- **Thin orchestrators** (call workflows, aggregate results)
- **DTO providers** (shape data for interfaces)

**No complex business logic lives here.** That belongs in workflows.

---

## File and Package Naming

### Single-File Services

For simple services, use a single file ending in `_svc.py`:

```
nomarr/services/domain/processing_svc.py  → ProcessingService
nomarr/services/domain/analytics_svc.py   → AnalyticsService
```

### Service Packages

For complex services with multiple concerns, use a **package** (folder) ending in `_svc`:

```
nomarr/services/domain/library_svc/
├── __init__.py      # Exports LibraryService
├── admin.py         # LibraryAdminMixin
├── scan.py          # LibraryScanMixin  
├── query.py         # LibraryQueryMixin
├── files.py         # LibraryFilesMixin
└── config.py        # LibraryServiceConfig dataclass
```

**Rules for service packages:**
- Package folder must end in `_svc`
- Internal files do NOT need `_svc.py` suffix
- The `__init__.py` exports the composed `<Domain>Service` class
- Internal classes (mixins, config) don't follow `<Domain>Service` pattern

### Infrastructure Packages

Some folders in `services/infrastructure/` are support packages, not services:

```
nomarr/services/infrastructure/workers/
├── __init__.py
└── discovery_worker.py       # DiscoveryWorker(Process) - runner process
```

These are exempt from `_svc.py` naming since they're not services themselves.

---

## Worker Processes (Runners)

`services/infrastructure/workers/` contains **runner processes** — `multiprocessing.Process` subclasses that execute work in separate subprocesses.

**Why they live here:**
- Spawned and managed by `WorkerSystemService` (co-location with their manager)
- Not components (they call workflows, which components cannot do)
- Not workflows (they contain the execution loop, not just orchestration)
- They are **internal entrypoints**, similar to CLI or API routes

**Architectural exemptions for workers:**

| Normal Service Rule | Worker Exemption |
|---------------------|------------------|
| Services are thin orchestrators | Workers contain execution loops |
| Services call workflows, not components directly | Workers may call both |
| Files must end in `_svc.py` | Worker files end in `_worker.py` |
| Classes must end in `Service` | Worker classes end in `Worker` |

**Rationale:** The subprocess boundary requires self-contained, picklable process classes. Fragmenting them to "follow the rules" would increase complexity without benefit. The architecture rules exist to improve maintainability and code reuse — workers don't need reuse, they need reliability.

**Worker file naming:**
- `*_worker.py` — Process subclass definitions
- Classes should be named `<Domain>Worker` (e.g., `DiscoveryWorker`)

---

## Allowed Imports

```python
# ✅ Allowed
from nomarr.workflows import scan_library_workflow, process_file_workflow
from nomarr.persistence import Database
from nomarr.components.ml import MLBackend
from nomarr.helpers.dto import LibraryDict, ProcessResult
```

## Forbidden Imports

```python
# ❌ NEVER import these in services
from nomarr.interfaces import ...     # Services don't know about HTTP/CLI
from fastapi import HTTPException     # No HTTP semantics
from pydantic import BaseModel        # No Pydantic models
```

---

## Service Method Naming

All public methods use `<verb>_<noun>`:

```python
# ✅ Good
get_library()
list_libraries()
scan_library()
queue_file_for_tagging()
start_processing()
stop_workers()

# ❌ Bad
api_get_library()     # No transport prefixes
get_library_for_admin()  # No audience suffixes
```

### Allowed Verbs

- **Read:** `get_`, `list_`, `exists_`, `count_`, `fetch_`
- **Write:** `create_`, `update_`, `delete_`, `set_`, `rename_`
- **Domain:** `scan_`, `tag_`, `queue_`, `start_`, `stop_`, `sync_`, `import_`, `export_`
- **Boolean:** `enable_`, `disable_`

---

## Complexity Rule: DI + Orchestration Only

A service method should:
1. Collect dependencies
2. Call workflow(s)
3. Return result

**Extract to workflow when you see:**
- Loops
- Branching logic
- Multi-step operations
- Data transformations

```python
# ✅ Good - orchestration only
def process_file(self, file_id: str) -> ProcessResult:
    file_path = self._resolve_file_path(file_id)
    return process_file_workflow(
        db=self.db,
        file_path=file_path,
        models_dir=self.config.models_dir,
    )

# ❌ Bad - business logic in service
def process_file(self, file_id: str) -> ProcessResult:
    file_path = self._resolve_file_path(file_id)
    if self._should_skip(file_path):  # ← Logic belongs in workflow
        return ProcessResult(skipped=True)
    embeddings = compute_embeddings(file_path)  # ← Direct component call
    # ... more logic
```

---

## DTO Requirements

**Public methods returning structured data must return DTOs.**

```python
# ✅ Correct - DTO return
def get_job(self, job_id: int) -> JobDict | None: ...

# ✅ Correct - trivial return (no DTO needed)
def is_enabled(self) -> bool: ...
def get_count(self) -> int: ...

# ❌ Wrong - returning raw dict
def get_job(self, job_id: int) -> dict[str, Any]: ...
```

### DTO Placement

- **Single-service DTOs:** Define in the service file
- **Cross-layer DTOs:** Must live in `helpers/dto/<domain>.py`

---

## Long-Lived Resources

Services own:
- DB connections (`Database`)
- Config snapshots (`ConfigService`)
- ML backends
- Queue handles
- Worker managers

Use constructor injection:

```python
class LibraryService:
    def __init__(self, db: Database, config: ConfigService):
        self.db = db
        self.config = config
```

---

## Validation Checklist

Before committing service code, verify:

- [ ] Does this file import from interfaces? **→ Violation**
- [ ] Does this file import FastAPI, HTTPException, or Pydantic? **→ Violation**
- [ ] Does this method contain loops, branching, or computation? **→ Extract to workflow**
- [ ] Does this method call components directly? **→ Should call workflow instead**
- [ ] Are public methods returning DTOs for structured data? **→ Required**
- [ ] Is the method name `<verb>_<noun>`? **→ Required pattern**

---

## Layer Scripts

This skill includes validation scripts in `.github/skills/layer-services/scripts/`:

### `lint.py`

Runs all linters on the services layer:

```powershell
python .github/skills/layer-services/scripts/lint.py
```

Executes: ruff, mypy, vulture, bandit, radon, lint-imports

### `check_naming.py`

Validates services naming conventions:

```powershell
python .github/skills/layer-services/scripts/check_naming.py
```

Checks:
- Standalone service files must end in `_svc.py`
- Service **packages** (folders ending in `_svc/`) exempt their internal files from suffix rule
- Infrastructure packages (e.g., `workers/`) are exempt from service naming rules
- Classes must end in `Service`
- Methods must follow `<verb>_<noun>` pattern

**Package vs File:**
- Simple service: `processing_svc.py` → `ProcessingService`
- Complex service: `library_svc/` folder with `admin.py`, `scan.py`, `query.py` mixins
