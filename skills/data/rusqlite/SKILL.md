---
name: rusqlite
description: SQLite database bindings for Rust
triggers:
  - rusqlite
  - sqlite
  - database
  - Connection
  - params!
  - query_row
  - execute
---

# rusqlite

Ergonomic SQLite bindings for Rust. rusqlite wraps the SQLite C library with safe, idiomatic Rust APIs for database operations.

## Key Types

### Connection
The main entry point - represents a SQLite database connection.

```rust
use rusqlite::Connection;

// Open file-based database
let conn = Connection::open("path/to/db.sqlite")?;

// Open in-memory database (testing)
let conn = Connection::open_in_memory()?;
```

### Statement
Prepared SQL statement for repeated execution with different parameters.

```rust
let mut stmt = conn.prepare("SELECT id, name FROM users WHERE active = ?")?;
```

### Row
Represents a single result row. Access columns by index or name.

```rust
|row| {
    let id: i64 = row.get(0)?;           // By index
    let name: String = row.get("name")?;  // By name
    Ok((id, name))
}
```

### params! Macro
Convenient parameter binding that converts Rust types to SQL values.

```rust
use rusqlite::params;

conn.execute(
    "INSERT INTO users (name, age) VALUES (?1, ?2)",
    params!["Alice", 30],
)?;
```

### OptionalExtension Trait
Converts `Result<T, Error>` to `Result<Option<T>, Error>` for queries that may return no rows.

```rust
use rusqlite::OptionalExtension;

let user: Option<User> = conn
    .query_row("SELECT * FROM users WHERE id = ?", params![id], row_to_user)
    .optional()?;  // Returns None instead of error if no rows
```

## Usage in script-kit-gpui

### Database Files
All databases stored in `~/.scriptkit/db/`:

| File | Purpose |
|------|---------|
| `clipboard-history.sqlite` | Clipboard entry storage with hash dedup |
| `ai-chats.sqlite` | AI chat conversations and messages |
| `notes.sqlite` | User notes with FTS5 search |
| `apps.sqlite` | Application launcher cache |
| `menu-cache.sqlite` | Menu bar item cache |

### Clipboard History Schema
```sql
CREATE TABLE history (
    id TEXT PRIMARY KEY,
    content TEXT NOT NULL,
    content_hash TEXT,           -- SHA-256 for O(1) dedup
    content_type TEXT NOT NULL DEFAULT 'text',
    timestamp INTEGER NOT NULL,  -- milliseconds since epoch
    pinned INTEGER DEFAULT 0,
    ocr_text TEXT,
    text_preview TEXT,           -- First 100 chars for list view
    image_width INTEGER,
    image_height INTEGER,
    byte_size INTEGER DEFAULT 0
);

CREATE INDEX idx_timestamp ON history(timestamp DESC);
CREATE INDEX idx_pinned_timestamp ON history(pinned DESC, timestamp DESC);
CREATE INDEX idx_dedup ON history(content_type, content_hash);
```

### AI Chat Schema
```sql
CREATE TABLE chats (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL DEFAULT 'New Chat',
    created_at TEXT NOT NULL,    -- RFC3339 format
    updated_at TEXT NOT NULL,
    deleted_at TEXT,             -- Soft delete
    model_id TEXT NOT NULL,
    provider TEXT NOT NULL
);

CREATE TABLE messages (
    id TEXT PRIMARY KEY,
    chat_id TEXT NOT NULL,
    role TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at TEXT NOT NULL,
    tokens_used INTEGER,
    FOREIGN KEY (chat_id) REFERENCES chats(id) ON DELETE CASCADE
);

-- FTS5 for full-text search
CREATE VIRTUAL TABLE chats_fts USING fts5(title, content='chats', content_rowid='rowid');
CREATE VIRTUAL TABLE messages_fts USING fts5(content, content='messages', content_rowid='rowid');
```

## Connection Management

### Global Singleton Pattern
script-kit-gpui uses `OnceLock<Arc<Mutex<Connection>>>` for thread-safe global connections:

```rust
use std::sync::{Arc, Mutex, OnceLock};
use rusqlite::Connection;

static DB_CONNECTION: OnceLock<Arc<Mutex<Connection>>> = OnceLock::new();

pub fn get_connection() -> Result<Arc<Mutex<Connection>>> {
    if let Some(conn) = DB_CONNECTION.get() {
        return Ok(conn.clone());
    }

    let conn = Connection::open(&db_path)?;
    
    // Configure connection
    conn.execute_batch("PRAGMA journal_mode=WAL; PRAGMA synchronous=NORMAL;")?;
    conn.execute_batch("PRAGMA busy_timeout = 5000;")?;
    conn.execute_batch("PRAGMA foreign_keys=ON;")?;
    
    let conn = Arc::new(Mutex::new(conn));
    
    if DB_CONNECTION.set(conn.clone()).is_err() {
        return Ok(DB_CONNECTION.get().unwrap().clone());
    }
    
    Ok(conn)
}
```

### Essential PRAGMAs

```rust
// WAL mode for concurrent reads during writes
conn.execute_batch("PRAGMA journal_mode=WAL;")?;

// Balance durability vs performance
conn.execute_batch("PRAGMA synchronous=NORMAL;")?;

// Avoid "database is locked" errors (5 second timeout)
conn.execute_batch("PRAGMA busy_timeout = 5000;")?;

// Enable foreign key enforcement (off by default!)
conn.execute_batch("PRAGMA foreign_keys=ON;")?;

// Enable incremental vacuum for disk space recovery
conn.execute_batch("PRAGMA auto_vacuum = INCREMENTAL;")?;
```

## Query Patterns

### Single Row Query
```rust
let count: i64 = conn.query_row(
    "SELECT COUNT(*) FROM history",
    [],
    |row| row.get(0),
)?;
```

### Optional Single Row
```rust
use rusqlite::OptionalExtension;

let entry: Option<Entry> = conn
    .query_row(
        "SELECT id, content FROM history WHERE id = ?",
        params![id],
        |row| Ok(Entry { id: row.get(0)?, content: row.get(1)? }),
    )
    .optional()?;
```

### Multiple Rows with query_map
```rust
let mut stmt = conn.prepare(
    "SELECT id, content, timestamp FROM history ORDER BY timestamp DESC LIMIT ?"
)?;

let entries: Vec<Entry> = stmt
    .query_map(params![limit], |row| {
        Ok(Entry {
            id: row.get(0)?,
            content: row.get(1)?,
            timestamp: row.get(2)?,
        })
    })?
    .filter_map(|r| r.ok())
    .collect();
```

### Execute (INSERT/UPDATE/DELETE)
```rust
// Returns number of affected rows
let affected = conn.execute(
    "DELETE FROM history WHERE timestamp < ?",
    params![cutoff_timestamp],
)?;

if affected == 0 {
    anyhow::bail!("Entry not found");
}
```

### Execute Batch (Multiple Statements)
```rust
conn.execute_batch(r#"
    CREATE TABLE IF NOT EXISTS notes (...);
    CREATE INDEX IF NOT EXISTS idx_notes_updated_at ON notes(updated_at DESC);
"#)?;
```

### Transactions
```rust
let mut conn = db.lock()?;
let tx = conn.transaction()?;

tx.execute("INSERT INTO messages ...", params![...])?;
tx.execute("UPDATE chats SET updated_at = ? WHERE id = ?", params![now, chat_id])?;

tx.commit()?;  // Atomic commit, single fsync
```

### Upsert (INSERT OR UPDATE)
```rust
conn.execute(
    r#"
    INSERT INTO notes (id, title, content, updated_at)
    VALUES (?1, ?2, ?3, ?4)
    ON CONFLICT(id) DO UPDATE SET
        title = excluded.title,
        content = excluded.content,
        updated_at = excluded.updated_at
    "#,
    params![note.id, note.title, note.content, now],
)?;
```

## Schema Migrations

### Check Column Existence
```rust
let has_column: bool = conn
    .query_row(
        "SELECT COUNT(*) FROM pragma_table_info('history') WHERE name='ocr_text'",
        [],
        |row| row.get::<_, i32>(0),
    )
    .map(|count| count > 0)
    .unwrap_or(false);

if !has_column {
    conn.execute("ALTER TABLE history ADD COLUMN ocr_text TEXT", [])?;
    info!("Migration: added ocr_text column");
}
```

### Data Migration
```rust
// Convert timestamps from seconds to milliseconds
let needs_migration: i64 = conn.query_row(
    "SELECT COUNT(*) FROM history WHERE timestamp < 100000000000 AND timestamp > 0",
    [],
    |row| row.get(0),
).unwrap_or(0);

if needs_migration > 0 {
    conn.execute(
        "UPDATE history SET timestamp = timestamp * 1000 
         WHERE timestamp < 100000000000 AND timestamp > 0",
        [],
    )?;
}
```

### FTS5 Triggers for Sync
```sql
-- Keep FTS in sync with main table
CREATE TRIGGER notes_ai AFTER INSERT ON notes BEGIN
    INSERT INTO notes_fts(rowid, title, content)
    VALUES (NEW.rowid, NEW.title, NEW.content);
END;

CREATE TRIGGER notes_ad AFTER DELETE ON notes BEGIN
    INSERT INTO notes_fts(notes_fts, rowid, title, content)
    VALUES('delete', OLD.rowid, OLD.title, OLD.content);
END;

-- IMPORTANT: Only trigger on content changes, not metadata
CREATE TRIGGER notes_au AFTER UPDATE OF title, content ON notes BEGIN
    INSERT INTO notes_fts(notes_fts, rowid, title, content)
    VALUES('delete', OLD.rowid, OLD.title, OLD.content);
    INSERT INTO notes_fts(rowid, title, content)
    VALUES (NEW.rowid, NEW.title, NEW.content);
END;
```

## Full-Text Search (FTS5)

### Basic FTS Query
```rust
fn sanitize_fts_query(query: &str) -> String {
    let escaped = query.replace('"', "\"\"");
    format!("\"{}\"", escaped)
}

let sanitized = sanitize_fts_query(user_query);
let mut stmt = conn.prepare(
    "SELECT * FROM notes WHERE rowid IN (SELECT rowid FROM notes_fts WHERE notes_fts MATCH ?)"
)?;
let results = stmt.query_map(params![sanitized], row_to_note)?;
```

### FTS with Fallback to LIKE
```rust
// Try FTS first, fall back to LIKE on parse errors
let fts_result: rusqlite::Result<Vec<Note>> = (|| {
    let mut stmt = conn.prepare("SELECT ... WHERE notes_fts MATCH ?1")?;
    stmt.query_map(params![sanitized], row_to_note)?.collect()
})();

match fts_result {
    Ok(notes) => Ok(notes),
    Err(_) => {
        // FTS failed, use LIKE fallback
        let like_pattern = format!("%{}%", query);
        let mut stmt = conn.prepare("SELECT ... WHERE title LIKE ?1 OR content LIKE ?1")?;
        // ...
    }
}
```

## Type Conversions

### Rust to SQL
| Rust Type | SQLite Type |
|-----------|-------------|
| `i32`, `i64` | INTEGER |
| `f32`, `f64` | REAL |
| `String`, `&str` | TEXT |
| `Vec<u8>`, `&[u8]` | BLOB |
| `bool` | INTEGER (0/1) |
| `Option<T>` | NULL or T |

### Boolean Handling
SQLite has no native boolean - use INTEGER:

```rust
// Writing
params![entry.pinned as i32]  // or: if pinned { 1 } else { 0 }

// Reading
let pinned: bool = row.get::<_, i64>(4)? != 0;
```

### DateTime Handling
Store as TEXT (RFC3339) or INTEGER (Unix timestamp):

```rust
// TEXT format (RFC3339)
params![datetime.to_rfc3339()]

// Reading
let created_at = DateTime::parse_from_rfc3339(&row.get::<_, String>(2)?)
    .map(|dt| dt.with_timezone(&Utc))
    .unwrap_or_else(|_| Utc::now());
```

## Anti-patterns

### SQL Injection - NEVER String Format
```rust
// WRONG - SQL injection vulnerability!
let query = format!("SELECT * FROM users WHERE name = '{}'", user_input);
conn.execute(&query, [])?;

// CORRECT - Use parameterized queries
conn.execute("SELECT * FROM users WHERE name = ?", params![user_input])?;
```

### Forgetting to Enable Foreign Keys
```rust
// Foreign keys are OFF by default in SQLite!
// Must enable per-connection:
conn.execute_batch("PRAGMA foreign_keys=ON;")?;
```

### Not Handling Lock Contention
```rust
// WRONG - Will fail under concurrent access
let conn = Connection::open(&path)?;

// CORRECT - Set busy timeout
conn.execute_batch("PRAGMA busy_timeout = 5000;")?;
// Or use the method:
conn.busy_timeout(std::time::Duration::from_millis(5000))?;
```

### Forgetting to Drop Lock Before Cache Update
```rust
// WRONG - Deadlock if cache update needs DB
let conn = get_connection()?;
let conn = conn.lock()?;
conn.execute(...)?;
update_cache();  // May need DB lock!

// CORRECT - Drop lock first
let conn = get_connection()?;
let conn = conn.lock()?;
conn.execute(...)?;
drop(conn);  // Release lock
update_cache();  // Now safe
```

### Not Using Transactions for Multi-Statement Ops
```rust
// WRONG - Two fsyncs, not atomic
conn.execute("INSERT INTO messages ...", params![...])?;
conn.execute("UPDATE chats ...", params![...])?;

// CORRECT - Single fsync, atomic
let tx = conn.transaction()?;
tx.execute("INSERT INTO messages ...", params![...])?;
tx.execute("UPDATE chats ...", params![...])?;
tx.commit()?;
```

## Error Handling

### Common Error Types
```rust
use rusqlite::Error;

match result {
    Err(Error::QueryReturnedNoRows) => { /* Handle missing row */ }
    Err(Error::SqliteFailure(err, msg)) => {
        // err.code - SQLite error code
        // err.extended_code - Extended error code
        // msg - Error message
    }
    Err(e) => { /* Other errors */ }
    Ok(v) => { /* Success */ }
}
```

### Pattern: Return Affected Row Count
```rust
pub fn remove_entry(id: &str) -> Result<()> {
    let affected = conn.execute("DELETE FROM history WHERE id = ?", params![id])?;
    
    if affected == 0 {
        anyhow::bail!("Entry not found: {}", id);
    }
    
    Ok(())
}
```

## Maintenance Operations

### WAL Checkpoint
```rust
// Passive - doesn't block writers
conn.execute_batch("PRAGMA wal_checkpoint(PASSIVE);")?;
```

### Incremental Vacuum
```rust
// Reclaim space from deleted rows (100 pages at a time)
conn.execute_batch("PRAGMA incremental_vacuum(100);")?;
```

## Testing

### In-Memory Database for Tests
```rust
#[cfg(test)]
fn test_db() -> Connection {
    let conn = Connection::open_in_memory().unwrap();
    init_schema(&conn).unwrap();
    conn
}
```

### Temporary File Database
```rust
#[cfg(test)]
fn test_db_file() -> (Connection, tempfile::TempDir) {
    let dir = tempfile::tempdir().unwrap();
    let path = dir.path().join("test.db");
    let conn = Connection::open(&path).unwrap();
    (conn, dir)  // dir keeps file alive
}
```

## References

- [rusqlite docs](https://docs.rs/rusqlite/latest/rusqlite/)
- [SQLite documentation](https://www.sqlite.org/docs.html)
- [FTS5 full-text search](https://www.sqlite.org/fts5.html)
- [WAL mode](https://www.sqlite.org/wal.html)
