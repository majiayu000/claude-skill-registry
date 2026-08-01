---
name: acuantia-dataform
description: 'Use when working on Acuantia''s BigQuery Dataform pipeline (acuantia-gcp-dataform
  project) - adds Acuantia-specific patterns on top of dataform-engineering-fundamentals:
  ODS two-arg ref() syntax, looke'
---

---
name: acuantia-dataform
description: Use when working on Acuantia's BigQuery Dataform pipeline (acuantia-gcp-dataform project) - adds Acuantia-specific patterns on top of dataform-engineering-fundamentals: ODS two-arg ref() syntax, looker_ filename prefix, Looker integration (looker_prod/looker_dev), acuantia dataset conventions, coordination with callrail_data_export/dialpad_data_integration/looker projects
---

# Acuantia Dataform Engineering

## REQUIRED PREREQUISITE

**YOU MUST USE `dataform-engineering-fundamentals` SKILL FIRST.**

This skill is a **thin extension layer** that adds Acuantia-specific patterns on top of the generic `dataform-engineering-fundamentals` skill.

**Before using this skill:**
1. Read and follow `dataform-engineering-fundamentals` completely
2. Apply ALL generic Dataform practices from that skill
3. Then apply the Acuantia-specific patterns below

**This skill does NOT repeat generic practices.** If you're looking for:
- TDD workflow → See `dataform-engineering-fundamentals`
- Safety practices (--schema-suffix dev, --dry-run) → See `dataform-engineering-fundamentals`
- ${ref()} enforcement → See `dataform-engineering-fundamentals`
- Documentation standards → See `dataform-engineering-fundamentals`
- Architecture patterns → See `dataform-engineering-fundamentals`

**This skill ONLY adds**: Acuantia-specific conventions that differ from or extend generic patterns.

## When to Use

Use this skill when working on:
- `acuantia-gcp-dataform` project
- Tables that integrate with Acuantia's Looker instance
- Transformations using Acuantia's ODS (Operational Data Store) architecture
- Pipelines coordinating with `callrail_data_export` or `dialpad_data_integration` projects

## Acuantia-Specific Patterns

### 1. ODS Architecture and Two-Argument ref()

Acuantia uses a special ODS (Operational Data Store) architecture that requires two-argument ref() syntax.

**ODS Architecture**:
- `acuantia.ods` - Source of truth (master operational data)
- `acuantia.ods_dev` - Development/staging dataset
- `acuantia.ods_prod` - Production staging dataset

**CRITICAL**: Use two-argument ref() for ODS tables to avoid suffix duplication:

```sql
-- CORRECT: Two-argument ref() for ODS
FROM ${ref("ods", "sap_customers")}
FROM ${ref("ods", "magento_orders")}

-- WRONG: Single-argument causes ods_dev_dev with --schema-suffix dev
FROM ${ref("sap_customers")}  -- Creates ods_dev_dev ❌
```

**Why**: The ODS schema name itself gets the suffix applied. Two-argument ref() prevents `ods_dev_dev` when using `--schema-suffix dev`.

**All other tables**: Use single-argument ref() as per `dataform-engineering-fundamentals`.

### 2. Looker Table Naming Convention

Tables in `definitions/output/looker/` MUST be prefixed with `looker_`.

**File naming**:
```
definitions/output/looker/looker_customer_metrics.sqlx  ✅
definitions/output/looker/looker_sales_summary.sqlx     ✅
definitions/output/looker/customer_metrics.sqlx         ❌
```

**Schema configuration**:
```sql
config {
  type: "table",
  schema: "looker_prod",  // Production Looker tables
  tags: ["looker", "daily"]
}
```

**Why**:
- Makes Looker-specific tables immediately identifiable
- Prevents naming conflicts with intermediate tables
- Aligns with Looker project conventions in `looker/` directory

### 3. Acuantia Dataset Conventions

**Primary Datasets**:
- `acuantia.ods` - Master operational data store (source of truth)
- `acuantia.ods_dev` / `acuantia.ods_prod` - ODS staging datasets
- `acuantia.looker_prod` - Production Looker tables
- `acuantia.looker_dev` - Development Looker tables
- `acuantia.dataform` - Operations and temp tables
- `acuantia.callrail_api` - CallRail raw data
- `acuantia.dialpad_api` - Dialpad raw data
- `acuantia.hubspot` - HubSpot data (via Fivetran)
- `acuantia.magento_rotoplas_me_22_prod` - Magento/Adobe Commerce data (via Fivetran)

**Schema suffix behavior**:
```bash
# With --schema-suffix dev
looker_prod → looker_dev
ods → ods (no suffix, use two-arg ref)
dataform → dataform_dev
```

### 4. Looker Integration Context

Tables in `definitions/output/looker/` feed Acuantia's Looker instance at https://looker.acuantia.com.

**Optimization requirements**:
- Add partitioning/clustering for query performance (Looker users run ad-hoc queries)
- Use descriptive column names (Looker dimension names derive from these)
- Include comprehensive column descriptions (synced to Looker metadata via scripts)
- Consider common Looker user query patterns (filters, aggregations)

**Looker-specific config pattern**:
```sql
config {
  type: "table",
  schema: "looker_prod",
  tags: ["looker", "daily"],
  bigquery: {
    partitionBy: "DATE(order_date)",
    clusterBy: ["customer_id", "region"]
  },
  columns: {
    customer_id: "Unique customer identifier from SAP (KUNNR field)",
    order_date: "Date when order was placed",
    region: "Geographic region for reporting (matches Looker region dimension)"
  }
}
```

**Metadata sync**: Use `node scripts/updateLookerDescriptions.js` in `acuantia-gcp-dataform` to sync column descriptions to Looker views.

### 5. Source System Integration

Acuantia integrates data from multiple source systems. Use specific terminology when documenting columns:

**SAP ERP**:
```sql
columns: {
  customer_id: "SAP Customer Number (KUNNR) - unique identifier in SAP ERP",
  customer_name: "Customer name (NAME1 field) - legal business name",
  account_group: "Customer Account Group (KTOKD) - classification code"
}
```

**Dialpad API** (from `dialpad_data_integration` project):
```sql
-- Source declaration
-- definitions/sources/dialpad/calls.sqlx
config {
  type: "declaration",
  database: "acuantia",
  schema: "dialpad_api",
  name: "calls",
  description: "Dialpad call records with transcripts and sentiment analysis",
  columns: {
    call_id: "Unique call identifier from Dialpad API",
    transcript: "Full call transcript from Dialpad AI",
    sentiment: "Overall call sentiment: positive/negative/neutral/mixed"
  }
}
```

**CallRail API** (from `callrail_data_export` project):
```sql
-- Source declaration
-- definitions/sources/callrail/calls.sqlx
config {
  type: "declaration",
  database: "acuantia",
  schema: "callrail_api",
  name: "calls",
  columns: {
    call_id: "Unique CallRail call identifier",
    tracking_phone_number: "CallRail tracking number that received the call",
    attribution: "Nested attribution data (source, medium, campaign)"
  }
}
```

**HubSpot CRM** (via Fivetran):
```sql
config {
  type: "declaration",
  database: "acuantia",
  schema: "hubspot",
  name: "contact"
}
```

**Magento/Adobe Commerce** (via Fivetran):
```sql
config {
  type: "declaration",
  database: "acuantia",
  schema: "magento_rotoplas_me_22_prod",
  name: "sales_order"
}
```

### 6. Cross-Project Coordination

Acuantia's data platform spans multiple projects that work together:

```
callrail_data_export/          → acuantia.callrail_api.*
dialpad_data_integration/      → acuantia.dialpad_api.*
acuantia-gcp-dataform/         → Transform and model
looker/                        → Visualize and report
```

**When modifying schemas**:
1. **Source changes** (callrail_data_export or dialpad_data_integration):
   - Update Python schema definitions
   - Test with small data exports
   - Deploy to production

2. **Dataform updates** (acuantia-gcp-dataform):
   - Update source declarations in `definitions/sources/`
   - Modify transformations if needed
   - Update `definitions/output/looker/` tables
   - Test with `--schema-suffix dev`

3. **Looker updates** (looker project):
   - Update view definitions
   - Add new dimensions/measures
   - Test in development environment

**Schema change protocol**: Always coordinate changes across all three layers (raw → transformed → visualization).

### 7. Business Context

Acuantia serves four main product verticals:
- **Septic**: Septic tank systems
- **General**: General purpose containers
- **Industrial**: Industrial containers and equipment
- **Chemical**: Chemical storage containers

**Key business entities**:
- TankHolding: Key business vertical with specialized recovery operations
- Customer Journey: Multi-touch attribution across CallRail, HubSpot, and Magento
- Voice of Customer (VoC): Dialpad call transcripts analyzed for sentiment and topics

**When creating tables**, consider how they support these business verticals and use cases.

## Validation Queries (Acuantia-Specific)

```bash
# Check Looker dev tables
bq query --use_legacy_sql=false \
  "SELECT COUNT(*) FROM \`acuantia.looker_dev.looker_customer_metrics\`"

# Check ODS tables
bq query --use_legacy_sql=false \
  "SELECT COUNT(*) FROM \`acuantia.ods.sap_customers\`"

# Verify CallRail data freshness
bq query --use_legacy_sql=false \
  "SELECT MAX(start_time) FROM \`acuantia.callrail_api.calls\`"

# Verify Dialpad data freshness
bq query --use_legacy_sql=false \
  "SELECT MAX(start_time) FROM \`acuantia.dialpad_api.calls\`"
```

## Common Acuantia-Specific Mistakes

### Mistake 1: Using single-argument ref() for ODS tables

```sql
-- WRONG: Creates ods_dev_dev with --schema-suffix dev
FROM ${ref("sap_customers")}

-- CORRECT: Two-argument ref() for ODS
FROM ${ref("ods", "sap_customers")}
```

### Mistake 2: Missing looker_ prefix

```
# WRONG
definitions/output/looker/customer_metrics.sqlx

# CORRECT
definitions/output/looker/looker_customer_metrics.sqlx
```

### Mistake 3: Using wrong schema for Looker tables

```sql
-- WRONG
config {
  type: "table",
  schema: "reporting"  // Not Looker-specific
}

-- CORRECT
config {
  type: "table",
  schema: "looker_prod"  // Consumed by Looker
}
```

### Mistake 4: Hardcoding acuantia.ods in queries

```sql
-- WRONG: Hardcoded path
FROM `acuantia.ods.sap_customers`

-- CORRECT: Use two-argument ref()
FROM ${ref("ods", "sap_customers")}
```

## Red Flags - Acuantia-Specific

If you're thinking any of these thoughts, STOP:

- "I'll use single-argument ref() for ODS tables (it's simpler)"
- "I don't need the looker_ prefix for this Looker table"
- "I'll use a different schema name instead of looker_prod"
- "I'll skip coordinating with the looker/ project team"
- "I don't need to check CallRail/Dialpad data freshness"

**All of these mean**: You're about to break Acuantia conventions. Follow the patterns above.

## Quick Reference

| Pattern | Acuantia Convention |
|---------|---------------------|
| ODS tables | Two-argument ref(): `${ref("ods", "table_name")}` |
| Looker tables | Prefix with `looker_` and use `schema: "looker_prod"` |
| CallRail data | `acuantia.callrail_api.*` |
| Dialpad data | `acuantia.dialpad_api.*` |
| HubSpot data | `acuantia.hubspot.*` |
| Magento data | `acuantia.magento_rotoplas_me_22_prod.*` |
| Dev testing | `--schema-suffix dev` (see dataform-engineering-fundamentals) |
| Looker metadata | Run `node scripts/updateLookerDescriptions.js` |

## Summary

This skill adds **only Acuantia-specific patterns**. For all generic Dataform practices:
- TDD workflow
- Safety practices
- ${ref()} enforcement (general cases)
- Documentation standards
- Architecture patterns
- Troubleshooting

**→ See `dataform-engineering-fundamentals` skill.**

The patterns in this skill (ODS two-arg ref, looker_ prefix, Acuantia datasets, cross-project coordination) are **required additions** to the generic foundation, not replacements.
