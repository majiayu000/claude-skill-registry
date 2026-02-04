---
name: aws-architecture
description: "AWS cloud architecture patterns and best practices. Use when designing, deploying, or reviewing AWS infrastructure including EC2, ECS, EKS, Lambda, RDS, S3, IAM, and VPC."
---

# AWS Architecture

Comprehensive guide for building secure, scalable, and cost-effective infrastructure on Amazon Web Services.

## When to Use

- Designing AWS architecture for new projects
- Deploying applications to AWS services
- Setting up networking (VPC, subnets, security groups)
- Configuring IAM policies and roles
- Optimizing costs and performance
- Security hardening AWS resources

## Core Services Overview

### Compute

| Service | Use Case | Key Features |
|---------|----------|--------------|
| EC2 | Virtual servers | Full control, any workload |
| ECS | Container orchestration | Docker on AWS |
| EKS | Managed Kubernetes | K8s without cluster management |
| Lambda | Serverless functions | Event-driven, pay-per-use |
| Fargate | Serverless containers | No server management |

### Storage

| Service | Use Case | Key Features |
|---------|----------|--------------|
| S3 | Object storage | Unlimited, 11 9s durability |
| EBS | Block storage (EC2) | Persistent volumes |
| EFS | File storage (NFS) | Shared across instances |
| FSx | Managed file systems | Windows/Lustre |

### Database

| Service | Use Case | Key Features |
|---------|----------|--------------|
| RDS | Managed relational | MySQL, PostgreSQL, etc. |
| Aurora | High-performance SQL | 5x MySQL, 3x PostgreSQL |
| DynamoDB | NoSQL key-value | Serverless, any scale |
| ElastiCache | In-memory cache | Redis, Memcached |
| DocumentDB | MongoDB compatible | Managed document DB |

### Networking

| Service | Use Case | Key Features |
|---------|----------|--------------|
| VPC | Virtual network | Isolated cloud network |
| ALB/NLB | Load balancing | Layer 7/Layer 4 |
| CloudFront | CDN | Global edge caching |
| Route 53 | DNS | Domain management |
| API Gateway | API management | REST/WebSocket APIs |

## VPC Architecture

### Standard 3-Tier VPC

```
┌─────────────────────────────────────────────────────────────────┐
│ VPC: 10.0.0.0/16                                                │
│                                                                 │
│  ┌─────────────────────┐    ┌─────────────────────┐            │
│  │   Public Subnet     │    │   Public Subnet     │            │
│  │   10.0.1.0/24       │    │   10.0.2.0/24       │            │
│  │   (us-east-1a)      │    │   (us-east-1b)      │            │
│  │   ┌─────────────┐   │    │   ┌─────────────┐   │            │
│  │   │ NAT Gateway │   │    │   │ NAT Gateway │   │            │
│  │   └─────────────┘   │    │   └─────────────┘   │            │
│  │   ┌─────────────┐   │    │   ┌─────────────┐   │            │
│  │   │     ALB     │   │    │   │     ALB     │   │            │
│  │   └─────────────┘   │    │   └─────────────┘   │            │
│  └─────────────────────┘    └─────────────────────┘            │
│                                                                 │
│  ┌─────────────────────┐    ┌─────────────────────┐            │
│  │   Private Subnet    │    │   Private Subnet    │            │
│  │   10.0.10.0/24      │    │   10.0.20.0/24      │            │
│  │   (us-east-1a)      │    │   (us-east-1b)      │            │
│  │   ┌─────────────┐   │    │   ┌─────────────┐   │            │
│  │   │ App Servers │   │    │   │ App Servers │   │            │
│  │   └─────────────┘   │    │   └─────────────┘   │            │
│  └─────────────────────┘    └─────────────────────┘            │
│                                                                 │
│  ┌─────────────────────┐    ┌─────────────────────┐            │
│  │   Database Subnet   │    │   Database Subnet   │            │
│  │   10.0.100.0/24     │    │   10.0.200.0/24     │            │
│  │   (us-east-1a)      │    │   (us-east-1b)      │            │
│  │   ┌─────────────┐   │    │   ┌─────────────┐   │            │
│  │   │     RDS     │───┼────┼───│ RDS Replica │   │            │
│  │   └─────────────┘   │    │   └─────────────┘   │            │
│  └─────────────────────┘    └─────────────────────┘            │
└─────────────────────────────────────────────────────────────────┘
```

### Terraform VPC Example

```hcl
# Using AWS VPC Module
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.0.0"

  name = "${var.project}-${var.environment}"
  cidr = "10.0.0.0/16"

  azs             = ["us-east-1a", "us-east-1b", "us-east-1c"]
  public_subnets  = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  private_subnets = ["10.0.10.0/24", "10.0.20.0/24", "10.0.30.0/24"]
  database_subnets = ["10.0.100.0/24", "10.0.200.0/24", "10.0.300.0/24"]

  enable_nat_gateway     = true
  single_nat_gateway     = var.environment != "prod"  # Cost saving for non-prod
  enable_vpn_gateway     = false
  enable_dns_hostnames   = true
  enable_dns_support     = true

  # Database subnet group
  create_database_subnet_group = true

  # VPC Flow Logs
  enable_flow_log                      = true
  create_flow_log_cloudwatch_iam_role  = true
  create_flow_log_cloudwatch_log_group = true

  tags = local.common_tags

  public_subnet_tags = {
    "kubernetes.io/role/elb" = 1
  }

  private_subnet_tags = {
    "kubernetes.io/role/internal-elb" = 1
  }
}
```

### Security Groups

```hcl
# ALB Security Group
resource "aws_security_group" "alb" {
  name_prefix = "${var.project}-alb-"
  vpc_id      = module.vpc.vpc_id

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "HTTPS from internet"
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "HTTP (redirect to HTTPS)"
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(local.common_tags, { Name = "${var.project}-alb-sg" })
}

# Application Security Group
resource "aws_security_group" "app" {
  name_prefix = "${var.project}-app-"
  vpc_id      = module.vpc.vpc_id

  ingress {
    from_port       = 8080
    to_port         = 8080
    protocol        = "tcp"
    security_groups = [aws_security_group.alb.id]
    description     = "App port from ALB"
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(local.common_tags, { Name = "${var.project}-app-sg" })
}

# Database Security Group
resource "aws_security_group" "db" {
  name_prefix = "${var.project}-db-"
  vpc_id      = module.vpc.vpc_id

  ingress {
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.app.id]
    description     = "PostgreSQL from app"
  }

  tags = merge(local.common_tags, { Name = "${var.project}-db-sg" })
}
```

## IAM Best Practices

### Least Privilege Policies

```hcl
# Application Role
resource "aws_iam_role" "app" {
  name = "${var.project}-app-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "ecs-tasks.amazonaws.com"
      }
    }]
  })
}

# S3 Access (specific bucket, specific actions)
resource "aws_iam_policy" "s3_access" {
  name = "${var.project}-s3-access"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "ListBucket"
        Effect = "Allow"
        Action = ["s3:ListBucket"]
        Resource = aws_s3_bucket.data.arn
      },
      {
        Sid    = "ReadWriteObjects"
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:DeleteObject"
        ]
        Resource = "${aws_s3_bucket.data.arn}/*"
      }
    ]
  })
}

# Secrets Manager Access
resource "aws_iam_policy" "secrets_access" {
  name = "${var.project}-secrets-access"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = [
        "secretsmanager:GetSecretValue"
      ]
      Resource = [
        "arn:aws:secretsmanager:${var.region}:${data.aws_caller_identity.current.account_id}:secret:${var.project}/*"
      ]
    }]
  })
}

resource "aws_iam_role_policy_attachment" "app_s3" {
  role       = aws_iam_role.app.name
  policy_arn = aws_iam_policy.s3_access.arn
}

resource "aws_iam_role_policy_attachment" "app_secrets" {
  role       = aws_iam_role.app.name
  policy_arn = aws_iam_policy.secrets_access.arn
}
```

### Cross-Account Access

```hcl
# Role that can be assumed from another account
resource "aws_iam_role" "cross_account" {
  name = "CrossAccountDeployRole"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = {
        AWS = "arn:aws:iam::${var.trusted_account_id}:root"
      }
      Action = "sts:AssumeRole"
      Condition = {
        StringEquals = {
          "sts:ExternalId" = var.external_id
        }
      }
    }]
  })
}
```

## ECS/Fargate

### ECS Service with Fargate

```hcl
# ECS Cluster
resource "aws_ecs_cluster" "main" {
  name = "${var.project}-cluster"

  setting {
    name  = "containerInsights"
    value = "enabled"
  }
}

# Task Definition
resource "aws_ecs_task_definition" "app" {
  family                   = "${var.project}-app"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = 256
  memory                   = 512
  execution_role_arn       = aws_iam_role.ecs_execution.arn
  task_role_arn            = aws_iam_role.app.arn

  container_definitions = jsonencode([{
    name  = "app"
    image = "${var.ecr_repository_url}:${var.image_tag}"

    portMappings = [{
      containerPort = 8080
      hostPort      = 8080
      protocol      = "tcp"
    }]

    environment = [
      { name = "NODE_ENV", value = "production" }
    ]

    secrets = [
      {
        name      = "DATABASE_URL"
        valueFrom = aws_secretsmanager_secret.db_url.arn
      }
    ]

    logConfiguration = {
      logDriver = "awslogs"
      options = {
        awslogs-group         = aws_cloudwatch_log_group.app.name
        awslogs-region        = var.region
        awslogs-stream-prefix = "app"
      }
    }

    healthCheck = {
      command     = ["CMD-SHELL", "wget -q --spider http://localhost:8080/health || exit 1"]
      interval    = 30
      timeout     = 5
      retries     = 3
      startPeriod = 60
    }
  }])
}

# ECS Service
resource "aws_ecs_service" "app" {
  name            = "${var.project}-app"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.app.arn
  desired_count   = var.app_count
  launch_type     = "FARGATE"

  deployment_configuration {
    minimum_healthy_percent = 50
    maximum_percent         = 200
  }

  network_configuration {
    subnets          = module.vpc.private_subnets
    security_groups  = [aws_security_group.app.id]
    assign_public_ip = false
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.app.arn
    container_name   = "app"
    container_port   = 8080
  }

  lifecycle {
    ignore_changes = [desired_count]  # Allow autoscaling
  }
}

# Auto Scaling
resource "aws_appautoscaling_target" "app" {
  max_capacity       = 10
  min_capacity       = var.environment == "prod" ? 2 : 1
  resource_id        = "service/${aws_ecs_cluster.main.name}/${aws_ecs_service.app.name}"
  scalable_dimension = "ecs:service:DesiredCount"
  service_namespace  = "ecs"
}

resource "aws_appautoscaling_policy" "cpu" {
  name               = "${var.project}-cpu-scaling"
  policy_type        = "TargetTrackingScaling"
  resource_id        = aws_appautoscaling_target.app.resource_id
  scalable_dimension = aws_appautoscaling_target.app.scalable_dimension
  service_namespace  = aws_appautoscaling_target.app.service_namespace

  target_tracking_scaling_policy_configuration {
    predefined_metric_specification {
      predefined_metric_type = "ECSServiceAverageCPUUtilization"
    }
    target_value       = 70.0
    scale_in_cooldown  = 300
    scale_out_cooldown = 60
  }
}
```

## Lambda

### Lambda Function with API Gateway

```hcl
# Lambda Function
resource "aws_lambda_function" "api" {
  function_name = "${var.project}-api"
  role          = aws_iam_role.lambda.arn
  handler       = "index.handler"
  runtime       = "nodejs20.x"
  timeout       = 30
  memory_size   = 256

  filename         = data.archive_file.lambda.output_path
  source_code_hash = data.archive_file.lambda.output_base64sha256

  environment {
    variables = {
      NODE_ENV     = "production"
      TABLE_NAME   = aws_dynamodb_table.main.name
    }
  }

  vpc_config {
    subnet_ids         = module.vpc.private_subnets
    security_group_ids = [aws_security_group.lambda.id]
  }

  tracing_config {
    mode = "Active"  # X-Ray tracing
  }
}

# API Gateway
resource "aws_apigatewayv2_api" "main" {
  name          = "${var.project}-api"
  protocol_type = "HTTP"

  cors_configuration {
    allow_origins = ["https://${var.domain}"]
    allow_methods = ["GET", "POST", "PUT", "DELETE"]
    allow_headers = ["Content-Type", "Authorization"]
    max_age       = 3600
  }
}

resource "aws_apigatewayv2_integration" "lambda" {
  api_id             = aws_apigatewayv2_api.main.id
  integration_type   = "AWS_PROXY"
  integration_uri    = aws_lambda_function.api.invoke_arn
  integration_method = "POST"
}

resource "aws_apigatewayv2_route" "default" {
  api_id    = aws_apigatewayv2_api.main.id
  route_key = "$default"
  target    = "integrations/${aws_apigatewayv2_integration.lambda.id}"
}

resource "aws_apigatewayv2_stage" "prod" {
  api_id      = aws_apigatewayv2_api.main.id
  name        = "prod"
  auto_deploy = true

  default_route_settings {
    throttling_burst_limit = 100
    throttling_rate_limit  = 50
  }
}

resource "aws_lambda_permission" "apigw" {
  statement_id  = "AllowAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.api.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.main.execution_arn}/*/*"
}
```

## RDS

### Aurora PostgreSQL

```hcl
resource "aws_rds_cluster" "main" {
  cluster_identifier = "${var.project}-aurora"
  engine             = "aurora-postgresql"
  engine_version     = "15.4"
  database_name      = var.db_name
  master_username    = var.db_username
  master_password    = random_password.db.result

  db_subnet_group_name   = module.vpc.database_subnet_group_name
  vpc_security_group_ids = [aws_security_group.db.id]

  storage_encrypted = true
  kms_key_id        = aws_kms_key.db.arn

  backup_retention_period = var.environment == "prod" ? 30 : 7
  preferred_backup_window = "03:00-04:00"
  skip_final_snapshot     = var.environment != "prod"

  enabled_cloudwatch_logs_exports = ["postgresql"]

  serverlessv2_scaling_configuration {
    min_capacity = var.environment == "prod" ? 1 : 0.5
    max_capacity = var.environment == "prod" ? 16 : 4
  }

  tags = local.common_tags
}

resource "aws_rds_cluster_instance" "main" {
  count = var.environment == "prod" ? 2 : 1

  identifier         = "${var.project}-aurora-${count.index}"
  cluster_identifier = aws_rds_cluster.main.id
  instance_class     = "db.serverless"
  engine             = aws_rds_cluster.main.engine
  engine_version     = aws_rds_cluster.main.engine_version

  performance_insights_enabled = true

  tags = local.common_tags
}
```

## S3

### Secure S3 Bucket

```hcl
resource "aws_s3_bucket" "data" {
  bucket = "${var.project}-data-${data.aws_caller_identity.current.account_id}"

  tags = local.common_tags
}

resource "aws_s3_bucket_versioning" "data" {
  bucket = aws_s3_bucket.data.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "data" {
  bucket = aws_s3_bucket.data.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm     = "aws:kms"
      kms_master_key_id = aws_kms_key.s3.arn
    }
    bucket_key_enabled = true
  }
}

resource "aws_s3_bucket_public_access_block" "data" {
  bucket = aws_s3_bucket.data.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_lifecycle_configuration" "data" {
  bucket = aws_s3_bucket.data.id

  rule {
    id     = "archive"
    status = "Enabled"

    transition {
      days          = 90
      storage_class = "STANDARD_IA"
    }

    transition {
      days          = 180
      storage_class = "GLACIER"
    }

    expiration {
      days = 365
    }

    noncurrent_version_expiration {
      noncurrent_days = 30
    }
  }
}
```

## Cost Optimization

### Strategies

| Strategy | Savings | Effort |
|----------|---------|--------|
| Reserved Instances (1yr) | 30-40% | Low |
| Savings Plans | 20-30% | Low |
| Spot Instances | 60-90% | Medium |
| Right-sizing | 20-50% | Medium |
| S3 Lifecycle | Variable | Low |

### Cost Tags

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
```

### Budget Alerts

```hcl
resource "aws_budgets_budget" "monthly" {
  name         = "${var.project}-monthly-budget"
  budget_type  = "COST"
  limit_amount = var.monthly_budget
  limit_unit   = "USD"
  time_unit    = "MONTHLY"

  notification {
    comparison_operator        = "GREATER_THAN"
    threshold                  = 80
    threshold_type             = "PERCENTAGE"
    notification_type          = "FORECASTED"
    subscriber_email_addresses = [var.budget_alert_email]
  }

  notification {
    comparison_operator        = "GREATER_THAN"
    threshold                  = 100
    threshold_type             = "PERCENTAGE"
    notification_type          = "ACTUAL"
    subscriber_email_addresses = [var.budget_alert_email]
  }
}
```

## CLI Reference

```bash
# EC2
aws ec2 describe-instances --filters "Name=tag:Environment,Values=prod"
aws ec2 start-instances --instance-ids i-1234567890abcdef0
aws ec2 stop-instances --instance-ids i-1234567890abcdef0

# ECS
aws ecs list-clusters
aws ecs list-services --cluster my-cluster
aws ecs update-service --cluster my-cluster --service my-service --force-new-deployment

# Lambda
aws lambda invoke --function-name my-function output.json
aws lambda update-function-code --function-name my-function --s3-bucket bucket --s3-key code.zip

# S3
aws s3 ls s3://bucket-name/
aws s3 cp file.txt s3://bucket-name/
aws s3 sync ./folder s3://bucket-name/folder

# RDS
aws rds describe-db-instances
aws rds create-db-snapshot --db-instance-identifier mydb --db-snapshot-identifier mydb-snapshot

# Secrets Manager
aws secretsmanager get-secret-value --secret-id my-secret
aws secretsmanager create-secret --name my-secret --secret-string '{"key":"value"}'

# CloudWatch
aws logs tail /aws/lambda/my-function --follow
aws cloudwatch get-metric-statistics --namespace AWS/EC2 --metric-name CPUUtilization ...
```

## Security Checklist

- [ ] VPC with private subnets for sensitive workloads
- [ ] Security groups with least privilege
- [ ] IAM roles (not users) for applications
- [ ] No hardcoded credentials
- [ ] S3 buckets encrypted and private
- [ ] RDS encrypted at rest and in transit
- [ ] CloudTrail enabled for audit
- [ ] GuardDuty enabled for threat detection
- [ ] Config rules for compliance

## Integration

Works with:
- `/terraform` - AWS provider configuration
- `/devops` - AWS deployment pipelines
- `/security` - AWS security review
- `cost-optimization` skill - AWS cost analysis
