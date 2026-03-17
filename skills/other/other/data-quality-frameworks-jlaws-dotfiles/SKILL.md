---
name: data-quality-frameworks
description: Implement data quality validation with Great Expectations, dbt tests, and data contracts. Use when building data quality pipelines, implementing validation rules, or establishing data contracts.
---

# Data Quality Frameworks

## Data Quality Dimensions

| Dimension | Example Check |
|-----------|---------------|
| **Completeness** | `expect_column_values_to_not_be_null` |
| **Uniqueness** | `expect_column_values_to_be_unique` |
| **Validity** | `expect_column_values_to_be_in_set` |
| **Accuracy** | Cross-reference validation |
| **Consistency** | `expect_column_pair_values_A_to_be_greater_than_B` |
| **Timeliness** | `expect_column_max_to_be_between` |

## Pattern 1: Great Expectations Suite

```python
from great_expectations.core import ExpectationSuite
from great_expectations.core.expectation_configuration import ExpectationConfiguration

def build_orders_suite() -> ExpectationSuite:
    suite = ExpectationSuite(expectation_suite_name="orders_suite")

    # Schema
    suite.add_expectation(ExpectationConfiguration(
        expectation_type="expect_table_columns_to_match_set",
        kwargs={"column_set": ["order_id", "customer_id", "amount", "status", "created_at"], "exact_match": False}
    ))
    # Primary key
    suite.add_expectation(ExpectationConfiguration(expectation_type="expect_column_values_to_not_be_null", kwargs={"column": "order_id"}))
    suite.add_expectation(ExpectationConfiguration(expectation_type="expect_column_values_to_be_unique", kwargs={"column": "order_id"}))
    # Categorical
    suite.add_expectation(ExpectationConfiguration(
        expectation_type="expect_column_values_to_be_in_set",
        kwargs={"column": "status", "value_set": ["pending", "processing", "shipped", "delivered", "cancelled"]}
    ))
    # Numeric ranges
    suite.add_expectation(ExpectationConfiguration(
        expectation_type="expect_column_values_to_be_between",
        kwargs={"column": "amount", "min_value": 0, "max_value": 100000, "strict_min": True}
    ))
    # Row count sanity
    suite.add_expectation(ExpectationConfiguration(
        expectation_type="expect_table_row_count_to_be_between",
        kwargs={"min_value": 1000, "max_value": 10000000}
    ))
    return suite
```

## Pattern 2: Great Expectations Checkpoint

```yaml
# great_expectations/checkpoints/orders_checkpoint.yml
name: orders_checkpoint
config_version: 1.0
class_name: Checkpoint
validations:
  - batch_request:
      datasource_name: warehouse
      data_connector_name: default_inferred_data_connector_name
      data_asset_name: orders
      data_connector_query:
        index: -1
    expectation_suite_name: orders_suite
action_list:
  - name: store_validation_result
    action: { class_name: StoreValidationResultAction }
  - name: update_data_docs
    action: { class_name: UpdateDataDocsAction }
  - name: send_slack_notification
    action:
      class_name: SlackNotificationAction
      slack_webhook: ${SLACK_WEBHOOK}
      notify_on: failure
```

## Pattern 3: dbt Data Tests

```yaml
# models/marts/core/_core__models.yml
version: 2
models:
  - name: fct_orders
    tests:
      - dbt_utils.recency:
          datepart: day
          field: created_at
          interval: 1
    columns:
      - name: order_id
        tests: [unique, not_null]
      - name: customer_id
        tests:
          - not_null
          - relationships:
              to: ref('dim_customers')
              field: customer_id
      - name: order_status
        tests:
          - accepted_values:
              values: ['pending', 'processing', 'shipped', 'delivered', 'cancelled']
      - name: total_amount
        tests:
          - not_null
          - dbt_utils.expression_is_true:
              expression: ">= 0"
```

## Pattern 4: Custom dbt Tests

```sql
-- tests/generic/test_row_count_in_range.sql
{% test row_count_in_range(model, min_count, max_count) %}
with row_count as (select count(*) as cnt from {{ model }})
select cnt from row_count where cnt < {{ min_count }} or cnt > {{ max_count }}
{% endtest %}

-- tests/singular/assert_orders_customers_match.sql
with orphaned_orders as (
    select o.customer_id
    from (select distinct customer_id from {{ ref('fct_orders') }}) o
    left join {{ ref('dim_customers') }} c using (customer_id)
    where c.customer_id is null
)
select * from orphaned_orders
```

## Pattern 5: Data Contracts

```yaml
apiVersion: datacontract.com/v1.0.0
kind: DataContract
metadata:
  name: orders
  version: 1.0.0
  owner: data-platform-team
schema:
  type: object
  properties:
    order_id: { type: string, format: uuid, required: true, unique: true }
    customer_id: { type: string, format: uuid, required: true, pii: true }
    total_amount: { type: number, minimum: 0, maximum: 100000 }
    status: { type: string, enum: [pending, processing, shipped, delivered, cancelled] }
quality:
  type: SodaCL
  specification:
    checks for orders:
      - row_count > 0
      - missing_count(order_id) = 0
      - duplicate_count(order_id) = 0
      - freshness(created_at) < 24h
sla:
  availability: 99.9%
  freshness: 1 hour
  latency: 5 minutes
```

## Pattern 6: Automated Quality Pipeline

```python
from dataclasses import dataclass
from typing import List, Dict, Any
import great_expectations as gx
from datetime import datetime

@dataclass
class QualityResult:
    table: str
    passed: bool
    total_expectations: int
    failed_expectations: int
    details: List[Dict[str, Any]]

class DataQualityPipeline:
    def __init__(self, context: gx.DataContext):
        self.context = context

    def validate_table(self, table: str, suite: str) -> QualityResult:
        result = self.context.run_checkpoint(**{
            "name": f"{table}_validation", "config_version": 1.0, "class_name": "Checkpoint",
            "validations": [{"batch_request": {"datasource_name": "warehouse", "data_asset_name": table}, "expectation_suite_name": suite}],
        })
        validation_result = list(result.run_results.values())[0]
        results = validation_result.results
        failed = [r for r in results if not r.success]
        return QualityResult(
            table=table, passed=result.success, total_expectations=len(results), failed_expectations=len(failed),
            details=[{"expectation": r.expectation_config.expectation_type, "success": r.success, "observed_value": r.result.get("observed_value")} for r in results]
        )

    def run_all(self, tables: Dict[str, str]) -> Dict[str, QualityResult]:
        return {table: self.validate_table(table, suite) for table, suite in tables.items()}
```
