---
name: aws-solution-architect
description: Master AWS solution architecture covering Well-Architected Framework, service selection, high availability, security, cost optimization, and cloud-native design patterns. Use PROACTIVELY for AWS architecture decisions, cloud migrations, security reviews, or cost optimization.
---

# AWS Solution Architect

Master AWS solution architecture principles, service selection, and design patterns for building secure, reliable, performant, and cost-effective cloud solutions.

## When to Use This Skill

- Designing new AWS architectures
- Reviewing cloud infrastructure for best practices
- Migrating workloads to AWS
- Optimizing AWS costs
- Implementing security and compliance
- Troubleshooting performance issues
- Preparing for scale requirements
- Making service selection decisions

## Core Concepts

### 1. AWS Well-Architected Framework

Structure your architecture review around the six pillars.

```
┌──────────────────────────────────────────────────────────────────┐
│               AWS WELL-ARCHITECTED PILLARS                        │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  1. OPERATIONAL EXCELLENCE                                        │
│     ├── Operations as code (IaC, CI/CD)                          │
│     ├── Make frequent, small, reversible changes                 │
│     ├── Refine operations procedures frequently                  │
│     ├── Anticipate failure (runbooks, game days)                 │
│     └── Learn from all operational events                        │
│                                                                   │
│  2. SECURITY                                                      │
│     ├── Implement strong identity foundation (IAM)               │
│     ├── Enable traceability (CloudTrail, logs)                   │
│     ├── Apply security at all layers                             │
│     ├── Automate security best practices                         │
│     └── Protect data in transit and at rest                      │
│                                                                   │
│  3. RELIABILITY                                                   │
│     ├── Automatically recover from failure                       │
│     ├── Test recovery procedures                                 │
│     ├── Scale horizontally for aggregate availability            │
│     ├── Stop guessing capacity (auto-scaling)                    │
│     └── Manage change through automation                         │
│                                                                   │
│  4. PERFORMANCE EFFICIENCY                                        │
│     ├── Democratize advanced technologies (managed services)     │
│     ├── Go global in minutes                                     │
│     ├── Use serverless architectures                             │
│     ├── Experiment more often                                    │
│     └── Consider mechanical sympathy                             │
│                                                                   │
│  5. COST OPTIMIZATION                                             │
│     ├── Implement cloud financial management                     │
│     ├── Adopt consumption model (pay for what you use)           │
│     ├── Measure overall efficiency                               │
│     ├── Stop spending on undifferentiated heavy lifting          │
│     └── Analyze and attribute expenditure                        │
│                                                                   │
│  6. SUSTAINABILITY                                                │
│     ├── Understand your impact                                   │
│     ├── Establish sustainability goals                           │
│     ├── Maximize utilization                                     │
│     ├── Use managed services                                     │
│     └── Reduce downstream impact                                 │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘
```

### 2. High Availability Patterns

Design for failure at every layer.

```
MULTI-AZ ARCHITECTURE:

┌─────────────────────────────────────────────────────────────────┐
│                         REGION (us-east-1)                       │
│                                                                  │
│    ┌─────────────────┐              ┌─────────────────┐         │
│    │   AZ-1 (1a)     │              │   AZ-2 (1b)     │         │
│    │                 │              │                 │         │
│    │ ┌─────────────┐ │              │ ┌─────────────┐ │         │
│    │ │ Public      │ │              │ │ Public      │ │         │
│    │ │ Subnet      │ │              │ │ Subnet      │ │         │
│    │ │ ┌───────┐   │ │              │ │ ┌───────┐   │ │         │
│    │ │ │  NAT  │   │ │              │ │ │  NAT  │   │ │         │
│    │ │ │Gateway│   │ │              │ │ │Gateway│   │ │         │
│    │ │ └───────┘   │ │              │ │ └───────┘   │ │         │
│    │ └─────────────┘ │              │ └─────────────┘ │         │
│    │                 │              │                 │         │
│    │ ┌─────────────┐ │              │ ┌─────────────┐ │         │
│    │ │ Private     │ │              │ │ Private     │ │         │
│    │ │ Subnet      │ │              │ │ Subnet      │ │         │
│    │ │ ┌───────┐   │ │    ┌───┐    │ │ ┌───────┐   │ │         │
│    │ │ │  EC2  │◄──┼─┼────┤ALB├────┼─┼►│  EC2  │   │ │         │
│    │ │ │(ASG)  │   │ │    └───┘    │ │ │(ASG)  │   │ │         │
│    │ │ └───────┘   │ │              │ │ └───────┘   │ │         │
│    │ └─────────────┘ │              │ └─────────────┘ │         │
│    │                 │              │                 │         │
│    │ ┌─────────────┐ │              │ ┌─────────────┐ │         │
│    │ │ Data        │ │              │ │ Data        │ │         │
│    │ │ Subnet      │ │              │ │ Subnet      │ │         │
│    │ │ ┌─────────┐ │ │   sync      │ │ ┌─────────┐ │ │         │
│    │ │ │   RDS   │◄┼─┼─────────────┼─┼►│   RDS   │ │ │         │
│    │ │ │(Primary)│ │ │              │ │ │(Standby)│ │ │         │
│    │ │ └─────────┘ │ │              │ │ └─────────┘ │ │         │
│    │ └─────────────┘ │              │ └─────────────┘ │         │
│    └─────────────────┘              └─────────────────┘         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

KEY HA PATTERNS:

1. STATELESS COMPUTE
   ├── No local state on instances
   ├── Session data in ElastiCache/DynamoDB
   ├── Auto Scaling Group across AZs
   └── Instance can be replaced any time

2. DATA LAYER HA
   ├── RDS Multi-AZ (synchronous standby)
   ├── Aurora (multiple read replicas)
   ├── DynamoDB (built-in replication)
   └── ElastiCache (cluster mode)

3. DNS FAILOVER
   ├── Route 53 health checks
   ├── Failover routing policy
   ├── Multi-region active-active
   └── Weighted routing for gradual shifts
```

### 3. Security Architecture

Defense in depth across all layers.

```
SECURITY LAYERS:

┌────────────────────────────────────────────────────────────────┐
│                        EDGE SECURITY                            │
│                                                                 │
│  CloudFront ───► WAF ───► Shield                               │
│  ├── HTTPS/TLS               ├── SQL injection                 │
│  ├── Geo restriction         ├── XSS protection                │
│  └── Signed URLs             └── DDoS protection               │
└────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌────────────────────────────────────────────────────────────────┐
│                       NETWORK SECURITY                          │
│                                                                 │
│  VPC ───► Security Groups ───► NACLs                           │
│  ├── Private subnets         ├── Stateful rules                │
│  ├── No public IPs           ├── Instance level                │
│  ├── VPC endpoints           ├── Least privilege               │
│  └── Transit Gateway         └── Subnet level (stateless)      │
└────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌────────────────────────────────────────────────────────────────┐
│                      APPLICATION SECURITY                       │
│                                                                 │
│  IAM ───► Secrets Manager ───► KMS                             │
│  ├── Role-based access       ├── Rotate secrets                │
│  ├── No long-term keys       ├── No hardcoded creds            │
│  ├── MFA enforced            └── Encryption at rest            │
│  └── Permission boundaries                                      │
└────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌────────────────────────────────────────────────────────────────┐
│                       DATA SECURITY                             │
│                                                                 │
│  S3 ───► RDS ───► DynamoDB                                     │
│  ├── Bucket policies         ├── Encryption (SSE-KMS)          │
│  ├── Block public access     ├── VPC only access               │
│  ├── Versioning              ├── Fine-grained access           │
│  └── Object lock             └── Audit logging                 │
└────────────────────────────────────────────────────────────────┘

IAM BEST PRACTICES:

# ✅ CORRECT: Role-based, least privilege
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:PutObject"
            ],
            "Resource": "arn:aws:s3:::my-bucket/uploads/*",
            "Condition": {
                "StringEquals": {
                    "s3:x-amz-acl": "bucket-owner-full-control"
                }
            }
        }
    ]
}

# ❌ WRONG: Overly permissive
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "s3:*",
            "Resource": "*"
        }
    ]
}
```

### 4. Service Selection Matrix

Choose the right service for the job.

```
COMPUTE OPTIONS:

┌─────────────────┬──────────────────────────────────────────────┐
│ Service         │ Best For                                     │
├─────────────────┼──────────────────────────────────────────────┤
│ EC2             │ Full control, long-running, specific OS      │
│ ECS/Fargate     │ Containerized apps, microservices            │
│ EKS             │ Kubernetes workloads, portability            │
│ Lambda          │ Event-driven, short duration (<15min)        │
│ App Runner      │ Simple container deployments                 │
│ Batch           │ Batch processing, HPC                        │
│ Lightsail       │ Simple apps, predictable pricing             │
└─────────────────┴──────────────────────────────────────────────┘

DATABASE OPTIONS:

┌─────────────────┬───────────────┬──────────────────────────────┐
│ Service         │ Type          │ Best For                     │
├─────────────────┼───────────────┼──────────────────────────────┤
│ RDS             │ Relational    │ Traditional apps, ACID       │
│ Aurora          │ Relational    │ High performance, HA         │
│ DynamoDB        │ NoSQL (KV)    │ Low latency, scale, simple   │
│ DocumentDB      │ NoSQL (Doc)   │ MongoDB compatibility        │
│ ElastiCache     │ In-memory     │ Caching, sessions            │
│ Neptune         │ Graph         │ Relationships, networks      │
│ Timestream      │ Time-series   │ IoT, metrics                 │
│ Redshift        │ Data warehouse│ Analytics, BI                │
│ OpenSearch      │ Search        │ Full-text, logs              │
└─────────────────┴───────────────┴──────────────────────────────┘

STORAGE OPTIONS:

┌─────────────────┬──────────────────────────────────────────────┐
│ Service         │ Best For                                     │
├─────────────────┼──────────────────────────────────────────────┤
│ S3 Standard     │ Frequently accessed data                     │
│ S3 IA           │ Infrequently accessed (>30 days)             │
│ S3 Glacier      │ Archive (minutes to hours retrieval)         │
│ S3 Glacier Deep │ Long-term archive (12 hours retrieval)       │
│ EBS gp3         │ General purpose block storage                │
│ EBS io2         │ High IOPS, databases                         │
│ EFS             │ Shared file storage (Linux)                  │
│ FSx             │ Windows, Lustre, NetApp                      │
└─────────────────┴──────────────────────────────────────────────┘

MESSAGING OPTIONS:

┌─────────────────┬──────────────────────────────────────────────┐
│ Service         │ Best For                                     │
├─────────────────┼──────────────────────────────────────────────┤
│ SQS             │ Decoupling, at-least-once delivery           │
│ SQS FIFO        │ Ordering guaranteed, exactly-once            │
│ SNS             │ Pub/sub, fan-out                             │
│ EventBridge     │ Event routing, SaaS integration              │
│ Kinesis Streams │ Real-time streaming, ordering                │
│ Kinesis Firehose│ Data delivery to S3/Redshift                 │
│ MSK (Kafka)     │ Kafka workloads, replay                      │
│ MQ              │ ActiveMQ/RabbitMQ migration                  │
└─────────────────┴──────────────────────────────────────────────┘
```

### 5. Serverless Architecture Patterns

Event-driven, fully managed patterns.

```
SERVERLESS WEB APPLICATION:

┌────────────────────────────────────────────────────────────────┐
│                       SERVERLESS STACK                          │
│                                                                 │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐    │
│  │CloudFront│──►│   S3     │   │API       │──►│ Lambda   │    │
│  │  (CDN)   │   │ (Static) │   │Gateway   │   │(Compute) │    │
│  └──────────┘   └──────────┘   └──────────┘   └────┬─────┘    │
│                                                     │          │
│                                    ┌────────────────┼────────┐ │
│                                    │                │        │ │
│                               ┌────▼────┐    ┌─────▼─────┐   │ │
│                               │DynamoDB │    │  Aurora   │   │ │
│                               │ (NoSQL) │    │Serverless │   │ │
│                               └─────────┘    └───────────┘   │ │
└────────────────────────────────────────────────────────────────┘

EVENT-DRIVEN PROCESSING:

┌────────────────────────────────────────────────────────────────┐
│                                                                 │
│   S3 Upload ───► EventBridge ───► Step Functions               │
│        │               │               │                        │
│        │               │          ┌────┴────┐                   │
│        │               │          │         │                   │
│        │               │     ┌────▼───┐ ┌───▼────┐              │
│        │               │     │Lambda 1│ │Lambda 2│              │
│        │               │     │(Process)│ │(Notify)│              │
│        │               │     └────────┘ └────────┘              │
│        │               │                                        │
│        │          ┌────▼────┐                                   │
│        │          │   SNS   │                                   │
│        │          │(Fan-out)│                                   │
│        │          └────┬────┘                                   │
│        │               │                                        │
│   ┌────▼────┐    ┌────▼────┐                                   │
│   │  SQS    │    │Lambda 3 │                                   │
│   │(Buffer) │    │ (Async) │                                   │
│   └─────────┘    └─────────┘                                   │
└────────────────────────────────────────────────────────────────┘

LAMBDA BEST PRACTICES:

1. COLD START OPTIMIZATION
   ├── Keep package size small
   ├── Use Provisioned Concurrency for critical paths
   ├── Initialize SDK clients outside handler
   └── Use ARM (Graviton2) for cost/performance

2. CONNECTION MANAGEMENT
   ├── Use RDS Proxy for database connections
   ├── Keep connections open between invocations
   └── Set appropriate timeout values

3. SECURITY
   ├── Least privilege IAM roles
   ├── Don't store secrets in environment variables
   ├── Use VPC only when necessary (adds latency)
   └── Enable X-Ray tracing

# Lambda configuration example (CDK/TypeScript)
new lambda.Function(this, 'ProcessorFunction', {
    runtime: lambda.Runtime.NODEJS_20_X,
    architecture: lambda.Architecture.ARM_64,
    handler: 'index.handler',
    code: lambda.Code.fromAsset('lambda'),
    timeout: Duration.seconds(30),
    memorySize: 1024,  // CPU scales with memory
    reservedConcurrentExecutions: 100,  // Limit blast radius
    tracing: lambda.Tracing.ACTIVE,
    environment: {
        TABLE_NAME: table.tableName,
    },
});
```

### 6. Cost Optimization

Control and reduce cloud spending.

```
COST OPTIMIZATION STRATEGIES:

┌────────────────────────────────────────────────────────────────┐
│                    COST REDUCTION LEVERS                        │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. RIGHT-SIZING                                                │
│     ├── Use Compute Optimizer recommendations                  │
│     ├── Start small, scale up based on metrics                 │
│     ├── Review utilization monthly                             │
│     └── Consider Graviton (ARM) instances (20-40% cheaper)     │
│                                                                 │
│  2. PURCHASING OPTIONS                                          │
│     ├── Reserved Instances (up to 72% savings)                 │
│     │   └── Commit to 1-3 years for steady workloads          │
│     ├── Savings Plans (up to 72% savings)                      │
│     │   └── Flexible commitment (compute or EC2)               │
│     ├── Spot Instances (up to 90% savings)                     │
│     │   └── Fault-tolerant, flexible workloads                │
│     └── On-Demand                                               │
│         └── Variable, unpredictable workloads                  │
│                                                                 │
│  3. STORAGE OPTIMIZATION                                        │
│     ├── S3 Intelligent Tiering (automatic)                     │
│     ├── Lifecycle policies to Glacier                          │
│     ├── Delete unused EBS snapshots                            │
│     └── gp3 volumes (baseline IOPS included)                   │
│                                                                 │
│  4. ARCHITECTURE CHANGES                                        │
│     ├── Serverless (pay per use, no idle cost)                 │
│     ├── Containerization (better bin packing)                  │
│     ├── Caching (reduce backend load)                          │
│     └── CDN (reduce origin requests)                           │
│                                                                 │
└────────────────────────────────────────────────────────────────┘

COST MONITORING:

┌────────────────────────────────────────────────────────────────┐
│  Tool                    │ Use For                             │
├──────────────────────────┼─────────────────────────────────────┤
│  Cost Explorer           │ Visualize and analyze spending      │
│  Budgets                 │ Alerts when approaching limits      │
│  Cost Anomaly Detection  │ ML-based unusual spend detection    │
│  Compute Optimizer       │ Right-sizing recommendations        │
│  Trusted Advisor         │ Cost optimization checks            │
│  Cost Allocation Tags    │ Attribute costs to projects/teams   │
└────────────────────────────────────────────────────────────────┘

TAGGING STRATEGY:

Required tags for all resources:
├── Environment: dev | staging | prod
├── Project: project-name
├── Owner: team-name
├── CostCenter: cost-center-code
└── CreatedBy: terraform | manual | cdk
```

### 7. Data Architecture Patterns

Design for data at scale.

```
DATA LAKE ARCHITECTURE:

┌────────────────────────────────────────────────────────────────┐
│                        DATA LAKE                                │
│                                                                 │
│  Ingestion ──────────────────────────────────────────────────► │
│  │                                                              │
│  │  ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐     │
│  ├──│ Kinesis │   │ Glue    │   │ Lake    │   │ Athena  │     │
│  │  │Firehose │──►│ ETL     │──►│Formation│──►│ Query   │     │
│  │  └─────────┘   └─────────┘   └─────────┘   └─────────┘     │
│  │                                    │              │          │
│  │                               ┌────▼────┐   ┌─────▼─────┐   │
│  │                               │   S3    │   │ Redshift  │   │
│  │                               │(Storage)│   │ (DW)      │   │
│  │                               └─────────┘   └───────────┘   │
│  │                                    │              │          │
│  └────────────────────────────────────┴──────────────┴─────────│
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                   DATA ZONES                              │  │
│  │  ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐  │  │
│  │  │  Raw    │──►│Cleansed │──►│Curated  │──►│Consumed │  │  │
│  │  │ (Bronze)│   │(Silver) │   │ (Gold)  │   │  (Apps) │  │  │
│  │  └─────────┘   └─────────┘   └─────────┘   └─────────┘  │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────┘

EVENT SOURCING WITH AWS:

┌────────────────────────────────────────────────────────────────┐
│                                                                 │
│   API ───► EventBridge ───► Kinesis ───► Lambda ───► DynamoDB  │
│             │                  │            │                   │
│             │                  │            │ (Projections)     │
│             │                  ▼            │                   │
│             │              S3 (archive)     │                   │
│             │                               │                   │
│             └───► SNS ───► Lambda ──────────┘                   │
│                  (notifications)                                │
│                                                                 │
└────────────────────────────────────────────────────────────────┘

CACHING STRATEGY:

┌────────────────────────────────────────────────────────────────┐
│                        CACHE LAYERS                             │
│                                                                 │
│  Browser ───► CloudFront ───► ElastiCache ───► Database        │
│    │              │               │                │            │
│    │         Edge cache      App cache         Source          │
│    │         (seconds)       (minutes)       of truth          │
│    │                                                            │
│  Local cache                     │                              │
│  (session storage)               │                              │
│                        ┌─────────┴─────────┐                    │
│                        │                   │                    │
│                   Cache-aside         Read-through              │
│                   (app manages)      (cache manages)            │
└────────────────────────────────────────────────────────────────┘
```

### 8. Migration Strategies

Move workloads to AWS effectively.

```
THE 7 R's OF MIGRATION:

┌────────────────────────────────────────────────────────────────┐
│                                                                 │
│  REHOST (Lift & Shift)                                         │
│  ├── Move as-is to AWS                                         │
│  ├── Fast, minimal changes                                     │
│  └── Use: VM Import, CloudEndure                               │
│                                                                 │
│  RELOCATE (Hypervisor-level)                                   │
│  ├── Move to VMware Cloud on AWS                               │
│  └── Minimal changes, keep VMware skills                       │
│                                                                 │
│  REPLATFORM (Lift, Tinker, Shift)                              │
│  ├── Minor optimizations                                       │
│  ├── Example: Move to managed database                         │
│  └── Moderate effort, good cloud benefits                      │
│                                                                 │
│  REPURCHASE (Drop & Shop)                                      │
│  ├── Move to SaaS version                                      │
│  └── Example: On-prem CRM → Salesforce                         │
│                                                                 │
│  REFACTOR (Re-architect)                                       │
│  ├── Redesign cloud-native                                     │
│  ├── Maximum cloud benefits                                    │
│  └── Highest effort and risk                                   │
│                                                                 │
│  RETIRE                                                         │
│  ├── Decommission unused applications                          │
│  └── Often 10-20% of portfolio                                 │
│                                                                 │
│  RETAIN                                                         │
│  ├── Keep on-premises for now                                  │
│  └── Compliance, dependency, or timing reasons                 │
│                                                                 │
└────────────────────────────────────────────────────────────────┘

MIGRATION PHASES:

Phase 1: ASSESS
├── Discover inventory (Application Discovery Service)
├── Analyze dependencies
├── Define migration groups
└── Build business case

Phase 2: MOBILIZE
├── Build landing zone (Control Tower)
├── Train teams
├── Prove migration pattern (pilot)
└── Refine approach

Phase 3: MIGRATE & MODERNIZE
├── Execute migration waves
├── Validate functionality
├── Optimize after migration
└── Iterate and improve

HYBRID CONNECTIVITY:

┌────────────────────────────────────────────────────────────────┐
│                                                                 │
│  On-Premises ◄──────────────────────────────────────► AWS      │
│       │                                                    │    │
│       │  Site-to-Site VPN (encrypted, internet)           │    │
│       │  ├── Quick to set up                              │    │
│       │  └── Variable performance                         │    │
│       │                                                    │    │
│       │  Direct Connect (dedicated)                        │    │
│       │  ├── Consistent performance                        │    │
│       │  ├── Lower latency                                 │    │
│       │  └── Higher bandwidth                              │    │
│       │                                                    │    │
│       │  Transit Gateway                                   │    │
│       │  ├── Hub for multiple VPCs                         │    │
│       │  └── Simplifies network architecture               │    │
│       │                                                    │    │
└────────────────────────────────────────────────────────────────┘
```

## Quick Reference

### Key Limits to Remember

| Service     | Limit          | Notes                         |
| ----------- | -------------- | ----------------------------- |
| Lambda      | 15 min timeout | Use Step Functions for longer |
| Lambda      | 10 GB memory   | CPU scales with memory        |
| API Gateway | 29 sec timeout | Consider ALB for longer       |
| SQS         | 256 KB message | Use S3 for larger payloads    |
| DynamoDB    | 400 KB item    | Design for smaller items      |
| S3          | 5 TB object    | Use multipart for >100 MB     |
| VPC         | 5 per region   | Can request increase          |

### Service Abbreviations

| Abbr | Service                     |
| ---- | --------------------------- |
| ALB  | Application Load Balancer   |
| NLB  | Network Load Balancer       |
| ASG  | Auto Scaling Group          |
| ECS  | Elastic Container Service   |
| EKS  | Elastic Kubernetes Service  |
| MSK  | Managed Streaming for Kafka |
| MQ   | Amazon MQ                   |

## Common Pitfalls

| Pitfall               | Problem                | Solution                       |
| --------------------- | ---------------------- | ------------------------------ |
| All in one VPC        | Blast radius too large | Separate VPCs per environment  |
| Public subnets only   | Security exposure      | Use private subnets + NAT      |
| No encryption         | Compliance risk        | Enable encryption everywhere   |
| Hardcoded credentials | Security vulnerability | Use IAM roles, Secrets Manager |
| No monitoring         | Blind to issues        | CloudWatch, X-Ray, alarms      |
| Over-provisioned      | Wasted cost            | Right-size, use Spot/Reserved  |
| Single AZ             | Availability risk      | Multi-AZ for production        |
| No DR plan            | Business continuity    | Cross-region backups, runbooks |

## Best Practices Summary

### Security

- Use IAM roles, never access keys
- Enable encryption at rest and in transit
- Private subnets for compute, VPC endpoints for services
- Enable CloudTrail, Config, GuardDuty

### Reliability

- Multi-AZ for all stateful services
- Auto Scaling based on metrics
- Health checks at every layer
- Regular DR testing

### Performance

- Cache aggressively (CloudFront, ElastiCache)
- Right-size instances based on actual usage
- Use Provisioned Concurrency for latency-critical Lambda
- Monitor P99, not just average

### Cost

- Tag everything for cost allocation
- Set up Budgets and alerts
- Review Cost Explorer weekly
- Use Reserved/Savings Plans for steady workloads


## Parent Hub
- [_devops-cloud-mastery](../_devops-cloud-mastery/SKILL.md)


## Part of Workflow
This skill is utilized in the following sequential workflows:
- [_workflow-feature-lifecycle](../_workflow-feature-lifecycle/SKILL.md)
