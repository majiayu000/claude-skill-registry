---
name: opentofu-provisioning-workflow
description: Infrastructure as Code development patterns, resource lifecycle management, and state management workflows with OpenTofu
license: Apache-2.0
compatibility: opencode
metadata:
  audience: developers
  workflow: infrastructure-provisioning
---

# OpenTofu Provisioning Workflow

## What I do

I guide you through complete Infrastructure as Code (IaC) development workflows using OpenTofu. I help you:

- **Resource Provisioning**: Create, update, and manage infrastructure resources
- **Lifecycle Management**: Handle resource creation, modification, and deletion
- **State Management**: Maintain and troubleshoot Terraform state
- **Best Practices**: Apply IaC best practices from OpenTofu and Terraform documentation
- **Dependency Management**: Handle resource dependencies and ordering
- **Validation and Planning**: Ensure infrastructure changes are safe and predictable

## When to use me

Use this skill when you need to:
- Create new infrastructure resources (VPCs, EC2, databases, etc.)
- Update existing infrastructure configurations
- Plan and preview infrastructure changes before applying
- Troubleshoot state issues or drift
- Implement infrastructure best practices and patterns
- Manage complex resource dependencies
- Perform safe infrastructure updates and rollbacks

## Prerequisites

- **OpenTofu CLI installed**: Install from https://opentofu.org/docs/intro/install/
- **Provider Configured**: Complete `opentofu-provider-setup` skill first
- **Provider Authentication**: Valid credentials for your cloud provider
- **Understanding of HCL**: HashiCorp Configuration Language basics
- **State Backend**: Remote state backend configured (S3, Azure Storage, GCS)

## Steps

### Step 1: Define Resources

Create `main.tf` with your infrastructure resources:

```hcl
# Example: AWS EC2 instance
resource "aws_instance" "web_server" {
  ami           = var.ami_id
  instance_type = var.instance_type

  tags = {
    Name        = "WebServer"
    Environment = var.environment
  }

  # User data script
  user_data = <<-EOF
              #!/bin/bash
              yum update -y
              yum install -y httpd
              systemctl start httpd
              EOF
}

# Example: VPC and Subnet
resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "${var.project_name}-vpc"
  }
}

resource "aws_subnet" "public" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = var.public_subnet_cidr
  map_public_ip_on_launch = true
  availability_zone       = var.availability_zone

  tags = {
    Name = "${var.project_name}-public-subnet"
  }
}
```

### Step 2: Define Variables

Create `variables.tf` for reusability:

```hcl
variable "ami_id" {
  description = "ID of AMI to use for EC2 instance"
  type        = string
  default     = "ami-0c55b159cbfafe1f0"
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t2.micro"
}

variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}

variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "project_name" {
  description = "Project name used for tagging"
  type        = string
}
```

### Step 3: Define Outputs

Create `outputs.tf` to expose values:

```hcl
output "vpc_id" {
  description = "ID of the VPC"
  value       = aws_vpc.main.id
}

output "public_subnet_id" {
  description = "ID of the public subnet"
  value       = aws_subnet.public.id
}

output "instance_public_ip" {
  description = "Public IP of the EC2 instance"
  value       = aws_instance.web_server.public_ip
}

output "instance_private_ip" {
  description = "Private IP of the EC2 instance"
  value       = aws_instance.web_server.private_ip
}
```

### Step 4: Create Terraform Variables File (Optional)

Create `terraform.tfvars` for environment-specific values:

```hcl
# terraform.tfvars
ami_id          = "ami-0c55b159cbfafe1f0"
instance_type   = "t2.micro"
environment     = "dev"
vpc_cidr        = "10.0.0.0/16"
project_name    = "my-project"
availability_zone = "us-east-1a"
```

### Step 5: Initialize and Format

```bash
# Initialize (download providers)
tofu init

# Format code for consistency
tofu fmt

# Validate configuration
tofu validate
```

### Step 6: Plan Changes

```bash
# Show execution plan
tofu plan

# Save plan for review or automation
tofu plan -out=tfplan

# Review plan in detail
tofu show tfplan
```

### Step 7: Apply Changes

```bash
# Apply changes interactively
tofu apply

# Apply saved plan
tofu apply tfplan

# Auto-approve (use with caution in automation)
tofu apply -auto-approve
```

### Step 8: Inspect State

```bash
# List all resources in state
tofu state list

# Show specific resource details
tofu state show aws_instance.web_server

# Show current state as JSON
tofu show -json
```

### Step 9: Update Resources

```bash
# Modify configuration and plan changes
tofu plan -out=tfplan

# Review and apply changes
tofu apply tfplan
```

### Step 10: Destroy Resources

```bash
# Plan destruction
tofu plan -destroy

# Destroy all resources in configuration
tofu destroy

# Destroy specific resources
tofu destroy -target=aws_instance.web_server
```

## Best Practices

### Resource Management

1. **Use Descriptive Names**: Make resource names self-documenting
2. **Tag Everything**: Apply consistent tagging for cost tracking and organization
3. **Use Variables**: Avoid hardcoding values; use variables for flexibility
4. **Separate Environments**: Use workspaces or separate state files for dev/staging/prod
5. **Limit Resource Scope**: Keep configurations focused and modular

### State Management

```bash
# Use remote state backends for team collaboration
# Reference: https://www.terraform.io/docs/language/settings/backends/index.html

# State best practices:
# - Enable encryption
# - Enable versioning
# - Use state locking
# - Regular backups
```

### Dependency Management

```hcl
# Implicit dependencies (reference attributes)
resource "aws_security_group" "web" {
  name = "web-security-group"
  # ...
}

resource "aws_instance" "web" {
  vpc_security_group_ids = [aws_security_group.web.id]
  # Depends implicitly on security group
}

# Explicit dependencies
resource "aws_instance" "db" {
  depends_on = [aws_instance.web]
  # ...
}

# Use for_each and count for multiple resources
resource "aws_instance" "servers" {
  count         = 3
  ami           = var.ami_id
  instance_type = var.instance_type

  tags = {
    Name = "Server-${count.index + 1}"
  }
}
```

### Validation and Planning

```bash
# Always run plan before apply
tofu plan -out=tfplan
tofu apply tfplan

# Use targeted plans for specific changes
tofu plan -target=aws_instance.web_server

# Use refresh-only to detect drift
tofu apply -refresh-only
```

### Modularization

```hcl
# Create reusable modules
# modules/vpc/main.tf
resource "aws_vpc" "main" {
  cidr_block           = var.cidr_block
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = merge(var.tags, {
    Name = "${var.name}-vpc"
  })
}

# modules/vpc/variables.tf
variable "cidr_block" {
  type = string
}

variable "name" {
  type = string
}

variable "tags" {
  type = map(string)
  default = {}
}

# Use module in main configuration
module "vpc" {
  source = "./modules/vpc"

  cidr_block = var.vpc_cidr
  name       = var.project_name
  tags       = var.common_tags
}
```

### Data Sources

```hcl
# Use data sources to reference existing resources
data "aws_ami" "amazon_linux_2" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }
}

resource "aws_instance" "web" {
  ami = data.aws_ami.amazon_linux_2.id
  # ...
}
```

### Lifecycle Management

```hcl
resource "aws_instance" "web" {
  # Prevent recreation if tags change
  lifecycle {
    create_before_destroy = true
    ignore_changes = [
      tags,
      user_data
    ]
  }

  # Prevent accidental destruction
  lifecycle {
    prevent_destroy = true
  }
}
```

## Common Issues

### Issue: State File Lock

**Symptom**: Error `Error: Error acquiring the state lock`

**Solution**:
```bash
# Check who has the lock
tofu state pull

# Force unlock if necessary (caution!)
tofu force-unlock <LOCK_ID>

# Reference: https://www.terraform.io/docs/language/state/locking.html
```

### Issue: Resource Already Exists

**Symptom**: Error `Error: Error creating ...: ... already exists`

**Solution**:
```bash
# Import existing resource into state
tofu import aws_instance.web_server i-0123456789abcdef0

# Then remove from configuration if needed
tofu state rm aws_instance.web_server
```

### Issue: Plan Shows Destroy and Create

**Symptom**: Plan wants to destroy and recreate resource instead of updating

**Solution**:
```hcl
# Use create_before_destroy lifecycle
resource "aws_instance" "web" {
  lifecycle {
    create_before_destroy = true
  }
}

# Or ignore changes to certain attributes
lifecycle {
  ignore_changes = [tags]
}
```

### Issue: State Drift

**Symptom**: Actual infrastructure differs from state

**Solution**:
```bash
# Refresh state to detect drift
tofu refresh

# Apply only to sync state (no changes)
tofu apply -refresh-only

# For manual drift, use terraform import
tofu import <resource_type>.<resource_name> <resource_id>
```

### Issue: Dependency Cycle

**Symptom**: Error `Error: Cycle: ...`

**Solution**:
```bash
# Review resource dependencies
tofu graph | dot -Tpng > graph.png

# Use explicit dependencies or refactor configuration
resource "aws_instance" "db" {
  depends_on = [aws_instance.web, aws_security_group.db]
  # ...
}
```

### Issue: Timeout During Apply

**Symptom**: Apply operation hangs or times out

**Solution**:
```bash
# Use timeouts in resource configuration
resource "aws_instance" "web" {
  timeouts {
    create = "10m"
    delete = "15m"
  }
  # ...
}

# Run plan in background
tofu apply -auto-parallelism=4 &
```

## Reference Documentation

- **OpenTofu Documentation**: https://opentofu.org/docs/
- **Terraform Language**: https://www.terraform.io/docs/language/
- **Terraform State**: https://www.terraform.io/docs/language/state/
- **Resource Lifecycle**: https://www.terraform.io/docs/language/meta-arguments/lifecycle.html
- **Data Sources**: https://www.terraform.io/docs/language/data-sources/index.html
- **Modules**: https://www.terraform.io/docs/language/modules/develop/index.html

## Examples

### Complete Web Application Stack

```hcl
# main.tf
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# Provider configuration
provider "aws" {
  region = var.aws_region
}

# VPC
resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "${var.project_name}-vpc"
  }
}

# Internet Gateway
resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "${var.project_name}-igw"
  }
}

# Public Subnet
resource "aws_subnet" "public" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = var.public_subnet_cidr
  map_public_ip_on_launch = true
  availability_zone       = var.availability_zone

  tags = {
    Name = "${var.project_name}-public-subnet"
  }
}

# Route Table
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }

  tags = {
    Name = "${var.project_name}-public-rt"
  }
}

# Route Table Association
resource "aws_route_table_association" "public" {
  subnet_id      = aws_subnet.public.id
  route_table_id = aws_route_table.public.id
}

# Security Group
resource "aws_security_group" "web" {
  name        = "${var.project_name}-web-sg"
  description = "Allow HTTP/HTTPS inbound"
  vpc_id      = aws_vpc.main.id

  ingress {
    description = "HTTP from anywhere"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "HTTPS from anywhere"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.project_name}-web-sg"
  }
}

# EC2 Instance
resource "aws_instance" "web_server" {
  ami           = data.aws_ami.amazon_linux_2.id
  instance_type = var.instance_type
  subnet_id     = aws_subnet.public.id

  vpc_security_group_ids = [aws_security_group.web.id]

  tags = {
    Name        = "${var.project_name}-web-server"
    Environment = var.environment
  }

  user_data = <<-EOF
              #!/bin/bash
              yum update -y
              yum install -y httpd
              systemctl start httpd
              systemctl enable httpd
              echo "<h1>Hello from ${var.project_name}!</h1>" > /var/www/html/index.html
              EOF
}

# Data Source for AMI
data "aws_ami" "amazon_linux_2" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }
}

# variables.tf
variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "public_subnet_cidr" {
  description = "CIDR block for public subnet"
  type        = string
  default     = "10.0.1.0/24"
}

variable "availability_zone" {
  description = "Availability zone"
  type        = string
  default     = "us-east-1a"
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t2.micro"
}

variable "project_name" {
  description = "Project name"
  type        = string
}

variable "environment" {
  description = "Environment"
  type        = string
}

# outputs.tf
output "vpc_id" {
  description = "VPC ID"
  value       = aws_vpc.main.id
}

output "public_subnet_id" {
  description = "Public subnet ID"
  value       = aws_subnet.public.id
}

output "instance_public_ip" {
  description = "Web server public IP"
  value       = aws_instance.web_server.public_ip
}

output "instance_public_dns" {
  description = "Web server public DNS"
  value       = aws_instance.web_server.public_dns
}
```

### Workflow Commands

```bash
# Complete provisioning workflow
tofu init           # Initialize
tofu fmt            # Format
tofu validate       # Validate
tofu plan -out=tfplan  # Plan
tofu apply tfplan    # Apply
tofu output         # Show outputs
tofu show           # Show state

# Update workflow
tofu plan -out=tfplan -refresh=true
tofu apply tfplan

# Destroy workflow
tofu plan -destroy
tofu destroy
```

## Tips and Tricks

- **Use tofu fmt**: Auto-format code for consistency
- **Run tofu validate**: Catch syntax errors early
- **Review plans**: Always review plans before applying
- **Use workspaces**: Manage multiple environments
- **Module everything**: Create reusable modules for common patterns
- **Tag resources**: For cost tracking and organization
- **Use data sources**: Reference existing infrastructure
- **Import existing resources**: Bring existing resources under management
- **State isolation**: Use separate state files for different environments
- **Version control**: Store configuration in Git (but not state files!)

## Next Steps

After mastering provisioning workflows, explore:
- **Terraform Modules**: Create reusable infrastructure components
- **Terraform Workspaces**: Manage multiple environments
- **CI/CD Integration**: Automate infrastructure provisioning
- **Terraform Cloud/Enterprise**: Enterprise-grade state management
- **Infrastructure Testing**: Use tools like terratest for testing
