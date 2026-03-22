---
name: evidence
description: Expert guidance for Evidence, the open-source BI framework that generates beautiful, interactive dashboards from SQL queries and Markdown. Helps developers build data reports as code, deploy them as static sites, and create self-service analytics without heavy BI tools.
license: Apache-2.0
compatibility: No special requirements
metadata:
  author: terminal-skills
  version: 1.0.0
  category: data-ai
  tags:
  - bi
  - dashboards
  - sql
  - markdown
  - reporting
---

# Evidence — Code-Driven BI Dashboards


## Overview


Evidence, the open-source BI framework that generates beautiful, interactive dashboards from SQL queries and Markdown. Helps developers build data reports as code, deploy them as static sites, and create self-service analytics without heavy BI tools.


## Instructions

### Project Setup

```bash
# Create a new Evidence project
npx degit evidence-dev/template my-dashboard
cd my-dashboard
npm install
npm run dev    # Dashboard at localhost:3000
```

### Writing Reports

Evidence reports are Markdown files with embedded SQL:

```markdown
<!-- pages/sales-overview.md — Sales dashboard page -->
# Sales Overview

```sql monthly_revenue
SELECT
  date_trunc('month', created_at) AS month,
  SUM(amount) AS revenue,
  COUNT(*) AS orders,
  SUM(amount) / COUNT(*) AS avg_order_value
FROM orders
WHERE created_at >= '2025-01-01'
GROUP BY 1
ORDER BY 1
```

Revenue has grown **{fmt(monthly_revenue[monthly_revenue.length - 1].revenue, 'usd')}** this month,
a {pct_change} change from last month.

<LineChart
  data={monthly_revenue}
  x=month
  y=revenue
  yFmt=usd
  title="Monthly Revenue"
/>

<BarChart
  data={monthly_revenue}
  x=month
  y=orders
  title="Orders per Month"
/>

## Revenue by Product

```sql product_breakdown
SELECT
  p.name AS product,
  SUM(oi.quantity * oi.unit_price) AS revenue,
  SUM(oi.quantity) AS units_sold
FROM order_items oi
JOIN products p ON p.id = oi.product_id
JOIN orders o ON o.id = oi.order_id
WHERE o.created_at >= current_date - interval '30 days'
GROUP BY 1
ORDER BY 2 DESC
LIMIT 10
```

<DataTable data={product_breakdown} rows=10>
  <Column id=product title="Product" />
  <Column id=revenue title="Revenue" fmt=usd />
  <Column id=units_sold title="Units Sold" fmt=num0 />
</DataTable>

<BarChart
  data={product_breakdown}
  x=product
  y=revenue
  yFmt=usd
  swapXY=true
  title="Top 10 Products by Revenue"
/>
```

### Data Source Configuration

Connect to your databases:

```yaml
# sources/mydb/connection.yaml — PostgreSQL connection
name: mydb
type: postgres
host: localhost
port: 5432
database: analytics
user: evidence_reader
password: ${POSTGRES_PASSWORD}    # From environment variable
ssl: true

# sources/duckdb/connection.yaml — DuckDB for file-based analytics
name: local
type: duckdb
filename: data/analytics.duckdb

# sources/bigquery/connection.yaml — Google BigQuery
name: warehouse
type: bigquery
project_id: my-gcp-project
dataset: analytics
credentials_path: ./gcp-key.json

# sources/csv/connection.yaml — CSV files
name: csvdata
type: csv
path: data/        # All CSV files in this directory become tables
```

### Interactive Components

```markdown
<!-- pages/cohort-analysis.md — Interactive filters -->
# Cohort Analysis

<!-- Dropdown filter -->
<Dropdown name=time_period title="Time Period">
  <DropdownOption value="7 days" valueLabel="Last 7 Days" />
  <DropdownOption value="30 days" valueLabel="Last 30 Days" />
  <DropdownOption value="90 days" valueLabel="Last 90 Days" />
</Dropdown>

<Dropdown name=segment title="Customer Segment" data={segments} value=id label=name />

```sql cohort_data
SELECT
  date_trunc('week', first_purchase) AS cohort_week,
  weeks_since_first AS week_number,
  COUNT(DISTINCT customer_id) AS customers,
  SUM(revenue) AS revenue
FROM customer_cohorts
WHERE first_purchase >= current_date - interval '${inputs.time_period}'
  AND segment = '${inputs.segment.value}'
GROUP BY 1, 2
ORDER BY 1, 2
```

<Heatmap
  data={cohort_data}
  x=week_number
  y=cohort_week
  value=customers
  title="Customer Retention by Cohort"
/>

<!-- Big number KPIs -->
<BigValue
  data={cohort_data}
  value=customers
  title="Total Customers"
  fmt=num0
  comparison=revenue
  comparisonTitle="Total Revenue"
  comparisonFmt=usd
/>
```

### Templated Pages

Generate pages dynamically from data:

```markdown
<!-- pages/products/[product_name].md — One page per product -->
# {params.product_name}

```sql product_detail
SELECT * FROM products WHERE slug = '${params.product_name}'
```

```sql product_sales
SELECT
  date_trunc('day', o.created_at) AS date,
  SUM(oi.quantity) AS units,
  SUM(oi.quantity * oi.unit_price) AS revenue
FROM order_items oi
JOIN orders o ON o.id = oi.order_id
JOIN products p ON p.id = oi.product_id
WHERE p.slug = '${params.product_name}'
  AND o.created_at >= current_date - interval '90 days'
GROUP BY 1
ORDER BY 1
```

<LineChart data={product_sales} x=date y=revenue yFmt=usd />
<LineChart data={product_sales} x=date y=units />
```

### Deployment

```bash
# Build static site
npm run build

# Deploy to any static hosting
# Vercel
npx vercel

# Netlify
npx netlify deploy --prod --dir=build

# Evidence Cloud (managed hosting)
npx evidence deploy

# Schedule refreshes with cron
# Evidence rebuilds queries at build time
# Set up a cron job to rebuild periodically:
# 0 */4 * * * cd /app/dashboard && npm run build && cp -r build /var/www/dashboard
```


## Examples


### Example 1: Creating a weekly SaaS metrics report

**User request:**

```
Build an Evidence dashboard that shows our weekly SaaS metrics — MRR, churn rate, new trials, and conversion rate — from our PostgreSQL database.
```

The agent scaffolds an Evidence project, configures the PostgreSQL connection in `evidence.plugins.yaml`, creates SQL queries for each metric (`select date_trunc('week', created_at) as week, sum(amount) as mrr from subscriptions...`), builds a Markdown page with `<LineChart>`, `<BigValue>`, and `<DataTable>` components, and adds date range inputs with `<DateRange>` for filtering.

### Example 2: Building a templated customer health page

**User request:**

```
I need a per-customer detail page in Evidence that shows usage trends, support tickets, and renewal date for each customer.
```

The agent creates a templated page at `pages/customers/[customer_id].md`, writes SQL queries that filter by `${params.customer_id}`, adds a customer index page with `<DataTable>` linking to each detail page, and includes `<BarChart>` for usage and `<Alert>` components for upcoming renewals.


## Guidelines

1. **SQL is the source of truth** — Write queries directly in Markdown; no abstraction layer between you and the data
2. **Use parameterized queries carefully** — Evidence supports `${inputs.x}` but sanitize inputs; prefer dropdown constraints over free text
3. **One page per topic** — Keep reports focused; use navigation for different areas (sales, product, customer)
4. **Templated pages for catalogs** — Use `[param].md` for product pages, customer profiles, or any entity-level reports
5. **Read-only database users** — Connect Evidence with a read-only database user; it should never write data
6. **Version control reports** — Evidence projects are code; store in Git, review in PRs, deploy via CI
7. **Build-time queries** — Queries run at build time, not on page load; schedule rebuilds based on data freshness needs
8. **DuckDB for local analysis** — Use DuckDB as a data source for CSV/Parquet files; no database server needed
