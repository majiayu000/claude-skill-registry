---
name: pg-data
description: Generate safe, read-only PostgreSQL queries from natural language. Use when users need to query blog_small, ecommerce_medium, or saas_crm_large databases. Supports query generation, execution, and result analysis with confidence scoring.
---

# PostgreSQL Data Query Generator

Generate safe, production-ready PostgreSQL SELECT queries from natural language descriptions. This skill analyzes user requests, matches them to the appropriate database schema, generates secure SQL, tests execution, and validates results.

## When to Use This Skill

Use this skill when the user wants to:

- **Query data** from blog_small, ecommerce_medium, or saas_crm_large databases
- **Analyze data** with aggregations, joins, or complex filters
- **Generate reports** from the available databases
- **Explore database content** through natural language queries

## Available Databases

| Database | Description | Use Cases |
|----------|-------------|-----------|
| **blog_small** | Blog platform with users, posts, comments, categories, tags | Content analytics, author stats, engagement metrics |
| **ecommerce_medium** | E-commerce with products, orders, inventory, reviews | Sales analysis, inventory management, customer insights |
| **saas_crm_large** | Multi-tenant CRM with leads, deals, accounts, tickets | Pipeline analysis, sales performance, support metrics |

## Security Requirements

**CRITICAL**: All generated SQL must comply with these security rules:

### Allowed Operations
- `SELECT` statements only
- Read-only aggregate functions (COUNT, SUM, AVG, MIN, MAX, etc.)
- JOINs, subqueries, CTEs, window functions
- WHERE, GROUP BY, HAVING, ORDER BY, LIMIT clauses

### Prohibited Operations
- **NO** INSERT, UPDATE, DELETE, TRUNCATE, DROP, ALTER, CREATE
- **NO** EXECUTE, CALL, DO blocks
- **NO** pg_sleep, pg_terminate_backend, or any system functions
- **NO** COPY, \copy, or file operations
- **NO** SET, RESET, or configuration changes
- **NO** Comments containing sensitive data
- **NO** Dynamic SQL or string concatenation for queries
- **NO** Access to pg_catalog system tables (except for metadata queries)
- **NO** Sensitive data exposure (passwords, API keys, tokens, hashes)

### SQL Injection Prevention
- Use parameterized queries when possible
- Validate and sanitize any user-provided values
- Never concatenate user input directly into SQL
- Escape special characters properly

## Workflow

### Step 1: Analyze User Request

Parse the user's natural language query to determine:

1. **Target database**: Which database(s) does this query relate to?
   - Blog content, posts, comments, authors → `blog_small`
   - Products, orders, sales, inventory, reviews → `ecommerce_medium`
   - Leads, deals, accounts, contacts, tickets, subscriptions → `saas_crm_large`

2. **Query intent**: What data does the user want?
   - Listing/searching records
   - Aggregation/statistics
   - Relationships/joins
   - Time-based analysis

3. **Output format**: Does the user want SQL only or results?
   - If user says "give me the SQL" or "show me the query" → Return SQL only
   - Otherwise → Execute and return results (default)

### Step 2: Read Database Reference

Read the appropriate reference file(s) to understand the schema:

```bash
# Read the reference file for the target database
cat .claude/skills/pg-data/references/<database_name>.md
```

Reference files contain:
- Table structures with columns and types
- Foreign key relationships
- Available views
- Common query patterns

### Step 3: Generate SQL

Generate a SQL query following these guidelines:

1. **Start with the primary table** that best matches the user's intent
2. **Add JOINs** only when necessary for the requested data
3. **Use appropriate indexes** - check the reference for available indexes
4. **Include sensible defaults**:
   - Add `LIMIT 100` for unbounded queries
   - Use meaningful column aliases
   - Order results logically

#### SQL Template

```sql
-- Purpose: <brief description of what this query does>
SELECT
    <columns with meaningful aliases>
FROM <primary_table> <alias>
[JOIN <related_table> ON <condition>]
[WHERE <filters>]
[GROUP BY <grouping>]
[HAVING <aggregate_filters>]
[ORDER BY <ordering>]
[LIMIT <reasonable_limit>];
```

### Step 4: Validate SQL Safety

Before execution, verify the query:

1. **Check for prohibited keywords**:
   ```
   INSERT, UPDATE, DELETE, DROP, ALTER, CREATE, TRUNCATE,
   EXECUTE, CALL, DO, COPY, SET, RESET, pg_sleep, pg_terminate
   ```

2. **Verify read-only nature**: Query must only retrieve data

3. **Check for sensitive data exposure**: Exclude password_hash, api_key, token fields

### Step 5: Execute and Test

Execute the SQL using psql:

```bash
PGPASSWORD=postgres psql -h localhost -p 5432 -U postgres -d <database_name> -c "<SQL_QUERY>"
```

**If execution fails:**
1. Analyze the error message
2. Check for:
   - Invalid column/table names
   - Type mismatches
   - Syntax errors
   - Missing JOINs
3. Regenerate the SQL with corrections
4. Return to Step 5 (max 3 retries)

### Step 6: Analyze Results and Score Confidence

Evaluate the query results and assign a confidence score (0-10):

| Score | Meaning | Action |
|-------|---------|--------|
| 10 | Perfect match, expected results | Return results |
| 8-9 | Good match, minor uncertainties | Return results with notes |
| 7 | Acceptable but could be improved | Return results with caveats |
| 5-6 | Uncertain if this answers the question | Regenerate or ask for clarification |
| 1-4 | Likely wrong interpretation | Regenerate SQL |
| 0 | Completely wrong or empty results | Regenerate or explain issue |

**Scoring Criteria:**
- Does the result count seem reasonable?
- Do the columns match what was asked?
- Are the values in expected ranges?
- Does the data make logical sense?

**If score < 7:**
1. Analyze what might be wrong
2. Consider alternative interpretations
3. Regenerate SQL with different approach
4. Return to Step 5

### Step 7: Return Results

Based on user's preference:

**If returning results (default):**
```
## Query Results

**Database**: <database_name>
**Confidence**: <score>/10

### SQL Executed
\`\`\`sql
<the_sql_query>
\`\`\`

### Results
<formatted_results_table>

### Analysis
<brief explanation of what the results show>
```

**If returning SQL only:**
```
## Generated SQL

**Database**: <database_name>
**Purpose**: <what_this_query_does>

\`\`\`sql
<the_sql_query>
\`\`\`

### Usage
\`\`\`bash
PGPASSWORD=postgres psql -h localhost -p 5432 -U postgres -d <database_name> -c "<sql>"
\`\`\`
```

## Example Queries

### Blog Database Examples

**User**: "Show me the top 10 authors by post count"

```sql
SELECT
    u.username,
    u.full_name,
    COUNT(p.id) AS post_count,
    SUM(p.view_count) AS total_views
FROM users u
JOIN posts p ON u.id = p.author_id
WHERE p.status = 'published'
GROUP BY u.id, u.username, u.full_name
ORDER BY post_count DESC
LIMIT 10;
```

**User**: "Find posts with the most comments in the last 30 days"

```sql
SELECT
    p.title,
    p.slug,
    u.username AS author,
    COUNT(c.id) AS comment_count,
    p.view_count
FROM posts p
JOIN users u ON p.author_id = u.id
LEFT JOIN comments c ON p.id = c.post_id
WHERE p.published_at >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY p.id, u.username
ORDER BY comment_count DESC
LIMIT 20;
```

### E-commerce Database Examples

**User**: "What are the best selling products this month?"

```sql
SELECT
    p.name AS product_name,
    p.sku,
    c.name AS category,
    SUM(oi.quantity) AS units_sold,
    SUM(oi.total_price) AS revenue
FROM products p
JOIN order_items oi ON p.id = oi.product_id
JOIN orders o ON oi.order_id = o.id
LEFT JOIN categories c ON p.category_id = c.id
WHERE o.created_at >= DATE_TRUNC('month', CURRENT_DATE)
    AND o.status NOT IN ('cancelled', 'refunded')
GROUP BY p.id, p.name, p.sku, c.name
ORDER BY revenue DESC
LIMIT 20;
```

**User**: "Show me customers who haven't ordered in 90 days"

```sql
SELECT
    u.email,
    u.first_name,
    u.last_name,
    MAX(o.created_at) AS last_order_date,
    COUNT(o.id) AS total_orders,
    SUM(o.total_amount) AS lifetime_value
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id, u.email, u.first_name, u.last_name
HAVING MAX(o.created_at) < CURRENT_DATE - INTERVAL '90 days'
    OR MAX(o.created_at) IS NULL
ORDER BY lifetime_value DESC NULLS LAST
LIMIT 50;
```

### CRM Database Examples

**User**: "Show the sales pipeline for organization 1"

```sql
SELECT
    ps.name AS stage_name,
    ps.stage_type,
    COUNT(d.id) AS deal_count,
    SUM(d.amount) AS total_value,
    AVG(d.probability) AS avg_probability,
    SUM(d.amount * d.probability / 100) AS weighted_value
FROM pipeline_stages ps
LEFT JOIN deals d ON ps.id = d.stage_id
JOIN pipelines p ON ps.pipeline_id = p.id
WHERE p.organization_id = 1
GROUP BY ps.id, ps.name, ps.stage_type, ps.display_order
ORDER BY ps.display_order;
```

**User**: "Find all overdue tickets with high priority"

```sql
SELECT
    t.ticket_number,
    t.subject,
    t.priority,
    t.status,
    a.name AS account_name,
    u.first_name || ' ' || u.last_name AS assigned_to,
    t.created_at,
    CURRENT_DATE - DATE(t.created_at) AS days_open
FROM tickets t
LEFT JOIN accounts a ON t.account_id = a.id
LEFT JOIN users u ON t.assigned_to = u.id
WHERE t.status NOT IN ('resolved', 'closed')
    AND t.priority IN ('high', 'urgent')
ORDER BY
    CASE t.priority WHEN 'urgent' THEN 1 WHEN 'high' THEN 2 END,
    t.created_at
LIMIT 50;
```

## Handling Ambiguous Requests

When the user's request is unclear:

1. **Ask clarifying questions** if critical information is missing:
   - Which database to query?
   - What time period?
   - What filters to apply?

2. **Make reasonable assumptions** and document them:
   - Default to recent data (last 30 days)
   - Use sensible limits (LIMIT 100)
   - Include common filters (active records, published posts)

3. **Suggest alternatives** if multiple interpretations exist:
   - "I interpreted this as X. If you meant Y, let me know."

## Reference Files

- **[blog_small.md](./references/blog_small.md)** - Blog platform schema
- **[ecommerce_medium.md](./references/ecommerce_medium.md)** - E-commerce schema
- **[saas_crm_large.md](./references/saas_crm_large.md)** - SaaS CRM schema

## Error Recovery

### Common Errors and Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `column does not exist` | Wrong column name | Check reference file for correct name |
| `relation does not exist` | Wrong table name | Verify table exists in schema |
| `operator does not exist` | Type mismatch | Cast to correct type |
| `syntax error` | Invalid SQL | Review query structure |
| `permission denied` | Attempting write op | Ensure SELECT only |

### Retry Logic

1. Parse error message
2. Identify the issue
3. Consult reference file
4. Regenerate corrected SQL
5. Maximum 3 retry attempts
6. If still failing, explain the issue to user

## Notes

- Always respect multi-tenant boundaries in saas_crm_large (filter by organization_id)
- Use views when available for common query patterns
- Consider query performance for large result sets
- Results are truncated to first 100 rows by default
