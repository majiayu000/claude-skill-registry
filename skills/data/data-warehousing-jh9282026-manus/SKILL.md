---
name: data-warehousing
description: "Design and implement data warehouse architectures for analytics and reporting. Use for: dimensional modeling, star and snowflake schemas, ETL design, data mart creation, slowly changing dimensions, fact table design, OLAP cubes, data warehouse optimization, cloud data warehousing (Snowflake/Redshift/BigQuery), and enterprise data architecture."
---

# Data Warehousing

Design and implement centralized data repositories optimized for analytics and business intelligence.

## Overview

Data warehousing involves creating subject-oriented, integrated, time-variant, and non-volatile collections of data to support management decision-making. This skill covers architectural patterns, dimensional modeling techniques, implementation strategies, and best practices for building scalable, performant data warehouses.

## Data Warehouse Architecture

### Three-Tier Architecture

**Data Source Layer**: Operational databases, external sources, files
**Staging Layer**: Temporary storage for ETL processing
**Data Warehouse Layer**: Integrated, historical data storage
**Data Mart Layer**: Department-specific subsets
**Presentation Layer**: BI tools, reports, dashboards

### Cloud Data Warehouse Architectures

| Platform | Architecture | Key Features |
|----------|--------------|--------------|
| Snowflake | Multi-cluster shared data | Separation of storage and compute, auto-scaling |
| Amazon Redshift | Massively parallel processing | Columnar storage, integration with AWS ecosystem |
| Google BigQuery | Serverless | Automatic scaling, pay-per-query, ML integration |
| Azure Synapse | Unified analytics | Integration with Power BI, data lake support |

## Dimensional Modeling

### Star Schema

Central fact table surrounded by dimension tables:
- **Fact Table**: Measures/metrics (sales amount, quantity, profit)
- **Dimension Tables**: Descriptive attributes (customer, product, time, location)
- **Benefits**: Simple queries, fast aggregations, easy to understand
- **Use Case**: Most common pattern for data warehouses

**Example**:
```
Fact_Sales (fact table)
- sale_id (PK)
- date_key (FK)
- product_key (FK)
- customer_key (FK)
- store_key (FK)
- sales_amount
- quantity
- profit

Dim_Date, Dim_Product, Dim_Customer, Dim_Store (dimension tables)
```

### Snowflake Schema

Normalized dimension tables with sub-dimensions:
- **Benefits**: Reduced redundancy, smaller storage footprint
- **Drawbacks**: More complex queries, more joins
- **Use Case**: When storage is premium or dimensions are highly hierarchical

### Fact Table Types

**Transaction Fact Table**: One row per transaction (most granular)
**Periodic Snapshot**: Regular intervals (daily, monthly balances)
**Accumulating Snapshot**: Process lifecycle (order to delivery)
**Factless Fact Table**: Events without measures (attendance, coverage)

### Dimension Table Design

**Attributes**:
- Natural key (business key)
- Surrogate key (system-generated)
- Descriptive attributes
- Hierarchies (category > subcategory > product)

**Slowly Changing Dimensions (SCD)**:

**Type 1**: Overwrite (no history)
```sql
UPDATE Dim_Customer
SET city = 'New York'
WHERE customer_id = 123;
```

**Type 2**: Add new row (full history)
```sql
-- Old row
customer_key | customer_id | name | city | effective_date | end_date | is_current
1 | 123 | John | Boston | 2025-01-01 | 2026-03-15 | N

-- New row
2 | 123 | John | New York | 2026-03-16 | 9999-12-31 | Y
```

**Type 3**: Add new column (limited history)
```sql
customer_key | customer_id | name | current_city | previous_city
1 | 123 | John | New York | Boston
```

## ETL vs ELT

### ETL (Extract, Transform, Load)

Transform data before loading into warehouse:
- **Pros**: Clean data in warehouse, less storage needed
- **Cons**: Slower, less flexible, transformation bottleneck
- **Use Case**: Traditional on-premise warehouses

### ELT (Extract, Load, Transform)

Load raw data, transform in warehouse:
- **Pros**: Faster loading, leverage warehouse compute, more flexible
- **Cons**: More storage needed, raw data in warehouse
- **Use Case**: Modern cloud warehouses with powerful compute

## Data Warehouse Design Patterns

### Kimball Methodology (Bottom-Up)

1. Select business process
2. Declare grain (level of detail)
3. Identify dimensions
4. Identify facts
5. Build dimensional model
6. Aggregate to data marts

**Benefits**: Faster time to value, business-focused
**Drawbacks**: Potential redundancy across marts

### Inmon Methodology (Top-Down)

1. Build enterprise data model
2. Create normalized data warehouse
3. Build data marts from warehouse

**Benefits**: Single source of truth, less redundancy
**Drawbacks**: Longer implementation time, more complex

### Data Vault

Hybrid approach with three table types:
- **Hubs**: Business keys
- **Links**: Relationships between hubs
- **Satellites**: Descriptive attributes and history

**Benefits**: Highly flexible, audit trail, parallel loading
**Use Case**: Complex, frequently changing environments

## Implementation Best Practices

### Grain Definition

Define the lowest level of detail in fact tables:
- **Too granular**: Performance issues, excessive storage
- **Too aggregated**: Loss of analytical flexibility
- **Right grain**: Balance between detail and performance

### Surrogate Keys

Use system-generated keys instead of natural keys:
- **Benefits**: Performance, handles changes, independence from source
- **Implementation**: Auto-increment integers or UUIDs

### Indexing Strategy

**Fact Tables**:
- Clustered index on date (most common filter)
- Non-clustered indexes on foreign keys
- Columnstore indexes for analytics (SQL Server, Synapse)

**Dimension Tables**:
- Clustered index on surrogate key
- Non-clustered index on natural key
- Consider covering indexes for common queries

### Partitioning

Divide large tables into smaller, manageable pieces:
- **Range Partitioning**: By date (most common)
- **List Partitioning**: By category or region
- **Hash Partitioning**: Distribute evenly
- **Benefits**: Faster queries, easier maintenance, parallel processing

## Data Quality and Governance

### Data Quality Checks

- **Completeness**: No missing required values
- **Accuracy**: Data matches source
- **Consistency**: Same data across systems
- **Timeliness**: Data is current
- **Validity**: Data conforms to business rules

### Metadata Management

Document and track:
- Data lineage (source to destination)
- Business definitions
- Transformation rules
- Data ownership
- Refresh schedules
- Usage statistics

### Security

- **Row-Level Security**: Filter data by user
- **Column-Level Security**: Mask sensitive columns
- **Encryption**: At rest and in transit
- **Audit Logging**: Track access and changes

## Performance Optimization

### Query Optimization

- Use appropriate indexes
- Partition large tables
- Materialize common aggregations
- Use columnar storage for analytics
- Implement query result caching

### Storage Optimization

- Compress data (columnar compression)
- Archive old data
- Use appropriate data types
- Remove unused indexes
- Implement data retention policies

### Incremental Loading

Load only new or changed data:
- **Timestamp-based**: Track last modified date
- **Change Data Capture (CDC)**: Capture changes from source
- **Delta Detection**: Compare current vs previous state

## Cloud Data Warehouse Features

### Snowflake

**Virtual Warehouses**: Independent compute clusters
**Time Travel**: Query historical data (up to 90 days)
**Zero-Copy Cloning**: Instant table/database copies
**Data Sharing**: Share live data across accounts

### Amazon Redshift

**Spectrum**: Query data in S3 without loading
**Concurrency Scaling**: Auto-scale for concurrent queries
**Materialized Views**: Pre-computed aggregations
**Federated Query**: Query across Redshift and RDS

### Google BigQuery

**Partitioning**: By date or integer range
**Clustering**: Organize data within partitions
**BI Engine**: In-memory analysis
**ML Integration**: Train models with SQL

## Modern Data Warehouse Patterns

### Lambda Architecture

**Batch Layer**: Historical data processing
**Speed Layer**: Real-time data processing
**Serving Layer**: Merge batch and real-time views

### Kappa Architecture

Simplified Lambda with only streaming:
- All data treated as stream
- Single processing pipeline
- Reprocess from stream for corrections

### Data Lakehouse

Combine data lake and warehouse:
- Store raw data in data lake (S3, ADLS, GCS)
- Apply schema and governance
- Query with SQL engines (Databricks, Synapse)
- Support both BI and ML workloads

## Using the Reference Files

### When to Read Each Reference

**`/references/dimensional-modeling-patterns.md`** — Read when designing fact and dimension tables, implementing SCDs, or choosing between star and snowflake schemas.

**`/references/cloud-warehouse-comparison.md`** — Read when selecting a cloud data warehouse platform or optimizing for specific cloud features.

**`/references/performance-tuning.md`** — Read when optimizing query performance, implementing partitioning strategies, or troubleshooting slow queries.
