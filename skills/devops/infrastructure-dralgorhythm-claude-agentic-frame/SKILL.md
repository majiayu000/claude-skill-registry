---
name: infrastructure
description: Manage infrastructure as code. Use when provisioning resources, managing cloud infrastructure, or setting up environments. Covers Terraform and IaC patterns.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Infrastructure as Code

## Principles

1. **Everything in Code**: No manual changes
2. **Version Controlled**: All changes tracked
3. **Idempotent**: Safe to run multiple times
4. **Tested**: Validate before apply

## Terraform Basics

### Project Structure
```
infrastructure/
├── main.tf           # Main configuration
├── variables.tf      # Input variables
├── outputs.tf        # Output values
├── providers.tf      # Provider config
├── terraform.tfvars  # Variable values
└── modules/
    └── vpc/          # Reusable modules
```

### Example: AWS VPC

```hcl
# providers.tf
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# main.tf
resource "aws_vpc" "main" {
  cidr_block = var.vpc_cidr

  tags = {
    Name        = "${var.project}-vpc"
    Environment = var.environment
  }
}

# variables.tf
variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
  default     = "10.0.0.0/16"
}
```

## Workflows

```bash
# Initialize
terraform init

# Plan changes
terraform plan -out=tfplan

# Apply changes
terraform apply tfplan

# Destroy resources
terraform destroy
```

## Best Practices

1. **Use Remote State**: Store state in S3/GCS
2. **Lock State**: Prevent concurrent modifications
3. **Use Modules**: Reusable infrastructure components
4. **Environment Separation**: Separate state per environment
5. **Secret Management**: Never store secrets in code

## State Management

```hcl
terraform {
  backend "s3" {
    bucket         = "terraform-state-bucket"
    key            = "prod/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-locks"
    encrypt        = true
  }
}
```

## ECS/Fargate

```hcl
# Task Definition
resource "aws_ecs_task_definition" "app" {
  family                   = "${var.project}-task"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = 256
  memory                   = 512
  execution_role_arn       = aws_iam_role.ecs_execution.arn

  container_definitions = jsonencode([{
    name  = "app"
    image = "${aws_ecr_repository.app.repository_url}:latest"
    portMappings = [{
      containerPort = 8080
      protocol      = "tcp"
    }]
    logConfiguration = {
      logDriver = "awslogs"
      options = {
        awslogs-group         = aws_cloudwatch_log_group.app.name
        awslogs-region        = var.aws_region
        awslogs-stream-prefix = "app"
      }
    }
  }])
}

# ECS Service
resource "aws_ecs_service" "app" {
  name            = "${var.project}-service"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.app.arn
  desired_count   = var.app_count
  launch_type     = "FARGATE"

  network_configuration {
    subnets         = aws_subnet.private[*].id
    security_groups = [aws_security_group.app.id]
  }
}
```

## S3 Buckets

```hcl
resource "aws_s3_bucket" "assets" {
  bucket = "${var.project}-assets-${var.environment}"
}

resource "aws_s3_bucket_versioning" "assets" {
  bucket = aws_s3_bucket.assets.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "assets" {
  bucket = aws_s3_bucket.assets.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}
```
