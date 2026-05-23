---
name: sqlalchemy
description: Python SQL toolkit and ORM for defining schemas and issuing SQL/ORM queries with explicit transaction control.
version: 2.0
ecosystem: python
license: MIT
generated_with: gpt-5.2
---

## Imports

```python
import sqlalchemy
from sqlalchemy import (
    create_engine,
    text,
    select,
    insert,
    update,
    delete,
    bindparam,
    ForeignKey,
    Integer,
    String,
    Column,
    MetaData,
    Table,
    event,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    Session,
    sessionmaker,
    joinedload,
)
from sqlalchemy.ext.associationproxy import association_proxy
```

## Core Patterns

### Engine + explicit transactions (Core) ✅ Current
```python
from __future__ import annotations

from sqlalchemy import create_engine, text

def main() -> None:
    engine = create_engine("sqlite+pysqlite:///:memory:", future=True)

    with engine.begin() as conn:
        conn.execute(text("CREATE TABLE user_account (id INTEGER PRIMARY KEY, name TEXT NOT NULL)"))
        conn.execute(
            text("INSERT INTO user_account (name) VALUES (:name)"),
            [{"name": "alice"}, {"name": "bob"}],
        )

    with engine.connect() as conn:
        rows = conn.execute(text("SELECT id, name FROM user_account ORDER BY id")).all()
        print(rows)

if __name__ == "__main__":
    main()
```
* Use `engine.begin()` for an explicit transaction boundary (commit on success, rollback on error).
* Use `text()` with bound parameters (e.g., `:name`) instead of string interpolation.

### SQL Expression Language CRUD with bound parameters ✅ Current
```python
from __future__ import annotations

from sqlalchemy import create_engine, Integer, String, bindparam, select, insert, update, delete
from sqlalchemy import MetaData, Table, Column

def main() -> None:
    engine = create_engine("sqlite+pysqlite:///:memory:", future=True)
    metadata = MetaData()

    user_account = Table(
        "user_account",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("name", String, nullable=False),
    )

    metadata.create_all(engine)

    with engine.begin() as conn:
        conn.execute(insert(user_account), [{"name": "alice"}, {"name": "bob"}])

        # UPDATE with bound parameters (safe + cacheable)
        conn.execute(
            update(user_account)
            .where(user_account.c.name == bindparam("old_name"))
            .values(name=bindparam("new_name")),
            {"old_name": "bob", "new_name": "robert"},
        )

        # SELECT
        names = conn.execute(select(user_account.c.id, user_account.c.name).order_by(user_account.c.id)).all()
        print(names)

        # DELETE
        conn.execute(delete(user_account).where(user_account.c.name == "alice"))

    with engine.connect() as conn:
        remaining = conn.execute(select(user_account.c.name).order_by(user_account.c.name)).scalars().all()
        print(remaining)

if __name__ == "__main__":
    main()
```
* Prefer `select()/insert()/update()/delete()` over handwritten SQL when practical.
* Use `bindparam()` for explicit parameter binding in reusable statements.

### Declarative ORM models + relationships ✅ Current
```python
from __future__ import annotations

from typing import List

from sqlalchemy import create_engine, ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)

    addresses: Mapped[List["Address"]] = relationship(back_populates="user", cascade="all, delete-orphan")

class Address(Base):
    __tablename__ = "address"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"), nullable=False)

    user: Mapped[User] = relationship(back_populates="addresses")

def main() -> None:
    engine = create_engine("sqlite+pysqlite:///:memory:", future=True)
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        u = User(name="alice", addresses=[Address(email="alice@example.com")])
        session.add(u)
        session.commit()

    with Session(engine) as session:
        users = session.execute(
            sqlalchemy.select(User).order_by(User.id)  # type: ignore[attr-defined]
        ).scalars().all()
        print([(user.id, user.name, [a.email for a in user.addresses]) for user in users])

if __name__ == "__main__":
    main()
```
* Use `DeclarativeBase`, `Mapped[...]`, and `mapped_column()` for SQLAlchemy 2.0-style typed ORM mappings.
* Model relationships explicitly with `relationship()` and `ForeignKey()`.

### ORM unit-of-work with explicit commit/rollback ✅ Current
```python
from __future__ import annotations

from sqlalchemy import create_engine, select, String
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user_account"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)

def main() -> None:
    engine = create_engine("sqlite+pysqlite:///:memory:", future=True)
    Base.metadata.create_all(engine)

    # Write transaction
    with Session(engine) as session:
        session.add_all([User(name="alice"), User(name="bob")])
        session.commit()

    # Read-only pattern (no commit needed)
    with Session(engine) as session:
        names = session.execute(select(User.name).order_by(User.name)).scalars().all()
        print(names)

if __name__ == "__main__":
    main()
```
* ORM changes are not durable until `Session.commit()` succeeds; structure code around clear unit-of-work boundaries.
* Use `Session(...)` as a context manager to ensure resources are released.

### Eager loading relationships ✅ Current
```python
from __future__ import annotations

from typing import List

from sqlalchemy import create_engine, ForeignKey, String, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship, joinedload

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user_account"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    addresses: Mapped[List["Address"]] = relationship(back_populates="user")

class Address(Base):
    __tablename__ = "address"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"), nullable=False)
    user: Mapped[User] = relationship(back_populates="addresses")

def main() -> None:
    engine = create_engine("sqlite+pysqlite:///:memory:", future=True)
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        session.add(User(name="alice", addresses=[Address(email="alice@example.com")]))
        session.commit()

    # Eager load addresses with JOIN to avoid N+1 queries
    with Session(engine) as session:
        stmt = select(User).options(joinedload(User.addresses)).order_by(User.id)
        users = session.execute(stmt).scalars().unique().all()
        print([(u.name, [a.email for a in u.addresses]) for u in users])

if __name__ == "__main__":
    main()
```
* Use `joinedload()` to eagerly load relationships using a JOIN, avoiding N+1 query problems.
* Call `.unique()` after `.scalars()` when using `joinedload()` to deduplicate results.

### Association proxy for simplified many-to-many access ✅ Current
```python
from __future__ import annotations

from typing import List

from sqlalchemy import create_engine, ForeignKey, String, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship
from sqlalchemy.ext.associationproxy import association_proxy

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user_account"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    
    user_keywords: Mapped[List["UserKeyword"]] = relationship(back_populates="user")
    keywords: Mapped[List[str]] = association_proxy(
        "user_keywords", "keyword", 
        creator=lambda kw: UserKeyword(keyword=kw)
    )

class UserKeyword(Base):
    __tablename__ = "user_keyword"
    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"), primary_key=True)
    keyword: Mapped[str] = mapped_column(String(50), primary_key=True)
    user: Mapped[User] = relationship(back_populates="user_keywords")

def main() -> None:
    engine = create_engine("sqlite+pysqlite:///:memory:", future=True)
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        u = User(name="alice", keywords=["python", "sql"])
        session.add(u)
        session.commit()

    with Session(engine) as session:
        user = session.execute(select(User)).scalars().first()
        print(user.keywords)  # Access keywords directly without going through association table

if __name__ == "__main__":
    main()
```
* Use `association_proxy()` to simplify access to many-to-many relationships by hiding the association table.
* Provide a `creator` function to construct association objects from scalar values.

### Event listening ✅ Current
```python
from __future__ import annotations

from sqlalchemy import create_engine, String, event, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user_account"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)

def after_insert_listener(mapper, connection, target):
    """Called after an INSERT on User"""
    print(f"Inserted user: {target.name}")

# Register event listener
event.listen(User, "after_insert", after_insert_listener)

def main() -> None:
    engine = create_engine("sqlite+pysqlite:///:memory:", future=True)
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        session.add(User(name="alice"))
        session.commit()  # Triggers the after_insert event

if __name__ == "__main__":
    main()
```
* Use `event.listen()` to register event listeners on ORM classes, engine connections, or sessions.
* Common events include `before_insert`, `after_insert`, `before_update`, `after_update`, `before_delete`, `after_delete`.

## Configuration

- **Database URL**: pass to `create_engine()` (sync) as `"dialect+driver://user:pass@host/dbname"`.
  - SQLite in-memory: `"sqlite+pysqlite:///:memory:"`
- **Connection pooling**: configured via `create_engine()` kwargs (e.g., `pool_size`, `max_overflow`, `pool_pre_ping`).
- **Echo / SQL logging**: `create_engine(..., echo=True)` to log SQL emitted by SQLAlchemy.
- **Session configuration**:
  - Create ad-hoc sessions with `Session(engine)`.
  - Or create a factory with `sessionmaker(bind=engine)` for application-wide reuse.
  - Configure session behavior: `autoflush=True` (default), `expire_on_commit=True` (default).
- **Transactions**:
  - Core: prefer `with engine.begin() as conn: ...`
  - ORM: prefer `with Session(engine) as session: ...; session.commit()`
- **Parameter binding**: always use bound parameters (`text("... :name")`, `bindparam("name")`) rather than interpolating literals into SQL strings.
- **Eager loading**: use `joinedload()`, `selectinload()`, or `subqueryload()` to control relationship loading strategy.

## Pitfalls

### Wrong: assuming ORM `add()` persists without `commit()`
```python
from __future__ import annotations

from sqlalchemy import create_engine, String
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user_account"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)

engine = create_engine("sqlite+pysqlite:///:memory:", future=True)
Base.metadata.create_all(engine)

session = Session(engine)
session.add(User(name="alice"))
session.close()  # closes without commit; transaction is rolled back
```

### Right: commit within a clear unit of work
```python
from __future__ import annotations

from sqlalchemy import create_engine, String
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user_account"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)

engine = create_engine("sqlite+pysqlite:///:memory:", future=True)
Base.metadata.create_all(engine)

with Session(engine) as session:
    session.add(User(name="alice"))
    session.commit()
```

### Wrong: SQL injection via string interpolation with `exec_driver_sql()`
```python
from __future__ import annotations

from sqlalchemy import create_engine

engine = create_engine("sqlite+pysqlite:///:memory:", future=True)

name = "alice' OR 1=1 --"
with engine.connect() as conn:
    conn.exec_driver_sql(f"SELECT '{name}'")  # interpolated SQL; unsafe pattern
```

### Right: use `text()` + bound parameters
```python
from __future__ import annotations

from sqlalchemy import create_engine, text

engine = create_engine("sqlite+pysqlite:///:memory:", future=True)

name = "alice' OR 1=1 --"
with engine.connect() as conn:
    value = conn.execute(text("SELECT :name"), {"name": name}).scalar_one()
    print(value)
```

### Wrong: forgetting to wrap Core writes in a transaction
```python
from __future__ import annotations

from sqlalchemy import create_engine, text

engine = create_engine("sqlite+pysqlite:///:memory:", future=True)

with engine.connect() as conn:
    conn.execute(text("CREATE TABLE t (id INTEGER PRIMARY KEY, name TEXT)"))
    conn.execute(text("INSERT INTO t (name) VALUES ('alice')"))
    # no commit; many DBAPIs will roll back when the connection closes
```

### Right: use `engine.begin()` for Core writes
```python
from __future__ import annotations

from sqlalchemy import create_engine, text

engine = create_engine("sqlite+pysqlite:///:memory:", future=True)

with engine.begin() as conn:
    conn.execute(text("CREATE TABLE t (id INTEGER PRIMARY KEY, name TEXT)"))
    conn.execute(text("INSERT INTO t (name) VALUES (:name)"), {"name": "alice"})
```

### Wrong: selecting ORM entities but not using `.scalars()`
```python
from __future__ import annotations

from sqlalchemy import create_engine, select, String
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user_account"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)

engine = create_engine("sqlite+pysqlite:///:memory:", future=True)
Base.metadata.create_all(engine)

with Session(engine) as session:
    session.add_all([User(name="alice"), User(name="bob")])
    session.commit()

with Session(engine) as session:
    rows = session.execute(select(User)).all()
    # rows are Row objects containing User at index 0, not a list[User]
    users = [r for r in rows]
    print(users)
```

### Right: use `.scalars()` to get mapped instances
```python
from __future__ import annotations

from sqlalchemy import create_engine, select, String
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user_account"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)

engine = create_engine("sqlite+pysqlite:///:memory:", future=True)
Base.metadata.create_all(engine)

with Session(engine) as session:
    session.add_all([User(name="alice"), User(name="bob")])
    session.commit()

with Session(engine) as session:
    users = session.execute(select(User).order_by(User.id)).scalars().all()
    print([u.name for u in users])
```

### Wrong: not calling `.unique()` after `.scalars()` with `joinedload()`
```python
from __future__ import annotations

from typing import List

from sqlalchemy import create_engine, ForeignKey, String, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship, joinedload

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user_account"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    addresses: Mapped[List["Address"]] = relationship()

class Address(Base):
    __tablename__ = "address"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"), nullable=False)

engine = create_engine("sqlite+pysqlite:///:memory:", future=True)
Base.metadata.create_all(engine)

with Session(engine) as session:
    session.add(User(name="alice", addresses=[
        Address(email="alice1@example.com"),
        Address(email="alice2@example.com")
    ]))
    session.commit()

with Session(engine) as session:
    stmt = select(User).options(joinedload(User.addresses))
    users = session.execute(stmt).scalars().all()
    # Returns duplicate User objects (one per joined address row)
    print(len(users))  # 2 instead of 1
```

### Right: call `.unique()` to deduplicate after `joinedload()`
```python
from __future__ import annotations

from typing import List

from sqlalchemy import create_engine, ForeignKey, String, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship, joinedload

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user_account"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    addresses: Mapped[List["Address"]] = relationship()

class Address(Base):
    __tablename__ = "address"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"), nullable=False)

engine = create_engine("sqlite+pysqlite:///:memory:", future=True)
Base.metadata.create_all(engine)

with Session(engine) as session:
    session.add(User(name="alice", addresses=[
        Address(email="alice1@example.com"),
        Address(email="alice2@example.com")
    ]))
    session.commit()

with Session(engine) as session:
    stmt = select(User).options(joinedload(User.addresses))
    users = session.execute(stmt).scalars().unique().all()
    print(len(users))  # 1 (deduplicated)
    print(len(users[0].addresses))  # 2
```

## References

- [Homepage](https://www.sqlalchemy.org)
- [Documentation](https://docs.sqlalchemy.org)
- [Changelog](https://docs.sqlalchemy.org/latest/changelog/index.html)
- [Source Code](https://github.com/sqlalchemy/sqlalchemy)
- [Issue Tracker](https://github.com/sqlalchemy/sqlalchemy/issues)
- [Discussions](https://github.com/sqlalchemy/sqlalchemy/discussions)

## Migration from v1.4

- SQLAlchemy 2.0 formalizes "2.0 style" usage that was available in 1.4:
  - Prefer `select()` constructs and `Session.execute(select(...))` over legacy `Query` patterns.
  - Prefer explicit transaction scopes: `engine.begin()` (Core) and `Session(...); commit()` (ORM).
  - Prefer typed ORM mappings: `DeclarativeBase`, `Mapped[...]`, `mapped_column()`.

### Legacy ORM query style ⚠️ Soft Deprecation
* Deprecated since: 1.4 (2.0-style recommended)
* Still works: True (in many configurations), but prefer 2.0 style for new code
* Modern alternative: `Session.execute(select(...)).scalars()`
* Migration guidance: replace `session.query(Model).filter(...)` with `session.execute(select(Model).where(...)).scalars()`

```python
from __future__ import annotations

from sqlalchemy import create_engine, select, String
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user_account"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)

def main() -> None:
    engine = create_engine("sqlite+pysqlite:///:memory:", future=True)
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        session.add_all([User(name="alice"), User(name="bob")])
        session.commit()

    with Session(engine) as session:
        # 2.0 style:
        users = session.execute(select(User).where(User.name == "alice")).scalars().all()
        print([u.name for u in users])

if __name__ == "__main__":
    main()
```

## API Reference

- **sqlalchemy.create_engine(url, \*\*kwargs)** - Create an `Engine`; key kwargs include `echo`, pool options, and dialect/driver URL.
- **sqlalchemy.Engine.connect()** - Acquire a `Connection` for SQL execution (explicit transaction management required for writes).
- **sqlalchemy.Engine.begin()** - Context manager that provides a `Connection` with an explicit transaction (commit/rollback).
- **sqlalchemy.text(sql_text)** - Create a textual SQL statement supporting bound parameters (`:name`).
- **sqlalchemy.select(\*entities)** - Build a SELECT statement from tables/columns/ORM entities.
- **sqlalchemy.insert(table)** - Build an INSERT statement.
- **sqlalchemy.update(table)** - Build an UPDATE statement.
- **sqlalchemy.delete(table)** - Build a DELETE statement.
- **sqlalchemy.bindparam(name)** - Define an explicit bound parameter for SQL constructs.
- **sqlalchemy.Column(\*args, primary_key=False, nullable=True, \*\*kwargs)** - Define a table column (legacy Core API, prefer `mapped_column()` for ORM).
- **sqlalchemy.ForeignKey(column, \*, onupdate=None, ondelete=None, \*\*kwargs)** - Define a foreign key constraint.
- **sqlalchemy.Integer()** - Integer column type.
- **sqlalchemy.String(length=None)** - String/VARCHAR column type.
- **sqlalchemy.MetaData()** - Container object for schema constructs like `Table`.
- **sqlalchemy.Table(name, metadata, \*columns, \*\*kwargs)** - Represent a database table in Core.
- **sqlalchemy.event.listen(target, identifier, fn, \*\*kwargs)** - Register an event listener on a target object.
- **sqlalchemy.orm.Session(bind=None, \*, autoflush=True, expire_on_commit=True, \*\*kwargs)** - ORM session (unit of work / identity map); use `commit()` to persist.
- **sqlalchemy.orm.Session.add(instance)** - Add an object to the session.
- **sqlalchemy.orm.Session.add_all(instances)** - Add multiple objects to the session.
- **sqlalchemy.orm.Session.commit()** - Commit the current transaction.
- **sqlalchemy.orm.Session.execute(statement, params=None, \*\*kwargs)** - Execute a SQL statement and return a `Result`.
- **sqlalchemy.orm.Session.scalars(statement, params=None, \*\*kwargs)** - Execute a statement and return scalar results.
- **sqlalchemy.orm.sessionmaker(bind=engine, \*\*kwargs)** - Factory for creating configured `Session` objects.
- **sqlalchemy.orm.DeclarativeBase** - Base class for declarative ORM mappings (2.0 style).
- **sqlalchemy.orm.Mapped[T]** - Typing annotation used for ORM-mapped attributes.
- **sqlalchemy.orm.mapped_column(\*args, primary_key=False, nullable=None, default=None, \*\*kwargs)** - Declare an ORM-mapped column with typing support.
- **sqlalchemy.orm.relationship(argument=None, \*, cascade=None, backref=None, lazy='select', \*\*kwargs)** - Define ORM relationships between mapped classes.
- **sqlalchemy.orm.joinedload(attr, \*, innerjoin=False)** - Eager load a relationship using a JOIN.
- **sqlalchemy.ext.associationproxy.association_proxy(target_collection, attr, \*\*kwargs)** - Create an association proxy for simplified many-to-many access.
- **sqlalchemy.orm.Query** ⚠️ - Legacy query API (soft deprecation; prefer `select()` for 2.0 style).

## Current Library State

SQLAlchemy 2.0 is a mature, production-ready ORM and SQL toolkit following these core principles:

### Philosophy
- **Transactions as the norm**: Nothing persists until `commit()` is called explicitly.
- **Bound parameters everywhere**: Never render literal values in SQL; use bound parameters to prevent SQL injection and enable query plan caching.
- **Choose the right tool**: Use Core for SQL operations that don't need object mapping; use ORM when you need the data mapper pattern.
- **Full SQL exposure**: SQLAlchemy exposes relational database functionality fully rather than hiding it.
- **Developer control**: You control all design decisions regarding object model structure, schema design, and naming conventions.

### Key Capabilities
- **Identity map**: Session maintains a single instance per database identity within a session.
- **Unit of work**: Changes are tracked and flushed to the database as a coordinated unit.
- **Data mapper pattern**: Separates domain model from relational schema with explicit mappings.
- **Declarative configuration**: Define ORM models with typed attributes using `DeclarativeBase` and `Mapped[...]`.
- **Query construction**: Build SQL queries using Pythonic constructs that render to optimized SQL.
- **Eager loading control**: Choose loading strategies (joined, selectin, subquery, lazy) per-query.
- **Connection pooling**: Built-in connection pool management with configurable sizing and behavior.
- **Schema metadata**: Reflect existing database schemas or define new ones programmatically.
- **Event system**: Hook into ORM and Core operations with event listeners.

### Common Pitfalls
- **Transaction management**: Assuming changes persist without calling `commit()` - they don't.
- **SQL injection**: Using string interpolation instead of bound parameters - always use bound parameters.
- **Wrong tool selection**: Using ORM when Core would suffice - ORM adds overhead for simple operations.
- **Query responsibility**: Blaming SQLAlchemy for bad queries - you control query structure including joins, subqueries, and correlation.
- **Impedance mismatch**: Expecting databases to behave like object collections (or vice versa) - use SQLAlchemy's mediation patterns.