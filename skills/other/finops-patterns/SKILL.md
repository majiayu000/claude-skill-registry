---
name: finops-patterns
description: Provides FinOps practices for cloud cost optimization, budget management, and resource rightsizing. Use when analyzing cloud spend, optimizing costs, or when user mentions 'finops', 'cloud cost', 'rightsizing', 'budget', 'cost allocation', 'reserved instance', 'spot instance', 'showback', 'chargeback'.
type: skill
category: patterns
status: stable
origin: tibsfox
modified: false
first_seen: 2026-02-07
first_path: examples/finops-patterns/SKILL.md
superseded_by: null
---
# FinOps Patterns

Best practices for managing cloud financial operations -- visibility, optimization, and governance of cloud spend at scale.

## Cloud Cost Anatomy

Understanding where cloud money goes is the first step to controlling it.

```
Total Cloud Spend
  |
  +-- Compute (60-70%)
  |     +-- VMs / Instances
  |     +-- Containers (EKS, GKE, ECS)
  |     +-- Serverless (Lambda, Cloud Functions)
  |     +-- GPU / ML Training
  |
  +-- Storage (15-20%)
  |     +-- Block (EBS, Persistent Disks)
  |     +-- Object (S3, GCS, Blob)
  |     +-- Database (RDS, Cloud SQL, DynamoDB)
  |
  +-- Network (10-15%)
  |     +-- Data Transfer (egress is expensive)
  |     +-- Load Balancers
  |     +-- CDN
  |     +-- VPN / Direct Connect
  |
  +-- Other (5-10%)
        +-- Monitoring / Logging
        +-- DNS / Certificates
        +-- Support Plans
        +-- Marketplace
```

| Cost Driver | Typical Waste | Quick Win |
|------------|--------------|-----------|
| Idle instances | 20-30% of compute | Schedule dev/test shutdown nights + weekends |
| Over-provisioned instances | 40-60% of instances | Rightsize based on actual CPU/memory usage |
| Unattached storage volumes | 5-10% of storage | Automated cleanup of orphaned EBS/disks |
| Unused Elastic IPs | Small but cumulative | Release unattached IPs |
| Old snapshots | 10-20% of storage | Lifecycle policy with retention limits |
| Cross-region data transfer | 5-15% of network | Co-locate services in same region |

## FinOps Maturity Model

Organizations progress through three phases of FinOps practice maturity.

| Dimension | Crawl | Walk | Run |
|-----------|-------|------|-----|
| Visibility | Monthly bill review | Tagged cost allocation by team | Real-time cost dashboards per service |
| Allocation | Single account, no tagging | Cost centers with basic tags | Full showback/chargeback by product line |
| Optimization | Ad-hoc rightsizing | Quarterly review with recommendations | Automated rightsizing and scaling policies |
| Forecasting | None | Spreadsheet-based projections | ML-based anomaly detection and forecasts |
| Governance | No budgets | Account-level budgets | Per-team budgets with automated enforcement |
| Commitment | On-demand only | Some Reserved Instances | Savings Plans + Spot + RI portfolio managed |
| Culture | Central IT pays the bill | Engineering aware of costs | Engineers own cost as a feature metric |
| Tooling | AWS Console only | Cost Explorer + basic reports | FinOps platform (Kubecost, CloudHealth, etc.) |

## Cost Allocation Tagging Strategy

Tags are the foundation of cost visibility. Without consistent tagging, cost allocation is impossible.

### Required Tag Schema

```yaml
# tagging-policy.yaml -- Enforced via AWS Organizations SCP or Terraform
required_tags:
  - key: "team"
    description: "Owning team (must match teams registry)"
    example: "platform-engineering"
    validation: "^[a-z]+-[a-z]+$"

  - key: "service"
    description: "Service or application name"
    example: "payment-api"
    validation: "^[a-z]+-[a-z]+(-[a-z]+)?$"

  - key: "environment"
    description: "Deployment environment"
    allowed_values: ["production", "staging", "development", "sandbox"]

  - key: "cost-center"
    description: "Finance cost center code"
    example: "CC-4200"
    validation: "^CC-\\d{4}$"

  - key: "data-classification"
    description: "Data sensitivity level"
    allowed_values: ["public", "internal", "confidential", "restricted"]

optional_tags:
  - key: "project"
    description: "Project or initiative code"

  - key: "managed-by"
    description: "IaC tool managing this resource"
    allowed_values: ["terraform", "pulumi", "cloudformation", "manual"]

  - key: "expiry"
    description: "Auto-delete date for temporary resources"
    format: "YYYY-MM-DD"
```

### Tag Enforcement via AWS SCP

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "RequireTagsOnResourceCreation",
      "Effect": "Deny",
      "Action": [
        "ec2:RunInstances",
        "rds:CreateDBInstance",
        "s3:CreateBucket",
        "eks:CreateCluster",
        "lambda:CreateFunction"
      ],
      "Resource": "*",
      "Condition": {
        "Null": {
          "aws:RequestTag/team": "true",
          "aws:RequestTag/service": "true",
          "aws:RequestTag/environment": "true",
          "aws:RequestTag/cost-center": "true"
        }
      }
    }
  ]
}
```

## Rightsizing Analysis

### Instance Rightsizing Script

```python
#!/usr/bin/env python3
"""rightsizing.py -- Analyze EC2 instances for rightsizing opportunities."""

import boto3
from datetime import datetime, timedelta, timezone
from dataclasses import dataclass

UTILIZATION_THRESHOLD = 40  # percent -- instances below this are candidates
LOOKBACK_DAYS = 14
MIN_DATAPOINTS = 100  # Require sufficient data before recommending


@dataclass
class RightsizeRecommendation:
    instance_id: str
    instance_type: str
    avg_cpu: float
    max_cpu: float
    avg_memory: float  # Requires CloudWatch agent
    recommended_type: str
    monthly_savings: float
    confidence: str  # "high" | "medium" | "low"


# Instance family downsizing map (simplified)
DOWNSIZE_MAP = {
    "m5.2xlarge": "m5.xlarge",
    "m5.xlarge": "m5.large",
    "m5.large": "m5.medium",    # Careful: medium may be too small
    "c5.2xlarge": "c5.xlarge",
    "c5.xlarge": "c5.large",
    "r5.2xlarge": "r5.xlarge",
    "r5.xlarge": "r5.large",
    "t3.xlarge": "t3.large",
    "t3.large": "t3.medium",
}

# Approximate on-demand hourly pricing (us-east-1)
HOURLY_PRICING = {
    "m5.2xlarge": 0.384, "m5.xlarge": 0.192, "m5.large": 0.096,
    "c5.2xlarge": 0.340, "c5.xlarge": 0.170, "c5.large": 0.085,
    "r5.2xlarge": 0.504, "r5.xlarge": 0.252, "r5.large": 0.126,
    "t3.xlarge": 0.1664, "t3.large": 0.0832, "t3.medium": 0.0416,
}


def get_cpu_utilization(cw_client, instance_id: str) -> tuple[float, float]:
    """Return (avg_cpu, max_cpu) over the lookback period."""
    end = datetime.now(timezone.utc)
    start = end - timedelta(days=LOOKBACK_DAYS)

    response = cw_client.get_metric_statistics(
        Namespace="AWS/EC2",
        MetricName="CPUUtilization",
        Dimensions=[{"Name": "InstanceId", "Value": instance_id}],
        StartTime=start,
        EndTime=end,
        Period=3600,  # 1-hour intervals
        Statistics=["Average", "Maximum"],
    )

    datapoints = response.get("Datapoints", [])
    if len(datapoints) < MIN_DATAPOINTS:
        return -1.0, -1.0  # Insufficient data

    avg = sum(dp["Average"] for dp in datapoints) / len(datapoints)
    peak = max(dp["Maximum"] for dp in datapoints)
    return avg, peak


def analyze_fleet() -> list[RightsizeRecommendation]:
    """Analyze all running EC2 instances for rightsizing."""
    ec2 = boto3.client("ec2")
    cw = boto3.client("cloudwatch")
    recommendations = []

    # Get all running instances
    paginator = ec2.get_paginator("describe_instances")
    for page in paginator.paginate(
        Filters=[{"Name": "instance-state-name", "Values": ["running"]}]
    ):
        for reservation in page["Reservations"]:
            for instance in reservation["Instances"]:
                instance_id = instance["InstanceId"]
                instance_type = instance["InstanceType"]

                # Skip instances not in our downsize map
                if instance_type not in DOWNSIZE_MAP:
                    continue

                avg_cpu, max_cpu = get_cpu_utilization(cw, instance_id)
                if avg_cpu < 0:
                    continue  # Insufficient data

                if avg_cpu < UTILIZATION_THRESHOLD:
                    recommended = DOWNSIZE_MAP[instance_type]
                    current_cost = HOURLY_PRICING.get(instance_type, 0)
                    new_cost = HOURLY_PRICING.get(recommended, 0)
                    monthly_savings = (current_cost - new_cost) * 730

                    confidence = "high" if max_cpu < 60 else "medium"

                    recommendations.append(RightsizeRecommendation(
                        instance_id=instance_id,
                        instance_type=instance_type,
                        avg_cpu=round(avg_cpu, 1),
                        max_cpu=round(max_cpu, 1),
                        avg_memory=-1.0,
                        recommended_type=recommended,
                        monthly_savings=round(monthly_savings, 2),
                        confidence=confidence,
                    ))

    # Sort by savings potential (highest first)
    recommendations.sort(key=lambda r: r.monthly_savings, reverse=True)
    return recommendations


if __name__ == "__main__":
    recs = analyze_fleet()
    total_savings = sum(r.monthly_savings for r in recs)

    print(f"\n{'='*80}")
    print(f"RIGHTSIZING RECOMMENDATIONS ({len(recs)} instances)")
    print(f"Potential monthly savings: ${total_savings:,.2f}")
    print(f"{'='*80}\n")

    for r in recs:
        print(f"  {r.instance_id}: {r.instance_type} -> {r.recommended_type}")
        print(f"    CPU avg={r.avg_cpu}% max={r.max_cpu}%")
        print(f"    Savings: ${r.monthly_savings}/mo  Confidence: {r.confidence}")
        print()
```

## Budget Alert Configuration

### AWS CloudWatch Budget Alarm

```yaml
# cloudformation/budget-alerts.yaml
AWSTemplateFormatVersion: "2010-09-09"
Description: FinOps budget alerts with multi-threshold notifications

Parameters:
  TeamName:
    Type: String
    Description: Team name for cost allocation
  MonthlyBudget:
    Type: Number
    Description: Monthly budget in USD
  AlertEmail:
    Type: String
    Description: Email for budget notifications
  SlackWebhookArn:
    Type: String
    Description: ARN of Lambda that posts to Slack

Resources:
  # SNS topic for budget alerts
  BudgetAlertTopic:
    Type: AWS::SNS::Topic
    Properties:
      TopicName: !Sub "${TeamName}-budget-alerts"
      Subscription:
        - Protocol: email
          Endpoint: !Ref AlertEmail
        - Protocol: lambda
          Endpoint: !Ref SlackWebhookArn

  # Monthly budget with progressive thresholds
  TeamBudget:
    Type: AWS::Budgets::Budget
    Properties:
      Budget:
        BudgetName: !Sub "${TeamName}-monthly-budget"
        BudgetLimit:
          Amount: !Ref MonthlyBudget
          Unit: USD
        TimeUnit: MONTHLY
        BudgetType: COST
        CostFilters:
          TagKeyValue:
            - !Sub "user:team$${TeamName}"

      NotificationsWithSubscribers:
        # 50% threshold -- informational
        - Notification:
            NotificationType: ACTUAL
            ComparisonOperator: GREATER_THAN
            Threshold: 50
            ThresholdType: PERCENTAGE
          Subscribers:
            - SubscriptionType: SNS
              Address: !Ref BudgetAlertTopic

        # 80% threshold -- warning
        - Notification:
            NotificationType: ACTUAL
            ComparisonOperator: GREATER_THAN
            Threshold: 80
            ThresholdType: PERCENTAGE
          Subscribers:
            - SubscriptionType: SNS
              Address: !Ref BudgetAlertTopic

        # 100% threshold -- critical
        - Notification:
            NotificationType: ACTUAL
            ComparisonOperator: GREATER_THAN
            Threshold: 100
            ThresholdType: PERCENTAGE
          Subscribers:
            - SubscriptionType: SNS
              Address: !Ref BudgetAlertTopic

        # Forecasted to exceed -- early warning
        - Notification:
            NotificationType: FORECASTED
            ComparisonOperator: GREATER_THAN
            Threshold: 100
            ThresholdType: PERCENTAGE
          Subscribers:
            - SubscriptionType: SNS
              Address: !Ref BudgetAlertTopic

  # CloudWatch alarm for sudden spend spikes (daily granularity)
  DailySpendAlarm:
    Type: AWS::CloudWatch::Alarm
    Properties:
      AlarmName: !Sub "${TeamName}-daily-spend-spike"
      AlarmDescription: "Daily spend exceeds expected daily average by 2x"
      Namespace: AWS/Billing
      MetricName: EstimatedCharges
      Dimensions:
        - Name: Currency
          Value: USD
      Statistic: Maximum
      Period: 86400  # 24 hours
      EvaluationPeriods: 1
      # Threshold = (monthly budget / 30 days) * 2 (spike factor)
      Threshold: !Sub "${AWS::NoValue}"
      ComparisonOperator: GreaterThanThreshold
      AlarmActions:
        - !Ref BudgetAlertTopic
```

## Spot Instance Handling

### Spot Instance Strategy with Fallback

```yaml
# kubernetes/spot-node-pool.yaml -- EKS managed node group with spot
apiVersion: eksctl.io/v1alpha5
kind: ClusterConfig

metadata:
  name: production-cluster
  region: us-east-1

managedNodeGroups:
  # On-demand baseline for critical workloads
  - name: baseline-on-demand
    instanceType: m5.xlarge
    desiredCapacity: 3
    minSize: 3
    maxSize: 6
    labels:
      node-type: on-demand
      workload-class: critical
    taints:
      - key: workload-class
        value: critical
        effect: NoSchedule

  # Spot instances for fault-tolerant workloads
  - name: spot-workers
    instanceTypes:
      # Diversify across instance types to reduce interruption risk
      - m5.xlarge
      - m5a.xlarge
      - m5d.xlarge
      - m4.xlarge
      - m5n.xlarge
    spot: true
    desiredCapacity: 6
    minSize: 2
    maxSize: 20
    labels:
      node-type: spot
      workload-class: batch
    tags:
      k8s.io/cluster-autoscaler/enabled: "true"

---
# Pod disruption budget to handle spot interruptions
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: batch-processor-pdb
spec:
  minAvailable: 2
  selector:
    matchLabels:
      app: batch-processor

---
# Deployment tolerating spot nodes
apiVersion: apps/v1
kind: Deployment
metadata:
  name: batch-processor
spec:
  replicas: 6
  selector:
    matchLabels:
      app: batch-processor
  template:
    metadata:
      labels:
        app: batch-processor
    spec:
      # Prefer spot, but allow on-demand as fallback
      affinity:
        nodeAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
            - weight: 90
              preference:
                matchExpressions:
                  - key: node-type
                    operator: In
                    values: ["spot"]
            - weight: 10
              preference:
                matchExpressions:
                  - key: node-type
                    operator: In
                    values: ["on-demand"]
      # Handle spot interruption gracefully
      terminationGracePeriodSeconds: 120
      containers:
        - name: batch-processor
          image: registry.example.com/batch-processor:latest
          lifecycle:
            preStop:
              exec:
                command:
                  - /bin/sh
                  - -c
                  - "echo 'Draining...' && /app/drain.sh && sleep 30"
```

## Cost Anomaly Detection

### Automated Anomaly Detection Script

```python
#!/usr/bin/env python3
"""cost-anomaly.py -- Detect unusual spending patterns using AWS Cost Explorer."""

import boto3
import json
from datetime import datetime, timedelta
from dataclasses import dataclass

ANOMALY_THRESHOLD = 1.5    # 50% above average triggers alert
LOOKBACK_DAYS = 30         # Historical baseline period
MINIMUM_DAILY_COST = 10.0  # Ignore services with trivial spend


@dataclass
class CostAnomaly:
    service: str
    date: str
    actual_cost: float
    expected_cost: float
    deviation_pct: float
    severity: str  # "warning" | "critical"


def get_daily_costs(ce_client, days: int) -> dict[str, list[float]]:
    """Fetch daily costs by service for the past N days."""
    end = datetime.utcnow().date()
    start = end - timedelta(days=days)

    response = ce_client.get_cost_and_usage(
        TimePeriod={
            "Start": start.isoformat(),
            "End": end.isoformat(),
        },
        Granularity="DAILY",
        Metrics=["UnblendedCost"],
        GroupBy=[
            {"Type": "DIMENSION", "Key": "SERVICE"},
        ],
    )

    # Organize costs by service
    service_costs: dict[str, list[float]] = {}
    for result in response["ResultsByTime"]:
        for group in result["Groups"]:
            service = group["Keys"][0]
            cost = float(group["Metrics"]["UnblendedCost"]["Amount"])
            if service not in service_costs:
                service_costs[service] = []
            service_costs[service].append(cost)

    return service_costs


def detect_anomalies(service_costs: dict[str, list[float]]) -> list[CostAnomaly]:
    """Detect cost anomalies using rolling average comparison."""
    anomalies = []

    for service, costs in service_costs.items():
        if len(costs) < 7:
            continue  # Not enough data

        # Use all but last day as baseline
        baseline = costs[:-1]
        latest = costs[-1]

        avg_cost = sum(baseline) / len(baseline)

        # Skip low-spend services
        if avg_cost < MINIMUM_DAILY_COST:
            continue

        if avg_cost == 0:
            continue

        deviation = latest / avg_cost

        if deviation >= ANOMALY_THRESHOLD:
            deviation_pct = (deviation - 1) * 100
            severity = "critical" if deviation >= 2.0 else "warning"

            anomalies.append(CostAnomaly(
                service=service,
                date=datetime.utcnow().date().isoformat(),
                actual_cost=round(latest, 2),
                expected_cost=round(avg_cost, 2),
                deviation_pct=round(deviation_pct, 1),
                severity=severity,
            ))

    # Sort by deviation severity
    anomalies.sort(key=lambda a: a.deviation_pct, reverse=True)
    return anomalies


def send_alert(anomalies: list[CostAnomaly]) -> None:
    """Send anomaly alerts via SNS."""
    if not anomalies:
        return

    sns = boto3.client("sns")
    topic_arn = "arn:aws:sns:us-east-1:123456789:finops-alerts"

    total_excess = sum(a.actual_cost - a.expected_cost for a in anomalies)

    message_lines = [
        f"COST ANOMALY ALERT -- {len(anomalies)} services affected",
        f"Estimated excess spend today: ${total_excess:,.2f}",
        "",
    ]

    for a in anomalies:
        message_lines.append(
            f"  [{a.severity.upper()}] {a.service}: "
            f"${a.actual_cost} (expected ${a.expected_cost}, "
            f"+{a.deviation_pct}%)"
        )

    sns.publish(
        TopicArn=topic_arn,
        Subject=f"FinOps Alert: {len(anomalies)} cost anomalies detected",
        Message="\n".join(message_lines),
    )


if __name__ == "__main__":
    ce = boto3.client("ce")
    costs = get_daily_costs(ce, LOOKBACK_DAYS)
    anomalies = detect_anomalies(costs)

    if anomalies:
        print(f"\nDETECTED {len(anomalies)} ANOMALIES:\n")
        for a in anomalies:
            print(f"  [{a.severity}] {a.service}")
            print(f"    Today: ${a.actual_cost}  Avg: ${a.expected_cost}  "
                  f"Deviation: +{a.deviation_pct}%")
            print()
        send_alert(anomalies)
    else:
        print("No cost anomalies detected.")
```

## Showback vs Chargeback Models

| Aspect | Showback | Chargeback |
|--------|----------|------------|
| Definition | Report costs to teams for visibility | Bill costs back to team budgets |
| Financial impact | Informational only | Deducted from team budget |
| Accountability | Soft (awareness) | Hard (budget ownership) |
| Implementation complexity | Low | High (needs finance integration) |
| Cultural resistance | Low | Medium-High |
| Best for | FinOps Crawl/Walk maturity | FinOps Run maturity |
| Shared costs | Shown but not allocated | Must be allocated (often contentious) |

### Shared Cost Allocation Methods

| Method | How it Works | Best For |
|--------|-------------|----------|
| Even split | Divide equally among teams | Simple, low contention |
| Proportional (usage) | Allocate by % of usage metrics | Fair but needs good metrics |
| Proportional (headcount) | Allocate by team size | Easy, rough approximation |
| Fixed ratio | Pre-agreed percentages | Stable, predictable |
| Tag-based | Allocate by tagged resource ownership | Most accurate, needs tagging discipline |

## FinOps Team Structure and RACI

| Activity | FinOps Lead | Engineering | Finance | Management |
|----------|:-----------:|:-----------:|:-------:|:----------:|
| Set budget targets | C | I | A | R |
| Tag resources | I | R | - | A |
| Review cost reports | R | C | C | I |
| Approve Reserved Instances | C | C | A | R |
| Implement rightsizing | C | R | I | A |
| Anomaly investigation | A | R | I | C |
| Negotiate cloud contracts | R | C | A | I |
| Build cost dashboards | R | C | I | I |
| Enforce tagging policy | A | R | - | I |
| Quarterly cost review | R | C | C | A |

**R** = Responsible, **A** = Accountable, **C** = Consulted, **I** = Informed

## Commitment Strategy: Reserved vs Spot vs On-Demand

| Purchase Model | Discount | Commitment | Flexibility | Best For |
|---------------|---------|-----------|-------------|----------|
| On-Demand | 0% | None | Full | Unpredictable workloads, spikes |
| Savings Plans (Compute) | 30-40% | 1 or 3 year | High (any instance type) | Steady-state baseline |
| Savings Plans (Instance) | 40-50% | 1 or 3 year | Medium (one family) | Known instance families |
| Reserved Instances | 40-60% | 1 or 3 year | Low (specific type) | Databases, fixed workloads |
| Spot Instances | 60-90% | None | None (can be reclaimed) | Batch, CI/CD, fault-tolerant |

### Portfolio Strategy

```
Total compute spend = 100%

Committed (Savings Plans / RI): 60-70%
  -- Covers steady-state baseline that runs 24/7
  -- Buy based on minimum observed usage over 3 months

On-Demand: 10-20%
  -- Covers variable load above baseline
  -- Handles unpredictable spikes

Spot: 10-20%
  -- Batch processing, CI/CD runners, dev/test
  -- Workloads that tolerate interruption
```

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| No tagging strategy | Cannot allocate costs to teams or services | Enforce required tags via SCP; deny untagged resource creation |
| Single payer, no visibility | Teams have no cost awareness | Implement showback reports; per-team dashboards |
| Over-buying Reserved Instances | Locked into unused capacity | Start with Compute Savings Plans; buy RI only for stable workloads |
| Ignoring data transfer costs | Network egress surprises on the bill | Architect for same-region; use VPC endpoints; monitor egress |
| No budget alerts | Overspend discovered at month-end | Set progressive alerts at 50%, 80%, 100% of budget |
| Dev/test runs 24/7 | Paying for resources nobody uses nights/weekends | Schedule auto-stop; 65% savings for 10hr/day schedule |
| Orphaned resources | EBS volumes, IPs, snapshots accumulate after instances deleted | Automated weekly cleanup of unattached resources |
| Rightsizing by gut feel | Wrong instance types selected without data | Use CloudWatch metrics; require 2+ weeks data before resizing |
| No commitment strategy | Paying full on-demand price for steady workloads | Analyze usage baseline; buy Savings Plans for committed floor |
| Cost optimization as one-time project | Savings erode as teams spin up new resources | Continuous FinOps practice; monthly reviews; automated policies |
| Shared account with no allocation | Impossible to attribute costs | Separate accounts per team/environment; use AWS Organizations |
| Ignoring storage lifecycle | Hot-tier pricing for cold data | S3 lifecycle policies; archive to Glacier after 90 days |
| No unit economics | Cannot correlate cost to business value | Track cost-per-transaction, cost-per-user, cost-per-API-call |

## FinOps Implementation Checklist

### Phase 1: Crawl (Visibility)

- [ ] Enable AWS Cost Explorer / GCP Billing Export / Azure Cost Management
- [ ] Define and enforce mandatory tagging schema (team, service, environment, cost-center)
- [ ] Create monthly cost reports broken down by service and team
- [ ] Identify top 10 cost drivers and their owners
- [ ] Set up basic budget alerts at account level (80% and 100% thresholds)
- [ ] Inventory all running resources and identify obvious waste (idle, unattached)
- [ ] Establish FinOps lead role (can be part-time initially)

### Phase 2: Walk (Optimization)

- [ ] Implement showback reports delivered to engineering leads weekly
- [ ] Run rightsizing analysis on all compute instances (2-week data minimum)
- [ ] Schedule dev/test environment shutdown outside business hours
- [ ] Purchase Compute Savings Plans for baseline steady-state usage
- [ ] Implement automated cleanup of orphaned resources (EBS, snapshots, IPs)
- [ ] Set per-team budgets with progressive alert thresholds
- [ ] Establish quarterly FinOps review cadence with engineering and finance
- [ ] Deploy cost anomaly detection with automated alerts
- [ ] Introduce Spot Instances for batch processing and CI/CD workloads

### Phase 3: Run (Governance)

- [ ] Implement chargeback model with finance system integration
- [ ] Track unit economics (cost per transaction, per user, per API call)
- [ ] Deploy ML-based cost forecasting and anomaly detection
- [ ] Automate rightsizing recommendations with approval workflows
- [ ] Establish commitment portfolio management (RI + Savings Plans + Spot)
- [ ] Integrate cost checks into CI/CD (Infracost, cost impact on PRs)
- [ ] Implement real-time cost dashboards accessible to all engineers
- [ ] Run FinOps training for all engineering teams annually
- [ ] Negotiate Enterprise Discount Programs with cloud providers
- [ ] Publish monthly FinOps scorecard to leadership
