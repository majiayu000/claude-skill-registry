---
name: aws-cli-beast
description: Provides advanced AWS CLI patterns for managing EC2, Lambda, S3, DynamoDB, RDS, VPC, IAM, and CloudWatch. Generates bulk operation scripts, automates cross-service workflows, validates security configurations, and executes JMESPath queries for complex filtering. Triggers on "aws cli help", "aws command line", "aws scripting", "aws automation", "aws batch operations", "aws bulk operations", "aws cli pagination", "aws multi-region", "aws profiles", "aws cli troubleshooting".
allowed-tools: Read, Write, Bash
---

# AWS CLI Beast Mode

## Overview

Advanced AWS CLI patterns for speed, precision, and security-first automation. Covers JMESPath queries, bulk operations, waiters, cross-account access, and destructive operation safety.

## When to Use

- Bulk operations across thousands of AWS resources
- Advanced JMESPath filtering and output transformation
- Automated scripts for AWS routines
- Multi-profile and multi-region management
- Security auditing and compliance checks
- CLI-driven infrastructure-as-code workflows

## Instructions

### Step 1: Categorize the Request

| Category | Services | Commands |
|----------|----------|----------|
| Compute | EC2, Lambda | describe-instances, invoke, publish-version |
| Storage | S3 | sync, cp, mb, rb, presign |
| Database | DynamoDB, RDS | query, scan, batch-write-item |
| Networking | VPC, Route53 | describe-vpcs, describe-security-groups |
| Security | IAM | simulate-principal-policy, get-policy-version |
| Observability | CloudWatch | get-metric-statistics, filter-log-events |

### Step 2: Apply Beast Mode Principles

1. **Dry-run first**: Always validate with `--dryrun` or `--dry-run`
2. **Query server-side**: Use `--query` with JMESPath to filter before transfer
3. **Batch intelligently**: Paginate with `--max-results` and parallelize with xargs
4. **Wait properly**: Use built-in waiters or exponential backoff polling
5. **Switch contexts**: Use `--profile` and `--region` for multi-account operations

### Step 3: Validate Destructive Operations

**MANDATORY** for any destructive operation:

```bash
# S3 sync with delete - MUST dry-run first
aws s3 sync s3://source/ s3://dest/ --delete --dryrun
# Review output, then remove --dryrun only if satisfied

# Bulk EC2 stop - validate targets first
aws ec2 describe-instances \
  --filters "Name=tag:Environment,Values=development" \
  --query 'Reservations[].Instances[?State.Name==`running`].InstanceId' \
  --output text
# Confirm list, then pipe to stop command

# IAM policy attachment - simulate first
aws iam simulate-principal-policy \
  --policy-source-arn arn:aws:iam::123456789012:user/myuser \
  --action-names s3:DeleteObject \
  --resource-arns arn:aws:s3:::my-bucket/*
```

### Step 4: Reference Detailed Guides

- `compute-mastery.md` - EC2, Lambda, Spot Fleets, ASG
- `data-ops-beast.md` - S3 multipart, DynamoDB batch, RDS snapshots
- `networking-security-hardened.md` - VPC Flow Logs, IAM policies, security groups
- `automation-patterns.md` - Shell aliases, JMESPath templates, CI/CD integration

## Examples

### Example 1: Bulk EC2 Stop

**"Stop all development instances"**

```bash
# 1. Dry-run: identify targets
aws ec2 describe-instances \
  --filters "Name=tag:Environment,Values=development" \
           "Name=instance-state-name,Values=running" \
  --query 'Reservations[].Instances[].InstanceId' \
  --output text

# 2. Confirm IDs, then execute
aws ec2 describe-instances \
  --filters "Name=tag:Environment,Values=development" \
           "Name=instance-state-name,Values=running" \
  --query 'Reservations[].Instances[].InstanceId' \
  --output text | xargs aws ec2 stop-instances --instance-ids
```

### Example 2: S3 Migration with Encryption

**"Migrate data between buckets with SSE"**

```bash
# 1. Dry-run migration
aws s3 sync s3://source-bucket/ s3://dest-bucket/ \
  --sse AES256 \
  --storage-class GLACIER \
  --exclude "*.tmp" \
  --dryrun

# 2. Enable versioning on destination
aws s3api put-bucket-versioning \
  --bucket dest-bucket \
  --versioning-configuration Status=Enabled

# 3. Execute after review
aws s3 sync s3://source-bucket/ s3://dest-bucket/ \
  --sse AES256 \
  --storage-class GLACIER \
  --exclude "*.tmp"
```

### Example 3: IAM Security Audit

**"Find overprivileged IAM users"**

```bash
aws iam list-users --query 'Users[].UserName' --output text | \
while read user; do
  echo "Checking $user..."
  aws iam simulate-principal-policy \
    --policy-source-arn "arn:aws:iam::123456789012:user/$user" \
    --action-names DeleteItem,DeleteTable,DeleteFunction \
    --resource-arns "*" \
    --query 'EvaluationResults[?EvalDecision==`allowed`]'
done
```

### Example 4: Multi-Region Lambda Deployment

**"Deploy Lambda to all regions"**

```bash
for region in us-east-1 us-west-2 eu-west-1; do
  echo "Deploying to $region..."
  aws lambda update-function-code \
    --function-name my-function \
    --zip-file fileb://function.zip \
    --region $region \
    --publish
  aws lambda wait function-active \
    --function-name my-function \
    --region $region
done
```

### Example 5: JMESPath Advanced Filtering

**"Get running instances with specific tags as table"**

```bash
aws ec2 describe-instances \
  --query 'Reservations[].Instances[?State.Name==`running`].[InstanceId,Tags[?Key==`Name`].Value[0]|[0],PrivateIpAddress]' \
  --output table
```

## Best Practices

1. Use `--output json` for programmatic processing
2. Filter with JMESPath server-side before transfer
3. Implement retry logic with exponential backoff
4. Use waiters instead of manual polling loops
5. Tag all resources for cost allocation and automation
6. Separate dev/staging/prod with AWS profiles
7. Enable CloudTrail for audit compliance
8. Validate IAM policies with simulate-principal-policy before attachment
9. Use --dry-run on every state-modifying operation
10. Enable MFA for security-sensitive operations

## Constraints and Warnings

### Rate Limiting
- AWS API throttling applies; use `--max-throttle` and exponential backoff
- Check `aws service-quotas` for current limits

### Pagination
- Default page size is variable; use `--max-results` for consistency
- Use `--no-paginate` with jq for full dataset processing

### Destructive Operations
- **S3 sync --delete**: Irreversibly removes files not in source
- **EC2 terminate-instances**: Cannot be undone; validate instance IDs first
- **IAM detach/policy**: May break existing access; simulate before applying
- **RDS delete-db-instance**: Snapshots do not protect all scenarios; verify retention

### Security
- Never commit AWS credentials; use `aws configure` or environment variables
- Rotate access keys regularly with `aws iam create-access-key`
- Use least-privilege: simulate before granting permissions
