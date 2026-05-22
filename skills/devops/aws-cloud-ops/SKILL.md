---
name: aws-cloud-ops
description: AWS cloud operations for CloudWatch, S3, Lambda, EC2, and IAM
allowed-tools: [Bash, Read]
---

# AWS Cloud Operations Skill

## Overview

Provides 90%+ context savings vs raw AWS MCP server. Multi-service support with progressive disclosure by service category.

## Requirements

- AWS CLI v2
- Configured credentials (AWS_PROFILE or ~/.aws/credentials)
- AWS_REGION environment variable

## Tools (Progressive Disclosure)

### CloudWatch Operations

| Tool         | Description       | Confirmation |
| ------------ | ----------------- | ------------ |
| logs-groups  | List log groups   | No           |
| logs-tail    | Tail log stream   | No           |
| logs-filter  | Filter log events | No           |
| metrics-list | List metrics      | No           |
| metrics-get  | Get metric data   | No           |
| alarm-list   | List alarms       | No           |
| alarm-create | Create alarm      | Yes          |

### S3 Operations

| Tool    | Description          | Confirmation |
| ------- | -------------------- | ------------ |
| s3-ls   | List buckets/objects | No           |
| s3-cp   | Copy objects         | Yes          |
| s3-sync | Sync directories     | Yes          |
| s3-rm   | Delete objects       | Yes          |

### Lambda Operations

| Tool          | Description          | Confirmation |
| ------------- | -------------------- | ------------ |
| lambda-list   | List functions       | No           |
| lambda-get    | Get function details | No           |
| lambda-invoke | Invoke function      | Yes          |
| lambda-logs   | Get function logs    | No           |

### EC2 Operations

| Tool         | Description          | Confirmation |
| ------------ | -------------------- | ------------ |
| ec2-list     | List instances       | No           |
| ec2-describe | Describe instance    | No           |
| ec2-start    | Start instance       | Yes          |
| ec2-stop     | Stop instance        | Yes          |
| sg-list      | List security groups | No           |

### IAM Operations (Read-Only)

| Tool         | Description   | Confirmation |
| ------------ | ------------- | ------------ |
| iam-users    | List users    | No           |
| iam-roles    | List roles    | No           |
| iam-policies | List policies | No           |

## Quick Reference

```bash
# List EC2 instances
aws ec2 describe-instances --output table

# Tail CloudWatch logs
aws logs tail /aws/lambda/my-function --follow

# List S3 buckets
aws s3 ls

# Invoke Lambda
aws lambda invoke --function-name my-func output.json
```

## Configuration

- **AWS_PROFILE**: Named profile to use
- **AWS_REGION**: Target region (e.g., us-east-1)
- **AWS_DEFAULT_OUTPUT**: Output format (json/table/text)

## Security

⚠️ **Never hardcode credentials**
⚠️ **Use IAM roles when possible**
⚠️ **IAM write operations are blocked**

## Agent Integration

- **devops** (primary): Cloud operations
- **cloud-integrator** (primary): Multi-cloud
- **incident-responder** (secondary): Troubleshooting

## Troubleshooting

| Issue         | Solution              |
| ------------- | --------------------- |
| Access denied | Check IAM permissions |
| Region error  | Set AWS_REGION        |
| Credentials   | Run aws configure     |
