---
name: terraform
description: Terraform infrastructure as code including modules, state management, and cloud provisioning. Activate for tf files, IaC, infrastructure provisioning, and cloud resource management.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# Terraform Skill

Provides comprehensive Terraform infrastructure as code capabilities for the Golden Armada AI Agent Fleet Platform.

## When to Use This Skill

Activate this skill when working with:
- Infrastructure provisioning
- Terraform modules and configurations
- State management
- Cloud resource definitions
- Multi-environment deployments

## Quick Reference

### Common Commands
\`\`\`bash
# Initialize
terraform init
terraform init -upgrade

# Plan
terraform plan
terraform plan -out=tfplan
terraform plan -var="environment=prod"

# Apply
terraform apply
terraform apply tfplan
terraform apply -auto-approve

# Destroy
terraform destroy
terraform destroy -target=aws_instance.example

# State
terraform state list
terraform state show <resource>
terraform state mv <source> <destination>
terraform state rm <resource>

# Workspace
terraform workspace list
terraform workspace new dev
terraform workspace select prod

# Format/Validate
terraform fmt -recursive
terraform validate
\`\`\`

## Project Structure

\`\`\`
terraform/
├── main.tf
├── variables.tf
├── outputs.tf
├── providers.tf
├── versions.tf
├── terraform.tfvars
├── environments/
│   ├── dev.tfvars
│   └── prod.tfvars
└── modules/
    ├── networking/
    ├── compute/
    └── database/
\`\`\`

## Provider Configuration

\`\`\`hcl
# versions.tf
terraform {
  required_version = ">= 1.0.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.0"
    }
  }

  backend "s3" {
    bucket         = "golden-armada-terraform-state"
    key            = "state/terraform.tfstate"
    region         = "us-west-2"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}

# providers.tf
provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = "golden-armada"
      Environment = var.environment
      ManagedBy   = "terraform"
    }
  }
}
\`\`\`

## Variables

\`\`\`hcl
# variables.tf
variable "environment" {
  description = "Environment name"
  type        = string
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}

variable "instance_count" {
  description = "Number of instances"
  type        = number
  default     = 2
}

variable "tags" {
  description = "Resource tags"
  type        = map(string)
  default     = {}
}

# terraform.tfvars
environment    = "dev"
instance_count = 2
\`\`\`

## Module Example

\`\`\`hcl
# modules/eks-cluster/main.tf
resource "aws_eks_cluster" "main" {
  name     = "${var.project}-${var.environment}"
  role_arn = aws_iam_role.cluster.arn
  version  = var.kubernetes_version

  vpc_config {
    subnet_ids              = var.subnet_ids
    endpoint_private_access = true
    endpoint_public_access  = var.public_access
  }

  tags = var.tags
}

# modules/eks-cluster/variables.tf
variable "project" {
  type = string
}

variable "environment" {
  type = string
}

variable "kubernetes_version" {
  type    = string
  default = "1.28"
}

# Usage
module "eks" {
  source = "./modules/eks-cluster"

  project            = "golden-armada"
  environment        = var.environment
  subnet_ids         = module.vpc.private_subnets
  kubernetes_version = "1.28"
  tags               = local.tags
}
\`\`\`

## Best Practices

1. **State Management**: Use remote state with locking
2. **Modules**: Create reusable modules for common patterns
3. **Workspaces**: Separate environments using workspaces
4. **Variables**: Use tfvars files per environment
5. **Outputs**: Export important values for other modules
6. **Tagging**: Apply consistent tags to all resources
