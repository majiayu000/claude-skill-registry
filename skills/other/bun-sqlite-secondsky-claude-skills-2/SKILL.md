---
name: Bun SQLite
description: Use for bun:sqlite, SQLite operations, prepared statements, transactions, and queries.
version: 1.0.0
---

# Bun SQLite

Bun has a built-in, high-performance SQLite driver via `bun:sqlite`.

## Quick Start

```typescript
import { Database } from "bun:sqlite";

// Create/open database
const db = new Database("mydb.sqlite");

// Create table
db.run(`
  CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE
  )
`);

// Insert data
db.run("INSERT INTO users (name, email) VALUES (?, ?)", ["Alice", "alice@example.com"]);

// Query data
const users = db.query("SELECT * FROM users").all();
console.log(users);

// Close
db.close();
```

## Opening Databases

```typescript
import { Database } from "bun:sqlite";

// File-based database
const db = new Database("data.sqlite");

// In-memory database
const memDb = new Database(":memory:");

// Read-only mode
const readDb = new Database("data.sqlite", { readonly: true });

// Create if not exists (default)
const createDb = new Database("new.sqlite", { create: true });

// Strict mode (recommended)
const strictDb = new Database("strict.sqlite", { strict: true });
```

## Running Queries

### Direct Execution

```typescript
// Run (for INSERT, UPDATE, DELETE, DDL)
db.run("CREATE TABLE items (id INTEGER PRIMARY KEY, name TEXT)");
db.run("INSERT INTO items (name) VALUES (?)", ["Item 1"]);
db.run("DELETE FROM items WHERE id = ?", [1]);

// Get changes info
const result = db.run("DELETE FROM items WHERE id > ?", [10]);
console.log(result.changes); // Rows affected
console.log(result.lastInsertRowid); // Last inserted ID
```

### Prepared Statements (Recommended)

```typescript
// Create prepared statement
const stmt = db.prepare("SELECT * FROM users WHERE id = ?");

// Get single row
const user = stmt.get(1);

// Get all rows
const allUsers = db.prepare("SELECT * FROM users").all();

// Get values as array
const values = db.prepare("SELECT name, email FROM users").values();
// [[name1, email1], [name2, email2], ...]

// Iterate with for...of
const iter = db.prepare("SELECT * FROM users");
for (const user of iter.iterate()) {
  console.log(user);
}
```

## Parameters

### Positional Parameters

```typescript
const stmt = db.prepare("INSERT INTO users (name, email) VALUES (?, ?)");
stmt.run("Bob", "bob@example.com");

// Or as array
stmt.run(["Charlie", "charlie@example.com"]);
```

### Named Parameters

```typescript
const stmt = db.prepare("INSERT INTO users (name, email) VALUES ($name, $email)");
stmt.run({ $name: "Dave", $email: "dave@example.com" });

// Also works with : and @
const stmt2 = db.prepare("SELECT * FROM users WHERE name = :name");
stmt2.get({ name: "Dave" }); // Note: no colon in object key
```

## Query Methods

```typescript
const stmt = db.prepare("SELECT * FROM users WHERE active = ?");

// .get() - First row or null
const first = stmt.get(true);

// .all() - All rows as array
const all = stmt.all(true);

// .values() - Rows as arrays (not objects)
const values = stmt.values(true);
// [[1, "Alice", true], [2, "Bob", true]]

// .iterate() - Iterator for memory efficiency
for (const row of stmt.iterate(true)) {
  processRow(row);
}

// .run() - Execute without returning data
db.prepare("DELETE FROM cache WHERE expires < ?").run(Date.now());
```

## Transactions

```typescript
// Simple transaction
const insertMany = db.transaction((users: { name: string; email: string }[]) => {
  const insert = db.prepare("INSERT INTO users (name, email) VALUES ($name, $email)");
  for (const user of users) {
    insert.run(user);
  }
  return users.length;
});

const count = insertMany([
  { name: "User1", email: "user1@example.com" },
  { name: "User2", email: "user2@example.com" },
]);

// Transaction modes
const tx = db.transaction(() => {
  db.run('INSERT INTO users (name, email) VALUES (?, ?)', ['Alice', 'alice@example.com']);
  db.run('UPDATE accounts SET balance = balance - 100 WHERE user_id = ?', [1]);
});

tx.deferred();   // Default: defer lock until first write
tx.immediate();  // Lock immediately on transaction start
tx.exclusive();  // Exclusive lock, blocks all other connections
```

## Batch Operations

```typescript
// WAL mode for better concurrent performance
db.run("PRAGMA journal_mode = WAL");

// Bulk insert with transaction
const insertBulk = db.transaction((items: string[]) => {
  const stmt = db.prepare("INSERT INTO items (name) VALUES (?)");
  for (const item of items) {
    stmt.run(item);
  }
});

insertBulk(["A", "B", "C", "D", "E"]);
```

## Column Types

```typescript
// SQLite types map to JavaScript
/*
  SQLite      JavaScript
  ------      ----------
  INTEGER     number | bigint
  REAL        number
  TEXT        string
  BLOB        Uint8Array
  NULL        null
*/

// Handle BigInt for large integers
const bigStmt = db.prepare("SELECT COUNT(*) as count FROM users");
const result = bigStmt.get();
// result.count may be bigint if > Number.MAX_SAFE_INTEGER

// Store/retrieve Uint8Array
db.run("INSERT INTO files (data) VALUES (?)", [new Uint8Array([1, 2, 3])]);
const file = db.prepare("SELECT data FROM files WHERE id = ?").get(1);
// file.data is Uint8Array
```

## Column Definitions

```typescript
// Get column info
const stmt = db.prepare("SELECT * FROM users");
const columns = stmt.columnNames;
// ["id", "name", "email"]

// Type annotations (Bun extension)
const typedStmt = db.prepare<{ id: number; name: string }, [number]>(
  "SELECT id, name FROM users WHERE id = ?"
);
const user = typedStmt.get(1);
// user is typed as { id: number; name: string } | null
```

## Error Handling

```typescript
import { Database, SQLiteError } from "bun:sqlite";

try {
  db.run("INSERT INTO users (email) VALUES (?)", ["duplicate@example.com"]);
} catch (error) {
  if (error instanceof SQLiteError) {
    console.error("SQLite error:", error.code, error.message);
    // error.code: "SQLITE_CONSTRAINT_UNIQUE"
  }
  throw error;
}
```

## Database Management

```typescript
// Close database
db.close();

// Check if open
console.log(db.inTransaction); // Is in transaction

// Serialize to buffer
const buffer = db.serialize();
await Bun.write("backup.sqlite", buffer);

// Load from buffer
const data = await Bun.file("backup.sqlite").arrayBuffer();
const restored = Database.deserialize(data);

// Filename
console.log(db.filename); // Path or ":memory:"
```

## Common Patterns

### Repository Pattern

```typescript
import { Database } from "bun:sqlite";

interface User {
  id: number;
  name: string;
  email: string;
}

class UserRepository {
  private db: Database;
  private stmts: {
    findById: ReturnType<Database["prepare"]>;
    findAll: ReturnType<Database["prepare"]>;
    create: ReturnType<Database["prepare"]>;
    update: ReturnType<Database["prepare"]>;
    delete: ReturnType<Database["prepare"]>;
  };

  constructor(db: Database) {
    this.db = db;
    this.stmts = {
      findById: db.prepare("SELECT * FROM users WHERE id = ?"),
      findAll: db.prepare("SELECT * FROM users"),
      create: db.prepare("INSERT INTO users (name, email) VALUES ($name, $email)"),
      update: db.prepare("UPDATE users SET name = $name, email = $email WHERE id = $id"),
      delete: db.prepare("DELETE FROM users WHERE id = ?"),
    };
  }

  findById(id: number): User | null {
    return this.stmts.findById.get(id) as User | null;
  }

  findAll(): User[] {
    return this.stmts.findAll.all() as User[];
  }

  create(user: Omit<User, "id">): number {
    const result = this.stmts.create.run(user);
    return Number(result.lastInsertRowid);
  }
}
```

## Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `SQLITE_CONSTRAINT` | Constraint violation | Check UNIQUE/FK constraints |
| `SQLITE_BUSY` | Database locked | Use WAL mode, add retry logic |
| `no such table` | Table doesn't exist | Run CREATE TABLE first |
| `database is locked` | Concurrent access | Enable WAL mode |

## Performance Tips

```sql
-- Enable WAL mode (better concurrency)
PRAGMA journal_mode = WAL;

-- Faster writes (less durable)
PRAGMA synchronous = NORMAL;

-- Increase cache size
PRAGMA cache_size = 10000;

-- Enable foreign keys
PRAGMA foreign_keys = ON;
```

## When to Load References

Load `references/pragmas.md` when:
- Performance tuning
- Journal modes
- Memory configuration

Load `references/fts.md` when:
- Full-text search
- FTS5 configuration
