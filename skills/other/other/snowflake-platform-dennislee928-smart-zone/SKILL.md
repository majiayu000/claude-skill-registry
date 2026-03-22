---
name: snowflake-platform
description: |
  Build on Snowflake's AI Data Cloud with snow CLI, Cortex AI (COMPLETE, SUMMARIZE, AI_FILTER), Native Apps, and Snowpark. Covers JWT auth, account identifiers, Marketplace publishing. Prevents 11 documented errors.

  Use when: Snowflake apps, Cortex AI SQL, Native App publishing. Troubleshoot: JWT auth failures, account locator confusion, memory leaks, AI throttling.
user-invocable: true
license: MIT
---

# Snowflake Platform Skill

Build and deploy applications on Snowflake's AI Data Cloud using the snow CLI, Cortex AI functions, Native Apps, and Snowpark.

## Quick Start

### Install Snowflake CLI

```bash
pip install snowflake-cli
snow --version  # Should show 3.14.0+
```

### Configure Connection

```bash
# Interactive setup
snow connection add

# Or create ~/.snowflake/config.toml manually
```

```toml
[connections.default]
account = "orgname-accountname"
user = "USERNAME"
authenticator = "SNOWFLAKE_JWT"
private_key_path = "~/.snowflake/rsa_key.p8"
```

### Test Connection

```bash
snow connection test -c default
snow sql -q "SELECT CURRENT_USER(), CURRENT_ACCOUNT()"
```

## When to Use This Skill

**Use when:**
- Building applications on Snowflake platform
- Using Cortex AI functions in SQL queries
- Developing Native Apps for Marketplace
- Setting up JWT key-pair authentication
- Working with Snowpark Python

**Don't use when:**
- Building Streamlit apps (use `streamlit-snowflake` skill)
- Need data engineering/ETL patterns
- Working with BI tools (Tableau, Looker)

## Cortex AI Functions

Snowflake Cortex provides LLM capabilities directly in SQL. Functions are in the `SNOWFLAKE.CORTEX` schema.

### Core Functions

| Function | Purpose | GA Status |
|----------|---------|-----------|
| `COMPLETE` / `AI_COMPLETE` | Text generation from prompt | GA Nov 2025 |
| `SUMMARIZE` / `AI_SUMMARIZE` | Summarize text | GA |
| `TRANSLATE` / `AI_TRANSLATE` | Translate between languages | GA Sep 2025 |
| `SENTIMENT` / `AI_SENTIMENT` | Sentiment analysis | GA Jul 2025 |
| `AI_FILTER` | Natural language filtering | GA Nov 2025 |
| `AI_CLASSIFY` | Categorize text/images | GA Nov 2025 |
| `AI_AGG` | Aggregate insights across rows | GA Nov 2025 |

### COMPLETE Function

```sql
-- Simple prompt
SELECT SNOWFLAKE.CORTEX.COMPLETE(
    'llama3.1-70b',
    'Explain quantum computing in one sentence'
) AS response;

-- With conversation history
SELECT SNOWFLAKE.CORTEX.COMPLETE(
    'llama3.1-70b',
    [
        {'role': 'system', 'content': 'You are a helpful assistant'},
        {'role': 'user', 'content': 'What is Snowflake?'}
    ]
) AS response;

-- With options
SELECT SNOWFLAKE.CORTEX.COMPLETE(
    'mistral-large2',
    'Summarize this document',
    {'temperature': 0.3, 'max_tokens': 500}
) AS response;
```

**Available Models:**
- `llama3.1-70b`, `llama3.1-8b`, `llama3.2-3b`
- `mistral-large2`, `mistral-7b`
- `snowflake-arctic`
- `gemma-7b`
- `claude-3-5-sonnet` (200K context)

**Model Context Windows** (Updated 2025):

| Model | Context Window | Best For |
|-------|----------------|----------|
| Claude 3.5 Sonnet | 200,000 tokens | Large documents, long conversations |
| Llama3.1-70b | 128,000 tokens | Complex reasoning, medium documents |
| Llama3.1-8b | 8,000 tokens | Simple tasks, short text |
| Llama3.2-3b | 8,000 tokens | Fast inference, minimal text |
| Mistral-large2 | Variable | Check current docs |
| Snowflake Arctic | Variable | Check current docs |

**Token Math**: ~4 characters = 1 token. A 32,000 character document ≈ 8,000 tokens.

**Error**: `Input exceeds context window limit` → Use smaller model or chunk your input.

### SUMMARIZE Function

```sql
-- Single text
SELECT SNOWFLAKE.CORTEX.SUMMARIZE(article_text) AS summary
FROM articles
LIMIT 10;

-- Aggregate across rows (no context window limit)
SELECT AI_SUMMARIZE_AGG(review_text) AS all_reviews_summary
FROM product_reviews
WHERE product_id = 123;
```

### TRANSLATE Function

```sql
-- Translate to English (auto-detect source)
SELECT SNOWFLAKE.CORTEX.TRANSLATE(
    review_text,
    '',      -- Empty = auto-detect source language
    'en'     -- Target language
) AS translated
FROM international_reviews;

-- Explicit source language
SELECT AI_TRANSLATE(
    description,
    'es',    -- Source: Spanish
    'en'     -- Target: English
) AS translated
FROM spanish_products;
```

### AI_FILTER (Natural Language Filtering)

**Performance**: As of September 2025, AI_FILTER includes automatic optimization delivering 2-10x speedup and up to 60% token reduction for suitable queries.

```sql
-- Filter with plain English
SELECT * FROM customer_feedback
WHERE AI_FILTER(
    feedback_text,
    'mentions shipping problems or delivery delays'
);

-- Combine with SQL predicates for maximum optimization
-- Query planner applies standard filters FIRST, then AI on smaller dataset
SELECT * FROM support_tickets
WHERE created_date > '2025-01-01'  -- Standard filter applied first
  AND AI_FILTER(description, 'customer is angry or frustrated');
```

**Best Practice**: Always combine AI_FILTER with traditional SQL predicates (date ranges, categories, etc.) to reduce the dataset before AI processing. This maximizes the automatic optimization benefits.

**Throttling**: During peak usage, AI function requests may be throttled with retry-able errors. Implement exponential backoff for production applications (see Known Issue #10).

### AI_CLASSIFY

```sql
-- Categorize support tickets
SELECT
    ticket_id,
    AI_CLASSIFY(
        description,
        ['billing', 'technical', 'shipping', 'other']
    ) AS category
FROM support_tickets;
```

### Billing

Cortex AI functions bill based on tokens:
- ~4 characters = 1 token
- Both input AND output tokens are billed
- Rates vary by model (larger models cost more)

**Cost Management at Scale** (Community-sourced):

Real-world production case study showed a single AI_COMPLETE query processing 1.18 billion records cost nearly $5K in credits. Cost drivers to watch:

1. **Cross-region inference**: Models not available in your region incur additional data transfer costs
2. **Warehouse idle time**: Unused compute still bills, but aggressive auto-suspend adds resume overhead
3. **Large table joins**: Complex queries with AI functions multiply costs

```sql
-- This seemingly simple query can be expensive at scale
SELECT
    product_id,
    AI_COMPLETE('mistral-large2', 'Summarize: ' || review_text) as summary
FROM product_reviews  -- 1 billion rows
WHERE created_date > '2024-01-01';

-- Cost = (input tokens + output tokens) × row count × model rate
-- At scale, this adds up fast
```

**Best Practices**:
- Filter datasets BEFORE applying AI functions
- Right-size warehouses (don't over-provision)
- Monitor credit consumption with QUERY_HISTORY views
- Consider batch processing instead of row-by-row AI operations

**Source**: [The Hidden Cost of Snowflake Cortex AI](https://seemoredata.io/blog/snowflake-cortex-ai/) (Community blog with billing evidence)

## Authentication

### JWT Key-Pair Authentication

**Critical**: Snowflake uses TWO account identifier formats:

| Format | Example | Used For |
|--------|---------|----------|
| **Organization-Account** | `irjoewf-wq46213` | REST API URLs, connection config |
| **Account Locator** | `NZ90655` | JWT claims (`iss`, `sub`) |

**These are NOT interchangeable!**

#### Discover Your Account Locator

```sql
SELECT CURRENT_ACCOUNT();  -- Returns: NZ90655
```

#### Generate RSA Key Pair

```bash
# Generate private key (PKCS#8 format required)
openssl genrsa 2048 | openssl pkcs8 -topk8 -inform PEM -out ~/.snowflake/rsa_key.p8 -nocrypt

# Generate public key
openssl rsa -in ~/.snowflake/rsa_key.p8 -pubout -out ~/.snowflake/rsa_key.pub

# Get fingerprint for JWT claims
openssl rsa -in ~/.snowflake/rsa_key.p8 -pubout -outform DER | \
  openssl dgst -sha256 -binary | openssl enc -base64
```

#### Register Public Key with User

```sql
-- In Snowflake worksheet (requires ACCOUNTADMIN or SECURITYADMIN)
ALTER USER my_user SET RSA_PUBLIC_KEY='MIIBIjANBgkq...';
```

#### JWT Claim Format

```
iss: ACCOUNT_LOCATOR.USERNAME.SHA256:fingerprint
sub: ACCOUNT_LOCATOR.USERNAME
```

**Example:**
```
iss: NZ90655.JEZWEB.SHA256:jpZO6LvU2SpKd8tE61OGfas5ZXpfHloiJd7XHLPDEEA=
sub: NZ90655.JEZWEB
```

### SPCS Container Authentication (v4.2.0+)

**New in January 2026**: Connector automatically detects and uses SPCS service identifier tokens when running inside Snowpark Container Services.

```python
# No special configuration needed inside SPCS containers
import snowflake.connector

# Auto-detects SPCS_TOKEN environment variable
conn = snowflake.connector.connect()
```

This enables seamless authentication from containerized Snowpark services without explicit credentials.

**Source**: [Release v4.2.0](https://github.com/snowflakedb/snowflake-connector-python/releases/tag/v4.2.0)

## Snow CLI Commands

### Project Management

```bash
# Initialize project
snow init

# Execute SQL
snow sql -q "SELECT 1"
snow sql -f query.sql

# View logs
snow logs
```

### Native App Commands

```bash
# Development
snow app run              # Deploy and run locally
snow app deploy           # Upload to stage only
snow app teardown         # Remove app

# Versioning
snow app version create V1_0
snow app version list
snow app version drop V1_0

# Publishing
snow app publish --version V1_0 --patch 0

# Release Channels
snow app release-channel list
snow app release-channel add-version --channel ALPHA --version V1_0
snow app release-directive set default --version V1_0 --patch 0 --channel DEFAULT
```

### Streamlit Commands

```bash
snow streamlit deploy --replace
snow streamlit deploy --replace --open
```

### Stage Commands

```bash
snow stage list
snow stage copy @my_stage/file.txt ./local/
```

## Native App Development

### Project Structure

```
my_native_app/
├── snowflake.yml           # Project config
├── manifest.yml            # App manifest
├── setup_script.sql        # Installation script
├── app/
│   └── streamlit/
│       ├── environment.yml
│       └── streamlit_app.py
└── scripts/
    └── setup.sql
```

### snowflake.yml

```yaml
definition_version: 2

native_app:
  name: my_app
  package:
    name: my_app_pkg
    distribution: external    # For marketplace
  application:
    name: my_app
  source_stage: stage/dev
  artifacts:
    - src: manifest.yml
      dest: manifest.yml
    - src: setup_script.sql
      dest: setup_script.sql
    - src: app/streamlit/environment.yml
      dest: streamlit/environment.yml
    - src: app/streamlit/streamlit_app.py
      dest: streamlit/streamlit_app.py
  enable_release_channels: true  # For ALPHA/BETA channels
```

### manifest.yml

```yaml
manifest_version: 1

artifacts:
  setup_script: setup_script.sql
  default_streamlit: streamlit/streamlit_app.py

# Note: Do NOT include privileges section - Native Apps can't declare privileges
```

### External Access Integration

Native Apps calling external APIs need this setup:

```sql
-- 1. Create network rule (in a real database, NOT app package)
CREATE DATABASE IF NOT EXISTS MY_APP_UTILS;

CREATE OR REPLACE NETWORK RULE MY_APP_UTILS.PUBLIC.api_rule
  MODE = EGRESS
  TYPE = HOST_PORT
  VALUE_LIST = ('api.example.com:443');

-- 2. Create integration
CREATE OR REPLACE EXTERNAL ACCESS INTEGRATION my_app_integration
  ALLOWED_NETWORK_RULES = (MY_APP_UTILS.PUBLIC.api_rule)
  ENABLED = TRUE;

-- 3. Grant to app
GRANT USAGE ON INTEGRATION my_app_integration
  TO APPLICATION MY_APP;

-- 4. CRITICAL: Attach to Streamlit (must repeat after EVERY deploy!)
ALTER STREAMLIT MY_APP.config_schema.my_streamlit
  SET EXTERNAL_ACCESS_INTEGRATIONS = (my_app_integration);
```

**Warning**: Step 4 resets on every `snow app run`. Must re-run after each deploy!

### Shared Data Pattern

When your Native App needs data from an external database:

```sql
-- 1. Create shared_data schema in app package
CREATE SCHEMA IF NOT EXISTS MY_APP_PKG.SHARED_DATA;

-- 2. Create views referencing external database
CREATE OR REPLACE VIEW MY_APP_PKG.SHARED_DATA.MY_VIEW AS
SELECT * FROM EXTERNAL_DB.SCHEMA.TABLE;

-- 3. Grant REFERENCE_USAGE (CRITICAL!)
GRANT REFERENCE_USAGE ON DATABASE EXTERNAL_DB
  TO SHARE IN APPLICATION PACKAGE MY_APP_PKG;

-- 4. Grant access to share
GRANT USAGE ON SCHEMA MY_APP_PKG.SHARED_DATA
  TO SHARE IN APPLICATION PACKAGE MY_APP_PKG;
GRANT SELECT ON ALL VIEWS IN SCHEMA MY_APP_PKG.SHARED_DATA
  TO SHARE IN APPLICATION PACKAGE MY_APP_PKG;
```

In `setup_script.sql`, reference `shared_data.view_name` (NOT the original database).

## Marketplace Publishing

### Security Review Workflow

```bash
# 1. Deploy app
snow app run

# 2. Create version
snow app version create V1_0

# 3. Check security review status
snow app version list
# Wait for review_status = APPROVED

# 4. Set release directive
snow app release-directive set default --version V1_0 --patch 0 --channel DEFAULT

# 5. Create listing in Snowsight Provider Studio (UI only)
```

### Security Review Statuses

| Status | Meaning | Action |
|--------|---------|--------|
| `NOT_REVIEWED` | Scan hasn't run | Check DISTRIBUTION is EXTERNAL |
| `IN_PROGRESS` | Scan running | Wait |
| `APPROVED` | Passed | Can publish |
| `REJECTED` | Failed | Fix issues or appeal |
| `MANUAL_REVIEW` | Human reviewing | Wait (can take days) |

**Triggers manual review**: External access integrations, Streamlit components, network calls.

### Provider Studio Fields

| Field | Max Length | Notes |
|-------|------------|-------|
| Title | 72 chars | App name |
| Subtitle | 128 chars | One-liner |
| Description | 10,000 chars | HTML editor |
| Business Needs | 6 max | Select from dropdown |
| Quick Start Examples | 10 max | Title + Description + SQL |
| Data Dictionary | Required | **Mandatory for data listings (2025)** |

### Paid Listing Prerequisites

| # | Requirement |
|---|-------------|
| 1 | Full Snowflake account (not trial) |
| 2 | ACCOUNTADMIN role |
| 3 | Provider Profile approved |
| 4 | Stripe account configured |
| 5 | Provider & Consumer Terms accepted |
| 6 | Contact Marketplace Ops |

**Note**: Cannot convert free listing to paid. Must create new listing.

## Snowpark Python

### Session Setup

```python
from snowflake.snowpark import Session

connection_params = {
    "account": "orgname-accountname",
    "user": "USERNAME",
    "password": "PASSWORD",  # Or use private_key_path
    "warehouse": "COMPUTE_WH",
    "database": "MY_DB",
    "schema": "PUBLIC"
}

session = Session.builder.configs(connection_params).create()
```

### DataFrame Operations

```python
# Read table
df = session.table("MY_TABLE")

# Filter and select
result = df.filter(df["STATUS"] == "ACTIVE") \
           .select("ID", "NAME", "CREATED_AT") \
           .sort("CREATED_AT", ascending=False)

# Execute
result.show()

# Collect to Python
rows = result.collect()
```

### Row Access (Common Gotcha)

```python
# WRONG - dict() doesn't work on Snowpark Row
config = dict(result[0])

# CORRECT - Access columns explicitly
row = result[0]
config = {
    'COLUMN_A': row['COLUMN_A'],
    'COLUMN_B': row['COLUMN_B'],
}
```

### DML Statistics (v4.2.0+)

**New in January 2026**: `SnowflakeCursor.stats` property exposes granular DML statistics for operations where `rowcount` is insufficient (e.g., CTAS queries).

```python
# Before v4.2.0 - rowcount returns -1 for CTAS
cursor.execute("CREATE TABLE new_table AS SELECT * FROM source WHERE active = true")
print(cursor.rowcount)  # Returns -1 (not helpful!)

# After v4.2.0 - stats property shows actual row counts
cursor.execute("CREATE TABLE new_table AS SELECT * FROM source WHERE active = true")
print(cursor.stats)  # Returns {'rows_inserted': 1234, 'duplicates': 0, ...}
```

**Source**: [Release v4.2.0](https://github.com/snowflakedb/snowflake-connector-python/releases/tag/v4.2.0)

### UDFs and Stored Procedures

```python
from snowflake.snowpark.functions import udf, sproc

# Register UDF
@udf(name="my_udf", replace=True)
def my_udf(x: int) -> int:
    return x * 2

# Register Stored Procedure
@sproc(name="my_sproc", replace=True)
def my_sproc(session: Session, table_name: str) -> str:
    df = session.table(table_name)
    count = df.count()
    return f"Row count: {count}"
```

## REST API (SQL API v2)

The REST API is the foundation for programmatic Snowflake access from Cloudflare Workers.

### Endpoint

```
https://{org-account}.snowflakecomputing.com/api/v2/statements
```

### Required Headers (CRITICAL)

**ALL requests** must include these headers - missing `Accept` causes silent failures:

```typescript
const headers = {
  'Authorization': `Bearer ${jwt}`,
  'Content-Type': 'application/json',
  'Accept': 'application/json',  // REQUIRED - "null" error if missing
  'User-Agent': 'MyApp/1.0',
};
```

### Async Query Handling

Even simple queries return async (HTTP 202). Always implement polling:

```typescript
// Submit returns statementHandle, not results
const submit = await fetch(url, { method: 'POST', headers, body });
const { statementHandle } = await submit.json();

// Poll until complete
while (true) {
  const status = await fetch(`${url}/${statementHandle}`, { headers });
  if (status.status === 200) break;  // Complete
  if (status.status === 202) {
    await sleep(2000);  // Still running
    continue;
  }
}
```

### Workers Subrequest Limits

| Plan | Limit | Safe Polling |
|------|-------|--------------|
| Free | 50 | 45 attempts @ 2s = 90s max |
| Paid | 1,000 | 100 attempts @ 500ms = 50s max |

### Fetch Timeouts

Workers `fetch()` has **no default timeout**. Always use AbortController:

```typescript
const response = await fetch(url, {
  signal: AbortSignal.timeout(30000),  // 30 seconds
  headers,
});
```

### Cancel on Timeout

Cancel queries when timeout occurs to avoid warehouse costs:

```
POST /api/v2/statements/{statementHandle}/cancel
```

See `templates/snowflake-rest-client.ts` for complete implementation.

## Known Issues

### 1. Account Identifier Confusion

**Symptom**: JWT auth fails silently, queries don't appear in Query History.

**Cause**: Using org-account format in JWT claims instead of account locator.

**Fix**: Use `SELECT CURRENT_ACCOUNT()` to get the actual account locator.

### 2. External Access Reset

**Symptom**: API calls fail after `snow app run`.

**Cause**: External access integration attachment resets on every deploy.

**Fix**: Re-run `ALTER STREAMLIT ... SET EXTERNAL_ACCESS_INTEGRATIONS` after each deploy.

### 3. Release Channel Syntax

**Symptom**: `ALTER APPLICATION PACKAGE ... SET DEFAULT RELEASE DIRECTIVE` fails.

**Cause**: Legacy SQL syntax doesn't work with release channels enabled.

**Fix**: Use snow CLI: `snow app release-directive set default --version V1_0 --patch 0 --channel DEFAULT`

### 4. Artifact Nesting

**Symptom**: Files appear in `streamlit/streamlit/` instead of `streamlit/`.

**Cause**: Directory mappings in snowflake.yml nest the folder name.

**Fix**: List individual files explicitly in artifacts, not directories.

### 5. REFERENCE_USAGE Missing

**Symptom**: "A view that is added to the shared content cannot reference objects from other databases"

**Cause**: Missing `GRANT REFERENCE_USAGE ON DATABASE` for shared data.

**Fix**: Always grant REFERENCE_USAGE before `snow app run` when using external databases.

### 6. REST API Missing Accept Header

**Symptom**: "Unsupported Accept header null is specified" on polling requests.

**Cause**: Initial request had `Accept: application/json` but polling request didn't.

**Fix**: Use consistent headers helper function for ALL requests (submit, poll, cancel).

### 7. Workers Fetch Hangs Forever

**Symptom**: Worker hangs indefinitely waiting for Snowflake response.

**Cause**: Cloudflare Workers' `fetch()` has no default timeout.

**Fix**: Always use `AbortSignal.timeout(30000)` on all Snowflake requests.

### 8. Too Many Subrequests

**Symptom**: "Too many subrequests" error during polling.

**Cause**: Polling every 1 second × 600 attempts = 600 subrequests exceeds limits.

**Fix**: Poll every 2-5 seconds, limit to 45 (free) or 100 (paid) attempts.

### 9. Warehouse Not Auto-Resuming (Perceived)

**Symptom**: Queries return statementHandle but never complete (code 090001 indefinitely).

**Cause**: `090001` means "running" not error. Warehouse IS resuming, just takes time.

**Fix**: Auto-resume works. Wait longer or explicitly resume first: `POST /api/v2/warehouses/{wh}:resume`

### 10. Memory Leaks in Connector 4.x (Active Issue)

**Error**: Long-running Python applications show memory growth over time
**Source**: [GitHub Issue #2727](https://github.com/snowflakedb/snowflake-connector-python/issues/2727), [#2725](https://github.com/snowflakedb/snowflake-connector-python/issues/2725)
**Affects**: snowflake-connector-python 4.0.0 - 4.2.0

**Why It Happens**:
- `SessionManager` uses `defaultdict` which prevents garbage collection
- `SnowflakeRestful.fetch()` holds references that leak during query execution

**Prevention**:
Reuse connections rather than creating new ones repeatedly. Fix is in progress via [PR #2741](https://github.com/snowflakedb/snowflake-connector-python/pull/2741) and [PR #2726](https://github.com/snowflakedb/snowflake-connector-python/pull/2726).

```python
# AVOID - creates new connection each iteration
for i in range(1000):
    conn = snowflake.connector.connect(...)
    cursor = conn.cursor()
    cursor.execute("SELECT 1")
    cursor.close()
    conn.close()

# BETTER - reuse connection
conn = snowflake.connector.connect(...)
cursor = conn.cursor()
for i in range(1000):
    cursor.execute("SELECT 1")
cursor.close()
conn.close()
```

**Status**: Fix expected in connector v4.3.0 or later

### 11. AI Function Throttling During Peak Usage

**Error**: "Request throttled due to high usage. Please retry."
**Source**: [Snowflake Cortex Documentation](https://docs.snowflake.com/en/user-guide/snowflake-cortex/aisql)
**Affects**: All Cortex AI functions (COMPLETE, FILTER, CLASSIFY, etc.)

**Why It Happens**:
AI/LLM requests may be throttled during high usage periods to manage platform capacity. Throttled requests return errors and require manual retries.

**Prevention**:
Implement retry logic with exponential backoff:

```python
import time
import snowflake.connector

def execute_with_retry(cursor, query, max_retries=3):
    for attempt in range(max_retries):
        try:
            return cursor.execute(query).fetchall()
        except snowflake.connector.errors.DatabaseError as e:
            if "throttled" in str(e).lower() and attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff
                time.sleep(wait_time)
            else:
                raise
```

**Status**: Documented behavior, no fix planned

## References

- [Snowflake CLI Documentation](https://docs.snowflake.com/en/developer-guide/snowflake-cli/index)
- [SQL REST API Reference](https://docs.snowflake.com/en/developer-guide/sql-api/reference)
- [SQL API Authentication](https://docs.snowflake.com/en/developer-guide/sql-api/authenticating)
- [Cortex AI Functions](https://docs.snowflake.com/en/user-guide/snowflake-cortex/llm-functions)
- [Native Apps Framework](https://docs.snowflake.com/en/developer-guide/native-apps/native-apps-about)
- [Snowpark Python](https://docs.snowflake.com/en/developer-guide/snowpark/python/index)
- [Marketplace Publishing](https://docs.snowflake.com/en/developer-guide/native-apps/publish-app)

## Related Skills

- `streamlit-snowflake` - Streamlit in Snowflake apps
