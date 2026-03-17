---
name: dst-query
description: Execute SQL queries on Danmarks Statistik data stored in DuckDB. Use when user needs specific data analysis, filtering, aggregation, or joins. Also includes table summary functionality.
---

# DST Query Skill

## Purpose

Execute SQL queries to analyze DST data stored in DuckDB. This is the core skill for data analysis - enabling filtering, aggregation, joins, and extracting insights from stored statistical data.

## DST Data Patterns

### Handling Suppressed Values
DST uses `".."` for suppressed/confidential data. Must handle before numeric operations.

**Filter approach:**
```sql
SELECT * FROM dst_table
WHERE INDHOLD != '..'  -- Filter out suppressed
```

**Safe casting approach:**
```sql
SELECT
  TID,
  CASE
    WHEN INDHOLD != '..' THEN CAST(INDHOLD AS INTEGER)
    ELSE NULL
  END as value
FROM dst_table
```

**Using helpers:**
```python
from scripts.db.helpers import safe_numeric_cast

query = f"SELECT TID, {safe_numeric_cast('INDHOLD')} as value FROM dst_table"
```

### Aggregate Codes
DST uses special codes for totals/aggregates:
- `"TOT"` - Total
- `"I alt"` - Total (Danish)
- `"Drivmidler i alt"` - All fuel types
- `"IALT"` - Total (alternative)

**Filter them out when analyzing details:**
```sql
SELECT * FROM dst_table
WHERE fuel_type NOT IN ('Drivmidler i alt', 'I alt')
  AND gender NOT IN ('TOT', 'IALT')
```

### Time Format Handling
DST time codes as strings don't sort chronologically:
- `"2024K1"` - Quarter 1, 2024
- `"2024M01"` - January 2024
- `"2024"` - Year 2024

**Extract for proper sorting:**
```sql
-- For quarters
SELECT
  TID,
  CAST(SUBSTRING(TID, 1, 4) AS INTEGER) as year,
  CAST(SUBSTRING(TID, 6, 1) AS INTEGER) as quarter
FROM dst_table
WHERE TID LIKE '%K%'
ORDER BY year, quarter
```

## When to Use

- User asks analytical questions about the data
- Need to filter or aggregate data
- Joining multiple DST tables
- Extracting specific insights or trends
- Computing custom statistics
- Exploring table structure and contents (use table summary)

## Table Summary

### Purpose
Get a quick overview of table structure and statistics before detailed querying.

### Usage
```bash
python scripts/db/table_summary.py --table-id <TABLE_ID>
```

### When to Use
- Before writing complex queries
- Understanding table structure
- Checking available columns
- Seeing sample data
- Getting quick statistics

### Output Includes
- Record count
- Column names and types
- Sample rows (first 5)
- Statistics for numeric columns (min, max, avg, median)
- Distinct value counts
- NULL counts
- Top values for categorical columns

## Running SQL Queries

### Basic Usage

Execute a SQL query:
```bash
python scripts/db/query_data.py --sql "<QUERY>"
```

### Output Formats

**Table format** (default - console-friendly):
```bash
--format table
```

**JSON format** (for programmatic use):
```bash
--format json
```

**CSV format** (for exports):
```bash
--format csv
```

### Save to File

Save query results:
```bash
--output <file>
```

### Safety Limit

Add automatic LIMIT:
```bash
--limit 100
```

## Table Naming Convention

All DST tables in DuckDB follow this pattern:
- Format: `dst_{table_id}` (lowercase)
- Example: FOLK1A → `dst_folk1a`
- Example: AUP01 → `dst_aup01`

**Important:** Always use lowercase in queries.

## Data Format in DuckDB

Tables stored from DST API use these conventions:
- **Separator**: Data was fetched as semicolon-separated CSV (`;`)
- **Encoding**: UTF-8 with BOM (handled automatically)
- **Column names**: Based on variable IDs from tableinfo
- **Value codes**: Exact codes from DST (e.g., "000", "101", "2024K1")
- **Data types**: DuckDB infers types (usually strings for codes, numeric for values)

## Common Query Patterns

### 1. Explore Data
```sql
SELECT * FROM dst_folk1a LIMIT 10
```

### 2. Count Records
```sql
SELECT COUNT(*) FROM dst_folk1a
```

### 3. Check Column Structure
```sql
-- See what columns exist
DESCRIBE dst_folk1a;

-- Or use table summary (recommended)
-- python scripts/db/table_summary.py --table-id FOLK1A
```

### 4. Aggregation
```sql
SELECT region, SUM(population) as total_pop
FROM dst_folk1a
GROUP BY region
ORDER BY total_pop DESC
```

### 5. Time Series Analysis
```sql
-- Note: Time codes from DST (e.g., "2024K1" for Q1 2024)
SELECT tid, value
FROM dst_folk1a
WHERE område = '000'  -- Whole country
ORDER BY tid
```

### 6. Filtering with DST Codes
```sql
-- Use exact codes from tableinfo
SELECT *
FROM dst_folk1a
WHERE tid LIKE '2024%'  -- All 2024 periods
  AND område IN ('000', '101')  -- Denmark and Copenhagen
  AND køn IN ('1', '2')  -- Men and women (not 'TOT')
```

### 7. Multiple Aggregations
```sql
SELECT
  område,
  COUNT(*) as record_count,
  AVG(CAST(indhold AS DOUBLE)) as avg_value,
  MAX(CAST(indhold AS DOUBLE)) as max_value
FROM dst_folk1a
GROUP BY område
```

### 8. Join Tables
```sql
SELECT
  a.område,
  a.indhold as population,
  b.indhold as employment
FROM dst_folk1a a
JOIN dst_aup01 b ON a.område = b.område AND a.tid = b.tid
WHERE a.tid = '2024K1'
```

### 9. Percentages
```sql
SELECT
  område,
  CAST(indhold AS DOUBLE) as value,
  100.0 * CAST(indhold AS DOUBLE) / SUM(CAST(indhold AS DOUBLE)) OVER () as percentage
FROM dst_folk1a
WHERE tid = '2024K1' AND køn = 'TOT'
```

### 10. Latest Period Analysis
```sql
-- Find most recent quarter
WITH latest AS (
  SELECT MAX(tid) as max_tid FROM dst_folk1a
)
SELECT område, SUM(CAST(indhold AS DOUBLE)) as total
FROM dst_folk1a
WHERE tid = (SELECT max_tid FROM latest)
GROUP BY område
ORDER BY total DESC
```

## Best Practices

### Query Development
1. **Start with table summary** to understand structure
2. **Use LIMIT** for exploratory queries
3. **Build incrementally** - test small queries first
4. **Check record counts** before expensive operations

### Performance
- Use WHERE clauses to filter early
- Add indexes if querying repeatedly (advanced)
- Aggregate before joining when possible
- Be mindful of large result sets

### Safety
- Queries are **READ-ONLY** (SELECT only)
- Cannot modify data (no INSERT/UPDATE/DELETE)
- Cannot alter schema (no DROP/CREATE/ALTER)
- Script validates queries before execution

### Data Quality
- Handle NULL values explicitly
- Use COALESCE for NULL handling
- Verify data types before operations
- Check for duplicates if unexpected

### Understanding Data Freshness
Before analyzing, check when data was last updated:
```sql
SELECT table_id, last_updated, row_count
FROM dst_metadata
WHERE table_id = 'FOLK1A'
```

Recommendations:
- Check freshness before major analysis
- Re-fetch if data is stale (use dst-check-freshness skill)
- Note DST update frequency varies by table
- Some tables update quarterly, others monthly or annually

## Examples

### Example 1: Get table summary
```bash
python scripts/db/table_summary.py --table-id FOLK1A
```

### Example 2: Simple exploration
```bash
python scripts/db/query_data.py --sql "SELECT * FROM dst_folk1a LIMIT 5"
```

### Example 3: Aggregation by year
```bash
python scripts/db/query_data.py --sql "SELECT year, SUM(population) as total FROM dst_folk1a GROUP BY year ORDER BY year"
```

### Example 4: Regional analysis
```bash
python scripts/db/query_data.py --sql "SELECT region, AVG(value) as avg_val FROM dst_folk1a WHERE year >= 2020 GROUP BY region"
```

### Example 5: Export to CSV
```bash
python scripts/db/query_data.py --sql "SELECT * FROM dst_folk1a" --format csv --output results.csv
```

### Example 6: JSON output
```bash
python scripts/db/query_data.py --sql "SELECT * FROM dst_folk1a LIMIT 100" --format json --output data.json
```

### Example 7: With safety limit
```bash
python scripts/db/query_data.py --sql "SELECT * FROM dst_folk1a" --limit 1000
```

## Advanced Queries

### Window Functions
```sql
SELECT
  year,
  value,
  LAG(value) OVER (ORDER BY year) as prev_year_value,
  value - LAG(value) OVER (ORDER BY year) as change
FROM dst_folk1a
WHERE region = '000'
ORDER BY year
```

### Pivoting Data
```sql
SELECT
  region,
  MAX(CASE WHEN year = 2023 THEN value END) as val_2023,
  MAX(CASE WHEN year = 2024 THEN value END) as val_2024
FROM dst_folk1a
GROUP BY region
```

### Percentiles
```sql
SELECT
  PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY value) as p25,
  PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY value) as median,
  PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY value) as p75
FROM dst_folk1a
```

### Complex Filtering
```sql
SELECT *
FROM dst_folk1a
WHERE year BETWEEN 2020 AND 2024
  AND region IN (SELECT DISTINCT region FROM dst_aup01 WHERE employment > 1000)
  AND value IS NOT NULL
ORDER BY value DESC
LIMIT 100
```

## Tips

### Before Querying
- **Run table summary first** to see structure
- Check column names and types (often Danish: område, tid, køn, etc.)
- Review sample data to understand value formats
- Verify table has data and check last_updated in dst_metadata
- Note: Column names are lowercase variable IDs from DST

### Working with DST Data Codes
- **Time codes**: `"2024K1"` (quarterly), `"2024M01"` (monthly), `"2024"` (annual)
- **Geographic codes**: `"000"` (whole country), `"101"` (Copenhagen), etc.
- **Aggregate codes**: `"TOT"`, `"IALT"` often represent totals
- **Use LIKE**: For pattern matching time periods: `tid LIKE '2024%'`
- **Cast when needed**: Value columns may be strings: `CAST(indhold AS DOUBLE)`

### Query Writing
- Use table aliases for clarity (a, b, etc.)
- Format SQL for readability
- Comment complex queries
- Test with LIMIT first
- Handle Danish characters properly (æ, ø, å)

### Analysis Workflow
1. **Understand:** Get table summary
2. **Check freshness:** Query dst_metadata for last_updated
3. **Explore:** Simple SELECT with LIMIT
4. **Filter:** Add WHERE clauses with exact DST codes
5. **Aggregate:** Use GROUP BY (cast numeric columns first)
6. **Refine:** Add ORDER BY, calculations
7. **Export:** Save final results

### Performance Tips
- Filter first, aggregate second
- Use specific columns, not SELECT *
- Add LIMIT for large tables
- Use indexes on commonly filtered columns (advanced)
- Consider creating views for repeated queries (advanced)
- Cache results locally if running same query multiple times

## Troubleshooting

### "Table not found"
- Verify table exists: `python scripts/db/list_tables.py` (dst-list-tables skill)
- Check table name is lowercase
- Ensure format: dst_{table_id}
- Example: FOLK1A becomes `dst_folk1a`

### "Column not found"
- Run table summary to see actual column names
- Column names are lowercase DST variable IDs
- Common columns: `område` (region), `tid` (time), `køn` (gender), `indhold` (value)
- Check spelling including Danish characters (æ, ø, å)
- Verify column exists in that specific table

### Data Type Issues
- Value columns often stored as strings (e.g., `indhold`)
- Cast to numeric for calculations: `CAST(indhold AS DOUBLE)`
- Time codes are strings: use LIKE for patterns
- Don't assume numeric types without checking

### Unexpected Results
- **Empty results**: Check if data was actually fetched for that table
- **Wrong aggregations**: Verify you're filtering out 'TOT' codes if needed
- **Time ordering issues**: Time codes as strings may not sort chronologically
  - Solution: Extract year/quarter or use CASE statements
- **Duplicate rows**: Table may have multiple dimensions - check GROUP BY

### Large Result Sets
- Add LIMIT clause for exploration
- Use aggregation to reduce rows
- Export to file instead of console: `--output results.csv`
- Check row count first: `SELECT COUNT(*) FROM table`

### Slow Queries
- Check WHERE filters are effective
- Filter by indexed columns (primary keys)
- Simplify joins
- Reduce columns selected
- Check data size with COUNT first
- Avoid SELECT * on large tables

### Query Syntax Errors
- Verify SQL syntax (DuckDB follows PostgreSQL conventions)
- Check quotes: use single quotes for string literals
- Danish characters: ensure UTF-8 encoding
- Test simple version first
- Review error message carefully

### Character Encoding Issues
- DuckDB handles UTF-8 automatically
- If seeing odd characters, verify terminal encoding
- CSV exports preserve Danish characters (æ, ø, å)

## Common Workflows

### Workflow 1: Explore New Table
```bash
# 1. Get summary
python scripts/db/table_summary.py --table-id FOLK1A

# 2. See sample data
python scripts/db/query_data.py --sql "SELECT * FROM dst_folk1a LIMIT 5"

# 3. Check record count
python scripts/db/query_data.py --sql "SELECT COUNT(*) FROM dst_folk1a"

# 4. Explore key dimensions
python scripts/db/query_data.py --sql "SELECT DISTINCT region FROM dst_folk1a"
```

### Workflow 2: Trend Analysis
```bash
# 1. Get summary statistics
python scripts/db/table_summary.py --table-id FOLK1A

# 2. Query time series
python scripts/db/query_data.py --sql "SELECT year, SUM(value) as total FROM dst_folk1a GROUP BY year ORDER BY year"

# 3. Calculate growth
python scripts/db/query_data.py --sql "SELECT year, value, value - LAG(value) OVER (ORDER BY year) as growth FROM dst_folk1a WHERE region = '000'"

# 4. Export results
python scripts/db/query_data.py --sql "..." --format csv --output analysis.csv
```

### Workflow 3: Compare Regions
```bash
# 1. Get regional breakdown
python scripts/db/query_data.py --sql "SELECT region, COUNT(*) as records, AVG(value) as avg_value FROM dst_folk1a GROUP BY region ORDER BY avg_value DESC"

# 2. Top regions
python scripts/db/query_data.py --sql "SELECT region, SUM(value) as total FROM dst_folk1a WHERE year = 2024 GROUP BY region ORDER BY total DESC LIMIT 10"

# 3. Compare specific regions
python scripts/db/query_data.py --sql "SELECT year, region, value FROM dst_folk1a WHERE region IN ('000', '101', '147') ORDER BY year, region"
```

## SQL Reference

### Useful DuckDB Functions

**Aggregation:**
- COUNT, SUM, AVG, MIN, MAX
- MEDIAN, STDDEV, VARIANCE
- STRING_AGG (concatenate strings)

**String Functions:**
- UPPER, LOWER, TRIM
- SUBSTRING, CONCAT
- LIKE, ILIKE (case-insensitive)

**Date Functions:**
- CURRENT_DATE, CURRENT_TIMESTAMP
- DATE_DIFF, DATE_ADD
- EXTRACT (year, month, day)

**Window Functions:**
- ROW_NUMBER, RANK, DENSE_RANK
- LAG, LEAD
- FIRST_VALUE, LAST_VALUE

**Conditional:**
- CASE WHEN ... THEN ... END
- COALESCE (handle NULLs)
- NULLIF

## Best Practices Summary

1. **Always start with table summary**
2. **Use LIMIT during development**
3. **Build queries incrementally**
4. **Handle NULLs explicitly**
5. **Use clear aliases and formatting**
6. **Test before running on full dataset**
7. **Export results for further analysis**
8. **Document complex queries**
