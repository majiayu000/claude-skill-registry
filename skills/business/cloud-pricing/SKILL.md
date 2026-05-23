---
name: cloud-pricing
description: Expert knowledge of cloud provider pricing models for AWS, Azure, GCP covering compute, storage, database, networking, and serverless services. Includes 2025 pricing data, regional differences, free tiers, pricing calculators, and cost comparison across providers. Activates for cloud pricing, how much does it cost, price comparison, AWS vs Azure vs GCP pricing, pricing calculator, estimate costs, regional pricing, free tier, what's cheaper.
---

# Cloud Pricing Expert

Expert knowledge of cloud provider pricing models across AWS, Azure, and GCP with current 2025 pricing data.

## Compute Pricing (2025)

### AWS EC2 (us-east-1)
```yaml
t3.micro:   $0.0104/hour  (2 vCPU, 1GB)
t3.small:   $0.0208/hour  (2 vCPU, 2GB)
t3.medium:  $0.0416/hour  (2 vCPU, 4GB)
t3.large:   $0.0832/hour  (2 vCPU, 8GB)
m5.large:   $0.096/hour   (2 vCPU, 8GB)
c5.large:   $0.085/hour   (2 vCPU, 4GB) - compute-optimized
r5.large:   $0.126/hour   (2 vCPU, 16GB) - memory-optimized

Spot pricing: 50-90% discount (variable)
Reserved (1yr): 35-40% discount
Reserved (3yr): 60-65% discount
Savings Plans: 30-70% discount (flexible)
```

### Azure VMs (East US)
```yaml
B1s:     $0.0104/hour  (1 vCPU, 1GB) - burstable
B2s:     $0.0416/hour  (2 vCPU, 4GB)
D2s v5:  $0.096/hour   (2 vCPU, 8GB)
F2s v2:  $0.085/hour   (2 vCPU, 4GB) - compute-optimized
E2s v5:  $0.126/hour   (2 vCPU, 16GB) - memory-optimized

Spot: 50-90% discount
Reserved (1yr): 40% discount  
Reserved (3yr): 62% discount
```

### GCP Compute Engine (us-central1)
```yaml
e2-micro:   $0.0084/hour  (0.25-2 vCPU, 1GB)
e2-small:   $0.0168/hour  (0.5-2 vCPU, 2GB)
e2-medium:  $0.0335/hour  (1-2 vCPU, 4GB)
n2-standard-2: $0.0971/hour (2 vCPU, 8GB)
c2-standard-4: $0.2088/hour (4 vCPU, 16GB) - compute

Preemptible: 60-91% discount
Committed (1yr): 37% discount
Committed (3yr): 55% discount
```

## Serverless Pricing

### AWS Lambda
```yaml
Requests: $0.20 per 1M requests
Compute:
  - $0.0000166667 per GB-second
  - 128MB, 1s = $0.0000021
  - 1024MB, 1s = $0.0000166667

Free tier: 1M requests, 400K GB-seconds/month

Example: 10M requests, 512MB, 200ms avg
  = 10M * $0.20/1M + 10M * 0.5GB * 0.2s * $0.0000166667
  = $2 + $16.67 = $18.67/month
```

### Azure Functions
```yaml
Consumption Plan:
  - $0.20 per 1M executions
  - $0.000016 per GB-second
  
Premium Plan (always-on):
  - EP1: $0.2065/hour (1 vCPU, 3.5GB)
  - EP2: $0.413/hour (2 vCPU, 7GB)

Free tier: 1M requests, 400K GB-seconds
```

### GCP Cloud Functions
```yaml
Invocations: $0.40 per 1M invocations
Compute: $0.0000025 per GB-second
Networking: $0.12/GB egress

Free tier: 2M invocations, 400K GB-seconds
```

## Storage Pricing

### AWS S3 (us-east-1)
```yaml
Standard:           $0.023/GB/month
Standard-IA:        $0.0125/GB  (54% cheaper, min 128KB, 30 days)
Glacier Instant:    $0.004/GB   (83% cheaper, min 128KB, 90 days)
Glacier Flexible:   $0.0036/GB  (84% cheaper, 90 days, 1-5min retrieval)
Deep Archive:       $0.00099/GB (96% cheaper, 180 days, 12hr retrieval)

Requests:
  - PUT/COPY/POST: $0.005 per 1K requests
  - GET/SELECT: $0.0004 per 1K requests

Data Transfer: $0.09/GB out to internet (first 10TB)
```

### Azure Blob Storage
```yaml
Hot:     $0.0184/GB  (frequent access)
Cool:    $0.01/GB    (min 30 days)
Archive: $0.00099/GB (min 180 days, 15hr retrieval)

Transactions:
  - Write: $0.05 per 10K
  - Read: $0.004 per 10K
```

### GCP Cloud Storage
```yaml
Standard:  $0.020/GB
Nearline:  $0.010/GB (min 30 days)
Coldline:  $0.004/GB (min 90 days)
Archive:   $0.0012/GB (min 365 days)

Operations: $0.05 per 10K Class A (write)
            $0.004 per 10K Class B (read)
```

## Database Pricing

### AWS RDS PostgreSQL (db.t3.medium)
```yaml
On-demand:      $0.068/hour ($49.64/month)
Reserved 1yr:   $0.043/hour (37% savings)
Reserved 3yr:   $0.029/hour (57% savings)

Storage (gp3): $0.115/GB/month
Backup:        $0.095/GB/month

Aurora Serverless: $0.12 per ACU-hour (auto-scaling)
```

### Azure SQL Database
```yaml
General Purpose (2 vCore):
  - Provisioned: $0.5556/hour ($406/month)
  - Serverless: $0.75-1.50/vCore-hour (auto-pause)
  
Storage: $0.115/GB/month
```

### GCP Cloud SQL PostgreSQL
```yaml
db-n1-standard-1 (1 vCPU, 3.75GB):
  - On-demand: $0.0413/hour ($30.15/month)
  - Committed 1yr: 37% discount
  
Storage (SSD): $0.17/GB/month
```

### DynamoDB / Cosmos DB / Firestore
```yaml
DynamoDB (us-east-1):
  - On-demand: $1.25 per 1M read, $1.25 per 1M write
  - Provisioned: $0.00065/hour per RCU, $0.00065/hour per WCU
  - Storage: $0.25/GB

Cosmos DB:
  - Provisioned: $0.008/hour per 100 RU/s
  - Serverless: $0.25 per 1M RU
  
Firestore:
  - Reads: $0.06 per 100K
  - Writes: $0.18 per 100K
  - Storage: $0.18/GB
```

## Networking Pricing

### Data Transfer (AWS, per GB)
```yaml
Internet egress (us-east-1):
  - First 10TB:    $0.09/GB
  - 10-50TB:       $0.085/GB
  - 50-150TB:      $0.070/GB
  
Cross-region:      $0.02/GB
Same AZ:           Free
VPC peering:       $0.01/GB

NAT Gateway:
  - $0.045/hour
  - $0.045/GB processed
```

### CDN Pricing
```yaml
CloudFront (per GB):
  - First 10TB:  $0.085/GB
  - 10-50TB:     $0.080/GB
  
Azure CDN:
  - First 10TB:  $0.081/GB
  
Cloud CDN:
  - First 10TB:  $0.085/GB
```

## Price Comparison Examples

### Example 1: Simple Web Application
```typescript
const requirements = {
  compute: '2 x t3.medium (24/7)',
  storage: '100GB SSD',
  database: 'PostgreSQL (db.t3.medium)',
  traffic: '1TB/month egress',
};

const costs = {
  aws: {
    ec2: 2 * 0.0416 * 730 = 60.74,
    ebs: 100 * 0.10 = 10,
    rds: 49.64 + (20 * 0.115) = 51.94,
    transfer: 1000 * 0.09 = 90,
    total: 212.68,
  },
  azure: {
    vm: 2 * 0.0416 * 730 = 60.74,
    disk: 100 * 0.048 = 4.80,
    sql: 406, // Managed SQL more expensive
    transfer: 1000 * 0.087 = 87,
    total: 558.54,
  },
  gcp: {
    compute: 2 * 0.0335 * 730 = 48.91,
    disk: 100 * 0.17 = 17,
    sql: 30.15 + (20 * 0.17) = 33.55,
    transfer: 1000 * 0.12 = 120,
    total: 219.46,
  },
};

// Winner: AWS ($212.68/month)
// With Reserved Instances (1yr): $140/month (34% savings)
```

### Example 2: Serverless API
```typescript
const requirements = {
  requests: '50M/month',
  avgDuration: '200ms',
  avgMemory: '512MB',
};

const lambda = {
  requests: 50 * 0.20 = 10,
  compute: 50e6 * 0.5 * 0.2 * 0.0000166667 = 83.33,
  total: 93.33,
};

const azureFunctions = {
  executions: 50 * 0.20 = 10,
  compute: 50e6 * 0.5 * 0.2 * 0.000016 = 80,
  total: 90,
};

const cloudFunctions = {
  invocations: 50 * 0.40 = 20,
  compute: 50e6 * 0.5 * 0.2 * 0.0000025 = 12.5,
  networking: 1000 * 0.12 = 120, // 1TB egress
  total: 152.50,
};

// Winner: Azure Functions ($90/month)
```

## Free Tiers (Always Free, 2025)

### AWS
```yaml
EC2: 750 hours/month t2.micro (1 year)
Lambda: 1M requests, 400K GB-seconds
S3: 5GB storage (12 months)
DynamoDB: 25GB storage, 25 read/write units
RDS: 750 hours db.t2.micro (12 months)
CloudFront: 1TB transfer (12 months)
```

### Azure
```yaml
App Service: 10 web apps
Functions: 1M requests/month
Blob Storage: 5GB (12 months)
Cosmos DB: 1000 RU/s, 25GB
SQL Database: 100K vCore-seconds (12 months)
```

### GCP
```yaml
Compute: 1 f1-micro instance (744 hours/month)
Cloud Functions: 2M invocations, 400K GB-seconds
Cloud Storage: 5GB standard
Cloud Run: 2M requests, 360K GB-seconds
Firestore: 1GB storage, 50K reads, 20K writes
```

## Pricing Calculators

**AWS Pricing Calculator**: https://calculator.aws
**Azure Pricing Calculator**: https://azure.microsoft.com/pricing/calculator
**GCP Pricing Calculator**: https://cloud.google.com/products/calculator

## Regional Pricing Differences

**Most Expensive**: Asia Pacific (Tokyo, Sydney)
**Cheapest**: US regions (us-east-1, us-west-2)
**Middle**: Europe (eu-west-1, eu-central-1)

Difference: 10-30% higher in APAC vs US East

Make informed pricing decisions with up-to-date cost data!
