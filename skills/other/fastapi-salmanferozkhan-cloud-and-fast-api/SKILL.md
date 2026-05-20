---
name: fastapi
description: Expert guidance for building REST APIs with FastAPI framework in Python. Use when (1) creating new FastAPI projects from scratch, (2) implementing API endpoints with routing, (3) working with Pydantic models for validation, (4) setting up dependency injection, (5) implementing authentication (OAuth2, JWT, API keys), (6) integrating databases (SQLAlchemy sync/async), (7) writing tests for FastAPI apps, (8) deploying FastAPI to production (Docker, Gunicorn), or (9) implementing advanced features like WebSockets, middleware, background tasks.
---

# FastAPI Development Guide

Build REST APIs with FastAPI - from Hello World to production.

## Quick Start

### Minimal App
```python
from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World"}
```
Run: `fastapi dev main.py` → Visit `http://127.0.0.1:8000/docs`

### New Project Setup
Copy starter template from `assets/starter-project/` or:
```bash
pip install "fastapi[standard]"
```

## Core Concepts

| Concept | Description |
|---------|-------------|
| Path params | `@app.get("/users/{id}")` → `def get(id: int)` |
| Query params | `def list(skip: int = 0, limit: int = 10)` |
| Request body | Use Pydantic models: `def create(item: Item)` |
| Dependencies | `def route(db = Depends(get_db))` |
| Response model | `@app.post("/", response_model=ItemOut)` |

## Reference Files

Load these based on the task at hand:

| Topic | File | When to Use |
|-------|------|-------------|
| **Basics** | [basics.md](references/basics.md) | Path/query params, request bodies, forms, files, status codes |
| **Models** | [models.md](references/models.md) | Pydantic schemas, validation, nested models, serialization |
| **Dependencies** | [dependencies.md](references/dependencies.md) | DI patterns, class-based deps, global deps, Annotated |
| **Auth** | [auth.md](references/auth.md) | JWT, OAuth2, API keys, RBAC, CORS, security headers |
| **Database** | [database.md](references/database.md) | SQLAlchemy sync/async, Alembic migrations, repository pattern |
| **Testing** | [testing.md](references/testing.md) | TestClient, pytest, fixtures, mocking, coverage |
| **Deployment** | [deployment.md](references/deployment.md) | Docker, Gunicorn, Nginx, env config, health checks |
| **Advanced** | [advanced.md](references/advanced.md) | Lifespan, middleware, WebSockets, streaming, caching, GraphQL |

## Project Structure (Professional)

```
project/
├── main.py              # App entry point
├── app/
│   ├── __init__.py
│   ├── config.py        # Settings (pydantic-settings)
│   ├── database.py      # DB connection, session
│   ├── models/          # SQLAlchemy models
│   ├── schemas/         # Pydantic schemas
│   ├── api/
│   │   ├── v1/
│   │   │   ├── endpoints/
│   │   │   └── router.py
│   │   └── deps.py      # Common dependencies
│   ├── services/        # Business logic
│   └── repositories/    # Data access layer
├── tests/
├── alembic/             # Migrations
├── Dockerfile
└── requirements.txt
```

## Common Patterns

### CRUD Endpoint
```python
@router.post("/", response_model=ItemOut, status_code=201)
def create(item: ItemCreate, db: DBDep, user: UserDep):
    return service.create_item(db, item, user.id)

@router.get("/{id}", response_model=ItemOut)
def read(id: int, db: DBDep):
    item = service.get_item(db, id)
    if not item:
        raise HTTPException(404, "Not found")
    return item
```

### Typed Dependencies (Recommended)
```python
from typing import Annotated

DBDep = Annotated[Session, Depends(get_db)]
UserDep = Annotated[User, Depends(get_current_user)]
SettingsDep = Annotated[Settings, Depends(get_settings)]
```

### Error Handling
```python
from fastapi import HTTPException, status

raise HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Item not found"
)
```

## Workflow

1. **Define schemas** (Pydantic) → Input validation + docs
2. **Create endpoints** → Route handlers with type hints
3. **Add dependencies** → DB, auth, settings injection
4. **Write tests** → TestClient + pytest
5. **Deploy** → Docker + Gunicorn/Uvicorn

## Best Practices

- Use `Annotated` for reusable dependency types
- Separate schemas: `Create`, `Update`, `Response`, `InDB`
- Use `response_model` to control output shape
- Keep business logic in services, not routes
- Use async only when needed (DB, external APIs)
- Enable CORS early in development
- Add health check endpoint (`/health`)
- Use pydantic-settings for configuration
