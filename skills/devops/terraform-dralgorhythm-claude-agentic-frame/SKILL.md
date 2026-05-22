---
name: terraform
description: Write Terraform infrastructure code. Use when provisioning cloud resources, managing infrastructure as code, or automating deployments. Covers HCL patterns.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Terraform Development

## Project Structure

```
terraform/
├── main.tf           # Main resources
├── variables.tf      # Input variables
├── outputs.tf        # Output values
├── providers.tf      # Provider config
├── versions.tf       # Version constraints
├── terraform.tfvars  # Variable values
└── modules/
    └── vpc/
        ├── main.tf
        ├── variables.tf
        └── outputs.tf
```

## Provider Configuration

```hcl
# versions.tf
terraform {
  required_version = ">= 1.5"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    bucket         = "terraform-state"
    key            = "prod/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-locks"
    encrypt        = true
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Environment = var.environment
      ManagedBy   = "terraform"
    }
  }
}
```

## Variables

```hcl
# variables.tf
variable "environment" {
  description = "Environment name"
  type        = string

  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}

variable "instance_config" {
  description = "EC2 instance configuration"
  type = object({
    instance_type = string
    ami_id        = string
    volume_size   = number
  })

  default = {
    instance_type = "t3.micro"
    ami_id        = "ami-12345678"
    volume_size   = 20
  }
}
```

## Resources

```hcl
# main.tf
resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true

  tags = {
    Name = "${var.project}-vpc"
  }
}

resource "aws_subnet" "private" {
  count             = length(var.availability_zones)
  vpc_id            = aws_vpc.main.id
  cidr_block        = cidrsubnet(var.vpc_cidr, 8, count.index)
  availability_zone = var.availability_zones[count.index]

  tags = {
    Name = "${var.project}-private-${count.index + 1}"
  }
}
```

## Modules

```hcl
# Using a module
module "vpc" {
  source = "./modules/vpc"

  project     = var.project
  environment = var.environment
  cidr_block  = "10.0.0.0/16"
}

# Module outputs
output "vpc_id" {
  value = module.vpc.vpc_id
}
```

## Data Sources

```hcl
data "aws_ami" "amazon_linux" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }
}

resource "aws_instance" "web" {
  ami           = data.aws_ami.amazon_linux.id
  instance_type = var.instance_type
}
```

## Workflow

```bash
# Initialize
terraform init

# Format
terraform fmt -recursive

# Validate
terraform validate

# Plan
terraform plan -out=tfplan

# Apply
terraform apply tfplan

# Destroy
terraform destroy
```

## Best Practices

1. Use remote state with locking
2. Use modules for reusability
3. Use variables for all configurable values
4. Use data sources for existing resources
5. Tag all resources
6. Use workspaces or directories for environments
