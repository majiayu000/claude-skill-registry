---
name: sql-data-analysis
description: "Perform data analysis using SQL for business intelligence and decision-making. Use for: writing complex queries, data extraction and transformation, aggregate analysis, JOIN operations, window functions, subqueries and CTEs, data cleaning and validation, performance optimization, time series analysis, cohort analysis, funnel analysis, data preparation for visualization, database querying across MySQL/PostgreSQL/SQL Server/BigQuery, and analytical reporting."
---

# SQL Data Analysis

Extract insights from databases using Structured Query Language for business intelligence and analytics.

## Overview

SQL (Structured Query Language) is the foundational language for data extraction, transformation, and analysis across relational databases. This skill covers writing efficient queries, performing complex analyses, optimizing performance, and preparing data for visualization and reporting. SQL enables analysts to work directly with data at scale, combining multiple sources and applying business logic to generate actionable insights.

## Core SQL Concepts for Analysis

### Data Retrieval Fundamentals

**SELECT Statement Structure**:
```sql
SELECT column1, column2, aggregate_function(column3)
FROM table_name
WHERE condition
GROUP BY column1, column2
HAVING aggregate_condition
ORDER BY column1 DESC
LIMIT 100;
```

**Key Clauses**:
- **SELECT**: Specify columns to retrieve
- **FROM**: Identify source table(s)
- **WHERE**: Filter rows before aggregation
- **GROUP BY**: Organize rows into groups
- **HAVING**: Filter groups after aggregation
- **ORDER BY**: Sort results
- **LIMIT/TOP**: Restrict number of rows returned

### Filtering and Conditions

| Operator | Purpose | Example |
|----------|---------|--------|
| = | Equality | `WHERE status = 'active'` |
| <>, != | Inequality | `WHERE category <> 'test'` |
| >, <, >=, <= | Comparison | `WHERE revenue > 1000` |
| BETWEEN | Range | `WHERE date BETWEEN '2026-01-01' AND '2026-03-15'` |
| IN | List membership | `WHERE country IN ('US', 'UK', 'CA')` |
| LIKE | Pattern matching | `WHERE email LIKE '%@gmail.com'` |
| IS NULL | Null check | `WHERE phone IS NULL` |
| AND, OR, NOT | Logical operators | `WHERE age > 18 AND status = 'active'` |

### Aggregate Functions

**Common Aggregations**:
```sql
SELECT
  COUNT(*) as total_records,
  COUNT(DISTINCT user_id) as unique_users,
  SUM(revenue) as total_revenue,
  AVG(order_value) as average_order,
  MIN(created_date) as first_order,
  MAX(created_date) as last_order,
  STDDEV(order_value) as std_deviation,
  VARIANCE(order_value) as variance
FROM orders
WHERE order_date >= '2026-01-01';
```

## JOIN Operations

### JOIN Types

**INNER JOIN**: Returns matching rows from both tables
```sql
SELECT
  o.order_id,
  o.order_date,
  c.customer_name,
  c.email
FROM orders o
INNER JOIN customers c ON o.customer_id = c.customer_id
WHERE o.order_date >= '2026-01-01';
```

**LEFT JOIN**: Returns all rows from left table, matching rows from right
```sql
SELECT
  c.customer_id,
  c.customer_name,
  COUNT(o.order_id) as order_count,
  COALESCE(SUM(o.total), 0) as total_spent
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.customer_name;
```

**RIGHT JOIN**: Returns all rows from right table, matching rows from left
```sql
SELECT
  p.product_name,
  COALESCE(SUM(oi.quantity), 0) as units_sold
FROM order_items oi
RIGHT JOIN products p ON oi.product_id = p.product_id
GROUP BY p.product_name;
```

**FULL OUTER JOIN**: Returns all rows when there's a match in either table
```sql
SELECT
  COALESCE(a.date, b.date) as date,
  a.website_visits,
  b.app_sessions
FROM website_analytics a
FULL OUTER JOIN app_analytics b ON a.date = b.date;
```

**CROSS JOIN**: Cartesian product of two tables
```sql
SELECT
  d.date,
  p.product_id
FROM date_dimension d
CROSS JOIN products p
WHERE d.date BETWEEN '2026-01-01' AND '2026-12-31';
```

### Multiple JOIN Example

```sql
SELECT
  c.customer_name,
  o.order_id,
  o.order_date,
  p.product_name,
  oi.quantity,
  oi.unit_price,
  (oi.quantity * oi.unit_price) as line_total
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
INNER JOIN order_items oi ON o.order_id = oi.order_id
INNER JOIN products p ON oi.product_id = p.product_id
WHERE o.order_date >= '2026-01-01'
ORDER BY o.order_date DESC, o.order_id, oi.line_number;
```

## Advanced Query Techniques

### Subqueries

**Scalar Subquery** (returns single value):
```sql
SELECT
  product_name,
  price,
  price - (SELECT AVG(price) FROM products) as price_vs_average
FROM products;
```

**Subquery in WHERE Clause**:
```sql
SELECT customer_id, customer_name, total_spent
FROM customers
WHERE total_spent > (
  SELECT AVG(total_spent)
  FROM customers
);
```

**Subquery in FROM Clause** (derived table):
```sql
SELECT
  category,
  AVG(product_count) as avg_products_per_subcategory
FROM (
  SELECT
    category,
    subcategory,
    COUNT(*) as product_count
  FROM products
  GROUP BY category, subcategory
) as subcategory_counts
GROUP BY category;
```

**Correlated Subquery**:
```sql
SELECT
  o1.order_id,
  o1.customer_id,
  o1.order_total,
  (
    SELECT COUNT(*)
    FROM orders o2
    WHERE o2.customer_id = o1.customer_id
      AND o2.order_date < o1.order_date
  ) as previous_orders
FROM orders o1;
```

### Common Table Expressions (CTEs)

**Simple CTE**:
```sql
WITH high_value_customers AS (
  SELECT
    customer_id,
    SUM(order_total) as lifetime_value
  FROM orders
  GROUP BY customer_id
  HAVING SUM(order_total) > 10000
)
SELECT
  c.customer_name,
  c.email,
  hvc.lifetime_value
FROM high_value_customers hvc
JOIN customers c ON hvc.customer_id = c.customer_id
ORDER BY hvc.lifetime_value DESC;
```

**Multiple CTEs**:
```sql
WITH monthly_revenue AS (
  SELECT
    DATE_TRUNC('month', order_date) as month,
    SUM(order_total) as revenue
  FROM orders
  GROUP BY DATE_TRUNC('month', order_date)
),
revenue_growth AS (
  SELECT
    month,
    revenue,
    LAG(revenue) OVER (ORDER BY month) as previous_month_revenue,
    revenue - LAG(revenue) OVER (ORDER BY month) as revenue_change
  FROM monthly_revenue
)
SELECT
  month,
  revenue,
  previous_month_revenue,
  revenue_change,
  ROUND(100.0 * revenue_change / NULLIF(previous_month_revenue, 0), 2) as growth_percentage
FROM revenue_growth
ORDER BY month;
```

**Recursive CTE** (hierarchical data):
```sql
WITH RECURSIVE employee_hierarchy AS (
  -- Anchor: top-level employees
  SELECT
    employee_id,
    employee_name,
    manager_id,
    1 as level,
    CAST(employee_name AS VARCHAR(1000)) as path
  FROM employees
  WHERE manager_id IS NULL
  
  UNION ALL
  
  -- Recursive: employees reporting to previous level
  SELECT
    e.employee_id,
    e.employee_name,
    e.manager_id,
    eh.level + 1,
    eh.path || ' > ' || e.employee_name
  FROM employees e
  INNER JOIN employee_hierarchy eh ON e.manager_id = eh.employee_id
)
SELECT * FROM employee_hierarchy
ORDER BY path;
```

## Window Functions

### Ranking Functions

```sql
SELECT
  product_name,
  category,
  revenue,
  ROW_NUMBER() OVER (PARTITION BY category ORDER BY revenue DESC) as row_num,
  RANK() OVER (PARTITION BY category ORDER BY revenue DESC) as rank,
  DENSE_RANK() OVER (PARTITION BY category ORDER BY revenue DESC) as dense_rank,
  NTILE(4) OVER (PARTITION BY category ORDER BY revenue DESC) as quartile
FROM product_revenue
ORDER BY category, revenue DESC;
```

### Aggregate Window Functions

```sql
SELECT
  order_date,
  order_total,
  SUM(order_total) OVER (ORDER BY order_date) as running_total,
  AVG(order_total) OVER (ORDER BY order_date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) as moving_avg_7day,
  SUM(order_total) OVER (PARTITION BY EXTRACT(MONTH FROM order_date)) as monthly_total,
  order_total / SUM(order_total) OVER (PARTITION BY EXTRACT(MONTH FROM order_date)) as pct_of_monthly_total
FROM orders
ORDER BY order_date;
```

### LAG and LEAD Functions

```sql
SELECT
  date,
  revenue,
  LAG(revenue, 1) OVER (ORDER BY date) as previous_day_revenue,
  LEAD(revenue, 1) OVER (ORDER BY date) as next_day_revenue,
  revenue - LAG(revenue, 1) OVER (ORDER BY date) as day_over_day_change,
  LAG(revenue, 7) OVER (ORDER BY date) as same_day_last_week,
  revenue - LAG(revenue, 7) OVER (ORDER BY date) as week_over_week_change
FROM daily_revenue
ORDER BY date;
```

## Data Cleaning and Transformation

### Handling NULL Values

```sql
SELECT
  customer_id,
  COALESCE(phone, 'No phone') as phone,
  COALESCE(email, 'No email') as email,
  NULLIF(discount_code, '') as discount_code,  -- Convert empty string to NULL
  CASE
    WHEN address IS NULL THEN 'Address missing'
    ELSE address
  END as address_status
FROM customers;
```

### String Manipulation

```sql
SELECT
  UPPER(customer_name) as name_upper,
  LOWER(email) as email_lower,
  TRIM(phone) as phone_trimmed,
  CONCAT(first_name, ' ', last_name) as full_name,
  SUBSTRING(email, 1, POSITION('@' IN email) - 1) as email_username,
  REPLACE(phone, '-', '') as phone_no_dashes,
  LENGTH(description) as description_length,
  LEFT(product_code, 3) as product_category_code,
  RIGHT(order_id, 6) as order_number
FROM customers;
```

### Date Manipulation

```sql
SELECT
  order_date,
  EXTRACT(YEAR FROM order_date) as year,
  EXTRACT(MONTH FROM order_date) as month,
  EXTRACT(DAY FROM order_date) as day,
  EXTRACT(DOW FROM order_date) as day_of_week,  -- 0=Sunday
  DATE_TRUNC('month', order_date) as month_start,
  DATE_TRUNC('week', order_date) as week_start,
  order_date + INTERVAL '30 days' as due_date,
  AGE(CURRENT_DATE, order_date) as order_age,
  DATE_PART('day', CURRENT_DATE - order_date) as days_since_order
FROM orders;
```

### CASE Statements

```sql
SELECT
  customer_id,
  total_spent,
  CASE
    WHEN total_spent >= 10000 THEN 'VIP'
    WHEN total_spent >= 5000 THEN 'Premium'
    WHEN total_spent >= 1000 THEN 'Standard'
    ELSE 'Basic'
  END as customer_tier,
  CASE
    WHEN last_order_date >= CURRENT_DATE - INTERVAL '30 days' THEN 'Active'
    WHEN last_order_date >= CURRENT_DATE - INTERVAL '90 days' THEN 'At Risk'
    ELSE 'Churned'
  END as customer_status
FROM customer_summary;
```

## Analytical Patterns

### Cohort Analysis

```sql
WITH user_cohorts AS (
  SELECT
    user_id,
    DATE_TRUNC('month', MIN(signup_date)) as cohort_month
  FROM users
  GROUP BY user_id
),
user_activity AS (
  SELECT
    user_id,
    DATE_TRUNC('month', activity_date) as activity_month
  FROM user_activities
)
SELECT
  uc.cohort_month,
  ua.activity_month,
  DATE_PART('month', AGE(ua.activity_month, uc.cohort_month)) as months_since_signup,
  COUNT(DISTINCT ua.user_id) as active_users
FROM user_cohorts uc
JOIN user_activity ua ON uc.user_id = ua.user_id
GROUP BY uc.cohort_month, ua.activity_month
ORDER BY uc.cohort_month, ua.activity_month;
```

### Funnel Analysis

```sql
WITH funnel_steps AS (
  SELECT
    user_id,
    MAX(CASE WHEN event_name = 'page_view' THEN 1 ELSE 0 END) as viewed,
    MAX(CASE WHEN event_name = 'add_to_cart' THEN 1 ELSE 0 END) as added_cart,
    MAX(CASE WHEN event_name = 'checkout_start' THEN 1 ELSE 0 END) as started_checkout,
    MAX(CASE WHEN event_name = 'purchase' THEN 1 ELSE 0 END) as purchased
  FROM events
  WHERE event_date >= '2026-03-01'
  GROUP BY user_id
)
SELECT
  SUM(viewed) as step1_viewed,
  SUM(added_cart) as step2_added_cart,
  SUM(started_checkout) as step3_started_checkout,
  SUM(purchased) as step4_purchased,
  ROUND(100.0 * SUM(added_cart) / NULLIF(SUM(viewed), 0), 2) as pct_view_to_cart,
  ROUND(100.0 * SUM(started_checkout) / NULLIF(SUM(added_cart), 0), 2) as pct_cart_to_checkout,
  ROUND(100.0 * SUM(purchased) / NULLIF(SUM(started_checkout), 0), 2) as pct_checkout_to_purchase
FROM funnel_steps;
```

### RFM Analysis (Recency, Frequency, Monetary)

```sql
WITH customer_rfm AS (
  SELECT

## Using the Reference Files

### When to Read Each Reference

**`/references/advanced-techniques.md`** — Read when implementing complex analytical queries, working with hierarchical data, or optimizing query performance.

**`/references/window-functions-guide.md`** — Read when performing running totals, moving averages, ranking, or comparative analysis across rows.

**`/references/database-specific-features.md`** — Read when working with PostgreSQL, MySQL, SQL Server, or BigQuery-specific functionality and optimizations.
