---
name: ecs-troubleshooting
description: ECS troubleshooting and debugging guide covering task failures, service issues, networking problems, and performance diagnostics. Use when diagnosing ECS issues, debugging task failures (STOPPED, PENDING), resolving networking problems, investigating IAM/permissions errors, troubleshooting container health checks, or analyzing ECS service health.
---

# ECS Troubleshooting Guide

Complete guide to diagnosing and resolving common ECS issues.

## Quick Diagnostic Commands

```bash
# Check service status
aws ecs describe-services \
  --cluster production \
  --services my-service \
  --query 'services[0].{status:status,running:runningCount,desired:desiredCount,events:events[:5]}'

# List stopped tasks (failures)
aws ecs list-tasks \
  --cluster production \
  --service-name my-service \
  --desired-status STOPPED

# Describe stopped task
aws ecs describe-tasks \
  --cluster production \
  --tasks <task-arn> \
  --query 'tasks[0].{status:lastStatus,reason:stoppedReason,containers:containers[*].{name:name,reason:reason,exitCode:exitCode}}'

# View recent logs
aws logs tail /ecs/my-app --since 1h --follow

# Execute into container (debug)
aws ecs execute-command \
  --cluster production \
  --task <task-id> \
  --container my-app \
  --interactive \
  --command "/bin/sh"
```

## Task Failures

### Task Status: STOPPED

#### Symptom
Tasks immediately stop after starting or fail to start.

#### Diagnostic Steps

```python
import boto3

ecs = boto3.client('ecs')

def diagnose_stopped_task(cluster: str, task_arn: str):
    """Diagnose why a task stopped"""

    response = ecs.describe_tasks(cluster=cluster, tasks=[task_arn])
    task = response['tasks'][0]

    print(f"Task Status: {task['lastStatus']}")
    print(f"Stop Code: {task.get('stopCode', 'N/A')}")
    print(f"Stopped Reason: {task.get('stoppedReason', 'N/A')}")

    for container in task['containers']:
        print(f"\nContainer: {container['name']}")
        print(f"  Status: {container['lastStatus']}")
        print(f"  Exit Code: {container.get('exitCode', 'N/A')}")
        print(f"  Reason: {container.get('reason', 'N/A')}")
```

#### Common Causes & Solutions

**1. Essential container failed**
```
stoppedReason: "Essential container in task exited"
```
**Solution:** Check container logs for application errors

```bash
aws logs tail /ecs/my-app --since 30m
```

**2. Task failed to start**
```
stoppedReason: "Task failed to start"
```
**Solution:** Check execution role permissions

```bash
# Verify execution role can pull image
aws iam get-role-policy --role-name ecsTaskExecutionRole --policy-name ecr-access
```

**3. CannotPullContainerError**
```
reason: "CannotPullContainerError: Error response from daemon"
```
**Solutions:**
- Check ECR permissions in execution role
- Verify image exists: `aws ecr describe-images --repository-name my-app`
- Check VPC endpoints or NAT gateway for private subnets

**4. OutOfMemoryError**
```
reason: "OutOfMemoryError: Container killed due to memory usage"
exitCode: 137
```
**Solution:** Increase memory in task definition

```hcl
memory = 2048  # Increase from current value
```

**5. Exit Code 1 (Application Error)**
```
exitCode: 1
```
**Solution:** Check application logs for errors

```bash
aws logs filter-events \
  --log-group-name /ecs/my-app \
  --filter-pattern "ERROR"
```

### Task Status: PENDING

#### Symptom
Tasks stuck in PENDING state, not transitioning to RUNNING.

#### Diagnostic Steps

```python
def diagnose_pending_tasks(cluster: str, service: str):
    """Check why tasks are stuck in PENDING"""

    # List pending tasks
    pending = ecs.list_tasks(
        cluster=cluster,
        serviceName=service,
        desiredStatus='RUNNING'
    )

    for task_arn in pending['taskArns']:
        task = ecs.describe_tasks(cluster=cluster, tasks=[task_arn])['tasks'][0]

        if task['lastStatus'] == 'PENDING':
            print(f"Task {task_arn.split('/')[-1]} is PENDING")

            # Check attachments for ENI issues
            for attachment in task.get('attachments', []):
                print(f"  Attachment: {attachment['type']} - {attachment['status']}")
                for detail in attachment.get('details', []):
                    print(f"    {detail['name']}: {detail['value']}")
```

#### Common Causes & Solutions

**1. No available capacity**
```
Service my-service was unable to place a task because no container instance met all of its requirements
```
**Solutions for Fargate:**
- Check capacity provider limits
- Verify subnet has available IPs
- Check if region/AZ has Fargate capacity

**2. ENI provisioning issues**
```
Attachment status: PRECREATED
```
**Solutions:**
- Check security group allows required traffic
- Verify subnet has available IPs
- Check ENI limits for EC2 instances

**3. Image pull taking too long**
```
Container image: pulling
```
**Solutions:**
- Check image size (use smaller base images)
- Verify network connectivity to ECR
- Use VPC endpoints for faster pulls

## Service Issues

### Service Not Starting Tasks

#### Diagnostic

```bash
# Check service events
aws ecs describe-services \
  --cluster production \
  --services my-service \
  --query 'services[0].events[:10]'
```

#### Common Events & Solutions

**1. "service my-service is unable to place a task"**

Check task placement constraints and capacity.

**2. "service my-service has reached a steady state"**

Service is healthy - tasks are running as expected.

**3. "service my-service was unable to place a task because no container instance met all requirements"**

For Fargate: Check CPU/memory configurations are valid combinations.

### Deployment Stuck

#### Symptom
Deployment never reaches COMPLETED state.

#### Diagnostic

```python
def check_deployment_status(cluster: str, service: str):
    """Check deployment progress"""

    response = ecs.describe_services(cluster=cluster, services=[service])
    svc = response['services'][0]

    for deployment in svc['deployments']:
        print(f"\nDeployment: {deployment['id']}")
        print(f"  Status: {deployment['status']}")
        print(f"  Rollout State: {deployment['rolloutState']}")
        print(f"  Tasks: {deployment['runningCount']}/{deployment['desiredCount']}")

        if deployment['rolloutState'] == 'IN_PROGRESS':
            reason = deployment.get('rolloutStateReason', '')
            print(f"  Reason: {reason}")
```

#### Common Causes

**1. Health check failures**
```
rolloutStateReason: "ECS deployment circuit breaker: tasks failed to start"
```
**Solutions:**
- Check target group health check settings
- Increase `healthCheckGracePeriodSeconds`
- Verify application responds on health check path

**2. Insufficient capacity**
```
rolloutStateReason: "Service my-service was unable to place a task"
```
**Solutions:**
- Check subnet IP availability
- Reduce `maximumPercent` to allow more headroom

## Networking Issues

### Tasks Cannot Connect to Internet

#### Symptoms
- Cannot pull images
- Cannot reach external APIs
- Timeouts on external calls

#### Solutions

**For private subnets:**
```hcl
# Option 1: NAT Gateway
resource "aws_nat_gateway" "main" {
  allocation_id = aws_eip.nat.id
  subnet_id     = aws_subnet.public.id
}

# Option 2: VPC Endpoints (recommended)
resource "aws_vpc_endpoint" "ecr_api" {
  vpc_id            = aws_vpc.main.id
  service_name      = "com.amazonaws.us-east-1.ecr.api"
  vpc_endpoint_type = "Interface"
  subnet_ids        = aws_subnet.private[*].id
}
```

### Tasks Cannot Connect to Each Other

#### Symptom
Service-to-service communication fails.

#### Diagnostic

```bash
# Check security group rules
aws ec2 describe-security-groups \
  --group-ids sg-12345 \
  --query 'SecurityGroups[0].IpPermissions'
```

#### Solutions

```hcl
# Allow traffic between ECS tasks
resource "aws_security_group_rule" "ecs_to_ecs" {
  type                     = "ingress"
  from_port                = 8080
  to_port                  = 8080
  protocol                 = "tcp"
  security_group_id        = aws_security_group.ecs_tasks.id
  source_security_group_id = aws_security_group.ecs_tasks.id
}
```

### Load Balancer Health Checks Failing

#### Symptom
```
Target group app-tg: 0 healthy, 3 unhealthy
```

#### Diagnostic

```bash
# Check target health
aws elbv2 describe-target-health \
  --target-group-arn <target-group-arn>
```

#### Common Causes & Solutions

**1. Wrong health check path**
```hcl
health_check {
  path = "/health"  # Must match application endpoint
}
```

**2. Container not listening on expected port**
```bash
# Verify inside container
aws ecs execute-command --cluster production --task <task-id> \
  --container my-app --interactive --command "netstat -tlnp"
```

**3. Security group blocking ALB**
```hcl
# Allow ALB to reach ECS tasks
resource "aws_security_group_rule" "alb_to_ecs" {
  type                     = "ingress"
  from_port                = 8080
  to_port                  = 8080
  protocol                 = "tcp"
  security_group_id        = aws_security_group.ecs_tasks.id
  source_security_group_id = aws_security_group.alb.id
}
```

## IAM & Permissions Issues

### CannotPullContainerError

#### Symptom
```
CannotPullContainerError: Error response from daemon: pull access denied
```

#### Solution: Task Execution Role

```hcl
resource "aws_iam_role_policy_attachment" "ecs_task_execution" {
  role       = aws_iam_role.ecs_task_execution.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

# For cross-account ECR
resource "aws_iam_role_policy" "cross_account_ecr" {
  role = aws_iam_role.ecs_task_execution.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = [
        "ecr:GetDownloadUrlForLayer",
        "ecr:BatchGetImage"
      ]
      Resource = "arn:aws:ecr:*:OTHER_ACCOUNT:repository/*"
    }]
  })
}
```

### Secrets Access Denied

#### Symptom
```
ResourceInitializationError: unable to pull secrets
```

#### Solution

```hcl
resource "aws_iam_role_policy" "secrets_access" {
  role = aws_iam_role.ecs_task_execution.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = ["secretsmanager:GetSecretValue"]
        Resource = "arn:aws:secretsmanager:*:*:secret:my-app/*"
      },
      {
        Effect = "Allow"
        Action = ["ssm:GetParameters"]
        Resource = "arn:aws:ssm:*:*:parameter/my-app/*"
      },
      {
        Effect = "Allow"
        Action = ["kms:Decrypt"]
        Resource = aws_kms_key.secrets.arn
      }
    ]
  })
}
```

### Execute Command Not Working

#### Symptom
```
SessionManagerPlugin is not found
```
or
```
Execute command is disabled
```

#### Solutions

**1. Enable execute command on service**
```hcl
resource "aws_ecs_service" "app" {
  enable_execute_command = true
}
```

**2. Add SSM permissions to task role**
```hcl
resource "aws_iam_role_policy" "ssm_exec" {
  role = aws_iam_role.ecs_task.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = [
        "ssmmessages:CreateControlChannel",
        "ssmmessages:CreateDataChannel",
        "ssmmessages:OpenControlChannel",
        "ssmmessages:OpenDataChannel"
      ]
      Resource = "*"
    }]
  })
}
```

## Performance Issues

### High CPU/Memory Usage

#### Diagnostic

```python
import boto3

cloudwatch = boto3.client('cloudwatch')

def get_service_metrics(cluster: str, service: str):
    """Get CPU and memory metrics"""

    response = cloudwatch.get_metric_statistics(
        Namespace='AWS/ECS',
        MetricName='CPUUtilization',
        Dimensions=[
            {'Name': 'ClusterName', 'Value': cluster},
            {'Name': 'ServiceName', 'Value': service}
        ],
        StartTime=datetime.utcnow() - timedelta(hours=1),
        EndTime=datetime.utcnow(),
        Period=300,
        Statistics=['Average', 'Maximum']
    )

    for point in sorted(response['Datapoints'], key=lambda x: x['Timestamp']):
        print(f"{point['Timestamp']}: Avg={point['Average']:.1f}%, Max={point['Maximum']:.1f}%")
```

#### Solutions

**1. Right-size tasks**
```hcl
# Increase resources
cpu    = "1024"  # from 512
memory = "2048"  # from 1024
```

**2. Enable auto-scaling**
```hcl
resource "aws_appautoscaling_policy" "cpu" {
  target_tracking_scaling_policy_configuration {
    target_value = 70.0
  }
}
```

### Slow Task Startup

#### Causes & Solutions

**1. Large container image**
- Use smaller base images (alpine, distroless)
- Enable image caching with Fargate Platform 1.4.0

**2. Slow application startup**
- Increase `startPeriod` in health check
- Optimize application initialization

**3. Slow secret/config loading**
- Use VPC endpoints for faster access
- Cache configuration at startup

## Log Analysis

### CloudWatch Logs Queries

```bash
# Find errors in last hour
aws logs filter-events \
  --log-group-name /ecs/my-app \
  --start-time $(date -d '-1 hour' +%s000) \
  --filter-pattern "ERROR"

# Find OOM kills
aws logs filter-events \
  --log-group-name /ecs/my-app \
  --filter-pattern "OutOfMemory"

# Find slow requests
aws logs filter-events \
  --log-group-name /ecs/my-app \
  --filter-pattern "[timestamp, level, duration>1000, ...]"
```

### CloudWatch Insights

```sql
-- Top errors by count
fields @timestamp, @message
| filter @message like /ERROR/
| stats count(*) as errorCount by @message
| sort errorCount desc
| limit 10

-- Average response time
fields @timestamp, responseTime
| stats avg(responseTime) as avgTime, max(responseTime) as maxTime by bin(5m)
```

## Related Skills

- **boto3-ecs**: SDK patterns
- **terraform-ecs**: Infrastructure as Code
- **ecs-fargate**: Fargate specifics
- **ecs-deployment**: Deployment strategies

## Quick Reference

| Symptom | First Check | Common Cause |
|---------|-------------|--------------|
| Task STOPPED | `stoppedReason` | Container crash, OOM |
| Task PENDING | Attachments | ENI/network issues |
| Deployment stuck | Health checks | ALB health check failing |
| Cannot pull image | Execution role | Missing ECR permissions |
| Cannot connect | Security groups | Wrong SG rules |
