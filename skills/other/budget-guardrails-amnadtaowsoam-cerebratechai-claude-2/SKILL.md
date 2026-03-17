---
name: Budget Guardrails and Cost Controls
description: Implementation of preventive and detective controls to prevent cloud bill shock and ensure fiscal governance.
---

# Budget Guardrails and Cost Controls

## Overview

Budget Guardrails are a set of automated policies and workflows designed to prevent "bill shock"—unforeseen spikes in cloud spending. While observability tells you when you've spent money, guardrails prevent you from spending more than you planned.

**Core Principle**: "Governance at scale requires automation, not just spreadsheets."

---

## 1. Budget Types and Hierarchies

Effective governance requires dividing the total budget into manageable segments.

| Budget Type | Scope | Ownership |
| :--- | :--- | :--- |
| **Departmental** | Entire Engineering or Marketing org. | CTO / VP |
| **Project** | A specific initiative (e.g., "Migration to K8s"). | Project Manager |
| **Environment** | Dev vs. Staging vs. Production. | Platform Team |
| **Sandbox** | Individual developer playgrounds. | Individual Engineer |

### Buffer Allocation
Always include a **10-20% Buffer**. Cloud costs are rarely 100% predictable due to unexpected traffic spikes or scaling events.

---

## 2. Enforcement Mechanisms

### Soft Limits (Detective)
*   **Action**: Alerts sent to Slack/Email.
*   **Impact**: Non-disruptive.
*   **Best For**: Production environments where uptime is more critical than cost.

### Hard Limits (Preventive)
*   **Action**: Resources are stopped, scaled to zero, or new provisioning is blocked.
*   **Impact**: Disruptive.
*   **Best For**: Sandbox environments, non-critical Dev labs, and high-risk API services.

---

## 3. Alert Thresholds and Escalation

Don't wait until 100% of the budget is spent to alert the team.

*   **50% Threshold**: Informational. "Halfway through the month, everything looks normal."
*   **80% Threshold**: Warning. "Slowing down non-essential testing."
*   **100% Threshold**: Critical. "Immediate review required; evaluate shutdown of non-prod infra."
*   **Forecasted Overrun**: Predictive. "At current burn rate, we will exceed budget by the 25th."

---

## 4. Automation: Cloud-Native Cost Controls

### AWS: Budgets + Lambda Auto-Shutdown
AWS Budgets can trigger an Action (via SNS) to a Lambda function which stops instances.

```python
import boto3

# Lambda to stop EC2 instances when budget is hit
def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    # Filter for non-production instances
    instances = ec2.describe_instances(Filters=[{'Name': 'tag:Env', 'Values': ['Dev']}])
    
    instance_ids = []
    for reservation in instances['Reservations']:
        for instance in reservation['Instances']:
            instance_ids.append(instance['InstanceId'])
            
    if instance_ids:
        ec2.stop_instances(InstanceIds=instance_ids)
        return f"Stopped {len(instance_ids)} instances."
```

### GCP: Budget Alerts + Cloud Functions
GCP can notify a Cloud Function to disable billing for a project (Extreme measure).

---

## 5. Resource Quotas (Cloud and K8s)

Quotas limit the *quantity* of resources to prevent runaway spend.

### Kubernetes ResourceQuotas
Limit the total CPU/Memory a namespace can consume.
```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: team-alpha-quota
  namespace: team-alpha
spec:
  hard:
    requests.cpu: "4"
    requests.memory: 8Gi
    limits.cpu: "8"
    limits.memory: 16Gi
```

### Cloud Service Quotas
*   **AWS Service Quotas**: Limit the max number of Running on-demand instances (e.g., limit P3/P4 GPU instances to 1).

---

## 6. Developer Self-Service and "Shift-Left" Cost

The goal is to provide cost feedback to developers *before* they deploy.

### Infracost (The "Pre-flight" check)
Infracost analyzes Terraform/HCL and lists the monthly cost in the Git Pull Request.

```markdown
# Pull Request Cost Estimate
+ $156.22 / month
----------------------------------
+ 2 x aws_instance.web_server ($86.40)
+ 1 x aws_db_instance.db_prod ($69.82)
```

---

## 7. Sandbox Environment Management

Sandbox accounts are often where massive waste occurs.

1.  **Time-Boxing**: Auto-delete any resource without a `LeaseExpiration` tag.
2.  **Nightly Shutdown**: Stop all non-critical development VMs at 7:00 PM and restart at 8:00 AM (saves ~65% of compute cost).
3.  **Restricted Instance Types**: Prevent developers from spinning up high-cost instance types (e.g., `x1e.32xlarge`) via SCP (Service Control Policies).

---

## 8. Runaway Resource Protection

*   **Cleanup Policies**: S3 Lifecycle for logs after 30 days. Auto-delete EBS snapshots older than 14 days.
*   **Idle Instance Detection**: Use **AWS Trusted Advisor** or **Azure Advisor** to identify zombies.
*   **Kill-Switch for LLM/Batch**: Stop long-running processing jobs that exceed a time-limit.

---

## 9. Governance Framework: The Monthly Review

A successful FinOps culture requires a regular meeting:

1.  **Review Spikes**: Why did spend increase on the 10th?
2.  **Budget Alignment**: Are we on track for the quarter?
3.  **Optimize Backlog**: Which "Right-sizing" recommendations are we implementing this month?
4.  **Unit Economics Update**: Is our cost per user still profitable?

---

## 10. Tools for Budget Guardrails

1.  **AWS Budgets / AWS Control Tower**.
2.  **GCP Quotas / Budgets**.
3.  **Terraform-cost-estimation** (TFE).
4.  **Infracost** (CI/CD integration).
5.  **CloudCustodian**: A powerful open-source engine for writing YAML policies to manage cloud resources (e.g., "Delete any unencrypted volume").

---

## 11. Real-World Case Study: Preventing the $60,000 Oops
*   **Scenario**: A developer accidentally started a script that spun up 100 GPU instances in a test account.
*   **Guardrail in Place**: An AWS Budget set to $500/day for the Test Account.
*   **Outcome**: When the spend hit $500 (within 2 hours), the Budget triggered a Lambda that wiped all resources in the test account and revoked the developer's IAM permissions for 24 hours. 
*   **Savings**: Estimated $59,500 saved compared to a weekend of undetected usage.

---

## Related Skills
* `42-cost-engineering/cost-observability`
* `42-cost-engineering/cloud-cost-models`
* `44-ai-governance/ai-risk-management`
