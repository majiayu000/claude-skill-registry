---
name: opentofu-aws-explorer
description: Explore and manage AWS cloud infrastructure resources using OpenTofu/Terraform
license: Apache-2.0
compatibility: opencode
metadata:
  audience: developers
  workflow: cloud-infrastructure
---

# OpenTofu AWS Explorer

## What I do

I guide you through managing Amazon Web Services (AWS) infrastructure using the AWS provider for OpenTofu/Terraform. I help you:

- **Compute Resources**: Manage EC2, Lambda, ECS, and container resources
- **Networking**: Create VPCs, subnets, route tables, and security groups
- **Storage**: Configure S3, EBS, EFS, and file systems
- **Databases**: Setup RDS, DynamoDB, ElastiCache, and Redshift
- **Security**: Implement IAM, KMS, Security Groups, and WAF
- **Best Practices**: Follow AWS Well-Architected Framework and provider documentation

## When to use me

Use this skill when you need to:
- Provision AWS infrastructure as code
- Automate AWS resource creation and management
- Implement multi-tier architectures (web, app, data)
- Setup secure networking and VPC configurations
- Manage IAM roles, policies, and security groups
- Configure AWS services for production workloads
- Implement AWS best practices and governance

**Note**: OpenTofu and Terraform are used interchangeably throughout this skill. OpenTofu is an open-source implementation of Terraform and maintains full compatibility with Terraform providers.

## Prerequisites

- **OpenTofu CLI installed**: Install from https://opentofu.org/docs/intro/install/
- **AWS Account**: Valid AWS account with appropriate permissions
- **AWS Credentials**: Access keys or IAM role for authentication
- **Basic AWS Knowledge**: Understanding of AWS services and concepts

## Provider Documentation

- **Terraform Registry (AWS Provider)**: https://registry.terraform.io/providers/hashicorp/aws/latest/docs
- **Latest Provider Version**: hashicorp/aws ~> 5.0.0
- **Provider Source**: https://github.com/hashicorp/terraform-provider-aws
- **AWS Well-Architected Framework**: https://docs.aws.amazon.com/wellarchitected/

## Steps

### Step 1: Install and Configure OpenTofu

```bash
# Verify OpenTofu installation
tofu version

# Initialize project
mkdir aws-terraform
cd aws-terraform
tofu init
```

### Step 2: Configure AWS Provider

Create `versions.tf`:

```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0.0"
    }
  }
  required_version = ">= 1.0"

  # Remote state backend
  backend "s3" {
    bucket         = "terraform-state"
    key            = "prod/terraform.tfstate"
    region         = "ap-southeast-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}
```

### Step 3: Configure AWS Authentication

Create `provider.tf`:

```hcl
provider "aws" {
  region = var.aws_region

  # Method 1: Access Keys (environment variables)
  # AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY
  # Best for development and testing

  # Method 2: Shared Credentials File
  # ~/.aws/credentials with profiles
  # Best for multiple AWS accounts

  # Method 3: IAM Role (recommended for production)
  # assume_role {
  #   role_arn = "arn:aws:iam::123456789012:role/TerraformRole"
  #   session_name = "terraform-session"
  #   external_id = "external-id"
  # }

  # Method 4: Assume Role with MFA
  # assume_role {
  #   role_arn = "arn:aws:iam::123456789012:role/TerraformRole"
  #   mfa_serial = "arn:aws:iam::123456789012:mfa/user"
  # }

  # Default tags (applied to all resources)
  default_tags {
    tags = {
      ManagedBy  = "Terraform"
      Project    = var.project_name
      Environment = var.environment
    }
  }
}
```

### Step 4: Configure Environment Variables

```bash
# Method 1: Environment variables (recommended)
export AWS_ACCESS_KEY_ID="AKIAIOSFODNN7EXAMPLE"
export AWS_SECRET_ACCESS_KEY="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
export AWS_DEFAULT_REGION="ap-southeast-1"

# Method 2: AWS CLI profile
export AWS_PROFILE="my-profile"

# Method 3: Using AWS Vault (best for security)
# https://github.com/99designs/aws-vault
aws-vault exec terraform-role -- tofu plan
```

### Step 5: Create VPC Networking

Create `networking.tf`:

```hcl
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

# Public Subnets (2 AZs for HA)
resource "aws_subnet" "public" {
  count                   = 2
  vpc_id                  = aws_vpc.main.id
  cidr_block              = cidrsubnet(var.vpc_cidr, 8, count.index)
  availability_zone       = data.aws_availability_zones.available.names[count.index]
  map_public_ip_on_launch = true

  tags = {
    Name = "${var.project_name}-public-subnet-${count.index + 1}"
    Type = "Public"
  }
}

# Private Subnets (2 AZs for HA)
resource "aws_subnet" "private" {
  count             = 2
  vpc_id            = aws_vpc.main.id
  cidr_block        = cidrsubnet(var.vpc_cidr, 8, count.index + 2)
  availability_zone = data.aws_availability_zones.available.names[count.index]

  tags = {
    Name = "${var.project_name}-private-subnet-${count.index + 1}"
    Type = "Private"
  }
}

# Database Subnets (2 AZs for HA)
resource "aws_subnet" "database" {
  count             = 2
  vpc_id            = aws_vpc.main.id
  cidr_block        = cidrsubnet(var.vpc_cidr, 8, count.index + 4)
  availability_zone = data.aws_availability_zones.available.names[count.index]

  tags = {
    Name = "${var.project_name}-database-subnet-${count.index + 1}"
    Type = "Database"
  }
}

# EIP for NAT Gateway
resource "aws_eip" "nat" {
  count = 2
  domain = "vpc"

  tags = {
    Name = "${var.project_name}-nat-eip-${count.index + 1}"
  }

  depends_on = [aws_internet_gateway.main]
}

# NAT Gateways
resource "aws_nat_gateway" "public" {
  count         = 2
  allocation_id = aws_eip.nat[count.index].id
  subnet_id     = aws_subnet.public[count.index].id

  tags = {
    Name = "${var.project_name}-nat-gw-${count.index + 1}"
  }

  depends_on = [aws_internet_gateway.main]
}

# Route Tables
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

resource "aws_route_table" "private" {
  count  = 2
  vpc_id = aws_vpc.main.id

  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.public[count.index].id
  }

  tags = {
    Name = "${var.project_name}-private-rt-${count.index + 1}"
  }
}

# Route Table Associations
resource "aws_route_table_association" "public" {
  count          = 2
  subnet_id      = aws_subnet.public[count.index].id
  route_table_id = aws_route_table.public.id
}

resource "aws_route_table_association" "private" {
  count          = 2
  subnet_id      = aws_subnet.private[count.index].id
  route_table_id = aws_route_table.private[count.index].id
}

resource "aws_route_table_association" "database" {
  count          = 2
  subnet_id      = aws_subnet.database[count.index].id
  route_table_id = aws_route_table.private[count.index].id
}

# Data source for availability zones
data "aws_availability_zones" "available" {
  state = "available"
}
```

### Step 6: Create Security Groups

Create `security.tf`:

```hcl
# Web Server Security Group
resource "aws_security_group" "web" {
  name        = "${var.project_name}-web-sg"
  description = "Security group for web servers"
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

  ingress {
    description = "SSH from specific IP"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.ssh_allowed_cidr]
  }

  egress {
    description = "All outbound traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.project_name}-web-sg"
  }
}

# Application Server Security Group
resource "aws_security_group" "app" {
  name        = "${var.project_name}-app-sg"
  description = "Security group for application servers"
  vpc_id      = aws_vpc.main.id

  ingress {
    description     = "HTTP from web servers"
    from_port      = 8080
    to_port        = 8080
    protocol       = "tcp"
    security_groups = [aws_security_group.web.id]
  }

  egress {
    description = "All outbound traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.project_name}-app-sg"
  }
}

# Database Security Group
resource "aws_security_group" "database" {
  name        = "${var.project_name}-db-sg"
  description = "Security group for databases"
  vpc_id      = aws_vpc.main.id

  ingress {
    description     = "MySQL from app servers"
    from_port      = 3306
    to_port        = 3306
    protocol       = "tcp"
    security_groups = [aws_security_group.app.id]
  }

  egress {
    description = "All outbound traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.project_name}-db-sg"
  }
}

# Load Balancer Security Group
resource "aws_security_group" "lb" {
  name        = "${var.project_name}-lb-sg"
  description = "Security group for load balancer"
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
    description = "All outbound traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.project_name}-lb-sg"
  }
}
```

### Step 7: Create EC2 Instances

Create `compute.tf`:

```hcl
# Launch Template
resource "aws_launch_template" "web" {
  name_prefix   = "${var.project_name}-web-"
  image_id      = data.aws_ami.amazon_linux_2.id
  instance_type = var.web_instance_type
  key_name      = var.ssh_key_name

  network_interfaces {
    associate_public_ip_address = true
    security_groups             = [aws_security_group.web.id]
  }

  user_data = base64encode(templatefile("${path.module}/user_data.sh", {
    name = "Web Server"
  }))

  tag_specifications {
    resource_type = "instance"
    tags = {
      Name = "${var.project_name}-web"
      Type = "Web"
    }
  }

  monitoring {
    enabled = true
  }
}

# Auto Scaling Group
resource "aws_autoscaling_group" "web" {
  vpc_zone_identifier = aws_subnet.public[*].id
  desired_capacity    = 2
  max_size           = 4
  min_size           = 2

  target_group_arns = [aws_lb_target_group.web.arn]

  launch_template {
    id      = aws_launch_template.web.id
    version = "$Latest"
  }

  tag {
    key                 = "Name"
    value               = "${var.project_name}-web"
    propagate_at_launch = true
  }

  tag {
    key                 = "Type"
    value               = "Web"
    propagate_at_launch = true
  }
}

# Application Load Balancer
resource "aws_lb" "web" {
  name               = "${var.project_name}-lb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.lb.id]
  subnets           = aws_subnet.public[*].id

  enable_deletion_protection = false

  tags = {
    Name = "${var.project_name}-lb"
  }
}

# Target Group
resource "aws_lb_target_group" "web" {
  name        = "${var.project_name}-tg"
  port        = 80
  protocol    = "HTTP"
  vpc_id      = aws_vpc.main.id

  health_check {
    path                = "/health"
    interval            = 30
    timeout             = 5
    healthy_threshold   = 2
    unhealthy_threshold = 3
  }

  tags = {
    Name = "${var.project_name}-tg"
  }
}

# Listener
resource "aws_lb_listener" "front_end" {
  load_balancer_arn = aws_lb.web.arn
  port              = "80"
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.web.arn
  }
}

# Data source for latest AMI
data "aws_ami" "amazon_linux_2" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}
```

### Step 8: Create RDS Database

Create `database.tf`:

```hcl
# RDS Subnet Group
resource "aws_db_subnet_group" "main" {
  name       = "${var.project_name}-db-subnet-group"
  subnet_ids = aws_subnet.database[*].id

  tags = {
    Name = "${var.project_name}-db-subnet-group"
  }
}

# RDS Parameter Group
resource "aws_db_parameter_group" "main" {
  name        = "${var.project_name}-db-parameter-group"
  family      = "mysql8.0"
  description = "Custom parameter group for MySQL"

  parameter {
    name  = "max_connections"
    value = "100"
  }
}

# RDS Instance
resource "aws_db_instance" "main" {
  identifier             = "${var.project_name}-db"
  engine                 = "mysql"
  engine_version          = "8.0"
  instance_class         = "db.t3.micro"
  allocated_storage      = 20
  storage_type          = "gp2"
  storage_encrypted     = true

  db_name  = var.db_name
  username = var.db_username
  password = var.db_password

  db_subnet_group_name   = aws_db_subnet_group.main.name
  vpc_security_group_ids = [aws_security_group.database.id]
  multi_az               = true

  backup_retention_period = 7
  backup_window         = "03:00-04:00"
  maintenance_window     = "Mon:04:00-Mon:05:00"

  parameter_group_name = aws_db_parameter_group.main.name
  skip_final_snapshot = false
  final_snapshot_identifier = "${var.project_name}-db-final-snapshot"

  tags = {
    Name = "${var.project_name}-db"
  }
}
```

### Step 9: Create S3 Bucket

Create `storage.tf`:

```hcl
# S3 Bucket
resource "aws_s3_bucket" "data" {
  bucket_prefix = "${var.project_name}-data-"
  force_destroy = var.environment == "dev" ? true : false

  tags = {
    Name = "${var.project_name}-data"
  }
}

# S3 Bucket Versioning
resource "aws_s3_bucket_versioning" "data" {
  bucket = aws_s3_bucket.data.id
  versioning_configuration {
    status = "Enabled"
  }
}

# S3 Bucket Server-Side Encryption
resource "aws_s3_bucket_server_side_encryption_configuration" "data" {
  bucket = aws_s3_bucket.data.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# S3 Bucket Public Access Block
resource "aws_s3_bucket_public_access_block" "data" {
  bucket = aws_s3_bucket.data.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# S3 Bucket Lifecycle
resource "aws_s3_bucket_lifecycle_configuration" "data" {
  bucket = aws_s3_bucket.data.id

  rule {
    id     = "cleanup"
    status = "Enabled"

    transition {
      days          = 30
      storage_class = "STANDARD_IA"
    }

    transition {
      days          = 90
      storage_class = "GLACIER"
    }

    expiration {
      days = 365
    }
  }
}
```

### Step 10: Create IAM Roles

Create `iam.tf`:

```hcl
# IAM Role for EC2
resource "aws_iam_role" "ec2_role" {
  name = "${var.project_name}-ec2-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      }
    ]
  })

  tags = {
    Name = "${var.project_name}-ec2-role"
  }
}

# IAM Policy for EC2
resource "aws_iam_role_policy" "ec2_policy" {
  name = "${var.project_name}-ec2-policy"
  role = aws_iam_role.ec2_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:ListBucket"
        ]
        Effect = "Allow"
        Resource = [
          "${aws_s3_bucket.data.arn}/*",
          aws_s3_bucket.data.arn
        ]
      },
      {
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Effect = "Allow"
        Resource = "*"
      }
    ]
  })
}

# IAM Instance Profile
resource "aws_iam_instance_profile" "ec2_profile" {
  name = "${var.project_name}-ec2-profile"
  role = aws_iam_role.ec2_role.name
}
```

### Step 11: Create CloudWatch Alarms

Create `monitoring.tf`:

```hcl
# CPU Utilization Alarm
resource "aws_cloudwatch_metric_alarm" "cpu_high" {
  alarm_name          = "${var.project_name}-cpu-high"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = "2"
  metric_name         = "CPUUtilization"
  namespace           = "AWS/EC2"
  period             = "300"
  statistic           = "Average"
  threshold          = "80"
  alarm_description   = "This metric monitors EC2 CPU utilization"

  dimensions {
    AutoScalingGroupName = aws_autoscaling_group.web.name
  }
}

# Disk Space Alarm
resource "aws_cloudwatch_metric_alarm" "disk_space_low" {
  alarm_name          = "${var.project_name}-disk-low"
  comparison_operator = "LessThanOrEqualToThreshold"
  evaluation_periods  = "1"
  metric_name         = "DiskSpaceUtilization"
  namespace           = "CWAgent"
  period             = "300"
  statistic           = "Average"
  threshold          = "20"
  alarm_description   = "This metric monitors disk space"
}
```

### Step 12: Define Variables

Create `variables.tf`:

```hcl
variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "ap-southeast-1"
}

variable "project_name" {
  description = "Project name used for tagging"
  type        = string
}

variable "environment" {
  description = "Environment name"
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

variable "web_instance_type" {
  description = "Instance type for web servers"
  type        = string
  default     = "t3.micro"
}

variable "ssh_key_name" {
  description = "SSH key name"
  type        = string
}

variable "ssh_allowed_cidr" {
  description = "CIDR block allowed for SSH access"
  type        = string
  default     = "0.0.0.0/0"
}

variable "db_name" {
  description = "Database name"
  type        = string
}

variable "db_username" {
  description = "Database username"
  type        = string
}

variable "db_password" {
  description = "Database password"
  type        = string
  sensitive   = true
}
```

### Step 13: Create Outputs

Create `outputs.tf`:

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

output "database_subnet_ids" {
  description = "Database subnet IDs"
  value       = aws_subnet.database[*].id
}

output "lb_dns_name" {
  description = "Load balancer DNS name"
  value       = aws_lb.web.dns_name
}

output "db_endpoint" {
  description = "Database endpoint"
  value       = aws_db_instance.main.endpoint
  sensitive   = true
}

output "s3_bucket_arn" {
  description = "S3 bucket ARN"
  value       = aws_s3_bucket.data.arn
}
```

### Step 14: Initialize and Apply

```bash
# Initialize providers
tofu init

# Plan changes
tofu plan -out=tfplan

# Apply changes
tofu apply tfplan

# Show outputs
tofu output
```

## Best Practices

### Security

1. **Least Privilege**: Grant minimal permissions in IAM roles and policies
2. **Encryption**: Enable encryption at rest and in transit
3. **Security Groups**: Restrict access to necessary IPs and security groups
4. **KMS**: Use AWS KMS for encryption key management
5. **MFA**: Enable MFA for root and privileged IAM users

### High Availability

1. **Multi-AZ Deployments**: Spread resources across availability zones
2. **Auto Scaling**: Use auto scaling groups for compute resources
3. **Load Balancing**: Distribute traffic with load balancers
4. **Database HA**: Enable multi-AZ for RDS instances
5. **Health Checks**: Configure proper health checks for all services

### Cost Optimization

1. **Right-Sizing**: Choose appropriate instance types and storage
2. **Reserved Instances**: Use reserved instances for predictable workloads
3. **S3 Lifecycle**: Implement S3 lifecycle policies for cost savings
4. **Spot Instances**: Use spot instances for fault-tolerant workloads
5. **Monitor Costs**: Use AWS Cost Explorer and Budgets

### Networking

1. **VPC Best Practices**: Use separate subnets for tiers (web, app, db)
2. **NAT Gateways**: Use NAT gateways in each AZ for outbound internet
3. **Route Tables**: Separate route tables for public and private subnets
4. **DNS**: Use Route 53 for DNS management
5. **VPC Peering**: Use VPC peering for inter-VPC communication

### State Management

1. **Remote State**: Use S3 or other remote backends for state
2. **State Locking**: Enable DynamoDB for state locking
3. **State Encryption**: Encrypt state files
4. **State Versioning**: Enable versioning on state bucket
5. **State Backup**: Regularly backup state files

## Common Issues

### Issue: Provider Not Found

**Symptom**: Error `Error: Failed to query available provider packages`

**Solution**:
```bash
# Update provider versions
tofu init -upgrade

# Check internet connectivity
curl https://registry.terraform.io/

# Verify provider source and version
```

### Issue: Authentication Failed

**Symptom**: Error `Error: error configuring Terraform AWS Provider`

**Solution**:
```bash
# Verify credentials
aws sts get-caller-identity

# Check environment variables
echo $AWS_ACCESS_KEY_ID
echo $AWS_SECRET_ACCESS_KEY
echo $AWS_DEFAULT_REGION

# Test credentials
aws s3 ls

# Reference: https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html
```

### Issue: Resource Already Exists

**Symptom**: Error `Error: ... already exists`

**Solution**:
```bash
# Import existing resource
tofu import aws_vpc.main vpc-12345678

# Or use -target to create specific resources
tofu apply -target=aws_s3_bucket.data
```

### Issue: State Lock Error

**Symptom**: Error `Error: Error acquiring the state lock`

**Solution**:
```bash
# Check who has the lock
tofu state pull

# Force unlock (caution!)
tofu force-unlock <LOCK_ID>

# Or wait for other operation to complete
```

### Issue: Invalid IAM Policy

**Symptom**: Error `Error: Error creating IAM policy`

**Solution**:
```hcl
# Validate JSON syntax
jq . policy.json

# Use jsonencode for policies
policy = jsonencode({
  Version = "2012-10-17"
  Statement = [...]
})
```

### Issue: Security Group Rule Conflict

**Symptom**: Error `Error: Error creating Security Group`

**Solution**:
```bash
# Check existing security group rules
aws ec2 describe-security-groups --group-ids sg-12345678

# Ensure no overlapping rules
# Use security_group_rule resource if needed
```

## Reference Documentation

- **Terraform Registry (AWS Provider)**: https://registry.terraform.io/providers/hashicorp/aws/latest/docs
- **AWS Documentation**: https://docs.aws.amazon.com/
- **AWS Well-Architected Framework**: https://docs.aws.amazon.com/wellarchitected/
- **OpenTofu Documentation**: https://opentofu.org/docs/
- **AWS CLI**: https://docs.aws.amazon.com/cli/

## Examples

### Complete 3-Tier Architecture

```hcl
# VPC and Networking
resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
}

resource "aws_subnet" "web" {
  count = 2
  vpc_id = aws_vpc.main.id
  cidr_block = cidrsubnet("10.0.0.0/16", 8, count.index)
}

# Security Groups
resource "aws_security_group" "web" {
  name = "web-sg"
  vpc_id = aws_vpc.main.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# EC2 with ALB
resource "aws_lb" "web" {
  name               = "web-lb"
  load_balancer_type = "application"
  subnets           = aws_subnet.web[*].id
}

resource "aws_autoscaling_group" "web" {
  vpc_zone_identifier = aws_subnet.web[*].id
  desired_capacity    = 2
  max_size           = 4
  min_size           = 2

  launch_template {
    id = aws_launch_template.web.id
  }
}
```

### RDS Database Setup

```hcl
resource "aws_db_instance" "main" {
  identifier             = "production-db"
  engine                 = "mysql"
  instance_class         = "db.t3.medium"
  allocated_storage      = 100
  storage_encrypted     = true
  multi_az               = true
  backup_retention_period = 30

  db_name  = "appdb"
  username = "admin"
  password = var.db_password

  parameter_group_name = aws_db_parameter_group.main.name
}
```

### S3 with Lifecycle

```hcl
resource "aws_s3_bucket" "data" {
  bucket = "my-app-data"
}

resource "aws_s3_bucket_lifecycle_configuration" "data" {
  bucket = aws_s3_bucket.data.id

  rule {
    id     = "archive"
    status = "Enabled"

    transition {
      days          = 30
      storage_class = "STANDARD_IA"
    }

    expiration {
      days = 365
    }
  }
}
```

## Tips and Tricks

- **Use Data Sources**: Reference existing resources with data sources
- **Use Outputs**: Export important values for other configurations
- **Use Modules**: Create reusable infrastructure components
- **Use Workspaces**: Manage multiple environments
- **Import Resources**: Import existing resources into state
- **Validate Configuration**: Run `tofu validate` before applying
- **Use Remote State**: Share state across configurations

## Next Steps

After mastering AWS provider, explore:
- **opentofu-kubernetes-explorer**: Kubernetes deployment provider
- **AWS Services**: Explore advanced AWS services (Lambda, ECS, EKS)
- **AWS Well-Architected**: Implement AWS best practices
- **Cost Management**: Use AWS Cost Explorer and Budgets
