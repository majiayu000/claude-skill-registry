---
name: effect-sql-db
description: Effect patterns for SQL databases (Drizzle/Kysely/Prisma): services, transactions, retries, streaming, and observability.
allowed-tools: Read, Grep, Glob, Edit, Write
---

# SQL & Databases

## When to use
- You are integrating a SQL client (Drizzle, Kysely, Prisma, mysql2/pg) with Effect
- You want typed errors, retries, transactions, and observability

## Provide DB config via Layer
```ts
import { Config, Effect, Layer } from "effect"

class DbConfig extends Effect.Service<DbConfig>()("DbConfig", {
  sync: () => ({
    url: process.env.DATABASE_URL ?? ""
  })
}){}

// Provide once at app boundary
export const DbConfigLive = DbConfig.Default
```

## Wrap a client in a Service (typed errors)
```ts
import { Effect } from "effect"

class DatabaseError extends Data.TaggedError("DatabaseError")<{ cause: unknown }>{}

export class Database extends Effect.Service<Database>()("Database", {
  effect: Effect.gen(function* () {
    // drizzle() / new PrismaClient() / kysely instance
    const client = makeDbClient() // your factory (validated url)
    return {
      // use-pattern ensures client is passed from a single place
      use: <A>(cb: (c: typeof client) => Promise<A>) =>
        Effect.tryPromise({ try: () => cb(client), catch: (cause) => new DatabaseError({ cause }) })
    }
  })
}){}
```

## Real-world snippet: Drizzle wrapper with `use(cb)`
```ts
// Pattern adapted from Cap
export class Database extends Effect.Service<Database>()("Database", {
  effect: Effect.gen(function* () {
    return {
      use: <T>(cb: (_: DbClient) => Promise<T>) =>
        Effect.tryPromise({ try: () => cb(db()), catch: (cause) => new DatabaseError({ cause }) })
    }
  })
}){}
```

## Transactions with retry-on-deadlock
```ts
// Generic transactional helper with selective retry
const isDeadlock = (e: unknown) => typeof e === "object" && e !== null && (e as any).code === "1213" // MySQL

export const transactional = <A>(eff: Effect.Effect<A, DatabaseError, Database>) =>
  Effect.gen(function* () {
    const db = yield* Database
    return yield* Effect.tryPromise({
      try: () => db.use((c) => c.transaction(async (tx) => await Effect.runPromise(eff))),
      catch: (cause) => new DatabaseError({ cause })
    })
  }).pipe(
    Effect.retry({ schedule: Schedule.exponential("100 millis"), times: 3, while: isDeadlock })
  )
```

## Query helpers (Drizzle examples)
```ts
// Fallback to existing column if value is undefined
export const updateIfDefined = <T>(v: T | undefined, col: AnyMySqlColumn) =>
  sql`COALESCE(${v === undefined ? sql`NULL` : v}, ${col})`

// JSON_EXTRACT helper that returns string | undefined
export function jsonExtractString(column: MySqlColumn<any>, field: string) {
  return sql<string | undefined>`JSON_UNQUOTE(JSON_EXTRACT(${column}, ${`$.${field}`}))`
}
```

## Streaming large result sets
```ts
// If your driver supports async iteration over rows
const rowsAsync = client.executeStream("SELECT * FROM events") // placeholder
const stream = Stream.fromAsyncIterable(rowsAsync).pipe(
  Stream.mapEffect(processRow, { concurrency: 16 })
)
yield* Stream.runDrain(stream)
```

## Observability: spans and slow query logging
```ts
const withSqlSpan = <A, E, R>(name: string, eff: Effect.Effect<A, E, R>) =>
  eff.pipe(Effect.withSpan(name, { attributes: { "db.system": "mysql" } }))

const logSlow = <A, E, R>(thresholdMs: number, eff: Effect.Effect<A, E, R>) =>
  Effect.timed(eff).pipe(
    Effect.tap(([d]) => Duration.toMillis(d) > thresholdMs ? Effect.logWarning(`slow query: ${Duration.toMillis(d)}ms`) : Effect.void),
    Effect.map(([_, a]) => a)
  )
```

## Testing patterns
```ts
// Provide an in-memory or test DB client via Layer
export const DatabaseTest = Layer.succeed(Database, {
  use: <A>(cb: (c: any) => Promise<A>) => Effect.tryPromise({ try: () => cb(makeTestDb()), catch: (cause) => new DatabaseError({ cause }) })
})

// Or fully mock repository methods at the service boundary
```

## Guidance
- Centralize DB usage in a service; callers never touch the client directly
- Map low-level driver errors to a single DatabaseError; consider domain mapping at repository layer
- Use transactions for multi-row invariants; add retry policy for deadlocks/timeouts
- Always add timeouts for long-running operations; log slow queries
- Keep queries in repositories; route/handler stays thin

## Pitfalls
- Leaking raw client/connection across layers → hard to test and observe
- No retry on deadlocks/timeouts → transient failures bubble to users
- Building SQL strings manually → prefer query builder/typed ORM where possible

## Cross-links
- Resources & Scope for wrapping external clients and spans
- Errors & Retries for selective retry policies
- Config & Schema for validated DB configuration

## Local Source Reference

**CRITICAL: Search local Effect source before implementing**

The full Effect source code is available at `docs/effect-source/`. Always search the actual implementation before writing Effect code.

### Key Source Files
- SqlClient: `docs/effect-source/sql/src/SqlClient.ts`
- SqlConnection: `docs/effect-source/sql/src/SqlConnection.ts`
- SqlResolver: `docs/effect-source/sql/src/SqlResolver.ts`
- Drizzle integration: `docs/effect-source/sql-drizzle/src/`
- SQLite Node: `docs/effect-source/sql-sqlite-node/src/`

### Example Searches
```bash
# Find SqlClient patterns
grep -F "SqlClient" docs/effect-source/sql/src/SqlClient.ts

# Study transaction patterns
grep -rF "withTransaction" docs/effect-source/sql/src/

# Find Drizzle integration
grep -rF "export" docs/effect-source/sql-drizzle/src/

# Look at SQL test examples
grep -rF "SqlClient." docs/effect-source/sql/test/
```

### Workflow
1. Identify the SQL API you need (e.g., SqlClient, transactions)
2. Search `docs/effect-source/sql/src/` for the implementation
3. Study the types and transaction patterns
4. Look at test files for usage examples
5. Write your code based on real implementations

**Real source code > documentation > assumptions**

## References
- Agent Skills overview: https://www.anthropic.com/news/skills
- Skills guide: https://docs.claude.com/en/docs/claude-code/skills
- EffectPatterns: https://github.com/PaulJPhilp/EffectPatterns

