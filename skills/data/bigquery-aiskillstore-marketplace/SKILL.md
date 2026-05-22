---
name: bigquery
description: Comprehensive guide for using BigQuery CLI (bq) to query and inspect tables in Monzo's BigQuery projects, with emphasis on data sensitivity and INFORMATION_SCHEMA queries.
---

# BigQuery CLI Skill

This skill provides comprehensive guidance on using the BigQuery CLI (`bq`) for querying and inspecting data in Monzo's BigQuery projects.

## Core Principles

1. **Always specify the project explicitly** using `--project_id=PROJECT_NAME`
2. **Always use Standard SQL** with `--use_legacy_sql=false`
3. **Respect data sensitivity** - avoid querying actual content from sensitive tables
4. **Use INFORMATION_SCHEMA** for metadata queries (schemas, columns, tables)

## Common Query Patterns

### 1. Check Table Schema (INFORMATION_SCHEMA)

Use this to inspect column names, types, and structure **without accessing sensitive data**:

```bash
bq query --project_id=monzo-analytics --use_legacy_sql=false \
  "SELECT column_name, data_type, is_nullable
   FROM \`monzo-analytics.DATASET_NAME.INFORMATION_SCHEMA.COLUMNS\`
   WHERE table_name = 'TABLE_NAME'
   ORDER BY ordinal_position"
```

**Examples:**
```bash
# Check dims dataset table schema
bq query --project_id=monzo-analytics --use_legacy_sql=false \
  "SELECT column_name, data_type FROM \`monzo-analytics.dims.INFORMATION_SCHEMA.COLUMNS\`
   WHERE table_name = 'vulnerable_customer_logs_dim' ORDER BY ordinal_position"

# Check prod dataset table schema
bq query --project_id=monzo-analytics --use_legacy_sql=false \
  "SELECT column_name, data_type FROM \`monzo-analytics.prod.INFORMATION_SCHEMA.COLUMNS\`
   WHERE table_name = 'transactions' ORDER BY ordinal_position"
```

### 2. Count Rows (Safe for Sensitive Tables)

Use `COUNT(*)` to check table size without exposing data:

```bash
bq query --project_id=monzo-analytics --use_legacy_sql=false \
  "SELECT COUNT(*) as row_count FROM \`monzo-analytics.DATASET.TABLE_NAME\`"
```

**Example:**
```bash
bq query --project_id=monzo-analytics --use_legacy_sql=false \
  "SELECT COUNT(*) as row_count FROM \`monzo-analytics.dims.vulnerable_customer_logs_dim\`"
```

### 3. List All Tables in a Dataset

```bash
bq query --project_id=monzo-analytics --use_legacy_sql=false \
  "SELECT table_name, table_type
   FROM \`monzo-analytics.DATASET_NAME.INFORMATION_SCHEMA.TABLES\`
   ORDER BY table_name"
```

**Example:**
```bash
bq query --project_id=monzo-analytics --use_legacy_sql=false \
  "SELECT table_name FROM \`monzo-analytics.dims.INFORMATION_SCHEMA.TABLES\`
   ORDER BY table_name"
```

### 4. Export Schema to File

Useful for programmatic processing of table schemas:

```bash
bq query --project_id=monzo-analytics --use_legacy_sql=false \
  --format=csv --quiet \
  "SELECT column_name FROM \`monzo-analytics.DATASET.INFORMATION_SCHEMA.COLUMNS\`
   WHERE table_name = 'TABLE_NAME' ORDER BY ordinal_position" \
  | tail -n +2 > /tmp/columns.txt
```

**Example:**
```bash
bq query --project_id=monzo-analytics --use_legacy_sql=false \
  --format=csv --quiet \
  "SELECT column_name FROM \`monzo-analytics.dims.INFORMATION_SCHEMA.COLUMNS\`
   WHERE table_name = 'vulnerable_customer_logs_dim' ORDER BY ordinal_position" \
  | tail -n +2 > /tmp/columns.txt
```

### 5. Check Table Metadata

Get table creation time, size, and other metadata:

```bash
bq query --project_id=monzo-analytics --use_legacy_sql=false \
  "SELECT
     table_name,
     creation_time,
     ROUND(size_bytes/1024/1024/1024, 2) as size_gb,
     row_count
   FROM \`monzo-analytics.DATASET_NAME.INFORMATION_SCHEMA.TABLES\`
   WHERE table_name = 'TABLE_NAME'"
```

### 6. Find Tables by Pattern

Search for tables matching a naming pattern:

```bash
bq query --project_id=monzo-analytics --use_legacy_sql=false \
  "SELECT table_name
   FROM \`monzo-analytics.DATASET_NAME.INFORMATION_SCHEMA.TABLES\`
   WHERE table_name LIKE '%PATTERN%'
   ORDER BY table_name"
```

**Example:**
```bash
# Find all customer-related tables
bq query --project_id=monzo-analytics --use_legacy_sql=false \
  "SELECT table_name FROM \`monzo-analytics.dims.INFORMATION_SCHEMA.TABLES\`
   WHERE table_name LIKE '%customer%' ORDER BY table_name"
```

### 7. Get Detailed Column Information

Get comprehensive column metadata including descriptions:

```bash
bq query --project_id=monzo-analytics --use_legacy_sql=false \
  "SELECT
     column_name,
     data_type,
     is_nullable,
     is_partitioning_column
   FROM \`monzo-analytics.DATASET.INFORMATION_SCHEMA.COLUMNS\`
   WHERE table_name = 'TABLE_NAME'
   ORDER BY ordinal_position"
```

### 8. Sample Data (Non-Sensitive Tables Only)

**⚠️ WARNING:** Only use this on non-sensitive tables. Never query actual content from people/staff/PII tables.

```bash
bq query --project_id=monzo-analytics --use_legacy_sql=false \
  "SELECT * FROM \`monzo-analytics.DATASET.TABLE_NAME\` LIMIT 10"
```

## Output Formatting Options

Control how results are displayed:

```bash
# CSV format
--format=csv

# JSON format
--format=json

# Pretty table format (default)
--format=prettyjson

# Quiet mode (no status messages)
--quiet

# Maximum rows to return
--max_rows=100
```

## Common Projects and Datasets

### Main Analytics Projects
- `monzo-analytics` - Main analytics warehouse
- `monzo-analytics-v2` - New OOM architecture models
- `monzo-analytics-pii` - PII-containing data (use with caution)
- `sanitized-events-prod` - Sanitised event data
- `raw-analytics-events-prod` - Raw event data

### Common Datasets
- `dims` - Dimension tables
- `prod` - Production tables
- `lending` - Lending-specific tables
- `slurpee` - Slurpee data

## Data Sensitivity Guidelines

### ✅ SAFE Operations (Always Allowed)

1. **INFORMATION_SCHEMA queries** - These only return metadata, not actual data
2. **COUNT(*) queries** - These only return row counts
3. **Schema inspection** - Column names, types, table structure

### ⚠️ RESTRICTED Operations (Use with Caution)

1. **Querying actual content** from:
   - People/staff data tables
   - PII-containing tables
   - Customer financial data
   - Authentication/security tables

2. **When in doubt:**
   - Stick to INFORMATION_SCHEMA queries
   - Use COUNT(*) to verify table exists
   - Ask the user before querying actual content

### 🚫 NEVER Do This

- Query actual rows from `people`, `staff`, `hibob` tables
- Export PII data to local files
- Query authentication credentials or tokens
- Access customer financial details without explicit permission

## Error Handling

### Common Errors and Solutions

**Error: "Not found: Table"**
```bash
# Solution: Check the table exists first
bq query --project_id=monzo-analytics --use_legacy_sql=false \
  "SELECT table_name FROM \`monzo-analytics.DATASET.INFORMATION_SCHEMA.TABLES\`
   WHERE table_name LIKE '%SEARCH_TERM%'"
```

**Error: "Access Denied"**
```bash
# Solution: You may not have permissions for that project/dataset
# Try a different project or ask the user about access
```

**Error: "Syntax error"**
```bash
# Solution: Ensure you're using Standard SQL (--use_legacy_sql=false)
# Check backtick usage around project.dataset.table identifiers
```

## Best Practices

1. **Always use fully-qualified table names** with backticks:
   ```sql
   `project-id.dataset.table`
   ```

2. **Use LIMIT for exploratory queries** to avoid large result sets:
   ```sql
   SELECT * FROM `project.dataset.table` LIMIT 10
   ```

3. **Check row counts before running expensive queries**:
   ```bash
   # First check size
   bq query --project_id=monzo-analytics --use_legacy_sql=false \
     "SELECT COUNT(*) FROM \`project.dataset.table\`"

   # Then run full query if reasonable
   ```

4. **Use dry-run for cost estimation** (for expensive queries):
   ```bash
   bq query --dry_run --use_legacy_sql=false "YOUR_QUERY_HERE"
   ```

5. **Export large results to file**:
   ```bash
   bq query --project_id=monzo-analytics --use_legacy_sql=false \
     --format=csv "YOUR_QUERY" > output.csv
   ```

## Quick Reference Commands

```bash
# Schema check
bq query --project_id=PROJECT --use_legacy_sql=false \
  "SELECT column_name, data_type FROM \`PROJECT.DATASET.INFORMATION_SCHEMA.COLUMNS\`
   WHERE table_name = 'TABLE' ORDER BY ordinal_position"

# Row count
bq query --project_id=PROJECT --use_legacy_sql=false \
  "SELECT COUNT(*) FROM \`PROJECT.DATASET.TABLE\`"

# List tables
bq query --project_id=PROJECT --use_legacy_sql=false \
  "SELECT table_name FROM \`PROJECT.DATASET.INFORMATION_SCHEMA.TABLES\`
   ORDER BY table_name"

# Table metadata
bq query --project_id=PROJECT --use_legacy_sql=false \
  "SELECT table_name, row_count, size_bytes
   FROM \`PROJECT.DATASET.INFORMATION_SCHEMA.TABLES\`
   WHERE table_name = 'TABLE'"
```

## When to Use This Skill

Invoke this skill when you need to:
- Query BigQuery tables or datasets
- Inspect table schemas or column types
- Count rows or check table existence
- Export table metadata
- Verify data before running dbt models
- Investigate data issues or table structures
- Find tables by naming patterns

## Integration with dbt Workflow

When working on dbt models in the analytics repository:

1. **Before creating import models** - Use BigQuery CLI to inspect source schemas
2. **Before running dbt** - Verify source tables exist and have expected structure
3. **Debugging dbt failures** - Query actual tables to understand data issues
4. **Validating generators** - Check that column types match between source and generator

Remember: Always respect data sensitivity guidelines and use INFORMATION_SCHEMA when possible.
