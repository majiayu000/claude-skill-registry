---
name: aws-cost-optimization
description: Provides structured AWS cost optimization guidance using five pillars (right-sizing, elasticity, pricing models, storage optimization, monitoring) and twelve actionable best practices with executable AWS CLI examples. Use when optimizing AWS costs, reviewing AWS spending, finding unused AWS resources, implementing FinOps practices, reducing EC2/EBS/S3 bills, configuring AWS Budgets, or performing AWS Well-Architected cost reviews.
allowed-tools: Read, Write, Bash
---

# AWS Cost Optimization

## Overview

Guide a structured AWS cost review covering right-sizing, elasticity, pricing models, storage optimization, and continuous monitoring. References AWS native tools (Cost Explorer, Budgets, Compute Optimizer, Trusted Advisor, Cost Anomaly Detection) and delivers twelve prioritized best practices organized under five optimization pillars. All examples use the AWS CLI.

## When to Use

- Optimizing AWS costs or reviewing AWS spending
- Finding unused or under-utilized AWS resources
- Implementing FinOps practices for cloud cost governance
- Reducing EC2, EBS, S3, or load balancer bills
- Choosing between On-Demand, Spot, Reserved Instances, and Savings Plans
- Configuring AWS Budgets, Cost Explorer, or Cost Anomaly Detection
- Performing an AWS Well-Architected Framework cost pillar review
- Cleaning up orphaned EBS snapshots or unused volumes
- Automating start/stop schedules for non-production workloads

Trigger: "Optimize my AWS costs", "Review AWS spending", "Find unused AWS resources", "Help me with FinOps", "Reduce my EC2 bill", "Clean up unused EBS volumes", "Set up AWS Budgets"

## Instructions

### Five Optimization Pillars

Work through each pillar in order during a cost review.

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

1. Analyze steady-state baseline using Cost Explorer RI Coverage and Savings Plans Coverage reports
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

### Review Process

Follow this structured flow when the user asks for a cost review:

1. **Scope** — Ask which AWS accounts, regions, and services to review
2. **Data Gathering** — Pull Cost Explorer data for the last 30–90 days; identify top-5 cost drivers
3. **Pillar Walk-Through** — Evaluate each of the five pillars in order
4. **Checklist** — Present the twelve best practices as a scored checklist (done / not done / partial)
5. **Quick Wins** — Highlight the three highest-impact, lowest-effort actions
6. **Roadmap** — Propose a 30/60/90-day optimization plan with estimated savings

## Examples

### Example 1 — List Unattached EBS Volumes

User: "Find unused EBS volumes in my account."

CLI commands to include in the response:

```bash
# List all EBS volumes in available (unattached) state
aws ec2 describe-volumes \
  --filters Name=status,Values=available \
  --query 'Volumes[*].{VolumeId:VolumeId,Size:Size,Type:VolumeType,Zone:AvailabilityZone,CreateTime:CreateTime}' \
  --output table

# Get monthly cost estimate for unused volumes (approx $0.08/GB/mo for gp3)
aws ec2 describe-volumes \
  --filters Name=status,Values=available \
  --query 'length(Volumes[*].[VolumeId,Size])' \
  --output text

# List orphaned snapshots (not linked to any AMI)
aws ec2 describe-snapshots \
  --owner-ids self \
  --query 'Snapshots[?!contains(Description, `ami-`)].[SnapshotId,VolumeId,StartTime,Size]'
```

### Example 2 — EC2 Right-Sizing with Compute Optimizer

User: "How can I reduce my EC2 bill?"

CLI commands to include in the response:

```bash
# Get Compute Optimizer right-sizing recommendations for EC2
aws compute-optimizer get-ec2-instance-recommendations \
  --query 'instanceRecommendations[*].{InstanceArn:instanceArn,CurrentInstanceType:currentInstanceType,RecommendedInstanceType:recommendations[0].instanceType,MonthlySaving:recommendations[0].estimatedMonthlySavings.value}' \
  --output table

# Pull average CPU utilization for an instance over 14 days
aws cloudwatch get-metric-statistics \
  --namespace AWS/EC2 \
  --metric-name CPUUtilization \
  --dimensions Name=InstanceId,Value=i-1234567890abcdef0 \
  --start-time 2026-03-09T00:00:00Z \
  --end-time 2026-03-23T00:00:00Z \
  --period 86400 \
  --statistics Average \
  --output table

# List all running instances by type for baseline analysis
aws ec2 describe-instances \
  --filters Name=instance-state-name,Values=running \
  --query 'Reservations[].Instances[].[InstanceId,InstanceType,Tags[?Key==`Name`].Value|[0],State.Name]' \
  --output table
```

### Example 3 — Cost Explorer and Budgets Setup

User: "Set up AWS Budgets and monitor my spend."

CLI commands to include in the response:

```bash
# Create a monthly cost budget with alert thresholds at 50%, 80%, 100%
aws budgets create-budget \
  --account-id 123456789012 \
  --budget '{
    "BudgetName": "Monthly-Cost-Budget",
    "BudgetLimit": {"Amount": "5000", "Unit": "USD"},
    "TimeUnit": "MONTHLY",
    "BudgetType": "COST"
  }' \
  --notifications-with-subscribers '[{"Notification": {"ComparisonOperator": "GREATER_THAN", "NotificationType": "ACTUAL", "Threshold": 80},"Subscribers": [{"Address": "email@example.com","SubscriptionType": "EMAIL"}]}]'

# Get top-5 cost drivers from Cost Explorer (last 30 days)
aws ce get-cost-and-usage \
  --time-period Start=2026-02-23,End=2026-03-23 \
  --granularity MONTHLY \
  --metrics "BlendedCost" "UnblendedCost" \
  --group-by Type=DIMENSION,Key=SERVICE \
  --query 'ResultsByTime[0].Groups[*].{Service:Keys[0],BlendedCost:Metrics.BlendedCost.Amount}' \
  --output table

# Enable Cost Anomaly Detection alert
aws ce create-anomaly-monitor \
  --monitor-name "Daily-Cost-Anomaly" \
  --monitor-arn "arn:aws:ce::123456789012:anomaly-monitor/cost-explorer"
```

### Example 4 — S3 Lifecycle and Storage Tiering

User: "Optimize my S3 storage costs."

CLI commands to include in the response:

```bash
# List S3 buckets with size and storage class distribution
aws s3api list-buckets --query 'Buckets[*].Name'
aws s3api get-bucket-storage-type-aggregation --bucket YOUR-BUCKET-NAME

# Apply S3 Intelligent-Tiering lifecycle rule for objects older than 90 days
aws s3api put-bucket-lifecycle-configuration \
  --bucket YOUR-BUCKET-NAME \
  --lifecycle-configuration '{
    "Rules": [{
      "ID": "MoveToIntelligentTiering",
      "Status": "Enabled",
      "Filter": {},
      "Transitions": [
        {"Days": 30, "StorageClass": "INTELLIGENT_TIERING"},
        {"Days": 90, "StorageClass": "GLACIER_IR"}
      ]
    }]
  }'
```

### Example 5 — Spot Instances and Savings Plans

User: "Should I use Spot Instances or Savings Plans?"

CLI commands to include in the response:

```bash
# Check current RI and Savings Plans coverage
aws ce get-savings-plans-coverage \
  --time-period Start=2026-01-01,End=2026-03-23 \
  --granularity MONTHLY

# List available Spot price history for an instance type
aws ec2 describe-spot-price-history \
  --instance-types t3.medium \
  --product-description "Linux/UNIX" \
  --availability-zone us-east-1a \
  --query 'SpotPriceHistory[*].{Price:SpotPrice,Date:Timestamp}' \
  --output table

# Estimate savings with Savings Plans vs On-Demand
aws savingsplans describe-savings-plans-rates \
  --savings-plan-arn arn:aws:savingsplans::123456789012:savings-plan/SP-EXAMPLE
```

## Best Practices

### General Principles
- Quantify estimated savings in dollars per month before recommending changes
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

### Anti-Patterns to Avoid
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
- **Support tier**: Cost Explorer and Compute Optimizer need Business/Enterprise Support

## AWS Tools Quick Reference

| Tool | Use Case |
|---|---|
| Cost Explorer | Visualize and filter AWS spend by service, account, or tag |
| AWS Budgets | Set custom spend budgets with threshold alerts |
| AWS Pricing Calculator | Model pricing for new or changed workloads |
| Compute Optimizer | ML-driven right-sizing recommendations for EC2, EBS, Lambda |
| Trusted Advisor | Automated cost optimization, security, performance checks |
| Data Lifecycle Manager | Automate EBS snapshot creation and retention |
| Cost Anomaly Detection | ML-powered spend anomaly alerts with root-cause analysis |

## Twelve Best Practices Checklist

| # | Practice | Pillar |
|---|---|---|
| 1 | Choose appropriate AWS region (cost, latency, data sovereignty) | Right-Size |
| 2 | Schedule start/stop for non-production instances | Elasticity |
| 3 | Identify under-utilized EC2 instances | Right-Size |
| 4 | Reduce EC2 costs with Spot Instances | Pricing Model |
| 5 | Optimize Auto Scaling Group policies | Elasticity |
| 6 | Use or resell under-utilized Reserved Instances | Pricing Model |
| 7 | Leverage Compute Savings Plans | Pricing Model |
| 8 | Monitor and delete unused EBS volumes | Storage |
| 9 | Identify and clean up orphaned EBS snapshots | Storage |
| 10 | Remove idle load balancers; use CloudFront | Right-Size |
| 11 | Implement cost allocation tagging | Monitoring |
| 12 | Automate anomaly detection | Monitoring |
