---
name: cost-optimization
description: Cloud spend optimization strategies including GPU cost management, right-sizing, credits programs, and compute procurement decisions.
---

# Cloud Cost Optimization

## When to Use This Skill

Use when evaluating cloud spend, choosing compute procurement strategies, setting up cost monitoring, or managing GPU costs for ML workloads. Relevant for startups burning through credits or approaching profitability.

## Compute Procurement Strategy

| Workload Type | On-Demand | Reserved/Savings Plan | Spot/Preemptible | Strategy |
|---|---|---|---|---|
| Production API servers | Baseline | 1yr for base load | No | Reserve 60-70% base, on-demand for peaks |
| Dev/staging environments | Off nights/weekends | No | Yes with fallback | Spot + scheduled shutdown |
| ML training (checkpointable) | No | No | Yes | Spot with checkpointing, 60-90% savings |
| ML inference (latency-sensitive) | Burst overflow | 1yr for steady state | No | Reserve base, on-demand burst |
| Batch processing / ETL | No | No | Yes | Spot with retry logic |
| CI/CD runners | No | No | Yes | Spot with on-demand fallback |
| GPU fine-tuning | No | No | Yes | Spot A100/H100, checkpoint every 30min |
| Database (RDS/CloudSQL) | No | 1yr reserved | No | Always reserve; 30-40% savings |

### Startup Credits Programs

| Provider | Program | Amount | Duration | Gotcha |
|---|---|---|---|---|
| AWS | Activate | $10K-$100K | 1-2 years | Must apply through accelerator/VC |
| GCP | for Startups | $100K-$200K | 1-2 years | Requires <$100K revenue |
| Azure | for Startups | $5K-$150K | 1-2 years | Linked to Founders Hub tier |
| CoreWeave | Startup program | Varies | Varies | GPU-focused, good for ML |
| Lambda Labs | Direct | Pay-as-go | N/A | Often cheapest H100 spot |

## AWS Cost Explorer Queries

### Monthly Cost Breakdown by Service

```bash
aws ce get-cost-and-usage \
  --time-period Start=$(date -d '-30 days' +%Y-%m-%d),End=$(date +%Y-%m-%d) \
  --granularity MONTHLY \
  --metrics BlendedCost \
  --group-by Type=DIMENSION,Key=SERVICE \
  | jq '.ResultsByTime[0].Groups
        | sort_by(.Metrics.BlendedCost.Amount | tonumber)
        | reverse | .[:10]'
```

### Find Idle Resources

```bash
# Unattached EBS volumes (pure waste)
aws ec2 describe-volumes \
  --filters Name=status,Values=available \
  --query 'Volumes[*].{ID:VolumeId,Size:Size,Type:VolumeType}' \
  --output table

# Idle Elastic IPs (charged when unattached)
aws ec2 describe-addresses \
  --query 'Addresses[?AssociationId==null].{IP:PublicIp,AllocId:AllocationId}' \
  --output table
```

## Spot Instance Fallback Pattern

### Terraform with Mixed Instance Policy

```hcl
resource "aws_autoscaling_group" "workers" {
  desired_capacity = 4
  max_size         = 10
  min_size         = 2

  mixed_instances_policy {
    instances_distribution {
      on_demand_base_capacity                  = 1  # 1 guaranteed instance
      on_demand_percentage_above_base_capacity = 0  # rest are spot
      spot_allocation_strategy                 = "capacity-optimized"
      spot_max_price                           = "" # on-demand price cap
    }
    launch_template {
      launch_template_specification {
        launch_template_id = aws_launch_template.worker.id
        version            = "$Latest"
      }
      override { instance_type = "m6i.xlarge"; weighted_capacity = "1" }
      override { instance_type = "m6a.xlarge"; weighted_capacity = "1" }
      override { instance_type = "m5.xlarge";  weighted_capacity = "1" }
      override { instance_type = "m5a.xlarge"; weighted_capacity = "1" }
    }
  }
}
```

### Spot Interruption Handler (Python)

```python
import requests, signal, sys, threading, time

METADATA_URL = "http://169.254.169.254/latest/meta-data/spot/instance-action"

def check_spot_interruption() -> dict | None:
    try:
        resp = requests.get(METADATA_URL, timeout=1)
        if resp.status_code == 200:
            return resp.json()
    except requests.exceptions.RequestException:
        pass
    return None

def graceful_shutdown(checkpoint_fn):
    def handler(signum, frame):
        checkpoint_fn()
        sys.exit(0)
    signal.signal(signal.SIGTERM, handler)

    def poll():
        while True:
            if check_spot_interruption():
                checkpoint_fn()
                sys.exit(0)
            time.sleep(5)
    threading.Thread(target=poll, daemon=True).start()
```

## Auto-Scaling Policies

### Target Tracking with Scale-Down Protection

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: api-server
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: api-server
  minReplicas: 2
  maxReplicas: 20
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
        - type: Percent
          value: 25
          periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
        - type: Percent
          value: 100
          periodSeconds: 60
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 65
```

### Scheduled Scaling for Dev Environments

```bash
# Scale down at 20:00 weekdays
aws autoscaling update-auto-scaling-group \
  --auto-scaling-group-name dev-workers \
  --min-size 0 --max-size 0 --desired-capacity 0

# Scale up at 08:00 weekdays
aws autoscaling update-auto-scaling-group \
  --auto-scaling-group-name dev-workers \
  --min-size 1 --max-size 4 --desired-capacity 2
```

## Budget Alerts

### Terraform Budget with Threshold Alerts

```hcl
resource "aws_budgets_budget" "monthly" {
  name         = "monthly-total"
  budget_type  = "COST"
  limit_amount = "5000"
  limit_unit   = "USD"
  time_unit    = "MONTHLY"

  dynamic "notification" {
    for_each = [50, 80, 100, 120]
    content {
      comparison_operator       = "GREATER_THAN"
      threshold                 = notification.value
      threshold_type            = "PERCENTAGE"
      notification_type         = notification.value <= 100 ? "FORECASTED" : "ACTUAL"
      subscriber_email_addresses = ["eng-leads@company.com"]
      subscriber_sns_topic_arns  = [aws_sns_topic.budget_alerts.arn]
    }
  }
}

resource "aws_budgets_budget" "gpu" {
  name         = "gpu-spend"
  budget_type  = "COST"
  limit_amount = "2000"
  limit_unit   = "USD"
  time_unit    = "MONTHLY"

  cost_filter {
    name   = "Service"
    values = ["Amazon Elastic Compute Cloud - Compute"]
  }

  notification {
    comparison_operator       = "GREATER_THAN"
    threshold                 = 80
    threshold_type            = "PERCENTAGE"
    notification_type         = "ACTUAL"
    subscriber_email_addresses = ["ml-team@company.com"]
  }
}
```

## Gotchas and Anti-Patterns

### Hidden Costs: Data Egress
- **Problem**: Cross-region and internet egress charges silently accumulate. $0.09/GB adds up with large datasets or high-traffic APIs.
- **Fix**: Keep compute and storage co-located. Use CloudFront/CDN for public content. Monitor DataTransfer-Out-Bytes. Watch NAT Gateway costs ($0.045/GB).
### Hidden Costs: API Calls and Storage
- **Problem**: S3 LIST requests cost 5x GET. DynamoDB capacity units surprise teams. CloudWatch log ingestion at $0.50/GB.
- **Fix**: Audit API call patterns. Set S3 lifecycle policies. Use DynamoDB on-demand for unpredictable workloads.
### GPU Idle Waste
- **Problem**: GPU instances running 24/7 for jobs that run hours/day. Idle p4d.24xlarge costs ~$800/day.
- **Fix**: Use spot with checkpointing. Implement job queues that acquire/release GPUs per job. Alert on GPU utilization < 10% over 1 hour.
### Over-Provisioned Dev Environments
- **Problem**: Dev mirrors production sizing. 8 devs on m5.2xlarge 24/7 = $4,300/month mostly idle.
- **Fix**: Use t3.medium for dev. Schedule auto-shutdown outside business hours (saves 65%). Use cloud workstations on demand.
