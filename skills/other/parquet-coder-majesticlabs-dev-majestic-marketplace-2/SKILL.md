---
name: parquet-coder
description: Columnar file patterns including partitioning, predicate pushdown, and schema evolution.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

# Parquet-Coder

Patterns for efficient columnar data storage with Parquet.

## Basic Operations

```python
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

# Write with compression
df.to_parquet('data.parquet', compression='snappy', index=False)

# Common compression options:
# - snappy: Fast, good compression (default)
# - gzip: Slower, better compression
# - zstd: Best balance of speed/compression
# - None: No compression (fastest writes)

# Read entire file
df = pd.read_parquet('data.parquet')

# Read specific columns only (predicate pushdown)
df = pd.read_parquet('data.parquet', columns=['id', 'name', 'value'])
```

## PyArrow for Large Files

```python
# Read as PyArrow Table (more memory efficient)
table = pq.read_table('data.parquet')

# Convert to pandas when needed
df = table.to_pandas()

# Filter while reading (row group filtering)
table = pq.read_table(
    'data.parquet',
    filters=[
        ('date', '>=', '2024-01-01'),
        ('status', '=', 'active')
    ]
)

# Read in batches for huge files
parquet_file = pq.ParquetFile('huge.parquet')
for batch in parquet_file.iter_batches(batch_size=100_000):
    df_batch = batch.to_pandas()
    process(df_batch)
```

## Partitioned Datasets

```python
# Write partitioned by columns
df.to_parquet(
    'data/',
    partition_cols=['year', 'month'],
    compression='snappy'
)
# Creates: data/year=2024/month=01/part-0.parquet

# Read partitioned dataset
df = pd.read_parquet('data/')  # Reads all partitions

# Read specific partitions only
df = pd.read_parquet('data/year=2024/')

# With PyArrow dataset API (more control)
import pyarrow.dataset as ds

dataset = ds.dataset('data/', format='parquet', partitioning='hive')

# Filter on partition columns (very fast)
table = dataset.to_table(
    filter=(ds.field('year') == 2024) & (ds.field('month') >= 6)
)
```

## Schema Definition

```python
# Explicit schema for consistency
schema = pa.schema([
    ('id', pa.int64()),
    ('name', pa.string()),
    ('value', pa.float64()),
    ('date', pa.date32()),
    ('tags', pa.list_(pa.string())),
    ('metadata', pa.map_(pa.string(), pa.string())),
])

# Write with schema
table = pa.Table.from_pandas(df, schema=schema)
pq.write_table(table, 'data.parquet')

# Read and validate schema
file_schema = pq.read_schema('data.parquet')
assert file_schema.equals(schema), "Schema mismatch!"
```

## Schema Evolution

```python
def merge_schemas(old_schema: pa.Schema, new_schema: pa.Schema) -> pa.Schema:
    """Create unified schema from old and new."""
    fields = {f.name: f for f in old_schema}
    for field in new_schema:
        if field.name not in fields:
            fields[field.name] = field
        elif fields[field.name].type != field.type:
            # Handle type conflicts (e.g., promote int to float)
            fields[field.name] = pa.field(
                field.name,
                promote_type(fields[field.name].type, field.type)
            )
    return pa.schema(list(fields.values()))

def append_with_schema_evolution(
    existing_path: str,
    new_df: pd.DataFrame,
    output_path: str
) -> None:
    """Append data with automatic schema evolution."""
    existing = pq.read_table(existing_path)
    new_table = pa.Table.from_pandas(new_df)

    # Unify schemas
    unified_schema = pa.unify_schemas([existing.schema, new_table.schema])

    # Cast both to unified schema
    existing = existing.cast(unified_schema)
    new_table = new_table.cast(unified_schema)

    # Concatenate and write
    combined = pa.concat_tables([existing, new_table])
    pq.write_table(combined, output_path)
```

## Row Group Optimization

```python
# Control row group size (affects read performance)
pq.write_table(
    table,
    'data.parquet',
    row_group_size=100_000,  # Rows per group
    compression='snappy'
)

# Read metadata to see row groups
parquet_file = pq.ParquetFile('data.parquet')
print(f"Num row groups: {parquet_file.metadata.num_row_groups}")
print(f"Num rows: {parquet_file.metadata.num_rows}")

# Read specific row groups
table = parquet_file.read_row_groups([0, 1])  # First two groups
```

## Metadata and Statistics

```python
# Add custom metadata
custom_metadata = {
    b'created_by': b'etl_pipeline',
    b'version': b'1.0',
    b'source': b'api_export'
}
schema = table.schema.with_metadata(custom_metadata)
table = table.cast(schema)
pq.write_table(table, 'data.parquet')

# Read metadata
parquet_file = pq.ParquetFile('data.parquet')
print(parquet_file.schema.metadata)

# Column statistics (min/max for filtering)
metadata = parquet_file.metadata
for i in range(metadata.num_row_groups):
    rg = metadata.row_group(i)
    for j in range(rg.num_columns):
        col = rg.column(j)
        if col.statistics:
            print(f"{col.path_in_schema}: min={col.statistics.min}, max={col.statistics.max}")
```

## Delta Lake Integration

```python
from deltalake import DeltaTable, write_deltalake

# Write as Delta table (versioned parquet)
write_deltalake('delta_table/', df, mode='overwrite')

# Append data
write_deltalake('delta_table/', new_df, mode='append')

# Read Delta table
dt = DeltaTable('delta_table/')
df = dt.to_pandas()

# Time travel
df_old = dt.load_version(0).to_pandas()

# Compact small files
dt.optimize.compact()

# Vacuum old versions
dt.vacuum(retention_hours=168)  # Keep 7 days
```

## Performance Tips

```python
# 1. Use appropriate column types
schema = pa.schema([
    ('category', pa.dictionary(pa.int8(), pa.string())),  # For repeated strings
    ('count', pa.int32()),  # Not int64 if values fit
])

# 2. Sort data before writing (improves predicate pushdown)
df = df.sort_values(['date', 'category'])
df.to_parquet('sorted.parquet')

# 3. Use column selection
df = pd.read_parquet('data.parquet', columns=['needed', 'columns'])

# 4. Use filters for row pruning
df = pd.read_parquet('data/', filters=[('status', '==', 'active')])

# 5. Parallel reads
import pyarrow.dataset as ds
dataset = ds.dataset('data/', format='parquet')
table = dataset.to_table(use_threads=True)
```

## Conversion Utilities

```python
def csv_to_parquet(
    csv_path: str,
    parquet_path: str,
    chunk_size: int = 100_000
) -> None:
    """Convert large CSV to Parquet efficiently."""
    writer = None

    for chunk in pd.read_csv(csv_path, chunksize=chunk_size):
        table = pa.Table.from_pandas(chunk)

        if writer is None:
            writer = pq.ParquetWriter(parquet_path, table.schema)

        writer.write_table(table)

    writer.close()

def json_to_parquet(json_path: str, parquet_path: str) -> None:
    """Convert JSON lines to Parquet."""
    df = pd.read_json(json_path, lines=True)
    df.to_parquet(parquet_path, compression='snappy')
```
