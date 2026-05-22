---
name: layer-persistence
description: Use when creating or modifying code in nomarr/persistence/. Persistence handles database and queue access. Never stores business logic.
---

# Persistence Layer

**Purpose:** Own all database and queue access. Provide a clean data access API for higher layers.

Persistence is the **data access layer**:
- `Database` class owns the connection
- `*Operations` classes own SQL for specific tables
- External code accesses via `db.queue.enqueue()`, `db.tags.get_track_tags()`

---

## Directory Structure

```
persistence/
├── db.py                   # Database class (connection owner)
├── arango_client.py        # ArangoDB client wrapper
├── database/               # *_aql.py modules (AQL queries)
│   ├── file_tags_aql.py    # Tag query operations
│   ├── library_files_aql.py # Library file operations
│   ├── worker_claims_aql.py # Worker claim operations
│   └── ...
└── __init__.py
```

---

## Allowed Imports

```python
# ✅ Allowed
from nomarr.helpers.dto import FileDict, LibraryDict
from nomarr.helpers.time_helper import now_ms
```

## Forbidden Imports

```python
# ❌ NEVER import these in persistence
from nomarr.services import ...      # No services
from nomarr.workflows import ...     # No workflows
from nomarr.components import ...    # No components
from nomarr.interfaces import ...    # No interfaces
```

---

## Database Access Pattern

External code **never** imports from `persistence/database/` directly:

```python
# ✅ Correct - access via Database instance
def some_workflow(db: Database):
    files = db.library_files.get_pending_files(library_key)
    tags = db.tags.get_song_tags(file_id)

# ❌ Wrong - direct import
from nomarr.persistence.database.library_files_aql import LibraryFilesAQL
```

---

## ArangoDB ID Fields

**Never rename `_id` or `_key`.**

These are ArangoDB-native identifiers:
- `_key`: Document key (unique within collection)
- `_id`: Full document ID (`collection/_key`)

```python
# ✅ Correct
{"_key": "abc123", "_id": "tracks/abc123", "title": "..."}

# ❌ Wrong - renaming to generic names
{"id": "abc123", "uuid": "abc123"}  # DON'T DO THIS
```

---

## Operations Class Pattern

Each `*AQL` class owns all queries for a related set of collections:

```python
class LibraryFilesAQL:
    def __init__(self, arango: ArangoClient):
        self._arango = arango
    
    def get_pending_files(self, library_key: str, limit: int = 100) -> list[FileDict]:
        """Get pending files for processing."""
        ...
    
    def mark_discovered(self, file_key: str, discovered_at: int) -> None:
        """Mark file as discovered."""
        ...
    
    def update_status(self, file_key: str, status: str) -> None:
        """Update file processing status."""
        ...
```

---

## No Business Logic

Persistence **only** performs data access. No business decisions:

```python
# ✅ Correct - pure data access
def get_pending_files(self, library_key: str, limit: int = 100) -> list[FileDict]:
    return self._arango.execute_query(
        "FOR file IN library_files FILTER file.library_key == @lib AND file.status == 'pending' LIMIT @limit RETURN file",
        bind_vars={"lib": library_key, "limit": limit},
    )

# ❌ Wrong - business logic in persistence
def get_files_to_process(self, library_key: str) -> list[FileDict]:
    files = self.get_pending_files(library_key)
    # ❌ Business logic - this belongs in a workflow
    if len(files) > 10 and self._is_overloaded():
        return files[:5]
    return files
```

---

## Health Data vs Business Decisions

Persistence **stores and retrieves** health data. It does **not** make liveness decisions:

```python
# ✅ Correct - persistence reports facts
def get_last_heartbeat(self, component_id: str) -> int | None:
    """Return timestamp of last heartbeat, or None if never seen."""
    ...

# ❌ Wrong - persistence making decisions
def is_component_healthy(self, component_id: str) -> bool:
    """Check if component is healthy."""
    # This logic belongs in a service or component, not persistence
    heartbeat = self.get_last_heartbeat(component_id)
    return heartbeat is not None and (now_ms() - heartbeat) < 30000
```

---

## Validation Checklist

Before committing persistence code, verify:

- [ ] Does this file import from services, workflows, components, or interfaces? **→ Violation**
- [ ] Does this code make business decisions? **→ Move to workflow/component**
- [ ] Are `_id` and `_key` preserved as-is? **→ Required**
- [ ] Is external code importing from `database/*` directly? **→ Access via `Database`**
- [ ] Is health/liveness logic here instead of in services? **→ Move to service**

---

## Layer Scripts

This skill includes validation scripts in `.github/skills/layer-persistence/scripts/`:

### `lint.py`

Runs all linters on the persistence layer:

```powershell
python .github/skills/layer-persistence/scripts/lint.py
```

Executes: ruff, mypy, vulture, bandit, radon, lint-imports

### `check_naming.py`

Validates persistence naming conventions:

```powershell
python .github/skills/layer-persistence/scripts/check_naming.py
```

Checks:
- Database module files must end in `_aql.py`
- Classes must end in `Operations` (e.g., `LibraryFilesOperations`)
