---
name: aws-ecs
description: "Manage AWS ECS clusters, services, tasks, and task definitions."
metadata: {"thinkfleetbot":{"emoji":"📦","requires":{"bins":["aws","jq"],"env":["AWS_ACCESS_KEY_ID","AWS_SECRET_ACCESS_KEY"]}}}
---

# AWS ECS

Manage ECS clusters, services, and tasks.

## Environment Variables

- `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` - AWS credentials
- `AWS_DEFAULT_REGION` - Region

## List clusters

```bash
aws ecs list-clusters --query 'clusterArns[]' --output table
```

## Describe cluster

```bash
aws ecs describe-clusters --clusters my-cluster --query 'clusters[].{Name:clusterName,Status:status,Running:runningTasksCount,Pending:pendingTasksCount,Services:activeServicesCount}' --output table
```

## List services

```bash
aws ecs list-services --cluster my-cluster --query 'serviceArns[]' --output table
```

## Describe service

```bash
aws ecs describe-services --cluster my-cluster --services my-service --query 'services[].{Name:serviceName,Status:status,Running:runningCount,Desired:desiredCount,TaskDef:taskDefinition}' --output table
```

## Update service (force new deployment)

```bash
aws ecs update-service --cluster my-cluster --service my-service --force-new-deployment | jq '{serviceName: .service.serviceName, desiredCount: .service.desiredCount}'
```

## Scale service

```bash
aws ecs update-service --cluster my-cluster --service my-service --desired-count 3 | jq '{serviceName: .service.serviceName, desiredCount: .service.desiredCount}'
```

## List tasks

```bash
aws ecs list-tasks --cluster my-cluster --service-name my-service --query 'taskArns[]' --output table
```

## Describe tasks

```bash
aws ecs describe-tasks --cluster my-cluster --tasks $(aws ecs list-tasks --cluster my-cluster --service-name my-service --query 'taskArns[0]' --output text) --query 'tasks[].{TaskId:taskArn,Status:lastStatus,Health:healthStatus,StartedAt:startedAt}' --output table
```

## View task logs

```bash
aws logs tail /ecs/my-service --since 30m --format short
```

## Describe task definition

```bash
aws ecs describe-task-definition --task-definition my-task-def --query 'taskDefinition.{Family:family,Revision:revision,Cpu:cpu,Memory:memory,Containers:containerDefinitions[].{Name:name,Image:image,Cpu:cpu,Memory:memory}}' | jq .
```

## List task definition revisions

```bash
aws ecs list-task-definitions --family-prefix my-task-def --sort DESC --query 'taskDefinitionArns[:5]' --output table
```

## Run standalone task

```bash
aws ecs run-task --cluster my-cluster --task-definition my-task-def --count 1 --launch-type FARGATE \
  --network-configuration 'awsvpcConfiguration={subnets=[subnet-xxx],securityGroups=[sg-xxx],assignPublicIp=ENABLED}' | jq '.tasks[].taskArn'
```

## Notes

- Use `--force-new-deployment` to trigger a rolling update with the same task definition.
- Confirm before scaling, updating, or stopping services.
- Fargate tasks require network configuration; EC2 launch type may not.
