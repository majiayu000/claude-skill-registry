---
name: terraform
description: Terraform 基础设施即代码
version: 1.0.0
author: terminal-skills
tags: [devops, terraform, iac, infrastructure]
---

# Terraform 基础设施即代码

## 概述
HCL 编写、状态管理、模块开发等技能。

## 基础命令

```bash
# 初始化
terraform init
terraform init -upgrade             # 升级 provider

# 格式化
terraform fmt
terraform fmt -recursive

# 验证
terraform validate

# 计划
terraform plan
terraform plan -out=plan.tfplan

# 应用
terraform apply
terraform apply plan.tfplan
terraform apply -auto-approve

# 销毁
terraform destroy
terraform destroy -auto-approve

# 查看状态
terraform show
terraform state list
terraform state show resource_type.name

# 输出
terraform output
terraform output -json
```

## HCL 语法

### Provider 配置
```hcl
# providers.tf
terraform {
  required_version = ">= 1.0"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  
  backend "s3" {
    bucket = "my-terraform-state"
    key    = "prod/terraform.tfstate"
    region = "us-east-1"
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

### 变量定义
```hcl
# variables.tf
variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.micro"
}

variable "environment" {
  description = "Environment name"
  type        = string
  
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}

variable "tags" {
  description = "Resource tags"
  type        = map(string)
  default     = {}
}

variable "subnets" {
  description = "Subnet configuration"
  type = list(object({
    cidr_block = string
    az         = string
  }))
}
```

### 资源定义
```hcl
# main.tf
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  
  tags = {
    Name = "${var.environment}-vpc"
  }
}

resource "aws_subnet" "public" {
  count             = length(var.subnets)
  vpc_id            = aws_vpc.main.id
  cidr_block        = var.subnets[count.index].cidr_block
  availability_zone = var.subnets[count.index].az
  
  tags = {
    Name = "${var.environment}-public-${count.index + 1}"
  }
}

resource "aws_instance" "web" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = var.instance_type
  subnet_id     = aws_subnet.public[0].id
  
  tags = merge(var.tags, {
    Name = "${var.environment}-web"
  })
}
```

### 数据源
```hcl
# data.tf
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"]  # Canonical
  
  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }
}

data "aws_availability_zones" "available" {
  state = "available"
}
```

### 输出
```hcl
# outputs.tf
output "vpc_id" {
  description = "VPC ID"
  value       = aws_vpc.main.id
}

output "instance_public_ip" {
  description = "Public IP of web instance"
  value       = aws_instance.web.public_ip
}

output "subnet_ids" {
  description = "Subnet IDs"
  value       = aws_subnet.public[*].id
}
```

## 状态管理

### 状态命令
```bash
# 列出资源
terraform state list

# 查看资源
terraform state show aws_instance.web

# 移动资源
terraform state mv aws_instance.web aws_instance.app

# 删除资源（从状态中）
terraform state rm aws_instance.web

# 导入现有资源
terraform import aws_instance.web i-1234567890abcdef0

# 拉取远程状态
terraform state pull > state.json

# 推送状态
terraform state push state.json
```

### 远程后端
```hcl
# S3 后端
terraform {
  backend "s3" {
    bucket         = "my-terraform-state"
    key            = "prod/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}

# 初始化后端
terraform init -backend-config="bucket=my-bucket"
```

## 模块

### 模块结构
```
modules/
└── vpc/
    ├── main.tf
    ├── variables.tf
    ├── outputs.tf
    └── README.md
```

### 模块定义
```hcl
# modules/vpc/main.tf
resource "aws_vpc" "this" {
  cidr_block           = var.cidr_block
  enable_dns_hostnames = var.enable_dns_hostnames
  
  tags = merge(var.tags, {
    Name = var.name
  })
}

# modules/vpc/variables.tf
variable "name" {
  type = string
}

variable "cidr_block" {
  type = string
}

variable "enable_dns_hostnames" {
  type    = bool
  default = true
}

variable "tags" {
  type    = map(string)
  default = {}
}

# modules/vpc/outputs.tf
output "vpc_id" {
  value = aws_vpc.this.id
}
```

### 使用模块
```hcl
# 本地模块
module "vpc" {
  source = "./modules/vpc"
  
  name       = "my-vpc"
  cidr_block = "10.0.0.0/16"
  tags       = var.tags
}

# 远程模块
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.0.0"
  
  name = "my-vpc"
  cidr = "10.0.0.0/16"
}

# 引用模块输出
resource "aws_subnet" "public" {
  vpc_id = module.vpc.vpc_id
  # ...
}
```

## 工作区

```bash
# 列出工作区
terraform workspace list

# 创建工作区
terraform workspace new dev
terraform workspace new prod

# 切换工作区
terraform workspace select dev

# 删除工作区
terraform workspace delete dev

# 在配置中使用
locals {
  environment = terraform.workspace
}
```

## 常见场景

### 场景 1：条件创建资源
```hcl
variable "create_instance" {
  type    = bool
  default = true
}

resource "aws_instance" "web" {
  count = var.create_instance ? 1 : 0
  
  ami           = data.aws_ami.ubuntu.id
  instance_type = var.instance_type
}
```

### 场景 2：for_each 循环
```hcl
variable "instances" {
  type = map(object({
    instance_type = string
    ami           = string
  }))
}

resource "aws_instance" "this" {
  for_each = var.instances
  
  ami           = each.value.ami
  instance_type = each.value.instance_type
  
  tags = {
    Name = each.key
  }
}
```

### 场景 3：动态块
```hcl
resource "aws_security_group" "this" {
  name   = "my-sg"
  vpc_id = aws_vpc.main.id
  
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

### 场景 4：依赖管理
```hcl
resource "aws_instance" "web" {
  # 隐式依赖
  subnet_id = aws_subnet.public.id
  
  # 显式依赖
  depends_on = [aws_internet_gateway.main]
}
```

## 故障排查

| 问题 | 排查方法 |
|------|----------|
| 状态锁定 | `terraform force-unlock LOCK_ID` |
| Provider 错误 | `terraform init -upgrade` |
| 状态不一致 | `terraform refresh` |
| 循环依赖 | 检查 `depends_on` |

```bash
# 调试模式
TF_LOG=DEBUG terraform plan

# 查看详细计划
terraform plan -out=plan.tfplan
terraform show -json plan.tfplan | jq

# 验证配置
terraform validate
```
