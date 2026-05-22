---
name: database-patterns
# prettier-ignore
description: SQLite operations using better-sqlite3 with prepared statements. Use when implementing CRUD operations, timestamps, and user-scoped queries with row-level security.
---

# Database Patterns

## Quick Start

```typescript
import { db } from '$lib/server/db';
import { nanoid } from 'nanoid';

// SELECT with user_id (row-level security)
const contact = db
	.prepare('SELECT * FROM contacts WHERE id = ? AND user_id = ?')
	.get(id, user_id) as Contact | undefined;

// INSERT with nanoid and timestamps
const stmt = db.prepare(
	'INSERT INTO contacts (id, user_id, name, created_at, updated_at) VALUES (?, ?, ?, ?, ?)',
);
stmt.run(nanoid(), user_id, name, Date.now(), Date.now());
```

## Core Principles

- **Prepared statements**: Use for all queries (SQL injection
  prevention)
- **ID generation**: Use `nanoid()` for all primary keys (no
  auto-increment)
- **Timestamps**: Store as Unix epoch with `Date.now()` (milliseconds)
- **Row-level security**: Always include `user_id` in WHERE clause
  (never query by ID alone)
- **Transactions**: Use for multi-table operations (all-or-nothing)
- **Synchronous**: better-sqlite3 is sync - no async/await needed

## Reference Files

- [schema.md](references/schema.md) - Complete schema with columns and
  types
- [relationships.md](references/relationships.md) - Table
  relationships and foreign keys
- [query-examples.md](references/query-examples.md) - Joins,
  transactions, and advanced patterns
