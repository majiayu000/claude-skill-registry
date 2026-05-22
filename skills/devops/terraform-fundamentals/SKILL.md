---
name: terraform-fundamentals
description: Master Terraform HCL syntax, resources, providers, variables, and outputs with production-ready patterns
sasmp_version: "1.3.0"
version: "2.0.0"
bonded_agent: 01-terraform-fundamentals
bond_type: PRIMARY_BOND
---

# Terraform Fundamentals Skill

Master HashiCorp Configuration Language (HCL) and core Terraform concepts for building production infrastructure.

## Quick Reference

```hcl
# Block Types Overview
terraform {}     # Settings & provider requirements
provider "x" {}  # Provider configuration
resource "x" {}  # Infrastructure objects
data "x" {}      # Read external data
variable "x" {}  # Input parameters
output "x" {}    # Export values
locals {}        # Computed values
module "x" {}    # Reusable components
```

## Core Concepts

### 1. Provider Configuration
```hcl
terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Environment = var.environment
      ManagedBy   = "Terraform"
    }
  }
}
```

### 2. Resource Definitions
```hcl
resource "aws_instance" "web" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = var.instance_type
  subnet_id     = aws_subnet.main.id

  tags = merge(local.common_tags, {
    Name = "${var.project}-web"
  })

  lifecycle {
    create_before_destroy = true
    prevent_destroy       = var.environment == "prod"
    ignore_changes        = [tags["LastModified"]]
  }
}
```

### 3. Variables with Validation
```hcl
variable "environment" {
  type        = string
  description = "Deployment environment"

  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Must be dev, staging, or prod."
  }
}

variable "instance_config" {
  type = object({
    instance_type     = string
    volume_size       = number
    enable_monitoring = optional(bool, true)
  })

  default = {
    instance_type = "t3.micro"
    volume_size   = 20
  }
}
```

### 4. Outputs
```hcl
output "instance_id" {
  description = "EC2 instance ID"
  value       = aws_instance.web.id
}

output "connection_info" {
  description = "SSH connection details"
  value = {
    host = aws_instance.web.public_ip
    user = "ubuntu"
  }
  sensitive = true
}
```

### 5. Data Sources
```hcl
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"]  # Canonical

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-*-22.04-amd64-server-*"]
  }
}

data "aws_availability_zones" "available" {
  state = "available"
}
```

### 6. Locals
```hcl
locals {
  common_tags = {
    Project     = var.project
    Environment = var.environment
    Owner       = var.team
  }

  name_prefix = "${var.project}-${var.environment}"

  subnet_cidrs = [for i in range(3) : cidrsubnet(var.vpc_cidr, 8, i)]
}
```

## Meta-Arguments

### count
```hcl
resource "aws_instance" "web" {
  count = var.instance_count

  ami           = data.aws_ami.ubuntu.id
  instance_type = var.instance_type

  tags = {
    Name = "${var.project}-web-${count.index}"
  }
}
```

### for_each
```hcl
resource "aws_iam_user" "users" {
  for_each = toset(var.user_names)
  name     = each.value
}

resource "aws_instance" "apps" {
  for_each = var.app_configs

  ami           = data.aws_ami.ubuntu.id
  instance_type = each.value.instance_type

  tags = {
    Name = each.key
    Role = each.value.role
  }
}
```

### depends_on
```hcl
resource "aws_instance" "app" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t3.micro"

  depends_on = [
    aws_iam_role_policy_attachment.app
  ]
}
```

## Expressions

### Conditionals
```hcl
instance_type = var.environment == "prod" ? "t3.large" : "t3.micro"
count         = var.create_resource ? 1 : 0
```

### For Expressions
```hcl
# List transformation
upper_names = [for name in var.names : upper(name)]

# Filtering
prod_instances = [for i in var.instances : i if i.environment == "prod"]

# Map transformation
instance_ips = {for i in aws_instance.web : i.tags.Name => i.private_ip}
```

### Splat Expressions
```hcl
instance_ids = aws_instance.web[*].id
private_ips  = aws_instance.web[*].private_ip
```

## Common Patterns

### Conditional Resource Creation
```hcl
resource "aws_eip" "nat" {
  count  = var.enable_nat_gateway ? 1 : 0
  domain = "vpc"
}
```

### Dynamic Blocks
```hcl
resource "aws_security_group" "web" {
  name   = "${var.project}-web"
  vpc_id = var.vpc_id

  dynamic "ingress" {
    for_each = var.ingress_rules
    content {
      from_port   = ingress.value.port
      to_port     = ingress.value.port
      protocol    = ingress.value.protocol
      cidr_blocks = ingress.value.cidr_blocks
    }
  }
}
```

## Troubleshooting

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `Invalid HCL syntax` | Missing brace/quote | Run `terraform fmt` |
| `Provider not found` | Missing `required_providers` | Add provider block |
| `Reference to undeclared` | Typo in resource name | Check exact spelling |
| `Cycle detected` | Circular dependency | Use `depends_on` or restructure |

### Debug Commands
```bash
# Validate syntax
terraform validate

# Format code
terraform fmt -recursive

# Show dependency graph
terraform graph | dot -Tpng > graph.png
```

## Usage

```python
Skill("terraform-fundamentals")
```

## Related

- **Agent**: 01-terraform-fundamentals (PRIMARY_BOND)
- **Skill**: terraform-providers (SECONDARY_BOND)
