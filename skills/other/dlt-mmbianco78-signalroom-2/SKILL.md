---
name: dlt
description: dlt (data load tool) patterns for SignalRoom ETL pipelines. Use when creating sources, debugging pipeline failures, understanding schema evolution, or implementing incremental loading.
---

# dlt Data Load Tool

## Core Concepts

**dlt** handles extract, normalize, and load. You define sources and resources; dlt handles schema inference, table creation, and loading.

## Source Structure

```
src/signalroom/sources/{source_name}/
└── __init__.py  # Contains @dlt.source and @dlt.resource
```

### Creating a New Source

```python
import dlt
from signalroom.common import settings

@dlt.source(name="my_source")
def my_source():
    """Source docstring appears in dlt metadata."""

    @dlt.resource(write_disposition="append", primary_key="id")
    def my_resource():
        yield from fetch_data()

    return [my_resource]
```

### Register in Pipeline Runner

Add to `src/signalroom/pipelines/runner.py`:

```python
SOURCES = {
    "my_source": "signalroom.sources.my_source:my_source",
}
```

## Write Dispositions

| Mode | Use Case | Behavior |
|------|----------|----------|
| `append` | Immutable events (clicks, conversions) | Always insert new rows |
| `merge` | Mutable entities (campaigns, contacts) | Upsert by primary_key |
| `replace` | Full refresh (feature flags, config) | Drop and recreate table |

## Incremental Loading

Only fetch new data since last run:

```python
@dlt.resource(write_disposition="append", primary_key="id")
def events(
    updated_at: dlt.sources.incremental[str] = dlt.sources.incremental(
        "updated_at",
        initial_value="2024-01-01"
    )
):
    # Only fetches records after last loaded timestamp
    yield from api.get_events(since=updated_at.last_value)
```

**WARNING: High-Volume Sources**

`dlt.sources.incremental` tracks every row for deduplication. If many rows share the same cursor value, this causes O(n²) performance.

| Rows per cursor value | Overhead | Recommendation |
|----------------------|----------|----------------|
| < 100 | Negligible | Use incremental |
| 100 - 1,000 | Noticeable | Monitor performance |
| > 1,000 | Severe | Use file-level state instead |

For high-volume sources (like S3 CSV imports), use `dlt.current.resource_state()` for file-level tracking:

```python
@dlt.resource(write_disposition="merge", primary_key=["file_name", "row_id"])
def csv_resource():
    state = dlt.current.resource_state()
    last_date = state.get("last_file_date", "2024-01-01")

    for file in get_files_since(last_date):
        yield from process_file(file)
        state["last_file_date"] = file.date  # Manual state update
```

## Primary Keys

Required for `merge` disposition:

```python
# Single key
@dlt.resource(primary_key="id")

# Composite key
@dlt.resource(primary_key=["date", "affiliate_id"])
```

## Schema Evolution

dlt auto-evolves schemas. New columns added automatically. To see current schema:

```sql
SELECT * FROM {schema}._dlt_loads ORDER BY inserted_at DESC LIMIT 5;
```

## Debugging Failed Loads

### Check dlt metadata tables

```sql
-- Recent loads
SELECT load_id, schema_name, status, inserted_at
FROM {schema}._dlt_loads
ORDER BY inserted_at DESC LIMIT 10;

-- Pipeline state
SELECT * FROM {schema}._dlt_pipeline_state;
```

### Common Errors

**"Primary key violation"**
- Using `append` when you need `merge`
- Duplicate records in source data

**"Column type mismatch"**
- Schema evolved incompatibly
- Fix: Drop table or add explicit column hints

**"Connection refused"**
- Check Supabase pooler settings (port 6543, user format)

### Drop Pending Packages

If pipeline is stuck:

```bash
dlt pipeline {pipeline_name} drop-pending-packages
```

## SignalRoom Sources

| Source | Write Mode | Primary Key | State Tracking |
|--------|------------|-------------|----------------|
| `s3_exports` | merge | `_file_name, _row_id` | File-level (`resource_state`) |
| `everflow` | merge | `date, affiliate_id, advertiser_id` | Row-level (`incremental`) |
| `redtrack` | merge | `date, source_id` | Row-level (`incremental`) |

## Testing Locally

Use DuckDB for fast local testing:

```python
pipeline = dlt.pipeline(
    pipeline_name="test",
    destination="duckdb",
    dataset_name="test"
)
```

## Resources

- [dlt Documentation](https://dlthub.com/docs)
- [Write Dispositions](https://dlthub.com/docs/general-usage/incremental-loading)
- [Schema Evolution](https://dlthub.com/docs/general-usage/schema)
- **SignalRoom API Reference**: `docs/API_REFERENCE.md` — Live docs, auth, request/response examples
