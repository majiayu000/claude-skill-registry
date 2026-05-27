---
name: Cloud Cost Models
description: Comprehensive guide to cloud pricing models, cost structures, and optimization strategies across major providers.
---

# Cloud Cost Models and Pricing

## Overview

Cloud cost management (FinOps) is the practice of bringing financial accountability to the variable spend model of cloud computing. Understanding the underlying cost models of major providers is the foundation of building cost-efficient, scalable systems.

**Core Principle**: "Optimize for value, not just cost. Move from 'how much did we spend' to 'how much value did we get for our spend'."

---

## 1. Cloud Pricing Fundamentals

Cloud providers typically use a consumption-based model with three primary levers:

1.  **Compute**: Charged by time (seconds/hours) and capacity (CPU/RAM).
2.  **Storage**: Charged by volume (GB/month), redundancy level, and performance (IOPS).
3.  **Data Transfer**: Usually free for "Inbound", charged for "Outbound" (Egress) and sometimes between internal zones/regions.

### The Compute Continuum

| Model | Pricing Metric | Best For | Typical Provider Product |
| :--- | :--- | :--- | :--- |
| **Virtual Machines** | Unit/Hour or Unit/Second | Consistent, legacy, or long-running apps | EC2, GCE, Azure VM |
| **Containers** | Resource Requests (CPU/RAM) | Microservices, dynamic scaling | Fargate, Cloud Run, ACI |
| **Serverless** | Requests + Execution Duration | Event-driven, intermittent traffic | Lambda, Cloud Functions |

---

## 2. AWS Pricing Model

AWS uses a complex but granular pricing structure.

### EC2 (Elastic Compute Cloud)
*   **On-Demand**: Lowest commitment, highest cost. Pay by the second.
*   **Reserved Instances (RI)**: Up to 72% discount for 1-3 year commitment. Best for steady-state workloads.
*   **Savings Plans**: Flexible 1-3 year commitment ($/hour) across EC2, Fargate, and Lambda.
*   **Spot Instances**: Up to 90% discount. AWS can reclaim with 2-minute notice. Best for stateless, fault-tolerant apps (CI/CD, batch processing).

### S3 (Simple Storage Service)
*   **S3 Standard**: Active data ($0.023/GB).
*   **S3 Intelligent-Tiering**: Auto-moves data based on access patterns ($0.023/GB + monitoring fee).
*   **S3 Standard-IA**: Infrequent access, fast retrieval ($0.0125/GB).
*   **S3 Glacier Instant Retrieval**: Archival data, millisecond retrieval ($0.004/GB).
*   **S3 Glacier Deep Archive**: Long-term storage (7-10 years), 12-hour retrieval ($0.00099/GB).

### Lambda
*   **Requests**: $0.20 per 1M requests.
*   **Duration**: Calculated in GB-seconds (Memory allocated × Duration).
*   **Provisioned Concurrency**: Extra fee to keep functions "warm" to avoid cold starts.

### RDS (Relational Database Service)
*   **Instance**: Based on type (db.m5.large, etc.).
*   **Storage**: Multi-AZ doubles instance and storage costs.
*   **I/O**: Charged per million I/O requests for some engine types.

### Data Transfer Costs
*   **Ingress (Internet to AWS)**: Free.
*   **Egress (AWS to Internet)**: ~$0.09/GB (first 10TB).
*   **Inter-AZ**: $0.01/GB (both directions).
*   **Inter-Region**: $0.02/GB.

---

## 3. GCP Pricing Model

GCP emphasizes simplicity and "Sustained Use Discounts".

### Compute Engine
*   **Standard**: Pay-as-you-go.
*   **Sustained Use Discounts (SUD)**: Automatic discounts (up to 30%) for running instances for a large portion of the month.
*   **Committed Use Discounts (CUD)**: 1 or 3-year commitment for specific vCPU/RAM amounts.
*   **Preemptible VMs**: Equivalent to AWS Spot, but fixed 24-hour max runtime and fixed ~80% discount.

### Cloud Storage
*   **Standard**: Hot data.
*   **Nearline**: Data accessed < once/month.
*   **Coldline**: Data accessed < once/quarter.
*   **Archive**: Data accessed < once/year.

### BigQuery
*   **Analysis (On-Demand)**: $5 per TB scanned.
*   **Analysis (Capacity/Flat-rate)**: Reserved slots (vCPUs) for predictable high-volume billing.
*   **Storage**: $0.02/GB (Active), $0.01/GB (Long-term > 90 days).

---

## 4. Azure Pricing Model

### Virtual Machines
*   **Pay-as-you-go**: Standard rates.
*   **Reserved Virtual Machine Instances**: 1 or 3-year commitment (up to 72% savings).
*   **Azure Hybrid Benefit**: Use existing on-premises Windows Server/SQL Server licenses on Azure to save up to 40%.

### Blob Storage
*   **Hot**: Frequently accessed.
*   **Cool**: Stored for 30+ days.
*   **Archive**: Stored for 180+ days.

### Functions
*   **Consumption Plan**: Billed based on executions and execution time.
*   **Premium Plan**: Avoids cold starts, allows VNet integration, billed per vCPU and Memory.

---

## 5. Hidden Costs (The "Silent Killers")

Many teams blow their budgets on items that aren't the primary compute instances:

1.  **Data Egress**: Moving data out of the cloud or between regions is expensive.
2.  **NAT Gateways**: AWS charges ~$0.045 per GB processed through a NAT Gateway *plus* the hourly fee for the gateway itself.
3.  **Load Balancers**: LCU (Load Balancer Capacity Units) can scale costs significantly with high connection counts or high throughput.
4.  **Logging & Monitoring**: Storing multi-terabyte internal logs in CloudWatch or Datadog can often exceed the cost of the application itself.
5.  **Unused Elastic IPs**: AWS charges for IPs that are allocated but *not* attached to a running instance.
6.  **Snapshots & Backups**: Retaining daily snapshots of 10TB volumes indefinitely.

---

## 6. Cost Optimization Strategies

### The Optimization Pyramid
1.  **Right-Sizing**: Ensure instance sizes match actual utilization (CPU < 40% means you should downsize).
2.  **Modernization**: Move from VMs to Fargate/Lambda or Graviton (ARM) processors. Graviton typically offers 40% better price-performance.
3.  **Deletions**: Clean up "unattached" resources (EBS volumes, EIPs, Load Balancers).
4.  **Purchasing Options**: Apply RIs and Savings Plans *after* right-sizing.

### Storage Lifecycle Policy Example (S3)
```json
{
    "Rules": [
        {
            "ID": "MoveToIAAndGlacier",
            "Prefix": "logs/",
            "Status": "Enabled",
            "Transitions": [
                { "Days": 30, "StorageClass": "STANDARD_IA" },
                { "Days": 90, "StorageClass": "GLACIER" }
            ],
            "Expiration": { "Days": 365 }
        }
    ]
}
```

---

## 7. Cost Allocation and Tagging

If you can't measure it, you can't manage it.

### Required Tags Hierarchy
*   **Project**: `Project: ProjectPhoenix`
*   **Environment**: `Env: Prod`, `Env: Dev`
*   **Owner**: `Owner: TeamAlpha`
*   **Cost Center**: `CostCenter: CC-9901`

### enforcement with Terraform
```hcl
resource "aws_instance" "example" {
  ami           = "ami-12345678"
  instance_type = "t3.medium"

  tags = {
    Name        = "PhoenixAPI"
    Environment = "Prod"
    Owner       = "TeamAlpha"
    CostCenter  = "12345"
  }
}
```

---

## 8. FinOps Principles (Crawl, Walk, Run)

The **FinOps Foundation** defines the lifecycle:

1.  **Inform**: Visibility into spend. Allocation, tagging, and reporting.
2.  **Optimize**: Real-time decision making. Right-sizing and identifying waste.
3.  **Operate**: Aligning teams to business goals. Budgets, unit economics, and governance.

| Phase | Activities |
| :--- | :--- |
| **Crawl** | Spreadsheet reports, basic tags, monthly reviews. |
| **Walk** | Multi-cloud dashboards, automated alerts, RI purchases. |
| **Run** | Automated right-sizing, unit-cost tracking, AI-driven anomaly detection. |

---

## 9. Tools and Integration

*   **Native**: AWS Cost Explorer, GCP Billing, Azure Cost Management.
*   **Infrastructure as Code**: **Infracost** (shows cost changes in Pull Requests).
*   **Kubernetes**: **Kubecost** (allocates cluster costs to namespaces/pods).
*   **Anomaly detection**: AWS Cost Anomaly Detection (Machine Learning based).

---

## 10. TCO (Total Cost of Ownership) Calculation

Avoid the "Sticker Price" trap. TCO includes:
*   **Direct Costs**: Server, Storage, Network.
*   **Indirect Costs**: Employee time for patching, DBA time for backups, security compliance.
*   **Risk Cost**: Cost of downtime if self-hosting vs. provider SLA.

### TCO Calculation Table (Example: Self-Hosted vs. Managed DB)

| Aspect | Self-Hosted (EC2) | Managed (RDS) |
| :--- | :--- | :--- |
| **Instance Cost** | $100/mo | $140/mo |
| **Storage/Backup**| $20/mo | $30/mo |
| **Engineer Hours**| 10 hrs ($1000) | 1 hr ($100) |
| **Total Cost** | **$1120/mo** | **$270/mo** |
| **Winner** | | ✅ **RDS** |

---

## 11. Real Cost Optimization Case Studies

### Case Study 1: The "Zombie" Resource Cleanup
*   **Scenario**: A company was spending $50k/month on AWS.
*   **Discovery**: $8k was spent on EBS volumes not attached to any VM.
*   **Action**: Ran a script to find and delete volumes unattached > 14 days.
*   **Outcome**: Immediate $8,000/month (16%) savings.

### Case Study 2: Graviton Migration
*   **Scenario**: E-commerce API running on m5.large (Intel).
*   **Action**: Switched to m6g.large (AWS Graviton2).
*   **Outcome**: 20% lower instance cost and 15% better throughput.

---

## 12. Optimization Checklist

* [ ] **Tagging**: Are 100% of resources tagged with `CostCenter`?
* [ ] **Right-Sizing**: Do any instances have < 10% average CPU over 7 days?
* [ ] **Orphans**: Are there unattached EBS volumes or ELBs?
* [ ] **Storage**: Are S3 lifecycle policies active for `logs/` buckets?
* [ ] **Compute**: Are we using Spot instances for CI/CD runners?
* [ ] **Networking**: Are we transferring data across regions unnecessarily?
* [ ] **Commitment**: Do we have 1-year Savings Plans for our "baseline" load?

## Related Skills
* `42-cost-engineering/infra-sizing`
* `42-cost-engineering/budget-guardrails`
* `42-cost-engineering/cost-observability`
