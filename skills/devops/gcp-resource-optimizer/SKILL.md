---
name: gcp-resource-optimizer
description: Optimize Google Cloud Platform resource allocation and manage cloud credits efficiently. Use when planning GCP deployments, analyzing cloud spend, maximizing value from expiring credits, right-sizing instances, or designing cost-effective architectures. Triggers on GCP cost optimization, credit management, resource allocation planning, or cloud budget concerns.
license: MIT
---

# GCP Resource Optimizer

Maximize value from GCP resources and credits through strategic allocation.

## Credit Burn Strategy

### Credit Expiration Planning

When managing expiring credits:

1. **Audit current usage**: `gcloud billing accounts describe ACCOUNT_ID`
2. **Calculate burn rate**: Total credits ÷ Days remaining = Required daily spend
3. **Identify high-value uses**: What creates lasting value vs. ephemeral compute?

### High-Value Credit Uses

**Lasting value (prioritize):**
- Training ML models (artifacts persist)
- Building container images
- Generating datasets
- Running batch processing on accumulated work

**Ephemeral (use strategically):**
- Compute instances (gone when shut down)
- Development environments
- Testing infrastructure

## Cost Optimization Patterns

### Compute Engine

**Right-sizing instances:**
```bash
# Check recommendations
gcloud recommender recommendations list \
  --project=PROJECT_ID \
  --location=ZONE \
  --recommender=google.compute.instance.MachineTypeRecommender
```

**Cost-effective machine types:**
| Need | Recommended | Why |
|------|-------------|-----|
| General workload | e2-medium | Best price/performance |
| Memory-intensive | n2-highmem | Better RAM ratio |
| CPU burst | e2-micro/small | Burstable, cheap |
| ML training | n1 + GPU | Required for accelerators |
| Spot-tolerant | Spot VMs | 60-91% discount |

**Preemptible/Spot VMs:**
- 60-91% cheaper than standard
- Can be terminated with 30s notice
- Good for: batch jobs, fault-tolerant workloads, development
- Bad for: production, stateful services

### Cloud Run

**Optimizing Cloud Run:**
```yaml
# Minimize cold starts and costs
spec:
  template:
    spec:
      containerConcurrency: 80  # Maximize requests per instance
      timeoutSeconds: 300
    metadata:
      annotations:
        autoscaling.knative.dev/minScale: '0'  # Scale to zero
        autoscaling.knative.dev/maxScale: '10'  # Cap costs
        run.googleapis.com/cpu-throttling: 'true'  # CPU only when processing
```

### Cloud Storage

**Storage class optimization:**
| Class | Use Case | Cost/GB/mo |
|-------|----------|------------|
| Standard | Frequent access | ~$0.020 |
| Nearline | Monthly access | ~$0.010 |
| Coldline | Quarterly access | ~$0.004 |
| Archive | Yearly access | ~$0.0012 |

**Lifecycle rules:**
```json
{
  "lifecycle": {
    "rule": [
      {
        "action": {"type": "SetStorageClass", "storageClass": "NEARLINE"},
        "condition": {"age": 30}
      },
      {
        "action": {"type": "SetStorageClass", "storageClass": "COLDLINE"},
        "condition": {"age": 90}
      },
      {
        "action": {"type": "Delete"},
        "condition": {"age": 365}
      }
    ]
  }
}
```

### BigQuery

**Cost control:**
```sql
-- Set maximum bytes billed
#standardSQL
-- @maximumBytesBilled 10000000000
SELECT * FROM dataset.table
```

**Partitioning for cost reduction:**
```sql
CREATE TABLE dataset.table
PARTITION BY DATE(timestamp_column)
CLUSTER BY user_id
AS SELECT * FROM source_table
```

## Budget Alerts

**Set up budget alerts:**
```bash
gcloud billing budgets create \
  --billing-account=BILLING_ACCOUNT_ID \
  --display-name="Monthly Budget" \
  --budget-amount=100USD \
  --threshold-rule=percent=50 \
  --threshold-rule=percent=90 \
  --threshold-rule=percent=100
```

## Resource Cleanup

### Find Unused Resources

```bash
# Unused disks
gcloud compute disks list --filter="NOT users:*"

# Unused IPs
gcloud compute addresses list --filter="status=RESERVED"

# Idle VMs (by CPU)
gcloud monitoring time-series list \
  --filter='metric.type="compute.googleapis.com/instance/cpu/utilization"' \
  --interval="start=2024-01-01T00:00:00Z"
```

### Cleanup Script

```bash
#!/bin/bash
# cleanup_unused.sh - Review before running!

# List (don't delete) unused resources
echo "=== Unused Disks ==="
gcloud compute disks list --filter="NOT users:*" --format="table(name,zone,sizeGb)"

echo "=== Reserved IPs ==="
gcloud compute addresses list --filter="status=RESERVED" --format="table(name,region,address)"

echo "=== Snapshots older than 30 days ==="
gcloud compute snapshots list --filter="creationTimestamp<$(date -d '30 days ago' -Iseconds)" --format="table(name,diskSizeGb,creationTimestamp)"
```

## Architecture Patterns for Cost

### Serverless-First
```
Request → Cloud Run → Firestore → Done
         (scales to zero)  (pay per op)

vs.

Request → GKE → Cloud SQL → Done
         (always running)  (always running)
```

### Batch Processing
```
Pub/Sub → Cloud Functions → BigQuery (batch load)
                           (cheaper than streaming)
```

### Development vs Production

**Dev environment:**
- Spot/preemptible VMs
- Smaller machine types
- Scale-to-zero services
- Shared resources

**Prod environment:**
- Committed use discounts (1-3 year)
- Right-sized dedicated instances
- Redundancy only where needed

## Monitoring Setup

```bash
# Enable billing export to BigQuery
gcloud beta billing accounts describe ACCOUNT_ID

# Query costs
#standardSQL
SELECT
  service.description,
  SUM(cost) as total_cost
FROM `project.dataset.gcp_billing_export_v1_*`
WHERE _PARTITIONTIME >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
GROUP BY 1
ORDER BY 2 DESC
```

## References

- `references/pricing-cheatsheet.md` - Quick pricing reference
- `references/cost-queries.md` - BigQuery cost analysis queries
