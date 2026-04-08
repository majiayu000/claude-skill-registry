---
name: duckdb-sql
description: DuckDB SQL reference for MotherDuck. Use when you need exact DuckDB syntax, function behavior, supported MotherDuck SQL features, or to resolve whether PostgreSQL-oriented SQL will fail on MotherDuck.
argument-hint: [syntax-or-error]
license: MIT
---

# DuckDB SQL Reference for MotherDuck

Use this skill when you need exact DuckDB syntax, function behavior, or a quick sanity check that a statement will actually work on MotherDuck.

## Source Of Truth

- Prefer current DuckDB SQL docs for language features and function semantics.
- Use current MotherDuck SQL docs for MotherDuck-only commands such as shares, secrets, snapshots, and Dive operations.
- If the connection path matters, verify behavior against the current Postgres-endpoint docs before promising server-mode support.

## Default Posture

- Write DuckDB SQL, not PostgreSQL SQL, even when the client connects through the Postgres endpoint.
- Use fully qualified `"database"."schema"."table"` names once more than one database or share is in scope.
- Prefer DuckDB-native constructs when they simplify the query: `GROUP BY ALL`, `QUALIFY`, `UNION BY NAME`, `arg_max`, `EXCLUDE`, and `REPLACE`.
- Check whether the statement depends on local files, extension install/load, temporary-table behavior, or other client-only features before claiming it will work in MotherDuck.
- Treat MotherDuck SQL as an additional surface on top of DuckDB SQL, not a replacement for it.

## Workflow

1. Confirm the connection path and whether the question is about syntax, feature support, or a specific error.
2. Write or repair the statement in DuckDB SQL first.
3. Verify any MotherDuck-only command or server-mode limitation against the current docs.
4. If the user needs exact syntax or function details, open `references/SYNTAX_REFERENCE.md`.

## Open Next

- `references/SYNTAX_REFERENCE.md` for DuckDB data types, friendly SQL features, functions, complex types, and common MotherDuck-specific gotchas

## Related Skills

- `query` for writing and validating analytical SQL against live MotherDuck data
- `connect` when syntax support depends on PG endpoint versus native DuckDB behavior
- `explore` when the problem is really missing schema context rather than missing syntax knowledge
