---
name: fastapi
description: "FastAPI Python framework. Covers REST APIs, validation, dependencies, security. Keywords: Pydantic, async, OAuth2, JWT."
version: "0.128.0"
release_date: "2025-12-27"
---

# FastAPI

This skill provides comprehensive guidance for building APIs with FastAPI.

## Quick Navigation

| Topic              | Reference                           |
| ------------------ | ----------------------------------- |
| Getting started    | `references/first-steps.md`         |
| Path parameters    | `references/path-parameters.md`     |
| Query parameters   | `references/query-parameters.md`    |
| Request body       | `references/request-body.md`        |
| Validation         | `references/validation.md`          |
| Body advanced      | `references/body-advanced.md`       |
| Cookies/Headers    | `references/cookies-headers.md`     |
| Pydantic models    | `references/models.md`              |
| Forms/Files        | `references/forms-files.md`         |
| Error handling     | `references/error-handling.md`      |
| Path config        | `references/path-config.md`         |
| Dependencies       | `references/dependencies.md`        |
| Security           | `references/security.md`            |
| Middleware         | `references/middleware.md`          |
| CORS               | `references/cors.md`                |
| Database           | `references/sql-databases.md`       |
| Project structure  | `references/bigger-applications.md` |
| Background tasks   | `references/background-tasks.md`    |
| Metadata/Docs      | `references/metadata-docs.md`       |
| Testing            | `references/testing.md`             |
| Advanced responses | `references/responses-advanced.md`  |
| WebSockets         | `references/websockets.md`          |
| Templates          | `references/templates.md`           |
| Settings/Env vars  | `references/settings.md`            |
| Lifespan events    | `references/lifespan.md`            |
| OpenAPI advanced   | `references/openapi-advanced.md`    |

## When to Use

- Creating REST APIs with Python
- Adding endpoints with automatic validation
- Implementing OAuth2/JWT authentication
- Working with Pydantic models
- Adding dependency injection
- Configuring CORS, middleware
- Uploading files, handling forms
- Testing API endpoints

## Installation

```bash
pip install "fastapi[standard]"  # Full with uvicorn
pip install fastapi              # Minimal
pip install python-multipart     # For forms/files
```

## Quick Start

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}
```

Run: `fastapi dev main.py`

## Core Patterns

### Type-Safe Parameters

```python
from typing import Annotated
from fastapi import Path, Query

@app.get("/items/{item_id}")
def read_item(
    item_id: Annotated[int, Path(ge=1)],
    q: Annotated[str | None, Query(max_length=50)] = None
):
    return {"item_id": item_id, "q": q}
```

### Request Body with Validation

```python
from pydantic import BaseModel, Field

class Item(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    price: float = Field(gt=0)

@app.post("/items/", response_model=Item)
def create_item(item: Item):
    return item
```

### Dependencies

```python
from fastapi import Depends

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/users/")
def list_users(db: Annotated[Session, Depends(get_db)]):
    return db.query(User).all()
```

### Authentication

```python
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    return decode_token(token)

@app.get("/users/me")
def read_me(user: Annotated[User, Depends(get_current_user)]):
    return user
```

## API Documentation

- Swagger UI: `/docs`
- ReDoc: `/redoc`
- OpenAPI: `/openapi.json`

## Best Practices

- Use `Annotated[Type, ...]` for parameters
- Define Pydantic models for request/response
- Use `response_model` for output filtering
- Add `status_code` for proper HTTP codes
- Use `tags` for API organization
- Add `dependencies` at router/app level for auth

## Prohibitions

- ❌ Return raw database models (use response models)
- ❌ Store passwords in plain text (use bcrypt/passlib)
- ❌ Mix `Body` with `Form`/`File` in same endpoint
- ❌ Use sync blocking I/O in async endpoints
- ❌ Skip HTTPException for error handling

## Links

- Docs: https://fastapi.tiangolo.com/
- Tutorial: https://fastapi.tiangolo.com/tutorial/
- Advanced: https://fastapi.tiangolo.com/advanced/
