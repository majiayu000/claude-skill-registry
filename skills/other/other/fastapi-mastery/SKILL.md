---
name: fastapi-mastery
description: Comprehensive FastAPI development skill covering REST API creation, routing, request/response handling, validation, authentication, database integration, middleware, and deployment. Use when working with FastAPI projects, building APIs, implementing CRUD operations, setting up authentication/authorization, integrating databases (SQL/NoSQL), adding middleware, handling WebSockets, or deploying FastAPI applications. Triggered by requests involving .py files with FastAPI code, API endpoint creation, Pydantic models, or FastAPI-specific features.
---

# FastAPI Mastery

## Overview

Build production-ready REST APIs with FastAPI using modern Python features, automatic validation, interactive documentation, and asynchronous capabilities.

## Quick Start

**Create a basic FastAPI application:**

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}
```

**Run with:**
```bash
uvicorn main:app --reload
```

**Access interactive docs:** http://localhost:8000/docs

## Skill Structure by Complexity Level

This skill is organized into three progressive levels:

### Beginner (references/01-beginner.md)
Read when working with:
- First FastAPI application setup
- Basic routing and path operations
- Request parameters (path, query, body)
- Pydantic models and validation
- Response models and status codes
- Basic error handling

### Intermediate (references/02-intermediate.md)
Read when implementing:
- Authentication and authorization (JWT, OAuth2)
- Database integration (SQLAlchemy, async databases)
- Dependency injection system
- Middleware and CORS
- Background tasks
- File uploads and downloads

### Advanced (references/03-advanced.md)
Read when building:
- WebSocket connections
- Testing strategies (pytest, TestClient)
- Performance optimization
- Containerization and deployment
- API versioning
- Advanced error handling and logging

## Common Development Workflows

### Building a CRUD API

1. Define Pydantic models for request/response
2. Set up database models (SQLAlchemy)
3. Create path operations (GET, POST, PUT, DELETE)
4. Add validation and error handling
5. Implement authentication if needed
6. Add tests

**See references/01-beginner.md** for basic CRUD patterns, **references/02-intermediate.md** for database integration.

### Adding Authentication

1. Choose authentication method (JWT, OAuth2, API keys)
2. Set up security dependencies
3. Create login endpoint
4. Protect routes with dependencies
5. Handle token refresh if using JWT

**See references/02-intermediate.md** for complete authentication implementation.

### Database Integration

1. Choose database (PostgreSQL, MySQL, MongoDB)
2. Install and configure ORM (SQLAlchemy, Tortoise, Motor)
3. Define database models
4. Set up database connection and session management
5. Create CRUD operations
6. Add migrations (Alembic)

**See references/02-intermediate.md** for database patterns.

## Best Practices

**Type hints:** Always use Python type hints for automatic validation and documentation.

```python
from typing import Optional
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float
    description: Optional[str] = None
```

**Dependency injection:** Use FastAPI's dependency injection for shared logic.

```python
from fastapi import Depends

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Validate token and return user
    return user
```

**Async when beneficial:** Use async for I/O-bound operations (database, external APIs).

```python
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    item = await database.fetch_one(query)
    return item
```

**Response models:** Always define response models for API documentation and validation.

```python
@app.get("/items/{item_id}", response_model=ItemResponse)
async def read_item(item_id: int):
    return item
```

## Reference Guide Selection

**Choose the appropriate reference based on your task:**

- **Creating first API or basic endpoints?** → references/01-beginner.md
- **Adding auth, databases, or middleware?** → references/02-intermediate.md
- **WebSockets, testing, or deployment?** → references/03-advanced.md

All reference files include comprehensive examples and can be read independently.
