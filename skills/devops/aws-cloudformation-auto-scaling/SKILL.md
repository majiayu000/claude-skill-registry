---
name: aws-cloudformation-auto-scaling
description: AWS CloudFormation patterns for Auto Scaling including EC2, ECS, and Lambda. Use when creating Auto Scaling groups, launch configurations, launch templates, scaling policies, lifecycle hooks, and predictive scaling. Covers template structure with Parameters, Outputs, Mappings, Conditions, cross-stack references, and best practices for high availability and cost optimization.
category: aws
tags: [aws, cloudformation, auto-scaling, ec2, ecs, lambda, infrastructure, iaac, scaling]
version: 1.1.0
allowed-tools: Read, Write, Bash
---

# AWS CloudFormation Auto Scaling

## Overview

Create production-ready Auto Scaling infrastructure using AWS CloudFormation templates. This skill covers Auto Scaling Groups for EC2, ECS, and Lambda, launch configurations, launch templates, scaling policies, lifecycle hooks, and best practices for high availability and cost optimization.

## When to Use

Use this skill when:
- Creating Auto Scaling Groups for EC2 instances
- Configuring Launch Configurations or Launch Templates
- Implementing scaling policies (step, target tracking, simple)
- Adding lifecycle hooks for lifecycle management
- Creating scaling for ECS services
- Implementing Lambda provisioned concurrency scaling
- Organizing templates with Parameters, Outputs, Mappings, Conditions
- Implementing cross-stack references with export/import
- Using mixed instances policies for diversity

## CloudFormation Template Structure

### Base Template with Standard Format

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: Auto Scaling group with load balancer

Metadata:
  AWS::CloudFormation::Interface:
    ParameterGroups:
      - Label:
          default: Auto Scaling Configuration
        Parameters:
          - MinSize
          - MaxSize
          - DesiredCapacity
      - Label:
          default: Instance Configuration
        Parameters:
          - InstanceType
          - AmiId

Parameters:
  MinSize:
    Type: Number
    Default: 2
    Description: Minimum number of instances

  MaxSize:
    Type: Number
    Default: 10
    Description: Maximum number of instances

  DesiredCapacity:
    Type: Number
    Default: 2
    Description: Desired number of instances

  InstanceType:
    Type: String
    Default: t3.micro
    AllowedValues:
      - t3.micro
      - t3.small
      - t3.medium
      - t3.large

  AmiId:
    Type: AWS::EC2::Image::Id
    Description: AMI ID for instances

Mappings:
  EnvironmentConfig:
    dev:
      InstanceType: t3.micro
      MinSize: 1
      MaxSize: 3
    staging:
      InstanceType: t3.medium
      MinSize: 2
      MaxSize: 6
    production:
      InstanceType: t3.large
      MinSize: 3
      MaxSize: 12

Conditions:
  IsProduction: !Equals [!Ref Environment, production]
  UseSpotInstances: !Or [!Equals [!Ref Environment, dev], !Equals [!Ref Environment, staging]]

Resources:
  # Auto Scaling Group
  MyAutoScalingGroup:
    Type: AWS::AutoScaling::AutoScalingGroup
    Properties:
      AutoScalingGroupName: !Sub "${AWS::StackName}-asg"
      MinSize: !Ref MinSize
      MaxSize: !Ref MaxSize
      DesiredCapacity: !Ref DesiredCapacity
      VPCZoneIdentifier: !Ref SubnetIds
      LaunchConfigurationName: !Ref MyLaunchConfiguration
      LoadBalancerNames:
        - !Ref MyLoadBalancer
      HealthCheckType: ELB
      HealthCheckGracePeriod: 300
      TerminationPolicies:
        - OldestInstance
        - Default
      Tags:
        - Key: Environment
          Value: !Ref Environment
          PropagateAtLaunch: true
        - Key: ManagedBy
          Value: CloudFormation
          PropagateAtLaunch: true

Outputs:
  AutoScalingGroupName:
    Description: Name of the Auto Scaling Group
    Value: !Ref MyAutoScalingGroup
```

## Parameters Best Practices

### AWS-Specific Parameter Types

```yaml
Parameters:
  # AWS-specific types for validation
  InstanceType:
    Type: AWS::EC2::Instance::Type
    Description: EC2 instance type

  AmiId:
    Type: AWS::EC2::Image::Id
    Description: AMI ID for instances

  SubnetIds:
    Type: List<AWS::EC2::Subnet::Id>
    Description: Subnets for Auto Scaling group

  SecurityGroupIds:
    Type: List<AWS::EC2::SecurityGroup::Id>
    Description: Security groups for instances

  LoadBalancerArn:
    Type: AWS::ElasticLoadBalancingV2::LoadBalancer::Arn
    Description: Application Load Balancer ARN

  TargetGroupArn:
    Type: AWS::ElasticLoadBalancingV2::TargetGroup::Arn
    Description: Target Group ARN for ALB

  LaunchTemplateId:
    Type: AWS::EC2::LaunchTemplate::LaunchTemplateId
    Description: Launch template ID

  ScalingPolicyArn:
    Type: AWS::AutoScaling::ScalingPolicy::Arn
    Description: Scaling policy ARN
```

### Parameter Constraints

```yaml
Parameters:
  MinSize:
    Type: Number
    Default: 1
    Description: Minimum number of instances
    MinValue: 0
    MaxValue: 1000
    ConstraintDescription: Must be between 0 and 1000

  MaxSize:
    Type: Number
    Default: 10
    Description: Maximum number of instances
    MinValue: 1
    MaxValue: 1000
    ConstraintDescription: Must be between 1 and 1000

  DesiredCapacity:
    Type: Number
    Default: 2
    Description: Desired number of instances
    MinValue: 0
    MaxValue: 1000

  InstanceType:
    Type: String
    Default: t3.micro
    Description: EC2 instance type
    ConstraintDescription: Must be a valid EC2 instance type

  AmiId:
    Type: AWS::EC2::Image::Id
    Description: AMI ID

  EnvironmentName:
    Type: String
    Default: dev
    Description: Deployment environment
    AllowedValues:
      - dev
      - staging
      - production
    ConstraintDescription: Must be dev, staging, or production
```

### SSM Parameter References

```yaml
Parameters:
  LatestAmiId:
    Type: AWS::SSM::Parameter::Value<AWS::EC2::Image::Id>
    Default: /aws/service/ami-amazon-linux-latest/amzn2-ami-hvm-x86_64-gp2
    Description: Latest Amazon Linux 2 AMI from SSM

  InstanceConfiguration:
    Type: AWS::SSM::Parameter::Value<String>
    Default: /myapp/instance-configuration
    Description: Instance configuration from SSM
```

## Outputs and Cross-Stack References

### Export/Import Patterns

```yaml
# Stack A - Network and Auto Scaling Stack
AWSTemplateFormatVersion: 2010-09-09
Description: Auto Scaling infrastructure stack

Resources:
  MyAutoScalingGroup:
    Type: AWS::AutoScaling::AutoScalingGroup
    Properties:
      AutoScalingGroupName: !Sub "${AWS::StackName}-asg"
      MinSize: 2
      MaxSize: 10
      DesiredCapacity: 2
      VPCZoneIdentifier: !Ref SubnetIds
      LaunchConfigurationName: !Ref MyLaunchConfiguration

Outputs:
  AutoScalingGroupName:
    Description: Name of the Auto Scaling Group
    Value: !Ref MyAutoScalingGroup
    Export:
      Name: !Sub "${AWS::StackName}-AutoScalingGroupName"

  AutoScalingGroupArn:
    Description: ARN of the Auto Scaling Group
    Value: !Sub "arn:aws:autoscaling:${AWS::Region}:${AWS::AccountId}:autoScalingGroup:*:autoScalingGroupName/${MyAutoScalingGroup}"
    Export:
      Name: !Sub "${AWS::StackName}-AutoScalingGroupArn"

  LaunchConfigurationName:
    Description: Name of the Launch Configuration
    Value: !Ref MyLaunchConfiguration
    Export:
      Name: !Sub "${AWS::StackName}-LaunchConfigurationName"
```

```yaml
# Stack B - Application Stack (imports from Stack A)
AWSTemplateFormatVersion: 2010-09-09
Description: Application stack using Auto Scaling from infrastructure stack

Parameters:
  InfraStackName:
    Type: String
    Default: infra-stack
    Description: Name of the infrastructure stack

Resources:
  ScalingPolicy:
    Type: AWS::AutoScaling::ScalingPolicy
    Properties:
      PolicyName: !Sub "${AWS::StackName}-scale-up"
      PolicyType: StepScaling
      AdjustmentType: PercentChangeInCapacity
      Cooldown: 300
      StepAdjustments:
        - MetricIntervalLowerBound: 0
          MetricIntervalUpperBound: 10000
          ScalingAdjustment: 200
        - MetricIntervalLowerBound: 10000
          ScalingAdjustment: 400
      AutoScalingGroupName: !ImportValue
        !Sub "${InfraStackName}-AutoScalingGroupName"
```

### Nested Stacks for Modularity

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: Main stack with nested Auto Scaling stacks

Resources:
  # Nested stack for EC2 Auto Scaling
  EC2AutoScalingStack:
    Type: AWS::CloudFormation::Stack
    Properties:
      TemplateURL: https://s3.amazonaws.com/bucket/ec2-asg.yaml
      TimeoutInMinutes: 15
      Parameters:
        Environment: !Ref Environment
        InstanceType: !Ref InstanceType
        MinSize: !Ref MinSize
        MaxSize: !Ref MaxSize

  # Nested stack for scaling policies
  ScalingPoliciesStack:
    Type: AWS::CloudFormation::Stack
    Properties:
      TemplateURL: https://s3.amazonaws.com/bucket/scaling-policies.yaml
      TimeoutInMinutes: 15
      Parameters:
        AutoScalingGroupName: !GetAtt EC2AutoScalingStack.Outputs.AutoScalingGroupName
        Environment: !Ref Environment
```

## Launch Configurations

### Base Launch Configuration

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: Auto Scaling with Launch Configuration

Parameters:
  InstanceType:
    Type: String
    Default: t3.micro

  AmiId:
    Type: AWS::EC2::Image::Id

  KeyName:
    Type: AWS::EC2::KeyPair::KeyName

Resources:
  MyLaunchConfiguration:
    Type: AWS::AutoScaling::LaunchConfiguration
    Properties:
      LaunchConfigurationName: !Sub "${AWS::StackName}-lc"
      ImageId: !Ref AmiId
      InstanceType: !Ref InstanceType
      KeyName: !Ref KeyName
      SecurityGroups:
        - !Ref InstanceSecurityGroup
      InstanceMonitoring: Enabled
      SpotPrice: !If [UseSpot, "0.05", !Ref AWS::NoValue]
      UserData:
        Fn::Base64: |
          #!/bin/bash
          yum update -y
          yum install -y httpd
          systemctl start httpd
          echo "Hello from Auto Scaling" > /var/www/html/index.html

  InstanceSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupName: !Sub "${AWS::StackName}-instance-sg"
      GroupDescription: Security group for instances
      VpcId: !Ref VPCId
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 80
          ToPort: 80
          CidrIp: 0.0.0.0/0
        - IpProtocol: tcp
          FromPort: 22
          ToPort: 22
          CidrIp: 0.0.0.0/0

Conditions:
  UseSpot: !Equals [!Ref UseSpotInstances, true]

Parameters:
  UseSpotInstances:
    Type: String
    Default: false
    AllowedValues:
      - true
      - false
```

## Launch Templates

### Launch Template with Customization

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: Auto Scaling with Launch Template

Parameters:
  InstanceType:
    Type: String
    Default: t3.micro

  AmiId:
    Type: AWS::EC2::Image::Id

Resources:
  MyLaunchTemplate:
    Type: AWS::EC2::LaunchTemplate
    Properties:
      LaunchTemplateName: !Sub "${AWS::StackName}-lt"
      LaunchTemplateData:
        ImageId: !Ref AmiId
        InstanceType: !Ref InstanceType
        Monitoring:
          Enabled: true
        NetworkInterfaces:
          - DeviceIndex: 0
            AssociatePublicIpAddress: false
            Groups:
              - !Ref InstanceSecurityGroup
        TagSpecifications:
          - ResourceType: instance
            Tags:
              - Key: Name
                Value: !Sub "${AWS::StackName}-instance"
              - Key: Environment
                Value: !Ref Environment
        UserData:
          Fn::Base64: |
            #!/bin/bash
            yum update -y
            systemctl enable httpd
            systemctl start httpd

  InstanceSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupName: !Sub "${AWS::StackName}-sg"
      GroupDescription: Security group for instances
      VpcId: !Ref VPCId

  MyAutoScalingGroup:
    Type: AWS::AutoScaling::AutoScalingGroup
    Properties:
      AutoScalingGroupName: !Sub "${AWS::StackName}-asg"
      MinSize: 2
      MaxSize: 10
      DesiredCapacity: 2
      VPCZoneIdentifier: !Ref SubnetIds
      LaunchTemplate:
        LaunchTemplateId: !Ref MyLaunchTemplate
        Version: !GetAtt MyLaunchTemplate.LatestVersionNumber
```

## Auto Scaling Groups

### ASG with Load Balancer

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: Auto Scaling group with Application Load Balancer

Resources:
  MyAutoScalingGroup:
    Type: AWS::AutoScaling::AutoScalingGroup
    Properties:
      AutoScalingGroupName: !Sub "${AWS::StackName}-asg"
      MinSize: 2
      MaxSize: 10
      DesiredCapacity: 2
      VPCZoneIdentifier: !Ref PrivateSubnetIds
      LaunchConfigurationName: !Ref MyLaunchConfiguration
      TargetGroupARNs:
        - !Ref MyTargetGroup
      HealthCheckType: ELB
      HealthCheckGracePeriod: 300
      TerminationPolicies:
        - OldestInstance
        - Default
      InstanceMaintenancePolicy:
        MinHealthyPercentage: 50
        MaxHealthyPercentage: 200
      Tags:
        - Key: Environment
          Value: !Ref Environment
          PropagateAtLaunch: true
        - Key: Name
          Value: !Sub "${AWS::StackName}-instance"
          PropagateAtLaunch: true

  MyTargetGroup:
    Type: AWS::ElasticLoadBalancingV2::TargetGroup
    Properties:
      Name: !Sub "${AWS::StackName}-tg"
      Port: 80
      Protocol: HTTP
      VpcId: !Ref VPCId
      HealthCheckPath: /
      HealthCheckIntervalSeconds: 30
      HealthCheckTimeoutSeconds: 5
      HealthyThresholdCount: 5
      UnhealthyThresholdCount: 2
      TargetType: instance
```

### ASG with Launch Template and Mixed Instances

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: Auto Scaling with Mixed Instances Policy

Resources:
  MyLaunchTemplate:
    Type: AWS::EC2::LaunchTemplate
    Properties:
      LaunchTemplateName: !Sub "${AWS::StackName}-lt"
      LaunchTemplateData:
        ImageId: !Ref AmiId
        InstanceType: t3.micro
        KeyName: !Ref KeyName

  MyAutoScalingGroup:
    Type: AWS::AutoScaling::AutoScalingGroup
    Properties:
      AutoScalingGroupName: !Sub "${AWS::StackName}-asg"
      MinSize: 2
      MaxSize: 10
      DesiredCapacity: 2
      VPCZoneIdentifier: !Ref SubnetIds
      LaunchTemplate:
        LaunchTemplateId: !Ref MyLaunchTemplate
        Version: !GetAtt MyLaunchTemplate.LatestVersionNumber
      MixedInstancesPolicy:
        InstancesDistribution:
          OnDemandAllocationStrategy: prioritized
          OnDemandBaseCapacity: 2
          OnDemandPercentageAboveBaseCapacity: 50
          SpotAllocationStrategy: capacity-optimized
          SpotInstancePools: 3
          SpotMaxPrice: !Ref MaxSpotPrice
        LaunchTemplate:
          LaunchTemplateId: !Ref MyLaunchTemplate
          Overrides:
            - InstanceType: t3.micro
            - InstanceType: t3.small
            - InstanceType: t3.medium
```

### ASG with Lifecycle Hooks

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: Auto Scaling with lifecycle hooks

Resources:
  MyLaunchConfiguration:
    Type: AWS::AutoScaling::LaunchConfiguration
    Properties:
      LaunchConfigurationName: !Sub "${AWS::StackName}-lc"
      ImageId: !Ref AmiId
      InstanceType: t3.micro

  MyAutoScalingGroup:
    Type: AWS::AutoScaling::AutoScalingGroup
    Properties:
      AutoScalingGroupName: !Sub "${AWS::StackName}-asg"
      MinSize: 2
      MaxSize: 10
      DesiredCapacity: 2
      VPCZoneIdentifier: !Ref SubnetIds
      LaunchConfigurationName: !Ref MyLaunchConfiguration

  # Lifecycle Hook - Instance Launch
  LifecycleHookLaunch:
    Type: AWS::AutoScaling::LifecycleHook
    Properties:
      LifecycleHookName: !Sub "${AWS::StackName}-launch-hook"
      AutoScalingGroupName: !Ref MyAutoScalingGroup
      LifecycleTransition: autoscaling:EC2_INSTANCE_LAUNCHING
      HeartbeatTimeout: 900
      NotificationTargetARN: !Ref SnsTopicArn
      RoleARN: !GetAtt LifecycleHookRole.Arn

  # Lifecycle Hook - Instance Termination
  LifecycleHookTermination:
    Type: AWS::AutoScaling::LifecycleHook
    Properties:
      LifecycleHookName: !Sub "${AWS::StackName}-termination-hook"
      AutoScalingGroupName: !Ref MyAutoScalingGroup
      LifecycleTransition: autoscaling:EC2_INSTANCE_TERMINATING
      HeartbeatTimeout: 3600
      NotificationTargetARN: !Ref SnsTopicArn
      RoleARN: !GetAtt LifecycleHookRole.Arn

  # IAM Role for Lifecycle Hooks
  LifecycleHookRole:
    Type: AWS::IAM::Role
    Properties:
      RoleName: !Sub "${AWS::StackName}-lifecycle-role"
      AssumeRolePolicyDocument:
        Version: "2012-10-17"
        Statement:
          - Effect: Allow
            Principal:
              Service: autoscaling.amazonaws.com
            Action: sts:AssumeRole
      Policies:
        - PolicyName: !Sub "${AWS::StackName}-lifecycle-policy"
          PolicyDocument:
            Version: "2012-10-17"
            Statement:
              - Effect: Allow
                Action:
                  - sns:Publish
                Resource: !Ref SnsTopicArn

  SnsTopic:
    Type: AWS::SNS::Topic
    Properties:
      TopicName: !Sub "${AWS::StackName}-lifecycle"
```

## Scaling Policies

### Target Tracking Policy

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: Auto Scaling with Target Tracking scaling policy

Resources:
  MyAutoScalingGroup:
    Type: AWS::AutoScaling::AutoScalingGroup
    Properties:
      AutoScalingGroupName: !Sub "${AWS::StackName}-asg"
      MinSize: 2
      MaxSize: 10
      DesiredCapacity: 2
      VPCZoneIdentifier: !Ref SubnetIds
      LaunchConfigurationName: !Ref MyLaunchConfiguration

  TargetTrackingPolicy:
    Type: AWS::AutoScaling::ScalingPolicy
    Properties:
      PolicyName: !Sub "${AWS::StackName}-target-tracking"
      PolicyType: TargetTrackingScaling
      AutoScalingGroupName: !Ref MyAutoScalingGroup
      TargetTrackingConfiguration:
        PredefinedMetricSpecification:
          PredefinedMetricType: ASGAverageCPUUtilization
        TargetValue: 70
        DisableScaleIn: false
```

### Step Scaling Policy

```yaml
Resources:
  StepScalingPolicy:
    Type: AWS::AutoScaling::ScalingPolicy
    Properties:
      PolicyName: !Sub "${AWS::StackName}-step-scaling"
      PolicyType: StepScaling
      AdjustmentType: PercentChangeInCapacity
      Cooldown: 300
      StepAdjustments:
        - MetricIntervalLowerBound: 0
          MetricIntervalUpperBound: 10000
          ScalingAdjustment: 200
        - MetricIntervalLowerBound: 10000
          MetricIntervalUpperBound: 20000
          ScalingAdjustment: 400
        - MetricIntervalLowerBound: 20000
          ScalingAdjustment: 600
      AutoScalingGroupName: !Ref MyAutoScalingGroup

  # Alarm for Step Scaling
  HighCpuAlarm:
    Type: AWS::CloudWatch::Alarm
    Properties:
      AlarmName: !Sub "${AWS::StackName}-high-cpu"
      AlarmDescription: Alarm when CPU utilization is high
      MetricName: CPUUtilization
      Namespace: AWS/EC2
      Dimensions:
        - Name: AutoScalingGroupName
          Value: !Ref MyAutoScalingGroup
      Statistic: Average
      Period: 60
      EvaluationPeriods: 3
      Threshold: 70
      ComparisonOperator: GreaterThanThreshold
      AlarmActions:
        - !Ref StepScalingPolicy
```

### Simple Scaling Policy

```yaml
Resources:
  SimpleScalingPolicy:
    Type: AWS::AutoScaling::ScalingPolicy
    Properties:
      PolicyName: !Sub "${AWS::StackName}-simple-scale-up"
      PolicyType: SimpleScaling
      AdjustmentType: ChangeInCapacity
      ScalingAdjustment: 1
      Cooldown: 300
      AutoScalingGroupName: !Ref MyAutoScalingGroup

  ScaleDownPolicy:
    Type: AWS::AutoScaling::ScalingPolicy
    Properties:
      PolicyName: !Sub "${AWS::StackName}-simple-scale-down"
      PolicyType: SimpleScaling
      AdjustmentType: ChangeInCapacity
      ScalingAdjustment: -1
      Cooldown: 600
      AutoScalingGroupName: !Ref MyAutoScalingGroup

  HighCpuAlarm:
    Type: AWS::CloudWatch::Alarm
    Properties:
      AlarmName: !Sub "${AWS::StackName}-high-cpu"
      MetricName: CPUUtilization
      Namespace: AWS/EC2
      Dimensions:
        - Name: AutoScalingGroupName
          Value: !Ref MyAutoScalingGroup
      Statistic: Average
      Period: 120
      EvaluationPeriods: 2
      Threshold: 80
      ComparisonOperator: GreaterThanThreshold
      AlarmActions:
        - !Ref SimpleScalingPolicy

  LowCpuAlarm:
    Type: AWS::CloudWatch::Alarm
    Properties:
      AlarmName: !Sub "${AWS::StackName}-low-cpu"
      MetricName: CPUUtilization
      Namespace: AWS/EC2
      Dimensions:
        - Name: AutoScalingGroupName
          Value: !Ref MyAutoScalingGroup
      Statistic: Average
      Period: 300
      EvaluationPeriods: 2
      Threshold: 30
      ComparisonOperator: LessThanThreshold
      AlarmActions:
        - !Ref ScaleDownPolicy
```

### Scheduled Scaling

```yaml
Resources:
  ScheduledScaleUp:
    Type: AWS::AutoScaling::ScheduledAction
    Properties:
      ScheduledActionName: !Sub "${AWS::StackName}-scheduled-scale-up"
      AutoScalingGroupName: !Ref MyAutoScalingGroup
      MinSize: 5
      MaxSize: 15
      DesiredCapacity: 5
      StartTime: "2024-01-01T08:00:00Z"

  ScheduledScaleDown:
    Type: AWS::AutoScaling::ScheduledAction
    Properties:
      ScheduledActionName: !Sub "${AWS::StackName}-scheduled-scale-down"
      AutoScalingGroupName: !Ref MyAutoScalingGroup
      MinSize: 2
      MaxSize: 10
      DesiredCapacity: 2
      StartTime: "2024-01-01T20:00:00Z"

  # Recurring schedule using cron
  RecurringScaleUp:
    Type: AWS::AutoScaling::ScheduledAction
    Properties:
      ScheduledActionName: !Sub "${AWS::StackName}-morning-scale-up"
      AutoScalingGroupName: !Ref MyAutoScalingGroup
      MinSize: 5
      MaxSize: 15
      DesiredCapacity: 5
      Recurrence: "0 8 * * *"
```

## ECS Auto Scaling

### ECS Service Scaling

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: ECS service with Auto Scaling

Resources:
  # ECS Cluster
  EcsCluster:
    Type: AWS::ECS::Cluster
    Properties:
      ClusterName: !Sub "${AWS::StackName}-cluster"

  # Task Definition
  TaskDefinition:
    Type: AWS::ECS::TaskDefinition
    Properties:
      Family: !Sub "${AWS::StackName}-task"
      Cpu: "512"
      Memory: "1024"
      NetworkMode: awsvpc
      RequiresCompatibilities:
        - FARGATE
      ContainerDefinitions:
        - Name: web
          Image: nginx:latest
          PortMappings:
            - ContainerPort: 80
          LogConfiguration:
            LogDriver: awslogs
            Options:
              awslogs-group: !Ref LogGroup
              awslogs-region: !Ref AWS::Region

  # ECS Service
  EcsService:
    Type: AWS::ECS::Service
    Properties:
      ServiceName: !Sub "${AWS::StackName}-service"
      Cluster: !Ref EcsCluster
      TaskDefinition: !Ref TaskDefinition
      DesiredCount: 2
      LaunchType: FARGATE
      NetworkConfiguration:
        AwsvpcConfiguration:
          AssignPublicIp: DISABLED
          SecurityGroups:
            - !Ref ServiceSecurityGroup
          Subnets: !Ref PrivateSubnets
      LoadBalancers:
        - ContainerName: web
          ContainerPort: 80
          TargetGroupArn: !Ref TargetGroup

  # Application Auto Scaling Target
  ScalableTarget:
    Type: AWS::ApplicationAutoScaling::ScalableTarget
    Properties:
      MaxCapacity: 10
      MinCapacity: 2
      ResourceId: !Sub "service/${EcsCluster}/${EcsService.Name}"
      RoleARN: !GetAtt EcsServiceScalingRole.Arn
      ScalableDimension: ecs:service:DesiredCount
      ServiceNamespace: ecs

  # Target Tracking Scaling Policy
  EcsTargetTrackingPolicy:
    Type: AWS::ApplicationAutoScaling::ScalingPolicy
    Properties:
      PolicyName: !Sub "${AWS::StackName}-ecs-target-tracking"
      PolicyType: TargetTrackingScaling
      ScalingTargetId: !Ref ScalableTarget
      TargetTrackingScalingPolicyConfiguration:
        PredefinedMetricSpecification:
          PredefinedMetricType: ECSServiceAverageCPUUtilization
        TargetValue: 70
        ScaleInCooldown: 300
        ScaleOutCooldown: 60

  # Log Group
  LogGroup:
    Type: AWS::Logs::LogGroup
    Properties:
      LogGroupName: !Sub "/ecs/${AWS::StackName}"
      RetentionInDays: 30

  # Security Group
  ServiceSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupName: !Sub "${AWS::StackName}-service-sg"
      GroupDescription: Security group for ECS service
      VpcId: !Ref VPCId

  # Application Load Balancer Target Group
  TargetGroup:
    Type: AWS::ElasticLoadBalancingV2::TargetGroup
    Properties:
      Name: !Sub "${AWS::StackName}-ecs-tg"
      Port: 80
      Protocol: HTTP
      VpcId: !Ref VPCId
      TargetType: ip

  # IAM Role for ECS Service Scaling with Least Privilege
  EcsServiceScalingRole:
    Type: AWS::IAM::Role
    Properties:
      RoleName: !Sub "${AWS::StackName}-ecs-scaling-role"
      AssumeRolePolicyDocument:
        Version: "2012-10-17"
        Statement:
          - Effect: Allow
            Principal:
              Service: application-autoscaling.amazonaws.com
            Action: sts:AssumeRole
      Policies:
        - PolicyName: !Sub "${AWS::StackName}-ecs-scaling-policy"
          PolicyDocument:
            Version: "2012-10-17"
            Statement:
              - Effect: Allow
                Action:
                  - ecs:DescribeServices
                  - ecs:UpdateService
                Resource: !Sub "arn:aws:ecs:${AWS::Region}:${AWS::AccountId}:service/${EcsCluster}/*"
```

## Lambda Provisioned Concurrency Scaling

### Lambda with Provisioned Concurrency Auto Scaling

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: Lambda with Application Auto Scaling for provisioned concurrency

Resources:
  # Lambda Function
  MyLambdaFunction:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: !Sub "${AWS::StackName}-function"
      Runtime: python3.11
      Handler: app.handler
      Code:
        S3Bucket: !Ref CodeBucket
        S3Key: lambda/function.zip
      MemorySize: 512
      Timeout: 30
      Role: !GetAtt LambdaExecutionRole.Arn

  # Lambda Version
  LambdaVersion:
    Type: AWS::Lambda::Version
    Properties:
      FunctionName: !Ref MyLambdaFunction
      Description: Version for provisioned concurrency

  # Application Auto Scaling Scalable Target
  LambdaScalableTarget:
    Type: AWS::ApplicationAutoScaling::ScalableTarget
    Properties:
      MaxCapacity: 20
      MinCapacity: 5
      ResourceId: !Sub "function:${MyLambdaFunction}:${LambdaVersion.Version}"
      RoleARN: !GetAtt LambdaScalingRole.Arn
      ScalableDimension: lambda:function:ProvisionedConcurrency
      ServiceNamespace: lambda

  # Target Tracking Scaling Policy
  LambdaTargetTrackingPolicy:
    Type: AWS::ApplicationAutoScaling::ScalingPolicy
    Properties:
      PolicyName: !Sub "${AWS::StackName}-lambda-target-tracking"
      PolicyType: TargetTrackingScaling
      ScalingTargetId: !Ref LambdaScalableTarget
      TargetTrackingScalingPolicyConfiguration:
        TargetValue: 90
        PredefinedMetricSpecification:
          PredefinedMetricType: LambdaProvisionedConcurrencyUtilization
        ScaleInCooldown: 120
        ScaleOutCooldown: 60

  # Lambda Execution Role
  LambdaExecutionRole:
    Type: AWS::IAM::Role
    Properties:
      RoleName: !Sub "${AWS::StackName}-lambda-role"
      AssumeRolePolicyDocument:
        Version: "2012-10-17"
        Statement:
          - Effect: Allow
            Principal:
              Service: lambda.amazonaws.com
            Action: sts:AssumeRole
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole

  # IAM Role for Lambda Scaling with Least Privilege
  LambdaScalingRole:
    Type: AWS::IAM::Role
    Properties:
      RoleName: !Sub "${AWS::StackName}-lambda-scaling-role"
      AssumeRolePolicyDocument:
        Version: "2012-10-17"
        Statement:
          - Effect: Allow
            Principal:
              Service: application-autoscaling.amazonaws.com
            Action: sts:AssumeRole
      Policies:
        - PolicyName: !Sub "${AWS::StackName}-lambda-scaling-policy"
          PolicyDocument:
            Version: "2012-10-17"
            Statement:
              - Effect: Allow
                Action:
                  - lambda:PutProvisionedConcurrencyConfig
                  - lambda:GetProvisionedConcurrencyConfig
                Resource: !Sub "arn:aws:lambda:${AWS::Region}:${AWS::AccountId}:function:${MyLambdaFunction}:*"
```

## Conditions and Transform

### Conditions for Environment-Specific Scaling

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: Auto Scaling with conditional scaling configuration

Parameters:
  Environment:
    Type: String
    Default: dev
    AllowedValues:
      - dev
      - staging
      - production

Conditions:
  IsProduction: !Equals [!Ref Environment, production]
  IsStaging: !Equals [!Ref Environment, staging]
  UseSpot: !Or [!Equals [!Ref Environment, dev], !Equals [!Ref Environment, staging]]
  UseAlb: !Not [!Equals [!Ref Environment, dev]]
  EnableDetailedMonitoring: !Not [!Equals [!Ref Environment, dev]]

Resources:
  MyLaunchConfiguration:
    Type: AWS::AutoScaling::LaunchConfiguration
    Properties:
      LaunchConfigurationName: !Sub "${AWS::StackName}-lc"
      ImageId: !Ref AmiId
      InstanceType: !If [IsProduction, t3.large, !If [IsStaging, t3.medium, t3.micro]]
      InstanceMonitoring: !If [EnableDetailedMonitoring, Enabled, Basic]

  MyAutoScalingGroup:
    Type: AWS::AutoScaling::AutoScalingGroup
    Properties:
      AutoScalingGroupName: !Sub "${AWS::StackName}-asg"
      MinSize: !If [IsProduction, 3, !If [IsStaging, 2, 1]]
      MaxSize: !If [IsProduction, 12, !If [IsStaging, 6, 3]]
      DesiredCapacity: !If [IsProduction, 3, !If [IsStaging, 2, 1]]
      VPCZoneIdentifier: !Ref SubnetIds
      LaunchConfigurationName: !Ref MyLaunchConfiguration
      HealthCheckType: !If [UseAlb, ELB, EC2]
      HealthCheckGracePeriod: !If [UseAlb, 300, 300]
```

### Transform for Code Reuse

```yaml
AWSTemplateFormatVersion: 2010-09-09
Transform: AWS::Serverless-2016-10-31

Description: Using SAM for simplified Auto Scaling

Globals:
  Function:
    Timeout: 30
    Runtime: python3.11
    Tracing: Active
    Environment:
      Variables:
        LOG_LEVEL: INFO

Parameters:
  Environment:
    Type: String
    Default: dev

Resources:
  # Auto Scaling Group using SAM
  WebServerGroup:
    Type: AWS::Serverless::Application
    Properties:
      Location: ./asg-template.yaml
      Parameters:
        Environment: !Ref Environment
```

## CloudFormation Stack Management Best Practices

### Stack Policies

Stack Policies prevent unintentional updates to critical stack resources. Use them to protect Auto Scaling Groups from accidental modifications or deletions.

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: Stack with policy to protect Auto Scaling resources

Resources:
  MyAutoScalingGroup:
    Type: AWS::AutoScaling::AutoScalingGroup
    Properties:
      AutoScalingGroupName: !Sub "${AWS::StackName}-asg"
      MinSize: 2
      MaxSize: 10
      DesiredCapacity: 2
      VPCZoneIdentifier: !Ref SubnetIds
      LaunchConfigurationName: !Ref MyLaunchConfiguration

  MyLaunchConfiguration:
    Type: AWS::AutoScaling::LaunchConfiguration
    Properties:
      LaunchConfigurationName: !Sub "${AWS::StackName}-lc"
      ImageId: !Ref AmiId
      InstanceType: t3.micro

Metadata:
  AWS::CloudFormation::StackPolicy:
    Statement:
      - Effect: Allow
        Resource: "*"
        Action: Update:Modify
      - Effect: Deny
        Resource: "*"
        Action: Update:Delete
        Condition:
          StringEquals:
            ResourceType:
              - AWS::AutoScaling::AutoScalingGroup
              - AWS::AutoScaling::LaunchConfiguration
```

### Termination Protection

Enable termination protection to prevent accidental deletion of Auto Scaling Groups. This is critical for production environments.

```bash
# Enable termination protection on an existing stack
aws cloudformation update-termination-protection \
  --stack-name my-auto-scaling-stack \
  --enable-termination-protection

# Check if termination protection is enabled
aws cloudformation describe-stacks \
  --stack-name my-auto-scaling-stack \
  --query "Stacks[0].EnableTerminationProtection"
```

### Drift Detection

Detect when your Auto Scaling infrastructure has been modified outside of CloudFormation.

```bash
# Detect drift on a stack
aws cloudformation detect-stack-drift \
  --stack-name my-auto-scaling-stack

# Get drift detection status
aws cloudformation describe-stack-drift-detection-status \
  --stack-name my-auto-scaling-stack

# Get drift detection results
aws cloudformation describe-stack-resource-drifts \
  --stack-name my-auto-scaling-stack

# Check specific resource drift
aws cloudformation describe-stack-resource-drifts \
  --stack-name my-auto-scaling-stack \
  --stack-resource-drifts-not-in-sync
```

### Change Sets

Use Change Sets to preview and review changes before applying them to your Auto Scaling infrastructure.

```bash
# Create a change set
aws cloudformation create-change-set \
  --stack-name my-auto-scaling-stack \
  --change-set-name my-changeset \
  --template-body file://template.yaml \
  --parameters ParameterKey=Environment,ParameterValue=production

# List change sets
aws cloudformation list-change-sets \
  --stack-name my-auto-scaling-stack

# Describe change set
aws cloudformation describe-change-set \
  --stack-name my-auto-scaling-stack \
  --change-set-name my-changeset

# Execute change set
aws cloudformation execute-change-set \
  --stack-name my-auto-scaling-stack \
  --change-set-name my-changeset
```

```yaml
# Automated change set creation in CI/CD pipeline
Resources:
  ChangeSetRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: "2012-10-17"
        Statement:
          - Effect: Allow
            Principal:
              Service: cloudformation.amazonaws.com
            Action: sts:AssumeRole
      Policies:
        - PolicyName: ChangeSetPolicy
          PolicyDocument:
            Version: "2012-10-17"
            Statement:
              - Effect: Allow
                Action:
                  - autoscaling:Describe*
                  - cloudwatch:Describe*
                  - ec2:Describe*
                Resource: "*"
              - Effect: Allow
                Action:
                  - autoscaling:UpdateAutoScalingGroup
                  - autoscaling:CreateOrUpdateTags
                  - cloudwatch:PutMetricAlarm
                  - cloudwatch:DeleteAlarms
                Resource:
                  - !Sub "arn:aws:autoscaling:${AWS::Region}:${AWS::AccountId}:autoScalingGroup:*:autoScalingGroupName/*"
                  - !Sub "arn:aws:cloudwatch:${AWS::Region}:${AWS::AccountId}:alarm:*"
```

## Best Practices

### High Availability

- Distribute instances across multiple AZs
- Use ALB with health checks for automatic routing
- Implement lifecycle hooks for graceful shutdown
- Configure appropriate termination policies
- Use mixed instances policies for diversity

### Cost Optimization

- Use Spot Instances for fault-tolerant workloads
- Implement right-sizing of instances
- Configure aggressive scale-in policies
- Use scheduled scaling for predictable patterns
- Monitor and optimize regularly

### Monitoring

- Create CloudWatch Alarms for key metrics
- Implement scaling policies based on metrics
- Use lifecycle hooks for logging and analytics
- Configure SNS notifications for scaling events
- Implement detailed monitoring for troubleshooting

### Security

- Use IAM roles with minimum permissions
- Encrypt EBS volumes with KMS
- Configure restrictive security groups
- Use VPC with appropriate subnets
- Implement parameter store for sensitive configuration
- Avoid using broad managed policies like `CloudWatchFullAccess`
- Use specific permissions instead of broad managed policies

#### Least Privilege IAM Examples

```yaml
# Instead of CloudWatchFullAccess, use specific permissions
ScalingAlarmRole:
  Type: AWS::IAM::Role
  Properties:
    RoleName: !Sub "${AWS::StackName}-scaling-alarm-role"
    AssumeRolePolicyDocument:
      Version: "2012-10-17"
      Statement:
        - Effect: Allow
          Principal:
            Service: autoscaling.amazonaws.com
          Action: sts:AssumeRole
    Policies:
      - PolicyName: !Sub "${AWS::StackName}-cloudwatch-specific-policy"
        PolicyDocument:
          Version: "2012-10-17"
          Statement:
            - Effect: Allow
              Action:
                - cloudwatch:PutMetricAlarm
                - cloudwatch:DescribeAlarms
                - cloudwatch:DeleteAlarms
                - cloudwatch:EnableAlarmActions
                - cloudwatch:DisableAlarmActions
              Resource: !Sub "arn:aws:cloudwatch:${AWS::Region}:${AWS::AccountId}:alarm:*"
```

## Related Resources

- [Auto Scaling Documentation](https://docs.aws.amazon.com/autoscaling/)
- [AWS CloudFormation User Guide](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/)
- [Auto Scaling Best Practices](https://docs.aws.amazon.com/autoscaling/plans/userguide/auto-scaling-best-practices.html)
- [Application Auto Scaling](https://docs.aws.amazon.com/autoscaling/application/userguide/what-is-application-auto-scaling.html)

## Additional Files

For complete details on resources and their properties, consult:
- [REFERENCE.md](reference.md) - Detailed reference guide for all CloudFormation resources
- [EXAMPLES.md](examples.md) - Complete production-ready examples
