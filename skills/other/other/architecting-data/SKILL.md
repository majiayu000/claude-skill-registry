---
name: architecting-data
description: Strategic guidance for designing modern data platforms, covering storage paradigms (data lake, warehouse, lakehouse), modeling approaches (dimensional, normalized, data vault, wide tables), data mesh principles, and medallion architecture patterns. Use when architecting data platforms, choosing between centralized vs decentralized patterns, selecting table formats (Iceberg, Delta Lake), or designing data governance frameworks.
---

# Data Architecture

## Purpose

Guide architects and platform engineers through strategic data architecture decisions for modern cloud-native data platforms.

## When to Use This Skill

Invoke this skill when:
- Designing a new data platform or modernizing legacy systems
- Choosing between data lake, data warehouse, or data lakehouse
- Deciding on data modeling approaches (dimensional, normalized, data vault, wide tables)
- Evaluating centralized vs data mesh architecture
- Selecting open table formats (Apache Iceberg, Delta Lake, Apache Hudi)
- Designing medallion architecture (bronze, silver, gold layers)
- Implementing data governance and cataloging

## Core Concepts

### 1. Storage Paradigms

Three primary patterns for analytical data storage:

**Data Lake:** Centralized repository for raw data at scale
- Schema-on-read, cost-optimized ($0.02-0.03/GB/month)
- Use when: Diverse data sources, exploratory analytics, ML/AI training data

**Data Warehouse:** Structured repository optimized for BI
- Schema-on-write, ACID transactions, fast queries
- Use when: Known BI requirements, strong governance needed

**Data Lakehouse:** Hybrid combining lake flexibility with warehouse reliability
- Open table formats (Iceberg, Delta Lake), ACID on object storage
- Use when: Mixed BI + ML workloads, cost optimization (60-80% cheaper than warehouse)

**Decision Framework:**
- BI/Reporting only + Known queries → Data Warehouse
- ML/AI primary + Raw data needed → Data Lake or Lakehouse
- Mixed BI + ML + Cost optimization → Data Lakehouse (recommended)
- Exploratory/Unknown use cases → Data Lake

For detailed comparison, see [references/storage-paradigms.md](references/storage-paradigms.md).

### 2. Data Modeling Approaches

Four primary modeling patterns:

**Dimensional (Kimball):** Star/snowflake schemas for BI
- Use when: Known query patterns, BI dashboards, trend analysis

**Normalized (3NF):** Eliminate redundancy for transactional systems
- Use when: OLTP systems, frequent updates, strong consistency

**Data Vault 2.0:** Flexible model with complete audit trail
- Use when: Compliance requirements, multiple sources, agile warehousing

**Wide Tables:** Denormalized, optimized for columnar storage
- Use when: ML feature stores, data science notebooks, high-performance dashboards

**Decision Framework:**
- Analytical (BI) + Known queries → Dimensional (Star Schema)
- Transactional (OLTP) → Normalized (3NF)
- Compliance/Audit → Data Vault 2.0
- Data Science/ML → Wide Tables

For detailed patterns, see [references/modeling-approaches.md](references/modeling-approaches.md).

### 3. Data Mesh Principles

Decentralized architecture for large organizations (>500 people).

**Four Core Principles:**
1. Domain-oriented decentralization
2. Data as a product (SLAs, quality, documentation)
3. Self-serve data infrastructure
4. Federated computational governance

**Readiness Assessment (Score 1-5 each):**
1. Domain clarity
2. Team maturity
3. Platform capability
4. Governance maturity
5. Scale need
6. Organizational buy-in

**Scoring:** 24-30: Strong candidate | 18-23: Hybrid | 12-17: Build foundation first | 6-11: Centralized

**Red Flags:** Small org (<100 people), unclear domains, no platform team, weak governance

For full guide, see [references/data-mesh-guide.md](references/data-mesh-guide.md).

### 4. Medallion Architecture

Standard lakehouse pattern: Bronze (raw) → Silver (cleaned) → Gold (business-level)

**Bronze Layer:** Exact copy of source data, immutable, append-only

**Silver Layer:** Validated, deduplicated, typed data

**Gold Layer:** Business logic, aggregates, dimensional models, ML features

**Data Quality by Layer:**
- Bronze → Silver: Schema validation, type checks, deduplication
- Silver → Gold: Business rule validation, referential integrity
- Gold: Anomaly detection, statistical checks

For patterns, see [references/medallion-pattern.md](references/medallion-pattern.md).

### 5. Open Table Formats

Enable ACID transactions on data lakes:

**Apache Iceberg:** Multi-engine, vendor-neutral (Context7: 79.7 score)
- Use when: Avoid vendor lock-in, multi-engine flexibility

**Delta Lake:** Databricks ecosystem, Spark-optimized
- Use when: Committed to Databricks

**Apache Hudi:** Optimized for CDC and frequent upserts
- Use when: CDC-heavy workloads

**Recommendation:** Apache Iceberg for new projects (vendor-neutral, broadest support)

For comparison, see [references/table-formats.md](references/table-formats.md).

### 6. Modern Data Stack

**Standard Layers:**
- Ingestion: Fivetran, Airbyte, Kafka
- Storage: Snowflake, Databricks, BigQuery
- Transformation: dbt (Context7: 87.0 score), Spark
- Orchestration: Airflow, Dagster, Prefect
- Visualization: Tableau, Looker, Power BI
- Governance: DataHub, Alation, Great Expectations

**Tool Selection:**
- Fivetran vs Airbyte: Pre-built connectors vs cost-sensitive
- Snowflake vs Databricks: BI-focused vs ML-focused
- dbt vs Spark: SQL-based vs large-scale processing

For detailed recommendations, see [references/tool-recommendations.md](references/tool-recommendations.md) and [references/modern-data-stack.md](references/modern-data-stack.md).

### 7. Data Governance

**Data Catalog:** Searchable inventory (DataHub, Alation, Collibra)

**Data Lineage:** Track data flow (OpenLineage, Marquez)

**Data Quality:** Validation and testing (Great Expectations, Soda, dbt tests)

**Access Control:**
- RBAC: Role-based (sales_analyst role)
- ABAC: Attribute-based (row-level security)
- Column-level: Dynamic data masking for PII

For governance patterns, see [references/governance-patterns.md](references/governance-patterns.md).

## Decision Frameworks

### Framework 1: Storage Paradigm Selection

**Step 1: Identify Primary Use Case**
- BI/Reporting only → Data Warehouse
- ML/AI primary → Data Lake or Lakehouse
- Mixed BI + ML → Data Lakehouse
- Exploratory → Data Lake

**Step 2: Evaluate Budget**
- High budget, known queries → Data Warehouse
- Cost-sensitive, flexible → Data Lakehouse

**Recommendation by Org Size:**
- Startup (<50): Data Warehouse (simplicity)
- Growth (50-500): Data Lakehouse (balance)
- Enterprise (>500): Hybrid or unified Lakehouse

See [references/decision-frameworks.md](references/decision-frameworks.md#storage-paradigm).

### Framework 2: Data Modeling Approach

**Decision Tree:**
- Analytical (BI) workload → Dimensional or Wide Tables
- Transactional (OLTP) → Normalized (3NF)
- Compliance/Audit → Data Vault 2.0
- Data Science/ML → Wide Tables

See [references/decision-frameworks.md](references/decision-frameworks.md#modeling-approach).

### Framework 3: Data Mesh Readiness

Use 6-factor assessment. Score interpretation:
- 24-30: Proceed with data mesh
- 18-23: Hybrid approach
- 12-17: Build foundation first
- 6-11: Centralized

See [references/decision-frameworks.md](references/decision-frameworks.md#data-mesh-readiness).

### Framework 4: Open Table Format Selection

**Decision Tree:**
- Multi-engine flexibility → Apache Iceberg
- Databricks ecosystem → Delta Lake
- Frequent upserts/CDC → Apache Hudi

**Recommendation:** Apache Iceberg for new projects

See [references/decision-frameworks.md](references/decision-frameworks.md#table-format).

## Common Scenarios

### Startup Data Platform

**Context:** 50-person startup, PostgreSQL + MongoDB + Stripe

**Recommendation:**
- Storage: BigQuery or Snowflake
- Ingestion: Airbyte or Fivetran
- Transformation: dbt
- Orchestration: dbt Cloud
- Architecture: Simple data warehouse

See [references/scenarios.md](references/scenarios.md#startup).

### Enterprise Modernization

**Context:** Legacy Oracle warehouse, need cloud migration

**Recommendation:**
- Storage: Data Lakehouse (Databricks or Snowflake with Iceberg)
- Strategy: Incremental migration with CDC
- Architecture: Medallion (bronze, silver, gold)
- Cost Savings: 60-80%

See [references/scenarios.md](references/scenarios.md#enterprise-modernization).

### Data Mesh Assessment

**Context:** 200-person company, 5-person central data team

**Recommendation:** NOT YET. Build foundation first.
- Organization too small (<500 recommended)
- Central team not yet bottleneck
- Invest in self-serve platform and governance

See [references/scenarios.md](references/scenarios.md#data-mesh).

## Tool Recommendations

### Research-Validated (Context7, December 2025)

**dbt:** Score 87.0, 3,532+ code snippets
- SQL-based transformations, version control, testing
- Industry standard for data transformation

**Apache Iceberg:** Score 79.7, 832+ code snippets
- Open table format, multi-engine, vendor-neutral
- Production-ready (Netflix, Apple, Adobe)

**Tool Stack by Use Case:**

**Startup:** BigQuery + Airbyte + dbt + Metabase (<$1K/month)

**Growth:** Snowflake + Fivetran + dbt + Airflow + Tableau ($10K-50K/month)

**Enterprise:** Snowflake + Databricks + Fivetran + Kafka + dbt + Airflow + Alation ($50K-500K/month)

See [references/tool-recommendations.md](references/tool-recommendations.md).

## Implementation Patterns

### Pattern 1: Medallion Architecture

```sql
-- Bronze: Raw ingestion
CREATE TABLE bronze.raw_customers (_ingested_at TIMESTAMP, _raw_data STRING);

-- Silver: Cleaned
CREATE TABLE silver.customers AS
SELECT json_extract(_raw_data, '$.id') AS customer_id, ...
FROM bronze.raw_customers
QUALIFY ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY _ingested_at DESC) = 1;

-- Gold: Business-level
CREATE TABLE gold.fact_sales AS
SELECT s.order_id, d.date_key, c.customer_key, ...
FROM silver.sales s
JOIN gold.dim_date d ON s.order_date = d.date;
```

### Pattern 2: Apache Iceberg Table

```sql
CREATE TABLE catalog.db.sales (order_id BIGINT, amount DECIMAL(10,2))
USING iceberg
PARTITIONED BY (days(order_date));

-- Time travel
SELECT * FROM catalog.db.sales TIMESTAMP AS OF '2025-01-01';
```

### Pattern 3: dbt Transformation

```sql
-- models/staging/stg_customers.sql
WITH source AS (SELECT * FROM {{ source('raw', 'customers') }}),
cleaned AS (
  SELECT customer_id, UPPER(customer_name) AS customer_name
  FROM source WHERE customer_id IS NOT NULL
)
SELECT * FROM cleaned
```

For complete examples, see [examples/](examples/).

## Best Practices

1. **Start simple:** Avoid over-engineering; begin with warehouse or basic lakehouse
2. **Invest in governance early:** Catalog, lineage, quality from day one
3. **Medallion architecture:** Use bronze-silver-gold for clear quality layers
4. **Open table formats:** Prefer Iceberg or Delta Lake to avoid vendor lock-in
5. **Assess mesh readiness:** Don't decentralize prematurely (<500 people)
6. **Automate quality:** Integrate tests (Great Expectations, dbt) into CI/CD
7. **Monitor pipelines:** Observability is critical (freshness, quality, health)
8. **Document as code:** Use dbt docs, DataHub, YAML for self-service
9. **Incremental loading:** Only load new/changed data (watermark columns)
10. **Business alignment:** Align architecture to outcomes, not just technologies

## Anti-Patterns

- ❌ Data swamp: Lake without governance or cataloging
- ❌ Premature mesh: Mesh before organizational readiness
- ❌ Tool sprawl: Too many tools without integration
- ❌ No quality checks: "Garbage in, garbage out"
- ❌ Centralized bottleneck: Single team in large org (>500 people)
- ❌ Vendor lock-in: Proprietary formats without migration path
- ❌ No lineage: Can't answer "where did this come from?"
- ❌ Over-engineering: Complex architecture for simple use cases

## Integration with Other Skills

**Direct Dependencies:**
- **ingesting-data:** ETL/ELT mechanics, Fivetran, Airbyte implementation
- **data-transformation:** dbt and Dataform detailed implementation
- **streaming-data:** Kafka, Flink for real-time pipelines

**Complementary:**
- **databases-relational:** PostgreSQL, MySQL as source systems
- **databases-document:** MongoDB, DynamoDB as sources
- **ai-data-engineering:** Feature stores, ML training pipelines
- **designing-distributed-systems:** CAP theorem, consistency models
- **observability:** Monitoring pipeline health, data quality metrics

**Downstream:**
- **visualizing-data:** BI and dashboard patterns
- **sql-optimization:** Query performance tuning

**Common Workflows:**

**End-to-End Analytics:**
```
data-architecture (warehouse) → ingesting-data (Fivetran) →
data-transformation (dbt) → visualizing-data (Tableau)
```

**Data Platform for AI/ML:**
```
data-architecture (lakehouse) → ingesting-data (Kafka) →
data-transformation (dbt features) → ai-data-engineering (feature store)
```

## Further Reading

**Reference Files:**
- [decision-frameworks.md](references/decision-frameworks.md) - All 4 decision frameworks in detail
- [storage-paradigms.md](references/storage-paradigms.md) - Lake vs warehouse vs lakehouse
- [modeling-approaches.md](references/modeling-approaches.md) - Dimensional, normalized, data vault, wide
- [data-mesh-guide.md](references/data-mesh-guide.md) - Data mesh principles and implementation
- [medallion-pattern.md](references/medallion-pattern.md) - Bronze, silver, gold layers
- [table-formats.md](references/table-formats.md) - Iceberg, Delta Lake, Hudi comparison
- [tool-recommendations.md](references/tool-recommendations.md) - Tool analysis and recommendations
- [modern-data-stack.md](references/modern-data-stack.md) - Tool categories and selection
- [governance-patterns.md](references/governance-patterns.md) - Catalog, lineage, quality, access control
- [scenarios.md](references/scenarios.md) - Startup, enterprise, data mesh scenarios

**Examples:**
- [examples/dbt-project/](examples/dbt-project/) - dbt project with medallion architecture

**External Resources:**
- Apache Iceberg: https://iceberg.apache.org/
- dbt Documentation: https://docs.getdbt.com/
- Data Mesh (Zhamak Dehghani): https://www.datamesh-architecture.com/
- Databricks Medallion: https://www.databricks.com/glossary/medallion-architecture
