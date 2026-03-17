---
name: etl-elt-patterns
description: Use when designing data pipelines, choosing between ETL and ELT approaches, or implementing data transformation patterns. Covers modern data pipeline architecture.
allowed-tools: Read, Glob, Grep
---

# ETL/ELT Patterns

Patterns for data extraction, loading, and transformation including modern ELT approaches and pipeline design.

## When to Use This Skill

- Choosing between ETL and ELT
- Designing data pipelines
- Implementing data transformations
- Building modern data stacks
- Handling data quality in pipelines

## ETL vs ELT

### ETL (Extract, Transform, Load)

```text
┌─────────┐     ┌─────────────┐     ┌─────────────┐
│ Sources │ ──► │  Transform  │ ──► │  Warehouse  │
└─────────┘     │   Server    │     └─────────────┘
                └─────────────┘
                (Transformation happens
                 before loading)

Characteristics:
- Transform before load
- Requires ETL server/tool
- Schema-on-write
- Traditional approach

Best for:
- Complex transformations
- Limited target storage
- Strict data quality requirements
- Legacy systems
```

### ELT (Extract, Load, Transform)

```text
┌─────────┐     ┌─────────────┐     ┌─────────────┐
│ Sources │ ──► │   Target    │ ──► │  Transform  │
└─────────┘     │  (Load raw) │     │  (in-place) │
                └─────────────┘     └─────────────┘
                                    (Transformation happens
                                     after loading)

Characteristics:
- Load first, transform later
- Uses target system's compute
- Schema-on-read
- Modern approach

Best for:
- Cloud data warehouses
- Flexible exploration
- Iterative development
- Large data volumes
```

### Comparison

| Factor | ETL | ELT |
| ------ | --- | --- |
| Transform timing | Before load | After load |
| Compute location | Separate server | Target system |
| Raw data access | Limited | Full |
| Flexibility | Low | High |
| Latency | Higher | Lower |
| Cost model | ETL server + storage | Storage + target compute |
| Best for | Complex, pre-defined | Exploratory, iterative |

## Modern Data Stack

```text
Extract:        Fivetran, Airbyte, Stitch, Custom
                        │
                        ▼
Load:           Cloud Warehouse (Snowflake, BigQuery, Redshift)
                        │
                        ▼
Transform:      dbt, Dataform, SQLMesh
                        │
                        ▼
Visualize:      Looker, Tableau, Metabase
```

### dbt (Data Build Tool)

```text
Core concepts:
- Models: SQL SELECT statements that define transformations
- Tests: Data quality assertions
- Documentation: Inline docs and lineage
- Macros: Reusable SQL snippets

Example model:
-- models/customers.sql
SELECT
    customer_id,
    first_name,
    last_name,
    order_count
FROM {{ ref('stg_customers') }}
LEFT JOIN {{ ref('customer_orders') }} USING (customer_id)
```

## Pipeline Patterns

### Full Refresh

```text
Strategy: Drop and recreate entire table

Process:
1. Extract all data from source
2. Truncate target table
3. Load all data

Pros: Simple, consistent
Cons: Slow for large tables, can't handle deletes
Best for: Small dimension tables, reference data
```

### Incremental Load

```text
Strategy: Only process new/changed records

Process:
1. Track high watermark (last processed timestamp/ID)
2. Extract records > watermark
3. Merge into target

Pros: Fast, efficient
Cons: Complex, may miss updates
Best for: Large fact tables, event data
```

### Change Data Capture (CDC)

```text
Strategy: Capture all changes from source

Approaches:
┌────────────────────────────────────────────────┐
│ Log-based CDC (Debezium, AWS DMS)              │
│ - Reads database transaction log               │
│ - Captures inserts, updates, deletes           │
│ - No source table modification needed          │
└────────────────────────────────────────────────┘

┌────────────────────────────────────────────────┐
│ Trigger-based CDC                              │
│ - Database triggers on changes                 │
│ - Writes to change table                       │
│ - Adds load to source                          │
└────────────────────────────────────────────────┘

┌────────────────────────────────────────────────┐
│ Timestamp-based CDC                            │
│ - Query by updated_at timestamp                │
│ - Simple but misses hard deletes              │
└────────────────────────────────────────────────┘
```

### Merge (Upsert) Pattern

```sql
-- Snowflake/BigQuery style MERGE
MERGE INTO target t
USING source s ON t.id = s.id
WHEN MATCHED THEN UPDATE SET
    t.name = s.name,
    t.updated_at = CURRENT_TIMESTAMP
WHEN NOT MATCHED THEN INSERT (id, name, created_at)
    VALUES (s.id, s.name, CURRENT_TIMESTAMP);
```

## Data Quality Patterns

### Validation Gates

```text
Pipeline with quality gates:

Extract → Validate → Load → Transform → Validate → Serve
            │                              │
            ▼                              ▼
         Quarantine                    Alert/Block
         (bad records)                 (quality issue)
```

### Quality Checks

```text
Schema validation:
- Required fields present
- Data types match
- Field lengths within limits

Data validation:
- Null checks
- Range checks
- Format validation (dates, emails)
- Referential integrity

Statistical validation:
- Row count within expected range
- Value distributions normal
- No unexpected duplicates
```

### Data Contracts

```text
Define expectations between producer and consumer:

{
  "contract_version": "1.0",
  "schema": {
    "customer_id": {"type": "string", "required": true},
    "email": {"type": "string", "format": "email"},
    "created_at": {"type": "timestamp"}
  },
  "quality": {
    "freshness": "< 1 hour",
    "completeness": "> 99%",
    "row_count": "10000-100000"
  }
}
```

## Pipeline Architecture

### Batch Pipeline

```text
Schedule-based processing:

┌─────────┐     ┌─────────┐     ┌─────────┐
│  Cron   │ ──► │  Spark  │ ──► │   DW    │
│ (daily) │     │  (ETL)  │     │         │
└─────────┘     └─────────┘     └─────────┘

Best for: Non-real-time, large volumes
Tools: Airflow, Dagster, Prefect
```

### Streaming Pipeline

```text
Real-time processing:

┌─────────┐     ┌─────────┐     ┌─────────┐
│  Kafka  │ ──► │  Flink  │ ──► │   DW    │
│(events) │     │(process)│     │(stream) │
└─────────┘     └─────────┘     └─────────┘

Best for: Real-time analytics, event-driven
Tools: Kafka Streams, Flink, Spark Streaming
```

### Lambda Architecture

```text
Batch + Speed layers:

                    ┌─────────────────┐
             ┌────► │   Batch Layer   │ ────┐
             │      │ (comprehensive) │     │
┌─────────┐  │      └─────────────────┘     │  ┌─────────┐
│  Data   │──┤                              ├─►│ Serving │
│ Sources │  │      ┌─────────────────┐     │  │  Layer  │
└─────────┘  └────► │   Speed Layer   │ ────┘  └─────────┘
                    │ (real-time)     │
                    └─────────────────┘

Pros: Complete + real-time
Cons: Complex, duplicate logic
```

### Kappa Architecture

```text
Streaming only (reprocess from log):

┌─────────┐     ┌─────────┐     ┌─────────┐
│  Kafka  │ ──► │ Stream  │ ──► │ Serving │
│  (log)  │     │ Process │     │  Layer  │
└─────────┘     └─────────┘     └─────────┘
      │
      └── Replay for reprocessing

Pros: Simple, single codebase
Cons: Requires replayable log
```

## Orchestration

### DAG-Based Orchestration

```text
Directed Acyclic Graph of tasks:

    extract_a ──┐
                ├── transform ── load
    extract_b ──┘

Tools: Airflow, Dagster, Prefect
```

### Orchestration Best Practices

```text
1. Idempotent tasks (safe to retry)
2. Clear dependencies
3. Appropriate granularity
4. Monitoring and alerting
5. Backfill support
6. Parameterized runs
```

## Error Handling

### Retry Strategies

```text
Transient errors (network, timeout):
- Exponential backoff
- Max retry count
- Circuit breaker

Data errors (validation failure):
- Quarantine bad records
- Continue processing good records
- Alert for review
```

### Dead Letter Queue

```text
Failed records → DLQ → Manual review → Reprocess

Capture:
- Original record
- Error message
- Timestamp
- Retry count
```

## Best Practices

### Pipeline Design

```text
1. Idempotent transformations
2. Clear lineage tracking
3. Appropriate checkpointing
4. Graceful failure handling
5. Comprehensive logging
6. Data quality gates
```

### Performance

```text
1. Partition data appropriately
2. Incremental processing when possible
3. Parallel extraction
4. Efficient file formats (Parquet, ORC)
5. Compression
6. Resource sizing
```

## Related Skills

- `data-architecture` - Data platform design
- `stream-processing` - Real-time processing
- `ml-system-design` - Feature engineering
