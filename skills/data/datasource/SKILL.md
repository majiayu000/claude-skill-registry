---
context: fork
---

# /datasource

Create a DataSource note documenting a specific database, table, API endpoint, dataset, or data entity with schema, quality metrics, and access information.

## Usage

```
/datasource <name>
/datasource "SAP Invoices"
/datasource "DataPlatform Revenue Fact Table"
/datasource "Snowflake Customers"
```

## Instructions

### Phase 1: Parse Input & Link to System

1. Extract data source name
2. Ask which system owns this data:
   ```
   Which system owns this data source?
   Search: [user searches for System]
   Or create new System? (Y/n)
   ```
3. Confirm link: "Link to [[System - {{system}}]]? (Y/n)"

### Phase 2: Essential Information

```
Creating DataSource: {{name}} (owned by {{system}})

1️⃣ Data Type:
   - database-table (relational table)
   - database-view (virtual table)
   - api-endpoint (REST/GraphQL data)
   - kafka-topic (event stream)
   - data-warehouse-table (Snowflake/BigQuery)
   - data-lake (file-based storage)
   - cache (Redis/Memcached)
   Default: database-table
   User input: [selection]

2️⃣ Record Count (approximate):
   Default: null
   User input: [number, e.g., 5000000]

3️⃣ Data Volume per Day:
   Default: null
   User input: [e.g., "2.5GB", "500K records"]

4️⃣ Refresh Frequency:
   - real-time
   - hourly
   - daily
   - weekly
   - on-demand
   Default: daily
   User input: [selection]

5️⃣ Classification:
   - public
   - internal
   - confidential
   - secret
   Default: internal
   User input: [selection]
```

### Phase 3: Data Quality (Optional)

Ask: "Add data quality metrics? (Y/n)"

If YES:
```
- Completeness (%): 98.5
- Uniqueness (%): 99.9
- Accuracy: high | medium | low
- Timeliness: how fresh (< 5 minutes, < 1 hour, etc.)
```

### Phase 4: Schema & Key Fields

```
Key Fields (comma-separated):
invoice_id, vendor_id, amount
```

Then ask:
```
Schema details needed? (Y/n)
- Parent entities (sources of this data)
- Child entities (what feeds from this)
- Related tables
```

### Phase 5: Access & Consumers

```
How is this data accessed?
- REST API
- GraphQL
- Direct database query
- Kafka topic
- Batch export / S3
- Other
Default: [based on data type]

Which systems consume this data?
Search: [[System - DataPlatform]]
Add: [[System - Analytics]]
```

### Phase 6: Generate Frontmatter

```yaml
type: DataSource
title: "{{name}}"

sourceId: "{{sourceId}}"
sourceSystem: "[[System - {{system}}]]"
owner: "[[{{person}}]]"

dataType: {{type}}
recordCount: {{count}}
volumePerDay: "{{volume}}"
refreshFrequency: {{frequency}}

classification: {{classification}}
gdprApplicable: {{gdpr}}
piiFields: [{{pii}}]

completeness: {{completeness}}
uniqueness: {{uniqueness}}
accuracy: {{accuracy}}
timeliness: {{timeliness}}

exposedVia: [rest-api, kafka-topic]
consumerCount: {{consumer_count}}
criticalConsumers: [{{critical_systems}}]

confidence: medium
freshness: current
verified: false

created: 2026-01-14
tags: [type/data-source, {{sourceSystem|lower}}]
```

### Phase 7: Generate Body Content

1. **Overview**: What data this contains
2. **Data Volume & Performance**: Size, growth, refresh
3. **Data Schema**: Sample table structure
4. **Field Mapping**: Key fields explained
5. **Data Quality**: Completeness, accuracy metrics
6. **Access & Integration**: How systems access it
7. **Security & Governance**: Classification, PII, GDPR
8. **Related Integration Notes**: What uses this data

### Phase 8: Create File

**Filename**: `DataSource - {{name}}.md`

**Location**: Vault root

**Output**:
```
✅ Created: DataSource - {{name}}.md

Linked to:
- [[System - {{owning system}}]]

Next steps:
1. Create integration: /integration {{source}} {{target}}
2. Document consumer systems
3. Add to architecture diagram
```

## Example Interaction

```
User: /datasource "SAP Invoices"

System: Which system owns this data?
> SAP S/4HANA

Data Type:
> database-table

Record Count:
> 200000000

Volume per Day:
> 5GB

Refresh Frequency:
> hourly

Classification:
> confidential

Data Quality:
Completeness: 98.5
Uniqueness: 99.9
Accuracy: high
Timeliness: < 5 minutes

Key Fields:
> invoice_id, vendor_id, company_code, amount, invoice_date

Consumers (search for Systems):
> DataPlatform
> Snowflake
> Analytics

✅ Created: DataSource - SAP Invoices.md

Updated:
- [[System - SAP S/4HANA]] added to owns/exposes
- [[System - DataPlatform]] added to consumers
- [[System - Snowflake]] added to consumers
```
