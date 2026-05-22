---
name: psql
description: Run PostgreSQL queries and meta-commands via CLI
version: 1.0.0
license: MIT
compatibility: opencode
---

## Overview

CLI tool for running SQL queries and psql meta-commands against PostgreSQL databases. Each query is executed directly via the `psql` CLI - no persistent connection required.

## Prerequisites

- [bun](https://bun.sh) runtime installed
- [psql](https://www.postgresql.org/docs/current/app-psql.html) client installed
- PostgreSQL connection environment variables set in `<git-root>/.env` or exported

## Environment Variables

Set these in your `.env` file or export them:

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `PGHOST` | Yes | - | Database host |
| `PGPORT` | No | `5432` | Database port |
| `PGDATABASE` | Yes | - | Database name |
| `PGUSER` | Yes | - | Database user |
| `PGPASSWORD` | Yes | - | Database password |
| `PGSSLMODE` | No | - | SSL mode (disable, require, etc.) |

Example `.env`:
```bash
PGHOST=localhost
PGPORT=5432
PGDATABASE=myapp
PGUSER=myapp
PGPASSWORD=secret
PGSSLMODE=disable
```

## Command

### Query

Run a SQL query, meta-command, or SQL file.

```bash
bun .opencode/skill/psql/query.js <query> [options]
bun .opencode/skill/psql/query.js --file <path> [options]
```

**Arguments:**
- `query` - SQL query or meta-command to execute

**Options:**
- `--file <path>` - Execute SQL file instead of inline query
- `--tuples` - Tuples only output (no headers or row count)
- `--timeout <ms>` - Query timeout in milliseconds (default: 30000)
- `--json` - Wrap output in JSON
- `--help` - Show help

**Examples:**

```bash
# SQL queries
bun .opencode/skill/psql/query.js "SELECT * FROM users LIMIT 5;"
bun .opencode/skill/psql/query.js "SELECT COUNT(*) FROM orders WHERE status = 'pending';"

# Meta-commands
bun .opencode/skill/psql/query.js "\dt"
bun .opencode/skill/psql/query.js "\d users"
bun .opencode/skill/psql/query.js "\di"
bun .opencode/skill/psql/query.js "\l"

# Execute SQL file
bun .opencode/skill/psql/query.js --file migrations/001_create_users.sql
bun .opencode/skill/psql/query.js --file scripts/seed_data.sql

# Tuples only (for scripting/parsing)
bun .opencode/skill/psql/query.js "SELECT id FROM users;" --tuples

# With longer timeout for slow queries
bun .opencode/skill/psql/query.js "SELECT * FROM large_table;" --timeout 60000
```

---

## Common Workflows

### Explore Database Schema

```bash
# List all tables
bun .opencode/skill/psql/query.js "\dt"

# Describe a specific table
bun .opencode/skill/psql/query.js "\d users"

# Show indexes
bun .opencode/skill/psql/query.js "\di"

# Show foreign keys for a table
bun .opencode/skill/psql/query.js "\d+ orders"
```

### Run Analytical Queries

```bash
# Count records
bun .opencode/skill/psql/query.js "SELECT COUNT(*) FROM orders;"

# Group by aggregation
bun .opencode/skill/psql/query.js "SELECT status, COUNT(*) FROM orders GROUP BY status;"

# Recent activity
bun .opencode/skill/psql/query.js "SELECT * FROM orders WHERE created_at > NOW() - INTERVAL '1 day' ORDER BY created_at DESC LIMIT 10;"
```

### Database Administration

```bash
# Check table sizes
bun .opencode/skill/psql/query.js "SELECT relname, pg_size_pretty(pg_total_relation_size(relid)) FROM pg_catalog.pg_statio_user_tables ORDER BY pg_total_relation_size(relid) DESC LIMIT 10;"

# Check active connections
bun .opencode/skill/psql/query.js "SELECT count(*) FROM pg_stat_activity WHERE state = 'active';"

# List databases
bun .opencode/skill/psql/query.js "\l"
```

### Run Migrations

```bash
# Execute a migration file
bun .opencode/skill/psql/query.js --file migrations/001_create_users.sql

# Execute seed data
bun .opencode/skill/psql/query.js --file scripts/seed.sql
```

---

## Output Behavior

- Query output is displayed directly to the user in the terminal
- **Do not re-summarize or reformat query output** - the user can already see it
- Use `--tuples` for clean output without headers (useful for piping to other tools)
- Use `--json` for structured output when parsing programmatically

## Notes

- Each query is executed as a separate `psql` invocation (no persistent connection)
- Meta-commands (starting with `\`) work the same as SQL queries
- Long-running queries may need `--timeout` increased from the default 30 seconds
- The `--tuples` flag is useful when you need to parse output or pipe to other commands
