---
name: database-patterns
description: Database design and operations - PostgreSQL, SQLite, Redis, schema design, migrations, query optimization, and connection management. Auto-triggers when working with databases.
---

# Database Patterns Skill

## Schema Design

### Naming Conventions

| Element            | Convention              | Example          |
| ------------------ | ----------------------- | ---------------- |
| Tables             | plural, snake_case      | `user_profiles`  |
| Columns            | singular, snake_case    | `created_at`     |
| Primary keys       | `id` or `<table>_id`    | `id`             |
| Foreign keys       | `<referenced_table>_id` | `user_id`        |
| Indexes            | `ix_<table>_<columns>`  | `ix_users_email` |
| Unique constraints | `uq_<table>_<columns>`  | `uq_users_email` |

### Common Column Patterns

```sql
CREATE TABLE users (
    id          BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    email       TEXT NOT NULL UNIQUE,
    name        TEXT NOT NULL,
    status      TEXT NOT NULL DEFAULT 'active'
                CHECK (status IN ('active', 'inactive', 'banned')),
    metadata    JSONB DEFAULT '{}',
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Auto-update updated_at
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();
```

### Relationships

```sql
-- One-to-Many
CREATE TABLE orders (
    id          BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id     BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    total       DECIMAL(10,2) NOT NULL,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX ix_orders_user_id ON orders(user_id);

-- Many-to-Many
CREATE TABLE user_roles (
    user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    role_id BIGINT NOT NULL REFERENCES roles(id) ON DELETE CASCADE,
    PRIMARY KEY (user_id, role_id)
);
```

## PostgreSQL Patterns

### JSONB Operations

```sql
-- Query JSONB fields
SELECT * FROM users WHERE metadata->>'plan' = 'premium';
SELECT * FROM users WHERE metadata @> '{"verified": true}';

-- Update JSONB
UPDATE users SET metadata = metadata || '{"verified": true}' WHERE id = 1;

-- Index JSONB for fast queries
CREATE INDEX ix_users_metadata ON users USING GIN (metadata);
```

### Common Table Expressions (CTEs)

```sql
WITH active_users AS (
    SELECT id, name, email
    FROM users
    WHERE status = 'active'
),
user_order_counts AS (
    SELECT user_id, COUNT(*) as order_count
    FROM orders
    GROUP BY user_id
)
SELECT au.name, au.email, COALESCE(uoc.order_count, 0) as orders
FROM active_users au
LEFT JOIN user_order_counts uoc ON au.id = uoc.user_id
ORDER BY orders DESC;
```

### Window Functions

```sql
-- Rank users by order count
SELECT
    name,
    COUNT(o.id) as order_count,
    RANK() OVER (ORDER BY COUNT(o.id) DESC) as rank
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id, u.name;
```

## SQLite Patterns

### Python Usage

```python
import sqlite3
from contextlib import contextmanager

@contextmanager
def get_db(path: str = "app.db"):
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row  # Dict-like access
    conn.execute("PRAGMA journal_mode=WAL")  # Better concurrency
    conn.execute("PRAGMA foreign_keys=ON")   # Enforce FK constraints
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

# Usage
with get_db() as db:
    db.execute(
        "INSERT INTO users (name, email) VALUES (?, ?)",
        (name, email),
    )
```

### SQLite Best Practices

| Setting                    | Why                                |
| -------------------------- | ---------------------------------- |
| `PRAGMA journal_mode=WAL`  | Better concurrent read/write       |
| `PRAGMA foreign_keys=ON`   | Enforce referential integrity      |
| `PRAGMA busy_timeout=5000` | Wait 5s instead of failing on lock |
| Use `?` placeholders       | Prevent SQL injection              |

## Redis Patterns

### Common Data Structures

```python
import redis

r = redis.Redis(host="localhost", port=6379, decode_responses=True)

# String (cache)
r.setex("user:123:profile", 3600, json.dumps(profile))  # 1hr TTL
cached = json.loads(r.get("user:123:profile") or "{}")

# Hash (object fields)
r.hset("user:123", mapping={"name": "Alice", "email": "alice@example.com"})
name = r.hget("user:123", "name")

# Sorted Set (leaderboard)
r.zadd("leaderboard", {"alice": 100, "bob": 85})
top_10 = r.zrevrange("leaderboard", 0, 9, withscores=True)

# List (queue)
r.lpush("task_queue", json.dumps(task))
task = json.loads(r.brpop("task_queue", timeout=30)[1])
```

### Caching Patterns

```python
def get_user(user_id: str) -> dict:
    # Check cache first
    cached = r.get(f"user:{user_id}")
    if cached:
        return json.loads(cached)

    # Cache miss - fetch from DB
    user = db.query("SELECT * FROM users WHERE id = %s", (user_id,))

    # Cache for 1 hour
    r.setex(f"user:{user_id}", 3600, json.dumps(user))
    return user

def invalidate_user(user_id: str):
    r.delete(f"user:{user_id}")
```

## Migrations

### Alembic (SQLAlchemy)

```bash
# Initialize
alembic init migrations

# Create migration
alembic revision --autogenerate -m "add users table"

# Run migrations
alembic upgrade head

# Rollback one step
alembic downgrade -1
```

### Migration Best Practices

| Do                                             | Don't                                    |
| ---------------------------------------------- | ---------------------------------------- |
| Make migrations reversible (include downgrade) | Drop columns without backup              |
| Add indexes concurrently in production         | Lock tables with long-running migrations |
| Use transactions for DDL                       | Mix schema changes with data changes     |
| Test migrations against production-like data   | Assume empty tables                      |

## Query Optimization

### Index Strategy

```sql
-- Single column (equality lookups)
CREATE INDEX ix_users_email ON users(email);

-- Composite (multi-column queries, order matters)
CREATE INDEX ix_orders_user_status ON orders(user_id, status);

-- Partial (subset of rows)
CREATE INDEX ix_users_active ON users(email) WHERE status = 'active';

-- Covering (avoid table lookup)
CREATE INDEX ix_orders_covering ON orders(user_id) INCLUDE (total, status);
```

### EXPLAIN ANALYZE

```sql
EXPLAIN ANALYZE
SELECT u.name, COUNT(o.id)
FROM users u
JOIN orders o ON u.id = o.user_id
WHERE u.status = 'active'
GROUP BY u.id;
```

| Look For    | Meaning                                 |
| ----------- | --------------------------------------- |
| Seq Scan    | Full table scan (may need index)        |
| Index Scan  | Using an index (good)                   |
| Nested Loop | O(n\*m) join (fine for small tables)    |
| Hash Join   | Efficient for large tables              |
| Sort        | May indicate missing index for ORDER BY |

### Connection Pooling

```python
# SQLAlchemy
from sqlalchemy import create_engine

engine = create_engine(
    "postgresql://user:pass@localhost/db",
    pool_size=10,          # Maintain 10 connections
    max_overflow=20,       # Allow 20 additional under load
    pool_timeout=30,       # Wait 30s for connection
    pool_recycle=1800,     # Recycle connections every 30min
)
```

## Activation Triggers

This skill auto-activates when prompts contain:

- "database", "schema", "migration"
- "postgresql", "postgres", "sqlite", "redis"
- "sql", "query", "index", "table"
- "connection pool", "ORM", "alembic"

## Integration

- **@database-architect** agent: Schema design and optimization
- **api-design** skill: Database-backed API patterns
- **docker-essentials** skill: Database containers
