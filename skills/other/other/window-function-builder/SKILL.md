---
name: window-function-builder
description: Эксперт SQL window functions. Используй для аналитических запросов, OVER clauses и ranking functions.
---

# SQL Window Function Builder

Эксперт по SQL window functions и аналитическим запросам для бизнес-аналитики.

## Core Function Categories

### Function Overview

```yaml
window_functions:
  ranking:
    - ROW_NUMBER(): "Unique sequential numbers"
    - RANK(): "Ranking with gaps for ties"
    - DENSE_RANK(): "Ranking without gaps"
    - NTILE(n): "Divide into n buckets"

  aggregate:
    - SUM(): "Running/cumulative totals"
    - AVG(): "Moving averages"
    - COUNT(): "Running counts"
    - MIN(): "Running minimum"
    - MAX(): "Running maximum"

  offset:
    - LAG(col, n): "Access previous row"
    - LEAD(col, n): "Access next row"
    - FIRST_VALUE(): "First value in frame"
    - LAST_VALUE(): "Last value in frame"
    - NTH_VALUE(col, n): "Nth value in frame"

  statistical:
    - PERCENT_RANK(): "Relative rank as percentage"
    - CUME_DIST(): "Cumulative distribution"
    - PERCENTILE_CONT(): "Interpolated percentile"
    - PERCENTILE_DISC(): "Discrete percentile"
```

---

## Basic Syntax

### OVER Clause Structure

```sql
function_name(expression) OVER (
    [PARTITION BY partition_expression, ...]
    [ORDER BY sort_expression [ASC|DESC], ...]
    [frame_clause]
)
```

### Frame Specifications

```sql
-- Frame clause syntax
ROWS | RANGE BETWEEN frame_start AND frame_end

-- Frame bounds
UNBOUNDED PRECEDING  -- From first row of partition
n PRECEDING          -- n rows before current
CURRENT ROW          -- Current row
n FOLLOWING          -- n rows after current
UNBOUNDED FOLLOWING  -- To last row of partition

-- Common frame patterns
ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW  -- Running total (default for ORDER BY)
ROWS BETWEEN 6 PRECEDING AND CURRENT ROW          -- 7-day rolling
ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING          -- 3-row centered
RANGE BETWEEN INTERVAL '30' DAY PRECEDING AND CURRENT ROW  -- 30-day range
```

---

## Ranking Functions

### ROW_NUMBER, RANK, DENSE_RANK

```sql
-- Basic ranking comparison
SELECT
    employee_id,
    department,
    salary,
    ROW_NUMBER() OVER (ORDER BY salary DESC) AS row_num,
    RANK() OVER (ORDER BY salary DESC) AS rank,
    DENSE_RANK() OVER (ORDER BY salary DESC) AS dense_rank
FROM employees;

-- Results with tied salaries:
-- | employee_id | salary | row_num | rank | dense_rank |
-- |-------------|--------|---------|------|------------|
-- | 101         | 100000 | 1       | 1    | 1          |
-- | 102         | 100000 | 2       | 1    | 1          |  <- same salary
-- | 103         | 90000  | 3       | 3    | 2          |  <- note rank skips 2
```

### Ranking Within Groups

```sql
-- Top 3 salaries per department
WITH ranked AS (
    SELECT
        employee_id,
        employee_name,
        department,
        salary,
        DENSE_RANK() OVER (
            PARTITION BY department
            ORDER BY salary DESC
        ) AS dept_rank
    FROM employees
)
SELECT *
FROM ranked
WHERE dept_rank <= 3;
```

### NTILE for Percentiles

```sql
-- Divide customers into quartiles by revenue
SELECT
    customer_id,
    customer_name,
    total_revenue,
    NTILE(4) OVER (ORDER BY total_revenue DESC) AS revenue_quartile,
    CASE NTILE(4) OVER (ORDER BY total_revenue DESC)
        WHEN 1 THEN 'Top 25%'
        WHEN 2 THEN '25-50%'
        WHEN 3 THEN '50-75%'
        WHEN 4 THEN 'Bottom 25%'
    END AS segment
FROM customer_revenue;
```

---

## Running Calculations

### Running Totals

```sql
-- Running total of sales
SELECT
    order_date,
    order_amount,
    SUM(order_amount) OVER (
        ORDER BY order_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS running_total
FROM orders;

-- Running total per customer
SELECT
    customer_id,
    order_date,
    order_amount,
    SUM(order_amount) OVER (
        PARTITION BY customer_id
        ORDER BY order_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS customer_running_total
FROM orders;
```

### Moving Averages

```sql
-- 7-day moving average
SELECT
    date,
    daily_revenue,
    AVG(daily_revenue) OVER (
        ORDER BY date
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) AS moving_avg_7d,
    -- Also track the count for partial windows
    COUNT(*) OVER (
        ORDER BY date
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) AS days_in_window
FROM daily_sales;

-- Centered moving average (3 days before, current, 3 days after)
SELECT
    date,
    daily_revenue,
    AVG(daily_revenue) OVER (
        ORDER BY date
        ROWS BETWEEN 3 PRECEDING AND 3 FOLLOWING
    ) AS centered_avg_7d
FROM daily_sales;
```

### Cumulative Percentage

```sql
-- Cumulative percentage of total
SELECT
    product_category,
    revenue,
    SUM(revenue) OVER (ORDER BY revenue DESC) AS cumulative_revenue,
    ROUND(
        100.0 * SUM(revenue) OVER (ORDER BY revenue DESC) /
        SUM(revenue) OVER (),
        2
    ) AS cumulative_pct
FROM category_sales
ORDER BY revenue DESC;
```

---

## LAG and LEAD

### Period-over-Period Comparison

```sql
-- Month-over-month growth
SELECT
    month,
    revenue,
    LAG(revenue, 1) OVER (ORDER BY month) AS prev_month_revenue,
    revenue - LAG(revenue, 1) OVER (ORDER BY month) AS mom_change,
    ROUND(
        100.0 * (revenue - LAG(revenue, 1) OVER (ORDER BY month)) /
        NULLIF(LAG(revenue, 1) OVER (ORDER BY month), 0),
        2
    ) AS mom_growth_pct
FROM monthly_revenue;

-- Year-over-year comparison
SELECT
    date,
    revenue,
    LAG(revenue, 365) OVER (ORDER BY date) AS yoy_revenue,
    revenue - LAG(revenue, 365) OVER (ORDER BY date) AS yoy_change
FROM daily_revenue;
```

### Gap Analysis

```sql
-- Find gaps between orders
SELECT
    customer_id,
    order_date,
    LAG(order_date) OVER (
        PARTITION BY customer_id
        ORDER BY order_date
    ) AS previous_order_date,
    order_date - LAG(order_date) OVER (
        PARTITION BY customer_id
        ORDER BY order_date
    ) AS days_since_last_order
FROM orders;

-- Identify churned customers (no order > 90 days)
WITH order_gaps AS (
    SELECT
        customer_id,
        order_date,
        LEAD(order_date) OVER (
            PARTITION BY customer_id
            ORDER BY order_date
        ) AS next_order_date,
        LEAD(order_date) OVER (
            PARTITION BY customer_id
            ORDER BY order_date
        ) - order_date AS gap_days
    FROM orders
)
SELECT DISTINCT customer_id
FROM order_gaps
WHERE gap_days > 90
   OR (next_order_date IS NULL AND order_date < CURRENT_DATE - INTERVAL '90 days');
```

### Lead for Future Values

```sql
-- Forecast vs actual comparison
SELECT
    forecast_date,
    predicted_value,
    LEAD(actual_value, 7) OVER (ORDER BY forecast_date) AS actual_7d_later,
    LEAD(actual_value, 7) OVER (ORDER BY forecast_date) - predicted_value AS forecast_error
FROM forecasts;
```

---

## FIRST_VALUE and LAST_VALUE

### First/Last in Group

```sql
-- First and last order per customer
SELECT
    customer_id,
    order_id,
    order_date,
    order_amount,
    FIRST_VALUE(order_date) OVER (
        PARTITION BY customer_id
        ORDER BY order_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) AS first_order_date,
    LAST_VALUE(order_date) OVER (
        PARTITION BY customer_id
        ORDER BY order_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) AS last_order_date
FROM orders;

-- Note: LAST_VALUE requires explicit frame to see all rows!
```

### Baseline Comparison

```sql
-- Compare each day to first day of month
SELECT
    date,
    revenue,
    FIRST_VALUE(revenue) OVER (
        PARTITION BY DATE_TRUNC('month', date)
        ORDER BY date
    ) AS first_day_revenue,
    revenue - FIRST_VALUE(revenue) OVER (
        PARTITION BY DATE_TRUNC('month', date)
        ORDER BY date
    ) AS diff_from_first_day
FROM daily_revenue;
```

---

## Statistical Functions

### Percentile Calculations

```sql
-- Calculate percentiles
SELECT
    product_id,
    price,
    PERCENT_RANK() OVER (ORDER BY price) AS percent_rank,
    CUME_DIST() OVER (ORDER BY price) AS cumulative_dist,
    NTILE(100) OVER (ORDER BY price) AS percentile
FROM products;

-- Median calculation (50th percentile)
SELECT
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY salary) AS median_salary,
    PERCENTILE_DISC(0.5) WITHIN GROUP (ORDER BY salary) AS median_salary_discrete,
    AVG(salary) AS mean_salary
FROM employees;

-- Multiple percentiles at once
SELECT
    department,
    PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY salary) AS p25,
    PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY salary) AS median,
    PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY salary) AS p75,
    PERCENTILE_CONT(0.90) WITHIN GROUP (ORDER BY salary) AS p90
FROM employees
GROUP BY department;
```

---

## Business Analytics Patterns

### Customer Lifecycle Analysis

```sql
-- Customer order sequence and lifecycle metrics
WITH customer_orders AS (
    SELECT
        customer_id,
        order_id,
        order_date,
        order_amount,
        ROW_NUMBER() OVER (
            PARTITION BY customer_id
            ORDER BY order_date
        ) AS order_number,
        FIRST_VALUE(order_date) OVER (
            PARTITION BY customer_id
            ORDER BY order_date
        ) AS first_order_date,
        SUM(order_amount) OVER (
            PARTITION BY customer_id
            ORDER BY order_date
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ) AS lifetime_value,
        LAG(order_date) OVER (
            PARTITION BY customer_id
            ORDER BY order_date
        ) AS previous_order_date
    FROM orders
)
SELECT
    customer_id,
    order_id,
    order_number,
    order_amount,
    lifetime_value,
    order_date - first_order_date AS days_since_first_order,
    order_date - previous_order_date AS days_since_last_order,
    CASE
        WHEN order_number = 1 THEN 'New'
        WHEN order_date - previous_order_date > 90 THEN 'Reactivated'
        ELSE 'Repeat'
    END AS customer_status
FROM customer_orders;
```

### Cohort Analysis

```sql
-- Monthly cohort retention
WITH user_cohorts AS (
    SELECT
        user_id,
        DATE_TRUNC('month', first_activity_date) AS cohort_month,
        DATE_TRUNC('month', activity_date) AS activity_month
    FROM user_activity
),
cohort_sizes AS (
    SELECT
        cohort_month,
        COUNT(DISTINCT user_id) AS cohort_size
    FROM user_cohorts
    GROUP BY cohort_month
),
monthly_activity AS (
    SELECT
        cohort_month,
        activity_month,
        COUNT(DISTINCT user_id) AS active_users,
        EXTRACT(MONTH FROM AGE(activity_month, cohort_month)) AS month_number
    FROM user_cohorts
    GROUP BY cohort_month, activity_month
)
SELECT
    ma.cohort_month,
    ma.month_number,
    cs.cohort_size,
    ma.active_users,
    ROUND(100.0 * ma.active_users / cs.cohort_size, 2) AS retention_rate
FROM monthly_activity ma
JOIN cohort_sizes cs ON ma.cohort_month = cs.cohort_month
ORDER BY ma.cohort_month, ma.month_number;
```

### Sales Performance

```sql
-- Sales rep performance with rankings and targets
WITH sales_performance AS (
    SELECT
        sales_rep_id,
        rep_name,
        region,
        SUM(deal_amount) AS total_sales,
        COUNT(*) AS deal_count,
        AVG(deal_amount) AS avg_deal_size
    FROM sales_deals
    WHERE close_date >= DATE_TRUNC('quarter', CURRENT_DATE)
    GROUP BY sales_rep_id, rep_name, region
)
SELECT
    sales_rep_id,
    rep_name,
    region,
    total_sales,
    deal_count,
    avg_deal_size,
    RANK() OVER (ORDER BY total_sales DESC) AS overall_rank,
    RANK() OVER (PARTITION BY region ORDER BY total_sales DESC) AS region_rank,
    total_sales - AVG(total_sales) OVER () AS vs_company_avg,
    total_sales - AVG(total_sales) OVER (PARTITION BY region) AS vs_region_avg,
    PERCENT_RANK() OVER (ORDER BY total_sales) AS percentile
FROM sales_performance;
```

### Inventory Analysis

```sql
-- Inventory movement analysis
SELECT
    product_id,
    transaction_date,
    transaction_type,
    quantity,
    SUM(
        CASE WHEN transaction_type = 'IN' THEN quantity
             WHEN transaction_type = 'OUT' THEN -quantity
             ELSE 0
        END
    ) OVER (
        PARTITION BY product_id
        ORDER BY transaction_date, transaction_id
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS running_inventory,
    AVG(
        CASE WHEN transaction_type = 'OUT' THEN quantity END
    ) OVER (
        PARTITION BY product_id
        ORDER BY transaction_date
        ROWS BETWEEN 29 PRECEDING AND CURRENT ROW
    ) AS avg_daily_usage_30d
FROM inventory_transactions;
```

---

## Platform-Specific Features

### PostgreSQL

```sql
-- FILTER clause with window functions
SELECT
    date,
    category,
    amount,
    SUM(amount) OVER (ORDER BY date) AS total_running,
    SUM(amount) FILTER (WHERE category = 'A') OVER (ORDER BY date) AS category_a_running
FROM transactions;

-- GROUPS frame type
SELECT
    date,
    amount,
    SUM(amount) OVER (
        ORDER BY date
        GROUPS BETWEEN 1 PRECEDING AND 1 FOLLOWING
    ) AS sum_adjacent_groups
FROM transactions;
```

### SQL Server

```sql
-- STRING_AGG with OVER (SQL Server 2017+)
-- Not directly supported, use workaround:
SELECT DISTINCT
    department,
    STRING_AGG(employee_name, ', ') WITHIN GROUP (ORDER BY employee_name)
        OVER (PARTITION BY department) AS employees
FROM employees;

-- OFFSET with frames (SQL Server 2022+)
SELECT
    date,
    value,
    AVG(value) OVER (
        ORDER BY date
        ROWS BETWEEN 7 PRECEDING AND 1 PRECEDING
    ) AS previous_week_avg
FROM daily_metrics;
```

### BigQuery

```sql
-- QUALIFY clause (filter on window function results)
SELECT
    customer_id,
    order_date,
    order_amount
FROM orders
QUALIFY ROW_NUMBER() OVER (
    PARTITION BY customer_id
    ORDER BY order_date DESC
) = 1;

-- Equivalent to CTE approach:
-- WITH ranked AS (
--     SELECT *, ROW_NUMBER() OVER (...) AS rn FROM orders
-- )
-- SELECT * FROM ranked WHERE rn = 1;
```

### Snowflake

```sql
-- QUALIFY clause
SELECT *
FROM sales
QUALIFY DENSE_RANK() OVER (
    PARTITION BY region
    ORDER BY revenue DESC
) <= 5;

-- CONDITIONAL_TRUE_EVENT for sessionization
SELECT
    user_id,
    event_time,
    CONDITIONAL_TRUE_EVENT(
        DATEDIFF('minute', LAG(event_time) OVER (
            PARTITION BY user_id ORDER BY event_time
        ), event_time) > 30
    ) OVER (
        PARTITION BY user_id
        ORDER BY event_time
    ) AS session_id
FROM user_events;
```

---

## Performance Optimization

### Indexing Strategy

```sql
-- Composite index for window function
-- Index columns: PARTITION BY columns first, then ORDER BY columns
CREATE INDEX idx_orders_customer_date
ON orders (customer_id, order_date);

-- For running totals across all data
CREATE INDEX idx_orders_date_amount
ON orders (order_date, order_amount);
```

### Query Optimization Tips

```yaml
optimization_tips:
  - tip: "Add indexes on PARTITION BY + ORDER BY columns"
    reason: "Reduces sort operations"

  - tip: "Use CTEs to compute window once, reference multiple times"
    reason: "Avoids redundant calculations"

  - tip: "Limit rows before applying window functions when possible"
    reason: "Smaller dataset = faster windows"

  - tip: "Be explicit about frame clause"
    reason: "Prevents unexpected defaults"

  - tip: "Use QUALIFY when supported"
    reason: "Cleaner and often faster than subquery"
```

### CTE Pattern for Clarity

```sql
-- Use CTEs for complex window queries
WITH
-- Step 1: Calculate raw metrics
daily_metrics AS (
    SELECT
        date,
        SUM(amount) AS daily_total
    FROM transactions
    GROUP BY date
),
-- Step 2: Add window calculations
with_windows AS (
    SELECT
        date,
        daily_total,
        SUM(daily_total) OVER (ORDER BY date) AS running_total,
        AVG(daily_total) OVER (
            ORDER BY date
            ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
        ) AS rolling_7d_avg,
        LAG(daily_total, 7) OVER (ORDER BY date) AS same_day_last_week
    FROM daily_metrics
)
-- Step 3: Final calculations
SELECT
    date,
    daily_total,
    running_total,
    rolling_7d_avg,
    daily_total - same_day_last_week AS wow_change
FROM with_windows
WHERE date >= CURRENT_DATE - INTERVAL '30 days';
```

---

## Лучшие практики

1. **Явно указывай frame clause** — дефолтное поведение может быть неожиданным
2. **Используй CTE для сложных запросов** — улучшает читаемость и maintainability
3. **Создавай composite индексы** — на PARTITION BY + ORDER BY колонки
4. **Проверяй NULL handling** — LAG/LEAD возвращают NULL для граничных строк
5. **Тестируй edge cases** — первая/последняя строка, одна строка в партиции
6. **Используй QUALIFY где поддерживается** — чище чем subquery
7. **Учитывай особенности СУБД** — синтаксис и функции различаются
8. **Оптимизируй сначала WHERE** — фильтруй до применения window functions
