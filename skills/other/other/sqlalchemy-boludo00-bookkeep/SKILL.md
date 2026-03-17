---
name: sqlalchemy
description: |
  Defines database models, relationships, and ORM queries in SQLAlchemy 2.x for the Bookkeep backend.
  Use when: creating models, defining relationships, writing queries, handling sessions, or managing database operations.
allowed-tools: Read, Edit, Write, Glob, Grep, Bash
---

# SQLAlchemy Skill

Bookkeep uses SQLAlchemy 2.x ORM with declarative base for 14 database tables. The codebase uses synchronous sessions with FastAPI dependency injection. PostgreSQL is the primary database in production; SQLite is supported for development with WAL mode enabled.

## Quick Start

### Define a Model

```python
# backend/app/models.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    hardcover_id = Column(Integer, nullable=True, index=True, unique=True)
    ebook_available = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    requests = relationship("BookRequest", back_populates="book")
    download_tasks = relationship("DownloadTask", back_populates="book", cascade="all, delete-orphan")
```

### Query with Eager Loading

```python
from sqlalchemy.orm import joinedload

# Avoid N+1 - load book and user with request
request = db.query(models.BookRequest).options(
    joinedload(models.BookRequest.book),
    joinedload(models.BookRequest.user)
).filter(models.BookRequest.id == request_id).first()
```

### Session Dependency

```python
# backend/app/routers/books.py
from fastapi import Depends
from app import database, models

@router.get("/{book_id}")
def get_book(book_id: int, db: Session = Depends(database.get_db)):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book
```

## Key Concepts

| Concept | Usage | Example |
|---------|-------|---------|
| Base | Declarative base class | `from app.database import Base` |
| Session | Request-scoped via `get_db` | `db: Session = Depends(database.get_db)` |
| Relationship | Bidirectional with `back_populates` | `relationship("Book", back_populates="requests")` |
| Index | Add `index=True` for frequent queries | `hardcover_id = Column(Integer, index=True)` |
| Cascade | Delete related records | `cascade="all, delete-orphan"` |

## Common Patterns

### Upsert Pattern (Check-then-Create)

**When:** Creating records that may already exist by unique constraint.

```python
# backend/app/routers/books.py:148-163
if book_dict.get("hardcover_id"):
    existing = db.query(models.Book).filter(
        models.Book.hardcover_id == book_dict["hardcover_id"]
    ).first()
    if existing:
        for key, value in book_dict.items():
            setattr(existing, key, value)
        db.commit()
        db.refresh(existing)
        return existing

# Create new if not found
db_book = models.Book(**book_dict)
db.add(db_book)
db.commit()
```

### Filter with Multiple Conditions

```python
# Active download tasks for a specific book
tasks = db.query(DownloadTask).filter(
    DownloadTask.book_id == book_id,
    DownloadTask.state.in_(['queued', 'downloading', 'complete'])
).all()
```

## See Also

- [patterns](references/patterns.md) - Query patterns, relationships, error handling
- [workflows](references/workflows.md) - Migrations, testing, background jobs

## Related Skills

- See the **fastapi** skill for API route integration with database sessions
- See the **alembic** skill for database migrations
- See the **postgresql** skill for production database configuration
- See the **pytest** skill for testing database operations