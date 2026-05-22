---
name: data-quality
description: Data quality testing with dbt tests, Great Expectations, and monitoring.
---

# Data Quality

## Quality Dimensions

| Dimension | Description | Test |
|-----------|-------------|------|
| **Completeness** | No missing values | NOT NULL, count checks |
| **Uniqueness** | No duplicates | UNIQUE, distinct counts |
| **Validity** | Values in range | Range checks, regex |
| **Consistency** | Matches across sources | Cross-table checks |
| **Timeliness** | Data is fresh | Freshness checks |

## dbt Tests

### Schema Tests

```yaml
models:
  - name: fct_orders
    columns:
      - name: order_id
        tests:
          - unique
          - not_null
      - name: status
        tests:
          - accepted_values:
              values: ['pending', 'completed', 'cancelled']
      - name: amount
        tests:
          - not_null
          - dbt_utils.accepted_range:
              min_value: 0
              max_value: 1000000
```

### Custom Tests

```sql
-- tests/assert_positive_revenue.sql
select *
from {{ ref('fct_orders') }}
where amount < 0
```

### Relationship Tests

```yaml
- name: customer_id
  tests:
    - relationships:
        to: ref('dim_customer')
        field: customer_id
```

## Great Expectations

```python
import great_expectations as gx

context = gx.get_context()

validator = context.sources.pandas_default.read_csv("data.csv")

validator.expect_column_values_to_not_be_null("order_id")
validator.expect_column_values_to_be_unique("order_id")
validator.expect_column_values_to_be_between("amount", 0, 1000000)

results = validator.validate()
```

## Monitoring

- Row count trends
- Null percentage trends
- Schema drift detection
- Freshness SLAs
- Anomaly detection
