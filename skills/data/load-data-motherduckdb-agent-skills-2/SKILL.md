---
name: load-data
description: Load data into MotherDuck from local files, object storage, HTTPS, dataframes, or external databases. Use when choosing a MotherDuck-specific ingestion path, especially CTAS and INSERT...SELECT, bulk loading, secrets, and Postgres-endpoint versus DuckDB-client tradeoffs.
argument-hint: [source-and-target]
license: MIT
---

# Load Data into MotherDuck

Use this skill when the job is getting data into MotherDuck correctly and efficiently, not just writing one ad hoc import query.

## Source Of Truth

- Prefer current MotherDuck loading, cloud-storage, and Postgres-endpoint loading docs first.
- Use `CREATE SECRET` and cloud-storage docs for protected-object-store workflows.
- Keep the loading advice aligned with MotherDuck's documented posture:
  - batch over streaming
  - Parquet over CSV when you control the format
  - dataframe, `COPY`, CTAS, or `INSERT ... SELECT` over row-by-row inserts
  - native MotherDuck storage first unless DuckLake is explicitly required

## Default Posture

- Start by classifying the source: object storage or HTTPS, local file or local DuckDB, in-memory rows, or an external database.
- Prefer `CREATE TABLE AS SELECT` for first loads and `INSERT INTO ... SELECT` for appends.
- Use Parquet for durable bulk movement whenever you control the source format.
- Treat the Postgres endpoint as a thin-client path for server-side remote reads, not for local-file or extension-driven ingestion.
- Bootstrap the target MotherDuck database first when the ingestion tool does not create it automatically.
- Keep source storage close to the MotherDuck region when you control placement.

## Workflow

1. Identify where the source data actually lives.
2. Choose the loading path:
   - object storage or HTTPS: remote read into MotherDuck
   - local file or local DuckDB: use a DuckDB client path
   - in-memory rows: Arrow or dataframe bulk load first, batched inserts only as a fallback
   - external database: use the appropriate scan or replication path from a DuckDB-capable environment
3. Land the data into a raw or staging table with minimal transformation.
4. Validate row counts, types, and a few business aggregates immediately after the load.
5. Promote into modeled tables only after the landing step is correct.

## Open Next

- `references/INGESTION_PATTERNS.md` for format-specific options, cloud-storage secrets, Postgres-endpoint loading tradeoffs, Python dataframe paths, and advanced ingestion patterns

## Related Skills

- `connect` for choosing between the Postgres endpoint and a DuckDB client path
- `explore` for inspecting destination databases and validating landed tables
- `query` for writing CTAS, append, and validation SQL
- `model-data` for promoting landed data into staging and analytics tables
- `ducklake` only when object-storage-backed lakehouse storage is an explicit requirement
