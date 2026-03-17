---
name: boto3-ecs
description: AWS Boto3 SDK patterns for Amazon ECS cluster management, task definitions, services, and Fargate deployments. Use when working with ECS clusters, managing task definitions, deploying services, running one-off tasks, monitoring deployments, or integrating ECS with Python applications.
---

# AWS Boto3 ECS Integration

Complete patterns for managing Amazon ECS clusters, services, and tasks using AWS Boto3 SDK.

## Quick Reference

### Client Initialization

```python
import boto3
from typing import Optional

def get_ecs_client(region_name: str = 'us-east-1',
                   profile_name: Optional[str] = None):
    """Initialize ECS client with optional profile"""
    session = boto3.Session(
        region_name=region_name,
        profile_name=profile_name
    )
    return session.client('ecs')

# Usage
ecs = get_ecs_client(region_name='us-west-2')
```

### Essential Cluster Operations

```python
# List clusters
clusters = ecs.list_clusters()
for cluster_arn in clusters['clusterArns']:
    print(cluster_arn)

# Describe cluster
cluster = ecs.describe_clusters(
    clusters=['my-cluster'],
    include=['ATTACHMENTS', 'SETTINGS', 'STATISTICS']
)
print(f"Status: {cluster['clusters'][0]['status']}")
print(f"Running Tasks: {cluster['clusters'][0]['runningTasksCount']}")

# Create cluster with Fargate
response = ecs.create_cluster(
    clusterName='my-cluster',
    capacityProviders=['FARGATE', 'FARGATE_SPOT'],
    defaultCapacityProviderStrategy=[
        {'capacityProvider': 'FARGATE', 'weight': 1, 'base': 1},
        {'capacityProvider': 'FARGATE_SPOT', 'weight': 1}
    ],
    settings=[
        {'name': 'containerInsights', 'value': 'enabled'}
    ]
)
```

### Task Definition Management

```python
# Register task definition
response = ecs.register_task_definition(
    family='my-app',
    networkMode='awsvpc',
    requiresCompatibilities=['FARGATE'],
    cpu='256',
    memory='512',
    executionRoleArn='arn:aws:iam::123456789:role/ecsTaskExecutionRole',
    taskRoleArn='arn:aws:iam::123456789:role/myAppTaskRole',
    containerDefinitions=[
        {
            'name': 'my-app',
            'image': '123456789.dkr.ecr.us-east-1.amazonaws.com/my-app:latest',
            'essential': True,
            'portMappings': [
                {'containerPort': 8080, 'protocol': 'tcp'}
            ],
            'logConfiguration': {
                'logDriver': 'awslogs',
                'options': {
                    'awslogs-group': '/ecs/my-app',
                    'awslogs-region': 'us-east-1',
                    'awslogs-stream-prefix': 'ecs'
                }
            },
            'environment': [
                {'name': 'ENV', 'value': 'production'}
            ],
            'secrets': [
                {
                    'name': 'DB_PASSWORD',
                    'valueFrom': 'arn:aws:secretsmanager:us-east-1:123456789:secret:db-password'
                }
            ]
        }
    ]
)
task_def_arn = response['taskDefinition']['taskDefinitionArn']

# Describe task definition
task_def = ecs.describe_task_definition(
    taskDefinition='my-app:1',
    include=['TAGS']
)

# List task definition families
families = ecs.list_task_definition_families(
    status='ACTIVE'
)

# List task definitions for a family
revisions = ecs.list_task_definitions(
    familyPrefix='my-app',
    status='ACTIVE',
    sort='DESC'
)
```

### Service Operations

```python
# Create service with Fargate
response = ecs.create_service(
    cluster='my-cluster',
    serviceName='my-service',
    taskDefinition='my-app:1',
    desiredCount=3,
    launchType='FARGATE',
    platformVersion='1.4.0',
    networkConfiguration={
        'awsvpcConfiguration': {
            'subnets': ['subnet-12345', 'subnet-67890'],
            'securityGroups': ['sg-12345'],
            'assignPublicIp': 'DISABLED'
        }
    },
    loadBalancers=[
        {
            'targetGroupArn': 'arn:aws:elasticloadbalancing:...:targetgroup/my-tg/...',
            'containerName': 'my-app',
            'containerPort': 8080
        }
    ],
    deploymentConfiguration={
        'maximumPercent': 200,
        'minimumHealthyPercent': 100,
        'deploymentCircuitBreaker': {
            'enable': True,
            'rollback': True
        }
    },
    enableExecuteCommand=True
)

# Update service
response = ecs.update_service(
    cluster='my-cluster',
    service='my-service',
    taskDefinition='my-app:2',
    desiredCount=5,
    forceNewDeployment=True
)

# Describe services
services = ecs.describe_services(
    cluster='my-cluster',
    services=['my-service'],
    include=['TAGS']
)
for svc in services['services']:
    print(f"{svc['serviceName']}: {svc['status']}")
    print(f"  Running: {svc['runningCount']}/{svc['desiredCount']}")

# Delete service
ecs.update_service(cluster='my-cluster', service='my-service', desiredCount=0)
ecs.delete_service(cluster='my-cluster', service='my-service')
```

### Running Tasks

```python
# Run one-off task
response = ecs.run_task(
    cluster='my-cluster',
    taskDefinition='my-app:1',
    launchType='FARGATE',
    platformVersion='1.4.0',
    count=1,
    networkConfiguration={
        'awsvpcConfiguration': {
            'subnets': ['subnet-12345'],
            'securityGroups': ['sg-12345'],
            'assignPublicIp': 'ENABLED'
        }
    },
    overrides={
        'containerOverrides': [
            {
                'name': 'my-app',
                'command': ['python', 'migrate.py'],
                'environment': [
                    {'name': 'MIGRATION_MODE', 'value': 'true'}
                ]
            }
        ]
    }
)
task_arn = response['tasks'][0]['taskArn']

# List tasks
tasks = ecs.list_tasks(
    cluster='my-cluster',
    serviceName='my-service',
    desiredStatus='RUNNING'
)

# Describe tasks
task_details = ecs.describe_tasks(
    cluster='my-cluster',
    tasks=tasks['taskArns'],
    include=['TAGS']
)
for task in task_details['tasks']:
    print(f"Task: {task['taskArn']}")
    print(f"  Status: {task['lastStatus']}")
    print(f"  Health: {task.get('healthStatus', 'N/A')}")

# Stop task
ecs.stop_task(
    cluster='my-cluster',
    task=task_arn,
    reason='Manual stop for maintenance'
)
```

### Capacity Providers

```python
# Use capacity provider strategy instead of launchType
response = ecs.create_service(
    cluster='my-cluster',
    serviceName='my-service',
    taskDefinition='my-app:1',
    desiredCount=3,
    capacityProviderStrategy=[
        {'capacityProvider': 'FARGATE', 'weight': 1, 'base': 1},
        {'capacityProvider': 'FARGATE_SPOT', 'weight': 3}
    ],
    networkConfiguration={
        'awsvpcConfiguration': {
            'subnets': ['subnet-12345'],
            'securityGroups': ['sg-12345'],
            'assignPublicIp': 'DISABLED'
        }
    }
)
```

## Common Patterns

### Error Handling

```python
from botocore.exceptions import ClientError, BotoCoreError

try:
    response = ecs.describe_services(
        cluster='my-cluster',
        services=['my-service']
    )
except ecs.exceptions.ClusterNotFoundException:
    print("Cluster not found")
except ecs.exceptions.ServiceNotFoundException:
    print("Service not found")
except ClientError as e:
    error_code = e.response['Error']['Code']
    if error_code == 'AccessDeniedException':
        print("Insufficient permissions")
    else:
        print(f"AWS Error: {error_code}")
except BotoCoreError as e:
    print(f"Connection error: {e}")
```

### Wait for Service Stable

```python
# Using waiters
waiter = ecs.get_waiter('services_stable')
waiter.wait(
    cluster='my-cluster',
    services=['my-service'],
    WaiterConfig={
        'Delay': 15,
        'MaxAttempts': 40
    }
)
print("Service is stable")

# Wait for tasks running
waiter = ecs.get_waiter('tasks_running')
waiter.wait(
    cluster='my-cluster',
    tasks=[task_arn]
)
```

### Deployment Monitoring

```python
def monitor_deployment(cluster: str, service: str, timeout: int = 600):
    """Monitor ECS deployment progress"""
    import time
    start = time.time()

    while time.time() - start < timeout:
        response = ecs.describe_services(
            cluster=cluster,
            services=[service]
        )
        svc = response['services'][0]

        # Check deployments
        for deployment in svc['deployments']:
            status = deployment['rolloutState']
            print(f"Deployment {deployment['id'][:8]}: {status}")
            print(f"  Running: {deployment['runningCount']}/{deployment['desiredCount']}")

            if status == 'COMPLETED':
                print("Deployment complete!")
                return True
            elif status == 'FAILED':
                print(f"Deployment failed: {deployment.get('rolloutStateReason', 'Unknown')}")
                return False

        time.sleep(15)

    print("Deployment timed out")
    return False
```

## Progressive Disclosure

### Quick Start (This File)
- Client initialization
- Cluster operations
- Task definition management
- Service CRUD operations
- Running tasks
- Basic error handling

### Detailed References
- **[Cluster Operations](references/cluster-operations.md)**: Cluster lifecycle, capacity providers, settings
- **[Task Definitions](references/task-definitions.md)**: Advanced container definitions, secrets, volumes
- **[Service Management](references/service-management.md)**: Deployments, load balancers, auto-scaling

## When to Use This Skill

Use this skill when:
- Managing ECS clusters programmatically
- Creating or updating task definitions
- Deploying and scaling services
- Running one-off tasks (migrations, batch jobs)
- Monitoring deployments
- Integrating ECS with Python applications

## Dependencies

```bash
pip install boto3 botocore
```

## Related Skills

- **terraform-ecs**: Infrastructure as Code for ECS
- **ecs-fargate**: Fargate-specific patterns
- **ecs-deployment**: Deployment strategies
- **ecs-troubleshooting**: Debugging guide

## Best Practices

1. **Use capacity providers** instead of launchType for flexibility
2. **Enable deployment circuit breaker** for automatic rollback
3. **Use secrets manager** for sensitive data, never environment variables
4. **Enable execute command** for debugging access
5. **Always specify platform version** (e.g., '1.4.0') explicitly
6. **Use awsvpc network mode** for Fargate (required) and EC2 (recommended)
7. **Implement proper error handling** for all API calls
8. **Use waiters** for async operations instead of polling
