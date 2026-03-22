---
name: dr-profile
description: Profile Datarails Finance OS table fields. Analyze numeric fields for statistics and outliers, categorical fields for cardinality and frequencies.
user-invocable: true
allowed-tools:
  - mcp__datarails-finance-os__get_table_schema
  - mcp__datarails-finance-os__profile_table_summary
  - mcp__datarails-finance-os__profile_numeric_fields
  - mcp__datarails-finance-os__profile_categorical_fields
  - mcp__datarails-finance-os__get_field_distinct_values
argument-hint: "<table_id> [--numeric] [--categorical] [--field <field_name>]"
---

# Datarails Table Profiling

Deep profiling of Finance OS tables - analyze numeric statistics, categorical distributions, and data quality metrics.

## Workflow

### Step 1: Verify Authentication

If any tool call fails with an authentication or connection error, guide the user to connect via the Connectors UI ("+" > Connectors > Datarails > Connect).

### Step 2: Profile the Table

**Full profile (default):**
1. Get table schema with `get_table_schema`
2. Run `profile_table_summary` for overview
3. Run `profile_numeric_fields` for all numeric columns
4. Run `profile_categorical_fields` for all categorical columns
5. Present findings in organized sections

**Numeric only (--numeric):**
- Focus on `profile_numeric_fields`
- Show: min, max, mean, median, std dev, percentiles
- Highlight outliers (values beyond 3σ)

**Categorical only (--categorical):**
- Focus on `profile_categorical_fields`
- Show: cardinality, top values, null counts
- Highlight high-cardinality fields

**Specific field (--field):**
- Profile just that field with appropriate method
- Show detailed statistics and distribution

## Arguments

| Argument | Description |
|----------|-------------|
| `<table_id>` | Required - the table to profile |
| `--numeric` | Profile only numeric fields |
| `--categorical` | Profile only categorical fields |
| `--field <name>` | Profile a specific field |
| `--fields <a,b,c>` | Profile specific fields (comma-separated) |

## Example Interactions

**User: "/dr-profile 11442"**
```
📊 Profile: GL Transactions (ID: 11442)

═══════════════════════════════════════════════════
📈 NUMERIC FIELDS (8 columns)
═══════════════════════════════════════════════════

amount
├── Range: -1,250,000 to 8,750,000
├── Mean: 45,231 | Median: 12,500
├── Std Dev: 125,432
├── Nulls: 0 (0%)
├── Percentiles: P25=5,000 | P50=12,500 | P75=35,000 | P95=250,000
└── ⚠️ Outliers: 127 values beyond 3σ

quantity
├── Range: 0 to 10,000
├── Mean: 125 | Median: 50
├── Nulls: 1,234 (0.98%)
└── Distribution: Normal

═══════════════════════════════════════════════════
📋 CATEGORICAL FIELDS (16 columns)
═══════════════════════════════════════════════════

account_code (156 unique values)
├── Top: 4000-100 (10.0%), 4000-200 (6.6%), 5100-300 (6.3%)
├── Nulls: 0 (0%)
└── Cardinality: Low (156 / 125,432 = 0.12%)

department
├── Top: Sales (35%), Marketing (22%), Operations (18%)
├── Nulls: 892 (0.71%)
└── Cardinality: Very Low (12 unique)

vendor_id (HIGH CARDINALITY ⚠️)
├── Unique: 45,231 (36% of rows)
├── Nulls: 2,341 (1.87%)
└── Note: Consider if this should be a dimension table
```

**User: "/dr-profile 11442 --numeric"**
```
📈 Numeric Profile: GL Transactions

| Field     | Min      | Max        | Mean    | Median  | Std Dev | Nulls | Outliers |
|-----------|----------|------------|---------|---------|---------|-------|----------|
| amount    | -1.25M   | 8.75M      | 45,231  | 12,500  | 125,432 | 0%    | 127 ⚠️   |
| quantity  | 0        | 10,000     | 125     | 50      | 342     | 0.98% | 23       |
| unit_cost | 0.01     | 15,000     | 89.50   | 45.00   | 245     | 0%    | 45       |
...
```

**User: "/dr-profile 11442 --field amount"**
```
📊 Field Profile: amount (GL Transactions)

Type: DECIMAL
Nullable: No
Nulls: 0 (0%)

Statistics:
├── Count: 125,432
├── Min: -1,250,000
├── Max: 8,750,000
├── Mean: 45,231.45
├── Median: 12,500.00
├── Mode: 10,000.00
├── Std Dev: 125,432.18
├── Variance: 15,733,227,164

Percentiles:
├── P1:  -50,000    P5:  -10,000
├── P25:   5,000    P50:  12,500
├── P75:  35,000    P95: 250,000
└── P99: 750,000

Distribution: Right-skewed (many small values, few large)

Outliers (|z| > 3): 127 records
├── Below -3σ: 12 records (min: -1,250,000)
└── Above +3σ: 115 records (max: 8,750,000)

💡 Recommendation: Investigate the 127 outlier transactions
   Use: /dr-query 11442 "amount > 500000 OR amount < -100000"
```

## Data Quality Indicators

| Symbol | Meaning |
|--------|---------|
| ⚠️ | Potential issue requiring attention |
| ❌ | Data quality problem detected |
| ✅ | Field looks healthy |
| 📊 | Statistical insight |

## Tips

- Profile before running anomaly detection to understand baseline
- High null rates (>5%) may indicate data collection issues
- High cardinality categorical fields may need normalization
- Outliers aren't always bad - verify against business rules
## Related Skills

- `/dr-tables` - Discover available tables
- `/dr-anomalies` - Automated anomaly detection
- `/dr-query` - Investigate specific records
