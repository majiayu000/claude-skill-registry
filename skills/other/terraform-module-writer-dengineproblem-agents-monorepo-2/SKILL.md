---
name: terraform-module-writer
description: Эксперт по Terraform модулям. Используй для создания переиспользуемых модулей, variables, outputs и best practices.
---

# Terraform Module Writer

Эксперт по созданию высококачественных, переиспользуемых Terraform модулей с соблюдением industry best practices.

## Module Structure

### Standard Directory Layout

```
modules/
└── my-module/
    ├── main.tf           # Primary resource definitions
    ├── variables.tf      # Input variable declarations
    ├── outputs.tf        # Output value definitions
    ├── versions.tf       # Provider version constraints
    ├── locals.tf         # Local values and computations
    ├── data.tf           # Data source definitions
    ├── README.md         # Module documentation
    ├── CHANGELOG.md      # Version history
    ├── examples/
    │   ├── basic/
    │   │   ├── main.tf
    │   │   └── outputs.tf
    │   └── advanced/
    │       ├── main.tf
    │       └── outputs.tf
    └── tests/
        └── module_test.go
```

### versions.tf Template

```hcl
terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.0.0, < 6.0.0"
    }
    random = {
      source  = "hashicorp/random"
      version = ">= 3.5.0"
    }
  }
}
```

---

## Input Variable Design

### Variable Declaration Best Practices

```hcl
# variables.tf

# Required variables (no default)
variable "name" {
  description = "Name prefix for all resources created by this module"
  type        = string

  validation {
    condition     = can(regex("^[a-z][a-z0-9-]*$", var.name))
    error_message = "Name must start with a letter and contain only lowercase letters, numbers, and hyphens."
  }
}

variable "environment" {
  description = "Environment name (e.g., dev, staging, prod)"
  type        = string

  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be one of: dev, staging, prod."
  }
}

# Optional variables with sensible defaults
variable "instance_type" {
  description = "EC2 instance type for the application servers"
  type        = string
  default     = "t3.medium"

  validation {
    condition     = can(regex("^[a-z][0-9][.][a-z]+$", var.instance_type))
    error_message = "Instance type must be a valid AWS instance type format."
  }
}

variable "enable_monitoring" {
  description = "Enable detailed monitoring for resources"
  type        = bool
  default     = true
}

variable "min_instances" {
  description = "Minimum number of instances in the Auto Scaling Group"
  type        = number
  default     = 2

  validation {
    condition     = var.min_instances >= 1 && var.min_instances <= 100
    error_message = "Minimum instances must be between 1 and 100."
  }
}

variable "max_instances" {
  description = "Maximum number of instances in the Auto Scaling Group"
  type        = number
  default     = 10

  validation {
    condition     = var.max_instances >= 1 && var.max_instances <= 100
    error_message = "Maximum instances must be between 1 and 100."
  }
}
```

### Complex Variable Types

```hcl
# Object type with optional attributes
variable "vpc_config" {
  description = "VPC configuration for the module"
  type = object({
    vpc_id             = string
    subnet_ids         = list(string)
    security_group_ids = optional(list(string), [])
    assign_public_ip   = optional(bool, false)
  })

  validation {
    condition     = length(var.vpc_config.subnet_ids) >= 2
    error_message = "At least 2 subnet IDs required for high availability."
  }
}

# Map with specific value types
variable "tags" {
  description = "Additional tags to apply to all resources"
  type        = map(string)
  default     = {}

  validation {
    condition     = alltrue([for k, v in var.tags : can(regex("^[a-zA-Z][a-zA-Z0-9:/_-]*$", k))])
    error_message = "Tag keys must start with a letter and contain only valid characters."
  }
}

# List of objects
variable "ingress_rules" {
  description = "List of ingress rules for the security group"
  type = list(object({
    description = string
    from_port   = number
    to_port     = number
    protocol    = string
    cidr_blocks = optional(list(string), [])
    security_groups = optional(list(string), [])
  }))
  default = []

  validation {
    condition = alltrue([
      for rule in var.ingress_rules :
      rule.from_port >= 0 && rule.from_port <= 65535 &&
      rule.to_port >= 0 && rule.to_port <= 65535
    ])
    error_message = "Port numbers must be between 0 and 65535."
  }
}

# Sensitive variables
variable "database_password" {
  description = "Master password for the RDS instance"
  type        = string
  sensitive   = true

  validation {
    condition     = length(var.database_password) >= 16
    error_message = "Database password must be at least 16 characters."
  }
}
```

---

## Local Values

### locals.tf Template

```hcl
locals {
  # Naming convention
  name_prefix = "${var.name}-${var.environment}"

  # Common tags applied to all resources
  common_tags = merge(
    var.tags,
    {
      Name        = local.name_prefix
      Environment = var.environment
      ManagedBy   = "terraform"
      Module      = "my-module"
      Project     = var.name
    }
  )

  # Computed values
  is_production      = var.environment == "prod"
  enable_encryption  = local.is_production
  backup_retention   = local.is_production ? 30 : 7
  instance_count     = local.is_production ? var.max_instances : var.min_instances

  # Derived configurations
  monitoring_config = {
    enabled         = var.enable_monitoring || local.is_production
    detailed        = local.is_production
    retention_days  = local.is_production ? 90 : 30
    alarm_threshold = local.is_production ? 80 : 90
  }

  # Dynamic block helpers
  ingress_rules_map = {
    for idx, rule in var.ingress_rules :
    "${rule.protocol}-${rule.from_port}-${rule.to_port}" => rule
  }

  # Conditional resource naming
  bucket_name = var.bucket_name != null ? var.bucket_name : "${local.name_prefix}-storage-${random_id.bucket.hex}"
}
```

---

## Resource Definitions

### main.tf Template

```hcl
# main.tf

#------------------------------------------------------------------------------
# Security Group
#------------------------------------------------------------------------------
resource "aws_security_group" "this" {
  name_prefix = "${local.name_prefix}-sg-"
  description = "Security group for ${var.name} ${var.environment}"
  vpc_id      = var.vpc_config.vpc_id

  tags = merge(local.common_tags, {
    Name = "${local.name_prefix}-sg"
  })

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_security_group_rule" "ingress" {
  for_each = local.ingress_rules_map

  type              = "ingress"
  security_group_id = aws_security_group.this.id
  description       = each.value.description
  from_port         = each.value.from_port
  to_port           = each.value.to_port
  protocol          = each.value.protocol
  cidr_blocks       = length(each.value.cidr_blocks) > 0 ? each.value.cidr_blocks : null
  source_security_group_id = length(each.value.security_groups) > 0 ? each.value.security_groups[0] : null
}

resource "aws_security_group_rule" "egress" {
  type              = "egress"
  security_group_id = aws_security_group.this.id
  description       = "Allow all outbound traffic"
  from_port         = 0
  to_port           = 0
  protocol          = "-1"
  cidr_blocks       = ["0.0.0.0/0"]
}

#------------------------------------------------------------------------------
# Launch Template
#------------------------------------------------------------------------------
resource "aws_launch_template" "this" {
  name_prefix   = "${local.name_prefix}-lt-"
  description   = "Launch template for ${var.name} ${var.environment}"
  image_id      = data.aws_ami.amazon_linux.id
  instance_type = var.instance_type

  network_interfaces {
    associate_public_ip_address = var.vpc_config.assign_public_ip
    security_groups             = concat([aws_security_group.this.id], var.vpc_config.security_group_ids)
    delete_on_termination       = true
  }

  iam_instance_profile {
    arn = aws_iam_instance_profile.this.arn
  }

  monitoring {
    enabled = local.monitoring_config.detailed
  }

  metadata_options {
    http_endpoint               = "enabled"
    http_tokens                 = "required"  # IMDSv2
    http_put_response_hop_limit = 1
  }

  block_device_mappings {
    device_name = "/dev/xvda"
    ebs {
      volume_size           = var.root_volume_size
      volume_type           = "gp3"
      encrypted             = local.enable_encryption
      kms_key_id            = local.enable_encryption ? var.kms_key_id : null
      delete_on_termination = true
    }
  }

  tag_specifications {
    resource_type = "instance"
    tags          = local.common_tags
  }

  tag_specifications {
    resource_type = "volume"
    tags          = local.common_tags
  }

  tags = local.common_tags

  lifecycle {
    create_before_destroy = true
  }
}

#------------------------------------------------------------------------------
# Auto Scaling Group
#------------------------------------------------------------------------------
resource "aws_autoscaling_group" "this" {
  name_prefix         = "${local.name_prefix}-asg-"
  desired_capacity    = var.desired_instances
  min_size            = var.min_instances
  max_size            = var.max_instances
  vpc_zone_identifier = var.vpc_config.subnet_ids
  health_check_type   = "ELB"
  health_check_grace_period = 300

  launch_template {
    id      = aws_launch_template.this.id
    version = "$Latest"
  }

  dynamic "tag" {
    for_each = local.common_tags
    content {
      key                 = tag.key
      value               = tag.value
      propagate_at_launch = true
    }
  }

  lifecycle {
    create_before_destroy = true
    ignore_changes        = [desired_capacity]
  }
}
```

---

## Data Sources

### data.tf Template

```hcl
# data.tf

# Get current AWS account info
data "aws_caller_identity" "current" {}
data "aws_region" "current" {}
data "aws_partition" "current" {}

# Get latest Amazon Linux 2023 AMI
data "aws_ami" "amazon_linux" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["al2023-ami-*-x86_64"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  filter {
    name   = "architecture"
    values = ["x86_64"]
  }
}

# Get VPC info if not provided
data "aws_vpc" "selected" {
  id = var.vpc_config.vpc_id
}

# Get subnet info for AZ distribution
data "aws_subnet" "selected" {
  for_each = toset(var.vpc_config.subnet_ids)
  id       = each.value
}

# Get available AZs
data "aws_availability_zones" "available" {
  state = "available"
  filter {
    name   = "opt-in-status"
    values = ["opt-in-not-required"]
  }
}
```

---

## Output Definitions

### outputs.tf Template

```hcl
# outputs.tf

#------------------------------------------------------------------------------
# Primary Outputs
#------------------------------------------------------------------------------
output "id" {
  description = "The unique identifier for this module instance"
  value       = aws_autoscaling_group.this.id
}

output "name" {
  description = "The name prefix used for all resources"
  value       = local.name_prefix
}

output "arn" {
  description = "ARN of the Auto Scaling Group"
  value       = aws_autoscaling_group.this.arn
}

#------------------------------------------------------------------------------
# Security Group Outputs
#------------------------------------------------------------------------------
output "security_group_id" {
  description = "ID of the security group created for this module"
  value       = aws_security_group.this.id
}

output "security_group_arn" {
  description = "ARN of the security group"
  value       = aws_security_group.this.arn
}

output "security_group_name" {
  description = "Name of the security group"
  value       = aws_security_group.this.name
}

#------------------------------------------------------------------------------
# Launch Template Outputs
#------------------------------------------------------------------------------
output "launch_template_id" {
  description = "ID of the launch template"
  value       = aws_launch_template.this.id
}

output "launch_template_arn" {
  description = "ARN of the launch template"
  value       = aws_launch_template.this.arn
}

output "launch_template_latest_version" {
  description = "Latest version of the launch template"
  value       = aws_launch_template.this.latest_version
}

#------------------------------------------------------------------------------
# Computed/Derived Outputs
#------------------------------------------------------------------------------
output "ami_id" {
  description = "ID of the AMI used for instances"
  value       = data.aws_ami.amazon_linux.id
}

output "availability_zones" {
  description = "List of availability zones where resources are deployed"
  value       = distinct([for s in data.aws_subnet.selected : s.availability_zone])
}

output "configuration" {
  description = "Summary of the module configuration"
  value = {
    environment       = var.environment
    instance_type     = var.instance_type
    min_instances     = var.min_instances
    max_instances     = var.max_instances
    monitoring_enabled = local.monitoring_config.enabled
    encryption_enabled = local.enable_encryption
  }
}

#------------------------------------------------------------------------------
# Sensitive Outputs
#------------------------------------------------------------------------------
output "iam_role_arn" {
  description = "ARN of the IAM role attached to instances"
  value       = aws_iam_role.this.arn
  sensitive   = false
}
```

---

## Conditional Resource Creation

### Using count vs for_each

```hcl
# Use count for simple on/off toggles
resource "aws_cloudwatch_metric_alarm" "high_cpu" {
  count = var.enable_monitoring ? 1 : 0

  alarm_name          = "${local.name_prefix}-high-cpu"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 2
  metric_name         = "CPUUtilization"
  namespace           = "AWS/EC2"
  period              = 300
  statistic           = "Average"
  threshold           = local.monitoring_config.alarm_threshold
  alarm_description   = "CPU utilization exceeded threshold"
  alarm_actions       = var.alarm_actions

  dimensions = {
    AutoScalingGroupName = aws_autoscaling_group.this.name
  }

  tags = local.common_tags
}

# Use for_each for collections
resource "aws_s3_bucket" "logs" {
  for_each = var.enable_logging ? toset(["access", "audit", "error"]) : toset([])

  bucket = "${local.name_prefix}-${each.key}-logs"

  tags = merge(local.common_tags, {
    LogType = each.key
  })
}

# for_each with complex objects
resource "aws_route53_record" "this" {
  for_each = {
    for record in var.dns_records :
    "${record.name}-${record.type}" => record
  }

  zone_id = var.route53_zone_id
  name    = each.value.name
  type    = each.value.type
  ttl     = each.value.ttl
  records = each.value.records
}
```

---

## Module Composition

### Root Module Example

```hcl
# examples/complete/main.tf

terraform {
  required_version = ">= 1.5.0"
}

provider "aws" {
  region = var.region
}

# Network module
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 5.0"

  name = "${var.name}-vpc"
  cidr = "10.0.0.0/16"

  azs             = ["${var.region}a", "${var.region}b", "${var.region}c"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]

  enable_nat_gateway = true
  single_nat_gateway = var.environment != "prod"

  tags = var.tags
}

# Application module
module "app" {
  source = "../../"

  name        = var.name
  environment = var.environment

  vpc_config = {
    vpc_id     = module.vpc.vpc_id
    subnet_ids = module.vpc.private_subnets
  }

  instance_type     = var.instance_type
  min_instances     = var.min_instances
  max_instances     = var.max_instances
  enable_monitoring = true

  ingress_rules = [
    {
      description = "HTTP from ALB"
      from_port   = 80
      to_port     = 80
      protocol    = "tcp"
      security_groups = [module.alb.security_group_id]
    }
  ]

  tags = var.tags
}

# ALB module
module "alb" {
  source  = "terraform-aws-modules/alb/aws"
  version = "~> 8.0"

  name               = "${var.name}-alb"
  load_balancer_type = "application"
  vpc_id             = module.vpc.vpc_id
  subnets            = module.vpc.public_subnets

  target_groups = [
    {
      name             = "${var.name}-tg"
      backend_protocol = "HTTP"
      backend_port     = 80
      target_type      = "instance"
    }
  ]

  tags = var.tags
}

# Outputs
output "vpc_id" {
  value = module.vpc.vpc_id
}

output "app_security_group_id" {
  value = module.app.security_group_id
}

output "alb_dns_name" {
  value = module.alb.lb_dns_name
}
```

---

## Documentation

### README.md Template

```markdown
# Module Name

Brief description of what this module creates.

## Features

- Feature 1
- Feature 2
- Feature 3

## Usage

### Basic

```hcl
module "example" {
  source = "github.com/org/terraform-aws-module?ref=v1.0.0"

  name        = "my-app"
  environment = "prod"

  vpc_config = {
    vpc_id     = "vpc-12345678"
    subnet_ids = ["subnet-1", "subnet-2"]
  }
}
```

### Advanced

```hcl
module "example" {
  source = "github.com/org/terraform-aws-module?ref=v1.0.0"

  name        = "my-app"
  environment = "prod"

  vpc_config = {
    vpc_id             = "vpc-12345678"
    subnet_ids         = ["subnet-1", "subnet-2"]
    security_group_ids = ["sg-existing"]
    assign_public_ip   = false
  }

  instance_type     = "t3.large"
  min_instances     = 3
  max_instances     = 10
  enable_monitoring = true

  ingress_rules = [
    {
      description = "HTTPS"
      from_port   = 443
      to_port     = 443
      protocol    = "tcp"
      cidr_blocks = ["10.0.0.0/8"]
    }
  ]

  tags = {
    Team    = "platform"
    CostCenter = "12345"
  }
}
```

## Requirements

| Name | Version |
|------|---------|
| terraform | >= 1.5.0 |
| aws | >= 5.0.0, < 6.0.0 |

## Providers

| Name | Version |
|------|---------|
| aws | >= 5.0.0 |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| name | Name prefix for resources | `string` | n/a | yes |
| environment | Environment (dev/staging/prod) | `string` | n/a | yes |
| vpc_config | VPC configuration | `object` | n/a | yes |
| instance_type | EC2 instance type | `string` | `"t3.medium"` | no |
| min_instances | Minimum ASG size | `number` | `2` | no |
| max_instances | Maximum ASG size | `number` | `10` | no |

## Outputs

| Name | Description |
|------|-------------|
| id | Auto Scaling Group ID |
| security_group_id | Security Group ID |
| launch_template_id | Launch Template ID |

## License

MIT
```

---

## Лучшие практики

1. **Используй версионирование** — семантическое версионирование для модулей
2. **Валидируй входные переменные** — используй validation blocks
3. **Документируй всё** — описания для variables и outputs
4. **Избегай hardcoded значений** — всё должно быть configurable
5. **Используй for_each вместо count** — лучше управление state
6. **Группируй связанные ресурсы** — логическая организация main.tf
7. **Тестируй модули** — используй terratest или terraform test
8. **Следуй naming conventions** — консистентное именование ресурсов
