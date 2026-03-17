---
name: postgres-schema-design
description: PostgreSQL schema design with SQLModel. Use when designing database schemas, creating ERDs, defining models, planning migrations, or reviewing table structures. Triggers on tasks involving database tables, relationships, indexes, or data modeling for PostgreSQL.
---

# PostgreSQL Schema Design (SQLModel)

## Quick Start

```python
import uuid
from datetime import datetime
from sqlmodel import Field, Relationship, SQLModel

class TimestampMixin(SQLModel):
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class User(TimestampMixin, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    email: str = Field(unique=True, index=True)
    name: str = Field(index=True)

class Post(TimestampMixin, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(index=True)
    author_id: uuid.UUID = Field(foreign_key="user.id", index=True)
    author: User | None = Relationship(back_populates="posts")
```

## Decision Guide

### Primary Key: UUID vs Integer

| Use UUID | Use Integer |
|----------|-------------|
| Distributed systems | Single database |
| Hide record count | Need ordering by ID |
| Client-generated IDs | Simpler debugging |
| API exposure | Smaller storage |

```python
# UUID (recommended default)
id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

# Integer auto-increment
id: int | None = Field(default=None, primary_key=True)
```

### Table Names: Singular

SQLModel converts `UserAccount` → `useraccount`. Override if needed:

```python
class UserAccount(SQLModel, table=True):
    __tablename__ = "user_account"
```

### Always Index Foreign Keys

PostgreSQL does NOT auto-index FKs:

```python
# WRONG - no index on FK
author_id: uuid.UUID = Field(foreign_key="user.id")

# CORRECT - indexed FK
author_id: uuid.UUID = Field(foreign_key="user.id", index=True)
```

## Relationship Patterns

### One-to-Many
```python
class Team(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    members: list["User"] = Relationship(back_populates="team")

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    team_id: int | None = Field(default=None, foreign_key="team.id", index=True)
    team: Team | None = Relationship(back_populates="members")
```

### Many-to-Many
```python
class UserRoleLink(SQLModel, table=True):
    user_id: uuid.UUID = Field(foreign_key="user.id", primary_key=True)
    role_id: uuid.UUID = Field(foreign_key="role.id", primary_key=True)

class User(SQLModel, table=True):
    roles: list["Role"] = Relationship(back_populates="users", link_model=UserRoleLink)

class Role(SQLModel, table=True):
    users: list[User] = Relationship(back_populates="roles", link_model=UserRoleLink)
```

### Self-Referential (Tree)
```python
class Category(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    parent_id: uuid.UUID | None = Field(default=None, foreign_key="category.id", index=True)
    parent: "Category | None" = Relationship(
        back_populates="children",
        sa_relationship_kwargs={"remote_side": "Category.id"}
    )
    children: list["Category"] = Relationship(back_populates="parent")
```

## PostgreSQL-Specific Features

### JSONB Column
```python
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSONB

class User(SQLModel, table=True):
    metadata: dict = Field(default={}, sa_column=Column(JSONB))
```

### Composite/Partial Index
```python
from sqlalchemy import Index, text

class User(SQLModel, table=True):
    __table_args__ = (
        Index('idx_user_tenant_email', 'tenant_id', 'email', unique=True),
        Index('idx_user_active', 'id', postgresql_where=text('deleted_at IS NULL')),
    )
```

### Check Constraint
```python
class Order(SQLModel, table=True):
    __table_args__ = (
        CheckConstraint("status IN ('pending', 'shipped', 'delivered')"),
    )
```

## Resources

| Need | Reference |
|------|-----------|
| ERD creation | [assets/erd-template.md](assets/erd-template.md) |
| Migration SQL | [assets/migration-template.sql](assets/migration-template.sql) |
| Pre-deploy checklist | [assets/schema-checklist.md](assets/schema-checklist.md) |
| Naming rules | [references/naming-conventions.md](references/naming-conventions.md) |
| Normalization (1NF-3NF) | [references/normalization.md](references/normalization.md) |
| Index strategies | [references/index-guidelines.md](references/index-guidelines.md) |
| Common patterns (RBAC, audit, soft-delete, multi-tenant) | [references/common-patterns.md](references/common-patterns.md) |

### Scripts

Generate SQLModel boilerplate:
```bash
python scripts/generate_models.py --example --output models.py
```

## Checklist (Critical Items)

- [ ] Every table has a primary key
- [ ] All foreign keys are indexed
- [ ] `created_at`/`updated_at` on mutable tables
- [ ] Unique constraints where business rules require
- [ ] No sensitive data in plain text
- [ ] Soft delete uses partial index for active records
