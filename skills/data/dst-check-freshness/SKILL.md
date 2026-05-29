---
name: dst-check-freshness
description: Check data freshness and age for DST tables in DuckDB. Use when determining if data needs refreshing or validating data currency before analysis.
---

# DST Check Freshness Skill

## Purpose

Verify data freshness and determine if a refresh is needed. This is essential for ensuring your analysis uses current data and making informed decisions about when to re-fetch from DST.

## When to Use

- Before starting analysis (ensure data is current)
- User asks about data age or currency
- Deciding whether to re-fetch data from DST
- Validating that analysis uses recent data
- After discovering data with dst-list-tables skill
- As part of automated data refresh workflows

## How to Use

### Basic Freshness Check

Check how old the data is:
```bash
python scripts/db/query_metadata.py --table-id <TABLE_ID> --check-freshness
```

### Check Against Threshold

Determine if data is fresh or stale using a specific age threshold:
```bash
python scripts/db/query_metadata.py --table-id <TABLE_ID> --check-freshness --max-age-days <N>
```

## Expected Output

The freshness check provides:

### Without Threshold
```
======================================================================
FRESHNESS CHECK FOR TABLE: FOLK1A
======================================================================
Table Name:      Population at the first day of the quarter
Last Updated:    2025-10-15T10:30:00
Fetch Timestamp: 2025-10-25T09:15:00
Data Age:        5 days ago (5 days)
======================================================================
```

### With Threshold
```
======================================================================
FRESHNESS CHECK FOR TABLE: FOLK1A
======================================================================
Table Name:      Population at the first day of the quarter
Last Updated:    2025-10-15T10:30:00
Fetch Timestamp: 2025-10-25T09:15:00
Data Age:        5 days ago (5 days)
Threshold:       30 days
Status:          ✓ FRESH

→ Data is within acceptable age threshold
======================================================================
```

### Stale Data Example
```
Status:          ✗ STALE

→ Data exceeds age threshold - consider refreshing
```

## Freshness Thresholds (Recommended)

Choose threshold based on how often DST updates the source data:

| Update Frequency | Recommended Threshold | Example Use Case |
|-----------------|----------------------|------------------|
| Daily | 1-2 days | Daily economic indicators |
| Weekly | 7 days | Weekly employment stats |
| Monthly | 30 days | Monthly population data |
| Quarterly | 90 days | Quarterly financial data |
| Annually | 365 days | Yearly census data |

**Note:** These are guidelines. Adjust based on your analysis requirements and tolerance for data lag.

## Decision Guide

### ✓ FRESH Status
- **Action:** Proceed with analysis confidently
- **Rationale:** Data is within acceptable age
- **Next Step:** Continue with dst-query or table-summary

### ✗ STALE Status
- **Action:** Consider refreshing data
- **Rationale:** Data exceeds age threshold
- **Next Step:** Evaluate if staleness impacts your analysis
- **Refresh:** Use Fetcher Agent if refresh needed

### Evaluation Questions
1. **Does staleness matter for this analysis?**
   - Trends over time: Fresh data may not be critical
   - Current snapshot: Fresh data is essential

2. **What's the cost of using stale data?**
   - Low impact: Proceed with disclaimer
   - High impact: Refresh immediately

3. **How expensive is refresh?**
   - Small table: Refresh quickly
   - Large table: Evaluate necessity first

## Interpreting Results

### Last Updated vs Fetch Timestamp

- **Last Updated**: When DST updated the source data
- **Fetch Timestamp**: When we downloaded it locally

**Important:** If last_updated is recent but fetch_timestamp is old, the source data has changed and a refresh will get newer data.

### Age Calculation

- **"5 days ago"**: Simple, human-readable
- **(5 days)**: Exact day count for threshold comparison
- **Just now**: Recently fetched (< 1 minute)
- **X hours/minutes ago**: Very recent
- **X months ago**: Quite old
- **X years ago**: Very stale

## Next Steps

### If Fresh → Continue Analysis
```bash
# Proceed with query or analysis
python scripts/db/table_summary.py --table-id <TABLE_ID>
python scripts/db/query_data.py --sql "SELECT * FROM dst_<table_id> LIMIT 10"
```

### If Stale → Inform User
Present findings to user:
- Data age
- Threshold used
- Recommendation (refresh or proceed)

### If Refresh Needed → Switch to Fetcher
```bash
python scripts/fetch_and_store.py --table-id <TABLE_ID> --overwrite
```

### If Acceptable → Proceed with Disclaimer
Continue analysis but note data age in results:
- "Analysis based on data from [date]"
- "Data is X days old as of [today]"

## Examples

### Example 1: Basic freshness check
```bash
python scripts/db/query_metadata.py --table-id FOLK1A --check-freshness
```

### Example 2: Check with 30-day threshold
```bash
python scripts/db/query_metadata.py --table-id FOLK1A --check-freshness --max-age-days 30
```

### Example 3: Strict 7-day threshold for daily data
```bash
python scripts/db/query_metadata.py --table-id DAILY_STATS --check-freshness --max-age-days 7
```

### Example 4: Lenient 90-day threshold for quarterly data
```bash
python scripts/db/query_metadata.py --table-id QUARTERLY_FIN --check-freshness --max-age-days 90
```

## Tips

### Before Important Analysis
- **Always check freshness** before critical analyses
- **Document data age** in your results
- **Consider impact** of staleness on conclusions

### Update Frequency Awareness
- Research DST's update schedule for specific tables
- Some tables update daily, others annually
- Match threshold to update frequency

### Automated Workflows
- Check freshness before scheduled analyses
- Auto-refresh if stale
- Log refresh decisions

### User Communication
- **Inform users** about data age
- **Explain thresholds** used
- **Recommend actions** based on results

## Common Workflows

### Workflow 1: Pre-Analysis Check
```bash
# 1. List available data
python scripts/db/query_metadata.py --list-all

# 2. Check freshness
python scripts/db/query_metadata.py --table-id FOLK1A --check-freshness --max-age-days 30

# 3. If fresh → analyze
# 4. If stale → refresh first
```

### Workflow 2: Conditional Refresh
```bash
# 1. Check freshness
python scripts/db/query_metadata.py --table-id FOLK1A --check-freshness --max-age-days 7

# 2. If stale → refresh
python scripts/fetch_and_store.py --table-id FOLK1A --overwrite

# 3. Proceed with fresh data
```

### Workflow 3: Multiple Tables
```bash
# Check freshness of all tables needed for analysis
python scripts/db/query_metadata.py --table-id TABLE1 --check-freshness --max-age-days 30
python scripts/db/query_metadata.py --table-id TABLE2 --check-freshness --max-age-days 30

# Refresh any stale tables
# Then proceed with analysis
```

## Troubleshooting

### "No fetch timestamp available"
- Table metadata may be incomplete
- Check metadata with dst-list-tables
- Re-fetch data to populate timestamp

### Unexpected Age
- Verify system clock is correct
- Check timestamp format in metadata
- Investigate if manual changes were made

### Always Shows Stale
- Threshold may be too strict
- Adjust --max-age-days parameter
- Consider DST's actual update frequency

## Best Practices

1. **Check freshness early** in your workflow
2. **Use appropriate thresholds** for data type
3. **Document data age** in analysis results
4. **Automate freshness checks** for regular analyses
5. **Balance refresh cost** vs staleness impact
6. **Communicate clearly** with users about data currency
