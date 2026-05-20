---
name: aws-ec2-setup
description: Launch and configure EC2 instances with security groups, IAM roles, key pairs, AMIs, and auto-scaling. Use for virtual servers and managed infrastructure.
---

# AWS EC2 Setup

## Overview

Amazon EC2 provides resizable compute capacity in the cloud. Launch and configure virtual servers with complete control over networking, storage, and security settings. Scale automatically based on demand.

## When to Use

- Web application servers
- Application backends and APIs
- Batch processing and compute jobs
- Development and testing environments
- Containerized applications (ECS)
- Kubernetes clusters (EKS)
- Database servers
- VPN and proxy servers

## Implementation Examples

### 1. **EC2 Instance Creation with AWS CLI**

```bash
# Create security group
aws ec2 create-security-group \
  --group-name web-server-sg \
  --description "Web server security group" \
  --vpc-id vpc-12345678

# Add ingress rules
aws ec2 authorize-security-group-ingress \
  --group-id sg-0123456789abcdef0 \
  --protocol tcp \
  --port 80 \
  --cidr 0.0.0.0/0

aws ec2 authorize-security-group-ingress \
  --group-id sg-0123456789abcdef0 \
  --protocol tcp \
  --port 443 \
  --cidr 0.0.0.0/0

aws ec2 authorize-security-group-ingress \
  --group-id sg-0123456789abcdef0 \
  --protocol tcp \
  --port 22 \
  --cidr YOUR_IP/32

# Create key pair
aws ec2 create-key-pair \
  --key-name my-app-key \
  --query 'KeyMaterial' \
  --output text > my-app-key.pem

chmod 400 my-app-key.pem

# Create IAM role for EC2
aws iam create-role \
  --role-name ec2-app-role \
  --assume-role-policy-document '{
    "Version": "2012-10-17",
    "Statement": [{
      "Effect": "Allow",
      "Principal": {"Service": "ec2.amazonaws.com"},
      "Action": "sts:AssumeRole"
    }]
  }'

# Attach policies
aws iam attach-role-policy \
  --role-name ec2-app-role \
  --policy-arn arn:aws:iam::aws:policy/CloudWatchAgentServerPolicy

# Create instance profile
aws iam create-instance-profile --instance-profile-name ec2-app-profile
aws iam add-role-to-instance-profile \
  --instance-profile-name ec2-app-profile \
  --role-name ec2-app-role

# Launch instance
aws ec2 run-instances \
  --image-id ami-0c55b159cbfafe1f0 \
  --instance-type t3.micro \
  --key-name my-app-key \
  --security-group-ids sg-0123456789abcdef0 \
  --iam-instance-profile Name=ec2-app-profile \
  --user-data file://user-data.sh \
  --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=web-server}]'
```

### 2. **User Data Script**

```bash
#!/bin/bash
# user-data.sh

set -e
set -x

# Update system
apt-get update
apt-get upgrade -y

# Install dependencies
apt-get install -y \
  curl \
  wget \
  git \
  nodejs \
  npm \
  postgresql-client

# Install Node.js application
mkdir -p /opt/app
cd /opt/app
git clone https://github.com/myorg/myapp.git .
npm install --production

# Create systemd service
cat > /etc/systemd/system/myapp.service << EOF
[Unit]
Description=My Node App
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/opt/app
ExecStart=/usr/bin/node index.js
Restart=on-failure
RestartSec=5

Environment="NODE_ENV=production"
Environment="PORT=3000"

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable myapp
systemctl start myapp

# Install and configure CloudWatch agent
wget https://s3.amazonaws.com/amazoncloudwatch-agent/ubuntu/amd64/latest/amazon-cloudwatch-agent.deb
dpkg -i -E ./amazon-cloudwatch-agent.deb

# Configure log streaming
cat > /opt/aws/amazon-cloudwatch-agent/etc/amazon-cloudwatch-agent.json << EOF
{
  "logs": {
    "logs_collected": {
      "files": {
        "collect_list": [
          {
            "file_path": "/var/log/syslog",
            "log_group_name": "/aws/ec2/web-server",
            "log_stream_name": "{instance_id}"
          },
          {
            "file_path": "/opt/app/logs/*.log",
            "log_group_name": "/aws/ec2/app",
            "log_stream_name": "{instance_id}"
          }
        ]
      }
    }
  },
  "metrics": {
    "metrics_collected": {
      "cpu": {"measurement": [{"name": "cpu_usage_idle"}]},
      "mem": {"measurement": [{"name": "mem_used_percent"}]},
      "disk": {"measurement": [{"name": "used_percent"}]}
    }
  }
}
EOF

/opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl \
  -a fetch-config \
  -m ec2 \
  -s \
  -c file:/opt/aws/amazon-cloudwatch-agent/etc/amazon-cloudwatch-agent.json
```

### 3. **Terraform EC2 Configuration**

```hcl
# ec2.tf
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

# VPC
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true

  tags = { Name = "main-vpc" }
}

# Public Subnet
resource "aws_subnet" "public" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = "us-east-1a"
  map_public_ip_on_launch = true

  tags = { Name = "public-subnet" }
}

# Internet Gateway
resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id

  tags = { Name = "main-igw" }
}

# Route table
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block      = "0.0.0.0/0"
    gateway_id      = aws_internet_gateway.main.id
  }

  tags = { Name = "public-rt" }
}

resource "aws_route_table_association" "public" {
  subnet_id      = aws_subnet.public.id
  route_table_id = aws_route_table.public.id
}

# Security group
resource "aws_security_group" "web" {
  name_prefix = "web-"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["YOUR_IP/32"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# IAM role
resource "aws_iam_role" "ec2_role" {
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "ec2.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "ec2_policy" {
  role       = aws_iam_role.ec2_role.name
  policy_arn = "arn:aws:iam::aws:policy/CloudWatchAgentServerPolicy"
}

resource "aws_iam_instance_profile" "ec2_profile" {
  role = aws_iam_role.ec2_role.name
}

# Key pair
resource "aws_key_pair" "deployer" {
  key_name   = "deployer-key"
  public_key = file("~/.ssh/id_rsa.pub")
}

# AMI data source
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"] # Canonical

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }
}

# EC2 instance
resource "aws_instance" "web" {
  ami                    = data.aws_ami.ubuntu.id
  instance_type          = "t3.micro"
  subnet_id              = aws_subnet.public.id
  vpc_security_group_ids = [aws_security_group.web.id]
  iam_instance_profile   = aws_iam_instance_profile.ec2_profile.name
  key_name               = aws_key_pair.deployer.key_name

  user_data = base64encode(file("${path.module}/user-data.sh"))

  root_block_device {
    volume_size           = 20
    volume_type           = "gp3"
    delete_on_termination = true
    encrypted             = true
  }

  tags = {
    Name = "web-server"
  }

  lifecycle {
    create_before_destroy = true
  }
}

# Elastic IP
resource "aws_eip" "web" {
  instance = aws_instance.web.id
  domain   = "vpc"

  tags = { Name = "web-eip" }
}

# Auto Scaling Group
resource "aws_launch_template" "app" {
  image_id      = data.aws_ami.ubuntu.id
  instance_type = "t3.small"

  vpc_security_group_ids = [aws_security_group.web.id]
  iam_instance_profile {
    name = aws_iam_instance_profile.ec2_profile.name
  }

  user_data = base64encode(file("${path.module}/user-data.sh"))

  tag_specifications {
    resource_type = "instance"
    tags = {
      Name = "app-instance"
    }
  }
}

resource "aws_autoscaling_group" "app" {
  name                = "app-asg"
  vpc_zone_identifier = [aws_subnet.public.id]
  min_size            = 1
  max_size            = 3
  desired_capacity    = 2

  launch_template {
    id      = aws_launch_template.app.id
    version = "$Latest"
  }

  health_check_type         = "ELB"
  health_check_grace_period = 300

  tag {
    key                 = "Name"
    value               = "app-asg-instance"
    propagate_at_launch = true
  }
}
```

## Best Practices

### ✅ DO
- Use security groups for network control
- Attach IAM roles for AWS access
- Enable CloudWatch monitoring
- Use AMI for consistent deployments
- Implement auto-scaling for variable load
- Use EBS for persistent storage
- Enable termination protection for production
- Keep systems patched and updated

### ❌ DON'T
- Use overly permissive security groups
- Store credentials in user data
- Ignore CloudWatch metrics
- Use outdated AMIs
- Create hardcoded configurations
- Forget to monitor costs

## Monitoring

- CloudWatch metrics and dashboards
- CloudWatch Logs from applications
- CloudWatch Alarms for thresholds
- EC2 Instance Health Checks
- Auto Scaling Activities

## Resources

- [AWS EC2 Documentation](https://docs.aws.amazon.com/ec2/)
- [EC2 Best Practices](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-best-practices.html)
