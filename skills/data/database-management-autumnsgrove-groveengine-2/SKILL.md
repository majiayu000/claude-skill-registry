---
name: database-management
description: Implement SQLite database patterns using the database.py interface with complete SQL isolation. MANDATORY for all database projects. Use when working with databases, data persistence, or SQLite.
---

# Database Management Skill

## When to Activate

Activate this skill when:
- Setting up database functionality
- Creating database schemas
- Implementing data persistence
- Writing database queries
- Working with SQLite or any database

**IMPORTANT**: This is MANDATORY for all projects requiring database functionality.

## Core Architecture

### Principles
1. **SQLite Only**: Use SQLite as default database
2. **Single Interface**: All database operations through `database.py`
3. **Complete SQL Isolation**: All SQL statements in `database.py`
4. **Function-Based**: Simple, reusable function interface

### File Structure

```
project/
├── database.py         # ALL SQL lives here
├── app.py              # Uses database functions (no SQL!)
└── tests/
    └── test_database.py
```

## Standard Interface Pattern

```python
# database.py - All database code lives here
import sqlite3
from typing import List, Dict, Optional, Any

DB_PATH = "app.db"

def get_connection(db_path: str = DB_PATH) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db(db_path: str = DB_PATH) -> None:
    """Initialize database with schema."""
    conn = get_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def db_query(query: str, params: tuple = ()) -> List[Dict[str, Any]]:
    """Execute SELECT query and return results."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def db_execute(query: str, params: tuple = ()) -> int:
    """Execute INSERT/UPDATE/DELETE and return affected rows."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    return affected

def db_insert(query: str, params: tuple = ()) -> int:
    """Execute INSERT and return last row ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    last_id = cursor.lastrowid
    conn.close()
    return last_id
```

## Domain-Specific Functions

```python
# Add to database.py - Clean API for application code

def get_user_by_id(user_id: int) -> Optional[Dict[str, Any]]:
    """Get user by ID."""
    results = db_query("SELECT * FROM users WHERE id = ?", (user_id,))
    return results[0] if results else None

def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
    """Get user by email."""
    results = db_query("SELECT * FROM users WHERE email = ?", (email,))
    return results[0] if results else None

def create_user(username: str, email: str) -> int:
    """Create new user and return ID."""
    return db_insert(
        "INSERT INTO users (username, email) VALUES (?, ?)",
        (username, email)
    )

def delete_user(user_id: int) -> bool:
    """Delete user by ID."""
    return db_execute("DELETE FROM users WHERE id = ?", (user_id,)) > 0
```

## Application Usage

```python
# app.py - NO SQL HERE!
from database import init_db, get_user_by_id, create_user

def main():
    init_db()

    # Create user (no SQL!)
    user_id = create_user("alice", "alice@example.com")
    print(f"Created user: {user_id}")

    # Get user (no SQL!)
    user = get_user_by_id(user_id)
    print(f"User: {user['username']}")
```

## Anti-Patterns to Avoid

### ❌ WRONG: SQL in application code
```python
def process_user(user_id):
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
```

### ✅ CORRECT: Use database functions
```python
def process_user(user_id):
    user = get_user_by_id(user_id)
```

## Security: Always Use Parameters

```python
# ❌ WRONG: SQL injection vulnerability!
query = f"SELECT * FROM users WHERE email = '{email}'"

# ✅ CORRECT: Parameterized query
query = "SELECT * FROM users WHERE email = ?"
results = db_query(query, (email,))
```

## Common Patterns

### Pagination
```python
def get_users_paginated(page: int = 1, per_page: int = 10):
    offset = (page - 1) * per_page
    return db_query(
        "SELECT * FROM users ORDER BY created_at DESC LIMIT ? OFFSET ?",
        (per_page, offset)
    )
```

### Transactions
```python
def db_transaction(operations: List[tuple]) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    try:
        for query, params in operations:
            cursor.execute(query, params)
        conn.commit()
        return True
    except:
        conn.rollback()
        return False
    finally:
        conn.close()
```

## Golden Rules

1. ✅ **All SQL in database.py** - nowhere else
2. ✅ **Parameterized queries** - prevent SQL injection
3. ✅ **Meaningful return types** - Optional, List, bool, int
4. ✅ **Transaction support** - for multi-operation consistency
5. ✅ **Add *.db to .gitignore** - don't commit databases

## Related Resources

See `AgentUsage/db_usage.md` for complete documentation including:
- Full database.py template
- Migration patterns
- Testing database functions
- Performance optimization
