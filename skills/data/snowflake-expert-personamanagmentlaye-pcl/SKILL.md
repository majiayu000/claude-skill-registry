---
name: snowflake-expert
version: 1.0.0
description: Expert-level Snowflake data warehouse platform, virtual warehouses, data sharing, streams, tasks, and SQL optimization
category: data
author: PCL Team
license: Apache-2.0
tags:
  - snowflake
  - data-warehouse
  - sql
  - analytics
  - cloud
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
requirements:
  snowflake-connector-python: ">=3.0.0"
---

# Snowflake Expert

You are an expert in Snowflake with deep knowledge of virtual warehouses, data sharing, streams, tasks, time travel, zero-copy cloning, and SQL optimization. You design and manage enterprise-scale data warehouses that are performant, cost-effective, and secure.

## Core Expertise

### Architecture and Virtual Warehouses

**Virtual Warehouse Management:**
```sql
-- Create virtual warehouse
CREATE WAREHOUSE analytics_wh
WITH
    WAREHOUSE_SIZE = 'MEDIUM'
    AUTO_SUSPEND = 300
    AUTO_RESUME = TRUE
    MIN_CLUSTER_COUNT = 1
    MAX_CLUSTER_COUNT = 4
    SCALING_POLICY = 'STANDARD'
    COMMENT = 'Warehouse for analytics workloads';

-- Alter warehouse
ALTER WAREHOUSE analytics_wh SET
    WAREHOUSE_SIZE = 'LARGE'
    MAX_CLUSTER_COUNT = 6;

-- Suspend and resume
ALTER WAREHOUSE analytics_wh SUSPEND;
ALTER WAREHOUSE analytics_wh RESUME;

-- Drop warehouse
DROP WAREHOUSE analytics_wh;

-- Show warehouses
SHOW WAREHOUSES;

-- Query warehouse metrics
SELECT
    warehouse_name,
    avg_running,
    avg_queued_load,
    avg_queued_provisioning
FROM SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_LOAD_HISTORY
WHERE start_time >= DATEADD(day, -7, CURRENT_TIMESTAMP())
ORDER BY start_time DESC;
```

**Resource Monitors:**
```sql
-- Create resource monitor
CREATE RESOURCE MONITOR monthly_limit
WITH
    CREDIT_QUOTA = 1000
    FREQUENCY = MONTHLY
    START_TIMESTAMP = IMMEDIATELY
    TRIGGERS
        ON 75 PERCENT DO NOTIFY
        ON 90 PERCENT DO SUSPEND
        ON 100 PERCENT DO SUSPEND_IMMEDIATE;

-- Assign to warehouse
ALTER WAREHOUSE analytics_wh
SET RESOURCE_MONITOR = monthly_limit;

-- Show monitors
SHOW RESOURCE MONITORS;
```

### Database Objects and Organization

**Multi-Cluster Architecture:**
```sql
-- Create database hierarchy
CREATE DATABASE production;
CREATE SCHEMA production.sales;
CREATE SCHEMA production.marketing;

-- Create tables
CREATE TABLE production.sales.orders (
    order_id NUMBER AUTOINCREMENT,
    customer_id NUMBER NOT NULL,
    order_date TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    total_amount NUMBER(12,2),
    status VARCHAR(20),
    metadata VARIANT,
    PRIMARY KEY (order_id)
);

-- Create external table
CREATE EXTERNAL TABLE production.sales.external_orders
WITH LOCATION = @my_s3_stage/orders/
FILE_FORMAT = (TYPE = PARQUET)
AUTO_REFRESH = TRUE
PATTERN = '.*orders_.*[.]parquet';

-- Create materialized view
CREATE MATERIALIZED VIEW production.sales.daily_summary AS
SELECT
    DATE(order_date) AS order_date,
    status,
    COUNT(*) AS order_count,
    SUM(total_amount) AS total_amount
FROM production.sales.orders
GROUP BY DATE(order_date), status;

-- Refresh materialized view
ALTER MATERIALIZED VIEW production.sales.daily_summary REFRESH;
```

**Clustering and Partitioning:**
```sql
-- Create table with clustering
CREATE TABLE events (
    event_id NUMBER,
    event_date DATE,
    event_type VARCHAR(50),
    user_id NUMBER,
    data VARIANT
)
CLUSTER BY (event_date, event_type);

-- Add clustering to existing table
ALTER TABLE events CLUSTER BY (event_date, event_type);

-- Check clustering information
SELECT
    SYSTEM$CLUSTERING_INFORMATION('events', '(event_date, event_type)');

-- Automatic clustering
ALTER TABLE events RESUME RECLUSTER;
ALTER TABLE events SUSPEND RECLUSTER;

-- Search optimization
ALTER TABLE events ADD SEARCH OPTIMIZATION;
ALTER TABLE events DROP SEARCH OPTIMIZATION;
```

### Data Loading and Stages

**Stage Management:**
```sql
-- Create internal stage
CREATE STAGE my_internal_stage
    FILE_FORMAT = (TYPE = CSV FIELD_DELIMITER = ',' SKIP_HEADER = 1);

-- Create external stage (S3)
CREATE STAGE my_s3_stage
    URL = 's3://mybucket/path/'
    CREDENTIALS = (AWS_KEY_ID = 'xxx' AWS_SECRET_KEY = 'yyy')
    FILE_FORMAT = (TYPE = PARQUET);

-- Create external stage (Azure)
CREATE STAGE my_azure_stage
    URL = 'azure://myaccount.blob.core.windows.net/mycontainer/path/'
    CREDENTIALS = (AZURE_SAS_TOKEN = 'xxx')
    FILE_FORMAT = (TYPE = JSON);

-- List files in stage
LIST @my_s3_stage;

-- Remove files from stage
REMOVE @my_internal_stage PATTERN = '.*.csv';
```

**Data Loading with COPY:**
```sql
-- Load from stage
COPY INTO production.sales.orders
FROM @my_s3_stage/orders/
FILE_FORMAT = (TYPE = CSV FIELD_DELIMITER = ',' SKIP_HEADER = 1)
ON_ERROR = 'CONTINUE'
PURGE = TRUE;

-- Load with transformation
COPY INTO production.sales.orders (order_id, customer_id, order_date, total_amount)
FROM (
    SELECT
        $1::NUMBER,
        $2::NUMBER,
        $3::TIMESTAMP_NTZ,
        $4::NUMBER(12,2)
    FROM @my_s3_stage/orders/
)
FILE_FORMAT = (TYPE = CSV)
ON_ERROR = 'SKIP_FILE';

-- Load JSON
COPY INTO raw_events
FROM @my_s3_stage/events/
FILE_FORMAT = (TYPE = JSON)
MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE;

-- Load with validation
COPY INTO production.sales.orders
FROM @my_s3_stage/orders/
FILE_FORMAT = (TYPE = CSV)
VALIDATION_MODE = 'RETURN_ERRORS';

-- Check load history
SELECT
    file_name,
    status,
    row_count,
    row_parsed,
    error_count,
    first_error
FROM TABLE(INFORMATION_SCHEMA.COPY_HISTORY(
    TABLE_NAME => 'production.sales.orders',
    START_TIME => DATEADD(hours, -24, CURRENT_TIMESTAMP())
));
```

**Snowpipe for Continuous Loading:**
```sql
-- Create pipe
CREATE PIPE production.sales.orders_pipe
    AUTO_INGEST = TRUE
    AWS_SNS_TOPIC = 'arn:aws:sns:us-east-1:123456789012:my-topic'
AS
    COPY INTO production.sales.orders
    FROM @my_s3_stage/orders/
    FILE_FORMAT = (TYPE = CSV);

-- Show pipe status
SHOW PIPES;

-- Check pipe status
SELECT SYSTEM$PIPE_STATUS('production.sales.orders_pipe');

-- Pause and resume pipe
ALTER PIPE production.sales.orders_pipe SET PIPE_EXECUTION_PAUSED = TRUE;
ALTER PIPE production.sales.orders_pipe SET PIPE_EXECUTION_PAUSED = FALSE;

-- Refresh pipe (manually trigger)
ALTER PIPE production.sales.orders_pipe REFRESH;
```

### Streams and Tasks

**Change Data Capture with Streams:**
```sql
-- Create stream on table
CREATE STREAM orders_stream ON TABLE production.sales.orders;

-- Query stream
SELECT
    order_id,
    customer_id,
    total_amount,
    METADATA$ACTION AS dml_action,
    METADATA$ISUPDATE AS is_update,
    METADATA$ROW_ID AS row_id
FROM orders_stream;

-- Consume stream in merge
MERGE INTO production.sales.orders_summary t
USING orders_stream s
ON t.order_id = s.order_id
WHEN MATCHED AND s.METADATA$ACTION = 'DELETE' THEN DELETE
WHEN MATCHED THEN UPDATE SET
    t.total_amount = s.total_amount,
    t.status = s.status
WHEN NOT MATCHED AND s.METADATA$ACTION != 'DELETE' THEN INSERT
    (order_id, customer_id, total_amount, status)
VALUES
    (s.order_id, s.customer_id, s.total_amount, s.status);

-- Stream on view
CREATE STREAM orders_view_stream ON VIEW production.sales.orders_v;

-- Show streams
SHOW STREAMS;

-- Check stream offset
SELECT SYSTEM$STREAM_HAS_DATA('orders_stream');
```

**Task Automation:**
```sql
-- Create task
CREATE TASK process_orders
    WAREHOUSE = analytics_wh
    SCHEDULE = '5 MINUTE'
AS
    INSERT INTO production.sales.processed_orders
    SELECT * FROM production.sales.orders
    WHERE processed = FALSE;

-- Task with stream consumption
CREATE TASK process_order_changes
    WAREHOUSE = analytics_wh
    SCHEDULE = '1 MINUTE'
WHEN
    SYSTEM$STREAM_HAS_DATA('orders_stream')
AS
    MERGE INTO production.sales.orders_summary t
    USING orders_stream s
    ON t.order_id = s.order_id
    WHEN MATCHED THEN UPDATE SET t.total_amount = s.total_amount;

-- Task with dependencies
CREATE TASK parent_task
    WAREHOUSE = analytics_wh
    SCHEDULE = '60 MINUTE'
AS
    INSERT INTO staging_table SELECT * FROM source_table;

CREATE TASK child_task
    WAREHOUSE = analytics_wh
    AFTER parent_task
AS
    INSERT INTO final_table SELECT * FROM staging_table;

-- Resume and suspend tasks
ALTER TASK process_orders RESUME;
ALTER TASK process_orders SUSPEND;

-- Show tasks
SHOW TASKS;

-- Check task history
SELECT
    name,
    state,
    scheduled_time,
    completed_time,
    error_code,
    error_message
FROM TABLE(INFORMATION_SCHEMA.TASK_HISTORY(
    TASK_NAME => 'process_orders',
    SCHEDULED_TIME_RANGE_START => DATEADD(hours, -24, CURRENT_TIMESTAMP())
))
ORDER BY scheduled_time DESC;
```

### Time Travel and Zero-Copy Cloning

**Time Travel:**
```sql
-- Query historical data
SELECT * FROM orders AT(OFFSET => -300); -- 5 minutes ago
SELECT * FROM orders BEFORE(STATEMENT => '01a1b2c3-0001-4567-8901-234567890abc');
SELECT * FROM orders AT(TIMESTAMP => '2024-01-15 10:00:00'::TIMESTAMP);

-- Restore table
CREATE TABLE orders_restored CLONE orders AT(TIMESTAMP => '2024-01-15 09:00:00'::TIMESTAMP);

-- Undrop table
UNDROP TABLE orders;

-- Set data retention
ALTER TABLE orders SET DATA_RETENTION_TIME_IN_DAYS = 7;

-- Check retention
SHOW PARAMETERS LIKE 'DATA_RETENTION_TIME_IN_DAYS' FOR TABLE orders;
```

**Zero-Copy Cloning:**
```sql
-- Clone table
CREATE TABLE orders_dev CLONE orders;

-- Clone schema
CREATE SCHEMA dev_schema CLONE production.sales;

-- Clone database
CREATE DATABASE dev_db CLONE production;

-- Clone with time travel
CREATE TABLE orders_snapshot CLONE orders AT(TIMESTAMP => '2024-01-15 00:00:00'::TIMESTAMP);

-- Swap tables (blue-green deployment)
ALTER TABLE orders SWAP WITH orders_new;
```

### Data Sharing

**Secure Data Sharing:**
```sql
-- Create share (provider)
CREATE SHARE sales_share;
GRANT USAGE ON DATABASE production TO SHARE sales_share;
GRANT USAGE ON SCHEMA production.sales TO SHARE sales_share;
GRANT SELECT ON TABLE production.sales.orders TO SHARE sales_share;

-- Add consumer account
ALTER SHARE sales_share ADD ACCOUNTS = xy12345;

-- Show shares
SHOW SHARES;

-- Revoke access
ALTER SHARE sales_share REMOVE ACCOUNTS = xy12345;

-- Consumer: Create database from share
CREATE DATABASE shared_sales FROM SHARE provider_account.sales_share;

-- Use shared data
SELECT * FROM shared_sales.sales.orders;
```

**Secure Views for Sharing:**
```sql
-- Create secure view
CREATE SECURE VIEW production.sales.orders_public AS
SELECT
    order_id,
    order_date,
    total_amount,
    CASE
        WHEN CURRENT_ROLE() = 'ADMIN' THEN customer_id
        ELSE NULL
    END AS customer_id
FROM production.sales.orders;

-- Share secure view
GRANT SELECT ON VIEW production.sales.orders_public TO SHARE sales_share;
```

### Advanced SQL and Optimization

**Semi-Structured Data (VARIANT):**
```sql
-- Query JSON data
SELECT
    data:user_id::NUMBER AS user_id,
    data:email::STRING AS email,
    data:metadata.source::STRING AS source,
    data:tags[0]::STRING AS first_tag
FROM events;

-- Flatten nested arrays
SELECT
    event_id,
    f.value:product_id::NUMBER AS product_id,
    f.value:quantity::NUMBER AS quantity
FROM events,
LATERAL FLATTEN(input => data:items) f;

-- Parse JSON
SELECT
    PARSE_JSON('{"name": "Alice", "age": 30}') AS json_data;

-- Object construction
SELECT
    OBJECT_CONSTRUCT(
        'order_id', order_id,
        'total', total_amount,
        'status', status
    ) AS order_json
FROM orders;

-- Array aggregation
SELECT
    customer_id,
    ARRAY_AGG(OBJECT_CONSTRUCT('order_id', order_id, 'amount', total_amount)) AS orders
FROM orders
GROUP BY customer_id;
```

**Window Functions and Analytics:**
```sql
-- Running total
SELECT
    order_date,
    total_amount,
    SUM(total_amount) OVER (ORDER BY order_date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_total
FROM orders;

-- Percentile
SELECT
    customer_id,
    total_amount,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY total_amount) OVER (PARTITION BY customer_id) AS median_amount
FROM orders;

-- Lead/Lag with ignore nulls
SELECT
    order_date,
    revenue,
    LAG(revenue) IGNORE NULLS OVER (ORDER BY order_date) AS previous_revenue
FROM daily_revenue;
```

**Query Optimization:**
```sql
-- Use result cache
ALTER SESSION SET USE_CACHED_RESULT = TRUE;

-- Partition pruning
SELECT * FROM orders
WHERE order_date BETWEEN '2024-01-01' AND '2024-01-31';

-- Clustering helps with partition pruning
ALTER TABLE orders CLUSTER BY (order_date);

-- Use materialized views for common queries
CREATE MATERIALIZED VIEW monthly_summary AS
SELECT
    DATE_TRUNC('month', order_date) AS month,
    COUNT(*) AS order_count,
    SUM(total_amount) AS total_amount
FROM orders
GROUP BY DATE_TRUNC('month', order_date);

-- Query profile analysis
ALTER SESSION SET QUERY_TAG = 'daily_report';
SELECT * FROM orders WHERE order_date = CURRENT_DATE();

-- Check query history
SELECT
    query_id,
    query_text,
    execution_time,
    warehouse_size,
    bytes_scanned
FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
WHERE query_tag = 'daily_report'
ORDER BY start_time DESC
LIMIT 10;
```

### Access Control and Security

**Role-Based Access Control:**
```sql
-- Create roles
CREATE ROLE data_engineer;
CREATE ROLE data_analyst;
CREATE ROLE data_viewer;

-- Grant privileges
GRANT USAGE ON DATABASE production TO ROLE data_analyst;
GRANT USAGE ON SCHEMA production.sales TO ROLE data_analyst;
GRANT SELECT ON ALL TABLES IN SCHEMA production.sales TO ROLE data_analyst;
GRANT SELECT ON FUTURE TABLES IN SCHEMA production.sales TO ROLE data_analyst;

-- Role hierarchy
GRANT ROLE data_viewer TO ROLE data_analyst;
GRANT ROLE data_analyst TO ROLE data_engineer;

-- Assign role to user
GRANT ROLE data_analyst TO USER alice;

-- Set default role
ALTER USER alice SET DEFAULT_ROLE = data_analyst;

-- Switch role
USE ROLE data_analyst;
```

**Row-Level Security:**
```sql
-- Create row access policy
CREATE ROW ACCESS POLICY region_policy AS (region_column STRING)
RETURNS BOOLEAN ->
    CASE
        WHEN CURRENT_ROLE() = 'ADMIN' THEN TRUE
        WHEN CURRENT_ROLE() = 'SALES_US' THEN region_column = 'US'
        WHEN CURRENT_ROLE() = 'SALES_EU' THEN region_column = 'EU'
        ELSE FALSE
    END;

-- Apply policy to table
ALTER TABLE orders ADD ROW ACCESS POLICY region_policy ON (region);

-- Remove policy
ALTER TABLE orders DROP ROW ACCESS POLICY region_policy;
```

**Column-Level Security:**
```sql
-- Create masking policy
CREATE MASKING POLICY email_mask AS (val STRING)
RETURNS STRING ->
    CASE
        WHEN CURRENT_ROLE() IN ('ADMIN', 'COMPLIANCE') THEN val
        ELSE REGEXP_REPLACE(val, '.+@', '****@')
    END;

-- Apply masking policy
ALTER TABLE customers MODIFY COLUMN email SET MASKING POLICY email_mask;

-- Remove masking policy
ALTER TABLE customers MODIFY COLUMN email UNSET MASKING POLICY;
```

## Best Practices

### 1. Warehouse Sizing and Management
- Start with smaller warehouses and scale up as needed
- Use multi-cluster warehouses for concurrency
- Set AUTO_SUSPEND to 5-10 minutes to avoid cold starts
- Monitor credit usage with resource monitors
- Use separate warehouses for different workloads (ETL, BI, ad-hoc)

### 2. Data Organization
- Use databases for major boundaries (prod/dev/test)
- Use schemas for logical grouping
- Implement clustering for large tables (>1TB)
- Use transient tables for temporary data to reduce storage costs
- Leverage zero-copy cloning for development/testing

### 3. Cost Optimization
- Use table types appropriately (permanent, transient, temporary)
- Set data retention periods based on needs
- Monitor and drop unused objects
- Use result caching for repeated queries
- Implement query timeouts to prevent runaway queries

### 4. Performance Optimization
- Cluster large tables on commonly filtered columns
- Use materialized views for expensive aggregations
- Leverage search optimization for point lookups
- Partition pruning with proper WHERE clauses
- Monitor query profile for bottlenecks

### 5. Security and Governance
- Implement role-based access control
- Use row-level and column-level security
- Enable network policies for IP whitelisting
- Use secure views for data sharing
- Enable MFA for privileged accounts

## Anti-Patterns

### 1. Over-Clustering
```sql
-- Bad: Too many clustering keys
ALTER TABLE orders CLUSTER BY (order_date, customer_id, status, product_id);

-- Good: 1-3 columns, most selective first
ALTER TABLE orders CLUSTER BY (order_date, customer_id);
```

### 2. Undersized Warehouses
```sql
-- Bad: Using X-Small for large ETL jobs
CREATE WAREHOUSE etl_wh WITH WAREHOUSE_SIZE = 'X-SMALL';

-- Good: Appropriately sized for workload
CREATE WAREHOUSE etl_wh WITH WAREHOUSE_SIZE = 'LARGE';
```

### 3. Not Using Streams for CDC
```sql
-- Bad: Full table scan for changes
SELECT * FROM orders WHERE updated_at > LAST_PROCESSED_TIME;

-- Good: Use streams
CREATE STREAM orders_stream ON TABLE orders;
SELECT * FROM orders_stream;
```

### 4. Ignoring Query History
```sql
-- Bad: Not monitoring expensive queries
-- Good: Regular review of query history
SELECT
    query_text,
    total_elapsed_time,
    bytes_scanned
FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
WHERE execution_status = 'SUCCESS'
    AND start_time >= DATEADD(day, -7, CURRENT_TIMESTAMP())
ORDER BY total_elapsed_time DESC
LIMIT 20;
```

## Resources

- [Snowflake Documentation](https://docs.snowflake.com/)
- [Snowflake Best Practices](https://docs.snowflake.com/en/user-guide/best-practices)
- [Snowflake University](https://learn.snowflake.com/)
- [Snowflake Community](https://community.snowflake.com/)
- [Snowflake SQL Reference](https://docs.snowflake.com/en/sql-reference)
- [Snowflake Performance Optimization](https://docs.snowflake.com/en/user-guide/performance)
- [Snowflake Security](https://docs.snowflake.com/en/user-guide/security)
