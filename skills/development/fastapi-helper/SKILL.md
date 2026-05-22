---
name: fastapi-helper
description: |
  FastAPI development assistant for building modern Python web APIs. Provides guidance on routing, request/response handling, dependency injection, authentication, middleware, WebSockets, testing, and Pydantic models. Use when: (1) Creating FastAPI applications or endpoints, (2) Implementing CRUD operations, (3) Setting up authentication/authorization, (4) Working with request parameters (path, query, body, headers, cookies, forms, files), (5) Configuring middleware or CORS, (6) Implementing WebSocket connections, (7) Writing tests for FastAPI apps, (8) Defining Pydantic models for validation.
---

# FastAPI Helper

Build modern, high-performance Python APIs with FastAPI.

## Quick Start

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}
```

Run: `uvicorn main:app --reload`

## Core Concepts

### Route Decorators

| Decorator | HTTP Method |
|-----------|-------------|
| `@app.get()` | GET |
| `@app.post()` | POST |
| `@app.put()` | PUT |
| `@app.delete()` | DELETE |
| `@app.patch()` | PATCH |

### Parameter Functions

| Function | Source |
|----------|--------|
| `Path()` | URL path `/items/{id}` |
| `Query()` | Query string `?q=foo` |
| `Body()` | JSON body |
| `Header()` | HTTP headers |
| `Cookie()` | Cookies |
| `Form()` | Form data |
| `File()` / `UploadFile` | File uploads |

### Dependency Injection

```python
from fastapi import Depends

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/items/")
async def read_items(db: Session = Depends(get_db)):
    return db.query(Item).all()
```

### Common Imports

```python
from fastapi import (
    FastAPI, APIRouter, Depends, HTTPException, status,
    Request, Response, BackgroundTasks, WebSocket,
    Path, Query, Body, Header, Cookie, Form, File, UploadFile
)
from fastapi.responses import JSONResponse, HTMLResponse, FileResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, EmailStr
```

## Reference Documentation

Load these based on task:

| Task | Reference File |
|------|----------------|
| Routes, APIRouter, decorators | [references/routing.md](references/routing.md) |
| Path, Query, Body, Form, File params | [references/parameters.md](references/parameters.md) |
| Response types, status codes, headers | [references/responses.md](references/responses.md) |
| Depends, Security, OAuth2 | [references/dependencies.md](references/dependencies.md) |
| Middleware, CORS, lifespan, BackgroundTasks | [references/middleware-events.md](references/middleware-events.md) |
| WebSocket connections | [references/websockets.md](references/websockets.md) |
| HTTPException, error handlers | [references/exceptions.md](references/exceptions.md) |
| Pydantic models, validation | [references/pydantic-models.md](references/pydantic-models.md) |
| TestClient, pytest fixtures | [references/testing.md](references/testing.md) |

## Common Patterns

### CRUD Endpoint Structure

```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

router = APIRouter(prefix="/items", tags=["items"])

@router.get("/", response_model=list[ItemOut])
async def list_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Item).offset(skip).limit(limit).all()

@router.get("/{item_id}", response_model=ItemOut)
async def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.post("/", response_model=ItemOut, status_code=status.HTTP_201_CREATED)
async def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    db_item = Item(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.put("/{item_id}", response_model=ItemOut)
async def update_item(item_id: int, item: ItemUpdate, db: Session = Depends(get_db)):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    for key, value in item.model_dump(exclude_unset=True).items():
        setattr(db_item, key, value)
    db.commit()
    return db_item

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(db_item)
    db.commit()
```

### CORS Setup

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### JWT Authentication Pattern

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
```
