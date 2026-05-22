---
name: connect
description: Connect to MotherDuck from any application. Use when setting up database connectivity via the Postgres endpoint (recommended), pg_duckdb, native DuckDB API, or JDBC. Covers connection strings, authentication, SSL, and environment variable configuration.
argument-hint: [app-or-runtime]
license: MIT
---

# Connect to MotherDuck

Use this skill when establishing database connectivity from any application, script, or service to MotherDuck. Start here before running queries or loading data.

## Source Of Truth

- Prefer current MotherDuck connection, attach-mode, read-scaling, and multithreading docs.
- If the MotherDuck MCP `ask_docs_question` feature is available, use it first for current connection behavior.
- When it is unavailable, verify guidance against the public docs before making firm claims about connection strings, token types, or read-scaling behavior.

## Default Posture

- Start with the PG endpoint for backend applications that want PostgreSQL wire compatibility.
- Use the native DuckDB API only when you need local files, hybrid local/cloud execution, or direct DuckDB control.
- Use `md:` workspace connections for multi-database exploration, bootstrap flows, and temporary validation environments.
- Start with one connection. Add pooling or read scaling only when real concurrent-read pressure exists.
- Treat `custom_user_agent` watermarking as a native DuckDB pattern, not a PG endpoint pattern.

## Workflow

1. Choose one connection method and do not mix methods in the same application.
2. Put the MotherDuck token in environment-managed secrets, not in source code.
3. Establish the connection with explicit SSL settings where required.
4. Verify the connection with `SELECT 1 AS connected` and then list reachable tables.
5. If the workload is read-heavy and concurrent, evaluate read scaling and `session_hint`.

## Open Next

- `references/CONNECTION_GUIDE.md` for connection-method selection, PG endpoint and native DuckDB examples, token handling, read scaling, attach modes, and common failure modes

## Related Skills

- `explore` for discovering databases, tables, columns, and shares after the connection is established
- `query` for executing DuckDB SQL against the connected databases
- `duckdb-sql` for DuckDB syntax and function lookup support
