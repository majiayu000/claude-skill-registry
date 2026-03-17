---
name: postgresql
description: |
  Manages PostgreSQL database schema, migrations, and queries for Bookkeep.
  Use when: configuring database connections, writing migrations, optimizing queries, handling connection pooling, or troubleshooting database issues.
allowed-tools: Read, Edit, Write, Glob, Grep, Bash
---

# PostgreSQL Skill

Bookkeep uses PostgreSQL 16.x as its primary data store with SQLAlchemy 2.x ORM and Alembic migrations. The database layer supports SQLite fallback for development but PostgreSQL is required for production deployments.

## Quick Start

### Connection Setup

```python
# backend/app/database.py - Connection with pooling
engine = create_engine(
    DATABASE_URL,
    pool_size=10,              # Base connections
    max_overflow=20,           # Burst capacity
    pool_timeout=30,           # Wait time for connection
    pool_recycle=1800,         # Recycle every 30 min
    pool_pre_ping=True,        # Validate before use
)
```

### Session Dependency

```python
# FastAPI dependency injection pattern
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Usage in routers
@router.get("/books/{id}")
def get_book(id: int, db: Session = Depends(get_db)):
    return db.query(Book).filter(Book.id == id).first()
```

## Key Concepts

| Concept | Usage | Location |
|---------|-------|----------|
| Connection Pool | 10+20 connections with pre-ping | `backend/app/database.py` |
| Session Lifecycle | Request-scoped via Depends() | All routers |
| Migrations | Alembic with autogenerate | `backend/alembic/versions/` |
| Timestamps | Server-side `func.now()` defaults | `backend/app/models.py` |

## Common Patterns

### Prevent N+1 Queries

```python
from sqlalchemy.orm import joinedload

# Always eager-load relationships for list endpoints
requests = db.query(BookRequest).options(
    joinedload(BookRequest.book),
    joinedload(BookRequest.user)
).order_by(BookRequest.created_at.desc()).all()
```

### Handle Race Conditions on Create

```python
try:
    db.add(book)
    db.flush()  # Catch constraint violations early
    db.commit()
except IntegrityError:
    db.rollback()
    existing = db.query(Book).filter(Book.hardcover_id == id).first()
    return existing
```

## Environment Variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `DATABASE_URL` | required | PostgreSQL connection string |
| `DB_POOL_SIZE` | 10 | Base pool connections |
| `DB_MAX_OVERFLOW` | 20 | Additional connections under load |
| `DB_POOL_TIMEOUT` | 30 | Seconds to wait for connection |
| `DB_POOL_RECYCLE` | 1800 | Seconds before connection recycled |

## See Also

- [patterns](references/patterns.md) - Query patterns, transaction handling
- [workflows](references/workflows.md) - Migrations, debugging, optimization

## Related Skills

- See the **sqlalchemy** skill for ORM models and relationships
- See the **alembic** skill for migration workflows
- See the **fastapi** skill for session dependency injection
- See the **redis** skill for cache invalidation patterns