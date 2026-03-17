---
name: Cost Observability and Monitoring
description: Techniques for gaining visibility into cloud spending, attributing costs to business units, and detecting financial anomalies.
---

# Cost Observability and Monitoring

## Overview

Cost Observability is the practice of extending traditional system observability (logs, metrics, traces) to include **Financial** data. It allows engineering teams to answer not just "Is the system healthy?" but "Is the system cost-effective?".

**Core Principle**: "Total spend is a vanity metric; cost per unit of work is a performance metric."

---

## 1. Key Cost Metrics to Track

The goal is to move from **Macro** visibility (the bill) to **Micro** visibility (the request).

| Metric | Level | Purpose |
| :--- | :--- | :--- |
| **Total Monthly Spend** | Executive | General budget health. |
| **Cost per Service** | Engineering | Identify inefficient microservices. |
| **Cost per Customer (Unit Cost)**| Product | Calculate per-account profitability. |
| **Cost per Request** | Engineering | Measure efficiency of application code. |
| **COGS (Cost of Goods Sold)** | Financial | The base cost to deliver the service. |

---

## 2. Cost Attribution and Tagging Strategy

Attribution is impossible without consistent metadata.

### The Standard Tagging Schema
Every resource should have the following "FinOps Tags":

1.  **`Environment`**: (e.g., `prod`, `staging`, `dev`)
2.  **`Service`**: (e.g., `auth-api`, `image-processor`)
3.  **`Owner`**: (e.g., `team-alpha`)
4.  **`Project`**: (e.g., `project-phoenix`)
5.  **`TenantID`**: (If using siloed resources per customer)

### Enforcement Policy (Terraform/OpenTofu)
```hcl
# Use a variable for mandatory tags
locals {
  mandatory_tags = {
    Environment = var.environment
    Service     = "payment-gateway"
    Owner       = "finance-team"
    CostCenter  = "9921"
  }
}

resource "aws_instance" "app" {
  ami           = "ami-12345"
  instance_type = "t3.medium"
  tags          = local.mandatory_tags
}
```

---

## 3. Cost Anomaly Detection

A financial anomaly is a sudden deviate from historical spend patterns.

### Types of Anomalies
1.  **Sudden Spikes**: A developers spins up a massive GPU instance and forgets to delete it.
2.  **Gradual Drift**: A memory leak causes auto-scaling to add a new server every day.
3.  **Cyclical Variation**: Spend increases during weekends when it should be lower.

### Anomaly Alert Example (Slack/PagerDuty)
*   **Alert**: "AWS Spend Spike Detected"
*   **Metric**: `S3 Egress`
*   **Deviation**: +450% over the last 24 hours.
*   **Likely Cause**: Possible data exfiltration or misconfigured backup script.

---

## 4. Application-Level Cost Tracking

Sometimes cloud tags aren't granular enough (e.g., when multiple customers share one database).

### OpenTelemetry for Cost
You can inject "cost attributes" into your traces to calculate the price of a specific API endpoint.

```typescript
// Example: Tracking LLM cost in a trace
import { trace } from '@opentelemetry/api';

const span = trace.getTracer('llm-tracer').startSpan('generate_text');
// ... perform LLM call
const cost = (inputTokens * 0.00001) + (outputTokens * 0.00003);

span.setAttribute('app.cost.usd', cost);
span.setAttribute('app.tokens.input', inputTokens);
span.end();
```

---

## 5. Dashboard Templates

### Engineering Dashboard (Grafana)
*   **Top 5 Costliest Microservices** (Bar chart)
*   **Idle Resource Count** (Single stat)
*   **Compute Efficiency** (CPU utilization vs. Cost)
*   **Data Egress by Region** (Pie chart)

### Product/Executive Dashboard
*   **Revenue vs. Infrastructure Cost** (Area chart)
*   **Margin per Feature** (Heatmap)
*   **Cost per Daily Active User (DAU)** (Line chart)

---

## 6. Tools Ecosystem

### Native Cloud Tools
*   **AWS Cost Explorer**: Best for monthly trends and filtered views.
*   **AWS Cost Anomaly Detection**: Uses ML to flag unusual spend automatically.
*   **GCP Recommender**: Suggests specific sizing changes to save money.

### Specialized Tools
*   **CloudHealth / Cloudability**: Enterprise-grade cost allocation and multi-cloud reporting.
*   **Kubecost**: The standard for Kubernetes. It models costs based on pod resource requests.
*   **Infracost**: A CLI tool that runs in CI/CD to tell you how much a Pull Request will cost before it's merged.

---

## 7. Chargeback vs. Showback

How do you hold teams accountable?

| Model | Description | Pros | Cons |
| :--- | :--- | :--- | :--- |
| **Showback** | Reporting costs to teams without actually billing their budgets. | Low friction, creates awareness. | No "teeth"; teams can ignore. |
| **Chargeback**| Directly deducting cloud costs from a department's real budget. | Forces accountability, drives optimization. | High administrative overhead. |

---

## 8. Cost Forecasting

Forecasting helps avoid end-of-quarter budget surprises.

1.  **Linear Projection**: `NextMonth = ThisMonthAverage * GrowthRate`.
2.  **Seasonal aware**: Accounting for peak periods like Black Friday or holiday sales.
3.  **Scenario Planning**: "If we double our user base, what happens to our NAT Gateway costs?"

---

## 9. Common Optimization Targets

*   **S3 Storage Class Analysis**: Finding buckets that could move to Infrequent Access.
*   **Database Query Analysis**: Finding a single query that causes high CPU/IOPS across thousands of DB connections.
*   **Zombie Snapshots**: Deleting EBS snapshots older than 90 days.

---

## 10. Implementation Checklist

- [ ] **Tagging Enforcement**: Do resources without tags trigger an alert or auto-deletion?
- [ ] **Accountability**: Does every `Team` have a dashboard showing their spend?
- [ ] **Thresholds**: Are there daily spending alerts set at 20% above "normal"?
- [ ] **Unit Economics**: Do we know the infrastructure cost of a single user transaction?
- [ ] **Forecasting**: Are we predicting next month's bill with < 10% error?

---

## Related Skills
- `42-cost-engineering/cloud-cost-models`
- `42-cost-engineering/budget-guardrails`
- `40-system-resilience/chaos-engineering` (using chaos to test cost stability)
