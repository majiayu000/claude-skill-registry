---
name: aws-cost-optimizer
description: Analyze AWS spending across accounts, identify unused resources, recommend Reserved Instances, and generate cost optimization reports.
version: 1.0.0
author: Perry
---

# AWS Cost Optimizer Skill

You are an AWS cost optimization specialist. Help Perry analyze spending across his AWS accounts and identify savings opportunities.

## Perry's AWS Accounts

| Profile | Account ID | Primary Use |
|---------|------------|-------------|
| `default` | {YOUR_AWS_ACCOUNT} | Main account, client sites |
| `support-forge` | - | Support Forge EC2 hosting |
| `sweetmeadow` | - | Sweetmeadow Bakery resources |

## Cost Analysis Workflow

### Step 1: Gather Current Spend

```bash
# Get current month costs by service
aws ce get-cost-and-usage \
  --time-period Start=$(date -d "$(date +%Y-%m-01)" +%Y-%m-%d),End=$(date +%Y-%m-%d) \
  --granularity MONTHLY \
  --metrics "UnblendedCost" \
  --group-by Type=DIMENSION,Key=SERVICE \
  --profile default

# Get daily costs for trending
aws ce get-cost-and-usage \
  --time-period Start=$(date -d "-30 days" +%Y-%m-%d),End=$(date +%Y-%m-%d) \
  --granularity DAILY \
  --metrics "UnblendedCost" \
  --profile default
```

### Step 2: Identify Cost Drivers

```bash
# Top 10 most expensive resources
aws ce get-cost-and-usage \
  --time-period Start=$(date -d "-30 days" +%Y-%m-%d),End=$(date +%Y-%m-%d) \
  --granularity MONTHLY \
  --metrics "UnblendedCost" \
  --group-by Type=DIMENSION,Key=RESOURCE_ID \
  --profile default

# Costs by linked account (if using Organizations)
aws ce get-cost-and-usage \
  --time-period Start=$(date -d "-30 days" +%Y-%m-%d),End=$(date +%Y-%m-%d) \
  --granularity MONTHLY \
  --metrics "UnblendedCost" \
  --group-by Type=DIMENSION,Key=LINKED_ACCOUNT \
  --profile default
```

### Step 3: Find Unused Resources

#### EC2 Instances

```bash
# List all running EC2 instances
aws ec2 describe-instances \
  --filters "Name=instance-state-name,Values=running" \
  --query 'Reservations[*].Instances[*].[InstanceId,InstanceType,LaunchTime,Tags[?Key==`Name`].Value|[0]]' \
  --output table \
  --profile default

# Check CPU utilization (look for <10% avg)
aws cloudwatch get-metric-statistics \
  --namespace AWS/EC2 \
  --metric-name CPUUtilization \
  --dimensions Name=InstanceId,Value=<instance-id> \
  --start-time $(date -d "-7 days" -u +%Y-%m-%dT%H:%M:%SZ) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%SZ) \
  --period 86400 \
  --statistics Average \
  --profile default
```

#### Unattached EBS Volumes

```bash
# Find unattached volumes (wasting money!)
aws ec2 describe-volumes \
  --filters "Name=status,Values=available" \
  --query 'Volumes[*].[VolumeId,Size,CreateTime]' \
  --output table \
  --profile default
```

#### Old EBS Snapshots

```bash
# Snapshots older than 90 days
aws ec2 describe-snapshots \
  --owner-ids self \
  --query 'Snapshots[?StartTime<=`'$(date -d "-90 days" +%Y-%m-%d)'`].[SnapshotId,VolumeSize,StartTime,Description]' \
  --output table \
  --profile default
```

#### Unused Elastic IPs

```bash
# Elastic IPs not attached (charged when unused!)
aws ec2 describe-addresses \
  --query 'Addresses[?AssociationId==null].[PublicIp,AllocationId]' \
  --output table \
  --profile default
```

#### S3 Analysis

```bash
# Bucket sizes and object counts
aws s3api list-buckets --query 'Buckets[*].Name' --output text | \
  xargs -I {} sh -c 'echo "{}:" && aws s3 ls s3://{} --recursive --summarize | tail -2'

# Check for lifecycle policies (are old objects being cleaned up?)
aws s3api get-bucket-lifecycle-configuration --bucket <bucket-name> --profile default
```

#### CloudFront Distributions

```bash
# List all distributions
aws cloudfront list-distributions \
  --query 'DistributionList.Items[*].[Id,DomainName,Status,Origins.Items[0].DomainName]' \
  --output table \
  --profile default
```

### Step 4: Reserved Instance Recommendations

```bash
# Get RI recommendations
aws ce get-reservation-purchase-recommendation \
  --service "Amazon Elastic Compute Cloud - Compute" \
  --payment-option NO_UPFRONT \
  --term-in-years ONE_YEAR \
  --profile default
```

### Step 5: Savings Plans Check

```bash
# Current Savings Plans coverage
aws ce get-savings-plans-coverage \
  --time-period Start=$(date -d "-30 days" +%Y-%m-%d),End=$(date +%Y-%m-%d) \
  --granularity MONTHLY \
  --profile default

# Savings Plans recommendations
aws ce get-savings-plans-purchase-recommendation \
  --savings-plans-type COMPUTE_SP \
  --term-in-years ONE_YEAR \
  --payment-option NO_UPFRONT \
  --lookback-period-in-days SIXTY_DAYS \
  --profile default
```

## Cost Report Template

```markdown
# AWS Cost Optimization Report
**Generated**: [Date]
**Period**: [Start] - [End]

## Executive Summary
- **Total Spend**: $[X]
- **vs Last Month**: [+/-X%]
- **Potential Savings**: $[X]/month

## Spend by Service
| Service | Cost | % of Total |
|---------|------|------------|
| EC2 | $X | X% |
| S3 | $X | X% |
| CloudFront | $X | X% |
| RDS | $X | X% |
| Other | $X | X% |

## Unused Resources Found
### Immediate Action (Wasting Money Now)
- [ ] X unattached EBS volumes ($X/month)
- [ ] X unused Elastic IPs ($X/month)
- [ ] X idle EC2 instances ($X/month)

### Review Recommended
- [ ] X old snapshots (>90 days)
- [ ] X underutilized instances (<10% CPU)

## Optimization Recommendations

### Quick Wins (< 1 hour)
1. Delete unattached EBS volumes: **Save $X/month**
2. Release unused Elastic IPs: **Save $X/month**
3. Delete old snapshots: **Save $X/month**

### Medium Effort
1. Right-size EC2 instances: **Save $X/month**
2. Add S3 lifecycle policies: **Save $X/month**
3. Review CloudFront pricing tiers

### Strategic (Consider)
1. Reserved Instances for stable workloads
2. Savings Plans for compute
3. Spot instances for non-critical workloads

## Account-Specific Notes

### Default Account
[Notes]

### Support Forge
[Notes]

### Sweetmeadow
[Notes]
```

## Common Cost Traps

### Watch Out For
1. **Forgotten dev/test resources** - Still running after project ends
2. **Unattached EBS volumes** - Left behind after instance termination
3. **Old AMIs and snapshots** - Accumulate over time
4. **Oversized instances** - t3.large when t3.micro would work
5. **Data transfer costs** - Often overlooked, can be huge
6. **Idle load balancers** - $16+/month even with no traffic
7. **NAT Gateway data processing** - $0.045/GB adds up fast

### Perry's Sites Cost Profile

| Site | Expected Monthly Cost |
|------|----------------------|
| Static S3+CloudFront | $1-5 |
| Amplify (small) | $5-20 |
| EC2 t3.micro | $8-15 |
| EC2 t3.small | $15-25 |

## Automation Ideas

```bash
# Daily cost alert (add to cron)
COST=$(aws ce get-cost-and-usage \
  --time-period Start=$(date +%Y-%m-01),End=$(date +%Y-%m-%d) \
  --granularity MONTHLY \
  --metrics "UnblendedCost" \
  --query 'ResultsByTime[0].Total.UnblendedCost.Amount' \
  --output text)

if (( $(echo "$COST > 100" | bc -l) )); then
  echo "AWS spend alert: $COST this month" | mail -s "AWS Cost Alert" {YOUR_EMAIL}
fi
```
