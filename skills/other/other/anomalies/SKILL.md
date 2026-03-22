---
name: dr-anomalies
description: Detect data anomalies in Datarails Finance OS tables. Finds outliers, missing values, duplicates, and data quality issues.
user-invocable: true
allowed-tools:
  - mcp__datarails-finance-os__get_table_schema
  - mcp__datarails-finance-os__profile_table_summary
  - mcp__datarails-finance-os__detect_anomalies
  - mcp__datarails-finance-os__profile_numeric_fields
  - mcp__datarails-finance-os__profile_categorical_fields
  - mcp__datarails-finance-os__get_records_by_filter
  - mcp__datarails-finance-os__get_sample_records
argument-hint: "<table_id> [--severity critical|high|medium|low] [--type <anomaly_type>]"
---

# Datarails Anomaly Detection

Automated anomaly detection for Finance OS tables - find data quality issues, outliers, and suspicious patterns.

## Workflow

### Step 1: Verify Authentication

If any tool call fails with an authentication or connection error, guide the user to connect via the Connectors UI ("+" > Connectors > Datarails > Connect).

### Step 2: Run Detection

1. Get table schema for context
2. Run `detect_anomalies` for comprehensive analysis
3. Optionally run `profile_numeric_fields` and `profile_categorical_fields` for deeper stats
4. If specific anomalies need investigation, use `get_records_by_filter` to fetch examples

### Step 3: Present Findings

Organize findings by severity:
- 🔴 **Critical** - Requires immediate attention
- 🟠 **High** - Should be addressed soon
- 🟡 **Medium** - Worth investigating
- 🟢 **Low** - Minor issues or informational

## Arguments

| Argument | Description |
|----------|-------------|
| `<table_id>` | Required - the table to analyze |
| `--severity <level>` | Filter to specific severity (critical, high, medium, low) |
| `--type <type>` | Filter to specific anomaly type |

## Anomaly Types Detected

| Type | Description |
|------|-------------|
| `outliers` | Numeric values beyond 3 standard deviations |
| `missing` | Unexpected NULL values or patterns |
| `duplicates` | Potential duplicate records |
| `temporal` | Date/time anomalies (gaps, future dates) |
| `categorical` | Rare values, unexpected categories |
| `referential` | Foreign key or relationship issues |

## Example Interactions

**User: "/dr-anomalies 11442"**
```
🔍 Anomaly Detection: GL Transactions (ID: 11442)
═══════════════════════════════════════════════════════════

Scanned 125,432 records | Found 47 anomalies

🔴 CRITICAL (3 findings)
───────────────────────────────────────────────────────────

1. DUPLICATE TRANSACTIONS
   • 23 potential duplicate records detected
   • Same amount, date, and vendor within 1 minute
   • Records: [45231, 45232], [67892, 67893], ...

   💡 Recommendation: Review for accidental double-entry
   📋 Query: /dr-query 11442 "transaction_id IN (45231, 45232)"

2. FUTURE-DATED TRANSACTIONS
   • 5 transactions with posting_date > today
   • Dates range from 2024-02-15 to 2024-12-31

   💡 Recommendation: Verify if these are planned entries
   📋 Query: /dr-query 11442 "posting_date > '2024-01-20'"

3. NEGATIVE INVENTORY QUANTITIES
   • 8 records with quantity < 0
   • Min value: -500 (record 89234)

   💡 Recommendation: Check if returns are properly coded

🟠 HIGH (12 findings)
───────────────────────────────────────────────────────────

4. AMOUNT OUTLIERS
   • 127 transactions beyond normal range
   • 115 above $500,000 (expected max ~$250,000)
   • 12 below -$100,000 (expected min ~-$50,000)

   💡 Recommendation: Verify large transactions are approved

5. HIGH NULL RATE: vendor_name
   • 2,341 records (1.87%) missing vendor_name
   • But vendor_id is present

   💡 Recommendation: Join with vendor master to populate

...

🟡 MEDIUM (18 findings)
───────────────────────────────────────────────────────────

12. RARE CATEGORY VALUES
    • department contains 3 values appearing < 10 times
    • Values: "TEST", "MIGRATION", "UNKNOWN"

    💡 Recommendation: Standardize or reclassify

...

🟢 LOW (14 findings)
───────────────────────────────────────────────────────────

35. TRAILING WHITESPACE
    • account_code has 45 values with trailing spaces

    💡 Recommendation: Trim during ETL

═══════════════════════════════════════════════════════════
📊 SUMMARY
═══════════════════════════════════════════════════════════

| Severity | Count | Action                    |
|----------|-------|---------------------------|
| Critical | 3     | Investigate immediately   |
| High     | 12    | Address this week         |
| Medium   | 18    | Plan for remediation      |
| Low      | 14    | Fix during maintenance    |

Data Quality Score: 87/100 ⚠️
Primary concerns: Duplicates, Future dates, Amount outliers
```

**User: "/dr-anomalies 11442 --severity critical"**
```
🔴 Critical Anomalies: GL Transactions

Found 3 critical issues requiring immediate attention:

1. DUPLICATE TRANSACTIONS (23 records)
   ...

2. FUTURE-DATED TRANSACTIONS (5 records)
   ...

3. NEGATIVE INVENTORY QUANTITIES (8 records)
   ...
```

**User: "/dr-anomalies 11442 --type outliers"**
```
📊 Outlier Analysis: GL Transactions

Analyzed 8 numeric fields for statistical outliers (|z| > 3)

amount: 127 outliers
├── Above 3σ: 115 records
│   ├── Max: $8,750,000 (z=12.4)
│   ├── Sample: [45231: $2.1M], [67892: $1.8M], [89234: $1.5M]
│   └── Pattern: Mostly Q4 entries (82%)
└── Below -3σ: 12 records
    ├── Min: -$1,250,000 (z=-8.2)
    └── Sample: [12345: -$800K], [23456: -$650K]

quantity: 23 outliers
├── All above 3σ (high quantities)
├── Max: 10,000 (z=5.1)
└── 18 of 23 are from department="Warehouse"

unit_cost: 45 outliers
...
```

## Investigation Workflow

When anomalies are detected:

1. **Review findings** - Understand the scope and patterns
2. **Fetch examples** - Use `/dr-query` to see actual records
3. **Verify business rules** - Some "anomalies" may be valid
4. **Document decisions** - Note which are false positives
5. **Create remediation plan** - Prioritize by severity

## Related Skills

- `/dr-profile` - Detailed field statistics
- `/dr-query` - Fetch specific records
- `/dr-tables` - Understand table structure
