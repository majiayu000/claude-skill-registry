---
name: pipeline-design
description: Design ETL/ELT pipeline architectures with proper patterns for reliability and scalability.
---

# Pipeline Design

## ETL vs ELT

| Approach | When to Use |
|----------|-------------|
| **ETL** | Transform before load, limited warehouse compute |
| **ELT** | Modern warehouses (Snowflake, BigQuery, Redshift) |

## Pipeline Patterns

### Batch

```
Source → Extract → Stage → Transform → Load → Target
         │                    │
         └── Checkpoint ──────┘
```

- Scheduled intervals (hourly, daily)
- Full or incremental loads
- Idempotent operations

### Streaming

```
Source → Kafka/Kinesis → Process → Sink
              │
              └── State Store
```

- Real-time requirements
- Event-driven architecture
- Exactly-once semantics

## Design Principles

1. **Idempotent** - Safe to re-run
2. **Incremental** - Process only new/changed data
3. **Observable** - Metrics, logs, alerts
4. **Testable** - Unit tests for transformations
5. **Recoverable** - Checkpoints, retry logic

## Staging Pattern

```sql
-- 1. Land raw data
COPY INTO raw.source_data FROM @stage;

-- 2. Deduplicate
CREATE TABLE staging.deduped AS
SELECT * FROM raw.source_data
QUALIFY ROW_NUMBER() OVER (PARTITION BY id ORDER BY _loaded_at DESC) = 1;

-- 3. Transform to target
MERGE INTO target.dim_customer
USING staging.deduped
ON target.id = staging.id
WHEN MATCHED THEN UPDATE ...
WHEN NOT MATCHED THEN INSERT ...;
```

## Error Handling

- Dead letter queues for failed records
- Retry with exponential backoff
- Alert on threshold breaches
- Quarantine bad data for review
