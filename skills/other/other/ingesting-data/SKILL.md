---
name: ingesting-data
description: Data ingestion patterns for loading data from cloud storage, APIs, files, and streaming sources into databases. Use when importing CSV/JSON/Parquet files, pulling from S3/GCS buckets, consuming API feeds, or building ETL pipelines.
---

# Data Ingestion Patterns

This skill provides patterns for getting data INTO systems from external sources.

## When to Use This Skill

- Importing CSV, JSON, Parquet, or Excel files
- Loading data from S3, GCS, or Azure Blob storage
- Consuming REST/GraphQL API feeds
- Building ETL/ELT pipelines
- Database migration and CDC (Change Data Capture)
- Streaming data ingestion from Kafka/Kinesis

## Ingestion Pattern Decision Tree

```
What is your data source?
├── Cloud Storage (S3, GCS, Azure) → See cloud-storage.md
├── Files (CSV, JSON, Parquet) → See file-formats.md
├── REST/GraphQL APIs → See api-feeds.md
├── Streaming (Kafka, Kinesis) → See streaming-sources.md
├── Legacy Database → See database-migration.md
└── Need full ETL framework → See etl-tools.md
```

## Quick Start by Language

### Python (Recommended for ETL)

**dlt (data load tool) - Modern Python ETL:**
```python
import dlt

# Define a source
@dlt.source
def github_source(repo: str):
    @dlt.resource(write_disposition="merge", primary_key="id")
    def issues():
        response = requests.get(f"https://api.github.com/repos/{repo}/issues")
        yield response.json()
    return issues

# Load to destination
pipeline = dlt.pipeline(
    pipeline_name="github_issues",
    destination="postgres",  # or duckdb, bigquery, snowflake
    dataset_name="github_data"
)

load_info = pipeline.run(github_source("owner/repo"))
print(load_info)
```

**Polars for file processing (faster than pandas):**
```python
import polars as pl

# Read CSV with schema inference
df = pl.read_csv("data.csv")

# Read Parquet (columnar, efficient)
df = pl.read_parquet("s3://bucket/data.parquet")

# Read JSON lines
df = pl.read_ndjson("events.jsonl")

# Write to database
df.write_database(
    table_name="events",
    connection="postgresql://user:pass@localhost/db",
    if_table_exists="append"
)
```

### TypeScript/Node.js

**S3 ingestion:**
```typescript
import { S3Client, GetObjectCommand } from "@aws-sdk/client-s3";
import { parse } from "csv-parse/sync";

const s3 = new S3Client({ region: "us-east-1" });

async function ingestFromS3(bucket: string, key: string) {
  const response = await s3.send(new GetObjectCommand({ Bucket: bucket, Key: key }));
  const body = await response.Body?.transformToString();

  // Parse CSV
  const records = parse(body, { columns: true, skip_empty_lines: true });

  // Insert to database
  await db.insert(eventsTable).values(records);
}
```

**API feed polling:**
```typescript
import { Hono } from "hono";

// Webhook receiver for real-time ingestion
const app = new Hono();

app.post("/webhooks/stripe", async (c) => {
  const event = await c.req.json();

  // Validate webhook signature
  const signature = c.req.header("stripe-signature");
  // ... validation logic

  // Ingest event
  await db.insert(stripeEventsTable).values({
    eventId: event.id,
    type: event.type,
    data: event.data,
    receivedAt: new Date()
  });

  return c.json({ received: true });
});
```

### Rust

**High-performance file ingestion:**
```rust
use polars::prelude::*;
use aws_sdk_s3::Client;

async fn ingest_parquet(client: &Client, bucket: &str, key: &str) -> Result<DataFrame> {
    // Download from S3
    let resp = client.get_object()
        .bucket(bucket)
        .key(key)
        .send()
        .await?;

    let bytes = resp.body.collect().await?.into_bytes();

    // Parse with Polars
    let df = ParquetReader::new(Cursor::new(bytes))
        .finish()?;

    Ok(df)
}
```

### Go

**Concurrent file processing:**
```go
package main

import (
    "context"
    "encoding/csv"
    "github.com/aws/aws-sdk-go-v2/service/s3"
)

func ingestCSV(ctx context.Context, client *s3.Client, bucket, key string) error {
    resp, err := client.GetObject(ctx, &s3.GetObjectInput{
        Bucket: &bucket,
        Key:    &key,
    })
    if err != nil {
        return err
    }
    defer resp.Body.Close()

    reader := csv.NewReader(resp.Body)
    records, err := reader.ReadAll()
    if err != nil {
        return err
    }

    // Batch insert to database
    return batchInsert(ctx, records)
}
```

## Ingestion Patterns

### 1. Batch Ingestion (Files/Storage)

For periodic bulk loads:

```
Source → Extract → Transform → Load → Validate
  ↓         ↓          ↓         ↓        ↓
 S3      Download   Clean/Map  Insert   Count check
```

**Key considerations:**
- Use chunked reading for large files (>100MB)
- Implement idempotency with checksums
- Track file processing state
- Handle partial failures

### 2. Streaming Ingestion (Real-time)

For continuous data flow:

```
Source → Buffer → Process → Load → Ack
  ↓        ↓         ↓        ↓      ↓
Kafka   In-memory  Transform  DB   Commit offset
```

**Key considerations:**
- At-least-once vs exactly-once semantics
- Backpressure handling
- Dead letter queues for failures
- Checkpoint management

### 3. API Polling (Feeds)

For external API data:

```
Schedule → Fetch → Dedupe → Load → Update cursor
   ↓         ↓        ↓       ↓         ↓
 Cron     API call  By ID   Insert   Last timestamp
```

**Key considerations:**
- Rate limiting and backoff
- Incremental loading (cursors, timestamps)
- API pagination handling
- Retry with exponential backoff

### 4. Change Data Capture (CDC)

For database replication:

```
Source DB → Capture changes → Transform → Target DB
    ↓             ↓               ↓            ↓
 Postgres    Debezium/WAL      Map schema   Insert/Update
```

**Key considerations:**
- Initial snapshot + streaming changes
- Schema evolution handling
- Ordering guarantees
- Conflict resolution

## Library Recommendations

| Use Case | Python | TypeScript | Rust | Go |
|----------|--------|------------|------|-----|
| **ETL Framework** | dlt, Meltano, Dagster | - | - | - |
| **Cloud Storage** | boto3, gcsfs, adlfs | @aws-sdk/*, @google-cloud/* | aws-sdk-s3, object_store | aws-sdk-go-v2 |
| **File Processing** | polars, pandas, pyarrow | papaparse, xlsx, parquetjs | polars-rs, arrow-rs | encoding/csv, parquet-go |
| **Streaming** | confluent-kafka, aiokafka | kafkajs | rdkafka-rs | franz-go, sarama |
| **CDC** | Debezium, pg_logical | - | - | - |

## Reference Documentation

- `references/cloud-storage.md` - S3, GCS, Azure Blob patterns
- `references/file-formats.md` - CSV, JSON, Parquet, Excel handling
- `references/api-feeds.md` - REST polling, webhooks, GraphQL subscriptions
- `references/streaming-sources.md` - Kafka, Kinesis, Pub/Sub
- `references/database-migration.md` - Schema migration, CDC patterns
- `references/etl-tools.md` - dlt, Meltano, Airbyte, Fivetran

## Scripts

- `scripts/validate_csv_schema.py` - Validate CSV against expected schema
- `scripts/test_s3_connection.py` - Test S3 bucket connectivity
- `scripts/generate_dlt_pipeline.py` - Generate dlt pipeline scaffold

## Chaining with Database Skills

After ingestion, chain to appropriate database skill:

| Destination | Chain to Skill |
|-------------|----------------|
| PostgreSQL, MySQL | `databases-relational` |
| MongoDB, DynamoDB | `databases-document` |
| Qdrant, Pinecone | `databases-vector` (after embedding) |
| ClickHouse, TimescaleDB | `databases-timeseries` |
| Neo4j | `databases-graph` |

For vector databases, chain through `ai-data-engineering` for embedding:
```
ingesting-data → ai-data-engineering → databases-vector
```
