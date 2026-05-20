---
name: terraform
description: HashiCorp Terraform Infrastructure as Code (IaC) tool for provisioning, managing, and versioning cloud infrastructure
version: 1.0.0
category: infrastructure
complexity: comprehensive
when-to-use:
  - "When user mentions 'terraform', 'IaC', or 'infrastructure as code'"
  - "When working with cloud infrastructure provisioning (AWS, Azure, GCP, etc.)"
  - "When managing Terraform state, modules, or providers"
  - "When writing or debugging .tf configuration files"
  - "When planning, applying, or destroying infrastructure"
  - "When importing existing infrastructure into Terraform"
  - "When troubleshooting Terraform errors or state issues"
---

# Terraform Infrastructure as Code Skill

Comprehensive assistance with HashiCorp Terraform for infrastructure provisioning, configuration management, and infrastructure lifecycle automation across cloud providers and on-premises environments.

## When to Use This Skill

**Explicit Triggers:**
- When user says "create terraform configuration", "write terraform code", or "terraform plan/apply"
- When working with `.tf`, `.tfvars`, or `.tfstate` files
- When managing cloud resources (AWS, Azure, GCP, Kubernetes, etc.) declaratively
- When discussing infrastructure state management, modules, or providers
- When importing existing infrastructure or migrating to Terraform
- When debugging Terraform errors, state drift, or dependency issues

**Context Indicators:**
- Mentions of `resource`, `data`, `module`, `provider`, `variable`, `output` blocks
- Infrastructure provisioning workflows (create, update, destroy)
- State management operations (state list, state show, state mv, state rm)
- Module development or registry usage
- Multi-environment infrastructure (dev, staging, production)

## When NOT to Use This Skill

- When writing CloudFormation, Pulumi, or other IaC tools (different syntax/semantics)
- When managing Kubernetes manifests directly (use kubectl or Helm skills)
- When writing Ansible playbooks (configuration management, not IaC)
- When using Terraform Cloud/Enterprise (platform-specific features)
- When working with Terraform CDK (TypeScript/Python abstraction layer)

## Prerequisites

### Knowledge Requirements
- Understanding of target infrastructure platform (AWS, Azure, GCP, etc.)
- Basic networking concepts (VPC, subnets, security groups, load balancers)
- Resource dependencies and lifecycle management
- State management and locking concepts

### Environment Setup
- Terraform CLI installed (`terraform version` ≥ 1.0)
- Cloud provider credentials configured (AWS CLI, Azure CLI, gcloud, etc.)
- Backend configured for state storage (S3, Azure Storage, Terraform Cloud)
- Version control system (Git) for `.tf` files

### Project Structure
```
terraform-project/
├── main.tf              # Primary resource definitions
├── variables.tf         # Input variable declarations
├── outputs.tf           # Output value definitions
├── terraform.tfvars     # Variable values (gitignored if sensitive)
├── versions.tf          # Terraform and provider version constraints
├── backend.tf           # State backend configuration
└── modules/             # Reusable module definitions
    └── networking/
        ├── main.tf
        ├── variables.tf
        └── outputs.tf
```

## Core Terraform Workflow

### Step 1: Initialize Terraform
```bash
# Download providers and initialize backend
terraform init

# Reinitialize if backend config changes
terraform init -reconfigure

# Upgrade providers to latest versions
terraform init -upgrade
```

**What happens:**
- Downloads provider plugins (AWS, Azure, GCP, etc.)
- Initializes backend for state storage
- Creates `.terraform/` directory and lock file

### Step 2: Write Configuration

**Resource Block** (creates infrastructure):
```hcl
resource "aws_instance" "web_server" {
  ami           = var.ami_id
  instance_type = var.instance_type

  tags = {
    Name        = "web-server-${var.environment}"
    Environment = var.environment
    ManagedBy   = "Terraform"
  }

  # Lifecycle management
  lifecycle {
    create_before_destroy = true
    prevent_destroy       = false
  }
}
```

**Data Source** (queries existing infrastructure):
```hcl
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"] # Canonical

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }
}
```

**Variable Declaration**:
```hcl
variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.micro"

  validation {
    condition     = contains(["t3.micro", "t3.small", "t3.medium"], var.instance_type)
    error_message = "Instance type must be t3.micro, t3.small, or t3.medium."
  }
}
```

**Output Values**:
```hcl
output "instance_public_ip" {
  description = "Public IP address of the web server"
  value       = aws_instance.web_server.public_ip
  sensitive   = false
}
```

### Step 3: Plan Changes
```bash
# Preview infrastructure changes
terraform plan

# Save plan to file for review
terraform plan -out=tfplan

# Plan for specific target resource
terraform plan -target=aws_instance.web_server

# Show plan with variable values
terraform plan -var="environment=production"
```

**Plan Output Analysis:**
- `+` = Resource will be created
- `-` = Resource will be destroyed
- `~` = Resource will be modified in-place
- `-/+` = Resource will be destroyed and recreated
- `<=` = Data source will be read

### Step 4: Apply Changes
```bash
# Apply changes (requires confirmation)
terraform apply

# Apply saved plan (no confirmation needed)
terraform apply tfplan

# Auto-approve (use with caution)
terraform apply -auto-approve

# Apply with variable overrides
terraform apply -var="instance_type=t3.small"
```

### Step 5: Verify and Inspect
```bash
# List all resources in state
terraform state list

# Show detailed resource state
terraform state show aws_instance.web_server

# Show all outputs
terraform output

# Show specific output value
terraform output instance_public_ip
```

### Step 6: Destroy Infrastructure
```bash
# Destroy all managed infrastructure
terraform destroy

# Destroy specific resource
terraform destroy -target=aws_instance.web_server

# Preview destruction plan
terraform plan -destroy
```

## Advanced Terraform Patterns

### Module Usage

**Calling a Module**:
```hcl
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 5.0"

  name = "my-vpc"
  cidr = "10.0.0.0/16"

  azs             = ["us-west-2a", "us-west-2b", "us-west-2c"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]

  enable_nat_gateway = true
  enable_vpn_gateway = false

  tags = {
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}

# Reference module outputs
resource "aws_instance" "app" {
  subnet_id = module.vpc.private_subnets[0]
  # ...
}
```

**Creating a Module** (`modules/compute/main.tf`):
```hcl
variable "instance_count" {
  type    = number
  default = 1
}

variable "subnet_ids" {
  type = list(string)
}

resource "aws_instance" "this" {
  count = var.instance_count

  ami           = data.aws_ami.ubuntu.id
  instance_type = "t3.micro"
  subnet_id     = element(var.subnet_ids, count.index)

  tags = {
    Name = "instance-${count.index + 1}"
  }
}

output "instance_ids" {
  value = aws_instance.this[*].id
}
```

### Dynamic Blocks
```hcl
resource "aws_security_group" "this" {
  name   = "web-sg"
  vpc_id = var.vpc_id

  dynamic "ingress" {
    for_each = var.ingress_rules
    content {
      from_port   = ingress.value.from_port
      to_port     = ingress.value.to_port
      protocol    = ingress.value.protocol
      cidr_blocks = ingress.value.cidr_blocks
    }
  }
}
```

### For Each and Count

**for_each** (map or set):
```hcl
resource "aws_s3_bucket" "this" {
  for_each = toset(var.bucket_names)

  bucket = each.value

  tags = {
    Name = each.value
  }
}
```

**count** (numeric iteration):
```hcl
resource "aws_instance" "web" {
  count = var.instance_count

  ami           = var.ami_id
  instance_type = var.instance_type

  tags = {
    Name = "web-${count.index + 1}"
  }
}
```

### Conditional Resources
```hcl
resource "aws_eip" "this" {
  count = var.create_eip ? 1 : 0

  instance = aws_instance.web.id
  domain   = "vpc"
}
```

### Dependencies

**Implicit Dependencies** (automatic):
```hcl
resource "aws_instance" "web" {
  subnet_id = aws_subnet.main.id  # Implicit dependency
}
```

**Explicit Dependencies** (`depends_on`):
```hcl
resource "aws_instance" "web" {
  # ...

  depends_on = [
    aws_security_group.allow_web,
    aws_subnet.main
  ]
}
```

## State Management

### State Commands
```bash
# List resources in state
terraform state list

# Show resource details
terraform state show aws_instance.web_server

# Move resource to different address
terraform state mv aws_instance.old aws_instance.new

# Remove resource from state (doesn't destroy)
terraform state rm aws_instance.decommissioned

# Pull remote state to local file
terraform state pull > terraform.tfstate.backup

# Push local state to remote backend
terraform state push terraform.tfstate
```

### Remote State Backend (S3 + DynamoDB)
```hcl
terraform {
  backend "s3" {
    bucket         = "my-terraform-state"
    key            = "prod/terraform.tfstate"
    region         = "us-west-2"
    encrypt        = true
    dynamodb_table = "terraform-lock"
  }
}
```

### State Locking
- **Prevents concurrent modifications** (race conditions)
- **DynamoDB table** (AWS), **Azure Storage**, or **Consul** for locking
- **Force unlock** if lock stuck: `terraform force-unlock <lock-id>`

### State Drift Detection
```bash
# Detect drift between state and real infrastructure
terraform plan -refresh-only

# Apply drift detection (update state without changes)
terraform apply -refresh-only
```

## Importing Existing Infrastructure

### Import Workflow
```bash
# Step 1: Write resource configuration (without computed attributes)
cat > imported.tf <<'EOF'
resource "aws_instance" "imported_server" {
  # ami and instance_type will be populated after import
}
EOF

# Step 2: Import existing resource into state
terraform import aws_instance.imported_server i-1234567890abcdef0

# Step 3: Run plan to see differences
terraform plan

# Step 4: Update configuration to match actual infrastructure
# (Copy values from plan output)

# Step 5: Verify no changes needed
terraform plan  # Should show "No changes"
```

### Bulk Import with Generated Code
```bash
# Generate configuration from existing resources (Terraform 1.5+)
terraform plan -generate-config-out=generated.tf

# Review and edit generated configuration
code generated.tf

# Apply to sync state
terraform apply
```

## Provider Configuration

### Multiple Provider Instances (Aliases)
```hcl
provider "aws" {
  region = "us-west-2"
}

provider "aws" {
  alias  = "east"
  region = "us-east-1"
}

resource "aws_instance" "west" {
  provider = aws  # Default provider
  # ...
}

resource "aws_instance" "east" {
  provider = aws.east  # Aliased provider
  # ...
}
```

### Provider Version Constraints
```hcl
terraform {
  required_version = ">= 1.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"  # >= 5.0, < 6.0
    }
    random = {
      source  = "hashicorp/random"
      version = ">= 3.5.0"
    }
  }
}
```

## Functions and Expressions

### Common Built-in Functions

**String Functions**:
```hcl
# String interpolation
name = "server-${var.environment}-${var.region}"

# String manipulation
upper("hello")          # "HELLO"
lower("WORLD")          # "world"
title("hello world")    # "Hello World"
trimspace("  text  ")   # "text"
format("instance-%03d", 5)  # "instance-005"
```

**Collection Functions**:
```hcl
# List operations
length([1, 2, 3])              # 3
concat([1, 2], [3, 4])         # [1, 2, 3, 4]
element(["a", "b", "c"], 1)    # "b"
contains(["a", "b"], "a")      # true
distinct([1, 2, 2, 3])         # [1, 2, 3]

# Map operations
merge({a = 1}, {b = 2})        # {a = 1, b = 2}
keys({a = 1, b = 2})           # ["a", "b"]
values({a = 1, b = 2})         # [1, 2]
lookup({a = 1}, "b", "default") # "default"
```

**Type Conversion**:
```hcl
tostring(42)           # "42"
tonumber("42")         # 42
tobool("true")         # true
tolist(toset([1, 2]))  # [1, 2]
tomap({a = 1})         # {a = 1}
```

**Filesystem Functions**:
```hcl
file("${path.module}/userdata.sh")          # Read file content
templatefile("${path.module}/config.tpl", { # Render template
  port = 8080
})
fileexists("${path.module}/optional.txt")   # true/false
```

**Date/Time**:
```hcl
timestamp()                        # "2025-12-31T12:00:00Z"
formatdate("YYYY-MM-DD", timestamp()) # "2025-12-31"
```

### Conditional Expressions
```hcl
# Ternary operator
instance_type = var.environment == "prod" ? "t3.large" : "t3.micro"

# Null coalescing
ami_id = var.custom_ami != "" ? var.custom_ami : data.aws_ami.default.id
```

### For Expressions
```hcl
# Transform list
instance_names = [for i in aws_instance.web : i.tags.Name]

# Transform map
instance_ips = {for k, v in aws_instance.web : k => v.private_ip}

# Filter with condition
prod_instances = [for i in aws_instance.all : i if i.tags.Environment == "prod"]
```

### Splat Expressions
```hcl
# Equivalent to: [for i in aws_instance.web : i.id]
instance_ids = aws_instance.web[*].id

# With nested attributes
subnet_ids = aws_subnet.private[*].id
```

## Workspaces (Multi-Environment)

### Workspace Commands
```bash
# List workspaces
terraform workspace list

# Create new workspace
terraform workspace new staging

# Switch workspace
terraform workspace select production

# Show current workspace
terraform workspace show

# Delete workspace
terraform workspace delete dev
```

### Workspace-Aware Configuration
```hcl
resource "aws_instance" "web" {
  instance_type = terraform.workspace == "prod" ? "t3.large" : "t3.micro"

  tags = {
    Environment = terraform.workspace
    Name        = "web-${terraform.workspace}"
  }
}
```

## Troubleshooting Common Issues

### Issue 1: Provider Authentication Errors
```
Error: error configuring Terraform AWS Provider: no valid credential sources
```

**Solution**:
```bash
# Set AWS credentials
export AWS_ACCESS_KEY_ID="your-access-key"
export AWS_SECRET_ACCESS_KEY="your-secret-key"
export AWS_DEFAULT_REGION="us-west-2"

# Or use AWS CLI profile
export AWS_PROFILE="terraform"

# Verify credentials
aws sts get-caller-identity
```

### Issue 2: State Lock Errors
```
Error: Error acquiring the state lock
```

**Solution**:
```bash
# Check who holds the lock in DynamoDB table
aws dynamodb get-item --table-name terraform-lock --key '{"LockID": {"S": "my-state-file"}}'

# Force unlock (use with caution)
terraform force-unlock <lock-id>
```

### Issue 3: Resource Already Exists
```
Error: creating EC2 Instance: InvalidParameterValue: Instance already exists
```

**Solution**:
```bash
# Import existing resource
terraform import aws_instance.web i-1234567890abcdef0

# Or remove from state if managed elsewhere
terraform state rm aws_instance.web
```

### Issue 4: Dependency Cycle
```
Error: Cycle: aws_security_group.app -> aws_instance.web -> aws_security_group.app
```

**Solution**:
```hcl
# Break cycle by removing circular dependency
# Option 1: Use separate ingress rules
resource "aws_security_group_rule" "app_to_web" {
  type                     = "ingress"
  security_group_id        = aws_security_group.web.id
  source_security_group_id = aws_security_group.app.id
  from_port                = 80
  to_port                  = 80
  protocol                 = "tcp"
}
```

### Issue 5: Missing Required Argument
```
Error: Missing required argument: subnet_id
```

**Solution**:
```hcl
# Add missing required argument
resource "aws_instance" "web" {
  ami           = var.ami_id
  instance_type = var.instance_type
  subnet_id     = aws_subnet.main.id  # Add this
}
```

## Best Practices

### Code Organization
✅ **DO:**
- Use consistent naming conventions (`snake_case` for resources, `kebab-case` for files)
- Group related resources in same file (networking.tf, compute.tf, storage.tf)
- Use modules for reusable components
- Pin provider versions in `versions.tf`
- Store sensitive values in `.tfvars` (gitignored) or use secrets manager

❌ **DON'T:**
- Hardcode values (use variables)
- Mix resource types in single file (poor organization)
- Use `count` and `for_each` on same resource
- Skip documentation (use `description` fields)
- Commit `.tfvars` files with secrets

### State Management
✅ **DO:**
- Use remote backend (S3, Azure Storage, Terraform Cloud)
- Enable state locking (DynamoDB, Azure Storage)
- Enable state encryption (`encrypt = true`)
- Use separate states for different environments
- Back up state regularly

❌ **DON'T:**
- Edit state files manually
- Commit state files to version control
- Share state files insecurely
- Use local state for production

### Security
✅ **DO:**
- Use least-privilege IAM policies
- Enable encryption (EBS, S3, RDS)
- Use security groups/network ACLs restrictively
- Rotate credentials regularly
- Use AWS Secrets Manager/Parameter Store for secrets

❌ **DON'T:**
- Hardcode credentials in `.tf` files
- Use overly permissive security rules (0.0.0.0/0)
- Commit `.tfvars` with sensitive data
- Disable encryption to simplify config

### Version Control
✅ **DO:**
- Commit all `.tf` files
- Commit `.terraform.lock.hcl` (provider version locking)
- Use `.gitignore` for sensitive files
- Use feature branches for changes
- Review plans before applying

❌ **DON'T:**
- Commit `.terraform/` directory
- Commit `terraform.tfstate` or `.tfvars` with secrets
- Apply changes without peer review
- Skip `terraform plan` before `apply`

## Examples

### Example 1: AWS VPC with Public/Private Subnets

**Scenario**: Create production-grade VPC with high availability across 3 AZs.

**main.tf**:
```hcl
terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name        = "${var.project}-vpc"
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}

resource "aws_subnet" "public" {
  count = length(var.public_subnet_cidrs)

  vpc_id                  = aws_vpc.main.id
  cidr_block              = var.public_subnet_cidrs[count.index]
  availability_zone       = data.aws_availability_zones.available.names[count.index]
  map_public_ip_on_launch = true

  tags = {
    Name = "${var.project}-public-${count.index + 1}"
    Type = "public"
  }
}

resource "aws_subnet" "private" {
  count = length(var.private_subnet_cidrs)

  vpc_id            = aws_vpc.main.id
  cidr_block        = var.private_subnet_cidrs[count.index]
  availability_zone = data.aws_availability_zones.available.names[count.index]

  tags = {
    Name = "${var.project}-private-${count.index + 1}"
    Type = "private"
  }
}

resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "${var.project}-igw"
  }
}

resource "aws_eip" "nat" {
  count  = length(var.public_subnet_cidrs)
  domain = "vpc"

  tags = {
    Name = "${var.project}-nat-eip-${count.index + 1}"
  }
}

resource "aws_nat_gateway" "main" {
  count = length(var.public_subnet_cidrs)

  allocation_id = aws_eip.nat[count.index].id
  subnet_id     = aws_subnet.public[count.index].id

  tags = {
    Name = "${var.project}-nat-${count.index + 1}"
  }

  depends_on = [aws_internet_gateway.main]
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }

  tags = {
    Name = "${var.project}-public-rt"
  }
}

resource "aws_route_table" "private" {
  count  = length(var.private_subnet_cidrs)
  vpc_id = aws_vpc.main.id

  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.main[count.index].id
  }

  tags = {
    Name = "${var.project}-private-rt-${count.index + 1}"
  }
}

resource "aws_route_table_association" "public" {
  count = length(var.public_subnet_cidrs)

  subnet_id      = aws_subnet.public[count.index].id
  route_table_id = aws_route_table.public.id
}

resource "aws_route_table_association" "private" {
  count = length(var.private_subnet_cidrs)

  subnet_id      = aws_subnet.private[count.index].id
  route_table_id = aws_route_table.private[count.index].id
}

data "aws_availability_zones" "available" {
  state = "available"
}
```

**variables.tf**:
```hcl
variable "aws_region" {
  description = "AWS region for resources"
  type        = string
  default     = "us-west-2"
}

variable "project" {
  description = "Project name for resource naming"
  type        = string
}

variable "environment" {
  description = "Environment (dev, staging, prod)"
  type        = string
}

variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "public_subnet_cidrs" {
  description = "CIDR blocks for public subnets"
  type        = list(string)
  default     = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
}

variable "private_subnet_cidrs" {
  description = "CIDR blocks for private subnets"
  type        = list(string)
  default     = ["10.0.11.0/24", "10.0.12.0/24", "10.0.13.0/24"]
}
```

**outputs.tf**:
```hcl
output "vpc_id" {
  description = "VPC ID"
  value       = aws_vpc.main.id
}

output "public_subnet_ids" {
  description = "Public subnet IDs"
  value       = aws_subnet.public[*].id
}

output "private_subnet_ids" {
  description = "Private subnet IDs"
  value       = aws_subnet.private[*].id
}

output "nat_gateway_ips" {
  description = "NAT Gateway public IPs"
  value       = aws_eip.nat[*].public_ip
}
```

**terraform.tfvars**:
```hcl
project     = "myapp"
environment = "production"
aws_region  = "us-west-2"
```

**Execution**:
```bash
terraform init
terraform plan -out=tfplan
terraform apply tfplan
```

**Rationale**: This example demonstrates production-grade networking with high availability, proper routing, and NAT gateways for private subnet internet access.

### Example 2: Auto Scaling Web Application

**Scenario**: Deploy web application with auto-scaling, load balancer, and RDS database.

**compute.tf**:
```hcl
resource "aws_launch_template" "web" {
  name_prefix   = "${var.project}-web-"
  image_id      = data.aws_ami.amazon_linux_2.id
  instance_type = var.instance_type

  vpc_security_group_ids = [aws_security_group.web.id]

  user_data = base64encode(templatefile("${path.module}/userdata.sh", {
    db_endpoint = aws_db_instance.main.endpoint
    app_version = var.app_version
  }))

  iam_instance_profile {
    name = aws_iam_instance_profile.web.name
  }

  monitoring {
    enabled = true
  }

  tag_specifications {
    resource_type = "instance"
    tags = {
      Name = "${var.project}-web"
      Environment = var.environment
    }
  }
}

resource "aws_autoscaling_group" "web" {
  name                = "${var.project}-web-asg"
  vpc_zone_identifier = var.private_subnet_ids
  target_group_arns   = [aws_lb_target_group.web.arn]
  health_check_type   = "ELB"
  min_size            = var.asg_min_size
  max_size            = var.asg_max_size
  desired_capacity    = var.asg_desired_capacity

  launch_template {
    id      = aws_launch_template.web.id
    version = "$Latest"
  }

  tag {
    key                 = "Name"
    value               = "${var.project}-web-asg"
    propagate_at_launch = true
  }
}

resource "aws_autoscaling_policy" "scale_up" {
  name                   = "${var.project}-scale-up"
  autoscaling_group_name = aws_autoscaling_group.web.name
  adjustment_type        = "ChangeInCapacity"
  scaling_adjustment     = 1
  cooldown               = 300
}

resource "aws_cloudwatch_metric_alarm" "high_cpu" {
  alarm_name          = "${var.project}-high-cpu"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 2
  metric_name         = "CPUUtilization"
  namespace           = "AWS/EC2"
  period              = 120
  statistic           = "Average"
  threshold           = 80

  dimensions = {
    AutoScalingGroupName = aws_autoscaling_group.web.name
  }

  alarm_actions = [aws_autoscaling_policy.scale_up.arn]
}

resource "aws_lb" "web" {
  name               = "${var.project}-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb.id]
  subnets            = var.public_subnet_ids

  enable_deletion_protection = var.environment == "prod" ? true : false
}

resource "aws_lb_target_group" "web" {
  name     = "${var.project}-web-tg"
  port     = 80
  protocol = "HTTP"
  vpc_id   = var.vpc_id

  health_check {
    enabled             = true
    healthy_threshold   = 2
    unhealthy_threshold = 2
    timeout             = 5
    interval            = 30
    path                = "/health"
    matcher             = "200"
  }
}

resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.web.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.web.arn
  }
}
```

**database.tf**:
```hcl
resource "aws_db_subnet_group" "main" {
  name       = "${var.project}-db-subnet-group"
  subnet_ids = var.private_subnet_ids
}

resource "aws_db_instance" "main" {
  identifier           = "${var.project}-db"
  engine               = "postgres"
  engine_version       = "15.4"
  instance_class       = var.db_instance_class
  allocated_storage    = var.db_allocated_storage
  storage_encrypted    = true

  db_name  = var.db_name
  username = var.db_username
  password = var.db_password  # Use AWS Secrets Manager in production

  db_subnet_group_name   = aws_db_subnet_group.main.name
  vpc_security_group_ids = [aws_security_group.db.id]

  backup_retention_period = var.environment == "prod" ? 7 : 1
  backup_window           = "03:00-04:00"
  maintenance_window      = "mon:04:00-mon:05:00"

  skip_final_snapshot = var.environment != "prod"

  tags = {
    Name        = "${var.project}-db"
    Environment = var.environment
  }
}
```

**Rationale**: Demonstrates auto-scaling patterns, load balancing, health checks, and RDS integration for production workloads.

### Example 3: Multi-Region Disaster Recovery

**Scenario**: Deploy application in two regions with Route53 failover.

**main.tf** (us-west-2):
```hcl
module "primary_region" {
  source = "./modules/regional-stack"

  providers = {
    aws = aws.primary
  }

  region      = "us-west-2"
  is_primary  = true
  project     = var.project
  environment = var.environment
}

module "secondary_region" {
  source = "./modules/regional-stack"

  providers = {
    aws = aws.secondary
  }

  region      = "us-east-1"
  is_primary  = false
  project     = var.project
  environment = var.environment
}

resource "aws_route53_zone" "main" {
  name = var.domain_name
}

resource "aws_route53_record" "primary" {
  zone_id = aws_route53_zone.main.zone_id
  name    = var.domain_name
  type    = "A"

  set_identifier = "primary"

  failover_routing_policy {
    type = "PRIMARY"
  }

  alias {
    name                   = module.primary_region.alb_dns_name
    zone_id                = module.primary_region.alb_zone_id
    evaluate_target_health = true
  }

  health_check_id = aws_route53_health_check.primary.id
}

resource "aws_route53_record" "secondary" {
  zone_id = aws_route53_zone.main.zone_id
  name    = var.domain_name
  type    = "A"

  set_identifier = "secondary"

  failover_routing_policy {
    type = "SECONDARY"
  }

  alias {
    name                   = module.secondary_region.alb_dns_name
    zone_id                = module.secondary_region.alb_zone_id
    evaluate_target_health = true
  }
}

resource "aws_route53_health_check" "primary" {
  fqdn              = module.primary_region.alb_dns_name
  port              = 80
  type              = "HTTP"
  resource_path     = "/health"
  failure_threshold = 3
  request_interval  = 30
}
```

**Rationale**: Multi-region deployment with automatic DNS failover for high availability and disaster recovery.

## Quality Standards

**Configuration Quality:**
- [ ] All resources have meaningful names and tags
- [ ] Variables use descriptive names and include descriptions
- [ ] Outputs document what values they expose
- [ ] Provider versions are pinned
- [ ] Remote backend is configured for production
- [ ] State locking is enabled
- [ ] Sensitive values use `sensitive = true`

**Code Organization:**
- [ ] Related resources grouped in logical files
- [ ] Modules used for reusable components
- [ ] Consistent naming conventions followed
- [ ] No hardcoded values (use variables)
- [ ] Comments explain complex logic

**Security:**
- [ ] IAM policies follow least privilege
- [ ] Encryption enabled for data at rest/transit
- [ ] Security groups are restrictive
- [ ] No credentials in code
- [ ] `.tfvars` with secrets not committed

**Operational:**
- [ ] `terraform plan` shows expected changes
- [ ] No state drift detected
- [ ] Destroy plan reviewed before execution
- [ ] Backup strategy defined
- [ ] Rollback procedure documented

## Common Pitfalls

❌ **Using `count` with for_each**
```hcl
# ERROR: Cannot use both
resource "aws_instance" "web" {
  count    = var.instance_count
  for_each = toset(var.instance_names)
}
```

✅ **Choose one iteration method**
```hcl
resource "aws_instance" "web" {
  for_each = toset(var.instance_names)
  # ...
}
```

❌ **Editing state files manually**
```bash
# DON'T: Edit terraform.tfstate directly
vim terraform.tfstate
```

✅ **Use state commands**
```bash
# DO: Use terraform state commands
terraform state rm aws_instance.old
terraform state mv aws_instance.old aws_instance.new
```

❌ **Hardcoding credentials**
```hcl
# DON'T: Embed secrets
resource "aws_db_instance" "main" {
  password = "MySecretPassword123!"
}
```

✅ **Use secrets management**
```hcl
# DO: Reference secrets from external store
data "aws_secretsmanager_secret_version" "db_password" {
  secret_id = "prod/db/password"
}

resource "aws_db_instance" "main" {
  password = data.aws_secretsmanager_secret_version.db_password.secret_string
}
```

❌ **Circular dependencies**
```hcl
# ERROR: A depends on B, B depends on A
resource "aws_security_group" "a" {
  ingress {
    security_groups = [aws_security_group.b.id]
  }
}

resource "aws_security_group" "b" {
  ingress {
    security_groups = [aws_security_group.a.id]
  }
}
```

✅ **Break cycle with separate rules**
```hcl
resource "aws_security_group" "a" {}
resource "aws_security_group" "b" {}

resource "aws_security_group_rule" "a_to_b" {
  security_group_id        = aws_security_group.a.id
  source_security_group_id = aws_security_group.b.id
}

resource "aws_security_group_rule" "b_to_a" {
  security_group_id        = aws_security_group.b.id
  source_security_group_id = aws_security_group.a.id
}
```

## Integration with Command & Control System

**Related Skills:**
- **aws-skill**: Cloud-specific AWS operations and best practices
- **kubernetes-skill**: Container orchestration (often Terraform-provisioned)
- **git-workflow-skill**: Version control for `.tf` files
- **ci-cd-skill**: Automated Terraform pipelines

**Related Commands:**
- `/infrastructure-plan`: Generate Terraform plan with architecture review
- `/infrastructure-apply`: Execute Terraform changes with approval gates
- `/state-audit`: Analyze Terraform state for drift and anomalies

**MCP Dependencies:**
- **AWS MCP Server**: Cloud provider integration for resource queries
- **GitHub MCP Server**: Version control for infrastructure code
- **Secrets MCP Server**: Secure credential management

**Orchestration Notes:**
- Can be chained with `aws-skill` for post-provisioning configuration
- Invoked by `infrastructure-orchestrator` for multi-stage deployments
- Outputs used as inputs for `kubernetes-skill` cluster configuration

## Version History

- **1.0.0** (2025-12-31): Initial comprehensive skill release
  - Full Terraform workflow coverage (init, plan, apply, destroy)
  - State management and remote backends
  - Module patterns and advanced features
  - Multi-region deployment examples
  - Troubleshooting guide
  - Best practices and security guidelines

## Resources

### Official Documentation
- [Terraform Documentation](https://developer.hashicorp.com/terraform/docs)
- [Terraform Registry](https://registry.terraform.io/)
- [Terraform Language Reference](https://developer.hashicorp.com/terraform/language)
- [Terraform CLI Commands](https://developer.hashicorp.com/terraform/cli)

### Learning Resources
- [HashiCorp Learn](https://learn.hashicorp.com/terraform)
- [Terraform Best Practices](https://www.terraform-best-practices.com/)
- [AWS Terraform Examples](https://github.com/hashicorp/terraform-provider-aws/tree/main/examples)

### Community
- [Terraform Discuss](https://discuss.hashicorp.com/c/terraform-core)
- [Terraform GitHub](https://github.com/hashicorp/terraform)
- [r/Terraform](https://www.reddit.com/r/Terraform/)

## Updating This Skill

To refresh with latest Terraform features:
```bash
# Update config with new documentation sections
vim configs/terraform.json

# Regenerate skill
skill-seekers scrape --config configs/terraform.json

# Review and merge updates
diff output/terraform/SKILL.md INTEGRATION/incoming/terraform/SKILL.md
```

---

**Skill Status**: ✅ Production Ready
**Terraform Versions Supported**: 1.0+
**Last Updated**: December 31, 2025
**Maintained By**: Claude Command & Control Team
