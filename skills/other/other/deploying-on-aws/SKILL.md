---
name: deploying-on-aws
description: Selecting and implementing AWS services and architectural patterns. Use when designing AWS cloud architectures, choosing compute/storage/database services, implementing serverless or container patterns, or applying AWS Well-Architected Framework principles.
---

# AWS Patterns

## Purpose

This skill provides decision frameworks and implementation patterns for Amazon Web Services. Navigate AWS's 200+ services through proven selection criteria, architectural patterns, and Well-Architected Framework principles. Focus on practical service selection, cost-aware design, and modern 2025 patterns including Lambda SnapStart, EventBridge Pipes, and S3 Express One Zone.

Use this skill when designing AWS solutions, selecting services for specific workloads, implementing serverless or container architectures, or optimizing existing AWS infrastructure for cost, performance, and reliability.

## When to Use This Skill

Invoke this skill when:

- Choosing between Lambda, Fargate, ECS, EKS, or EC2 for compute workloads
- Selecting database services (RDS, Aurora, DynamoDB) based on access patterns
- Designing VPC architecture for multi-tier applications
- Implementing serverless patterns with API Gateway and Lambda
- Building container-based microservices on ECS or EKS
- Applying AWS Well-Architected Framework to designs
- Optimizing AWS costs while maintaining performance
- Implementing security best practices (IAM, KMS, encryption)

## Core Service Selection Frameworks

### Compute Service Selection

**Decision Flow:**

```
Execution Duration:
  <15 minutes → Evaluate Lambda
  >15 minutes → Evaluate containers or VMs

Event-Driven/Scheduled:
  YES → Lambda (serverless)
  NO → Consider traffic patterns

Containerized:
  YES → Need Kubernetes?
    YES → EKS
    NO → ECS (Fargate or EC2)
  NO → Evaluate EC2 or containerize first

Special Requirements:
  GPU/Windows/BYOL licensing → EC2
  Predictable high traffic → EC2 or ECS on EC2 (cost optimization)
  Variable traffic → Lambda or Fargate
```

**Quick Reference:**

| Workload | Primary Choice | Cost Model | Key Benefit |
|----------|---------------|------------|-------------|
| API Backend | Lambda + API Gateway | Pay per request | Auto-scale, no servers |
| Microservices | ECS on Fargate | Pay for runtime | Simple operations |
| Kubernetes Apps | EKS | $73/mo + compute | Portability, ecosystem |
| Batch Jobs | Lambda or Fargate Spot | Request/spot pricing | Cost efficiency |
| Long-Running | EC2 Reserved Instances | 30-60% savings | Predictable cost |

For detailed service comparisons including cost examples, performance characteristics, and use case guidance, see `references/compute-services.md`.

### Database Service Selection

**Decision Matrix by Access Pattern:**

| Access Pattern | Data Model | Primary Choice | Key Criteria |
|----------------|------------|----------------|--------------|
| Transactional (OLTP) | Relational | Aurora | Performance + HA |
| Simple CRUD | Relational | RDS PostgreSQL | Cost vs. features |
| Key-Value Lookups | NoSQL | DynamoDB | Serverless scale |
| Document Storage | JSON/BSON | DynamoDB | Flexibility vs. MongoDB compat |
| Caching | In-Memory | ElastiCache Redis | Speed + durability |
| Analytics (OLAP) | Columnar | Redshift/Athena | Dedicated vs. serverless |
| Time-Series | Timestamped | Timestream | Purpose-built |

**Query Complexity Guide:**

- **Simple Key-Value:** DynamoDB (single-digit ms latency)
- **Moderate Joins (2-3 tables):** Aurora or RDS (cost vs. performance)
- **Complex Analytics:** Redshift (dedicated) or Athena (serverless, query S3)
- **Real-Time Streams:** DynamoDB Streams + Lambda

For storage class selection, cost comparisons, and migration patterns, see `references/database-services.md`.

### Storage Service Selection

**Primary Decision Tree:**

```
Data Type:
  Objects (files, media) → S3 + lifecycle policies
  Blocks (databases, boot volumes) → EBS
  Shared Files (cross-instance) → Evaluate protocol

File Protocol Required:
  NFS (Linux) → EFS
  SMB (Windows) → FSx for Windows
  High-Performance HPC → FSx for Lustre
  Multi-Protocol + Enterprise → FSx for NetApp ONTAP
```

**Cost Comparison (1TB/month):**

| Service | Monthly Cost | Access Pattern |
|---------|--------------|----------------|
| S3 Standard | $23 | Frequent access |
| S3 Standard-IA | $12.50 | Infrequent (>30 days) |
| S3 Glacier Instant | $4 | Archive, instant retrieval |
| EBS gp3 | $80 | Block storage |
| EFS Standard | $300 | Shared files, frequent |
| EFS IA | $25 | Shared files, infrequent |

**Recommendation:** Use S3 for 80%+ of storage needs. Use EFS/FSx only when shared file access is required.

For S3 storage classes, EBS volume types, and lifecycle policy examples, see `references/storage-services.md`.

## Serverless Architecture Patterns

### Pattern 1: REST API (Lambda + API Gateway + DynamoDB)

**Architecture:**
```
Client → API Gateway (HTTP API) → Lambda → DynamoDB
                                        ↓
                                       S3 (file uploads)
```

**Use When:**
- Building RESTful APIs with CRUD operations
- Variable or unpredictable traffic
- Minimal operational overhead desired
- Pay-per-request cost model acceptable

**Cost Estimate (1M requests/month):**
- API Gateway: $3.50
- Lambda: $3.53
- DynamoDB: ~$7.50
- **Total: ~$15/month** (vs. Fargate ~$35+, EC2 ~$50+)

**Key Components:**
- API Gateway HTTP API (cheaper than REST API)
- Lambda with appropriate memory allocation (1024MB typically optimal)
- DynamoDB on-demand billing (for variable traffic)
- CloudWatch Logs for debugging

See `examples/cdk/serverless-api/` and `examples/terraform/serverless-api/` for complete implementations.

### Pattern 2: Event-Driven Processing (EventBridge + Lambda + SQS)

**Architecture:**
```
S3 Upload → EventBridge Rule → Lambda (process) → DynamoDB (metadata)
                                              ↓
                                            SQS (downstream tasks)
```

**Use When:**
- Asynchronous file processing
- Decoupled microservices communication
- Fan-out patterns (one event, multiple consumers)
- Need retry logic and dead-letter queues

**Key Features (2025):**
- **EventBridge Pipes:** Simplified source → filter → enrichment → target
- **Lambda Response Streaming:** Stream responses up to 20MB
- **Step Functions Distributed Map:** Process millions of items in parallel

See `references/serverless-patterns.md` for additional patterns including Step Functions orchestration, API Gateway WebSockets, and Lambda SnapStart configuration.

## Container Architecture Patterns

### Pattern 1: ECS on Fargate (Serverless Containers)

**Architecture:**
```
ALB → ECS Service (Fargate tasks) → RDS Aurora
                                 ↓
                           ElastiCache Redis
```

**Use When:**
- Containerized applications without cluster management
- Variable traffic with auto-scaling
- Avoid EC2 instance management
- Docker-based deployment

**Key Components:**
- Application Load Balancer (path-based routing)
- ECS Cluster with Fargate launch type
- Task definitions (CPU, memory, container image)
- Auto-scaling based on CPU/memory or custom metrics
- Service Connect for built-in service mesh (2025 feature)

**Cost Model (2 vCPU, 4GB RAM, 24/7):**
- Fargate: ~$70/month
- ALB: ~$20/month
- RDS Aurora db.t3.medium: ~$50/month
- **Total: ~$140/month**

### Pattern 2: EKS (Kubernetes on AWS)

**Use When:**
- Kubernetes expertise exists in team
- Multi-cloud or hybrid cloud strategy
- Need Kubernetes ecosystem (Helm, Operators, Istio)
- Complex workload orchestration requirements

**Key Features (2025):**
- **EKS Auto Mode:** Fully managed node lifecycle
- **EKS Pod Identities:** Simplified IAM (replaces IRSA)
- **EKS Hybrid Nodes:** Run on-premises nodes

**Cost Considerations:**
- EKS control plane: $73/month per cluster
- Worker nodes: Fargate or EC2 pricing
- Use EKS on Fargate for simplicity, EC2 for cost optimization

For ECS task definitions, EKS cluster setup with CDK/Terraform, and service mesh patterns, see `references/container-patterns.md`.

## Networking Essentials

### VPC Architecture

**Standard 3-Tier Pattern:**

```
VPC: 10.0.0.0/16

Per Availability Zone (deploy across 3 AZs):
  Public Subnet:    10.0.X.0/24   (ALB, NAT Gateway)
  Private Subnet:   10.0.1X.0/24  (ECS, Lambda, app tier)
  Database Subnet:  10.0.2X.0/24  (RDS, Aurora, isolated)
```

**Best Practices:**
- Use /16 for VPC CIDR (65,536 IPs for growth)
- Use /24 for subnet CIDRs (256 IPs, 251 usable)
- Deploy across minimum 2 AZs (3 recommended) for high availability
- Use Security Groups (stateful) for instance-level firewall
- Enable VPC Flow Logs for troubleshooting

### Load Balancing

**Service Selection:**

| Load Balancer | Protocol | Use Case | Key Feature |
|---------------|----------|----------|-------------|
| ALB | HTTP/HTTPS | Web apps, APIs | Path/host routing, Lambda targets |
| NLB | TCP/UDP | High performance | Static IP, ultra-low latency |
| GWLB | Layer 3 | Security appliances | Inline inspection |

**ALB Features:**
- Path-based routing: `/api` → backend, `/web` → frontend
- Host-based routing: `api.example.com`, `web.example.com`
- WebSocket and gRPC support
- Integration with Lambda (serverless backends)

For CloudFront CDN patterns, Route 53 routing policies, and VPC peering configurations, see `references/networking.md`.

## Security Best Practices

### IAM Principles

**Least Privilege Pattern:**

```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Action": ["s3:GetObject", "s3:PutObject"],
    "Resource": "arn:aws:s3:::my-bucket/uploads/*"
  }]
}
```

**Core Practices:**
- Use IAM roles (not users) for applications
- Implement least privilege (grant minimum permissions needed)
- Enable MFA for privileged users
- Use IAM Access Analyzer to validate policies
- Leverage AWS Organizations SCPs for guardrails

### Data Protection

**Encryption Requirements:**

| Service | At-Rest Encryption | In-Transit Encryption |
|---------|-------------------|----------------------|
| S3 | SSE-S3 or SSE-KMS | HTTPS (TLS 1.2+) |
| EBS | KMS encryption | N/A (within instance) |
| RDS/Aurora | KMS encryption | TLS connections |
| DynamoDB | KMS encryption | HTTPS API |

**Secrets Management:**
- **Secrets Manager:** Database credentials with automatic rotation
- **Parameter Store:** Application configuration (free tier available)
- **KMS:** Encryption key management (customer-managed keys)

For WAF rules, GuardDuty configuration, and network security patterns, see `references/security.md`.

## AWS Well-Architected Framework

### Six Pillars Overview

**1. Operational Excellence**
- Infrastructure as code (CDK, Terraform, CloudFormation)
- Automated deployments (CI/CD pipelines)
- Observability (CloudWatch Logs, Metrics, X-Ray)
- Runbooks and playbooks for common operations

**2. Security**
- Strong identity foundation (IAM roles and policies)
- Defense in depth (Security Groups, NACLs, WAF)
- Data protection (encryption at rest and in transit)
- Detective controls (CloudTrail, GuardDuty, Security Hub)

**3. Reliability**
- Multi-AZ deployments (RDS Multi-AZ, Aurora replicas)
- Auto-scaling (EC2 ASG, ECS Service Auto Scaling)
- Backup and recovery (automated snapshots, cross-region)
- Chaos engineering (Fault Injection Simulator)

**4. Performance Efficiency**
- Right-size resources (use Compute Optimizer)
- Use managed services (reduce operational overhead)
- Caching strategies (CloudFront, ElastiCache, DAX)
- Monitor and optimize continuously

**5. Cost Optimization**
- Right-sizing compute (match capacity to demand)
- Pricing models (Reserved Instances, Savings Plans, Spot)
- Storage optimization (S3 Intelligent-Tiering, lifecycle policies)
- Cost monitoring (Cost Explorer, Budgets, Trusted Advisor)

**6. Sustainability (Added 2024)**
- Use Graviton processors (60% less energy, 25% better performance)
- Optimize workload placement (renewable energy regions)
- Storage efficiency (delete unused data, compression)
- Software optimization (efficient code, async processing)

For detailed pillar implementation guides, architectural review checklists, and Well-Architected Tool integration, see `references/well-architected.md`.

## Infrastructure as Code

### Tool Selection

**AWS CDK (Cloud Development Kit):**
- **Languages:** TypeScript, Python, Java, C#, Go
- **Best For:** AWS-native workloads, type-safe infrastructure
- **Key Benefit:** High-level constructs, synthesizes to CloudFormation
- **Example:** `examples/cdk/serverless-api/`

**Terraform:**
- **Language:** HCL (HashiCorp Configuration Language)
- **Best For:** Multi-cloud environments
- **Key Benefit:** Largest ecosystem, mature state management
- **Example:** `examples/terraform/serverless-api/`

**CloudFormation:**
- **Language:** YAML or JSON
- **Best For:** Native AWS integration, no additional tools
- **Key Benefit:** AWS service support on day 1
- **Example:** `examples/cloudformation/lambda-api.yaml`

### CDK Quick Start

```bash
# Install CDK CLI
npm install -g aws-cdk

# Initialize new project
cdk init app --language=typescript
npm install

# Deploy infrastructure
cdk bootstrap  # One-time setup
cdk deploy
```

### Terraform Quick Start

```bash
# Install Terraform
brew install terraform  # macOS

# Initialize project
terraform init

# Preview changes
terraform plan

# Apply changes
terraform apply
```

For complete working examples with VPC networking, multi-tier applications, and event-driven architectures, see the `examples/` directory.

## Cost Optimization Strategies

### Compute Cost Optimization

**Right-Sizing:**
- Use AWS Compute Optimizer for EC2/Lambda recommendations
- Monitor CloudWatch metrics (CPU, memory utilization)
- Start conservatively, scale based on actual usage

**Pricing Models:**

| Model | Commitment | Savings | Best For |
|-------|------------|---------|----------|
| On-Demand | None | 0% | Variable workloads |
| Savings Plans | 1-3 years | 30-40% | Flexible compute |
| Reserved Instances | 1-3 years | 30-60% | Predictable workloads |
| Spot Instances | None | 60-90% | Fault-tolerant tasks |

**Graviton Advantage:**
- Graviton3 instances: 25% better performance vs. Graviton2
- 60% less energy consumption
- Available: EC2, Lambda, Fargate, RDS, ElastiCache

### Storage Cost Optimization

**S3 Lifecycle Policies:**
```
Day 0-30:    S3 Standard         ($0.023/GB)
Day 30-90:   S3 Standard-IA      ($0.0125/GB)
Day 90-365:  S3 Glacier Instant  ($0.004/GB)
Day 365+:    S3 Deep Archive     ($0.00099/GB)
```

**EBS Optimization:**
- Use gp3 volumes (20% cheaper than gp2, configurable IOPS)
- Delete unused snapshots
- Archive old snapshots (75% cheaper)

**Monitoring:**
- Enable AWS Cost Explorer (free)
- Set up AWS Budgets with alerts
- Use Cost Allocation Tags for attribution
- Review Trusted Advisor cost checks

## Common Patterns and Examples

### Serverless Three-Tier Application

```
CloudFront (CDN)
  → S3 (React frontend)
  → API Gateway (REST API)
    → Lambda (business logic)
      → DynamoDB (data)
      → S3 (file storage)
```

**Complete CDK implementation:** `examples/cdk/three-tier-app/`
**Complete Terraform implementation:** `examples/terraform/three-tier-app/`

### Containerized Microservices

```
Route 53 (DNS)
  → CloudFront (CDN)
    → ALB (load balancer)
      → ECS Fargate (services)
        → RDS Aurora (database)
        → ElastiCache Redis (cache)
```

**Complete implementation:** `examples/cdk/ecs-fargate/`

### Event-Driven Data Pipeline

```
S3 Upload
  → EventBridge Rule
    → Lambda (transform)
      → Kinesis Firehose
        → S3 Data Lake
          → Athena (query)
```

**Complete implementation:** `examples/cdk/event-driven/`

## Integration with Other Skills

### Related Skills

- **infrastructure-as-code** - Multi-cloud IaC concepts, CDK and Terraform patterns
- **kubernetes-operations** - EKS cluster operations, kubectl, Helm charts
- **building-ci-pipelines** - CodePipeline, CodeBuild, GitHub Actions → AWS
- **secret-management** - Secrets Manager rotation, Parameter Store hierarchies
- **observability** - CloudWatch advanced queries, X-Ray distributed tracing
- **security-hardening** - IAM policy best practices, security automation
- **disaster-recovery** - Multi-region strategies, backup automation

### Cross-Skill Patterns

**EKS + kubernetes-operations:**
- Use this skill for EKS cluster provisioning (CDK/Terraform)
- Use kubernetes-operations for kubectl, Helm, application deployment

**Secrets Management:**
- Use this skill for Secrets Manager/Parameter Store setup
- Use secret-management skill for rotation policies, access patterns

**CI/CD Integration:**
- Use this skill for CodePipeline infrastructure
- Use building-ci-pipelines skill for pipeline configuration

## Reference Documentation

### Detailed Guides

- **Compute Services:** `references/compute-services.md` - Lambda, Fargate, ECS, EKS, EC2 deep dive
- **Database Services:** `references/database-services.md` - RDS, Aurora, DynamoDB, ElastiCache comparison
- **Storage Services:** `references/storage-services.md` - S3 classes, EBS types, EFS/FSx selection
- **Networking:** `references/networking.md` - VPC design, load balancing, CloudFront, Route 53
- **Security:** `references/security.md` - IAM patterns, KMS, Secrets Manager, WAF
- **Serverless Patterns:** `references/serverless-patterns.md` - Advanced Lambda, Step Functions, EventBridge
- **Container Patterns:** `references/container-patterns.md` - ECS Service Connect, EKS Pod Identities
- **Well-Architected:** `references/well-architected.md` - Six pillars implementation guide

### Working Examples

- **CDK Examples:** `examples/cdk/` - TypeScript implementations
- **Terraform Examples:** `examples/terraform/` - HCL implementations
- **CloudFormation Examples:** `examples/cloudformation/` - YAML templates

### Utility Scripts

- **Cost Estimation:** `scripts/cost-estimate.sh` - Estimate infrastructure costs
- **Resource Audit:** `scripts/resource-audit.sh` - Audit AWS resources
- **Security Check:** `scripts/security-check.sh` - Basic security validation

## AWS Service Updates (2025)

**Recent Innovations to Consider:**

- **Lambda SnapStart:** Near-instant cold starts for Java functions
- **Lambda Response Streaming:** Stream responses up to 20MB
- **EventBridge Pipes:** Simplified event processing (source → filter → enrichment → target)
- **S3 Express One Zone:** 10x faster S3, single-digit millisecond latency
- **ECS Service Connect:** Built-in service mesh for ECS
- **EKS Auto Mode:** Fully managed Kubernetes node lifecycle
- **EKS Pod Identities:** Simplified IAM for pods (replaces IRSA)
- **Aurora Limitless Database:** Horizontal write scaling beyond single-writer limit
- **DynamoDB Standard-IA:** Infrequent access tables at 60% cost savings
- **RDS Blue/Green Deployments:** Zero-downtime version upgrades

---

## Quick Decision Checklist

**Before choosing a service, answer:**

1. **Traffic Pattern:** Predictable or variable? (affects compute choice)
2. **Data Model:** Relational, key-value, document, or graph? (affects database choice)
3. **Access Pattern:** Frequent, infrequent, or archive? (affects storage class)
4. **Latency Requirements:** Milliseconds, seconds, or minutes acceptable?
5. **Scaling Needs:** Vertical (bigger instances) or horizontal (more instances)?
6. **Operational Overhead:** Prefer managed services or need control?
7. **Cost Sensitivity:** Optimize for cost, performance, or balance?
8. **Compliance Requirements:** Data residency, encryption, audit logging needed?

**Then consult the relevant decision framework in this skill or detailed references.**

## Getting Started

**For New AWS Projects:**

1. Define architecture using Well-Architected Framework pillars
2. Choose compute service using decision tree (Lambda/Fargate/ECS/EKS/EC2)
3. Select database based on access patterns and data model
4. Design VPC with 3-tier subnet architecture
5. Implement IaC using CDK or Terraform (see examples/)
6. Apply security best practices (IAM, encryption, logging)
7. Set up monitoring and cost tracking

**For Existing AWS Projects:**

1. Run AWS Trusted Advisor for recommendations
2. Review Well-Architected Framework pillars
3. Optimize costs (right-size, Reserved Instances, storage lifecycle)
4. Migrate to modern services (EC2 → Fargate, RDS → Aurora)
5. Improve security posture (enable GuardDuty, implement least privilege)
6. Automate with IaC (reverse-engineer to Terraform or CDK)
