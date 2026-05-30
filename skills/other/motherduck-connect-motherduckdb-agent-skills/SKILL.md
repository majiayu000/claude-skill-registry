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

## Runtime Selection

Pick the connection method (above) and the runtime separately. The runtime is what actually executes queries: an MCP server, a Python script, a Node script, or the DuckDB CLI.

Classify the workload first:

- **Ad-hoc / exploration**: one-shot, interactive, may be discarded. No artifact ships.
- **Recurring / pipeline**: scheduled, version-controlled, runs unattended. Code is checked into a repo.

Then resolve in this order, stopping at the first match:

1. **MotherDuck MCP available + workload is ad-hoc** → use the MCP tools (`query`, `list_databases`, `list_tables`, `list_columns`, `search_catalog`). No client to install. Stop here.
2. **`uv` is installed** (`command -v uv`) → run scripts via `uv run --with "duckdb==<version>" script.py`. Preferred for both ad-hoc scripts and pipelines because dependencies are declared inline and reproducible.
3. **`python3` + `pip` available** → `pip install "duckdb==<version>"` inside a project-managed venv.
4. **`node` + `npm` available** → `npm install @duckdb/node-api@<version>`.
5. **None of the above** → install the DuckDB CLI: `curl -s https://install.motherduck.com | env -u motherduck_token HOME="$install_home" sh`. Pick `$install_home` as a writable, project-local path (for example `./.duckdb`) rather than polluting the user's home.

If the host project already declares a language (a `pyproject.toml`, `package.json`, or similar lockfile is present), follow that language even if the priority order would suggest otherwise. Do not introduce a second runtime alongside an existing one.

Before any install step, fetch `https://motherduck.com/docs/duckdb-versions.json` and pick the highest MotherDuck-supported DuckDB version. Pin that version explicitly in the install command. Latest upstream DuckDB is **not** automatically supported on MotherDuck.

## Workflow

1. Choose one connection method and do not mix methods in the same application.
2. Put the MotherDuck token in environment-managed secrets, not in source code.
3. Establish the connection with explicit SSL settings where required.
4. Verify the connection with `SELECT 1 AS connected` and then list reachable tables.
5. If the workload is read-heavy and concurrent, evaluate read scaling and `session_hint`.

## Open Next

- `references/CONNECTION_GUIDE.md` for connection-method selection, PG endpoint and native DuckDB examples, token handling, read scaling, attach modes, and common failure modes
- `references/RUNTIME_SELECTION.md` for the MCP-vs-Python-vs-Node-vs-CLI decision tree, detection commands, install snippets, and the DuckDB version-pinning workflow

## Related Skills

- `motherduck-explore` for discovering databases, tables, columns, and shares after the connection is established
- `motherduck-query` for executing DuckDB SQL against the connected databases
- `motherduck-duckdb-sql` for DuckDB syntax and function lookup support
