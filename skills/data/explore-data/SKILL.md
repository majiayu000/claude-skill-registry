---
name: explore-data
description: "Explores data in a Bauplan lakehouse safely using the Bauplan Python SDK. Use to inspect namespaces, tables, schemas, samples, and profiling queries; and to export larger result sets to files. Read-only exploration only; no writes or pipeline runs."
allowed-tools:
  - Bash(bauplan:*)
  - Read
  - Write
  - Glob
  - Grep
  - WebFetch(domain:docs.bauplanlabs.com)
---

# Exploring Data in Bauplan

Explore and understand data stored in a Bauplan lakehouse using the Python SDK. This skill is read-only. It must not create tables, import data, run pipelines, or merge branches.

If the user asks for any write operation, stop and suggest switching to a write-capable skill (data-pipeline or safe-ingestion).

## Before You Start

Ask the user which branch or ref to explore. All reads must be scoped to an explicit ref. Never rely on implicit defaults.

## Required Deliverables

Every exploration MUST produce a `summary.md` file in the project root. This file is written in Phase 4. If you reach the end of Phase 3, you MUST proceed to Phase 4 and write `summary.md`. Do not end the conversation after Phase 3. The exploration is incomplete without `summary.md`.

## Phased Execution (Critical)

This skill runs in four phases. Each phase is a separate bash execution of `data_explorer.py`. After each phase, **report findings in the chat** before proceeding to the next phase. The user must see incremental progress throughout the exploration.

The phases are:

| Phase | Name | Typical duration | Gate |
|-------|------|-----------------|------|
| 1 | Discovery | <30s | Report table list. Ask which tables to explore. |
| 2 | Schema + Semantics | 1-2 min | Report schemas and table descriptions. Proceed automatically. |
| 3 | Profiling + Anomalies | 1-2 min per table | Announce each table before profiling, report findings after. |
| 4 | Joins + Summary | <1 min | Write `summary.md`. Present to user. |

**Between every phase, post a chat message summarizing what was found.** Do not chain all phases into a single bash call.

**Responsiveness rule (hard constraint):** Always post a chat message between consecutive bash calls. Never execute two bash calls back-to-back without a message to the user in between.

## Single Script, Iterative Execution

All exploration code lives in one file: `data_explorer.py` in the project root. Overwrite this file at the start of each phase with the code for that phase. Each phase prints its findings to stdout. Do not create additional Python files or subdirectories.

## Setup Block

Write the following setup once at the top of `data_explorer.py`. All subsequent examples assume this block exists.

```python
import bauplan
import polars as pl
from datetime import datetime, timezone

client = bauplan.Client()
ref = "<ref_to_explore>"  # branch name or commit hash — always explicit
```

---

## Phase 1 — Discovery

**Goal:** List all namespaces and tables available on the ref. Report them. Ask the user which tables to explore in depth.

```python
namespaces = list(client.get_namespaces(ref=ref))
print("=== Namespaces ===")
for ns in namespaces:
    print(f"  {ns.namespace}")

tables = list(client.get_tables(ref=ref))
print("\n=== Tables ===")
for t in tables:
    print(f"  {t.namespace}.{t.name}")
```

**After execution:** Post the table list in the chat. Ask: "Which tables should I explore in depth? I can inspect all of them, or you can pick a subset." If the user selects a subset, only those tables proceed to Phase 2. If the user says "all," proceed with all tables.

---

## Phase 2 — Schema + Semantics

**Goal:** For each selected table, inspect its schema, sample 20 rows, and produce a one-sentence description of its purpose and grain.

### 2A. Schema and metadata

```python
table = client.get_table(table="my_table", namespace="bauplan", ref=ref)
print(f"\n=== {table.namespace}.{table.name} ===")
print(f"Records: {table.records}")
for c in table.fields:
    print(f"  {c.name}: {c.type}")
```

### 2B. Sample and semantics

```python
res = client.query("""
    SELECT *
    FROM bauplan.my_table
    LIMIT 20
""", ref=ref, max_rows=20)
df = pl.from_arrow(res.to_arrow())
print(df)
```

From the schema and sample, produce a one-sentence description: what entity each row represents, what the grain is, and what the table likely feeds into. Print this description as part of the output.

Example: `"bauplan.raw_ecommerce_events: one row per user interaction with a product, timestamped, grouped by session."`

**After execution:** Post schemas and descriptions in the chat. Proceed to Phase 3 automatically.

If more than 5 tables are selected, split Phase 2 into batches of 5 tables per bash call. Post findings after each batch.

---

## Phase 3 — Profiling + Anomalies

**Goal:** Profile each selected table and detect anomalies. Process one table at a time. Announce each table before running queries, then report findings immediately after.

### Execution rule (hard constraint)

**Profile ONE table per bash execution. Do not loop over multiple tables in a single script run.**

The sequence for each table is:

1. **Chat message.** Tell the user which table you are about to profile and where you are in the list: `"Profiling bauplan.orders (3 of 7)..."`
2. **Rewrite `data_explorer.py`** with queries for that single table only.
3. **Run it.** One bash call, one table.
4. **Chat message.** Report findings using the compact format below.
5. **Move to the next table.** Go back to step 1.

Do not combine multiple tables into one script. Do not use a for-loop over tables. Each bash call must target exactly one table. This ensures the user sees progress after every table.

**Report format:**

```
📊 bauplan.orders (3/7)
  Rows: 1,234,567
  Time range: 2024-01-01 → 2024-12-31 (56 days stale)
  Null flags: shipping_address (72% null)
  Duplicate keys: none
```

If standard checks raise a flag, tell the user before running deep checks: `"→ shipping_address is 72% null. Running deep checks..."` Then report those results in a follow-up message.

### Standard checks (always run)

Combine row count, time range, and null rates into a **single query** per table. Phase 2 already collected the schema, so you know every column name. Generate the query dynamically.

```python
# One query covers row count, time range, and null rates for all columns.
# Adjust column names based on the schema collected in Phase 2.
client.query("""
    SELECT
        COUNT(*) AS row_count,
        MIN(event_time) AS min_t,
        MAX(event_time) AS max_t,
        1.0 - CAST(COUNT(order_id) AS DOUBLE) / COUNT(*) AS null_rate_order_id,
        1.0 - CAST(COUNT(customer_id) AS DOUBLE) / COUNT(*) AS null_rate_customer_id,
        1.0 - CAST(COUNT(shipping_address) AS DOUBLE) / COUNT(*) AS null_rate_shipping_address
    FROM bauplan.orders
""", ref=ref, max_rows=1)
```

For every timestamp column, compare `MAX` to today. If the gap exceeds what the table's grain implies (e.g., an hourly event table whose latest row is 30 days old), flag the table as potentially stale. Print the gap in days.

Flag any column where the null rate exceeds 50%.

**Candidate key duplicates** (second query). For columns whose names contain `_id` or that appear first in the schema, check for duplicates.

```python
client.query("""
    SELECT order_id, COUNT(*) AS n
    FROM bauplan.my_table
    GROUP BY order_id
    HAVING COUNT(*) > 1
    LIMIT 10
""", ref=ref, max_rows=10)
```

Report the count of duplicated keys and a few examples if any exist.

That is two queries per table for standard checks.

### Deep checks (opt-in)

Run these when the standard checks raise a flag, or when the user explicitly requests a thorough inspection. Announce what triggered the deep check and which column you are investigating.

**Cardinality surprises.** Compute distinct count for categorical columns (status, type, category) and identifiers (user_id, order_id). Flag if a categorical column has unexpectedly high cardinality or an identifier has unexpectedly low cardinality.

```python
client.query("""
    SELECT
        COUNT(DISTINCT status) AS distinct_status,
        COUNT(DISTINCT user_id) AS distinct_user_id
    FROM bauplan.my_table
""", ref=ref, max_rows=1)
```

**Value distribution for flagged columns.** When a column has a high null rate or unexpected cardinality, sample its values.

```python
client.query("""
    SELECT status, COUNT(*) AS n
    FROM bauplan.my_table
    GROUP BY status
    ORDER BY n DESC
    LIMIT 20
""", ref=ref, max_rows=20)
```

**Type-value mismatches.** For columns whose names imply a specific format (email, url, phone, ip_address, zip_code), sample values and verify they match the expected pattern.

```python
client.query("""
    SELECT email
    FROM bauplan.my_table
    WHERE email IS NOT NULL
    LIMIT 20
""", ref=ref, max_rows=20)
```

Inspect the sample. If values clearly violate the expected format, flag the column.

---

## Phase 4 — Joins + Summary

**Goal:** Identify join candidates across tables, then write `summary.md`.

### 4A. Join candidates

After inspecting multiple tables, look for columns that serve as join keys.

**Name matching.** Scan column names across all inspected tables. Columns with identical names or conventional foreign key patterns (e.g., `PULocationID` matching `LocationID`) are candidates.

**Key overlap.** For each candidate pair, verify overlap.

```python
client.query("""
    SELECT COUNT(*) AS overlap
    FROM (
        SELECT DISTINCT user_id FROM bauplan.orders
        INTERSECT
        SELECT DISTINCT user_id FROM bauplan.users
    )
""", ref=ref, max_rows=1)
```

**Join cardinality.** Determine whether the relationship is one-to-one, one-to-many, or many-to-many.

```python
client.query("""
    SELECT
        COUNT(*) AS total_rows,
        COUNT(DISTINCT user_id) AS distinct_keys
    FROM bauplan.orders
""", ref=ref, max_rows=1)
```

If `total_rows == distinct_keys`, the key is unique on that side.

For each viable join, print: the two tables, the join columns, the overlap count, and the cardinality (e.g., "orders.user_id → users.user_id: 98% overlap, many-to-one").

### 4B. Write summary.md

Write `summary.md` in the project root. This is a required deliverable. Use the template below.

```markdown
# Data Exploration Summary

**Ref:** <ref explored>
**Date:** <timestamp>
**Tables inspected:** <count>

## Tables

### <namespace>.<table_name>

**Semantics:** <one-sentence description of purpose and grain>

**Stats:**
- Rows: <count>
- Time range: <min> → <max> (<N days stale> or "fresh")

**Schema (key columns):**
| Column | Type |
|--------|------|
| col1   | type |
| col2   | type |

**Anomalies:**
<List each flag from Phase 3. If none, state "No anomalies detected.">

**Join candidates:**
<List viable joins with overlap and cardinality. If none, state "No join candidates identified.">

---

(Repeat for each table.)

## Cross-Table Observations

<Any patterns that span multiple tables: shared keys, referential integrity gaps, schema inconsistencies, temporal misalignment between tables. If none, state "No cross-table observations.">
```

Separate facts (derived from queries) from inferences (suggested by patterns). Label inferences explicitly.

**After execution:** Present `summary.md` to the user. The exploration is complete only after this file is delivered.

---

## Compare Across Refs

When the user needs to compare branches, run the same query with different `ref=` values.

```python
q = "SELECT COUNT(*) AS n FROM bauplan.my_table"
n_main = client.query(q, ref="main", max_rows=1)
n_dev = client.query(q, ref="<username>.<branch>", max_rows=1)
```

## Export Results to File

Use CSV by default. Switch to Parquet when the result set exceeds ~1M rows.

```python
# CSV (default)
client.query_to_csv_file(
    path="results.csv",
    query="SELECT col1, col2 FROM bauplan.my_table WHERE event_date >= '2026-01-01'",
    ref=ref,
    max_rows=1_000_000,
)

# Parquet (large results only)
client.query_to_parquet_file(
    path="results.parquet",
    query="SELECT col1, col2 FROM bauplan.my_table WHERE event_date >= '2026-01-01'",
    ref=ref,
    max_rows=10_000_000,
)
```

## Query Safety Rules

- Every SELECT must include a `LIMIT` clause.
- Every SELECT must list columns explicitly. The only exception is `SELECT *` in Phase 2 (semantics step) where the goal is to see all columns in a small sample.
- Use `max_rows` as an additional SDK-level guardrail.
- Avoid wide scans when a filter can reduce data early.

## Outputs

The exploration produces two artifacts:

1. **`data_explorer.py`** — the exploration script in its final state.
2. **`summary.md`** — structured summary of all findings, written in Phase 4.

Both live in the project root.
