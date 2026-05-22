---
name: aws-cloudformation-ec2
description: AWS CloudFormation patterns for EC2 instances, Security Groups, IAM roles, and load balancers. Use when creating EC2 instances, SPOT instances, Security Groups, IAM roles for EC2, Application Load Balancers (ALB), Target Groups, and implementing template structure with Parameters, Outputs, Mappings, Conditions, and cross-stack references.
category: aws
tags: [aws, cloudformation, ec2, security-group, iam-role, alb, load-balancer, target-group, spot, infrastructure, iaac]
version: 1.0.0
allowed-tools: Read, Write, Bash
---

# AWS CloudFormation EC2 Infrastructure

## Overview

Create production-ready EC2 infrastructure using AWS CloudFormation templates. This skill covers EC2 instances (On-Demand and SPOT), Security Groups, IAM roles and instance profiles, Application Load Balancers (ALB), Target Groups, template structure best practices, parameter patterns, and cross-stack references for modular, reusable infrastructure as code.

## When to Use

Use this skill when:
- Creating new EC2 instances (On-Demand or SPOT)
- Configuring Security Groups for network access control
- Creating IAM roles and instance profiles for EC2
- Setting up Application Load Balancers (ALB) with target groups
- Implementing template Parameters with AWS-specific types
- Creating Outputs for cross-stack references
- Organizing templates with Mappings and Conditions
- Designing reusable, modular CloudFormation templates

## Quick Start

### Basic EC2 Instance with Secure Configuration

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: Simple EC2 instance with secure SSH access

Parameters:
  LatestAmiId:
    Type: AWS::SSM::Parameter::Value<AWS::EC2::Image::Id>
    Default: /aws/service/ami-amazon-linux-latest/amzn2-ami-hvm-x86_64-gp2

  InstanceType:
    Type: String
    Default: t3.micro
    AllowedValues:
      - t3.micro
      - t3.small
      - t3.medium

  KeyName:
    Type: AWS::EC2::KeyPair::KeyName
    Description: SSH key pair name

  SshLocation:
    Type: String
    Description: CIDR block for SSH access
    Default: 10.0.0.0/16
    AllowedPattern: ^([0-9]{1,3}\.){3}[0-9]{1,3}/[0-9]{1,2}$

Resources:
  InstanceSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: Security group for EC2 instance
      VpcId: !Ref VpcId
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 22
          ToPort: 22
          CidrIp: !Ref SshLocation
        - IpProtocol: tcp
          FromPort: 80
          ToPort: 80
          CidrIp: 0.0.0.0/0

  Ec2Instance:
    Type: AWS::EC2::Instance
    Properties:
      ImageId: !Ref LatestAmiId
      InstanceType: !Ref InstanceType
      KeyName: !Ref KeyName
      SecurityGroupIds:
        - !Ref InstanceSecurityGroup
      SubnetId: !Ref SubnetId
      Tags:
        - Key: Name
          Value: !Sub ${AWS::StackName}-instance

Outputs:
  InstanceId:
    Description: EC2 Instance ID
    Value: !Ref Ec2Instance

  PublicIp:
    Description: Public IP address
    Value: !GetAtt Ec2Instance.PublicIp
```

### EC2 Instance with IAM Role

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: EC2 instance with IAM role for S3 access

Resources:
  # IAM Role for EC2 with least privilege permissions
  Ec2Role:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: "2012-10-17"
        Statement:
          - Effect: Allow
            Principal:
              Service: ec2.amazonaws.com
            Action: sts:AssumeRole
      ManagedPolicyArns: []
      Policies:
        - PolicyName: S3WriteAccess
          PolicyDocument:
            Version: "2012-10-17"
            Statement:
              - Effect: Allow
                Action:
                  - s3:PutObject
                  - s3:GetObject
                Resource: !Sub "arn:aws:s3:::${S3BucketName}/*"

  # Instance Profile
  Ec2InstanceProfile:
    Type: AWS::IAM::InstanceProfile
    Properties:
      Roles:
        - !Ref Ec2Role
      InstanceProfileName: !Sub ${AWS::StackName}-profile

  # EC2 Instance
  Ec2Instance:
    Type: AWS::EC2::Instance
    Properties:
      ImageId: !Ref LatestAmiId
      InstanceType: !Ref InstanceType
      IamInstanceProfile: !Ref Ec2InstanceProfile
      # ... other properties
```

## Template Structure

### Template Sections Overview

AWS CloudFormation templates are JSON or YAML files with specific sections. Each section serves a purpose in defining your infrastructure.

```yaml
AWSTemplateFormatVersion: 2010-09-09  # Required - template version
Description: Optional description string  # Optional description

# Section order matters for readability but CloudFormation accepts any order
Mappings: {}       # Static configuration tables
Metadata: {}       # Additional information about resources
Parameters: {}     # Input values for customization
Rules: {}          # Parameter validation rules
Conditions: {}     # Conditional resource creation
Transform: {}      # Macro processing (e.g., AWS::Serverless)
Resources: {}      # AWS resources to create (REQUIRED)
Outputs: {}        # Return values after stack creation
```

### Format Version

The `AWSTemplateFormatVersion` identifies the template version. Current version is `2010-09-09`.

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: My CloudFormation Template
```

### Description

Add a description to document the template's purpose. Must appear after the format version.

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: >
  This template creates an EC2 instance with a security group
  and IAM role for running web applications. It includes:
  - EC2 instance configuration
  - Security group with HTTP/HTTPS access
  - IAM role with S3 access permissions
```

### Metadata

Use `Metadata` for additional information about resources or parameters.

```yaml
Metadata:
  AWS::CloudFormation::Interface:
    ParameterGroups:
      - Label:
          default: EC2 Configuration
        Parameters:
          - InstanceType
          - KeyName
      - Label:
          default: Network Configuration
        Parameters:
          - VpcId
          - SubnetId
    ParameterLabels:
      InstanceType:
        default: EC2 Instance Type
      KeyName:
        default: SSH Key Pair
```

### Resources Section

The `Resources` section is the only required section. It defines AWS resources to provision.

```yaml
Resources:
  MyInstance:
    Type: AWS::EC2::Instance
    Properties:
      ImageId: ami-0ff8a95407f89df2f
      InstanceType: t3.micro
      KeyName: my-key-pair
      Tags:
        - Key: Name
          Value: !Sub ${AWS::StackName}-instance
```

## Parameters

### Parameter Types

Use AWS-specific parameter types for validation and easier selection in the console.

```yaml
Parameters:
  VpcId:
    Type: AWS::EC2::VPC::Id
    Description: Select an existing VPC

  SubnetId:
    Type: AWS::EC2::Subnet::Id
    Description: Select a subnet

  SecurityGroupIds:
    Type: List<AWS::EC2::SecurityGroup::Id>
    Description: Select existing security groups

  InstanceType:
    Type: AWS::EC2::InstanceType
    Description: EC2 instance type
    Default: t3.micro
    AllowedValues:
      - t3.micro
      - t3.small
      - t3.medium
      - t3.large

  AmiId:
    Type: AWS::EC2::Image::Id
    Description: Select an AMI

  KeyName:
    Type: AWS::EC2::KeyPair::KeyName
    Description: Select an existing key pair

  AlbArn:
    Type: AWS::ElasticLoadBalancingV2::LoadBalancer::Arn
    Description: Select an ALB
```

### SSM Parameter Types

Reference Systems Manager parameters for dynamic values.

```yaml
Parameters:
  LatestAmiId:
    Type: AWS::SSM::Parameter::Value<AWS::EC2::Image::Id>
    Description: Latest AMI ID from SSM
    Default: /aws/service/ami-amazon-linux-latest/amzn2-ami-hvm-x86_64-gp2

  LatestAmiIdARM:
    Type: AWS::SSM::Parameter::Value<AWS::EC2::Image::Id>
    Description: Latest ARM AMI ID from SSM
    Default: /aws/service/ami-amazon-linux-latest/amzn2-ami-hvm-arm64-gp2
```

### Parameter Constraints

Add constraints to validate parameter values.

```yaml
Parameters:
  VpcCidr:
    Type: String
    Description: CIDR block for the VPC
    Default: 10.0.0.0/16
    AllowedPattern: ^([0-9]{1,3}\.){3}[0-9]{1,3}/[0-9]{1,2}$
    ConstraintDescription: Must be a valid CIDR block (x.x.x.x/x)

  InstanceCount:
    Type: Number
    Description: Number of instances to launch
    Default: 1
    MinValue: 1
    MaxValue: 10

  Environment:
    Type: String
    Description: Deployment environment
    Default: development
    AllowedValues:
      - development
      - staging
      - production
    ConstraintDescription: Must be development, staging, or production

  VolumeSize:
    Type: Number
    Description: EBS volume size in GB
    Default: 20
    MinValue: 8
    MaxValue: 1000
```

## Mappings

Use `Mappings` for static configuration data based on regions or other factors.

```yaml
Mappings:
  RegionMap:
    us-east-1:
      HVM64: ami-0ff8a95407f89df2f
      HVMG2: ami-0a0c776d80e2a1f3c
    us-west-2:
      HVM64: ami-0a0c776d80e2a1f3c
      HVMG2: ami-0a0c776d80e2a1f3c
    eu-west-1:
      HVM64: ami-0ff8a95407f89df2f
      HVMG2: ami-0a0c776d80e2a1f3c

  EnvironmentConfig:
    development:
      InstanceType: t3.micro
      MinInstances: 1
      MaxInstances: 2
      EnableAutoScaling: false
    staging:
      InstanceType: t3.small
      MinInstances: 1
      MaxInstances: 3
      EnableAutoScaling: false
    production:
      InstanceType: t3.medium
      MinInstances: 2
      MaxInstances: 10
      EnableAutoScaling: true

Resources:
  Instance:
    Type: AWS::EC2::Instance
    Properties:
      ImageId: !FindInMap [RegionMap, !Ref AWS::Region, HVM64]
      InstanceType: !FindInMap [EnvironmentConfig, !Ref Environment, InstanceType]
```

## Conditions

Use `Conditions` to conditionally create resources based on parameters.

```yaml
Parameters:
  DeployAlb:
    Type: String
    Default: true
    AllowedValues:
      - true
      - false

  Environment:
    Type: String
    Default: development
    AllowedValues:
      - development
      - staging
      - production

  UseSpotInstance:
    Type: String
    Default: false
    AllowedValues:
      - true
      - false

Conditions:
  ShouldDeployAlb: !Equals [!Ref DeployAlb, true]
  IsProduction: !Equals [!Ref Environment, production]
  ShouldUseSpot: !Equals [!Ref UseSpotInstance, true]
  IsNotDevelopment: !Not [!Equals [!Ref Environment, development]]

Resources:
  ApplicationLoadBalancer:
    Type: AWS::ElasticLoadBalancingV2::LoadBalancer
    Condition: ShouldDeployAlb
    Properties:
      Scheme: internet-facing
      SecurityGroups:
        - !Ref AlbSecurityGroup
      Subnets: !Ref PublicSubnetIds

  ProductionScalingPolicy:
    Type: AWS::AutoScaling::ScalingPolicy
    Condition: IsProduction
    Properties:
      AutoScalingGroupName: !Ref AutoScalingGroup
      PolicyType: TargetTrackingScaling
      TargetTrackingConfiguration:
        PredefinedMetricSpecification:
          PredefinedMetricType: ASGAverageCPUUtilization
        TargetValue: 70.0
```

## Transform

Use `Transform` for macros like AWS::Serverless for SAM templates.

```yaml
AWSTemplateFormatVersion: 2010-09-09
Transform: AWS::Serverless-2016-10-31
Description: SAM template for serverless application with EC2

Resources:
  MyFunction:
    Type: AWS::Serverless::Function
    Properties:
      Handler: index.handler
      Runtime: nodejs18.x
      CodeUri: function/
```

## Outputs and Cross-Stack References

### Basic Outputs

```yaml
Outputs:
  InstanceId:
    Description: EC2 Instance ID
    Value: !Ref Ec2Instance

  PublicIp:
    Description: Public IP address
    Value: !GetAtt Ec2Instance.PublicIp

  PrivateIp:
    Description: Private IP address
    Value: !GetAtt Ec2Instance.PrivateIp

  AvailabilityZone:
    Description: Availability Zone
    Value: !GetAtt Ec2Instance.AvailabilityZone
```

### Exporting Values for Cross-Stack References

Export values so other stacks can import them.

```yaml
Outputs:
  InstanceId:
    Description: EC2 Instance ID for other stacks
    Value: !Ref Ec2Instance
    Export:
      Name: !Sub ${AWS::StackName}-InstanceId

  SecurityGroupId:
    Description: Security Group ID for other stacks
    Value: !Ref InstanceSecurityGroup
    Export:
      Name: !Sub ${AWS::StackName}-SecurityGroupId

  InstanceRoleArn:
    Description: IAM Role ARN for other stacks
    Value: !GetAtt Ec2Role.Arn
    Export:
      Name: !Sub ${AWS::StackName}-InstanceRoleArn

  TargetGroupArn:
    Description: Target Group ARN for other stacks
    Value: !Ref ApplicationTargetGroup
    Export:
      Name: !Sub ${AWS::StackName}-TargetGroupArn
```

### Importing Values in Another Stack

```yaml
Parameters:
  VpcId:
    Type: AWS::EC2::VPC::Id
    Description: VPC ID from network stack

  SecurityGroupId:
    Type: AWS::EC2::SecurityGroup::Id
    Description: Security Group ID from security stack

  InstanceRoleArn:
    Type: String
    Description: IAM Role ARN from security stack

  # Or use Fn::ImportValue for programmatic access
Resources:
  SecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      VpcId: !ImportValue
        Fn::Sub: ${NetworkStackName}-VpcId
      GroupDescription: Security group for application

  Instance:
    Type: AWS::EC2::Instance
    Properties:
      IamInstanceProfile: !ImportValue
        Fn::Sub: ${SecurityStackName}-InstanceRoleArn
```

### Cross-Stack Reference Pattern

Create a dedicated security stack that exports values:

```yaml
# security-stack.yaml
AWSTemplateFormatVersion: 2010-09-09
Description: Security resources stack

Resources:
  InstanceSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: Security group for EC2 instances
      VpcId: !Ref VpcId
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 80
          ToPort: 80
          CidrIp: 0.0.0.0/0

  Ec2Role:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: "2012-10-17"
        Statement:
          - Effect: Allow
            Principal:
              Service: ec2.amazonaws.com
            Action: sts:AssumeRole

Outputs:
  SecurityGroupId:
    Value: !Ref InstanceSecurityGroup
    Export:
      Name: !Sub ${AWS::StackName}-SecurityGroupId

  InstanceRoleArn:
    Value: !GetAtt Ec2Role.Arn
    Export:
      Name: !Sub ${AWS::StackName}-InstanceRoleArn
```

Application stack imports these values:

```yaml
# application-stack.yaml
AWSTemplateFormatVersion: 2010-09-09
Description: Application stack that imports from security stack

Parameters:
  SecurityStackName:
    Type: String
    Description: Name of the security stack
    Default: security-stack

Resources:
  Ec2Instance:
    Type: AWS::EC2::Instance
    Properties:
      ImageId: !Ref AmiId
      InstanceType: !Ref InstanceType
      SecurityGroupIds:
        - !ImportValue
          Fn::Sub: ${SecurityStackName}-SecurityGroupId
      IamInstanceProfile: !ImportValue
        Fn::Sub: ${SecurityStackName}-InstanceRoleArn
```

## EC2 Instances

### Basic Instance Configuration

```yaml
Resources:
  Ec2Instance:
    Type: AWS::EC2::Instance
    Properties:
      ImageId: !Ref AmiId
      InstanceType: !Ref InstanceType
      KeyName: !Ref KeyName
      SubnetId: !Ref SubnetId
      SecurityGroupIds:
        - !Ref SecurityGroup
      UserData:
        Fn::Base64: |
          #!/bin/bash
          yum update -y
          yum install -y httpd
          systemctl start httpd
      Tags:
        - Key: Name
          Value: !Sub ${AWS::StackName}-instance
        - Key: Environment
          Value: !Ref EnvironmentName
```

### Instance with Multiple Volumes

```yaml
Resources:
  Ec2Instance:
    Type: AWS::EC2::Instance
    Properties:
      ImageId: !Ref AmiId
      InstanceType: !Ref InstanceType
      BlockDeviceMappings:
        - DeviceName: /dev/xvda
          Ebs:
            VolumeSize: 20
            DeleteOnTermination: true
            VolumeType: gp3
        - DeviceName: /dev/xvdh
          Ebs:
            VolumeSize: 50
            DeleteOnTermination: false
            VolumeType: gp3
        - DeviceName: /dev/xvdi
          Ebs:
            VolumeSize: 100
            DeleteOnTermination: false
            VolumeType: st1
```

### Instance with Detailed Monitoring

```yaml
Resources:
  Ec2Instance:
    Type: AWS::EC2::Instance
    Properties:
      ImageId: !Ref AmiId
      InstanceType: !Ref InstanceType
      Monitoring: true
      Metrics:
        CollectionInterval: 60
```

### Instance with Placement

```yaml
Resources:
  Ec2Instance:
    Type: AWS::EC2::Instance
    Properties:
      ImageId: !Ref AmiId
      InstanceType: !Ref InstanceType
      Placement:
        AvailabilityZone: !Select [0, !GetAZs '']
        GroupName: !Ref PlacementGroup
        Tenancy: default
```

## SPOT Instances

### SPOT Fleet

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: SPOT Fleet for cost-optimized instances

Parameters:
  MaxPrice:
    Type: Number
    Default: 0.05
    Description: Maximum price per instance hour

Resources:
  SpotFleet:
    Type: AWS::EC2::SpotFleet
    Properties:
      SpotFleetRequestConfigData:
        TargetCapacity: 10
        IamFleetRole: !GetAtt SpotFleetRole.Arn
        LaunchSpecifications:
          - InstanceType: t3.micro
            ImageId: !Ref AmiId
            SubnetId: !Ref SubnetId
            WeightedCapacity: 1
          - InstanceType: t3.small
            ImageId: !Ref AmiId
            SubnetId: !Ref SubnetId
            WeightedCapacity: 2
        AllocationStrategy: lowestPrice
        SpotPrice: !Sub ${MaxPrice}

  SpotFleetRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: "2012-10-17"
        Statement:
          - Effect: Allow
            Principal:
              Service: spotfleet.amazonaws.com
            Action: sts:AssumeRole
      Policies:
        - PolicyName: SpotFleetPolicy
          PolicyDocument:
            Version: "2012-10-17"
            Statement:
              - Effect: Allow
                Action:
                  - ec2:DescribeInstances
                  - ec2:DescribeImages
                Resource: "*"
```

### SPOT Instance Request

```yaml
Resources:
  SpotRequest:
    Type: AWS::EC2::SpotFleet
    Properties:
      SpotFleetRequestConfigData:
        TargetCapacity: 1
        IamFleetRole: !GetAtt SpotFleetRole.Arn
        LaunchSpecifications:
          - InstanceType: t3.medium
            ImageId: !Ref AmiId
            SubnetId: !Ref SubnetId
            KeyName: !Ref KeyName
        Type: persistent
```

### SPOT Instance with Fallback

```yaml
Resources:
  OnDemandInstance:
    Type: AWS::EC2::Instance
    Condition: IsNotSpot
    Properties:
      ImageId: !Ref AmiId
      InstanceType: !Ref InstanceType

  SpotInstance:
    Type: AWS::EC2::SpotFleet
    Condition: UseSpot
    Properties:
      SpotFleetRequestConfigData:
        TargetCapacity: 1
        IamFleetRole: !GetAtt SpotFleetRole.Arn
        LaunchSpecifications:
          - InstanceType: t3.medium
            ImageId: !Ref AmiId
            SubnetId: !Ref SubnetId
```

## Security Groups

### Basic Security Group

```yaml
Resources:
  WebSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: Security group for web servers
      VpcId: !Ref VpcId
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 80
          ToPort: 80
          CidrIp: 0.0.0.0/0
        - IpProtocol: tcp
          FromPort: 443
          ToPort: 443
          CidrIp: 0.0.0.0/0
        - IpProtocol: tcp
          FromPort: 22
          ToPort: 22
          CidrIp: 10.0.0.0/16
      SecurityGroupEgress:
        - IpProtocol: tcp
          FromPort: 443
          ToPort: 443
          CidrIp: 0.0.0.0/0
      Tags:
        - Key: Name
          Value: !Sub ${AWS::StackName}-web-sg
```

### Security Group with Self Reference

```yaml
Resources:
  AppSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: Security group for application
      VpcId: !Ref VpcId
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 8080
          ToPort: 8080
          SourceSecurityGroupId: !Ref LoadBalancerSecurityGroup
      Tags:
        - Key: Name
          Value: !Sub ${AWS::StackName}-app-sg

  DatabaseSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: Security group for database
      VpcId: !Ref VpcId
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 5432
          ToPort: 5432
          SourceSecurityGroupId: !Ref AppSecurityGroup
      Tags:
        - Key: Name
          Value: !Sub ${AWS::StackName}-db-sg
```

### Security Group for ALB

```yaml
Resources:
  AlbSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: Security group for Application Load Balancer
      VpcId: !Ref VpcId
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 80
          ToPort: 80
          CidrIp: 0.0.0.0/0
        - IpProtocol: tcp
          FromPort: 443
          ToPort: 443
          CidrIp: 0.0.0.0/0
      SecurityGroupEgress:
        - IpProtocol: tcp
          FromPort: 80
          ToPort: 80
          SourceSecurityGroupId: !Ref AppSecurityGroup
        - IpProtocol: tcp
          FromPort: 443
          ToPort: 443
          SourceSecurityGroupId: !Ref AppSecurityGroup
```

## IAM Roles

### EC2 IAM Role with Least Privilege

```yaml
Resources:
  Ec2Role:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: "2012-10-17"
        Statement:
          - Effect: Allow
            Principal:
              Service: ec2.amazonaws.com
            Action: sts:AssumeRole
      ManagedPolicyArns: []
      Policies:
        - PolicyName: S3Access
          PolicyDocument:
            Version: "2012-10-17"
            Statement:
              - Effect: Allow
                Action:
                  - s3:GetObject
                  - s3:PutObject
                  - s3:DeleteObject
                Resource: !Sub "arn:aws:s3:::${S3BucketName}/*"
        - PolicyName: CloudWatchLogs
          PolicyDocument:
            Version: "2012-10-17"
            Statement:
              - Effect: Allow
                Action:
                  - logs:CreateLogGroup
                  - logs:CreateLogStream
                  - logs:PutLogEvents
                  - logs:DescribeLogStreams
                Resource: !Sub "arn:aws:logs:${AWS::Region}:${AWS::AccountId}:log-group:/ec2/${EnvironmentName}/*"

  Ec2InstanceProfile:
    Type: AWS::IAM::InstanceProfile
    Properties:
      Roles:
        - !Ref Ec2Role
      InstanceProfileName: !Sub ${AWS::StackName}-profile
```

### Role for Systems Manager

```yaml
Resources:
  SsmRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: "2012-10-17"
        Statement:
          - Effect: Allow
            Principal:
              Service: ec2.amazonaws.com
            Action: sts:AssumeRole
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore
      Policies:
        - PolicyName: S3ReadAccess
          PolicyDocument:
            Version: "2012-10-17"
            Statement:
              - Effect: Allow
                Action:
                  - s3:GetObject
                Resource: !Sub "arn:aws:s3:::${S3BucketName}/*"
```

## Application Load Balancer (ALB)

### Basic ALB

```yaml
Resources:
  ApplicationLoadBalancer:
    Type: AWS::ElasticLoadBalancingV2::LoadBalancer
    Properties:
      Name: !Sub ${AWS::StackName}-alb
      Scheme: internet-facing
      SecurityGroups:
        - !Ref AlbSecurityGroup
      Subnets:
        - !Ref PublicSubnet1
        - !Ref PublicSubnet2
      Type: application

  ApplicationTargetGroup:
    Type: AWS::ElasticLoadBalancingV2::TargetGroup
    Properties:
      Name: !Sub ${AWS::StackName}-tg
      Port: 80
      Protocol: HTTP
      VpcId: !Ref VpcId
      TargetType: instance
      HealthCheckPath: /health
      HealthCheckIntervalSeconds: 30
      HealthCheckTimeoutSeconds: 5
      HealthyThresholdCount: 2
      UnhealthyThresholdCount: 3
      Tags:
        - Key: Name
          Value: !Sub ${AWS::StackName}-tg

  ApplicationListener:
    Type: AWS::ElasticLoadBalancingV2::Listener
    Properties:
      DefaultActions:
        - Type: forward
          TargetGroupArn: !Ref ApplicationTargetGroup
      LoadBalancerArn: !Ref ApplicationLoadBalancer
      Port: 80
      Protocol: HTTP
```

### ALB with HTTPS

```yaml
Resources:
  ApplicationLoadBalancer:
    Type: AWS::ElasticLoadBalancingV2::LoadBalancer
    Properties:
      Name: !Sub ${AWS::StackName}-alb
      Scheme: internet-facing
      SecurityGroups:
        - !Ref AlbSecurityGroup
      Subnets:
        - !Ref PublicSubnet1
        - !Ref PublicSubnet2

  ApplicationTargetGroup:
    Type: AWS::ElasticLoadBalancingV2::TargetGroup
    Properties:
      Name: !Sub ${AWS::StackName}-tg
      Port: 443
      Protocol: HTTPS
      VpcId: !Ref VpcId
      TargetType: instance
      HealthCheckPath: /health
      HealthCheckProtocol: HTTPS

  ApplicationListener:
    Type: AWS::ElasticLoadBalancingV2::Listener
    Properties:
      DefaultActions:
        - Type: forward
          TargetGroupArn: !Ref ApplicationTargetGroup
      LoadBalancerArn: !Ref ApplicationLoadBalancer
      Port: 443
      Protocol: HTTPS
      Certificates:
        - CertificateArn: !Ref CertificateArn

  ApplicationListenerHttpRedirect:
    Type: AWS::ElasticLoadBalancingV2::Listener
    Properties:
      DefaultActions:
        - Type: redirect
          RedirectConfig:
            Host: "#{host}"
            Path: "/#{path}"
            Port: "443"
            Protocol: "HTTPS"
            Query: "#{query}"
            StatusCode: HTTP_301
      LoadBalancerArn: !Ref ApplicationLoadBalancer
      Port: 80
      Protocol: HTTP
```

### ALB with Multiple Target Groups

```yaml
Resources:
  ApplicationLoadBalancer:
    Type: AWS::ElasticLoadBalancingV2::LoadBalancer
    Properties:
      Name: !Sub ${AWS::StackName}-alb
      Scheme: internet-facing
      SecurityGroups:
        - !Ref AlbSecurityGroup
      Subnets:
        - !Ref PublicSubnet1
        - !Ref PublicSubnet2

  ApiTargetGroup:
    Type: AWS::ElasticLoadBalancingV2::TargetGroup
    Properties:
      Name: !Sub ${AWS::StackName}-api-tg
      Port: 8080
      Protocol: HTTP
      VpcId: !Ref VpcId
      HealthCheckPath: /actuator/health

  WebTargetGroup:
    Type: AWS::ElasticLoadBalancingV2::TargetGroup
    Properties:
      Name: !Sub ${AWS::StackName}-web-tg
      Port: 80
      Protocol: HTTP
      VpcId: !Ref VpcId
      HealthCheckPath: /health

  ApiListenerRule:
    Type: AWS::ElasticLoadBalancingV2::ListenerRule
    Properties:
      Actions:
        - Type: forward
          TargetGroupArn: !Ref ApiTargetGroup
      Conditions:
        - Field: path-pattern
          Values:
            - /api/*
            - /v1/*
      ListenerArn: !Ref ApplicationListener
      Priority: 10

  WebListenerRule:
    Type: AWS::ElasticLoadBalancingV2::ListenerRule
    Properties:
      Actions:
        - Type: forward
          TargetGroupArn: !Ref WebTargetGroup
      Conditions:
        - Field: path-pattern
          Values:
            - /*
      ListenerArn: !Ref ApplicationListener
      Priority: 100
```

### ALB with Cross-Zone Load Balancing

```yaml
Resources:
  ApplicationLoadBalancer:
    Type: AWS::ElasticLoadBalancingV2::LoadBalancer
    Properties:
      Name: !Sub ${AWS::StackName}-alb
      Scheme: internet-facing
      SecurityGroups:
        - !Ref AlbSecurityGroup
      Subnets:
        - !Ref PublicSubnet1
        - !Ref PublicSubnet2
      LoadBalancerAttributes:
        - Key: load_balancing.cross_zone.enabled
          Value: true
```

## Complete Example

### Full EC2 Stack with ALB

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: Complete EC2 stack with ALB, security groups, and IAM role

Parameters:
  EnvironmentName:
    Type: String
    Default: production

  LatestAmiId:
    Type: AWS::SSM::Parameter::Value<AWS::EC2::Image::Id>
    Default: /aws/service/ami-amazon-linux-latest/amzn2-ami-hvm-x86_64-gp2

  InstanceType:
    Type: String
    Default: t3.micro
    AllowedValues:
      - t3.micro
      - t3.small
      - t3.medium
      - t3.large

  VpcCidr:
    Type: String
    Default: 10.0.0.0/16

Resources:
  # VPC
  VPC:
    Type: AWS::EC2::VPC
    Properties:
      CidrBlock: !Ref VpcCidr
      EnableDnsHostnames: true
      EnableDnsSupport: true
      Tags:
        - Key: Name
          Value: !Sub ${EnvironmentName}-vpc
        - Key: Environment
          Value: !Ref EnvironmentName

  # Internet Gateway
  InternetGateway:
    Type: AWS::EC2::InternetGateway
    Properties:
      Tags:
        - Key: Name
          Value: !Sub ${EnvironmentName}-igw
        - Key: Environment
          Value: !Ref EnvironmentName

  InternetGatewayAttachment:
    Type: AWS::EC2::VPCGatewayAttachment
    Properties:
      VpcId: !Ref VPC
      InternetGatewayId: !Ref InternetGateway

  # Public Subnets
  PublicSubnet1:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref VPC
      CidrBlock: 10.0.1.0/24
      AvailabilityZone: !Select [0, !GetAZs '']
      MapPublicIpOnLaunch: true
      Tags:
        - Key: Name
          Value: !Sub ${EnvironmentName}-public-1
        - Key: SubnetType
          Value: Public

  PublicSubnet2:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref VPC
      CidrBlock: 10.0.2.0/24
      AvailabilityZone: !Select [1, !GetAZs '']
      MapPublicIpOnLaunch: true
      Tags:
        - Key: Name
          Value: !Sub ${EnvironmentName}-public-2
        - Key: SubnetType
          Value: Public

  # Security Group for ALB
  AlbSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: Security group for ALB
      VpcId: !Ref VPC
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 80
          ToPort: 80
          CidrIp: 0.0.0.0/0
        - IpProtocol: tcp
          FromPort: 443
          ToPort: 443
          CidrIp: 0.0.0.0/0
      Tags:
        - Key: Name
          Value: !Sub ${EnvironmentName}-alb-sg
        - Key: Environment
          Value: !Ref EnvironmentName

  # Security Group for EC2
  InstanceSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: Security group for EC2 instances
      VpcId: !Ref VPC
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 80
          ToPort: 80
          SourceSecurityGroupId: !Ref AlbSecurityGroup
        - IpProtocol: tcp
          FromPort: 22
          ToPort: 22
          CidrIp: 10.0.0.0/16
      Tags:
        - Key: Name
          Value: !Sub ${EnvironmentName}-instance-sg
        - Key: Environment
          Value: !Ref EnvironmentName

  # IAM Role with specific permissions
  Ec2Role:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: "2012-10-17"
        Statement:
          - Effect: Allow
            Principal:
              Service: ec2.amazonaws.com
            Action: sts:AssumeRole
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore
      Policies:
        - PolicyName: S3Access
          PolicyDocument:
            Version: "2012-10-17"
            Statement:
              - Effect: Allow
                Action:
                  - s3:GetObject
                  - s3:PutObject
                Resource: !Sub "arn:aws:s3:::${S3BucketName}/*"
        - PolicyName: CloudWatchLogs
          PolicyDocument:
            Version: "2012-10-17"
            Statement:
              - Effect: Allow
                Action:
                  - logs:CreateLogGroup
                  - logs:CreateLogStream
                  - logs:PutLogEvents
                Resource: !Sub "arn:aws:logs:${AWS::Region}:${AWS::AccountId}:log-group:/ec2/${EnvironmentName}/*"
      Tags:
        - Key: Name
          Value: !Sub ${EnvironmentName}-ec2-role

  Ec2InstanceProfile:
    Type: AWS::IAM::InstanceProfile
    Properties:
      Roles:
        - !Ref Ec2Role

  # Application Load Balancer
  ApplicationLoadBalancer:
    Type: AWS::ElasticLoadBalancingV2::LoadBalancer
    Properties:
      Name: !Sub ${EnvironmentName}-alb
      Scheme: internet-facing
      SecurityGroups:
        - !Ref AlbSecurityGroup
      Subnets:
        - !Ref PublicSubnet1
        - !Ref PublicSubnet2
      Type: application

  ApplicationTargetGroup:
    Type: AWS::ElasticLoadBalancingV2::TargetGroup
    Properties:
      Name: !Sub ${EnvironmentName}-tg
      Port: 80
      Protocol: HTTP
      VpcId: !Ref VPC
      TargetType: instance
      HealthCheckPath: /health
      HealthCheckIntervalSeconds: 30
      HealthCheckTimeoutSeconds: 5
      HealthyThresholdCount: 2
      UnhealthyThresholdCount: 3
      Tags:
        - Key: Name
          Value: !Sub ${EnvironmentName}-tg

  ApplicationListener:
    Type: AWS::ElasticLoadBalancingV2::Listener
    Properties:
      DefaultActions:
        - Type: forward
          TargetGroupArn: !Ref ApplicationTargetGroup
      LoadBalancerArn: !Ref ApplicationLoadBalancer
      Port: 80
      Protocol: HTTP

  # EC2 Instance
  Ec2Instance:
    Type: AWS::EC2::Instance
    Properties:
      ImageId: !Ref LatestAmiId
      InstanceType: !Ref InstanceType
      IamInstanceProfile: !Ref Ec2InstanceProfile
      SecurityGroupIds:
        - !Ref InstanceSecurityGroup
      SubnetId: !Ref PublicSubnet1
      UserData:
        Fn::Base64: |
          #!/bin/bash
          yum update -y
          yum install -y httpd
          systemctl start httpd
          systemctl enable httpd
          echo "<h1>Hello from $(hostname)</h1>" > /var/www/html/index.html
      Tags:
        - Key: Name
          Value: !Sub ${EnvironmentName}-instance
        - Key: Environment
          Value: !Ref EnvironmentName

Outputs:
  InstanceId:
    Description: EC2 Instance ID
    Value: !Ref Ec2Instance

  InstancePublicIp:
    Description: EC2 Instance Public IP
    Value: !GetAtt Ec2Instance.PublicIp

  LoadBalancerDnsName:
    Description: ALB DNS Name
    Value: !GetAtt ApplicationLoadBalancer.DNSName

  TargetGroupArn:
    Description: Target Group ARN
    Value: !Ref ApplicationTargetGroup

  SecurityGroupId:
    Description: Instance Security Group ID
    Value: !Ref InstanceSecurityGroup

  RoleArn:
    Description: IAM Role ARN
    Value: !GetAtt Ec2Role.Arn
```

## Best Practices

### Use AWS-Specific Parameter Types

Always use AWS-specific parameter types for validation and easier selection.

```yaml
Parameters:
  VpcId:
    Type: AWS::EC2::VPC::Id
    Description: Select a VPC

  SubnetIds:
    Type: List<AWS::EC2::Subnet::Id>
    Description: Select subnets

  SecurityGroupIds:
    Type: List<AWS::EC2::SecurityGroup::Id>
    Description: Select security groups

  InstanceType:
    Type: AWS::EC2::InstanceType
    Description: EC2 instance type

  KeyName:
    Type: AWS::EC2::KeyPair::KeyName
    Description: Select a key pair
```

### Organize by Lifecycle

Separate resources that change at different rates into different stacks.

```yaml
# Network stack - rarely changes
AWSTemplateFormatVersion: 2010-09-09
Description: Network infrastructure (VPC, subnets, routes)
Resources:
  VPC: AWS::EC2::VPC
  Subnets: AWS::EC2::Subnet

# Security stack - changes occasionally
AWSTemplateFormatVersion: 2010-09-09
Description: Security resources (IAM roles, security groups)
Resources:
  SecurityGroups: AWS::EC2::SecurityGroup
  Roles: AWS::IAM::Role

# Application stack - changes frequently
AWSTemplateFormatVersion: 2010-09-09
Description: Application resources (EC2 instances, ALB)
Parameters:
  NetworkStackName:
    Type: String
  SecurityStackName:
    Type: String
Resources:
  Instances: AWS::EC2::Instance
  LoadBalancer: AWS::ElasticLoadBalancingV2::LoadBalancer
```

### Use Meaningful Names

Use `AWS::StackName` and parameters for consistent naming.

```yaml
Resources:
  Ec2Instance:
    Type: AWS::EC2::Instance
    Properties:
      Tags:
        - Key: Name
          Value: !Sub ${AWS::StackName}-instance
        - Key: Environment
          Value: !Ref EnvironmentName
```

### Use Pseudo Parameters

Use pseudo parameters for region-agnostic templates.

```yaml
Resources:
  S3Bucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Sub ${AWS::StackName}-${AWS::AccountId}-${AWS::Region}

  Ec2Instance:
    Type: AWS::EC2::Instance
    Properties:
      Tags:
        - Key: StackName
          Value: !Ref AWS::StackName
        - Key: Region
          Value: !Ref AWS::Region
```

### Validate Before Deployment

```bash
# Validate template
aws cloudformation validate-template --template-body file://template.yaml

# Check for syntax errors
aws cloudformation validate-template \
  --template-body file://template.yaml \
  --query 'Description'

# Use cfn-lint for advanced validation
pip install cfn-lint
cfn-lint template.yaml
```

### Stack Policies

Stack policies protect stack resources from unintended updates that could cause service disruption. Apply policies to prevent accidental modifications or deletions of critical resources.

```yaml
Resources:
  # EC2 instance - allow updates but prevent deletion
  Ec2Instance:
    Type: AWS::EC2::Instance
    DeletionPolicy: Retain
    UpdateReplacePolicy: Retain

  # Database - prevent all updates
  DatabaseInstance:
    Type: AWS::RDS::DBInstance
    DeletionPolicy: Snapshot
    UpdateReplacePolicy: Retain
```

**Stack Policy JSON Example:**

```json
{
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "Update:*",
      "Principal": "*",
      "Resource": "*"
    },
    {
      "Effect": "Deny",
      "Action": ["Update:Delete", "Update:Replace"],
      "Principal": "*",
      "Resource": "LogicalId=Ec2Instance"
    },
    {
      "Effect": "Deny",
      "Action": "Update:*",
      "Principal": "*",
      "Resource": "LogicalId=DatabaseInstance"
    }
  ]
}
```

**Apply Stack Policy:**

```bash
aws cloudformation set-stack-policy \
  --stack-name my-ec2-stack \
  --stack-policy-body file://stack-policy.json

# Or from a file
aws cloudformation set-stack-policy \
  --stack-name my-ec2-stack \
  --stack-policy-url https://s3.amazonaws.com/bucket/policy.json
```

### Termination Protection

Enable termination protection to prevent accidental deletion of production stacks. This is critical for production environments.

```bash
# Enable termination protection when creating a stack
aws cloudformation create-stack \
  --stack-name my-ec2-stack \
  --template-body file://template.yaml \
  --enable-termination-protection

# Enable termination protection on existing stack
aws cloudformation update-termination-protection \
  --stack-name my-ec2-stack \
  --enable-termination-protection

# Disable termination protection (use with caution)
aws cloudformation update-termination-protection \
  --stack-name my-ec2-stack \
  --no-enable-termination-protection

# Check if termination protection is enabled
aws cloudformation describe-stacks \
  --stack-name my-ec2-stack \
  --query 'Stacks[0].EnableTerminationProtection'
```

**Best Practices for Termination Protection:**

- Enable on all production stacks
- Use AWS Organizations SCP to enforce termination protection
- Review before deleting development stacks
- Document the process for emergency termination

### Drift Detection

Drift detection identifies differences between the actual infrastructure and the CloudFormation template. Regular drift checks ensure compliance and security.

```bash
# Detect drift on a stack
aws cloudformation detect-drift \
  --stack-name my-ec2-stack

# Get drift detection status
aws cloudformation describe-stack-drift-detection-status \
  --stack-drift-detection-id abc123

# Get resources that have drifted
aws cloudformation describe-stack-resource-drifts \
  --stack-name my-ec2-stack

# Get detailed drift information for a specific resource
aws cloudformation describe-stack-resource-drifts \
  --stack-name my-ec2-stack \
  --stack-resource-drifts-limit 10
```

**Detect Drift Programmatically:**

```bash
#!/bin/bash
# detect-drift.sh - Automated drift detection script

STACK_NAME=$1
if [ -z "$STACK_NAME" ]; then
    echo "Usage: $0 <stack-name>"
    exit 1
fi

echo "Detecting drift for stack: $STACK_NAME"

# Start drift detection
DETECTION_ID=$(aws cloudformation detect-drift \
  --stack-name $STACK_NAME \
  --query 'StackId' \
  --output text)

echo "Drift detection started: $DETECTION_ID"

# Wait for drift detection to complete
STATUS="DETECTION_IN_PROGRESS"
while [ "$STATUS" = "DETECTION_IN_PROGRESS" ]; do
    sleep 5
    STATUS=$(aws cloudformation describe-stack-drift-detection-status \
      --stack-drift-detection-id $DETECTION_ID \
      --query 'DetectionStatus' \
      --output text)
    echo "Status: $STATUS"
done

# Get drift status
DRIFT_STATUS=$(aws cloudformation describe-stack-drift-detection-status \
  --stack-drift-detection-id $DETECTION_ID \
  --query 'DriftStatus' \
  --output text)

echo "Drift Status: $DRIFT_STATUS"

if [ "$DRIFT_STATUS" = "DRIFTED" ]; then
    echo "Resources with drift:"
    aws cloudformation describe-stack-resource-drifts \
      --stack-name $STACK_NAME \
      --query 'StackResourceDrifts[].{LogicalId:LogicalResourceId,Status:ResourceDriftStatus,Type:ResourceType}'
else
    echo "No drift detected - stack is in sync with template"
fi
```

**Common Drift Scenarios:**

| Drift Type | Description | Action Required |
|------------|-------------|-----------------|
| MODIFIED | Resource properties changed | Review and update template or revert changes |
| DELETED | Resource deleted outside CFN | Recreate via template or import |
| ADDED | Resource created outside CFN | Import to stack or delete manually |

### Change Sets

Change sets preview the impact of stack changes before execution. Always review change sets in production environments.

```bash
# Create a change set
aws cloudformation create-change-set \
  --stack-name my-ec2-stack \
  --change-set-name my-ec2-changeset \
  --template-body file://updated-template.yaml \
  --capabilities CAPABILITY_IAM \
  --change-set-type UPDATE

# List change sets for a stack
aws cloudformation list-change-sets \
  --stack-name my-ec2-stack

# Describe a change set to see the planned changes
aws cloudformation describe-change-set \
  --stack-name my-ec2-stack \
  --change-set-name my-ec2-changeset

# Execute a change set
aws cloudformation execute-change-set \
  --stack-name my-ec2-stack \
  --change-set-name my-ec2-changeset

# Delete a change set if changes are not needed
aws cloudformation delete-change-set \
  --stack-name my-ec2-stack \
  --change-set-name my-ec2-changeset
```

**Change Set Types:**

| Type | Description | Use Case |
|------|-------------|----------|
| UPDATE | Preview changes to existing stack | Modifying existing resources |
| CREATE | Preview new stack creation | Creating new stacks from template |
| IMPORT | Preview resources to import | Importing existing resources |

**Review Change Sets with Filters:**

```bash
# Get changes affecting specific resource types
aws cloudformation describe-change-set \
  --stack-name my-ec2-stack \
  --change-set-name my-ec2-changeset \
  --query 'Changes[?ResourceChange.ResourceType==`AWS::EC2::Instance`]'

# Get changes with replacement impact
aws cloudformation describe-change-set \
  --stack-name my-ec2-stack \
  --change-set-name my-ec2-changeset \
  --query 'Changes[?ResourceChange.Replacement!=`None`]'
```

**Automated Change Set Review Script:**

```bash
#!/bin/bash
# review-changeset.sh - Automated change set review

STACK_NAME=$1
CHANGE_SET_NAME=$2
AUTO_APPROVE=false

while getopts "a" opt; do
  case $opt in
    a) AUTO_APPROVE=true ;;
    *) echo "Usage: $0 [-a] <stack-name> <change-set-name>"
       echo "  -a: Auto-approve if no critical changes"
       exit 1 ;;
  esac
done

echo "Reviewing change set: $CHANGE_SET_NAME"
echo "Stack: $STACK_NAME"
echo ""

# Get change set summary
CHANGES=$(aws cloudformation describe-change-set \
  --stack-name $STACK_NAME \
  --change-set-name $CHANGE_SET_NAME \
  --query 'Changes[*].{Type:Type,Resource:ResourceChange.LogicalResourceId,Action:ResourceChange.Action,Replacement:ResourceChange.Replacement}' \
  --output table)

echo "Planned Changes:"
echo "$CHANGES"
echo ""

# Check for critical changes (replacements or deletions)
CRITICAL_CHANGES=$(aws cloudformation describe-change-set \
  --stack-name $STACK_NAME \
  --change-set-name $CHANGE_SET_NAME \
  --query 'Changes[?ResourceChange.Replacement==`True` || ResourceChange.Action==`Remove`]' \
  --output json)

if [ -n "$CRITICAL_CHANGES" ] && [ "$CRITICAL_CHANGES" != "[]" ]; then
    echo "WARNING: Critical changes detected that require manual review:"
    echo "$CRITICAL_CHANGES"
    echo ""
    echo "Please review manually before executing."
    exit 1
fi

if [ "$AUTO_APPROVE" = true ]; then
    echo "No critical changes - auto-executing change set..."
    aws cloudformation execute-change-set \
      --stack-name $STACK_NAME \
      --change-set-name $CHANGE_SET_NAME
    echo "Change set executed successfully."
else
    echo "Review complete. No critical changes detected."
    echo "To execute: aws cloudformation execute-change-set --stack-name $STACK_NAME --change-set-name $CHANGE_SET_NAME"
fi
```

## Related Resources

- For advanced examples: See [EXAMPLES.md](EXAMPLES.md)
- For reference: See [REFERENCE.md](REFERENCE.md)
- AWS CloudFormation User Guide: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/
- AWS EC2 Documentation: https://docs.aws.amazon.com/ec2/
- AWS ALB Documentation: https://docs.aws.amazon.com/elasticloadbalancing/latest/application/
