---
name: postgres-drizzle
description: PostgreSQL and Drizzle ORM best practices. Use when writing database schemas, queries, migrations, or any database-related code. Triggers on mentions of PostgreSQL, Postgres, Drizzle, database, schema, tables, columns, indexes, queries, migrations, ORM, relations, joins, transactions, or SQL. Proactively apply when creating APIs, backends, or data models.
---

# PostgreSQL + Drizzle ORM Best Practices

Type-safe database applications with PostgreSQL 18 and Drizzle ORM.

## Directory Structure

```
src/db/
├── schema/
│   ├── index.ts      # Re-export all tables
│   ├── users.ts      # User table + relations
│   └── posts.ts      # Post table + relations
├── db.ts             # Database connection
└── migrate.ts        # Migration runner
drizzle/
└── migrations/       # Generated SQL migrations
drizzle.config.ts     # drizzle-kit configuration
```

## Essential Commands

```bash
npx drizzle-kit generate   # Generate migration from schema
npx drizzle-kit migrate    # Apply migrations
npx drizzle-kit push       # Push schema directly (dev only)
npx drizzle-kit studio     # Database browser
```

## PostgreSQL 18 Highlights

| Feature | Benefit |
|---------|---------|
| **UUIDv7** | Timestamp-ordered UUIDs, better index performance |
| **Async I/O** | Up to 3x faster sequential scans |
| **Index Skip Scan** | ~40% faster queries on composite indexes |
| **RETURNING OLD/NEW** | Access previous values in UPDATE/DELETE |

## Performance Checklist

- [ ] Use `uuidv7()` for primary keys (PG18+) or `defaultRandom()`
- [ ] Create indexes on foreign keys
- [ ] Use partial indexes for filtered subsets
- [ ] Use relational queries API to avoid N+1
- [ ] Configure connection pooling in production
- [ ] Run `EXPLAIN (ANALYZE, BUFFERS)` for slow queries

---

## Code Examples

Complete, runnable examples in the `examples/` directory:

### TypeScript (Drizzle ORM)

| File | Description |
|------|-------------|
| **Schema** | |
| `examples/typescript/schema/users.ts` | User table with timestamps, soft delete |
| `examples/typescript/schema/posts.ts` | Posts with foreign key, indexes |
| `examples/typescript/schema/many-to-many.ts` | Junction table pattern |
| `examples/typescript/schema/enums-jsonb.ts` | Enums and typed JSONB |
| **Queries** | |
| `examples/typescript/queries/select.ts` | Filters, pagination, search |
| `examples/typescript/queries/joins.ts` | Left/inner/multiple joins |
| `examples/typescript/queries/aggregations.ts` | Count, sum, group by |
| `examples/typescript/queries/mutations.ts` | Insert, update, delete, upsert |
| `examples/typescript/queries/transactions.ts` | Transactions, savepoints |
| **Relations** | |
| `examples/typescript/relations/relational-queries.ts` | Nested queries, column selection |
| **Migrations** | |
| `examples/typescript/migrations/drizzle.config.ts` | drizzle-kit configuration |
| `examples/typescript/migrations/migrate.ts` | Programmatic migration runner |
| `examples/typescript/migrations/seed.ts` | Database seeding |
| **Setup** | |
| `examples/typescript/db.ts` | Connection with pooling |

### SQL (PostgreSQL)

| File | Description |
|------|-------------|
| `examples/sql/indexes.sql` | B-tree, partial, covering, GIN indexes |
| `examples/sql/partitioning.sql` | Range, list, hash partitioning |
| `examples/sql/rls.sql` | Row-level security policies |
| `examples/sql/jsonb.sql` | JSONB operators, functions, indexing |
| `examples/sql/pg18-features.sql` | UUIDv7, async I/O, RETURNING OLD/NEW |

---

## Reference Documentation

Detailed explanations in `references/`:

- **[SCHEMA.md](references/SCHEMA.md)** - Column types, constraints, patterns
- **[QUERIES.md](references/QUERIES.md)** - Operators, joins, aggregations
- **[RELATIONS.md](references/RELATIONS.md)** - One-to-many, many-to-many, relational API
- **[MIGRATIONS.md](references/MIGRATIONS.md)** - drizzle-kit workflows
- **[POSTGRES.md](references/POSTGRES.md)** - PostgreSQL 18 features, RLS, partitioning
- **[PERFORMANCE.md](references/PERFORMANCE.md)** - Indexing, optimization, pooling
- **[CHEATSHEET.md](references/CHEATSHEET.md)** - Quick reference

---

## Resources

- **Drizzle Docs**: https://orm.drizzle.team
- **PostgreSQL Docs**: https://www.postgresql.org/docs/18/
- **Drizzle Studio**: `npx drizzle-kit studio`
