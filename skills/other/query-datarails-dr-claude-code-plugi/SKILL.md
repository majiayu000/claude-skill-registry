---
name: dr-query
description: Query Datarails Finance OS tables with filters. Fetch specific records, get samples, or run custom queries for investigation.
user-invocable: true
allowed-tools:
  - mcp__datarails-finance-os__get_table_schema
  - mcp__datarails-finance-os__get_records_by_filter
  - mcp__datarails-finance-os__get_sample_records
  - mcp__datarails-finance-os__execute_query
  - mcp__datarails-finance-os__get_field_distinct_values
argument-hint: "<table_id> [filter_expression] [--sample] [--limit N]"
---

# Datarails Data Query

Query Finance OS tables - fetch records by filter, get samples, or run custom queries.

## Workflow

### Step 1: Verify Authentication

If any tool call fails with an authentication or connection error, guide the user to connect via the Connectors UI ("+" > Connectors > Datarails > Connect).

### Step 2: Understand the Request

- **Sample data**: Use `get_sample_records` (max 20 rows)
- **Filtered records**: Use `get_records_by_filter` (max 500 rows)
- **Custom query**: Use `execute_query` (max 1000 rows)

### Step 3: Execute and Present

Format results as a readable table. Highlight any notable patterns.

## Arguments

| Argument | Description |
|----------|-------------|
| `<table_id>` | Required - the table to query |
| `[filter]` | Filter expression (see syntax below) |
| `--sample` | Get random sample (default 20 rows) |
| `--limit N` | Limit results (max 500 for filters, 1000 for queries) |
| `--sql` | Treat filter as raw SQL-like query |

## Filter Syntax

**Basic equality:**
```
field = "value"
field = 123
```

**Comparison:**
```
amount > 1000
amount >= 1000
amount < 5000
posting_date > "2024-01-01"
```

**Multiple conditions:**
```
amount > 1000 AND department = "Sales"
status = "active" OR status = "pending"
```

**IN list:**
```
account_code IN ("4000-100", "4000-200", "4000-300")
```

**NULL checks:**
```
vendor_name IS NULL
vendor_name IS NOT NULL
```

**Pattern matching:**
```
description LIKE "%adjustment%"
account_code LIKE "4000-%"
```

## Example Interactions

**User: "/dr-query 11442 --sample"**
```
📋 Sample: GL Transactions (20 random records)

| transaction_id | account_code | amount    | posting_date | department |
|----------------|--------------|-----------|--------------|------------|
| 45231          | 4000-100     | 12,500.00 | 2024-01-15   | Sales      |
| 67892          | 5100-200     | -3,200.00 | 2024-01-14   | Operations |
| 23456          | 4000-300     | 45,000.00 | 2024-01-13   | Marketing  |
...

Showing 20 of 125,432 total records
```

**User: "/dr-query 11442 amount > 100000"**
```
📋 Query Results: GL Transactions
Filter: amount > 100000

| transaction_id | account_code | amount      | posting_date | vendor_name     |
|----------------|--------------|-------------|--------------|-----------------|
| 89234          | 4000-100     | 2,150,000   | 2024-01-10   | Acme Corp       |
| 12345          | 4000-200     | 1,800,000   | 2024-01-08   | Global Supply   |
| 34567          | 5100-100     | 850,000     | 2024-01-05   | Tech Partners   |
...

Found 127 records matching filter (showing first 100)
Use --limit 500 to see more results
```

**User: "/dr-query 11442 department = 'Sales' AND amount > 50000 --limit 50"**
```
📋 Query Results: GL Transactions
Filter: department = 'Sales' AND amount > 50000

Found 234 records (showing 50)

| transaction_id | account_code | amount    | posting_date | vendor_name     |
|----------------|--------------|-----------|--------------|-----------------|
| 45231          | 4000-100     | 125,000   | 2024-01-15   | ABC Company     |
...
```

**User: "/dr-query 11442 --sql SELECT account_code, SUM(amount) as total FROM table GROUP BY account_code ORDER BY total DESC"**
```
📋 Custom Query Results

| account_code | total          |
|--------------|----------------|
| 4000-100     | 45,231,000.00  |
| 4000-200     | 32,150,000.00  |
| 5100-300     | 28,750,000.00  |
...

Returned 156 rows
```

**User: "/dr-query 11442 posting_date > '2024-01-01' AND vendor_name IS NULL"**
```
📋 Query Results: GL Transactions
Filter: posting_date > '2024-01-01' AND vendor_name IS NULL

Found 892 records with missing vendor_name since Jan 1

| transaction_id | account_code | amount    | posting_date | vendor_id |
|----------------|--------------|-----------|--------------|-----------|
| 56789          | 4000-100     | 5,000.00  | 2024-01-12   | V-1234    |
...

💡 Note: These records have vendor_id but missing vendor_name
   Consider joining with vendor master table
```

## Filter Object Format (API)

When using `get_records_by_filter` programmatically:

```json
{
  "status": "active",                    // Equality
  "amount": {">": 1000, "<": 5000},      // Range
  "account_code": {"in": ["A", "B"]},    // IN list
  "vendor_name": {"is_null": true},      // NULL check
  "description": {"like": "%adj%"}       // Pattern
}
```

## Limits

| Method | Max Rows | Use Case |
|--------|----------|----------|
| `get_sample_records` | 20 | Quick data inspection |
| `get_records_by_filter` | 500 | Investigation queries |
| `execute_query` | 1000 | Complex aggregations |

## Tips

- Start with `--sample` to understand data format
- Use filters to investigate anomalies found by `/dr-anomalies`
- For aggregations, use `--sql` with GROUP BY
- If you need more than 500 rows, consider profiling instead
## Related Skills

- `/dr-tables` - Get schema before querying
- `/dr-anomalies` - Find issues to investigate
- `/dr-profile` - Statistical analysis
