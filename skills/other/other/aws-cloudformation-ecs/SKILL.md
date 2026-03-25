---
name: aws-cloudformation-ecs
description: Provides AWS CloudFormation patterns for ECS clusters, task definitions, services, container definitions, auto scaling, blue/green deployments, CodeDeploy integration, ALB integration, service discovery, monitoring, logging, template structure, parameters, outputs, and cross-stack references. Use when creating ECS clusters with CloudFormation, configuring Fargate and EC2 launch types, implementing blue/green deployments, managing auto scaling, integrating with ALB and NLB, and implementing ECS best practices.
allowed-tools: Read, Write, Bash
---

# AWS CloudFormation ECS

## Overview

Provides CloudFormation patterns for ECS clusters, task definitions, services, container definitions, auto scaling, blue/green deployments, ALB integration, monitoring, and cross-stack references.

## When to Use

- Creating or updating ECS clusters with CloudFormation
- Configuring Fargate/EC2 launch types and capacity providers
- Deploying services with ALB/NLB integration or blue/green deployments
- Implementing auto scaling for ECS services
- Setting up monitoring with Container Insights

## Instructions

Follow these steps to create ECS infrastructure with CloudFormation:

### 1. Define ECS Cluster Parameters

Specify launch type, networking, and capacity settings:

```yaml
Parameters:
  LaunchType:
    Type: String
    Default: FARGATE
    AllowedValues:
      - EC2
      - FARGATE
    Description: ECS launch type

  ContainerPort:
    Type: Number
    Default: 80
    Description: Container port

  TaskCPU:
    Type: String
    Default: 256
    AllowedValues:
      - 256
      - 512
      - 1024
      - 2048
      - 4096
    Description: Task CPU units

  TaskMemory:
    Type: String
    Default: 512
    AllowedValues:
      - 512
      - 1024
      - 2048
      - 3072
      - 4096
      - 5120
      - 6144
      - 7168
      - 8192
      - 9216
      - 10240
    Description: Task memory in MB
```

### 2. Create ECS Cluster

Define the cluster infrastructure:

```yaml
Resources:
  ECSCluster:
    Type: AWS::ECS::Cluster
    Properties:
      ClusterName: !Sub "${AWS::StackName}-cluster"
      ClusterSettings:
        - Name: containerInsights
          Value: enabled
      CapacityProviders:
        - FARGATE
        - FARGATE_SPOT
      DefaultCapacityProviderStrategy:
        - CapacityProvider: FARGATE
          Weight: 1
        - CapacityProvider: FARGATE_SPOT
          Weight: 0
```

### 3. Create Task Definition

Define container configurations:

```yaml
Resources:
  TaskDefinition:
    Type: AWS::ECS::TaskDefinition
    Properties:
      Family: !Sub "${AWS::StackName}-task"
      NetworkMode: awsvpc
      RequiresCompatibilities:
        - FARGATE
      Cpu: !Ref TaskCPU
      Memory: !Ref TaskMemory
      ExecutionRoleArn: !Ref ExecutionRole
      TaskRoleArn: !Ref TaskRole
      ContainerDefinitions:
        - Name: application
          Image: !Ref ImageUrl
          PortMappings:
            - ContainerPort: !Ref ContainerPort
              Protocol: tcp
          Environment:
            - Name: LOG_LEVEL
              Value: INFO
          LogConfiguration:
            LogDriver: awslogs
            Options:
              awslogs-group: !Ref LogGroup
              awslogs-region: !Ref AWS::Region
              awslogs-stream-prefix: ecs
          Memory: !Ref TaskMemory
```

**Validate task definition syntax before proceeding:**
```bash
aws cloudformation validate-template --template-body file://template.yaml
```

### 4. Configure Execution Roles

Set up IAM roles for task execution:

```yaml
Resources:
  ExecutionRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: "2012-10-17"
        Statement:
          - Effect: Allow
            Principal:
              Service: ecs-tasks.amazonaws.com
            Action: sts:AssumeRole
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy

  TaskRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: "2012-10-17"
        Statement:
          - Effect: Allow
            Principal:
              Service: ecs-tasks.amazonaws.com
            Action: sts:AssumeRole
      Policies:
        - PolicyName: S3Access
          PolicyDocument:
            Version: "2012-10-17"
            Statement:
              - Effect: Allow
                Action:
                  - s3:GetObject
                Resource: !Sub "${DataBucket.Arn}/*"
```

### 5. Create ECS Service

Define the service configuration:

```yaml
Resources:
  ECSService:
    Type: AWS::ECS::Service
    Properties:
      ServiceName: !Sub "${AWS::StackName}-service"
      Cluster: !Ref ECSCluster
      TaskDefinition: !Ref TaskDefinition
      DesiredCount: 2
      LaunchType: FARGATE
      NetworkConfiguration:
        AwsvpcConfiguration:
          Subnets:
            - !Ref PrivateSubnet1
            - !Ref PrivateSubnet2
          SecurityGroups:
            - !Ref SecurityGroup
          AssignPublicIp: DISABLED
      LoadBalancers:
        - TargetGroupArn: !Ref TargetGroup
          ContainerName: application
          ContainerPort: !Ref ContainerPort
```

### 6. Configure Load Balancer

Set up ALB for traffic distribution:

```yaml
Resources:
  LoadBalancer:
    Type: AWS::ElasticLoadBalancingV2::LoadBalancer
    Properties:
      Name: !Sub "${AWS::StackName}-alb"
      Scheme: internet-facing
      Type: application
      Subnets:
        - !Ref PublicSubnet1
        - !Ref PublicSubnet2
      SecurityGroups:
        - !Ref ALBSecurityGroup

  TargetGroup:
    Type: AWS::ElasticLoadBalancingV2::TargetGroup
    Properties:
      Port: 80
      Protocol: HTTP
      VpcId: !Ref VPC
      TargetType: ip

  Listener:
    Type: AWS::ElasticLoadBalancingV2::Listener
    Properties:
      DefaultActions:
        - TargetGroupArn: !Ref TargetGroup
          Type: forward
      LoadBalancerArn: !Ref LoadBalancer
      Port: 80
      Protocol: HTTP
```

### 7. Implement Auto Scaling

Configure Application Auto Scaling:

```yaml
Resources:
  ScalableTarget:
    Type: AWS::ApplicationAutoScaling::ScalableTarget
    Properties:
      MaxCapacity: 10
      MinCapacity: 1
      ResourceId: !Sub "service/${ECSCluster}/${ECSService}"
      ScalableDimension: ecs:service:DesiredCount
      ServiceNamespace: ecs

  ScalingPolicy:
    Type: AWS::ApplicationAutoScaling::ScalingPolicy
    Properties:
      PolicyName: !Sub "${AWS::StackName}-scaling"
      PolicyType: TargetTrackingScaling
      ScalingTargetId: !Ref ScalableTarget
      TargetTrackingScalingPolicyConfiguration:
        TargetValue: 70.0
        PredefinedMetricSpecification:
          PredefinedMetricType: ECSServiceAverageCPUUtilization
```

### 8. Configure Monitoring

Enable CloudWatch Container Insights:

```yaml
Resources:
  LogGroup:
    Type: AWS::Logs::LogGroup
    Properties:
      LogGroupName: !Sub "/ecs/${AWS::StackName}"
      RetentionInDays: 7
```

**Before deployment:** Create a change set to preview changes:
```bash
aws cloudformation create-change-set \
  --stack-name my-ecs-stack \
  --template-body file://template.yaml \
  --change-set-type CREATE
aws cloudformation execute-change-set --change-set-name <arn>
```

## Best Practices

### Task Definition
- Use `Family` naming for version tracking and immutable deployments
- Keep task definition under 1 KB (CloudFormation limit) by referencing external configs
- Configure `HealthCheck` in container definitions for ECS health monitoring
- Set both `Cpu` and `Memory` at task level for Fargate

### Service Deployment
- Enable `DeploymentCircuitBreaker` for automatic rollback on failures
- Use `HealthCheckGracePeriodSeconds` matching application startup time
- Configure `MinimumHealthyPercent` (100) and `MaximumPercent` (200) for zero-downtime updates
- Reference task definition by logical ID only—ECS automatically uses latest revision

### Networking
- Always use `awsvpc` network mode for Fargate
- Place tasks in private subnets with NAT gateway for outbound access
- Configure security groups to allow only required ports (not 0.0.0.0/0)

### Scaling
- Use Fargate Spot with base capacity of 1 on-demand for cost optimization
- Set `MaxHealthyDuration` on capacity provider strategy for Spot interruption handling
- Monitor `STEADY_STATE` failures in CloudWatch for task startup issues

## Constraints and Warnings

### Resource Limits
- Task definition size limit: 1 KB when using CloudFormation (use ParameterStore/Secrets Manager for large configs)
- Maximum 10 containers per task definition in Fargate
- CPU must be specified for Fargate tasks (256-4096 units, in 1024 increments)
- Memory must be allocated (512-30720 MB depending on CPU)

### Operational Limits
- ENI limits apply per subnet—plan for at least 1 ENI per task in each AZ
- Fargate Spot tasks receive 2-minute interruption notice—implement graceful shutdown signals (SIGTERM)
- Service updates require new task definition revision—cannot modify existing versions
- `DesiredCount` updates during deployment may conflict with auto scaling policies

### CloudFormation-Specific
- Cross-stack references required for VPC IDs, Subnet IDs, and Security Group IDs passed between stacks
- Use `!GetAtt` for referencing stack outputs in same template
- Ensure IAM role ARNs use `Fn::Sub` with stack name for portability

## Examples

### Minimal Fargate Service
```yaml
AWSTemplateFormatVersion: "2010-09-09"
Description: Minimal ECS Fargate service

Resources:
  Cluster:
    Type: AWS::ECS::Cluster
    Properties:
      ClusterName: !Sub "${AWS::StackName}-cluster"

  TaskDefinition:
    Type: AWS::ECS::TaskDefinition
    Properties:
      Family: !Sub "${AWS::StackName}-task"
      NetworkMode: awsvpc
      RequiresCompatibilities: [FARGATE]
      Cpu: 256
      Memory: 512
      ContainerDefinitions:
        - Name: app
          Image: nginx:latest
          PortMappings:
            - ContainerPort: 80

  Service:
    Type: AWS::ECS::Service
    Properties:
      Cluster: !Ref Cluster
      ServiceName: !Sub "${AWS::StackName}-svc"
      TaskDefinition: !Ref TaskDefinition
      DesiredCount: 2
      LaunchType: FARGATE
      DeploymentCircuitBreaker:
        Enable: true
        Rollback: true
```

### ECS with ALB Integration
```yaml
Resources:
  Service:
    Type: AWS::ECS::Service
    Properties:
      Cluster: !Ref ECSCluster
      TaskDefinition: !Ref TaskDefinition
      DesiredCount: 2
      LaunchType: FARGATE
      HealthCheckGracePeriodSeconds: 30
      NetworkConfiguration:
        AwsvpcConfiguration:
          Subnets: [!Ref PrivateSubnet1, !Ref PrivateSubnet2]
          SecurityGroups: [!Ref TaskSecurityGroup]
      LoadBalancers:
        - TargetGroupArn: !Ref TargetGroup
          ContainerName: app
          ContainerPort: 8080

  TargetGroup:
    Type: AWS::ElasticLoadBalancingV2::TargetGroup
    Properties:
      Port: 80
      Protocol: HTTP
      VpcId: !Ref VPC
      TargetType: ip
      HealthCheckPath: /health
```

## References

For detailed implementation guidance, see:

- **[constraints.md](references/constraints.md)** - Resource limits (task definition size, container limits, memory limits, CPU limits), operational constraints (service updates, ENI limits, task start time, scaling delays), security constraints (IAM roles, network mode, security groups, secrets rotation), cost considerations (Fargate pricing, data transfer, ECR storage, monitoring), deployment constraints (blue/green requirements, CodeDeploy integration, rollbacks, task drift), and availability constraints (Fargate Spot, multi-AZ, health checks, service discovery)

## Related Resources

- [AWS ECS Documentation](https://docs.aws.amazon.com/ecs/)
- [ECS Task Definitions](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task_definitions.html)
- [ECS Services](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs_services.html)
- [AWS CloudFormation User Guide](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/)
- [ECS Blue/Green Deployments](https://docs.aws.amazon.com/codedeploy/latest/userguide/deployment-steps-ecs.html)
- [CloudFormation Stack Policies](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/protect-stack-resources.html)
- [CloudFormation Drift Detection](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/detect-drift-stack.html)
- [CloudFormation Change Sets](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-changesets.html)
