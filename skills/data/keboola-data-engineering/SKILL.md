---
name: keboola-data-engineering
description: 'Expert assistant for Keboola data platform. Builds working data pipelines,
  not just advice. Use for: data extraction, transformation, validation, orchestration,
  dashboard creation.'
---

---
name: keboola-data-engineering
description: Expert assistant for Keboola data platform. Builds working data pipelines, not just advice. Use for: data extraction, transformation, validation, orchestration, dashboard creation.
---

# Keboola Data Engineering Skill v4.1

## Quick Start (Copy-Paste Workflow)

**Build a pipeline in 4 steps:**
```yaml
1. Understand: Ask outcome questions → Save context → Track with todos
2. Discover: List data sources → Use agents for complex searches → Map to extractors
3. Propose: Show architecture + diagram → Get explicit approval
4. Build: Generate configs → Test in sandbox → Validate impact → Deploy → Monitor
```

**Tool Pattern**: `Read KNOWLEDGE_MAP → Read component docs → Write config → Bash deploy`

---

## Tool Reference Card

| Task | Tool | Command Pattern |
|------|------|-----------------|
| **Find component** | Read | `Read resources/KNOWLEDGE_MAP.md`, search for name |
| **Complex search** | Task | `Task(subagent_type=Explore, prompt=...)` for multi-file searches |
| **Search docs** | Grep | `Grep pattern in docs-repos/` |
| **Get template** | Read | `Read resources/templates/{name}.md` |
| **Save config** | Write | `Write {name}.json with content` |
| **Save context** | Write | `Write project_context.json` - persist requirements |
| **Track progress** | TodoWrite | Track requirements, validations, decisions |
| **Deploy config** | Bash | `curl -X POST {api_url} -d @{file}` |
| **Test pipeline** | Bash | `curl {queue_api} -d {job_params}` |
| **Check MCP** | - | If `mcp__keboola_*` tools exist, use them |

---

## Core Workflow

### Step 1: Understand Business Problem (5 questions)

**Ask these, nothing more until answered:**
1. "What decision does this enable? Who makes it?"
2. "What's the ONE metric that matters most?"
3. "How often is this needed? (Real-time/Hourly/Daily/Weekly)"
4. "Does data contain PII? (Names/Emails/SSNs/Financial data)"
5. "What does success look like in 30 days?"

**Output**: `{Decision: "X", Metric: "Y", Frequency: "Z", PII: Yes/No, Success: "..."}`

**⭐ NEW: Persist Context** (Feature 1: File-based state tracking)

**Use Write tool** to save `project_context.json`:
```json
{
  "decision": "{what decision this enables}",
  "decision_maker": "{who makes the decision}",
  "metric": "{the ONE key metric}",
  "frequency": "{Real-time/Hourly/Daily/Weekly}",
  "pii": true/false,
  "success_criteria": "{what success looks like in 30 days}",
  "timestamp": "{ISO 8601 timestamp}"
}
```

**⭐ NEW: Track Context with Todos** (Feature 2: TodoWrite context tracking)

**Use TodoWrite tool** to track business requirements:
```json
{
  "todos": [
    {"content": "Business context captured: {metric}, {frequency}, PII={yes/no}", "status": "completed", "activeForm": "Capturing business context"},
    {"content": "Validate architecture includes PII handling (required)", "status": "pending", "activeForm": "Validating PII requirements"},
    {"content": "Ensure {frequency} schedule is implemented", "status": "pending", "activeForm": "Implementing schedule"}
  ]
}
```

**Use Read tool** on `resources/templates/Discovery_Prompt.txt` for 15 more optional questions.

---

### Step 2: Discover Data Sources

**If MCP available**: Call `mcp__keboola_storage_api(endpoint="/buckets")` to list existing data

**If MCP unavailable**: Ask "What systems do you use?" then:

**⭐ NEW: Complex Discovery with Agents** (Feature 5: Multi-agent delegation)

For complex searches (e.g., "Find all extractors for CRM systems"):
```yaml
Use Task tool:
  subagent_type: Explore
  thoroughness: medium
  prompt: |
    Find Keboola components for: {user's data sources}

    Search:
    - resources/KNOWLEDGE_MAP.md for component IDs
    - docs-repos/connection-docs/components/extractors/ for configs

    Return structured list:
    - Component ID (e.g., keboola.ex-salesforce)
    - Doc path
    - Common config patterns (incremental, primaryKey)
    - Typical use cases
```

For simple lookups:
1. **Use Read tool** on `resources/KNOWLEDGE_MAP.md`
2. **Use Grep tool** to search for system name (e.g., "Salesforce", "MySQL")
3. Note component ID and doc path

**Data Inventory Template**:
```json
{
  "have": [
    {"system": "Salesforce", "component": "keboola.ex-salesforce", "tables": ["Opportunity", "Account"]},
    {"system": "MySQL", "component": "keboola.ex-db-mysql", "tables": ["orders", "customers"]}
  ],
  "need": [
    {"system": "Stripe", "status": "user will provide API key"},
    {"system": "Product events", "status": "missing - defer to Phase 2"}
  ]
}
```

**Use Write tool** to save inventory as `data_inventory.json`

---

### Step 3: Propose Architecture & Get Approval

**⚠️ CONTEXT-AWARE DESIGN** (Feature 1: Read saved context)

**Use Read tool** on `project_context.json` to retrieve requirements, then check:
```yaml
IF pii = true:
  MUST include:
    - PII field identification
    - Masking/hashing/removal strategy
    - Access control notes

IF frequency = "Real-time":
  MUST use:
    - CDC extractors (not batch)
    - Stream processing pattern

IF metric contains revenue/financial/cost:
  MUST include:
    - Impact simulation (current state vs projected)
    - Rollback plan
```

**Use Read tool** on `resources/templates/Design_Brief.md`, then create:

```markdown
## {Problem} Solution

**Outcome**: {What user will get}
**Frequency**: {Daily at 6am}
**Data Sources**: {List from Step 2}

**Pipeline**:
{Source 1} --[Extractor]--> in.c-{source}.{table}
{Source 2} --[Extractor]--> in.c-{source}.{table}
    ↓
[SQL Transform + Validation]
    ↓
out.c-{purpose}.{table}
    ↓
[Dashboard/Writer]

**Data Quality**:
- Freshness: < {X} hours
- Completeness: No NULLs in {key_fields}
- Validation: {What checks will run}

**PII Handling** (if applicable):
- {field}: Masked/Hashed/Removed

**Impact** (if metric-driven):
- Current state: {baseline}
- Projected: {expected change}
- Risk: {potential issues}
```

**⭐ NEW: Visual Architecture Diagram** (Feature 7: Visual diagrams)

Generate mermaid diagram for visual representation:
```mermaid
graph LR
    A[{Source 1}] -->|{Extractor}| B[in.c-{source}.{table}]
    C[{Source 2}] -->|{Extractor}| D[in.c-{source}.{table}]

    B --> E[SQL Transform]
    D --> E

    E --> F[out.c-{purpose}.{table}]

    F --> G[{Writer/Dashboard}]

    style E fill:#f9f,stroke:#333,stroke-width:4px
    style F fill:#bbf,stroke:#333,stroke-width:2px
```

**⚠️ STOP**: Ask "Should I proceed with building this?"
- If NO: Iterate on Step 3
- If YES: Continue to Step 4

**Use Write tool** to save as `architecture_proposal.md`

**Use TodoWrite** to update:
```json
{"content": "Architecture proposal approved by user", "status": "completed", "activeForm": "Getting architecture approval"}
```

---

### Step 4: Build It

#### A. Component Configs

**Pattern**: Find docs → Generate config → Deploy via API

**Example: Salesforce Extractor**

1. **Use Read tool** on path from KNOWLEDGE_MAP (e.g., `docs-repos/connection-docs/components/extractors/marketing-sales/salesforce/index.md`)

2. **Use Write tool** to create `salesforce_config.json`:
```json
{
  "parameters": {
    "objects": [
      {
        "name": "Opportunity",
        "soql": "SELECT Id, Amount, StageName, CloseDate FROM Opportunity WHERE LastModifiedDate >= LAST_N_DAYS:7",
        "output": "in.c-salesforce.opportunities"
      }
    ]
  }
}
```

3. **Use Bash tool** to deploy:
```bash
curl -X POST "https://connection.keboola.com/v2/storage/components/keboola.ex-salesforce/configs" \
  -H "X-StorageApi-Token: $KEBOOLA_API_TOKEN" \
  --form 'name="Salesforce Opportunities"' \
  --form "configuration=@salesforce_config.json" \
  | tee response.json

CONFIG_ID=$(jq -r '.id' response.json)
echo "Extractor config ID: $CONFIG_ID"
```

**Repeat for each data source** from Step 2 inventory.

#### B. SQL Transformations (Validation MANDATORY)

**Pattern**: Business logic + Validation + Abort if fail

**⭐ NEW: Agent-Assisted SQL Generation** (Feature 5: Multi-agent delegation)

For complex transformations (joins, calculations, ML features):
```yaml
Use Task tool:
  subagent_type: general-purpose
  prompt: |
    Generate Snowflake SQL transformation for: {business requirement}

    Context from project_context.json:
    - Metric: {metric from context}
    - PII: {yes/no from context}
    - Frequency: {frequency from context}

    Apply DA/DE concepts:
    - Use Read tool on resources/Keboola_Data_Enablement_Guide.md
    - Apply relevant patterns (aggregation, window functions, etc.)

    MUST include:
    1. Business logic SQL (CREATE TABLE with calculations)
    2. PII handling (if PII=true): mask/hash/remove sensitive fields
    3. Validation SQL (freshness, volume, schema, completeness)
    4. SET ABORT_TRANSFORMATION pattern (fail fast on issues)
    5. Comments explaining DA/DE concepts applied

    Return: Complete SQL ready to test in sandbox
```

For simple transformations, manually write:

**Use Write tool** to create `transform.sql`:
```sql
-- 1. Business Logic
CREATE OR REPLACE TABLE "out.c-analytics.{output_table}" AS
SELECT
  {columns},
  {calculated_fields}
FROM "in.c-{source}.{table}"
{joins}
{where_clauses};

-- 2. Validation (REQUIRED - DO NOT SKIP)
CREATE OR REPLACE TABLE "_validation" AS
SELECT
  COUNT(*) as row_count,
  COUNT(DISTINCT {primary_key}) as unique_keys,
  COUNT(*) - COUNT({critical_field}) as null_count,
  DATEDIFF('hour', MAX({timestamp_field}), CURRENT_TIMESTAMP) as hours_old,
  CASE
    WHEN COUNT(*) = 0 THEN 'FAIL: No data'
    WHEN null_count > 0 THEN 'FAIL: NULLs in {critical_field}'
    WHEN hours_old > {max_hours} THEN 'FAIL: Data too old'
    WHEN row_count != unique_keys THEN 'FAIL: Duplicate keys'
    ELSE 'PASS'
  END as status
FROM "out.c-analytics.{output_table}";

-- 3. Abort if validation fails
SET ABORT_TRANSFORMATION = (
  SELECT CASE WHEN status != 'PASS' THEN status ELSE '' END FROM "_validation"
);
```

**⭐ NEW: Sandbox Testing** (Feature 4: Sandbox testing)

Before deploying to production:
```bash
# 1. Create temporary workspace for testing
curl -X POST "https://connection.keboola.com/v2/storage/workspaces" \
  -H "X-StorageApi-Token: $KEBOOLA_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"backend":"snowflake"}' \
  | tee workspace.json

WORKSPACE_ID=$(jq -r '.id' workspace.json)

# 2. Load sample data (last 7 days or 1000 rows)
curl -X POST "https://connection.keboola.com/v2/storage/workspaces/$WORKSPACE_ID/load" \
  -H "X-StorageApi-Token: $KEBOOLA_API_TOKEN" \
  -d "input=in.c-{source}.{table}&days=7"

# 3. Run SQL in workspace
# (Use workspace credentials from workspace.json to connect and test SQL)

# 4. Verify results
echo "Check: Did SQL complete without errors?"
echo "Check: Are output tables created?"
echo "Check: Do row counts make sense?"

# 5. If tests pass, continue to deployment
# 6. Cleanup workspace after testing
curl -X DELETE "https://connection.keboola.com/v2/storage/workspaces/$WORKSPACE_ID" \
  -H "X-StorageApi-Token: $KEBOOLA_API_TOKEN"
```

**Use Bash tool** to deploy:
```bash
curl -X POST "https://connection.keboola.com/v2/storage/components/keboola.snowflake-transformation/configs" \
  -H "X-StorageApi-Token: $KEBOOLA_API_TOKEN" \
  --form 'name="{Transform Name}"' \
  --form "configuration={\"queries\": [\"$(cat transform.sql)\"]}" \
  | tee transform_response.json

TRANSFORM_ID=$(jq -r '.id' transform_response.json)
```

**Use Read tool** on `resources/patterns/validation-patterns.md` for 10+ validation examples.

#### C. Orchestrate with Flow

**Flows are UI-based**. **Use Write tool** to create `flow_instructions.md`:

```markdown
# Create Flow in Keboola UI:

1. Go to Flows → Create Flow
2. Name: "{Pipeline Name}"
3. Add components:
   - Step 1 (parallel):
     • Extractor 1 (config: {CONFIG_ID_1})
     • Extractor 2 (config: {CONFIG_ID_2})
   - Step 2: Transformation (config: {TRANSFORM_ID})
   - Step 3: Writer/App (if applicable)
4. Schedule: {cronTab expression}
5. Save and note Flow Config ID

Then schedule via API:
```

**Use Bash tool** after user creates Flow:
```bash
# Create schedule
SCHEDULE=$(curl -X POST "https://connection.keboola.com/v2/storage/components/keboola.scheduler/configs/" \
  -H "X-StorageApi-Token: $KEBOOLA_API_TOKEN" \
  --form 'name="{Pipeline} Schedule"' \
  --form "configuration={\"schedule\":{\"cronTab\":\"{cron}\",\"timezone\":\"UTC\",\"state\":\"enabled\"},\"target\":{\"componentId\":\"keboola.orchestrator\",\"configurationId\":\"{FLOW_ID}\",\"mode\":\"run\"}}" \
  | jq -r '.id')

# Activate (requires Master Token with scheduler permissions)
curl -X POST "https://scheduler.keboola.com/schedules" \
  -H "X-StorageApi-Token: $MASTER_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"configurationId\": \"$SCHEDULE\"}"
```

#### D. Test Pipeline

**Use Bash tool** to run and verify:
```bash
# Queue job
JOB=$(curl -X POST "https://queue.keboola.com/jobs" \
  -H "X-StorageApi-Token: $KEBOOLA_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"mode\":\"run\",\"component\":\"keboola.orchestrator\",\"config\":\"{FLOW_ID}\"}" \
  | jq -r '.id')

echo "Job ID: $JOB"
echo "Monitor: https://connection.keboola.com/admin/projects/{PROJECT_ID}/jobs/$JOB"

# Wait for job to complete (poll every 10 seconds)
for i in {1..30}; do
  STATUS=$(curl -s "https://queue.keboola.com/jobs/$JOB" \
    -H "X-StorageApi-Token: $KEBOOLA_API_TOKEN" \
    | jq -r '.status')

  if [ "$STATUS" = "success" ]; then
    echo "✅ Job completed successfully"
    break
  elif [ "$STATUS" = "error" ]; then
    echo "❌ Job failed"
    break
  else
    echo "⏳ Status: $STATUS... (${i}/30)"
    sleep 10
  fi
done
```

**⭐ NEW: Error Recovery** (Feature 6: Error recovery workflows)

If job fails:
```yaml
1. Get error message:
   curl "https://queue.keboola.com/jobs/$JOB" | jq '.result.message'

2. Use decision tree to diagnose:
   - "No data" → Check extractor ran successfully, verify source connectivity
   - "Validation failed" → Check _validation table, review thresholds
   - "SQL error" → Review syntax, test in workspace
   - "Timeout" → Optimize query (add indexes, reduce date range)
   - "Permission denied" → Check API token permissions

3. For complex issues, spawn troubleshooting agent:
   Use Task tool:
     subagent_type: general-purpose
     prompt: |
       Debug Keboola pipeline failure

       Error message: {error from job logs}
       Component: {component_id}

       Steps:
       1. Use Read tool on resources/runbooks/common_issues.md
       2. Search docs-repos/ for error message using Grep
       3. Provide:
          - Root cause diagnosis
          - Fix (SQL change, config change, or API call)
          - Prevention (validation to add, monitoring to set up)

       Return structured fix with code

4. Apply fix and re-test
```

**Preview output** (first 10 rows):
```bash
curl "https://connection.keboola.com/v2/storage/tables/out.c-analytics.{table}/data-preview" \
  -H "X-StorageApi-Token: $KEBOOLA_API_TOKEN" \
  | head -10
```

---

### ⭐ NEW: Step 4.5 - Validate Business Impact (Feature 3: Business validation)

**Before marking complete, validate the solution meets business requirements.**

**Use Read tool** on `project_context.json` to retrieve original goals.

#### Validation Checklist

```yaml
1. Data Quality Verification:
   - Use Bash: Query _validation table
   - Confirm: "status = 'PASS'"
   - Check: Freshness, completeness, volume meet thresholds

2. Business Impact Analysis (for metric-driven projects):
   IF metric relates to revenue/cost/conversions:
     - Generate impact simulation:
       • Query baseline (current state)
       • Query projection (with new data/model)
       • Calculate % change
       • Identify affected entities (customers, SKUs, etc.)

     Example SQL:
     SELECT
       'Current' as scenario,
       SUM({metric}) as total,
       COUNT(DISTINCT {entity}) as entities_affected
     FROM {baseline_table}
     UNION ALL
     SELECT
       'Projected' as scenario,
       SUM({metric}) as total,
       COUNT(DISTINCT {entity}) as entities_affected
     FROM {new_output_table};

3. Risk Assessment:
   - Low sample size warning: entities with < 30 data points
   - High impact changes: > 20% change in key metrics
   - Data quality issues: validation warnings (not failures)

4. Rollback Plan Documentation:
   Use Write tool to create rollback_plan.md:

   ## Rollback Plan

   **If {metric} drops > {threshold}% in first week:**

   1. Revert to previous config:
      curl -X POST "https://connection.keboola.com/v2/storage/components/{component}/configs/{id}/versions/{version}/rollback"

   2. Disable schedule:
      curl -X DELETE "https://scheduler.keboola.com/schedules/{schedule_id}"

   3. Alert stakeholders:
      - {decision_maker from context}
      - Data team lead

   **Monitoring:**
   - Check {metric} daily for first week
   - Alert if validation fails 2+ times
   - Review impact after 30 days (success criteria: {from context})
```

#### Approval Gate (Feature 3: Structured approval)

Show simulation/validation results, then ask:

```
📊 VALIDATION RESULTS:
- Data quality: {PASS/WARN}
- Impact simulation: {metric} expected to change by {X%}
- Entities affected: {count}
- Risks identified: {list}

Review rollback_plan.md for contingency.

Reply with one of:
1. "deploy" - Deploy to production with {frequency} schedule
2. "test" - Run as one-off test first, review results before scheduling
3. "revise" - Adjust parameters (specify what to change)
```

**Use TodoWrite** to track:
```json
{"content": "Business impact validated and approved", "status": "completed", "activeForm": "Validating business impact"}
```

---

#### E. Document Deliverables

**Use Write tool** to create `DELIVERABLES.md`:

```markdown
## Delivered: {Pipeline Name}

### Components Created:
| Component | ID | Purpose |
|-----------|----|----|
| {Extractor 1} | {ID} | Extract {data} |
| {Transformation} | {ID} | Calculate {metric} |
| {Flow} | {ID} | Orchestrate {frequency} run |

### Output Data:
- **Table**: out.c-analytics.{table}
- **Rows**: {count}
- **Freshness**: {hours} hours old
- **Sample**: {show first 5 rows}

### Data Quality Results:
✅ Validation: PASS
✅ Freshness: {X} hours (target: < {Y})
✅ Completeness: 0 NULLs in critical fields
✅ Uniqueness: No duplicates

### Business Impact:
- **Metric**: {metric from context}
- **Current**: {baseline value}
- **Projected**: {expected value}
- **Change**: {%}

### Schedule:
- Runs: {frequency} at {time}
- Next run: {timestamp}

### Access:
- Keboola UI: {project_url}/flows/{flow_id}
- Table: {project_url}/storage/tables/out.c-analytics.{table}

### Rollback:
- See rollback_plan.md for contingency procedures
- Monitor {metric} for first 30 days
- Success criteria: {from context}
```

---

## Decision Trees (Structured)

### Choosing Extractor Type
```yaml
question: "What's your data source?"
answers:
  - condition: "Database (MySQL, PostgreSQL, Snowflake, etc.)"
    component_pattern: "keboola.ex-db-{database}"
    path: "docs-repos/connection-docs/components/extractors/database/"

  - condition: "SaaS API (Salesforce, Stripe, GA, etc.)"
    component_pattern: "keboola.ex-{service}"
    path: "docs-repos/connection-docs/components/extractors/marketing-sales/"

  - condition: "Custom REST API"
    component: "keboola.ex-generic-v2"
    path: "docs-repos/developers-docs/extend/generic-extractor/"

  - condition: "File upload (CSV, JSON)"
    component: "keboola.ex-storage"
    path: "docs-repos/connection-docs/components/extractors/storage/"
```

### Validation Strategy
```yaml
question: "What data quality checks are needed?"
checks:
  freshness:
    when: "Time-sensitive data (orders, events, etc.)"
    sql: "DATEDIFF('hour', MAX(timestamp_col), CURRENT_TIMESTAMP) < {max_hours}"

  completeness:
    when: "Critical fields must exist"
    sql: "COUNT(*) = COUNT({critical_field})"

  uniqueness:
    when: "Primary key must be unique"
    sql: "COUNT(*) = COUNT(DISTINCT {primary_key})"

  volume:
    when: "Expecting consistent row counts"
    sql: "COUNT(*) BETWEEN {min} AND {max}"

  distribution:
    when: "Detecting anomalies in metrics"
    sql: "AVG({metric}) BETWEEN {historical_avg - 3*stddev} AND {historical_avg + 3*stddev}"
```

### Bucket Naming
```yaml
question: "How to name buckets?"
guidance: "Match existing project conventions. Common patterns:"
patterns:
  source_based:
    input: "in.c-{source}.{table}"
    output: "out.c-{purpose}.{table}"
    example: "in.c-salesforce.opportunities → out.c-analytics.revenue"

  layer_based:
    raw: "in.c-bronze.{source}_{table}"
    cleaned: "out.c-silver.{domain}_{entity}"
    analytics: "out.c-gold.{business_metric}"
    example: "bronze.salesforce_opp → silver.sales_pipeline → gold.revenue_daily"

  advice: "Use Read tool on existing project buckets to match convention"
```

---

## Pattern Library

### Pattern 1: CDC to Analytics
```yaml
name: "Change Data Capture to Analytics Dashboard"
use_case: "Real-time operational data → Business metrics"
components:
  - {type: "CDC Extractor", examples: ["MySQL CDC", "PostgreSQL CDC"]}
  - {type: "Stream Transform", tool: "Snowflake transformation"}
  - {type: "Aggregation", sql: "Windowed aggregates"}
  - {type: "Dashboard", tool: "Streamlit/Tableau"}
frequency: "Continuous (5-15min latency)"
template: "Use Read tool on resources/flows/examples/flow_cdc_orders.md"
```

### Pattern 2: Batch ETL
```yaml
name: "Daily Batch Extract-Transform-Load"
use_case: "Nightly data warehouse refresh"
components:
  - {type: "Batch Extractor", schedule: "Daily 2am"}
  - {type: "SQL Transform", layers: ["bronze", "silver", "gold"]}
  - {type: "Data Warehouse Writer", targets: ["Snowflake", "BigQuery"]}
frequency: "Daily"
template: "Use Read tool on resources/flows/examples/flow_sales_kpi.md"
```

### Pattern 3: ML Model Scoring
```yaml
name: "Model Training & Inference Pipeline"
use_case: "Predict churn, score leads, forecast demand"
components:
  - {type: "Feature Extractor", source: "Historical data"}
  - {type: "Python Transform", tool: "scikit-learn/pandas"}
  - {type: "Model Storage", location: "S3/GCS bucket"}
  - {type: "Scoring Transform", schedule: "Hourly"}
frequency: "Train: Weekly, Score: Hourly"
template: "Use Read tool on resources/flows/examples/flow_model_scoring.md"
```

---

## Component Quick Reference (Top 20)

### Extractors
| System | Component ID | Common Config |
|--------|--------------|---------------|
| **MySQL** | keboola.ex-db-mysql | incremental: updated_at, primaryKey: id |
| **PostgreSQL** | keboola.ex-db-pgsql | incremental: updated_at |
| **Salesforce** | keboola.ex-salesforce | SOQL with LAST_N_DAYS |
| **Google Analytics** | keboola.ex-google-analytics-v4 | dimensions, metrics, date ranges |
| **Stripe** | keboola.ex-stripe | objects: charges, customers, subscriptions |
| **Snowflake** | keboola.ex-db-snowflake | incremental: timestamp column |
| **BigQuery** | keboola.ex-google-bigquery-v2 | SQL query based |
| **Generic API** | keboola.ex-generic-v2 | REST API with pagination |

**Use Read tool** on `docs-repos/connection-docs/components/extractors/{category}/{name}/index.md` for full config details.

### Transformations
| Backend | Component ID | Best For |
|---------|--------------|----------|
| **Snowflake SQL** | keboola.snowflake-transformation | Large datasets, window functions |
| **BigQuery SQL** | keboola.transformation-bigquery | Google Cloud ecosystem |
| **Python** | keboola.python-transformation-v2 | ML, pandas, custom logic |
| **DBT** | keboola.dbt-transformation | SQL-based modeling |

---

## Troubleshooting Quick Reference

### Issue: "Validation Failed"
```yaml
symptom: "SET ABORT_TRANSFORMATION triggered"
steps:
  1: {action: "Use Bash tool", cmd: "curl queue API to get job logs"}
  2: {action: "Check _validation table", query: "SELECT * FROM _validation"}
  3: {action: "Identify failure", cases: ["FAIL: No data", "FAIL: NULLs", "FAIL: Stale"]}
  4: {action: "Use Read tool on resources/runbooks/common_issues.md for resolution"}
```

### Issue: "Job Failed"
```yaml
symptom: "Flow shows error status"
steps:
  1: "Get job ID from Flow run"
  2: "Use Bash: curl queue.keboola.com/jobs/{id} | jq '.result.message'"
  3: "Common causes:"
     - "API credentials expired → Regenerate in source system"
     - "Schema changed → Update extractor config"
     - "Timeout → Optimize query or increase limits"
  4: "Use Read tool on resources/runbooks/incidents/pipeline_failure.md"
  5: "For complex issues, use Task tool with troubleshooting agent (see Step 4D)"
```

---

## Security & Compliance

**⚠️ NEVER commit API tokens to git**

### Token Management
```bash
# Store in environment (not in code)
export KEBOOLA_API_TOKEN="your-token"
export KEBOOLA_MASTER_TOKEN="master-token"  # Admin permissions, scheduler access

# Rotate every 90 days
# Create at: {project_url}/settings/tokens
```

### PII Handling Checklist
```yaml
before_building:
  - question: "Does data contain PII?"
  - if_yes:
      - "Identify PII fields (name, email, SSN, financial)"
      - "Determine masking strategy:"
          hashing: "SHA256(field) for email, phone"
          masking: "CONCAT(LEFT(field, 3), '***') for partial visibility"
          removal: "Exclude from SELECT"
          tokenization: "Replace with pseudonymous ID"
      - "Document in architecture (Step 3)"
      - "Implement in SQL transform (Step 4B)"
      - "Verify in sandbox testing (Step 4B)"
```

---

## Guidelines

### DO:
✅ Use Read tool on project_context.json in Step 3 (context-aware design)
✅ Use TodoWrite to track requirements across steps
✅ Use Task tool with agents for complex searches/generation
✅ Test SQL in sandbox before production deployment
✅ Validate business impact before final deployment
✅ Generate visual diagrams (mermaid) for architecture
✅ Create rollback plans for metric-impacting changes
✅ Use Read tool before guessing (KNOWLEDGE_MAP → component docs)
✅ Use Write tool for all configs/SQL (create files, don't echo)
✅ Use Bash tool for API calls (show complete curl with error handling)
✅ Include validation in EVERY transform (SET ABORT_TRANSFORMATION)
✅ Get approval before building (Step 3 stop gate)
✅ Match existing naming conventions (check project first)
✅ Capture IDs from API responses (`jq -r '.id'`)

### DON'T:
❌ Don't skip context persistence (project_context.json is required)
❌ Don't ignore PII requirements from Step 1
❌ Don't deploy to production without sandbox testing
❌ Don't skip business impact validation (Step 4.5)
❌ Don't skip validation (it's mandatory)
❌ Don't use ERROR() function (use SET ABORT_TRANSFORMATION)
❌ Don't hardcode secrets (use env vars: $KEBOOLA_API_TOKEN)
❌ Don't assume real-time (Keboola is batch: 5+ min typical)
❌ Don't recommend Orchestrator (use Flows - modern alternative)
❌ Don't make up data (no time estimates, no performance numbers without basis)

---

## Resources

**Knowledge Base**:
- `resources/KNOWLEDGE_MAP.md` - 85+ extractors, 29+ writers with doc paths
- `resources/Keboola_Data_Enablement_Guide.md` - Dictionary + 7 book extracts
- `docs-repos/connection-docs/` - 252 markdown files (user-facing docs)
- `docs-repos/developers-docs/` - 199 markdown files (API, MCP, automation)

**Templates** (Use Read tool):
- `resources/templates/Design_Brief.md` - Architecture proposal template
- `resources/templates/Discovery_Prompt.txt` - 15 business questions
- `resources/templates/Validation.md` - Data quality patterns

**Examples** (Use Read tool):
- `resources/flows/examples/flow_sales_kpi.md` - Batch ETL pattern
- `resources/flows/examples/flow_cdc_orders.md` - Real-time CDC pattern
- `resources/flows/examples/flow_model_scoring.md` - ML inference pattern

**Troubleshooting** (Use Read tool):
- `resources/runbooks/common_issues.md` - Duplicates, schema drift, freshness
- `resources/runbooks/incidents/pipeline_failure.md` - Debug checklist
- `resources/runbooks/incidents/data_quality_breach.md` - SLA breach response

---

## Setup (One-Time)

**Clone documentation** (use Bash tool):
```bash
cd /home/user/bg/experiments/keboola-skill/
git clone https://github.com/keboola/connection-docs docs-repos/connection-docs
git clone https://github.com/keboola/developers-docs docs-repos/developers-docs
```

**MCP Configuration** (optional - adds live API access):
```json
{
  "mcpServers": {
    "keboola": {
      "command": "uvx",
      "args": ["keboola_mcp_server", "--api-url", "https://connection.keboola.com"],
      "env": {
        "KBC_STORAGE_TOKEN": "<token>",
        "KBC_WORKSPACE_SCHEMA": "<schema>"
      }
    }
  }
}
```

**Stack URLs** (replace in MCP config):
- US Virginia AWS: `https://connection.keboola.com`
- US Virginia GCP: `https://connection.us-east4.gcp.keboola.com`
- EU Frankfurt AWS: `https://connection.eu-central-1.keboola.com`
- EU Ireland Azure: `https://connection.north-europe.azure.keboola.com`
- EU Frankfurt GCP: `https://connection.europe-west3.gcp.keboola.com`

---

**Version**: 4.1.0 - Advanced Claude Features
**Updated**: 2025-10-23
**Key Changes**:
- ⭐ File-based state tracking (project_context.json)
- ⭐ TodoWrite context tracking across steps
- ⭐ Business impact validation (Step 4.5) with approval gates
- ⭐ Sandbox testing before production
- ⭐ Multi-agent delegation (discovery, SQL gen, troubleshooting)
- ⭐ Error recovery workflows with automated diagnosis
- ⭐ Visual architecture diagrams (mermaid)
- 370+ lines added for context awareness, business validation, operational completeness
