---
name: sqlmesh
description: Use when working with SQLMesh models — creating, modifying, debugging, or running plans. Covers model creation patterns, verification workflow, debugging failures (virtual layer errors, type mismatches, missing snapshots, Python exporter issues, mixed gateways), live PG data sources, and Python utilities.
---

# SQLMesh Skill

> **Read `sqlmesh/README.md` first.** It is the single source of truth for architecture, conventions, macros, and patterns.

## Key Rules (reminders — README is canonical)

- **Filter on `start_datetime` (UTC)**, never on `start_datetime_tz`
- **Use `@start_ts` / `@end_ts`** for timestamp filters, never `@start_ds` / `@end_ds`
- **Use `@create_index()`** macro, never raw `CREATE INDEX`
- **Model `start`/`end` must include timezone offset** (`+0100` for winter boundaries)
- File name must match model name in `MODEL` block

## PostgreSQL Live Tables (data sources for archive_zone)

```
carpool_v2.carpools          # Core journey data
carpool_v2.geo               # Geographic data
carpool_v2.status            # Acquisition status
policy.incentives            # Incentive data
operator.operators           # Operator metadata
company.companies            # Company info (SIRET)
```

## Python Utilities

| Module | Purpose |
|--------|---------|
| `utils/loading.py` | Load CSV, Excel, Parquet, GeoPackage |
| `utils/cleaning.py` | Column normalization, type casting |
| `utils/s3.py` | S3 client initialization |
| `utils/export_data.py` | Query export to CSV/Parquet |
| `utils/upload.py` | S3 multipart upload |

## Verification Workflow

After any model change, always run:

```bash
cd sqlmesh

# 1. Check the rendered SQL is correct
sqlmesh render <model_name>

# 2. Preview the plan (never auto-apply without review)
sqlmesh plan dev
```

For production: `sqlmesh plan` (no env suffix).

## Quick Setup

```bash
cd sqlmesh
uv sync
cp .env.example .env  # edit with local credentials
```

## Model Creation Patterns

### SQL Model Template

```sql
MODEL (
  name schema_name.model_name,
  kind INCREMENTAL_BY_TIME_RANGE (
    time_column start_datetime,
    lookback 7,
    batch_size 30,
  ),
  start '2020-01-01',
  cron '@daily',
  grain (_id),
  tags ('zone_name'),
);

SELECT
  ...
FROM trusted_zone.journeys
WHERE valid_acquisition_status = true
  AND start_datetime BETWEEN @start_ts AND @end_ts
```

### Key Conventions

- Use `@start_ts` / `@end_ts` for timestamp filters (never `@start_ds` / `@end_ds`)
- Filter on `start_datetime` (UTC), never `start_datetime_tz`
- Use `@create_index()` macro for indexes, never raw `CREATE INDEX`
- File name must match model name in `MODEL` block
- `trusted_zone.journeys` is the standard base for refined models

---

# Debugging SQLMesh Plans

## Overview

SQLMesh plan failures cascade in non-obvious ways. The virtual layer update runs AFTER all model batches and touches ALL models — not just selected ones. A single missing snapshot table blocks the entire plan.

## Virtual Layer: The #1 Source of Failures

The virtual layer update creates/swaps views for ALL models in the project, regardless of `--select-model`. It runs only after all model batches succeed.

**Consequence:** A missing snapshot table for ANY model (even one you didn't select) blocks the entire plan.

### Diagnosing Virtual Layer Failures

```
Error: Execution failed for node SnapshotId<"db"."schema"."model": 1234567890>
```

This means SQLMesh tried to create a view pointing to a snapshot table that doesn't exist.

**Inspection (via DuckDB MCP or fetchdf):**

```sql
-- Check if the snapshot table exists
SELECT tablename FROM pg_tables
WHERE schemaname = 'raw_zone' AND tablename LIKE 'model_name%';

-- Check what views exist
SELECT viewname, definition FROM pg_views
WHERE schemaname = 'raw_zone' AND viewname = 'model_name';
```

### Fixing Missing Snapshot Tables

Materialize the specific missing model:

```bash
sqlmesh plan --restate-model 'schema.missing_model' --select-model 'schema.missing_model' --auto-apply
```

Then re-run your original plan. Repeat until the virtual layer passes all models.

**Common culprits:** DuckDB-gateway models (`read_parquet`) that were added to state but never successfully materialized.

## Chicken-and-Egg: Exporters vs Views

Python exporters query SQLMesh views via raw `psycopg2` connections (bypassing SQLMesh model resolution). If the view points to a stale snapshot:

```
Exporter fails -> plan fails -> virtual layer never runs -> view never updated
```

### Fix: Two-Stage Plan

1. Run SQL models only (exclude Python exporters):

   ```bash
   sqlmesh plan --select-model 'archive_zone.journeys_*' --select-model 'archive_zone.cee_applications' --auto-apply
   ```

2. Once views are updated, run everything:

   ```bash
   sqlmesh plan --select-model 'archive_zone.*' --auto-apply
   ```

### Fix: Make Exporters Resilient

When the exporter's `COLUMNS_TYPES` references column names, use the ACTUAL column names from the model output — not expressions against raw source tables:

```python
# BAD: references raw source columns (breaks when model already transforms them)
("st_x(end_position::geometry)", "FLOAT4", "end_position_x"),

# GOOD: references model output column directly
("end_position_x", "REAL", "end_position_x"),
```

## Type Mismatches in UNION Views

### Enum vs VARCHAR

Live PostgreSQL tables use custom enum types (`policy.incentive_status_enum`). Parquet-sourced models store these as `varchar`. UNION views mixing both fail:

```
UNION types character varying and policy.incentive_status_enum cannot be matched
```

**Fix:** Cast enum columns to `VARCHAR` in both the macro (for `_latest` models reading live PG) and the UNION view:

```sql
-- In the macro querying live PG tables:
pi.status::VARCHAR AS status,
pi.state::VARCHAR AS state

-- In the UNION view (belt-and-suspenders):
status::VARCHAR AS status,
state::VARCHAR AS state
```

### JSONB vs VARCHAR

Same pattern with `jsonb` columns from live PG vs `varchar` from parquet:

```
COALESCE types jsonb and character varying cannot be matched
```

**Fix:** Cast the parquet-sourced value to match the live type:

```sql
COALESCE(geo.geo_errors, j.geo_errors::jsonb)::jsonb AS geo_errors
```

## `--restate-model` Does NOT Pick Up Schema Changes

`--restate-model` reuses the existing snapshot definition. If you changed the model SQL (added casts, renamed columns), the old snapshot definition is still used.

**Fix:** Run a plain `sqlmesh plan` (without `--restate-model`) so SQLMesh detects the model as "Directly Modified" and creates a new snapshot with the updated definition.

## Python Module Caching

SQLMesh caches Python imports within a plan run. If you edit a shared utility file (`utils/journeys_export.py`) and re-run:

- The plan DIFF correctly shows the change
- But execution may use CACHED old code

**Fix:** The change takes effect on the NEXT plan run. If the plan detected it as "Breaking", the model will be re-run with fresh imports.

## Reserved Words as Column Names

Column names like `uuid` conflict with SQL type keywords. SQLMesh's linter can't resolve them in `read_parquet()` sources:

```
ambiguousorinvalidcolumn: Column 'uuid' could not be resolved
```

**Fix:** Use `SELECT *` for parquet sources (matching the pattern of all other raw_zone models). The `columns` block in the MODEL declaration still enforces the output schema.

## Quick Reference: Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `Execution failed for node SnapshotId<...>` | Missing snapshot table | `--restate-model` the specific model |
| `column "X" does not exist` in exporter | COLUMNS_TYPES outdated or view stale | Update COLUMNS_TYPES to match model output |
| `UNION types X and Y cannot be matched` | Enum/jsonb type vs varchar from parquet | Cast to common type (VARCHAR or jsonb) |
| `COALESCE types X and Y cannot be matched` | Same as above but in COALESCE | Cast parquet-sourced arg to match live type |
| `print() got unexpected keyword argument 'exc_info'` | `exc_info` is `logging`, not `print` | Use `print(str(e))` or `logging.error(..., exc_info=True)` |
| `relation "X" does not exist` in exporter | Model renamed but exporter not updated | Update table reference in exporter code |
| Linter: `ambiguousorinvalidcolumn` on parquet | Reserved word column name | Use `SELECT *` for parquet sources |
| `cannot drop table X because other objects depend on it` | View depends on snapshot table being replaced | Don't restate models that already have working views |

## Workflow: Debugging a Failed `sqlmesh plan`

```dot
digraph debug_flow {
  "plan fails" [shape=doublecircle];
  "virtual layer?" [shape=diamond];
  "model batch?" [shape=diamond];
  "type mismatch?" [shape=diamond];

  "find missing snapshot" [shape=box];
  "restate specific model" [shape=box];
  "check COLUMNS_TYPES" [shape=box];
  "cast enums/jsonb" [shape=box];
  "two-stage plan" [shape=box];
  "re-run plan" [shape=doublecircle];

  "plan fails" -> "virtual layer?" [label="check error"];
  "virtual layer?" -> "find missing snapshot" [label="SnapshotId error"];
  "virtual layer?" -> "model batch?" [label="no"];
  "find missing snapshot" -> "restate specific model";
  "restate specific model" -> "re-run plan";

  "model batch?" -> "type mismatch?" [label="DatatypeMismatch"];
  "model batch?" -> "check COLUMNS_TYPES" [label="UndefinedColumn"];
  "type mismatch?" -> "cast enums/jsonb" [label="UNION/COALESCE"];
  "check COLUMNS_TYPES" -> "two-stage plan" [label="stale view"];
  "cast enums/jsonb" -> "re-run plan";
  "check COLUMNS_TYPES" -> "re-run plan";
  "two-stage plan" -> "re-run plan";
}
```
