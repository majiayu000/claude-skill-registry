---
name: sqlite
description: Integrates SQLite embedded database with Node.js using better-sqlite3 for synchronous operations or the native Node.js SQLite module. Use when building applications with local storage, embedded databases, or when user mentions SQLite, better-sqlite3, or embedded SQL.
---

# SQLite

Embedded SQL database for Node.js with zero configuration and serverless architecture.

## Quick Start

```bash
# Install better-sqlite3 (recommended)
npm install better-sqlite3
npm install -D @types/better-sqlite3

# Or use native Node.js SQLite (experimental, Node 22.5+)
# No installation needed, but requires --experimental-sqlite flag
```

## better-sqlite3

### Connection

```typescript
import Database from 'better-sqlite3';

// Open database (creates if doesn't exist)
const db = new Database('app.db');

// With options
const db = new Database('app.db', {
  readonly: false,
  fileMustExist: false,
  timeout: 5000,
  verbose: console.log, // Log all queries
});

// In-memory database
const memDb = new Database(':memory:');

// Enable WAL mode for better concurrency
db.pragma('journal_mode = WAL');

// Close on exit
process.on('exit', () => db.close());
process.on('SIGHUP', () => process.exit(128 + 1));
process.on('SIGINT', () => process.exit(128 + 2));
process.on('SIGTERM', () => process.exit(128 + 15));
```

### Schema Setup

```typescript
// Create tables
db.exec(`
  CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT DEFAULT 'user' CHECK(role IN ('user', 'admin')),
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
  );

  CREATE TABLE IF NOT EXISTS posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT,
    author_id INTEGER NOT NULL,
    published INTEGER DEFAULT 0,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (author_id) REFERENCES users(id) ON DELETE CASCADE
  );

  CREATE INDEX IF NOT EXISTS idx_posts_author ON posts(author_id);
  CREATE INDEX IF NOT EXISTS idx_posts_published ON posts(published);
`);

// Enable foreign keys
db.pragma('foreign_keys = ON');
```

### Basic CRUD

```typescript
interface User {
  id: number;
  name: string;
  email: string;
  password_hash: string;
  role: 'user' | 'admin';
  created_at: string;
  updated_at: string;
}

// Insert
const insertUser = db.prepare(`
  INSERT INTO users (name, email, password_hash)
  VALUES (@name, @email, @password_hash)
`);

const result = insertUser.run({
  name: 'Alice',
  email: 'alice@example.com',
  password_hash: 'hashed_password',
});

console.log('Inserted ID:', result.lastInsertRowid);
console.log('Rows affected:', result.changes);

// Select one
const getUser = db.prepare('SELECT * FROM users WHERE id = ?');
const user = getUser.get(1) as User | undefined;

// Select all
const getAllUsers = db.prepare('SELECT * FROM users');
const users = getAllUsers.all() as User[];

// Select with named params
const getUserByEmail = db.prepare('SELECT * FROM users WHERE email = @email');
const user = getUserByEmail.get({ email: 'alice@example.com' }) as User | undefined;

// Update
const updateUser = db.prepare(`
  UPDATE users
  SET name = @name, updated_at = CURRENT_TIMESTAMP
  WHERE id = @id
`);

updateUser.run({ id: 1, name: 'Alice Smith' });

// Delete
const deleteUser = db.prepare('DELETE FROM users WHERE id = ?');
deleteUser.run(1);

// Iterate (memory efficient for large results)
const iterateUsers = db.prepare('SELECT * FROM users');
for (const user of iterateUsers.iterate()) {
  console.log((user as User).name);
}
```

### Prepared Statements with Types

```typescript
interface CreateUserParams {
  name: string;
  email: string;
  password_hash: string;
}

interface User {
  id: number;
  name: string;
  email: string;
  role: string;
  created_at: string;
}

// Type-safe repository
class UserRepository {
  private insertStmt = db.prepare<CreateUserParams>(`
    INSERT INTO users (name, email, password_hash)
    VALUES (@name, @email, @password_hash)
  `);

  private getByIdStmt = db.prepare<[number], User>(`
    SELECT id, name, email, role, created_at
    FROM users WHERE id = ?
  `);

  private getByEmailStmt = db.prepare<{ email: string }, User>(`
    SELECT id, name, email, role, created_at
    FROM users WHERE email = @email
  `);

  private updateStmt = db.prepare<{ id: number; name: string }>(`
    UPDATE users SET name = @name, updated_at = CURRENT_TIMESTAMP
    WHERE id = @id
  `);

  private deleteStmt = db.prepare<[number]>('DELETE FROM users WHERE id = ?');

  create(data: CreateUserParams): number {
    const result = this.insertStmt.run(data);
    return Number(result.lastInsertRowid);
  }

  getById(id: number): User | undefined {
    return this.getByIdStmt.get(id);
  }

  getByEmail(email: string): User | undefined {
    return this.getByEmailStmt.get({ email });
  }

  update(id: number, name: string): boolean {
    const result = this.updateStmt.run({ id, name });
    return result.changes > 0;
  }

  delete(id: number): boolean {
    const result = this.deleteStmt.run(id);
    return result.changes > 0;
  }
}

const userRepo = new UserRepository();
```

### Transactions

```typescript
// Implicit transaction (single statement)
db.prepare('INSERT INTO users (name, email) VALUES (?, ?)').run('Bob', 'bob@example.com');

// Explicit transaction
const insertMany = db.transaction((users: CreateUserParams[]) => {
  for (const user of users) {
    insertUser.run(user);
  }
  return users.length;
});

// Use transaction
const count = insertMany([
  { name: 'User 1', email: 'user1@example.com', password_hash: 'hash1' },
  { name: 'User 2', email: 'user2@example.com', password_hash: 'hash2' },
  { name: 'User 3', email: 'user3@example.com', password_hash: 'hash3' },
]);

// Transaction with rollback on error
const transfer = db.transaction((fromId: number, toId: number, amount: number) => {
  const from = db.prepare('SELECT balance FROM accounts WHERE id = ?').get(fromId);
  if (!from || from.balance < amount) {
    throw new Error('Insufficient funds');
  }

  db.prepare('UPDATE accounts SET balance = balance - ? WHERE id = ?').run(amount, fromId);
  db.prepare('UPDATE accounts SET balance = balance + ? WHERE id = ?').run(amount, toId);

  return { success: true };
});

try {
  transfer(1, 2, 100);
} catch (error) {
  console.error('Transfer failed:', error.message);
  // Transaction is automatically rolled back
}

// Nested transactions (savepoints)
const outerTransaction = db.transaction(() => {
  insertUser.run({ name: 'Outer', email: 'outer@example.com', password_hash: 'hash' });

  try {
    const innerTransaction = db.transaction(() => {
      insertUser.run({ name: 'Inner', email: 'inner@example.com', password_hash: 'hash' });
      throw new Error('Rollback inner');
    });
    innerTransaction();
  } catch {
    // Inner rolled back, outer continues
  }

  return 'completed';
});
```

### Aggregates and Functions

```typescript
// Built-in aggregates
const stats = db.prepare(`
  SELECT
    COUNT(*) as total,
    COUNT(CASE WHEN role = 'admin' THEN 1 END) as admins,
    MIN(created_at) as oldest,
    MAX(created_at) as newest
  FROM users
`).get();

// User-defined function
db.function('lower_case', (str: string) => str?.toLowerCase());

const result = db.prepare("SELECT lower_case(name) as name FROM users").all();

// Aggregate function
db.aggregate('concat_names', {
  start: () => [],
  step: (arr: string[], name: string) => { arr.push(name); return arr; },
  result: (arr: string[]) => arr.join(', '),
});

const names = db.prepare('SELECT concat_names(name) as names FROM users').get();
```

### Migrations

```typescript
// Simple migration system
interface Migration {
  version: number;
  name: string;
  up: string;
  down: string;
}

const migrations: Migration[] = [
  {
    version: 1,
    name: 'create_users',
    up: `
      CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
      );
    `,
    down: 'DROP TABLE users;',
  },
  {
    version: 2,
    name: 'add_user_role',
    up: `ALTER TABLE users ADD COLUMN role TEXT DEFAULT 'user';`,
    down: `ALTER TABLE users DROP COLUMN role;`,
  },
];

function migrate(db: Database.Database) {
  // Create migrations table
  db.exec(`
    CREATE TABLE IF NOT EXISTS migrations (
      version INTEGER PRIMARY KEY,
      name TEXT NOT NULL,
      applied_at TEXT DEFAULT CURRENT_TIMESTAMP
    );
  `);

  const applied = db.prepare('SELECT version FROM migrations').all() as { version: number }[];
  const appliedVersions = new Set(applied.map(m => m.version));

  const pending = migrations.filter(m => !appliedVersions.has(m.version));

  if (pending.length === 0) {
    console.log('No pending migrations');
    return;
  }

  const applyMigration = db.transaction((migration: Migration) => {
    console.log(`Applying migration ${migration.version}: ${migration.name}`);
    db.exec(migration.up);
    db.prepare('INSERT INTO migrations (version, name) VALUES (?, ?)').run(
      migration.version,
      migration.name
    );
  });

  for (const migration of pending.sort((a, b) => a.version - b.version)) {
    applyMigration(migration);
  }

  console.log(`Applied ${pending.length} migration(s)`);
}

migrate(db);
```

### Backup and Restore

```typescript
// Backup to file
db.backup('backup.db')
  .then(() => console.log('Backup complete'))
  .catch((err) => console.error('Backup failed:', err));

// Backup with progress
db.backup('backup.db').then((progress) => {
  console.log(`${progress.totalPages} pages to copy`);
}).progress(({ totalPages, remainingPages }) => {
  console.log(`Progress: ${totalPages - remainingPages}/${totalPages}`);
});

// Vacuum (reclaim space)
db.pragma('vacuum');

// Integrity check
const integrity = db.pragma('integrity_check');
if (integrity[0].integrity_check !== 'ok') {
  console.error('Database corruption detected!');
}
```

## Native Node.js SQLite (Experimental)

```typescript
// Requires Node.js 22.5+ with --experimental-sqlite flag
import { DatabaseSync } from 'node:sqlite';

// Open database
const db = new DatabaseSync(':memory:');

// Execute SQL
db.exec(`
  CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
  )
`);

// Prepared statement
const insert = db.prepare('INSERT INTO users (name) VALUES (?)');
insert.run('Alice');

const select = db.prepare('SELECT * FROM users WHERE id = ?');
const user = select.get(1);

// Close
db.close();
```

## Performance Tips

```typescript
// 1. Use WAL mode
db.pragma('journal_mode = WAL');

// 2. Batch inserts in transactions
const insertBatch = db.transaction((items: Item[]) => {
  for (const item of items) {
    insertStmt.run(item);
  }
});
insertBatch(items); // Much faster than individual inserts

// 3. Use EXPLAIN to analyze queries
const plan = db.prepare('EXPLAIN QUERY PLAN SELECT * FROM users WHERE email = ?').all('test@example.com');
console.log(plan);

// 4. Create appropriate indexes
db.exec('CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)');

// 5. Use .pluck() for single column results
const names = db.prepare('SELECT name FROM users').pluck().all();
// ['Alice', 'Bob', 'Charlie'] instead of [{name: 'Alice'}, ...]

// 6. Use .expand() for duplicate column names
const expanded = db.prepare('SELECT u.*, p.* FROM users u JOIN posts p ON u.id = p.author_id').expand().all();

// 7. Disable synchronous for speed (less safe)
db.pragma('synchronous = OFF'); // Only for non-critical data
```

## Reference Files

- [migrations.md](references/migrations.md) - Database migration patterns
- [performance.md](references/performance.md) - Optimization strategies
