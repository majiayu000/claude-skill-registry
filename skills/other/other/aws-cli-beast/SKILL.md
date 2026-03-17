---
name: aws-cli-beast
description: Provides comprehensive AWS CLI mastery cloud for advanced engineers. Use for complex AWS resource management, bulk operations, automation scripts, cross-service workflows, security hardening, and high-efficiency CLI patterns across EC2, Lambda, S3, DynamoDB, RDS, VPC, IAM, Bedrock, and CloudWatch. Triggers on "aws beast mode", "optimize aws resources via cli", "bulk s3 migration cli", "audit iam policies beast", "troubleshoot vpc networking cli".
allowed-tools: Read, Write, Bash
---

# AWS CLI Beast Mode

## Overview

This skill provides comprehensive AWS CLI mastery for advanced cloud engineers who need to manage AWS resources efficiently from the command line. The "Beast Mode" approach emphasizes speed, precision, automation, and security-first patterns for handling complex cloud infrastructure tasks.

## When to Use

Use this skill when:
- Performing bulk operations across thousands of AWS resources
- Need advanced JMESPath queries for filtering and transforming CLI output
- Creating automated scripts for routine AWS operations
- Troubleshooting AWS networking, security, or compute issues
- Managing multiple AWS profiles and regions simultaneously
- Implementing infrastructure-as-code workflows via CLI
- Performing security audits and compliance checks
- Working with AWS services that require waiters and polling
- Handling AWS CLI pagination for large datasets

### Trigger Phrases

- "aws beast mode"
- "optimize aws resources via cli"
- "bulk s3 migration cli"
- "audit iam policies beast"
- "troubleshoot vpc networking cli"
- "aws cli automation"
- "lambda deployment cli beast"
- "dynamodb bulk operations"
- "ec2 fleet management cli"
- "iam policy audit cli"

## Core Services Coverage

This skill covers the following AWS services with advanced CLI patterns:

1. **Compute**: EC2 (instances, spot fleets, ASG), Lambda (deployment, invocation, layers)
2. **Storage**: S3 (sync, multipart, lifecycle, replication, presigned URLs)
3. **Database**: DynamoDB (queries, batch operations, TTL), RDS (snapshots, parameter groups)
4. **Networking**: VPC (subnets, security groups, flow logs, NAT Gateway)
5. **Security & Identity**: IAM (policies, roles, access keys, password policy)
6. **AI/ML**: Bedrock (model invocation, provisioning, custom models)
7. **Observability**: CloudWatch (logs, metrics, alarms, dashboards)

## Instructions

### Step 1: Identify the Task Type

Determine which category best matches the user's request:

| Category | Services | Common Tasks |
|----------|----------|--------------|
| Compute | EC2, Lambda | Instance management, function deployment, cold starts |
| Storage | S3 | Data migration, lifecycle policies, security audits |
| Database | DynamoDB, RDS | Query optimization, backup management, scaling |
| Networking | VPC, Route53, CloudFront | Troubleshooting, DNS management, CDN config |
| Security | IAM, Secrets Manager | Policy generation, access audits, compliance |
| AI/ML | Bedrock | Model invocation, custom model deployment |
| Observability | CloudWatch | Log analysis, metric collection, alerting |

### Step 2: Select Appropriate Reference Guide

Reference guides are available in the `references/` directory:

- `compute-mastery.md` - EC2 and Lambda advanced patterns
- `data-ops-beast.md` - S3, DynamoDB, and RDS bulk operations
- `networking-security-hardened.md` - VPC, IAM, and security auditing
- `automation-patterns.md` - Scripts, aliases, and JMESPath templates

### Step 3: Apply Beast Mode Principles

Follow these core principles for all operations:

1. **Security First**: Always use `--dry-run`, `--no-clobber`, and least-privilege checks
2. **Query Everything**: Use JMESPath to filter output server-side
3. **Handle Scale**: Use pagination, parallel operations, and batching
4. **Wait Properly**: Implement waiters for async resource provisioning
5. **Profile Switching**: Leverage AWS profiles for multi-account management

### Step 4: Validate and Verify

Always verify operations:
- Use `--dry-run` before making changes
- Confirm resource state with describe commands
- Check CloudTrail for audit compliance
- Validate IAM policies with `iam-simulate-principal-policy`

## Beast Mode Features

### Advanced Querying with JMESPath

Use `--query` flag to transform and filter AWS CLI output:

```bash
# Get instance IDs and private IPs in one command
aws ec2 describe-instances \
  --query 'Reservations[*].Instances[*].[InstanceId,PrivateIpAddress,State.Name]' \
  --output table

# Filter by tag and get only running instances
aws ec2 describe-instances \
  --filters "Name=tag:Environment,Values=production" \
  --query 'Reservations[].Instances[?State.Name==`running`].[InstanceId,Tags[?Key==`Name`].Value[0]]' \
  --output json

# Aggregate costs by service
aws ce get-cost-and-usage \
  --time-period Start=2024-01-01,End=2024-01-31 \
  --granularity DAILY \
  --metrics UnblendedCost \
  --group-by Type=DIMENSION,Key=SERVICE \
  --query 'ResultsByTime[*].Groups[*].[Keys[0],Metrics.UnblendedCost.Amount]' \
  --output table
```

### Bulk Operations

Handle thousands of resources efficiently:

```bash
# Stop all EC2 instances in a specific tag
aws ec2 describe-instances \
  --filters "Name=tag:Environment,Values=development" \
  --query 'Reservations[].Instances[].InstanceId' \
  --output text | xargs aws ec2 stop-instances --instance-ids

# Delete old CloudWatch log streams
aws logs describe-log-streams \
  --log-group-name /aws/lambda/my-function \
  --query 'logStreams[?lastIngestionTime<`${cutoff_timestamp}`].logStreamName' \
  --output text | xargs -r aws logs delete-log-stream --log-group-name /aws/lambda/my-function --log-stream-name

# Parallel S3 sync with GNU Parallel
cat instance_ids.txt | parallel -j 10 "aws ssm start-session --target {}"
```

### Waiters and Polling

Properly handle asynchronous resource provisioning:

```bash
# Wait for EC2 instance to be running
aws ec2 wait instance-running --instance-ids i-1234567890abcdef0

# Wait for Lambda function to be active
aws lambda wait function-active --function-name my-function

# Wait for RDS instance to be available
aws rds wait db-instance-available --db-instance-identifier my-db

# Custom polling with exponential backoff
aws ec2 describe-instance-status \
  --instance-ids i-1234567890abcdef0 \
  --query 'InstanceStatuses[0].InstanceState.Name' \
  --output text && break || sleep $((i++ * 2))
```

### Security-First Patterns

Always apply security best practices:

```bash
# Dry run before any destructive operation
aws s3 rm s3://my-bucket/important/ --dryrun

# Validate IAM policy before attaching
aws iam simulate-principal-policy \
  --policy-source-arn arn:aws:iam::123456789012:user/myuser \
  --action-names s3:GetObject \
  --resource-arns arn:aws:s3:::my-bucket/*

# Use least-privilege: check before granting
aws iam get-policy-version \
  --policy-arn arn:aws:iam::aws:policy/ReadOnlyAccess \
  --version-id v1

# Enable MFA for sensitive operations
aws iam list-mfa-devices --user-name myuser
```

### Profile and Region Management

Seamlessly switch between AWS accounts and regions:

```bash
# List all available profiles
aws configure list-profiles

# Use specific profile
aws --profile production ec2 describe-instances

# Multi-region query
for region in us-east-1 us-west-2 eu-west-1; do
  aws --region $region ec2 describe-vpcs --query 'Vpcs[].VpcId'
done

# Assume role for cross-account access
aws sts assume-role \
  --role-arn arn:aws:iam::123456789012:role/AdminRole \
  --role-session-name admin-session
```

### Infrastructure as Code (CLI-driven)

Generate and deploy CloudFormation/SAM templates:

```bash
# Validate CloudFormation template
aws cloudformation validate-template \
  --template-body file://template.yaml

# Deploy stack with parameters
aws cloudformation deploy \
  --template-file template.yaml \
  --stack-name my-stack \
  --parameter-overrides ParameterKey=Env,ParameterValue=production \
  --capabilities CAPABILITY_IAM

# Package and deploy Lambda
aws cloudformation package \
  --template-file template.yaml \
  --s3-bucket my-bucket \
  --output-template-file packaged.yaml

# Generate SAM deployment config
sam build --use-container
sam deploy --guided
```

## Common Power Commands

### EC2 Management

```bash
# Get instance metadata
aws ec2 describe-instance-attribute --instance-id i-1234567890abcdef0 --attribute instanceType

# Modify instance type (stop first required)
aws ec2 modify-instance-attribute --instance-id i-1234567890abcdef0 --instance-type "{\"Value\": \"t3.large\"}"

# Create AMI from instance
aws ec2 create-image --instance-id i-1234567890abcdef0 --name "my-ami-$(date +%Y%m%d)" --no-reboot

# Manage Spot requests
aws ec2 describe-spot-instance-requests --filters "Name=status,Values=active"
```

### S3 Operations

```bash
# Sync with delete (be careful!)
aws s3 sync s3://source-bucket/ s3://dest-bucket/ --delete

# Multipart upload for large files
aws s3 cp large-file.tar.gz s3://my-bucket/ --storage-class STANDARD_IA

# Generate presigned URL with custom expiry
aws s3 presign s3://my-bucket/file.txt --expires-in 3600

# Configure bucket policy
aws s3api put-bucket-policy --bucket my-bucket --policy file://policy.json
```

### Lambda Operations

```bash
# Invoke with payload
aws lambda invoke \
  --function-name my-function \
  --payload '{"key": "value"}' \
  response.json

# Update function configuration
aws lambda update-function-configuration \
  --function-name my-function \
  --memory-size 512 \
  --timeout 300

# Publish new version
aws lambda publish-version --function-name my-function

# Layer management
aws lambda get-layer-version --layer-name my-layer --version-number 1
```

### DynamoDB Operations

```bash
# Query with complex key condition
aws dynamodb query \
  --table-name my-table \
  --key-condition-expression "PK = :pk AND SK BETWEEN :start AND :end" \
  --expression-attribute-values '{"=":{"S":"USER#123"},":start":{"S":"ORDER#0001"},":end":{"S":"ORDER#9999"}}'

# Batch write (up to 25 items)
aws dynamodb batch-write-item \
  --request-items file://items.json

# Enable TTL
aws dynamodb update-time-to-live \
  --table-name my-table \
  --time-to-live-specification "Enabled=true, AttributeName=expiresAt"
```

## Error Handling and Rate Limiting

### Retry Patterns

```bash
# Simple retry with backoff
for i in 1 2 3 4 5; do
  aws ec2 describe-instances && break
  sleep $((i ** 2))
done

# Use --cli-read-timeout and --cli-connect-timeout
aws --cli-read-timeout 60 --cli-connect-timeout 30 ec2 describe-instances
```

### Pagination

```bash
# Automatic pagination (default)
aws ec2 describe-instances --max-results 100

# Manual pagination
aws ec2 describe-instances --page-size 100

# Process all pages with jq
aws ec2 describe-instances | jq -r '.Reservations[].Instances[] | .InstanceId'
```

## Examples

### Example 1: Bulk EC2 Management

**User:** "Stop all development EC2 instances"

**Claude:**
```bash
aws ec2 describe-instances \
  --filters "Name=tag:Environment,Values=development" "Name=instance-state-name,Values=running" \
  --query "Reservations[].Instances[].InstanceId" \
  --output text | xargs aws ec2 stop-instances --instance-ids
```

### Example 2: Advanced S3 Migration

**User:** "Migrate all data between S3 buckets with encryption"

**Claude:**
```bash
# Enable versioning on destination
aws s3api put-bucket-versioning --bucket dest-bucket --versioning-configuration Status=Enabled

# Sync with encryption and lifecycle
aws s3 sync s3://source-bucket/ s3://dest-bucket/ \
  --sse AES256 \
  --storage-class GLACIER \
  --exclude "*.tmp"
```

### Example 3: IAM Security Audit

**User:** "Audit IAM policies for security issues"

**Claude:**
```bash
# List all IAM policies and simulate actions
aws iam list-policies --scope Local --query "Policies[].Arn" --output text | \
while read policy; do
  aws iam get-policy-version --policy-arn $policy --version-id v1 | \
    jq '.PolicyVersion.Document.Statement[] | select(.Effect=="Allow")'
done
```

### Example 4: Multi-Region Lambda Deployment

**User:** "Deploy Lambda function to all regions"

**Claude:**
```bash
for region in us-east-1 us-west-2 eu-west-1; do
  echo "Deploying to $region..."
  aws lambda update-function-code \
    --function-name my-function \
    --zip-file fileb://function.zip \
    --region $region \
    --publish
done
```

### Example 5: DynamoDB Bulk Operations

**User:** "Export DynamoDB table to JSON"

**Claude:**
```bash
aws dynamodb scan \
  --table-name my-table \
  --output json \
  --no-paginate | jq -c '.Items[]' > output.jsonl
```

## Best Practices

1. **Always use `--output json`** for programmatically processable output
2. **Use JMESPath** to filter data server-side, reducing bandwidth
3. **Implement proper error handling** with exit codes and retry logic
4. **Use waiters** instead of manual polling for resource state changes
5. **Enable CloudTrail** for audit compliance on all operations
6. **Use least-privilege IAM policies** with `iam-simulate-principal-policy`
7. **Tag all resources** for cost allocation and automation
8. **Use `--dry-run`** for any operation that modifies state
9. **Enable MFA** for operations that modify security settings
10. **Use profiles** for separating development, staging, and production

## Constraints and Warnings

### Critical Constraints

- **Rate Limiting**: AWS API limits apply; implement exponential backoff
- **Pagination**: Default page size is variable; use `--max-results` for consistency
- **Eventual Consistency**: Some operations take time to propagate
- **Cost**: Some CLI operations (like Describe* on large accounts) can be expensive

### Common Pitfalls

- Forgetting `--recursive` for S3 directory operations
- Not waiting for instance state changes before proceeding
- Using `rm` instead of `rb` for S3 bucket deletion
- Ignoring IAM policy simulation results
- Not specifying `--region` when operating cross-region
