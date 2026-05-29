---
name: LocalStack Service Tiers Reference
description: Reference for LocalStack AWS service availability by tier (Free/Base/Ultimate). Essential for KECS development to understand which AWS-compatible services can be used locally without cost.
allowed-tools:
  - Read
  - WebFetch
---

# LocalStack Service Tiers Reference

This skill provides knowledge about LocalStack service availability across pricing tiers.
KECS uses LocalStack for AWS-compatible services, relying on free tier services for ECS integrations.

## Quick Reference

### Key Insight for KECS Development

**ECS is NOT available in LocalStack Free tier** - it requires Base tier ($39/mo).
This is one of the primary reasons KECS exists: to provide a free, local ECS-compatible environment.

### Pricing Tiers

| Tier | Price | Services |
|------|-------|----------|
| Free (Community) | $0 | 30+ services |
| Base | $39/mo | 55+ services |
| Ultimate | $89/mo | 110+ services |

### Free Tier Services (Commonly Used with ECS)

These services are available for free and can be used with KECS:

- **S3** - Object storage
- **DynamoDB** - NoSQL database
- **SQS** - Simple Queue Service
- **SNS** - Simple Notification Service
- **IAM** - Identity and Access Management
- **SecretsManager** - Secrets management
- **KMS** - Key Management Service
- **SSM** - Systems Manager (Parameter Store)
- **STS** - Security Token Service
- **ACM** - Certificate Manager
- **CloudWatch** - Monitoring (basic features)
- **CloudWatch Logs** - Logging (basic features)
- **Lambda** - Serverless functions (basic features)

### Paid Tier Only Services (NOT Free)

These require LocalStack Base or Ultimate:

- **ECS** - Elastic Container Service (Base+)
- **ECR** - Elastic Container Registry (Base+)
- **ELB/ALB** - Load Balancing (Base+)
- **EC2** - Docker VM mode (Base+, Mock mode is free)

## Detailed Documentation

See `service-tiers.md` for complete service tier information.
