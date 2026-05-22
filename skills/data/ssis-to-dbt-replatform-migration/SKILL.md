---
name: ssis-to-dbt-replatform-migration
description: Validates, deploys, and operationalizes SnowConvert AI (SCAI) Replatform output — SSIS to dbt and Snowflake TASKs migrations. Use when user has SnowConvert Replatform output, converted SSIS packages, deploy dbt projects, deploy orchestration, validate replatform, deploy converted ETL, replatform deploy, SSIS to dbt deploy, SCAI replatform, SSIS migration, convert SSIS, migrate ETL, SnowConvert output, replatform output, dtsx migration, ETL to Snowflake.
---

# ETL Replatform Deploy

After **SnowConvert AI Replatform** converts SSIS packages into dbt projects and Snowflake TASKs/procedures, this skill validates the output, deploys it to Snowflake, and runs smoke tests.

## When to Use

- User has SnowConvert AI Replatform output (the `Output/ETL/` folder) ready to deploy
- User mentions SSIS-to-dbt migration, replatform output, or converted ETL packages
- User needs to validate, fix, and deploy converted dbt projects to Snowflake
- User wants to set up orchestration (TASKs/procedures) for deployed dbt projects
- User needs to troubleshoot deployment issues with replatformed ETL

## Tools Used

- `bash` — Run scanner CLI (`uv run python -m replatform_scanner`), run `snow dbt deploy`
- `snowflake_sql_execute` — Create databases/schemas/tables, deploy orchestration SQL, run smoke tests
- `ask_user_question` — Present briefing, confirm fixes, get deployment approval at every phase gate
- `read` / `write` / `edit` — Fix profiles.yml, sources.yml, orchestration SQL files

## Stopping Points

- ✋ Phase 0: User approves the workflow before any action
- ✋ Phase 1: User reviews scan inventory before validation
- ✋ Phase 2: User approves each fix; confirms all fixes before deployment
- ✋ Phase 3.1.5: User approves source table creation (stubs/seeds)
- ✋ Phase 3.3: User reviews deployment summary before smoke tests
- ✋ Phase 4: User reviews smoke test results

---

## Rules

1. **Consent Before Action**
   - ALWAYS present the Phase 0 briefing BEFORE running any commands, tools, or scripts
   - DO NOT execute any bash commands, SQL statements, or file modifications until the user explicitly approves
   - If the user declines, stop immediately and explain what they can do manually instead

2. **Use ONLY Provided Scripts**
   - ONLY use the provided CLI commands: `python -m replatform_scanner`
   - DO NOT create custom scripts to read or manipulate the JSON file
   - DO NOT use grep, jq, or other tools to parse the inventory directly
   - All interactions MUST go through the provided CLI

3. **Deploy in Correct Order**
   - `etl_configuration/` objects FIRST (tables, UDFs, procedures)
   - dbt projects SECOND (via `snow dbt deploy`)
   - Orchestration SQL THIRD (CREATE TASK / CREATE PROCEDURE)
   - NEVER deploy orchestration before dbt projects are deployed

4. **User Confirmation at Every Phase**
   - Stop at mandatory checkpoints before each phase
   - Present summary of what will happen
   - Wait for explicit approval before proceeding

5. **Schema Awareness**
   - Ask user for target DATABASE and SCHEMA before any deployment
   - Update hardcoded `public` schema references in `etl_configuration/` if target differs
   - Ensure `EXECUTE DBT PROJECT` names match deployed project names exactly

6. **No Custom HTML Reports**
   - DO NOT write custom HTML reports manually

---

## Prerequisites

Before using this skill:
- **SnowConvert AI Replatform output** directory (the `Output/ETL/` folder from a completed conversion)
- **Snowflake CLI (`snow`)** installed and configured for `snow dbt deploy` / `snow dbt execute`
- **Active Snowflake connection** with permissions to create tables, UDFs, procedures, tasks, and deploy dbt projects
- **Python 3.11+** and **uv** package manager installed

---

## Workflow

```
Replatform Deploy Progress:
- [ ] Phase 0: Briefing & Consent
- [ ] Phase 1: Scan & Inventory
- [ ] Phase 2: Validate & Fix
- [ ] Phase 3: Deploy
- [ ] Phase 4: Smoke Test
- [ ] Phase 5: Operationalize (optional)
```

### Phase 3 Detail:

```
Phase 3: Deploy
  ├─ 3.0: Collect target info (DB, schema, connection, warehouse)
  ├─ 3.0.1: Verify DB/schema exist
  │   ├─ DB missing → Create? / Different name? / Stop
  │   └─ Schema missing → Create? / Different name? / Stop
  ├─ 3.1: Deploy etl_configuration
  ├─ 3.1.5: Create source tables
  │   ├─ Seeds exist → dbt seed (preferred)
  │   ├─ No seeds → CREATE TABLE stubs
  │   └─ Skip (user creates manually)
  ├─ 3.2: Deploy dbt projects (snow dbt deploy)
  └─ 3.3: Deploy orchestration SQL
```

---

## Phase 0: Briefing & Consent

**Goal:** Explain what this skill does and get explicit user approval before executing anything.

**⚠️ STOP:** This phase MUST be completed before ANY other action. Do not run any commands, read any files, or execute any tools until the user approves.

**Load** `references/phase0-briefing.md` and present its content to the user using `ask_user_question`.

Ask the user: **"Shall I proceed with Phase 1 (Scan & Inventory)? This is read-only — it only reads files in your Replatform output directory and writes a JSON inventory file."**

Options:
- **Yes, proceed** — Continue to Phase 1
- **No, stop here** — End the workflow; explain they can run the CLI commands manually

**⚠️ STOP:** Do NOT proceed until the user selects "Yes, proceed".

---

## Phase 1: Scan & Inventory

**Goal:** Build a complete inventory of the Replatform output and understand the deployment topology.

### Step 1.1: Locate the Output Directory

Ask user for the path to the Replatform output (typically the `Output/ETL/` folder from SnowConvert AI).

### Step 1.2: Run the Scanner

```bash
uv run --project <SKILL_DIR> python -m replatform_scanner scan <ETL_OUTPUT_DIR> <INVENTORY_OUTPUT_PATH>
```

### Step 1.3: Review Inventory

```bash
uv run --project <SKILL_DIR> python -m replatform_scanner summary <INVENTORY_JSON>
```

Present summary (packages, dbt projects, orchestration types, etl_configuration components, validation issues). Ask: **Proceed to Phase 2?**

**⚠️ STOP:** Wait for user confirmation before proceeding to Phase 2.

---

## Phase 2: Validate & Fix

**Goal:** Identify and resolve issues before deployment.

### Step 2.1: Run Validation

```bash
uv run --project <SKILL_DIR> python -m replatform_scanner validate <INVENTORY_JSON>
```

This checks: placeholders in `sources.yml`/`profiles.yml`, missing files, project name mismatches, unsupported `profiles.yml` fields, `etl_configuration/` schema refs, `EXECUTE DBT PROJECT` refs, CREATE TASK clause ordering, `sources.yml` hardcoded database/schema, TASK DAG orphans, hardcoded schema prefixes in `EXECUTE DBT PROJECT`, hardcoded warehouse names in orchestration SQL, PROCEDURE-based orchestration using `EXECUTE DBT PROJECT` (**ERROR** — this is a Snowflake platform limitation, not just a warning), and `'{{ var(...) }}'::DATE` casts that fail on partial dates (**ERROR** — `YYYY-MM` is not a valid Snowflake DATE).

### Step 2.2: Present Issues and Apply Fixes

For each issue: show severity, category, file, problem, suggested fix. Ask: **Apply this fix? (Yes/No/Skip all of this type)**

**Issue Categories:** `PLACEHOLDER`, `NAME_MISMATCH`, `SCHEMA_MISMATCH`, `MISSING_FILE`, `ORPHAN_TASK`, `DANGLING_REF`, `SOURCE_SCHEMA_MISMATCH`, `PROFILES_OVERRIDE`, `ORCH_SCHEMA_PREFIX`, `ORCH_WAREHOUSE`, `PROC_EXECUTE_DBT`, `PARTIAL_DATE_CAST`

**Fix Patterns:**
- **`PROFILES_OVERRIDE`**: Replace source-env connection fields with target values. `snow dbt deploy` requires `account`, `user`, `role`, `database`, `schema`, `warehouse` to be present. **`role`, `account`, `user` are used verbatim** — they MUST be real target values (not 'placeholder'). `database`, `schema`, `warehouse` are overridden by CLI flags.
- **`PROC_EXECUTE_DBT`** (ERROR): `EXECUTE DBT PROJECT` cannot run inside SQL stored procedures. Convert to a TASK-based DAG where each `EXECUTE DBT PROJECT` is a separate child task with `AFTER` dependency.
- **`PARTIAL_DATE_CAST`** (ERROR): `'{{ var("x") }}'::DATE` fails when the variable value is `YYYY-MM` format. Fix by using `TO_DATE('{{ var("x") }}', 'YYYY-MM')` or ensuring variables are always `YYYY-MM-DD`.
- **`ORCH_SCHEMA_PREFIX`**: Replace hardcoded source schema (e.g., `ETL.`) in `EXECUTE DBT PROJECT` with the target schema (e.g., `PUBLIC.`).
- **`ORCH_WAREHOUSE`**: Replace hardcoded source warehouses (e.g., `ETL_WH`) with the target warehouse.
- **`SOURCE_SCHEMA_MISMATCH`**: Remove `database` field from `sources.yml` and set `schema` to the target schema.

After all fixes, present summary (found/fixed/skipped/remaining). Ask: **Proceed to Phase 3?**

**⚠️ STOP:** Wait for user confirmation before proceeding to Phase 3.

---

## Phase 3: Deploy

**Goal:** Deploy all components to Snowflake in the correct order.

### Step 3.0: Collect Target Information

Ask the user for: target DATABASE, target SCHEMA, Snowflake CLI connection name, warehouse.

### Step 3.0.1: Ensure Database and Schema Exist

**IMPORTANT — do this BEFORE any other SQL in Phase 3.**

Run these two statements silently (do NOT run `USE DATABASE` first — it will fail if the database does not exist yet):

```sql
CREATE DATABASE IF NOT EXISTS <TARGET_DATABASE>;
CREATE SCHEMA IF NOT EXISTS <TARGET_DATABASE>.<TARGET_SCHEMA>;
```

Then set active context:

```sql
USE DATABASE <TARGET_DATABASE>;
USE SCHEMA <TARGET_DATABASE>.<TARGET_SCHEMA>;
```

### Step 3.1: Deploy etl_configuration

Deploy shared infrastructure objects first (tables, UDFs, procedures). For each SQL file: read, check schema refs, present for review, execute on approval.

**If error occurs:**
- `Object already exists` → safe to skip if user confirms existing object is correct
- Schema reference error → check `etl_configuration/` SQL for hardcoded schema names; update to target schema

### Step 3.1.5: Create Source Tables

Before deploying dbt projects, check whether source tables from `sources.yml` exist in the target. For missing tables, offer:

1. **Seed from CSV** (preferred) — if `seeds/` has matching CSVs
2. **Create stub tables** — empty tables with columns from `sources.yml`
3. **Skip** — user creates manually

**IMPORTANT:** When creating stub tables, do NOT rely solely on `sources.yml` column declarations — they may be incomplete. **Always read the staging model SQL** (e.g., `stg_raw__customers.sql`) to find the exact columns referenced in the `SELECT` list. The model SQL is the source of truth for required columns.

**IMPORTANT:** Use `CREATE TABLE IF NOT EXISTS` for new stubs, `CREATE OR REPLACE TABLE` for tables with wrong columns. Never use `ALTER TABLE ADD COLUMN`. See `references/snowflake-sql-patterns.md` for exact syntax.

**⚠️ STOP:** Present the list of tables to create/seed and get approval before executing any CREATE or DROP statements.

### Step 3.2: Deploy dbt Projects

```bash
snow dbt deploy <PROJECT_NAME> \
  --source <PROJECT_DIR> \
  --database <TARGET_DATABASE> \
  --schema <TARGET_SCHEMA> \
  --connection <CONNECTION_NAME> \
  --warehouse <TARGET_WAREHOUSE> \
  --role <TARGET_ROLE> \
  --force
```

Track: `[DONE]` / `[FAIL]` / `[PENDING]` per project.

**If error occurs:**
- `Missing required fields` → profiles.yml needs all connection fields (see `PROFILES_OVERRIDE` fix pattern)
- `Failed to use role <name>` → `role` in profiles.yml must be a real target role, NOT a placeholder. `snow dbt deploy` uses `role` verbatim from profiles.yml — it is NOT overridden by CLI flags. Set it to the role from your Snowflake connection (e.g. `snow connection list` to check)
- `source table not found` → go back to Step 3.1.5 to create stubs/seeds
- `Project already exists` → use `--force` flag to overwrite

### Step 3.3: Deploy Orchestration SQL

For each package: read orchestration SQL, verify `EXECUTE DBT PROJECT` refs, present for review, execute.

**CRITICAL — TASK DAG creation order:**
Tasks that reference predecessors via `AFTER <task>` will fail with `Invalid predecessor` if the predecessor does not exist yet. You MUST create tasks in **dependency order**:

1. **Root tasks first** — tasks with a `SCHEDULE` clause and NO `AFTER` clause.
2. **Then child tasks** — in topological order so that every task referenced in an `AFTER` clause already exists.
3. **General rule:** if task B has `AFTER task_A`, then `task_A` must be created before `task_B`.

Parse each orchestration SQL file to identify the DAG structure before executing any `CREATE TASK` statements. If a file contains multiple tasks, reorder the statements so roots come first.

**If error occurs:**
- `Invalid predecessor 'X' was specified` → task creation order is wrong; create the predecessor task first, then retry
- `Object 'X' does not exist` → hardcoded schema prefix; apply `ORCH_SCHEMA_PREFIX` fix
- `Warehouse 'X' does not exist` → hardcoded warehouse; apply `ORCH_WAREHOUSE` fix
- `Unsupported statement type 'SHOW PARAMETER'` → procedure-based orchestration; must convert to TASK DAG (see `PROC_EXECUTE_DBT`)

**⚠️ STOP:** Present deployment summary (etl_configuration, dbt projects, orchestration). Ask: **Proceed to Phase 4?**

---

## Phase 4: Smoke Test

**Goal:** Verify the deployed pipeline works end-to-end.

### Step 4.1: Test dbt Projects Individually

```sql
EXECUTE DBT PROJECT <database>.<schema>.<project_name>
  ARGS = 'build --select tag:<tag> --target dev';
```

**Passing dbt vars** (e.g. for `report_month`):
```sql
EXECUTE DBT PROJECT <database>.<schema>.<project_name>
  ARGS = 'run --vars ''{report_month: 2024-01-01}''';
```

**IMPORTANT:** The syntax is `ARGS = '...'` (single equals, string literal). Do NOT use `ARGS => '...'` (Snowflake named-parameter syntax) — it will fail with a syntax error. Use fully-qualified `DATABASE.SCHEMA.PROJECT_NAME` in both EXECUTE statements and TASK definitions.

Track: `[PASS]` / `[FAIL]` per project with model counts and errors.

### Step 4.2: Test Orchestration

For TASK-based: `EXECUTE TASK <database>.<schema>.<package_name>;` then check `TASK_HISTORY()`.
For PROCEDURE-based: **⚠️ WARNING** — `EXECUTE DBT PROJECT` inside SQL stored procedures is a known Snowflake limitation (fails with `Unsupported statement type 'SHOW PARAMETER'`). If the scanner flagged `PROC_EXECUTE_DBT`, this orchestration pattern must be converted to a TASK-based DAG before it can work. See Troubleshooting table.

### Step 4.3: Data Validation

Row count checks on mart tables. Present results summary.

---

## Phase 5: Operationalize (Optional)

**Goal:** Set up ongoing scheduling and monitoring.

Options: Schedule TASKs with CRON, convert to Dynamic Tables, set up monitoring queries, or skip.

For CRON scheduling: `ALTER TASK ... SET SCHEDULE`, then `RESUME` child-to-root.
For Dynamic Tables: suggest loading the `dynamic-tables` skill.
For monitoring: provide `TASK_HISTORY()` query from `references/snowflake-sql-patterns.md`.

---

## CLI Reference

All CLI commands use:
```bash
uv run --project <SKILL_DIR> python -m replatform_scanner <command> [args]
```

| Command | Description |
|---------|-------------|
| `scan <etl_dir> <output_json>` | Scan Replatform output and produce inventory JSON |
| `summary <json>` | Print human-readable summary |
| `validate <json>` | Run all validation checks |
| `issues <json>` | List all validation issues with details |
| `packages <json>` | List packages with orchestration type |
| `dbt-projects <json>` | List dbt projects with deployment names |
| `deploy-order <json>` | Show recommended deployment order |
| `stats <json>` | Show statistics |

---

## Output

This skill produces:
- **`replatform_inventory.json`** — complete inventory of scanned Replatform output
- **Deployed Snowflake objects** — dbt projects, orchestration TASKs/procedures, etl_configuration tables/UDFs/procedures
- **Smoke test results** — pass/fail per dbt project build and orchestration execution
- **Data validation** — row counts on output mart tables

---

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `invalid identifier 'COLUMN_NAME'` during dbt build | `sources.yml` column declarations incomplete — stub table was created with fewer columns than the model SQL expects | Add missing columns to `sources.yml`, then recreate stub with `CREATE OR REPLACE TABLE` |
| `Missing required fields: account, database, role, schema, user, warehouse` | `profiles.yml` was stripped too aggressively or has placeholder values from the source environment | `snow dbt deploy` validates profiles.yml and **requires** all connection fields. Replace source-env values with target values. **`role`, `account`, `user` are used verbatim** — they must be real target values (not 'placeholder'). `database`, `schema`, `warehouse` are overridden by CLI flags so placeholders are OK for those. Run validator to detect with `PROFILES_OVERRIDE` category |
| `Failed to use role <name>` | `role` in profiles.yml is set to a placeholder or source-env value that doesn't exist in the target account | `snow dbt deploy` reads `role` directly from profiles.yml — it is NOT overridden by CLI flags. Set `role` to the actual Snowflake role from your target connection (e.g. the role shown by `snow connection list`) |
| `Invalid predecessor 'X' was specified` | Child tasks with `AFTER` clauses were created before their parent/predecessor tasks | Create tasks in dependency order: root tasks (with `SCHEDULE`, no `AFTER`) first, then children. See Step 3.3 |
| `source table not found` | Source tables don't exist in target — seeds not run, stubs not created | Run Step 3.1.5: seed from CSV or create stubs |
| `SOURCE_SCHEMA_MISMATCH` false positive | Validator flagged `schema: PUBLIC` without `database` | This was fixed — only `database` triggers the warning now. Update skill scripts if using old version |
| `SQL compilation error: syntax error ... ADD COLUMN` | Skill generated `ALTER TABLE ADD COLUMN` instead of `CREATE TABLE` | Use `CREATE TABLE IF NOT EXISTS` or `CREATE OR REPLACE TABLE` per `references/snowflake-sql-patterns.md` |
| dbt resolves source to wrong schema (e.g. `CONTOSO_OLTP` instead of `PUBLIC`) | `schema` omitted from `sources.yml` — dbt uses source `name` as schema when `schema` is not set | Add explicit `schema: PUBLIC` to each source in `sources.yml` |
| `Object 'ETL.LoadOrders' does not exist` when running orchestration | `EXECUTE DBT PROJECT` has hardcoded schema prefix from source environment (e.g. `ETL.`) that doesn't match the target schema | Change `ETL.LoadOrders` to `PUBLIC.LoadOrders` (or your target schema). Run validator to detect with `ORCH_SCHEMA_PREFIX` category |
| `Warehouse 'ETL_WH' does not exist` when running orchestration | `WAREHOUSE = ETL_WH` is hardcoded from the source environment | Change to your target warehouse (e.g. `COMPUTE_WH`). Run validator to detect with `ORCH_WAREHOUSE` category |
| `Unsupported statement type 'SHOW PARAMETER'` when calling a procedure | `EXECUTE DBT PROJECT` cannot run inside SQL stored procedures (LANGUAGE SQL `BEGIN…END`) | Convert the PROCEDURE-based orchestration to a TASK-based DAG. Each `EXECUTE DBT PROJECT` becomes a child task with `AFTER` dependency. Run validator to detect with `PROC_EXECUTE_DBT` category |
| `Can't parse '2024-01' as date` or `DATE_TRUNC does not support VARCHAR` | dbt model uses `'{{ var("x") }}'::DATE` but variable value is partial (e.g. `YYYY-MM`) | Replace `'{{ var("x") }}'::DATE` with `TO_DATE('{{ var("x") }}', 'YYYY-MM')`. Run validator to detect with `PARTIAL_DATE_CAST` category |

---

## Session Diary

**⚠️ STOP:** At the start of every session, check for an existing diary before running any commands.

**Load** `references/session-diary.md` for the full diary format and template.

**Quick reference:**
- Diary location: `~/.snowflake/cortex/memory/replatform/<connection>/<database>.<schema>.md`
- If diary exists: read it to restore context (phase reached, packages deployed, fixes applied)
- If new deployment: create diary after Phase 1 completes
- Update diary after each phase completes

---

## Success Criteria

Deployment is complete when:
- All `etl_configuration/` objects created in Snowflake
- All dbt projects deployed via `snow dbt deploy`
- All orchestration SQL executed (TASKs/procedures created)
- Smoke tests pass for at least the dbt project builds
- User has reviewed and approved the deployment

### Pre-Completion Checklist

```
[ ] Did I deploy etl_configuration objects first?
[ ] Did I verify dbt project names match EXECUTE DBT PROJECT references?
[ ] Did I run smoke tests on deployed dbt projects?
[ ] Did I present all results to the user?
```
