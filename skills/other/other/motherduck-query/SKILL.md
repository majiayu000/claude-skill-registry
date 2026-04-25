---
name: motherduck-query
description: Execute DuckDB SQL queries against MotherDuck databases. Use when running analytics, aggregations, transformations, or any SQL operation. Covers query best practices, CTEs, window functions, QUALIFY, and performance optimization.
license: MIT
---

# Query MotherDuck

Use this skill when executing SQL queries for analytics, aggregations, transformations, or data exploration against MotherDuck databases.

## Prerequisites

- MotherDuck connection established via `motherduck-connect`
- Target database and tables identified via `motherduck-explore`

## Default Posture

- Write DuckDB SQL, not PostgreSQL SQL, even when using the PG endpoint.
- Always use fully qualified `"database"."schema"."table"` names.
- Preserve the intended grain of every result set; state the grain before optimizing or materializing a query.
- Filter early, aggregate early, and prefer serving tables or summaries for repeated reads.
- Keep SQL obvious, multi-line, and explicit about grain, filters, and output shape.
- Treat DDL, DML, `ATTACH`, `DETACH`, and lifecycle commands such as `SHUTDOWN` as writes. Use MCP `query_rw` only when the user explicitly asks for the change and confirms it.
- Tag long-lived integrations with `custom_user_agent` when the connection path supports it.

## Workflow

1. Confirm the actual tables, columns, and grain before writing SQL.
2. Write the query in SQL first, then wrap it in Python or TypeScript only if needed.
3. Use CTEs and DuckDB-native patterns such as `GROUP BY ALL`, `QUALIFY`, and `arg_max`.
4. Check the plan, row count, and shape for pushdown, unnecessary sorts, or repeated raw rescans.
5. Materialize expensive repeated queries into serving tables or light views when warranted.

## Open Next

- `references/QUERY_PLAYBOOK.md` for DuckDB query patterns, exploration SQL, performance rules, common analytical shapes, and common mistakes

## Related Skills

- `motherduck-connect` for session setup
- `motherduck-duckdb-sql` for syntax and function reference
- `motherduck-explore` for understanding the source schema before writing queries
