---
name: developing-incremental-models
description: |
  Develops and troubleshoots dbt incremental models. Use when working with incremental materialization for:
  (1) Creating new incremental models (choosing strategy, unique_key, partition)
  (2) Task mentions "incremental", "append", "merge", "upsert", or "late arriving data"
  (3) Troubleshooting incremental failures (merge errors, partition pruning, schema drift)
  (4) Optimizing incremental performance or deciding table vs incremental
  Guides through strategy selection, handles common incremental gotchas.
---

# dbt Incremental Model Development

**Choose the right strategy. Design the unique_key carefully. Handle edge cases.**

## When to Use Incremental

| Scenario | Recommendation |
|----------|----------------|
| Source data < 10M rows | Use `table` (simpler, full refresh is fast) |
| Source data > 10M rows | Consider `incremental` |
| Source data updated in place | Use `incremental` with `merge` strategy |
| Append-only source (logs, events) | Use `incremental` with `append` strategy |
| Partitioned warehouse data | Use `insert_overwrite` if supported |

**Default to `table` unless you have a clear performance reason for incremental.**

## Critical Rules

1. **ALWAYS test with `--full-refresh` first** before relying on incremental logic
2. **ALWAYS verify unique_key is truly unique** in both source and target
3. **If merge fails 3+ times**, check unique_key for duplicates
4. **Run full refresh periodically** to prevent data drift

## Workflow

### 1. Confirm Incremental is Needed

```bash
# Check source table size
dbt show --inline "select count(*) from {{ source('schema', 'table') }}"
```

If count < 10 million, consider using `table` instead. Incremental adds complexity.

### 2. Understand the Source Data Pattern

Before choosing a strategy, answer:
- **Is data append-only?** (new rows added, never updated)
- **Are existing rows updated?** (need merge/upsert)
- **Is there a reliable timestamp?** (for filtering new data)
- **What's the unique identifier?** (for merge matching)

```bash
# Check for timestamp column
dbt show --inline "
  select
    min(updated_at) as earliest,
    max(updated_at) as latest,
    count(distinct date(updated_at)) as days_of_data
  from {{ source('schema', 'table') }}
"
```

### 3. Choose the Right Strategy

| Strategy | Use When | How It Works |
|----------|----------|--------------|
| `append` | Data is append-only, no updates | INSERT only, no deduplication |
| `merge` | Data can be updated | MERGE/UPSERT by unique_key |
| `delete+insert` | Data updated in batches | DELETE matching rows, then INSERT |
| `insert_overwrite` | Partitioned tables (BigQuery, Spark) | Replace entire partitions |

**Default:** `merge` is safest for most use cases.

**Note:** Strategy availability varies by adapter. Check the [dbt incremental strategy docs](https://docs.getdbt.com/docs/build/incremental-strategy) for your specific warehouse.

### 4. Design the Unique Key

**CRITICAL: unique_key must be truly unique in your data.**

```bash
# Verify uniqueness BEFORE creating model
dbt show --inline "
  select {{ unique_key_column }}, count(*)
  from {{ source('schema', 'table') }}
  group by 1
  having count(*) > 1
  limit 10
"
```

If duplicates exist:
- Add more columns to make composite key
- Add deduplication logic in model
- Use `delete+insert` instead of `merge`

### 5. Write the Incremental Model

```sql
{{
    config(
        materialized='incremental',
        incremental_strategy='merge',  -- or append, delete+insert
        unique_key='id',               -- MUST be unique
        on_schema_change='append_new_columns'  -- handle new columns
    )
}}

select
    id,
    column_a,
    column_b,
    updated_at
from {{ source('schema', 'table') }}

{% if is_incremental() %}
where updated_at > (select max(updated_at) from {{ this }})
{% endif %}
```

### 6. Build with Full Refresh First

**ALWAYS verify with full refresh before trusting incremental logic.**

```bash
# First run: full refresh to establish baseline
dbt build --select <model_name> --full-refresh

# Verify output
dbt show --select <model_name> --limit 10
dbt show --inline "select count(*) from {{ ref('model_name') }}"
```

### 7. Test Incremental Logic

```bash
# Run incrementally (no --full-refresh)
dbt build --select <model_name>

# Verify row count changed appropriately
dbt show --inline "select count(*) from {{ ref('model_name') }}"
```

### 8. Handle Schema Changes

Set `on_schema_change` based on your needs:

| Setting | Behavior |
|---------|----------|
| `ignore` (default) | New columns in source are ignored |
| `append_new_columns` | New columns added to target |
| `sync_all_columns` | Target schema matches source exactly |
| `fail` | Error if schema changes |

## Common Incremental Problems

### Problem: Merge Fails with Duplicate Key

**Symptom:** "Cannot MERGE with duplicate values"

**Cause:** Multiple rows with same unique_key in source or target.

**Fix:**
```sql
-- Add deduplication using a CTE (cross-database compatible)
with deduplicated as (
    select *,
        row_number() over (partition by id order by updated_at desc) as rn
    from {{ source('schema', 'table') }}
    {% if is_incremental() %}
    where updated_at > (select max(updated_at) from {{ this }})
    {% endif %}
)
select * from deduplicated where rn = 1
```

### Problem: No Partition Pruning (Full Table Scan)

**Symptom:** Incremental runs take as long as full refresh.

**Cause:** Dynamic date filter prevents partition pruning.

**Fix:**
```sql
{% if is_incremental() %}
-- Use static date instead of subquery for partition pruning
where updated_at >= {{ dbt.dateadd('day', -3, dbt.current_timestamp()) }}
  and updated_at > (select max(updated_at) from {{ this }})
{% endif %}
```

### Problem: Late-Arriving Data is Missed

**Symptom:** Some records never appear in incremental model.

**Cause:** Filtering by max(updated_at) misses late arrivals.

**Fix:** Use a lookback window with a fixed offset from current date:
```sql
{% if is_incremental() %}
-- Lookback 3 days to catch late-arriving data
where updated_at >= {{ dbt.dateadd('day', -3, dbt.current_timestamp()) }}
{% endif %}
```

Alternatively, use a variable for the lookback period:
```sql
{% set lookback_days = 3 %}

{% if is_incremental() %}
where updated_at >= {{ dbt.dateadd('day', -lookback_days, dbt.current_timestamp()) }}
{% endif %}
```

### Problem: Schema Drift Causes Errors

**Symptom:** "Column X not found" after source adds column.

**Fix:** Set `on_schema_change='append_new_columns'` in config.

### Problem: Data Drift Over Time

**Symptom:** Counts diverge between incremental and full refresh.

**Fix:** Schedule periodic full refresh:
```bash
# Weekly full refresh
dbt build --select <model_name> --full-refresh
```

## Incremental Strategy Reference

### Append (Simplest)

```sql
{{ config(materialized='incremental', incremental_strategy='append') }}

select * from {{ source('events', 'raw') }}
{% if is_incremental() %}
where event_timestamp > (select max(event_timestamp) from {{ this }})
{% endif %}
```

- No unique_key needed
- Fastest performance
- **Only use for append-only data** (logs, events, immutable records)

### Merge (Default)

```sql
{{ config(
    materialized='incremental',
    incremental_strategy='merge',
    unique_key='id'
) }}

select * from {{ source('crm', 'contacts') }}
{% if is_incremental() %}
where updated_at > (select max(updated_at) from {{ this }})
{% endif %}
```

- Requires unique_key
- Handles updates and inserts
- Most common strategy

### Delete+Insert (Batch Updates)

```sql
{{ config(
    materialized='incremental',
    incremental_strategy='delete+insert',
    unique_key='id'
) }}

select * from {{ source('orders', 'raw') }}
{% if is_incremental() %}
where order_date >= {{ dbt.dateadd('day', -7, dbt.current_timestamp()) }}
{% endif %}
```

- Deletes all matching rows first
- Good for reprocessing batches
- Use when merge has duplicate key issues

### Insert Overwrite (Partitioned)

```sql
{{ config(
    materialized='incremental',
    incremental_strategy='insert_overwrite',
    partition_by={'field': 'event_date', 'data_type': 'date'}
) }}

select * from {{ source('events', 'raw') }}
{% if is_incremental() %}
where event_date >= {{ dbt.dateadd('day', -3, dbt.current_timestamp()) }}
{% endif %}
```

- Replaces entire partitions
- Best for partitioned tables in BigQuery/Spark
- No unique_key needed (operates on partitions)

## Anti-Patterns

- Using incremental for small tables (< 10M rows)
- Not testing with full-refresh first
- Using append strategy when data can be updated
- Not verifying unique_key uniqueness
- Relying on exact timestamp match without lookback
- Never running full refresh (causes data drift)
- Using merge with non-unique keys

## Testing Checklist

- [ ] Model runs with `--full-refresh`
- [ ] Model runs incrementally (without flag)
- [ ] unique_key verified as truly unique
- [ ] Row counts reasonable after incremental run
- [ ] Late-arriving data handled (lookback window)
- [ ] Schema changes handled (on_schema_change set)
- [ ] Periodic full refresh scheduled
