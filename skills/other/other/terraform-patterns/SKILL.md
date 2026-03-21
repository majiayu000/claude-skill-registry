---
name: terraform-patterns
description: Module composition, state management, workspace strategy, provider versioning, and infrastructure-as-code best practices.
---

# Terraform Patterns

Production Terraform patterns for maintainable infrastructure-as-code.

## Module Composition

```hcl
# modules/vpc/main.tf - Reusable VPC module
variable "name" {
  type        = string
  description = "VPC name prefix"
}

variable "cidr" {
  type    = string
  default = "10.0.0.0/16"
}

variable "azs" {
  type    = list(string)
  default = ["us-east-1a", "us-east-1b", "us-east-1c"]
}

resource "aws_vpc" "main" {
  cidr_block           = var.cidr
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name        = var.name
    ManagedBy   = "terraform"
    Environment = terraform.workspace
  }
}

resource "aws_subnet" "private" {
  count             = length(var.azs)
  vpc_id            = aws_vpc.main.id
  cidr_block        = cidrsubnet(var.cidr, 8, count.index)
  availability_zone = var.azs[count.index]

  tags = {
    Name = "${var.name}-private-${var.azs[count.index]}"
    Tier = "private"
  }
}

output "vpc_id" {
  value = aws_vpc.main.id
}

output "private_subnet_ids" {
  value = aws_subnet.private[*.id]
}
```

## Root Module Composition

```hcl
# environments/production/main.tf
terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"    # Pin major version, allow minor updates
    }
  }

  backend "s3" {
    bucket         = "mycompany-terraform-state"
    key            = "production/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-locks"    # State locking
    encrypt        = true
  }
}

module "vpc" {
  source = "../../modules/vpc"
  name   = "prod"
  cidr   = "10.0.0.0/16"
  azs    = ["us-east-1a", "us-east-1b", "us-east-1c"]
}

module "database" {
  source    = "../../modules/rds"
  vpc_id    = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnet_ids

  instance_class    = "db.r6g.xlarge"
  allocated_storage = 100
  multi_az          = true
}

module "app" {
  source     = "../../modules/ecs-service"
  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnet_ids

  container_image = "myapp:${var.app_version}"
  desired_count   = 3
  cpu             = 512
  memory          = 1024

  environment_variables = {
    DATABASE_URL = module.database.connection_string
    LOG_LEVEL    = "info"
  }
}
```

## State Management

```hcl
# Remote state data source: reference other state files safely
data "terraform_remote_state" "networking" {
  backend = "s3"
  config = {
    bucket = "mycompany-terraform-state"
    key    = "networking/terraform.tfstate"
    region = "us-east-1"
  }
}

# Use outputs from networking state
module "app" {
  source     = "../../modules/ecs-service"
  vpc_id     = data.terraform_remote_state.networking.outputs.vpc_id
  subnet_ids = data.terraform_remote_state.networking.outputs.private_subnet_ids
}
```

## Resource Lifecycle

```hcl
resource "aws_instance" "app" {
  ami           = var.ami_id
  instance_type = var.instance_type

  lifecycle {
    # Create new before destroying old (zero-downtime replacement)
    create_before_destroy = true

    # Prevent accidental deletion of critical resources
    prevent_destroy = true

    # Ignore changes made outside Terraform (e.g., auto-scaling tags)
    ignore_changes = [tags["LastScaleEvent"]]
  }
}

# Import existing resources
import {
  to = aws_s3_bucket.existing
  id = "my-existing-bucket-name"
}
```

## Variables and Validation

```hcl
variable "environment" {
  type        = string
  description = "Deployment environment"

  validation {
    condition     = contains(["development", "staging", "production"], var.environment)
    error_message = "Environment must be development, staging, or production."
  }
}

variable "instance_count" {
  type    = number
  default = 2

  validation {
    condition     = var.instance_count >= 1 && var.instance_count <= 20
    error_message = "Instance count must be between 1 and 20."
  }
}

# Local values for computed configuration
locals {
  common_tags = {
    Environment = var.environment
    Project     = var.project_name
    ManagedBy   = "terraform"
    Team        = var.team
  }

  is_production = var.environment == "production"
  replica_count = local.is_production ? 3 : 1
}
```

## Dynamic Blocks and for_each

```hcl
# for_each over map (preferred over count for named resources)
variable "services" {
  type = map(object({
    port        = number
    health_path = string
    replicas    = number
  }))
}

resource "aws_ecs_service" "services" {
  for_each = var.services

  name            = each.key
  cluster         = aws_ecs_cluster.main.id
  desired_count   = each.value.replicas
  task_definition = aws_ecs_task_definition.tasks[each.key].arn
}

# Dynamic block for security group rules
resource "aws_security_group" "app" {
  name   = "${var.name}-sg"
  vpc_id = var.vpc_id

  dynamic "ingress" {
    for_each = var.ingress_rules
    content {
      from_port   = ingress.value.port
      to_port     = ingress.value.port
      protocol    = "tcp"
      cidr_blocks = ingress.value.cidr_blocks
      description = ingress.value.description
    }
  }
}
```

## Checklist

- [ ] Pin provider versions with `~>` (allow patch, lock major/minor)
- [ ] Remote state with locking (S3 + DynamoDB or Terraform Cloud)
- [ ] Separate state files per environment (not workspaces for prod vs dev)
- [ ] `prevent_destroy` on databases, S3 buckets, and IAM roles
- [ ] Variable validation blocks for all user-facing inputs
- [ ] Common tags via `locals` applied to every resource
- [ ] Use `for_each` over `count` (survives reordering without recreation)
- [ ] Run `terraform plan` in CI, `terraform apply` requires approval

## Anti-Patterns

- Single state file for all environments: one bad apply affects everything
- Hardcoded values: use variables with defaults and validation
- Using `count` with lists: removing item N recreates items N+1 through end
- No state locking: concurrent applies corrupt state
- Monolithic root module: 500+ resources in one state (split by lifecycle)
- Storing secrets in `.tf` files: use AWS Secrets Manager or Vault references
- Not pinning provider versions: surprise breaking changes on next init
