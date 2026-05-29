---
name: searching-message-history
description: Search Telegram conversation history and stored links. Use when finding past messages, what someone said, or links shared in chats.
allowed-tools: Read, Grep, Glob, Bash
---

# Message History

**Location**: `~/.valor/telegram_history.db` (SQLite)

## Tables

**messages**: `id`, `chat_id`, `message_id`, `sender`, `content`, `timestamp`, `message_type`

**links**: `id`, `url`, `final_url`, `title`, `description`, `domain`, `sender`, `chat_id`, `message_id`, `timestamp`, `tags`, `notes`, `status`, `ai_summary`

## Query Examples

```bash
# List all chats
sqlite3 ~/.valor/telegram_history.db "SELECT chat_id, COUNT(*) as count FROM messages GROUP BY chat_id ORDER BY count DESC"

# Recent messages (all chats)
sqlite3 ~/.valor/telegram_history.db "SELECT sender, substr(content, 1, 200), timestamp FROM messages ORDER BY timestamp DESC LIMIT 10"

# Messages from specific chat
sqlite3 ~/.valor/telegram_history.db "SELECT sender, content, timestamp FROM messages WHERE chat_id = '-5240384240' ORDER BY timestamp DESC LIMIT 10"

# Messages from Valor
sqlite3 ~/.valor/telegram_history.db "SELECT chat_id, substr(content, 1, 300), timestamp FROM messages WHERE sender='Valor' ORDER BY timestamp DESC LIMIT 10"

# Search by keyword
sqlite3 ~/.valor/telegram_history.db "SELECT sender, content, timestamp FROM messages WHERE content LIKE '%keyword%' ORDER BY timestamp DESC LIMIT 10"

# Search in specific chat
sqlite3 ~/.valor/telegram_history.db "SELECT sender, content, timestamp FROM messages WHERE chat_id = '-5240384240' AND content LIKE '%keyword%' ORDER BY timestamp DESC"
```

## Links

```bash
# Recent links
sqlite3 ~/.valor/telegram_history.db "SELECT url, title, sender, chat_id, timestamp FROM links ORDER BY timestamp DESC LIMIT 10"

# Links from specific chat
sqlite3 ~/.valor/telegram_history.db "SELECT url, title, sender FROM links WHERE chat_id = '-5240384240' ORDER BY timestamp DESC"

# Search links
sqlite3 ~/.valor/telegram_history.db "SELECT url, title, ai_summary FROM links WHERE title LIKE '%keyword%' OR ai_summary LIKE '%keyword%'"
```

## Note

The file `/Users/valorengels/src/ai/data/telegram_history.db` is NOT used. Always use `~/.valor/telegram_history.db`.
