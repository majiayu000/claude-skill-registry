---
name: warehouse-optimization
description: Query optimization, partitioning, clustering, and warehouse tuning.
---

# Warehouse Optimization

## Partitioning

```sql
-- Snowflake: Automatic clustering
ALTER TABLE fct_sales
CLUSTER BY (date_key, store_key);

-- BigQuery: Partition by date
CREATE TABLE fct_sales
PARTITION BY DATE(ordered_at)
CLUSTER BY store_id, product_id;

-- Redshift: Distribution and sort keys
CREATE TABLE fct_sales (
    ...
)
DISTKEY(store_id)
SORTKEY(ordered_at, store_id);
```

## Query Optimization

### Use EXPLAIN

```sql
EXPLAIN ANALYZE
SELECT ...
FROM fct_sales
WHERE date_key BETWEEN 20240101 AND 20240131;
```

### Common Issues

| Problem | Solution |
|---------|----------|
| Full table scan | Add partition filter |
| Skewed joins | Redistribute data |
| Large sorts | Pre-aggregate |
| Too many columns | Select only needed |

### Efficient Joins

```sql
-- ❌ Bad: Large table on left
SELECT * FROM fct_sales s
JOIN dim_date d ON s.date_key = d.date_key;

-- ✅ Good: Small table on left (broadcast)
SELECT * FROM dim_date d
JOIN fct_sales s ON d.date_key = s.date_key;
```

## Materialized Views

```sql
CREATE MATERIALIZED VIEW mv_daily_sales AS
SELECT
    date_key,
    store_key,
    SUM(amount) as total_sales,
    COUNT(*) as transaction_count
FROM fct_sales
GROUP BY 1, 2;
```

## Cost Management

- Monitor credit/byte usage
- Set query timeouts
- Use warehouse scheduling
- Archive old partitions
- Implement query tagging
