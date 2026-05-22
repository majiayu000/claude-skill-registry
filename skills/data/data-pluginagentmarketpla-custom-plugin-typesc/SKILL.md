---
name: data-engineering
description: Master data engineering, ETL/ELT, data warehousing, SQL optimization, and analytics. Use when building data pipelines, designing data systems, or working with large datasets.
sasmp_version: "1.3.0"
bonded_agent: 04-data-engineering-analytics
bond_type: PRIMARY_BOND
---

# Data Engineering & Analytics Skill

## Quick Start - SQL Data Pipeline

```sql
-- Create staging table
CREATE TABLE staging_events AS
SELECT 
  event_id,
  user_id,
  event_type,
  event_time,
  properties
FROM raw_events
WHERE event_time >= CURRENT_DATE - INTERVAL '1 day'
AND event_type IN ('click', 'purchase', 'view');

-- Aggregate metrics
SELECT
  DATE(event_time) as date,
  user_id,
  COUNT(*) as event_count,
  COUNT(DISTINCT event_type) as unique_events
FROM staging_events
GROUP BY 1, 2
ORDER BY date DESC, event_count DESC;
```

## Core Technologies

### Data Processing
- Apache Spark
- Apache Flink
- Pandas / Polars
- dbt (data transformation)

### Data Warehousing
- Snowflake
- BigQuery (GCP)
- Redshift (AWS)
- Azure Synapse

### ETL/ELT Tools
- dbt
- Airflow
- Talend
- Informatica

### Streaming
- Apache Kafka
- AWS Kinesis
- Apache Pulsar

### ML & Analytics
- scikit-learn
- TensorFlow
- Tableau / Power BI

## Best Practices

1. **Data Quality** - Validation and testing
2. **Documentation** - Clear metadata
3. **Performance** - Query optimization
4. **Governance** - Data security
5. **Monitoring** - Pipeline alerts
6. **Scalability** - Design for growth
7. **Version Control** - Git for code and configs
8. **Testing** - Data and pipeline testing

## Resources

- [Apache Spark Documentation](https://spark.apache.org/)
- [dbt Documentation](https://docs.getdbt.com/)
- [SQL Mode Tutorial](https://mode.com/sql-tutorial/)
- [Kaggle](https://www.kaggle.com/)
