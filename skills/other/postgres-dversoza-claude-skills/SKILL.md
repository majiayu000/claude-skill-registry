---
name: postgres
description: Read-only PostgreSQL database querying, schema introspection, and query planning. Use when the user asks to query a database, look up data, check a table, describe a schema, list tables, show indexes, explain a query plan, or any other read-only PostgreSQL interaction. Triggers on requests like "query the users table", "show me the schema", "what tables are in staging", "run this SQL", "describe the orders table", "check the database", "how many rows in X", "explain this query".
---

# Postgres

Read-only access to PostgreSQL databases via `psql`. All connections enforce `default_transaction_read_only=on` at the server level -- writes and DDL are rejected by PostgreSQL itself.

## Connection Setup

The script resolves database aliases from a `` ```pg-databases``` `` fenced code block in the project's `CLAUDE.local.md`. It searches from the current working directory upward. Credentials never appear on the command line -- only the alias is passed as an argument.

To discover available aliases:

```bash
python3 ~/.claude/skills/postgres/scripts/pg_query.py list
```

If no `CLAUDE.local.md` exists or it has no `pg-databases` block, ask the user for connection details and suggest they add a block like this to their project's `CLAUDE.local.md`:

````markdown
```pg-databases
staging=postgres://user:pass@staging-host:5432/myapp
local=postgres://localhost:5432/myapp_dev
analytics=postgres://analyst:pass@analytics-host:5432/warehouse
```
````

Remind the user that `CLAUDE.local.md` should be in `.gitignore` to keep credentials out of version control.

Do NOT pass connection URIs on the command line. Always use the alias.

## Subcommands

All subcommands take a database alias as the first argument.

### Introspection

```bash
python3 ~/.claude/skills/postgres/scripts/pg_query.py schemas staging                    # list non-system schemas
python3 ~/.claude/skills/postgres/scripts/pg_query.py tables staging                     # list tables in public schema
python3 ~/.claude/skills/postgres/scripts/pg_query.py tables staging --schema analytics  # list tables in a specific schema
python3 ~/.claude/skills/postgres/scripts/pg_query.py describe staging users             # columns, types, nullability
python3 ~/.claude/skills/postgres/scripts/pg_query.py describe staging analytics.events  # schema-qualified table
python3 ~/.claude/skills/postgres/scripts/pg_query.py indexes staging users              # indexes on a table
```

### Queries

```bash
python3 ~/.claude/skills/postgres/scripts/pg_query.py query staging "SELECT id, name FROM users LIMIT 10"
python3 ~/.claude/skills/postgres/scripts/pg_query.py explain staging "SELECT id, name FROM users WHERE active = true"
```

All subcommands return JSON to stdout. Errors go to stderr as JSON with an `error` field.

## Query Guidelines

- Always add `LIMIT` to queries unless the user explicitly asks for all rows or the query already includes one. Default to `LIMIT 100`.
- Prefer specific columns over `SELECT *` when the table structure is known (use `describe` first if needed).
- For large result sets, suggest the user narrow the query rather than removing the limit.
- Writes are impossible: the connection is read-only at the PostgreSQL session level. If a write is attempted, psql returns `ERROR: cannot execute X in a read-only transaction`. Report this to the user and explain the read-only constraint.
- When exploring an unfamiliar database, start with `schemas` then `tables` then `describe` before running queries.
