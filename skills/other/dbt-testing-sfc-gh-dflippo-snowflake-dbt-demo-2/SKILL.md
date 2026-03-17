---
name: dbt-testing
description:
  dbt testing strategies using dbt_constraints for database-level enforcement, generic tests, and
  singular tests. Use this skill when implementing data quality checks, adding primary/foreign key
  constraints, creating custom tests, or establishing comprehensive testing frameworks across
  bronze/silver/gold layers.
---

# dbt Testing

## Purpose

Transform AI agents into experts on dbt testing strategies, providing guidance on implementing
comprehensive data quality checks with database-enforced constraints, generic tests, and custom
singular tests to ensure data integrity across all layers.

## When to Use This Skill

Activate this skill when users ask about:

- Implementing data quality tests
- Adding primary key and foreign key constraints
- Using dbt_constraints package for database-level enforcement
- Creating generic (reusable) tests
- Writing singular (one-off) tests
- Testing strategies by layer (bronze/silver/gold)
- Debugging test failures
- Configuring test severity levels
- Storing test failures for analysis

**Official dbt Documentation**: [Testing](https://docs.getdbt.com/docs/build/tests)

---

## Testing Philosophy

Implement tests in this order for maximum data quality:

1. **Primary Keys** - Every dimension must have one
2. **Foreign Keys** - All fact relationships
3. **Unique Keys** - Business key constraints
4. **Business Rules** - Domain-specific validations
5. **Data Quality** - Completeness, accuracy, consistency

---

## Why Use dbt_constraints?

The `dbt_constraints` package provides database-level enforcement (not just dbt tests):

✅ **Database Enforcement** - Creates actual constraints in the data warehouse ✅ **Performance** -
Database-level constraints improve query optimization ✅ **Data Integrity** - Prevents invalid data
at all access points (not just dbt) ✅ **Documentation** - Constraints visible in database metadata
and BI tools ✅ **Query Optimization** - Database can use constraints for better execution plans

**Standard dbt tests** only validate during `dbt test` runs. **dbt_constraints** creates real
database constraints that are enforced 24/7.

**Official dbt_constraints Documentation**:
[GitHub - Snowflake-Labs/dbt_constraints](https://github.com/Snowflake-Labs/dbt_constraints)

---

## Package Installation

```yaml
# packages.yml
packages:
  - package: Snowflake-Labs/dbt_constraints
    version: [">=0.8.0", "<1.0.0"]

  - package: dbt-labs/dbt_utils
    version: [">=1.0.0", "<2.0.0"]
```

Install packages:

```bash
dbt deps
```

**Official dbt Docs**: [Package Management](https://docs.getdbt.com/docs/build/packages)

---

## Primary Key Testing

### Simple Primary Key (dbt_constraints)

**Required for every dimension:**

```yaml
# models/gold/_models.yml
models:
  - name: dim_customers
    columns:
      - name: customer_id
        tests:
          - dbt_constraints.primary_key
```

### Composite Primary Key

**When primary key spans multiple columns:**

```yaml
models:
  - name: fct_order_lines
    tests:
      - dbt_constraints.primary_key:
          column_names:
            - order_id
            - line_number
```

### Alternative: Built-in dbt Tests

**Not recommended - no database enforcement:**

```yaml
columns:
  - name: product_id
    tests:
      - not_null
      - unique
```

**Limitation**: Only validates during `dbt test` runs, doesn't prevent bad data from other sources.

---

## Foreign Key Testing

### Simple Foreign Key (dbt_constraints)

**Ensures referential integrity:**

```yaml
models:
  - name: fct_orders
    columns:
      - name: customer_id
        tests:
          - dbt_constraints.foreign_key:
              pk_table_name: ref('dim_customers')
              pk_column_name: customer_id
```

### Multiple Foreign Keys

**For facts with multiple dimension relationships:**

```yaml
models:
  - name: fct_order_lines
    columns:
      - name: order_id
        tests:
          - dbt_constraints.foreign_key:
              pk_table_name: ref('fct_orders')
              pk_column_name: order_id

      - name: product_id
        tests:
          - dbt_constraints.foreign_key:
              pk_table_name: ref('dim_products')
              pk_column_name: product_id

      - name: customer_id
        tests:
          - dbt_constraints.foreign_key:
              pk_table_name: ref('dim_customers')
              pk_column_name: customer_id
```

### Alternative: Built-in dbt Relationships Test

**Not recommended - no database enforcement:**

```yaml
columns:
  - name: customer_id
    tests:
      - relationships:
          to: ref('dim_customers')
          field: customer_id
```

---

## Unique Key Testing

### Simple Unique Key (dbt_constraints)

**For business keys (non-primary keys that must be unique):**

```yaml
columns:
  - name: customer_email
    tests:
      - dbt_constraints.unique_key
```

### Composite Unique Key

**When uniqueness spans multiple columns:**

```yaml
models:
  - name: stg_orders
    tests:
      - dbt_constraints.unique_key:
          column_names:
            - order_number
            - order_source
```

---

## Generic Tests (Reusable)

### Built-in dbt Tests

```yaml
columns:
  - name: order_status
    tests:
      - not_null
      - accepted_values:
          values: ["pending", "processing", "shipped", "delivered", "cancelled"]

  - name: order_amount
    tests:
      - not_null
```

### dbt_utils Tests

**Powerful generic tests from dbt_utils package:**

```yaml
columns:
  - name: customer_email
    tests:
      - dbt_utils.not_null_proportion:
          at_least: 0.95 # 95% of rows must have email

  - name: order_amount
    tests:
      - dbt_utils.accepted_range:
          min_value: 0
          max_value: 1000000

  - name: customer_status
    tests:
      - dbt_utils.not_empty_string
```

**Official dbt_utils Documentation**:
[dbt_utils - Generic Tests](https://github.com/dbt-labs/dbt-utils#generic-tests)

---

### Custom Generic Tests

**Create reusable test for common patterns:**

```sql
-- tests/generic/test_positive_values.sql
{% test positive_values(model, column_name) %}

select count(*)
from {{ model }}
where {{ column_name }} <= 0

{% endtest %}
```

**Usage:**

```yaml
columns:
  - name: order_total
    tests:
      - positive_values

  - name: quantity
    tests:
      - positive_values
```

**Another Example: Date Range Test**

```sql
-- tests/generic/test_recent_data.sql
{% test recent_data(model, column_name, days_ago=30) %}

select count(*)
from {{ model }}
where {{ column_name }} < dateadd(day, -{{ days_ago }}, current_date())

{% endtest %}
```

**Usage:**

```yaml
columns:
  - name: order_date
    tests:
      - recent_data:
          days_ago: 7 # Alert if no orders in last 7 days
```

---

## Singular Tests (One-Off)

**For complex business logic that doesn't fit generic tests:**

```sql
-- tests/singular/test_order_dates_sequential.sql
with date_validation as (
    select
        o.order_id,
        o.order_date,
        c.signup_date
    from {{ ref('fct_orders') }} o
    join {{ ref('dim_customers') }} c
        on o.customer_id = c.customer_id
    where o.order_date < c.signup_date  -- Order before signup = invalid
)

select * from date_validation
```

**Test fails if ANY rows are returned.**

### More Singular Test Examples

**Revenue Reconciliation:**

```sql
-- tests/singular/test_revenue_reconciliation.sql
-- Ensure fact table revenue matches source system
with fact_revenue as (
    select sum(order_amount) as total_revenue
    from {{ ref('fct_orders') }}
    where order_date = current_date() - 1
),

source_revenue as (
    select sum(amount) as total_revenue
    from {{ source('erp', 'orders') }}
    where order_date = current_date() - 1
),

comparison as (
    select
        f.total_revenue as fact_revenue,
        s.total_revenue as source_revenue,
        abs(f.total_revenue - s.total_revenue) as difference
    from fact_revenue f
    cross join source_revenue s
)

select * from comparison
where difference > 0.01  -- Tolerance of 1 cent
```

**Referential Integrity Check:**

```sql
-- tests/singular/test_orphaned_orders.sql
-- Find orders with invalid customer_id (not in dim_customers)
select
    o.order_id,
    o.customer_id
from {{ ref('fct_orders') }} o
left join {{ ref('dim_customers') }} c
    on o.customer_id = c.customer_id
where c.customer_id is null
  and o.customer_id != -1  -- Exclude ghost key
```

**Official dbt Documentation**:
[Singular Tests](https://docs.getdbt.com/docs/build/tests#singular-tests)

---

## Testing by Layer

### Bronze Layer (Staging)

**Focus**: Basic data quality at source

```yaml
models:
  - name: stg_tpc_h__customers
    columns:
      - name: customer_id
        tests:
          - dbt_constraints.primary_key

      - name: customer_email
        tests:
          - not_null
```

**Keep it simple** - just verify source data integrity.

---

### Silver Layer (Intermediate)

**Focus**: Business rule validation, calculated fields

```yaml
models:
  - name: int_customers__with_orders
    columns:
      - name: customer_id
        tests:
          - dbt_constraints.primary_key

      - name: lifetime_orders
        tests:
          - not_null
          - dbt_utils.accepted_range:
              min_value: 0

      - name: lifetime_value
        tests:
          - not_null
          - dbt_utils.accepted_range:
              min_value: 0
```

**Add business logic validation** - ensure calculated fields make sense.

---

### Gold Layer (Marts)

**Focus**: Comprehensive constraint enforcement with dbt_constraints

```yaml
models:
  - name: dim_customers
    description: "Customer dimension with full history and metrics"
    columns:
      - name: customer_id
        description: "Unique customer identifier"
        tests:
          - dbt_constraints.primary_key

      - name: customer_tier
        description: "Customer value classification"
        tests:
          - accepted_values:
              values: ["bronze", "silver", "gold", "platinum"]

      - name: customer_email
        tests:
          - dbt_constraints.unique_key

  - name: fct_orders
    description: "Order transactions fact table"
    columns:
      - name: order_id
        tests:
          - dbt_constraints.primary_key

      - name: customer_id
        tests:
          - dbt_constraints.foreign_key:
              pk_table_name: ref('dim_customers')
              pk_column_name: customer_id

      - name: product_id
        tests:
          - dbt_constraints.foreign_key:
              pk_table_name: ref('dim_products')
              pk_column_name: product_id

      - name: order_amount
        tests:
          - not_null
          - dbt_utils.accepted_range:
              min_value: 0
```

**Maximum enforcement** - use all constraint types to ensure production data quality.

---

## Test Configuration

### Store Test Failures

**Analyze failed test records:**

```bash
dbt test --store-failures
```

```yaml
# dbt_project.yml
tests:
  +store_failures: true
  +schema: dbt_test_failures
```

**Query failures:**

```sql
select * from dbt_test_failures.not_null_dim_customers_customer_email
```

---

### Test Severity Levels

**Warn vs Error:**

```yaml
columns:
  - name: customer_email
    tests:
      - dbt_constraints.unique_key:
          config:
            severity: warn # or 'error' (default)
```

**Severity Behavior:**

- `error`: Test failure stops dbt execution (exit code 1)
- `warn`: Test failure logs warning but continues (exit code 0)

**Use `warn` for**:

- Data quality checks that shouldn't block deployment
- Known edge cases during migration
- Monitoring tests

---

### Limit Test Execution

**Test specific model:**

```bash
dbt test --select dim_customers
```

**Test by type:**

```bash
dbt test --select test_type:generic    # All generic tests
dbt test --select test_type:singular   # All singular tests
```

**Test with dependencies:**

```bash
dbt test --select +dim_customers+  # Test model and all dependencies
```

**Official dbt Documentation**:
[Test Selection](https://docs.getdbt.com/reference/node-selection/test-selection-examples)

---

## Running Tests

```bash
# Run all tests
dbt test

# Build models and test together (recommended)
dbt build  # Runs models, then tests

# Test specific model
dbt test --select dim_customers

# Test specific column
dbt test --select dim_customers,column:customer_id

# Test by layer
dbt test --select tag:gold

# Test with failures stored
dbt test --store-failures --select fct_orders
```

**Best Practice**: Use `dbt build` instead of `dbt run` + `dbt test` separately.

---

## Testing Best Practices

### 1. Test Early and Often

Add tests as you build models, not after deployment.

### 2. Layer-Appropriate Testing

- **Bronze**: Basic not_null and primary key tests
- **Silver**: Business rule validation, range checks
- **Gold**: Comprehensive constraint enforcement with dbt_constraints

### 3. Use dbt_constraints for Production

Database-level constraints provide:

- 24/7 enforcement (not just during dbt runs)
- Performance optimization
- Better integration with BI tools

### 4. Document Test Purpose

```yaml
columns:
  - name: customer_tier
    description: "Customer segmentation based on lifetime value"
    tests:
      - accepted_values:
          values: ["bronze", "silver", "gold", "platinum"]
          config:
            severity: error
```

### 5. Balance Coverage vs Performance

- Don't over-test trivial columns
- Focus on business-critical fields
- Use sampling for very large tables if needed

---

## Testing Checklist

Before moving to production:

- [ ] All dimensions have primary key tests
- [ ] All facts have foreign key tests to dimensions
- [ ] Business rules are validated with tests
- [ ] Data quality tests are in place (not_null, accepted_values)
- [ ] Tests run successfully in CI/CD pipeline
- [ ] dbt_constraints enabled for all production marts
- [ ] Test failures configured to store in database
- [ ] Singular tests created for complex business logic

---

## Helping Users with Testing

### Strategy for Assisting Users

When users ask about testing:

1. **Identify model type**: Dimension? Fact? Intermediate?
2. **Recommend appropriate tests**: By layer and purpose
3. **Prioritize constraints**: Primary keys → Foreign keys → Business rules
4. **Provide complete examples**: Working YAML configurations
5. **Explain benefits**: Why dbt_constraints over standard tests
6. **Show how to run**: Commands and debugging approaches

### Common User Questions

**"What tests should I add?"**

- Start with dbt_constraints for primary/foreign keys
- Add not_null for required fields
- Use accepted_values for enums
- Create singular tests for complex business logic

**"Why use dbt_constraints instead of regular tests?"**

- Database-level enforcement (24/7, not just during dbt runs)
- Better query performance
- Prevents bad data from any source
- Visible in database metadata

**"How do I debug test failures?"**

- Use `--store-failures` to save failing records
- Query the test failure table
- Review actual data that failed the test
- Add more specific tests to isolate issue

---

## Related Official Documentation

- [dbt Docs: Tests](https://docs.getdbt.com/docs/build/tests)
- [dbt_constraints Package](https://github.com/Snowflake-Labs/dbt_constraints)
- [dbt_utils Generic Tests](https://github.com/dbt-labs/dbt-utils#generic-tests)
- [dbt Docs: Test Selection](https://docs.getdbt.com/reference/node-selection/test-selection-examples)

---

**Goal**: Transform AI agents into expert dbt testers who implement comprehensive, database-enforced
data quality checks that protect data integrity across all layers and access patterns.
