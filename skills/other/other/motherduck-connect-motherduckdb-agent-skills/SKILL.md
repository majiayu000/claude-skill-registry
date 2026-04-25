---
name: motherduck-connect
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

- Start with the PG endpoint for backend applications, BI tools, and serverless runtimes that want PostgreSQL wire compatibility.
- For BI tools, treat the PG endpoint as the compatibility path for Power BI and Tableau Cloud when current docs list them as supported.
- Use the native DuckDB API only when you need local files, hybrid local/cloud execution, or direct DuckDB control.
- Use `md:` workspace connections for multi-database exploration, bootstrap flows, and temporary validation environments.
- Reuse an existing connection, connector, or environment-managed token when the user's context already provides one; do not ask for secrets that can be discovered from the active workspace.
- Start with one connection. Add pooling or read scaling only when real concurrent-read pressure exists.
- Use native DuckDB `custom_user_agent` where supported; for PG endpoint clients, prefer the client's `application_name` setting when available.

## Workflow

1. Choose one connection method and do not mix methods in the same application.
2. Put the MotherDuck token in environment-managed secrets, not in source code.
3. Establish the connection with explicit SSL settings where required.
4. Verify the connection with `SELECT 1 AS connected` and then list reachable tables.
5. If the workload is read-heavy and concurrent, evaluate read scaling and `session_hint`.

## Open Next

- `references/CONNECTION_GUIDE.md` for connection-method selection, PG endpoint and native DuckDB examples, token handling, read scaling, attach modes, and common failure modes

## Related Skills

- `motherduck-explore` for discovering databases, tables, columns, and shares after the connection is established
- `motherduck-query` for executing DuckDB SQL against the connected databases
- `motherduck-duckdb-sql` for DuckDB syntax and function lookup support
