---
name: aws-cloud
description: Provides comprehensive AWS (Amazon Web Services) guidance including EC2, S3, RDS, Lambda, ECS/EKS, CloudFormation, API Gateway, CloudFront, cloud migration from on-premise/GCP/Azure, security configuration (IAM, KMS, Security Hub), cost optimization (Savings Plans, Reserved Instances), and multi-region deployment. Produces infrastructure as code (Terraform/CloudFormation/CDK), deployment scripts, security configurations, and architecture designs. Use when deploying to AWS, designing AWS infrastructure, migrating to AWS, configuring EC2 instances, setting up S3 buckets, managing RDS databases, deploying containers on ECS/EKS, building serverless applications, or when users mention AWS, Amazon Cloud, EC2, S3, Lambda, EKS, CloudFormation, CDK, or AWS services.
---

# AWS Cloud

## Core Capabilities

Provides expert guidance for AWS infrastructure and services:

1. **Compute Services** - EC2, Lambda, ECS, EKS, Fargate, Batch, Elastic Beanstalk
2. **Storage Services** - S3, EBS, EFS, FSx, Glacier, Storage Gateway
3. **Database Services** - RDS (MySQL, PostgreSQL, Oracle, SQL Server), Aurora, DynamoDB, ElastiCache, DocumentDB
4. **Networking** - VPC, ALB/NLB, Route 53, CloudFront, Direct Connect, VPN, Transit Gateway
5. **Container Services** - ECS (Elastic Container Service), EKS (Elastic Kubernetes Service), ECR (Elastic Container Registry)
6. **Serverless** - Lambda, API Gateway, Step Functions, EventBridge, SQS, SNS
7. **Infrastructure as Code** - CloudFormation, Terraform, CDK (Cloud Development Kit), SAM
8. **Security** - IAM, KMS, Secrets Manager, Security Hub, GuardDuty, WAF, Shield
9. **Migration** - Cloud migration strategies from on-premise, GCP, Azure to AWS

## Key Principles

## General Best Practices

- **Follow least privilege** - Use IAM roles with minimal required permissions
- **Enable monitoring** - Configure CloudWatch for all services with appropriate alarms
- **Use managed services** - Prefer RDS over self-managed databases, ECS Fargate over EC2
- **Implement IaC** - Use CloudFormation, Terraform, or CDK for reproducible infrastructure
- **Tag resources** - Apply tags for cost allocation, automation, and compliance
- **Design for HA** - Use Multi-AZ deployments and Auto Scaling Groups
- **Secure by default** - Enable encryption, use private subnets, configure security groups properly
- **Optimize costs** - Use Reserved Instances, Savings Plans, Spot Instances, and right-sizing

### Architecture Patterns

- **Multi-tier web apps**: VPC + ALB + EC2/ECS + RDS Multi-AZ
- **Serverless APIs**: API Gateway + Lambda + DynamoDB with CloudFront caching
- **Container workloads**: ECS/EKS with Fargate + RDS + ElastiCache
- **Data processing**: S3 + Lambda/Glue + Athena/EMR + QuickSight
- **Microservices**: EKS + Service Mesh + RDS Aurora + ElastiCache

### When to Use What

- **EC2**: Full control, Windows workloads, lift-and-shift migrations, specialized hardware
- **Lambda**: Event-driven processing, APIs, scheduled tasks, short-lived workloads (<15 min)
- **ECS/EKS**: Containerized applications, microservices, long-running services
- **RDS**: Relational databases with automated backups, Multi-AZ, read replicas
- **Aurora**: High-performance MySQL/PostgreSQL, serverless option, global databases
- **DynamoDB**: NoSQL, single-digit millisecond latency, serverless, automatic scaling
- **S3**: Object storage, static websites, data lakes, backups, archival
- **Elastic Beanstalk**: Quick deployment, managed platform, minimal configuration

## Detailed References

Load reference files based on specific needs:

- **Best Practices by Service**: See [best-practices.md](references/best-practices.md) for:
  - EC2 instance selection, security, HA, performance, and cost optimization
  - S3 security, encryption, data management, performance, and cost strategies
  - RDS and Aurora HA, security, performance tuning, and cost optimization
  - VPC networking, security groups, NACLs, load balancing, and DNS
  - Lambda function design, performance, security, reliability, and cost
  - ECS/EKS container orchestration and security
  - IAM access control, credential management, and compliance
  - Security threat detection, data protection, and compliance
  - Comprehensive cost optimization strategies across all services

- **Compute Services**: See [compute-services.md](references/compute-services.md) for:
  - EC2 instance types, families, and selection guide
  - Auto Scaling Groups configuration and policies
  - Lambda function patterns and event sources
  - Elastic Beanstalk deployment strategies
  - AWS Batch job scheduling and compute environments

- **Storage Solutions**: See [storage-solutions.md](references/storage-solutions.md) for:
  - S3 bucket configuration and lifecycle management
  - EBS volume types and performance optimization
  - EFS file system setup and mounting
  - FSx for Windows and Lustre use cases
  - Storage tier selection and cost optimization

- **Database Services**: See [database-services.md](references/database-services.md) for:
  - RDS instance configuration and best practices
  - Aurora serverless and global database setup
  - DynamoDB data modeling and performance optimization
  - ElastiCache (Redis/Memcached) patterns
  - Database migration strategies with DMS

- **Networking Architecture**: See [networking-architecture.md](references/networking-architecture.md) for:
  - VPC design patterns and CIDR planning
  - ALB/NLB configuration and target group management
  - Route 53 DNS routing policies
  - CloudFront distribution setup and caching strategies
  - Direct Connect and VPN Gateway configuration
  - Transit Gateway hub-and-spoke architecture

- **Container Orchestration**: See [container-orchestration.md](references/container-orchestration.md) for:
  - ECS cluster setup and task definition patterns
  - EKS cluster provisioning with eksctl/Terraform
  - Fargate vs EC2 launch type decision guide
  - ECR repository management and image lifecycle
  - Service mesh with AWS App Mesh

- **Serverless Architecture**: See [serverless-architecture.md](references/serverless-architecture.md) for:
  - Lambda function design patterns and best practices
  - API Gateway REST/HTTP/WebSocket APIs
  - Step Functions state machine workflows
  - EventBridge event-driven architectures
  - SQS/SNS messaging patterns
  - SAM and Serverless Framework usage

- **Infrastructure as Code**: See [infrastructure-as-code.md](references/infrastructure-as-code.md) for:
  - CloudFormation templates and stack management
  - Terraform AWS provider modules and patterns
  - CDK (Cloud Development Kit) constructs and stacks
  - SAM templates for serverless applications
  - Multi-environment deployment strategies
  - State management and remote backends

- **Cloud Migration**: See [cloud-migration.md](references/cloud-migration.md) for:
  - Migration strategies (6 R's: Rehost, Replatform, Refactor, Repurchase, Retire, Retain)
  - AWS Migration Hub and Application Discovery Service
  - Database migration with DMS (Database Migration Service)
  - Server migration with AWS MGN (Application Migration Service)
  - Data transfer with DataSync, Transfer Family, Snowball
  - Migration readiness assessment and planning

- **Security Configuration**: See [security-configuration.md](references/security-configuration.md) for:
  - IAM policy examples and best practices
  - KMS key management and encryption patterns
  - Secrets Manager integration patterns
  - Security group and NACL rule templates
  - CloudTrail multi-region setup
  - GuardDuty and Security Hub configuration
  - WAF rules and Shield Advanced setup
  - Compliance frameworks (PCI-DSS, HIPAA, SOC 2)

- **Monitoring and Operations**: See [monitoring-operations.md](references/monitoring-operations.md) for:
  - CloudWatch metrics, logs, and alarms
  - CloudWatch Insights queries for log analysis
  - X-Ray distributed tracing setup
  - EventBridge rules for event-driven automation
  - Systems Manager for fleet management
  - AWS Backup for centralized backup management
  - Disaster recovery strategies

- **Cost Management**: See [cost-management.md](references/cost-management.md) for:
  - Cost allocation tagging strategies
  - Reserved Instance and Savings Plan planning
  - Spot Instance strategies and best practices
  - Cost Explorer reports and analysis
  - AWS Budgets and anomaly detection
  - Trusted Advisor recommendations
  - FinOps best practices for cloud financial management

- **Well-Architected Framework**: See [well-architected.md](references/well-architected.md) for:
  - Operational Excellence pillar best practices
  - Security pillar implementation guide
  - Reliability pillar design patterns
  - Performance Efficiency optimization techniques
  - Cost Optimization strategies
  - Sustainability best practices
