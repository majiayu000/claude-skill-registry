---
name: motherduck-create-flight
description: Create, schedule, run, and debug MotherDuck Flights — Python jobs that run on MotherDuck compute. Use whenever someone wants to create a flight, schedule a Python script or recurring job on MotherDuck, set up scheduled ingestion from Postgres, dlt sources, S3, BigQuery, Snowflake, or APIs, refresh aggregates or transformations on a cron, or operate flights with get_flight_guide, create_flight, run_flight, flight logs, secrets, schedules, and versions.
license: MIT
---

# Create and Manage MotherDuck Flights

Use this skill when the user needs Python to run *on MotherDuck* — on a schedule or on demand — instead of in their own infrastructure. A Flight is a single-file Python program that MotherDuck executes in a managed runtime with a MotherDuck token injected, pip dependencies installed from a `requirements.txt`, and stdout/stderr captured as run logs. The primary use cases are scheduled ingestion (pull from Postgres, S3, APIs, other warehouses, or any dlt source into MotherDuck tables) and scheduled transformation (refresh aggregates, run dbt, recompute reporting tables).

## Source Of Truth

- **Non-negotiable ordering:** when MotherDuck MCP is available, call `get_flight_guide` before `create_flight`, `update_flight`, or `edit_flight_source`. The guide defines the current authoring contract, runtime limits, and tool semantics.
- Prefer current MotherDuck Flights docs over memory; the feature is in Preview and details shift.
- Without MCP, the same operations exist as SQL functions (`MD_CREATE_FLIGHT`, `MD_RUN_FLIGHT`, `MD_FLIGHTS()`, ...) that execute server-side on a MotherDuck connection. Parameter names differ slightly between the two surfaces; see the naming table in `references/FLIGHTS_GUIDE.md`.

## Default Posture

- One Flight = one single-file Python script with `def main(): ...` and `if __name__ == "__main__": main()`. No CLI args — every knob comes from env vars via `config` (non-secret) or `TYPE flights` secrets (sensitive).
- Connect with `duckdb.connect("md:")`; the runtime injects `MOTHERDUCK_TOKEN` automatically. Never hardcode a token in source, config, or requirements.
- Always pin dependencies in `requirements_txt`, and pin `duckdb` to the latest MotherDuck-supported version (currently `duckdb==1.5.2`); an unpinned `duckdb` can install a release MotherDuck does not accept yet and fail at connect.
- Each secret param arrives as the env var `<secret_name>_<PARAM>`, not the bare param name. This is the single most common authoring mistake.
- Bulk-load, never row-by-row: stage to `/tmp/` and `read_csv_auto`/`read_json_auto`/`read_parquet`, or one CTAS / `INSERT ... SELECT`. No `executemany()` against MotherDuck.
- Make every run idempotent: `CREATE OR REPLACE TABLE` full refresh, partition `DELETE` + `INSERT`, or dlt `write_disposition="merge"` with a primary key. Bootstrap with `CREATE DATABASE IF NOT EXISTS` / `CREATE SCHEMA IF NOT EXISTS` so the first run succeeds on a fresh account.
- Validate any config-supplied identifier (database, schema, table names) against `[A-Za-z_][A-Za-z0-9_]*` before interpolating it into DDL; bind all data values as `?` parameters.
- Create the flight **without** a schedule first, trigger one on-demand run, read the logs, and only then attach `schedule_cron` (5-field cron, UTC).
- For production, use a service-account token via `access_token_name` and keep its database permissions as narrow as the workload allows.
- A Flight is sized for orchestration and light processing (2 cores, 16GB RAM, ~150GB scratch at `/tmp/`), not for crunching large tables in Python memory — push heavy compute into SQL.

## Workflow

1. Classify the job: ingestion, transformation/refresh, export or alerting, or admin automation. If the job is interactive analysis or a one-off query, use `motherduck-query` instead — no Flight needed.
2. Call `get_flight_guide` (MCP) and confirm which database the flight writes to with `motherduck-explore`.
3. Start from the closest template in `references/FLIGHT_EXAMPLES.md` (dlt source, Postgres mirror, or S3 partition refresh) rather than writing from scratch; adapt via config knobs, not code surgery.
4. Create any required `TYPE flights` secret first, then `create_flight` with `name`, `source_code`, pinned `requirements_txt`, `config`, and secret names — no `schedule_cron` yet.
5. `run_flight`, poll `list_flight_runs` until terminal, and read `get_flight_logs`. Iterate with `edit_flight_source` (surgical) or `update_flight` (full field replacement); each content change creates a new version.
6. Once a run succeeds, set the schedule with `update_flight(schedule_cron = ...)` and tell the user the cron is UTC. Clear it later with `schedule_cron = ""`.

## Open Next

- Read `references/FLIGHTS_GUIDE.md` for the full concept and operations reference: anatomy, runtime environment, config vs secrets, scheduling, versioning, run lifecycle, the complete MCP tool reference, MCP-vs-SQL naming, loading strategies by data volume, and troubleshooting.
- Read `references/FLIGHT_EXAMPLES.md` for three complete, best-practice flight templates (dlt ingestion, Postgres ingestion, scheduled S3 partition refresh) with their `requirements.txt`, secret setup, and deploy calls.

## Related Skills

- `motherduck-load-data` for choosing the ingestion SQL the flight will run (CTAS, `INSERT ... SELECT`, cloud-storage secrets)
- `motherduck-query` for validating the DuckDB SQL inside the flight before deploying it
- `motherduck-explore` for confirming target databases, schemas, and tables exist
- `motherduck-build-data-pipeline` when the work is a full raw/staging/analytics pipeline design and the flight is just its scheduler
