---
name: opentofu
description: >-
  You are an expert in OpenTofu, the open-source fork of Terraform maintained
  by the Linux Foundation. You help developers and platform teams provision
  cloud infrastructure using HCL (HashiCorp Configuration Language), with full
  compatibility with existing Terraform modules, state files, and providers —
  plus new features like client-side state encryption, OCI registry support,
  and removed BSL license restrictions.
license: Apache-2.0
compatibility: ''
metadata:
  author: terminal-skills
  version: 1.0.0
  category: Infrastructure & DevOps
  tags:
    - iac
    - infrastructure
    - open-source
    - terraform-alternative
    - cloud
    - provisioning
---

# OpenTofu — Open-Source Terraform Alternative

You are an expert in OpenTofu, the open-source fork of Terraform maintained by the Linux Foundation. You help developers and platform teams provision cloud infrastructure using HCL (HashiCorp Configuration Language), with full compatibility with existing Terraform modules, state files, and providers — plus new features like client-side state encryption, OCI registry support, and removed BSL license restrictions.

## Core Capabilities

### Basic Usage

```hcl
# main.tf — Infrastructure definition
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  # State encryption (OpenTofu exclusive feature)
  encryption {
    method "aes_gcm" "default" {
      keys = key_provider.pbkdf2.default
    }
    state {
      method   = method.aes_gcm.default
      enforced = true                     # Reject unencrypted state
    }
  }
}

provider "aws" {
  region = var.region
}

# VPC with public and private subnets
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.5.0"

  name = "${var.project}-vpc"
  cidr = "10.0.0.0/16"

  azs             = ["${var.region}a", "${var.region}b", "${var.region}c"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]

  enable_nat_gateway = true
  single_nat_gateway = var.environment != "production"   # Save cost in non-prod

  tags = local.common_tags
}

# ECS Fargate service
resource "aws_ecs_service" "api" {
  name            = "${var.project}-api"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.api.arn
  desired_count   = var.environment == "production" ? 3 : 1
  launch_type     = "FARGATE"

  network_configuration {
    subnets         = module.vpc.private_subnets
    security_groups = [aws_security_group.api.id]
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.api.arn
    container_name   = "api"
    container_port   = 3000
  }
}

# Variables
variable "project" { default = "myapp" }
variable "region" { default = "us-east-1" }
variable "environment" { default = "staging" }

locals {
  common_tags = {
    Project     = var.project
    Environment = var.environment
    ManagedBy   = "opentofu"
  }
}
```

### State Encryption (OpenTofu Exclusive)

```hcl
# State encryption — data never stored in plaintext
terraform {
  encryption {
    key_provider "pbkdf2" "default" {
      passphrase = var.state_passphrase    # From env or vault
    }
    key_provider "aws_kms" "prod" {
      kms_key_id = "alias/opentofu-state"
      region     = "us-east-1"
    }
    method "aes_gcm" "default" {
      keys = key_provider.pbkdf2.default
    }
    method "aes_gcm" "prod" {
      keys = key_provider.aws_kms.prod
    }
    state {
      method   = method.aes_gcm.prod      # KMS-encrypted state
      enforced = true
    }
    plan {
      method   = method.aes_gcm.default   # Encrypt plan files too
      enforced = true
    }
  }
}
```

### Commands

```bash
# Drop-in replacement for terraform CLI
tofu init                                 # Initialize providers and modules
tofu plan                                 # Preview changes
tofu apply                               # Apply changes
tofu destroy                             # Tear down infrastructure
tofu state list                           # List resources in state
tofu import aws_s3_bucket.data my-bucket  # Import existing resources

# Migration from Terraform
# Just replace `terraform` with `tofu` — state files are compatible
```

## Installation

```bash
# macOS
brew install opentofu

# Linux
curl -fsSL https://get.opentofu.org/install-opentofu.sh | sh

# Docker
docker run -it ghcr.io/opentofu/opentofu:latest init
```

## Best Practices

1. **State encryption** — Enable client-side encryption for state files; OpenTofu's exclusive feature, use KMS for production
2. **Modules for reuse** — Package infrastructure patterns as modules; share via private registry or Git
3. **Remote state** — Store state in S3 + DynamoDB (locking) or Terraform Cloud/Spacelift; never local state for teams
4. **Workspaces for environments** — Use workspaces or separate state files for dev/staging/production
5. **Plan before apply** — Always `tofu plan` and review; use `-out=plan.tfplan` for deterministic applies in CI
6. **Import existing resources** — Use `tofu import` to bring existing infrastructure under management
7. **Compatible with Terraform** — All Terraform providers and modules work; migrate by replacing the binary
8. **Pin versions** — Pin provider and module versions; `~> 5.0` for minor updates, exact pins for production
