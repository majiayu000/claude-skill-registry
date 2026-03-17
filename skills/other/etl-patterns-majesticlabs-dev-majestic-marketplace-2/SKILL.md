---
name: etl-patterns
description: Production ETL patterns orchestrator. Routes to core reliability patterns and incremental load strategies.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

# ETL Patterns

Orchestrator for production-grade Extract-Transform-Load patterns.

## Skill Routing

| Need | Skill | Content |
|------|-------|---------|
| Reliability patterns | `etl-core-patterns` | Idempotency, checkpointing, error handling, chunking, retry, logging |
| Load strategies | `etl-incremental-patterns` | Backfill, timestamp-based, CDC, pipeline orchestration |

## Pattern Selection Guide

### By Reliability Need

| Need | Pattern | Skill |
|------|---------|-------|
| Repeatable runs | Idempotency | `etl-core-patterns` |
| Resume after failure | Checkpointing | `etl-core-patterns` |
| Handle bad records | Error handling + DLQ | `etl-core-patterns` |
| Memory management | Chunked processing | `etl-core-patterns` |
| Network resilience | Retry with backoff | `etl-core-patterns` |
| Observability | Structured logging | `etl-core-patterns` |

### By Load Strategy

| Scenario | Pattern | Skill |
|----------|---------|-------|
| Small tables (<100K) | Full refresh | `etl-incremental-patterns` |
| Large tables | Timestamp incremental | `etl-incremental-patterns` |
| Real-time sync | CDC events | `etl-incremental-patterns` |
| Historical migration | Parallel backfill | `etl-incremental-patterns` |
| Zero-downtime refresh | Swap pattern | `etl-incremental-patterns` |
| Multi-step pipelines | Pipeline orchestration | `etl-incremental-patterns` |

## Quick Reference

### Idempotency Options

```python
# Small datasets: Delete-then-insert
# Large datasets: UPSERT on conflict
# Change detection: Row hash comparison
```

### Load Strategy Decision

```
Is table < 100K rows?
  → Full refresh

Has reliable timestamp column?
  → Timestamp incremental

Source supports CDC?
  → CDC event processing

Need zero downtime?
  → Swap pattern (temp table → rename)

One-time historical load?
  → Parallel backfill with date ranges
```

## Common Pipeline Structure

```python
# 1. Setup
checkpoint = Checkpoint('.etl_checkpoint.json')
processor = ETLProcessor()

# 2. Extract (with incremental)
df = incremental_by_timestamp(source_table, 'updated_at')

# 3. Transform (with error handling)
transformed = processor.process_batch(df.to_dict('records'))

# 4. Load (with idempotency)
upsert_records(pd.DataFrame(transformed))

# 5. Checkpoint
checkpoint.set_last_processed('sync', df['updated_at'].max())

# 6. Handle failures
processor.save_failures('failures/')
```

## Related Skills

- `data-validation` - Validate data quality during ETL
- `data-quality` - Monitor data quality metrics
- `pandas-coder` - DataFrame transformations
