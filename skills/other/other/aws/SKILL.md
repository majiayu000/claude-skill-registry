---
name: aws
description: Amazon Web Services cloud platform with Lambda, EC2, S3, and RDS. Use for AWS infrastructure.
---

# AWS

Amazon Web Services (AWS) is the dominant cloud platform. In 2025, the focus is heavily on **Generative AI** (Bedrock, Q, Trainium chips) and **Serverless Data** (Aurora Limitless).

## When to Use

- **Enterprise**: The default choice for large-scale, compliant infrastructure.
- **AI/ML**: Amazon SageMaker and Bedrock provide the deepest toolset for training and inference.
- **Serverless**: Lambda + DynamoDB + API Gateway is the canonical serverless stack.

## Core Concepts

### VPC (Virtual Private Cloud)

Your isolated network. Subnets, Route Tables, Internet Gateways. Understanding networking is mandatory.

### IAM (Identity and Access Management)

Global service for permissions. "Deny by default". Use **Roles** for services, not access keys.

### Compute

- **EC2**: Virtual Machines.
- **ECS/EKS**: Containers (Docker/K8s).
- **Lambda**: Function-as-a-Service.

## Best Practices (2025)

**Do**:

- **Use AWS Organizations**: Separate Prod, Staging, and Dev into different _Accounts_, not just VPCs. Limits blast radius.
- **Use CDK / Terraform**: Never click in the console for production resources.
- **Cost Control**: Enable Cost Explorer and set up Budgets/Alerts on day one.

**Don't**:

- **Don't use Public Subnets for Apps**: Put your EC2s/RDS in Private Subnets. Only Load Balancers go in Public Subnets.

## References

- [AWS Documentation](https://docs.aws.amazon.com/)
