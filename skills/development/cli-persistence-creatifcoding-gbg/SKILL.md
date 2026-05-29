---
name: cli-persistence
description: SQLite storage patterns for Effect CLI using @effect/sql-sqlite-bun. Covers schema migrations, repositories, and transactional operations.
model_invoked: true
triggers:
  - "SQLite"
  - "cli storage"
  - "persistence"
  - "database CLI"
  - "@effect/sql"
  - "sql-sqlite-bun"
---

# CLI Persistence Patterns

SQLite storage patterns using `@effect/sql-sqlite-bun` for Effect CLI applications.

## Quick Start

```typescript
#!/usr/bin/env bun
import { SqliteClient } from "@effect/sql-sqlite-bun"
import { SqlClient } from "@effect/sql"
import { Effect, Layer } from "effect"

// Database path
const DB_PATH = `${process.env.HOME}/.myapp/data.db`

// Create SQLite layer
const SqliteLive = SqliteClient.layer({
  filename: DB_PATH,
})

// Use in commands
const myCommand = Command.make("cmd", {}, () =>
  Effect.gen(function* () {
    const sql = yield* SqlClient.SqlClient
    const rows = yield* sql`SELECT * FROM items`
    yield* Console.log(JSON.stringify(rows, null, 2))
  })
)

// Provide layer
pipe(
  program,
  Effect.provide(Layer.mergeAll(NodeContext.layer, SqliteLive)),
  NodeRuntime.runMain
)
```

---

## Schema Initialization

### Pattern: Idempotent Table Creation

```typescript
const initializeSchema = Effect.gen(function* () {
  const sql = yield* SqlClient.SqlClient

  // Main table
  yield* sql`
    CREATE TABLE IF NOT EXISTS sessions (
      id TEXT PRIMARY KEY,
      topic TEXT NOT NULL,
      status TEXT NOT NULL DEFAULT 'active',
      created_at TEXT NOT NULL DEFAULT (datetime('now')),
      updated_at TEXT NOT NULL DEFAULT (datetime('now'))
    )
  `

  // Related table with foreign key
  yield* sql`
    CREATE TABLE IF NOT EXISTS sources (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      session_id TEXT NOT NULL,
      type TEXT NOT NULL,
      url TEXT,
      content TEXT,
      created_at TEXT NOT NULL DEFAULT (datetime('now')),
      FOREIGN KEY (session_id) REFERENCES sessions(id) ON DELETE CASCADE
    )
  `

  // Indexes for common queries
  yield* sql`
    CREATE INDEX IF NOT EXISTS idx_sessions_status
    ON sessions(status)
  `

  yield* sql`
    CREATE INDEX IF NOT EXISTS idx_sessions_topic
    ON sessions(topic)
  `
})
```

### Pattern: Run at Startup

```typescript
const program = Effect.gen(function* () {
  // Initialize schema first
  yield* initializeSchema

  // Then run CLI
  yield* cli(process.argv)
})

pipe(
  program,
  Effect.provide(Layer.mergeAll(NodeContext.layer, SqliteLive)),
  NodeRuntime.runMain
)
```

---

## CRUD Operations

### Create

```typescript
const createSession = (topic: string, type: SessionType) =>
  Effect.gen(function* () {
    const sql = yield* SqlClient.SqlClient
    const id = crypto.randomUUID()

    yield* sql`
      INSERT INTO sessions (id, topic, type, status)
      VALUES (${id}, ${topic}, ${type}, 'active')
    `

    return id
  })
```

### Read (Single)

```typescript
const getSession = (id: string) =>
  Effect.gen(function* () {
    const sql = yield* SqlClient.SqlClient

    const rows = yield* sql`
      SELECT * FROM sessions WHERE id = ${id}
    `

    if (rows.length === 0) {
      return yield* Effect.fail(
        new SessionNotFoundError({
          id,
          suggestion: "Use 'list' to see available sessions",
        })
      )
    }

    return rows[0] as Session
  })
```

### Read (List with Filters)

```typescript
const listSessions = (
  status?: string,
  limit: number = 20
) =>
  Effect.gen(function* () {
    const sql = yield* SqlClient.SqlClient

    // Dynamic filtering
    if (status) {
      return yield* sql`
        SELECT * FROM sessions
        WHERE status = ${status}
        ORDER BY updated_at DESC
        LIMIT ${limit}
      `
    }

    return yield* sql`
      SELECT * FROM sessions
      ORDER BY updated_at DESC
      LIMIT ${limit}
    `
  })
```

### Update

```typescript
const updateSession = (
  id: string,
  updates: { topic?: string; status?: string }
) =>
  Effect.gen(function* () {
    const sql = yield* SqlClient.SqlClient

    // Verify exists first
    yield* getSession(id)

    // Build update dynamically
    if (updates.topic) {
      yield* sql`
        UPDATE sessions
        SET topic = ${updates.topic}, updated_at = datetime('now')
        WHERE id = ${id}
      `
    }

    if (updates.status) {
      yield* sql`
        UPDATE sessions
        SET status = ${updates.status}, updated_at = datetime('now')
        WHERE id = ${id}
      `
    }

    return yield* getSession(id)
  })
```

### Delete

```typescript
const deleteSession = (id: string) =>
  Effect.gen(function* () {
    const sql = yield* SqlClient.SqlClient

    // Verify exists
    yield* getSession(id)

    // Delete (cascade will handle related records)
    yield* sql`DELETE FROM sessions WHERE id = ${id}`
  })
```

---

## Search Patterns

### Full-Text Search (Simple)

```typescript
const searchSessions = (query: string) =>
  Effect.gen(function* () {
    const sql = yield* SqlClient.SqlClient
    const pattern = `%${query}%`

    return yield* sql`
      SELECT * FROM sessions
      WHERE topic LIKE ${pattern}
         OR notes LIKE ${pattern}
      ORDER BY updated_at DESC
    `
  })
```

### Full-Text Search (FTS5)

```typescript
// Schema setup
const initFTS = Effect.gen(function* () {
  const sql = yield* SqlClient.SqlClient

  yield* sql`
    CREATE VIRTUAL TABLE IF NOT EXISTS sessions_fts USING fts5(
      id,
      topic,
      notes,
      content='sessions',
      content_rowid='rowid'
    )
  `

  // Triggers to keep FTS in sync
  yield* sql`
    CREATE TRIGGER IF NOT EXISTS sessions_ai AFTER INSERT ON sessions BEGIN
      INSERT INTO sessions_fts(rowid, id, topic, notes)
      VALUES (new.rowid, new.id, new.topic, new.notes);
    END
  `
})

// Search using FTS
const searchFTS = (query: string) =>
  Effect.gen(function* () {
    const sql = yield* SqlClient.SqlClient

    return yield* sql`
      SELECT s.* FROM sessions s
      JOIN sessions_fts fts ON s.id = fts.id
      WHERE sessions_fts MATCH ${query}
      ORDER BY rank
    `
  })
```

---

## Transactions

### Pattern: Atomic Multi-Table Operations

```typescript
const createSessionWithSources = (
  topic: string,
  sources: Array<{ type: string; url: string }>
) =>
  Effect.gen(function* () {
    const sql = yield* SqlClient.SqlClient
    const id = crypto.randomUUID()

    // Wrap in transaction
    yield* sql.withTransaction(
      Effect.gen(function* () {
        // Create session
        yield* sql`
          INSERT INTO sessions (id, topic, status)
          VALUES (${id}, ${topic}, 'active')
        `

        // Create all sources
        for (const source of sources) {
          yield* sql`
            INSERT INTO sources (session_id, type, url)
            VALUES (${id}, ${source.type}, ${source.url})
          `
        }
      })
    )

    return id
  })
```

---

## Repository Pattern

### Service Definition

```typescript
import { Context, Effect, Layer } from "effect"

// Repository interface
interface SessionRepository {
  readonly create: (topic: string) => Effect.Effect<string, CreateError>
  readonly get: (id: string) => Effect.Effect<Session, NotFoundError>
  readonly list: (opts?: ListOptions) => Effect.Effect<Session[]>
  readonly update: (id: string, data: UpdateData) => Effect.Effect<Session>
  readonly delete: (id: string) => Effect.Effect<void, NotFoundError>
  readonly search: (query: string) => Effect.Effect<Session[]>
}

// Service tag
class SessionRepository extends Context.Tag("SessionRepository")<
  SessionRepository,
  SessionRepository
>() {}

// Implementation
const SessionRepositoryLive = Layer.effect(
  SessionRepository,
  Effect.gen(function* () {
    const sql = yield* SqlClient.SqlClient

    return {
      create: (topic) =>
        Effect.gen(function* () {
          const id = crypto.randomUUID()
          yield* sql`INSERT INTO sessions (id, topic) VALUES (${id}, ${topic})`
          return id
        }),

      get: (id) =>
        Effect.gen(function* () {
          const rows = yield* sql`SELECT * FROM sessions WHERE id = ${id}`
          if (rows.length === 0) {
            return yield* Effect.fail(new NotFoundError({ id }))
          }
          return rows[0] as Session
        }),

      list: (opts = {}) =>
        Effect.gen(function* () {
          const limit = opts.limit ?? 20
          return yield* sql`
            SELECT * FROM sessions
            ORDER BY updated_at DESC
            LIMIT ${limit}
          `
        }),

      update: (id, data) =>
        Effect.gen(function* () {
          yield* sql`
            UPDATE sessions
            SET topic = COALESCE(${data.topic}, topic),
                status = COALESCE(${data.status}, status),
                updated_at = datetime('now')
            WHERE id = ${id}
          `
          return yield* SessionRepository.get(id)
        }),

      delete: (id) =>
        Effect.gen(function* () {
          const result = yield* sql`DELETE FROM sessions WHERE id = ${id}`
          if (result.rowsAffected === 0) {
            return yield* Effect.fail(new NotFoundError({ id }))
          }
        }),

      search: (query) =>
        Effect.gen(function* () {
          const pattern = `%${query}%`
          return yield* sql`
            SELECT * FROM sessions WHERE topic LIKE ${pattern}
          `
        }),
    }
  })
)
```

### Usage in Commands

```typescript
const listCommand = Command.make("list", {}, () =>
  Effect.gen(function* () {
    const repo = yield* SessionRepository
    const sessions = yield* repo.list()
    yield* Console.log(formatTable(sessions))
  })
)

// Layer composition
const AppLayer = Layer.mergeAll(
  NodeContext.layer,
  SqliteLive,
  SessionRepositoryLive
)
```

---

## Migrations

### Pattern: Version-Based Migrations

```typescript
const MIGRATIONS = [
  {
    version: 1,
    up: (sql: SqlClient) => sql`
      CREATE TABLE sessions (
        id TEXT PRIMARY KEY,
        topic TEXT NOT NULL,
        created_at TEXT DEFAULT (datetime('now'))
      )
    `,
  },
  {
    version: 2,
    up: (sql: SqlClient) => sql`
      ALTER TABLE sessions ADD COLUMN status TEXT DEFAULT 'active'
    `,
  },
  {
    version: 3,
    up: (sql: SqlClient) => sql`
      CREATE INDEX idx_sessions_status ON sessions(status)
    `,
  },
]

const runMigrations = Effect.gen(function* () {
  const sql = yield* SqlClient.SqlClient

  // Create migrations table
  yield* sql`
    CREATE TABLE IF NOT EXISTS _migrations (
      version INTEGER PRIMARY KEY,
      applied_at TEXT DEFAULT (datetime('now'))
    )
  `

  // Get current version
  const rows = yield* sql`
    SELECT COALESCE(MAX(version), 0) as version FROM _migrations
  `
  const currentVersion = rows[0].version as number

  // Apply pending migrations
  for (const migration of MIGRATIONS) {
    if (migration.version > currentVersion) {
      yield* Console.log(`Applying migration v${migration.version}...`)
      yield* migration.up(sql)
      yield* sql`INSERT INTO _migrations (version) VALUES (${migration.version})`
    }
  }
})
```

---

## Anti-Patterns

### DON'T: Concatenate SQL strings

```typescript
// WRONG - SQL injection risk
const query = `SELECT * FROM sessions WHERE topic = '${userInput}'`
yield* sql.unsafe(query)

// CORRECT - Use tagged template
yield* sql`SELECT * FROM sessions WHERE topic = ${userInput}`
```

### DON'T: Forget to handle empty results

```typescript
// WRONG - Will crash on empty
const rows = yield* sql`SELECT * FROM sessions WHERE id = ${id}`
return rows[0].topic  // TypeError if empty!

// CORRECT - Check first
if (rows.length === 0) {
  return yield* Effect.fail(new NotFoundError({ id }))
}
return rows[0] as Session
```

### DON'T: Mix sync and async patterns

```typescript
// WRONG - Using raw better-sqlite3
import Database from "better-sqlite3"
const db = new Database(path)
db.exec("CREATE TABLE...")  // Sync, bypasses Effect

// CORRECT - Use SqlClient consistently
const sql = yield* SqlClient.SqlClient
yield* sql`CREATE TABLE...`
```

---

## File Locations

| Purpose | Pattern |
|---------|---------|
| DB path | `~/.appname/data.db` |
| Config | `~/.appname/config.json` |
| Logs | `~/.appname/logs/` |
| Cache | `~/.appname/cache/` |

### Ensuring Directory Exists

```typescript
import { FileSystem } from "@effect/platform"
import * as path from "node:path"

const ensureDbDir = Effect.gen(function* () {
  const fs = yield* FileSystem.FileSystem
  const dbDir = path.dirname(DB_PATH)
  yield* fs.makeDirectory(dbDir, { recursive: true })
})
```

---

## Related Skills

| Skill | Purpose |
|-------|---------|
| `cli/core` | Command definition |
| `cli/messaging` | Error formatting |
| `cli/services` | Service composition |
| `cli/config` | Configuration patterns |

---

## Quick Reference

| Operation | Pattern |
|-----------|---------|
| Get client | `yield* SqlClient.SqlClient` |
| Select | `sql\`SELECT * FROM t WHERE x = ${v}\`` |
| Insert | `sql\`INSERT INTO t (c) VALUES (${v})\`` |
| Update | `sql\`UPDATE t SET c = ${v} WHERE id = ${id}\`` |
| Delete | `sql\`DELETE FROM t WHERE id = ${id}\`` |
| Transaction | `sql.withTransaction(effect)` |
| Layer | `SqliteClient.layer({ filename: path })` |
