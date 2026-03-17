---
context: fork
---

# /dataasset

Create a DataAsset note documenting a data entity - database table, API endpoint, data product, Kafka topic, or file. Captures location, ownership, consumers, and planned changes.

## Usage

```
/dataasset <name>
/dataasset "Revenue Fact Table"
/dataasset "Customer Orders"
/dataasset "Maintenance Events"
```

## Instructions

### Phase 1: Parse Input & Identify System

1. Extract data asset name from input
2. Ask which system produces this data:
   ```
   Which system produces this data?
   Search: [user searches for System]
   Or create new System? (Y/n)
   ```
3. Confirm link: "Link to [[System - {{system}}]]? (Y/n)"

### Phase 2: Essential Information

```
Creating DataAsset: {{name}} (produced by {{system}})

1️⃣ Asset ID (unique identifier):
   Suggestion: {{SYSTEM}}-{{NAME}}-001
   User input: [accept or modify]

2️⃣ Data Type:
   - database-table (relational table)
   - database-view (virtual table)
   - api-endpoint (REST/GraphQL data)
   - kafka-topic (event stream)
   - data-product (curated dataset)
   - data-lake (file-based storage)
   - file (CSV, Excel, etc.)
   - report (BI report/dashboard)
   - cache (Redis/Memcached)
   Default: database-table
   User input: [selection]

3️⃣ Domain:
   - engineering
   - data
   - operations
   - finance
   - hr
   - supply-chain
   - maintenance
   Default: [infer from system]
   User input: [selection]

4️⃣ Classification:
   - public
   - internal
   - confidential
   - secret
   Default: internal
   User input: [selection]

5️⃣ Storage Location:
   Examples: "mydb.fact_revenue", "s3://bucket/path", "/api/v1/orders"
   User input: [path/table/endpoint]

6️⃣ Format:
   - sql
   - json
   - parquet
   - avro
   - csv
   - xml
   - binary
   Default: [infer from data type]
   User input: [selection]
```

### Phase 3: Ownership

```
7️⃣ Data Owner (accountable person):
   Search: [[Person - ...]]
   User input: [search or skip]

8️⃣ Data Steward (governance contact, optional):
   Search: [[Person - ...]]
   User input: [search or skip]
```

### Phase 4: Consumer Relationships (Key Differentiator)

```
Which systems currently consume this data?

Current Consumers (search for Systems):
> [[System - Data Warehouse]]
> [[System - Analytics Platform]]
[Enter blank to finish]

Planned Consumers (systems that WILL consume):
> [[System - New BI Tool]]
[Enter blank to finish]

Deprecating Consumers (systems moving AWAY from this data):
> [[System - Legacy Reporting]]
[Enter blank to finish]
```

### Phase 5: Data Lineage (Optional)

Ask: "Track data lineage? (Y/n)"

If YES:

```
Derived From (upstream data sources):
> [[DataAsset - Source Invoices]]
[Enter blank to finish]

Feeds Into (downstream data assets):
> [[DataAsset - Revenue Dashboard]]
[Enter blank to finish]
```

### Phase 6: Operational Details (Quick or Full)

Ask: "Quick capture or full detail? (Q/f)"

**If Quick** - skip to Phase 7 with defaults

**If Full**:

```
Refresh Frequency:
- real-time | hourly | daily | weekly | monthly | ad-hoc
Default: daily

Record Count (approximate): [number]
Volume per Day: [e.g., "2.5GB", "500K records"]
Retention Period: [e.g., "7 years", "90 days"]

Data Quality Metrics:
- Completeness (%): [e.g., 98.5]
- Uniqueness (%): [e.g., 99.9]
- Accuracy: high | medium | low
- Timeliness: [e.g., "< 5 minutes"]

SLAs:
- Availability: [e.g., "99.9%"]
- Latency: [e.g., "< 500ms"]

Governance:
- GDPR Applicable: Y/n
- PII Fields: [comma-separated list]
```

### Phase 7: Generate Frontmatter

```yaml
type: DataAsset
title: "{{name}}"
assetId: "{{assetId}}"

# Classification
domain: {{domain}}
dataType: {{dataType}}
classification: {{classification}}

# Location & Format
sourceSystem: "[[System - {{system}}]]"
storageLocation: "{{location}}"
format: {{format}}

# Ownership
owner: "[[{{owner}}]]"
steward: {{steward}}

# Relationships - Current State
producedBy: ["[[System - {{system}}]]"]
consumedBy: [{{consumers}}]
exposedVia: [{{exposedVia}}]

# Relationships - Future State
plannedConsumers: [{{plannedConsumers}}]
deprecatingConsumers: [{{deprecatingConsumers}}]

# Lineage
derivedFrom: [{{derivedFrom}}]
feedsInto: [{{feedsInto}}]

# Operational Metrics
refreshFrequency: {{frequency}}
recordCount: {{recordCount}}
volumePerDay: "{{volume}}"
retentionPeriod: "{{retention}}"

# Data Quality
completeness: {{completeness}}
uniqueness: {{uniqueness}}
accuracy: {{accuracy}}
timeliness: "{{timeliness}}"

# SLAs
slaAvailability: "{{slaAvailability}}"
slaLatency: "{{slaLatency}}"

# Governance
gdprApplicable: {{gdpr}}
piiFields: [{{piiFields}}]

# Quality Indicators
confidence: medium
freshness: current
verified: false
reviewed: null

created: {{today}}
modified: {{today}}
tags: [type/data-asset, domain/{{domain}}]
```

### Phase 8: Generate Body Content

Create structured body with:

1. **Overview** - What data this contains, business purpose
2. **Source Details** - Table with system, location, format
3. **Data Relationships** - Mermaid diagram showing producers/consumers
4. **Consumer Systems** - Table of current, planned, and deprecating consumers
5. **Data Lineage** - Upstream/downstream flow (if captured)
6. **Operational Metrics** - Volume, refresh, quality (if full detail)
7. **Security & Governance** - Classification, PII, GDPR status
8. **Related Notes** - Links to ADRs, integrations, system notes

### Phase 9: Create File

**Filename**: `DataAsset - {{name}}.md`

**Location**: Vault root

**Output**:

```
✅ Created: DataAsset - {{name}}.md

Linked to:
- [[System - {{producing system}}]] (producer)
- [[System - {{consumer1}}]] (consumer)
- [[System - {{consumer2}}]] (consumer)

Relationship summary:
- 1 producer
- {{n}} current consumers
- {{n}} planned consumers
- {{n}} deprecating consumers

Next steps:
1. Add to [[MOC - Data Assets]]
2. Create integration notes: /integration {{source}} {{target}}
3. Document data contract if critical
```

## Example Interaction

```
User: /dataasset "Work Orders"

System: Which system produces this data?
> ERP System

Asset ID suggestion: ERP-WORK-ORDERS-001
> [accept]

Data Type:
> database-table

Domain:
> engineering

Classification:
> internal

Storage Location:
> erp.dbo.work_orders

Format:
> sql

Data Owner:
> [[Data Owner Name]]

Data Steward:
> [skip]

Current Consumers:
> [[System - Data Warehouse]]
> [[System - Analytics Platform]]
> [done]

Planned Consumers:
> [[System - New BI Tool]]
> [done]

Deprecating Consumers:
> [[System - Legacy Reporting]]
> [done]

Track lineage? (Y/n)
> n

Quick or Full detail? (Q/f)
> q

✅ Created: DataAsset - Work Orders.md

Linked to:
- [[System - ERP System]] (producer)
- [[System - Data Warehouse]] (consumer)
- [[System - Analytics Platform]] (consumer)

Relationship summary:
- 1 producer
- 2 current consumers
- 1 planned consumer
- 1 deprecating consumer
```

## Key Differentiators from /datasource

| Aspect       | /datasource           | /dataasset                                 |
| ------------ | --------------------- | ------------------------------------------ |
| Future state | Not tracked           | `plannedConsumers`, `deprecatingConsumers` |
| Lineage      | Schema-level only     | System-level `derivedFrom`/`feedsInto`     |
| Detail level | Always full           | Quick vs Full capture modes                |
| Ownership    | Single owner          | `owner` + `steward`                        |
| SLAs         | Not tracked           | `slaAvailability`, `slaLatency`            |
