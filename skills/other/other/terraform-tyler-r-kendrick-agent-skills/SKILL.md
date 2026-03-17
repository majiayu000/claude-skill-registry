---
name: terraform
description: |
  Use when writing Terraform configurations for multi-cloud infrastructure. Covers HCL resources, modules, state management, providers, and plan/apply workflow.
  USE FOR: multi-cloud provisioning, HCL configuration, Terraform state management, provider modules, plan/apply workflow
  DO NOT USE FOR: imperative infrastructure code (use pulumi), Azure-only deployments (use bicep), AWS-only stacks (use cloud-formation)
license: MIT
metadata:
  displayName: "Terraform"
  author: "Tyler-R-Kendrick"
compatibility: claude, copilot, cursor
references:
  - title: "Terraform Documentation"
    url: "https://developer.hashicorp.com/terraform/docs"
  - title: "Terraform GitHub Repository"
    url: "https://github.com/hashicorp/terraform"
  - title: "Terraform Registry"
    url: "https://registry.terraform.io"
---

# Terraform

## Overview
Terraform is HashiCorp's open-source IaC tool for provisioning infrastructure across any cloud provider using HCL (HashiCorp Configuration Language). It uses a plan/apply workflow with state tracking to manage resource lifecycles declaratively.

## Basic Configuration
```hcl
terraform {
  required_version = ">= 1.9"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    bucket = "my-terraform-state"
    key    = "prod/terraform.tfstate"
    region = "us-east-1"
  }
}

provider "aws" {
  region = var.region
}

variable "region" {
  type    = string
  default = "us-east-1"
}

variable "environment" {
  type = string
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Must be dev, staging, or prod."
  }
}

resource "aws_s3_bucket" "assets" {
  bucket = "my-app-${var.environment}-assets"
  tags = {
    Environment = var.environment
  }
}

resource "aws_s3_bucket_versioning" "assets" {
  bucket = aws_s3_bucket.assets.id
  versioning_configuration {
    status = "Enabled"
  }
}

output "bucket_arn" {
  value = aws_s3_bucket.assets.arn
}
```

## Workflow
```bash
# Initialize providers and backend
terraform init

# Preview changes
terraform plan -var="environment=prod"

# Apply changes
terraform apply -var="environment=prod"

# Destroy resources
terraform destroy -var="environment=prod"
```

## Modules
```hcl
# modules/vpc/main.tf
variable "cidr_block" { type = string }
variable "name" { type = string }

resource "aws_vpc" "this" {
  cidr_block = var.cidr_block
  tags       = { Name = var.name }
}

output "vpc_id" { value = aws_vpc.this.id }
```

```hcl
# main.tf
module "vpc" {
  source     = "./modules/vpc"
  cidr_block = "10.0.0.0/16"
  name       = "my-vpc-${var.environment}"
}
```

## State Management
| Backend | Use Case |
|---------|----------|
| `s3` + DynamoDB | AWS (state in S3, locking in DynamoDB) |
| `azurerm` | Azure (state in Blob Storage) |
| `gcs` | GCP (state in Cloud Storage) |
| Terraform Cloud | Managed state with collaboration features |

## Key HCL Features
| Feature | Example |
|---------|---------|
| `for_each` | `for_each = toset(["a", "b"])` |
| `count` | `count = var.create ? 1 : 0` |
| `dynamic` blocks | Generate repeated nested blocks |
| `locals` | `locals { name = "${var.app}-${var.env}" }` |
| Data sources | `data "aws_ami" "latest" { ... }` |
| `depends_on` | Explicit dependency ordering |
| `lifecycle` | `prevent_destroy`, `ignore_changes`, `replace_triggered_by` |

## Best Practices
- Always run `terraform plan` before `apply` and review the diff.
- Use remote state with locking (S3 + DynamoDB, Terraform Cloud) for team collaboration.
- Pin provider versions with `~>` constraints to avoid breaking changes.
- Use modules for reusable infrastructure patterns.
- Use `terraform fmt` and `terraform validate` in CI.
- Never store secrets in `.tf` files — use variables with environment variables or a secrets manager.
- Use `lifecycle { prevent_destroy = true }` on critical stateful resources.
- Use workspaces or directory structure for environment separation (dev/staging/prod).
