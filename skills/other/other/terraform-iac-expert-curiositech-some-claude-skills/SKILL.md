---
name: terraform-iac-expert
description: Expert in Infrastructure as Code using Terraform and OpenTofu. Specializes in module design, state management, multi-cloud deployments, and CI/CD integration. Handles complex infrastructure patterns including multi-environment setups, remote state backends, and secure secrets management.
version: 1.0.0
category: devops
tags: [terraform, iac, infrastructure, aws, gcp, azure, opentofu]
---

# Terraform IaC Expert

## Overview

Expert in Infrastructure as Code using Terraform and OpenTofu. Specializes in module design, state management, multi-cloud deployments, and CI/CD integration. Handles complex infrastructure patterns including multi-environment setups, remote state backends, and secure secrets management.

## When to Use

- Setting up new Terraform projects and workspaces
- Designing reusable Terraform modules
- Managing state files and remote backends
- Implementing multi-environment (dev/staging/prod) infrastructure
- Migrating existing infrastructure to Terraform
- Troubleshooting state drift and plan failures
- Integrating Terraform with CI/CD pipelines
- Implementing security best practices (secrets, IAM, policies)

## Capabilities

### Project Structure
- Module-based architecture design
- Workspace vs directory structure strategies
- Variable and output organization
- Provider configuration and version constraints
- Backend configuration for remote state

### Module Development
- Reusable module patterns
- Input validation and type constraints
- Output design for module composition
- Local modules vs registry modules
- Module versioning and publishing

### State Management
- Remote state backends (S3, GCS, Azure Blob, Terraform Cloud)
- State locking mechanisms
- State migration and manipulation
- Import existing resources
- Handling state drift

### Multi-Environment Patterns
- Workspace-based environments
- Directory-based environments
- Terragrunt for DRY infrastructure
- Environment-specific variables
- Promotion workflows

### Security
- Sensitive variable handling
- IAM role design for Terraform
- Policy as Code (Sentinel, OPA)
- Secrets management integration (Vault, AWS Secrets Manager)
- Least privilege principles

### CI/CD Integration
- GitHub Actions for Terraform
- Atlantis for PR-based workflows
- Terraform Cloud/Enterprise
- Plan/Apply automation
- Cost estimation integration

## Dependencies

Works well with:
- `aws-solutions-architect` - AWS resource patterns
- `kubernetes-orchestrator` - K8s infrastructure
- `github-actions-pipeline-builder` - CI/CD automation
- `site-reliability-engineer` - Production infrastructure

## Examples

### Project Structure
```
terraform/
├── modules/
│   ├── vpc/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   ├── eks/
│   └── rds/
├── environments/
│   ├── dev/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── terraform.tfvars
│   │   └── backend.tf
│   ├── staging/
│   └── prod/
└── shared/
    └── provider.tf
```

### Root Module with Locals
```hcl
# environments/prod/main.tf
terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    bucket         = "mycompany-terraform-state"
    key            = "prod/terraform.tfstate"
    region         = "us-west-2"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}

locals {
  environment = "prod"
  project     = "myapp"

  common_tags = {
    Environment = local.environment
    Project     = local.project
    ManagedBy   = "terraform"
  }
}

module "vpc" {
  source = "../../modules/vpc"

  environment = local.environment
  cidr_block  = "10.0.0.0/16"
  tags        = local.common_tags
}

module "eks" {
  source = "../../modules/eks"

  environment       = local.environment
  vpc_id            = module.vpc.vpc_id
  private_subnet_ids = module.vpc.private_subnet_ids
  cluster_version   = "1.29"
  tags              = local.common_tags
}
```

### Reusable Module with Validation
```hcl
# modules/vpc/variables.tf
variable "environment" {
  type        = string
  description = "Environment name (dev, staging, prod)"

  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}

variable "cidr_block" {
  type        = string
  description = "VPC CIDR block"

  validation {
    condition     = can(cidrhost(var.cidr_block, 0))
    error_message = "Must be a valid CIDR block."
  }
}

variable "availability_zones" {
  type        = list(string)
  description = "List of AZs to use"
  default     = ["us-west-2a", "us-west-2b", "us-west-2c"]
}

variable "enable_nat_gateway" {
  type        = bool
  description = "Enable NAT Gateway for private subnets"
  default     = true
}

variable "tags" {
  type        = map(string)
  description = "Tags to apply to all resources"
  default     = {}
}
```

### Module with Dynamic Blocks
```hcl
# modules/security-group/main.tf
resource "aws_security_group" "this" {
  name        = var.name
  description = var.description
  vpc_id      = var.vpc_id

  dynamic "ingress" {
    for_each = var.ingress_rules
    content {
      from_port   = ingress.value.from_port
      to_port     = ingress.value.to_port
      protocol    = ingress.value.protocol
      cidr_blocks = ingress.value.cidr_blocks
      description = ingress.value.description
    }
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(var.tags, {
    Name = var.name
  })
}
```

### Remote State Data Source
```hcl
# Reference another environment's state
data "terraform_remote_state" "shared" {
  backend = "s3"

  config = {
    bucket = "mycompany-terraform-state"
    key    = "shared/terraform.tfstate"
    region = "us-west-2"
  }
}

# Use outputs from shared state
resource "aws_instance" "app" {
  ami           = data.terraform_remote_state.shared.outputs.base_ami_id
  instance_type = "t3.medium"
  subnet_id     = data.terraform_remote_state.shared.outputs.private_subnet_id
}
```

### GitHub Actions CI/CD
```yaml
# .github/workflows/terraform.yml
name: Terraform

on:
  pull_request:
    paths:
      - 'terraform/**'
  push:
    branches: [main]
    paths:
      - 'terraform/**'

env:
  TF_VERSION: 1.6.0
  AWS_REGION: us-west-2

jobs:
  plan:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pull-requests: write
      id-token: write  # For OIDC

    steps:
      - uses: actions/checkout@v4

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::123456789:role/terraform-github-actions
          aws-region: ${{ env.AWS_REGION }}

      - uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: ${{ env.TF_VERSION }}

      - name: Terraform Init
        working-directory: terraform/environments/prod
        run: terraform init

      - name: Terraform Plan
        working-directory: terraform/environments/prod
        run: terraform plan -out=tfplan

      - name: Upload Plan
        uses: actions/upload-artifact@v4
        with:
          name: tfplan
          path: terraform/environments/prod/tfplan

  apply:
    needs: plan
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    environment: production

    steps:
      - uses: actions/checkout@v4

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::123456789:role/terraform-github-actions
          aws-region: ${{ env.AWS_REGION }}

      - uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: ${{ env.TF_VERSION }}

      - name: Download Plan
        uses: actions/download-artifact@v4
        with:
          name: tfplan
          path: terraform/environments/prod

      - name: Terraform Apply
        working-directory: terraform/environments/prod
        run: terraform apply -auto-approve tfplan
```

### Import Existing Resources
```bash
# Import existing AWS resource into state
terraform import aws_s3_bucket.existing my-existing-bucket

# Import using for_each key
terraform import 'aws_iam_user.users["alice"]' alice

# Generate configuration from import (Terraform 1.5+)
terraform plan -generate-config-out=generated.tf
```

### Handling Sensitive Values
```hcl
# Reference secrets from AWS Secrets Manager
data "aws_secretsmanager_secret_version" "db_password" {
  secret_id = "prod/db/password"
}

resource "aws_db_instance" "main" {
  # ... other config ...
  password = data.aws_secretsmanager_secret_version.db_password.secret_string
}

# Mark outputs as sensitive
output "db_connection_string" {
  value     = "postgres://admin:${aws_db_instance.main.password}@${aws_db_instance.main.endpoint}"
  sensitive = true
}
```

## Best Practices

1. **Use remote state** - Never store state locally for team projects
2. **Enable state locking** - Prevent concurrent modifications
3. **Version pin providers** - Use `~>` constraints, not `>=`
4. **Separate environments** - Use directories or workspaces, not branches
5. **Module everything reusable** - But don't over-abstract
6. **Validate inputs** - Use variable validation blocks
7. **Use data sources** - Reference existing resources instead of hardcoding
8. **Tag all resources** - Apply consistent tags for cost tracking
9. **Review plans carefully** - Especially for destroy operations

## Common Pitfalls

- **State file conflicts** - Multiple people running terraform simultaneously
- **Hardcoded values** - Not using variables for environment differences
- **Circular dependencies** - Resources depending on each other
- **Missing dependencies** - Not using `depends_on` when implicit deps aren't enough
- **Large state files** - Not breaking up large infrastructure
- **Secrets in state** - State contains sensitive values, encrypt at rest
- **Provider version drift** - Different team members using different versions
- **Not using -target carefully** - Can cause drift, use sparingly
