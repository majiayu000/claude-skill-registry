---
name: sqlmodel
description: Expert guidance for SQLModel - the Python library combining SQLAlchemy and Pydantic for database models. Use when (1) creating database models that work as both SQLAlchemy ORM and Pydantic schemas, (2) building FastAPI apps with database integration, (3) defining model relationships (one-to-many, many-to-many), (4) performing CRUD operations with type safety, (5) setting up async database sessions, (6) integrating with Alembic migrations, (7) handling model inheritance and mixins, or (8) converting between database models and API schemas.
---

# SQLModel Development Guide

SQLModel combines SQLAlchemy and Pydantic into a single library - one model class serves as both ORM model and Pydantic schema.

## Quick Start

### Installation
```bash
pip install sqlmodel
```

### Minimal Example
```python
from sqlmodel import Field, SQLModel, Session, create_engine, select

class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    age: int | None = None

engine = create_engine("sqlite:///database.db")
SQLModel.metadata.create_all(engine)

# Create
with Session(engine) as session:
    hero = Hero(name="Spider-Boy", age=18)
    session.add(hero)
    session.commit()
    session.refresh(hero)

# Read
with Session(engine) as session:
    heroes = session.exec(select(Hero)).all()
```

## Core Concepts

| Concept | Description |
|---------|-------------|
| `table=True` | Makes class a database table (without it, it's just Pydantic) |
| `Field()` | Define column attributes: `primary_key`, `index`, `unique`, `foreign_key` |
| `Session` | Database session for CRUD operations |
| `select()` | Type-safe query builder |
| `Relationship` | Define relationships between models |

## Model Patterns

### Base Model (API Schema Only)
```python
class HeroBase(SQLModel):
    name: str
    age: int | None = None
```

### Table Model (Database)
```python
class Hero(HeroBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
```

### Request/Response Models
```python
class HeroCreate(HeroBase):
    secret_name: str

class HeroPublic(HeroBase):
    id: int

class HeroUpdate(SQLModel):
    name: str | None = None
    age: int | None = None
```

## CRUD Operations

### Create
```python
def create_hero(session: Session, hero: HeroCreate) -> Hero:
    db_hero = Hero.model_validate(hero)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero
```

### Read
```python
def get_hero(session: Session, hero_id: int) -> Hero | None:
    return session.get(Hero, hero_id)

def get_heroes(session: Session, skip: int = 0, limit: int = 100) -> list[Hero]:
    return session.exec(select(Hero).offset(skip).limit(limit)).all()
```

### Update
```python
def update_hero(session: Session, hero_id: int, hero_update: HeroUpdate) -> Hero | None:
    db_hero = session.get(Hero, hero_id)
    if not db_hero:
        return None
    hero_data = hero_update.model_dump(exclude_unset=True)
    db_hero.sqlmodel_update(hero_data)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero
```

### Delete
```python
def delete_hero(session: Session, hero_id: int) -> bool:
    hero = session.get(Hero, hero_id)
    if not hero:
        return False
    session.delete(hero)
    session.commit()
    return True
```

## FastAPI Integration

### Database Setup
```python
from sqlmodel import SQLModel, Session, create_engine

DATABASE_URL = "sqlite:///./database.db"
engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
```

### Dependency Injection
```python
from typing import Annotated
from fastapi import Depends

SessionDep = Annotated[Session, Depends(get_session)]

@app.post("/heroes/", response_model=HeroPublic)
def create_hero(hero: HeroCreate, session: SessionDep):
    db_hero = Hero.model_validate(hero)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero
```

### Lifespan Events
```python
from contextlib import asynccontextmanager
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)
```

## Reference Files

Load these based on the task at hand:

| Topic | File | When to Use |
|-------|------|-------------|
| **Models** | [models.md](references/models.md) | Field options, validators, computed fields, inheritance, mixins |
| **Relationships** | [relationships.md](references/relationships.md) | One-to-many, many-to-many, self-referential, lazy loading |
| **Async** | [async.md](references/async.md) | Async sessions, async engine, background tasks |
| **Migrations** | [migrations.md](references/migrations.md) | Alembic setup, auto-generation, migration patterns |

## Querying

### Basic Queries
```python
# All heroes
heroes = session.exec(select(Hero)).all()

# Single result (first or None)
hero = session.exec(select(Hero).where(Hero.name == "Spider-Boy")).first()

# Get by primary key
hero = session.get(Hero, 1)
```

### Filtering
```python
from sqlmodel import select, or_, and_

# Single condition
select(Hero).where(Hero.age >= 18)

# Multiple conditions (AND)
select(Hero).where(Hero.age >= 18, Hero.name == "Spider-Boy")

# OR conditions
select(Hero).where(or_(Hero.age < 18, Hero.age > 60))

# LIKE/contains
select(Hero).where(Hero.name.contains("Spider"))
```

### Ordering and Pagination
```python
select(Hero).order_by(Hero.name)
select(Hero).order_by(Hero.age.desc())
select(Hero).offset(10).limit(5)
```

## Best Practices

- **Separate table models from API schemas** - Use `table=True` only for actual DB tables
- **Use `model_validate()` for conversion** - Convert between schemas and table models
- **Use `sqlmodel_update()` for partial updates** - Pass `exclude_unset=True` to `model_dump()`
- **Always use `Field()` for constraints** - Primary keys, indexes, foreign keys, defaults
- **Use `Annotated` dependencies** - Clean, reusable session injection
- **Use lifespan for table creation** - Not deprecated `@app.on_event`
- **Index frequently queried columns** - `Field(index=True)`
- **Use `echo=True` during development** - See generated SQL queries

## Common Issues

| Issue | Solution |
|-------|----------|
| Missing `table=True` | Add `table=True` to models that need DB tables |
| Circular imports | Use `TYPE_CHECKING` and string annotations for relationships |
| Session already closed | Ensure session is still open when accessing lazy-loaded relationships |
| Migration not detecting changes | Use `compare_type=True` in Alembic env.py |
