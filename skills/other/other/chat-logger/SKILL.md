---
name: chat-logger
description: "Log all chat messages to a SQLite database for searchable history and audit. Use when: (1) Building chat history, (2) Auditing conversations, (3) Searching past messages, or (4) User asks to log chats."
---

# Chat Logger

Log all incoming and outgoing chat messages to a SQLite database for searchable history, analytics, and auditing. Works with any chat system or agent framework.

## When to use

- Building a searchable chat history system
- Auditing and reviewing past conversations
- Creating analytics on chat interactions
- Debugging chat flows and responses
- User asks to track or search conversation history

## Required tools / APIs

- Python standard library (sqlite3, datetime, json)
- Any programming language with SQLite support

No external APIs or services required.

## Database Schema

```sql
CREATE TABLE IF NOT EXISTS messages (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  timestamp TEXT NOT NULL,
  session_id TEXT,
  sender TEXT NOT NULL,           -- 'user', 'assistant', or identifier
  content TEXT,
  metadata TEXT,                  -- JSON: channel, tools_used, etc.
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_timestamp ON messages(timestamp);
CREATE INDEX idx_session ON messages(session_id);
CREATE INDEX idx_sender ON messages(sender);

-- Automatic purge: delete records older than 1 year
DELETE FROM messages WHERE created_at < datetime('now', '-1 year');
```

**Fields:**
- `id` - Auto-incrementing primary key
- `timestamp` - ISO 8601 timestamp of the message
- `session_id` - Optional session/conversation identifier
- `sender` - Message sender ('user', 'assistant', or custom ID)
- `content` - Message text content
- `metadata` - JSON field for additional data (channel, tools, context)
- `created_at` - Database insertion timestamp

## Basic Implementation

### Python

**Initialize database:**

```python
import sqlite3
from datetime import datetime
from pathlib import Path
import json

# Configure database path
DB_PATH = Path.home() / ".chat_logs" / "messages.db"

def init_db():
    """Initialize database and create tables."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            session_id TEXT,
            sender TEXT NOT NULL,
            content TEXT,
            metadata TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_timestamp ON messages(timestamp)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_session ON messages(session_id)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_sender ON messages(sender)")
    conn.commit()
    conn.close()

def purge_old_messages():
    """Delete messages older than 1 year to keep the database size sane."""
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("DELETE FROM messages WHERE created_at < datetime('now', '-1 year')")
    conn.commit()
    conn.close()

# Initialize on import and purge old records
init_db()
purge_old_messages()
```

**Log messages:**

```python
def log_message(sender: str, content: str, session_id: str = None, metadata: dict = None):
    """Log a chat message to the database."""
    conn = sqlite3.connect(str(DB_PATH))
    try:
        conn.execute(
            """INSERT INTO messages (timestamp, session_id, sender, content, metadata)
               VALUES (?, ?, ?, ?, ?)""",
            (
                datetime.utcnow().isoformat(),
                session_id,
                sender,
                content[:10000] if content else None,  # Truncate long messages
                json.dumps(metadata) if metadata else None
            )
        )
        conn.commit()
    finally:
        conn.close()

# Usage examples
log_message("user", "Hello, how are you?", session_id="session_123")
log_message("assistant", "I'm doing well, thank you!", session_id="session_123")
log_message("user", "Help me deploy a website", session_id="session_456",
            metadata={"channel": "web", "ip": "192.168.1.1"})
```

**Query messages:**

```python
def get_recent_messages(limit: int = 50):
    """Get recent messages."""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    cursor = conn.execute(
        "SELECT * FROM messages ORDER BY timestamp DESC LIMIT ?",
        (limit,)
    )
    results = cursor.fetchall()
    conn.close()
    return results

def get_session_history(session_id: str):
    """Get all messages from a specific session."""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    cursor = conn.execute(
        "SELECT * FROM messages WHERE session_id = ? ORDER BY timestamp ASC",
        (session_id,)
    )
    results = cursor.fetchall()
    conn.close()
    return results

def search_messages(query: str, limit: int = 20):
    """Search message content."""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    cursor = conn.execute(
        "SELECT * FROM messages WHERE content LIKE ? ORDER BY timestamp DESC LIMIT ?",
        (f"%{query}%", limit)
    )
    results = cursor.fetchall()
    conn.close()
    return results

# Usage
messages = get_recent_messages(10)
for msg in messages:
    print(f"[{msg['timestamp']}] {msg['sender']}: {msg['content'][:100]}")

# Search
results = search_messages("deploy website")
print(f"Found {len(results)} messages about deploying websites")
```

### Node.js

```javascript
import sqlite3 from "sqlite3";
import { promisify } from "util";
import path from "path";
import os from "os";

const DB_PATH = path.join(os.homedir(), ".chat_logs", "messages.db");

// Initialize database
const db = new sqlite3.Database(DB_PATH);
const run = promisify(db.run.bind(db));
const all = promisify(db.all.bind(db));

await run(`
  CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    session_id TEXT,
    sender TEXT NOT NULL,
    content TEXT,
    metadata TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
  )
`);

// Log message
async function logMessage(sender, content, sessionId = null, metadata = null) {
  await run(
    `INSERT INTO messages (timestamp, session_id, sender, content, metadata)
     VALUES (?, ?, ?, ?, ?)`,
    [
      new Date().toISOString(),
      sessionId,
      sender,
      content,
      metadata ? JSON.stringify(metadata) : null,
    ]
  );
}

// Query messages
async function getRecentMessages(limit = 50) {
  return await all(
    `SELECT * FROM messages ORDER BY timestamp DESC LIMIT ?`,
    [limit]
  );
}

// Usage
await logMessage("user", "Hello!", "session_123");
await logMessage("assistant", "Hi there!", "session_123");

const messages = await getRecentMessages(10);
console.log(messages);
```

## Bash Quick Queries

```bash
# View recent messages
sqlite3 ~/.chat_logs/messages.db "SELECT timestamp, sender, substr(content, 1, 80) FROM messages ORDER BY timestamp DESC LIMIT 20"

# Search for specific content
sqlite3 ~/.chat_logs/messages.db "SELECT * FROM messages WHERE content LIKE '%docker%' ORDER BY timestamp DESC"

# Count messages by sender
sqlite3 ~/.chat_logs/messages.db "SELECT sender, COUNT(*) as count FROM messages GROUP BY sender"

# Export session to JSON
sqlite3 -json ~/.chat_logs/messages.db "SELECT * FROM messages WHERE session_id='session_123' ORDER BY timestamp ASC" > conversation.json
```

## Integration Examples

### Generic Chat Application

```python
class ChatLogger:
    """Simple chat logger that can wrap any chat system."""

    def __init__(self, db_path: str = None):
        self.db_path = db_path or str(Path.home() / ".chat_logs" / "messages.db")
        self._init_db()

    def _init_db(self):
        # Same as init_db() above
        pass

    def log_user_message(self, content: str, session_id: str = None, **metadata):
        return log_message("user", content, session_id, metadata)

    def log_assistant_message(self, content: str, session_id: str = None, **metadata):
        return log_message("assistant", content, session_id, metadata)

    def get_conversation(self, session_id: str):
        return get_session_history(session_id)

# Usage in any chat system
logger = ChatLogger()

# In your chat handler
def handle_message(user_input, session_id):
    logger.log_user_message(user_input, session_id=session_id)

    # Process message...
    response = generate_response(user_input)

    logger.log_assistant_message(response, session_id=session_id)
    return response
```

### Decorator Pattern

```python
def with_logging(session_id: str = None):
    """Decorator to automatically log chat interactions."""
    def decorator(func):
        def wrapper(user_message, *args, **kwargs):
            # Log user message
            log_message("user", user_message, session_id=session_id)

            # Call original function
            response = func(user_message, *args, **kwargs)

            # Log assistant response
            log_message("assistant", response, session_id=session_id)

            return response
        return wrapper
    return decorator

# Usage
@with_logging(session_id="session_123")
def chat_handler(message):
    return f"You said: {message}"
```

## Agent Prompt

```text
You have chat logging capability. All conversations are logged to a SQLite database.

When user asks to:
- Search past conversations
- Find specific messages
- Review conversation history
- Export chat logs

Use the SQLite database at ~/.chat_logs/messages.db with this schema:
- messages table (id, timestamp, session_id, sender, content, metadata)

Query examples:
1. Recent history: SELECT * FROM messages ORDER BY timestamp DESC LIMIT 50
2. Search content: SELECT * FROM messages WHERE content LIKE '%keyword%'
3. Session history: SELECT * FROM messages WHERE session_id = ? ORDER BY timestamp ASC

Always use SQL queries to retrieve information and present results clearly to the user.
```

## Best Practices

1. **Truncate long messages** to avoid database bloat (e.g., 10,000 chars)
2. **Use indexes** on timestamp, session_id, and sender for fast queries
3. **Store metadata as JSON** for flexibility
4. **Use ISO 8601 timestamps** for consistency
5. **Session IDs** help organize conversations
6. **Privacy considerations**: be mindful of storing sensitive data
7. **Regular backups**: SQLite files are easy to backup/restore

## Troubleshooting

**Database locked error:**
- Close all connections properly with `conn.close()`
- Use connection pooling for high traffic

**Large database file:**
- Run `VACUUM` to compact: `sqlite3 messages.db "VACUUM"`
- Archive old messages periodically

**Query performance:**
- Ensure indexes are created (timestamp, session_id, sender)
- Use LIMIT on queries
- Consider pagination for large result sets

## See also

- [../file-tracker/SKILL.md](../file-tracker/SKILL.md) — Track file modifications
- [../web-search-api/SKILL.md](../web-search-api/SKILL.md) — Search external content
