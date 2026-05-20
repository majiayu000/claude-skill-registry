---
name: optimize-storage-costs
description: Optimize BigQuery storage costs by identifying and removing dead-end and unused tables. USE FOR analyzing storage waste, reviewing tables with no consumption, cleaning up unused datasets, or implementing storage cost reduction strategies.
---

# Optimize Storage Costs (Dead-end and Unused Tables)

## Purpose

Identify and remove BigQuery tables that contribute to storage costs but have no active consumption, based on Masthead Data lineage analysis.

## Table Categories

Masthead Data uses lineage analysis to identify tables, but relies on visible pipeline references. Modification timestamps are critical:

| Type         | Definition                                   | Indicators                         | Watch for                                                                                                     |
| ------------ | -------------------------------------------- | ---------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| **Dead-end** | Regularly updated, no downstream consumption | Updated but never read in 30+ days | External writers outside lineage graph (manual jobs, independent pipelines)                                   |
| **Unused**   | No upstream or downstream activity           | No reads/writes in 30+ days        | Recent `lastModifiedTime` despite "Unused" flag suggests external writer—**do not drop without verification** |

### Key Signal

If a table is flagged `Unused` **and** has a recent modification timestamp, something outside Masthead's visibility is writing to it. This always warrants investigation before dropping.

## When to Use

- Reducing storage costs when budget is constrained
- Cleaning up abandoned tables and pipelines
- Implementing regular storage hygiene
- Investigating sudden storage cost increases

## Prerequisites

- Masthead Data agent v0.2.7+ installed (for accurate lineage)
- Access to Masthead insights dataset: `masthead-prod.httparchive.insights`
- BigQuery permissions to query insights and drop tables

## Implementation Steps

### Step 1: Query Storage Waste

```bash
bq query --project_id=YOUR_PROJECT --use_legacy_sql=false --format=csv \
"SELECT
  subtype,
  project_id,
  target_resource,
  SAFE.STRING(operations[0].resource_type) AS resource_type,
  SAFE.INT64(overview.num_bytes) / POW(1024, 4) AS total_tib,
  SAFE.FLOAT64(overview.cost_30d) AS cost_usd_30d,
  SAFE.FLOAT64(overview.savings_30d) AS savings_usd_30d
FROM \`masthead-prod.httparchive.insights\`
WHERE category = 'Cost'
  AND subtype IN ('Dead end table', 'Unused table')
  AND overview.num_bytes IS NOT NULL
  AND SAFE.FLOAT64(overview.savings_30d) > 10
  AND target_resource NOT LIKE '%analytics_%'  -- Filter out low-impact GA intraday tables
ORDER BY savings_usd_30d DESC" > storage_waste.csv
```

**Note:** Sorting by `savings_usd_30d` instead of `total_tib` prioritizes high-impact targets for review.

**Alternative: Use Masthead UI**

- Navigate to [Dictionary page](https://app.mastheadata.com/dictionary?tab=Tables&deadEnd=true)
- Filter by `Dead-end` or `Unused` labels
- Export table list for review

### Step 2: Review and Decide

Review `storage_waste.csv` and add a `status` column with values:

- `keep` - Table is needed
- `to drop` - Safe to remove
- `investigate` - Needs further analysis

**Review criteria:**

- Is this a backup or archive table? (consider alternative storage)
- Is there a downstream dependency not captured in lineage?
- Is this table part of an active experiment or migration?
- **For repo-managed projects:** Search the codebase (e.g., `grep` for table name in model definitions, scripts) to confirm ownership. Table naming can be misleading (e.g., `cwv_tech_*` may seem like current outputs but could be legacy).
- **Check for disabled producers:** If a Dataform `publish()` has `disabled: true` but the underlying BigQuery table still exists and has recent modifications, either the table is abandoned or an external process took over—both warrant investigation.

### Step 3: Drop Approved Tables

```bash
# Generate DROP statements
awk -F',' '$NF=="to drop" {
  print "bq rm -f -t " $4
}' storage_waste.csv > drop_tables.sh

# Review generated commands
cat drop_tables.sh

# Execute (after review!)
bash drop_tables.sh
```

**Safe mode (dry-run first):**

```bash
# Add --dry-run flag to each command
sed 's/bq rm/bq rm --dry-run/' drop_tables.sh > drop_tables_dryrun.sh
bash drop_tables_dryrun.sh
```

### Step 4: Verify Savings

After 24-48 hours, check storage reduction in Masthead:

- [Storage Cost Insights](https://app.mastheadata.com/costs?tab=Storage+costs)
- Compare before/after storage size and costs

## Decision Framework

| Monthly Savings | Action                           | Recency Check                                                     |
| --------------- | -------------------------------- | ----------------------------------------------------------------- |
| < $10           | Consider keeping (low ROI)       | Skip if `lastModifiedTime` > 12 months old (hygiene only)         |
| $10-$100        | Review and drop if unused        | Check modification date; recent writes require owner verification |
| $100-$1000      | Priority review, likely drop     | Mandatory verification if modified in last 30 days                |
| > $1000         | Immediate investigation required | Always verify external writer before any action                   |

## Key Notes

- **Dead-end tables** may indicate pipeline issues - investigate before dropping
- **Unused tables with recent modifications** are the highest-priority investigate cases. The gap between Masthead's "no lineage" and actual writes means an external dependency exists.
- Tables can be restored from time travel (7 days) or fail-safe (7 days after time travel)
- Consider archiving to Cloud Storage if compliance requires retention
- Coordinate with data teams before dropping shared datasets
- Wait 14 days after storage billing model changes before dropping tables

## Related Optimizations

- **Storage billing model**: Switch between Logical/Physical pricing (see docs)
- **Table expiration**: Set automatic expiration for temporary tables
- **Partitioning**: Use partitioned tables with expiration policies

## Documentation

- [Masthead Storage Costs](https://docs.mastheadata.com/cost-insights/storage-costs)
- [BigQuery Storage Pricing](https://cloud.google.com/bigquery/pricing#storage)
