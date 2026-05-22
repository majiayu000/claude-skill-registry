---
name: dst-tableinfo
description: Get detailed metadata for a specific Danmarks Statistik table including variables, dimensions, and structure. Use before fetching data to understand table schema.
---

# DST Table Info Skill

## Purpose

Get complete metadata and structure for a DST table. This is an essential step before fetching data - it tells you what dimensions are available, what filters you can apply, and what to expect in the data.

## When to Use

- Before fetching data to understand table structure
- To see available variables and dimensions
- To determine appropriate filters for data fetch
- To understand table updates and units of measurement
- User asks "what's in this table?"
- After finding a table ID with dst-tables skill

## How to Use

### Basic Usage (JSON output)

Get table metadata:
```bash
python scripts/api/get_tableinfo.py --table-id <TABLE_ID>
```

### Verbose Format (Human-readable)

Get formatted, easy-to-read output:
```bash
python scripts/api/get_tableinfo.py --table-id <TABLE_ID> --verbose
```

### Save to File

Save metadata for reference:
```bash
python scripts/api/get_tableinfo.py --table-id <TABLE_ID> --output info.json
```

## Expected Output

The script returns complete table metadata including:

### Basic Information
- **id**: Table identifier
- **text**: Table name
- **description**: Detailed description
- **unit**: Unit of measurement
- **updated**: Last update timestamp

### Variables/Dimensions
- **id**: Variable identifier (e.g., "OMRÅDE", "TID")
- **text**: Variable description
- **values**: All available values for that variable
- **time**: Whether it's a time dimension

Example output structure:
```json
{
  "id": "FOLK1A",
  "text": "Population at the first day of the quarter",
  "description": "Population by region, age, and sex",
  "unit": "number",
  "updated": "2025-10-15T10:30:00",
  "variables": [
    {
      "id": "OMRÅDE",
      "text": "Region",
      "values": [
        {"id": "000", "text": "Whole country"},
        {"id": "101", "text": "Copenhagen"}
      ]
    },
    {
      "id": "TID",
      "text": "Time",
      "time": true,
      "values": [
        {"id": "2020Q1", "text": "2020Q1"},
        {"id": "2020Q2", "text": "2020Q2"}
      ]
    }
  ]
}
```

## Key Information to Extract

When analyzing table info, pay attention to:

1. **Table Description**: What data does it contain?
2. **Unit**: What do the numbers represent? (persons, kroner, percentage, etc.)
3. **Variables**: What dimensions can you filter by?
4. **Available Values**: What options exist for each variable?
5. **Time Coverage**: What time periods are available?
6. **Last Updated**: How fresh is the data?
7. **Elimination Flag**: Whether variables can be aggregated (see below)

### Understanding Variable Properties

Each variable has important metadata:

**elimination** flag:
- `true`: Variable can theoretically be aggregated/eliminated
- `false`: Variable must be explicitly specified
- **Note**: BULK format requires ALL variables regardless of this flag

**time** flag:
- `true`: This is the time dimension
- Time values have special formats: `2024` (annual), `2024K1` (quarterly), `2024M01` (monthly), `2024U01` (weekly)
- Time variables typically have `elimination: false`

**map** property:
- Present if variable has geographic mapping
- Example: `"map": "Denmark_municipality_07"`
- Indicates visualization possibilities

### Variable Value Codes

Important patterns in value IDs:
- **Aggregate codes**: `"TOT"`, `"IALT"`, `"000"` (whole country) - represent totals
- **Time codes**: `"2024K1"` = 2024 Quarter 1 (K=Kvartal), `"2024M01"` = 2024 January
- **Geographic codes**: `"000"` = Whole Denmark, `"101"` = Copenhagen, etc.
- Use exact codes from tableinfo in data requests

## Next Steps

After understanding the table structure:

1. **Decide on filters** (optional): Based on variables and values
2. **Fetch the data** using dst-data skill:
   ```bash
   python scripts/fetch_and_store.py --table-id <TABLE_ID>
   ```
3. **With filters** (if needed):
   ```bash
   python scripts/fetch_and_store.py --table-id <TABLE_ID> --filters '{"OMRÅDE":["000"]}'
   ```

## Examples

### Example 1: Get table info for FOLK1A
```bash
python scripts/api/get_tableinfo.py --table-id FOLK1A
```

### Example 2: Verbose, readable output
```bash
python scripts/api/get_tableinfo.py --table-id FOLK1A --verbose
```

### Example 3: Save to file
```bash
python scripts/api/get_tableinfo.py --table-id FOLK1A --output folk1a_structure.json
```

### Example 4: Check multiple tables
```bash
# Get info for population table
python scripts/api/get_tableinfo.py --table-id FOLK1A --verbose

# Get info for employment table
python scripts/api/get_tableinfo.py --table-id AUP01 --verbose
```

## Tips

### Before Fetching Data
- **Always check tableinfo first**: Large tables can take time to download
- **Calculate expected cells**: Multiply value counts to estimate size
- **Note available filters**: Limit data size by filtering dimensions
- **Check date range**: Understand temporal coverage (first/last periods)
- **Identify ALL variable IDs**: BULK format requires all specified

### Reading Metadata
- **Understand variables**: Know what you can group/filter by
- **Check elimination flags**: But remember BULK needs all variables anyway
- **Note time formats**: Quarterly (K), Monthly (M), Weekly (U), Annual
- **Find aggregate codes**: TOT, IALT, 000 are usually totals
- **Use verbose mode**: Easier to read when exploring interactively
- **Save JSON**: Keep machine-readable format for programmatic use

### Performance Considerations
- **Caching**: Tableinfo responses are cacheable (data structure rarely changes)
- **Case-insensitive**: Table IDs work in any case ("FOLK1A" = "folk1a")
- **Response time**: Typically 200-400ms
- **Call once**: Metadata doesn't change frequently, cache locally if needed

## Common Variables (Reference)

Typical DST variable names:
- **OMRÅDE**: Geographic region
- **TID**: Time period
- **ALDER**: Age
- **KØN**: Sex/Gender
- **BRANCHE**: Industry
- **UDDANNELSE**: Education level
- **INDKOMST**: Income bracket

Note: Variable names are usually in Danish.

## Understanding Values

Each variable has a set of possible values:
- **Hierarchical**: Some variables have parent-child relationships
- **Time values**: Format varies by table:
  - Annual: `"2024"`
  - Quarterly: `"2024K1"` (K=Kvartal/Quarter)
  - Monthly: `"2024M01"`
  - Weekly: `"2024U01"` (U=Uge/Week)
- **Region codes**: Numeric codes like `"000"` (whole country), `"101"` (Copenhagen)
- **Categories**: Text or numeric codes for classifications
- **Aggregate values**: `"TOT"`, `"IALT"`, `"000"` typically represent totals

### Analyzing Metadata for Data Requests

**Step 1: Count total cells**
```
cells = var1_values × var2_values × ... × varN_values
```
If cells > 1,000,000: Must use BULK format

**Step 2: Identify required variables**
- BULK format: ALL variables must be specified
- Check variable IDs from `"variables"` array
- Note which are time dimensions (`"time": true`)

**Step 3: Select appropriate values**
- Use `"*"` for all values
- Use specific IDs for filtering
- Use patterns for partial selection: `"2024*"`, `"*K1"`, etc.
- Use nth-rules for time: `"(1)"` = latest, `"(-n+5)"` = last 5

## Troubleshooting

### "EXTRACT-NOTFOUND: Table not found"
Error message: "Tabellen blev ikke fundet"
- Verify table ID is correct (though case-insensitive)
- Check table exists using dst-tables skill first
- Try with different case if needed
- Verify table is active (not discontinued)

### Empty or Limited Values
- Some tables may have limited options for certain variables
- Check if table is being updated (look at `"updated"` field)
- Inactive tables may have outdated metadata

### Large Output
- Use `--verbose` for human-readable summary
- Use `--output` to save full JSON for later analysis
- Large tables have many variables/values - normal behavior

### Network Errors
- Check internet connection
- DST API may be temporarily unavailable
- Typical response time: 200-400ms
- Retry after a few seconds if timeout occurs

### Understanding Complex Structures
- Variables with many values (100+) are common
- Time variables often have 50+ periods
- Geographic variables can have 100+ regions
- This is expected - use filters when fetching data
