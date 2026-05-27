# Database Migrations Skill

> D1 schema patterns for SaaS wrapper.

---

## Core Tables

### users
```sql
CREATE TABLE users (
  id TEXT PRIMARY KEY,
  email TEXT UNIQUE NOT NULL,
  password_hash TEXT,
  plan_id TEXT DEFAULT 'free',
  is_admin INTEGER DEFAULT 0,
  created_at TEXT DEFAULT (datetime('now'))
);
```

### n8n_connections
```sql
CREATE TABLE n8n_connections (
  id TEXT PRIMARY KEY,
  user_id TEXT NOT NULL REFERENCES users(id),
  name TEXT NOT NULL,
  n8n_url TEXT NOT NULL,
  n8n_api_key_encrypted TEXT NOT NULL,
  status TEXT DEFAULT 'active',
  created_at TEXT DEFAULT (datetime('now'))
);
```

### api_keys
```sql
CREATE TABLE api_keys (
  id TEXT PRIMARY KEY,
  user_id TEXT NOT NULL REFERENCES users(id),
  key_hash TEXT NOT NULL,
  key_prefix TEXT NOT NULL,
  created_at TEXT DEFAULT (datetime('now'))
);
```

## Commands

```bash
# Create database
wrangler d1 create cl-n8n-mcp-db

# Apply migration
wrangler d1 execute cl-n8n-mcp-db --local --file=./migrations/001.sql

# Query
wrangler d1 execute cl-n8n-mcp-db --remote --command "SELECT * FROM users"
```
