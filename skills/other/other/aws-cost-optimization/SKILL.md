---
name: aws-cost-optimization
description: Provides structured AWS cost optimization guidance using five pillars (right-sizing, elasticity, pricing models, storage optimization, monitoring) and twelve actionable best practices. Use when optimizing AWS costs, reviewing AWS spending, finding unused AWS resources, implementing FinOps practices, reducing EC2/EBS/S3 bills, configuring AWS Budgets, or performing AWS Well-Architected cost reviews.
allowed-tools: Read, Write, Bash
---

# AWS Cost Optimization

## Overview

Guide a structured AWS cost review covering right-sizing, elasticity, pricing models, storage optimization, and continuous monitoring. This skill references AWS native tools (Cost Explorer, Budgets, Compute Optimizer, Trusted Advisor, Cost Anomaly Detection) and delivers twelve actionable best practices organized under five optimization pillars.

## When to Use

Use this skill when:
- Optimizing AWS costs or reviewing AWS spending
- Finding unused or under-utilized AWS resources
- Implementing FinOps practices for cloud cost governance
- Reducing EC2, EBS, S3, or load balancer bills
- Choosing between On-Demand, Spot, Reserved Instances, and Savings Plans
- Configuring AWS Budgets, Cost Explorer, or Cost Anomaly Detection
- Performing an AWS Well-Architected Framework cost pillar review
- Cleaning up orphaned EBS snapshots or unused volumes
- Implementing cost allocation tagging strategies
- Automating start/stop schedules for non-production workloads

Trigger phrases:
- "Optimize my AWS costs"
- "Review AWS spending"
- "Find unused AWS resources"
- "Help me with FinOps"
- "How can I reduce my EC2 bill?"
- "Clean up unused EBS volumes"
- "Set up AWS Budgets"

## Instructions

### Five Optimization Pillars

When performing a cost review, work through each pillar in order:

#### Pillar 1 — Right-Size

Match provisioned resources to actual workload needs.

1. Pull 14-day average CPU/memory metrics from CloudWatch for every EC2 instance
2. Cross-reference with AWS Compute Optimizer recommendations
3. Flag instances where peak utilization stays below 40%
4. Recommend downsizing to the next smaller instance family/size
5. For RDS, check read/write IOPS vs. provisioned capacity

#### Pillar 2 — Increase Elasticity

Schedule instance stop/start and leverage Auto Scaling Groups.

1. Identify non-production instances running 24/7 (dev, staging, QA)
2. Propose stop/start schedules using AWS Instance Scheduler or EventBridge rules
3. Review Auto Scaling Group policies for over-provisioned min/desired counts
4. Recommend target-tracking scaling policies tied to actual demand metrics
5. Consider Lambda or Fargate for bursty, event-driven workloads

#### Pillar 3 — Leverage the Right Pricing Model

Choose the optimal mix of On-Demand, Spot, Reserved Instances, and Savings Plans.

1. Analyze steady-state baseline using Cost Explorer "RI Coverage" and "Savings Plans Coverage" reports
2. Recommend Compute Savings Plans for consistent baseline compute
3. Suggest Spot Instances for fault-tolerant, stateless workloads (batch, CI/CD runners)
4. Evaluate existing Reserved Instances for utilization; resell unused RIs on the RI Marketplace
5. Use the AWS Pricing Calculator to model total cost under each pricing option

#### Pillar 4 — Optimize Storage

Eliminate waste in EBS, S3, and snapshots.

1. List unattached EBS volumes (`available` state) and recommend deletion after backup review
2. Identify orphaned EBS snapshots no longer linked to an active AMI or volume
3. Review S3 bucket metrics; recommend Intelligent-Tiering or lifecycle rules for infrequent access data
4. Enable Amazon Data Lifecycle Manager (DLM) for automated snapshot retention
5. Check for gp2 volumes that should be migrated to gp3 for cost and performance gains

#### Pillar 5 — Measure, Monitor, and Improve

Establish continuous cost governance.

1. Implement a cost allocation tagging strategy (e.g., `Environment`, `Team`, `Project`, `CostCenter`)
2. Configure AWS Budgets with threshold alerts (50%, 80%, 100%, forecasted)
3. Enable AWS Cost Anomaly Detection for automatic spend anomaly alerts
4. Set up a monthly Cost Explorer saved report for leadership review
5. Create a Trusted Advisor check schedule for cost optimization recommendations

### Twelve Actionable Best Practices

Present these to the user as a prioritized checklist:

| # | Best Practice | Pillar | AWS Tool |
|---|---|---|---|
| 1 | Choose appropriate AWS region (cost, latency, data sovereignty) | Right-Size | AWS Pricing Calculator |
| 2 | Schedule start/stop for non-production instances | Elasticity | Instance Scheduler / EventBridge |
| 3 | Identify under-utilized EC2 instances | Right-Size | Cost Explorer / Compute Optimizer |
| 4 | Reduce EC2 costs with Spot Instances | Pricing Model | EC2 Spot / Spot Fleet |
| 5 | Optimize Auto Scaling Group policies | Elasticity | Auto Scaling / CloudWatch |
| 6 | Use or resell under-utilized Reserved Instances | Pricing Model | RI Marketplace / Cost Explorer |
| 7 | Leverage Compute Savings Plans | Pricing Model | Savings Plans Console |
| 8 | Monitor and delete unused EBS volumes | Storage | EC2 Console / Trusted Advisor |
| 9 | Identify and clean up orphaned EBS snapshots | Storage | Data Lifecycle Manager |
| 10 | Remove idle load balancers; use CloudFront | Right-Size | Trusted Advisor / CloudFront |
| 11 | Implement cost allocation tagging | Monitoring | AWS Tag Editor / Cost Allocation Tags |
| 12 | Automate anomaly detection | Monitoring | AWS Cost Anomaly Detection |

### AWS Native Tools Reference

| Tool | Purpose |
|---|---|
| AWS Cost Explorer | Visualize, filter, and forecast AWS spend by service, account, or tag |
| AWS Budgets | Set custom spend/usage budgets with threshold alerts |
| AWS Pricing Calculator | Model and compare pricing for new or changed workloads |
| AWS Compute Optimizer | ML-driven right-sizing recommendations for EC2, EBS, Lambda |
| AWS Trusted Advisor | Automated checks for cost optimization, security, performance |
| Amazon Data Lifecycle Manager | Automate EBS snapshot creation and retention policies |
| AWS Cost Anomaly Detection | ML-powered anomaly detection with root-cause analysis |

### Review Process

Follow this structured flow when the user asks for a cost review:

1. **Scope** — Ask which AWS accounts, regions, and services to review
2. **Data Gathering** — Pull Cost Explorer data for the last 30–90 days; identify top-5 cost drivers
3. **Pillar Walk-Through** — Evaluate each of the five pillars in order
4. **Checklist** — Present the twelve best practices as a scored checklist (done / not done / partial)
5. **Quick Wins** — Highlight the three highest-impact, lowest-effort actions
6. **Roadmap** — Propose a 30/60/90-day optimization plan with estimated savings

## Examples

### Example 1 — Quick Cost Audit

User: "Review my AWS spending and find quick wins."

Response approach:
1. Request access to Cost Explorer data or ask the user to share a CSV export
2. Identify the top-5 services by spend
3. Run through Pillars 1 (Right-Size) and 4 (Storage) for immediate savings
4. Check for unattached EBS volumes and idle load balancers via Trusted Advisor
5. Present three quick wins with estimated monthly savings

### Example 2 — EC2 Right-Sizing

User: "How can I reduce my EC2 bill?"

Response approach:
1. List all running EC2 instances by family and size
2. Pull CloudWatch CPU/memory utilization for the past 14 days
3. Cross-reference with Compute Optimizer recommendations
4. Recommend specific instance type changes (e.g., m5.xlarge → m5.large)
5. Suggest Spot Instances for stateless workloads
6. Evaluate Savings Plans for steady-state baseline

### Example 3 — Storage Cleanup

User: "Clean up unused EBS volumes and snapshots."

Response approach:
1. List all EBS volumes in `available` state across regions
2. Identify orphaned snapshots not linked to active AMIs
3. Calculate monthly cost of unused storage
4. Recommend deletion after confirming no data-loss risk
5. Set up Data Lifecycle Manager for automated snapshot retention

### Example 4 — FinOps Governance Setup

User: "Help me set up FinOps practices for my AWS accounts."

Response approach:
1. Define a cost allocation tagging strategy with mandatory tags
2. Configure AWS Budgets with tiered alerts (50%, 80%, 100%)
3. Enable Cost Anomaly Detection for each linked account
4. Set up a monthly Cost Explorer saved report
5. Propose a 30/60/90-day FinOps maturity roadmap

## Best Practices

### General Principles
- Always quantify estimated savings in dollars per month before recommending changes
- Never delete resources without confirming backup and data-loss risk first
- Prioritize quick wins (high impact, low effort) before long-term structural changes
- Use tags consistently — untagged resources are invisible to cost governance
- Review costs monthly; set calendar reminders for quarterly deep reviews

### Safety Guidelines
- Do not terminate or modify production instances without explicit user approval
- Always create snapshots before deleting EBS volumes
- Verify Reserved Instance utilization before recommending purchases
- Test Spot Instance interruption handling before migrating production workloads
- Confirm data sovereignty and compliance requirements before suggesting region changes

### Cost Optimization Anti-Patterns to Avoid
- Buying Reserved Instances before right-sizing (locks in waste)
- Ignoring data transfer costs between regions and AZs
- Over-provisioning "just in case" without auto-scaling
- Using gp2 EBS volumes when gp3 offers better price-performance
- Running dev/test environments 24/7 without stop/start schedules
- Neglecting S3 lifecycle policies for infrequently accessed data

## Constraints and Warnings

- **Read-only guidance**: This skill provides recommendations only — it cannot directly access or modify your AWS account
- **Cost estimates are approximations**: Actual savings depend on workload specifics
- **RI/Savings Plans are commitments**: 1-3 year terms, generally non-refundable — evaluate utilization first
- **Spot Instances risk**: 2-minute interruption warning — use for stateless/fault-tolerant workloads only
- **Irreversible actions**: Never delete resources without confirming backups exist
- **Compliance implications**: Region changes may affect data sovereignty and latency
- **Some features require support**: Cost Explorer and Compute Optimizer need Business/Enterprise Support
