---
name: opentofu-ecr-provision
description: Provision AWS Elastic Container Registry (ECR) repositories with GitHub OIDC integration following BETEKK standards
license: Apache-2.0
compatibility: opencode
metadata:
  audience: developers
  workflow: infrastructure-as-code
---

# OpenTofu ECR Provisioning

## What I do

I guide you through provisioning AWS Elastic Container Registry (ECR) repositories following BETEKK infrastructure standards:

- **ECR Repository Creation**: Create ECR repositories with proper configuration and lifecycle policies
- **GitHub OIDC Integration**: Setup IAM roles for GitHub Actions to push/pull images
- **State Management**: Configure S3 backend for Terraform state management
- **IAM Role Patterns**: Implement standardized IAM roles with OIDC trust relationships
- **Variable Naming**: Follow BETEKK naming conventions for consistency
- **Modular Structure**: Use reusable modules for ECR and IAM resources
- **Best Practices**: Apply AWS Well-Architected Framework principles

## When to use me

Use this skill when you need to:
- Provision a new ECR repository for Docker container images
- Setup GitHub Actions CI/CD for ECR integration
- Create standardized AWS infrastructure following BETEKK patterns
- Implement OIDC authentication for GitHub Actions
- Migrate existing ECR repositories to BETEKK standards
- Create reusable ECR infrastructure templates

**Reference Implementation**: `ecr/betekk_probe_engine_main/`

## Prerequisites

- **OpenTofu CLI installed**: Install from https://opentofu.org/docs/intro/install/
- **AWS Account**: Valid AWS account with appropriate permissions
- **AWS Credentials**: Access keys or IAM role for authentication
- **GitHub OIDC Provider**: OIDC provider configured for GitHub Actions (optional, can be created as part of workflow)
- **Basic OpenTofu/Terraform Knowledge**: Understanding of HCL syntax and provider concepts

## BETEKK Standards

### Variable Naming Convention

Follow these naming patterns for consistency:

```hcl
variable "environment" {
  description = "Environment type (e.g., dev, prod, uat)"
  type        = string
  default     = ""
}

variable "project_prefix" {
  description = "Project Prefix"
  type        = string
  default     = "betekk"
}

variable "repo_name" {
  description = "ECR Repository Name Prefix"
  type        = string
  default     = "betekk-<service-name>"
}

variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "ap-southeast-1"
}

variable "state_management_bucket_name" {
  description = "State Management Bucket Name"
  type        = string
  default     = "betekk-state-management-bucket"
}

variable "github_organization_old" {
  description = "Github Organization Name (old) for migration support"
  type        = string
  default     = "nus-cee"
}

variable "github_organization_new" {
  description = "Github Organization Name (new)"
  type        = string
  default     = "betekk"
}
```

### Folder Structure

Standard directory structure for ECR provisioning:

```
<service-name>/
├── modules/
│   ├── ecr/
│   │   ├── main.tf          # ECR repository resource
│   │   └── variables.tf    # ECR module variables
│   └── iam-role-assume/
│       ├── main.tf          # IAM assume role policy
│       └── variables.tf    # IAM module variables
├── .gitignore
├── .terraform.lock.hcl
├── README.md
├── data.tf                # Data sources (caller identity, etc.)
├── iam_policies.tf        # IAM policy definitions
├── iam_policy_attachments.tf
├── iam_roles.tf          # IAM role resources
├── main.tf               # Root module with module calls
├── outputs.tf            # Output values
├── providers.tf          # AWS provider configuration
├── terraform.tf         # Terraform configuration
└── variables.tf         # Input variables
```

### IAM Role Naming Patterns

```hcl
# ECR Upload Role
resource "aws_iam_role" "ecr_<project_prefix>_github_workflows_upload_role" {
  name = "${upper(var.project_prefix)}-GithubWorkflowsUploadRole"
  # ...
}

# Lambda Deploy Role
resource "aws_iam_role" "betekk_lambda_github_workflows_deploy_role" {
  name = "${upper(var.project_prefix)}-GithubWorkflowsLambdaDeployRole"
  # ...
}
```

## Steps

### Step 1: Initialize Project

Create project directory and initialize Terraform:

```bash
# Create project directory
mkdir -p <service-name>/modules/ecr
mkdir -p <service-name>/modules/iam-role-assume
cd <service-name>

# Initialize Terraform
tofu init
```

### Step 2: Configure Terraform

Create `terraform.tf`:

```hcl
terraform {
  required_version = "~> 1.8"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    bucket = var.state_management_bucket_name
    key    = "ecr/<service-name>/terraform.tfstate"
    region = var.aws_region
  }
}
```

### Step 3: Configure AWS Provider

Create `providers.tf`:

```hcl
provider "aws" {
  region = var.aws_region
}
```

### Step 4: Define Variables

Create `variables.tf`:

```hcl
variable "environment" {
  description = "Environment type (e.g., dev, prod, uat)"
  type        = string
  default     = ""
}

variable "project_prefix" {
  description = "Project Prefix"
  type        = string
  default     = "betekk"
}

variable "repo_name" {
  description = "ECR Repository Name Prefix"
  type        = string
  default     = "betekk-<service-name>"
}

variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "ap-southeast-1"
}

variable "state_management_bucket_name" {
  description = "State Management Bucket Name"
  type        = string
  default     = "betekk-state-management-bucket"
}

variable "github_organization_old" {
  description = "Github Organization Name (old)"
  type        = string
  default     = "nus-cee"
}

variable "github_organization_new" {
  description = "Github Organization Name (new)"
  type        = string
  default     = "betekk"
}
```

### Step 5: Create Data Sources

Create `data.tf`:

```hcl
data "aws_caller_identity" "current" {}
```

### Step 6: Create ECR Module

Create `modules/ecr/main.tf`:

```hcl
# Create an ECR repository where Docker images will be stored
# The repository URL will be used by:
# 1. Docker push commands to upload images
# 2. Kubernetes/Helm to pull images during deployment
resource "aws_ecr_repository" "repository" {
  name         = var.repository_name
  force_delete = false
}

# Output ECR repository URL for use in other parts of infrastructure
output "repository_url" {
  description = "ECR repository URL"
  value       = aws_ecr_repository.repository.repository_url
}

output "repository_arn" {
  description = "ECR repository ARN"
  value       = aws_ecr_repository.repository.arn
}
```

Create `modules/ecr/variables.tf`:

```hcl
variable "repository_name" {
  type        = string
  description = "ECR repository name"
}
```

### Step 7: Create IAM Assume Role Module

Create `modules/iam-role-assume/main.tf`:

```hcl
# Trust relationship is assumed to be set on role already.
# Attach policy to allow user to assume role
resource "aws_iam_policy" "assume_role_policy" {
  name        = "${var.project_prefix}_AssumeRolePolicy"
  description = "Policy allowing assume role access to a specific role"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect   = "Allow",
        Action   = "sts:AssumeRole",
        Resource = var.assume_role_arn
      }
    ]
  })
}

resource "aws_iam_policy_attachment" "assume_role_policy_attachment" {
  name       = "${var.project_prefix}-AssumeRoleAttachment"
  policy_arn = aws_iam_policy.assume_role_policy.arn
  users      = [var.user_arn]
}
```

Create `modules/iam-role-assume/variables.tf`:

```hcl
variable "project_prefix" {
  type        = string
  description = "Project prefix for naming"
}

variable "assume_role_arn" {
  type        = string
  description = "ARN of role to assume"
}

variable "user_arn" {
  type        = string
  description = "ARN of user to attach policy"
}
```

### Step 8: Create IAM Roles

Create `iam_roles.tf`:

```hcl
# Create IAM Role for GitHub ECR Upload
resource "aws_iam_role" "ecr_betekk_probe_engine_github_workflows_upload_role" {
  name = "${upper(var.project_prefix)}-GithubWorkflowsUploadRole"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          "Federated" = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:oidc-provider/token.actions.githubusercontent.com"
        }
        Action = "sts:AssumeRoleWithWebIdentity"
        Condition = {
          StringLike = {
            "token.actions.githubusercontent.com:aud" : "sts.amazonaws.com",
            "token.actions.githubusercontent.com:sub" : [
              "repo:${var.github_organization_old}/<repo-name>:*",
              "repo:${var.github_organization_new}/<repo-name>:*"
            ],
          }
        }
      }
    ]
  })
}

# Create IAM Role for Lambda Deployment
resource "aws_iam_role" "betekk_lambda_github_workflows_deploy_role" {
  name = "${upper(var.project_prefix)}-GithubWorkflowsLambdaDeployRole"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          "Federated" = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:oidc-provider/token.actions.githubusercontent.com"
        }
        Action = "sts:AssumeRoleWithWebIdentity"
        Condition = {
          StringLike = {
            "token.actions.githubusercontent.com:aud" : "sts.amazonaws.com",
            "token.actions.githubusercontent.com:sub" : [
              "repo:${var.github_organization_old}/<repo-name>:*",
              "repo:${var.github_organization_new}/<repo-name>:*"
            ]
          }
        }
      }
    ]
  })
}
```

### Step 9: Create IAM Policies

Create `iam_policies.tf`:

```hcl
# Policy for ECR Upload
resource "aws_iam_policy" "ecr_upload_policy" {
  name        = "${var.project_prefix}-ECRUploadPolicy"
  description = "Policy allowing ECR operations"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "ecr:GetDownloadUrlForLayer",
          "ecr:BatchGetImage",
          "ecr:BatchCheckLayerAvailability",
          "ecr:PutImage",
          "ecr:InitiateLayerUpload",
          "ecr:UploadLayerPart",
          "ecr:CompleteLayerUpload",
          "ecr:DescribeRepositories",
          "ecr:GetRepositoryPolicy",
          "ecr:ListImages",
          "ecr:DeleteRepository",
          "ecr:BatchDeleteImage",
          "ecr:SetRepositoryPolicy",
          "ecr:DeleteRepositoryPolicy"
        ]
        Resource = "*"
      }
    ]
  })
}

# Policy for Lambda Deployment
resource "aws_iam_policy" "lambda_deploy_policy" {
  name        = "${var.project_prefix}-LambdaDeployPolicy"
  description = "Policy allowing Lambda operations"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "lambda:CreateFunction",
          "lambda:UpdateFunctionCode",
          "lambda:UpdateFunctionConfiguration",
          "lambda:GetFunction",
          "lambda:DeleteFunction"
        ]
        Resource = "*"
      }
    ]
  })
}
```

### Step 10: Attach Policies

Create `iam_policy_attachments.tf`:

```hcl
# Attach ECR policy to upload role
resource "aws_iam_role_policy_attachment" "ecr_upload_attachment" {
  role       = aws_iam_role.ecr_betekk_probe_engine_github_workflows_upload_role.name
  policy_arn = aws_iam_policy.ecr_upload_policy.arn
}

# Attach Lambda policy to deploy role
resource "aws_iam_role_policy_attachment" "lambda_deploy_attachment" {
  role       = aws_iam_role.betekk_lambda_github_workflows_deploy_role.name
  policy_arn = aws_iam_policy.lambda_deploy_policy.arn
}
```

### Step 11: Create Root Module

Create `main.tf`:

```hcl
data "aws_caller_identity" "current" {}

module "ecr_betekk_<service-name>" {
  source          = "./modules/ecr"
  repository_name = var.repo_name
}
```

### Step 12: Create Outputs

Create `outputs.tf`:

```hcl
output "ecr_repository_url" {
  description = "ECR repository URL"
  value       = module.ecr_betekk_<service-name>.repository_url
}

output "ecr_repository_arn" {
  description = "ECR repository ARN"
  value       = module.ecr_betekk_<service-name>.repository_arn
}

output "ecr_upload_role_arn" {
  description = "ARN of ECR upload role"
  value       = aws_iam_role.ecr_betekk_probe_engine_github_workflows_upload_role.arn
}

output "lambda_deploy_role_arn" {
  description = "ARN of Lambda deploy role"
  value       = aws_iam_role.betekk_lambda_github_workflows_deploy_role.arn
}
```

### Step 13: Initialize and Apply

```bash
# Initialize Terraform
tofu init

# Plan changes
tofu plan -out=tfplan

# Apply changes
tofu apply tfplan

# Show outputs
tofu output
```

## Best Practices

### Security

1. **Least Privilege**: Grant minimal permissions in IAM roles and policies
2. **OIDC Authentication**: Use GitHub OIDC instead of long-lived credentials
3. **Repository Scanning**: Enable ECR image scanning for security vulnerabilities
4. **Encryption**: Enable ECR encryption at rest (enabled by default)
5. **Tagging**: Use consistent tags for all resources

### High Availability

1. **Multi-Region**: Deploy repositories to multiple regions if needed
2. **Cross-Account**: Use cross-account access patterns for multi-account deployments
3. **Image Replication**: Consider ECR replication for disaster recovery

### Cost Optimization

1. **Lifecycle Policies**: Implement ECR lifecycle policies to clean up old images
2. **Image Tagging**: Use consistent image tagging for easy cleanup
3. **Monitoring**: Monitor repository size and image count

### State Management

1. **Remote State**: Use S3 backend for state management
2. **State Locking**: Enable DynamoDB table for state locking (optional)
3. **State Encryption**: Encrypt state files
4. **State Versioning**: Enable versioning on state bucket

## Common Issues

### Issue: Repository Already Exists

**Symptom**: Error `Error: ... already exists`

**Solution**:
```bash
# Import existing repository
tofu import aws_ecr_repository.repository <repository-name>
```

### Issue: OIDC Provider Not Found

**Symptom**: Error `Error: OIDC provider does not exist`

**Solution**:
```bash
# Create OIDC provider
aws iam create-open-id-connect-provider \
  --url https://token.actions.githubusercontent.com \
  --client-id-list sts.amazonaws.com
```

### Issue: Authentication Failed

**Symptom**: Error `Error: error configuring Terraform AWS Provider`

**Solution**:
```bash
# Verify credentials
aws sts get-caller-identity

# Check environment variables
echo $AWS_ACCESS_KEY_ID
echo $AWS_SECRET_ACCESS_KEY
echo $AWS_DEFAULT_REGION
```

### Issue: State Lock Error

**Symptom**: Error `Error: Error acquiring the state lock`

**Solution**:
```bash
# Check who has the lock
tofu state pull

# Force unlock (caution!)
tofu force-unlock <LOCK_ID>

# Or wait for other operation to complete
```

## Examples

### Complete ECR Repository Setup

```hcl
# modules/ecr/main.tf
resource "aws_ecr_repository" "repository" {
  name                 = var.repository_name
  image_tag_mutability = "IMMUTABLE"

  encryption_configuration {
    encryption_type = "AES256"
  }

  image_scanning_configuration {
    scan_on_push = true
  }
}
```

### ECR Lifecycle Policy

```hcl
resource "aws_ecr_lifecycle_policy" "main" {
  repository = aws_ecr_repository.repository.name

  policy = jsonencode({
    rules = [
      {
        rulePriority = 1
        description  = "Keep last 50 images and remove older ones"
        selection   = {
          tagStatus     = "tagged"
          tagPrefixList = ["v"]
          countType     = "imageCountMoreThan"
          countNumber   = 50
        }
        action = {
          type = "expire"
        }
      }
    ]
  })
}
```

### GitHub Actions Workflow Example

```yaml
name: Build and Push to ECR

on:
  push:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      id-token: write
      contents: read

    steps:
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          role-to-assume: arn:aws:iam::123456789012:role/BETEKK-GithubWorkflowsUploadRole
          aws-region: ap-southeast-1

      - name: Login to Amazon ECR
        uses: aws-actions/amazon-ecr-login@v1

      - name: Build and push Docker image
        run: |
          docker build -t <repository-url>:latest .
          docker push <repository-url>:latest
```

## Reference Documentation

- **AWS ECR Documentation**: https://docs.aws.amazon.com/AmazonECR/
- **Terraform AWS Provider (ECR)**: https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/ecr_repository
- **GitHub OIDC**: https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/configuring-openid-connect-in-amazon-web-services
- **OpenTofu Documentation**: https://opentofu.org/docs/
- **BETEKK Reference**: ecr/betekk_probe_engine_main/

## Related Skills

- **opentofu-aws-explorer**: For managing other AWS resources
- **opentofu-provider-setup**: For configuring AWS authentication and backends
- **opentofu-provisioning-workflow**: For general infrastructure provisioning patterns
