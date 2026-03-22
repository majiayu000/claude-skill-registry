---
name: data-pipeline
description: "Data pipeline and ETL automation - extract, transform, load workflows for data integration and analytics"
version: "1.0.0"
author: claude-office-skills
license: MIT

category: data
tags:
  - etl
  - data-pipeline
  - integration
  - analytics
  - automation
department: Data Engineering

models:
  recommended:
    - claude-sonnet-4

mcp:
  server: data-mcp
  tools:
    - database_query
    - api_fetch
    - spreadsheet_write
    - file_transform

capabilities:
  - data_extraction
  - transformation
  - loading
  - scheduling
  - monitoring

languages:
  - en
  - zh

related_skills:
  - sheets-automation
  - data-analysis
  - airtable-automation
---

# Data Pipeline

Build data pipelines and ETL workflows for data integration, transformation, and analytics automation. Based on n8n's data workflow templates.

## Overview

This skill covers:
- Data extraction from multiple sources
- Transformation and cleaning
- Loading to destinations
- Scheduling and monitoring
- Error handling and alerts

---

## ETL Patterns

### Basic ETL Flow

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   EXTRACT   │───▶│  TRANSFORM  │───▶│    LOAD     │
│             │    │             │    │             │
│ • APIs      │    │ • Clean     │    │ • Database  │
│ • Databases │    │ • Map       │    │ • Warehouse │
│ • Files     │    │ • Aggregate │    │ • Files     │
│ • Webhooks  │    │ • Enrich    │    │ • APIs      │
└─────────────┘    └─────────────┘    └─────────────┘
```

### n8n ETL Workflow

```yaml
workflow: "Daily Sales ETL"
schedule: "2am daily"

nodes:
  # EXTRACT
  - name: "Extract from Shopify"
    type: shopify
    action: get_orders
    filter: created_at >= yesterday
    
  - name: "Extract from Stripe"
    type: stripe
    action: get_payments
    filter: created >= yesterday
    
  # TRANSFORM
  - name: "Merge Data"
    type: merge
    mode: combine_by_key
    key: order_id
    
  - name: "Transform"
    type: code
    code: |
      return items.map(item => ({
        date: item.created_at.split('T')[0],
        order_id: item.id,
        customer_email: item.email,
        total: parseFloat(item.total_price),
        currency: item.currency,
        items: item.line_items.length,
        source: item.source_name,
        payment_status: item.payment.status
      }));
      
  # LOAD
  - name: "Load to BigQuery"
    type: google_bigquery
    action: insert_rows
    table: sales_daily
    
  - name: "Update Google Sheets"
    type: google_sheets
    action: append_rows
    spreadsheet: "Daily Sales Report"
```

---

## Data Sources

### Common Extractors

```yaml
extractors:
  databases:
    - postgresql:
        connection: connection_string
        query: "SELECT * FROM orders WHERE date >= $1"
        
    - mysql:
        connection: connection_string
        query: custom_sql
        
    - mongodb:
        connection: connection_string
        collection: orders
        filter: {date: {$gte: yesterday}}
        
  apis:
    - rest_api:
        url: "https://api.example.com/data"
        method: GET
        headers: {Authorization: "Bearer {token}"}
        pagination: handle_automatically
        
    - graphql:
        url: "https://api.example.com/graphql"
        query: graphql_query
        
  files:
    - csv:
        source: sftp/s3/google_drive
        delimiter: ","
        encoding: utf-8
        
    - excel:
        source: file_path
        sheet: "Sheet1"
        
    - json:
        source: api/file
        path: "data.items"
        
  saas:
    - salesforce: get_objects
    - hubspot: get_contacts/deals
    - stripe: get_charges
    - shopify: get_orders
```

---

## Transformations

### Common Transformations

```yaml
transformations:
  cleaning:
    - remove_nulls: drop_or_fill
    - trim_whitespace: all_string_fields
    - deduplicate: by_key
    - validate: against_schema
    
  mapping:
    - rename_fields: {old_name: new_name}
    - convert_types: {date_string: date}
    - map_values: {status_code: status_name}
    
  aggregation:
    - group_by: [date, category]
    - sum: [revenue, quantity]
    - count: orders
    - average: order_value
    
  enrichment:
    - lookup: from_reference_table
    - geocode: from_address
    - calculate: derived_fields
    
  filtering:
    - where: condition
    - limit: n_rows
    - sample: percentage
```

### Code Transform Examples

```javascript
// Clean and normalize data
function transform(items) {
  return items.map(item => ({
    // Clean strings
    name: item.name?.trim().toLowerCase(),
    
    // Parse dates
    date: new Date(item.created_at).toISOString().split('T')[0],
    
    // Convert types
    amount: parseFloat(item.amount) || 0,
    
    // Map values
    status: statusMap[item.status_code] || 'unknown',
    
    // Calculate fields
    total: item.quantity * item.unit_price,
    
    // Filter nested
    tags: item.tags?.filter(t => t.active).map(t => t.name),
    
    // Default values
    source: item.source || 'direct'
  }));
}

// Aggregate data
function aggregate(items) {
  const grouped = {};
  
  items.forEach(item => {
    const key = `${item.date}_${item.category}`;
    if (!grouped[key]) {
      grouped[key] = {
        date: item.date,
        category: item.category,
        total_revenue: 0,
        order_count: 0
      };
    }
    grouped[key].total_revenue += item.amount;
    grouped[key].order_count += 1;
  });
  
  return Object.values(grouped);
}
```

---

## Data Destinations

### Common Loaders

```yaml
loaders:
  data_warehouses:
    - bigquery:
        project: project_id
        dataset: analytics
        table: sales
        write_mode: append/truncate
        
    - snowflake:
        account: account_id
        warehouse: compute_wh
        database: analytics
        schema: public
        
    - redshift:
        cluster: cluster_id
        database: analytics
        
  databases:
    - postgresql:
        upsert: on_conflict_update
        
    - mysql:
        batch_insert: 1000_rows
        
  files:
    - s3:
        bucket: data-lake
        path: /processed/{date}/
        format: parquet
        
    - google_cloud_storage:
        bucket: data-bucket
        
  spreadsheets:
    - google_sheets:
        mode: append/overwrite
        
    - airtable:
        base: base_id
        table: table_name
        
  apis:
    - webhook:
        url: destination_url
        batch_size: 100
```

---

## Scheduling & Monitoring

### Pipeline Scheduling

```yaml
scheduling:
  patterns:
    hourly:
      cron: "0 * * * *"
      use_for: real_time_dashboards
      
    daily:
      cron: "0 2 * * *"
      use_for: daily_reports
      
    weekly:
      cron: "0 3 * * 1"
      use_for: weekly_summaries
      
    on_demand:
      trigger: webhook/manual
      use_for: ad_hoc_analysis
      
  dependencies:
    - pipeline_a: must_complete_before pipeline_b
    - wait_for: all_extracts_complete
    
  retries:
    max_attempts: 3
    delay: exponential_backoff
    alert_on: final_failure
```

### Monitoring & Alerts

```yaml
monitoring:
  metrics:
    - rows_processed
    - execution_time
    - error_count
    - data_freshness
    
  alerts:
    pipeline_failed:
      channels: [slack, pagerduty]
      template: |
        🚨 *Pipeline Failed*
        
        Pipeline: {pipeline_name}
        Stage: {failed_stage}
        Error: {error_message}
        
        [View Logs]({logs_url})
        
    data_quality:
      trigger: anomaly_detected
      conditions:
        - row_count: differs_by > 50%
        - null_rate: exceeds_threshold
        - schema: changed_unexpectedly
        
    stale_data:
      trigger: last_update > threshold
      threshold: 2_hours
```

---

## Data Quality

### Quality Checks

```yaml
data_quality:
  schema_validation:
    - required_fields: [id, date, amount]
    - field_types:
        id: integer
        date: date
        amount: number
    - allowed_values:
        status: [active, pending, closed]
        
  statistical_checks:
    - null_rate: < 5%
    - duplicate_rate: < 1%
    - value_range:
        amount: [0, 1000000]
        
  business_rules:
    - total_equals_sum_of_line_items
    - dates_are_not_in_future
    - email_format_valid
    
  trend_analysis:
    - row_count: within_2_std_of_mean
    - total_value: within_expected_range
```

---

## Output Example

**Request**: "Create a daily sales data pipeline"

**Output**:

```markdown
# Daily Sales Data Pipeline

## Pipeline Overview

```
Shopify + Stripe → Transform → BigQuery + Sheets
```

## Schedule
- Runs: 2am daily
- Timezone: UTC
- Retry: 3 attempts

## Extract

### Shopify Orders
```yaml
source: shopify
filter: created_at >= yesterday
fields: [id, email, total_price, line_items, created_at]
```

### Stripe Payments
```yaml
source: stripe
filter: created >= yesterday
fields: [id, amount, status, metadata.order_id]
```

## Transform

```javascript
// Join and clean data
{
  date: order.created_at.split('T')[0],
  order_id: order.id,
  customer: order.email,
  revenue: parseFloat(order.total_price),
  items: order.line_items.length,
  payment_status: payment.status
}
```

## Load

### BigQuery
- Table: `analytics.sales_daily`
- Mode: Append

### Google Sheets
- Sheet: "Daily Sales Dashboard"
- Tab: "Raw Data"

## Quality Checks
- [ ] Row count > 0
- [ ] No null order_ids
- [ ] Revenue sum matches Stripe

## Alerts
- Slack: #data-alerts
- On failure: @data-team
```

---

*Data Pipeline Skill - Part of Claude Office Skills*
