---
name: aws-cloud-ops
description: AWS cloud operations for CloudWatch, S3, Lambda, EC2, and IAM
version: 1.0.0
model: sonnet
invoked_by: both
user_invocable: true
tools: [Bash, Read]
best_practices:
  - Never hardcode credentials
  - Use IAM roles when possible
  - Verify region before operations
error_handling: graceful
streaming: supported
---

# AWS Cloud Operations Skill

## Installation

The skill invokes the AWS CLI v2. Install and configure:

- **Linux x86**: Download [AWS CLI v2](https://aws.amazon.com/cli/), unzip, then `sudo ./aws/install`
- **macOS**: `curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "AWSCLIV2.pkg"` then run the installer
- **Windows**: Download MSI from [AWS CLI v2](https://aws.amazon.com/cli/) or use `msiexec`; or install via package managers

Configure: `aws configure` (access key, secret, region). Verify: `aws --version`

## Cheat Sheet & Best Practices

**Identity & config:** `aws sts get-caller-identity` — who am I; `aws configure list-profiles` — list profiles.

**S3:** `aws s3 ls`; `aws s3 cp <local> s3://bucket/`; `aws s3 sync ./dir s3://bucket/`; `aws s3 rm s3://bucket/key`.

**Lambda:** `aws lambda list-functions`; `aws lambda invoke --function-name X output.json`; `aws lambda get-function --function-name X`.

**CloudWatch:** `aws cloudwatch list-metrics`; `aws cloudwatch get-metric-statistics`; `aws cloudwatch describe-alarms`; `put-metric-alarm` for alerts.

**EC2:** `aws ec2 describe-instances`; `start-instances`/`stop-instances`/`terminate-instances` with `--instance-ids`.

**Best practices:** Use IAM roles over long-lived keys; set `AWS_REGION`/`AWS_PROFILE`; use `--output json` and `--query` to limit response size; run destructive ops only after `describe` to confirm resources.

## Certifications & Training

**Free:** [AWS Skill Builder](https://aws.amazon.com/certification/certification-prep/) — exam prep, Cloud Quest, Cloud Essentials. **Cloud Practitioner (CLF-C02):** Cloud concepts, security/compliance, technology/services, billing (~6 months exposure). **Solutions Architect Associate:** Next step; prep on Skill Builder.

**Skill data:** Map to S3, Lambda, CloudWatch, EC2, IAM; security best practices; no hardcoded credentials.

## Hooks & Workflows

**Suggested hooks:** Pre-deploy: validate credentials (`aws sts get-caller-identity`). Cost-tracking hook: optional CloudWatch/billing checks. No mandatory hook; use when **devops** is routed for AWS tasks.

**Workflows:** Use with **devops** (contextual: `aws_project`). Flow: detect AWS project → load aws-cloud-ops → run CLI via skill script. See `operations/incident-response` if debugging AWS resources.

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

## Memory Protocol (MANDATORY)

**Before starting:**
Read `.claude/context/memory/learnings.md`

**After completing:**

- New pattern -> `.claude/context/memory/learnings.md`
- Issue found -> `.claude/context/memory/issues.md`
- Decision made -> `.claude/context/memory/decisions.md`

> ASSUME INTERRUPTION: If it's not in memory, it didn't happen.
