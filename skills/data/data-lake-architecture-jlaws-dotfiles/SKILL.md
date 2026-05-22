---
name: data-lake-architecture
description: Design lakehouse architectures with Apache Iceberg, Delta Lake, and modern table formats
---

# Data Lake Architecture

## Decision Table

| Criteria | Apache Iceberg | Delta Lake | Apache Hudi |
|----------|---------------|------------|-------------|
| Multi-engine support | Best (Spark, Trino, Flink, DuckDB) | Good (Spark-native, growing) | Good (Spark, Flink) |
| Schema evolution | Full (add, drop, rename, reorder) | Add/rename columns | Add columns |
| Hidden partitioning | Yes (no partition columns in queries) | No (explicit partition cols) | No |
| Partition evolution | Yes (change without rewrite) | No (requires rewrite) | No |
| Time travel | Snapshot-based, configurable | Version-based, 30-day default | Timeline-based |
| CDC / upserts | Merge-on-read or copy-on-write | MERGE INTO | Built-in (MoR native) |
| Best for | Multi-engine lakehouse | Databricks-centric orgs | CDC-heavy workloads |

## Apache Iceberg

### PyIceberg Catalog and Table Creation

```python
# iceberg_setup.py
from pyiceberg.catalog import load_catalog
from pyiceberg.schema import Schema
from pyiceberg.types import NestedField, StringType, LongType, TimestampType, DoubleType
from pyiceberg.partitioning import PartitionSpec, PartitionField
from pyiceberg.transforms import DayTransform, BucketTransform

catalog = load_catalog("production", **{
    "type": "rest", "uri": "http://iceberg-rest:8181",
    "s3.endpoint": "http://minio:9000",
    "s3.access-key-id": "admin", "s3.secret-access-key": "password",
})

schema = Schema(
    NestedField(1, "event_id", StringType(), required=True),
    NestedField(2, "user_id", StringType(), required=True),
    NestedField(3, "event_type", StringType(), required=True),
    NestedField(4, "timestamp", TimestampType(), required=True),
)
# hidden partitioning: users write timestamp, Iceberg partitions by day
spec = PartitionSpec(PartitionField(
    source_id=4, field_id=1000, transform=DayTransform(), name="day"))

table = catalog.create_table("analytics.events", schema=schema, partition_spec=spec)
```

### Schema Evolution and Partition Evolution

```python
# schema_evolution.py
table = catalog.load_table("analytics.events")

# add columns (no rewrite needed)
with table.update_schema() as update:
    update.add_column("amount", DoubleType())
    update.add_column("region", StringType())

# rename column
with table.update_schema() as update:
    update.rename_column("region", "geo_region")

# partition evolution: change strategy without rewriting data
with table.update_spec() as update:
    update.add_field("user_bucket", BucketTransform(16), source_column_name="user_id")
```

### Time Travel

```python
# time_travel.py
table = catalog.load_table("analytics.events")

for snapshot in table.metadata.snapshots:
    print(f"ID: {snapshot.snapshot_id}, Time: {snapshot.timestamp_ms}")

# read at specific snapshot
df = table.scan(snapshot_id=123456789).to_pandas()

# read as of timestamp
from datetime import datetime
snap = table.snapshot_as_of_timestamp(int(datetime(2025, 1, 15).timestamp() * 1000))
df = table.scan(snapshot_id=snap.snapshot_id).to_pandas()
```

## Delta Lake

### PySpark Operations and MERGE INTO

```python
# delta_operations.py
from pyspark.sql import SparkSession
from delta.tables import DeltaTable

spark = (SparkSession.builder.appName("delta-lakehouse")
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
    .config("spark.sql.catalog.spark_catalog",
            "org.apache.spark.sql.delta.catalog.DeltaCatalog")
    .getOrCreate())

# write initial table
df = spark.read.parquet("s3://raw/events/")
df.write.format("delta").partitionBy("event_date").mode("overwrite").save("s3://lakehouse/events")

# MERGE INTO (upsert)
target = DeltaTable.forPath(spark, "s3://lakehouse/customers")
source = spark.read.parquet("s3://staging/customers_update/")
(target.alias("t")
 .merge(source.alias("s"), "t.customer_id = s.customer_id")
 .whenMatchedUpdate(set={"name": "s.name", "email": "s.email", "updated_at": "s.updated_at"})
 .whenNotMatchedInsert(values={
     "customer_id": "s.customer_id", "name": "s.name",
     "email": "s.email", "updated_at": "s.updated_at",
 })
 .whenNotMatchedBySourceDelete()
 .execute())
```

### OPTIMIZE, VACUUM, and Change Data Feed

```python
# delta_maintenance.py
dt = DeltaTable.forPath(spark, "s3://lakehouse/events")
dt.optimize().executeCompaction()                    # compact small files
dt.optimize().executeZOrderBy("user_id", "event_date")  # multi-dimensional clustering
dt.vacuum(retentionHours=168)                        # remove old files (7 days)

# enable change data feed
spark.sql("""ALTER TABLE delta.`s3://lakehouse/events`
    SET TBLPROPERTIES (delta.enableChangeDataFeed = true)""")

# read change feed
changes = (spark.read.format("delta")
    .option("readChangeFeed", "true").option("startingVersion", 10)
    .load("s3://lakehouse/events"))
# _change_type: insert, update_preimage, update_postimage, delete
```

## Query Engine Integration

### DuckDB with Iceberg

```python
# duckdb_iceberg.py
import duckdb

con = duckdb.connect()
con.install_extension("iceberg")
con.load_extension("iceberg")

df = con.sql("""
    SELECT user_id, count(*) as events, sum(amount) as total
    FROM iceberg_scan('s3://lakehouse/analytics/events')
    WHERE timestamp >= '2025-01-01'
    GROUP BY user_id ORDER BY total DESC LIMIT 100
""").fetchdf()
```

### Trino with Iceberg

```sql
-- trino query against Iceberg catalog
SELECT date_trunc('hour', event_time) AS hour,
       count(*) AS events,
       approx_percentile(latency_ms, 0.99) AS p99
FROM iceberg.analytics.api_events
WHERE event_time >= current_date - INTERVAL '7' DAY
GROUP BY 1 ORDER BY 1;

-- time travel
SELECT * FROM iceberg.analytics.events FOR VERSION AS OF 123456789;
```

## Compaction and File Sizing

```python
# compaction.py -- Iceberg maintenance via Spark
spark.sql("""CALL system.rewrite_data_files(
    table => 'analytics.events', strategy => 'sort',
    sort_order => 'user_id ASC, timestamp DESC',
    options => map(
        'target-file-size-bytes', '134217728',
        'min-file-size-bytes', '67108864',
        'max-file-size-bytes', '201326592'))""")

# expire old snapshots
spark.sql("""CALL system.expire_snapshots(
    table => 'analytics.events',
    older_than => TIMESTAMP '2025-01-01 00:00:00', retain_last => 10)""")

# remove orphan files from failed writes
spark.sql("""CALL system.remove_orphan_files(
    table => 'analytics.events',
    older_than => TIMESTAMP '2025-01-01 00:00:00')""")
```

## Gotchas

- **Small file problem** -- frequent writes create thousands of tiny files; schedule compaction regularly
- **VACUUM too aggressive** -- retention below 7 days (Delta) risks breaking concurrent readers
- **Partition cardinality** -- too many partitions (>10K) degrades metadata; use bucket transforms
- **Schema evolution with Parquet** -- column renames work in Iceberg (name-based) but break raw Parquet (position-based)
- **Catalog lock contention** -- concurrent writers need atomic commits; use catalog-level locking
- **Cost of time travel** -- every snapshot retains file references; unbounded snapshots bloat metadata
- **Delta outside Databricks** -- UniForm improves compatibility but some features are Databricks-only
- **DuckDB Iceberg scanning** -- reads metadata tree per query; for hot queries, materialize to local Parquet
- **Partition evolution pitfall** -- old data keeps old layout; spanning queries may scan more files
- **Z-order diminishing returns** -- effective for 2-4 columns; beyond that, benefits drop sharply
