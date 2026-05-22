---
name: aws-cloudformation-ecs
description: AWS CloudFormation patterns for ECS clusters, services, and task definitions. Use when creating ECS infrastructure with CloudFormation, configuring container definitions, scaling policies, service discovery, load balancing integration, and implementing template structure with Parameters, Outputs, Mappings, Conditions, cross-stack references, and blue/green deployments with CodeDeploy.
category: aws
tags: [aws, cloudformation, ecs, containers, docker, orchestration, infrastructure, iaac]
version: 1.1.0
allowed-tools: Read, Write, Bash
---

# AWS CloudFormation ECS

Create production-ready container infrastructure using AWS CloudFormation templates. This skill covers ECS clusters, services, task definitions, container configurations, scaling, service discovery, load balancing, and blue/green deployments with CodeDeploy.

## When to Use

Use this skill when:
- Creating new ECS clusters with CloudFormation
- Defining task definitions for container workloads
- Configuring ECS services with deployment strategies
- Integrating ECS with Application Load Balancer
- Implementing auto scaling for ECS services
- Configuring service discovery with Cloud Map
- Implementing blue/green deployments with CodeDeploy
- Organizing templates with Parameters, Outputs, Mappings, Conditions
- Implementing cross-stack references with export/import
- Using Transform for macro and reuse

## Template Structure

### Base Template with Standard Format

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: ECS cluster with service and load balancer

Metadata:
  AWS::CloudFormation::Interface:
    ParameterGroups:
      - Label:
          default: Cluster Configuration
        Parameters:
          - ClusterName
          - InstanceType
          - DesiredCapacity
      - Label:
          default: Container Configuration
        Parameters:
          - ContainerName
          - ContainerImage
          - ContainerPort

Parameters:
  ClusterName:
    Type: String
    Default: production-ecs-cluster
    Description: Name of the ECS cluster

  InstanceType:
    Type: String
    Default: t3.medium
    AllowedValues:
      - t3.small
      - t3.medium
      - t3.large
      - m5.large

  DesiredCapacity:
    Type: Number
    Default: 2
    MinValue: 1
    MaxValue: 20
    Description: Initial number of EC2 instances

  ContainerName:
    Type: String
    Default: web-app
    Description: Name of the container

  ContainerImage:
    Type: String
    Default: nginx:latest
    Description: Docker image for the container

  ContainerPort:
    Type: Number
    Default: 80
    Description: Port the container listens on

Mappings:
  EnvironmentConfig:
    dev:
      InstanceType: t3.small
      DesiredCapacity: 1
      ContainerMemoryHardLimit: 256
      ContainerMemorySoftLimit: 128
    staging:
      InstanceType: t3.medium
      DesiredCapacity: 2
      ContainerMemoryHardLimit: 512
      ContainerMemorySoftLimit: 256
    production:
      InstanceType: t3.large
      DesiredCapacity: 3
      ContainerMemoryHardLimit: 1024
      ContainerMemorySoftLimit: 512

Conditions:
  IsProduction: !Equals [!Ref Environment, production]
  UseSpotInstances: !Equals [!Ref SpotInstances, true]

Transform:
  - AWS::Serverless-2016-10-31

Resources:
  # ECS Cluster
  ECSCluster:
    Type: AWS::ECS::Cluster
    Properties:
      ClusterName: !Ref ClusterName
      ClusterSettings:
        - Name: containerInsights
          Value: enabled

  # EC2 Instance Configuration
  InstanceCapacity:
    Type: AWS::AutoScaling::LaunchConfiguration
    Properties:
      ImageId: !Ref AmiId
      InstanceType: !Ref InstanceType
      IamInstanceProfile: !Ref EcsInstanceProfile
      SecurityGroups:
        - !Ref EcsSecurityGroup
      UserData:
        Fn::Base64: !Sub |
          #!/bin/bash
          echo "ECS_CLUSTER=${ECSCluster.Name}" >> /etc/ecs/ecs.config
          echo "ECS_BACKEND_HOST=${ECSBackendHost}" >> /etc/ecs/ecs.config
      BlockDeviceMappings:
        - DeviceName: /dev/xvda
          Ebs:
            VolumeSize: 30
            VolumeType: gp3

  AutoScalingGroup:
    Type: AWS::AutoScaling::AutoScalingGroup
    Properties:
      AutoScalingGroupName: !Sub "${ClusterName}-asg"
      LaunchConfigurationName: !Ref InstanceCapacity
      MinSize: !Ref DesiredCapacity
      MaxSize: !Ref MaxCapacity
      DesiredCapacity: !Ref DesiredCapacity
      VPCZoneIdentifier: !Ref SubnetIds
      Tags:
        - Key: Name
          Value: !Sub "${ClusterName}-instance"
          PropagateAtLaunch: true
        - Key: Environment
          Value: !Ref Environment
          PropagateAtLaunch: true

Outputs:
  ClusterName:
    Description: Name of the ECS cluster
    Value: !Ref ECSCluster
    Export:
      Name: !Sub "${AWS::StackName}-ClusterName"

  ClusterArn:
    Description: ARN of the ECS cluster
    Value: !GetAtt ECSCluster.Arn
    Export:
      Name: !Sub "${AWS::StackName}-ClusterArn"
```

## Parameters Best Practices

### AWS-Specific Parameter Types

```yaml
Parameters:
  # AWS-specific types for validation
  VpcId:
    Type: AWS::EC2::VPC::Id
    Description: VPC where ECS cluster will be created

  SubnetIds:
    Type: List<AWS::EC2::Subnet::Id>
    Description: Subnets for ECS instances

  SecurityGroupIds:
    Type: List<AWS::EC2::SecurityGroup::Id>
    Description: Security groups for ECS service

  ClusterArn:
    Type: AWS::ECS::Cluster::Arn
    Description: ARN of existing ECS cluster

  TaskDefinitionArn:
    Type: AWS::ECS::TaskDefinition::Arn
    Description: ARN of ECS task definition

  ServiceArn:
    Type: AWS::ECS::Service::Arn
    Description: ARN of ECS service

  LoadBalancerArn:
    Type: AWS::ElasticLoadBalancingV2::LoadBalancer::Arn
    Description: ARN of Application Load Balancer

  TargetGroupArn:
    Type: AWS::ElasticLoadBalancingV2::TargetGroup::Arn
    Description: ARN of Target Group
```

### Parameter Constraints

```yaml
Parameters:
  ContainerName:
    Type: String
    Default: web-app
    Description: Container name
    ConstraintDescription: Must be 1-256 characters, alphanumeric and hyphens
    MinLength: 1
    MaxLength: 256
    AllowedPattern: "[a-zA-Z0-9-]+"

  DesiredCount:
    Type: Number
    Default: 2
    Description: Desired number of tasks
    MinValue: 0
    MaxValue: 1000
    ConstraintDescription: Must be between 0 and 1000

  Cpu:
    Type: String
    Default: 256
    Description: CPU units for container
    AllowedValues:
      - 128
      - 256
      - 512
      - 1024
      - 2048
      - 4096
    ConstraintDescription: Must be a valid CPU value

  Memory:
    Type: Number
    Default: 512
    Description: Memory limit in MiB
    MinValue: 4
    MaxValue: 15000
    ConstraintDescription: Must be between 4 and 15000 MiB
```

### SSM Parameter References

```yaml
Parameters:
  ContainerImage:
    Type: AWS::SSM::Parameter::Value<String>
    Default: /ecs/app/container-image
    Description: Container image from SSM Parameter Store

  DatabaseConnectionString:
    Type: AWS::SSM::Parameter::Value<SecureString>
    Default: /ecs/app/database/connection
    Description: Database connection from SSM
```

## Outputs and Cross-Stack References

### Export/Import Patterns

```yaml
# Stack A - Network Stack
AWSTemplateFormatVersion: 2010-09-09
Description: Network infrastructure stack for ECS

Resources:
  VPC:
    Type: AWS::EC2::VPC
    Properties:
      CidrBlock: 10.0.0.0/16
      EnableDnsHostnames: true
      EnableDnsSupport: true
      Tags:
        - Key: Name
          Value: !Sub "${AWS::StackName}-vpc"

  PublicSubnets:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref VPC
      AvailabilityZone: !Select [0, !GetAZs ""]
      CidrBlock: 10.0.1.0/24
      MapPublicIpOnLaunch: true

  PrivateSubnets:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref VPC
      AvailabilityZone: !Select [0, !GetAZs ""]
      CidrBlock: 10.0.2.0/24

Outputs:
  VpcId:
    Description: VPC ID
    Value: !Ref VPC
    Export:
      Name: !Sub "${AWS::StackName}-VpcId"

  PublicSubnetIds:
    Description: Public subnet IDs
    Value: !Join [",", [!Ref PublicSubnet1, !Ref PublicSubnet2]]
    Export:
      Name: !Sub "${AWS::StackName}-PublicSubnetIds"

  PrivateSubnetIds:
    Description: Private subnet IDs
    Value: !Join [",", [!Ref PrivateSubnet1, !Ref PrivateSubnet2]]
    Export:
      Name: !Sub "${AWS::StackName}-PrivateSubnetIds"

  EcsSecurityGroupId:
    Description: Security group ID for ECS
    Value: !Ref EcsSecurityGroup
    Export:
      Name: !Sub "${AWS::StackName}-EcsSecurityGroupId"
```

```yaml
# Stack B - ECS Stack (imports from Stack A)
AWSTemplateFormatVersion: 2010-09-09
Description: ECS application stack

Parameters:
  NetworkStackName:
    Type: String
    Default: network-stack
    Description: Name of the network stack

Resources:
  ECSService:
    Type: AWS::ECS::Service
    Properties:
      ServiceName: !Sub "${AWS::StackName}-service"
      Cluster: !ImportValue
        !Sub "${NetworkStackName}-ClusterArn"
      TaskDefinition: !Ref TaskDefinition
      DesiredCount: 2
      LaunchType: EC2
      NetworkConfiguration:
        AwsvpcConfiguration:
          AssignPublicIp: DISABLED
          SecurityGroups:
            - !ImportValue
              !Sub "${NetworkStackName}-EcsSecurityGroupId"
          Subnets:
            - !Select [0, !Split [",", !ImportValue !Sub "${NetworkStackName}-PrivateSubnetIds"]]
            - !Select [1, !Split [",", !ImportValue !Sub "${NetworkStackName}-PrivateSubnetIds"]]
```

### Nested Stacks for Modularity

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: Main stack with nested ECS stacks

Resources:
  # Nested stack for cluster
  ClusterStack:
    Type: AWS::CloudFormation::Stack
    Properties:
      TemplateURL: https://s3.amazonaws.com/bucket/ecs-cluster.yaml
      TimeoutInMinutes: 30
      Parameters:
        ClusterName: !Ref ClusterName
        Environment: !Ref Environment

  # Nested stack for services
  ServicesStack:
    Type: AWS::CloudFormation::Stack
    Properties:
      TemplateURL: https://s3.amazonaws.com/bucket/ecs-services.yaml
      TimeoutInMinutes: 30
      Parameters:
        ClusterArn: !GetAtt ClusterStack.Outputs.ClusterArn
        Environment: !Ref Environment

  # Nested stack for load balancer
  LoadBalancerStack:
    Type: AWS::CloudFormation::Stack
    Properties:
      TemplateURL: https://s3.amazonaws.com/bucket/ecs-alb.yaml
      TimeoutInMinutes: 30
      Parameters:
        VpcId: !Ref VpcId
        Subnets: !Ref Subnets
```

## ECS Task Definitions

### Basic Task Definition

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: ECS task definition

Resources:
  TaskDefinition:
    Type: AWS::ECS::TaskDefinition
    Properties:
      Family: web-app-task
      Cpu: "512"
      Memory: "1024"
      NetworkMode: awsvpc
      RequiresCompatibilities:
        - EC2
        - FARGATE
      ExecutionRoleArn: !Ref TaskExecutionRole
      TaskRoleArn: !Ref TaskRole
      ContainerDefinitions:
        - Name: web-app
          Image: !Ref ContainerImage
          Cpu: 256
          Memory: 512
          PortMappings:
            - ContainerPort: !Ref ContainerPort
              Protocol: tcp
          Environment:
            - Name: ENVIRONMENT
              Value: !Ref Environment
            - Name: LOG_LEVEL
              Value: INFO
          Secrets:
            - Name: DATABASE_URL
              ValueFrom: !Ref DatabaseSecretArn
          LogConfiguration:
            LogDriver: awslogs
            Options:
              awslogs-group: !Ref LogGroup
              awslogs-region: !Ref AWS::Region
              awslogs-stream-prefix: ecs
          HealthCheck:
            Command:
              - CMD-SHELL
              - curl -f http://localhost:8080/health || exit 1
            Interval: 30
            Timeout: 5
            Retries: 3
            StartPeriod: 60

  TaskExecutionRole:
    Type: AWS::IAM::Role
    Properties:
      RoleName: !Sub "${AWS::StackName}-task-execution-role"
      AssumeRolePolicyDocument:
        Version: "2012-10-17"
        Statement:
          - Effect: Allow
            Principal:
              Service: ecs-tasks.amazonaws.com
            Action: sts:AssumeRole
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy
      Policies:
        - PolicyName: EcsSecretsPolicy
          PolicyDocument:
            Version: "2012-10-17"
            Statement:
              - Effect: Allow
                Action:
                  - secretsmanager:GetSecretValue
                Resource: !Ref DatabaseSecretArn
        - PolicyName: EcsLogsPolicy
          PolicyDocument:
            Version: "2012-10-17"
            Statement:
              - Effect: Allow
                Action:
                  - logs:CreateLogStream
                  - logs:PutLogEvents
                Resource: !GetAtt LogGroup.Arn

  LogGroup:
    Type: AWS::Logs::LogGroup
    Properties:
      LogGroupName: !Sub "/ecs/${AWS::StackName}"
      RetentionInDays: 30
```

### Multi-Container Task Definition

```yaml
Resources:
  TaskDefinition:
    Type: AWS::ECS::TaskDefinition
    Properties:
      Family: multi-container-task
      Cpu: "1024"
      Memory: "2048"
      NetworkMode: awsvpc
      ContainerDefinitions:
        - Name: web
          Image: nginx:latest
          Cpu: 256
          Memory: 512
          PortMappings:
            - ContainerPort: 80
              Protocol: tcp
          DependsOn:
            - ContainerName: app
              Condition: HEALTHY
          Environment:
            - Name: BACKEND_URL
              Value: !Sub "http://localhost:${AppPort}"
          LogConfiguration:
            LogDriver: awslogs
            Options:
              awslogs-group: !Ref LogGroup
              awslogs-region: !Ref AWS::Region
              awslogs-stream-prefix: web

        - Name: app
          Image: !Ref AppImage
          Cpu: 512
          Memory: 1024
          PortMappings:
            - ContainerPort: !Ref AppPort
              Protocol: tcp
          Environment:
            - Name: DATABASE_URL
              ValueFrom: !Ref DatabaseSecretArn
            - Name: REDIS_URL
              ValueFrom: !Ref RedisSecretArn
          LogConfiguration:
            LogDriver: awslogs
            Options:
              awslogs-group: !Ref LogGroup
              awslogs-region: !Ref AWS::Region
              awslogs-stream-prefix: app

        - Name: redis
          Image: redis:alpine
          Cpu: 128
          Memory: 256
          PortMappings:
            - ContainerPort: 6379
              Protocol: tcp
          HealthCheck:
            Command:
              - CMD-SHELL
              - redis-cli ping | grep -q PONG
            Interval: 10
            Timeout: 5
            Retries: 3
```

## ECS Services

### Service with Application Load Balancer

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: ECS service with ALB

Resources:
  # Application Load Balancer
  ApplicationLoadBalancer:
    Type: AWS::ElasticLoadBalancingV2::LoadBalancer
    Properties:
      Name: !Sub "${AWS::StackName}-alb"
      Scheme: internet-facing
      SecurityGroups:
        - !Ref AlbSecurityGroup
      Subnets: !Ref PublicSubnets
      Type: application

  AlbSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupName: !Sub "${AWS::StackName}-alb-sg"
      GroupDescription: Security group for ALB
      VpcId: !Ref VpcId
      SecurityGroupIngress:
        # HTTP from anywhere - public-facing ALB requires this
        # For production, use AWS WAF or restrict to known CIDR ranges
        - IpProtocol: tcp
          FromPort: 80
          ToPort: 80
          CidrIp: 0.0.0.0/0
          Description: HTTP for public web traffic
        # HTTPS from anywhere - public-facing ALB requires this
        # For production, use AWS WAF or restrict to known CIDR ranges
        - IpProtocol: tcp
          FromPort: 443
          ToPort: 443
          CidrIp: 0.0.0.0/0
          Description: HTTPS for secure public web traffic

  # Target Groups
  BlueTargetGroup:
    Type: AWS::ElasticLoadBalancingV2::TargetGroup
    Properties:
      Name: !Sub "${AWS::StackName}-blue-tg"
      Port: 80
      Protocol: HTTP
      VpcId: !Ref VpcId
      Matcher:
        HttpCode: 200-499
      HealthCheckPath: /health
      HealthCheckIntervalSeconds: 30
      HealthCheckTimeoutSeconds: 5
      HealthyThresholdCount: 2
      UnhealthyThresholdCount: 3
      TargetType: ip
      IpAddressType: ipv4

  GreenTargetGroup:
    Type: AWS::ElasticLoadBalancingV2::TargetGroup
    Properties:
      Name: !Sub "${AWS::StackName}-green-tg"
      Port: 80
      Protocol: HTTP
      VpcId: !Ref VpcId
      Matcher:
        HttpCode: 200-499
      HealthCheckPath: /health
      HealthCheckIntervalSeconds: 30
      HealthCheckTimeoutSeconds: 5
      HealthyThresholdCount: 2
      UnhealthyThresholdCount: 3
      TargetType: ip
      IpAddressType: ipv4

  # Listener
  AlbListener:
    Type: AWS::ElasticLoadBalancingV2::Listener
    Properties:
      DefaultActions:
        - Type: forward
          ForwardConfig:
            TargetGroupStickinessConfig:
              Enabled: false
              DurationSeconds: 3600
            TargetGroups:
              - TargetGroupArn: !Ref BlueTargetGroup
                Weight: 100
      LoadBalancerArn: !Ref ApplicationLoadBalancer
      Port: 80
      Protocol: HTTP

  # ECS Service
  EcsService:
    Type: AWS::ECS::Service
    DependsOn: AlbListener
    Properties:
      ServiceName: !Sub "${AWS::StackName}-service"
      Cluster: !Ref ECSClusterArn
      TaskDefinition: !Ref TaskDefinitionArn
      DesiredCount: 2
      LaunchType: FARGATE
      DeploymentConfiguration:
        MaximumPercent: 200
        MinimumHealthyPercent: 50
        DeploymentCircuitBreaker:
          Enable: true
          Rollback: true
      NetworkConfiguration:
        AwsvpcConfiguration:
          AssignPublicIp: DISABLED
          SecurityGroups:
            - !Ref EcsSecurityGroup
          Subnets: !Ref PrivateSubnets
      LoadBalancers:
        - ContainerName: web
          ContainerPort: 80
          TargetGroupArn: !Ref BlueTargetGroup
      PropagateTags: SERVICE
      ServiceRegistries:
        - RegistryArn: !GetAtt ServiceDiscoveryService.Arn

  EcsSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupName: !Sub "${AWS::StackName}-ecs-sg"
      GroupDescription: Security group for ECS service
      VpcId: !Ref VpcId
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 80
          ToPort: 80
          SourceSecurityGroupId: !Ref AlbSecurityGroup

  # Service Discovery
  ServiceDiscoveryService:
    Type: AWS::ServiceDiscovery::Service
    Properties:
      Name: web-app
      DnsConfig:
        NamespaceId: !Ref ServiceDiscoveryNamespace
        DnsRecords:
          - Type: A
            TTL: 60
      HealthCheckConfig:
        Type: HTTP
        ResourcePath: /health

  ServiceDiscoveryNamespace:
    Type: AWS::ServiceDiscovery::PrivateDnsNamespace
    Properties:
      Name: !Sub "${Environment}.internal"
      VpcId: !Ref VpcId
```

## Auto Scaling

### Service Auto Scaling

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: ECS service with auto scaling

Resources:
  # Scalable Target
  ScalableTarget:
    Type: AWS::ApplicationAutoScaling::ScalableTarget
    Properties:
      MaxCapacity: 10
      MinCapacity: 2
      ResourceId: !Sub "service/${ECSClusterName}/${ECSServiceName}"
      RoleARN: !Ref AutoScalingRoleArn
      ScalableDimension: ecs:service:DesiredCount
      ServiceNamespace: ecs

  # Scaling Policy - CPU Utilization
  CpuScalingPolicy:
    Type: AWS::ApplicationAutoScaling::ScalingPolicy
    Properties:
      PolicyName: !Sub "${AWS::StackName}-cpu-scaling"
      PolicyType: TargetTrackingScaling
      ScalingTargetId: !Ref ScalableTarget
      TargetTrackingScalingPolicyConfiguration:
        PredefinedMetricSpecification:
          PredefinedMetricType: ECSServiceAverageCPUUtilization
        TargetValue: 70
        ScaleInCooldown: 300
        ScaleOutCooldown: 60

  # Scaling Policy - Memory Utilization
  MemoryScalingPolicy:
    Type: AWS::ApplicationAutoScaling::ScalingPolicy
    Properties:
      PolicyName: !Sub "${AWS::StackName}-memory-scaling"
      PolicyType: TargetTrackingScaling
      ScalingTargetId: !Ref ScalableTarget
      TargetTrackingScalingPolicyConfiguration:
        PredefinedMetricSpecification:
          PredefinedMetricType: ECSServiceAverageMemoryUtilization
        TargetValue: 80
        ScaleInCooldown: 300
        ScaleOutCooldown: 60

  # Step Scaling Policy
  RequestCountScalingPolicy:
    Type: AWS::ApplicationAutoScaling::ScalingPolicy
    Properties:
      PolicyName: !Sub "${AWS::StackName}-request-scaling"
      PolicyType: StepScaling
      ScalingTargetId: !Ref ScalableTarget
      StepScalingPolicyConfiguration:
        AdjustmentType: ChangeInCapacity
        Cooldown: 60
        MetricAggregationType: Average
        StepAdjustments:
          - MetricIntervalLowerBound: 0
            ScalingAdjustment: 1
          - MetricIntervalLowerBound: 1000
            ScalingAdjustment: 2
          - MetricIntervalLowerBound: 5000
            ScalingAdjustment: 4

  # CloudWatch Alarm
  HighCpuAlarm:
    Type: AWS::CloudWatch::Alarm
    Properties:
      AlarmName: !Sub "${AWS::StackName}-high-cpu"
      AlarmDescription: CPU utilization above threshold
      MetricName: CPUUtilization
      Namespace: AWS/ECS
      Dimensions:
        - Name: ClusterName
          Value: !Ref ECSClusterName
        - Name: ServiceName
          Value: !Ref ECSServiceName
      Statistic: Average
      Period: 60
      EvaluationPeriods: 2
      Threshold: 80
      ComparisonOperator: GreaterThanThreshold
      AlarmActions:
        - !Ref RequestCountScalingPolicy

  AutoScalingRoleArn:
    Type: AWS::IAM::Role
    Properties:
      RoleName: !Sub "${AWS::StackName}-autoscaling-role"
      AssumeRolePolicyDocument:
        Version: "2012-10-17"
        Statement:
          - Effect: Allow
            Principal:
              Service: application-autoscaling.amazonaws.com
            Action: sts:AssumeRole
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/service-role/AmazonEC2ContainerServiceAutoscaleRole
```

## Blue/Green Deployments with CodeDeploy

```yaml
AWSTemplateFormatVersion: 2010-09-09
Transform: AWS::CodeDeployBlueGreen

Description: ECS blue/green deployment with CodeDeploy

Parameters:
  Environment:
    Type: String
    Default: production
    AllowedValues:
      - staging
      - production

Resources:
  # ECS Cluster
  ECSCluster:
    Type: AWS::ECS::Cluster
    Properties:
      ClusterName: !Sub "${AWS::StackName}-cluster"

  # Task Definition (Blue)
  TaskDefinitionBlue:
    Type: AWS::ECS::TaskDefinition
    Properties:
      Family: blue-task
      Cpu: "512"
      Memory: "1024"
      NetworkMode: awsvpc
      RequiresCompatibilities:
        - FARGATE
      ContainerDefinitions:
        - Name: web
          Image: !Ref BlueImage
          Cpu: 256
          Memory: 512
          PortMappings:
            - ContainerPort: 80
          LogConfiguration:
            LogDriver: awslogs
            Options:
              awslogs-group: !Ref LogGroup
              awslogs-region: !Ref AWS::Region
              awslogs-stream-prefix: blue

  # Task Definition (Green)
  TaskDefinitionGreen:
    Type: AWS::ECS::TaskDefinition
    Properties:
      Family: green-task
      Cpu: "512"
      Memory: "1024"
      NetworkMode: awsvpc
      RequiresCompatibilities:
        - FARGATE
      ContainerDefinitions:
        - Name: web
          Image: !Ref GreenImage
          Cpu: 256
          Memory: 512
          PortMappings:
            - ContainerPort: 80
          LogConfiguration:
            LogDriver: awslogs
            Options:
              awslogs-group: !Ref LogGroup
              awslogs-region: !Ref AWS::Region
              awslogs-stream-prefix: green

  # Task Set (Blue)
  TaskSetBlue:
    Type: AWS::ECS::TaskSet
    Properties:
      Cluster: !Ref ECSCluster
      Service: !Ref ECSService
      TaskDefinition: !Ref TaskDefinitionBlue
      Scale:
        Unit: PERCENT
        Value: 100

  # Task Set (Green)
  TaskSetGreen:
    Type: AWS::ECS::TaskSet
    Properties:
      Cluster: !Ref ECSCluster
      Service: !Ref ECSService
      TaskDefinition: !Ref TaskDefinitionGreen
      Scale:
        Unit: PERCENT
        Value: 0

  # ECS Service
  ECSService:
    Type: AWS::ECS::Service
    Properties:
      ServiceName: !Sub "${AWS::StackName}-service"
      Cluster: !Ref ECSCluster
      TaskDefinition: !Ref TaskDefinitionBlue
      DesiredCount: 2
      LaunchType: FARGATE
      LoadBalancers:
        - ContainerName: web
          ContainerPort: 80
          TargetGroupArn: !Ref BlueTargetGroup

  # Target Groups
  BlueTargetGroup:
    Type: AWS::ElasticLoadBalancingV2::TargetGroup
    Properties:
      Name: !Sub "${AWS::StackName}-blue-tg"
      Port: 80
      Protocol: HTTP
      VpcId: !Ref VpcId
      HealthCheckPath: /health
      TargetType: ip

  GreenTargetGroup:
    Type: AWS::ElasticLoadBalancingV2::TargetGroup
    Properties:
      Name: !Sub "${AWS::StackName}-green-tg"
      Port: 80
      Protocol: HTTP
      VpcId: !Ref VpcId
      HealthCheckPath: /health
      TargetType: ip

  # Listener
  ProductionListener:
    Type: AWS::ElasticLoadBalancingV2::Listener
    Properties:
      DefaultActions:
        - Type: forward
          TargetGroupArn: !Ref BlueTargetGroup
      LoadBalancerArn: !Ref ApplicationLoadBalancer
      Port: 80
      Protocol: HTTP

  TestListener:
    Type: AWS::ElasticLoadBalancingV2::Listener
    Properties:
      DefaultActions:
        - Type: forward
          TargetGroupArn: !Ref BlueTargetGroup
      LoadBalancerArn: !Ref ApplicationLoadBalancer
      Port: 8080
      Protocol: HTTP

  ApplicationLoadBalancer:
    Type: AWS::ElasticLoadBalancingV2::LoadBalancer
    Properties:
      Name: !Sub "${AWS::StackName}-alb"
      Scheme: internet-facing
      Subnets: !Ref PublicSubnets
      SecurityGroups:
        - !Ref AlbSecurityGroup

  AlbSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupName: !Sub "${AWS::StackName}-alb-sg"
      GroupDescription: ALB security group
      VpcId: !Ref VpcId
      SecurityGroupIngress:
        # HTTP from anywhere - public-facing ALB requires this
        - IpProtocol: tcp
          FromPort: 80
          ToPort: 80
          CidrIp: 0.0.0.0/0
          Description: HTTP for public web traffic
        # Test traffic from internal network only
        - IpProtocol: tcp
          FromPort: 8080
          ToPort: 8080
          CidrIp: 10.0.0.0/16
          Description: Test traffic from internal VPC

  LogGroup:
    Type: AWS::Logs::LogGroup
    Properties:
      LogGroupName: !Sub "/ecs/${AWS::StackName}"
      RetentionInDays: 30

Hooks:
  BlueGreenHook:
    Type: AWS::CodeDeploy::BlueGreen
    Properties:
      TrafficRoutingConfig:
        Type: TimeBasedCanary
        TimeBasedCanary:
          StepPercentage: 15
          BakeTimeMins: 5
      AdditionalOptions:
        TerminationWaitTimeInMinutes: 5
      ServiceRole: !Ref CodeDeployRoleArn
      Applications:
        - Target:
            Type: AWS::ECS::Service
            LogicalID: ECSService
          ECSAttributes:
            TaskDefinitions:
              - TaskDefinitionBlue
              - TaskDefinitionGreen
            TaskSets:
              - TaskSetBlue
              - TaskSetGreen
            TrafficRouting:
              ProdTrafficRoute:
                Type: AWS::ElasticLoadBalancingV2::Listener
                LogicalID: ProductionListener
              TestTrafficRoute:
                Type: AWS::ElasticLoadBalancingV2::Listener
                LogicalID: TestListener
              TargetGroups:
                - BlueTargetGroup
                - GreenTargetGroup

  CodeDeployRoleArn:
    Value: !Sub "arn:aws:iam::${AWS::AccountId}:role/service-role/AmazonCodeDeployRoleForECS"
```

## Conditions and Transforms

### Conditions for Environment-Specific Resources

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: ECS with conditional resources

Parameters:
  Environment:
    Type: String
    Default: dev
    AllowedValues:
      - dev
      - staging
      - production

  EnableServiceDiscovery:
    Type: String
    Default: true
    AllowedValues:
      - true
      - false

  EnableSpotInstances:
    Type: String
    Default: false
    AllowedValues:
      - true
      - false

Conditions:
  IsProduction: !Equals [!Ref Environment, production]
  IsStaging: !Equals [!Ref Environment, staging]
  UseServiceDiscovery: !Equals [!Ref EnableServiceDiscovery, true]
  UseSpotInstances: !And
    - !Equals [!Ref EnableSpotInstances, true]
    - !Not [!Equals [!Ref Environment, production]]

Resources:
  # Always created
  ECSCluster:
    Type: AWS::ECS::Cluster
    Properties:
      ClusterName: !Sub "${AWS::StackName}-${Environment}"

  # Conditionally created service discovery
  ServiceDiscoveryNamespace:
    Type: AWS::ServiceDiscovery::PrivateDnsNamespace
    Condition: UseServiceDiscovery
    Properties:
      Name: !Sub "${Environment}.internal"
      VpcId: !Ref VpcId

  # Conditionally created DLQ
  DeadLetterQueue:
    Type: AWS::SQS::Queue
    Condition: IsProduction
    Properties:
      QueueName: !Sub "${AWS::StackName}-dlq"
```

### Transforms for Code Reuse

```yaml
AWSTemplateFormatVersion: 2010-09-09
Transform: AWS::Serverless-2016-10-31

Description: Using SAM Transform for ECS

Globals:
  Function:
    Timeout: 30
    Runtime: python3.11
    Tracing: Active

Resources:
  TaskFunction:
    Type: AWS::Serverless::Function
    Properties:
      FunctionName: !Sub "${AWS::StackName}-task-processor"
      Handler: task_handler.handler
      Policies:
        - ECSFullAccess
      Events:
        TaskQueue:
          Type: SQS
          Properties:
            Queue: !GetAtt TaskQueue.Arn
            BatchSize: 10

  TaskQueue:
    Type: AWS::SQS::Queue
    Properties:
      QueueName: !Sub "${AWS::StackName}-tasks"
      VisibilityTimeout: 360
```

## CloudFormation Best Practices

### Stack Policies

Stack Policies prevent accidental updates to critical infrastructure resources. Use them to protect ECS clusters, task definitions, and production services from unintended modifications.

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: ECS stack with protective policy

Resources:
  ECSCluster:
    Type: AWS::ECS::Cluster
    Properties:
      ClusterName: !Sub "${AWS::StackName}-cluster"

  EcsService:
    Type: AWS::ECS::Service
    Properties:
      ServiceName: !Sub "${AWS::StackName}-service"
      Cluster: !Ref ECSCluster
      TaskDefinition: !Ref TaskDefinition
      DesiredCount: 2

  TaskDefinition:
    Type: AWS::ECS::TaskDefinition
    Properties:
      Family: web-app-task
      Cpu: "512"
      Memory: "1024"
      NetworkMode: awsvpc
      RequiresCompatibilities:
        - FARGATE
      ContainerDefinitions:
        - Name: web
          Image: !Ref ContainerImage
          Cpu: 256
          Memory: 512
          PortMappings:
            - ContainerPort: 80

# Stack Policy JSON (apply via AWS Console or CLI)
StackPolicy:
  Statement:
    # Allow all updates to task definitions (needed for deployments)
    - Effect: Allow
      Action: Update:Modify
      Resource: "*"

    # Prevent modifications to the ECS cluster
    - Effect: Deny
      Action:
        - Update:Modify
        - Update:Replace
        - Delete
      Resource: "*"
      Condition:
        StringEquals:
          ResourceType:
            - AWS::ECS::Cluster

    # Prevent deletion of the ECS service in production
    - Effect: Deny
      Action: Delete
      Resource: "*"
      Condition:
        StringEquals:
          ResourceType:
            - AWS::ECS::Service
        StringEqualsIfExists:
          Environment: production
```

Apply stack policy using CLI:
```bash
aws cloudformation set-stack-policy \
  --stack-name my-ecs-stack \
  --stack-policy-body file://stack-policy.json
```

### Termination Protection

Enable termination protection to prevent accidental deletion of production stacks. This is critical for ECS infrastructure that handles production workloads.

```bash
# Enable termination protection when creating a stack
aws cloudformation create-stack \
  --stack-name production-ecs \
  --template-body file://ecs-template.yaml \
  --enable-termination-protection

# Enable termination protection on existing stack
aws cloudformation update-termination-protection \
  --stack-name production-ecs \
  --enable-termination-protection

# Disable termination protection (requires explicit confirmation)
aws cloudformation update-termination-protection \
  --stack-name production-ecs \
  --no-enable-termination-protection
```

In templates, add to resources that should be preserved:
```yaml
Resources:
  ProductionECSService:
    Type: AWS::ECS::Service
    DeletionPolicy: Retain
    UpdateReplacePolicy: Retain
    Properties:
      # ... service configuration
```

### Drift Detection

CloudFormation drift detection identifies when infrastructure has been modified outside of CloudFormation. Regular drift checks ensure your ECS infrastructure remains consistent with your templates.

```bash
# Detect drift on a stack
aws cloudformation detect-stack-drift \
  --stack-name my-ecs-stack

# Get drift detection status
aws cloudformation describe-stack-drift-detection-status \
  --stack-drift-detection-id <detection-id>

# Get stack resources with drift status
aws cloudformation describe-stack-resource-drifts \
  --stack-name my-ecs-stack

# Check specific resource drift
aws cloudformation detect-stack-resource-drift \
  --stack-name my-ecs-stack \
  --logical-resource-id EcsService
```

Drift status values:
- **IN_SYNC**: Resource matches template
- **MODIFIED**: Resource has been changed outside CloudFormation
- **DELETED**: Resource exists in template but not in AWS
- **NOT_CHECKED**: Resource not included in drift detection

Automated drift detection schedule:
```yaml
# Use AWS Config rules for continuous drift monitoring
Resources:
  CloudFormationStackDriftDetectionConfigRule:
    Type: AWS::Config::ConfigRule
    Properties:
      ConfigRuleName: cf-drift-detection
      Description: Detect CloudFormation stack drift
      Source:
        Owner: AWS
        SourceIdentifier: CFN_STACK_DRIFT_DETECTION_CHECK
      Scope:
        ComplianceResourceTypes:
          - AWS::CloudFormation::Stack
```

### Change Sets

Change Sets provide a preview of stack changes before execution. Always use change sets for production deployments to review and validate modifications.

```bash
# 1. Create a change set (dry-run)
aws cloudformation create-change-set \
  --stack-name production-ecs \
  --template-body file://ecs-template.yaml \
  --change-set-name production-ecs-changeset \
  --capabilities CAPABILITY_IAM \
  --parameters ParameterKey=Environment,ParameterValue=production

# 2. Wait for change set creation
aws cloudformation wait change-set-create-complete \
  --stack-name production-ecs \
  --change-set-name production-ecs-changeset

# 3. View change set (review changes)
aws cloudformation describe-change-set \
  --stack-name production-ecs \
  --change-set-name production-ecs-changeset \
  --output table

# 4. Execute change set (if changes are correct)
aws cloudformation execute-change-set \
  --stack-name production-ecs \
  --change-set-name production-ecs-changeset

# 5. Delete change set (if not executing)
aws cloudformation delete-change-set \
  --stack-name production-ecs \
  --change-set-name production-ecs-changeset
```

Change Set for nested stacks:
```bash
aws cloudformation create-change-set \
  --stack-name parent-stack \
  --template-body file://parent-template.yaml \
  --change-set-name parent-changeset \
  --nested-stack-resolution TEMPLATE
```

### Change Set Template Review

When reviewing change sets, examine:
1. **Resource modifications**: Changes to ECS services may cause service disruptions
2. **Deletions**: Ensure no critical resources are marked for deletion
3. **IAM changes**: New or modified roles require manual approval
4. **Parameter changes**: Verify parameter overrides are correct
5. **Replace operations**: Resources marked for replacement may cause downtime

## Security Best Practices

### Security

- Use IAM roles with minimum required permissions (Task Execution Role, Task Role)
- Encrypt container images with ECR
- Use Secrets Manager for sensitive data (passwords, API keys)
- Configure security groups with restrictive rules
- Use private subnets for ECS services
- Enable Container Insights for monitoring
- Implement task execution role with specific permissions

### Security Group Best Practices

For public-facing ALBs, HTTP/HTTPS from 0.0.0.0/0 is often necessary. However, enhance security with:

```yaml
AlbSecurityGroup:
  Type: AWS::EC2::SecurityGroup
  Properties:
    GroupName: !Sub "${AWS::StackName}-alb-sg"
    GroupDescription: ALB security group - restrict in production
    VpcId: !Ref VpcId
    SecurityGroupIngress:
      # HTTP from anywhere - required for public ALB
      - IpProtocol: tcp
        FromPort: 80
        ToPort: 80
        CidrIp: 0.0.0.0/0
        Description: HTTP for public web traffic
      # HTTPS from anywhere - required for public ALB
      - IpProtocol: tcp
        FromPort: 443
        ToPort: 443
        CidrIp: 0.0.0.0/0
        Description: HTTPS for secure public web traffic

# Security enhancements for production:
# 1. Use AWS WAF to filter malicious traffic
# 2. Place ALB behind CloudFront for additional protection
# 3. Use AWS Shield for DDoS protection
# 4. Implement rate limiting
# 5. Use AWS Network Firewall for advanced filtering
```

### Performance

- Choose CPU and memory based on container profiling
- Use right-sizing for EC2 instances or Fargate
- Implement auto scaling based on metrics (CPU, Memory, Request count)
- Optimize container startup with appropriate health checks
- Use task placement strategies for optimization
- Consider Spot instances for non-critical workloads

### Monitoring

- Enable Container Insights for detailed metrics
- Configure CloudWatch alarms for CPU, memory, and error rates
- Implement structured logging with awslogs driver
- Use X-Ray for distributed tracing
- Configure task-level monitoring

### Deployment

- Use blue/green deployments with CodeDeploy for production
- Implement deployment circuit breaker
- Use change sets before deployment
- Organize stacks by lifecycle and ownership
- Test task definitions locally before deployment

## Related Resources

- [ECS Documentation](https://docs.aws.amazon.com/ecs/)
- [ECS Task Definitions](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task_definitions.html)
- [ECS Services](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs_services.html)
- [AWS CloudFormation User Guide](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/)
- [ECS Blue/Green Deployments](https://docs.aws.amazon.com/codedeploy/latest/userguide/deployment-steps-ecs.html)
- [CloudFormation Stack Policies](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/protect-stack-resources.html)
- [CloudFormation Drift Detection](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/detect-drift-stack.html)
- [CloudFormation Change Sets](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-changesets.html)

## Additional Files

For complete details on resources and their properties, see:
- [REFERENCE.md](reference.md) - Detailed reference guide for all CloudFormation resources
- [EXAMPLES.md](examples.md) - Complete production-ready examples
