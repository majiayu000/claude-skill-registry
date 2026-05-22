---
name: deploy-aws-ecs
description: Deploy containerized applications to AWS ECS/Fargate. Use when deploying containers to AWS, managing ECS services, or setting up Fargate tasks. Covers task definitions and ECR.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Deploy to AWS ECS/Fargate

## Why ECS/Fargate?

- Serverless container orchestration
- No cluster management
- Auto-scaling built-in
- Deep AWS integration
- Pay-per-use pricing
- Production-grade reliability

## Quick Start

```bash
# Install AWS CLI
aws --version

# Configure credentials (use OIDC in production)
aws configure

# Login to ECR
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com
```

## ECR Setup

### Create Repository
```bash
# Create ECR repository
aws ecr create-repository --repository-name myapp

# Build and tag image
docker build -t myapp:latest .
docker tag myapp:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/myapp:latest

# Push to ECR
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/myapp:latest
```

## Task Definition

### Basic task-definition.json
```json
{
  "family": "myapp-task",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "256",
  "memory": "512",
  "executionRoleArn": "arn:aws:iam::<account-id>:role/ecsTaskExecutionRole",
  "containerDefinitions": [
    {
      "name": "myapp",
      "image": "<account-id>.dkr.ecr.us-east-1.amazonaws.com/myapp:latest",
      "portMappings": [
        {
          "containerPort": 8080,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {"name": "NODE_ENV", "value": "production"}
      ],
      "secrets": [
        {
          "name": "DATABASE_URL",
          "valueFrom": "arn:aws:secretsmanager:us-east-1:<account-id>:secret:db-url"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/myapp",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

### Register Task Definition
```bash
aws ecs register-task-definition --cli-input-json file://task-definition.json
```

## Service Creation

```bash
# Create ECS cluster
aws ecs create-cluster --cluster-name myapp-cluster

# Create service with ALB
aws ecs create-service \
  --cluster myapp-cluster \
  --service-name myapp-service \
  --task-definition myapp-task \
  --desired-count 2 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-xxx],securityGroups=[sg-xxx],assignPublicIp=ENABLED}" \
  --load-balancers "targetGroupArn=arn:aws:elasticloadbalancing:...,containerName=myapp,containerPort=8080"
```

## Deployment Workflow

### 1. Build and Push
```bash
# Build new version
docker build -t myapp:${VERSION} .

# Tag and push
docker tag myapp:${VERSION} ${ECR_REPO}:${VERSION}
docker tag myapp:${VERSION} ${ECR_REPO}:latest
docker push ${ECR_REPO}:${VERSION}
docker push ${ECR_REPO}:latest
```

### 2. Update Task Definition
```bash
# Register new task definition
aws ecs register-task-definition --cli-input-json file://task-definition.json
```

### 3. Update Service
```bash
# Force new deployment
aws ecs update-service \
  --cluster myapp-cluster \
  --service myapp-service \
  --force-new-deployment
```

## Best Practices

1. **Use Secrets Manager**: Store sensitive data in AWS Secrets Manager, reference in task definition
2. **Health Checks**: Configure ALB health checks for reliability
3. **Auto-scaling**: Set up target tracking based on CPU/memory
4. **Logging**: Always use CloudWatch Logs for centralized logging
5. **Tags**: Tag all resources for cost tracking and organization
6. **IAM Roles**: Use task roles for least-privilege access to AWS services
7. **CI/CD**: Integrate with GitHub Actions using OIDC (no long-lived credentials)

## Common Commands

```bash
# List services
aws ecs list-services --cluster myapp-cluster

# Describe service
aws ecs describe-services --cluster myapp-cluster --services myapp-service

# View logs (requires CloudWatch)
aws logs tail /ecs/myapp --follow

# Scale service
aws ecs update-service --cluster myapp-cluster --service myapp-service --desired-count 4

# Stop all tasks (for maintenance)
aws ecs update-service --cluster myapp-cluster --service myapp-service --desired-count 0
```

## Resources

- [ECS Task Definitions](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task_definitions.html)
- [Fargate Platform Versions](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/platform_versions.html)
- [ECR User Guide](https://docs.aws.amazon.com/AmazonECR/latest/userguide/)
