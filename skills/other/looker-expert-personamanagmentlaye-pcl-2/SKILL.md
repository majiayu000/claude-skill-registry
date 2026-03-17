---
name: looker-expert
version: 1.0.0
description: Expert-level Looker BI, LookML, explores, dimensions, measures, dashboards, and data modeling
category: data
author: PCL Team
license: Apache-2.0
tags:
  - looker
  - lookml
  - bi
  - analytics
  - dashboards
  - data-modeling
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
requirements:
  looker-sdk: ">=23.0.0"
---

# Looker Expert

You are an expert in Looker with deep knowledge of LookML, explores, dimensions, measures, dashboards, PDTs (Persistent Derived Tables), and semantic data modeling. You design maintainable, performant Looker models that enable self-service analytics.

## Core Expertise

### LookML Basics

**View Definition:**
```lookml
# views/orders.view.lkml
view: orders {
  sql_table_name: public.orders ;;
  drill_fields: [id]

  # Primary key
  dimension: id {
    primary_key: yes
    type: number
    sql: ${TABLE}.id ;;
  }

  # Foreign key
  dimension: user_id {
    type: number
    hidden: yes
    sql: ${TABLE}.user_id ;;
  }

  # Dimensions
  dimension: status {
    type: string
    sql: ${TABLE}.status ;;
    description: "Order status (pending, completed, cancelled, refunded)"
  }

  dimension: total_amount {
    type: number
    sql: ${TABLE}.total_amount ;;
    value_format_name: usd
    description: "Total order amount including tax and shipping"
  }

  # Date dimensions
  dimension_group: created {
    type: time
    timeframes: [
      raw,
      time,
      date,
      week,
      month,
      quarter,
      year
    ]
    sql: ${TABLE}.created_at ;;
    description: "When the order was created"
  }

  dimension_group: completed {
    type: time
    timeframes: [date, week, month]
    sql: ${TABLE}.completed_at ;;
    convert_tz: no
    datatype: date
  }

  # Measures
  measure: count {
    type: count
    drill_fields: [detail*]
  }

  measure: total_revenue {
    type: sum
    sql: ${total_amount} ;;
    value_format_name: usd
    description: "Sum of all order amounts"
  }

  measure: average_order_value {
    type: average
    sql: ${total_amount} ;;
    value_format_name: usd
    description: "Average order amount"
  }

  measure: completed_orders {
    type: count
    filters: [status: "completed"]
    description: "Count of completed orders"
  }

  # Sets for drilling
  set: detail {
    fields: [
      id,
      users.name,
      created_date,
      status,
      total_amount
    ]
  }
}
```

**Model Definition:**
```lookml
# models/analytics.model.lkml
connection: "production_database"

include: "/views/**/*.view.lkml"
include: "/dashboards/**/*.dashboard.lookml"

# Datagroups for caching
datagroup: daily_refresh {
  sql_trigger: SELECT CURRENT_DATE ;;
  max_cache_age: "24 hours"
}

datagroup: hourly_refresh {
  sql_trigger: SELECT FLOOR(EXTRACT(EPOCH FROM CURRENT_TIMESTAMP) / 3600) ;;
  max_cache_age: "1 hour"
}

# Explores
explore: orders {
  label: "Orders"
  description: "Order transactions and related data"

  # Joins
  join: users {
    type: left_outer
    sql_on: ${orders.user_id} = ${users.id} ;;
    relationship: many_to_one
  }

  join: order_items {
    type: left_outer
    sql_on: ${orders.id} = ${order_items.order_id} ;;
    relationship: one_to_many
  }

  join: products {
    type: left_outer
    sql_on: ${order_items.product_id} = ${products.id} ;;
    relationship: many_to_one
  }

  # Filters
  sql_always_where: ${orders.created_date} >= '2020-01-01' ;;
  always_filter: {
    filters: [orders.created_date: "last 90 days"]
  }

  # Access control
  access_filter: {
    field: users.country
    user_attribute: country
  }
}

explore: users {
  label: "Customers"

  join: orders {
    type: left_outer
    sql_on: ${users.id} = ${orders.user_id} ;;
    relationship: one_to_many
  }

  # Aggregate awareness
  aggregate_table: rollup__created_month__count {
    query: {
      dimensions: [created_month]
      measures: [count]
    }
    materialization: {
      datagroup_trigger: daily_refresh
    }
  }
}
```

### Advanced Dimensions and Measures

**Derived Dimensions:**
```lookml
view: users {
  # Concatenation
  dimension: full_name {
    type: string
    sql: CONCAT(${first_name}, ' ', ${last_name}) ;;
  }

  # Case statement
  dimension: customer_segment {
    type: string
    sql: CASE
          WHEN ${lifetime_value} >= 10000 THEN 'VIP'
          WHEN ${lifetime_value} >= 5000 THEN 'High Value'
          WHEN ${lifetime_value} >= 1000 THEN 'Medium Value'
          ELSE 'Low Value'
        END ;;
  }

  # Boolean dimension
  dimension: is_high_value {
    type: yesno
    sql: ${lifetime_value} >= 5000 ;;
  }

  # Duration calculation
  dimension: days_since_signup {
    type: number
    sql: DATEDIFF(day, ${created_date}, CURRENT_DATE) ;;
  }

  # Tier dimension
  dimension: age_tier {
    type: tier
    tiers: [18, 25, 35, 45, 55, 65]
    style: integer
    sql: ${age} ;;
  }

  # Yesno with complex logic
  dimension: is_active_customer {
    type: yesno
    sql: ${last_order_date} >= DATEADD(day, -90, CURRENT_DATE)
         AND ${is_deleted} = false ;;
  }
}
```

**Advanced Measures:**
```lookml
view: orders {
  # Conditional measures
  measure: high_value_orders {
    type: count
    filters: [total_amount: ">100"]
  }

  measure: revenue_high_value_orders {
    type: sum
    sql: ${total_amount} ;;
    filters: [total_amount: ">100"]
    value_format_name: usd
  }

  # Distinct count
  measure: unique_customers {
    type: count_distinct
    sql: ${user_id} ;;
    description: "Number of unique customers"
  }

  # Percentile
  measure: median_order_value {
    type: median
    sql: ${total_amount} ;;
    value_format_name: usd
  }

  measure: p95_order_value {
    type: percentile
    percentile: 95
    sql: ${total_amount} ;;
    value_format_name: usd
  }

  # Running total (table calculation alternative)
  measure: cumulative_revenue {
    type: running_total
    sql: ${total_revenue} ;;
    value_format_name: usd
  }

  # Filtered measure with OR logic
  measure: orders_pending_or_processing {
    type: count
    filters: [
      status: "pending,processing"
    ]
  }

  # Ratio measure
  measure: conversion_rate {
    type: number
    sql: 1.0 * ${completed_orders} / NULLIF(${count}, 0) ;;
    value_format_name: percent_2
  }

  # Average distinct (for distinct key values)
  measure: avg_daily_orders {
    type: average_distinct
    sql: ${count} ;;
    sql_distinct_key: ${created_date} ;;
  }
}
```

### Persistent Derived Tables (PDTs)

**SQL-Based PDTs:**
```lookml
view: customer_lifetime_metrics {
  derived_table: {
    sql:
      SELECT
        user_id,
        COUNT(*) as lifetime_orders,
        SUM(total_amount) as lifetime_value,
        AVG(total_amount) as avg_order_value,
        MIN(created_at) as first_order_date,
        MAX(created_at) as last_order_date
      FROM orders
      WHERE status = 'completed'
      GROUP BY user_id
    ;;

    # Persistence strategy
    datagroup_trigger: daily_refresh
    distribution_style: all
    sortkeys: ["user_id"]
    indexes: ["user_id"]
  }

  dimension: user_id {
    primary_key: yes
    type: number
    sql: ${TABLE}.user_id ;;
  }

  dimension: lifetime_orders {
    type: number
    sql: ${TABLE}.lifetime_orders ;;
  }

  measure: total_lifetime_value {
    type: sum
    sql: ${lifetime_value} ;;
    value_format_name: usd
  }
}
```

**Incremental PDTs:**
```lookml
view: daily_order_summary {
  derived_table: {
    sql:
      SELECT
        DATE(created_at) as order_date,
        status,
        COUNT(*) as order_count,
        SUM(total_amount) as total_revenue
      FROM orders
      WHERE
        {% condition order_date %} DATE(created_at) {% endcondition %}
      GROUP BY 1, 2
    ;;

    # Incremental strategy
    datagroup_trigger: hourly_refresh
    increment_key: "order_date"
    increment_offset: 3

    # SQL for incremental loads
    sql_trigger_value: SELECT CURRENT_DATE ;;
    partition_keys: ["order_date"]
  }

  dimension_group: order {
    type: time
    timeframes: [date, week, month]
    sql: ${TABLE}.order_date ;;
  }

  filter: order_date {
    type: date
  }
}
```

**Native Derived Tables (NDTs):**
```lookml
explore: orders {
  # Inline derived table
  join: order_summary {
    type: left_outer
    sql_on: ${orders.id} = ${order_summary.order_id} ;;
    relationship: one_to_one

    sql_table_name:
      (SELECT
        order_id,
        COUNT(*) as item_count,
        SUM(quantity) as total_quantity
      FROM order_items
      GROUP BY order_id)
    ;;
  }
}
```

### Explores and Joins

**Advanced Join Patterns:**
```lookml
explore: orders {
  # Many-to-one join
  join: users {
    type: left_outer
    sql_on: ${orders.user_id} = ${users.id} ;;
    relationship: many_to_one
  }

  # One-to-many join with symmetric aggregates
  join: order_items {
    type: left_outer
    sql_on: ${orders.id} = ${order_items.order_id} ;;
    relationship: one_to_many
  }

  # Many-to-one fanout prevention
  join: products {
    type: left_outer
    sql_on: ${order_items.product_id} = ${products.id} ;;
    relationship: many_to_one
    required_joins: [order_items]
  }

  # Join based on derived table
  join: customer_metrics {
    type: left_outer
    sql_on: ${users.id} = ${customer_metrics.user_id} ;;
    relationship: one_to_one
  }

  # Cross join (use sparingly)
  join: date_spine {
    type: cross
    relationship: many_to_many
  }

  # Join with additional conditions
  join: user_preferences {
    type: left_outer
    sql_on: ${users.id} = ${user_preferences.user_id}
           AND ${user_preferences.is_active} = true ;;
    relationship: one_to_one
  }
}
```

**Refinements:**
```lookml
# Extend base explore
explore: +orders {
  label: "Orders Extended"

  # Add additional join
  join: promotions {
    type: left_outer
    sql_on: ${orders.promotion_id} = ${promotions.id} ;;
    relationship: many_to_one
  }

  # Override existing join
  join: users {
    fields: [users.id, users.name, users.email]  # Limit fields
  }
}
```

### Parameters and Templated Filters

**Parameters:**
```lookml
view: orders {
  # Parameter for dynamic measures
  parameter: metric_selector {
    type: unquoted
    allowed_value: {
      label: "Revenue"
      value: "revenue"
    }
    allowed_value: {
      label: "Order Count"
      value: "count"
    }
    allowed_value: {
      label: "Average Order Value"
      value: "aov"
    }
  }

  measure: dynamic_metric {
    label_from_parameter: metric_selector
    type: number
    sql:
      {% if metric_selector._parameter_value == 'revenue' %}
        ${total_revenue}
      {% elsif metric_selector._parameter_value == 'count' %}
        ${count}
      {% elsif metric_selector._parameter_value == 'aov' %}
        ${average_order_value}
      {% else %}
        NULL
      {% endif %}
    ;;
  }

  # Date range parameter
  parameter: timeframe_picker {
    type: unquoted
    allowed_value: {
      label: "Day"
      value: "date"
    }
    allowed_value: {
      label: "Week"
      value: "week"
    }
    allowed_value: {
      label: "Month"
      value: "month"
    }
  }

  dimension: dynamic_timeframe {
    label_from_parameter: timeframe_picker
    type: string
    sql:
      {% if timeframe_picker._parameter_value == 'date' %}
        ${created_date}
      {% elsif timeframe_picker._parameter_value == 'week' %}
        ${created_week}
      {% elsif timeframe_picker._parameter_value == 'month' %}
        ${created_month}
      {% else %}
        ${created_date}
      {% endif %}
    ;;
  }
}
```

**Templated Filters:**
```lookml
view: orders {
  # Filter-only field
  filter: date_filter {
    type: date
    description: "Use this filter to define date range"
  }

  # Dimension using filter
  dimension: is_in_date_range {
    type: yesno
    sql: {% condition date_filter %} ${created_raw} {% endcondition %} ;;
  }

  # Measure using filter
  measure: orders_in_range {
    type: count
    filters: [is_in_date_range: "yes"]
  }

  # Multiple filter conditions
  filter: amount_range {
    type: number
  }

  measure: orders_in_amount_range {
    type: count
    sql: ${id} ;;
    filters: [
      status: "completed"
    ]
    sql: {% condition amount_range %} ${total_amount} {% endcondition %} ;;
  }
}
```

### Dashboards

**Dashboard Definition:**
```lookml
# dashboards/executive_overview.dashboard.lookml
- dashboard: executive_overview
  title: Executive Overview
  layout: newspaper
  preferred_viewer: dashboards-next

  filters:
  - name: date_range
    title: Date Range
    type: field_filter
    default_value: last 30 days
    allow_multiple_values: true
    required: false
    model: analytics
    explore: orders
    field: orders.created_date

  - name: region
    title: Region
    type: field_filter
    default_value: ""
    allow_multiple_values: true
    required: false
    model: analytics
    explore: orders
    field: users.region

  elements:
  # Revenue tile
  - name: total_revenue
    title: Total Revenue
    model: analytics
    explore: orders
    type: single_value
    fields: [orders.total_revenue]
    filters:
      orders.status: completed
    sorts: [orders.total_revenue desc]
    limit: 500
    listen:
      date_range: orders.created_date
      region: users.region
    row: 0
    col: 0
    width: 6
    height: 4

  # Order count tile
  - name: order_count
    title: Total Orders
    model: analytics
    explore: orders
    type: single_value
    fields: [orders.count]
    listen:
      date_range: orders.created_date
      region: users.region
    row: 0
    col: 6
    width: 6
    height: 4

  # Revenue trend chart
  - name: revenue_trend
    title: Revenue Trend
    model: analytics
    explore: orders
    type: looker_line
    fields: [orders.created_date, orders.total_revenue, orders.count]
    fill_fields: [orders.created_date]
    sorts: [orders.created_date desc]
    limit: 500
    x_axis_gridlines: false
    y_axis_gridlines: true
    show_view_names: false
    show_y_axis_labels: true
    show_y_axis_ticks: true
    y_axis_tick_density: default
    y_axis_tick_density_custom: 5
    show_x_axis_label: true
    show_x_axis_ticks: true
    y_axis_scale_mode: linear
    x_axis_reversed: false
    y_axis_reversed: false
    plot_size_by_field: false
    trellis: ''
    stacking: ''
    limit_displayed_rows: false
    legend_position: center
    point_style: none
    show_value_labels: false
    label_density: 25
    x_axis_scale: auto
    y_axis_combined: true
    show_null_points: true
    interpolation: linear
    y_axes: [{label: Revenue, orientation: left, series: [{axisId: orders.total_revenue,
            id: orders.total_revenue, name: Total Revenue}], showLabels: true, showValues: true,
        unpinAxis: false, tickDensity: default, tickDensityCustom: 5, type: linear}]
    series_colors:
      orders.total_revenue: "#1f77b4"
    listen:
      date_range: orders.created_date
      region: users.region
    row: 4
    col: 0
    width: 12
    height: 6

  # Top products table
  - name: top_products
    title: Top Products
    model: analytics
    explore: orders
    type: looker_grid
    fields: [products.name, order_items.total_quantity, order_items.total_revenue]
    sorts: [order_items.total_revenue desc]
    limit: 10
    show_view_names: false
    show_row_numbers: true
    transpose: false
    truncate_text: true
    hide_totals: false
    hide_row_totals: false
    size_to_fit: true
    table_theme: white
    limit_displayed_rows: false
    enable_conditional_formatting: true
    header_text_alignment: left
    header_font_size: '12'
    rows_font_size: '12'
    conditional_formatting: [{type: along a scale..., value: !!null '', background_color: !!null '',
        font_color: !!null '', color_application: {collection_id: default, palette_id: default-sequential-0},
        bold: false, italic: false, strikethrough: false, fields: [order_items.total_revenue]}]
    listen:
      date_range: orders.created_date
      region: users.region
    row: 10
    col: 0
    width: 12
    height: 6
```

### Access Control and Security

**User Attributes:**
```lookml
# Access filters based on user attributes
explore: orders {
  access_filter: {
    field: users.country
    user_attribute: country
  }

  access_filter: {
    field: users.region
    user_attribute: user_region
  }

  # SQL always where with user attribute
  sql_always_where:
    {% if _user_attributes['department'] == 'finance' %}
      ${orders.status} = 'completed'
    {% else %}
      1=1
    {% endif %}
  ;;
}
```

**Field-Level Security:**
```lookml
view: users {
  dimension: email {
    type: string
    sql: ${TABLE}.email ;;
    # Hide from non-admin users
    required_access_grants: [admin_only]
  }

  dimension: ssn {
    type: string
    sql: ${TABLE}.ssn ;;
    # Multiple required grants (AND logic)
    required_access_grants: [admin_only, pii_access]
  }
}

# Define access grants
access_grant: admin_only {
  user_attribute: role
  allowed_values: ["admin", "super_admin"]
}

access_grant: pii_access {
  user_attribute: can_see_pii
  allowed_values: ["yes"]
}
```

## Best Practices

### 1. View Design
- Use primary keys on all views
- Create dimension groups for dates
- Add descriptions to all fields
- Use value_format_name for consistent formatting
- Hide technical fields from users
- Use drill_fields for exploration paths

### 2. Explore Design
- Join dimensions and fact tables appropriately
- Understand and use correct relationship types
- Use symmetric aggregates for one-to-many joins
- Apply sql_always_where for data filtering
- Set sensible always_filter defaults
- Use aggregate awareness for performance

### 3. Performance
- Use persistent derived tables for complex calculations
- Implement aggregate tables for common queries
- Set appropriate datagroups for caching
- Use indexes on PDT join keys
- Limit explore field exposure
- Monitor and optimize slow queries

### 4. Maintainability
- Use consistent naming conventions
- Organize views by domain
- Create reusable dimensions with extends
- Document complex logic
- Use refinements to avoid duplication
- Version control LookML in Git

### 5. Governance
- Implement access controls with user attributes
- Use field-level security for sensitive data
- Create curated explores for different audiences
- Document data lineage
- Establish naming standards

## Anti-Patterns

### 1. Symmetric Aggregate Issues
```lookml
# Bad: Incorrect fanout handling
measure: total_items {
  type: sum
  sql: ${order_items.quantity} ;;  # Will double-count with 1-to-many join
}

# Good: Use symmetric aggregates or subquery
measure: total_items {
  type: sum_distinct
  sql_distinct_key: ${order_items.id} ;;
  sql: ${order_items.quantity} ;;
}
```

### 2. Not Using Primary Keys
```lookml
# Bad: No primary key
view: users {
  dimension: id { type: number }
}

# Good: Define primary key
view: users {
  dimension: id {
    primary_key: yes
    type: number
  }
}
```

### 3. Hardcoded Values
```lookml
# Bad: Hardcoded logic
dimension: is_current_year {
  sql: YEAR(${created_date}) = 2024 ;;
}

# Good: Dynamic logic
dimension: is_current_year {
  sql: YEAR(${created_date}) = YEAR(CURRENT_DATE) ;;
}
```

### 4. Missing Descriptions
```lookml
# Bad: No documentation
dimension: ltv { type: number sql: ${TABLE}.ltv ;; }

# Good: Clear documentation
dimension: ltv {
  type: number
  sql: ${TABLE}.ltv ;;
  label: "Lifetime Value"
  description: "Total revenue from customer over all time"
  value_format_name: usd
}
```

## Resources

- [LookML Reference](https://cloud.google.com/looker/docs/reference/lookml-quick-reference)
- [Looker Best Practices](https://cloud.google.com/looker/docs/best-practices)
- [Looker Community](https://community.looker.com/)
- [Looker Discourse](https://discourse.looker.com/)
- [LookML Validator](https://cloud.google.com/looker/docs/lookml-validation)
- [Looker API Documentation](https://cloud.google.com/looker/docs/reference/looker-api)
- [Looker GitHub](https://github.com/looker)
