---
name: dst-data
description: Fetch actual data from Danmarks Statistik API and store in DuckDB. Use when user wants to download and store specific DST table data for analysis.
---

# DST Data Skill

## Purpose

Fetch statistical data from Danmarks Statistik API and persist it in the local DuckDB database for analysis. This is the final step in the data acquisition workflow, transforming remote API data into queryable local tables.

## Critical API Quirks

### BULK Format Requirements
DST's BULK format (unlimited streaming) has a critical requirement:

**ALL variables must be specified in filters** - no auto-elimination like other formats.

**Error:** "Der skal vælges værdier for variabel: [VAR_NAME]"

**Solution:**
1. Get all variables from tableinfo
2. Specify each in filters: `{"VAR1":["*"], "VAR2":["*"], ...}`
3. Use wildcard `"*"` to get all values for a variable

### Suppressed Values ("..")
DST uses `".."` to indicate suppressed/confidential data.

**Impact:**
- Causes errors when casting to numeric: `CAST('..' AS INTEGER)` fails
- Common in small population cells, rare events
- Must be filtered before numeric operations

**Solutions:**
- Filter in SQL: `WHERE column != '..'`
- Safe casting: `CASE WHEN column != '..' THEN CAST(column AS INTEGER) END`
- Use helpers: `safe_numeric_cast(column)` from scripts/db/helpers.py

### Cell Limits
- **CSV/JSON formats:** 1,000,000 cell maximum
- **BULK format:** Unlimited (streaming)
- **Calculation:** cells = var1_count × var2_count × ... × varN_count

**Error:** "Forespørgslen returnerer for mange observationer" (REQUEST-LIMIT)

**Solution:** Use BULK format automatically (done by fetch_and_store.py)

## Common Error Codes

### EXTRACT-NOTALLOWED
**Message:** "Der skal vælges værdier for variabel: X"
**Cause:** BULK format missing variable in filters
**Fix:** Add variable to filters with at least one value

### EXTRACT-NOTFOUND
**Messages:**
- "Tabellen blev ikke fundet" (table not found)
- "Variablen blev ikke fundet" (variable not found)
- "Værdien blev ikke fundet" (value not found)

**Fix:** Verify IDs against tableinfo output

### REQUEST-LIMIT
**Message:** "Forespørgslen returnerer for mange observationer"
**Cause:** Request exceeds 1M cells (non-BULK formats)
**Fix:** Use BULK format or add more filters

## When to Use

- User requests specific table data to be downloaded
- Ready to download data after reviewing table structure (tableinfo)
- Need to refresh existing data with latest from DST
- Want to store data for offline analysis
- Building a local data repository from DST

## How to Use - Recommended (Combined Workflow)

The `fetch_and_store.py` script combines fetching and storing in one command. This is the **recommended approach**.

### Basic Usage

Fetch and store a complete table:
```bash
python scripts/fetch_and_store.py --table-id <TABLE_ID>
```

### With Filters

Fetch only specific data using filters:
```bash
python scripts/fetch_and_store.py --table-id <TABLE_ID> --filters '<JSON>'
```

Example filters:
```bash
# Filter by region
--filters '{"OMRÅDE":["000"]}'

# Filter by time period
--filters '{"TID":["2024*"]}'

# Multiple filters
--filters '{"OMRÅDE":["000","101"],"TID":["2024*"]}'
```

### Overwrite Existing Data

Replace existing table:
```bash
python scripts/fetch_and_store.py --table-id <TABLE_ID> --overwrite
```

### Skip if Fresh

Only fetch if data is older than threshold:
```bash
python scripts/fetch_and_store.py --table-id <TABLE_ID> --skip-if-fresh --max-age-days 30
```

## How to Use - Advanced (Separate Steps)

For advanced users who need more control, fetch and store can be done separately.

### Step 1: Fetch Data

Download data from API:
```bash
python scripts/api/fetch_data.py --table-id <TABLE_ID> --output data.json
```

### Step 2: Store Data

Save to DuckDB:
```bash
python scripts/db/store_data.py --table-id <TABLE_ID> --data-file data.json
```

## Expected Output

### Data Storage
- Data stored in table named `dst_{table_id}` (lowercase)
- Example: Table FOLK1A → `dst_folk1a`
- Metadata updated in `dst_metadata` table

### Success Message
```
✓ Created table dst_folk1a with 45231 records
```

### If Skipped (Fresh Data)
```
⊘ Skipped FOLK1A: data_is_fresh
```

Exit codes:
- 0: Success
- 1: Error
- 2: Skipped (when using --skip-if-fresh)

## Important Considerations

### Data Format
- **Default format: BULK** - Streaming CSV with no cell limit
- Semicolon-separated (`;`) not comma
- UTF-8 encoding with BOM
- Alternative formats: CSV, JSONSTAT, XLSX (1M cell limit)
- **BULK requires ALL variables specified** - no auto-elimination

### Cell Limits & Size
- **Non-streaming formats**: 1,000,000 cell limit (CSV, JSONSTAT, XLSX)
- **BULK format**: Unlimited cells (streaming)
- Large tables may take significant time to download
- Check table info first to estimate size: cells = var1_count × var2_count × ... × varN_count
- Use filters to limit data volume when possible
- Error if exceeded: "Forespørgslen returnerer for mange observationer" (REQUEST-LIMIT)

### Existing Data
- Default behavior: Fail if table already exists
- Use `--overwrite` to replace existing data
- Overwrites completely - no partial updates

### Network and Time
- Requires stable internet connection
- Large downloads may timeout - retry if needed
- Recommended: 4-5 requests/second maximum (self-imposed limit)
- Timeout recommendations: 30s (small), 60s (medium), 120s+ (large)

### Filters Format
- Filters must be valid JSON
- Keys are variable IDs from table info
- Values are arrays of allowed values
- Wildcard patterns: `*` (all), `prefix*`, `*suffix`, `>=value`, `<=value`
- Time patterns: `(1)` (latest), `(-n+5)` (last 5), `2024*` (year match)
- **BULK format validation**: Must specify all variables, check with tableinfo first

## Verification Steps

After storing data, verify success:

### 1. Check Metadata
```bash
python scripts/db/query_metadata.py --table-id <TABLE_ID>
```

### 2. Spot Check Data
```bash
python scripts/db/query_data.py --sql "SELECT * FROM dst_<table_id> LIMIT 5"
```

### 3. Verify Record Count
Compare record count in metadata with table info expectations.

## Next Steps

After successfully storing data:

1. **Data is ready for analysis**
2. **Switch to DST Analyst Agent** for querying and analysis
3. **Run SQL queries** using dst-query skill
4. **Create summaries** using table_summary script

Example:
```bash
python scripts/db/table_summary.py --table-id FOLK1A
```

## Examples

### Example 1: Simple fetch and store
```bash
python scripts/fetch_and_store.py --table-id FOLK1A
```

### Example 2: Overwrite existing data
```bash
python scripts/fetch_and_store.py --table-id FOLK1A --overwrite
```

### Example 3: Fetch with regional filter
```bash
python scripts/fetch_and_store.py --table-id FOLK1A --filters '{"OMRÅDE":["000","101"]}'
```

### Example 4: Skip if recently fetched
```bash
python scripts/fetch_and_store.py --table-id FOLK1A --skip-if-fresh --max-age-days 7
```

### Example 5: Advanced - separate steps
```bash
# Step 1: Fetch
python scripts/api/fetch_data.py --table-id FOLK1A --output folk1a.json

# Step 2: Store
python scripts/db/store_data.py --table-id FOLK1A --data-file folk1a.json
```

### Example 6: Export to CSV
```bash
python scripts/api/fetch_data.py --table-id FOLK1A --format csv --output data.csv
```

## Tips

### Before Large Downloads
1. **Check table info** to understand data size
2. **Use filters** to limit to needed data
3. **Test with small filter** first

### For Regular Updates
1. **Use --skip-if-fresh** to avoid unnecessary downloads
2. **Set appropriate max-age-days** based on update frequency
3. **Use --overwrite** when refresh is needed

### Performance
- Filter at API level (not after download)
- Monitor disk space for large datasets
- Consider time of day (API load varies)

### Data Quality
- Always verify after storage
- Check record counts match expectations
- Spot check data values for sanity

## Common Filter Patterns

### Time Filters
```bash
# Latest period (recommended for current data)
--filters '{"Tid":["(1)"]}'

# Last 5 periods
--filters '{"Tid":["(-n+5)"]}'

# Specific year
--filters '{"Tid":["2024"]}'

# Year range (wildcard)
--filters '{"Tid":["202*"]}'

# Specific quarters (K=Kvartal)
--filters '{"Tid":["2024K1","2024K2"]}'

# All Q1 quarters
--filters '{"Tid":["*K1"]}'

# Range operator
--filters '{"Tid":[">=2023K1<=2024K4"]}'
```

### Geographic Filters
```bash
# Whole country
--filters '{"OMRÅDE":["000"]}'

# Specific regions
--filters '{"OMRÅDE":["101","147"]}'

# All regions (wildcard)
--filters '{"OMRÅDE":["*"]}'

# Region codes: 000=Denmark, 101=Copenhagen, 147=Frederiksberg
```

### Combined Filters
```bash
# Multiple dimensions with patterns
--filters '{"OMRÅDE":["000"],"Tid":["(1)"],"KØN":["*"]}'

# Complex filtering
--filters '{"OMRÅDE":["101","147"],"Tid":[">=2020"],"KØN":["1","2"]}'
```

### Pattern Reference
- `*` - All values
- `prefix*` - Starts with prefix
- `*suffix` - Ends with suffix
- `(1)` - Latest period (nth-rule)
- `(-n+N)` - Last N periods
- `>=value` - From value onwards
- `<=value` - Up to value
- `>=A<=B` - Between A and B

## Troubleshooting

### "Table already exists"
- Use `--overwrite` flag to replace existing data
- Or query existing data first to check if refresh needed

### "Network timeout"
- Large table - try with filters to reduce size
- Increase timeout in script if needed (120s+ for large datasets)
- Retry the operation
- Check internet connection

### "REQUEST-LIMIT: Too many cells"
Error message: "Forespørgslen returnerer for mange observationer"
- **Solution**: Script should use BULK format automatically for large requests
- Verify format=BULK is being used
- Add more filters to reduce cell count
- Cell limit: 1,000,000 for non-streaming formats

### "EXTRACT-NOTALLOWED: Missing variable"
Error message: "Der skal vælges værdier for variabel: [VARIABLE_NAME]"
- **BULK format requires ALL variables specified**
- Check tableinfo to get all variable IDs
- Ensure every variable has a value selection
- Cannot rely on auto-elimination with BULK

### "EXTRACT-NOTFOUND: Invalid code"
Error messages: "Tabellen blev ikke fundet" / "Variablen blev ikke fundet" / "Værdien blev ikke fundet"
- Verify table ID is correct (case-insensitive)
- Check variable IDs match tableinfo exactly
- Verify value codes exist in tableinfo
- Run tableinfo first to validate codes

### "Invalid filters"
- Verify JSON syntax is correct (use single quotes around JSON, double quotes inside)
- Check variable IDs match table info exactly
- Ensure values exist in table info
- Test patterns: wildcards need asterisk `*`, ranges need `>=`/`<=`

### "No data returned"
- Filters may be too restrictive
- Verify table has data for requested filters
- Check table info for available values
- Try with fewer/broader filters first

### "Cannot sort time for streaming formats"
Error message: "Der kan ikke vælges sortering af tid for streamede formater"
- **BULK format does not support time sorting**
- Sort after data is stored in DuckDB
- Or use CSV format instead (if under 1M cells)

### Disk Space Issues
- Monitor available space before large downloads
- Clean up old/unused tables
- Use filters to limit data volume
- Check estimated size: run tableinfo and calculate cells
