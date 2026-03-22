---
name: terraform-ecs
description: Provision production-ready AWS ECS clusters with Terraform. Covers cluster configuration, Fargate and EC2 launch types, task definitions, services, load balancer integration, auto-scaling, and deployment strategies. Use when provisioning ECS, setting up container orchestration on AWS, configuring Fargate services, or managing ECS infrastructure as code.
---

# Terraform ECS Cluster Provisioning

Production-ready patterns for provisioning AWS ECS clusters with Terraform using the official terraform-aws-modules/ecs module.

## Quick Reference

| Command | Description |
|---------|-------------|
| `terraform init` | Initialize Terraform working directory |
| `terraform plan` | Preview infrastructure changes |
| `terraform apply` | Create/update ECS cluster |
| `terraform destroy` | Delete ECS cluster and resources |
| `aws ecs list-clusters` | List all ECS clusters |
| `terraform output` | View cluster outputs |

## Version Requirements

```hcl
terraform {
  required_version = ">= 1.11.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
}
```

## Basic ECS Cluster with Fargate

```hcl
module "ecs" {
  source  = "terraform-aws-modules/ecs/aws"
  version = "~> 5.0"

  cluster_name = "production-ecs"

  # Capacity providers
  default_capacity_provider_use_fargate = true

  fargate_capacity_providers = {
    FARGATE = {
      default_capacity_provider_strategy = {
        weight = 50
        base   = 1
      }
    }
    FARGATE_SPOT = {
      default_capacity_provider_strategy = {
        weight = 50
      }
    }
  }

  # CloudWatch Container Insights
  cluster_settings = {
    name  = "containerInsights"
    value = "enabled"
  }

  tags = {
    Environment = "production"
    Terraform   = "true"
  }
}
```

## Task Definition

```hcl
resource "aws_ecs_task_definition" "app" {
  family                   = "my-app"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "512"
  memory                   = "1024"
  execution_role_arn       = aws_iam_role.ecs_task_execution.arn
  task_role_arn            = aws_iam_role.ecs_task.arn

  container_definitions = jsonencode([
    {
      name      = "my-app"
      image     = "${aws_ecr_repository.app.repository_url}:latest"
      cpu       = 512
      memory    = 1024
      essential = true

      portMappings = [
        {
          containerPort = 8080
          hostPort      = 8080
          protocol      = "tcp"
        }
      ]

      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group"         = aws_cloudwatch_log_group.app.name
          "awslogs-region"        = data.aws_region.current.name
          "awslogs-stream-prefix" = "ecs"
        }
      }

      environment = [
        {
          name  = "APP_ENV"
          value = "production"
        }
      ]

      secrets = [
        {
          name      = "DB_PASSWORD"
          valueFrom = aws_secretsmanager_secret.db_password.arn
        }
      ]

      healthCheck = {
        command     = ["CMD-SHELL", "curl -f http://localhost:8080/health || exit 1"]
        interval    = 30
        timeout     = 5
        retries     = 3
        startPeriod = 60
      }
    }
  ])

  tags = var.tags
}
```

## Service with Load Balancer

```hcl
resource "aws_ecs_service" "app" {
  name            = "my-service"
  cluster         = module.ecs.cluster_id
  task_definition = aws_ecs_task_definition.app.arn
  desired_count   = 3

  # Use capacity providers instead of launch_type
  capacity_provider_strategy {
    capacity_provider = "FARGATE"
    weight            = 1
    base              = 1
  }

  capacity_provider_strategy {
    capacity_provider = "FARGATE_SPOT"
    weight            = 3
  }

  platform_version = "1.4.0"

  network_configuration {
    subnets          = module.vpc.private_subnets
    security_groups  = [aws_security_group.ecs_tasks.id]
    assign_public_ip = false
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.app.arn
    container_name   = "my-app"
    container_port   = 8080
  }

  deployment_configuration {
    maximum_percent         = 200
    minimum_healthy_percent = 100
  }

  deployment_circuit_breaker {
    enable   = true
    rollback = true
  }

  enable_execute_command = true

  depends_on = [aws_lb_listener.app]

  tags = var.tags

  lifecycle {
    ignore_changes = [task_definition]  # Allow external deployments
  }
}
```

## Application Load Balancer

```hcl
resource "aws_lb" "app" {
  name               = "app-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb.id]
  subnets            = module.vpc.public_subnets

  tags = var.tags
}

resource "aws_lb_target_group" "app" {
  name        = "app-tg"
  port        = 8080
  protocol    = "HTTP"
  vpc_id      = module.vpc.vpc_id
  target_type = "ip"  # Required for awsvpc network mode

  health_check {
    healthy_threshold   = 2
    unhealthy_threshold = 2
    timeout             = 5
    interval            = 30
    path                = "/health"
    matcher             = "200"
  }

  tags = var.tags
}

resource "aws_lb_listener" "app" {
  load_balancer_arn = aws_lb.app.arn
  port              = 443
  protocol          = "HTTPS"
  ssl_policy        = "ELBSecurityPolicy-TLS13-1-2-2021-06"
  certificate_arn   = aws_acm_certificate.app.arn

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.app.arn
  }
}
```

## Auto Scaling

```hcl
resource "aws_appautoscaling_target" "ecs" {
  max_capacity       = 10
  min_capacity       = 1
  resource_id        = "service/${module.ecs.cluster_name}/${aws_ecs_service.app.name}"
  scalable_dimension = "ecs:service:DesiredCount"
  service_namespace  = "ecs"
}

# CPU-based scaling
resource "aws_appautoscaling_policy" "cpu" {
  name               = "cpu-autoscaling"
  policy_type        = "TargetTrackingScaling"
  resource_id        = aws_appautoscaling_target.ecs.resource_id
  scalable_dimension = aws_appautoscaling_target.ecs.scalable_dimension
  service_namespace  = aws_appautoscaling_target.ecs.service_namespace

  target_tracking_scaling_policy_configuration {
    predefined_metric_specification {
      predefined_metric_type = "ECSServiceAverageCPUUtilization"
    }
    target_value       = 70.0
    scale_in_cooldown  = 300
    scale_out_cooldown = 60
  }
}

# Memory-based scaling
resource "aws_appautoscaling_policy" "memory" {
  name               = "memory-autoscaling"
  policy_type        = "TargetTrackingScaling"
  resource_id        = aws_appautoscaling_target.ecs.resource_id
  scalable_dimension = aws_appautoscaling_target.ecs.scalable_dimension
  service_namespace  = aws_appautoscaling_target.ecs.service_namespace

  target_tracking_scaling_policy_configuration {
    predefined_metric_specification {
      predefined_metric_type = "ECSServiceAverageMemoryUtilization"
    }
    target_value = 80.0
  }
}

# Request count scaling (requires ALB)
resource "aws_appautoscaling_policy" "requests" {
  name               = "requests-autoscaling"
  policy_type        = "TargetTrackingScaling"
  resource_id        = aws_appautoscaling_target.ecs.resource_id
  scalable_dimension = aws_appautoscaling_target.ecs.scalable_dimension
  service_namespace  = aws_appautoscaling_target.ecs.service_namespace

  target_tracking_scaling_policy_configuration {
    predefined_metric_specification {
      predefined_metric_type = "ALBRequestCountPerTarget"
      resource_label         = "${aws_lb.app.arn_suffix}/${aws_lb_target_group.app.arn_suffix}"
    }
    target_value = 1000
  }
}
```

## IAM Roles

```hcl
# Task Execution Role (for ECS agent)
resource "aws_iam_role" "ecs_task_execution" {
  name = "ecs-task-execution-role"

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

resource "aws_iam_role_policy_attachment" "ecs_task_execution" {
  role       = aws_iam_role.ecs_task_execution.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

resource "aws_iam_role_policy" "ecs_task_execution_secrets" {
  name = "secrets-access"
  role = aws_iam_role.ecs_task_execution.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "secretsmanager:GetSecretValue"
        ]
        Resource = aws_secretsmanager_secret.db_password.arn
      },
      {
        Effect = "Allow"
        Action = [
          "ssm:GetParameters"
        ]
        Resource = "arn:aws:ssm:*:*:parameter/ecs/*"
      }
    ]
  })
}

# Task Role (for application)
resource "aws_iam_role" "ecs_task" {
  name = "ecs-task-role"

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

resource "aws_iam_role_policy" "ecs_task" {
  name = "app-permissions"
  role = aws_iam_role.ecs_task.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject"
        ]
        Resource = "${aws_s3_bucket.app.arn}/*"
      },
      {
        Effect = "Allow"
        Action = [
          "ssmmessages:CreateControlChannel",
          "ssmmessages:CreateDataChannel",
          "ssmmessages:OpenControlChannel",
          "ssmmessages:OpenDataChannel"
        ]
        Resource = "*"
      }
    ]
  })
}
```

## VPC Configuration

```hcl
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 5.0"

  name = "ecs-vpc"
  cidr = "10.0.0.0/16"

  azs             = ["us-east-1a", "us-east-1b", "us-east-1c"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]

  enable_nat_gateway = true
  single_nat_gateway = false  # One per AZ for HA

  tags = var.tags
}

# Security Groups
resource "aws_security_group" "ecs_tasks" {
  name   = "ecs-tasks-sg"
  vpc_id = module.vpc.vpc_id

  ingress {
    from_port       = 8080
    to_port         = 8080
    protocol        = "tcp"
    security_groups = [aws_security_group.alb.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = var.tags
}

resource "aws_security_group" "alb" {
  name   = "alb-sg"
  vpc_id = module.vpc.vpc_id

  ingress {
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

  tags = var.tags
}
```

## Outputs

```hcl
output "cluster_id" {
  description = "ECS cluster ID"
  value       = module.ecs.cluster_id
}

output "cluster_name" {
  description = "ECS cluster name"
  value       = module.ecs.cluster_name
}

output "service_name" {
  description = "ECS service name"
  value       = aws_ecs_service.app.name
}

output "alb_dns_name" {
  description = "ALB DNS name"
  value       = aws_lb.app.dns_name
}
```

## Detailed Documentation

For comprehensive guides, see:

- **[Cluster Configuration](references/cluster-config.md)** - Cluster setup, capacity providers, settings
- **[Task Definitions](references/task-definitions.md)** - Container definitions, volumes, secrets
- **[Service Patterns](references/service-patterns.md)** - Deployment, load balancers, auto-scaling

## Common Commands

```bash
# Update kubeconfig equivalent - configure AWS CLI
aws ecs list-services --cluster production-ecs

# Check service status
aws ecs describe-services \
  --cluster production-ecs \
  --services my-service

# View task logs
aws logs tail /ecs/my-app --follow

# Execute command in container
aws ecs execute-command \
  --cluster production-ecs \
  --task <task-id> \
  --container my-app \
  --interactive \
  --command "/bin/sh"
```

## Best Practices

1. **Use capacity provider strategy** instead of launch_type for flexibility
2. **Enable deployment circuit breaker** with rollback for safety
3. **Use Fargate Spot** for cost optimization (up to 70% savings)
4. **Pin platform version** explicitly (e.g., "1.4.0")
5. **Enable Container Insights** for observability
6. **Use secrets manager** for sensitive configuration
7. **Separate task execution and task roles** for least privilege
8. **Use target_type = "ip"** for target groups with awsvpc mode

## References

- [terraform-aws-modules/ecs](https://registry.terraform.io/modules/terraform-aws-modules/ecs/aws/latest)
- [AWS ECS Best Practices](https://docs.aws.amazon.com/AmazonECS/latest/bestpracticesguide/)
- [ECS Workshop](https://ecsworkshop.com/)
