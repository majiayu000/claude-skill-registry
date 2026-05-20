---
name: ecs-deployment
description: ECS deployment strategies including rolling updates, blue-green with CodeDeploy, canary releases, and GitOps workflows. Covers deployment circuit breakers, rollback strategies, and production deployment patterns. Use when deploying ECS services, implementing blue-green deployments, setting up CI/CD pipelines, or managing production releases.
---

# ECS Deployment Strategies

Complete guide to deploying ECS services safely and efficiently, from rolling updates to blue-green deployments.

## Quick Reference

| Strategy | Downtime | Rollback Speed | Complexity | Best For |
|----------|----------|----------------|------------|----------|
| Rolling Update | Zero | Medium | Low | Most workloads |
| Blue-Green | Zero | Instant | High | Critical services |
| Canary | Zero | Fast | High | Risk mitigation |

## Rolling Updates (Default)

### Configuration

```hcl
resource "aws_ecs_service" "app" {
  deployment_configuration {
    maximum_percent         = 200  # Allow 2x during deployment
    minimum_healthy_percent = 100  # Keep 100% healthy
  }

  deployment_circuit_breaker {
    enable   = true   # Auto-detect failures
    rollback = true   # Auto-rollback on failure
  }
}
```

### Behavior

1. New task definition registered
2. New tasks launched (up to maximum_percent)
3. Health checks pass on new tasks
4. Old tasks drained and stopped
5. Continues until all tasks updated

### Boto3 Deployment

```python
import boto3

ecs = boto3.client('ecs')

def deploy_rolling_update(cluster: str, service: str,
                          new_image: str, container_name: str):
    """Deploy new image via rolling update"""

    # 1. Get current task definition
    svc = ecs.describe_services(cluster=cluster, services=[service])
    current_task_def = svc['services'][0]['taskDefinition']

    # 2. Create new task definition revision
    task_def = ecs.describe_task_definition(taskDefinition=current_task_def)
    new_task_def = task_def['taskDefinition'].copy()

    # Remove response-only fields
    for field in ['taskDefinitionArn', 'revision', 'status',
                  'requiresAttributes', 'compatibilities',
                  'registeredAt', 'registeredBy']:
        new_task_def.pop(field, None)

    # Update image
    for container in new_task_def['containerDefinitions']:
        if container['name'] == container_name:
            container['image'] = new_image

    response = ecs.register_task_definition(**new_task_def)
    new_task_def_arn = response['taskDefinition']['taskDefinitionArn']

    # 3. Update service
    ecs.update_service(
        cluster=cluster,
        service=service,
        taskDefinition=new_task_def_arn,
        forceNewDeployment=True
    )

    print(f"Deploying {new_task_def_arn}")
    return new_task_def_arn

# Usage
deploy_rolling_update(
    cluster='production',
    service='api',
    new_image='123456789.dkr.ecr.us-east-1.amazonaws.com/api:v2.0',
    container_name='api'
)
```

### Monitor Deployment

```python
def wait_for_deployment(cluster: str, service: str, timeout: int = 600):
    """Wait for deployment to complete"""
    import time

    start = time.time()
    while time.time() - start < timeout:
        response = ecs.describe_services(cluster=cluster, services=[service])
        svc = response['services'][0]

        for deployment in svc['deployments']:
            print(f"Deployment {deployment['id'][:8]}: "
                  f"{deployment['rolloutState']} "
                  f"({deployment['runningCount']}/{deployment['desiredCount']})")

            if deployment['status'] == 'PRIMARY':
                if deployment['rolloutState'] == 'COMPLETED':
                    print("Deployment successful!")
                    return True
                elif deployment['rolloutState'] == 'FAILED':
                    print(f"Deployment failed: {deployment.get('rolloutStateReason')}")
                    return False

        time.sleep(15)

    print("Deployment timed out")
    return False
```

## Blue-Green Deployments

### Architecture

```
                    ┌─────────────┐
                    │    ALB      │
                    └──────┬──────┘
                           │
           ┌───────────────┴───────────────┐
           │                               │
    ┌──────▼──────┐                 ┌──────▼──────┐
    │ Target Group│                 │ Target Group│
    │    (Blue)   │                 │   (Green)   │
    └──────┬──────┘                 └──────┬──────┘
           │                               │
    ┌──────▼──────┐                 ┌──────▼──────┐
    │ ECS Service │                 │ ECS Service │
    │   (Blue)    │                 │   (Green)   │
    └─────────────┘                 └─────────────┘
```

### Terraform with CodeDeploy

```hcl
# Two target groups
resource "aws_lb_target_group" "blue" {
  name        = "app-blue"
  port        = 8080
  protocol    = "HTTP"
  vpc_id      = module.vpc.vpc_id
  target_type = "ip"

  health_check {
    path = "/health"
  }
}

resource "aws_lb_target_group" "green" {
  name        = "app-green"
  port        = 8080
  protocol    = "HTTP"
  vpc_id      = module.vpc.vpc_id
  target_type = "ip"

  health_check {
    path = "/health"
  }
}

# ALB with two listeners
resource "aws_lb_listener" "prod" {
  load_balancer_arn = aws_lb.app.arn
  port              = 443
  protocol          = "HTTPS"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.blue.arn
  }

  lifecycle {
    ignore_changes = [default_action]  # Managed by CodeDeploy
  }
}

resource "aws_lb_listener" "test" {
  load_balancer_arn = aws_lb.app.arn
  port              = 8443
  protocol          = "HTTPS"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.green.arn
  }

  lifecycle {
    ignore_changes = [default_action]
  }
}

# ECS Service with CodeDeploy
resource "aws_ecs_service" "app" {
  name            = "app"
  cluster         = module.ecs.cluster_id
  task_definition = aws_ecs_task_definition.app.arn
  desired_count   = 3

  deployment_controller {
    type = "CODE_DEPLOY"
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.blue.arn
    container_name   = "app"
    container_port   = 8080
  }

  lifecycle {
    ignore_changes = [task_definition, load_balancer]
  }
}

# CodeDeploy Application
resource "aws_codedeploy_app" "app" {
  compute_platform = "ECS"
  name             = "app-deploy"
}

# CodeDeploy Deployment Group
resource "aws_codedeploy_deployment_group" "app" {
  app_name               = aws_codedeploy_app.app.name
  deployment_group_name  = "app-dg"
  deployment_config_name = "CodeDeployDefault.ECSAllAtOnce"
  service_role_arn       = aws_iam_role.codedeploy.arn

  auto_rollback_configuration {
    enabled = true
    events  = ["DEPLOYMENT_FAILURE", "DEPLOYMENT_STOP_ON_REQUEST"]
  }

  blue_green_deployment_config {
    deployment_ready_option {
      action_on_timeout = "CONTINUE_DEPLOYMENT"
    }

    terminate_blue_instances_on_deployment_success {
      action                           = "TERMINATE"
      termination_wait_time_in_minutes = 5
    }
  }

  deployment_style {
    deployment_option = "WITH_TRAFFIC_CONTROL"
    deployment_type   = "BLUE_GREEN"
  }

  ecs_service {
    cluster_name = module.ecs.cluster_name
    service_name = aws_ecs_service.app.name
  }

  load_balancer_info {
    target_group_pair_info {
      prod_traffic_route {
        listener_arns = [aws_lb_listener.prod.arn]
      }

      test_traffic_route {
        listener_arns = [aws_lb_listener.test.arn]
      }

      target_group {
        name = aws_lb_target_group.blue.name
      }

      target_group {
        name = aws_lb_target_group.green.name
      }
    }
  }
}
```

### Trigger Blue-Green Deployment

```python
import boto3
import json

codedeploy = boto3.client('codedeploy')

def deploy_blue_green(app_name: str, deployment_group: str,
                      task_definition_arn: str, container_name: str,
                      container_port: int):
    """Trigger blue-green deployment via CodeDeploy"""

    app_spec = {
        "version": "0.0",
        "Resources": [{
            "TargetService": {
                "Type": "AWS::ECS::Service",
                "Properties": {
                    "TaskDefinition": task_definition_arn,
                    "LoadBalancerInfo": {
                        "ContainerName": container_name,
                        "ContainerPort": container_port
                    }
                }
            }
        }]
    }

    response = codedeploy.create_deployment(
        applicationName=app_name,
        deploymentGroupName=deployment_group,
        revision={
            'revisionType': 'AppSpecContent',
            'appSpecContent': {
                'content': json.dumps(app_spec)
            }
        }
    )

    deployment_id = response['deploymentId']
    print(f"Started deployment: {deployment_id}")
    return deployment_id

# Usage
deploy_blue_green(
    app_name='app-deploy',
    deployment_group='app-dg',
    task_definition_arn='arn:aws:ecs:us-east-1:123456789:task-definition/app:5',
    container_name='app',
    container_port=8080
)
```

## Canary Releases

### ALB Weighted Routing

```hcl
resource "aws_lb_listener_rule" "canary" {
  listener_arn = aws_lb_listener.prod.arn
  priority     = 100

  action {
    type = "forward"
    forward {
      target_group {
        arn    = aws_lb_target_group.stable.arn
        weight = 90
      }
      target_group {
        arn    = aws_lb_target_group.canary.arn
        weight = 10
      }
    }
  }

  condition {
    path_pattern {
      values = ["/*"]
    }
  }
}
```

### Gradual Traffic Shift

```python
def shift_traffic(listener_rule_arn: str, canary_weight: int):
    """Shift traffic percentage to canary"""
    elb = boto3.client('elbv2')

    stable_weight = 100 - canary_weight

    elb.modify_rule(
        RuleArn=listener_rule_arn,
        Actions=[{
            'Type': 'forward',
            'ForwardConfig': {
                'TargetGroups': [
                    {
                        'TargetGroupArn': stable_tg_arn,
                        'Weight': stable_weight
                    },
                    {
                        'TargetGroupArn': canary_tg_arn,
                        'Weight': canary_weight
                    }
                ]
            }
        }]
    )

    print(f"Traffic: {stable_weight}% stable, {canary_weight}% canary")

# Progressive rollout
shift_traffic(rule_arn, 10)   # 10% to canary
# Monitor metrics...
shift_traffic(rule_arn, 25)   # 25% to canary
# Monitor metrics...
shift_traffic(rule_arn, 50)   # 50% to canary
# Monitor metrics...
shift_traffic(rule_arn, 100)  # 100% to canary (promote)
```

## Deployment Circuit Breaker

### How It Works

1. ECS monitors deployment health
2. Detects repeated task failures
3. Automatically stops deployment
4. Optional: Rolls back to previous version

### Configuration

```hcl
resource "aws_ecs_service" "app" {
  deployment_circuit_breaker {
    enable   = true
    rollback = true  # Auto-rollback on failure
  }
}
```

### Failure Detection

Circuit breaker triggers when:
- Tasks fail to reach RUNNING state
- Health checks fail repeatedly
- Tasks crash shortly after starting

## GitOps Workflow

### GitHub Actions Example

```yaml
name: Deploy to ECS

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1

      - name: Login to Amazon ECR
        id: login-ecr
        uses: aws-actions/amazon-ecr-login@v2

      - name: Build and push image
        env:
          ECR_REGISTRY: ${{ steps.login-ecr.outputs.registry }}
          IMAGE_TAG: ${{ github.sha }}
        run: |
          docker build -t $ECR_REGISTRY/myapp:$IMAGE_TAG .
          docker push $ECR_REGISTRY/myapp:$IMAGE_TAG

      - name: Update task definition
        id: task-def
        uses: aws-actions/amazon-ecs-render-task-definition@v1
        with:
          task-definition: task-definition.json
          container-name: myapp
          image: ${{ steps.login-ecr.outputs.registry }}/myapp:${{ github.sha }}

      - name: Deploy to ECS
        uses: aws-actions/amazon-ecs-deploy-task-definition@v2
        with:
          task-definition: ${{ steps.task-def.outputs.task-definition }}
          service: myapp-service
          cluster: production
          wait-for-service-stability: true
```

## Rollback Strategies

### Manual Rollback

```python
def rollback_to_previous(cluster: str, service: str):
    """Rollback to previous task definition"""

    # Get current task definition
    svc = ecs.describe_services(cluster=cluster, services=[service])
    current_td = svc['services'][0]['taskDefinition']

    # Parse family and revision
    # arn:aws:ecs:region:account:task-definition/family:revision
    parts = current_td.split('/')[-1].split(':')
    family = parts[0]
    current_revision = int(parts[1])

    # Go back to previous revision
    previous_td = f"{family}:{current_revision - 1}"

    # Update service
    ecs.update_service(
        cluster=cluster,
        service=service,
        taskDefinition=previous_td
    )

    print(f"Rolling back to {previous_td}")

# Usage
rollback_to_previous('production', 'api')
```

### Automatic Rollback (Circuit Breaker)

Enabled via `deployment_circuit_breaker.rollback = true`

## Best Practices

1. **Always enable circuit breaker** with rollback for production
2. **Use blue-green** for critical services requiring instant rollback
3. **Implement health checks** at container, task, and ALB levels
4. **Pin image digests** instead of tags for reproducibility
5. **Use immutable image tags** in ECR
6. **Monitor deployments** with CloudWatch alarms
7. **Test rollback procedures** regularly
8. **Keep previous task definitions** for quick rollback

## Progressive Disclosure

### Quick Start (This File)
- Rolling updates
- Blue-green basics
- Canary releases
- Circuit breaker

### Detailed References
- **[Blue-Green Setup](references/blue-green-setup.md)**: Complete CodeDeploy configuration
- **[CI/CD Pipelines](references/cicd-pipelines.md)**: GitHub Actions, CodePipeline
- **[Monitoring](references/deployment-monitoring.md)**: CloudWatch, alarms

## Related Skills

- **boto3-ecs**: SDK patterns
- **terraform-ecs**: Infrastructure as Code
- **ecs-troubleshooting**: Debugging deployments
