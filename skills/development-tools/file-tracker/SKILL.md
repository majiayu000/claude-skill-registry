---
name: file-tracker
description: "Log all file changes (write, edit, delete) to a SQLite database for debugging and audit. Use when: (1) Tracking code changes, (2) Debugging issues, (3) Auditing file modifications, or (4) The user asks to track file changes."
---

# File Tracker

Log every file change (write, edit, delete) to a SQLite database for debugging, audit trails, and version history tracking. Works with any file operation system or code editor.

## When to use

- Tracking file modifications during development
- Creating audit trails for file changes
- Debugging what files were modified and when
- Building version history without git
- User asks to track or review file changes

## Required tools / APIs

- Python standard library (sqlite3, datetime, os)
- Any programming language with SQLite support

No external APIs or services required.

## Database Schema

```sql
CREATE TABLE IF NOT EXISTS file_changes (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  timestamp TEXT NOT NULL,
  action TEXT NOT NULL,              -- 'write', 'edit', 'delete', 'rename'
  file_path TEXT NOT NULL,
  old_content TEXT,                  -- for edits/deletes
  new_content TEXT,                  -- for writes/edits
  file_size INTEGER,                 -- size in bytes
  metadata TEXT,                     -- JSON: user, session_id, etc.
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_file_path ON file_changes(file_path);
CREATE INDEX idx_timestamp ON file_changes(timestamp);
CREATE INDEX idx_action ON file_changes(action);

-- Automatic purge: delete records older than 1 year
DELETE FROM file_changes WHERE created_at < datetime('now', '-1 year');
```

**Fields:**
- `id` - Auto-incrementing primary key
- `timestamp` - ISO 8601 timestamp of the change
- `action` - Type of operation: 'write', 'edit', 'delete', 'rename'
- `file_path` - Absolute or relative path to the file
- `old_content` - Previous content (for edits) or deleted content (for deletes)
- `new_content` - New content (for writes/edits)
- `file_size` - File size in bytes after operation
- `metadata` - JSON field for additional context (user, session, tools)
- `created_at` - Database insertion timestamp

## Basic Implementation

### Python

**Initialize database:**

```python
import sqlite3
from datetime import datetime
from pathlib import Path
import json
import os

# Configure database path (customize as needed)
DB_PATH = Path.home() / ".file_tracker" / "changes.db"

def init_db():
    """Initialize database and create tables."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("""
        CREATE TABLE IF NOT EXISTS file_changes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            action TEXT NOT NULL,
            file_path TEXT NOT NULL,
            old_content TEXT,
            new_content TEXT,
            file_size INTEGER,
            metadata TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_file_path ON file_changes(file_path)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_timestamp ON file_changes(timestamp)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_action ON file_changes(action)")
    conn.commit()
    conn.close()

def purge_old_changes():
    """Delete file change records older than 1 year to keep the database size sane."""
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("DELETE FROM file_changes WHERE created_at < datetime('now', '-1 year')")
    conn.commit()
    conn.close()

# Initialize on import and purge old records
init_db()
purge_old_changes()
```

**Log file changes:**

```python
def log_file_change(
    action: str,
    file_path: str,
    old_content: str = None,
    new_content: str = None,
    metadata: dict = None
):
    """Log a file change to the database."""
    conn = sqlite3.connect(str(DB_PATH))
    try:
        # Get file size if file exists
        file_size = None
        if os.path.exists(file_path) and action != "delete":
            file_size = os.path.getsize(file_path)

        conn.execute(
            """INSERT INTO file_changes
               (timestamp, action, file_path, old_content, new_content, file_size, metadata)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (
                datetime.utcnow().isoformat(),
                action,
                file_path,
                old_content[:5000] if old_content else None,  # Truncate large content
                new_content[:5000] if new_content else None,
                file_size,
                json.dumps(metadata) if metadata else None
            )
        )
        conn.commit()
    finally:
        conn.close()

# Usage examples
log_file_change("write", "/path/to/file.py", new_content="print('Hello')")
log_file_change("edit", "/path/to/file.py", old_content="print('Hello')", new_content="print('Hi')")
log_file_change("delete", "/path/to/file.py", old_content="print('Hi')")
log_file_change("write", "/path/to/config.json", new_content='{"key": "value"}',
                metadata={"user": "john", "session": "sess_123"})
```

**Tracked file operations:**

```python
def tracked_write(file_path: str, content: str, metadata: dict = None):
    """Write file and log the change."""
    with open(file_path, 'w') as f:
        f.write(content)
    log_file_change("write", file_path, new_content=content, metadata=metadata)

def tracked_edit(file_path: str, old_content: str, new_content: str, metadata: dict = None):
    """Edit file and log the change."""
    with open(file_path, 'w') as f:
        f.write(new_content)
    log_file_change("edit", file_path, old_content=old_content,
                    new_content=new_content, metadata=metadata)

def tracked_delete(file_path: str, metadata: dict = None):
    """Delete file and log the change."""
    with open(file_path, 'r') as f:
        old_content = f.read()
    os.remove(file_path)
    log_file_change("delete", file_path, old_content=old_content, metadata=metadata)

# Usage
tracked_write("example.txt", "Hello, World!")
tracked_edit("example.txt", "Hello, World!", "Hello, Python!")
tracked_delete("example.txt")
```

**Query file history:**

```python
def get_file_history(file_path: str, limit: int = 20):
    """Get change history for a specific file."""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    cursor = conn.execute(
        """SELECT timestamp, action, old_content, new_content, file_size
           FROM file_changes
           WHERE file_path = ?
           ORDER BY timestamp DESC
           LIMIT ?""",
        (file_path, limit)
    )
    results = cursor.fetchall()
    conn.close()
    return results

def get_recent_changes(limit: int = 50):
    """Get recent file changes across all files."""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    cursor = conn.execute(
        """SELECT timestamp, action, file_path, file_size
           FROM file_changes
           ORDER BY timestamp DESC
           LIMIT ?""",
        (limit,)
    )
    results = cursor.fetchall()
    conn.close()
    return results

def search_file_changes(pattern: str):
    """Search for files matching a pattern."""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    cursor = conn.execute(
        """SELECT timestamp, action, file_path
           FROM file_changes
           WHERE file_path LIKE ?
           ORDER BY timestamp DESC""",
        (f"%{pattern}%",)
    )
    results = cursor.fetchall()
    conn.close()
    return results

def get_changes_by_action(action: str, limit: int = 50):
    """Get all changes of a specific type (write, edit, delete)."""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    cursor = conn.execute(
        """SELECT timestamp, file_path, file_size
           FROM file_changes
           WHERE action = ?
           ORDER BY timestamp DESC
           LIMIT ?""",
        (action, limit)
    )
    results = cursor.fetchall()
    conn.close()
    return results

# Usage
history = get_file_history("/path/to/file.py")
for change in history:
    print(f"[{change['timestamp']}] {change['action']}: {change['file_size']} bytes")

recent = get_recent_changes(10)
print(f"Last {len(recent)} file changes")

edits = get_changes_by_action("edit", limit=20)
print(f"Found {len(edits)} file edits")
```

### Node.js

```javascript
import sqlite3 from "sqlite3";
import { promisify } from "util";
import path from "path";
import os from "os";
import fs from "fs/promises";

const DB_PATH = path.join(os.homedir(), ".file_tracker", "changes.db");

// Initialize database
const db = new sqlite3.Database(DB_PATH);
const run = promisify(db.run.bind(db));
const all = promisify(db.all.bind(db));

await run(`
  CREATE TABLE IF NOT EXISTS file_changes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    action TEXT NOT NULL,
    file_path TEXT NOT NULL,
    old_content TEXT,
    new_content TEXT,
    file_size INTEGER,
    metadata TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
  )
`);

// Log file change
async function logFileChange(action, filePath, oldContent = null, newContent = null, metadata = null) {
  let fileSize = null;
  try {
    if (action !== "delete") {
      const stats = await fs.stat(filePath);
      fileSize = stats.size;
    }
  } catch (err) {
    // File might not exist
  }

  await run(
    `INSERT INTO file_changes (timestamp, action, file_path, old_content, new_content, file_size, metadata)
     VALUES (?, ?, ?, ?, ?, ?, ?)`,
    [
      new Date().toISOString(),
      action,
      filePath,
      oldContent,
      newContent,
      fileSize,
      metadata ? JSON.stringify(metadata) : null,
    ]
  );
}

// Tracked file operations
async function trackedWrite(filePath, content, metadata = null) {
  await fs.writeFile(filePath, content);
  await logFileChange("write", filePath, null, content, metadata);
}

async function trackedEdit(filePath, oldContent, newContent, metadata = null) {
  await fs.writeFile(filePath, newContent);
  await logFileChange("edit", filePath, oldContent, newContent, metadata);
}

// Query history
async function getFileHistory(filePath, limit = 20) {
  return await all(
    `SELECT timestamp, action, old_content, new_content, file_size
     FROM file_changes
     WHERE file_path = ?
     ORDER BY timestamp DESC
     LIMIT ?`,
    [filePath, limit]
  );
}

// Usage
await trackedWrite("example.txt", "Hello, World!");
const history = await getFileHistory("example.txt");
console.log(history);
```

## Bash Quick Queries

```bash
# View recent file changes
sqlite3 ~/.file_tracker/changes.db "SELECT timestamp, action, file_path FROM file_changes ORDER BY timestamp DESC LIMIT 20"

# Get history for a specific file
sqlite3 ~/.file_tracker/changes.db "SELECT timestamp, action FROM file_changes WHERE file_path='/path/to/file' ORDER BY timestamp DESC"

# Count changes by action type
sqlite3 ~/.file_tracker/changes.db "SELECT action, COUNT(*) as count FROM file_changes GROUP BY action"

# Find all Python file changes
sqlite3 ~/.file_tracker/changes.db "SELECT timestamp, action, file_path FROM file_changes WHERE file_path LIKE '%.py' ORDER BY timestamp DESC"

# Export file history to JSON
sqlite3 -json ~/.file_tracker/changes.db "SELECT * FROM file_changes WHERE file_path='/path/to/file' ORDER BY timestamp ASC" > file_history.json
```

## Integration Examples

### Context Manager Pattern

```python
class FileChangeTracker:
    """Context manager to automatically track file changes."""

    def __init__(self, file_path: str, action: str = "edit", metadata: dict = None):
        self.file_path = file_path
        self.action = action
        self.metadata = metadata
        self.old_content = None

    def __enter__(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as f:
                self.old_content = f.read()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:  # No exception
            new_content = None
            if os.path.exists(self.file_path):
                with open(self.file_path, 'r') as f:
                    new_content = f.read()

            log_file_change(
                self.action,
                self.file_path,
                old_content=self.old_content,
                new_content=new_content,
                metadata=self.metadata
            )

# Usage
with FileChangeTracker("config.json", action="edit"):
    # Modify file
    with open("config.json", 'w') as f:
        f.write('{"updated": true}')
# Change is automatically logged on exit
```

### Decorator Pattern

```python
def track_file_operation(action: str):
    """Decorator to track file operations."""
    def decorator(func):
        def wrapper(file_path, *args, **kwargs):
            # Read old content if file exists
            old_content = None
            if os.path.exists(file_path) and action in ["edit", "delete"]:
                with open(file_path, 'r') as f:
                    old_content = f.read()

            # Execute operation
            result = func(file_path, *args, **kwargs)

            # Read new content
            new_content = None
            if os.path.exists(file_path) and action in ["write", "edit"]:
                with open(file_path, 'r') as f:
                    new_content = f.read()

            # Log change
            log_file_change(action, file_path, old_content, new_content)

            return result
        return wrapper
    return decorator

# Usage
@track_file_operation("write")
def create_file(path, content):
    with open(path, 'w') as f:
        f.write(content)

@track_file_operation("edit")
def update_file(path, new_content):
    with open(path, 'w') as f:
        f.write(new_content)
```

## Agent Prompt

```text
You have file change tracking capability. All file operations are logged to a SQLite database.

When user asks to:
- Review file change history
- Track what files were modified
- Find when a file was changed
- Audit file operations

Use the SQLite database at ~/.file_tracker/changes.db with this schema:
- file_changes table (id, timestamp, action, file_path, old_content, new_content, file_size, metadata)

After performing file operations (write, edit, delete), always log them:
- Write: log_file_change("write", file_path, new_content=content)
- Edit: log_file_change("edit", file_path, old_content=old, new_content=new)
- Delete: log_file_change("delete", file_path, old_content=content)

Query examples:
1. File history: SELECT * FROM file_changes WHERE file_path = ? ORDER BY timestamp DESC
2. Recent changes: SELECT * FROM file_changes ORDER BY timestamp DESC LIMIT 50
3. Search files: SELECT * FROM file_changes WHERE file_path LIKE '%pattern%'

Always log file operations for audit trail and debugging purposes.
```

## Best Practices

1. **Truncate large content** (e.g., 5000 chars) to avoid database bloat
2. **Use indexes** on file_path, timestamp, and action for fast queries
3. **Store full paths** for clarity and uniqueness
4. **Log metadata** (user, session) for context
5. **Regular cleanup** of old entries to manage database size
6. **Privacy**: avoid storing sensitive file content
7. **Compression**: consider compressing old_content/new_content for large text files

## Troubleshooting

**Database getting too large:**
- Truncate old entries: `DELETE FROM file_changes WHERE timestamp < '2024-01-01'`
- Run VACUUM: `sqlite3 changes.db "VACUUM"`
- Limit content stored (already truncated to 5000 chars)

**Missing file changes:**
- Ensure log_file_change() is called after every file operation
- Check file permissions for database writes
- Verify DB_PATH is accessible

**Query performance slow:**
- Ensure indexes exist (file_path, timestamp, action)
- Use LIMIT on queries
- Consider archiving old entries

## See also

- [../chat-logger/SKILL.md](../chat-logger/SKILL.md) — Log chat messages
- [../generate-report/SKILL.md](../generate-report/SKILL.md) — Generate HTML reports
