---
name: python
description: |
  Develops Python 3.11+ backend services for Bookkeep using FastAPI, SQLAlchemy, and async patterns.
  Use when: writing routers, models, schemas, background tasks, or database operations in backend/app/
allowed-tools: Read, Edit, Write, Glob, Grep, Bash
---

# Python Skill

This codebase uses Python 3.11+ with FastAPI for async REST APIs, SQLAlchemy 2.x for ORM, and Pydantic for validation. All code lives in `backend/app/`. Use `uv` for package management and `structlog` for logging.

## Quick Start

### Router Pattern

```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas, database
import structlog

logger = structlog.get_logger()
router = APIRouter()

@router.get("/{book_id}", response_model=schemas.BookResponse)
async def get_book(book_id: int, db: Session = Depends(database.get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return book
```

### Async Service Pattern

```python
async def check_availability(book: models.Book, db: Session) -> dict:
    for server in get_servers(db):
        try:
            async with create_client(server) as client:
                result = await client.lookup(book.hardcover_id)
                if result:
                    return {"available": True, "source": server.name}
        except Exception as e:
            logger.warning("availability_check_failed", server_id=server.id, error=str(e))
    return {"available": False}
```

## Key Concepts

| Concept | Usage | Example |
|---------|-------|---------|
| Dependency Injection | Database sessions | `db: Session = Depends(get_db)` |
| Auth dependencies | Current user | `user: models.User = Depends(get_current_user)` |
| Response models | Type validation | `response_model=schemas.BookResponse` |
| ORM mode | Schema config | `from_attributes = True` |

## File Naming

- Files: `snake_case.py` (e.g., `download_settings.py`)
- Classes: `PascalCase` (e.g., `BookRequest`)
- Functions/variables: `snake_case` (e.g., `check_availability`)
- Constants: `SCREAMING_SNAKE` (e.g., `CACHE_TTL`)

## See Also

- [patterns](references/patterns.md) - Async, dependency injection, error handling
- [types](references/types.md) - Pydantic schemas, SQLAlchemy models
- [modules](references/modules.md) - Router structure, services, downloads
- [errors](references/errors.md) - HTTPException patterns, logging

## Related Skills

See the **fastapi** skill for router patterns and OpenAPI integration.
See the **sqlalchemy** skill for ORM queries and relationships.
See the **pytest** skill for testing patterns.