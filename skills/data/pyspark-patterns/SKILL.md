---
name: pyspark-patterns
description: PySpark best practices, TableUtilities methods, ETL patterns, logging standards, and DataFrame operations for this project. Use when writing or debugging PySpark code.
---

# PySpark Patterns & Best Practices

Comprehensive guide to PySpark patterns used in the Unify data migration project.

## Core Principle

**Always use DataFrame operations over raw SQL** when possible.

## TableUtilities Class Methods

Central utility class providing standardized DataFrame operations.

### add_row_hash()
Add hash column for change detection and deduplication.

```python
table_utilities = TableUtilities()
df_with_hash = table_utilities.add_row_hash(df)
```

### save_as_table()
Standard table save with timestamp conversion and automatic filtering.

```python
table_utilities.save_as_table(df, "database.table_name")
```

**Features**:
- Converts timestamp columns automatically
- Filters to last N years when `date_created` column exists (controlled by `NUMBER_OF_YEARS`)
- Prevents full dataset processing in local development

### clean_date_time_columns()
Intelligent timestamp parsing for various date formats.

```python
df_cleaned = table_utilities.clean_date_time_columns(df)
```

### Deduplication Methods

**Simple deduplication** (all columns):
```python
df_deduped = table_utilities.drop_duplicates_simple(df)
```

**Advanced deduplication** (specific columns, ordering):
```python
df_deduped = table_utilities.drop_duplicates_advanced(
    df,
    partition_columns=["id"],
    order_columns=["date_created"]
)
```

### filter_and_drop_column()
Remove duplicate flags after processing.

```python
df_filtered = table_utilities.filter_and_drop_column(df, "is_duplicate")
```

### generate_deduplicate()
Compare with existing table and identify new/changed records.

```python
df_new = table_utilities.generate_deduplicate(df, "database.existing_table")
```

### generate_unique_ids()
Generate auto-incrementing unique identifiers.

```python
df_with_id = table_utilities.generate_unique_ids(df, "unique_id_column_name")
```

## ETL Class Pattern

All silver and gold transformations follow this standardized pattern:

```python
class TableName:
    def __init__(self, bronze_table_name: str):
        self.bronze_table_name = bronze_table_name
        self.silver_database_name = f"silver_{self.bronze_table_name.split('.')[0].split('_')[-1]}"
        self.silver_table_name = self.bronze_table_name.split(".")[-1].replace("b_", "s_")

        # Execute ETL pipeline
        self.extract_sdf = self.extract()
        self.transform_sdf = self.transform()
        self.load()

    @synapse_error_print_handler
    def extract(self) -> DataFrame:
        """Extract data from source tables."""
        logger.info(f"Extracting from {self.bronze_table_name}")
        df = spark.table(self.bronze_table_name)
        logger.success(f"Extracted {df.count()} records")
        return df

    @synapse_error_print_handler
    def transform(self) -> DataFrame:
        """Transform data according to business rules."""
        logger.info("Starting transformation")
        # Apply transformations
        transformed_df = self.extract_sdf.filter(...).select(...)
        logger.success("Transformation complete")
        return transformed_df

    @synapse_error_print_handler
    def load(self) -> None:
        """Load data to target table."""
        logger.info(f"Loading to {self.silver_database_name}.{self.silver_table_name}")
        table_utilities.save_as_table(
            self.transform_sdf,
            f"{self.silver_database_name}.{self.silver_table_name}"
        )
        logger.success(f"Successfully loaded {self.silver_table_name}")


# Instantiate with exception handling
try:
    TableName("bronze_database.b_table_name")
except Exception as e:
    logger.error(f"Error processing TableName: {str(e)}")
    raise e
```

## Logging Standards

### Use NotebookLogger (Never print())

```python
from utilities.session_optimiser import NotebookLogger

logger = NotebookLogger()

# Log levels
logger.info("Starting process")           # Informational messages
logger.warning("Potential issue detected") # Warnings
logger.error("Operation failed")          # Errors
logger.success("Process completed")       # Success messages
```

### Logging Best Practices

1. **Always include table/database names**:
   ```python
   logger.info(f"Processing table {database}.{table}")
   ```

2. **Log at key milestones**:
   ```python
   logger.info("Starting extraction")
   # ... extraction code
   logger.success("Extraction complete")
   ```

3. **Include counts and metrics**:
   ```python
   logger.info(f"Extracted {df.count()} records from {table}")
   ```

4. **Error context**:
   ```python
   logger.error(f"Failed to process {table}: {str(e)}")
   ```

## Error Handling Pattern

### @synapse_error_print_handler Decorator

Wrap ALL processing functions with this decorator:

```python
from utilities.session_optimiser import synapse_error_print_handler

@synapse_error_print_handler
def extract(self) -> DataFrame:
    # Your code here
    return df
```

**Benefits**:
- Consistent error handling across codebase
- Automatic error logging
- Graceful error propagation

### Exception Handling at Instantiation

```python
try:
    MyETLClass("source_table")
except Exception as e:
    logger.error(f"Error processing MyETLClass: {str(e)}")
    raise e
```

## DataFrame Operations Patterns

### Filtering
```python
# Use col() for clarity
from pyspark.sql.functions import col

df_filtered = df.filter(col("status") == "active")
df_filtered = df.filter((col("age") > 18) & (col("country") == "AU"))
```

### Selecting and Aliasing
```python
from pyspark.sql.functions import col, lit

df_selected = df.select(
    col("id"),
    col("name").alias("person_name"),
    lit("constant_value").alias("constant_column")
)
```

### Joins
```python
# Always use explicit join keys and type
df_joined = df1.join(
    df2,
    df1["id"] == df2["person_id"],
    "inner"  # inner, left, right, outer
)

# Drop duplicate columns after join
df_joined = df_joined.drop(df2["person_id"])
```

### Window Functions
```python
from pyspark.sql import Window
from pyspark.sql.functions import row_number, rank, dense_rank

window_spec = Window.partitionBy("category").orderBy(col("date").desc())

df_windowed = df.withColumn(
    "row_num",
    row_number().over(window_spec)
).filter(col("row_num") == 1)
```

### Aggregations
```python
from pyspark.sql.functions import sum, avg, count, max, min

df_agg = df.groupBy("category").agg(
    count("*").alias("total_count"),
    sum("amount").alias("total_amount"),
    avg("amount").alias("avg_amount")
)
```

## JDBC Connection Pattern

```python
def get_connection_properties() -> dict:
    """Get JDBC connection properties."""
    return {
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
        "driver": "com.microsoft.sqlserver.jdbc.SQLServerDriver"
    }

# Use for JDBC reads
df = spark.read.jdbc(
    url=jdbc_url,
    table="schema.table",
    properties=get_connection_properties()
)
```

## Session Management

### Get Optimized Spark Session
```python
from utilities.session_optimiser import SparkOptimiser

spark = SparkOptimiser.get_optimised_spark_session()
```

### Reset Spark Context
```python
table_utilities.reset_spark_context()
```

**When to use**:
- Memory issues
- Multiple Spark sessions
- After large operations

## Memory Management

### Caching
```python
# Cache frequently accessed DataFrames
df_cached = df.cache()

# Unpersist when done
df_cached.unpersist()
```

### Partitioning
```python
# Repartition for better parallelism
df_repartitioned = df.repartition(10)

# Coalesce to reduce partitions
df_coalesced = df.coalesce(1)
```

## Common Pitfalls to Avoid

1. **Don't use print() statements** - Use logger methods
2. **Don't read entire tables without filtering** - Filter early
3. **Don't create DataFrames inside loops** - Collect and batch
4. **Don't use collect() on large DataFrames** - Process distributedly
5. **Don't forget to unpersist cached DataFrames** - Memory leaks

## Performance Tips

1. **Filter early**: Reduce data volume ASAP
2. **Use broadcast for small tables**: Optimize joins
3. **Partition strategically**: Balance parallelism
4. **Cache wisely**: Only for reused DataFrames
5. **Use window functions**: Instead of self-joins

## Code Quality Standards

### Type Hints
```python
from pyspark.sql import DataFrame

def process_data(df: DataFrame, table_name: str) -> DataFrame:
    return df.filter(col("active") == True)
```

### Line Length
**Maximum: 240 characters** (not standard 88/120)

### Blank Lines
**No blank lines inside functions** - Keep functions compact

### Imports
All imports at top of file, never inside functions
```python
from pyspark.sql import DataFrame
from pyspark.sql.functions import col, lit, when
from utilities.session_optimiser import TableUtilities, NotebookLogger
```
