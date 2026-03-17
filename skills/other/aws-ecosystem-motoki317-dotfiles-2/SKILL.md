---
name: AWS Ecosystem
description: This skill should be used when the user asks to "aws cli", "aws configure", "aws sso", "aws sts", "terraform aws", or works with AWS CLI and Terraform AWS Provider patterns. Provides comprehensive AWS ecosystem patterns and best practices.
---

# AWS Ecosystem

Patterns for AWS CLI configuration, authentication, and Terraform AWS Provider infrastructure as code.

## CLI Configuration

### Config Files
```ini
# ~/.aws/config
[default]
region = ap-northeast-1
output = json

[profile dev]
region = ap-northeast-1

# ~/.aws/credentials (prefer SSO over storing credentials)
[default]
aws_access_key_id = AKIA...
aws_secret_access_key = ...
```

### Environment Variables
- `AWS_PROFILE` - active profile
- `AWS_REGION` / `AWS_DEFAULT_REGION` - region
- `AWS_SESSION_TOKEN` - temporary credentials

### Profile Switching
```bash
export AWS_PROFILE=dev
# or inline
aws s3 ls --profile prod
```

## Authentication

### SSO (Recommended for Humans)
```ini
[profile sso-dev]
sso_session = my-sso
sso_account_id = 123456789012
sso_role_name = DeveloperAccess
region = ap-northeast-1

[sso-session my-sso]
sso_start_url = https://example.awsapps.com/start
sso_region = ap-northeast-1
```
```bash
aws sso login --sso-session my-sso
```

### Assume Role
```ini
[profile cross-account]
role_arn = arn:aws:iam::987654321098:role/CrossAccountRole
source_profile = default
```

### OIDC Federation (CI/CD Best Practice)
```yaml
# .github/workflows/deploy.yml
permissions:
  id-token: write
  contents: read
steps:
  - uses: aws-actions/configure-aws-credentials@v4
    with:
      role-to-assume: arn:aws:iam::123456789012:role/GitHubActionsRole
      aws-region: ap-northeast-1
```

### Verify Identity
```bash
aws sts get-caller-identity
```

## Common Commands

### S3
```bash
aws s3 ls s3://bucket/prefix/
aws s3 cp file.txt s3://bucket/
aws s3 sync ./local s3://bucket/prefix/
aws s3 presign s3://bucket/key --expires-in 3600
```

### EC2
```bash
aws ec2 describe-instances
aws ec2 start-instances --instance-ids i-123...
aws ec2 stop-instances --instance-ids i-123...
```

### Query Filtering
```bash
# Single value
aws ec2 describe-instances --query 'Reservations[0].Instances[0].InstanceId' --output text

# Filtered list
aws ec2 describe-instances --query 'Reservations[].Instances[?State.Name==`running`].InstanceId'
```

## Terraform Provider

### Basic Configuration
```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "ap-northeast-1"

  default_tags {
    tags = {
      Environment = "dev"
      ManagedBy   = "terraform"
    }
  }
}
```

### S3 Backend with Locking
```hcl
terraform {
  backend "s3" {
    bucket         = "my-terraform-state"
    key            = "env/dev/terraform.tfstate"
    region         = "ap-northeast-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}
```

### Common Resources

**IAM Role:**
```hcl
resource "aws_iam_role" "lambda" {
  name = "lambda-execution-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = { Service = "lambda.amazonaws.com" }
    }]
  })
}
```

**S3 Bucket:**
```hcl
resource "aws_s3_bucket" "main" {
  bucket = "my-bucket"
}

resource "aws_s3_bucket_public_access_block" "main" {
  bucket                  = aws_s3_bucket.main.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
```

**OIDC for GitHub Actions:**
```hcl
resource "aws_iam_openid_connect_provider" "github" {
  url             = "https://token.actions.githubusercontent.com"
  client_id_list  = ["sts.amazonaws.com"]
  thumbprint_list = ["ffffffffffffffffffffffffffffffffffffffff"]
}
```

### Terraform Commands
```bash
terraform init
terraform plan -out=tfplan
terraform apply tfplan
terraform fmt -recursive
terraform validate
```

## Best Practices

**Critical:**
- Eliminate long-term access keys; use SSO or IAM roles
- Use OIDC federation for CI/CD
- Instance Profiles for EC2, Execution Roles for Lambda

**High:**
- Enable MFA for all human users
- Follow least privilege; avoid wildcard permissions
- Enable CloudTrail for CLI activity monitoring

**Terraform:**
- Remote state with S3 + DynamoDB locking
- Enable state encryption
- Pin provider versions
- Use default_tags for consistent tagging

## Anti-Patterns

| Avoid | Instead |
|-------|---------|
| Hardcoded credentials | IAM roles, SSO, credential_process |
| Long-term access keys | Temporary credentials via SSO/AssumeRole |
| Root account for CLI | IAM users or SSO |
| Wildcard permissions | Least privilege with specific resources |
| State without locking | DynamoDB table for S3 backend |

## Constraints

**Must:**
- Use Terraform for infrastructure management
- Follow least-privilege IAM principles
- Enable encryption at rest and in transit

**Avoid:**
- Hardcoding credentials
- Overly permissive security groups
- Untagged resources

## Context7 Reference

Library ID: `/hashicorp/terraform-provider-aws`
