---
name: data-fetch-analysis
description: "Connect to databases, monitoring systems, analytics platforms, and APIs to fetch, analyze, and report on data. Use when the user says 'query the database', 'check the metrics', 'fetch data from', 'analyze this data', 'pull logs', 'generate a report', 'check error rates', 'what does the data show', 'dashboard data', or 'investigate this trend'. Also triggers on 'data analysis', 'database query', 'monitoring data', 'log analysis', 'metrics investigation', 'data pipeline', 'data fetching', 'SQL query', or 'run a query'."
version: 1.0.0
---

# Data Fetch & Analysis

## Purpose

Developers need to query databases, check dashboards, analyze logs, and investigate data without leaving their editor. This skill provides structured approaches for safe data fetching, thorough analysis, and clear presentation of findings. It enforces read-only defaults, query guardrails, and a disciplined workflow so that ad-hoc investigation does not turn into accidental data mutation or production incidents.

## When to Activate

- Querying databases to investigate bugs, verify behavior, or answer business questions
- Checking metrics, error rates, or dashboard data from monitoring systems
- Pulling and analyzing application logs for debugging or incident response
- Building ad-hoc reports from raw data sources
- Investigating performance trends, traffic patterns, or usage analytics
- Verifying data migrations, backfills, or pipeline correctness

## Safety-First Data Access

These five rules are non-negotiable. Every query must satisfy all of them.

### Rule 1: Default to Read-Only

Never run write operations (INSERT, UPDATE, DELETE, DROP, ALTER, TRUNCATE) unless the user explicitly asks for a write. Default to SELECT and read-only connections. If a write is requested, confirm the target environment and expected row count before executing.

### Rule 2: Always Use LIMIT on Exploratory Queries

Start with `LIMIT 10` for initial exploration. Increase only after confirming the result set size is manageable. For aggregation queries, ensure GROUP BY cardinality is bounded. Never `SELECT *` from a large table without LIMIT.

### Rule 3: Never Expose Credentials or PII

- Never print connection strings, passwords, API keys, or tokens in output
- Redact columns containing emails, phone numbers, SSNs, or other PII before displaying results
- Use environment variables for all connection parameters
- Remember that terminal scrollback is often visible to others

### Rule 4: Use Parameterized Queries

Never interpolate user-provided values directly into SQL strings. Use parameterized queries or prepared statements. This applies to every query language, not just SQL.

```sql
-- WRONG: String interpolation
SELECT * FROM users WHERE email = '${userInput}';

-- CORRECT: Parameterized
SELECT * FROM users WHERE email = $1;
```

### Rule 5: Confirm Before Expensive Operations

Before running any of the following, confirm with the user:
- Full table scans on tables with more than 100k rows
- Cross-joins or cartesian products
- Queries without WHERE clauses on large tables
- Queries touching multiple large tables
- Any query expected to run longer than 10 seconds

Use `EXPLAIN` (or equivalent) to estimate cost before executing.

## Analysis Workflow

Follow these five steps for every data investigation. Do not skip steps.

### Step 1: Define the Question

State the specific question this data analysis will answer. Vague requests produce vague results. Restate the user's question in precise, measurable terms.

- BAD: "Check the database for issues"
- GOOD: "What is the error rate for payment processing in the last 24 hours, broken down by error type?"

### Step 2: Identify the Source

Determine where the relevant data lives. Confirm:
- Which database, service, or API holds this data?
- Which environment (production, staging, development)?
- Is a read replica available? Always prefer read replicas for analytics.
- What authentication is needed?

### Step 3: Craft the Query

Write the minimal query that answers the question. Follow these principles:
- Select only the columns you need
- Apply filters early (WHERE before GROUP BY)
- Use appropriate indexes (check with EXPLAIN)
- Include LIMIT for safety
- Set explicit timeouts

### Step 4: Execute Safely

Run the query with guardrails:
- Set `statement_timeout` (PostgreSQL) or equivalent
- Use read-only connections or transactions where possible
- Monitor execution time; cancel if unexpectedly long
- Capture results before processing

### Step 5: Interpret and Present

Summarize findings in plain language with supporting data. Do not dump raw query output without interpretation. Use the output format specified below.

## Data Source Patterns

See `references/data-source-connectors.md` for detailed connection patterns covering:

- **PostgreSQL / MySQL** — CLI usage, connection strings, read-only setup, statement timeouts, SSL configuration
- **Redis** — Key inspection, memory analysis, slow log review
- **MongoDB** — mongosh usage, read preferences, query profiling
- **Application Logs** — Structured JSON parsing with jq, grep patterns for common log formats
- **HTTP APIs** — curl with authentication, pagination handling, rate limit awareness
- **Prometheus / Grafana** — PromQL basics, rate calculations, histogram queries, API endpoints

## Query Patterns

See `references/query-patterns.md` for reusable query templates covering:

- **Aggregation & Grouping** — COUNT, SUM, AVG with GROUP BY and HAVING
- **Time-Series Analysis** — Bucketing, moving averages, year-over-year comparisons
- **Anomaly Detection** — Standard deviation baselines, spike/drop detection, percentile analysis
- **Top-N Analysis** — Window functions, partitioned ranking
- **Funnel Analysis** — Multi-step conversion tracking
- **Join Patterns** — INNER, LEFT, LATERAL joins with performance considerations

## Output Format

Present every analysis using this structure:

```
DATA ANALYSIS REPORT
====================
Question: [what we're investigating]
Source: [database/service/API queried]
Time Range: [if applicable]

Findings:
1. [Key finding with supporting data]
2. [Key finding with supporting data]
3. [Key finding with supporting data]

Data:
[formatted table or summary statistics]

Recommendation: [actionable next step based on findings]
```

Guidelines for the report:
- Lead with the answer, not the methodology
- Include exact numbers, not just qualitative descriptions
- Format tables with aligned columns for readability
- Note any caveats (sample size, time range limitations, data quality issues)
- If the data does not conclusively answer the question, say so explicitly

## Gotchas

### Connection Timeouts

Set explicit timeouts on every connection. Default database connections hang forever if the server is unreachable. Use `connect_timeout` for connection establishment and `statement_timeout` for query execution.

```sql
-- PostgreSQL: set per-session timeout
SET statement_timeout = '30s';
```

### Environment Confusion

Confirm the target environment before running any query. A connection string that looks like staging may point to production. Verify by checking:
- The hostname (does it contain "prod", "primary", or a production IP range?)
- The database name
- Row counts (production usually has orders of magnitude more data)

### Memory Pressure from Large Result Sets

Large result sets crash the client process or exhaust memory. Mitigations:
- Always use LIMIT for exploration
- Use COPY or `\copy` for large exports
- Stream results with cursors for processing
- Paginate with keyset pagination (WHERE id > last_seen_id)

### Timezone Confusion

Database timestamps may be stored in UTC, server-local time, or without timezone information. Before analyzing time-series data:
- Check the column type (`timestamp` vs `timestamptz`)
- Check the session timezone (`SHOW timezone`)
- Convert explicitly (`AT TIME ZONE 'UTC'`)

### Sampling Bias

`LIMIT 10` returns the first 10 rows the database finds, not a representative sample. For analysis:
- Use `ORDER BY random() LIMIT n` for random sampling (expensive on large tables)
- Use `TABLESAMPLE SYSTEM(percentage)` in PostgreSQL for efficient sampling
- Aggregate the full dataset rather than sampling when precision matters

### PII in Results

Query results displayed in the terminal may contain personally identifiable information. Terminal history, screen sharing, and scrollback are all potential exposure vectors.
- Exclude PII columns from SELECT lists
- Use masking functions where available
- Truncate or hash sensitive values in output

### Index Usage on Production

Unindexed queries on production databases cause performance degradation for all users. Always:
- Run `EXPLAIN ANALYZE` on staging first
- Check that your WHERE and JOIN columns are indexed
- Avoid functions on indexed columns (they prevent index usage)
- Monitor query duration and cancel if unexpectedly slow
