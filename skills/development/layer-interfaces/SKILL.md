---
name: layer-interfaces
description: Use when creating or modifying code in nomarr/interfaces/. Covers API routes, CLI commands, and web handlers. Interfaces are thin adapters that validate inputs, call services, and serialize outputs.
---

# Interfaces Layer

**Purpose:** Expose Nomarr to the outside world via HTTP (FastAPI), CLI (Typer), and web handlers.

Interfaces are **thin adapters**. They do three things:
1. Validate inputs
2. Call **one** service method
3. Serialize outputs

**No business logic lives here.**

---

## Allowed Imports

```python
# ✅ Allowed
from nomarr.services import LibraryService, TaggingService
from nomarr.helpers.dto import LibraryDict, FileDict
from nomarr.interfaces.api.types import LibraryResponse  # Pydantic models
```

## Forbidden Imports

```python
# ❌ NEVER import these in interfaces
from nomarr.workflows import ...      # Call services, not workflows
from nomarr.components import ...     # Call services, not components
from nomarr.persistence import ...    # No direct DB access
```

---

## The One Service Call Rule

Each route handler should call **exactly one** service method.

```python
# ✅ Good - one service call
@router.get("/library/{library_id}")
def get_library(library_id: str, library_service: LibraryService = Depends(...)) -> LibraryResponse:
    library = library_service.get_library(library_id)
    return LibraryResponse.from_dto(library)

# ❌ Bad - multiple service calls
@router.post("/process/{library_id}")
def process(library_id: str, library_service: LibraryService = Depends(...), tagging_service: TaggingService = Depends(...)):
    library = library_service.get_library(library_id)
    tagging_service.tag_library(library.key)  # ← Extract to service method
    return {"status": "ok"}
```

**If you need multiple service calls:** Extract a service method that orchestrates them.

---

## Data Flow

### Request Flow
```
JSON → Pydantic Request Model → .to_dto() → Service (DTO)
```

### Response Flow
```
Service (DTO) → .from_dto() → Pydantic Response Model → JSON
```

Pydantic models live **only** in interfaces. Never let them leak into services.

---

## Authentication Rules

**MANDATORY: All API endpoints require authentication except login.**

### Web API (`/api/web/*`)
- Uses `verify_session` for session token authentication
- All routes MUST include `dependencies=[Depends(verify_session)]` or `_session: dict = Depends(verify_session)` as a parameter
- **Exception:** `/api/web/auth/login` is the only unauthenticated endpoint

### v1 API (`/api/v1/*`)
- Uses `verify_key` for API key authentication
- All routes MUST include `dependencies=[Depends(verify_key)]`
- **Exception:** `/api/v1/public/*` is intentionally public (version info)

### API Consumer Separation — DO NOT MIX

| Router | Auth Method | Consumer | Frontend Calls? |
|--------|-------------|----------|-----------------|
| `/api/web/*` | Session token (`verify_session`) | Web frontend | **YES** |
| `/api/v1/*` | API key (`verify_key`) | External tools (Navidrome, scripts) | **NEVER** |

**The web frontend MUST ONLY call `/api/web/*` endpoints.**

The v1 API uses API key authentication. The web frontend uses session authentication. These are incompatible — the frontend cannot authenticate to v1 endpoints.

If functionality exists in v1 but the frontend needs it, create a parallel route under web API.

---

## Error Handling

- HTTP routes: Raise `HTTPException`
- CLI commands: Raise `typer.Exit(1)`
- Let services/workflows raise domain exceptions, catch them here

```python
@router.get("/file/{file_key}")
def get_file(file_key: str, library_service: LibraryService = Depends(...)) -> FileResponse:
    file = library_service.get_file(file_key)
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse.from_dto(file)
```

---

## Validation Checklist

Before committing interface code, verify:

- [ ] Does this file import from workflows, components, or persistence? **→ Violation**
- [ ] Does this route call more than one service method? **→ Extract to service**
- [ ] Does this route contain business logic (loops, branching, computation)? **→ Move to service**
- [ ] Are Pydantic models staying in this layer only? **→ Services return DTOs**
- [ ] Is the DTO-to-Pydantic conversion explicit? **→ Use `.from_dto()`**
- [ ] Does this route have authentication? **→ Add `verify_session` (web) or `verify_key` (v1)**
- [ ] Is the frontend calling `/api/v1/*`? **→ Create web API route instead**

---

## Layer Scripts

This skill includes validation scripts in `.github/skills/layer-interfaces/scripts/`:

### `lint.py`

Runs all linters on the interfaces layer:

```powershell
python .github/skills/layer-interfaces/scripts/lint.py
```

Executes: ruff, mypy, vulture, bandit, radon, lint-imports

### `check_naming.py`

Validates interfaces naming conventions:

```powershell
python .github/skills/layer-interfaces/scripts/check_naming.py
```

Checks:
- Files must end in `_if.py`
- Route handlers should be thin (validate, call service, serialize)
