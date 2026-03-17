---
name: Data Quality Monitoring
description: Techniques and tools for ensuring the accuracy, completeness, and reliability of data across the pipeline.
---

# Data Quality Monitoring

## Overview

Data Quality (DQ) Monitoring is the continuous process of validating data against predefined rules and expectations. In a modern data stack, monitoring must happen at every stage: **Ingestion**, **Transformation**, and **Serving**.

**Core Principle**: "Garbage in, garbage out. If the data is wrong, the analytics, AI, and decisions will be wrong too."

---

## 1. The Six Dimensions of Data Quality

Common industry standards for measuring data health:

| Dimension | Definition | Example Metric |
| :--- | :--- | :--- |
| **Accuracy** | Does the data reflect reality? | % of records matching the source system. |
| **Completeness**| Are there missing values? | % of non-null values in mandatory fields. |
| **Consistency** | Does data match across systems? | Do user names match in both SQL and Redis? |
| **Timeliness** | Is data fresh enough? | Data latency (current time - event time). |
| **Uniqueness** | Are there duplicate records? | Count of duplicate primary keys. |
| **Validity** | Does it follow specified formats?| % of emails following the regex pattern. |

---

## 2. Automated DQ Testing (Frameworks)

### A. dbt (Data Build Tool) Tests
Ideal for SQL-based transformations.
```yaml
# schema.yml
models:
  - name: active_users
    columns:
      - name: user_id
        tests:
          - unique
          - not_null
      - name: age
        tests:
          - accepted_values:
              values: [18, 120]
```

### B. Great Expectations (Python)
The most flexible tool for complex Python-based data pipelines.
```python
import great_expectations as ge

df = ge.read_csv("data.csv")
df.expect_column_values_to_be_between("age", 18, 120)
df.expect_column_values_to_not_be_null("email")
df.expect_column_values_to_match_regex("email", r"[\w.-]+@[\w.-]+")
```

---

## 3. Real-Time DQ with SQL Assertions

You can run "Check" queries alongside your production workload to catch silent failures.

```sql
-- Detect "Price Drift" anomaly
SELECT 
    product_id, 
    AVG(price) OVER(PARTITION BY category) as avg_cat_price,
    price
FROM current_inventory
WHERE price > (avg_cat_price * 5) -- Alert if price is 5x the average
```

---

## 4. Monitoring Tools Landscape

| Tool | Focus | Best For |
| :--- | :--- | :--- |
| **Great Expectations**| Validation | Python pipelines, Airflow integration. |
| **Monte Carlo** | Data Observability | ML-driven anomaly detection, lineage. |
| **Soda** | Data Contracts / Monitoring | Collaborative DQ for Data & Business teams. |
| **Anodot** | Streaming Anomaly | Catching spikes/dips in real-time metrics. |

---

## 5. Data Profiling and Drift Detection

**Data Drift** occurs when the statistical properties of the data change over time, even if the schema stays the same.

*   **Schema Drift**: Adding/Removing columns.
*   **Concept Drift**: The meaning of a value changes (e.g., "Active" now means something different).
*   **Predictive Drift**: Distribution of data shifts (e.g., average purchase value drops by 50%).

---

## 6. DQ Incident Management

When a monitor fails, it should trigger an incident workflow:
1.  **Detect**: Alert fires (Slack/PagerDuty).
2.  **Triage**: Is the data just late, or is it incorrect?
3.  **Isolation**: Block downstream pipelines to prevent "polluting" the data warehouse.
4.  **Remediation**: Re-run the pipeline or fix the source code.
5.  **Validation**: Verify the fix.

---

## 7. The Data Quality Dashboard

A high-level view for stakeholders:
*   **DQ Score**: (0-100) Aggregated health of all datasets.
*   **Freshness SLA**: % of pipelines meeting their timeliness target.
*   **Top Failing Tests**: Which columns are most problematic?
*   **Time to Resolve**: Average time to fix DQ incidents.

---

## 8. Real-World Scenario: E-commerce Ghost Orders
*   **Scenario**: A promotional campaign led to a surge in orders, but a bug caused the `tax_amount` to be 0 for all of them.
*   **Detection**: A DQ monitor was in place checking that `tax_amount > 0` for all non-exempt regions.
*   **Response**: The monitor failed at 2:00 AM. The data pipeline was automatically paused.
*   **Outcome**: The finance team was notified before the morning report was generated. The tax glitch was fixed, preventing thousands of incorrect invoices.

---

## 9. DQ Monitoring Checklist

* [ ] **Completeness**: Are there checks for `NULL` values in primary keys?
* [ ] **Freshness**: Do we have alerts for data that hasn't arrived in X hours?
* [ ] **Volume**: Sudden drop or spike in row count (e.g., < 50% of typical volume)?
* [ ] **Distribution**: Has the average or median value shifted significantly today?
* [ ] **Schema**: Have any columns been renamed or dropped?
* [ ] **Downstream blocking**: Does a failure stop downstream tasks automatically?

---

## Related Skills
* `43-data-reliability/data-contracts`
* `43-data-reliability/data-lineage`
* `42-cost-engineering/cost-observability`
