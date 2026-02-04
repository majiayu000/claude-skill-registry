---
name: terraform-iac
description: "Infrastructure as Code with Terraform. Use when provisioning cloud resources, managing state, creating modules, or reviewing Terraform configurations."
---

# Terraform Infrastructure as Code

Comprehensive guide for building, managing, and scaling infrastructure with Terraform.

## When to Use

- Provisioning cloud infrastructure (AWS, GCP, Azure, etc.)
- Creating reusable infrastructure modules
- Managing multi-environment deployments
- Reviewing Terraform code for best practices
- Debugging state or plan issues
- Migrating infrastructure between providers

## Core Concepts

### State Management

**Remote State (Required for Teams)**
```hcl
# backend.tf - S3 backend with DynamoDB locking
terraform {
  backend "s3" {
    bucket         = "company-terraform-state"
    key            = "project/environment/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}
```

**State Backend Options:**
| Backend | Use Case | Locking |
|---------|----------|---------|
| S3 + DynamoDB | AWS teams | Yes |
| GCS | GCP teams | Yes |
| Azure Blob | Azure teams | Yes |
| Terraform Cloud | Enterprise/SaaS | Yes |
| Local | Solo dev only | No |

**State Commands:**
```bash
# List resources in state
terraform state list

# Show specific resource
terraform state show aws_instance.web

# Move resource (refactoring)
terraform state mv aws_instance.old aws_instance.new

# Remove from state (not destroy)
terraform state rm aws_instance.imported

# Import existing resource
terraform import aws_instance.web i-1234567890abcdef0
```

### Project Structure

**Standard Module Layout:**
```
project/
├── main.tf              # Primary resources
├── variables.tf         # Input variables
├── outputs.tf           # Output values
├── versions.tf          # Provider versions
├── terraform.tfvars     # Variable values (gitignored)
├── backend.tf           # State configuration
│
├── modules/             # Local modules
│   └── vpc/
│       ├── main.tf
│       ├── variables.tf
│       └── outputs.tf
│
└── environments/        # Environment-specific
    ├── dev/
    │   ├── main.tf      # Calls root module
    │   └── terraform.tfvars
    ├── staging/
    └── prod/
```

**versions.tf (Always Pin Versions)**
```hcl
terraform {
  required_version = ">= 1.6.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.5"
    }
  }
}
```

### Variables & Outputs

**Variable Types:**
```hcl
# variables.tf
variable "environment" {
  description = "Deployment environment"
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
    volume_size   = number
    tags          = map(string)
  })
  default = {
    instance_type = "t3.micro"
    volume_size   = 20
    tags          = {}
  }
}

variable "allowed_cidrs" {
  description = "List of allowed CIDR blocks"
  type        = list(string)
  default     = []
  sensitive   = false
}

variable "db_password" {
  description = "Database password"
  type        = string
  sensitive   = true  # Prevents logging
}
```

**Outputs:**
```hcl
# outputs.tf
output "instance_id" {
  description = "EC2 instance ID"
  value       = aws_instance.web.id
}

output "connection_string" {
  description = "Database connection string"
  value       = "postgresql://${aws_db_instance.main.endpoint}/${aws_db_instance.main.db_name}"
  sensitive   = true
}

output "all_instance_ips" {
  description = "All instance private IPs"
  value       = [for instance in aws_instance.web : instance.private_ip]
}
```

### Resource Patterns

**Conditional Resources:**
```hcl
resource "aws_instance" "bastion" {
  count = var.enable_bastion ? 1 : 0

  ami           = data.aws_ami.amazon_linux.id
  instance_type = "t3.micro"

  tags = {
    Name = "${var.project}-bastion"
  }
}

# Reference conditional resource
output "bastion_ip" {
  value = var.enable_bastion ? aws_instance.bastion[0].public_ip : null
}
```

**for_each (Preferred over count):**
```hcl
variable "instances" {
  type = map(object({
    instance_type = string
    subnet_id     = string
  }))
}

resource "aws_instance" "web" {
  for_each = var.instances

  ami           = data.aws_ami.amazon_linux.id
  instance_type = each.value.instance_type
  subnet_id     = each.value.subnet_id

  tags = {
    Name = "${var.project}-${each.key}"
  }
}
```

**Dynamic Blocks:**
```hcl
resource "aws_security_group" "web" {
  name = "${var.project}-web-sg"

  dynamic "ingress" {
    for_each = var.ingress_rules
    content {
      from_port   = ingress.value.port
      to_port     = ingress.value.port
      protocol    = ingress.value.protocol
      cidr_blocks = ingress.value.cidrs
      description = ingress.value.description
    }
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
```

### Modules

**Creating Reusable Modules:**
```hcl
# modules/vpc/main.tf
resource "aws_vpc" "main" {
  cidr_block           = var.cidr_block
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = merge(var.tags, {
    Name = "${var.name}-vpc"
  })
}

resource "aws_subnet" "public" {
  count = length(var.public_subnets)

  vpc_id                  = aws_vpc.main.id
  cidr_block              = var.public_subnets[count.index]
  availability_zone       = var.availability_zones[count.index]
  map_public_ip_on_launch = true

  tags = merge(var.tags, {
    Name = "${var.name}-public-${count.index + 1}"
    Tier = "Public"
  })
}

# modules/vpc/variables.tf
variable "name" {
  description = "VPC name prefix"
  type        = string
}

variable "cidr_block" {
  description = "VPC CIDR block"
  type        = string
  default     = "10.0.0.0/16"
}

variable "public_subnets" {
  description = "Public subnet CIDR blocks"
  type        = list(string)
  default     = ["10.0.1.0/24", "10.0.2.0/24"]
}

variable "availability_zones" {
  description = "Availability zones"
  type        = list(string)
}

variable "tags" {
  description = "Tags to apply to resources"
  type        = map(string)
  default     = {}
}

# modules/vpc/outputs.tf
output "vpc_id" {
  description = "VPC ID"
  value       = aws_vpc.main.id
}

output "public_subnet_ids" {
  description = "Public subnet IDs"
  value       = aws_subnet.public[*].id
}
```

**Using Modules:**
```hcl
# main.tf
module "vpc" {
  source = "./modules/vpc"

  name               = var.project
  cidr_block         = "10.0.0.0/16"
  public_subnets     = ["10.0.1.0/24", "10.0.2.0/24"]
  availability_zones = ["us-east-1a", "us-east-1b"]

  tags = local.common_tags
}

# Using registry modules
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.0.0"

  name = var.project
  cidr = "10.0.0.0/16"

  azs             = ["us-east-1a", "us-east-1b"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24"]

  enable_nat_gateway = true
  single_nat_gateway = var.environment != "prod"
}
```

### Workspaces

**Environment Isolation:**
```bash
# Create workspaces
terraform workspace new dev
terraform workspace new staging
terraform workspace new prod

# Switch workspace
terraform workspace select prod

# List workspaces
terraform workspace list
```

**Using Workspace in Config:**
```hcl
locals {
  environment = terraform.workspace

  instance_types = {
    dev     = "t3.micro"
    staging = "t3.small"
    prod    = "t3.medium"
  }

  instance_type = local.instance_types[local.environment]
}

resource "aws_instance" "web" {
  instance_type = local.instance_type

  tags = {
    Environment = local.environment
  }
}
```

### Data Sources

**Querying Existing Resources:**
```hcl
# Get latest Amazon Linux 2 AMI
data "aws_ami" "amazon_linux" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }
}

# Get current AWS account
data "aws_caller_identity" "current" {}

# Get available AZs
data "aws_availability_zones" "available" {
  state = "available"
}

# Query existing VPC
data "aws_vpc" "existing" {
  tags = {
    Name = "production-vpc"
  }
}

# Use in resources
resource "aws_instance" "web" {
  ami           = data.aws_ami.amazon_linux.id
  subnet_id     = data.aws_vpc.existing.id
}
```

### Security Best Practices

**1. Never Hardcode Secrets:**
```hcl
# BAD - Never do this
resource "aws_db_instance" "bad" {
  password = "hardcoded-password"  # NO!
}

# GOOD - Use variables
variable "db_password" {
  type      = string
  sensitive = true
}

resource "aws_db_instance" "good" {
  password = var.db_password
}

# BETTER - Use secrets manager
data "aws_secretsmanager_secret_version" "db" {
  secret_id = "prod/db/password"
}

resource "aws_db_instance" "better" {
  password = jsondecode(data.aws_secretsmanager_secret_version.db.secret_string)["password"]
}
```

**2. Encrypt Everything:**
```hcl
resource "aws_s3_bucket" "data" {
  bucket = "${var.project}-data"
}

resource "aws_s3_bucket_server_side_encryption_configuration" "data" {
  bucket = aws_s3_bucket.data.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm     = "aws:kms"
      kms_master_key_id = aws_kms_key.data.arn
    }
  }
}

resource "aws_s3_bucket_public_access_block" "data" {
  bucket = aws_s3_bucket.data.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
```

**3. Least Privilege IAM:**
```hcl
# Specific permissions, not wildcards
resource "aws_iam_policy" "app" {
  name = "${var.project}-app-policy"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject"
        ]
        Resource = "${aws_s3_bucket.data.arn}/*"
      },
      {
        Effect = "Allow"
        Action = [
          "s3:ListBucket"
        ]
        Resource = aws_s3_bucket.data.arn
      }
    ]
  })
}
```

### Workflow Commands

```bash
# Initialize (first time or after backend change)
terraform init

# Format code
terraform fmt -recursive

# Validate syntax
terraform validate

# Plan changes (always review!)
terraform plan -out=tfplan

# Apply from plan file
terraform apply tfplan

# Apply with auto-approve (CI/CD only)
terraform apply -auto-approve  # Dangerous in prod!

# Destroy (careful!)
terraform destroy

# Target specific resource
terraform apply -target=aws_instance.web

# Refresh state from real infrastructure
terraform refresh

# Show current state
terraform show

# Graph dependencies
terraform graph | dot -Tpng > graph.png
```

### Common Patterns

**Tagging Strategy:**
```hcl
locals {
  common_tags = {
    Project     = var.project
    Environment = var.environment
    ManagedBy   = "terraform"
    Owner       = var.owner
    CostCenter  = var.cost_center
  }
}

resource "aws_instance" "web" {
  # ...
  tags = merge(local.common_tags, {
    Name = "${var.project}-web"
    Role = "webserver"
  })
}
```

**Lifecycle Rules:**
```hcl
resource "aws_instance" "web" {
  # ...

  lifecycle {
    create_before_destroy = true  # Zero-downtime updates
    prevent_destroy       = true  # Protect critical resources
    ignore_changes        = [     # Ignore external changes
      tags["LastModified"],
    ]
  }
}
```

**Null Resource for Provisioning:**
```hcl
resource "null_resource" "app_deploy" {
  triggers = {
    version = var.app_version
  }

  provisioner "local-exec" {
    command = "./deploy.sh ${var.app_version}"
  }

  depends_on = [aws_instance.web]
}
```

### Troubleshooting

| Issue | Solution |
|-------|----------|
| State lock stuck | `terraform force-unlock LOCK_ID` |
| Resource drift | `terraform plan` to detect, `terraform apply` to fix |
| Import existing | `terraform import TYPE.NAME ID` |
| Module not found | `terraform init -upgrade` |
| Provider version conflict | Check `versions.tf`, run `terraform init -upgrade` |

### Checklist

Before applying:
- [ ] `terraform fmt` - Code formatted
- [ ] `terraform validate` - Syntax valid
- [ ] `terraform plan` reviewed - No surprises
- [ ] Sensitive values marked `sensitive = true`
- [ ] No hardcoded secrets
- [ ] Resources tagged properly
- [ ] State backend configured (not local)
- [ ] Provider versions pinned

## Integration

Works with:
- `/devops` - Infrastructure automation
- `/aws`, `/gcp`, `/azure` - Cloud-specific patterns
- `/security` - Security review of Terraform code
- `policy-as-code` skill - Terraform compliance checking
