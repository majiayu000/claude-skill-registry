---
name: dst-list-tables
description: List all Danmarks Statistik tables currently stored in DuckDB with metadata. Use when user wants to know what data is available locally or explore stored tables.
---

# DST List Tables Skill

## Purpose

Discover what DST data is currently stored in the local DuckDB database. This is typically the first step in any analysis workflow - finding out what data you have to work with.

## When to Use

- User asks "what data do we have?"
- Starting an analysis session
- Checking if specific data exists locally
- Exploring available tables
- Before deciding what to analyze
- Verifying data was stored successfully after fetch

## How to Use

### List All Tables

Show all tables stored locally:
```bash
python scripts/db/query_metadata.py --list-all
```

### Get Specific Table Metadata

Get detailed metadata for one table:
```bash
python scripts/db/query_metadata.py --table-id <TABLE_ID>
```

### JSON Output

Get machine-readable output:
```bash
python scripts/db/query_metadata.py --list-all --format json
```

## Expected Output

### List All Tables Format

Console-friendly table view:
```
================================================================================
DST TABLES IN LOCAL DATABASE
================================================================================

Found 3 table(s):

ID              Name                                Records    Age
--------------------------------------------------------------------------------
FOLK1A          Population at first day             45231      5 days ago
AUP01           Employment statistics               12450      2 weeks ago
NABB3           Business statistics                 8900       1 month ago
================================================================================
```

### Metadata Fields

For each table, you'll see:
- **table_id**: Unique identifier (use in queries as `dst_{id}`)
- **table_name**: Human-readable description
- **record_count**: Number of rows in the table
- **last_updated**: When DST last updated the source data
- **fetch_timestamp**: When we downloaded it
- **age**: How old our local copy is (human-readable)

### Example Metadata Output

```
======================================================================
METADATA FOR TABLE: FOLK1A
======================================================================
Table ID:        FOLK1A
Table Name:      Population at the first day of the quarter
Record Count:    45231
Last Updated:    2025-10-15T10:30:00
Fetch Timestamp: 2025-10-25T09:15:00
Data Age:        5 days ago
======================================================================
```

## Interpreting Results

### Table ID
- Use this for all queries
- Format in DuckDB: `dst_{table_id}` (lowercase)
- Example: FOLK1A → query as `dst_folk1a`

### Record Count
- Indicates dataset size
- Larger counts mean more data to analyze
- Compare with expected size to verify completeness

### Fetch Timestamp
- When data was downloaded from DST
- Indicates freshness of local copy
- Compare with last_updated to see if source changed

### Age
- Human-readable freshness indicator
- "5 days ago" means data is 5 days old locally
- Consider refreshing if too old for your needs

## Next Steps

### If Data Exists
Use query and analysis skills:
```bash
# Get table summary
python scripts/db/table_summary.py --table-id <TABLE_ID>

# Run SQL query
python scripts/db/query_data.py --sql "SELECT * FROM dst_<table_id> LIMIT 10"
```

### If Data Missing
Switch to Fetcher Agent to download:
```bash
python scripts/fetch_and_store.py --table-id <TABLE_ID>
```

### If Data Stale
Use **dst-check-freshness** skill to determine if refresh needed:
```bash
python scripts/db/query_metadata.py --table-id <TABLE_ID> --check-freshness --max-age-days 30
```

## Examples

### Example 1: List all stored tables
```bash
python scripts/db/query_metadata.py --list-all
```

### Example 2: Get specific table metadata
```bash
python scripts/db/query_metadata.py --table-id FOLK1A
```

### Example 3: JSON output for programmatic use
```bash
python scripts/db/query_metadata.py --list-all --format json
```

### Example 4: Check multiple tables
```bash
# List all
python scripts/db/query_metadata.py --list-all

# Get details for each interesting table
python scripts/db/query_metadata.py --table-id FOLK1A
python scripts/db/query_metadata.py --table-id AUP01
```

## Tips

### At Session Start
- **Always run --list-all first** to see what you have to work with
- Note table IDs for tables you want to analyze
- Check ages to identify stale data

### Data Quality
- Verify record counts seem reasonable
- Check fetch timestamps for freshness
- Compare last_updated vs fetch_timestamp

### Table Naming
- Remember: table IDs become `dst_{id}` in lowercase
- FOLK1A → dst_folk1a
- AUP01 → dst_aup01

### Empty Database
If no tables shown:
1. Verify database file exists
2. Use Fetcher Agent to download data
3. Check fetch operations completed successfully

## Common Workflows

### Workflow 1: Start Analysis
```bash
# 1. See what's available
python scripts/db/query_metadata.py --list-all

# 2. Get details on interesting table
python scripts/db/query_metadata.py --table-id FOLK1A

# 3. Check data age
python scripts/db/query_metadata.py --table-id FOLK1A --check-freshness

# 4. Proceed with analysis
python scripts/db/table_summary.py --table-id FOLK1A
```

### Workflow 2: Verify After Fetch
```bash
# 1. Fetch data
python scripts/fetch_and_store.py --table-id FOLK1A

# 2. Verify it's there
python scripts/db/query_metadata.py --table-id FOLK1A

# 3. Check record count is reasonable
```

## Troubleshooting

### "No tables found"
- Database may be empty
- Verify database file exists at path in .env
- Use Fetcher Agent to download data

### "Table not found"
- Check spelling of table ID (case-sensitive)
- Run --list-all to see what exists
- Table may not have been fetched yet

### Unexpected Record Counts
- May indicate partial fetch
- Check fetch logs for errors
- Consider re-fetching with --overwrite

### Old Fetch Timestamps
- Data may be stale
- Use dst-check-freshness to evaluate
- Consider refreshing with Fetcher Agent
